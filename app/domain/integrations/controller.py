from app.core import Controller as BaseController
from app.core import get, get_collection

from . import schema
from .service import Service


class Controller(BaseController):
    """
    Read-only view of all integrations.

    Identification and modification must occur through the relevant provider sub-route, e.g.:
    `/providers/<provider_id>/integrations`, etc.
    """

    tags = ["Integrations"]
    member_path = "{integration_id:uuid}"

    @get_collection()
    async def list_all_integrations(self, service: Service) -> list[schema.Integration]:
        """Paginated list of all integrations."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def integration_detail(self, service: Service) -> schema.Integration:
        """Integration member view."""
        return await service.show()
