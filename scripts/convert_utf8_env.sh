#!/bin/bash

set -e

iconv -f ISO-8859-1 -t UTF-8 ./env/prod.env > ./env/prod_utf8.env

rm ./env/prod.env

mv ./env/prod_utf8.env ./env/prod.env

echo "Konwersja plików .env zakonczona!"
