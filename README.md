<img alt="Starlite logo" src="./static/starlite-banner.svg" width="100%" height="auto">

# starlite-pg-redis-docker

A WIP Starlite API Implementation.

## TODO

- [ ] Header/cookie parameter example.
- [ ] CI?
- [ ] Profile
- [ ] Profile alternate UUID implementation (https://github.com/MagicStack/py-pgproto/blob/a4178145cd7cc3a44eee20cfc9e8b94a7fed2053/uuid.pyx)
- [ ] Gunicorn logconfig ignore sqlalchemy.engine logs
- [ ] explicitly include any dirs/files into docker and remove .dockerignore
- [ ] add pre-commit (I'll just make as equivalent as possible to the original pre-commit config in this project)
- [ ] configure pyupgrade for only --py310-plus
- [ ] use the Dockerfile from https://gist.github.com/Goldziher/942f4a027a7fa1e2cafaa35e0333b6dc
- [ ] remove black and isort from alembic hooks
- [ ] map docker ports to service defaults
- [ ] add pylint into tooling
- [ ] black and isort settings as per original
- [ ] websocket example project with simple front end???

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

- `pre-commit install`
- `$ cp .env.example .env`
- `$ docker-compose run --rm app alembic upgrade head`

### Run

`$ docker-compose up --build`

### Migrations

#### Revision

`$ docker-compose run --rm app alembic revision --autogenerate -m "revision description"`

#### Migration

`$ docker-compose run --rm app alembic upgrade head`

### Test

`$ poetry run pytest`

### Linting

`$ pre-commit run --all-files`

### Add Dependencies

#### Production

`$ poetry add starlite`

#### Dev

`$ poetry add starlite --extras=testing --dev`
