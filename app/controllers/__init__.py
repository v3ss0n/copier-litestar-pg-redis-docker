from litestar import Router

from app.domain.authors import Author

from . import authors

__all__ = ["create_router"]


def create_router() -> Router:
    return Router(path="/v1", route_handlers=[authors.AuthorController], signature_namespace={"Author": Author})
