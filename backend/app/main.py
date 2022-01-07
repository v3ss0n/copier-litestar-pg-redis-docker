from starlite import Starlite

import app.controllers.v1 as V1Router

app = Starlite(route_handlers=[V1Router])
