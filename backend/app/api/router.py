from starlite import Router

from .controllers import UserController

router = Router(path="/v1", route_handlers=[UserController])
