FROM python:3.11-slim-bullseye AS base

# renovate: datasource=github-releases depName=python-poetry/poetry extractVersion=^(?<version>.*)$
ARG POETRY_VERSION=1.6.0

RUN apt-get update && \
    # libpq-dev for psycopg
    apt-get install -y --no-install-recommends curl libpq-dev && \
    apt-get clean && \
    (rm -rf /var/lib/apt/lists/* || true)


RUN curl -sSL https://install.python-poetry.org > install-poetry.py && \
    POETRY_VERSION=${POETRY_VERSION} python3 install-poetry.py

ENV PATH="${PATH}:/root/.local/bin"

FROM base AS prod

WORKDIR /usr/app

COPY murkelhausen_app murkelhausen_app
COPY murkelhausen_info murkelhausen_info
COPY statements statements
COPY trainer trainer
COPY pages pages
COPY chat chat
COPY static static
COPY manage.py entrypoint.sh pyproject.toml poetry.lock* README.md ./

RUN poetry config installer.max-workers 10 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000

# TODO create real user and install poetry into its home directory
#USER 1000
