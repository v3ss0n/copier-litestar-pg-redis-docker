import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.decl_api import as_declarative, declared_attr


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: uuid.UUID | None = Column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
