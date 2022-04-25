FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="europe/madrid"
RUN apt update && apt-get upgrade -y  
RUN apt install build-essential dkms -y
RUN apt install libhunspell-dev -y 
RUN apt install libreoffice hunspell-es -y
RUN apt install libreoffice hyphen-es -y
RUN apt install python3.7 -y

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 && update-alternatives --config python3 &&  rm /usr/bin/python3 && ln -s python3.7 /usr/bin/python3

RUN apt install python3.7-dev python3-pip curl -y
RUN apt install curl default-jre -y

RUN curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get install nodejs mongodb -y

RUN rm -rf /tmp/*

RUN mkdir /data && mkdir /data/db 