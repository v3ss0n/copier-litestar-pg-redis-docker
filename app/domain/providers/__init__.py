from starlite import Provide, Router

from app.constants import Paths

from . import entities, integrations
from .controller import Controller
from .repository import Repository
from .service import Service

__all__ = [
    "Controller",
    "Repository",
    "Service",
    "entities",
    "integrations",
    "model",
    "router",
    "schema",
]

router = Router(
    path=Paths.PROVIDERS,
    route_handlers=[Controller, entities.router, integrations.router],
    dependencies={"service": Provide(Service.new)},
)
