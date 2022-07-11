from starlette.status import HTTP_409_CONFLICT
from starlite.exceptions import HTTPException


class RepositoryException(HTTPException):
    pass


class RepositoryConflictException(RepositoryException):
    status_code = HTTP_409_CONFLICT
