"""线程安全的增量结果写入器 + 历史结果读取。

用于 infer / judge 场景：把每条样本以 ``image_path`` 为主键写入同一个 jsonl，
在并发 worker 提交结果时按 ``save_interval`` 周期性落盘，崩溃也不会丢全量进度。
"""

from __future__ import annotations

import json
import os
import traceback
from threading import Lock

from .signal_utils import install_signal_handlers_once


def get_image_path(row: dict) -> str:
    """从一条 row 中取规范化后的图片相对路径（开源 jsonl 唯一字段：image_path）。"""
    for k in ("image_path", "img_path", "image"):
        v = row.get(k)
        if v:
            return v
    return ""


def read_processed(output_file: str, current_tasks: set[str]) -> tuple[dict[str, dict], set[str]]:
    """读历史落盘结果，返回 (image_path -> row, 需要重跑的 image_path 集合)。

    缺任意一个 ``current_tasks`` 中的 task 就视为需要补跑。
    """
    processed: dict[str, dict] = {}
    needs: set[str] = set()
    if not os.path.isfile(output_file):
        return processed, needs
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                key = get_image_path(item)
                if not key:
                    continue
                infer_results = item.get("infer_results") or item.get("judge_results") or {}
                completed = set(infer_results.keys())
                if not current_tasks.issubset(completed):
                    needs.add(key)
                processed[key] = item
    except Exception as e:
        print(f"读取已处理数据时出错: {e}")
    return processed, needs


class ResultWriter:
    """周期性落盘 + 全量替换写入；失败回退到 .tmp 文件。"""

    def __init__(self, output_file: str, processed: dict[str, dict], save_interval: int = 1):
        self.output_file = output_file
        self.processed = processed
        self.lock = Lock()
        self.tmp_file = output_file + ".tmp"
        self.save_interval = save_interval
        self.update_count = 0
        self.last_save_count = 0
        install_signal_handlers_once()

    def update_and_save(self, result: dict, force_save: bool = False) -> None:
        with self.lock:
            key = get_image_path(result)
            if not key:
                return
            self.processed[key] = result
            self.update_count += 1
            if force_save or (self.update_count - self.last_save_count >= self.save_interval):
                self._save_to_disk()
                self.last_save_count = self.update_count

    def _save_to_disk(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.output_file) or ".", exist_ok=True)
            with open(self.tmp_file, "w", encoding="utf-8") as f:
                for data in self.processed.values():
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")
            if os.path.exists(self.output_file):
                os.remove(self.output_file)
            os.rename(self.tmp_file, self.output_file)
        except Exception as e:
            print(f"保存到磁盘时出错: {e}")
            traceback.print_exc()

    def finalize(self) -> None:
        with self.lock:
            try:
                self._save_to_disk()
            except Exception as e:
                print(f"保存最终结果时出错: {e}")
                traceback.print_exc()
            finally:
                if os.path.exists(self.tmp_file):
                    try:
                        os.remove(self.tmp_file)
                    except Exception:
                        pass
