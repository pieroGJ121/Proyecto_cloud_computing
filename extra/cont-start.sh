#!/usr/bin/env sh

docker pull proyectoccgrupo7/frontend:latest
docker pull proyectoccgrupo7/api-games:latest
docker pull proyectoccgrupo7/api-reviews:latest
docker pull proyectoccgrupo7/api-ratings:latest
docker pull proyectoccgrupo7/api-profiles:latest

docker run -d -p 8030:3000 proyectoccgrupo7/frontend
docker run -d -p 8020:8020 proyectoccgrupo7/api-games
docker run -d -p 8021:8021 proyectoccgrupo7/api-reviews
docker run -d -p 8022:8022 proyectoccgrupo7/api-ratings
docker run -d -p 8023:8023 proyectoccgrupo7/api-profiles
