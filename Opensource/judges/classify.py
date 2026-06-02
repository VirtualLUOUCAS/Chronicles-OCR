"""字体分类（Classification）打分：exact match。

GT 端不做任何归一化（输入 jsonl 保证字体名属于七体之一）；
Pred 端的解析回退已在 ``prompts/classify.py`` 的 ``extract`` 中处理：
  - 严格前缀命中
  - 部分匹配（"楷书体" → "楷书"）
  - 整段最后一次命中（标记 ``fallback=True``）
因此这里只做严格相等比较。
"""

from __future__ import annotations


def judge(extract: dict, row: dict) -> dict:
    gt = str(row.get("font_type", "") or "").strip()
    pred = str((extract or {}).get("category", "") or "").strip()
    score = 1.0 if (gt and pred and gt == pred) else 0.0
    return {"score": score, "gt": gt, "pred": pred}
