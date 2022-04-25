'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from urllib.error import URLError

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from actions_module.Action_Generic import Action_Generic

from actions_utils import get_location_type, get_crop_type,get_duckling_numbers

from datetime import datetime

from browser import Browser

browser = Browser()




class ActionFarmingFarmCrop(Action_Generic):
    def name(self):
        return "action_farming_farm_crop"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)


        message = tracker.latest_message["text"]
        location = tracker.get_slot("location")

        if location is not None:
            crop_type = get_crop_type(message)

            if crop_type is not None:
                intent = self.get_intent(crop_type)
                print(crop_type, " ", intent)

                if intent is not None:
                    try:
                        answer = browser.search(
                            {"intents": [intent], "entities": [location]}
                        )
                        if len(answer) > 0:
                            try:
                                list_fincas = "{}"
                                if len(answer) > 5:
                                    list_fincas += f"\n\nPuede consultar el listado completo de fincas en el siguiente {browser.url}"
                                    answer = answer[:5]

                                dispatcher.utter_message(
                                    "Las fincas de {} son \n\t- {}".format(
                                        crop_type,
                                        list_fincas.format(
                                            "\n\t- ".join([x["answer0"] for x in answer])
                                        ),
                                    )
                                )
                            except:
                                dispatcher.utter_message(
                                    f"No se han encontrado datos de cultivo {crop_type} en {location}."
                                )
                        else:
                            dispatcher.utter_message(
                                f"No se han encontrado datos de cultivo {crop_type} en {location}."
                            )
                    except (URLError, Exception) as ex:
                        dispatcher.utter_message(str(ex))
                else:
                    dispatcher.utter_message(
                        "No he detectado tipos de cultivo válidos."
                    )
            else:
                dispatcher.utter_message("No he detectado tipos de cultivo.")
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar sus tipos de cultivo."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

    @staticmethod
    def get_intent(crop_type):
        if crop_type == "leñoso":
            return "fincasCultivoLenoso"
        elif crop_type == "secano":
            return "fincasSecanoLenosas"
        elif crop_type == "regadio":
            return "fincasRegadioLenosas"
        elif crop_type == "olivar":
            return "fincasOlivarLenosas"
        return None


class ActionFarmingFarmCropSize(Action_Generic):
    def name(self):
        return "action_farming_farm_crop_size"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)

        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]
        numbers = get_duckling_numbers(message)
        number = ""
        try:
            number = str(numbers[0]) if numbers != [] else str(datetime.now().year - 1)
        except Exception as e:
            number = str(datetime.now().year - 1)
        year = number
        a, b = "áéíóú", "aeiou"
        trans = str.maketrans(a, b)

        if location is not None:
            place_type_string = ""
            try:
                crop_type = get_crop_type(message)
                place_type = get_location_type(message)

                if crop_type is not None:
                    intent = self.get_intent(crop_type)
                    if intent is None:
                        dispatcher.utter_message(
                            "No se ha encontrado un tipo de cultivo del que buscar información"
                        )
                        events.extend([ SlotSet("location", None), SlotSet("number", None)])
                        return events
                else:
                    dispatcher.utter_message(
                        "No se ha encontrado un tipo de cultivo del que buscar información"
                    )
                    events.extend([ SlotSet("location", None), SlotSet("number", None)])
                    return events

                location_clean = location.lower().translate(trans)
                print(location_clean)

                if location_clean == "aragon":
                    location = "Aragón"
                    place_type = location_clean
                elif place_type == "municipio":
                    place_type_string = "el " + place_type + " de "
                elif place_type == "comarca":
                    place_type_string = "la " + place_type + " de "
                else:
                    place_type_string = "la " + place_type + " de "

                template = "En {}{} se cultivaron {} hectáreas de {}"
                if year is not None:
                    template += f" en el año {year}"
                else:
                    year = ""

                answer = browser.search(
                    {
                        "intents": [intent, "Year", "tipoLocalizacion"],
                        "entities": [location, str(year), place_type],
                    }
                )

                try:
                    if len(answer) > 0:
                        url = answer[0]["etiqueta"]
                        ano = url.split('/')[len(url.split('/'))-1]
                        template = "En {}{} se cultivaron {} hectáreas de {}"
                        year = ano
                        if year is not None:
                            template += f" en el año {year}"
                        else:
                            year = ""
                        dispatcher.utter_message(
                            template.format(
                                place_type_string, location, answer[0]["answer0"], crop_type, ano
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            f"No se han encontrado hectareas de cultivo de {location} del año {year}."
                        )
                except:
                    dispatcher.utter_message(
                        f"No se han encontrado hectareas de cultivo de {location} del año {year}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar las hectáreas de cultivo."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

    @staticmethod
    def get_intent(crop_type):
        if crop_type in ["olivar", "olivares", "oliva"]:
            return "hectareasOlivares"
        elif crop_type in ["viñedo", "viñedos", "uva"]:
            return "hectareasVinedos"
        elif crop_type in ["frutal", "frutales"]:
            return "hectareasFrutales"
        elif crop_type in ["herbaceos", "herbáceos"]:
            return "hectareasHerbaceos"
        elif crop_type in ["regadio", "regadío"]:
            return "hectareasRegadio"
        elif crop_type in ["rustico", "rustica"]:
            return "hectareasRustico"
        elif crop_type == "secano":
            return "hectareasSecano"

        return None


class ActionFarmingEcological(Action_Generic):
    def name(self):
        return "action_farming_ecological_agriculture"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]
        numbers = get_duckling_numbers(message)
        try:
            year = str(numbers[0]) if numbers != [] else str(datetime.now().year - 1)
        except Exception as e:
            year = str(datetime.now().year - 1)
        a, b = "áéíóú", "aeiou"
        trans = str.maketrans(a, b)

        if location is not None:
            place_type_string = ""
            try:
                place_type = get_location_type(message)
                locationclean = location.lower().translate(trans)

                if locationclean == "aragon":
                    location = "Aragón"
                    place_type = locationclean
                elif place_type == "municipio":
                    place_type_string = "el " + place_type + " de "
                else:
                    place_type_string = "la " + place_type + " de "
                template = "En {}{} se cultivaron {} hectáreas"
                if year is not None:
                    template += f" en el año {year}"
                else:
                    year = ""

                answer = browser.search(
                    {
                        "intents": [
                            "hectareasAgriculturaEcologica",
                            "Year",
                            "tipoLocalizacion",
                        ],
                        "entities": [location, str(year), place_type],
                    }
                )

                if len(answer) > 0 and answer != [{}]:
                    dispatcher.utter_message(
                        template.format(
                            place_type_string, location, answer[0]["answer0"]
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de agricultura ecológica en {location} en el año {year}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para dar las hectáreas de agricultura ecológica."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events
