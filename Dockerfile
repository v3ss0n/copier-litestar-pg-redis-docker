FROM python:3.10-slim AS install
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl git \
    && apt-get autoremove -y
RUN pip install --upgrade pip
WORKDIR /app/
# install poetry and keep the get-poetry script so it can be reused later.
ENV POETRY_HOME="/opt/poetry"
RUN curl https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py > get-poetry.py
RUN python get-poetry.py

FROM install AS app-image
# allow controlling the poetry installation of dependencies via external args
ARG INSTALL_ARGS="--no-dev"
WORKDIR /app/
# let poetry know where its installed and add the poetry bin to the path
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
COPY . .
# install without virtualenv, since we are inside a continer, follow by cleanup
RUN poetry config virtualenvs.create false \
    && poetry install $INSTALL_ARGS \
    && python get-poetry.py --uninstall \
    && rm get-poetry.py
# cleanup curl, git and apt cache
RUN apt-get purge -y curl git \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*
# switch to a non-root user for security
RUN addgroup --system --gid 1001 "app-user"
RUN adduser --system --uid 1001 "app-user"
USER "app-user"
