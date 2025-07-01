#!/bin/bash

set -e

APP_VERSION=$1

if [ -z "$APP_VERSION" ]; then
  echo "Podaj wersję jako argument. Przykład: ./swarm_deploy.sh 1.0.1"
  exit 1
fi

LOG_FILE="../swarm_deploy.log"

echo ">>> Budowanie obrazu z wersją: $APP_VERSION..."
APP_VERSION=${APP_VERSION} sudo docker-compose --env-file ../env/prod.env -f ../prod.swarm.docker-compose.yaml build --build-arg APP_VERSION=${APP_VERSION}

echo ">>> Aktualizacja stacka Traefik..."
sudo docker stack deploy -c ../dockerfiles/terafik/traefik.yml traefik

echo ">>> Aktualizacja stacka Swarm..."
sudo docker stack deploy -c ../prod.swarm.docker-compose.yaml spinetime_stack

echo ">>> Usuwanie nieużywanych obrazów..."
sudo docker image prune -f

DEPLOY_DATE=$(date '+%Y-%m-%d %H:%M:%S')
DEPLOY_MESSAGE="Swarm deploy zakończony. Wersja: $APP_VERSION, Data: $DEPLOY_DATE"

echo ">>> $DEPLOY_MESSAGE"
echo "$DEPLOY_MESSAGE" >> "$LOG_FILE"


