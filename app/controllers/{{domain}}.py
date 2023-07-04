# ruff: noqa: B008
from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK

from app.domain.{{domain|lower}}s import ReadDTO, Repository, Service, WriteDTO

if TYPE_CHECKING:
    from uuid import UUID

    from litestar.contrib.repository import FilterTypes
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.domain.{{domain|lower}}s import {{domain|capfirst}} 

__all__ = [
    "Controller",
]

DETAIL_ROUTE = "/{item_id:uuid}"


def provides_service(db_session: AsyncSession) -> Service:
    """Constructs repository and service objects for the request."""
    return Service(Repository(session=db_session))


class Controller(Controller):
    dto = WriteDTO
    return_dto = ReadDTO
    path = "/{{domain|lower}}s"
    dependencies = {"service": Provide(provides_service, sync_to_thread=False)}
    tags = ["{{domain|lower}}s"]

    @get()
    async def list(
        self, service: Service, filters: list[FilterTypes] = Dependency(skip_validation=True)
    ) -> list[{{domain|capfirst}}]:
        """Get a list of {{domain|capfirst}}."""
        return await service.list(*filters)

    @post()
    async def create(self, data: {{domain|capfirst}}, service: Service) -> {{domain|capfirst}}:
        """Create an `{{domain|capfirst}}`."""
        return await service.create(data)

    @get(DETAIL_ROUTE)
    async def retrive(self, service: Service, item_id: UUID) -> {{domain|capfirst}}:
        """Get {{domain|capfirst}} by ID."""
        return await service.get(item_id)

    @put(DETAIL_ROUTE)
    async def update(self, data: {{domain|capfirst}}, service: Service, item_id: UUID) -> {{domain|capfirst}}:
        """Update an {{domain|capfirst}}."""
        return await service.update(item_id, data)

    @delete(DETAIL_ROUTE, status_code=HTTP_200_OK)
    async def delete(self, service: Service, item_id: UUID) -> {{domain|capfirst}}:
        """Delete {{domain|capfirst}} by ID."""
        return await service.delete(item_id)
