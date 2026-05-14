"""
图像编码：把本地图片读成 OpenAI / Anthropic 等通用网关接受的 data URI。
"""

from __future__ import annotations

import base64
import os
from io import BytesIO

from PIL import Image

MAX_IMAGE_SIZE = 8 * 1024 * 1024  # 8MB，超过则压缩

try:
    import imghdr

    def _detect_format(image_bytes: bytes) -> str | None:
        return imghdr.what(None, image_bytes)
except ImportError:

    def _detect_format(image_bytes: bytes) -> str | None:
        try:
            with Image.open(BytesIO(image_bytes)) as img:
                return (img.format or "").lower() or None
        except Exception:
            return None


def _compress(image_bytes: bytes, max_size: int = MAX_IMAGE_SIZE) -> tuple[bytes, str]:
    with Image.open(BytesIO(image_bytes)) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        for quality in (95, 90, 85, 80, 75, 70, 60):
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=quality)
            if buf.tell() <= max_size:
                return buf.getvalue(), "jpeg"
        # 仍超限：缩小分辨率
        scale = 0.95
        while scale > 0.1:
            new_size = (int(img.width * scale), int(img.height * scale))
            resized = img.resize(new_size, Image.LANCZOS)
            buf = BytesIO()
            resized.save(buf, format="JPEG", quality=50)
            if buf.tell() <= max_size:
                return buf.getvalue(), "jpeg"
            scale -= 0.05
        return buf.getvalue(), "jpeg"


def encode_image(image_path: str) -> str:
    """把本地图片文件读成 ``data:image/<fmt>;base64,<b64>`` data URI。"""
    if not isinstance(image_path, str) or not image_path:
        raise ValueError(f"invalid image path: {image_path!r}")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(image_path)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    fmt = None
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            fmt = (img.format or "").lower() or None
    except Exception:
        fmt = _detect_format(image_bytes)
    if not fmt:
        raise ValueError(f"无法识别图像格式: {image_path}")

    if len(image_bytes) > MAX_IMAGE_SIZE:
        image_bytes, fmt = _compress(image_bytes)

    if fmt == "jpeg":
        fmt = "jpg"
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/{fmt};base64,{b64}"
