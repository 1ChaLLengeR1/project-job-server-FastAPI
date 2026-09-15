#!/bin/bash
# Trzywarstwowy smoke obrazu produkcyjnego PRZED buildem/pushem na Docker Hub.
# Layer 1 - build obrazu, Layer 2 - import/mappery, Layer 3 - boot + probe /health.
set -e

IMAGE="project_job_smoke:ci"
CONTAINER="project_job_smoke"

DUMMY_ENV=(
  -e BACKEND_SERVER_JOB_DB_HOST=localhost
  -e BACKEND_SERVER_JOB_DB_PORT=5432
  -e BACKEND_SERVER_JOB_DB_USER=smoke
  -e BACKEND_SERVER_JOB_DB_PASSWORD=smoke
  -e BACKEND_SERVER_JOB_DB_DBNAME=smoke
  -e BACKEND_SERVER_JOB_SECRET_KEY_TOKEN=smoke
  -e BACKEND_SERVER_JOB_SECRET_KEY_REFRESH_TOKEN=smoke
  -e BACKEND_SERVER_JOB_ALGORITHM=HS256
  -e BACKEND_SERVER_JOB_TOKEN_EXPIRES_HOURS=1
  -e BACKEND_SERVER_JOB_REFRESH_TOKEN_EXPIRES_HOURS=1
)

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "=== Layer 1: build obrazu produkcyjnego ==="
docker build -t "$IMAGE" -f infra/dockerfiles/dockerfile/production.dockerfile .

echo "=== Layer 2: import check (main + routery + modele) ==="
docker run --rm "${DUMMY_ENV[@]}" "$IMAGE" python -c "import main; print('import ok')"

echo "=== Layer 3: boot gunicorna + probe /health ==="
docker run -d --name "$CONTAINER" "${DUMMY_ENV[@]}" -p 3000:3000 "$IMAGE"

for _ in $(seq 1 30); do
  if curl -fsS http://localhost:3000/health >/dev/null 2>&1; then
    echo "=== Smoke OK: /health odpowiada ==="
    exit 0
  fi
  sleep 2
done

echo "!!! Backend nie wstał w 60 s - logi kontenera:"
docker logs "$CONTAINER"
exit 1
