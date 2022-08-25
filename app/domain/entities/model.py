from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, text
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped

from app.domain.model import InProviderDomain

from .types import EntitiesEnum

if TYPE_CHECKING:

    from uuid import UUID


class Entity(InProviderDomain):
    name: Mapped[str] = Column(String, nullable=False)
    type: Mapped[EntitiesEnum] = Column(Enum(EntitiesEnum, create_constraint=False), nullable=False)
    owner_id: Optional["UUID"] = Column(  # type:ignore[misc]
        pg.UUID, ForeignKey("entity.id"), index=True, nullable=True
    )
    # ryno id is an implementation detail, not to be exposed to clients.
    ryno_id: Mapped[int] = Column(Integer, index=True, nullable=True)
    extra: Mapped[dict[str, Any]] = Column(pg.JSONB, nullable=False, server_default=text("'{}'::jsonb"))
