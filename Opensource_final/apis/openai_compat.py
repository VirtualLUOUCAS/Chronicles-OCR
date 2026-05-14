"""OpenAI 兼容 API 客户端。

适用场景：
  1. 用户用 ``vllm serve`` / ``sglang`` / ``lmdeploy`` 等起的本地 OpenAI 兼容服务
  2. OpenAI 官方 / Gemini-OpenAI-compat / Claude-OpenAI-compat 等公有云
  3. 任意自托管的 OpenAI Chat Completions 协议网关

只依赖标准 ``openai`` Python 客户端，不引入任何特殊鉴权 / cos url 逻辑。
"""

from __future__ import annotations

import re
import time

from openai import OpenAI

from ..utils.image_utils import encode_image
from .base import APIBase

DEFAULT_TIMEOUT = 1200


def _split_think_answer(response: str) -> tuple[str, str]:
    """从模型输出中拆出 thinking / final answer。"""
    if not response or not response.strip():
        return "", ""
    m = re.search(r"<think>\n(.*?)\n</think>\n<answer>\n(.*?)\n</answer>", response, flags=re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "", response.strip()


class OpenAICompatAPI(APIBase):
    """走 OpenAI Chat Completions 协议的通用客户端。"""

    def __init__(
        self,
        model_name: str,
        base_url: str,
        api_key: str = "EMPTY",
        max_try: int = 3,
        timeout: int = DEFAULT_TIMEOUT,
        image_first: bool = True,
    ):
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key
        self.max_try = max_try
        self.timeout = timeout
        self.image_first = image_first
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def __call__(self, img_path: str | None, question: str, temperature: float | None = None, **kwargs):
        messages = self._build_messages(img_path, question)
        return self._send(messages, temperature=temperature)

    def _build_messages(self, img_path: str | None, question: str) -> list[dict]:
        if not img_path:
            assert question, "question is required when img_path is empty"
            return [{"role": "user", "content": [{"type": "text", "text": question}]}]
        data_uri = encode_image(img_path)
        img_part = {"type": "image_url", "image_url": {"url": data_uri}}
        txt_part = {"type": "text", "text": question}
        content = [img_part, txt_part] if self.image_first else [txt_part, img_part]
        return [{"role": "user", "content": content}]

    def _send(self, messages: list[dict], temperature: float | None = None):
        for attempt in range(1, self.max_try + 1):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    timeout=self.timeout,
                )
                response = completion.choices[0].message.content or ""
                thinking, answer = _split_think_answer(response)
                return True, thinking, answer
            except Exception as e:
                print(f"[OpenAICompatAPI] 尝试 {attempt}/{self.max_try} 失败: {e}")
                if attempt < self.max_try:
                    time.sleep(min(2 * attempt, 10))
        return False, "", ""
