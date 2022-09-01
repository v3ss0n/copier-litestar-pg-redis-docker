from starlite import Controller as BaseController
from starlite import delete, get, put

from app.core.handlers import create_pagination_dependencies, resolve_id_guards
from app.domain.integrations.schema import Integration

from .service import Service


class Controller(BaseController):
    tags = ["Provider-Integrations"]
    member_path = "{integration_type:str}"

    @get(dependencies=create_pagination_dependencies())
    async def list_provider_integrations(self, service: Service) -> list[Integration]:
        """Paginated list of provider's integrations."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def show_provider_integration(self, service: Service) -> Integration:
        """Provider integration member view."""
        return await service.show()

    @put(
        path=member_path,
        guards=resolve_id_guards([("provider_id", "provider_id"), ("type", "integration_type")]),
    )
    async def register_integration(self, data: Integration, service: Service) -> Integration:
        """Register, or update a provider integration."""
        return await service.upsert(data=data)

    @delete(path=member_path)
    async def delete_integration(self, service: Service) -> None:
        """Delete the provider integration."""
        await service.destroy()
