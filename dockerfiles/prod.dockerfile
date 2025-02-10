FROM python:3.10-slim

# Ustawienia środowiskowe
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalacja wymaganych pakietów systemowych dla psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie pliku requirements.txt
COPY ./../requirements.txt /app/requirements.txt

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie aplikacji
COPY . /app

# Uruchamianie FastAPI
CMD ["uvicorn", "main:app", "--reload", "--log-level", "debug", "--host", "0.0.0.0", "--port", "3000"]
