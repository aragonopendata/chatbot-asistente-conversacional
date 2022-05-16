#!/bin/bash

source ./src/test/script/mongoImportExport.sh
logPath=./log

mkdir -p $logPath

echo "working directory $PWD"

stopChatbot(){

    docker stop chatbot || true

    until [ $(docker ps -a | grep chatbot | wc -l ) -eq "0"  ];
    do
       echo "Stoping is running......"
       sleep 20
    done
}

waitingMongoStart(){

    until [ $(docker exec -t chatbot ps -edaf | grep mongo| wc -l ) -ne "0"  ];
    do
        #echo "mongo instance $(docker exec -t chatbot 'ps -edaf | grep mongo')"
        echo "waiting mongo server is running......"
        sleep 1
        #echo "mongo instance $( docker exec -t chatbot 'ps -edaf | grep mongo')"
    done
}

downloadingNer(){

    echo -ne "[INFO] download Ner from git ..."
    curl -fsSL -H  'PRIVATE-TOKEN: SHRCF-65tNzyifAuB6Vy'  'https://git.itainnova.es/api/v4/projects/96/repository/archive.tar.gz?ref=master'  | tar -xzv -C entity_detector-master --strip-components=1
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to download NER"
        exit $code
    fi
    echo "OK"

}

downloadingModel(){

    echo "download model glove "
    mkdir entity_detector-master/results/ner/ -p
    wget -qO-  $urlModel | tar -xzv -C entity_detector-master/results/ner/
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to download model glove"
        exit $code
    fi
    echo "OK"

    echo "download model resources "
    mkdir entity_detector-master/resources/ -p
    wget -qO-  $urlModelResources | tar -xzv -C entity_detector-master/resources/
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to download model resources"
        exit $code
    fi
    echo "OK"
}


importingMongo(){
    
    echo "[INFO] import mongo"
    mongoImport  > $logPath/importMongo.log  
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to import mongo"
        cat $logPath/importMongo.log
        exit $code
    fi
    echo "OK"

}
installingNodejs(){

   echo "node version "$(docker exec -t chatbot node -v)
    # NODEJS INSTALLATION
    echo -ne "[INFO] Installing NodeJS package: npm install -g yarn "
    docker exec  --user root chatbot  /bin/bash -c 'rm /nodejs/node_modules/ -Rf'
    docker exec -t --user root chatbot  /bin/bash -c 'cd /nodejs; npm install -g yarn' > $logPath/node-npm.log
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to install yarn"
        cat $logPath/node-npm.log
        exit $code
    fi
    echo "OK" 

    echo -ne "[INFO] installing  node_modules: yarn install "
    docker exec -t --user root chatbot  /bin/bash -c 'cd /nodejs; yarn install' > $logPath/node-install.log 
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to install node_modules"
        cat $logPath/node-install.log
        exit $code
    fi
    echo "OK"

    echo -ne "[INFO] Building nuxtJS: yarn run build "
    docker exec -t --user root chatbot /bin/bash -c 'cd /nodejs; yarn run build' > $logPath/node-build.log 
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to Builidng NodeJS"
        cat $logPath/node-build.log
        exit $code
    fi
    echo "OK"
	if [ -z "$startYarn" ];then
		echo -ne "[INFO] Starting server: yarn start "
		docker exec -t chatbot /bin/bash -c 'cd /nodejs; yarn start' > $logPath/node-start.log  & 
    else 
		echo -ne "[INFO] Starting server: $startYarn "
		docker exec  -i chatbot /bin/bash <<EOF > $logPath/node-start.log  2>&1  &
cd /nodejs; eval '$startYarn' 
exit
EOF

	fi 
	
	echo "OK"

}
installingPython(){

    # CHATBOT INSTALLATION
    echo "[INFO] Deploying chatbot infrastructure"
    echo -ne "[INFO] Deleting models directory... "
    docker exec --user root chatbot  /bin/bash -c 'rm /python/administrator/models/ -Rf'
    
    echo "OK"
    
    echo -ne "[INFO] Installing Python requirements..."
    docker exec -t --user root chatbot  /bin/bash -c 'python3.7 -m pip install --upgrade pip setuptools && pip3 install -r /python/administrator/requirements.txt' > $logPath/requirements.log 
    code=$?
    if [ $code -ne 0 ]; then
        echo "[Error] code $code"
        echo "[Error] to install requirements"
        cat $logPath/requirements.log
        exit $code
    fi
    echo "OK"

   
}

trainingModel(){

    echo -ne "[INFO] Training initial model... "
    docker exec -t chatbot /bin/bash -c 'cd /python/administrator/; python3.7 train_model.py' > $logPath/train.log 
    echo "OK"
}

downloadAndCopyModel(){

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
    docker exec -t --user root  chatbot  mkdir /python/administrator/models/GDA/AOD -p 
    docker cp   model-chatbot.tar.gz chatbot:/python/administrator/models/GDA/AOD
    echo "OK"
}

startingPython(){

    echo -ne "[INFO] Starting ner "
    docker exec -t chatbot /bin/bash -c 'cd /ner/; python3.7 apirest.py ' > $logPath/ner_rest.log  &
    echo "OK"
    sleep 10
    #echo -ne "[INFO] Starting back-end and chat-room Flask servers and Socket... "
    #docker exec -t chatbot /bin/bash -c 'cd /python/administrator/; python3.7 app.py 5006' > $logPath/app.log   &
    #docker exec -t chatbot /bin/bash -c 'cd /python/administrator/; python3.7 app_train.py 5008' >  $logPath/app_socket.log   &
	

    echo -ne "[INFO] Starting chatbot in path $startChatbot "	
    docker exec  -i chatbot /bin/bash <<EOF > $logPath/chatbot.log 2>&1  &
cd /python/administrator/; python3.7 app_chat.py 5000 "$startChatbot"
exit
EOF
	
    echo "OK"

    echo -ne "[INFO] Starting Rasa actions server... "
    docker exec -t chatbot /bin/bash -c 'cd /python/administrator/; rasa run actions' > $logPath/rasa.log  &
    echo "OK"
}


startDocker(){

    logPath=./log
    #create directory before launch docker. 
    rm entity_detector-master/ -Rf || true
    mkdir entity_detector-master/ -p

    docker run  --add-host api:127.0.0.1 --add-host mongodb:127.0.0.1 --add-host rasa:127.0.0.1 --add-host ner:127.0.0.1 --name chatbot --rm -it  -u $(id -u ${USER}):$(id -g ${USER})  -p 3001:3001 -p 5000:5000 -p 5008:5008 -p 5006:5006 -p 5055:5055 -d -e TZ=Europe/Madrid -v $PWD/entity_detector-master/:/ner -v $PWD/data/:/data/db -v $PWD/src/main/nodejs/:/nodejs  -v $PWD/src/main/python/:/python -v $PWD/src/test/:/test -v /var/log/chatbot/:/var/log/ --entrypoint=/bin/bash chatbot:latest
    
    docker exec -d --user root chatbot  /bin/bash -c ' rm /data/db -Rf && mkdir /data/db'
	docker exec -d --user root chatbot  /bin/bash -c 'chown -R mongodb:mongodb /data/db/'
	docker exec -d --user root chatbot /bin/bash -c 'sudo -u mongodb  mongod  --bind_ip_all  > /var/log/mongo.log '

}
startTest(){
    docker exec -t chatbot /bin/bash -c 'cd /python/administrator;export PYTHONPATH=${PYTHONPATH}:/python/administrator; python3.7 -m pytest -rsxpP' > ./log/testChatbot.log &
}

startDockerJenkins () {

    urlModel=http://193.144.231.29:8081/repository/war/models/model_glove_all_char100_300_3.weights.tar.gz
    urlModelResources=http://193.144.231.29:8081/repository/war/models/glove_all.tar.gz
    urlModelChatbot="http://193.144.231.29:8081/service/rest/v1/search/assets/download?sort=name&direction=desc&repository=war&group=%2Fmodels%2Fchatbot%2Fjenkins"

		
	startYarn="yarn cross-env PORT=3001 HOST=0.0.0.0 NODE_ENV=production BASE=/ node server/index.js"
	

    echo "parameter $1"
    if [ $1 -eq 1 ]; then
        echo "stop"
        stopChatbot
    fi
    if [ $1 -eq 2 ]; then
        echo "start"
        startDocker 
    fi
    if [ $1 -eq 3 ]; then
       echo "install all "
       waitingMongoStart

       downloadingNer
       downloadingModel
       importingMongo
       installingNodejs
       installingPython
       #trainingModel
       downloadAndCopyModel
       startingPython
    fi
    if [ $1 -eq 4 ]; then
        echo "start Test"
        startTest
    fi
}

startDockerDev () {

    logPath=/var/log/chatbot
    curl   -H "Content-type:application/json" -H "Authorization: Bearer xoxp-655522913862-653931250212-841449899972-897a181537ccde792a5eaa3251fcb183" -d '{"channel": "CKA7M1NCF", "text": "Redesplegando en dev"'}  -X POST https://slack.com/api/chat.postMessage
	stopChatbot

    urlModel=https://argon-docker.itainnova.es/repository/war/models/model_glove_all_char100_300_3.weights.tar.gz
    urlModelResources=https://argon-docker.itainnova.es/repository/war/models/glove_all.tar.gz
    urlModelChatbot="https://argon-docker.itainnova.es/service/rest/v1/search/assets/download?sort=name&direction=desc&repository=war&group=%2Fmodels%2Fchatbot%2Fdev"
	
		
	startYarn="yarn cross-env PORT=3001 HOST=0.0.0.0 NODE_ENV=production BASE=/loginchat node server/index.js"
	startChatbot="/servicios/chatbot"	


    docker run --name chatbot --rm -it -p 27017:27017 -p 4999:4999 -p 3001:3001 -p 5006:5006  -p 5000:5000  -d -e TZ=Europe/Madrid -v $PWD/data/:/data/db -v $PWD/entity_detector-master/:/ner -v $PWD/src/main/nodejs/:/nodejs -v $PWD/src/main/python/:/python -v $PWD/src/test/:/test -v /var/log/chatbot/:/var/log/ --entrypoint=/bin/bash chatbot:latest

    docker exec -d  chatbot  /bin/bash -c 'mongod --bind_ip_all > /var/log/mongo.log'


    waitingMongoStart

    downloadingNer
    downloadingModel
	#importingMongo
    installingNodejs
    installingPython
    #trainingModel
    downloadAndCopyModel
    startingPython
    
    docker exec -t chatbot /bin/bash -c 'cd /python/administrator;export PYTHONPATH=${PYTHONPATH}:/python/administrator; python -m pytest -rsxpP' > ./log/testChatbot.log &
    curl   -H "Content-type:application/json" -H "Authorization: Bearer xoxp-655522913862-653931250212-841449899972-897a181537ccde792a5eaa3251fcb183" -d '{"channel": "CKA7M1NCF", "text": "desplegado en dev, ok"'}  -X POST https://slack.com/api/chat.postMessage
}

startDockerPre () {
    logPath=/var/log/chatbot
    curl   -H "Content-type:application/json" -H "Authorization: Bearer xoxp-655522913862-653931250212-841449899972-897a181537ccde792a5eaa3251fcb183" -d '{"channel": "CKA7M1NCF", "text": "Redesplegando en pre"'}  -X POST https://slack.com/api/chat.postMessage
	stopChatbot
    
    urlModel=https://argon-docker.itainnova.es/repository/war/models/model_glove_all_char100_300_3.weights.tar.gz
    urlModelResources=https://argon-docker.itainnova.es/repository/war/models/glove_all.tar.gz
    urlModelChatbot="https://argon-docker.itainnova.es/service/rest/v1/search/assets/download?sort=name&direction=desc&repository=war&group=%2Fmodels%2Fchatbot%2Fpre"

	startYarn="yarn cross-env PORT=3001 HOST=0.0.0.0 NODE_ENV=production BASE=/loginchat node server/index.js"
	startChatbot="/servicios/chatbot"	
    
    docker run --name chatbot --rm -it  -p 3001:3001 -p 5006:5006  -p 5000:5000  -d -e TZ=Europe/Madrid -v $PWD/data/:/data/db -v $PWD/entity_detector-master/:/ner -v $PWD/src/main/nodejs/:/nodejs -v $PWD/src/main/python/:/python -v $PWD/src/test/:/test -v /var/log/chatbot/:/var/log/ --entrypoint=/bin/bash chatbot:latest

    docker exec -d  chatbot  /bin/bash -c 'mongod  > /var/log/mongo.log'


    waitingMongoStart

    downloadingNer
    downloadingModel
	#importingMongo
    installingNodejs
    installingPython
    #trainingModel
    downloadAndCopyModel
    startingPython
    
    #docker exec -t chatbot /bin/bash -c 'cd /python/administrator;export PYTHONPATH=${PYTHONPATH}:/python/administrator; python -m pytest -rsxpP' > ./log/testChatbot.log &
    curl   -H "Content-type:application/json" -H "Authorization: Bearer xoxp-655522913862-653931250212-841449899972-897a181537ccde792a5eaa3251fcb183" -d '{"channel": "CKA7M1NCF", "text": "desplegado en pre, ok "'}  -X POST https://slack.com/api/chat.postMessage
}


branch=$(git symbolic-ref --short HEAD)

if [ $? -ne "0" ]; then
    branch="deatch"
    echo "branch deatch"
    startDockerJenkins $1
fi

#if [ $branch  == "dev" ]; then
#    echo "branch dev"
#    startDockerDev
#fi

#if [ $branch  == "pre" ]; then
#    echo "branch pre"
#    startDockerPre
#fi

#if [ $branch  == "pro" ]; then
#    echo "branch pro"
#    startDockerPro
#fi
