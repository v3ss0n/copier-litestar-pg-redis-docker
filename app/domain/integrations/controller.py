from typing import TYPE_CHECKING

from starlite import Controller as BaseController
from starlite import get

from app.core.handlers import create_pagination_dependencies

from .service import Service

if TYPE_CHECKING:
    from .schema import Integration


class Controller(BaseController):
    """Read-only view of all integrations.

    Identification and modification must occur through the relevant
    provider sub-route, e.g.: `/providers/<provider_id>/integrations`,
    etc.
    """

    tags = ["Integrations"]
    member_path = "{integration_id:uuid}"

    @get(dependencies=create_pagination_dependencies())
    async def list_all_integrations(self, service: Service) -> list["Integration"]:
        """Paginated list of all integrations."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def integration_detail(self, service: Service) -> "Integration":
        """Integration member view."""
        return await service.show()
