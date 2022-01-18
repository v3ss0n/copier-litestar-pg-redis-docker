from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from starlite import DTOFactory
from starlite.plugins.sql_alchemy import SQLAlchemyPlugin

from .base import Base
from .mixins import DateFieldsMixins

UserDTOFactory = DTOFactory(plugins=[SQLAlchemyPlugin()])


class User(DateFieldsMixins, Base):
    username: str = Column(String(64), nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    hashed_password: str = Column(String(256), nullable=False)

    items = relationship("Item", back_populates="owner")


UserCreate = UserDTOFactory(
    "UserCreate",
    User,
    field_mapping={"hashed_password": ("password", str)},
)

UserRead = UserDTOFactory("UserRead", User, exclude=["hashed_password"])
