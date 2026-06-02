"""ChronoText benchmark inference entry point.

Usage:
    # 1) Local OpenAI-compatible service started by ``vllm serve`` / sglang / lmdeploy
    python infer.py --api_type openai_compat \
        --model_name Qwen2.5-VL-7B-Instruct \
        --base_url http://127.0.0.1:8000/v1 \
        --api_key EMPTY

    # 2) In-process vLLM, point ``--model_path`` to a local checkpoint
    python infer.py --api_type local_vllm \
        --model_path /path/to/checkpoint \
        --tensor_parallel_size 4

Outputs:
    Opensource/infer_results/<model_tag>/results.jsonl
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import tqdm

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT.parent))

from Opensource.apis import API_TYPES, get_api  # noqa: E402
from Opensource.prompts import (  # noqa: E402
    EXTRACT_FUNCS,
    PROMPTS,
    TASK_CLASSIFY,
    TASK_EXTRACT,
    TASK_REFERRING,
    TASK_SPOTTING,
)
from Opensource.prompts.referring import DEFAULT_SEED, prepare_referring_sample  # noqa: E402
from Opensource.utils.io import ResultWriter, get_image_path, read_processed  # noqa: E402
from Opensource.utils.signal_utils import ABORT_EVENT, install_signal_handlers_once  # noqa: E402

# ============================================================
# 配置
# ============================================================
DEFAULT_DATA_FILE = REPO_ROOT / "data" / "Chronicles_OCR.jsonl"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "infer_results"

# 古代三种字体额外执行 spotting / referring；近代字体只跑 classify / extract
ANCIENT_FONTS = {"甲骨文", "金文", "篆书"}
ALL_TASKS = [TASK_CLASSIFY, TASK_EXTRACT, TASK_SPOTTING, TASK_REFERRING]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ChronoText inference entry point")

    # API 选择
    p.add_argument(
        "--api_type",
        choices=API_TYPES,
        required=True,
        help="local_vllm: 进程内 vllm.LLM; openai_compat: 标准 OpenAI 协议",
    )

    # OpenAI compat 参数
    p.add_argument("--model_name", type=str, default=None, help="openai_compat 调用时使用的 model 字段")
    p.add_argument("--base_url", type=str, default=None, help="openai_compat 服务地址，例如 http://127.0.0.1:8000/v1")
    p.add_argument("--api_key", type=str, default="EMPTY")

    # local_vllm 参数
    p.add_argument("--model_path", type=str, default=None, help="local_vllm: 本地模型权重路径")
    p.add_argument("--tensor_parallel_size", type=int, default=1)
    p.add_argument("--max_model_len", type=int, default=None)
    p.add_argument("--gpu_memory_utilization", type=float, default=0.9)

    # 数据 / 输出
    p.add_argument(
        "--data_file", type=str, default=str(DEFAULT_DATA_FILE), help=f"benchmark jsonl 路径，默认 {DEFAULT_DATA_FILE}"
    )
    p.add_argument("--output_dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument(
        "--output_tag", type=str, default=None, help="结果子目录名，默认从 model_name / model_path / api_name 推断"
    )

    # 推理参数
    p.add_argument("--max_workers", type=int, default=64)
    p.add_argument("--max_try", type=int, default=3)
    p.add_argument("--max_rows", type=int, default=-1)
    p.add_argument("--save_interval", type=int, default=1)
    p.add_argument("--seed", type=int, default=DEFAULT_SEED, help="单字识别红框采样的随机种子")
    p.add_argument("--debug", action="store_true")

    return p.parse_args()


def build_api(args: argparse.Namespace):
    if args.api_type == "openai_compat":
        if not args.model_name or not args.base_url:
            raise ValueError("--api_type openai_compat 需要同时提供 --model_name 与 --base_url")
        return get_api(
            "openai_compat",
            model_name=args.model_name,
            base_url=args.base_url,
            api_key=args.api_key,
            max_try=args.max_try,
        )
    elif args.api_type == "local_vllm":
        if not args.model_path:
            raise ValueError("--api_type local_vllm 需要提供 --model_path")
        return get_api(
            "local_vllm",
            model_path=args.model_path,
            tensor_parallel_size=args.tensor_parallel_size,
            max_model_len=args.max_model_len,
            gpu_memory_utilization=args.gpu_memory_utilization,
            max_try=args.max_try,
        )
    else:
        raise ValueError(f"unsupported api_type: {args.api_type}")


def derive_output_tag(args: argparse.Namespace) -> str:
    if args.output_tag:
        return args.output_tag
    if args.api_type == "openai_compat" and args.model_name:
        return args.model_name
    if args.api_type == "local_vllm" and args.model_path:
        return Path(args.model_path).name
    return "default"


def resolve_image_path(row: dict, data_file_dir: Path) -> str:
    """开源 jsonl 里 ``image_path`` 是相对 data 目录的相对路径，需要拼成绝对路径。"""
    rel = get_image_path(row)
    if not rel:
        return ""
    if os.path.isabs(rel):
        return rel
    return str(data_file_dir / rel)


def tasks_for_row(row: dict) -> list[str]:
    """按 font_type 决定该样本应跑的任务列表（古代 4 / 近代 2）。"""
    if str(row.get("font_type", "")).strip() in ANCIENT_FONTS:
        return ALL_TASKS
    return [TASK_CLASSIFY, TASK_EXTRACT]


def process_one_row(
    api_instance,
    row: dict,
    abs_img_path: str,
    existing: dict,
    max_retries: int,
    referring_cache_dir: str,
    seed: int,
) -> dict | None:
    """对单条样本跑所有未完成的任务。返回新 row（包含合并后的 infer_results）。"""
    if not abs_img_path or not os.path.exists(abs_img_path):
        print(f"警告：图片不存在 {abs_img_path}")
        return None

    file_tasks = tasks_for_row(row)
    pending = [t for t in file_tasks if t not in existing]
    if not pending:
        return None

    infer_results = dict(existing)

    for task_name in pending:
        prompt_text = PROMPTS[task_name]
        task_img = abs_img_path
        referring_meta: dict | None = None

        # 单字识别：先采样 + 画红框，再用渲染图调用模型
        if task_name == TASK_REFERRING:
            sample = prepare_referring_sample(row, abs_img_path, seed=seed, out_dir=referring_cache_dir)
            if sample is None:
                infer_results[task_name] = {
                    "thinking": "",
                    "answer": "",
                    "error": "no_referring_target",
                    "skipped": True,
                }
                continue
            task_img = sample["rendered_img_path"]
            referring_meta = {
                "gt_char": sample["target_char"],
                "target_bbox_xyxy": sample["target_bbox_xyxy"],
                "target_index": sample["index"],
                "sample_key": sample["sample_key"],
                "seed": seed,
                "rendered_img_path": sample["rendered_img_path"],
            }

        last_error = None
        for attempt in range(1, max_retries + 1):
            if task_name == TASK_REFERRING and not os.path.exists(task_img):
                # 渲染图被外部清理掉则就地重画
                redrawn = prepare_referring_sample(row, abs_img_path, seed=seed, out_dir=referring_cache_dir)
                if redrawn is not None:
                    task_img = redrawn["rendered_img_path"]
            try:
                ok, thinking, answer = api_instance(task_img, prompt_text)
                if not ok or answer is None:
                    raise RuntimeError("API 调用失败或返回空结果")

                extract_fn = EXTRACT_FUNCS.get(task_name)
                extract_ok, extracted = (False, None)
                if extract_fn is not None:
                    try:
                        extract_ok, extracted = extract_fn(answer)
                    except Exception as e:
                        print(f"  任务 '{task_name}' 提取异常: {e}")
                        extract_ok = False

                if extract_fn is not None and not extract_ok and attempt < max_retries:
                    print(f"  任务 '{task_name}' 提取失败，重试 {attempt}/{max_retries}")
                    time.sleep(2)
                    continue

                rec = {"thinking": thinking or "", "answer": answer}
                if extract_ok:
                    rec["extract"] = extracted
                if referring_meta is not None:
                    rec.update(
                        {
                            k: referring_meta[k]
                            for k in ("gt_char", "target_bbox_xyxy", "target_index", "sample_key", "seed")
                        }
                    )
                infer_results[task_name] = rec
                break
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries:
                    print(f"  任务 '{task_name}' 失败 ({attempt}/{max_retries}): {last_error}")
                    time.sleep(2)
                else:
                    rec = {"thinking": "", "answer": "", "error": last_error}
                    if referring_meta is not None:
                        rec.update(
                            {
                                k: referring_meta[k]
                                for k in ("gt_char", "target_bbox_xyxy", "target_index", "sample_key", "seed")
                            }
                        )
                    infer_results[task_name] = rec

    result = dict(row)
    result["infer_results"] = infer_results
    result["image_path"] = get_image_path(row)  # 保持相对路径作为主键
    return result


def main() -> None:
    args = parse_args()

    data_file = Path(args.data_file).resolve()
    if not data_file.is_file():
        raise SystemExit(f"benchmark 文件不存在: {data_file}")
    data_dir = data_file.parent

    output_tag = derive_output_tag(args)
    output_dir = Path(args.output_dir).resolve() / output_tag
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "results.jsonl"
    referring_cache_dir = str(output_dir / ".referring_cache")

    print("=" * 72)
    print("ChronoText Inference")
    print("=" * 72)
    print(f"api_type     : {args.api_type}")
    print(f"output_tag   : {output_tag}")
    print(f"data_file    : {data_file}")
    print(f"output_file  : {output_file}")
    print(f"max_workers  : {args.max_workers}")
    print(f"max_rows     : {args.max_rows if args.max_rows > 0 else 'all'}")
    print(f"seed         : {args.seed}")

    # 读 jsonl
    rows: list[dict] = []
    with open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    if args.max_rows > 0:
        rows = rows[: args.max_rows]
    if args.debug:
        rows = rows[: min(5, len(rows))]
    print(f"loaded {len(rows)} rows")

    # API
    print("\n初始化 API...")
    api_instance = build_api(args)
    print("API 就绪")

    # 历史结果（增量）
    all_task_set = set(ALL_TASKS)
    processed, _needs = read_processed(str(output_file), all_task_set)
    print(f"历史结果: 已写入 {len(processed)} 条")

    # 待处理列表
    pending: list[tuple[dict, str, dict]] = []
    fully_done = 0
    for row in rows:
        rel = get_image_path(row)
        if not rel:
            continue
        abs_img = resolve_image_path(row, data_dir)
        existing_infer = processed.get(rel, {}).get("infer_results", {})
        file_tasks = set(tasks_for_row(row))
        if file_tasks.issubset(set(existing_infer.keys())):
            fully_done += 1
            continue
        pending.append((row, abs_img, existing_infer))

    print(f"完全完成: {fully_done}, 待处理: {len(pending)}\n")
    if not pending:
        print("没有需要处理的数据")
        return

    install_signal_handlers_once()
    writer = ResultWriter(str(output_file), processed, save_interval=args.save_interval)

    executor = ThreadPoolExecutor(max_workers=args.max_workers)
    aborted = False
    try:
        futures = {
            executor.submit(
                process_one_row,
                api_instance,
                row,
                abs_img,
                existing,
                args.max_try,
                referring_cache_dir,
                args.seed,
            ): row
            for row, abs_img, existing in pending
        }
        pbar = tqdm.tqdm(total=len(futures), desc="inference")
        for fut in concurrent.futures.as_completed(futures):
            if ABORT_EVENT.is_set():
                aborted = True
                break
            try:
                result = fut.result()
                if result:
                    writer.update_and_save(result)
            except Exception as e:
                print(f"\n处理失败: {e}")
                traceback.print_exc()
            pbar.update(1)
        pbar.close()
        if aborted:
            for f in futures:
                if not f.done():
                    f.cancel()
    finally:
        if ABORT_EVENT.is_set():
            executor.shutdown(wait=False, cancel_futures=True)
        else:
            executor.shutdown(wait=True)

    print("\n落盘最终结果...")
    writer.finalize()
    print(f"✅ 推理完成: {output_file}")
    if ABORT_EVENT.is_set():
        sys.exit(130)


if __name__ == "__main__":
    main()
