#!/bin/bash

downloadAndCopyModel(){
    urlModelChatbot="https://..."
    echo -ne "[INFO] download model... "
    echo "download model chatbot $urlModelChatbot"
    wget  $urlModelChatbot -O model-chatbot.tar.gz
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to download model chatbot"
        exit $code
    fi
    echo "OK"
    docker exec -t --user root  docker_rasa_1  mkdir /python/administrator/models/GDA/AOD -p
    docker cp   model-chatbot.tar.gz docker_rasa_1:/python/administrator/models/GDA/AOD
    echo "OK"
}


docker-compose  -f  ./src/main/docker/docker-compose.yml  up -d

downloadAndCopyModel

docker-compose  -f  ./src/main/docker/docker-compose.yml restart
