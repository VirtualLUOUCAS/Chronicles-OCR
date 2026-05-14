from __future__ import annotations

from .base import APIBase

API_TYPES = ("local_vllm", "openai_compat")


def get_api(api_type: str, **kwargs) -> APIBase:
    """构造一个 API 实例。

    Args:
        api_type: 取值 ``"local_vllm"`` / ``"openai_compat"``
        **kwargs: 转发给具体 API 类的参数

    Returns:
        APIBase 子类实例
    """
    if api_type == "local_vllm":
        from .local_vllm import LocalVLLMAPI

        return LocalVLLMAPI(**kwargs)
    if api_type == "openai_compat":
        from .openai_compat import OpenAICompatAPI

        return OpenAICompatAPI(**kwargs)

    raise ValueError(f"unsupported api_type: {api_type!r}, expected one of {API_TYPES}")
