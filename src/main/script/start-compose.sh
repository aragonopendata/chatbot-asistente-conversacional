#!/bin/bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory . --env-file ./src/main/docker/.rasa1.0 up -d


