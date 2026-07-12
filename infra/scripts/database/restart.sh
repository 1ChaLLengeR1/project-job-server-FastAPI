#!/bin/bash

show_error() {
    echo "================================"
    echo "BŁĄD: $1"
    echo "================================"
    exit 1
}

show_info() {
    echo "INFO: $1"
}

show_success() {
    echo "================================"
    echo "SUKCES: $1"
    echo "================================"
}

show_info "Rozpoczynam pełny restart bazy danych..."

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

show_info "Katalog projektu: $PROJECT_ROOT"

if [ -z "$1" ]; then
    echo "Użycie: $0 [local|prod]"
    exit 1
fi

show_info "Środowisko: $1"

ENV_FILE="$PROJECT_ROOT/env/$1.env"
show_info "Sprawdzam plik środowiskowy: $ENV_FILE"

if [ ! -f "$ENV_FILE" ]; then
    show_error "Plik środowiskowy $ENV_FILE nie istnieje!"
fi

show_info "Ładuję zmienne środowiskowe..."
set -a
source "$ENV_FILE"
set +a

if [ -z "$DB_HOST" ]; then show_error "DB_HOST nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_PORT" ]; then show_error "DB_PORT nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_USER" ]; then show_error "DB_USER nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_PASSWORD" ]; then show_error "DB_PASSWORD nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_DBNAME" ]; then show_error "DB_DBNAME nie jest ustawione w pliku $1.env"; fi

show_info "Wszystkie zmienne środowiskowe są dostępne"

cd "$PROJECT_ROOT" || show_error "Nie można przejść do katalogu $PROJECT_ROOT"

# ── KROK 1: Alembic downgrade base (usuwa tabele wg zarejestrowanych migracji) ──
echo "================================"
echo "KROK 1: alembic downgrade base"
echo "================================"

show_info "Ubijam tabele przez Alembic..."
if ! uv run alembic downgrade base; then
    show_error "Błąd podczas alembic downgrade base! Sprawdź logi powyżej."
fi
show_info "✓ Alembic downgrade base zakończony"

# ── KROK 2: migration_down.sh (database_down.sql — czyści alembic_version i resztę) ──
echo "================================"
echo "KROK 2: migration_down.sh"
echo "================================"

show_info "Uruchamiam migration_down.sh..."
if ! "$PROJECT_ROOT/infra/scripts/database/migration_down.sh" "$1"; then
    show_error "Błąd podczas migration_down.sh!"
fi
show_info "✓ migration_down.sh zakończony"

# ── KROK 3: Usunięcie plików wersji migracji ──
echo "================================"
echo "KROK 3: Czyszczenie versions/"
echo "================================"

VERSIONS_DIR="$PROJECT_ROOT/alembic/versions"
show_info "Usuwam pliki migracji z $VERSIONS_DIR ..."
find "$VERSIONS_DIR" -maxdepth 1 -name "*.py" ! -name "__init__.py" -delete
rm -rf "$VERSIONS_DIR/__pycache__"
show_info "✓ Pliki wersji usunięte"

# ── KROK 4: Generowanie nowej migracji init ──
echo "================================"
echo "KROK 4: alembic revision --autogenerate -m init"
echo "================================"

show_info "Generuję nową migrację init..."
if ! uv run alembic revision --autogenerate -m "init"; then
    show_error "Błąd podczas generowania migracji! Sprawdź logi powyżej."
fi
show_info "✓ Migracja init wygenerowana"

# ── KROK 5: migration_up.sh (extensions + alembic upgrade head + seedy) ──
echo "================================"
echo "KROK 5: migration_up.sh"
echo "================================"

show_info "Uruchamiam migration_up.sh..."
if ! "$PROJECT_ROOT/infra/scripts/database/migration_up.sh" "$1"; then
    show_error "Błąd podczas migration_up.sh!"
fi

show_success "Restart bazy danych zakończony pomyślnie!"
exit 0
