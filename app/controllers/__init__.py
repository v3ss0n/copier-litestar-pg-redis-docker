from litestar import Router

from app.domain.authors import Author
from app.domain.countries import Country
from app.domain.projects import Project

from . import authors, countries, projects

__all__ = ["create_router"]


def create_router() -> Router:
    return Router(
        path="/v1",
        route_handlers=[authors.AuthorController, countries.CountryController, projects.ApiController],
        signature_namespace={"Author": Author, "Country": Country, "Project": Project},
    )
