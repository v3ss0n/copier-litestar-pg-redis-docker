# flake8: noqa
from starlite import Provide, Router

from app.config import Paths

from .controller import Controller
from .repository import Repository
from .service import Service
from .types import IntegrationEnum

__all__ = [
    "Controller",
    "IntegrationEnum",
    "Repository",
    "Service",
    "model",
    "router",
    "schema",
]

router = Router(
    path=Paths.INTEGRATIONS,
    route_handlers=[Controller],
    dependencies={"service": Provide(Service.new)},
)
