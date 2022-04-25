<img src="http://presupuesto.aragon.es/static/assets/logo-gobierno-aragon.png" height="28px" /><span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>![Logo Aragón Open Data](budget_app/static/assets/logoAragonOpenData.png)

## GUIA DE USO DEL PROYECTO CHATBOT

En esta guía se va a especificar que componentes forman el proyecto del chatbot, su funcionamiento y su puesta en marcha.

### Aplicación chatbot

Aplicacion Web del cliente que interactua con el chatbot

### Aplicación Ner

Detector de entidades espeífico del dominio de Aragón

### Aplicación web

Dashboard de estadisticas de uso interno.

### Servidor de acciones de Rasa
Servicio que implementa las acciones en Python

### Servidor nginx
se usa para redirigir el tráfico entrante y publicar el modelo binario del chatbot

Para copiar el modelo y hacerlo publico se ejecuta este comando

docker cp  argon-nginx:/etc/nginx/conf.d/model/ model-chatbot.tar.gz

### Entrenamiento del modelo

La guía para entrenar el modelo esta en [`entrenamiento.md`](src\main\python\administrator\entrenamiento.md)

El modelo se copia dentro de la imagen del chatbot en la siguiente ruta.

    /python/administrator/models/GDA/AOD

### Ejecución tests

Los ficheros de test unitarios y de integracion estan en el directorio src\main\python\administrator\tests

Para lanzar los test hay que seleccionar o instalar el entorno de python y una vez seleccionado lanzar el comando
Esto lanzará todos los test, unitarios y de generacion de sentencias sparql contra la base de datos de opendata
```bash
python -m unittest -s -d ./tests/
```


## GUIA USO ADMINISTRADOR


para generar los docker se lana el siguiente comando

```bash
bash .\src\main\script\build-compose.sh

```
para lanzar los docker se lana el siguiente comando
```bash
bash .\src\main\script\start-compose.sh

```
