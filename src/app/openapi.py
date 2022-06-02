from openapi_schema_pydantic import Contact, License, Tag
from starlite import OpenAPIConfig

config = OpenAPIConfig(
    title="starlite-pg-redis-docker",
    version="1.0.0",
    contact=Contact(name="Peter Schutt", email="peter.github@proton.me"),
    description="Example Starlite Backend Stack.",
    license=License(
        name="MIT",
        url="https://github.com/starlite-api/starlite-pg-redis-docker/blob/main/LICENSE",
    ),
    tags=[
        Tag(name="Users", description="Create, modify and delete User objects."),
        Tag(name="User-Items", description="Create, modify and delete a User's Items."),
        Tag(name="Misc", description="Health check, etc."),
    ],
)
