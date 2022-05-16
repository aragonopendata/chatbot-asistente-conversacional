# Manual de entrenamiento de los datos del chatbot

## Generar los ficheros
Para entrenar el chatbot primero se han de generar los datos de entrenamiento. Para generar estos datos,
existe un proceso que se conecta a la base de datos de mongodb, donde estan las rules, entities y intents -> frases que lanzan la intencion.  Hay que abrir la conexion con AST para conectar con mongodb.

El fichero que genera los ficheros es train_model.py (también entrena el modelo, pero no es conveniente lanzarlo así el entrenamiento )

Lo que hace es generar el fichero de domain.yml train_data.yml rules.yml
## editar
Se pueden edita los ficheros para introducir mejoras.

## configurar del pipeline
como se entrena el modelo se realiza a partir del fichero de config.yml (me ha costado un monton dejarlo como está), pero se prodría tocar

## Lanzar el entrenamiento. Existen 2 modelos diferentes NLU y CORE
Para entrenar los modelos desde los comandos de rasa se lanza desde el path del proyecto de python el comando de "rasa train"

Es importante lanzar el modelo a mano porque existen componente que no son generados desde la base de datos de mongo.
 - al añadir los formularios de rasa, no se introducen las entidades de los formularios ni los datos de entrenamiento de formularios.
 - si no se meten estos datos no es capaz el sistema de extraer corectamente la intención. (tengo dudas si esto es porque no existe una historia que diga los paso ha realizar )

### NLU
NLU es el encargado del lenguaje y core se encarga de las reglas (intencion -> accion ) e historias (conjunto de pasos intenciones y acciones)

Lanza el modelo de entrenamiento pero sin conectarse al domino de rasa (bueno para debugear el modelo ) no lanza las acciones

Solo entrena NLU
rasa train --data data/training/nlu

puedes validar el modelo de NLU con  "rasa shell"

### CORE
Si no generas core no llama a las acciones de rasa
Una vez que está validado NLU puedes entrenar el modelo de core (al ser reglas cuesta 5 segundos )
rasa train --data data/training/nlu   -c config.yml -d  data/training/domain.yml --num-threads 50

rasa shell -m /data/jvea/chatbot/src/main/python/administrator/models/20211214-181951.tar.gz

## TEST
rasa test nlu --nlu ./data/training/nlu --cross-validation -c ./config.yml