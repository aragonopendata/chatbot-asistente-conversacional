## GUIA DE USO DEL PROYECTO CHATBOT

En esta guía se va a especificar que componentes forman el proyecto del chatbot, su funcionamiento y su puesta en marcha.
En general todas las aplicaciones se genereran con el comando de docker compose,

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  build
```

Y se levantan con el comando de docker compose

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d
```

A continuacion describimos cada una de estas aplicacones

### Aplicación de Nginx

Es la aplicacion que redireccion las peticiones de los servidores al chatbot y donde se publican los modelos entrenados del ner y del chatbot

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d argon-nginx
```

### Aplicación de mongodb

Es la aplicacion que almacena los datos de entrenamiento y de estadisticas de acceso a la aplicacicon

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d mongodb
```

### Aplicación de administracion

Es la aplicacion que gestiona los datos de entrenamiento y las estadísticas

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d web
```

### Aplicación Flask

En el script ```app_chat.py``` se encuentra la funcionalidad principal para hablar con el chatbot. Para poner en marcha el chatbot ejecutar:

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d chat
```

### Servidor de acciones

Algunas de las respuestas del chatbot no son cadenas de texto emitidas directmanete por el mismo, sino que una acción
procesa el texto y hace peticiones ya sea a una API, base de datos o cualquier otro componente externo. Por lo tanto,
es necesario poner en marcha el servidor de acciones para que Rasa sepa dónde ir a buscar una respuesta. Para ello sólo
hay que ejecutar el siguiente comando:

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d rasa
```

### Aplicación de API

Es la aplicacion que presta servicio a la aplicacion Web de administracion y se conecta con la base de datos de mongodb

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d api
```


### Aplicación del Ner

Es la aplicacion que ayuda al chatbot a encontrar en las frases de texto introducidas las entidades nombradas (personas, lugar, organizacion y miscelaneas)

```bash
docker-compose -f ./src/main/docker/docker-compose.yml --project-name chatbot --project-directory .  up -d ner
```

### Entrenamiento del modelo

Si se quisiera reentrenar el modelo, ya sea por qué se ha cambiado alguna intención, añadido alguna historia o modificado
alguna respuesta del dominio, se debería leer el documento [(entrenamiento.md)entrenamiento.md]  para reentrenar:

No es necesario entrenar si se ha cambiado algo dentro de alguna accion, este cambio se verá reflejado relanzando el
servidor de acciones tal y como se ha indicado previamente.

### Ejecución tests

Se han creado test unitarios para:
- las acciones
- la clase que conecta con sparql y genera las consultas
- los formularios

Se han creado test para comprobar los datos de la base de datos de sparql
- verificar que las fuentes de información mantiene la misma estructura que la esperada


Para lanzar los test se ejecuta el siguiente comando

```bash
docker run -it --rm --name test --network=chatbot_chatbot-network  -e PYTHONPATH=./:./tests/ rasa:1.0 /bin/bash -c 'pip install mock; python3 -m unittest'
```
