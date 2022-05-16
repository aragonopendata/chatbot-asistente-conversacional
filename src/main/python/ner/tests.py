import requests
import json

url = 'http://127.0.0.1:4999/ner'

person_array = [
    "Quien es el alcalde de Añon",
    "Dime el teléfono de Sanz Vitalla Pedro ",
    "Cual es el teléfono del guía turistico Sanz Vitalla Pedro? ",
    # "Cómo me pongo en contacto con el guía tursitico Sanz Vitalla Pedro",
    # "Cómo me pongo en contacto con Sanz Vitalla Pedro",
    "Cómo me pongo en contacto con Pedro Sanz Vitalla? ",
    # "Cual es el teléfono del guía turistico Pedro Sanz Vitalla ? ",
    "Cómo me pongo en contacto con Pedro Sanz ? ",
    "Quién es el alcalde de Zaragoza?",
    "Quién es el alcalde de Benasque?",
    # "Quiénes son los concejales de Zaragoza?",
    # "Quiénes son los concejales de Huesca?",
    "Quien es el alcalde de Almunia de Doña Godina"
]

location_array = ["En que comarca esta Zuera"  "cual es el email del restaurante El Torreon? ",
                  "cual es el correo electrónico del restaurante La Manon? ",
                  "cual es el correo electrónico del restaurante LA MANON? ",
                  "cual es el correo electrónico del restaurante KIKO? ",
                  "cual es el email del restaurante KIKO? ",
                  "Cual es el fax del restaurante La Manon",
                  "Dime el fax del restaurante La Manon",
                  "Cuál es el fax de El Fuelle?",
                  # "cual es el teléfono de la opera?",
                  "cuál es el teléfono del restaurante La Opera?",
                  # "cual es el teléfono del restaurante la opera?",
                  "cual es el teléfono de LA OPERA en zuera?",
                  "cual es el teléfono del restaurante LA OPERA? ",
                  "cual es el teléfono de cafeteria AISA?  ",
                  "cual es el teléfono de El Fuelle? ",
                  # "cual es el teléfono de El fuelle? ",
                  "cual es el teléfono de cafeteria Las Vegas de Zaragoza? ",
                  "sabes cual es la página web de El Molino?",
                  "cual es la página web de El Molino?",
                  "El restaurante El Molino tiene web?",
                  "cual es la página web del restaurente El Torreon?",
                  # "Cual es el website del Torreon?",
                  "sabes cual es la página web de Las Vegas? ",
                  "cuantos restaurantes hay en zaragoza? ",
                  "cuantas cafeterias hay en Zuera? ",
                  # "Como puedo reservar en el restaurante El torreon? ",
                  "Como puedo reservar en el restaurante El Torreon? ",
                  "Quiero reservar en El Torreon ",
                  "Cual es la capacidad de la cafetería AISA? ",
                  "Cuantas personas caben en la cafetería AISA?",
                  "cual es la capacidad del restaurante OLIMPIA? ",
                  "donde está la cafetería OLIMPIA? ",
                  "donde está el restaurante LA CUCHARA?",
                  "en donde está el restaurante El Torreon? ",
                  "donde está el restaurante El Torreon?",
                  "dime la dirección del restaurante El Torreon",
                  "Cual es la dirección del restaurante Las Galias? ",
                  "Cual es la dirección del restaurante El Fuelle ",
                  "Cual es la dirección del restaurante Agora? ",
                  "Dime los hoteles de Huesca? ",
                  "que hoteles hay en Zaragoza? ",
                  "¿Cuál es la página web del hotel Palafox? ",
                  # "Cual es el website del hotel palafox? ",
                  # "Cual es la dirección del Hotel Palafox? ",
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
                  # "Cual es el fax del camping Los Baños?",
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
                  "Qué rutas salen de Zaragoza? ",
                  "Qué senderos/rutas puedo hacer en Benasque ",
                  "Qué senderos puedo hacer en Benasque ",
                  "Qué rutas puedo hacer en Benasque ",
                  "Qué rutas salen en Benasque y terminan en Eriste? ",
                  "Qué rutas salen desde Benasque? ",
                  "Qué rutas llegan a Benasque? ",
                  "dime los guías turisticos de Zaragoza ",
                  "Dime los guias turisticos de Huesca ",
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
                  # "que fincas de cultivo leñoso de secano en el Valdejalon? ",
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
                  "Cuántos contenedores de vidrio hay en Zaragoza?",
                  "Cuántos contenedores de vidrio hay en Huesca?",
                  "Cuantas hectareas de superficies artificiales hay en Aragon?",
                  "Cuantas hectareas de superficies artificiales hay en Aragón?",
                  "Cuántos incendios hubo en Zaragoza en el año 1999?",
                  # "cuantos incendios hubo en aragon en 2012?",
                  "cuantos incendios hubo en Zaragoza en 2012?",
                  "cuantos incendios hubo en Zaragoza en 2018?",
                  # "cuantas hectareas se quemaron en aragon en 2012",
                  "cuantas hectareas se quemaron en Aragón en 2012",
                  "cuantas hectareas se quemaron en la provincia de Zaragoza en 2012",
                  # "cuantas depuradoras hay aragon en 2012",
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
                  "A que municipio pertenece la villa SEÑES",
                  "A que municipio pertenece la villa Señes",
                  "Cual es la poblacion de La Almunia de Doña Godina",
                  "Cual es la poblacion de LA ALMUNIA DE DOÑA GODINA",
                  "Donde está el Ayuntamiento de Zaragoza"
]

organizacion_array = [
    "Cuál es la dirección del ayuntamiento de Zaragoza?",
    "Cuál es el CIF del ayuntamiento de Zaragoza?",
    "Cuál es el teléfono del ayuntamiento de Zaragoza?",
    "Cuál es el fax del ayuntamiento de Zaragoza?",
    "Cuál es el fax del ayuntamiento de Calatayud?",
    "Cuál es el email del ayuntamiento de Zaragoza?",
    "Cuál es el correo electrónico del ayuntamiento de Zaragoza?",
    "Cual es el C.I.F. del ayuntamiento de Almunia de Doña Godina.",
    "Cual es el C.I.F. del ayuntamiento de LA ALMUNIA DE DOÑA GODINA",
    "Cual es el C.I.F. del ayuntamiento de LA VILLA DE SEÑES"
]

types = ['person','location','organization']

print("PERSONS")

for person in person_array:

    question = person
    print(question)
    myobj = {'words': question}

    result = requests.post(url, json = myobj)
    entities = d = json.loads(result.text)
    try:
        if len(entities['entities']) == 1:
            diccionario = entities['entities'][0]['entity']
            if diccionario == types[0]:
                print(entities['entities'][0]['value'])
                if len(entities['entities'][0]['value'])<5:
                    print("Longitud demasiado pequeño")
                    print("error\n")
                else:
                    print("ok\n")
            else:
                print(str(types[0]))
                print(entities['entities'][0]['entity'])
                print(entities['entities'][0]['value'])
                print("error\n")
        else:
            index = 0
            for entity in entities['entities']:
                diccionario = entities['entities'][index]['entity']
                if diccionario == types[0]:
                    print(entities['entities'][index]['value'])
                    if len(entities['entities'][index]['value']) < 5:
                        print("Longitud demasiado pequeño")
                        print("error\n")
                    else:
                        print("ok\n")
                else:
                    print(str(types[0]))
                    print(entities['entities'][index]['entity'])
                    print(entities['entities'][index]['value'])
                    print("error\n")
                index = index + 1
    except:
        print(question)
        print("error\n")

print("LOCATIONS")

for location in location_array:

    question = location
    print(question)
    myobj = {'words': question}

    result = requests.post(url, json = myobj)
    entities = d = json.loads(result.text)
    try:
        if len(entities['entities']) == 1:
            diccionario = entities['entities'][0]['entity']
            if diccionario == types[1]:
                print(entities['entities'][0]['value'])
                if len(entities['entities'][0]['value'])<5:
                    print("Longitud demasiado pequeño")
                    print("error\n")
                else:
                    print("ok\n")
            else:
                print(str(types[1]))
                print(entities['entities'][0]['entity'])
                print(entities['entities'][0]['value'])
                print("error\n")
        else:
            try:
                index = 0
                for entity in entities['entities']:
                    diccionario = entities['entities'][index]['entity']
                    if diccionario == types[1]:
                        print(entities['entities'][index]['value'])
                        if len(entities['entities'][index]['value']) < 5:
                            print("Longitud demasiado pequeño")
                            print("error\n")
                        else:
                            print("ok\n")
                    else:
                        print(str(types[1]))
                        print(entities['entities'][index]['entity'])
                        print(entities['entities'][index]['value'])
                        print("error\n")
                    index = index + 1
            except:
                pass
    except:
        print(question)
        print("error\n")

print("ORGANIZATIONS")

for organization in organizacion_array:

    question = organization
    print(question)
    myobj = {'words': question}

    result = requests.post(url, json = myobj)
    entities = d = json.loads(result.text)
    try:
        if len(entities['entities']) == 1:
            diccionario = entities['entities'][0]['entity']
            if diccionario == types[2]:
                print(entities['entities'][0]['value'])
                if len(entities['entities'][0]['value'])<5:
                    print("Longitud demasiado pequeño")
                    print("error\n")
                else:
                    print("ok\n")
            else:
                print(str(types[2]))
                print(entities['entities'][0]['entity'])
                print(entities['entities'][0]['value'])
                print("error\n")
        else:
            index = 0
            for entity in entities['entities']:
                diccionario = entities['entities'][index]['entity']
                if diccionario == types[2]:
                    print(entities['entities'][index]['value'])
                    if len(entities['entities'][index]['value']) < 5:
                        print("Longitud demasiado pequeño")
                        print("error\n")
                    else:
                        print("ok\n")
                else:
                    print(str(types[2]))
                    print(entities['entities'][index]['entity'])
                    print(entities['entities'][index]['value'])
                    print("error\n")
                index = index + 1
    except:
        print(question)
        print("error\n")