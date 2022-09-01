from starlite import Controller as BaseController
from starlite import get

from app.core.handlers import create_pagination_dependencies

from .schema import Integration
from .service import Service


class Controller(BaseController):
    """Read-only view of all integrations.

    Identification and modification must occur through the relevant
    provider sub-route, e.g.: `/providers/<provider_id>/integrations`,
    etc.
    """

    tags = ["Integrations"]
    member_path = "{integration_id:uuid}"

    @get(dependencies=create_pagination_dependencies())
    async def list_all_integrations(self, service: Service) -> list[Integration]:
        """Paginated list of all integrations."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def integration_detail(self, service: Service) -> Integration:
        """Integration member view."""
        return await service.show()
