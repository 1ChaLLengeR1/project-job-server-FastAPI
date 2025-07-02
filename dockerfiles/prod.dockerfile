FROM python:3.10-slim

# Ustawienia środowiskowe
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

RUN pip install gunicorn

# Kopiowanie aplikacji
COPY . /app

# Uruchamianie FastAPI
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:3000", "-w", "1"]
