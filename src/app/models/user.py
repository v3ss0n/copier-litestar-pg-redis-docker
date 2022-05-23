import uuid

from sqlalchemy import Boolean, Column, String

from .base import Base, BaseModel
from .mixins import DateFieldsMixins


class User(DateFieldsMixins, Base):
    username = Column(String(64), nullable=False)
    is_active = Column(Boolean, nullable=False)
    hashed_password = Column(String(256), nullable=False)


class UserModel(BaseModel):
    username: str
    is_active: bool = True


class UserCreateModel(UserModel):
    password: str


class UserReadModel(UserModel):
    id: uuid.UUID
