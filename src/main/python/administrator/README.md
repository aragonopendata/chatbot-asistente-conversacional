## GUIA DE USO DEL PROYECTO CHATBOT

En esta guía se va a especificar que componentes forman el proyecto del chatbot, su funcionamiento y su puesta en marcha.

### Aplicación Flask

En el script ```app_chat.py``` se encuentra la funcionalidad principal para hablar con el chatbot. Para poner en marcha el chatbot ejecutar:

```bash
python app_chat.py [port_number]
```

### Servidor de acciones

Algunas de las respuestas del chatbot no son cadenas de texto emitidas directmanete por el mismo, sino que una acción 
procesa el texto y hace peticiones ya sea a una API, base de datos o cualquier otro componente externo. Por lo tanto, 
es necesario poner en marcha el servidor de acciones para que Rasa sepa dónde ir a buscar una respuesta. Para ello sólo 
hay que ejecutar el siguiente comando:

```bash
rasa run actions
```

### Entrenamiento del modelo

Si se quisiera reentrenar el modelo, ya sea por qué se ha cambiado alguna intención, añadido alguna historia o modificado 
alguna respuesta del dominio, se debería ejecutar el siguiente comando para reentrenar:

```bash
python train_model.py
```

No es necesario entrenar si se ha cambiado algo dentro de ```actions.py```, este cmabio se verá reflejado relanzando el 
servidor de acciones tal y como se ha indicado previamente.

### Ejecución tests

Se ha creado una carpeta con ficheros con tests para comprobar el correcto funcionamiento del agente. Se han instalado 
dos nuevas dependencias
```pytest``` y ```pytest-dependency```. 

Antes de ejecutar los tests, se debe generar un fichero json con los datos contenidos en la base de datos de SPARQL, 
para ello ejecutar el siguiente script:
```bash
python browser/sparql_data_to_json.py ó cd browser_module && python sparql_data_to_json.py
```
Si no funciona, cambiar de directorio y ejecutarlo desde dentro de ```browser_module```

Además es necesario tener el servidor de acciones levantado.

RECORDATORIO LANZAR ACCIONES:
```bash
rasa run actions
```

Para pasar los tests, ejecutar el siguiente comnando:

```bash
python -m pytest -rsxpP [-p no:warnings]
```

El último parámetro es opcional, evita que los warnings se muestren por pantalla, los warnings son de versiones de 
otras librerias que tienen algún método deprecated


## GUIA USO ADMINISTRADOR

Se lanzan tanto el back-end del configurador, como el back-end de entrenamiento. Para ello:

```bash
python app.py [port_number]
python app_train.py [port_number]
```
