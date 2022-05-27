import uuid
from typing import Any

from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.types import TypeDecorator


class UUID(TypeDecorator):
    """
    Decorated `sqlalchemy.dialects.postgresql.UUID` type that ensures we are only
    dealing with stdlib's `uuid.UUID` outsdide of SQLAlchemy.

    This allows the type to play nicely with orjson.
    """

    cache_ok = True
    impl = pg.UUID

    def process_bind_param(self, value: "UUID | None", dialect: Any) -> str | None:
        if value is None:
            return None
        return str(value)

    def process_result_value(
        self, value: str | pg.UUID, dialect: Any
    ) -> uuid.UUID | None:
        if value is None:
            return None
        return uuid.UUID(str(value))
