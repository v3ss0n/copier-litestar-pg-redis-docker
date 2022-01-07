from starlite import Starlite, OpenAPIConfig, OpenAPIController, get
from starlite.controller import Controller

# import app.controllers.v1 as V1Router
from app.controllers.v1.user import UserController

app = Starlite(
    route_handlers=[OpenAPIController, UserController],
    openapi_config=OpenAPIConfig(title="API", version="1.0.0"),
)
