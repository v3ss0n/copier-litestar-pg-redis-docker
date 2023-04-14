from datetime import date
from typing import Annotated
from uuid import UUID

from litestar.contrib.sqlalchemy.base import AuditBase
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.contrib.sqlalchemy.repository import SQLAlchemyRepository
from litestar.dto.factory import DTOConfig, Mark, dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib import service

from . import countries

__all__ = [
    "Author",
    "ReadDTO",
    "Repository",
    "Service",
    "WriteDTO",
]


class Author(AuditBase):
    name: Mapped[str]
    dob: Mapped[date]
    country_id: Mapped[UUID | None] = mapped_column(ForeignKey("country.id"))
    nationality: Mapped[countries.Country | None] = relationship(lazy="joined", info=dto_field(Mark.READ_ONLY))


class Repository(SQLAlchemyRepository[Author]):
    model_type = Author


class Service(service.Service[Author]):
    repository_type = Repository


WriteDTO = SQLAlchemyDTO[Annotated[Author, DTOConfig(exclude={"id", "created", "updated", "nationality"})]]
ReadDTO = SQLAlchemyDTO[Author]
