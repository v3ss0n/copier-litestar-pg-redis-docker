from starlite import Router

from app.domain.authors import Author

from . import authors

__all__ = ["router"]

router = Router(path="/v1", route_handlers=[authors.router], signature_namespace={"Author": Author})
