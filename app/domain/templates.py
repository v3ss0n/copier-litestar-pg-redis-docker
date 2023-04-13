from typing import Annotated

from litestar.contrib.sqlalchemy.base import AuditBase
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.contrib.sqlalchemy.repository import SQLAlchemyRepository
from litestar.dto.factory.config import DTOConfig
from sqlalchemy.orm import Mapped

from app.lib import service

__all__ = [
    "Template",
    "ListDTO",
    "ReadDTO",
    "Repository",
    "Service",
    "WriteDTO",
]


class Template(AuditBase):
    key: Mapped[str]
    value: Mapped[int]


class Repository(SQLAlchemyRepository[Template]):
    model_type = Template


Service = service.Service[Template]

WriteDTO = SQLAlchemyDTO[Annotated[Template, DTOConfig(exclude={"id", "created", "updated"})]]
ListDTO = SQLAlchemyDTO[list[Template]]
ReadDTO = SQLAlchemyDTO[Template]
