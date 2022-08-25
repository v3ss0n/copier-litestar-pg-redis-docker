from uuid import uuid4

import pytest

from app.domain import entities, providers


@pytest.fixture()
def sport(provider: providers.schema.Provider) -> entities.schema.Entity:
    return entities.schema.Entity(
        id=uuid4(),
        name="Tennis",
        owner_id=None,
        provider_id=provider.id,
        type=entities.types.EntitiesEnum.sport,
    )


@pytest.fixture()
def sport_person(provider: providers.schema.Provider, sport: entities.schema.Entity) -> entities.schema.Entity:
    return entities.schema.Entity(
        id=uuid4(),
        name="Nick Kyrgios",
        owner_id=sport.id,
        provider_id=provider.id,
        type=entities.types.EntitiesEnum.sport_person,
    )


@pytest.fixture()
def contest(provider: providers.schema.Provider, sport: entities.schema.Entity) -> entities.schema.Entity:
    return entities.schema.Entity(
        id=uuid4(),
        name="Jubb v Kyrgios",
        owner_id=sport.id,
        provider_id=provider.id,
        type=entities.types.EntitiesEnum.contest,
    )


@pytest.fixture()
def competitor(
    provider: providers.schema.Provider,
    sport_person: entities.schema.Entity,
    contest: entities.schema.Entity,
) -> entities.schema.Entity:
    return entities.schema.Entity(
        id=uuid4(),
        name="Nick Kyrgios",
        owner_id=contest.id,
        provider_id=provider.id,
        type=entities.types.EntitiesEnum.competitor,
        extra=entities.schema.Extra(sub_entity=sport_person),
    )
