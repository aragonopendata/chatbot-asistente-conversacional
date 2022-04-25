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


COPY ./src/main/python/administrator/requirements.txt  /python/administrator/requirements.txt

RUN python3.7 -m pip install --upgrade pip setuptools && pip3 install -r /python/administrator/requirements.txt

RUN python3.7 -m spacy download es_core_news_sm
RUN pip3 install Jinja2==3.0.3

RUN pip3 install itsdangerous==2.0.1
RUN pip3 install Werkzeug==2.0.2
COPY ./src/main/python/administrator/  /python/administrator/

WORKDIR  /python/administrator
