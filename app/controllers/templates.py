# ruff: noqa: B008
from __future__ import annotations

from typing import TYPE_CHECKING

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK

from app.domain.templates import ListDTO, ReadDTO, Repository, Service, WriteDTO

if TYPE_CHECKING:
    from uuid import UUID

    from litestar.contrib.repository.abc import FilterTypes
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.domain.templates import Template

__all__ = [
    "TemplateController",
]

DETAIL_ROUTE = "/{template_id:uuid}"


def provides_service(db_session: AsyncSession) -> Service:
    """Constructs repository and service objects for the request."""
    return Service(Repository(session=db_session))


class TemplateController(Controller):
    dto = WriteDTO
    return_dto = ReadDTO
    path = "/templates"
    dependencies = {"service": Provide(provides_service)}
    tags = ["Templates"]

    @get(return_dto=ListDTO)
    async def filter(
        self, service: Service, filters: list[FilterTypes] = Dependency(skip_validation=True)
    ) -> list[Template]:
        """Get a list of templates."""
        return await service.list(*filters)

    @post()
    async def create(self, data: Template, service: Service) -> Template:
        """Create an `Template`."""
        return await service.create(data)

    @get(DETAIL_ROUTE)
    async def retrieve(self, service: Service, template_id: UUID) -> Template:
        """Get Template by ID."""
        return await service.get(template_id)

    @put(DETAIL_ROUTE)
    async def update(self, data: Template, service: Service, template_id: UUID) -> Template:
        """Update an template."""
        return await service.update(template_id, data)

    @delete(DETAIL_ROUTE, status_code=HTTP_200_OK)
    async def delete(self, service: Service, template_id: UUID) -> Template:
        """Delete Template by ID."""
        return await service.delete(template_id)
