import uuid
from typing import Any

from pydantic import BaseModel as _BaseModel
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm.decl_api import as_declarative, declared_attr
from sqlalchemy.types import TypeDecorator


class UUID(TypeDecorator):

    cache_ok = True
    impl = pg.UUID

    def process_bind_param(self, value: "UUID | None", dialect: Any) -> Any:
        return str(value)

    def process_result_value(self, value: Any, dialect: Any) -> uuid.UUID | None:
        if value is None:
            return None
        return uuid.UUID(value)


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: uuid.UUID = Column(UUID, default=uuid.uuid4, primary_key=True)


class BaseModel(_BaseModel):
    class Config:
        extra = "ignore"
        arbitrary_types_allowed = True
        orm_mode = True
