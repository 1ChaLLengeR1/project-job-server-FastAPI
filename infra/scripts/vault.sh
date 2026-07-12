#!/usr/bin/env bash
# (de)szyfrowanie infra/ansible/secrets.yml.
# Uzywa lokalnego ansible-vault, a gdy go nie ma - jednorazowego kontenera Docker.
# Uzycie: ANSIBLE_PASSWORD='haslo' bash infra/scripts/vault.sh {decrypt|encrypt|view}
set -euo pipefail

ACTION="${1:-}"
case "$ACTION" in
  decrypt|encrypt|view) ;;
  *) echo "Uzycie: $0 {decrypt|encrypt|view}" >&2; exit 1 ;;
esac

if [ -z "${ANSIBLE_PASSWORD:-}" ]; then
  echo "Brak ANSIBLE_PASSWORD w srodowisku." >&2
  exit 1
fi

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
VAULT_FILE="infra/ansible/secrets.yml"

if command -v ansible-vault >/dev/null 2>&1; then
  cd "$PROJECT_ROOT"
  VAULT_PASS_FILE="$(mktemp)"
  trap 'rm -f "$VAULT_PASS_FILE"' EXIT
  umask 077
  printf %s "$ANSIBLE_PASSWORD" > "$VAULT_PASS_FILE"
  exec ansible-vault "$ACTION" --vault-password-file "$VAULT_PASS_FILE" "$VAULT_FILE"
fi

if ! docker info >/dev/null 2>&1; then
  echo "Brak ansible-vault w systemie, a demon Dockera nie odpowiada." >&2
  echo "Zainstaluj ansible-core (pipx install ansible-core) albo uruchom Dockera." >&2
  exit 1
fi

# Git Bash na Windows nie ma psuc sciezek przy montowaniu woluminu
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'

docker build -q -f "$PROJECT_ROOT/infra/dockerfiles/dockerfile/vault.dockerfile" \
  -t project-job-vault "$PROJECT_ROOT/infra/dockerfiles/dockerfile" >/dev/null

docker run --rm \
  -e ANSIBLE_PASSWORD \
  -v "$PROJECT_ROOT":/work \
  -w /work \
  project-job-vault \
  sh -c 'umask 077; printf %s "$ANSIBLE_PASSWORD" > /tmp/vp;
         ansible-vault "$1" --vault-password-file /tmp/vp "$2";
         rc=$?; rm -f /tmp/vp; exit $rc' _ "$ACTION" "$VAULT_FILE"
