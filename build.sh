#!/bin/bash

repo_full="de_task"

#if [ "$1" ]; then
#  target="$1"
#else
#  target="production"
#fi

tags="-t $repo_full:latest"

DOCKER_BUILDKIT=1 \
docker build $tags -f Dockerfile .
