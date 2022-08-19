# Aragón Open Data

Aragón Open Data ha ido llevando a cabo una progresiva liberación de información del sector público. Esta apertura ha ido aumentando el conjunto de datos disponibles, el conjunto de los formatos de reutilización y mejorando el modo de acceso a todos estos recursos. Igualmente ha ido generando un conjunto de herramientas que permiten el mantenimiento de toda la infraestructura de Aragón Open Data.
Con el objeto de acercar más a la ciudadanía toda la información existente en Aragón Open Data, se ha propuesto el desarrollo de un asistente virtual (chatbot) que proporcione a los ciudadanos la ayuda necesaria para extraer la información existente en Aragón Open Data en relación a los siguientes temas:

- Turismo y viajes en Aragón
- Información general sobre Aragón y su territorio.
- Asistencia técnica o preguntas frecuentes en materia de sociedad de la información.
- Transporte
- Agricultura
El propósito del documento es realizar un análisis y diseño del chatbot que permita definir los requisitos y la estructura que va a tener el asistente conversacional. Las partes principales de las que va a constar este documento son:
- Definición de los casos de uso que forman parte del asistente virtual tanto de la interacción con el usuario como la parte del panel de control y de administración.
- Diseño del Interfaz de Usuario.
- Descripción de la arquitectura del sistema.
- Interfaces de comunicación
- Criterios de usabilidad y accesibilidad
- Criterios de Validación

## Descripción del contenido

- src\main\python\administrator\

Contiene el todo código chatbot y algoritmos usados para generar el asistente conversacional, así como el uso de la librería open source RASA que se ha empleado para desarrollar el chatbot.
- http://opendataei2a.aragon.es/servicios/chatbot/model/glove_all.tar.gz modelo del Ner
- http://opendataei2a.aragon.es/servicios/chatbot/model/model_glove_all_char100_300_3.weights.tar.gz modelo del Ner
- https://opendataei2a.aragon.es/servicios/chatbot/model/model-chatbot.tar.gz  Modelos conversacionales

Contiene los modelos conversacionales que usan los algoritmos para dar respuestas a las preguntas de los usuarios.

- src\main\python\administrator\actions_module\ -> Conectores a bases de datos

Contiene los conectores a las bases de datos para obtener las respuestas a las preguntas de los usuarios.

- src\src\main\nodejs\ -> Servidor web de estadísticas de uso y modificación del chatbot.

Contiene el código del servidor web para ver las estadísticas de uso del chatbot y el interface para modificar el modelo de una forma sencilla.

- src\src\main\mongo\ -> Estructura y datos de la base de datos conversacional

Base de datos en donde se almacena el modelo conversacional en detalle.

- src\main\docker\ -> Generación de dockers

Contiene los scripts de generación de dockers para el despligue en contenedores.

- src\test\ -> Scripts de pruebas automáticas.

Contiene los scritps de pruebas automáticas para la comprobación del correcto funcionamiento del chatbot.
