from uuid import UUID

from starlite import Dependency, Parameter
from starlite.exceptions import ValidationException

from app.core.dependencies import Filters
from app.domain import entities


class Service(entities.Service):
    async def upsert(self, data: entities.schema.Entity) -> entities.schema.Entity:
        if data.type == entities.EntitiesEnum.competitor and data.extra.sub_entity is None:
            raise ValidationException(
                "Competitors must have the team or sport-person entity they represent in `extra.sub_entity`"
            )
        return await super().upsert(data)

    @classmethod
    async def new(
        cls,
        *,
        provider_id: UUID = Parameter(),
        entity_id: UUID | None = Parameter(),
        filters: Filters = Dependency(),
    ) -> "Service":
        """Creates a new service object.

        Parameters
        ----------
        provider_id : UUID
            ID of provider that owns the entity, required.
        entity_id : UUID | None
            Filters the query by id if not `None`
        filters : core.dependencies.Filters
            Passed through to repository on instantiation and used to filter the query.

        Returns
        -------
        Service
        """
        inst = cls(id_=entity_id, filters=filters)
        inst.repository.filter_select_by_kwargs(provider_id=provider_id)
        return inst
