#!/bin/bash


downloadAndCopyModel(){
    docker exec -t --user root chat  mkdir /python/administrator/models/GDA/AOD -p
    docker cp   model-chatbot.tar.gz chat:/python/administrator/models/GDA/AOD

    docker exec argon-nginx mkdir /etc/nginx/conf.d/model/
    docker cp model-chatbot.tar.gz   argon-nginx:/etc/nginx/conf.d/model/
}


docker-compose  -f  ./src/main/docker/docker-compose.yml --project-name chatbot  --project-directory  .  up -d

downloadAndCopyModel

docker-compose  -f  ./src/main/docker/docker-compose.yml --project-directory  . restart
