from datetime import date
from email.message import EmailMessage
from typing import Annotated

from sqlalchemy.orm import Mapped
from starlite.contrib.sqlalchemy.base import AuditBase
from starlite.contrib.sqlalchemy.dto import SQLAlchemyDTO
from starlite.contrib.sqlalchemy.repository import SQLAlchemyRepository
from starlite.dto.factory.config import DTOConfig

from app.lib import email, service, settings
from app.lib.worker import queue

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


WriteDTO = SQLAlchemyDTO[Annotated[Author, DTOConfig(exclude={"id"})]]
ListDTO = SQLAlchemyDTO[list[Author]]
ReadDTO = SQLAlchemyDTO[Author]
