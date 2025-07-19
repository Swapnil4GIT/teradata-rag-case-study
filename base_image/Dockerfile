FROM python:3.11-slim

WORKDIR /opt/app

ARG POETRY_VERSION=1.8.4
RUN pip install --no-cache-dir --upgrade pip \
    && pip install poetry==$POETRY_VERSION

RUN mkdir -p base_image
RUN touch base_image/__init__.py
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry config virtualenvs.create false \
    && poetry install