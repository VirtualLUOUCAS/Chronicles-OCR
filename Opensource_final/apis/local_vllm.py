"""本地 vLLM 进程内推理：``from vllm import LLM`` 加载一个本地模型路径。

适用场景：用户提供一个本地权重路径（``--api_type local_vllm --model_path ...``），
"""

from __future__ import annotations

import threading
from pathlib import Path

from PIL import Image

from .base import APIBase

DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.0


class LocalVLLMAPI(APIBase):
    """vLLM 进程内推理。线程安全：同一个 ``LLM`` 实例可多线程并发调用 ``generate``。"""

    def __init__(
        self,
        model_path: str,
        tensor_parallel_size: int = 1,
        max_model_len: int | None = None,
        dtype: str = "auto",
        gpu_memory_utilization: float = 0.9,
        trust_remote_code: bool = True,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        max_try: int = 1,
        **engine_kwargs,
    ):
        from vllm import LLM, SamplingParams  # 延迟导入：openai_compat 用户可能没装 vllm

        self.model_path = model_path
        self.max_try = max_try
        self.sampling_params = SamplingParams(
            temperature=temperature,
            max_tokens=max_tokens,
        )

        engine_args = dict(
            model=model_path,
            tensor_parallel_size=tensor_parallel_size,
            dtype=dtype,
            gpu_memory_utilization=gpu_memory_utilization,
            trust_remote_code=trust_remote_code,
        )
        if max_model_len is not None:
            engine_args["max_model_len"] = max_model_len
        engine_args.update(engine_kwargs)
        self.llm = LLM(**engine_args)
        self._lock = threading.Lock()  # vLLM 自带异步引擎，但部分版本对 generate 调用串行更稳

        self._model_name = Path(model_path).name

    def __call__(self, img_path: str | None, question: str, **kwargs):
        try:
            inputs = self._build_inputs(img_path, question)
            with self._lock:
                outputs = self.llm.generate([inputs], self.sampling_params)
            text = outputs[0].outputs[0].text or ""
            return True, "", text.strip()
        except Exception as e:
            print(f"[LocalVLLMAPI] inference 失败: {e}")
            return False, "", ""

    def _build_inputs(self, img_path: str | None, question: str) -> dict:
        if not img_path:
            return {"prompt": question}
        # vLLM 多模态格式：使用 ``multi_modal_data``
        image = Image.open(img_path).convert("RGB")
        prompt = f"<|im_start|>user\n<image>\n{question}<|im_end|>\n<|im_start|>assistant\n"
        return {"prompt": prompt, "multi_modal_data": {"image": image}}
