# Manual de entrenamiento del Chatbot

## Generacion de los ficheros de entrenamientos

Los datos de los ficheros de entrenamiento estan en varios formatos. Primero se deben juntar antes de crear el modelo.

### Origen de los datos para el entrenamiento

El origen de los datos parte de la base de datos de MongoDb y del fichero ./data/GDA/AOD/forms.yml y ./data/GDA/AOD/rules.yml
En los datos de Mongodb estan las acciones _utter_, las intenciones con sus textos, las entidades y las reglas.
En el fichero ./data/GDA/AOD/forms.yml se ha establecido los datos necesario para hacer funcionar el formulario.
En el fichero ./data/GDA/AOD/rules.yml se ha establecido una regla genérica que se concatenará con las reglas de la base de datos

### activar el entorno de Python

- El entorno de Python se crea con el fichero (requerimients.txt)

### Generar los ficheros

Para entrenar el modelo del chatbot, primero se han de generar los datos de entrenamiento. Para generar estos datos,
existe un proceso que se conecta a la base de datos de mongodb, donde estan las rules, entities y intents -> frases que lanzan la intencion.

El fichero que genera los ficheros es scripts/generate_files.py

```bash
PYTHONPATH=./ python3 scripts/generate_files.py
```

Al lanzar este script, generar los ficheros de train_data.yml rules.yml y domain.yml

### ficheros adicionales

En la carpeta de ./administrator/data/GDA/AOD/*.yml existen un conjunto de ficheros de loookup para introducir mejoras en la deteccion de las entidades. Estos ficheros se copian en  ./administrator/data/training/nlu/ para mejorar el modelo.

## Creacion del modelo

El modelo se crea a partir de los datos generados por el proceso anterior y son dejados en la carpeta ./administrator/data/training/

### configurar del pipeline

El modelo usa como base de entrenamiento el fichero  config.yml. Ir a Rasa para mas informacion.

### Lanzar el entrenamiento. Existen 2 modelos diferentes NLU y CORE

Para entrenar los modelos desde los comandos de rasa se lanza desde el path del proyecto de python el comando de "rasa train"

Es importante lanzar el modelo a mano porque existen componente que no son generados desde la base de datos de mongo

-  Al añadir los formularios de Rasa, no se introducen las entidades de los formularios ni los datos de entrenamiento de formularios.
-  si no se meten estos datos no es capaz el sistema de extraer corectamente la intención.

Para seleccionar la trajeta gráfica se usa la siguiente variable de entorno

```bash
export CUDA_VISIBLE_DEVICE=1
```

### NLU

NLU es el encargado del lenguaje y core se encarga de las reglas (intencion -> accion ) e historias (conjunto de pasos intenciones y acciones)

Lanza el modelo de entrenamiento pero sin conectarse al domino de rasa. Se suele usar para debugear el modelo, al no lanza las acciones de Python
Solo entrena NLU
rasa train --data data/training/nlu

puedes validar el modelo de NLU con el comando de Rasa

```bash
rasa shell
```

### CORE

Si no generas core no llama a las acciones de rasa
Una vez que está validado NLU puedes entrenar el modelo de core (al ser reglas cuesta 5 segundos )
rasa train --data data/training/nlu   -c config.yml -d  data/training/domain.yml --num-threads 50

rasa shell -m ./src/main/python/administrator/models/20211214-181951.tar.gz

## TEST
rasa test nlu --nlu ./data/training/nlu --cross-validation -c ./config.yml