from __future__ import annotations

from typing import Callable

from . import classify, extract_text, referring, spotting

JUDGE_FUNCS: dict[str, Callable[[dict, dict], dict]] = {
    "字体分类": classify.judge,
    "字符提取": extract_text.judge,
    "字符检测": spotting.judge,
    "单字识别": referring.judge,
}
