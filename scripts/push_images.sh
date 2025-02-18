#!/bin/bash

# Nazwy repozytoriów na Docker Hub
FASTAPI_REPO="arturscibor/praca.server.arturscibor.pl"
NGINX_REPO="arturscibor/nginx-praca.server.arturscibor.pl"

# Wersja obrazu (możesz zmienić na np. `latest`)
VERSION="latest"

# Logowanie do Docker Huba
echo "Logowanie do Docker Hub..."
docker login
sleep 5

# Budowanie i wysyłanie obrazu FastAPI
echo "Budowanie obrazu FastAPI..."
docker build -t $FASTAPI_REPO:$VERSION -f ../dockerfiles/prod.dockerfile .
sleep 5

echo "Wysyłanie obrazu FastAPI do Docker Hub..."
docker push $FASTAPI_REPO:$VERSION
sleep 5

# Budowanie i wysyłanie obrazu Nginx
echo "Budowanie obrazu Nginx..."
docker build -t $NGINX_REPO:$VERSION -f ../dockerfiles/nginx.dockerfile .
sleep 5

echo "Wysyłanie obrazu Nginx do Docker Hub..."
docker push $NGINX_REPO:$VERSION
sleep 5

echo "Wszystkie obrazy zostały wysłane!"
sleep 5
