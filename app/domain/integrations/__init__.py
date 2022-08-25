from starlite import Provide, Router

from app.constants import Paths

from .controller import Controller
from .repository import Repository
from .service import Service
from .types import IntegrationEnum

router = Router(
    path=Paths.INTEGRATIONS,
    route_handlers=[Controller],
    dependencies={"service": Provide(Service.new)},
)

__all__ = [
    "Controller",
    "IntegrationEnum",
    "Repository",
    "Service",
    "model",
    "router",
    "schema",
]
