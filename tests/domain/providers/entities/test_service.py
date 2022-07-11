from uuid import uuid4

import pytest
from starlite.exceptions import ValidationException

from app.core.dependencies import Filters
from app.domain import entities
from app.domain.providers.entities import Service


@pytest.fixture
def filters() -> Filters:
    return Filters(created=None, id=None, limit_offset=None, updated=None)


@pytest.fixture
async def service(filters: Filters) -> Service:
    return await Service.new(entity_id=uuid4(), filters=filters)


async def test_upsert_competitor_type_extra_validation(
    competitor: entities.schema.Entity, service: Service
) -> None:
    competitor.extra.sub_entity = None
    with pytest.raises(ValidationException):
        await service.upsert(competitor)
