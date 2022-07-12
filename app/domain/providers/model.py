from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from app.core.model import Base


class Provider(Base):
    name: Mapped[str] = Column(String(64), nullable=False, unique=True)
