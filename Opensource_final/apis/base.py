"""APIBase：所有 API 实现的最小抽象基类。"""

from __future__ import annotations

from abc import ABC, abstractmethod


class APIBase(ABC):
    @abstractmethod
    def __call__(self, img_path: str | None, question: str, **kwargs) -> tuple[bool, str, str]:
        """统一调用接口。

        Args:
            img_path: 本地图片路径（``None`` 表示纯文本任务）
            question: prompt 文本

        Returns:
            ``(success, thinking, answer)`` 三元组：
              - success: 调用是否成功
              - thinking: 模型 think 段（可能为空）
              - answer: 模型最终回复
        """
        ...
