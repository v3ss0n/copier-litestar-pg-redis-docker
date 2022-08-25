from uuid import UUID  # noqa: TC003

from app import core


class Provider(core.Schema):
    id: UUID
    name: str
