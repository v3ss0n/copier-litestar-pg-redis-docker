from uuid import UUID

from sqlalchemy import Column, ForeignKey, String

from app.utils.pg_uuid import PostgresUUID

from .base import Base, BaseModel


class Item(Base):
    name: str = Column(String(64), nullable=False)
    owner_id: UUID = Column(PostgresUUID(as_uuid=True), ForeignKey("user.id"))


class ItemCreateModel(BaseModel):
    name: str


class ItemModel(BaseModel):
    id: UUID
    name: str
    owner_id: UUID
