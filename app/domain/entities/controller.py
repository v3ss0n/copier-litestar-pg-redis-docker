from app.core import Controller as BaseController
from app.core import get, get_collection

from . import schema
from .service import Service


class Controller(BaseController):
    """
    Read-only view of all identified entities.

    Identification and modification must occur through the relevant provider sub-route, e.g.:
    `/providers/<provider_id>/entities`, etc.
    """

    tags = ["Entities"]
    member_path = "{entity_id:uuid}"

    @get_collection()
    async def list_all_entities(self, service: Service) -> list[schema.Entity]:
        """Paginated list of all identified entities."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def show_entity_detail(self, service: Service) -> schema.Entity:
        """Entity member view."""
        return await service.show()
