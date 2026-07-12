#!/bin/bash
set -e
trap 'echo "❌ Wystąpił błąd w linii $LINENO"' ERR

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

# Fix Windows line endings (CRLF -> LF) in env files and scripts (bind mount z Windows)
if [ -f "$PROJECT_ROOT/env/local.env" ]; then
    sed -i 's/\r//' "$PROJECT_ROOT/env/local.env"
fi
find "$PROJECT_ROOT/infra/scripts" -name '*.sh' -exec sed -i 's/\r//' {} +

# Override uv run alembic -> python -m alembic for Docker
uv() {
    if [ "$1" = "run" ] && [ "$2" = "alembic" ]; then
        shift 2
        python -m alembic "$@"
    else
        command uv "$@"
    fi
}
export -f uv

"$PROJECT_ROOT/infra/scripts/database/migration_up.sh" local

echo "INFO: Startuję serwer..."
exec python -m uvicorn main:app --host 0.0.0.0 --port 3000 --reload
