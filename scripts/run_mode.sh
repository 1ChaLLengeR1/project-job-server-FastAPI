#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  echo "Użycie: $0 <new_mode>"
  echo "Dostępne tryby: local, dev, prod"
  exit 1
fi

NEW_MODE=$1

BASE_DIR="$(dirname "$(realpath "$0")")/.."
CONFIG_FILE="$BASE_DIR/config/app_config.py"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Plik config/app_config.py nie istnieje!"
  exit 1
fi

CONTENT=$(cat "$CONFIG_FILE")

CURRENT_MODE=""

if [[ "$CONTENT" == *"ENV_MODE = 'local'"* ]]; then
  CURRENT_MODE="local"
elif [[ "$CONTENT" == *"ENV_MODE = 'dev'"* ]]; then
  CURRENT_MODE="dev"
elif [[ "$CONTENT" == *"ENV_MODE = 'prod'"* ]]; then
  CURRENT_MODE="prod"
fi

if [ -n "$CURRENT_MODE" ]; then
  CONTENT=$(echo "$CONTENT" | sed "s/ENV_MODE = '$CURRENT_MODE'/ENV_MODE = '$NEW_MODE'/")

  echo "$CONTENT" > "$CONFIG_FILE"

  echo "Przełączono tryb z '$CURRENT_MODE' na '$NEW_MODE'"
else
  echo "Nie znaleziono obecnej wartości ENV_MODE w pliku."
  exit 1
fi
