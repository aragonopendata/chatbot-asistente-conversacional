# Manual de entrenamiento de los datos del chatbot

## Generar los ficheros
Para entrenar los datos del chatbot se usan los datos de la ruta src\main\python\administrator\data\training\nlu.

Se genera el entorno con el fichero que existe en src\main\python\administrator\requierments.txt

## editar
Se pueden edita los ficheros de los datos para introducir mejoras.

## configurar del pipeline
Se entrena el modelo a partir de la configuracion del fichero de config.yml

## Lanzar el entrenamiento. Existen 2 modelos diferentes NLU y CORE
Para entrenar los modelos desde los comandos de rasa se lanza desde el path del proyecto de python el comando de "rasa train"

### NLU
NLU es el encargado del lenguaje y core se encarga de las reglas (intencion -> accion ) e historias (conjunto de pasos intenciones y acciones)

Lanza el modelo de entrenamiento pero sin conectarse al domino de rasa (bueno para debugear el modelo ) no lanza las acciones

El comando para entrenar NLU es
```
rasa train --data data/training/nlu
```
puedes validar el modelo de NLU con  "rasa shell"

### CORE
Una vez que está validado NLU puedes entrenar el modelo de core

```
rasa train --data data/training/nlu   -c config.yml -d  data/training/domain.yml --num-threads 50
```

Generará un fichero de modelo que es encesario copiar dentro de los contenedores para hacer funcionar al chatbot.

Para probar el modelo desde la consola se lanza

```
rasa shell -m path_new_model.tar.gz
```

## TEST
rasa test nlu --nlu ./data/training/nlu --cross-validation -c ./config.yml