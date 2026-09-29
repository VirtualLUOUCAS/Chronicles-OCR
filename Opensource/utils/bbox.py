"""bbox 归一化：把数据集里几种 bbox 写法统一成像素坐标 (x1, y1, x2, y2)。

支持三种形态：
  - ``{"bbox": [x, y, w, h], "modern_char": ...}``（甲骨文）
  - ``{"bbox": {"x1","y1","x2","y2"}, "text": ...}``（金文 / 篆文）
  - ``{"bbox": [x1, y1, x2, y2], "text": ...}``（备用格式）
"""

from __future__ import annotations


def bbox_to_xyxy(item: dict) -> tuple[float, float, float, float] | None:
    bbox = item.get("bbox")

    if isinstance(bbox, dict):
        try:
            x1, y1, x2, y2 = (float(bbox[k]) for k in ("x1", "y1", "x2", "y2"))
        except (KeyError, TypeError, ValueError):
            return None
    elif isinstance(bbox, (list, tuple)) and len(bbox) == 4:
        try:
            bx = [float(v) for v in bbox]
        except (TypeError, ValueError):
            return None
        # xywh 的两个信号：显式的 modern_char 字段，或右下角小于左上角
        if "modern_char" in item or bx[2] < bx[0] or bx[3] < bx[1]:
            x1, y1, x2, y2 = bx[0], bx[1], bx[0] + bx[2], bx[1] + bx[3]
        else:
            x1, y1, x2, y2 = bx
    else:
        return None

    return (x1, y1, x2, y2) if (x2 > x1 and y2 > y1) else None


def item_char(item: dict) -> str:
    """取 spotting item 的字符字段（甲骨文用 modern_char，其余用 text）。"""
    ch = item.get("modern_char")
    if ch is None:
        ch = item.get("text", "")
    return str(ch or "").strip()
