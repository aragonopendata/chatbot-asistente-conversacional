"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
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
    """Class which executes action to obtain the phone number of a restaurant
    """

    def name(self):
        return "action_restaurant_phone"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain the phone number of a restaurant

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar el teléfono."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantFax(Action_Generic):
    """Class which executes action to obtain the fax number of a restaurant
    """
    def name(self):
        return "action_restaurant_fax"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain the fax number of a restaurant

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar el fax."
            )

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantEmail(Action_Generic):
    """Class which executes action to obtain the email address of a restaurant
    """

    def name(self):
        return "action_restaurant_email"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain the email address of a restaurant

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar el email."
            )

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantWeb(Action_Generic):
    """Class which executes action to obtain the web page of a restaurant
    """

    def name(self):
        return "action_restaurant_web"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain the web page of a restaurant

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar la página web."
            )

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantAddress(Action_Generic):
    """Class which executes action to obtain the address of a restaurant
    """

    def name(self):
        return "action_restaurant_address"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain the address of a restaurant

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Disculpa pero no he detectado ningún restaurante/bar del que buscar la dirección."
            )

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantsList(Action_Generic):
    """Class which executes action to obtain a list of restaurants in a specific place
    """

    def name(self):
        return "action_restaurant_list"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain a list of restaurants in a specific place

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

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
                    url_final = browser.__dict__['_Browser__query']
                    if len(answer) > 5:
                        '''if difference == True:
                            url_recover = browser.__dict__['_Browser__query']
                            url_recover = url_recover.replace('}','FILTER (?etiqueta="' + location.upper() + '") . }')
                            parse_query = url_parser.quote(url_recover)
                            url_final = "https://opendata.aragon.es/sparql?default-graph-uri=&query={0}&format=text%2Fhtml&timeout=0&debug=on".format(
                                parse_query
                            )
                        else:'''
                        url_recover = browser.__dict__['_Browser__query']
                        parse_query = url_parser.quote(url_recover)
                        url_final = "https://opendata.aragon.es/sparql?default-graph-uri=&query={0}&format=text%2Fhtml&timeout=0&debug=on".format(
                            parse_query
                        )
                        list_restaurants += f"\n\nPuedes consultar el listado completo de bares/restaurantes en el siguiente {url_final}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Hay cantidad de sitios donde disfrutar tomando algo en {}. Algunos de ellos, son:\n\t- {}".format(
                            location,
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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna localización del que buscar lugares para comer."
            )

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantReservation(Action_Generic):
    """Class which executes action to obtain the way to make a reservation in a restaurant
    """

    def name(self):
        return "action_restaurant_reservation"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain the way to make a reservation in a restaurant

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

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

                        try:
                            if len(responselist) > 2:
                                template += ", " + responselist[1] + " o " + responselist[2]
                            else:
                                template += " o " + responselist[1]
                        except:
                            pass
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

                            if len(responselist) == 1:
                                template += responselist[0]
                            else:
                                if len(responselist) == 2:
                                    template += responselist[0] + " o " + responselist[1]

                            template += "."
                            dispatcher.utter_message(template.format(response["etiqueta"]))

                    else:
                        dispatcher.utter_message(
                            f"No se han encontrado datos de como reservar en el restaurante {location}."
                        )

            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ningún restaurante/bar del que buscar información de reserva."
            )

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantLocation(Action_Generic):
    """Class which executes action to obtain where a restaurant is located
    """

    def name(self):
        return "action_restaurant_location"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain where a restaurant is located

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

        if location:
            try:
                # location = entities[0]["value"]
                answer = browser.search(
                    {"intents": ["municipioRestaurante"], "entities": [location]}
                )

                answer_filtered = filter_response(answer, location, exact=False)
                if len(answer_filtered) > 0:
                    dispatcher.utter_message(
                        "{} está en {}".format(location, answer_filtered[0]["answer0"].split('/')[len(answer_filtered[0]["answer0"].split('/'))-1])
                    )
                else:
                    dispatcher.utter_message(
                        f"Disculpa pero no encuentro donde está el restaurante/bar {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message("No he detectado ningún sitio válido.")

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionRestaurantNumber(Action_Generic):
    """Class which executes action to obtain how many restaurants there are in a specific area
    """

    def name(self):
        return "action_restaurant_number"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Information to obtain how many restaurants there are in a specific area

        Parameters
        ----------
        dispatcher: json
            Object where answer to the user is returned
        tracker: json
            Object that contains question, entities and intentions in order to solve th question
        domain:
            environment of the question

        Returns
        -------
        json dictionary

            Completed answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        try:
            location = clean_input(tracker.get_slot("location"), prefix=GASTRONOMY_TYPES)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("gastronomy_name")

        if location:
            try:
                # location = entities[0]["value"]
                answer = browser.search(
                    {"intents": ["numRestaurantes"], "entities": [location]}
                )
                if len(answer) > 0:
                    answer[0]['etiqueta'] = answer[0]['etiqueta'].split('/')[len(answer[0]['etiqueta'].split('/'))-1]
                    answer[0]['etiqueta'] = answer[0]['etiqueta'][0].upper() + answer[0]['etiqueta'][1:]
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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "Lo siento pero no he detectado ninguna localización de la que buscar el número de restaurantes."
            )

        # return []
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events
