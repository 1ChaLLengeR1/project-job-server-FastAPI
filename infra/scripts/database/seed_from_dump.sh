#!/bin/bash
# Wgrywa dane z dumpow pg_dump (data-only) do bazy wskazanej w env/<ENV>.env.
# Uruchamiac PO migration_restart - dumpy nie zawieraja DDL, tylko INSERT-y.
# Uzycie: bash infra/scripts/database/seed_from_dump.sh local [plik.sql ...]
set -uo pipefail

show_error() {
    echo "================================"
    echo "BŁĄD: $1"
    echo "================================"
    exit 1
}

show_info() {
    echo "INFO: $1"
}

if [ -z "${1:-}" ]; then
    echo "Użycie: $0 [local|prod] [dump.sql ...]"
    exit 1
fi

ENV="$1"
shift

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

# Domyslnie oba dumpy: lokalny (rentals_*) + serwerowy (calendar_*, tasks).
# Kolejnosc ma znaczenie - pierwszy dump wygrywa dla tabel wspolnych.
if [ "$#" -gt 0 ]; then
    DUMPS=("$@")
else
    DUMPS=(
        "$PROJECT_ROOT/docs/kopia_lokalna.sql"
        "$PROJECT_ROOT/docs/kopia_lokalna_z_serwera.sql"
    )
fi

# Tabele pomijane przy imporcie:
#   alembic_version      - migration_restart generuje nowa rewizje "init", stare ID zablokowaloby upgrade
#   users                - te same UUID-y w obu dumpach i w seedzie sql/users.sql
#   keyscalculatorpatryk - jw. (seed sql/key_calculator.sql)
SKIP_TABLES="${SKIP_TABLES:-alembic_version users keyscalculatorpatryk}"

# Filtr dumpu:
#   - linie zaczynajace sie od "\" (\restrict, \unrestrict, \connect) - dyrektywy pg_dump 18,
#     ktore przelaczylyby psql na baze "project_job"/"jobs" zamiast tej z env/<ENV>.env
#   - CREATE/ALTER DATABASE - jw.
#   - INSERT-y do tabel z SKIP_TABLES
# Reszta (SET, INSERT-y kwalifikowane przez public.*) przechodzi bez zmian.
FILTER_AWK='
BEGIN { n = split(skip, a, " "); for (i = 1; i <= n; i++) sk[i] = "INSERT INTO public." a[i] " " }
substr($0, 1, 1) == "\\" { next }
/^CREATE DATABASE / { next }
/^ALTER DATABASE / { next }
{ for (i = 1; i <= n; i++) if (index($0, sk[i]) == 1) next; print }
'

export PGPASSWORD="$DB_PASSWORD"

show_info "Środowisko: $ENV (baza $DB_DBNAME @ $DB_HOST:$DB_PORT)"
show_info "Pomijane tabele: $SKIP_TABLES"

for DUMP in "${DUMPS[@]}"; do
    if [ ! -f "$DUMP" ]; then
        show_error "Dump $DUMP nie istnieje!"
    fi

    echo "================================"
    echo "Import: $(basename "$DUMP")"
    echo "================================"

    if ! awk -v skip="$SKIP_TABLES" "$FILTER_AWK" "$DUMP" \
      | psql -v ON_ERROR_STOP=1 --single-transaction \
             -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -q -f -; then
        show_error "Import $(basename "$DUMP") nie powiódł się (transakcja wycofana)."
    fi

    show_info "✓ $(basename "$DUMP") zaimportowany"
done

echo "================================"
echo "Liczba wierszy po imporcie:"
echo "================================"
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -At -c "
SELECT relname || ': ' || n_live_tup
FROM pg_stat_user_tables
WHERE n_live_tup > 0
ORDER BY relname;"

echo "================================"
echo "SUKCES: Dane z dumpów wgrane do bazy $DB_DBNAME"
echo "================================"
