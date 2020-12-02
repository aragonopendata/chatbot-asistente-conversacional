FROM ubuntu:latest
RUN apt update 
RUN apt-get update && apt-get upgrade -y  
RUN apt-get install build-essential dkms -y
RUN apt-get install libhunspell-dev -y 
RUN apt-get install libreoffice hunspell-es -y
RUN apt-get install libreoffice hyphen-es -y
RUN apt install python3.7 -y

RUN  update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 && update-alternatives --config python3 &&  rm /usr/bin/python3 && ln -s python3.7 /usr/bin/python3

RUN apt-get install python3.7 python3.7-dev   python3-pip curl -y

RUN curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh
RUN  bash nodesource_setup.sh
RUN apt-get install nodejs mongodb default-jre -y

RUN mkdir /data && mkdir /data/db 