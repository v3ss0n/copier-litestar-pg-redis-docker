from starlite import Provide, Router

from app.config import Paths

from .controller import Controller
from .service import Service

__all__ = ["Controller", "Service", "router"]

router = Router(
    path=Paths.PROVIDER_INTEGRATIONS,
    route_handlers=[Controller],
    dependencies={"service": Provide(Service.new)},
)
