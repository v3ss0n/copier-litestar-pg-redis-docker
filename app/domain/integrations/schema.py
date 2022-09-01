from uuid import UUID

from app.core.schema import Schema as BaseSchema
from app.domain.integrations.types import IntegrationEnum


class Integration(BaseSchema):
    provider_id: UUID
    type: IntegrationEnum
