from starlite import Router

from .controllers import UserController

v1_router = Router(path="/v1", route_handlers=[UserController])
