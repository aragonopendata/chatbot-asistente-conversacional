#!/bin/bash
echo "copia el modelo de rasa"
mkdir -p src/main/python/administrator/models/GDA/AOD
cp ./model/model-chatbot.tar.gz  src/main/python/administrator/models/GDA/AOD

echo "copia el modelo del ner"

mkdir -p  src/main/python/ner/results/ner
mkdir -p src/main/python/ner/resources
tar  -xzvf ./model/model_glove_all_char100_300_3.weights.tar.gz   -C ./src/main/python/ner/results/ner/
tar  -xzvf ./model/glove_all.tar.gz  -C ./src/main/python/ner/resources


docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  build
