from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base
from .mixins import DateFieldsMixins


class Item(DateFieldsMixins, Base):
    name: str = Column(String(64), nullable=False)
    owner_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    owner = relationship("User", back_populates="items")
