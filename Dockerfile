FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry lock

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --only main

COPY ./app ./app

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "cd app/database && poetry run alembic upgrade head && cd ../.. && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /app/app"]