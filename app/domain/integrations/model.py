from sqlalchemy import Column, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped

from app.domain.model import InProviderDomain

from . import types


class Integration(InProviderDomain):
    type: Mapped[types.IntegrationEnum] = Column(Enum(types.IntegrationEnum), nullable=False, index=True)
    __table_args__ = (UniqueConstraint("provider_id", "type", name="ux_integration_provider_type"),)
