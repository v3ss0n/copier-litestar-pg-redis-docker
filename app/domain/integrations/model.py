from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.model import InProviderDomain

from .types import IntegrationEnum


class Integration(InProviderDomain):
    type: Mapped[Enum] = mapped_column(Enum(IntegrationEnum), nullable=False, index=True)
    __table_args__ = (UniqueConstraint("provider_id", "type", name="ux_integration_provider_type"),)
