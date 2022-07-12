from app.core import Controller as BaseController
from app.core import delete, get, get_collection, put
from app.domain.integrations import schema

from .service import Service


class Controller(BaseController):
    tags = ["Provider-Integrations"]
    member_path = "{integration_type:str}"

    @get_collection()
    async def list_provider_integrations(self, service: Service) -> list[schema.Integration]:
        """Paginated list of provider's integrations."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def show_provider_integration(self, service: Service) -> schema.Integration:
        """Provider integration member view."""
        return await service.show()

    @put(
        path=member_path,
        id_guard=[("provider_id", "provider_id"), ("type", "integration_type")],
    )
    async def register_integration(
        self, data: schema.Integration, service: Service
    ) -> schema.Integration:
        """Register, or update a provider integration."""
        return await service.upsert(data=data)

    @delete(path=member_path)
    async def delete_integration(self, service: Service) -> schema.Integration:
        """Delete the provider integration."""
        return await service.destroy()
