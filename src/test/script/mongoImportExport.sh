#!/bin/bash



mongoImport(){

    docker cp src/main/mongo/. chatbot:/data/

    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c entities  --file /data/entities.json
    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c intents  --file /data/intents.json
    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c interactions  --file /data/interactions.json
    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c models  --file /data/models.json
    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c projects  --file /data/projects.json
    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c stories  --file /data/stories.json
    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c templates  --file /data/templates.json
    docker exec -t chatbot mongoimport --mode=upsert -d rasa -c values  --file /data/values.json
}

