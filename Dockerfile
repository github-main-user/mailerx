FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-root

COPY . /app
