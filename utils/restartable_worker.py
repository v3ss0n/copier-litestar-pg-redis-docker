import os
import signal
import threading
import time
from typing import Any

from uvicorn.workers import UvicornWorker


class ReloaderThread(threading.Thread):
    def __init__(self, worker: UvicornWorker, sleep_interval: float = 1.0):
        super().__init__()
        self.daemon = True
        self._worker = worker
        self._interval = sleep_interval

    def run(self) -> None:
        """Sends a KILL signal to the current process if the worker's active
        flag is set to False."""
        while True:
            if not self._worker.alive:
                os.kill(os.getpid(), signal.SIGINT)
            time.sleep(self._interval)


class RestartableUvicornWorker(UvicornWorker):  # type: ignore[misc]
    """UvicornWorker with additional thread that sends a KILL signal to the
    current process if the worker's active flag is set to False.

    attribution: https://github.com/benoitc/gunicorn/issues/2339#issuecomment-867481389
    """

    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools"}

    def __init__(self, *args: list[Any], **kwargs: dict[str, Any]):
        super().__init__(*args, **kwargs)
        self._reloader_thread = ReloaderThread(self)

    def run(self) -> None:
        if self.cfg.reload:
            self._reloader_thread.start()
        super().run()
