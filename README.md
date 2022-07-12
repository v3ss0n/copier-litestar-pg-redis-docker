<img alt="Starlite logo" src="./static/starlite-banner.svg" width="100%" height="auto">

# starlite-pg-redis-docker

A WIP Starlite API Implementation.

## TODO

- [ ] Header/cookie parameter example.
- [ ] CI?
- [ ] Profile

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
- `$ docker-compose build`
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
