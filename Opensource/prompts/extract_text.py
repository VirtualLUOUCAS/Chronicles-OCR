"""字符提取（Parsing）任务。"""

from __future__ import annotations

import re

from ._text import clean_value, extract_by_prefix, strip_code_fence, strip_thinking

PROMPT = """你将被提供一张包含汉字字符的图片。请仔细观察图片，并将图片中的所有汉字字符以正确的阅读顺序提取出来。

要求：
- 严格按图片中文字的阅读顺序输出
- 仅输出识别到的字符本身，不要输出任何解释、标点补充或分析

输出格式（必须严格遵守）：
提取文本：<识别到的汉字字符>
"""

_OTHER_PREFIX_RE = re.compile(r"(?:字体分类|字体|分类)\s*[:：]")
_PREAMBLE_LINE_RE = re.compile(
    r"^(?:好的|好|没问题|当然|根据(?:图片|图像)|这是|以下是|图片中(?:的)?(?:内容|文字|字符)?(?:为|是|如下)?|无法(?:识别|看清)|抱歉|对不起)"
)


def _fallback_full_answer(text: str) -> str:
    """模型不按格式输出时，把整段答案当作字符提取结果，但清理"开场白"与"其它任务前缀"。"""
    if not text:
        return ""
    raw = strip_code_fence(text.strip())
    if not raw:
        return ""

    cleaned: list[str] = []
    for ln in raw.splitlines():
        s = ln.strip().strip("`").strip()
        if not s:
            continue
        if _OTHER_PREFIX_RE.match(s):
            continue
        if _PREAMBLE_LINE_RE.match(s):
            continue
        m = _OTHER_PREFIX_RE.search(s)
        if m:
            s = s[: m.start()].rstrip()
            if not s:
                continue
        cleaned.append(s)

    if not cleaned:
        return ""
    candidate = "\n".join(cleaned).strip()
    candidate = clean_value(candidate) or candidate
    if len(candidate) < 2:
        return ""
    return candidate


def extract(answer: str) -> tuple[bool, dict[str, str | bool]]:
    text = strip_thinking(answer)
    extracted = extract_by_prefix(
        text,
        ["提取文本", "提取结果", "识别结果", "识别文本", "文本"],
        merge_trailing_lines=True,
    )
    data: dict[str, str | bool] = {}
    if extracted:
        data["extracted_text"] = extracted
        return True, data

    fb = _fallback_full_answer(text)
    if fb:
        data["extracted_text"] = fb
        data["fallback"] = True
        return True, data

    return False, data
