#!/bin/bash

mongoExport(){
    nameFile=$(date '+%Y%m%d')

    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c entities  --out=/data/entities.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c intents  --out=/data/intents.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c interactions  --out=/data/interactions.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c models  --out=/data/models.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c projects  --out=/data/projects.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c stories  --out=/data/stories.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c templates  --out=/data/templates.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c values  --out=/data/values.json
    sudo docker exec -t docker_mongodb_1 sh -c "tar -czvf /data/mongoExport$nameFile.gz /data/*.json"
    sudo docker cp docker_mongodb_1:/data/mongoExport$nameFile.gz .
}

mongoExportGit(){
    nameFile=$(date '+%Y%m%d')

    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c entities  --out=/data/entities.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c intents  --out=/data/intents.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c interactions  --out=/data/interactions.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c models  --out=/data/models.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c projects  --out=/data/projects.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c stories  --out=/data/stories.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c templates  --out=/data/templates.json
    sudo docker exec -t docker_mongodb_1 mongoexport -d rasa -c values  --out=/data/values.json

    git checkout -t  origin/backupMongo

    git merge dev --no-edit -X theirs

    sudo docker cp docker_mongodb_1:/data/entities.json ./src/main/mongo/
    sudo docker cp docker_mongodb_1:/data/intents.json ./src/main/mongo/
    sudo docker cp docker_mongodb_1:/data/interactions.json ./src/main/mongo/
    sudo docker cp docker_mongodb_1:/data/models.json ./src/main/mongo/
    sudo docker cp docker_mongodb_1:/data/projects.json ./src/main/mongo/
    sudo docker cp docker_mongodb_1:/data/stories.json ./src/main/mongo/
    sudo docker cp docker_mongodb_1:/data/templates.json ./src/main/mongo/
    sudo docker cp docker_mongodb_1:/data/values.json ./src/main/mongo/

    git add  ./src/main/mongo/*.json
    git commit -am "backup Mongo diario $nameFile"


    git push "url git" backupMongo
    git checkout dev
    git branch -D backupMongo

}

mongoImport(){

    docker cp src/main/mongo/. docker_mongodb_1:/data/

    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c entities  --file /data/entities.json
    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c intents  --file /data/intents.json
    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c interactions  --file /data/interactions.json
    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c models  --file /data/models.json
    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c projects  --file /data/projects.json
    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c stories  --file /data/stories.json
    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c templates  --file /data/templates.json
    docker exec -t docker_mongodb_1 mongoimport --mode=upsert -d rasa -c values  --file /data/values.json
}

