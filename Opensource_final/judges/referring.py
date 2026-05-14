"""单字识别（Recognition）打分：Exact Match Accuracy。

GT 来自 infer 阶段写入 ``infer_results["单字识别"]["gt_char"]``。
"""

from __future__ import annotations


def _norm(s: str) -> str:
    return (s or "").strip().strip("。.；;，,\"'“”‘’《》<>()（）【】[]{}!?！？:：`·～~")


def judge(extract: dict, row: dict) -> dict:
    pred = str((extract or {}).get("char", "") or "").strip()
    infer_results = row.get("infer_results") or {}
    task_rec = infer_results.get("单字识别") or {}
    gt = str(task_rec.get("gt_char", "") or "").strip()
    if not gt:
        return {"score": 0.0, "metric": "exact_match", "gt": "", "pred": pred, "error": "no_gt"}
    score = 1.0 if _norm(pred) == _norm(gt) else 0.0
    return {"score": score, "metric": "exact_match", "gt": gt, "pred": pred}
