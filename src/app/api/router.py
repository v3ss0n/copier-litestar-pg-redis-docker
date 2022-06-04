from starlite import Router

from app.config import Paths

from .items import item_router
from .users import user_router

user_router.register(item_router)
v1_router = Router(path=Paths.V1, route_handlers=[user_router])
