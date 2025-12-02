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

COPY ./src/users_service .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
