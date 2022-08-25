from typing import TYPE_CHECKING

from app.core.schema import Schema as BaseSchema

if TYPE_CHECKING:
    from uuid import UUID

    from app.domain.integrations import IntegrationEnum


class Integration(BaseSchema):
    provider_id: "UUID"
    type: "IntegrationEnum"
