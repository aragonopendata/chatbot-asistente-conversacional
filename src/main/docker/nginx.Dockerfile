#FROM node:12  as build

#WORKDIR /app

#COPY ./src/main/nodejs/ /app/
#COPY ./main/vue/package-lock.json /app/package-lock.json


#RUN cd /app; yarn install
#RUN cd /app; BASE=/loginchat yarn run build

FROM nginx
COPY ./src/main/nginx/default.conf /etc/nginx/conf.d/default.conf
#COPY --from=build /app/dist /usr/share/nginx/html
