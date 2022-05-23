import uuid

from sqlalchemy import Boolean, Column, String

from .base import Base, BaseModel
from .mixins import DateFieldsMixins


class User(DateFieldsMixins, Base):
    username = Column(String(64), nullable=False)
    is_active = Column(Boolean, nullable=False)
    hashed_password = Column(String(256), nullable=False)


class UserModel(BaseModel):
    """
    Common attributes for all User representations.
    """

    username: str
    is_active: bool = True


class UserCreateModel(UserModel):
    """
    Fields available to for `User` create operations.

        >>> UserCreateModel(**{"username": "Rick Sanchez", "password": "wubbalubbadubdub"})
        UserCreateModel(username='Rick Sanchez', is_active=True, password='wubbalubbadubdub')
        >>> UserCreateModel(**{"username": "Rick Sanchez", "is_active": False, "password": "wubbalubbadubdub"})
        UserCreateModel(username='Rick Sanchez', is_active=False, password='wubbalubbadubdub')
    """

    password: str


class UserReadModel(UserModel):
    """
    Model for outbound representations of `User` instances.

        >>> user = User(id=uuid.uuid4(), username="Rick Sanchez", is_active=True)
        >>> UserReadModel.from_orm(user)  # doctest: +ELLIPSIS
        UserReadModel(username='Rick Sanchez', is_active=True, id=UUID('...'))
    """

    id: uuid.UUID
