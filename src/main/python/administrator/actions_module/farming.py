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

from browser import Browser

browser = Browser()


class ActionFarmingRegionsCity(Action_Generic):
    def name(self):
        return "action_farming_agricultural_regions_city"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["comarcasAgrariasLocalizacion"],
                        "entities": [location],
                    }
                )

                if len(answer) > 0:

                    list_comarcas = "{}"
                    if len(answer) > 5:
                        list_comarcas += f"\n\nPuede consultar el listado completo de comarcas agrarias en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "En {} hay las siguientes comarcas agrarías\n\t- {}".format(
                            location,
                            list_comarcas.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de comarcas agrarias en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar comarcas agrarias."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionFarmingRegions(Action_Generic):
    def name(self):
        return "action_farming_agricultural_regions"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["municipioComarcasAgrarias"], "entities": [location]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "La comarca agraría {} pertenece al municipio de {}".format(
                            location, answer[0]["etiqueta"]
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado la comarca agraria a la que pertenece {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar la comarca agraria a la que pertenece."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionFarmingVillasCity(Action_Generic):
    def name(self):
        return "action_farming_villas_and_lands_city"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["villasLocalizacion"], "entities": [location]}
                )

                if len(answer) > 0:
                    list_villas = "{}"
                    if len(answer) > 5:
                        list_villas += f"\n\nPuede consultar el listado completo de villas y tierras del municipio en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Las villas y tierras del municipio {} son\n\t- {}".format(
                            location,
                            list_villas.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de villas y tierras para {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar villas y tierras."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionFarmingVillas(Action_Generic):
    def name(self):
        return "action_farming_villas_and_lands"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["municipioVilla"], "entities": [location]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "La villa {} pertenece al municipio de  {}.".format(
                            location, answer[0]["answer0"]
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de la villa {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningúna villa válida para buscar el municipio al que pertenece."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionFarmingVillasInfo(Action_Generic):
    def name(self):
        return "action_farming_villas_and_lands_info"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

        location = tracker.get_slot("location")
        # organization = tracker.get_slot("organization")
        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["infoVilla"], "entities": [location]}
                )

                if len(answer) > 0:
                    dispatcher.utter_message(
                        "Los datos de la villa {} son:\n\t- localización: {}\n\t- teléfono: {}\n\t- email: {}\n\t- cif: {}".format(
                            answer[0]["etiqueta"],
                            answer[0]["answer0"],
                            answer[0]["answer1"],
                            answer[0]["answer2"],
                            answer[0]["answer3"],
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado informacion de la villa {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningúna villa valida para proporcionar su información."
            )

        return [SlotSet("location", None), SlotSet("number", None)]


class ActionFarmingFarmCrop(Action_Generic):
    def name(self):
        return "action_farming_farm_crop"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		

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

        return [SlotSet("location", None), SlotSet("number", None)]

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
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]
        numbers = get_duckling_numbers(message)
        number = ""
        if numbers != []:
            number = str(numbers[0])
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
                        return [SlotSet("location", None), SlotSet("number", None)]
                else:
                    dispatcher.utter_message(
                        "No se ha encontrado un tipo de cultivo del que buscar información"
                    )
                    return [SlotSet("location", None), SlotSet("number", None)]

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

        return [SlotSet("location", None), SlotSet("number", None)]

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
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]
        numbers = get_duckling_numbers(message)
        year = ""
        if numbers != []:
            year = str(numbers[0])

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
                elif place_type == "comarca":
                    place_type_string = "la " + place_type + " de "
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

        return [SlotSet("location", None), SlotSet("number", None)]
