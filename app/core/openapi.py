from openapi_schema_pydantic import Contact
from starlite import OpenAPIConfig

config = OpenAPIConfig(
    title="provider-integrations",
    version="1.0.0",
    contact=Contact(name="Peter Schutt", email="peter@topsport.com.au"),
    description="Central interface through which  providers can do stuff to our core.",
)
