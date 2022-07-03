from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, Column, String

from app.utils.security import get_password_hash

from .base import Base, BaseModel


class User(Base):
    username = Column(String(64), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)

    def __init__(self, password: str | None = None, **kwargs: Any) -> None:
        if password is not None:
            if "hashed_password" in kwargs:
                raise ValueError(
                    "`password` and `hashed_password` are mutually exclusive"
                )
            self.password = password
        super().__init__(**kwargs)

    @property
    def password(self) -> str:
        """
        Password cannot be retrieved.
        """
        raise AttributeError("`password` not persisted")

    @password.setter
    def password(self, value: str) -> None:
        """
        Allows for creation of `User` objects with a `password` parameter. Hashes the
        password and stores to the `hashed_password` attribute.

        Parameters
        ----------
        value : str
            The clear text password.
        """
        self.hashed_password = get_password_hash(value)


class BaseUserModel(BaseModel):
    """
    Common attributes for all User representations.
    """

    username: str


class UserCreateModel(BaseUserModel):
    """
    Fields available to for `User` create operations.

        >>> UserCreateModel(**{"username": "Rick Sanchez", "password": "wubbalubbadubdub"})
        UserCreateModel(username='Rick Sanchez', password='wubbalubbadubdub')
        >>> UserCreateModel(**{"username": "Rick Sanchez", "is_active": False, "password": "wubbalubbadubdub"})
        UserCreateModel(username='Rick Sanchez', password='wubbalubbadubdub')
    """

    password: str


class UserModel(BaseUserModel):
    """
    Model for outbound representations of `User` instances.

        >>> import uuid
        >>> user = User(id=uuid.uuid4(), username="Rick Sanchez", is_active=True)
        >>> UserModel.from_orm(user)  # doctest: +ELLIPSIS
        UserModel(username='Rick Sanchez', id=UUID('...'), is_active=True)
    """

    id: UUID
    is_active: bool
