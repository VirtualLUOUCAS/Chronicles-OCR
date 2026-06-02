"""字符检测（Detection / End-to-End Spotting）任务。

模型输出 JSON 数组，bbox 归一化到 0-1000，char 是该 bbox 对应的现代汉字。
"""

from __future__ import annotations

import json
import re

from ._text import strip_thinking

PROMPT = """你是一名古文字图像检测与识别专家。

任务：
请检测输入图像中所有可见的古文单字符，并为每个单字符同时给出边界框 bbox 和该字符本身。

检测对象：
- 每个独立古文字符作为一个目标
- 不要检测标点、背景纹理、裂纹、装饰线、器物边缘或非文字区域
- 如果一个字符残缺但仍可辨认为字符，也应检测
- 如果多个笔画明显属于同一个字符，只输出一个 bbox

坐标要求：
- bbox 格式为 [x1, y1, x2, y2]
- x1, y1 表示左上角坐标
- x2, y2 表示右下角坐标
- 所有坐标必须基于整张输入图像归一化到 0–1000 的整数范围
- x1 < x2，y1 < y2
- 不要输出小数

字符要求：
- char 字段填写该 bbox 区域对应的字符本身（使用现代汉字写出）
- 每个 bbox 只对应一个字符
- 如果字符无法识别，可以使用 "[UNK]" 代替，但仍需要输出该字符的 bbox

排序要求：
- 按从上到下、从左到右的顺序排输出
- idx 从 1 开始连续编号

输出要求：
- 只输出合法 JSON
- 不要输出解释、Markdown、代码块或多余文字

JSON 输出格式：
[
  {"idx": 1, "bbox": [x1, y1, x2, y2], "char": "<该bbox对应的字符>"},
  {"idx": 2, "bbox": [x1, y1, x2, y2], "char": "<该bbox对应的字符>"}
]
"""


def _strip_json_fence(text: str) -> str:
    if not text:
        return ""
    s = text.strip()
    m = re.match(r"^```(?:json|JSON)?\s*\n?(.*?)\n?```\s*$", s, flags=re.DOTALL)
    return m.group(1).strip() if m else s


def extract(answer: str) -> tuple[bool, dict]:
    data: dict = {"items": []}
    if not answer:
        return False, data

    s = _strip_json_fence(strip_thinking(answer))

    parsed = None
    try:
        parsed = json.loads(s)
    except Exception:
        parsed = None

    if parsed is None:
        lb, rb = s.find("["), s.rfind("]")
        if lb != -1 and rb != -1 and rb > lb:
            try:
                parsed = json.loads(s[lb : rb + 1])
            except Exception:
                parsed = None

    if parsed is None:
        for m in re.finditer(r"\[[\s\S]*?\]", s):
            try:
                cand = json.loads(m.group(0))
                if isinstance(cand, list):
                    parsed = cand
                    break
            except Exception:
                continue

    if parsed is None or not isinstance(parsed, list):
        return False, data

    items: list[dict] = []
    valid_all = True
    for i, it in enumerate(parsed, start=1):
        if not isinstance(it, dict):
            valid_all = False
            continue
        bbox = it.get("bbox")
        if not isinstance(bbox, list) or len(bbox) != 4 or not all(isinstance(v, (int, float)) for v in bbox):
            valid_all = False
            continue
        x1, y1, x2, y2 = [int(round(float(v))) for v in bbox]
        x1 = max(0, min(1000, x1))
        y1 = max(0, min(1000, y1))
        x2 = max(0, min(1000, x2))
        y2 = max(0, min(1000, y2))
        if not (x1 < x2 and y1 < y2):
            valid_all = False
            continue

        char = it.get("char", "")
        if not isinstance(char, str):
            char = str(char) if char is not None else ""
        char = char.strip()

        idx = it.get("idx", i)
        items.append(
            {
                "idx": int(idx) if isinstance(idx, (int, float)) else i,
                "bbox": [x1, y1, x2, y2],
                "char": char,
            }
        )

    data["items"] = items
    if len(parsed) == 0:
        return True, data
    if not items:
        return False, data
    return valid_all, data
