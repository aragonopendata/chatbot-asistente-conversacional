from actions_module.utils import *

from pprint import pprint
from urllib.error import URLError

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from actions_utils import build_virtuoso_response, get_entities, title
from browser import Browser

from actions_module.Action_Generic import Action_Generic

#browser = Browser()

class ActionMuseumsLocation(Action_Generic):
    """Class which executes those actions related to museums (conversational frame -> tourism)
    """

    def name(self):
        return "action_museums_location"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            General Information to obtain the list of museums

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

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["museosLocalidad"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_museums = "{}"
                    if len(answer) > 5:
                        list_museums += f"\n\nPuede consultar el listado completo de museos en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Los museos de {} son:\n\t- {}".format(
                            location,
                            list_museums.format(
                                "\n\t- ".join(
                                    [
                                        x["answer0"]
                                        for x in answer
                                    ]
                                )
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"En {location} no hay museos o no dispongo información de los mismos."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para informar sobre sus museos."
            )
        
        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

class ActionRoutesThrough(Action_Generic):
    """Class which executes those actions related to transport routes
    """
    def name(self):
        return "action_routes_through"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Show information about transport routes of passengers

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

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["rutasCamino"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_routes = "{}"
                    if len(answer) > 5:
                        list_routes += f"\n\nPuede consultar el listado completo de rutas en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las rutas que pasan por {} son :\n\t- {}".format(
                            location,
                            list_routes.format(
                                "\n\t- ".join([title(x["answer0"]) for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos que pasan por {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para informar sobre las rutas que pasan por allí."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTourGuidePhone(Action_Generic):
    """Class which executes those actions which obtain the phone of a tourist guide
    """
    def name(self):
        return "action_tour_guide_phone"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Show the telephone number of a tourist guide

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

        # TODO: Use an slot for people
        person = tracker.get_slot("person")
        
        if person is not None:
            try:
                answer = browser.search(
                    {"intents": ["telefonoGuia"], "entities": [person]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response("El teléfono de {} es {}", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado el teléfono del guia turistico {person}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún nombre válido de guía turístico para proporcionar el teléfono."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTourGuideEmail(Action_Generic):
    """Class which executes those actions which obtain the email of a tourist guide
    """
    def name(self):
        return "action_tour_guide_email"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Show the email of a tourist guide

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

        person = tracker.get_slot("person")
        
        if person is not None:
            try:
                answer = browser.search(
                    {"intents": ["emailGuia"], "entities": [person]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response("El email de {} es {}", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado el email del guía turístico {person}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún nombre válido de guía turístico para buscar su email."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTourGuideWeb(Action_Generic):
    """Class which executes those actions which obtain the web page of a tourist guide
    """

    def name(self):
        return "action_tour_guide_web"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Show the web page of a tourist guide

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

        person = tracker.get_slot("person")
        
        if person is not None:
            try:
                answer = browser.search({"intents": ["webGuia"], "entities": [person]})

                if len(answer) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response("La web de {} es {}", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado la web del guía turístico  {person}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún nombre válido de guía turístico para buscar su web."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTourGuideContactInfo(Action_Generic):
    """Class which executes those actions which obtain all the contact information tourist guide
    """

    def name(self):
        return "action_tour_guide_contact_info"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Show all the contact information of a tourist guide

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

        person = tracker.get_slot("person")
        
        if person is not None:
            try:
                answer = browser.search(
                    {"intents": ["informacionGuia"], "entities": [person]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "La información de contacto de {} es {}".format(
                            title(answer[0]["etiqueta"]),
                            ", ".join([answer[0][key] for key in answer[0].keys()]),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de contacto del guía turístico {person}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún nombre válido de guía turístico para proporcionar su web."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTourOfficePhone(Action_Generic):
    """Class which executes those actions which obtain the phone number of a tourist information office
    """
    def name(self):
        return "action_tour_office_phone"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Show the phone number of a tourist information office

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

        location = tracker.get_slot("location")
        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["telefonoTurismo"], "entities": [location]}
                )

                if len(answer) > 0:
                    for x in answer:
                        if "answer2" in x:
                            break
                    else:
                        dispatcher.utter_message(
                            f"No encuentro el número de télefono de ninguna de las oficinas de {location}."
                        )

                        events.extend([ SlotSet("location", None)])
                        return events

                    list_offices = "{}"
                    if len(answer) > 5:
                        list_offices += f"\n\nPuede consultar el listado completo de teléfonos de oficinas en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Teléfonos de las oficinas de turismo de {}:\n\t- {}".format(
                            location,
                            list_offices.format(
                                "\n\t- ".join(
                                    [
                                        "{} ({}) {}".format(
                                            x["answer0"], x["answer1"], x["answer2"]
                                        )
                                        for x in answer
                                        if "answer2" in x
                                    ]
                                )
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado teléfono de las oficinas de turismo de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para proporcionar el teléfono de sus oficinas de turismo."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTourOfficeLocation(Action_Generic):
    """Class which executes those actions which obtain the list of tourist information office of a location
    """

    def name(self):
        return "action_tour_office_location"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Show the list of tourist information office of a location

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

        location = tracker.get_slot("location")
        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["direccionTurismo"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_offices = "{}"
                    if len(answer) > 5:
                        list_offices += f"\n\nPuede consultar el listado completo de oficinas de turismo en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las oficinas de turismo de {} son \n\t- {}".format(
                            location,
                            list_offices.format(
                                "\n\t- ".join(
                                    [
                                        "{} en {}".format(
                                            title(x["answer0"]), title(x["answer1"])
                                        )
                                        for x in answer
                                    ]
                                )
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado oficinas de turismo en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para buscar ls oficinas de turismo."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events
