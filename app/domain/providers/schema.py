from uuid import UUID

from app import core


class Provider(core.Schema):
    id: UUID
    name: str
