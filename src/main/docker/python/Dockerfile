#FROM ubuntu:latest
FROM ubuntu:18.04
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
RUN apt install default-jre -y


RUN apt install wget  -y

RUN mkdir -p /ner

RUN mkdir /ner/results/ner/ -p
RUN mkdir /ner/resources/ -p

COPY ./src/main/python  /python

RUN python3.7 -m pip install --upgrade pip setuptools && pip3 install -r /python/administrator/requirements.txt

WORKDIR  /python/administrator
