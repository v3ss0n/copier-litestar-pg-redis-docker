# Pull base image
FROM python:3.10-slim

# Set shell pipefail
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Create working directory
RUN mkdir -p /workspace
WORKDIR /workspace

# Set python env vars
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set path
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install poetry
RUN apt-get update \
    && apt-get -y --no-install-recommends install curl \
    && curl -sSL https://install.python-poetry.org | python \
    && apt-get -y purge curl

# Install dependencies and tidy up
ARG poetry_options=""
COPY pyproject.toml ./
RUN apt-get update \
    && apt-get -y install --no-install-recommends libpq-dev python3-dev build-essential \
    && poetry install ${poetry_options} --no-root \
    && apt-get -y purge python3-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . ./

# Install app
RUN poetry install ${poetry_options}

CMD ["scripts/entry"]
