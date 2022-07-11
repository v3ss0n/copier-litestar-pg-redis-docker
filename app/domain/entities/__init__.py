# flake8: noqa
from starlite import Provide, Router

from app.config import Paths

from .controller import Controller
from .repository import Repository
from .service import Service
from .types import EntitiesEnum

__all__ = [
    "Controller",
    "Repository",
    "Service",
    "EntitiesEnum",
    "model",
    "router",
    "schema",
]

router = Router(
    path=Paths.ENTITIES,
    route_handlers=[Controller],
    dependencies={"service": Provide(Service.new)},
)
