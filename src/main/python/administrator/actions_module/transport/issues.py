'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from actions_module.transport import *
from urllib.error import URLError


from actions_module.Action_Generic import Action_Generic 


class ActionTransportIssues(Action_Generic):
    def name(self):
        return "action_transport_issues"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        print(location)
        if location is None:
            location = "Aragon"

        try:
            answer = browser.search(
                {"intents": ["transportIssues"], "entities": [location]}
            )
            print(answer)
            if len(answer) > 0:
                link = None
                if len(answer) > 5:
                    answer = answer[0:5]
                    link = "http://www.carreterasdearagon.es"

                list_response = ""
                for x in answer:
                    list_response += "\n\t- {} en la carretera {} desde {} ".format(
                        x["answer1"].strip(), x["answer0"], x["answer2"]
                    )
                    # list_response += "\n\t- {} - {} ".format(x["answer0"], x["answer1"])

                if link is not None:
                    list_answer = "{} \n\n Puedes consultar el listado de incidencias en el siguiente enlace {}".format(
                        list_response, link
                    )
                else:
                    list_answer = list_response

                dispatcher.utter_message(
                    "Las incidencias de tráfico en {} son:{}".format(
                        location, list_answer
                    )
                )
            else:
                dispatcher.utter_message(
                    f"No he encontrado incidencias de tráfico en {location}."
                )
        except (URLError, Exception) as ex:
            dispatcher.utter_message(str(ex))

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]


class ActionTransportIssueType(Action_Generic):
    def name(self):
        return "action_transport_issue_type"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is None:
            location = "Aragon"

        try:
            answer = browser.search(
                {"intents": ["transportIssueType"], "entities": [location]}
            )
            print(answer)
            if len(answer) > 0:
                link = None
                if len(answer) > 5:
                    answer = answer[0:5]
                    link = "http://www.carreterasdearagon.es"
                    # print(link)

                list_response = ""
                for x in answer:
                    list_response += "\n\t- {}".format(x["answer0"])

                if link is not None:
                    list_answer = "{} \n\n Puedes consultar el listado de tipos de incidencias en el siguiente enlace {}".format(
                        list_response, link
                    )
                else:
                    list_answer = list_response

                dispatcher.utter_message(
                    "Los tipos de incidencias de tráfico en {} son:{}".format(
                        location, list_answer
                    )
                )
            else:
                dispatcher.utter_message(
                    f"No he encontrado incidencias de tráfico en {location}."
                )
        except (URLError, Exception) as ex:
            print(ex)
            dispatcher.utter_message(str(ex))

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]


class ActionTransportIssueWhere(Action_Generic):
    def name(self):
        return "action_transport_issue_where"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is None:
            location = 'Aragon'

        if location is not None:
            try:
                answer = browser.search(
                    {"intents": ["transportIssueWhere"], "entities": [location]}
                )
                print(answer)
                if len(answer) > 0:
                    link = None
                    if len(answer) > 5:
                        answer = answer[0:5]
                        link = "http://www.carreterasdearagon.es"
                        # print(link)

                    list_response = ""
                    for x in answer:
                        if 'etiqueta3' in x:
                            list_response += "\n\t- Tramo {} en la carretera {} en el {} existe la limitacion de {}".format(
                                x["answer1"], x["answer0"],x["answer3"], x["answer2"]
                            )
                        else:
                            list_response += "\n\t- Tramo {} en la carretera {}".format(
                                x["answer1"], x["answer0"]
                            )
                    if link is not None:
                        list_answer = "{} \n\n Puedes consultar el listado completo de incidencias en el siguiente enlace  {}".format(
                            list_response, link
                        )
                    else:
                        list_answer = list_response

                    dispatcher.utter_message(
                        "Las incidencias de tráfico de la localidad de {} se encuentran en :{}".format(
                            location, list_answer
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No he encontrado incidencias de tráfico en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado población en la que buscar los tipos de incidencias de tráfico."
            )

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]


class ActionTransportIssueReasons(Action_Generic):
    def name(self):
        return "action_transport_issue_reasons"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")

        if location is None:
            location = "Aragon"
        try:
            answer = browser.search(
                {
                    "intents": ["tipoIncidencia", "transportIssueReason"],
                    "entities": ["", location],
                }
            )
            print(answer)
            if len(answer) > 0:
                link = None
                if len(answer) > 5:
                    answer = answer[0:5]
                    link = "http://www.carreterasdearagon.es"
                    # print(link)

                responseSet = []
                list_response = ""
                for x in answer:
                    try:
                        list_response += "\n\t -{}  en el tramo {} de la carretera {}".format(
                            x["answer2"], x["answer3"], x["answer0"]
                        )
                    except:
                        pass

                if link is not None:
                    list_answer = " {} \n\n Puedes consultar el listado completo de incidencias en el siguiente enlace  {}".format(
                        list_response, link
                    )
                else:
                    list_answer = list_response

                dispatcher.utter_message(
                    "Las causas de las incidencias de tráfico en {} son :{}".format(
                        location, list_answer
                    )
                )
            else:
                dispatcher.utter_message(
                    f"No he encontrado incidencias de tráfico en {location} para informar de sus causas."
                )
        except (URLError, Exception) as ex:
            dispatcher.utter_message(str(ex))

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]


class ActionTransportIssueByReason(Action_Generic):
    def name(self):
        return "action_transport_issue_by_reason"

    def run(self, dispatcher, tracker, domain):
        super().run(dispatcher, tracker, domain)
		
        location = tracker.get_slot("location")
        issue_type = get_issue_reason(tracker.latest_message["text"])

        if location is None:
            location = 'Aragon'

        if location is not None:
            try:
                answer = browser.search(
                    {
                        "intents": ["tipoIncidencia", "transportIssueReason"],
                        "entities": [issue_type, location],
                    }
                )
                print(answer)
                if len(answer) > 0:
                    link = None
                    if len(answer) > 5:
                        answer = answer[0:5]
                        link = "http://www.carreterasdearagon.es"

                    list_response = ""  # \n\t- ".join([x["answer0"] for x in answer])
                    for x in answer:
                        list_response += "\n\t- En la carretera {} {} - {}".format(
                            x["answer0"], x["answer1"], x["answer3"]
                        )

                    if link is not None:
                        list_answer = "{} \n\n Puedes consultar el listado completo en el siguiente enlace {}".format(
                            list_response, link
                        )
                    else:
                        list_answer = list_response

                    if issue_type is None or issue_type == "":
                        dispatcher.utter_message(
                            "Las incidencias de tráfico de la localidad de {} son :{}".format(
                                location, list_answer
                            )
                        )
                    else:
                        dispatcher.utter_message(
                            "Las incidencias de tráfico de la localidad de {} causadas por {} son :{}".format(
                                location, issue_type, list_answer
                            )
                        )

                else:
                    dispatcher.utter_message(
                        f"No he encontrado incidencias de tráfico por {issue_type} en {location}."
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "Perdona pero no he detectado población en la que buscar las incidencias de tráfico."
            )

        return [SlotSet("location", None), SlotSet("number", None), SlotSet("road_names", None)]