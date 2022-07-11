from starlite import Provide, Router

from app.core.dependencies import filters

from . import entities, integrations, providers

__all__ = [
    "entities",
    "integrations",
    "model",
    "providers",
    "router",
]

router = Router(
    path="",
    dependencies={"filters": Provide(filters)},
    route_handlers=[entities.router, integrations.router, providers.router],
)
