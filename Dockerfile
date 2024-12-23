FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .
