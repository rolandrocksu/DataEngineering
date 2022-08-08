#!/bin/bash

compose_file=docker-compose.yml

repo_full="de_task"

if [ "$1" == "--clean" ]; then
  docker-compose --project-name de_task --file $compose_file down -v
  exit
fi

set -a

if [ -t 1 ]; then
    INTERACTIVE_FLAG="-it"
else
    INTERACTIVE_FLAG=""
fi

./build.sh $1

image_name="$repo_full:latest"

docker-compose --project-name de_task --file $compose_file up

$SHELL
