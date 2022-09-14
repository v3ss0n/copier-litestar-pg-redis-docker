from pydantic_openapi_schema.v3_1_0 import Contact
from starlite.config import OpenAPIConfig
from starlite.openapi.controller import OpenAPIController as _OpenAPIController

from .constants import FAVICON_PATH


class OpenAPIController(_OpenAPIController):
    favicon_url = FAVICON_PATH


config = OpenAPIConfig(
    title="provider-integrations",
    version="1.0.0",
    contact=Contact(name="Peter Schutt", email="peter.github@proton.me"),
    description="Central interface through which providers can do stuff to our core.",
    openapi_controller=OpenAPIController,
)
