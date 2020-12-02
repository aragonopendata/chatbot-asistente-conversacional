'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from actions_module.transport.utils import *
from urllib.error import URLError


from actions_module.Action_Generic import Action_Generic 


from actions_utils import build_virtuoso_response, get_entities


class ActionBusLocation(Action_Generic):
    def name(self):
        return "action_transport_bus_location"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["autobus_location"], "entities": [location]}
                )
                # print(answer)
                if len(answer) > 0:
                    link = None
                    # if len(answer) > 5:
                    #    answer = answer[0:5]
                    #    link = browser.url
                    #    print(link)
                    answer.sort(key=lambda x: x["answer2"])
                    list_response = "\n\t- ".join([x["answer2"] for x in answer])
                    if link is not None:
                        list_answer = "{} \n\n Puedes consultar el listado completo de autobuses en siguiente enlace {}".format(
                            list_response, link
                        )
                    else:
                        list_answer = list_response

                    dispatcher.utter_message(
                        "Los autobuses que se pasan por {} son:\n\t- {}".format(
                            location, list_answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado autobuses que salgan, pasen o lleguen a {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna localización de la que proporcionar sus autobuses."
            )

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]


class ActionBusTimetable(Action_Generic):
    def name(self):
        return "action_transport_bus_timetable"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        entities = tracker.latest_message.get("entities", [])
        # print(entities)
        if len(entities) > 1:
            route = []
            for entity in entities:
                if entity['confidence'] >= 1:
                    route.append(entity)
            orig = getOriginValue(route[0]["value"])
            dst = getOriginValue(route[1]["value"])
            try:
                answer = browser.search(
                    {
                        "intents": ["horarioautobuses_desde", "horarioautobuses_hasta"],
                        "entities": [orig, dst],
                    }
                )

                # print(answer)

                if len(answer) > 0:
                    answer.sort(key=lambda x: x["answer6"])
                    link = None
                    # if len(answer) > 5:
                    #    answer = answer[0:5]
                    #    link = browser.url
                    #    print (link)

                    mensaje = ""
                    if len(answer) == 1:
                        mensaje = "El horario del autobús de {} a {} es {} - Línea {} {} ".format(
                            orig,
                            dst,
                            answer[0]["answer6"],
                            answer[0]["answer7"],
                            answer[0]["answer8"],
                        )
                    else:
                        list_response = ""
                        for x in answer:
                            list_response += "\n\t- {} - Línea {} {}".format(
                                x["answer6"], x["answer7"], x["answer8"]
                            )
                        mensaje = "Los horarios de los autobuses que van de {} a {} son:\n\t- {}".format(
                            orig, dst, list_response
                        )

                    if link is not None:
                        list_answer = "{} \n\n Puedes consultar el listado completo de autobuses en siguiente enlace {}".format(
                            mensaje, link
                        )
                    else:
                        list_answer = mensaje

                    dispatcher.utter_message(mensaje)
                else:
                    dispatcher.utter_message(
                        f"No he encontrado autobuses desde {orig} hasta {dst}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado 2 localizacines para mostrar los horarios de autobús."
            )

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]


class ActionBusCompany(Action_Generic):
    def name(self):
        return "action_transport_bus_company"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["typebuses"], "entities": [location]}
                )
                # print(answer)
                if len(answer) > 0:
                    if str(answer[0]) != '{}':
                        answer.sort(key=lambda x: x["answer2"])
                        link = None
                        # if len(answer) > 5:
                        #    answer = answer[0:5]
                        #    link = browser.url
                        #    print(link)
                        companies = []
                        for x in answer:
                            if x["answer2"].strip() != "":
                                company = x["answer2"].strip()
                                if company not in companies:
                                    companies.append(company)

                        companies = sorted(companies)

                        list_response = "\n\t- ".join([x for x in companies])

                        if link is not None:
                            list_answer = "{} \n\n Puedes consultar el listado completo de las empresas de transporte {}".format(
                                list_response, link
                            )
                        else:
                            list_answer = list_response

                        dispatcher.utter_message(
                            "Las empresas de autobuses que prestan servicio de transporte en {} son:\n\t- {}".format(
                                location, list_answer
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            f"No he encontrado autobuses que salgan, pasen o lleguen a {location}."
                        )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado autobuses que salgan, pasen o lleguen a {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado ninguna localización de la que proporcionar sus autobuses."
            )

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]