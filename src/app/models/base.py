import uuid

from pydantic import BaseModel as _BaseModel
from sqlalchemy import Column
from sqlalchemy.orm.decl_api import as_declarative, declared_attr

from .sa_uuid import UUID


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
