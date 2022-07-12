from app.core import Controller as BaseController
from app.core import delete, get, get_collection, put
from app.domain.entities import schema

from .service import Service


class Controller(BaseController):
    tags = ["Provider-Entities"]
    member_path = "{entity_id:uuid}"

    @get_collection()
    async def list_provider_entities(self, service: Service) -> list[schema.Entity]:
        """Paginated list of provider's entities."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def get_provider_entity(self, service: Service) -> schema.Entity:
        """Provider entity member view."""
        return await service.show()

    @put(path=member_path, id_guard=[("provider_id", "provider_id"), "entity_id"])
    async def register_provider_entity(
        self, data: schema.Entity, service: Service
    ) -> schema.Entity:
        """Register, or update a provider entity."""
        return await service.upsert(data=data)

    @delete(path=member_path)
    async def delete_provider_entity(self, service: Service) -> schema.Entity:
        """Delete the provider entity."""
        return await service.destroy()
