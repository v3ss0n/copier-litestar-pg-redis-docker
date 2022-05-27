import uuid

from sqlalchemy import Column, ForeignKey, String

from .base import Base, BaseModel
from .mixins import DateFieldsMixins
from .sa_uuid import UUID


class Item(DateFieldsMixins, Base):
    name: str = Column(String(64), nullable=False)
    owner_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("user.id"))


class ItemCreateModel(BaseModel):
    name: str


class ItemModel(BaseModel):
    id: uuid.UUID
    name: str
    owner_id: uuid.UUID
