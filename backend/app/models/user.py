from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base
from .mixins import DateFieldsMixins


class User(DateFieldsMixins, Base):
    username: str = Column(String(64), nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    hashed_password: str = Column(String(256), nullable=False)

    items = relationship("Item", back_populates="owner_id")
