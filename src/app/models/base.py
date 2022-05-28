from uuid import UUID, uuid4

from pydantic import BaseModel as _BaseModel
from sqlalchemy import Column
from sqlalchemy.orm.decl_api import as_declarative, declared_attr

from .pg_uuid import PostgresUUID


@as_declarative()
class Base:
    """
    Base for all SQLAlchemy declarative models.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: UUID = Column(PostgresUUID, default=uuid4, primary_key=True)


class BaseModel(_BaseModel):
    """
    Base for all Pydantic models.

    Have not included the `id` attribute that is included in the SQLAlchemy `Base`
    as that would force it to be available to all create and read models. Therefore,
    where a resource representation should include the `id` field, it must be added
    in the subclass.
    """

    class Config:
        extra = "ignore"
        arbitrary_types_allowed = True
        orm_mode = True
