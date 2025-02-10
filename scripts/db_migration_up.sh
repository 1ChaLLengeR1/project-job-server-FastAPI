#!/bin/bash

source ../env/local.env
#source ../env/prod.env

if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_DBNAME" ]; then
    echo "Wszystkie zmienne środowiskowe muszą być ustawione w pliku local.env"
    sleep 10
    exit 1
fi

if [ ! -f ../database/sql/database_up.sql ]; then
    echo "Plik ./database/sql/database_up.sql nie istnieje!"
    sleep 10
    exit 1
fi


export PGPASSWORD="$DB_PASSWORD_SCRIPT"
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -f "../database/sql/database_up.sql"
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -f "../database/sql/users.sql"
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -f "../database/sql/key_calculator.sql"


if [ $? -eq 0 ]; then
    echo "Migracja zakończona pomyślnie!"
else
    echo "Błąd podczas migracji."
    sleep 10
    exit 1
fi

echo "Skrypt zakończy się za 5 sekund..."
sleep 5

