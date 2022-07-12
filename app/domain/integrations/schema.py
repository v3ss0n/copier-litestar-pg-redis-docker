from uuid import UUID

from app.core.schema import Schema as BaseSchema

from . import types


class Integration(BaseSchema):
    provider_id: UUID
    type: types.IntegrationEnum
