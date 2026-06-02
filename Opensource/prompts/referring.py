"""单字识别（Fine-grained Archaic Character Recognition）任务。

工作流：
  1. ``prepare_referring_sample`` 从 spotting GT 中按 (seed + sample_key) 确定性采样一个非 [UNK] 字符；
  2. 在原图上绘制红色矩形框，落盘到稳定缓存目录；
  3. 用渲染图调用模型，模型只识别红框内字符；
  4. 评分使用 Exact Match Accuracy。
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import tempfile
import threading
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw

from ..utils.unk import is_unk_char
from ._text import clean_value, extract_by_prefix, strip_thinking

# ============================================================
# Prompt / Extract
# ============================================================
PROMPT = """你是一名精通中国古文字学的专家。

任务：
图中有一个**红色矩形框**，框内是一个古文字。请识别该红框内的古文字对应的**现代汉字**。

要求：
- 只识别红框内的单个字符，不要识别图片中其他位置的字符
- 输出必须是**一个**现代汉字（不要输出多个字，不要加拼音、标点、解释或其他任何字符）
- 如果无法识别，则输出：[UNK]

输出格式（必须严格遵守）：
现代汉字：<单个汉字>
"""

_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002ebef\U00030000-\U0003134f]")


def extract(answer: str) -> tuple[bool, dict[str, str]]:
    text = strip_thinking(answer)
    raw = extract_by_prefix(text, ["现代汉字", "汉字", "识别结果", "识别", "答案", "char"])
    if not raw:
        raw = clean_value(text)
    if not raw:
        return False, {}

    stripped = raw.strip()
    if stripped.upper() in {"[UNK]", "<UNK>", "UNK"}:
        return True, {"char": "[UNK]"}

    m = _CJK_RE.search(stripped)
    if m:
        return True, {"char": m.group(0)}

    first = stripped.split()[0] if stripped.split() else ""
    if first:
        return True, {"char": first[:1]}
    return False, {}


# ============================================================
# 红框采样 + 渲染
# ============================================================
DEFAULT_SEED = 42
RED_BOX_COLOR = (255, 0, 0)
MIN_BOX_WIDTH = 3
MAX_BOX_WIDTH = 12
BOX_WIDTH_RATIO = 0.006  # 0.6% of min(W,H)


def _bbox_to_xyxy(item: dict) -> Optional[tuple[float, float, float, float]]:
    """规范化 spotting item 的 bbox 为像素坐标 (x1,y1,x2,y2)。

    支持：
      - {"bbox":[x,y,w,h], "modern_char": ...}（甲骨文）
      - {"bbox":{"x1","y1","x2","y2"}, "text": ...}（金文/篆文）
      - {"bbox":[x1,y1,x2,y2], "text": ...}（备用格式）
    """
    bbox = item.get("bbox")
    if bbox is None:
        return None

    if isinstance(bbox, dict):
        try:
            x1 = float(bbox.get("x1"))
            y1 = float(bbox.get("y1"))
            x2 = float(bbox.get("x2"))
            y2 = float(bbox.get("y2"))
        except (TypeError, ValueError):
            return None
        return (x1, y1, x2, y2) if (x2 > x1 and y2 > y1) else None

    if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
        try:
            bx = [float(v) for v in bbox]
        except (TypeError, ValueError):
            return None
        if "modern_char" in item:
            x, y, w, h = bx
            x1, y1, x2, y2 = x, y, x + w, y + h
        else:
            if bx[2] < bx[0] or bx[3] < bx[1]:
                x, y, w, h = bx
                x1, y1, x2, y2 = x, y, x + w, y + h
            else:
                x1, y1, x2, y2 = bx
        return (x1, y1, x2, y2) if (x2 > x1 and y2 > y1) else None

    return None


def _item_char(item: dict) -> str:
    ch = item.get("modern_char")
    if ch is None:
        ch = item.get("text", "")
    return str(ch or "").strip()


def _build_sample_key(row: dict) -> str:
    parts: list[str] = []
    for k in ("image_path", "img_path", "image"):
        v = row.get(k)
        if v:
            parts.append(f"{k}={v}")
    sp = row.get("spotting")
    if isinstance(sp, list) and sp:
        fp = hashlib.md5(json.dumps(sp, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:12]
        parts.append(f"sp_fp={fp}")
    return "|".join(parts)


def _seeded_rng(key: str, seed: int) -> random.Random:
    h = hashlib.md5(f"{seed}::{key}".encode("utf-8")).hexdigest()
    return random.Random(int(h[:16], 16))


def _pick_target(row: dict, seed: int) -> Optional[dict]:
    sp = row.get("spotting") or []
    if not isinstance(sp, list) or not sp:
        return None

    candidates: list[tuple[int, str, tuple[float, float, float, float]]] = []
    for idx, it in enumerate(sp):
        if not isinstance(it, dict):
            continue
        ch = _item_char(it)
        if is_unk_char(ch):
            continue
        bb = _bbox_to_xyxy(it)
        if bb is None:
            continue
        candidates.append((idx, ch, bb))
    if not candidates:
        return None

    sample_key = _build_sample_key(row) or "no-key"
    rng = _seeded_rng(sample_key, seed)
    idx, ch, bb = rng.choice(candidates)
    return {"char": ch, "bbox_xyxy": bb, "index": idx, "sample_key": sample_key}


def _box_width(W: int, H: int) -> int:
    short = max(1, min(W, H))
    w = int(round(short * BOX_WIDTH_RATIO))
    return max(MIN_BOX_WIDTH, min(MAX_BOX_WIDTH, w))


def _draw_box(img_path: str, bbox_xyxy, out_dir: Optional[str]) -> str:
    with Image.open(img_path) as im:
        im = im.convert("RGB")
        W, H = im.size
        x1, y1, x2, y2 = [
            max(0.0, min(float(W - 1) if i % 2 == 0 else float(H - 1), float(v))) for i, v in enumerate(bbox_xyxy)
        ]
        bw = _box_width(W, H)
        ImageDraw.Draw(im).rectangle([x1, y1, x2, y2], outline=RED_BOX_COLOR, width=bw)

        if out_dir is None:
            out_dir = os.path.join(tempfile.gettempdir(), "chronotext_referring")
        os.makedirs(out_dir, exist_ok=True)
        stem = Path(img_path).stem
        tag = hashlib.md5(f"{img_path}|{x1:.2f},{y1:.2f},{x2:.2f},{y2:.2f}".encode("utf-8")).hexdigest()[:8]
        out_path = os.path.join(out_dir, f"{stem}_redbox_{tag}_{os.getpid()}_{threading.get_ident()}.png")

        tmp = f"{out_path}.tmp"
        im.save(tmp, format="PNG")
        os.replace(tmp, out_path)
        return out_path


def prepare_referring_sample(
    row: dict,
    img_path: str,
    seed: int = DEFAULT_SEED,
    out_dir: Optional[str] = None,
) -> Optional[dict]:
    """采样 + 画框 + 落盘。任一步失败返回 None。"""
    picked = _pick_target(row, seed=seed)
    if picked is None:
        return None
    if not img_path or not os.path.exists(img_path):
        return None

    rendered = _draw_box(img_path, picked["bbox_xyxy"], out_dir)
    if not (rendered and os.path.exists(rendered)):
        rendered = _draw_box(img_path, picked["bbox_xyxy"], out_dir)
    return {
        "rendered_img_path": rendered,
        "target_char": picked["char"],
        "target_bbox_xyxy": [float(v) for v in picked["bbox_xyxy"]],
        "index": picked["index"],
        "sample_key": picked["sample_key"],
    }
