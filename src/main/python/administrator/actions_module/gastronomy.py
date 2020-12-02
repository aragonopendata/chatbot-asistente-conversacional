'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from actions_module.utils import *

from urllib.error import URLError
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import urllib.parse as url_parser


from actions_module.Action_Generic import Action_Generic 

from actions_utils import (
    build_virtuoso_response,
    clean_input,
    GASTRONOMY_TYPES,
    filter_response,
)
from browser import Browser

browser = Browser()


class ActionRestaurantPhone(Action_Generic):
    def name(self):
        return "action_restaurant_phone"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["telefonoRestaurante"], "entities": [location]}
                )
                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "El teléfono de {} es {}.", answer_filtered
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado el teléfono del restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar el teléfono."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantFax(Action_Generic):
    def name(self):
        return "action_restaurant_fax"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["faxRestaurante"], "entities": [location]}
                )
                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response("El fax de {} es {}.", answer_filtered)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado el fax del restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar el fax."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantEmail(Action_Generic):
    def name(self):
        return "action_restaurant_email"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["emailRestaurante"], "entities": [location]}
                )

                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "El email de {} es {}.", answer_filtered
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado el correo electrónico del restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar el email."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantWeb(Action_Generic):
    def name(self):
        return "action_restaurant_web"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["webRestaurante"], "entities": [location]}
                )

                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response("La web de {} es {}.", answer_filtered)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado la página web del restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar la página web."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantAddress(Action_Generic):
    def name(self):
        return "action_restaurant_address"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["direccionRestaurante"], "entities": [location]}
                )

                if len(answer) > 0:
                    for x in answer:
                        template = "{} está en {}"
                        if "answer2" in x:
                            template += f", {x['answer2']}"
                        if "answer1" in x:
                            template += f" ({x['answer1']})"

                        template += "."
                        dispatcher.utter_message(
                            template.format(location, x["answer0"])
                        )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado la dirección del restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar la dirección."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantsList(Action_Generic):
    def name(self):
        return "action_restaurant_list"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["restaurantesCiudad"], "entities": [location]}
                )

                if len(answer) > 0:

                    answer2 = []
                    difference = False

                    for row in answer:
                        etiqueta = row['etiqueta']
                        if eliminaTildes(etiqueta.upper()) == eliminaTildes(location.upper()):
                            difference = True
                            answer2.append(row)

                    if len(answer2) > 0:
                        answer = answer2

                    list_restaurants = "{}"
                    if len(answer) > 5:
                        if difference == True:
                            url_recover = browser.__dict__['_Browser__query']
                            url_recover = url_recover.replace('}','FILTER (?etiqueta="' + location.upper() + '") . }')
                            parse_query = url_parser.quote(url_recover)
                            url_final = "https://opendata.aragon.es/sparql?default-graph-uri=&query={0}&format=text%2Fhtml&timeout=0&debug=on".format(
                                parse_query
                            )
                        else:
                            url_final = Browser.url
                        list_restaurants += f"\n\nPuedes consultar el listado completo de bares/restaurantes en el siguiente {url_final}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Hay cantidad de sitios donde disfrutar tomando algo en {}. Algunos de ellos, son:\n\t- {}".format(
                            answer[0]["etiqueta"],
                            list_restaurants.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado un listado de los restaurantes/bares de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna localización del que buscar lugares para comer."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantReservation(Action_Generic):
    def name(self):
        return "action_restaurant_reservation"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["reservaRestaurantes"], "entities": [location]}
                )

                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    for response in answer_filtered:
                        template = "Puedes reservar de diferentes formas en el restaurante {} : "
                        responselist = []
                        if "answer1" in response:
                            responselist.append(
                                f"mandando un email a {response['answer1']}"
                            )
                        if "answer2" in response:
                            responselist.append(f"llamando a {response['answer2']}")
                        if "answer0" in response:
                            responselist.append(f"yendo al local de la {response['answer0']}")

                        template += responselist[0]

                        if len(responselist) > 2:
                            template += ", " + responselist[1] + " o " + responselist[2]
                        else:
                            template += " o " + responselist[1]
                        template += "."
                        dispatcher.utter_message(template.format(response["etiqueta"]))
                else:
                    answer = browser.search(
                        {"intents": ["reservaRestaurantesTelefono"], "entities": [location]}
                    )
                    answer = filter_response(answer, location, exact=False)

                    if len(answer) > 0:
                        for response in answer:
                            template = "Puedes reservar den el restaurante {} : "
                            responselist = []
                            if "answer0" in response:
                                responselist.append(f"Yendo al local de la {response['answer0']}")
                            if "answer1" in response:
                                responselist.append(f"llamando a {response['answer1']}")

                            template += responselist[0] + " o " + responselist[1]

                            template += "."
                            dispatcher.utter_message(template.format(response["etiqueta"]))

                    else:
                        dispatcher.utter_message(
                            f"No se han encontrado datos de como reservar en el restaurante {location}."
                        )

            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ningún restaurante/bar del que buscar información de reserva."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantsSpots(Action_Generic):
    def name(self):
        return "action_restaurant_spots"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["plazasRestaurante"], "entities": [location]}
                )

                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    count = 0
                    for x in answer_filtered:
                        if x["etiqueta"].lower() == tracker.get_slot("location").lower():
                            dispatcher.utter_message(
                                "Las plazas de {} son {}".format(
                                    x["etiqueta"], x["answer0"]
                                )
                            )
                            count = count + 1
                    if count == 0:
                        dispatcher.utter_message(
                            f"No he encontrado cuantas plazas tiene el restaurante/bar {location}."
                        )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado cuantas plazas tiene el restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún restaurante/bar del que buscar su número de plazas."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantLocation(Action_Generic):
    def name(self):
        return "action_restaurant_location"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)

        if location:
            try:
                # location = entities[0]["value"]
                answer = browser.search(
                    {"intents": ["municipioRestaurante"], "entities": [location]}
                )

                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    dispatcher.utter_message(
                        "{} está en {}".format(location, answer_filtered[0]["answer0"])
                    )
                else:
                    dispatcher.utter_message(
                        f"Disculpa pero no encuentro donde está el restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ningún sitio válido.")

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRestaurantNumber(Action_Generic):
    def name(self):
        return "action_restaurant_number"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location:
            try:
                # location = entities[0]["value"]
                answer = browser.search(
                    {"intents": ["numRestaurantes"], "entities": [location]}
                )
                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "En {} hay {} sitios donde poder tomar algo",
                            answer_filtered,
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Disculpa pero no encuentro cuantos restaurantes/bares hay en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Lo siento pero no he detectado ninguna localización de la que buscar el número de restaurantes."
            )

        # return []
        return [SlotSet("location", None), SlotSet("number", None)]
