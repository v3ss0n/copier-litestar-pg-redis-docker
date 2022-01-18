# Pull base image
FROM python:3.10
WORKDIR /app/
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.12
RUN python3 -m pip install "poetry==${POETRY_VERSION}"
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini pyproject.toml .env ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-dev
