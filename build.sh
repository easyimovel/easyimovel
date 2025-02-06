#!/bin/sh
docker builder prune -f
if [ "$1" = "prod" ]; then
  ENV_FILE=".env.prod"
else
  ENV_FILE=".env.dev"
fi
docker build --build-arg ENV_FILE=$ENV_FILE -t easyimovel_api:latest .
docker tag easyimovel_api:latest muhrilobianco/easyimovel_api:latest
if [ "$1" = "prod" ]; then
	docker login
	docker push muhrilobianco/easyimovel_api:latest
fi
