import logging

from starlette.responses import Response
from starlite import HTTPException, Request

logger = logging.getLogger(__name__)


class RepositoryException(HTTPException):
    pass


def logging_exception_handler(request: Request, exc: Exception) -> Response:
    logger.error("Application Exception", exc_info=exc)
    return request.app.default_http_exception_handler(request, exc)
