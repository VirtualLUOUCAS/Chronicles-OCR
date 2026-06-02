"""ChronoText benchmark judging entry point.

Rule-based scoring only — no LLM / API call needed.

Usage:
    # Judge all models under infer_results/
    python judge.py

    # Judge specific models
    python judge.py --models qwen3-vl-8b gemini-3.1-pro

Outputs:
    Opensource/judge_results/<model_tag>/results.jsonl
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import tqdm

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT.parent))

from Opensource.judges import JUDGE_FUNCS  # noqa: E402
from Opensource.utils.io import ResultWriter, get_image_path  # noqa: E402

DEFAULT_DATA_FILE = REPO_ROOT / "data" / "Chronicles_OCR.jsonl"
DEFAULT_INFER_DIR = REPO_ROOT / "infer_results"
DEFAULT_JUDGE_DIR = REPO_ROOT / "judge_results"

ANCIENT_FONTS = {"甲骨文", "金文", "篆书"}
ALL_TASKS = ["字体分类", "字符提取", "字符检测", "单字识别"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ChronoText rule-based judging")
    p.add_argument("--data_file", type=str, default=str(DEFAULT_DATA_FILE), help="benchmark jsonl 路径")
    p.add_argument("--infer_dir", type=str, default=str(DEFAULT_INFER_DIR), help="infer_results 目录")
    p.add_argument("--output_dir", type=str, default=str(DEFAULT_JUDGE_DIR), help="judge_results 目录")
    p.add_argument(
        "--models", type=str, nargs="*", default=None, help="只评分指定模型；不传则扫描 infer_dir 下所有子目录"
    )
    p.add_argument("--max_workers", type=int, default=64)
    p.add_argument("--save_interval", type=int, default=1000)
    return p.parse_args()


def load_gt_index(data_file: Path) -> dict[str, dict]:
    """加载 GT jsonl，按 image_path 建索引。"""
    index: dict[str, dict] = {}
    with open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            key = get_image_path(row)
            if key:
                index[key] = row
    return index


def tasks_for_row(gt_row: dict) -> list[str]:
    if str(gt_row.get("font_type", "")).strip() in ANCIENT_FONTS:
        return ALL_TASKS
    return ["字体分类", "字符提取"]


def judge_one_row(infer_row: dict, gt_row: dict) -> dict:
    """对单条 infer 结果按对应 GT 评分。"""
    file_tasks = tasks_for_row(gt_row)

    # 把 GT 字段并入打分上下文
    judge_ctx = dict(gt_row)
    judge_ctx["infer_results"] = infer_row.get("infer_results") or {}

    judge_results: dict = {}
    for task in file_tasks:
        infer_task = (infer_row.get("infer_results") or {}).get(task)
        if not isinstance(infer_task, dict):
            judge_results[task] = {"score": {"score": 0.0}, "error": "no_infer"}
            continue
        extract = infer_task.get("extract")
        if extract is None:
            judge_results[task] = {"score": {"score": 0.0}, "error": "no_extract"}
            continue
        try:
            score = JUDGE_FUNCS[task](extract, judge_ctx)
            judge_results[task] = {"score": score}
        except Exception as e:
            print(f"  任务 '{task}' 评分异常: {e}")
            judge_results[task] = {"score": 0.0, "error": str(e)}

    out = dict(infer_row)
    out["judge_results"] = judge_results
    out["font_type"] = gt_row.get("font_type", out.get("font_type", ""))
    out["annotation"] = gt_row.get("annotation", out.get("annotation", ""))
    return out


def judge_one_model(
    model_tag: str,
    infer_file: Path,
    output_file: Path,
    gt_index: dict[str, dict],
    max_workers: int,
    save_interval: int,
) -> tuple[int, int, int]:
    """对单个模型的 infer 结果跑评分。返回 (total, judged, missing_in_gt)。"""
    infer_rows: list[dict] = []
    with open(infer_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            infer_rows.append(json.loads(line))

    output_file.parent.mkdir(parents=True, exist_ok=True)
    # 默认覆盖：不读历史 judge 结果
    writer = ResultWriter(str(output_file), processed={}, save_interval=save_interval)

    pairs: list[tuple[dict, dict]] = []
    missing = 0
    for r in infer_rows:
        key = get_image_path(r)
        gt = gt_index.get(key)
        if gt is None:
            missing += 1
            continue
        pairs.append((r, gt))

    if not pairs:
        print(f"  [{model_tag}] 无可评分样本")
        writer.finalize()
        return len(infer_rows), 0, missing

    judged = 0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(judge_one_row, ir, gt): ir for ir, gt in pairs}
        pbar = tqdm.tqdm(total=len(futures), desc=f"judge[{model_tag}]")
        for fut in concurrent.futures.as_completed(futures):
            try:
                result = fut.result()
                writer.update_and_save(result)
                judged += 1
            except Exception as e:
                print(f"\n评分失败: {e}")
                traceback.print_exc()
            pbar.update(1)
        pbar.close()
    writer.finalize()
    return len(infer_rows), judged, missing


def main() -> None:
    args = parse_args()

    data_file = Path(args.data_file).resolve()
    if not data_file.is_file():
        raise SystemExit(f"benchmark 文件不存在: {data_file}")

    infer_dir = Path(args.infer_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not infer_dir.is_dir():
        raise SystemExit(f"infer 目录不存在: {infer_dir}")

    print("=" * 72)
    print("ChronoText Judging")
    print("=" * 72)
    print(f"data_file  : {data_file}")
    print(f"infer_dir  : {infer_dir}")
    print(f"output_dir : {output_dir}")

    # 加载 GT
    gt_index = load_gt_index(data_file)
    print(f"GT 样本数  : {len(gt_index)}")

    # 模型清单
    if args.models:
        model_tags = args.models
    else:
        model_tags = sorted(d.name for d in infer_dir.iterdir() if d.is_dir() and not d.name.startswith("."))
    print(f"模型数量   : {len(model_tags)} -> {model_tags}\n")

    summary: list[tuple[str, int, int, int]] = []
    for tag in model_tags:
        infer_file = infer_dir / tag / "results.jsonl"
        if not infer_file.is_file():
            print(f"[{tag}] 跳过：找不到 {infer_file}")
            continue
        output_file = output_dir / tag / "results.jsonl"
        total, judged, missing = judge_one_model(
            tag,
            infer_file,
            output_file,
            gt_index,
            max_workers=args.max_workers,
            save_interval=args.save_interval,
        )
        summary.append((tag, total, judged, missing))
        print(f"[{tag}] total={total}, judged={judged}, missing_in_gt={missing}")

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)
    for tag, total, judged, missing in summary:
        print(f"  {tag:40s}  total={total:6d}  judged={judged:6d}  missing={missing:6d}")
    print(f"\n✅ judge 全部完成，结果在 {output_dir}")


if __name__ == "__main__":
    main()
