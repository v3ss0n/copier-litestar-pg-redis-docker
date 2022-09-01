from starlite import Controller as BaseController
from starlite import delete, get, put

from app.core.handlers import create_pagination_dependencies, resolve_id_guards
from app.domain.entities.schema import Entity

from .service import Service


class Controller(BaseController):
    tags = ["Provider-Entities"]
    member_path = "{entity_id:uuid}"

    @get(dependencies=create_pagination_dependencies())
    async def list_provider_entities(self, service: Service) -> list[Entity]:
        """Paginated list of provider's entities."""
        return await service.list()

    @get(path=member_path, cache=True)
    async def get_provider_entity(self, service: Service) -> Entity:
        """Provider entity member view."""
        return await service.show()

    @put(path=member_path, guards=resolve_id_guards([("provider_id", "provider_id"), "entity_id"]))
    async def register_provider_entity(self, data: Entity, service: Service) -> Entity:
        """Register, or update a provider entity."""
        return await service.upsert(data=data)

    @delete(path=member_path)
    async def delete_provider_entity(self, service: Service) -> None:
        """Delete the provider entity."""
        await service.destroy()
