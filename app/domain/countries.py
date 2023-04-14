from typing import Annotated

from litestar.contrib.sqlalchemy.base import AuditBase
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.contrib.sqlalchemy.repository import SQLAlchemyRepository
from litestar.dto.factory.config import DTOConfig
from sqlalchemy.orm import Mapped

from app.lib import service

__all__ = [
    "Country",
    "ReadDTO",
    "Repository",
    "Service",
    "WriteDTO",
]


class Country(AuditBase):
    name: Mapped[str]
    population: Mapped[int]


class Repository(SQLAlchemyRepository[Country]):
    model_type = Country


Service = service.Service[Country]

WriteDTO = SQLAlchemyDTO[Annotated[Country, DTOConfig(exclude={"id", "created", "updated"})]]
ReadDTO = SQLAlchemyDTO[Country]
