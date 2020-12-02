'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from urllib.error import URLError
from rasa_sdk.events import SlotSet
from actions_module.Action_Generic import Action_Generic
from browser import Browser

browser = Browser()


class ActionTouristActiveList(Action_Generic):
    def name(self):
        return "action_tourist_active_entreprise"

    def run(self, dispatcher, tracker, domain):

        super().run(dispatcher, tracker, domain)
		
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
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar empresas turisticas activas."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTouristActiveActivities(Action_Generic):
    def name(self):
        return "action_tourist_active_activities"

    def run(self, dispatcher, tracker, domain):

        super().run(dispatcher, tracker, domain)

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
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar empresas turisticas activas."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTouristActiveContacto(Action_Generic):
    def name(self):
        return "action_tourist_active_entreprise_contact"

    def run(self, dispatcher, tracker, domain):

        super().run(dispatcher, tracker, domain)

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
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para informacion de la empresa turística."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTouristActiveDireccion(Action_Generic):
    def name(self):
        return "action_tourist_active_entreprise_address"

    def run(self, dispatcher, tracker, domain):

        super().run(dispatcher, tracker, domain)

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
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido de la direccion de la empresa turistica."
            )

        return [SlotSet("location", None), SlotSet("number", None)]