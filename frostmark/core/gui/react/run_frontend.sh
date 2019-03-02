#!/bin/sh
set -xe

docker build --file Dockerfile.builder \
    --build-arg REACT_PROXY=${REACT_PROXY:-127.0.0.1} \
    --tag frostmark_builder .

docker kill frostmark_runner ||true
docker rm -vf frostmark_runner ||true

docker run -it \
    --volume $(pwd)/src:/app/src \
    --volume $(pwd)/public:/app/public \
    --publish 3000:3000 \
    --name frostmark_runner \
    frostmark_builder yarn run start
