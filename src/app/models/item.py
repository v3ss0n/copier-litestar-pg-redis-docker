from uuid import UUID

from sqlalchemy import Column, ForeignKey, String

from .base import Base, BaseModel
from .mixins import DateFieldsMixins
from .pg_uuid import PostgresUUID


class Item(DateFieldsMixins, Base):
    name: str = Column(String(64), nullable=False)
    owner_id: UUID = Column(PostgresUUID(as_uuid=True), ForeignKey("user.id"))


class ItemCreateModel(BaseModel):
    name: str


class ItemModel(BaseModel):
    id: UUID
    name: str
    owner_id: UUID
