FROM python:3.10-slim-bullseye AS poetry

ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /tmp

COPY poetry.lock pyproject.toml ./

RUN poetry export -f requirements.txt --output /tmp/requirements.txt

FROM python:3.10-slim-bullseye

COPY --from=poetry /tmp/requirements.txt /tmp

ENV PYTHONPATH=/app

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update -y && apt install -y libmagic1 \
    && pip install -r /tmp/requirements.txt

WORKDIR /app

COPY . /app

CMD exec uvicorn --port $PORT --host 0.0.0.0 main:app
