from typing import Any

from asyncpg.pgproto.pgproto import UUID
from starlite import Response


class UUIDResponse(Response):
    @staticmethod
    def serializer(value: Any) -> dict[str, Any]:
        if isinstance(value, UUID):
            return str(value)  # type:ignore[return-value]
        return Response.serializer(value)
