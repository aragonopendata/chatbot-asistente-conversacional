#!/bin/bash

docker volume create -d local-persist -o mountpoint=/app/chatbot/src/main/python/ --name  volume-pythonchatbot
docker volume create -d local-persist -o mountpoint=/app/chatbot/src/main/nodejs/ --name  volume-nodejschatbot
docker volume create -d local-persist -o mountpoint=/app/chatbot/data/            --name  volume-mongodbchatbot
docker volume create -d local-persist -o mountpoint=/app/chatbot/src/main/nginx/  --name  volume-nginxchatbot
