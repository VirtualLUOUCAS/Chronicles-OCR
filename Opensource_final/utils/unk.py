"""UNK 占位符的统一定义与处理。

数据集与模型预测里 "无法辨识的字符" 有多种写法，全部归一化到 ``[UNK]``：
  1. token 形态：``[UNK]`` / ``<UNK>`` / 裸 ``UNK``（不区分大小写）
  2. 方块占位 ：``□ ■ ▢ ◻ ◼``

注意：全角/半角问号属于标点，不在本模块的处理范围内（由打分时的标点剥离统一处理）。
"""

from __future__ import annotations

import re

UNK_CANONICAL = "[UNK]"

UNK_BLOCK_CHARS: frozenset[str] = frozenset(
    {
        "\u25a1",  # □
        "\u25a0",  # ■
        "\u25a2",  # ▢
        "\u25fb",  # ◻
        "\u25fc",  # ◼
    }
)

UNK_TOKEN_FORMS: frozenset[str] = frozenset({"[unk]", "<unk>", "unk"})

# 1-NED 等场景"剔除"用：[UNK] / <UNK> / 方块整体替换为空
_UNK_STRIP_PATTERN = re.compile(
    r"\[UNK\]|<UNK>|[" + "".join(UNK_BLOCK_CHARS) + r"]",
    flags=re.IGNORECASE,
)


def is_unk_char(ch: str | None) -> bool:
    """单 char 字段是否表示 UNK。

    覆盖：空字符串、[UNK]/<UNK>/裸 UNK（不区分大小写、忽略首尾空白）、
    以及 □ ■ ▢ ◻ ◼ 等方块占位（无论是单独一个还是包在空白里）。
    """
    if not ch:
        return True
    s = ch.strip()
    if not s:
        return True
    if s.lower() in UNK_TOKEN_FORMS:
        return True
    if all(c in UNK_BLOCK_CHARS for c in s):
        return True
    return False


def remove_unk(text: str) -> str:
    """剔除文本中所有 UNK 占位（用于 1-NED 等需要"忽略 UNK"的指标）。"""
    if not text:
        return ""
    return _UNK_STRIP_PATTERN.sub("", text)
