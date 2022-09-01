from typing import Optional
from uuid import UUID

from pydantic import Field

from app.core import Schema

from .types import EntitiesEnum


class Extra(Schema):
    """Extra information about the entity that may be required depending on the
    entity type.

    Contest competitors must define the `sub_entity` key to reference
    the team/sport-person that the competitor wraps.
    """

    sub_entity: Optional["Entity"]


class Entity(Schema):
    """Representation of provider entities that forces integrations to put the
    provider entities into the terms of our core entities."""

    id: UUID
    name: str
    owner_id: UUID | None
    provider_id: UUID
    type: EntitiesEnum
    extra: Extra = Field(default_factory=Extra)  # type:ignore[arg-type]


Extra.update_forward_refs()
