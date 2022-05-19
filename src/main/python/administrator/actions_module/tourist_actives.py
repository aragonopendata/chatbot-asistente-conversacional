from urllib.error import URLError
from rasa_sdk.events import SlotSet
from actions_module.Action_Generic import Action_Generic
from browser import Browser

browser = Browser()


class ActionTouristActiveList(Action_Generic):
    """Class which executes action to obtain a list of active tourist companies
    """

    def name(self):
        return "action_tourist_active_entreprise"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Information to obtain a list of active tourist companies

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
                    {
                        "intents": ["empresasTuristicasActivas"],
                        "entities": [location],
                    }
                )

                if len(answer) > 0:

                    list_empresas_turisticas = "{}"
                    if len(answer) > 5:
                        list_empresas_turisticas += f"\n\nPuede consultar el listado completo de empresas turisticas activas en la siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "En {} hay las siguiente lista de empresas activas\n\t- {}".format(
                            location,
                            list_empresas_turisticas.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de empresas turisticas activas en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar empresas turisticas activas."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTouristActiveActivities(Action_Generic):
    """Class which executes action to obtain a list of activities provided by active tourist companies
    """

    def name(self):
        return "action_tourist_active_activities"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Information to obtain a list of activities provided by active tourist companies

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

        location = tracker.get_slot('active_tourism_entreprise')

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["empresasTuristicasActividades"],
                        "entities": [location],
                    }
                )

                if len(answer) > 0:
                    try:
                        list_empresas_turisticas = "{}"
                        if len(answer) > 5:
                            list_empresas_turisticas += f"\n\nPuede consultar el listado completo de actividades de empresas turisticas activas en la siguiente {browser.url}"
                            answer = answer[:5]

                        dispatcher.utter_message(
                            "En {} hay las siguiente lista los servicios y actividades de las empresas turísticas \n\t- {}".format(
                                location,
                                list_empresas_turisticas.format(
                                    "\n\t- ".join([x["answer0"] for x in answer])
                                ),
                            )
                        )
                    except:
                        dispatcher.utter_message(
                            f"No se han encontrado datos de los servicios / actividades de empresas turisticas activas en {location}."
                        )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de los servicios / actividades de empresas turisticas activas en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar empresas turisticas activas."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTouristActiveContacto(Action_Generic):
    """Class which executes action to obtain a the main contact of a active tourist company
    """

    def name(self):
        return "action_tourist_active_entreprise_contact"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Information to obtain a the main contact of a active tourist company

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

        location = tracker.get_slot('active_tourism_entreprise')

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["empresasTuristicasContacto"],
                        "entities": [location],
                    }
                )

                if len(answer) > 0:
                    try:
                        dispatcher.utter_message(
                            "La empresa turistica {} tiene la siguiente datos de contacto {}".format(
                                answer[0]["etiqueta"], answer[0]["answer0"]
                            )
                        )
                    except:
                        dispatcher.utter_message(
                            f"No se han encontrado datos de contacto de la empresa turistica {location}."
                        )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de contacto de la empresa turistica {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para informacion de la empresa turística."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTouristActiveDireccion(Action_Generic):
    """Class which executes action to obtain a the address of a active tourist company
    """

    def name(self):
        return "action_tourist_active_entreprise_address"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. 
            Information tto obtain a the address of a active tourist company

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

        location = tracker.get_slot('active_tourism_entreprise')

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["empresasTuristicasDireccion"],
                        "entities": [location],
                    }
                )

                if len(answer) > 0:
                    try:
                        dispatcher.utter_message(
                            "La empresa turistica {} tiene la direccion {}".format(
                                answer[0]["etiqueta"], answer[0]["answer0"]
                            )
                        )
                    except:
                        dispatcher.utter_message(
                            f"No se han encontrado datos de contacto de la empresa turistica {location}."
                        )
                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado la direccion de la empresa turistica {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido de la direccion de la empresa turistica."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events