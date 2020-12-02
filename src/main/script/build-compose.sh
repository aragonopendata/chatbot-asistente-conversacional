
docker build  . -f  src/main/docker/python/Dockerfile  --tag python-chat:1.0
docker-compose  -f  ./src/main/docker/docker-compose.yml  build

