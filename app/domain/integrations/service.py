from uuid import UUID

from starlite import Dependency, Parameter

from app import core

from . import model, schema
from .repository import Repository


class Service(core.Service[model.Integration, Repository, schema.Integration]):
    """
    Read only service for the root `integration` domain. CRUD operations must be performed through a
    provider's subdomain.
    """

    model = model.Integration
    repository_type = Repository
    schema = schema.Integration

    @classmethod
    async def new(
        cls,
        *,
        integration_id: UUID | None = Parameter(),
        filters: core.dependencies.Filters = Dependency(),
    ) -> "Service":
        """
        Creates a new service object.

        Parameters
        ----------
        integration_id : UUID | None
            If not `None` filters database queries by id.
        filters : core.dependencies.Filters
            Passed through to repository on instantiation and used to filter the query.

        Returns
        -------
        Service
        """
        return cls(id_=integration_id, filters=filters)
