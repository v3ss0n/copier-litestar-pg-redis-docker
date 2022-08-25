from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql as pg

from app import core

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.orm import Mapped


class InProviderDomain(core.Base):
    __abstract__ = True

    provider_id: "Mapped[UUID]" = Column(  # type:ignore[misc]
        pg.UUID, ForeignKey("provider.id"), nullable=False
    )
