"""4 个任务的 prompt 与 extract 注册表。"""

from __future__ import annotations

from typing import Callable

from . import classify, extract_text, referring, spotting

TASK_CLASSIFY = "字体分类"
TASK_EXTRACT = "字符提取"
TASK_SPOTTING = "字符检测"
TASK_REFERRING = "单字识别"

PROMPTS: dict[str, str] = {
    TASK_CLASSIFY: classify.PROMPT,
    TASK_EXTRACT: extract_text.PROMPT,
    TASK_SPOTTING: spotting.PROMPT,
    TASK_REFERRING: referring.PROMPT,
}

EXTRACT_FUNCS: dict[str, Callable[[str], tuple[bool, dict]]] = {
    TASK_CLASSIFY: classify.extract,
    TASK_EXTRACT: extract_text.extract,
    TASK_SPOTTING: spotting.extract,
    TASK_REFERRING: referring.extract,
}
