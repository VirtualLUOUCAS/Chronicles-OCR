"""字体分类（Classification）任务。"""

from __future__ import annotations

from ._text import extract_by_prefix, strip_thinking

VALID_FONT_CATEGORIES = {"甲骨文", "金文", "篆书", "隶书", "楷书", "行书", "草书"}

PROMPT = """你是一名精通中国古文字学与书法史的专家。

任务：
请根据输入的古文字图像，对其中汉字的字体进行分类。

分类范围（仅允许从以下七类中选择一个）：
1. 甲骨文
2. 金文
3. 篆书
4. 隶书
5. 楷书
6. 行书
7. 草书

要求：
- 仔细观察字形结构、笔画特征、线条风格和整体布局
- 只能输出一个最可能的类别
- 不允许输出多个类别或"无法判断"（除非图像极其模糊）
- 不要输出解释（除非额外要求）

输出格式（必须严格遵守）：
字体分类：<类别名称>
"""


def extract(answer: str) -> tuple[bool, dict[str, str | bool]]:
    """三层回退：精确前缀 → 部分匹配（"楷书体"→"楷书"）→ 整段最后一次命中。"""
    text = strip_thinking(answer)
    category = extract_by_prefix(text, ["字体分类", "字体", "分类"])

    data: dict[str, str | bool] = {}
    if category and category in VALID_FONT_CATEGORIES:
        data["category"] = category
        return True, data

    # 部分匹配
    if category:
        for c in VALID_FONT_CATEGORIES:
            if c in category:
                data["category"] = c
                return True, data

    # 回退：扫整段答案，取最后一次出现的合法字体名
    if text:
        last_pos = -1
        last_hit: str | None = None
        for c in VALID_FONT_CATEGORIES:
            pos = text.rfind(c)
            if pos > last_pos:
                last_pos = pos
                last_hit = c
        if last_hit is not None:
            data["category"] = last_hit
            data["fallback"] = True
            return True, data

    return False, data
