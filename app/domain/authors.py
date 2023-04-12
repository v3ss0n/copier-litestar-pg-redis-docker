from datetime import date
from email.message import EmailMessage
from typing import Annotated
from uuid import UUID

from litestar.contrib.sqlalchemy.base import AuditBase
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.contrib.sqlalchemy.repository import SQLAlchemyRepository
from litestar.dto.factory import DTOConfig, Mark, dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib import email, service, settings
from app.lib.worker import queue

from .country import Country

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
    nationality: Mapped[Country | None] = relationship()


class Repository(SQLAlchemyRepository[Author]):
    model_type = Author


class Service(service.Service[Author]):
    async def create(self, data: Author) -> Author:
        created = await super().create(data)
        await queue.enqueue("author_created", data={"id": created.id})
        return data

    @staticmethod
    async def send_author_created_email(message_content: str) -> None:
        """Sends an email to alert that a new `Author` has been created.

        Args:
            message_content: The body of the email.
        """
        message = EmailMessage()
        message["From"] = settings.email.SENDER
        message["To"] = settings.email.RECIPIENT
        message["Subject"] = settings.email.NEW_AUTHOR_SUBJECT
        message.set_content(message_content)
        async with email.client:
            await email.client.send_message(message)


WriteDTO = SQLAlchemyDTO[Annotated[Author, DTOConfig(exclude={"id", "created", "updated"})]]
ListDTO = SQLAlchemyDTO[list[Author]]
ReadDTO = SQLAlchemyDTO[Author]
