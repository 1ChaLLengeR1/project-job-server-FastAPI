#!/bin/bash

if [ -z "$1" ]; then
    echo "Użycie: $0 [local|prod]"
    exit 1
fi

BASE_DIR="$(cd "$(dirname "$(realpath "$0")")/../../.." && pwd)"
ENV_FILE="$BASE_DIR/env/$1.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Plik środowiskowy $ENV_FILE nie istnieje!"
    exit 1
fi

source "$ENV_FILE"

if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_DBNAME" ]; then
    echo "Wszystkie zmienne środowiskowe muszą być ustawione w pliku $1.env"
    exit 1
fi

SQL_DIR="$BASE_DIR/database/sql"

if [ ! -f "$SQL_DIR/database_down.sql" ]; then
    echo "Plik $SQL_DIR/database_down.sql nie istnieje!"
    exit 1
fi

export PGPASSWORD="$DB_PASSWORD_SCRIPT"
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -f "$SQL_DIR/database_down.sql"

if [ $? -eq 0 ]; then
    echo "Migracja zakończona pomyślnie!"
else
    echo "Błąd podczas migracji."
    exit 1
fi
