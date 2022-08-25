from typing import TYPE_CHECKING, Optional

from starlite import Dependency, Parameter

from app import core

from . import model, schema
from .repository import Repository

if TYPE_CHECKING:
    from uuid import UUID


class Service(core.Service[model.Entity, Repository, schema.Entity]):
    """Read only service for the root `entity` domain.

    CRUD operations must be performed through a provider's subdomain.
    """

    model = model.Entity
    repository_type = Repository
    schema = schema.Entity

    @classmethod
    async def new(
        cls,
        *,
        entity_id: Optional["UUID"] = Parameter(),
        filters: core.dependencies.Filters = Dependency(),
    ) -> "Service":
        """Creates a new service object.

        Parameters
        ----------
        entity_id : UUID | None
            If not `None` filters database queries by id.
        filters : core.dependencies.Filters
            Passed through to repository on instantiation and used to filter the query.

        Returns
        -------
        Service
        """
        return cls(id_=entity_id, filters=filters)
