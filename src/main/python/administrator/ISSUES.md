## Pending

+ ¿Por qué salen dos answer en "¿Qué es la firma digital"
+ "Cuantas hectareas de suelo rústico hay en Aragón" sale del 2016 y se espera de 2014
+ Falta la intención de construcción de edificios para preguntas como "Cual es la fecha de construcción de los edificios de Zaragoza"
+ "Cuantas plazas hoteleras hay en Zaragoza" ¿Qué intención es esta?
+ "Cuantas habitaciones dobles tiene Casa Jaime" Falta accommodation type y slot person para sacarlo con el tracker y no hacer una segunda invocación al NER
+ Si se pasan localizaciones con mayúsculas da problemas para extraer las entidades con el NER
+ "comarca la Jacetania" saca "comarca" como location y "Jacetania" como regex
+ "Que tipo de cultivos hay en Zaragoza" ¿Qué pregunta es esta?
+ En 2011 había 6 millones de parados en la provincia de Zaragoza????
+ ¿Hay oficinas de turismo en Zaragoza?
+ En ci.digital_certificate_moreInfo hay un ejemplo con ${digital_signature}
+ En ci.digital_signature_install los hay con ${digital_certificate}
+ tourism.path_routes_in_out se lia con tourism.path_routes_out si se utiliza una ciudad que aparezca en los ejemplos
+ Mongo tiene dependencias en cascada no implementadas, por ejemplo cuando se cambia el nombre de una intención y aparece en alguna historia debería cambiarse, lo mismo con entidades en intenciones, etc.
+ action_land_uses tiene una comprobación de años entre 1900 y 2100 ¿?
+ Cuando salta una excepción se devuelve al usuario
+ Lista concejales se dividen por población pero el enlace tiene TODOS los concejales sin separar. Poner un enlace por población? Me refiero a browser.url
+ Cuando se pregunta por provincia y usos de suelo, en la query sale municipio
+ A la hora de formar las fechas en "action_contracts" se da por supuesto que el values vendrá una lista vacia, sería mejor recorrer la lista de entiades al revés: reversed(entities)
+ En el municipio de Zaragoza hay 1 casas rurales, plural cuando es sólo uno
+ action_acommodation_size, action_councilors, ¿mostrar url? son listas
+ Apartamentos de casa rural no existe la historia ni la acción
+ Cuando se pregunta por algo de acommodation sin especificar, por defecto se usa hotel, pero por ejemplo si se llama Casa Broto, podríamos deducir que es casa rural
+ Cuando se pide información de un guía turístico, se responde con lo primera información y puede que haya más: por ejemplo Dalda Abril Hilario
+ Oficinas de turismo de Zaragoza se guardan con etiqueta "ZARAGOZA297" y además no tienen teléfono ¿que hacer?
+ project_id y model_id sobran de absolutamente todo, el identificador único de cada documento es más que suficiente, es establecer características d elsa bases de datos relacionales en una base de datos no relacional
+ Flags de deleted y modified faltan en la base de datos
+ Todas las operaciones CRUD se pueden hacer desde el lado del cliente (Kike)
+ Filtrar por localización exacta cuando devuelve algo así:
[{'answer0': '52555',
  'etiqueta': 'http://opendata.aragon.es/recurso/territorio/Municipio/Huesca'},
 {'answer0': '172',
  'etiqueta': 'http://opendata.aragon.es/recurso/territorio/Municipio/Adahuesca'},
 {'answer0': '295',
  'etiqueta': 'http://opendata.aragon.es/recurso/territorio/Municipio/Casbas_de_Huesca'}]
+ diaptcher.utter_message(str(ex)) -> dispatcher.utter_message("Ha ocurrido un problema en el servidor")
+ Tests que ejecutan una acción que devuelven varios utter_message?? Comprobar todos los mensajes?
+ En la población, la respuesta viene en una URL, problema con Teruel pues al buscar el valor exacto de la localización no se machea :URL tiene "Comunidad de Teruel" no "Teruel", si busco por la última parte de la URL spliteada da problemas Huesca ya que "Csabas de Huesca" acaba en Huesca y saca los dos
+ Clases de configuracion para cada uno de los servidores: dev, pre, prod https://github.com/kevinqqnj/flask-template-advanced/blob/master/config.py ó https://gist.github.com/M0r13n/0b8c62c603fdbc98361062bd9ebe8153

## Solved

+ Arreglo ejemplos y añadidos algunos en las intenciones de información ciudadana
+ Arreglado Swagger
+ Iconos de tiempo
