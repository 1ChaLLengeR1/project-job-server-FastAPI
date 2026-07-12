#!/bin/bash
# Robi dump bazy wskazanej w env/<ENV>.env.
# Uzycie: bash infra/scripts/database/dump.sh local [full|data] [plik_wyjsciowy]
#   full (domyslnie) - format custom (-Fc), do odtwarzania przez pg_restore. Nie trzyma sie w gicie.
#   data             - plain SQL, tylko dane, bez alembic_version. Czytelne w code review, wersjonowalne.
set -uo pipefail

show_error() {
    echo "================================"
    echo "BŁĄD: $1"
    echo "================================"
    exit 1
}

show_info() { echo "INFO: $1"; }

if [ -z "${1:-}" ]; then
    echo "Użycie: $0 [local|prod] [full|data] [plik_wyjsciowy]"
    exit 1
fi

ENV="$1"
MODE="${2:-full}"

case "$MODE" in
    full|data) ;;
    *) show_error "Nieznany tryb '$MODE'. Dostepne: full, data" ;;
esac

PROJECT_ROOT="$(cd "$(dirname "$(realpath "$0")")/../../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/env/$ENV.env"

if [ ! -f "$ENV_FILE" ]; then
    show_error "Plik środowiskowy $ENV_FILE nie istnieje!"
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

for var in DB_HOST DB_PORT DB_USER DB_PASSWORD DB_DBNAME; do
    if [ -z "${!var:-}" ]; then
        show_error "$var nie jest ustawione w pliku $ENV.env"
    fi
done

export PGPASSWORD="$DB_PASSWORD"

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$PROJECT_ROOT/backups"

if [ "$MODE" = "full" ]; then
    OUT="${3:-$BACKUP_DIR/${DB_DBNAME}_${ENV}_${STAMP}.dump}"
else
    OUT="${3:-$BACKUP_DIR/${DB_DBNAME}_${ENV}_${STAMP}_data.sql}"
fi

mkdir -p "$(dirname "$OUT")"

show_info "Środowisko: $ENV (baza $DB_DBNAME @ $DB_HOST:$DB_PORT)"
show_info "Tryb: $MODE"
show_info "Plik wyjściowy: $OUT"

# Wspolne flagi:
#   --no-owner / --no-privileges - dump ma sie wgrywac na dowolnego usera (lokalny != produkcyjny)
#   --exclude-table=alembic_version - wersje schematu trzyma Alembic w repo, nie dump
COMMON=(
    -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d "$DB_DBNAME"
    --no-owner --no-privileges
    --exclude-table=alembic_version
)

if [ "$MODE" = "full" ]; then
    # Format custom: skompresowany, odtwarzany przez pg_restore (rownolegle, selektywnie).
    if ! pg_dump "${COMMON[@]}" -Fc -f "$OUT"; then
        show_error "pg_dump nie powiódł się."
    fi
else
    # Plain SQL, same dane. --inserts zamiast COPY: wolniejsze, ale czytelne w diffie
    # i odporne na roznice wersji serwera. Bez --create/--clean - baze robi Alembic.
    if ! pg_dump "${COMMON[@]}" --data-only --inserts --column-inserts -f "$OUT"; then
        show_error "pg_dump nie powiódł się."
    fi
fi

show_info "✓ Dump gotowy: $OUT ($(du -h "$OUT" | cut -f1))"

if [ "$MODE" = "full" ]; then
    echo "Odtworzenie:  pg_restore --no-owner --no-privileges -d <baza> -j 4 $OUT"
else
    echo "Odtworzenie:  bash infra/scripts/database/seed_from_dump.sh $ENV $OUT"
fi
