#!/bin/bash

logPath=./log
mkdir -p $logPath

docker  exec chatbot mkdir -p /test/python
docker cp src/test/python/questions.py  chatbot:/test/python
docker cp src/test/python/cmd.py  chatbot:/test/python
docker exec -t chatbot /bin/bash -c 'cd /test/python; python3.7 system_test.py'> $logPath/system_test.log
docker exec -t chatbot /bin/bash -c 'cd /test/python; python3.7 questions.py'> $logPath/questions.log
#docker  exec chatbot rm  /test/ -Rf 
