#!/bin/sh
set -xe

docker build \
    --tag frostmark_builder .

docker kill frostmark_runner ||true
docker rm -vf frostmark_runner ||true

docker run -dit \
    --name frostmark_runner \
    frostmark_builder tail -f /dev/null
docker cp frostmark_runner:/app/package.json package.json
docker kill frostmark_runner ||true
docker rm -vf frostmark_runner ||true

docker run -it \
    --volume $(pwd)/src:/app/src \
    --volume $(pwd)/public:/app/public \
    --publish 3000:3000 \
    --name frostmark_runner \
    frostmark_builder yarn run start
