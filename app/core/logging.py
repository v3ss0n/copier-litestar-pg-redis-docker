import logging
import re
from typing import Any

from starlette.status import HTTP_200_OK
from starlite import LoggingConfig

from app.constants import Paths
from app.settings import app_settings


class AccessLogFilter(logging.Filter):
    """For filtering log events based on request path.

    Parameters
    ----------
    path_re : str
        Regex string, if the path of the request matches the regex the log event is dropped.
    args : Any
    kwargs : Any
        Args and kwargs passed through to `logging.Filter`.
    """

    def __init__(self, *args: Any, path_re: str, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.path_filter = re.compile(path_re)

    def filter(self, record: logging.LogRecord) -> bool:
        *_, req_path, _, status_code = record.args  # type:ignore[misc]
        if (
            self.path_filter.match(req_path)  # type:ignore[arg-type]
            and status_code == HTTP_200_OK
        ):
            return False
        return True


log_config = LoggingConfig(
    root={"level": app_settings.LOG_LEVEL, "handlers": ["queue_listener"]},
    filters={
        "health_filter": {
            "()": AccessLogFilter,
            "path_re": f"^{Paths.HEALTH}$",
        }
    },
    formatters={"standard": {"format": "%(levelname)s - %(asctime)s - %(name)s - %(message)s"}},
    loggers={
        "app": {
            "propagate": True,
        },
        "gunicorn.error": {
            "propagate": True,
        },
        "uvicorn.access": {
            "propagate": True,
            "filters": ["health_filter"],
        },
        "uvicorn.error": {
            "propagate": True,
        },
        "sqlalchemy.engine": {
            "propagate": True,
        },
        "starlite": {
            "level": "WARNING",
            "propagate": True,
        },
    },
)
