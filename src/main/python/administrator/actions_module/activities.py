'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from actions_module.utils import *

from pprint import pprint
from urllib.error import URLError

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from actions_utils import build_virtuoso_response, get_entities, title
from browser import Browser

from actions_module.Action_Generic import Action_Generic

#browser = Browser()


class ActionMuseumWorks(Action_Generic):
    def name(self):
        return "action_museum_works"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["obrasMuseo"], "entities": [location]}
                )

                if len(answer) > 0:
                    # TODO: This string formation could be in a function
                    list_works = "{}"
                    if len(answer) > 5:
                        list_works += f"\n\nPuede consultar el listado completo de obras en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las obras de {} son:\n\t- {}".format(
                            answer[0]["etiqueta"],
                            list_works.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de obras en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún museo válido para informar sobre sus obras."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionMuseumsLocation(Action_Generic):
    def name(self):
        return "action_museums_location"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["museosLocalidad"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_museos = "{}"
                    if len(answer) > 5:
                        list_museos += f"\n\nPuede consultar el listado completo de museos en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Los museos de {} son:\n\t- {}".format(
                            location,
                            list_museos.format(
                                "\n\t- ".join(
                                    [
                                        x["answer0"]
                                        for x in answer
                                        if title(x["etiqueta"]) == location
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

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionLocationWork(Action_Generic):
    def name(self):
        return "action_location_work"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)


        entities = tracker.latest_message.get("entities", [])
        entity = next((x for x in entities if x["entity"] == "misc"), None)
        if entity is None:
            entity = next((x for x in entities if x["entity"] == "location"), None)
        if entity is not None:
            value = entity["value"]
            try:
                answer = browser.search(
                    {"intents": ["municipioObra"], "entities": [value]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "La obra {} la puedes encontrar en {}".format(
                            answer[0]["etiqueta"], answer[0]["answer0"]
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de la obra {value}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna obra válida.")

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRoutesOut(Action_Generic):
    def name(self):
        return "action_routes_out"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["rutasOrigen"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_rutas = "{}"
                    if len(answer) > 5:
                        list_rutas += f"\n\nPuede consultar el listado completo de rutas en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las rutas que salen de {} son:\n\t- {}".format(
                            location,
                            list_rutas.format(
                                "\n\t- ".join(
                                    [
                                        title(x["answer0"])
                                        for x in answer
                                        if title(x["etiqueta"]) == location
                                    ]
                                )
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de rutas en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido par informar sobre sus rutas."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRoutesIn(Action_Generic):
    def name(self):
        return "action_routes_in"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["rutasDestino"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_rutas = "{}"
                    if len(answer) > 5:
                        list_rutas += f"\n\nPuede consultar el listado completo de rutas en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las rutas que llegan a {} son :\n\t- {}".format(
                            location,
                            list_rutas.format(
                                "\n\t- ".join(
                                    [
                                        title(x["answer0"])
                                        for x in answer
                                        if title(x["etiqueta"]) == location
                                    ]
                                )
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No hay información de rutas que llegan a {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar las rutas que llegan."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRoutesThrough(Action_Generic):
    def name(self):
        return "action_routes_through"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["rutasCamino"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_rutas = "{}"
                    if len(answer) > 5:
                        list_rutas += f"\n\nPuede consultar el listado completo de rutas en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las rutas que pasan por {} son :\n\t- {}".format(
                            location,
                            list_rutas.format(
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

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionRoutesFromTo(Action_Generic):
    def name(self):
        return "action_routes_in_out"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        entities = tracker.latest_message.get("entities", [])

        if len(entities) > 1:
            route = []
            for entity in entities:
                if entity['confidence'] >= 1:
                    if entity['entity'] == 'location':
                        route.append(entity)
            try:
                orig = getOriginValue(route[0]["value"])
                dst = getOriginValue(route[1]["value"])
                answer = browser.search(
                    {
                        "intents": ["rutasOrigen", "rutasDestino"],
                        "entities": [orig, dst],
                    }
                )

                if len(answer) > 0:
                    list_rutas = "{}"
                    if len(answer) > 5:
                        list_rutas += f"\n\nPuede consultar el listado completo de hoteles en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las rutas que empiezan en {} y terminan en {} son:\n\t- {}".format(
                            orig,
                            dst,
                            list_rutas.format(
                                "\n\t- ".join([title(x["answer0"]) for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de rutas desde {orig} a {dst}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(
                    f"No se han encontrado datos de rutas entre las dos localizaciones."
                )
        else:
            dispatcher.utter_message(
                "No he detectado dos localizaciones para buscar rutas."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTourGuideName(Action_Generic):
    def name(self):
        return "action_tour_guide_name"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["guiasLocalidad"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_guias = "{}"
                    if len(answer) > 5:
                        list_guias += f"\n\nPuede consultar el listado completo de guias en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Los guias de turismo de {} son:\n\t- {}".format(
                            title(answer[0]["etiqueta"]),
                            list_guias.format(
                                "\n\t- ".join([title(x["answer0"]) for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado guías turísticos en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido par informas sobre guias turísticos."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTourGuidePhone(Action_Generic):
    def name(self):
        return "action_tour_guide_phone"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        # TODO: Utilizar un slot para las personas
        entities = tracker.latest_message.get("entities", [])
        entity = next((x for x in entities if x["entity"] == "person"), None)
        if entity is None:
            entity = next((x for x in entities if x["entity"] == "location"), None)
        if entity is not None:
            person = entity["value"]
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

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTourGuideEmail(Action_Generic):
    def name(self):
        return "action_tour_guide_email"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        entities = tracker.latest_message.get("entities", [])
        entity = next((x for x in entities if x["entity"] == "person"), None)
        if entity is None:
            entity = next((x for x in entities if x["entity"] == "location"), None)
        if entity is not None:
            person = entity["value"]
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

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTourGuideWeb(Action_Generic):
    def name(self):
        return "action_tour_guide_web"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        entities = tracker.latest_message.get("entities", [])
        entity = next((x for x in entities if x["entity"] == "person"), None)
        if entity is None:
            entity = next((x for x in entities if x["entity"] == "location"), None)
        if entity is not None:
            person = entity["value"]
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

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTourGuideContactInfo(Action_Generic):
    def name(self):
        return "action_tour_guide_contact_info"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        entities = tracker.latest_message.get("entities", [])
        print(entities)
        entity = next((x for x in entities if x["entity"] == "person"), None)
        if entity is None:
            entity = next((x for x in entities if x["entity"] == "location"), None)
        if entity is not None:
            person = entity["value"]
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

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTourOfficePhone(Action_Generic):
    def name(self):
        return "action_tour_office_phone"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

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

                        return [SlotSet("location", None)]

                    list_oficinas = "{}"
                    if len(answer) > 5:
                        list_oficinas += f"\n\nPuede consultar el listado completo de teléfonos de oficinas en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Teléfonos de las oficinas de turismo de {}:\n\t- {}".format(
                            location,
                            list_oficinas.format(
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

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionTourOfficeLocation(Action_Generic):
    def name(self):
        return "action_tour_office_location"

    def run(self, dispatcher, tracker, domain):
		
        super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")
        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["direccionTurismo"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_oficinas = "{}"
                    if len(answer) > 5:
                        list_oficinas += f"\n\nPuede consultar el listado completo de oficinas de turismo en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las oficinas de turismo de {} son \n\t- {}".format(
                            location,
                            list_oficinas.format(
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

        return [SlotSet("location", None), SlotSet("number", None)]
