"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
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
    """Class which answer to questions about general information about
        acommodation: address, phone, fax, email
       This class inherits from Action_Generic
    """
    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodation_info"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. Identify entities and intentions related
            with accomodation and send the information to the user

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

            Complete answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        # Extract the intention and the Question
        intent = tracker.latest_message.get("intent").get("name")
        message = tracker.latest_message["text"]

        # Try to find a location in the question send y the user
        try:
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        # Try to find the name of a accomodation place
        if location is None:
            location = tracker.get_slot("accomodation_name")

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                if accommodation_type is None:
                    dispatcher.utter_message(accommodation_list_string())
                    return []

                # Establish the query to extract information from Opne Data
                intent, template = self.get_intent_and_template(intent=intent)
                if intent is None:
                    dispatcher.utter_message(
                        "Información de alojamiento solicitada no reconocida."
                    )
                    events.extend([ SlotSet("location", None), SlotSet("number", None)])
                    return events

                # Compose the anwser to the user
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
                        equal = 0
                        for row in answer:
                            etiqueta = row['etiqueta']
                            if etiqueta.upper() == location.upper():
                                equal = equal + 1
                                if intent == "direccionAlojamiento":
                                    template = self.update_template(template, row)

                                dispatcher.utter_message(
                                    template.format(
                                        get_accommodation_type_output(accommodation_type),
                                        row["etiqueta"],
                                        row["answer0"],
                                    ) + "."
                                )
                        if equal == 0:
                            dispatcher.utter_message(
                                f"No he encontrado la información {get_accommodation_type_output(accommodation_type)} {location}."
                            )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado la información {get_accommodation_type_output(accommodation_type)} {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                f"No he detectado ningún alojamiento sobre el que buscar su dirección."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("accomodation_name", None)])
        return events

    @staticmethod
    def get_intent_and_template(intent):
        """ Depending on the question. Establish the template to query and the format of the answer

        Parameters
        ----------
        intent: json
            Detected intention

        Returns
        -------
        String, String

            Template to use to identify the query to execute
            Template for the answer
        """
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
        """ Update the template to use in the answer

        Parameters
        ----------
        template: json
        answer; String

        Returns
        -------
        String

            New template
        """
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
    """Class which answer to questions about list of accomodation in a specific areas
       This class inherits from Action_Generic
    """

    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodation_list"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class. Identify entities and intentions to search
            the list of accomodations and send it to the user

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

            Complete answer to the user
        """
        events = super().run(dispatcher, tracker, domain)

        #Try to find the location
        try:
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("accomodation_name")

        # Identify the question and the type of accomodation to search
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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                f"No he detectado ninguna localización de la que buscar su listado de {accommodation_type_plural}."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionAccommodationReservation(Action_Generic):
    """Class which answer to questions about reservations
       This class inherits from Action_Generic
    """

    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodation_reservation"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Identify the way to make a reservation in each accomodation

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

        message = tracker.latest_message["text"]

        try:
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

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

        if location is None:
            try:
                location = tracker.get_slot("accomodation_name")
            except:
                pass

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para realizar una reserva."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

    @staticmethod
    def get_template(response):
        """ Depending on the question. Establish the template to query and the format of the answer

        Parameters
        ----------
        response: json
            Detected intention

        Returns
        -------
        String

            Template for the answer
        """
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
        """ Depending on the question. Establish the template to query and the format of the answer
            This time only takes into account the phone of the accomodation

        Parameters
        ----------
        response: json
            Detected intention

        Returns
        -------
        String

            Template for the answer
        """
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
    """Class which answer to questions about accomadatios category
       This class inherits from Action_Generic
    """

    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodation_category"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Identify the category of a set of accomodations

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
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("accomodation_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún alojamiento válido para buscar su categoría."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionAccommodationCategoryHigher(Action_Generic):
    """Class which answer to questions about accomodations of a specific category
       This class inherits from Action_Generic
    """

    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodation_category_higher"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Identify which accomodations have a specific category

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
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("accomodation_name")

        message = tracker.latest_message["text"]

        if location is not None:
            try:
                accommodation_type = get_accommodation_type(message)
                try:
                    entities = get_duckling_entities(message)
                except Exception as e:
                    entities = None
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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún lugar válido para buscar la categoría de sus hoteles."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

class ActionAccommodationNumber(Action_Generic):
    """Class which answer to questions about the number of accomadation in a specific place
       This class inherits from Action_Generic
    """
    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodation_number"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Identify the number of accomodations in a specific place

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
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("accomodation_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                f"No he detectado ningún municipio del que buscar {accommodation_type_plural}."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionAccommodationLocation(Action_Generic):
    """Class which answer to questions about accomodations in specific place
       This class inherits from Action_Generic
    """
    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodation_city"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Identify accomodations in a specific place

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
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("accomodation_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(f"No he detectado ningún alojamiento válido.")

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionAccommodationsIn(Action_Generic):
    """Class which answer to questions about accomodations in specific place of a specific type
       This class inherits from Action_Generic
    """
    def name(self):
        """ Property class. Return the name of the class"""
        return "action_accommodations_in"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Identify accomodations in a specific place of a specific type

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
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        if location is None:
            location = tracker.get_slot("accomodation_name")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningún sitio válido para buscar los alojamientos disponibles."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionTravelAgencyInfo(Action_Generic):
    """Class which answer to questions about general information of travel agencies
       This class inherits from Action_Generic
    """

    def name(self):
        """ Property class. Return the name of the class"""
        return "action_travel_agency_info"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            General Information about travel agencies

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

        intent = tracker.latest_message.get("intent").get("name")

        try:
            location = clean_input(tracker.get_slot("location"), invalid_words=None)
        except:
            location = None

        if location is None:
            try:
                location = tracker.get_slot("accomodation_name")
            except:
                location = tracker.get_slot("misc")

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
                dispatcher.utter_message("No he podido conectar a la BBDD")
        else:
            dispatcher.utter_message(
                "No he detectado ningúna agencia de viajes válido para buscar su información."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events

    @staticmethod
    def get_intent_template_and_error(intent, location):
        """ Depending on the question. Establish the template to query and the format of the answer

        Parameters
        ----------
        intent: json
            Detected intention

        Returns
        -------
        String

            Template to format the answer about general information of travel agencies
        """
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

