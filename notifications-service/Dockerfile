FROM python:3.11-slim AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry==2.2.1 && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-root

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY ./src/notifications_service .

EXPOSE 8000

CMD ["faststream", "run", "faststream_app:faststream_app"]
