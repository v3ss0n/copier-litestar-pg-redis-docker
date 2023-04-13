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

from .countries import Country

__all__ = [
    "Author",
    "ListDTO",
    "ReadDTO",
    "Repository",
    "Service",
    "WriteDTO",
]


class Author(AuditBase):
    name: Mapped[str]
    dob: Mapped[date]
    country_id: Mapped[UUID | None] = mapped_column(ForeignKey("country.id"), info=dto_field(Mark.PRIVATE))
    nationality: Mapped[Country | None] = relationship(lazy="joined")


class Repository(SQLAlchemyRepository[Author]):
    model_type = Author


Service = service.Service[Author]

WriteDTO = SQLAlchemyDTO[Annotated[Author, DTOConfig(exclude={"id", "created", "updated"})]]
ListDTO = SQLAlchemyDTO[list[Author]]
ReadDTO = SQLAlchemyDTO[Author]
