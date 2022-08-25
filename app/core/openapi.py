from pydantic_openapi_schema.v3_1_0 import Contact
from starlite import OpenAPIConfig

config = OpenAPIConfig(
    title="provider-integrations",
    version="1.0.0",
    contact=Contact(name="Peter Schutt", email="peter.github@proton.me"),
    description="Central interface through which  providers can do stuff to our core.",
)
