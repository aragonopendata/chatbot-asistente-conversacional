#!bin/bash

docker run -it --name training --network=chatbot_chatbot-network  -e PYTHONPATH=./ rasa:1.0 /bin/bash -c 'python3 scripts/generate_files.py;rasa train --data data/training/nlu -c config.yml -d data/training/domain.yml --num-threads 50 --out /python/administrator/models/GDA/AOD/ --fixed-model-name model-chatbot'
docker commit training rasa:1.1
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory --env-file ./src/main/docker/.rasa1.1 . up -d
