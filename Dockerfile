# Pull base image
FROM python:3.10

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.12

WORKDIR /backend/

# Install dependencies
RUN python3 -m pip install "poetry==${POETRY_VERSION}"
COPY poetry.lock pyproject.toml /backend/
RUN poetry install

COPY ./backend /backend/

RUN alembic upgrade head

EXPOSE 8000