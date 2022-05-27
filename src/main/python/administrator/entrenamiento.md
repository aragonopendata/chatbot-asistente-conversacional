# Manual de entrenamiento del Chatbot

## TL;DR

Para recrear el modelo lanza el comando. Este comando generará una nueva imagen rasa:1.1 que se usará en el relanzamiento del docker-compose

```bash
./src/main/script/training.sh
```

## Estructura de directorios

A continuacion se describen cada una de las rutas que se usan en el entrenamiento de los datos
- Ruta donde se almacena el modelo **./models/GDA/AOD/**
- datos estáticos para realizar el entrenamiento **./data/GDA/AOD/**
- datos generados para realizar el entrenamiento **./data/training/nlu/**

## Generacion de los ficheros de entrenamientos

Los datos de los ficheros de entrenamiento estan en varios formatos. Primero se deben juntar antes de crear el modelo.

### Origen de los datos para el entrenamiento

El origen de los datos parte de la base de datos de MongoDb y del fichero ./data/GDA/AOD/forms.yml y ./data/GDA/AOD/rules.yml
En los datos de Mongodb estan las acciones _utter_, las intenciones con sus textos, las entidades y las reglas.
En el fichero ./data/GDA/AOD/forms.yml se ha establecido los datos necesario para hacer funcionar el formulario.
En el fichero ./data/GDA/AOD/rules.yml se ha establecido una regla genérica que se concatenará con las reglas de la base de datos

### Generar los ficheros

Para entrenar el modelo del chatbot, primero se han de generar los datos de entrenamiento. Para generar estos datos,
existe un proceso que se conecta a la base de datos de mongodb, donde estan las rules, entities y intents -> frases que lanzan la intencion.

El fichero que genera los ficheros es scripts/generate_files.py

Cómo generar los ficheros para entrenar el modelo

```bash
docker run --name training  --network=chatbot_chatbot-network --rm -e PYTHONPATH=./  -it rasa:1.0  python3 scripts/generate_files.py
```

Al lanzar este script, generar los ficheros de train_data.yml rules.yml y domain.yml en ./data/training/nlu

### ficheros adicionales

En la carpeta de ./data/GDA/AOD/*.yml existen un conjunto de ficheros de loookup para introducir mejoras en la deteccion de las entidades. Estos ficheros ya exiten en ./data/training/nlu/ y son usado para mejorar el modelo.

## Creacion del modelo

El modelo se crea a partir de los datos generados por el proceso anterior.

### configurar del pipeline

El modelo usa como base de entrenamiento el fichero config.yml. Ir a Rasa para mas informacion.

### Lanzar el entrenamiento. Existen 2 modelos diferentes NLU y CORE

Para entrenar los modelos desde los comandos de rasa se lanza desde el path del proyecto de python el comando de "rasa train"

### NLU

NLU es el encargado del lenguaje y core se encarga de las reglas (intencion -> accion ) e historias (conjunto de pasos intenciones y acciones)

Lanza el modelo de entrenamiento pero sin conectarse al domino de rasa. Se suele usar para debugear el modelo, al no lanza las acciones de Python

Para entrena solo el modelo de NLU lanza se lanza el siguiente comando. Este comando generará los ficheros y lanzara la generacion del modelo

```bash
docker run --name training  --network=chatbot_chatbot-network -e PYTHONPATH=./ -it rasa:1.0 /bin/bash -c ' python3 scripts/generate_files.py; rasa train --data data/training/nlu'
```

comando para guardar el modelo de NLU para su posterior evaluacion y uso se guarda como la imagen **training-nlu:1.0**

```bash
docker commit training training-nlu:1.0
```

Este commando de docker lanza la imagen guardada con el modelo de NLU para su evaluacion

```bash
docker run  -it --rm --name test-nlu --network=chatbot_chatbot-network  training-nlu:1.0 /bin/bash -c 'rasa shell '
```

Este comando da la posiblilidad de evaluar el modelo lanzando frases y se visualizarán los resultados

### CORE

Una vez que ha sido evaluado el modelo de NLU, se debe entrenar el modelo de CORE a partir de la imagen guardada **training-nlu:1.0**

```bash
docker run  -it --name training --network=chatbot_chatbot-network training-nlu:1.0 /bin/bash -c 'python3 scripts/generate_files.py; rasa train --data data/training/nlu -c config.yml -d data/training/domain.yml --num-threads 50 --out /python/administrator/models/GDA/AOD/ --fixed-model-name model-chatbot'
```

Una vez que se ha generado el modelo se puede guardar la imagen como nueva version de rasa

```bash
docker commit training rasa:1.1
```

Para lanzar la nueva imagen de Rasa:1.1, se seleccionará en el docker-compose la variable de entorno de --env-file ./src/main/docker/.rasa1.1

También se puede lanzar el nuevo modelo con la version de la imagen rasa:1.1 para evaluarlo

```bash
docker run  -it --rm --name test-model --network=chatbot_chatbot-network rasa:1.1  /bin/bash -c 'rasa shell --model /python/administrator/models/GDA/AOD/model-chatbot.tar.gz '
```

## TEST

Si se quiere evaluar el modelo de clasificacion de las intenciones se puede lanzar el siguiente comando

```bash
rasa test nlu --nlu ./data/training/nlu --cross-validation -c ./config.yml
```
