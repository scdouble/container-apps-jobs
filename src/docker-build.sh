#!/bin/bash

source ./var.sh

for index in ${!images[@]}; do
# Build the docker image
    docker build --platform linux/amd64 -t ${images[$index]}:$tag -f Dockerfile --build-arg FILENAME=${filenames[$index]} .
done