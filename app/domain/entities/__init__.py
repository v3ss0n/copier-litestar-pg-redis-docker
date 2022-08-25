from starlite import Provide, Router

from app.constants import Paths

from .controller import Controller
from .repository import Repository
from .service import Service
from .types import EntitiesEnum

router = Router(
    path=Paths.ENTITIES,
    route_handlers=[Controller],
    dependencies={"service": Provide(Service.new)},
)


__all__ = [
    "Controller",
    "Repository",
    "Service",
    "EntitiesEnum",
    "model",
    "router",
    "schema",
]
