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


from actions_module.Action_Generic import Action_Generic 

from actions_utils import (
    build_virtuoso_response,
    get_accommodation_type,
    accommodation_list_string,
    get_season,
    get_room_type,
    get_location_type,
    get_accommodation_type_plural,
    number_to_date,
    get_singular_or_plural,
    accommodation_plural_list_string,
    clean_input,
    get_accommodation_type_output,
    get_province_code,
    get_location_type_output,
    filter_response,
    get_duckling_entities
)

from browser import Browser

browser = Browser()


class ActionAccommodationInfo(Action_Generic):
    def name(self):
        return "action_accommodation_info"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        intent = tracker.latest_message.get("intent").get("name")
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"), invalid_words=None)

        if location is None:
            location = tracker.get_slot("accomodation_name")

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                if accommodation_type is None:
                    dispatcher.utter_message(accommodation_list_string())
                    return []

                intent, template = self.get_intent_and_template(intent=intent)
                if intent is None:
                    dispatcher.utter_message(
                        "Información de alojamiento solicitada no reconocida."
                    )
                    events.extend([ SlotSet("location", None), SlotSet("number", None)])
                    return events

                answer = browser.search(
                    {
                        "intents": [intent, "tipoAlojamiento"],
                        "entities": [location, accommodation_type],
                    }
                )
                
                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    if len(answer) == 1:
                        if intent == "direccionAlojamiento":
                            template = self.update_template(template, answer[0])

                        dispatcher.utter_message(
                            template.format(
                                get_accommodation_type_output(accommodation_type),
                                answer[0]["etiqueta"],
                                answer[0]["answer0"],
                            )+"."
                        )
                    else:
                        for row in answer:
                            etiqueta = row['etiqueta']
                            if etiqueta.upper() == location.upper():
                                if intent == "direccionAlojamiento":
                                    template = self.update_template(template, row)

                                dispatcher.utter_message(
                                    template.format(
                                        get_accommodation_type_output(accommodation_type),
                                        row["etiqueta"],
                                        row["answer0"],
                                    ) + "."
                                )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado la dirección {get_accommodation_type_output(accommodation_type)} {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                f"No he detectado ningún alojamiento sobre el que buscar su dirección."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("accomodation_name", None)])
        return events

    @staticmethod
    def get_intent_and_template(intent):
        # TODO: Set an error msg to respond accurately:
        # No he encontrado el {cosa} del {acc_type} {location}
        if "phone" in intent:
            return "telefonoAlojamiento", "El teléfono {} {} es {}"
        elif "fax" in intent:
            return "faxAlojamiento", "El fax {} {} es {}"
        elif "email" in intent:
            return "emailAlojamiento", "El email {} {} es {}"
        elif "web" in intent:
            return "webAlojamiento", "La web {} {} es {}"
        elif "address" in intent:
            return "direccionAlojamiento", "La dirección {} {} es {}"
        else:
            return None, ""

    @staticmethod
    def update_template(template, answer):
        original=template

        try:
            if "answer2" in answer:
                template += f", {answer['answer2']}"
            if "answer1" in answer:
                template += f" ({answer['answer1']})"

            return f"{template}"
        except Exception as inst:
            return original


class ActionAccommodationList(Action_Generic):
    def name(self):
        return "action_accommodation_list"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]
        accommodation_type_plural = get_accommodation_type_plural(message)

        if location is not None:
            try:
                if location.lower() in ["aragon", "aragón"]:
                    dispatcher.utter_message(
                        f"Solo dispongo de información de {accommodation_type_plural} en municipios y provincias."
                    )
                else:
                    location_type = get_location_type(message)
                    location_req = location
                    if location_type == "provincia":
                        location_req = get_province_code(location)

                    if accommodation_type_plural is None:
                        dispatcher.utter_message(accommodation_plural_list_string())
                        return []
                    else:
                        accommodation_type = get_singular_or_plural(
                            accommodation_type_plural
                        )

                    answer = browser.search(
                        {
                            "intents": [
                                "listadoAlojamiento",
                                "tipoAlojamiento",
                                "tipoLugar",
                            ],
                            "entities": [
                                location_req,
                                accommodation_type,
                                location_type,
                            ],
                        }
                    )
                    #answer = filter_response(answer, location_req)
                    if len(answer) > 0:

                        answer2 = []
                        for row in answer:
                            etiqueta = row['etiqueta']
                            if eliminaTildes(etiqueta.upper()) == eliminaTildes(location.upper()):
                                answer2.append(row)

                        if len(answer2) > 0:
                            answer = answer2

                        list_accomodations = "{}"
                        if len(answer) > 5:
                            list_accomodations += (
                                f"\n\nPuedes consultar el listado completo de {accommodation_type_plural} "
                                f"en el siguiente enlace {browser.url}"
                            )
                            answer = answer[:5]

                        dispatcher.utter_message(
                            "Este es el listado de {} en {}{}:\n\t- {}.".format(
                                accommodation_type_plural,
                                get_location_type_output(location_type),
                                location,
                                list_accomodations.format(
                                    "\n\t- ".join([x["answer0"] for x in answer])
                                ),
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            f"No se han encontrado {accommodation_type_plural} "
                            f"en {get_location_type_output(location_type)}{location}."
                        )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                f"No he detectado ninguna localización de la que buscar su listado de {accommodation_type_plural}."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionAccommodationReservation(Action_Generic):
    def name(self):
        return "action_accommodation_reservation"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"))
        
        if( "entities" in tracker.__dict__['latest_message']):
            entities_data = tracker.__dict__['latest_message']['entities']
            if len(entities_data) >= 1:
                misc_all = ''
                for entity_raw in entities_data:
                    if entity_raw['entity'] == 'misc':
                        misc_all = misc_all + entity_raw['value'] + ' '
                if len(misc_all)>0:
                    misc = misc_all[0:-1]
                else:
                    misc = None

        if location is None and misc is not None:
            location = misc

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                if accommodation_type is None:
                    dispatcher.utter_message(accommodation_list_string())
                    return []

                answer = browser.search(
                    {
                        "intents": ["reservarAlojamiento", "tipoAlojamiento"],
                        "entities": [location, accommodation_type],
                    }
                )
                answer = filter_response(answer, location, exact=False)

                if len(answer) > 0:

                    for response in answer:
                        template = self.get_template(response)
                        dispatcher.utter_message(
                            template.format(accommodation_type, response["etiqueta"])
                        )
                else:
                    answer = browser.search(
                        {
                            "intents": ["reservarAlojamiento_telefono", "tipoAlojamiento"],
                            "entities": [location, accommodation_type],
                        }
                    )
                    answer = filter_response(answer, location, exact=False)

                    if len(answer) > 0:

                        maximo = 5
                        if len(answer)<5:
                            maximo = len(answer)

                        for response in answer[0:maximo]:
                            template = self.get_template_only_telephone(response)
                            dispatcher.utter_message(
                                template.format(accommodation_type, response["etiqueta"])
                            )

                    else:
                        dispatcher.utter_message(
                            f"No se han encontrado datos de como reservar en {accommodation_type} {location}."
                        )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para realizar una reserva."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

    @staticmethod
    def get_template(response):
        template = "Puedes reservar en {} {} "
        response_list = []
        if "answer0" in response:
            response_list.append(f"mandando un email a {response['answer0']}")
        if "answer1" in response:
            response_list.append(f"llamando al {response['answer1']}")
        if "answer2" in response:
            response_list.append(f"yendo a {response['answer2']}")

        template += response_list[0]

        try:
            if len(response_list) > 2:
                template += f", {response_list[1]} o {response_list[2]}"
            else:
                template += f" o {response_list[1]}"
        except:
            pass

        return f"{template}."

    @staticmethod
    def get_template_only_telephone(response):
        template = "Puedes reservar en {} {} "
        response_list = []
        if "answer0" in response:
            response_list.append(f"llamando al {response['answer0']}")
        if "answer1" in response:
            response_list.append(f"yendo a {response['answer2']}")

        template += response_list[0]

        try:
            if len(response_list) > 2:
                template += f", {response_list[1]} o {response_list[2]}"
            else:
                template += f" o {response_list[1]}"
        except:
            pass

        return f"{template}."

class ActionAccommodationCategory(Action_Generic):
    def name(self):
        return "action_accommodation_category"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))
        message = tracker.latest_message["text"]

        if location is not None:
            try:
                accomondation_type = get_accommodation_type(message)
                answer = browser.search(
                    {
                        "intents": ["categoriaAlojamiento", "tipoAlojamiento"],
                        "entities": [location, accomondation_type],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response("{} tiene {} estrellas.", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado información de la categoria de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún alojamiento válido para buscar su categoría."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionAccommodationCategoryHigher(Action_Generic):
    def name(self):
        return "action_accommodation_category_higher"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                entities = get_duckling_entities(message)
                print(entities)
                number = None
                for ent in entities:
                    if ent["entity"] == "number":
                        for ent in entities:
                            if ent["entity"] == "number":
                                duckValue = ent["duckValue"]
                                number = int(duckValue["value"])
                                break

                if number == None:
                    dispatcher.utter_message(
                        "No se ha detectado ningun número de categoría válido"
                    )
                    return []

                try:
                    if 5 < number < 1:
                        raise ValueError

                except ValueError:
                    dispatcher.utter_message(
                        "No se ha detectado ningun número de categoría válido. Los números deben ser entre 1 y 5."
                    )
                    return []

                answer = browser.search(
                    {
                        "intents": [
                            "alojamientoCiudad",
                            "tipoAlojamiento",
                            "categoria",
                        ],
                        "entities": [location, accommodation_type, number],
                    }
                )
                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:
                    list_hoteles = "{}"
                    if len(answer) > 5:
                        list_hoteles += f"\n\nPuede consultar el listado completo de hoteles en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "La lista de hoteles con categoria mayor de {} en {} es:\n\t- {}".format(
                            number,
                            location,
                            list_hoteles.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no he encontrado {accommodation_type} con categoria mayor de {str(number)} en {location}"
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún lugar válido para buscar la categoría de sus hoteles."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


"""class ActionAccommodationRoomsTerrace(Action_Generic):
    def name(self):
        return "action_accommodation_room_terrace"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": [
                            "habitacionesTerrazaHotel",
                            "tipoAlojamiento",
                            "tipoHabitacion",
                        ],
                        "entities": [location, "hotel"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:
                    dispatcher.utter_message(
                        "El número de habitaciones con terraza del hotel {} es {}".format(
                            location, answer[0]["answer0"]
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No hay habitaciones con terraza en el hotel {location}."
                    )

            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún hotel válido para buscar habitaciones con terraza."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionAccommodationServices(Action_Generic):
    def name(self):
        return "action_accommodation_services"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["serviciosHotel", "tipoAlojamiento"],
                        "entities": [location, "hotel"],
                    }
                )
                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:
                    list_services = "{}"
                    if len(answer) > 5:

                        list_services += f"\n\nPuede consultar la lista completa de servicios en el siguiente {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "Los servicios de {} son:\n\t- {}".format(
                            location,
                            list_services.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento no he encontrado información sobre otros servicios en el hotel {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún hotel válido para buscar los servicios que dispone."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


class ActionAccommodationNumber(Action_Generic):
    def name(self):
        return "action_accommodation_number"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]
        accommodation_type_plural = get_accommodation_type_plural(message)

        if location is not None:
            try:
                place_type = get_location_type(message)
                if place_type == "municipio":
                    accommodation_type = get_singular_or_plural(
                        accommodation_type_plural
                    )
                    answer = browser.search(
                        {
                            "intents": ["numeroAlojamiento", "tipoAlojamiento"],
                            "entities": [location, accommodation_type],
                        }
                    )

                    #answer = filter_response(answer, location)
                    if len(answer) > 0:
                        
                        answer[0]['etiqueta'] = location

                        dispatcher.utter_message(
                            build_virtuoso_response(
                                "En el municipio de {} hay {} "
                                + accommodation_type_plural,
                                answer,
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            f"Lo siento no he encontrado datos de cuantos {accommodation_type_plural} hay en {location}."
                        )
                else:
                    dispatcher.utter_message(
                        f"Lo siento solo dispongo de datos de número de {accommodation_type_plural} en municipios."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                f"No he detectado ningún municipio del que buscar {accommodation_type_plural}."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


"""class ActionAccommodationNumberRooms(Action_Generic):
    def name(self):
        return "action_accommodation_number_rooms"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))
        message = tracker.latest_message["text"]

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                answer = browser.search(
                    {
                        "intents": [
                            "habitacionesHotel",
                            "tipoAlojamiento",
                            "tipoHabitacion",
                        ],
                        "entities": [location, accommodation_type, "total"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response("En {} hay {} habitaciones.", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no sé cuantas habitaciones tiene el {accommodation_type} {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(f"No he detectado ningún alojamiento válido.")

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionAccommodationNumberRoomsBathroom(Action_Generic):
    def name(self):
        return "action_accommodation_number_rooms_bathroom"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))
        message = tracker.latest_message["text"]

        if location is not None:
            intent = "habitacionesBañoHotel"
            template = "En {} hay {} habitaciones con baño."
            if "sin" in message:
                intent = "habitacionessinBañoHotel"
                template = template.replace("con", "sin")

            try:
                answer = browser.search(
                    {
                        "intents": [intent, "tipoAlojamiento"],
                        "entities": [location, "hotel"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(build_virtuoso_response(template, answer))
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no tengo información del número de habitaciones con baño del hotel {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún hotel válido para buscar información de baños en las habitaciones."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionAccommodationNumberBeds(Action_Generic):
    def name(self):
        return "action_accommodation_number_beds"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["camasHotel", "tipoAlojamiento"],
                        "entities": [location, "hotel"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response("En {} hay {} camas", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no tengo información del número de camas del hotel {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún hotel válido para buscar número de camas."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


class ActionAccommodationLocation(Action_Generic):
    def name(self):
        return "action_accommodation_city"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]

        if location is not None:

            try:
                accommodation_type = get_accommodation_type(message)
                answer = browser.search(
                    {
                        "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
                        "entities": [location, accommodation_type],
                    }
                )

                answer = filter_response(answer, location, exact=False)

                if len(answer) > 0:
                    answer[0]["answer0"] = answer[0]["answer0"].split('/')[len(answer[0]["answer0"].split('/'))-1]
                    dispatcher.utter_message(
                        "{} está en {}.".format(
                            answer[0]["etiqueta"], answer[0]["answer0"]
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no sé donde está el {accommodation_type} {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(f"No he detectado ningún alojamiento válido.")

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionAccommodationsIn(Action_Generic):
    def name(self):
        return "action_accommodations_in"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        message = tracker.latest_message["text"]

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                if accommodation_type is None:
                    accommodation_type = "hotel"
                answer = browser.search(
                    {
                        "intents": ["alojamientoCiudad", "tipoAlojamiento"],
                        "entities": [location, accommodation_type],
                    }
                )
                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:
                    list_accomodations = "{}"
                    if len(answer) > 5:
                        list_accomodations += (
                            f"\n\nPuedes consultar el listado completo de "
                            f"{get_singular_or_plural(accommodation_type, get_plural=True)} "
                            f"en el siguiente {browser.url}."
                        )
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "En {} te puedes alojar en los siguientes {}\n\t- {}".format(
                            location,
                            get_singular_or_plural(accommodation_type, get_plural=True),
                            list_accomodations.format(
                                "\n\t- ".join([x["etiqueta"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no sé donde te puedes alojar en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar los alojamientos disponibles."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


"""class ActionAccommodationSeason(Action_Generic):
    def name(self):
        return "action_accommodation_season"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
        
        location = clean_input(tracker.get_slot("location"))
        message = tracker.latest_message["text"]

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                season_type = get_season(message)
                if season_type is None:
                    dispatcher.utter_message(
                        "No se ha detectado una temporada válida. Prueba con alta, media o baja."
                    )

                answer = browser.search(
                    {
                        "intents": [
                            "temporadaAlojamiento",
                            "tipoAlojamiento",
                            "tipoTemporada",
                        ],
                        "entities": [location, accommodation_type, season_type],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        "En {} es temporada {} desde {} hasta {}.".format(
                            answer[0]["etiqueta"],
                            season_type,
                            number_to_date(answer[0]["answer0"]),
                            number_to_date(answer[0]["answer1"]),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado datos de {location} sobre temporada {season_type}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar informacion de sus temporadas."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


class ActionAccommodationRoomsType(Action_Generic):
    def name(self):
        return "action_accommodation_rooms_type"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))
        organization = clean_input(tracker.get_slot("organization"))
        message = tracker.latest_message["text"]
        accommodation_type = get_accommodation_type(message)

        ''' Informacion añadida al código '''

        if location is None and organization is not None:
            location = organization

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

        if location is not None:
            try:
                room_type = get_room_type(message)
                entities = get_duckling_entities(message)
                if room_type is None:
                    number = None
                    for ent in entities:
                        if ent["entity"] == "number":
                            duckValue = ent["duckValue"]
                            number = int(duckValue["value"])
                            break

                    if number == 4:
                        room_type = "cuadruple"
                        room = "cuadruples"
                    elif number == 3:
                        room_type = "triple"
                        room = "triples"
                    elif number == 2:
                        room_type = "doble"
                        room = "dobles"
                    elif number == 1:
                        room_type = "sencilla"
                        room = "sencillas"
                    else:
                        dispatcher.utter_message(
                            "No se ha detectado un tipo un habitación válido. Prueba con sencillas, dobles, triples, cuádruples o suits."
                        )
                        return []
                if room_type in ["triple","triples"]:
                    room = "triples"
                    room_type = "triple"
                elif room_type in ["cuadruple","cuadruples"]:
                    room_type = "cuadruple"
                    room = "cuádruples"
                elif room_type in ["doble","dobles"]:
                    room = "dobles"
                    room_type = "doble"
                elif room_type in ["sencilla","sencillas"]:
                    room = "sencillas"
                    room_type = "sencilla"
                elif room_type in ["suit","suits"]:
                    room = "suits"
                    room_type = "suit"

                answer = browser.search(
                    {
                        "intents": [
                            "habitacionesHotel",
                            "tipoAlojamiento",
                            "tipoHabitacion",
                        ],
                        "entities": [location, accommodation_type, room_type],
                    }
                )
                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    for x in answer:
                        dispatcher.utter_message(
                            "En {} {} hay {} habitaciones {}.".format(
                                accommodation_type, x["etiqueta"], x["answer0"], room
                            )
                        )
                else:
                    dispatcher.utter_message(
                        f"No se han encontrado habitaciones {room_type} en {accommodation_type} {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún alojamiento del que buscar habitaciones."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


"""class ActionApartmentsRuralHouse(Action_Generic):
    def name(self):
        return "action_apartments_rural_house"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["apartamentosCasaRural", "tipoAlojamiento"],
                        "entities": [location, "casa rural"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response("{} tiene {} apartamentos.", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no tengo información de cuantos apartamentos tiene la casa rural {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna casa rural de la que buscar los apartamentos."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionApartmentsRooms(Action_Generic):
    def name(self):
        return "action_apartments_rooms"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))
        message = tracker.latest_message["text"]

        if location is not None:
            try:
                if "sencillas" in message:
                    kind = "sencillas"
                    intent = "habitacionesSencillasCasaRural"
                elif "dobles" in message:
                    kind = "dobles"
                    intent = "habitacionesDoblesCasaRural"
                else:
                    dispatcher.utter_message(
                        "No se ha detectado ningún tipo de habitación. Prueba incluyendo sencillas o dobles en el mensaje."
                    )
                    events.extend([ SlotSet("location", None), SlotSet("number", None)])
                    return events

                answer = browser.search(
                    {
                        "intents": [intent, "tipoAlojamiento"],
                        "entities": [location, "casa rural"],
                    }
                )
                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:
                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "{} tiene {} habitaciones " + kind+".", answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no sé qué tipos de habitaciones tiene la casa rural {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message("No he detectado ninguna casa rural válida.")

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionAccommodationSize(Action_Generic):
    def name(self):
        return "action_accommodation_size"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        message = tracker.latest_message["text"]
        location = clean_input(tracker.get_slot("location"))
        accommodation_type = get_accommodation_type(message)

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["plazasAlojamiento", "tipoAlojamiento"],
                        "entities": [location, accommodation_type],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:
                    for x in answer:
                        dispatcher.utter_message(
                            f"{get_accommodation_type_output(accommodation_type, True)} {x['etiqueta']} tiene {x['answer0']} plazas."
                        )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no sé cuantas plazas tiene {accommodation_type} {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún alojamiento para buscar el número de plazas que tiene."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionBungalowsCamping(Action_Generic):
    def name(self):
        return "action_bungalows_camping"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["bungalowsCamping", "tipoAlojamiento"],
                        "entities": [location, "camping"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response("{} tiene {} bungalows.", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento pero no sé cuantos bungalows tiene el camping {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar bungalows."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionCaravansCamping(Action_Generic):
    def name(self):
        return "action_caravans_camping"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["caravanasCamping", "tipoAlojamiento"],
                        "entities": [location, "camping"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response(
                            "{} tiene {} plazas para caravanas.", answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento no he encontrado información sobre cuantas plazas para caravanas tiene el camping {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún camping válido para buscar sus plazas para caravanas."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


"""class ActionPlotsCamping(Action_Generic):
    def name(self):
        return "action_plots_camping"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(tracker.get_slot("location"))

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["parcelasCamping", "tipoAlojamiento"],
                        "entities": [location, "camping"],
                    }
                )

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    dispatcher.utter_message(
                        build_virtuoso_response("{} tiene {} parcelas.", answer)
                    )
                else:
                    dispatcher.utter_message(
                        f"Lo siento no he encontrado información sobre cuantas parcelas tiene el camping {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún camping válido para buscar parcelas."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""


class ActionTravelAgencyInfo(Action_Generic):
    def name(self):
        return "action_travel_agency_info"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        intent = tracker.latest_message.get("intent").get("name")
        location = clean_input(tracker.get_slot("location"))
        if location is None:
            location = clean_input(tracker.get_slot("misc"))

        if location is not None:
            try:
                if intent is not None:
                    intent = intent.lower()
                else:
                    dispatcher.utter_message(
                        "Información solicitada no reconocida para la agencia de viajes."
                    )
                    events.extend([ SlotSet("location", None), SlotSet("number", None)])
                    return events

                intent, template, errmsg = self.get_intent_template_and_error(
                    intent, location
                )
                # TODO: Check if intent is not None and dispatch errmsgs
                answer = browser.search({"intents": [intent], "entities": [location]})

                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    if intent == "direccionAgenciaViajes":
                        if "answer2" in answer[0]:
                            template += f", {answer[0]['answer2']}"
                        if "answer1" in answer[0]:
                            template += f" ({answer[0]['answer1']})"

                        template += "."

                    dispatcher.utter_message(
                        template.format(answer[0]["etiqueta"], answer[0]["answer0"])
                    )
                else:
                    dispatcher.utter_message(errmsg)
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningúna agencia de viajes válido para buscar su información."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

    @staticmethod
    def get_intent_template_and_error(intent, location):
        if "phone" in intent:
            return (
                "telefonoAgenciaViajes",
                "El teléfono de la agencia de viajes {} es {}.",
                f"Lo siento pero no he encontrado el teléfono de la agencia de viajes {location}",
            )
        elif "email" in intent or "contact" in intent:
            return (
                "emailAgenciaViajes",
                "El email de la agencia de viajes {} es {}.",
                f"Lo siento pero no he encontrado el email de la agencia de viajes {location}",
            )
        elif "web" in intent:
            return (
                "webAgenciaViajes",
                "La web de la agencia de viajes {} es {}.",
                f"Lo siento pero no he encontrado la web de la agencia de viajes {location}",
            )
        elif "address" in intent:
            return (
                "direccionAgenciaViajes",
                "La dirección de la agencia de viajes {} es {}",
                f"Lo siento pero no he encontrado la dirección de la agencia de viajes {location}",
            )


        return None, "", ""

"""class ActionTravelAgencyList(Action_Generic):
    def name(self):
        return "action_travel_agency_list"

    def run(self, dispatcher, tracker, domain):
        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        if location is None:
            location = clean_input(tracker.get_slot("misc"))

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["listAgenciaViajes"], "entities": [location]}
                )
                answer = filter_response(answer, location, exact=False)
                if len(answer) > 0:

                    answer2 = []
                    for row in answer:
                        etiqueta = row['etiqueta']
                        if eliminaTildes(etiqueta.upper()) == eliminaTildes(location.upper()):
                            answer2.append(row)

                    if len(answer2) > 0:
                        answer = answer2

                    list_agencias = "{}"
                    if len(answer) > 5:
                        list_agencias += f"\n\nPuedes consultar el listado completo de agencias de viaje en el siguiente enlace {browser.url}"
                        answer = answer[:5]

                    dispatcher.utter_message(
                        "En {} hay las siguientes agencias de viaje \n\t- {}".format(
                            location,
                            list_agencias.format(
                                "\n\t- ".join([x["answer0"] for x in answer])
                            ),
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he se cuantas agencias de viaje hay en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar agencias de viajes."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events"""
