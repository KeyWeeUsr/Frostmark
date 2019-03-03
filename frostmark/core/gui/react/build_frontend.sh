#!/bin/sh
set -xe

docker build --tag frostmark_builder .

docker run --rm --interactive --tty \
    --volume $(pwd)/src:/app/src \
    --volume $(pwd)/public:/app/public \
    --volume $(pwd)/build:/app/build \
    frostmark_builder yarn build
