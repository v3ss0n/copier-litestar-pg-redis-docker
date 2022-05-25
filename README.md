<img alt="Starlite logo" src="./static/starlite-banner.svg" width="100%" height="auto"> 

# backend-starlite-postgres

Warning this example project is a WIP.

## TODO
- [x] Audit config files, include in pyproject.toml if possible and ensure no unnecessary config included
- [x] Change .env to .env.example and add .env to .gitignore
- [x] Add .dockerignore
- [x] Make all environment variables non optional and include in .env.example
- [x] Usage documentation in README
- [x] Pydantic settings for gunicorn for consistency and simplify
- [x] Add dev deps
- [x] Create test runner script
- [x] Add src/ directory
- [x] Use gunicorn in entry script
- [x] Make app installable
- [x] Fix runtime errors
- [x] Make the database session commit scope outside of request handling scope
- [x] Documentation
- [x] Make repositories more helpful (raise NotFoundExceptions, return Pydantic Models etc)
- [x] Document `RestartableUvicornWorker`.
- [x] Expand tests
- [x] Isolate tests from database
- [x] Remove need for sync database uri and driver (entry script and migrations)
- [x] Change to only require database uri in environment
- [x] Cache sets URL via environment, DB URL is build inside app, make consistent.
- [x] Register cache backend and use it on a route
- [ ] Handle mismatch between url parameter id and payload id value
- [ ] Add nested items routes

### Post Fork
Things to do to project after I fork off for internal use.

- [ ] CI?
- [ ] explicitly include any dirs/files into docker and remove .dockerignore
- [ ] add pre-commit (I'll just make as equivalent as possible to the original pre-commit config in this project)
- [ ] configure pyupgrade for only --py310-plus
- [ ] use the Dockerfile from https://gist.github.com/Goldziher/942f4a027a7fa1e2cafaa35e0333b6dc
- [ ] remove black and isort from alembic hooks
- [ ] map docker ports to service defaults
- [ ] add pylint into tooling
- [ ] black and isort settings as per original

## Starlite

Starlite is a light and flexible ASGI API framework. 

[Starlite documentation 📚](https://starlite-api.github.io/starlite/)

### RestartableUvicornWorker

There is a known issue when running gunicorn with uvicorn workers, see 
[here](https://github.com/benoitc/gunicorn/issues/2339).

For convenience an implementation of the workaround 
([this one](https://github.com/benoitc/gunicorn/issues/2339#issuecomment-867481389))
suggested in that gunicorn issue is included in the application source.

To use the included `RestartableUvicornWorker` set the `GUNICORN_WORKER_CLASS` env var
to `app.utils.restartable_worker.RestartableUvicornWorker`.

In production, set the `GUNICORN_WORKER_CLASS` env var to `uvicorn.workers.UvicornWorker`
as advised [here](https://www.uvicorn.org/deployment/).

### Setup

- `$ cp .env.example .env`
- `$ docker-compose run --rm app alembic upgrade head`

### Run

`$ docker-compose up --build`

### Test

`$ docker-compose run --rm app scripts/tests`

### Format

#### black

`$ docker-compose run --rm app black .` 

#### isort

`$ docker-compose run --rm app isort .`

### Add Dependencies

#### Production 

`$ docker-compose run --rm app poetry add <dependency>`

#### Dev

`$ docker-compose run --rm app poetry add <dependency> --dev`

#### Rebuild

`$ docker-compose build`

### Migrations

#### Ensure the database service is up

`$ docker-compose up -d db`

#### Revision
`$ docker-compose run --rm app alembic revision --autogenerate -m "revision description"`

May have issue with permissions after having docker generate the revision file, to fix:

`$ sudo chown <user> ./alembic/versions/<filename>.py`

#### Migration
`$ docker-compose run --rm app alembic upgrade head`
