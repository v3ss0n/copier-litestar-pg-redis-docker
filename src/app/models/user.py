from sqlalchemy import Boolean, Column, String
from starlite import DTOFactory
from starlite.plugins.sql_alchemy import SQLAlchemyPlugin

from .base import Base
from .mixins import DateFieldsMixins


class User(DateFieldsMixins, Base):
    username: str = Column(String(64), nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    hashed_password: str = Column(String(256), nullable=False)


UserDTOFactory = DTOFactory(plugins=[SQLAlchemyPlugin()])
UserCreateDTO = UserDTOFactory(
    "UserCreateDTO",
    User,
    exclude=["created_date", "updated_date", "items", "id"],
    field_mapping={"hashed_password": ("password", str)},
)
UserReadDTO = UserDTOFactory("UserReadDTO", User, exclude=["hashed_password"])
