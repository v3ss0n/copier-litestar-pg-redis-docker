from uuid import UUID

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped

from app import core


class InProviderDomain(core.Base):
    __abstract__ = True

    provider_id: Mapped[UUID] = Column(  # type:ignore[misc]
        pg.UUID, ForeignKey("provider.id"), nullable=False
    )
