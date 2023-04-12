from litestar import Router

from app.domain.authors import Author
from app.domain.country import Country

from . import authors, country

__all__ = ["create_router"]


def create_router() -> Router:
    return Router(
        path="/v1",
        route_handlers=[authors.AuthorController, country.CountryController],
        signature_namespace={"Author": Author, "Country": Country},
    )
