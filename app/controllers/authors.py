# ruff: noqa: B008
from __future__ import annotations

from typing import TYPE_CHECKING

from starlite import Router, delete, get, post, put
from starlite.di import Provide
from starlite.params import Dependency
from starlite.status_codes import HTTP_200_OK

from app.domain.authors import Author, ListDTO, ReadDTO, Repository, Service, WriteDTO

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession
    from starlite.contrib.repository.abc import FilterTypes

__all__ = ["create_author", "delete_author", "get_author", "get_authors", "provides_service", "update_author"]


DETAIL_ROUTE = "/{author_id:uuid}"


def provides_service(db_session: AsyncSession) -> Service:
    """Constructs repository and service objects for the request."""
    return Service(Repository(session=db_session))


@get(return_dto=ListDTO)
async def get_authors(service: Service, filters: list[FilterTypes] = Dependency(skip_validation=True)) -> list[Author]:
    """Get a list of authors."""
    return await service.list(*filters)


@post(data_dto=WriteDTO, return_dto=ReadDTO)
async def create_author(data: Author, service: Service) -> Author:
    """Create an `Author`."""
    return await service.create(data)


@get(DETAIL_ROUTE, return_dto=ReadDTO)
async def get_author(service: Service, author_id: UUID) -> Author:
    """Get Author by ID."""
    return await service.get(author_id)


@put(DETAIL_ROUTE, data_dto=WriteDTO, return_dto=ReadDTO)
async def update_author(data: Author, service: Service, author_id: UUID) -> Author:
    """Update an author."""
    return await service.update(author_id, data)


@delete(DETAIL_ROUTE, status_code=HTTP_200_OK, return_dto=ReadDTO)
async def delete_author(service: Service, author_id: UUID) -> Author:
    """Delete Author by ID."""
    return await service.delete(author_id)


router = Router(
    path="/authors",
    route_handlers=[get_authors, create_author, get_author, update_author, delete_author],
    dependencies={"service": Provide(provides_service)},
    tags=["Authors"],
)
