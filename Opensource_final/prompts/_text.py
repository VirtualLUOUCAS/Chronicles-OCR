"""Prompt / Extract 共用文本工具。

- ``strip_thinking``: 剥离模型输出里的 ``<think>...</think>`` / ``<answer>...</answer>``
- ``extract_by_prefix``: 按多前缀（"字体分类:" / "字体:" / ...）从纯文本中抽取冒号后的内容
- ``clean_value``: 清理首尾空白、代码块围栏、常见标点引号
"""

from __future__ import annotations

import re

_OTHER_PREFIX_RE = re.compile(r"^(?:字体分类|字体|分类|提取文本|提取结果|识别结果|识别文本|文本)\s*[:：]")


def strip_thinking(text: str) -> str:
    """剥离 thinking 段，只保留最终答案。

    支持 ``<think>...</think><answer>...</answer>`` / 仅 ``</think>`` / 仅 ``<think>`` 等多种形态。
    """
    if not text:
        return ""
    s = text

    ans_m = re.search(r"<\s*answer\s*>([\s\S]*?)<\s*/\s*answer\s*>", s, flags=re.IGNORECASE)
    if ans_m:
        return ans_m.group(1).strip()

    close_matches = list(re.finditer(r"<\s*/\s*(?:think|thinking|reasoning)\s*>", s, flags=re.IGNORECASE))
    if close_matches:
        last = close_matches[-1]
        tail = s[last.end() :].strip()
        tail = re.sub(r"^\s*<\s*answer\s*>\s*", "", tail, flags=re.IGNORECASE)
        tail = re.sub(r"\s*<\s*/?\s*answer\s*>\s*$", "", tail, flags=re.IGNORECASE)
        return tail.strip()

    open_m = re.search(r"<\s*(?:think|thinking|reasoning)\s*>", s, flags=re.IGNORECASE)
    if open_m:
        head = s[: open_m.start()].strip()
        return head if head else ""

    return s.strip()


def strip_code_fence(s: str) -> str:
    if s is None:
        return ""
    s = s.strip()
    m = re.match(r"^`{3,}[^\n`]*\n?(.*?)\n?`{3,}\s*$", s, re.DOTALL)
    if m:
        return m.group(1).strip()
    return s.strip("`").strip()


def clean_value(s: str) -> str:
    if not s:
        return ""
    s = strip_code_fence(s)
    s = s.strip().strip("。.；;，,\"'“”‘’")
    return s.strip()


def extract_by_prefix(text: str, prefixes: list[str], merge_trailing_lines: bool = False) -> str:
    """按 ``前缀:`` 抽取冒号之后的答案，命中多次取最后一次。

    ``merge_trailing_lines=True`` 时，"同行答案 + 后续多行非空"一并合并，
    用于"字符提取"任务（模型常把多行文本写在前缀之后）。
    """
    if not text:
        return ""

    prefix_pattern = "|".join(re.escape(p) for p in prefixes)
    head_pattern = re.compile(rf"(?:{prefix_pattern})\s*[:：]")
    matches = list(head_pattern.finditer(text))
    if not matches:
        return ""

    last = matches[-1]
    tail = text[last.end() :]
    first_line, _nl, rest = tail.partition("\n")
    first_line_stripped = first_line.strip()

    starts_with_fence = bool(re.match(r"^`{3,}", first_line_stripped))
    first_line_no_fence = re.sub(r"^`{3,}[^\n`]*", "", first_line_stripped).strip("` ").strip()

    if not starts_with_fence and first_line_no_fence:
        if not merge_trailing_lines:
            return clean_value(first_line_no_fence)
        follow_lines: list[str] = []
        for ln in rest.splitlines():
            ln_s = ln.strip().strip("`").strip()
            if not ln_s:
                continue
            if _OTHER_PREFIX_RE.search(ln_s):
                break
            follow_lines.append(ln_s)
        head_clean = clean_value(first_line_no_fence)
        if not follow_lines:
            return head_clean
        cleaned_follow = [(clean_value(ln) or ln) for ln in follow_lines]
        return "\n".join([head_clean, *cleaned_follow]).strip()

    multiline_src = rest
    if starts_with_fence:
        close_m = re.search(r"\n?`{3,}\s*(\n|$)", rest)
        if close_m:
            multiline_src = rest[: close_m.start()]

    lines = [ln.strip().strip("`").strip() for ln in multiline_src.splitlines()]
    lines = [ln for ln in lines if ln]
    if not lines:
        return ""
    if len(lines) == 1:
        return clean_value(lines[0])
    cleaned = [(clean_value(ln) or ln) for ln in lines]
    return "\n".join(cleaned).strip()
