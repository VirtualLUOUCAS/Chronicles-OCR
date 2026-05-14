"""全局中止信号：第一次 Ctrl+C 设标志位优雅退出，第二次直接强退。"""

from __future__ import annotations

import os
import signal
import threading

ABORT_EVENT = threading.Event()
_INSTALLED = False
_SIGINT_COUNT = 0


def _handler(signum, frame):
    global _SIGINT_COUNT
    _SIGINT_COUNT += 1
    ABORT_EVENT.set()
    msg = (
        "\n[中止] 收到 Ctrl+C，正在请求主循环退出并落盘，再次按 Ctrl+C 将强制退出...\n"
        if _SIGINT_COUNT == 1
        else "\n[中止] 再次收到 Ctrl+C，立即强制退出（可能丢失最近未落盘数据）。\n"
    )
    try:
        os.write(2, msg.encode("utf-8", errors="replace"))
    except Exception:
        pass
    if _SIGINT_COUNT >= 2:
        os._exit(130)


def install_signal_handlers_once() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    try:
        signal.signal(signal.SIGINT, _handler)
        signal.signal(signal.SIGTERM, _handler)
    except Exception:
        pass
    _INSTALLED = True
