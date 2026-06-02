"""字符提取（Parsing）打分：1 − NED (Normalized Edit Distance)。

  score = 1 - Levenshtein(pred, gt) / max(|pred|, |gt|)

双边都先做 ``normalize_for_parsing``（去空白 / 换行 / 标点），再剔除 ``[UNK]`` 占位。
"""

from __future__ import annotations

from ..utils.unk import remove_unk
from ._text import normalize_for_parsing

try:
    from rapidfuzz.distance import Levenshtein as _rf_Levenshtein

    _HAS_RF = True
except ImportError:
    _rf_Levenshtein = None
    _HAS_RF = False


def _levenshtein(s1: str, s2: str) -> int:
    if s1 == s2:
        return 0
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    if _HAS_RF:
        return _rf_Levenshtein.distance(s1, s2)
    # 纯 Python 兜底实现：滚动数组 DP，O(|s1|*|s2|) 时间 / O(|s2|) 空间。
    prev = list(range(len(s2) + 1))
    curr = [0] * (len(s2) + 1)
    for i, c1 in enumerate(s1, start=1):
        curr[0] = i
        for j, c2 in enumerate(s2, start=1):
            curr[j] = prev[j - 1] if c1 == c2 else 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, prev
    return prev[len(s2)]


def judge(extract: dict, row: dict) -> dict:
    gt_raw = normalize_for_parsing(row.get("annotation", "") or "")
    pred_raw = normalize_for_parsing((extract or {}).get("extracted_text", "") or "")
    gt = remove_unk(gt_raw)
    pred = remove_unk(pred_raw)

    len_gt, len_pred = len(gt), len(pred)
    if len_gt == 0 and len_pred == 0:
        return {"score": 1.0, "metric": "1ned", "edit_distance": 0, "len_pred": 0, "len_gt": 0}
    if len_gt == 0:
        return {"score": 0.0, "metric": "1ned", "edit_distance": len_pred, "len_pred": len_pred, "len_gt": 0}

    ed = _levenshtein(pred, gt)
    denom = max(len_pred, len_gt)
    score = max(0.0, 1.0 - ed / denom)
    return {
        "score": score,
        "metric": "1ned",
        "edit_distance": ed,
        "len_pred": len_pred,
        "len_gt": len_gt,
    }
