FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Ustawienia środowiskowe
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PYTHON_DOWNLOADS=never
# venv poza /app, żeby bind-mount kodu nie nadpisywał środowiska
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Pakiety systemowe: libpq-dev+gcc dla psycopg2, postgresql-client dla
# skryptów migracji (docker_entrypoint.sh) i debugowania
RUN apt-get update && apt-get install -y \
    libpq-dev gcc postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Najpierw same zależności (cache warstwy przy zmianach w kodzie)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --extra prod --no-install-project

# Kopiowanie aplikacji
COPY . /app
RUN uv sync --frozen --no-dev --extra prod

ENV PATH="/opt/venv/bin:$PATH"

# Uruchamianie FastAPI
CMD ["gunicorn", "main:app", "-c", "config/gunicorn.py"]
