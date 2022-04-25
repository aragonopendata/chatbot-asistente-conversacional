FROM node:16
WORKDIR /nodejs

COPY  ./src/main/nodejs  /nodejs 
RUN cd /nodejs; yarn install
RUN cd /nodejs; yarn run build

EXPOSE 3001

CMD ["yarn","run","build"]
