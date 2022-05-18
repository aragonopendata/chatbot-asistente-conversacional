from actions_module.transport.utils import *
from urllib.error import URLError
from collections import Counter
import math


from actions_module.Action_Generic import Action_Generic 

class ActionTransportRoadList(Action_Generic):
    def name(self):
        return "action_transport_road_list"

    def run(self, dispatcher, tracker, domain):

        """Returns a list of roads of a concrete town or county.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        print(location)
        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoads"], "entities": [location]}
                )
                print(answer)
                if len(answer) > 0:
                    roads = []
                    for x in answer:
                        try:
                            if (
                                x["answer1"].strip() != ""
                                and x["answer0"].strip() != ""
                            ):
                                description = x["answer1"].strip()
                                road = "{}  {}".format(
                                    x["answer0"].strip(), x["answer1"].strip()
                                )
                                if road not in roads:
                                    roads.append(road)
                        except:
                            pass

                    roads = sorted(roads)

                    link = None

                    if len(roads) > 5:
                        roads = roads[0:5]

                    list_response = "\n\t- ".join([x for x in roads])
                    if link is not None:
                        list_answer = "{} \n\n Puedes consultar el listado completo de carreteras en siguiente enlace {}".format(
                            list_response, link
                        )
                    else:
                        list_answer = list_response

                    dispatcher.utter_message(
                        "Las carreteras de la provincia de {} son:\n\t- {}".format(
                            location, list_answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado carreteras en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna provincia de la que proporcionar sus carreteras."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadSpeed(Action_Generic):
    def name(self):
        return "action_transport_road_speed"

    def run(self, dispatcher, tracker, domain):

        """Returns the maximum of a concrete road.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadSpeed"], "entities": [road_name]}
                )
                # print(answer)
                if len(answer) > 0:
                    answer.sort(key=lambda x: float(x["answer2"]), reverse=True)

                    dispatcher.utter_message(
                        "La velocidad máxima de la carretera {} es {} kilómetros por hora.".format(
                            road_name, math.trunc(float(answer[0]["answer2"]))
                        )
                    )

                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos de la carretera {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna carretera de la que proporcionar su velocidad."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadType(Action_Generic):
    def name(self):
        return "action_transport_road_type"

    def run(self, dispatcher, tracker, domain):

        """Returns the type of the road

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadType"], "entities": [road_name]}
                )
                # print(answer)

                if len(answer) > 0:

                    description = ""
                    description_counts = Counter(d["answer1"] for d in answer)

                    if len(description_counts.keys()) > 0:
                        for key in description_counts.keys():
                            if key.strip() != "":
                                description += "\n\t- " + get_road_type(key)

                    if description == "":
                        dispatcher.utter_message(
                            "No he encontrado tipo en la carretera {}.".format(
                                road_name
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            "La carretera {} es:{}".format(road_name, description)
                        )

                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos de la carretera {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna carretera de la que proporcionar sus datos."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadDescription(Action_Generic):
    def name(self):
        return "action_transport_road_description"

    def run(self, dispatcher, tracker, domain):

        """Returns all the information, or description, about a concrete road.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadDescription"], "entities": [road_name]}
                )
                print(answer)
                if len(answer) > 0:

                    description = "desconocida"

                    for x in answer:
                        if x["answer1"].strip() != "":
                            description = x["answer1"].strip()
                            break

                    dispatcher.utter_message(
                        "La descripción de la carretera {} es {}.".format(
                            road_name, description
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos de la carretera {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna carretera de la que proporcionar su descripción."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadLocation(Action_Generic):
    def name(self):
        return "action_transport_road_location"

    def run(self, dispatcher, tracker, domain):

        """Returns the location of a concrete road.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is None:
            location = 'Aragon'

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadLocation"], "entities": [location]}
                )

                if len(answer) > 0:
                    roads = []
                    for x in answer:
                        if x["answer1"].strip() != "" and x["answer0"].strip() != "":
                            description = x["answer1"].strip()
                            road = "{} : {}".format(
                                x["answer0"].strip(), x["answer1"].strip()
                            )
                            if road not in roads:
                                roads.append(road)

                    roads = sorted(roads)
                    list_response = "\n\t- ".join([x for x in roads])
                    dispatcher.utter_message(
                        "Las carreteras que llegan a {} son:\n\t- {}".format(
                            location, list_response
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado carreteras en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna localización de la que proporcionar sus carreteras de acceso."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadZones(Action_Generic):
    def name(self):
        return "action_transport_road_zones"

    def run(self, dispatcher, tracker, domain):

        """Returns the zone (public, private or etc) of a concrte road.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadZones"], "entities": [road_name]}
                )
                print(answer)
                if len(answer) > 0:
                    link = None
                    if len(answer) > 5:
                        answer = answer[0:5]
                        link = browser.url
                        print(link)

                    list_response = "\n\t- ".join([x["answer0"] for x in answer])
                    if link is not None:
                        list_answer = "{} \n\n Puedes consultar el listado completo de zonas en siguiente enlace {}".format(
                            list_response, link
                        )
                    else:
                        list_answer = list_response

                    dispatcher.utter_message(
                        "Los zonas cercanas a la carretera {} son:\n\t- {}".format(
                            road_name, list_answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado zonas en la carretera {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna carretera de la que proporcionar sus zonas."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadBridge(Action_Generic):
    def name(self):
        return "action_transport_road_bridge"

    def run(self, dispatcher, tracker, domain):

        """Returns a list of bridges of a road.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadBridges"], "entities": [road_name]}
                )
                print(answer)
                if len(answer) > 0:
                    link = None

                    answer.sort(key=lambda x: x["answer1"])

                    # if len(answer) > 5:
                    #    answer = answer[0:5]
                    #   link = browser.url
                    #   print(link)

                    list_response = "\n\t- ".join([x["answer0"] for x in answer])
                    if link is not None:
                        list_answer = "{} \n\n Puedes consultar el listado completo de puentes en siguiente enlace {}".format(
                            list_response, link
                        )
                    else:
                        list_answer = list_response

                    dispatcher.utter_message(
                        "Los puentes de la carretera {} en son:\n\t- {}".format(
                            road_name, list_answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado puentes en la carretera {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna carretera de la que proporcionar sus puentes."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadBridgeLocation(Action_Generic):
    def name(self):
        return "action_transport_road_bridge_location"

    def run(self, dispatcher, tracker, domain):

        """Returns the bridges of a location.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message)  and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is not None:

            entities = tracker.__dict__['latest_message']['entities']

            provincia = ""
            for entity in entities:
                if entity['entity'] == 'location':
                    if entity['value'] != location:
                        provincia = entity['value']

            if provincia == "":
                location = "Aragon/" + location
            else:
                location = provincia + "/" + location

            try:
                answer = browser.search(
                    {"intents": ["transportBridgesLocation"], "entities": [location]}
                )
                print(answer)
                if len(answer) > 0:
                    try:
                        answer.sort(key=lambda x: x["answer2"])  # ERROR no llega answer2
                    except:
                        pass
                    list_answer = "\n\t- ".join([x["answer0"] for x in answer])

                    tipo = location.split('/')[0]
                    ubicacion = location.split('/')[1]

                    if ubicacion.upper() == "ARAGON" or ubicacion.upper() == "ARAGÓN":
                        dispatcher.utter_message(
                            "Los puentes que hay en {} son:\n\t- {}".format(
                                ubicacion, list_answer
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            "Los puentes que hay en la {} de {} son:\n\t- {}".format(
                                tipo, ubicacion, list_answer
                            )
                        )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado puentes en carreteras que pasen por la localidad de {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna población de la que proporcionar sus puentes."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadBridgeKm(Action_Generic):
    def name(self):
        return "action_transport_road_bridge_km"

    def run(self, dispatcher, tracker, domain):

        """Returns a list of bridges with its km position.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadKmBridge"], "entities": [location]}
                )
                print(answer)
                if len(answer) > 0:
                    answer.sort(key=lambda x: x["answer0"])

                    mensaje = ""
                    if len(answer) == 1:
                        kms = "%.3f" % float(answer[0]["answer0"])
                        mensaje = "El puente de {} se encuentra en el punto kilométrico {} de la carretera {}".format(
                            location, kms, answer[0]["answer1"]
                        )
                    else:
                        list_response = ""
                        for x in answer:
                            kms = "%.3f" % float(x["answer0"])
                            list_response += "\n\t- {} de la carretera {}".format(
                                kms, x["answer1"]
                            )
                        mensaje = "Los puentes de {} se encuentran en los puntos kilométricos:{}".format(
                            location, list_response
                        )

                    dispatcher.utter_message(mensaje)
                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos del puente {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ningún puente del que proporcionar su situación."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadBridgesKms(Action_Generic):
    def name(self):
        return "action_transport_road_brigdes_roads_km"

    def run(self, dispatcher, tracker, domain):

        """Returns a list of bridges with its km position.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportBridgesKms"], "entities": [road_name]}
                )
                print(answer)
                if len(answer) > 0:
                    answer.sort(key=lambda x: x["answer1"])
                    list_answer = "\n\t- ".join([x["answer1"] for x in answer])

                    dispatcher.utter_message(
                        "Los puentes de la carretera {} están en los puntos kilométricos:\n\t- {}".format(
                            road_name, list_answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado puentes en {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna carrtera de la que proporcionar sus puentes por km."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadBridgesLocations(Action_Generic):
    def name(self):
        return "action_transport_road_brigdes_locations"

    def run(self, dispatcher, tracker, domain):

        """Returns a list of locations where there is a any bridge in a location of a concrete road.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)
		
        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoBridLocations"], "entities": [road_name]}
                )
                print(answer)
                if len(answer) > 0:
                    responseSet = []

                    for x in answer:
                        responseSet.append(x["answer0"].strip())

                    responseSet = sorted(set(responseSet))
                    list_answer = ""
                    for r in responseSet:
                        list_answer += "\n\t- " + r

                    dispatcher.utter_message(
                        "Los puentes de la carretera {} están en las siguientes localidades:{}".format(
                            road_name, list_answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado puentes en {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna carrtera de la que proporcionar sus puentes por localidad."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events


class ActionTransportRoadLength(Action_Generic):
    def name(self):
        return "action_transport_road_length"

    def run(self, dispatcher, tracker, domain):

        """Returns a list of distances of a road.

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message) and events

            """

        events = super().run(dispatcher, tracker, domain)

        road_name = get_road_name(
            tracker.get_slot("misc"),
            tracker.get_slot("location"),
            tracker.latest_message["text"],
        )

        if tracker.get_slot("road_names") is not None:
            road_name = tracker.get_slot("road_names").upper()

        if road_name.find('-')==-1:
            entities = tracker.__dict__['latest_message']['entities']
            for entity in entities:
                value = entity['value']
                if value.find('-'):
                    road_name = entity['value'].upper()
                    break

        orig = None
        dst = None

        if road_name.find('-')==-1:
            road_name = None

        if road_name == None:
            try:
                entities = get_entities(tracker.latest_message["text"], duckling=False)
            except Exception as e:
                entities = None
            print(entities)
            orig = None
            dst = None
            if entities is not None:
                for ent in entities:
                    if ent["entity"] == "location" and ent["depth"] == 0:
                        value = clean_input(
                            ent["value"],
                            [
                                "carretera de",
                                "población de",
                                "localidad de",
                                "ciudad de",
                                "carretera",
                            ],
                        )
                        if value != None:
                            if orig == None:
                                orig = value.strip()
                            elif orig != value.strip():
                                dst = value.strip()
                                break

        if orig != None and dst == None:
            road_name = orig

        if orig != None and dst != None:
            try:
                answer = browser.search(
                    {
                        "intents": [
                            "transportRoadLengthOrigen",
                            "transportRoadLengthDestino",
                        ],
                        "entities": [orig, dst],
                    }
                )

                if len(answer) > 0:
                    suma = 0.0
                    for x in answer:
                        suma += float(x["answer1"])

                    suma = suma / 1000

                    dispatcher.utter_message(
                        "La longitud de la carretera entre {} y {} es de {:.2f} kilómetros".format(
                            orig, dst, suma
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos de la carretera entre {orig} y {dst}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")
        elif road_name != None:
            try:
                answer = browser.search(
                    {"intents": ["transportRoadNameLength"], "entities": [road_name]}
                )
                print(answer)
                if len(answer) > 0:
                    if float(answer[0]['answer1']) != 0:
                        dispatcher.utter_message(
                            "La carretera {} tiene {} kilómetros de longitud.".format(
                                road_name, answer[0]["answer1"]
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            f"Perdona no he encontrado datos de la carretera {road_name}."
                        )
                else:
                    dispatcher.utter_message(
                        f"Perdona no he encontrado datos de la carretera {road_name}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message("No he podido conectarme a la BBDD")

        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado una carretera para proporcionar su longitud."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None),SlotSet("misc", None)])
        return events