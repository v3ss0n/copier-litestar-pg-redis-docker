from app.core import Controller as BaseController
from app.core import delete, get, get_collection, put

from . import schema
from .service import Service


class Controller(BaseController):
    tags = ["Providers"]
    member_path = "{provider_id:uuid}"

    @get_collection()
    async def list_providers(self, service: Service) -> list[schema.Provider]:
        """A paginated list of all registered providers"""
        return await service.list()

    @get(path=member_path)
    async def get_provider(self, service: Service) -> schema.Provider:
        """Individual provider detail view."""
        return await service.show()

    @put(path=member_path, id_guard="provider_id")
    async def register_provider(self, data: schema.Provider, service: Service) -> schema.Provider:
        """Register, or update a provider"""
        return await service.upsert(data=data)

    @delete(path=member_path)
    async def delete_provider(self, service: Service) -> schema.Provider:
        """Delete the provider and return its representation"""
        return await service.destroy()
