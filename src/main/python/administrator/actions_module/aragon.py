'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
"""
Module of the action package to cover all the questions an user can
ask about territory or environment.

All the actions inherits from the interface 'Action' of Rasa, which
declares two mandatory methods for every action: a name and a run
method, in order to identify it in the action server and execute
whichever the task it has defined

Every action is auto documented with its name
"""

import re
from collections import defaultdict
from datetime import datetime
from pprint import pprint
from urllib.error import URLError

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from actions_module.Action_Generic import Action_Generic
import datetime

from actions_utils import (
    build_virtuoso_response,
    title,
    get_location_type,
    get_sector_type,
    get_person_type,
    get_land_type,
    get_duckling_entities,
    get_duckling_numbers,
    extract_value,
    get_surface_type,
    get_employ_sector_type,
    get_location_type_output,
    filter_response,
    clean_input,
    PLACE_TYPE,
    get_year,
)
#from browser import Browser

# Instance of the browser with an open connection with a Virtuoso
# database that will make queries to get an answer for the user
#browser = Browser()
from actions_module.utils import *


def find_location(entities):
    location = next((x for x in entities if x["entity"] == "location"), None)
    organization = next((x for x in entities if x["entity"] == "organization"), None)
    person = next((x for x in entities if x["entity"] == "person"), None)
    if location is None and organization is not None  and "entities" in organization:
            oentities=organization.get("entities", [])
            location = next((x for x in oentities if x["entity"] == "location"), None) #se deberia buscar recursivamente
    if location is None and person is not None and "entities" in person:
            pentities = person.get("entities", [])
            location = next((x for x in pentities if x["entity"] == "location"), None)  # se deberia buscar recursivamente


    if location is not None:
        return location.get("value",None)

    return None

class ActionLandUses(Action_Generic):
    def name(self):
        return "action_land_uses"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        message = tracker.latest_message["text"]
        year = getYear(message)

        if location is not None:
            try:
                # TODO: Is needed this verification?
                # TODO: If needed, surround with try catch, not if
                # if number != "":
                #     numberint = int(number)
                #     if 1900 < numberint < 2100:
                #         year = str(number)

                # TODO: Base class with this method, it is repeated
                # TODO: Add 'Aragón' to the function get_location_type
                # User can ask for region, province, municipality or Aragón
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                answer = browser.search(
                    {
                        "intents": ["usoSuelo", "tipoLocalizacion", "Year"],
                        "entities": [location, location_type, year],
                    }
                )

                if len(answer) > 0:
                    try:
                        year = extract_value(answer[0]["fecha"])
                    except:
                        year = getYear(message)
                    # TODO: Number 5 is hardcoded, should be declared in each action class or in base class
                    # If the answer is a list of a lot of elements, trim to 5
                    # and show a link to the full answer
                    list_uses = "{}"
                    if len(answer) > 5:
                        list_uses += f"\n\nPuede consultar el listado completo de usos del suelo en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "El suelo en {}{} en al año {} se utilizó para:\n\t- {}".format(
                            get_location_type_output(location_type),
                            location,
                            year,
                            list_uses.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de los usos que se le da al suelo de {location} en {year}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna localización válida.")

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionComarca(Action_Generic):
    def name(self):
        return "action_region"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["ComarcaMunicipio"], "entities": [location]}
                )

                if len(answer) > 0:
                    answer = filter_response(answer, location, exact=False)
                    found = []
                    for row in answer:
                        etiqueta = row['etiqueta']
                        if etiqueta.upper() == location.upper():
                            found.append(row)
                    if len(found) > 0:
                        dispatcher.utter_message(
                            build_virtuoso_response(
                                "{} se encuentra en la comarca {}.", found, is_title=True
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            build_virtuoso_response(
                                "{} se encuentra en la comarca {}.", answer, is_title=True
                            )
                        )
                else:
                    dispatcher.utter_message(
                        f"El municipio de {location} no pertenece a ninguna comarca."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna localización válida.")

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionLandType(Action_Generic):
    def name(self):
        return "action_land_type"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        text = tracker.latest_message["text"]
        year = getYearValuePerDefect(text,"2016")

        if location is not None:
            try:
                # TODO: Is needed this verification?
                # TODO: If needed, surround with try catch, not if
                if year is not None and year != "":
                    numberint = int(year)
                    if 1900 < numberint < 2100:
                        year = str(year)

                land_type = get_land_type(text)

                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                if land_type is not None:
                    answer = browser.search(
                        {
                            "intents": [
                                "hectareasTipoSuelo",
                                "tipoLocalizacion",
                                "Year",
                                "tipoSuelo",
                            ],
                            "entities": [location, location_type, year, land_type],
                        }
                    )

                    if len(answer) > 0:
                        utter_message = ""
                        for x in answer:
                            if "fecha" in x:
                                year = extract_value(x["fecha"])

                            utter_message += (
                                f"En {year} las hectáreas de suelo {land_type} "
                                f"en {get_location_type_output(location_type)}"
                                f"{extract_value(x['etiqueta'])} son {float(x['answer0'])}\n"
                            )

                        dispatcher.utter_message(utter_message)

                    else:
                        dispatcher.utter_message(
                            f"Lo siento pero no he encontrado datos del suelo {land_type} en {location} en mi base de conocimiento."
                        )
                else:
                    dispatcher.utter_message(
                        "Disculpa pero no he detectado ningún tipo de uso del suelo válido."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún municipio/comarca o provincia del que buscar el uso del suelo."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionBuildingAge(Action_Generic):
    def name(self):
        return "action_building_age"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        text = tracker.latest_message["text"]
        if location is not None:
            try:

                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(text)

                answer = browser.search(
                    {
                        "intents": [
                            "antiguedadEdificios",
                            "tipoLocalizacion",
                            "antiguedad",
                        ],
                        "entities": [location, location_type, ""],
                    }
                )

                if len(answer) > 0:
                    try:
                        diff_year = get_year(tracker.latest_message['text'])
                        uter_message = ""
                        total = 0
                        now = datetime.now()
                        year = now.year
                        for x in answer:
                            if extract_value(x['etiqueta2']).strip() != 'No aplicable':
                                try:
                                    year_ano = int(extract_value(x['etiqueta2']))
                                except:
                                    try:
                                        year_ano = int(extract_value(x['etiqueta2']).split('-')[1].strip())
                                    except:
                                        year_ano = int(extract_value(x['etiqueta2']).split(' ')[3].strip())
                                difference = year - year_ano
                                if difference>=diff_year:
                                    total = total + int(x['answer0'])
                        uter_message += (
                            f"Se construyeron en "
                            f"{get_location_type_output(location_type)}"
                            f"{extract_value(x['etiqueta'])} {total} edificios\n"
                        )
                        dispatcher.utter_message(uter_message)
                    except:
                        dispatcher.utter_message(
                            f"Lo siento pero no he encontrado datos en mi base de conocimiento sobre la antiguedad de los edificios en {location}"
                        )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado datos en mi base de conocimiento sobre la antiguedad de los edificios en {location}"
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún municipio/comarca o provincia del que buscar la edad de los edificios."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionPopulation(Action_Generic):
    def name(self):
        return "action_population"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

        location = clean_input(
            tracker.get_slot("location"),
            prefix=PLACE_TYPE
        )
        message = tracker.latest_message["text"]
        year_str = getYear(message)

        if location != tracker.get_slot("location"):
            location = tracker.get_slot("location")

        if location is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                # If there is no number at all, get current population
                answer = browser.search(
                    {
                        "intents": ["Poblacion", "Year", "tipoLocalizacion"],
                        "entities": [location, year_str, location_type],
                    }
                )

                if len(answer) > 0:
                    answer = filter_response(answer, location, exact=False)
                    if len(answer) > 1:
                        location_new = tracker.get_slot("location")
                        result = getCorrectRegister(answer,location_new)
                        umessage = f"La población en {location_new} en {year_str} es de {result[0]['answer0']} habitantes."
                    else:
                        location_new = tracker.get_slot("location")
                        link_test = extract_value(answer[0]['etiqueta'].title())
                        if link_test.find('(La)') > -1:
                            link_test = location_new
                        umessage = f"La población en {get_location_type_output(location_type)}{link_test} en {year_str} es de {answer[0]['answer0']} habitantes."
                    dispatcher.utter_message(umessage)

                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado datos de la poblacion de {get_location_type_output(location_type)}{location}"
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para buscar la población."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionCityHallAddress(Action_Generic):
    def name(self):
        return "action_city_hall_address"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = find_location(tracker.latest_message.get("entities", []))
        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["DireccionAyuntamiento"], "entities": [location]}
                )

                if len(answer) > 0:
                    answer = filter_response(answer, label=location)
                    found = []
                    for row in answer:
                        etiqueta = row['etiqueta']
                        if etiqueta.upper() == location.upper():
                            found.append(row)
                    if len(found)>0:
                        dispatcher.utter_message(
                            build_virtuoso_response(
                                "El ayuntamiento de {} está en {}.", found, is_title=True
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            build_virtuoso_response(
                                "El ayuntamiento de {} está en {}.", answer, is_title=True
                            )
                        )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado la dirección del ayuntamiento de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna municipio válido para informar sobre su ayuntamiento."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionCityHallCIF(Action_Generic):
    def name(self):
        return "action_city_hall_cif"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

        location = find_location(tracker.latest_message.get("entities", []))

        if location is not None:
            try:

                answer = browser.search(
                    {"intents": ["CIFAyuntamiento"], "entities": [location]}
                )

                if len(answer) > 0:
                    answer = filter_response(answer, label=location)
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "El CIF del ayuntamiento de {} es {}.", answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado el CIF del ayuntamiento de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ningún municipio válido.")

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionCityHallPhone(Action_Generic):
    def name(self):
        return "action_city_hall_phone"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = find_location(tracker.latest_message.get("entities", []))

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["TelefonoAyuntamiento"], "entities": [location]}
                )

                if len(answer) > 0:
                    answer = filter_response(answer, label=location)
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "El teléfono del ayuntamiento de {} es {}.", answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado el teléfono del ayuntamiento de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna localización válida.")

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionCityHallFax(Action_Generic):
    def name(self):
        return "action_city_hall_fax"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

        location = find_location(tracker.latest_message.get("entities", []))

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["FaxAyuntamiento"], "entities": [location]}
                )

                if len(answer) > 0:
                    answer = filter_response(answer, label=location)
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "El fax del ayuntamiento de {} es {}.", answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado el fax del ayuntamiento de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna localización válida.")

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionCityHallEmail(Action_Generic):
    def name(self):
        return "action_city_hall_email"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = find_location(tracker.latest_message.get("entities", []))

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["EmailAyuntamiento"], "entities": [location]}
                )

                if len(answer) > 0:
                    answer = filter_response(answer, label=location)
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "El email del ayuntamiento de {} es {}.", answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado el email del ayuntamiento de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna localización válida.")

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionMajor(Action_Generic):
    def name(self):
        return "action_major"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        entities = tracker.latest_message['entities']
        encontrado = False
        for entity in entities:
            type = entity['entity']
            if type == 'location':
                if entity['value'] == 'comarca':
                    encontrado = True
                    break

        if encontrado == False:
            location = find_location(tracker.latest_message.get("entities", []))
        else:
            location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["Municipio", "Cargo"],
                        "entities": [location, "Alcalde"],
                    }
                )

                if len(answer) > 0:
                    answer = filter_response(answer, label=location,exact=False)

                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "{} esta presidida por {}", answer, is_title=True
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado quién es el alcalde de {location}."
                    )

            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún municipio del que buscar su alcalde."
            )
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionCouncilors(Action_Generic):
    def name(self):
        return "action_councilors"

    def run(self, dispatcher, tracker, domain):

        super().run(dispatcher, tracker, domain)

        location = find_location(tracker.latest_message.get("entities", []))
        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["Municipio", "Cargo"],
                        "entities": [location, "Concejal"],
                    }
                )

                if len(answer) > 0:
                    # link = None
                    councilors = defaultdict(list)
                    # if len(answer) > 5:
                    #     answer = answer[0:5]
                    #     link = browser.url

                    answer = filter_response(answer, label=location)
                    for x in answer:
                        councilors[title(x["etiqueta"])].append(title(x["answer0"]))

                    response = ""
                    for place in councilors:
                        list_councilors = "\n\t- ".join(councilors[place])
                        # TODO: Not necessary
                        # if link is not None:
                        #     list_answer = "{}\n\nPuede consultar el listado completo de concejales en el siguiente {}".format(
                        #         list_councilors, link
                        #     )
                        # else:
                        #     list_answer = list_councilors
                        #
                        response += "En {}, la concejalía está formada por:\n\t- {}\n\n".format(
                            place, list_councilors
                        )

                    dispatcher.utter_message(response)
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado concejales de {location} en mi base de conocimiento."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún municipio del que buscar sus concejales."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionNumberContainers(Action_Generic):
    def name(self):
        return "action_number_containers"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        year = getYear(tracker.latest_message["text"])

        if location is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                answer = browser.search(
                    {
                        "intents": ["numContenedoresVidrio", "tipoLocalizacion","year"],
                        "entities": [location, location_type,year],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "En {}{} hay {} contenedores de vidrio".format(
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                            answer[0]["answer0"],
                        )
                    )

                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos de los contenedores de vidrio de {get_location_type_output(location_type)}{location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún municipio,comarca o provincia del que buscar sus contenedores de vidrio."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionGlassKgs(Action_Generic):
    def name(self):
        return "action_glass_kgs"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        message = tracker.latest_message["text"]
        year = getYear(message)

        if location is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                answer = browser.search(
                    {
                        "intents": ["kilosVidrioRecogidos", "tipoLocalizacion", "Year"],
                        "entities": [location, location_type, year],
                    }
                )

                if len(answer) > 0:
                    # TODO: Check if necesary
                    if year:
                        dispatcher.utter_message(
                            "En {}{} en {} se recogieron {} kilógramos de vidrio.".format(
                                get_location_type_output(location_type),
                                extract_value(answer[0]["etiqueta"]),
                                year,
                                answer[0]["answer0"],
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            "En {}{} se recogieron {} kilógramos de vidrio.".format(
                                get_location_type_output(location_type),
                                extract_value(answer[0]["etiqueta"]),
                                answer[0]["answer0"],
                            )
                        )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado datos sobre la recogida de vidrio en {get_location_type_output(location_type)}{location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna localización válida.")

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


# TODO ver que tipos de superficie se deben pasar
class ActionSurfaceType2(Action_Generic):
    def name(self):
        return "action_surface_type"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)

        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        surface_type = get_surface_type(tracker.latest_message["text"])
        if location is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                answer = browser.search(
                    {
                        "intents": [
                            "hectareasZona",
                            "tipoLocalizacion",
                            "tipoSuperficie",
                        ],
                        "entities": [
                            location,
                            location_type,
                            surface_type.replace(" ", "-"),
                        ],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "En {}{} hay {} hectareas de {}".format(
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                            float(answer[0]["answer0"]),
                            surface_type,
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos de {surface_type} para {get_location_type_output(location_type)}{location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún municipio,comarca o provincia del que buscar "
                + surface_type
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionFires(Action_Generic):
    def name(self):
        return "action_fires"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        message = tracker.latest_message["text"]
        year = getYear(message)

        if location is not None and year is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                answer = browser.search(
                    {
                        "intents": ["numIncendios", "tipoLocalizacion", "Year"],
                        "entities": [location, location_type, year],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "En {}{} hubo {} incendios durante el año {}".format(
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                            answer[0]["answer0"],
                            year,
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de incendios en {get_location_type_output(location_type)}{location} en el año {year}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para buscar información de incendios."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionSurfaceBurned(Action_Generic):
    def name(self):
        return "action_surface_burned"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        message = tracker.latest_message["text"]
        year = getYear(message)

        if location is not None and year is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                answer = browser.search(
                    {
                        "intents": ["hectareasQuemadas", "tipoLocalizacion", "Year"],
                        "entities": [location, location_type, year],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "En {}{} se quemaron {} hectáreas durante el año {}.".format(
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                            answer[0]["answer0"],
                            year,
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de superficie quemada de {get_location_type_output(location_type)}{location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para buscar superficie quemada."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTreatmentPlants(Action_Generic):
    def name(self):
        return "action_treatment_plants"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        message = tracker.latest_message["text"]
        year = getYear(message)

        if location is not None and year is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])
                answer = browser.search(
                    {
                        "intents": ["numDepuradoras", "tipoLocalizacion", "Year"],
                        "entities": [location, location_type, year],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "En {}{} había {} plantas depuradoras en {}.".format(
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                            answer[0]["answer0"],
                            year,
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de depuradoras en {get_location_type_output(location_type)}{location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para buscar depuradoras."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


# TODO: revisar respuesta sparql
class ActionCorpsSector(Action_Generic):
    def name(self):
        return "action_corps_sector"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        if location is not None:
            try:
                sector = get_sector_type(tracker.latest_message["text"])
                if sector is None:
                    dispatcher.utter_message(
                        "No se ha detectado un sector válido, los sectores disponibles son: construcción, industria, agricultura y servicios."
                    )
                    return [SlotSet("location", None), SlotSet("number", None)]

                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                answer = browser.search(
                    {
                        "intents": ["empresasPorSector", "tipoLocalizacion", "sector"],
                        "entities": [location, location_type, sector],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "En {}{} hay {} empresas del sector {}.".format(
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                            answer[0]["answer0"],
                            sector,
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de empresas en {get_location_type_output(location_type)}{location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para buscar empresas."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionSelfEmployed(Action_Generic):
    def name(self):
        return "action_self_employed"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        entities = get_duckling_entities(message.lower())
        entity = next(
            (
                x
                for x in entities
                if x["entity"] == "time" and x["duckValue"]["grain"] == "month"
            ),
            None,
        )
        if location is None or location == "":
            location = "Aragón"

        if entity is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                person_type = get_person_type(message)
                date = str(entity["duckValue"]["value"])
                year, month, _ = date.split("-")
                if month not in ["03", "06", "09", "12"]:
                    dispatcher.utter_message(
                        "Sólo se tienen datos de los meses de fin de trimestre: 3, 6, 9 ó 12"
                    )
                    return [SlotSet("location", None), SlotSet("number", None)]

                date = f"{year}-{month}"
                answer = browser.search(
                    {
                        "intents": [
                            "numeroAutonomos",
                            "tipoLocalizacion",
                            "Year",
                            "sexo",
                        ],
                        "entities": [location, location_type, date, person_type],
                    }
                )

                if len(answer) > 0:
                    message = "{} personas se dieron de alta como profesionales por cuenta propia en el mes de {} en {}{}"
                    if person_type == "mujeres":
                        message = (
                            "{} mujeres se dieron de alta como profesionales por cuenta propia en el mes de {} en {}{}"
                        )
                    elif person_type == "hombres":
                        message = (
                            "{} hombre se dieron de alta como profesionales por cuenta propia en el mes de {} en {}{}"
                        )

                    dispatcher.utter_message(
                        message.format(
                            answer[0]["answer0"],
                            entity["value"],
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de autonomos en {get_location_type_output(location_type)}{location} en {date}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado una expresión temporal válida para buscar datos de trabajadores autonomos."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionCorpsSize(Action_Generic):
    def name(self):
        return "action_corps_size"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        # TODO: Function in base class
        entities = get_duckling_entities(message)
        entity = next(
            (
                x
                for x in entities
                if x["entity"] == "time"
                and "grain" in x["duckValue"]
                and x["duckValue"]["grain"] == "month"
            ),
            None,
        )
        # de 1 a 9  , de 1 - 9, entre 1 y 9, mas de 5000

        # Looking for interval of workers

        try:

            num_workers = None
            pattern = re.compile(r"([0-9]+ *[-ya] *[0-9]+)")
            match = pattern.search(message)
            group = match.group(0)

            if group is not None:
                interval = re.split(r"[-ya]", group)
                num_workers = interval[0].strip() + "-a-" + interval[1].strip()

            if num_workers is not None:
                if entity is not None:
                    try:
                        if location.lower() in ["aragon", "aragón"]:
                            location_type = "Aragon"
                        else:
                            location_type = get_location_type(
                                tracker.latest_message["text"]
                            )

                        date = str(entity["duckValue"]["value"])
                        year, month, _ = date.split("-")
                        if month not in ["03", "06", "09", "12"]:
                            dispatcher.utter_message(
                                "Sólo se tienen datos de los meses de fin de trimestre: 3, 6, 9 ó 12"
                            )
                            return [SlotSet("location", None), SlotSet("number", None)]

                        date = f"{year}-{month}"

                        answer = browser.search(
                            {
                                "intents": [
                                    "empresasPorTrabajadores",
                                    "tipoLocalizacion",
                                    "Year",
                                    "numTrabajadores",
                                ],
                                "entities": [location, location_type, date, num_workers],
                            }
                        )

                        if len(answer) > 0:
                            dispatcher.utter_message(
                                "En {} de {} había en {}{} {} empresas de {} trabajadores".format(
                                    month,
                                    year,
                                    get_location_type_output(location_type),
                                    extract_value(answer[0]["etiqueta"]),
                                    answer[0]["answer0"],
                                    group,
                                )
                            )
                        else:
                            dispatcher.utter_message(
                                f"No se han encontrado datos empresas de {get_location_type_output(location_type)}{location}."
                            )
                    except (URLError, Exception) as ex:
                        dispatcher.utter_message(str(ex))
                else:
                    dispatcher.utter_message(
                        "No he detectado una expresión temporal válida para buscar empresas."
                    )
            else:
                dispatcher.utter_message(
                    "No he detectado un rango válido. Tengo información en los siguientes rangos 1-9, 10-19, 20-49, 50-99, 100-199, 200-499, 500-999 y 1000-4999"
                )

        except:
            dispatcher.utter_message(
                "No se han encontrado datos de empresas en este periodo temporal."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionUnemployment(Action_Generic):
    def name(self):
        return "action_unemployment"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        year = getYear(message)

        if location is None or location == "":
            location = "Aragón"

        try:
            if location.lower() in ["aragon", "aragón"]:
                location_type = "Aragon"
            else:
                location_type = get_location_type(tracker.latest_message["text"])

            person_type = get_person_type(message)
            sector_type = get_employ_sector_type(message)

            # TODO: Comprobar que el mes sea los válidos: 3-6-9-12

            answer = browser.search(
                {
                    "intents": [
                        "numParados",
                        "tipoLocalizacion",
                        "Year",
                        "sexo",
                        "sector",
                    ],
                    "entities": [
                        location,
                        location_type,
                        year,
                        person_type,
                        sector_type,
                    ],
                }
            )

            if len(answer) > 0:
                message = "En {} había {} desempleados en {}{} en el sector {}"
                if person_type == "mujeres":
                    message = "En {} había {} mujeres desempleadas en {}{} en el sector {}"
                elif person_type == "hombres":
                    message = "En {} había {} hombres desempleados en {}{} en el sector {}"

                dispatcher.utter_message(
                    message.format(
                        year,
                        answer[0]["answer0"],
                        get_location_type_output(location_type),
                        extract_value(answer[0]["etiqueta"]),
                        sector_type,
                    )
                )
            else:
                dispatcher.utter_message(
                    f"No se han encontrado datos de desempleo de {get_location_type_output(location_type)}{location}."
                )

        except (URLError, Exception) as ex:
            dispatcher.utter_message(str(ex))

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionContracts(Action_Generic):
    def name(self):
        return "action_contracts"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)

        # We need to extract a month to search for contracts numbers
        entities = get_duckling_entities(message)
        pprint(entities)
        entity = next(
            (
                x
                for x in entities
                if x["entity"] == "time"
                and x["duckValue"]["grain"] == "month"
                and x["duckValue"]["values"] == []
            ),
            None,
        )
        if location is None or location == "":
            location = "Aragón"

        if entity is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(message)

                person_type = get_person_type(message)
                date = str(entity["duckValue"]["value"])
                year, month, _ = date.split("-")
                # Database contains data splitted each quarter of the year
                if month not in ["03", "06", "09", "12"]:
                    dispatcher.utter_message(
                        "Sólo se tienen datos de los meses de fin de trimestre: 3, 6, 9 ó 12"
                    )
                    return [SlotSet("location", None), SlotSet("number", None)]

                # Format for the database
                date = f"{year}-{month}"
                print("DATE", date)
                answer = browser.search(
                    {
                        "intents": [
                            "numContratados",
                            "tipoLocalizacion",
                            "Year",
                            "sexo",
                        ],
                        "entities": [location, location_type, date, person_type],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "En {} se contrataron {} {} en {}{}".format(
                            entity["value"],
                            answer[0]["answer0"],
                            person_type,
                            get_location_type_output(location_type),
                            extract_value(answer[0]["etiqueta"]),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de contratación en {get_location_type_output(location_type)}{location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado una expresión temporal válida para buscar datos de contratación."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionWorkAccidents(Action_Generic):
    def name(self):
        return "action_work_accidents"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        year = getYear(message)

        if location is None or location == "":
            location = "Aragón"

        try:
            if location.lower() in ["aragon", "aragón"]:
                location_type = "Aragon"
            else:
                location_type = get_location_type(message)

            answer = browser.search(
                {
                    "intents": ["numAccidentesLaborales", "tipoLocalizacion", "Year"],
                    "entities": [location, location_type, year],
                }
            )

            if len(answer) > 0:
                dispatcher.utter_message(
                    "En {} hubo {} accidentes laborales en {}{}".format(
                        year,
                        answer[0]["answer0"],
                        get_location_type_output(location_type),
                        extract_value(answer[0]["etiqueta"]),
                    )
                )
            else:
                dispatcher.utter_message(
                    f"No se han encontrado datos de accidentes laborales de {get_location_type_output(location_type)}{location}."
                )

        except (URLError, Exception) as ex:
            dispatcher.utter_message(str(ex))

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionPerCapitaIncome(Action_Generic):
    def name(self):
        return "action_per_capita_income"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"), prefix=PLACE_TYPE)
        year = getYear(message)

        if location is None or location == "":
            location = "Aragón"

        try:
            if location.lower() in ["aragon", "aragón"]:
                location_type = "Aragon"
            else:
                location_type = get_location_type(message)

            print(year)
            print(location_type)
            print(location)

            answer = browser.search(
                {
                    "intents": ["rentaPerCapita", "tipoLocalizacion", "Year"],
                    "entities": [location, location_type, year],
                }
            )

            if len(answer) > 0:
                message = "En {} la renta per capita fue de {} en {}{}."

                dispatcher.utter_message(
                    message.format(
                        year,
                        answer[0]["answer0"],
                        get_location_type_output(location_type),
                        extract_value(answer[0]["etiqueta"]),
                    )
                )
            else:
                dispatcher.utter_message(
                    f"No se han encontrado datos de renta per capita de {get_location_type_output(location_type)}{location}."
                )

        except (URLError, Exception) as ex:
            dispatcher.utter_message(str(ex))

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]

"""
class ActionSurface(Action_Generic):
    def name(self):
        return "action_surface"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        try:
            if location is not None:
                answer = browser.search(
                    {"intents": ["SuperficieMunicipio"], "entities": [location]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "La superficie de {} es de {} kilómetros cuadrados", answer
                        )
                    )
                else:
                    dispatcher.utter_message("No se han encontrado datos en Virtuoso.")
            else:
                dispatcher.utter_message("No he detectado ninguna localización válida")
        except (URLError, Exception) as ex:
            dispatcher.utter_message(str(ex))

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionSurfaceType(Action_Generic):
    def name(self):
        return "action_surface_type"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        kind = tracker.get_slot("kind")

        if kind not in ["regadio", "secano"]:
            dispatcher.utter_message(
                "No se ha detectado ningún tipo de superficie, especifique si es de secano o de regadio "
                "la información que pretende buscar."
            )
            return [SlotSet("kind", None)]

        location = tracker.get_slot("location")

        if location is not None:
            try:
                response = ""
                year_str =  tracker.get_slot("number") # extract_year(tracker.latest_message.get("text"))
                # Year checking value, storing year to search for, current if anything fails parsing the text
                if year_str:
                    try:
                        if 2015 < int(year_str) < 1995:
                            year_str = "2014"
                            response = "No se tienen datos más alla de 2015 o prevíos a 1995. Los últimos datos que se tienen son de 2014. "

                    except ValueError:
                        year_str = "2014"
                        response = f"No se ha detectado un año concreto. Los últimos datos que se tienen de superficie de {kind} son de 2014. "
                else:
                    year_str = "2014"
                    response = f"No se ha detectado un año concreto. Los últimos datos que se tienen de superficie de {kind} son de 2014. "

                answer = browser.search(
                    {
                        "intents": [f"Superficie{kind.capitalize()}", "Year"],
                        "entities": [location, year_str],
                    }
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            response
                            + "La superficie de %s en {} en %s era de {} hectaréas."
                            % (kind, year_str),
                            answer,
                        )
                    )
                else:
                    dispatcher.utter_message("No se han encontrado datos en Virtuoso.")
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna localización válida.")

        return [SlotSet("location", None), SlotSet("kind", None)]



"""
