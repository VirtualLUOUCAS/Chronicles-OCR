from __future__ import annotations


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\\n", "").replace("\\\n", "")
    return text.replace(" ", "").replace("\u3000", "").replace("\t", "").replace("\r", "").replace("\n", "")


_PUNCT_CHARS = (
    r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    "，。、；：「」『』（）【】〔〕〈〉《》"
    "！？…—–·．“”‘’「」『』〝〞"
    "￥％＃＆＊＠／＼｜＋－＝＿"
    "～｀＾"
)
_PUNCT_TRANS = str.maketrans("", "", _PUNCT_CHARS)


def normalize_for_parsing(text: str) -> str:
    """字符提取 / 1-NED 评分专用：基础清洗 + 去标点。"""
    return normalize_text(text).translate(_PUNCT_TRANS)
