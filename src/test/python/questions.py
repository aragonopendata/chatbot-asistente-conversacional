'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import requests
import time
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError

from cmd import *
from pprint import pprint

CHAT_ROOM_URL = "http://127.0.0.1:5000"

QUESTIONS_ANSWERS_ARAGON_TEXT =[
    {"Que usos se la dio al suelo en Zaragoza en 2004":"No se han encontrado datos de los usos que se le da al suelo de Zaragoza en 2004."},
    {"a que comarca pertenece la poblacion de Fraga":"Fraga se encuentra en la comarca Bajo Cinca/baix Cinca."},
    {"a que comarca pertenece la poblacion de Teruel":"Teruel se encuentra en la comarca Comunidad de Teruel."},
    {"Cuantas hectareas de suelo rustico hay en Zaragoza":"En 2016 las hectáreas de suelo rustico en el municipio de Zaragoza son 87293.5\n"},
    {"Cuantas hectareas de suelo rustico hay en la provincia de Huesca":"En 2016 las hectáreas de suelo rustico en la provincia de Huesca son 1554730.0\n"},
    {"Cuantas hectareas de suelo rustico hay en Aragon ":"En 2016 las hectáreas de suelo rustico en Aragón son 4728900.0\n"},
    {"Cuantos habitantes hay en Zaragoza en 2018":"La población en el municipio de Zaragoza en 2018 es de 666880 habitantes."},
    {"cuantos habitantes habia en la provincia de Teruel en 2005":"La población en la provincia de Teruel en 2005 es de 141091 habitantes."},
    {"cuantos habitantes habia en la comarca de Teruel en 2005":"La población en la comarca de Comunidad De Teruel en 2005 es de 44806 habitantes."},
    {"cuantos habitantes habia en la Aragon en 2011":"La población en Aragón en 2011 es de 1346293 habitantes."},
    {"Cual es la direccion del ayuntamiento de Zaragoza": "El ayuntamiento de Zaragoza está en Pza. del Pilar, 18."},
    {"Cual es la direccion del ayuntamiento de Fraga":"El ayuntamiento de Fraga está en Pso. Barron 1."},
    {"Cual es la direccion del ayuntamiento de Teruel":"El ayuntamiento de Teruel está en Pza. Catedral, 1."},
    {"Cual es fax del ayuntamiento de Zaragoza":"El fax del ayuntamiento de Zaragoza es 976 399 304."},
    {"Cual es fax del ayuntamiento de Huesca":"El fax del ayuntamiento de Huesca es 974 292 163."},
    {"Cual es fax del ayuntamiento de Teruel":"El fax del ayuntamiento de Teruel es 978 603 715."},
    {"Cual es el CIF del ayuntamiento de Zaragoza":"El CIF del ayuntamiento de Zaragoza es P-5030300-G."},
    {"Cual es el CIF del ayuntamiento de Fraga":"El CIF del ayuntamiento de Fraga es P-2215500-F."},
    {"Cual es el CIF del ayuntamiento de Teruel":"El CIF del ayuntamiento de Teruel es P-4422900-C."},
    {"Cual es la teléfono del ayuntamiento de Zaragoza":"El teléfono del ayuntamiento de Zaragoza es 976 721 100."},
    {"Cual es la teléfono del ayuntamiento de Fraga":"El teléfono del ayuntamiento de Fraga es 974 470 050."},
    {"Cual es la teléfono del ayuntamiento de Teruel":"El teléfono del ayuntamiento de Teruel es 978 619 900."},
    {"Cual es el email del ayuntamiento de Zaragoza":"El email del ayuntamiento de Zaragoza es gabinetealcaldia@zaragoza.es."},
    {"Cual es el email del ayuntamiento de Fraga":"El email del ayuntamiento de Fraga es ayuntamiento@fraga.org."},
    {"Cual es el email del ayuntamiento de Teruel":"El email del ayuntamiento de Teruel es alcaldia.aytoteruel@teruel.net."},
    {"Como se llama el alcalde de Monzon":"Monzon esta presidida por Isaac Claver Ortigosa"},
    {"cuantas hectareas de superficies artificiales hay la provincia de Zaragoza":"En la provincia de Zaragoza hay 25833.1 hectareas de superficies artificiales"},
    {"cuantas hectareas de superficies de agua hay la comarca de Teruel":"En la comarca de Comunidad de Teruel hay 129.668 hectareas de superficies de agua"},
    {"cuantas hectareas de zonas humedas en Zaragoza":"En el municipio de Zaragoza hay 27.7697 hectareas de zonas humedas"},
    {"cuantas hectareas de zonas agricolas hay la provincia de Zaragoza":"En la provincia de Zaragoza hay 1073480.0 hectareas de zonas agricolas"},
    {"cuantas hectareas de zonas forestales con vegetacion natural y espacios abiertos hay en Aragon":"En Aragón hay 2369290.0 hectareas de zonas forestales con vegetacion natural y espacios abiertos"},
    {"Cuantos incendios hubo en Zaragoza en 2010":"En el municipio de Zaragoza hubo 10 incendios durante el año 2010"},
    {"Cuantos incendios hubo en la comarca de Teruel en 2010":"En la comarca de Comunidad de Teruel hubo 11 incendios durante el año 2010"},
    {"Cuantos incendios hubo en Aragon en 2010":"En Aragón hubo 342 incendios durante el año 2010"},
    {"cuantas hectareas se quemaron en Zaragoza en el año 2010":"En el municipio de Zaragoza se quemaron 3.28 hectáreas durante el año 2010."},
    {"cuantas hectareas se quemaron la comarca de Teruel en el año 2010":"En la comarca de Comunidad de Teruel se quemaron 22.06 hectáreas durante el año 2010."},
    {"cuantas hectareas se quemaron en Aragon en el año 2010":"En Aragón se quemaron 1144.03 hectáreas durante el año 2010."},
    {"cuantas depuradoras habia en la provincia de Zaragoza en el año 2014":"En la provincia de Zaragoza había 82 plantas depuradoras en 2014."},
    {"cuantas depuradoras había en Aragón en el año 2014":"En Aragón había 187 plantas depuradoras en 2014."},
    {"Cuántas empresas del sector servicios hay en la provincia de Zaragoza":"En la provincia de Zaragoza hay 994224 empresas del sector servicios."},
    {"Cuántas empresas del sector servicios hay en Aragon":"En Aragón hay 1377462 empresas del sector servicios."},
    {"¿Cuántos autónomos hay dados de alta en marzo del 2012 en Aragon?":"103638 personas se dieron de alta como profesionales por cuenta propia en el mes de marzo del 2012 en Aragón"},
    {"¿Cuántos hombres autónomos hay dados de alta en marzo del 2012 en la comarca de Teruel?":"2546 hombre se dieron de alta como profesionales por cuenta propia en el mes de marzo del 2012 en la comarca de Comunidad de Teruel"},
    {"¿Cuántos mujeres autónomas hay dadas de alta en marzo del 2012 en Aragón?":"34458 mujeres se dieron de alta como profesionales por cuenta propia en el mes de marzo del 2012 en Aragón" },
    {"Empresas de 1 a 9 trabajadores en marzo de 2012 en la provincia de Teruel": "En 03 de 2012 había en la provincia de Teruel 4254 empresas de 1 a 9 trabajadores" },
    {"¿Cuántos parados hay en el sector servicios en provincia de Zaragoza en 2011?":"En 2011 había 517037 desempleados en la provincia de Zaragoza en el sector servicios" },
    {"¿Cuántos nuevos contratos hubo en marzo en marzo de 2012 en la comarca la Jacetania?":"En marzo de 2012 se contrataron 416 personas en la comarca de La Jacetania"},
    {"¿Cuántos nuevos contratos de hombres hubo en marzo en marzo de 2012 en la comarca la Jacetania?":"En marzo de 2012 se contrataron 201 hombres en la comarca de La Jacetania"},
    {"¿Cuántos nuevos contratos de mujeres hubo en marzo en marzo de 2012 en la comarca la Jacetania?":"En marzo de 2012 se contrataron 215 mujeres en la comarca de La Jacetania"},
    {"¿Cuántos accidentes laborales en 2011 en la municipio de Zaragoza?":"En 2011 hubo 2066 accidentes laborales en el municipio de Zaragoza"},
    {"¿Cuántos accidentes laborales en 2011 en la provincia de Zaragoza?":"En 2011 hubo 10 accidentes laborales en la provincia de Zaragoza"},
    {"¿Cuántos accidentes laborales en 2011 en la comarca de Teruel?":"En 2011 hubo 133 accidentes laborales en la comarca de Comunidad de Teruel"},
    {"¿Cuántos accidentes laborales en 2011 en Aragon?":"En 2011 hubo 73 accidentes laborales en Aragón"},
    {"¿Cual fue la renta per capita en 2011 en la municipio de Zaragoza?":"En 2011 la renta per capita fue de 17272.7 en el municipio de Zaragoza."},
    {"¿Cual fue la renta per capita en 2011 en la provincia de Zaragoza?":"En 2011 la renta per capita fue de 15901.2 en la provincia de Zaragoza." },
    {"¿Cual fue la renta per capita en 2011 en la comarca de Teruel?":"En 2011 la renta per capita fue de 16471.3 en la comarca de Comunidad de Teruel."},
    {"¿Cual fue la renta per capita en 2011 en Aragon?":"En 2011 la renta per capita fue de 15731.0 en Aragón."},
    {"¿cuantos incendios hubo en aragon en 2012?":"En Aragón hubo 553 incendios durante el año 2012"},
    {"cuantos incendios hubo en Zaragoza en 2012?":"En el municipio de Zaragoza hubo 13 incendios durante el año 2012"},
    {"¿Cuántas plazas tiene el restaurante Garnet?":"No he encontrado cuantas plazas tiene el restaurante/bar Garnet."},
    {"¿Cuántos edificios de más de 20 años hay en Zaragoza?":"Se construyeron en el municipio de Zaragoza 221749 edificios"},

]

QUESTIONS_ANSWERS_ARAGON_LEN=[

    {"Que usos se la dio al suelo en Zaragoza":8},
    {"Cual es la fecha de construcción de los edificios de Zaragoza":13},
    {"Cual es la fecha de construcción de los edificios de Huesca":13},
    {"Cual es la fecha de construcción de los edificios de la comarca de Teruel":13},
    {"Como se llaman los concejales  de Monzon":6}
]


QUESTIONS_ANSWERS_ACTIVITIES_TEXT = [ 
    {"cual es el telefono de la guia turistica Hernández Royo":"El teléfono de Hernández Royo Ana Elisa es 976-178273 / 615-084875" },
    {"cual es el email de la guia turistica Hernández Royo":"El email de Hernández Royo Ana Elisa es sastago40@hotmail.com"},
    {"cual es la web del guia turistico Dalda Abril Hilario":"La web de Dalda Abril Hilario es www.elandador.es"},
    {"cual es la direccion de contacto del guia turistico Dalda Abril Hilario":"La información de contacto de Dalda Abril Hilario es dalda.hilario@gmail.es, 978-700381 / 651-300984, DALDA ABRIL HILARIO" },
    {"¿Dame la dirección del apartamento Maribel?":"La dirección del apartamento MARIBEL es AVDA. CATALUÑA, 45, CALACEITE (44610)." },
    {"¿Cuál es la dirección del apartamento Maribel?":"La dirección del apartamento MARIBEL es AVDA. CATALUÑA, 45, CALACEITE (44610)." },
    {"¿Tiene el hotel La Bodega habitaciones cuádruples?":"En hotel LA BODEGA hay 37 habitaciones cuádruples." }
  
]


QUESTIONS_ANSWERS_ACTIVITIES_LEN = [
   
    {"Que obras tiene el museo Pablo Gargallo":200},
    {"cuales son las rutas que salen de Jaca":4},
    {"cuales son las rutas que llegan a Jaca":4},
    {"cuales son las rutas que pasan por Jaca":5},
    {"que rutas empiezan Pamplona y terminan en Jaca":1},
    {"Dime guias de turismo de la comarca RIBERA BAJA DEL EBRO": 3 },
    {"Dirección de las oficinas de turismo de Zaragoza": 7 },
    {"Cuantas plazas hoteleras hay en Zaragoza":15},
    {"Teléfonos de las oficinas de turismo de Zaragoza":2},
    {"Teléfonos de las oficinas de turismo de Teruel":2}
]

QUESTIONS_ANSWERS_ACCOMODATION_TEXT = [ 
    
    {"Cual es el teléfono del restaurante Lacasta":"El teléfono de Taberna Doña Casta es 976205852."},
    {"Cual es el fax del restaurante Pepito Casanova":"El fax de Pepito Casanova es 974345223."},
    {"Cual es el email del restaurante Fajardo":"El email de Fajardo es asadorfajardo@hotmail.com."},
    {"Cual es la web del restaurante Basho Cafe":"La web de Basho Cafe es www.bashogastro.com."},
    {"Cual es la direccion del restaurante Fajardo":"Fajardo está en AVDA. MONTAÑANA, 244, MONTAÑANA (50059)."},
    {"Como puedo reservar en el restaurante Fajardo":"Puedes reservar de diferentes formas en el restaurante FAJARDO : mandando un email a asadorfajardo@hotmail.com, llamando a 976575763 o yendo al local de la AVDA. MONTAÑANA, 244."},
    {"¿Cuál es el aforo del asador FAJARDO?":"Las plazas de FAJARDO son 56"},
    {"Donde esta el restaurante PALENQUE":"PALENQUE está en C/ HERMANOS GAMBRA, 10, ZARAGOZA (50010)."},        
    {"Cuantos restaurantes hay en Borja":"En Borja hay 7 sitios donde poder tomar algo"},    
    {"Cuantos restaurantes hay en Zaragoza":"En Zaragoza hay 1211 sitios donde poder tomar algo"},
    {"Cual es el FAX del camping Valle de Tena":"El fax del camping CAMPING VALLE DE TENA, S.L.-VALLE DE TENA es 974482551." },
    {"Cual es el teléfono del hotel Boston":"El teléfono del hotel EUROSTARS BOSTON-EUROSTARS es 976599192." },
    {"Cual es el email del casa rural Casa Jaime":"El email de la casa rural CASA JAIME es mbalet@hotmail.es." },
    {"Cual la Web de los apartamentos Casa Modesto":"La web del apartamento CASA MODESTO es www.apartamentoscasamodesto.com." },
    {"Cual la direccion del albergue Hermanos Nerin":"La dirección del albergue HERMANOS NERIN, S.C. es C/. FRANCIA, TORLA (22376)." },
    {"Como puedo reservar el camping Valle de Tena":"Puedes reservar en camping CAMPING VALLE DE TENA, S.L.-VALLE DE TENA mandando un email a correo@campipngvalledetena.com o llamando al 974480977." },
    {"Como puedo reservar en el hotel Boston":"Puedes reservar en hotel EUROSTARS BOSTON-EUROSTARS mandando un email a direccion@eurostarsboston.com o llamando al 976599192." },
    {"como puedo reservar la casa rural Casa Jaime":"Puedes reservar en casa rural CASA JAIME mandando un email a mbalet@hotmail.es o llamando al 654176203." },
    {"como puedo reservar en el apartamento PUERTA DE ORDESA":"Puedes reservar en apartamento PUERTA DE ORDESA mandando un email a amayatv@hotmail.com o llamando al 974505101."},
    {"como puedo reservar el albergue ANZÁNIGO":"Puedes reservar en albergue ANZÁNIGO, S.L. mandando un email a info@anzanigo.com o llamando al 974348040."},
    {"cual es la categoría del hotel Boston":"Eurostars Boston-eurostars tiene 4 estrellas"},
    {"que hoteles tienen 5 estrellas en La provincia de Zaragoza":"La lista de hoteles con categoria mayor de 5 en Zaragoza es:\n\t- PALAFOX-PALAFOX HOTELES\n\t- REINA PETRONILA -PALAFOX"},
    {"cuantas habitaciones para 4 personas tiene el hotel Boston": "En hotel EUROSTARS BOSTON-EUROSTARS hay 285 habitaciones cuádruples."},
    {"que servicios proporciona el hotel PARIS CENTRO":"Los servicios de PARIS CENTRO son:\n\t- Restaurante"},
    {"Cuantas casas rurales hay en Torla":"En el municipio de Torla hay 19 casas rurales"},
    {"Cuantas habitaciones tiene el hotel Boston":"En Eurostars Boston-eurostars hay 313 habitaciones"},
    {"Cuantas habitaciones sin baño hay el hotel LOS HERREROS":"En Los Herreros hay 5 habitaciones sin baño."},
    {"Cuantas habitaciones con baño hay el hotel LOS HERREROS":"En Los Herreros hay 15 habitaciones con baño."},
    {"Cuantas habitaciones tiene el hotel PHYSIO NATURAL con baño": "En Physio Natural hay 3 habitaciones con baño."},
    {"Cuantos habitaciones dobles tiene PHYSIO NATURAL": "En hotel PHYSIO NATURAL hay 3 habitaciones dobles."},
    {"donde esta el hotel PALAFOX-PALAFOX": "PALAFOX-PALAFOX HOTELES está en ZARAGOZA."},
    {"Dame el listado de hoteles de Tarazona":"Este es el listado de hoteles en el municipio de Tarazona:\n\t- CONDES DE VISCONTI\n\t- LA MERCED DE LA CONCORDIA\n\t- BRUJAS IRUES\n\t- PALACETE DE LOS ARCEDIANOS\n\t- SANTA AGUEDA"},
    {"¿Cuándo es la temporada baja en el camping CAMPING VALLE DE TENA?":"En CAMPING VALLE DE TENA, S.L.-VALLE DE TENA es temporada baja desde 01/10 hasta 30/11"},
    {"Habitaciones sencillas en el hotel Boston":"En hotel EUROSTARS BOSTON-EUROSTARS hay 28 habitaciones sencillas"},
    {"Cuantas plazas tiene la casa rural Casa del Cura":"La casa rural CASA DEL CURA tiene 4 plazas"},
    {"Cuantas bungalows tiene el Camping Gavin":"Camping Gavin, S.l.-gavin tiene 114 bungalows"},
    {"Cuantas plazas para caravanas tiene el Camping Ainsa": "Camping Ainsa, S.l.-ainsa tiene 16 plazas para caravanas"},
    {"Cuantas parcelas tiene el Camping Ainsa": "Camping Ainsa, S.l.-ainsa tiene 125 parcelas"},
    {"Cual es el teléfono de la agencia de viajes Unión del Valle Viajes":"El teléfono de la agencia de viajes UNIÓN DEL VALLE VIAJES es 628-158516."},
    {"Cual es el email de la agencia de viajes Viaser":"El email de la agencia de viajes VIASER es info@viaserviajes.com."},
    {"Cual la Web de la agencia de viajes Viajar por Aragon": "La web de la agencia de viajes VIAJAR POR ARAGON es www.viajarporaragon.com."},
    {"Cual la direccion de la agencia de viajes Viajes Male": "La dirección de la agencia de viajes VIAJES MALE, S.L.L. es Avda. La Jota, 57, ZARAGOZA (50014)."},
    {"que agencias de Viajes hay en Barbastro":"En Barbastro hay las siguientes agencias de viaje \n\t- ENOARTE, ENOLOGIA Y TURISMO S.L.\n\t- TORNAMON VIAJES, S.L.\n\t- GUARA TOURS S.L.\n\t- EL CÍRCULO TRAVEL"}
]
QUESTIONS_ANSWERS_ACCOMODATION_LEN = [
 {"Listado de hoteles de Tarazona":5},
 {"que restaurantes hay en Bulbuente": 30}
 ]


QUESTIONS_ANSWERS_FARMING_TEXT = [
 {"A que municipio pertenece la comarca agraria Calatayud":"La comarca agraría Calatayud pertenece al municipio de CALATAYUD" },
 {"Cuales son las villas y tierras del municipio SOBRARBE": "Las villas y tierras del municipio SOBRARBE son\n\t- MANC. FORESTAL DE LINAS DE BROTO, BROTO Y FRAGEN\n\t- MANC. FORESTAL VALLE DE BROTO\n\t- MANC. FORESTAL BUESA-BROTO\n\t- MANC. VALLE DE VIO Y SOLANA\n\t- MANC. FORESTAL SIN, SEÑES Y SERVETO"},
 {"informacion sobre la villa de Fago":"Los datos de la villa MANC. FORESTAL ANSO FAGO son:\n\t- localización: LA JACETANIA\n\t- teléfono: 974 370 003\n\t- email: mfansofago@aragob.es\n\t- cif: P 2200008 G" },
 {"A que municipio pertenece la villa SEÑES":"La villa SEÑES pertenece al municipio de  SOBRARBE"},
 {"A que municipio pertenece la villa de SEÑES Y SERVETO ":"La villa SEÑES Y SERVETO pertenece al municipio de  SOBRARBE."},
 {"Hectáreas de olivares en Aragon en 1989":"En Aragón se cultivaron 40648 hectáreas de olivares en el año 1989"},
 {"Hectáreas de olivares en la comarca de Jacetania en 1989":"En la comarca de Jacetania se cultivaron 0 hectáreas de olivares en el año 1989"},
 {"Hectáreas de olivares en el municipio de Zaragoza en 1989.":"En el municipio de Zaragoza se cultivaron 62 hectáreas de olivares en el año 1989"},
 {"Hectáreas de olivares en la provincia de Teruel en 1989.":"En la provincia de Teruel se cultivaron 20900 hectáreas de olivares en el año 1989"},
 {"Hectáreas de viñedos en Aragon en 1989":"En Aragón se cultivaron 53853 hectáreas de viñedos en el año 1989"},
 {"Hectáreas de viñedos en la comarca de Jacetania en 1989":"En la comarca de Jacetania se cultivaron 15 hectáreas de viñedos en el año 1989"},
 {"Hectáreas de viñedos en el municipio de Zaragoza en 1989.":"En el municipio de Zaragoza se cultivaron 71 hectáreas de viñedos en el año 1989"},
 { "Hectáreas de viñedos en la provincia de Teruel en 1989.":"En la provincia de Teruel se cultivaron 5396 hectáreas de viñedos en el año 1989"},
 {"Hectáreas de frutales en Aragon en 1989": "En Aragón se cultivaron 107059 hectáreas de frutales en el año 1989"},
 {"Hectáreas de regadío en el municipio de Zaragoza en 1989.":"En el municipio de Zaragoza se cultivaron 12529.0 hectáreas de regadio en el año 1989"},
 {"Hectáreas de secano en la provincia de Teruel en 1989.":"En la provincia de Teruel se cultivaron 378553.0 hectáreas de secano en el año 1989"},
 {"Hectáreas de agricultura ecológica en Aragon en 2013":"En Aragón se cultivaron 56907.7 hectáreas en el año 2013"},
 {"Hectáreas de agricultura ecológica en la provincia Teruel en 2013":"En la provincia de Teruel se cultivaron 11031.6 hectáreas en el año 2013"},
 {"Hectáreas de agricultura ecológica en la comarca Jacetania en 2013":"En la comarca de Jacetania se cultivaron 812.56 hectáreas en el año 2013"} ,
 {"Hectáreas de agricultura ecológica en Zaragoza en 2013":"En el municipio de Zaragoza se cultivaron 1447.17 hectáreas en el año 2013"},
 {"¿Cuál es el CIF del ayuntamiento La Almunia de Doña Godina?" : "El CIF del ayuntamiento de Almunia de Doña Godina, la es P-5002500-F."},
 {"¿Cuál es el CIF del ayuntamiento de La Almunia de Doña Godina?":"El CIF del ayuntamiento de Almunia de Doña Godina, la es P-5002500-F."},
 {"¿A qué comarca pertenece Jaca?":"Jaca se encuentra en la comarca la Jacetania."},
 {"¿Cuál es la población de La Almunia de Doña Godina en el año 2000?":"La población en el municipio de La Almunia De Doña Godina en 2000 es de 5591 habitantes."},
 {"¿Cuál es la población de La Joyosa el año 2018?":"La población en el municipio de La Joyosa en 2018 es de 1072 habitantes."},
 {"Cuál es la dirección del ayuntamiento Joyosa?": "El ayuntamiento de Joyosa, la está en Pza. España, 4."},
 {"¿Cuál es el email del ayuntamiento de La Almunia de Doña godina?": "El email del ayuntamiento de Almunia de Doña Godina, la es info@laalmunia.es."},
 {"¿Quién es el alcalde de La Almunia de Doña Godina y quiera compuesto?": "Almunia de Doña Godina, la esta presidida por Marta Blanca Gracia Blanco"},
 {"¿Cuántas hectáreas de viñedos hay en Zaragoza?": "En el municipio de Zaragoza se cultivaron 97 hectáreas de viñedos en el año "},
]

QUESTIONS_ANSWERS_CALENDAR_TRANSPORT_TEXT = [  
    {"¿Dónde se celebra el Nupzial?":"Nupzial tiene lugar en ZARAGOZA el 06-11-2020"},
    {"Donde se encuentra la obra de pintura ABRAZO EN LA PUERTA DORADA" : "La obra Abrazo en la puerta dorada la puedes encontrar en CDAN Centro de Arte y Naturaleza Fundacion Beulas"},
    {"¿A qué velocidad se puede ir por la carretera A-2?":"La velocidad máxima de la carretera A-2 es 120 kilómetros por hora."},
    {"¿Cuál es la descripción de la carretera A-220?":"La descripción de la carretera A-220 es La Almunia de Doña Godina por Cariñena a Belchite."},
    {"¿Qué puentes hay en la localidad de Huesca?":"Los puentes que hay en la localidad de Huesca son:\n\t- A-131 km 98.300"},
    {"¿En qué localidades se encuentran los puentes de la carretera A-2101?":"Los puentes de la carretera A-2101 están en las siguientes localidades:\n\t- BOTORRITA"},
    {"¿Que longitud tiene la carretera A-220?":"La carretera A-220 tiene 67.509 kilómetros de longitud."}
    
]

QUESTIONS_START_WORD = [ 
    {"¿Qué empresas de turismo activo hay en Zaragoza?" :{ "En Zaragoza hay las siguiente lista de empresas activas" : 11} },
    {"¿Qué rutas salen de Huesca?" :{ "Las rutas que salen de Huesca son:" : 12} },
    {"¿Qué rutas llegan a Huesca?" :{ "Las rutas que llegan a Huesca son" : 12} },
    {"¿Qué autobuses van a Benasque?": {"Los autobuses que se pasan por Benasque son:": 12}},
    {"Qué horarios tiene el autobús que va desde Zaragoza a Caspe?":{"Los horarios de los autobuses que van de Zaragoza a Caspe son:":12}},
    {"Estoy en Zaragoza y quiero ir a Huesca. ¿Qué autobuses van?" :{"Los horarios de los autobuses que van de Zaragoza a Huesca son:":20}},
    {"¿Qué carreteras hay en la provincia Huesca?" :{"Las carreteras de la provincia de Huesca son:": 12 } },
    {"¿Qué tipo de zonas hay cercanas a la carretera A-220?": {"Los zonas cercanas a la carretera A-220 son:":12 }},
    {"Dime todas los tipos de incidencias activas en Aragon": {"Los tipos de incidencias de tráfico en Aragon son:":12}},
    {"¿Cuáles son las comarcas agrarias del municipio Ribagorza?" :{"En Ribagorza hay las siguientes comarcas agrarías": 12}},
    {"¿Cuáles son las villas y tierras de Zaragoza?" : {"Las villas y tierras del municipio Zaragoza son":12}},
    {"¿Qué fincas son de regadío en el municipio Huesca?":{"Las fincas de regadio son":12}},
    {"Las carreteras de la provincia de Huesca son:":{"Las carreteras de la provincia de Huesca son:":21}},
    {"¿Qué empresas de turismo activo hay en Zaragoza?":{"En Zaragoza hay las siguiente lista de empresas activas":12}},

]
QUESTIONS_SEVERALS_START_ANSWER = [
    {"¿Existe alguna incidencia de tráfico en la localidad Fraga?" :["Las incidencias de tráfico en Fraga son:", "No he encontrado incidencias de tráfico en Fraga."] },
    {"¿Qué tipo de incidencias de tráfico hay en la localidad Fraga?":["Los tipos de incidencias de tráfico en Fraga son:","No he encontrado incidencias de tráfico en Fraga."]},
    {"Dime todas los tipos de incidencias activas en la localidad Fraga" : [ "Los tipos de incidencias de tráfico en Fraga son:", "No he encontrado incidencias de tráfico en Fraga."]},
    {"¿En qué tramos se encuentran las incidencias de tráfico de la localidad Fraga?": ["Las incidencias de tráfico de la localidad de Fraga se encuentran en :","No he encontrado incidencias de tráfico en Fraga."]}
]

QUESTIONS = [
    "donde puedo comer en zuera?",
    "dónde puedo comer en Zuera?",
    "donde me puedo tomar un café en Zuera?",
    "dónde me puedo tomar un café en Zuera? ",
    "Cual es la dirección del restaurante Agora? ",
    "en donde está el restaurante El Torreon? ",
    "donde está el restaurante El Torreon?",
    "dime la dirección del restaurante El Torreon",
    "Cual es la dirección del restaurante Las Galias? ",
    "Cual es la dirección del restaurante El Fuelle ",
    "cual es el email del restaurante El Torreon? ",
    "cual es el correo electrónico del restaurante La Manon? ",
    "cual es el correo electrónico del restaurante LA MANON? ",
    "cual es el correo electrónico del restaurante KIKO? ",
    "cual es el email del restaurante KIKO? ",
    "Cual es el fax del restaurante La Manon",
    "Dime el fax del restaurante La Manon",
    "Cuál es el fax de El Fuelle?",
    "cual es el teléfono de la opera?",
    "cuál es el teléfono del restaurante La Opera?",
    "cual es el teléfono del restaurante la opera?",
    "cual es el teléfono de LA OPERA en zuera?",
    "cual es el teléfono del restaurante LA OPERA? ",
    "cual es el teléfono de cafeteria AISA?  ",
    "cual es el teléfono de El Fuelle? ",
    "cual es el teléfono de El fuelle? ",
    "cual es el teléfono de cafeteria Las Vegas de Zaragoza? ",
    "sabes cual es la página web de El Molino?",
    "cual es la página web de El Molino?",
    "El restaurante El Molino, tiene web?",
    "cual es la página web del restaurente El Torreon?",
    "Cual es el website del Torreon?",
    "sabes cual es la página web de Las Vegas? ",
    "cuantos restaurantes hay en zaragoza? ",
    "cuantas cafeterias hay en Zuera? ",
    "Como puedo reservar en el restaurante El torreon? ",
    "Como puedo reservar en el restaurante El Torreon? ",
    "Quiero reservar en El Torreon ",
    "Cual es la capacidad de la cafetería AISA? ",
    "Cuantas personas caben en la cafetería AISA?",
    "cual es la capacidad del restaurante OLIMPIA? ",
    "donde está la cafetería OLIMPIA? ",
    "donde está el restaurante LA CUCHARA?",
    "dónde está el restaurante LA CUCHARA? ",
    "Dime los hoteles de Huesca? ",
    "que hoteles hay en Zaragoza? ",
    "¿Cuál es la página web del hotel Palafox? ",
    "Cual es el website del hotel palafox? ",
    "Cual es la dirección del Hotel Palafox? ",
    "Cual es la dirección del hotel Palafox? ",
    "Cual es el teléfono del Hotel Palafox? ",
    "Cual es el teléfono del hotel Palafox? ",
    "Cómo puedo reservar en el hotel Palafox? ",
    "¿Qué categoría tiene el hotel Palafox?  ",
    "¿Qué hoteles con categoría 3 estrellas o superior hay en Zaragoza? ",
    "¿Tiene el hotel Palafox habitaciones con terraza? ",
    "¿Tiene el hotel Palafox habitaciones triples? ",
    "¿Tiene el hotel Palafox habitaciones cuadruples? ",
    "qué otros servicios ofrece el hotel Palafox? ",
    "que servicios ofrece el hotel Palafox? ",
    "Cuantos hoteles hay en Zaragoza? ",
    "¿Cuántas habitaciones tiene el hotel Palafox?  ",
    "¿Cuántas habitaciones tiene el hotel Palafox con baño? ",
    "¿Cuántas habitaciones dobles tiene el hotel Palafox?  ",
    "¿Cuántas habitaciones suits tiene el hotel Palafox?  ",
    "¿Cuántas suits tiene el hotel Palafox?    ",
    "Cuántas camas tiene el hotel Palafox? ",
    "En qué ciudad está el hotel Palafox? ",
    "Dónde puedo alojarme en Zaragoza? ",
    "Cual es la temporada baja del hotel Palafox?",
    "Cual es la temporada alta del hotel Palafox?",
    "Dime las casas rurales de Benasque ",
    "que casas rurales hay en Benasque ",
    "que casas rurales hay en la provincia de Huesca ",
    "Cual es el telefono de la casa rural MONTE PERDIDO ",
    "Cual es el telefono de la casa rural Monte Perdido ",
    "Cual es el email de la casa rural CASA ARBOLEDALAFUENTE ",
    "Cual es el fax de la casa rural CASA ARBOLEDALAFUENTE ",
    "Cual es el fax de la casa rural Arboledalafuente ",
    "Cual es el fax de la casa rural ArboledaLafuente? ",
    "¿Cuál es la página web de la casa rural Casa ArboledaLafuente? ",
    "dime la web de la casa rural ArboledaLafuente ",
    "dime la web de la casa rural Casa ArboledaLafuente ",
    "Cual es la direccion de la casa rural CASA RURAL MONTE PERDIDO? ",
    "Cual es la direccion de la casa rural Monte Perdido? ",
    "Cuál es la dirección de contacto de la casa rural Monte Perdido? ",
    "Cómo puedo reservar en la casa rural Monte Perdido? ",
    "Cuántas las casas rurales hay en el municipio de Zaragoza? ",
    "¿Cuántos apartamentos tiene la casa rural Monte Perdido?  ",
    "¿Cuántos apartamentos tiene la casa rural Morillo? ",
    "Cuántas habitaciones tiene la casa rural Monte Perdido con baño? ",
    "¿Cuántas habitaciones sencillas tiene la casa rural Monte Perdido?  ",
    "¿Cuántas habitaciones dobles tiene la casa rural Monte Perdido? ",
    "Numero de plazas de la casa rural Monte Perdido ",
    "Cuántas plazas totales tiene la casa rural Monte Perdido ",
    "En qué ciudad se encuentra la casa rural Monte Perdido? ",
    "En qué municipio se encuentra la casa rural Monte Perdido? ",
    "¿Cuándo es temporada baja en la casa rural Monte Perdido? ",
    "Dónde puedo alojarme en Benasque? ",
    "Dime los apartamentos de Benasque ",
    "Dime los apartamentos de Zaragoza ",
    "qué apartamentos hay en Zaragoza? ",
    "Cual es el telefono de los apartamentos FORATATA ",
    "dime el telefono de los apartamentos FORATATA ",
    "cual es el email de los apartamentos FORATATA? ",
    "cual es el email de los apartamento BALCÓN DEL PIRINEO RURAL ORDESA ",
    "Cuál es la página web del apartamentos FORATATA? ",
    "Cuál es la página web del apartamentos BALCÓN DEL PIRINEO RURAL ORDESA ",
    "Cuál es la página web del apartamentos Panticosa ",
    "Cuál es la página web del apartamentos Foratata? ",
    "Cual es la direccion de los apartamentos Panticosa? ",
    "Cual es la direccion de los apartamentos Foratata? ",
    "Cómo puedo reservar en los apartamentos Panticosa? ",
    "Cuántos apartamentos hay en el municipio de Zaragoza? ",
    "Cuántos apartamentos hay en Zaragoza? ",
    "Cuántos apartamentos hay en la provincia de Zaragoza? ",
    "Cuál es la categoría del apartamentos Panticosa ",
    "Cuantas plazas tiene los apartamentos Panticosa? ",
    "Dime los campings de Zaragoza ",
    "que campings hay en Zaragoza? ",
    "que campings hay en la provincia de Zaragoza? ",
    "Cual es el telefono del camping Pineta? ",
    "Cual es el fax del camping Pineta? ",
    "Cual es el fax del camping Los Baños?",
    "Cual es el email del camping Pineta? ",
    "Cual es el email del camping Los Baños? ",
    "Cual es la página web del camping Pineta? ",
    "Cual es la web del camping Pineta? ",
    "Cual es la web del camping Los Baños? ",
    "Cómo puedo reserver en el camping Pineta? ",
    "Cómo puedo reservar en el camping Pineta? ",
    "Cómo puedo reservar en el camping Los Baños? ",
    "Cómo puedo reservar en Los Baños? ",
    "Cual es la dirección del camping Pineta? ",
    "Cuantos campings hay en Zaragoza? ",
    "Cuántos bungalows tiene el camping los Baños? ",
    "Cuantas plazas para caravanas tiene el camping Los Baños? ",
    "Cuántas parcelas tiene el camping Los Baños? ",
    "Cuándo es temporada baja en el camping Los Baños? ",
    "Cuándo es temporada media en el camping Los Baños? ",
    "Cuándo es temporada alta en el camping Los Baños? ",
    "En qué ciudad se encuentra el camping Los Baños? ",
    "dime los albergues de Zaragoza? ",
    "dime los albergues de Huesca?  ",
    "dime los albergues de la provincia de Huesca? ",
    "dime los albergues del municipio de Zaragoza?",
    "Cual es el telefono del albergue FUNDACION ASISTENCIAL ATADES HUESCA? ",
    "Cual es el telefono del albergue Atades Huesca? ",
    "Cual es el fax del albergue Atades Huesca? ",
    "Cual es el email del albergue Atades Huesca? ",
    "Cual es la página web del albergue Atades Huesca? ",
    "Cual es la dirección del albergue Atades Huesca? ",
    "Cuál es la dirección de contacto del albergue atades Huesca? ",
    "Como puedo reservar en Atades Huesca? ",
    "Como puedo reservar en el albergue Atades Huesca? ",
    "Cuantos albergues hay en Zaragoza? ",
    "Cuantos albergues hay en Huesca? ",
    "Cuántas plazas tiene el albergue Atades Huesca? ",
    "Dime las agencias de viaje de Zaragoza ",
    "Dime las agencias de viaje de Huesca ",
    "Dime las agencias de viaje de la provincia de Zaragoza ",
    "Cual es el telefono de la agencia de viajes ALMOZARA VIAJES? ",
    "Cual es el telefono de la agencia de viajes Almozara Viajes? ",
    "Cual es el telefono de la agencia de viajes Almozara? ",
    "Cual es el email de la agencia de viajes Almozara? ",
    "Cual es el correo electrónico de la agencia de viajes Almozara? ",
    "Cual es la web de la agencia de viajes Almozara? ",
    "Cual es la pagina web de la agencia de viajes Almozara? ",
    "Cual es la dirección de la agencia de viajes Almoraza? ",
    "Cuales son los museos de Zuera ",
    "dime los museos del municipio de Zaragoza ",
    "que obras tiene el museo de Zaragoza? ",
    "Dime las obras  ",
    "Donde se encuentra la obra Abrazo en la puerta dorada ",
    "Dónde se encuentra la obra Abrazo en la puerta dorada ",
    "Dónde se encuentra la obra 'Abrazo en la puerta dorada' ",
    "Qué rutas salen de Zaragoza? ",
    "Qué senderos/rutas puedo hacer en Benasque ",
    "Qué senderos puedo hacer en Benasque ",
    "Qué rutas puedo hacer en Benasque ",
    "Qué rutas salen en Benasque y terminan en Eriste? ",
    "Qué rutas salen desde Benasque? ",
    "Qué rutasllegan a Benasque? ",
    "dime los guías turisticos de Zaragoza ",
    "Dime los guias turisticos de Huesca ",
    "Dime el teléfono de Sanz Vitalla Pedro ",
    "Cual es el teléfono del guía turistico Sanz Vitalla Pedro? ",
    "Cómo me pongo en contacto con el guía tursitico Sanz Vitalla Pedro",
    "Cómo me pongo en contacto con Sanz Vitalla Pedro",
    "Cómo me pongo en contacto con Pedro Sanz Vitalla? ",
    "Cual es el teléfono del guía turistico Pedro Sanz Vitalla ? ",
    "Cómo me pongo en contacto con Pedro Sanz ? ",
    "dime las oficinas de turismo de Huesca ",
    "Cuales son las oficinas de turismo de Huesca? ",
    "Cual es el teléfono de la oficina de turismo de Huesca? ",
    "Cual es el teléfono de la oficina de turismo de Zaragoza? ",
    "¿Cuáles son las comarcas agrarias de Zaragoza? ",
    "¿Cuáles son las comarcas agrarias de la provincia de Zaragoza? ",
    "¿Cuáles son las comarcas agrarias del municipio de Zaragoza? ",
    "¿Cuáles son las villas y tierras de Zaragoza? ",
    "¿Cuáles son las villas y tierras del municipio de Zaragoza?",
    "¿Cuáles son las villas y tierras de Huesca? ",
    "¿Qué fincas tienen cultivo leñoso en Zaragoza? ",
    "¿Qué fincas tienen cultivo leñoso en Zuera? ",
    "¿Qué fincas tienen cultivo leñoso en Huesca? ",
    "que fincas de cultivo leñoso de secano en el Valdejalon? ",
    "Cuántas hectáreas agricultura ecológica hay Aragón? ",
    "Cuántas hectáreas agricultura ecológica hay en la provincia de Huesca? ",
    "Cuantas hectareas de agricultura ecologica en Aragon en 2013? ",
    "Cuantas hectareas de agricultura ecologica hay en Aragon en 2013? ",
    "Cuantas hectareas de agricultura ecologica en Aragón en 2013? ",
    "Cuantas hectareas de olivares en Aragon en 1989 ",
    "Cuantas hectareas de olivares se cultivaron en Aragon ? ",
    "Cuantas hectareas de olivares se cultivaron en Aragón en 2001? ",
    "Cuantas hectareas de olivares se cultivaron en la provincia de Teruel ? ",
    "Cuantas hectareas de olivares se cultivaron en la provincia de Teruel en 1989? ",
    "Qué usos se le da al suelo en el municipio de Teruel?",
    "Qué usos se le da al suelo en la provincia de Huesca?",
    "A que comarca pertenece el municipio de Calatayud?",
    "A que comarca pertenece Calatayud?",
    "Cuantas hectareas de suelo rustico hay en la provincia de Teruel?",
    "¿Cuántos edificios de más de 15 años hay en Zaragoza?",
    "Cuantos edificios de mas de 50 años hay en la provincia de Teruel?",
    "Cual es la poblacion en la provincia de Teruel en 2005?",
    "Cual es la poblacion en la comarca de Jacetania en 2005?",
    "Cual es la poblacion en el municipio de Zaragoza en 2005?",
    "Cuantas mujeres viven en Zaragoza provenientes de Africa en 2005?",
    "Cuantas personas viven en la provincia de Teruel provenientes de America en el año 2005?",
    "Cuál es la dirección del ayuntamiento de Zaragoza?",
    "Cuál es el CIF del ayuntamiento de Zaragoza?",
    "Cuál es el teléfono del ayuntamiento de Zaragoza?",
    "Cuál es el fax del ayuntamiento de Zaragoza?",
    "Cuál es el fax del ayuntamiento de Calatayud?",
    "Cuál es el email del ayuntamiento de Zaragoza?",
    "Cuál es el correo electrónico del ayuntamiento de Zaragoza?",
    "Quién es el alcalde de Zaragoza?",
    "Quién es el alcalde de Benasque?",
    "Quiénes son los concejales de Zaragoza?",
    "Quiénes son los concejales de Huesca?",
    "Cuántos contenedores de vidrio hay en Zaragoza?",
    "Cuántos contenedores de vidrio hay en Huesca?",
    "Cuantas hectareas de superficies artificiales hay en Aragon?",
    "Cuantas hectareas de superficies artificiales hay en Aragón?",
    "Cuántos incendios hubo en Zaragoza en el año 1999?",
    "cuantos incendios hubo en aragon en 2012?",
    "cuantos incendios hubo en Zaragoza en 2012?",
    "cuantos incendios hubo en Zaragoza en 2018?",
    "cuantas hectareas se quemaron en aragon en 2012",
    "cuantas hectareas se quemaron en Aragón en 2012",
    "cuantas hectareas se quemaron en la provincia de Zaragoza en 2012",
    "cuantas depuradoras hay aragon en 2012",
    "Qué empresas del sector servicios hay en Teruel",
    "Qué empresas del sector servicios hay en la provincia de Teruel",
    "Qué empresas del sector servicios hay en la provincia de Zaragoza",
    "Qué empresas del sector industrial hay en la provincia de Zaragoza",
    "Cuantas empresas dedicadas a la hosteleria en la provincia de Teruel?",
    "Cuantos hombres autonomos hay dados de alta en el marzo del 2012 en Aragon?",
    "Cuantos hombres autonomos hay dados de alta en el Enero del 2012 en Zaragoza?",
    "Cuantos mujeres autonomas hay dados de alta en el Enero del 2012 en Zaragoza?",
    "Cuantas empresas entre 1-9 trabajadores en marzo de 2012 en Teruel?",
    "Cuantos hombres autonomos hay dados de alta en el marzo del 2012 en Aragon?",
    "Cuantos hombres parados hay en el sector servicios en 2012 en Aragon?",
    "Cuantos hombres parados hay en el sector servicios en 2012 en la provincia de Zaragoza?",
    "Cuantas mujeres paradas hay en el sector servicios en 2012 en la provincia de Zaragoza?",
    "Cuántos hombres fueron contratados en marzo en 2012 en Aragon?",
    "Cuantos hombres fueron contratados en marzo en 2012 en la provincia de Zaragoza?",
    "Cuantos hombres contratados en marzo en 2012 en Aragon?",
    "Cuantos hombres contratados en marzo en 2012 en la provincia de Huesca?",
    "Cuantos accidentes laborales hubo en 2012 en Aragon?",
    "Cual es la renta per capita en 2012 en Aragon?",
    "Cual es la renta per capita en 2012 en el municipio de Zaragoza?",
]

def test_questions(question_text:list,question_len:list,question_start_word:list,question_severals:list,results:list)-> None:
    """
    Test of chat room: connectivity, agent status and input processing
    
    response = requests.get(CHAT_ROOM_URL)
    if response.status_code == 200:
        #print_passed("Chat room is running")
        print("Chat room is running")
    else:
        #print_failed("Error in administrator Flask server")
        print("Error in administrator Flask server")
        exit(-1)
    """
    
    response_status = 0
    count = 0
    print(f"try connect to chatbot port {CHAT_ROOM_URL}")
    while count< 60*5:
        try :
            count += 1
            response_status = requests.get(CHAT_ROOM_URL + "/status")
            if response_status.status_code != 500:
                break
            else:
                time.sleep(1)

        except ConnectionError:
            time.sleep(1)
            print(".")
        except NewConnectionError:
            time.sleep(1)
    
    response = requests.get(CHAT_ROOM_URL)
    if response.status_code == 200:
        #print_passed("Chat room agent is running")
        print("Chat room agent is running")
    else:
        #print_failed("Error chat room agent, agent not ready")
        print("Error chat room agent, agent not ready")
        exit(-1)

    cookies_dict = response.cookies.get_dict()
    #all_questions = [f"pregunta ','esperado','respondido','correcto'\n"]
    all_questions =[]
    fails=0
    passed = 0

    if cookies_dict:

        for element in question_text:
            question = list(dict(element).keys())[0]
            answer =  element.get(question)
            response = requests.post(
                CHAT_ROOM_URL + "/chat",
                cookies=cookies_dict,
                json={"text": question, "timeout": False},
            )

            if response.status_code == 200:
                json_response = response.json()
                if len(json_response["answer"]) > 0 and   answer.lower() in  ("".join( json_response["answer"]).lower() ):
#                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{True} \n")
                    passed=passed+1
                else:
                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{False} \n")
                    fails=fails+1
                    #questions_fails.append({"pregunta":question , "esperado":answer , "respondido":" ".join(json_response["answer"]) })
            results.append([" ".join( json_response["answer"]),answer,fails])

        csv = ' '.join(all_questions)
        if fails == 0:
            #print_passed("Question OK")
            print("Question OK")

        else:
            #print_failed(f"Question all  , fails: {fails} of  {passed + fails}:\n {csv}")
            print(f"Question all  , fails: {fails} of  {passed + fails}:\n {csv}")

        fails=0
        passed = 0
        all_questions=[]
        
        for element in question_len:
            question = list(dict(element).keys())[0]
            answer =  element.get(question)
            response = requests.post(
                CHAT_ROOM_URL + "/chat",
                cookies=cookies_dict,
                json={"text": question, "timeout": False},
            )

            if response.status_code == 200:
                json_response = response.json()
                if len(json_response["answer"]) > 0 and len("".join(json_response["answer"])) >=  answer:
#                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{True}")
                    passed=passed+1                    
                else:
                    fails=fails+1
                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{False}")
                    #questions_fails.append({"pregunta":question , "esperado":answer , "respondido":" ".join(json_response["answer"]) })
                results.append([json_response["answer"], json_response["answer"], fails])
        
        # we have a list as answer ckeck start and a lot of text 
        for element in question_start_word:
            question = list(dict(element).keys())[0]
            tmp =  element.get(question)
            
            answer =  list(dict(tmp).keys())[0]
            #print (answer )
            words =  tmp.get(answer)
            #print (words)
            response = requests.post(
                CHAT_ROOM_URL + "/chat",
                cookies=cookies_dict,
                json={"text": question, "timeout": False},
            )

            if response.status_code == 200:
                json_response = response.json()
                if len(json_response["answer"]) > 0 and  "".join(json_response["answer"]).startswith(answer) and   len("".join(json_response["answer"]).split()) >=  words :
#                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{True}")
                    passed=passed+1                    
                else:
                    fails=fails+1
                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{False}")
                    #questions_fails.append({"pregunta":question , "esperado":answer , "respondido":" ".join(json_response["answer"]) })
                results.append([json_response["answer"], json_response["answer"], fails])
    
        # we have severals answer ( data or no data in database) ckeck if answer in almost one expected answer
        for element in question_severals:
            question = list(dict(element).keys())[0]
            answer =  element.get(question)

            response = requests.post(
                CHAT_ROOM_URL + "/chat",
                cookies=cookies_dict,
                json={"text": question, "timeout": False},
            )

            if response.status_code == 200:
                json_response = response.json()

                if len(json_response["answer"]) > 0 and  "".join(json_response["answer"]).startswith(tuple(answer)):
#                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{True}")
                    passed=passed+1                    
                else:
                    fails=fails+1
                    all_questions.append(f" '{question}' , '{answer}' ,'{''.join(json_response['answer'])}' ,{False}")
                    #questions_fails.append({"pregunta":question , "esperado":answer , "respondido":" ".join(json_response["answer"]) })
                results.append([json_response["answer"], json_response["answer"], fails])                

        if fails == 0:
            #print_passed("Question OK")
            print("Question OK")

        else:
            csv = ' '.join(all_questions)
            #print_failed(f"Question all , fails: {fails} of  {len(all_questions)}:\n {csv}")
            print(f"Question all , fails: {fails} of  {len(all_questions)}:\n {csv}")


    return results

if __name__ == "__main__":
    results = []
    results = test_questions([],[],QUESTIONS_START_WORD,QUESTIONS_SEVERALS_START_ANSWER, results)

    results = test_questions(QUESTIONS_ANSWERS_ARAGON_TEXT,QUESTIONS_ANSWERS_ARAGON_LEN,[],[],results)
    results = test_questions(QUESTIONS_ANSWERS_ACCOMODATION_TEXT, QUESTIONS_ANSWERS_ACCOMODATION_LEN,[],[], results)
    results = test_questions(QUESTIONS_ANSWERS_ACTIVITIES_TEXT,QUESTIONS_ANSWERS_ACTIVITIES_LEN,[],[], results)
    results = test_questions(QUESTIONS_ANSWERS_FARMING_TEXT,[],[],[], results)
    results = test_questions(QUESTIONS_ANSWERS_CALENDAR_TRANSPORT_TEXT,[],[],[], results)
    if len(results) > 0 : 
        exit(-1)
    #print(str(results))
