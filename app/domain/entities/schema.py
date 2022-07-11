from uuid import UUID

from pydantic import Field

from app import core

from .types import EntitiesEnum


class Extra(core.Schema):
    """
    Extra information about the entity that may be required depending on the entity type.

    Contest competitors must define the `sub_entity` key to reference the team/sport-person that the
    competitor wraps.
    """

    sub_entity: "Entity | None"


class Entity(core.Schema):
    """
    Representation of provider entities that forces integrations to put the provider entities into
    the terms of our core entities.
    """

    id: UUID
    name: str
    owner_id: UUID | None
    provider_id: UUID
    type: EntitiesEnum
    extra: Extra = Field(default_factory=Extra)


Extra.update_forward_refs()
