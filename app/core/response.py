from typing import Any

from asyncpg.pgproto import pgproto
from starlite import Response as _Response


class Response(_Response):
    @staticmethod
    def serializer(value: Any) -> Any:
        if isinstance(value, pgproto.UUID):  # pylint: disable=c-extension-no-member
            return str(value)
        return _Response.serializer(value)
