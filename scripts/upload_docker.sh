#!/bin/bash

set -e

APP_VERSION=$1
DOCKER_USER="arturscibor"
DOCKER_REPO="praca.server.arturscibor.pl"
FULL_IMAGE_NAME="$DOCKER_USER/$DOCKER_REPO:$APP_VERSION"

if [ -z "$APP_VERSION" ]; then
  echo "Podaj wersję jako argument. Przykład: ./upload_docker.sh 1.0.1"
  exit 1
fi

echo ">>> Budowanie obrazu: $FULL_IMAGE_NAME ..."
docker build -t $FULL_IMAGE_NAME -f dockerfiles/prod.dockerfile .

echo ">>> Nadpisywanie latest tagiem..."
docker tag $FULL_IMAGE_NAME $DOCKER_USER/$DOCKER_REPO:latest

# 🔐 Logowanie tylko jeśli DOCKER_PASSWORD jest ustawione
if [ -n "$DOCKER_PASSWORD" ]; then
  echo ">>> Logowanie do Docker Huba..."
  echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin
else
  echo ">>> Pomijam logowanie do Docker Huba – już jesteś zalogowany lub używasz credential helpera."
fi

echo ">>> Wysyłanie obrazu do Docker Huba..."
docker push $FULL_IMAGE_NAME
docker push $DOCKER_USER/$DOCKER_REPO:latest

echo ">>> Obrazy zostały wysłane pomyślnie!"
