from typing import TYPE_CHECKING

from starlite import Controller as BaseController
from starlite import get

from app.core.handlers import create_pagination_dependencies

if TYPE_CHECKING:
    from .schema import Entity
    from .service import Service


class Controller(BaseController):
    """Read-only view of all identified entities.

    Identification and modification must occur through the relevant
    provider sub-route, e.g.: `/providers/<provider_id>/entities`, etc.
    """

    tags = ["Entities"]
    member_path = "{entity_id:uuid}"

    @get(dependencies=create_pagination_dependencies())
    async def list_all_entities(self, service: "Service") -> list["Entity"]:
        """Paginated list of all identified entities."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def show_entity_detail(self, service: "Service") -> "Entity":
        """Entity member view."""
        return await service.show()
