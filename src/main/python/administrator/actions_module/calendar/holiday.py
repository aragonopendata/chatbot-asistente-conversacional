from actions_module.calendar.utils import *
from actions_utils import get_entities
from urllib.error import URLError
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import dateutil.parser


from actions_module.Action_Generic import Action_Generic 

def dateToString(date):

    """Returns the date in a string format

        Parameters
        ----------
        date (variable) date

        Returns
        -------
        date_str str

        """

    formatoFechaDucklinf = "%d-%m-%y"
    date_str = None
    if date is not None:
        year = date[0:4]
        month = date[5:7]
        day = date[8:10]
        date_str = day + "-" + month + "-" + year
    return date_str


class ActionCalendarEvents(Action_Generic):

    def name(self):
        return "action_calendar_events"

    def run(self, dispatcher, tracker, domain):


        """Returns all the events of a Calendar

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message)

            """


        events = super().run(dispatcher, tracker, domain)
		
        formatoFechaDuckling = "%Y-%m-%dT%H:%M:%SZ"  # "yyyy-MM-dd'T'hh:mm:ss.SSSTZD"
        location = None

        try:
            location = clean_input(
                tracker.get_slot("location"),
                prefix=[
                    "localidad de ",
                    "municipio de ",
                    "provincia de",
                    "poblacion de",
                    "comarca de",
                ],
            )
        except:
            pass

        # It will be necessary to modify with Tracker adding a new conditional.
        # if Tracker.__dict__['latest_message']['entities'] then.

        entities = get_duckling_entities(tracker.latest_message["text"].lower())

        dateFrom = None
        dateTo = None
        timeValue = None
        grain = None
        for ent in entities:
            if ent["entity"] == "time":
                print(ent)
                timeValue = ent["value"]
                duckValue = ent["duckValue"]
                duckType = duckValue["type"]
                if duckType == "interval":
                    grain = duckValue["from"]["grain"]
                    dateFrom = dateutil.parser.parse(
                        duckValue["from"]["value"]
                    )  #  datetime.strptime(formatoFechaDuckling,duckValue["from"]["value"])
                    dateTo = dateutil.parser.parse(
                        duckValue["to"]["value"]
                    )  # datetime.strptime(formatoFechaDuckling,duckValue["to"]["value"])
                    break
                elif duckType == "value":
                    grain = duckValue["grain"]
                    value = duckValue["value"]
                    print(value)
                    if dateFrom == None:
                        dateFrom = dateutil.parser.parse(
                            value
                        )  # datetime.strptime(formatoFechaDuckling,value)
                    else:
                        dateTo = dateutil.parser.parse(
                            value
                        )  # datetime.strptime(formatoFechaDuckling,value)
                        break

        if dateFrom == None:
            timeValue = datetime.now().year
            dateFrom_str = "01-01-" + str(timeValue)
            dateTo_str = "01-01-" + str(timeValue + 1)

        else:
            if dateTo == None:
                if grain == "day":
                    dateTo = dateFrom + relativedelta(days=1)
                elif grain == "month":
                    dateTo = dateFrom + relativedelta(months=1)
                elif grain == "year":
                    dateTo = dateFrom + relativedelta(years=1)

            formatoFecha = "%d-%m-%Y"
            dateFrom_str = dateFrom.strftime(formatoFecha)
            dateTo_str = dateTo.strftime(formatoFecha)

        location_type = ""
        if location is None:
            location = "Aragon"

        if location is not None:
            try:
                location_type = ""
                if location.lower() in ["aragon", "aragón"]:
                    location_type = "Aragon"
                else:
                    location_type = get_location_type(tracker.latest_message["text"])

                entitiesReq = [location, dateFrom_str, dateTo_str, location_type]
                print(entitiesReq)

                # If there is no number at all, get current population
                answer = browser.search(
                    {
                        "intents": [
                            "calendarRangeHolidays",
                            "dateFrom",
                            "dateTo",
                            "tipoLocalizacion",
                        ],
                        "entities": entitiesReq,
                    }
                )
                print(answer)

                if len(answer) > 0 and answer != [{}]:
                    list_response = ""
                    list_responseEventos = ""
                    answer.sort(
                        key=lambda x: datetime.strptime(x["answer4"], "%d-%m-%Y")
                    )
                    for x in answer:
                        if x["answer6"].find(' (La)'):
                            exact_location = x["answer6"].split(' (La)')[0]
                        else:
                            exact_location = x["answer6"]
                        if x["answer1"] == "Festivos":
                            descripcion = x["answer3"]
                            if descripcion == "":
                                if x["answer2"].find(' (La)'):
                                    descripcion = x["answer2"].split(' (La)')[0]
                                else:
                                    descripcion = x["answer2"]
                            list_response += "\n\t- {} en {} - {}  ".format(
                                x["answer4"], exact_location, descripcion
                            )
                        else:
                            descripcion = x["answer2"]
                            list_responseEventos += "\n\t- {} al {} en {} - {}  ".format(
                                x["answer4"], x["answer5"], exact_location, descripcion
                            )

                    if list_response != "":
                        if list_responseEventos != "":
                            dispatcher.utter_message(
                                "Los festivos de {} en {}{} son:{}\n\n Los eventos son {} ".format(
                                    timeValue,
                                    get_location_type_output(location_type),
                                    location,
                                    list_response,
                                    list_responseEventos,
                                )
                            )
                        else:
                            dispatcher.utter_message(
                                "Los festivos de {} en {}{} son {} ".format(
                                    timeValue,
                                    get_location_type_output(location_type),
                                    location,
                                    list_response,
                                )
                            )
                    elif list_responseEventos != "":
                        dispatcher.utter_message(
                            "Los eventos de {} en {}{} son {} ".format(
                                timeValue,
                                get_location_type_output(location_type),
                                location,
                                list_responseEventos,
                            )
                        )

                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado datos para {  get_location_type_output(location_type)}{location} en {timeValue}"
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:
            dispatcher.utter_message(
                "No he detectado ninguna localización válida para buscar eventos o festividades."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionCalendarHolidaysWhen(Action_Generic):
    def name(self):
        return "action_calendar_when"

    def run(self, dispatcher, tracker, domain):

        """Returns holidays introducing a concrete day

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message)

            """

        events = super().run(dispatcher, tracker, domain)
		

        entities = tracker.latest_message.get("entities", [])
        misc_entity = next((x for x in entities if x["entity"] == "misc"), None)

        if misc_entity is not None:
            misc = misc_entity["value"]
        else:
            location_entity = next((x for x in entities if x["entity"] == "location"), None)
            if location_entity is not None:
                misc = location_entity["value"]
            else:
                misc = tracker.get_slot("misc")

        if misc is not None:
            try:
                answer = browser.search(
                    {"intents": ["calendarHolidaysWhen"], "entities": [misc]}
                )
                print(answer)

                if len(answer) > 0:
                    if len(answer) == 1:
                        dispatcher.utter_message(
                            "{} se celebra el {} en {}".format(
                                misc, answer[0]["answer5"], answer[0]["answer7"]
                            )
                        )
                    else:
                        for row in answer:
                            dispatcher.utter_message(
                                "{} se celebra el {} en {}".format(
                                    misc, row["answer5"], row["answer7"]
                                )
                            )
                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado información de {misc} en los calendarios"
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))

        else:
            dispatcher.utter_message(
                "No he detectado ninguna festividad o evento válido."
            )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionCalendarWhere(Action_Generic):
    def name(self):
        return "action_calendar_where"

    def run(self, dispatcher, tracker, domain):

        """Returns places introducing a concrete day

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message)

            """

        events = super().run(dispatcher, tracker, domain)
		        
        misc = tracker.get_slot("misc")
        if misc is None:
            try:
                misc = tracker.get_slot("location")
            except:
                pass

        if misc is None:
            entities = tracker.latest_message.get("entities", [])
            misc_entity = next((x for x in entities if x["entity"] == "misc"), None)

            if misc_entity is not None:
                misc=misc_entity["value"]
            else:
                try:
                    location_entity = next((x for x in entities if x["entity"] == "location"), None)
                    if location_entity is not None:
                        misc = location_entity["value"]
                    else:
                        misc = None
                except:
                    misc = None

        if misc is not None:
            try:
                # If there is no number at all, get current population
                answer = browser.search(
                    {"intents": ["calendarHolidaysWhere"], "entities": [misc]}
                )
                print(answer)
                if len(answer) > 0:
                    if len(answer) == 1:
                        dispatcher.utter_message(
                            "{} tiene lugar en {} el {}".format(
                                misc, answer[0]["answer7"], answer[0]["answer5"]
                            )
                        )
                    else:
                        answer.sort(
                            key=lambda x: datetime.strptime(x["answer5"], "%d-%m-%Y")
                        )
                        list_response = ""
                        for x in answer:
                            try:
                                list_response += "\n\t- {} en {}".format(
                                    x["answer5"], x["answer7"]
                                )
                            except:
                                pass
                        dispatcher.utter_message(
                            "En la provincia de {} se celebren las siguientes festividades o eventos en las siguientes fechas:{}".format(misc, list_response)
                        )

                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado datos de {misc}"
                    )
            except (URLError, Exception) as ex:
                dispatcher.utter_message(str(ex))
        else:

            formatoFechaDuckling = "%Y-%m-%dT%H:%M:%SZ"  # "yyyy-MM-dd'T'hh:mm:ss.SSSTZD"

            dateEntity = get_duckling_entities(tracker.latest_message["text"].lower())

            dateEntity = dateEntity[0]

            if dateEntity != None:
                timeValue = dateEntity["value"]
                duckValue = dateEntity["duckValue"]
                grain = duckValue["grain"]
                dateFrom = dateutil.parser.parse(duckValue["value"])
                dateTo = None
                if grain == "day":
                    dateTo = dateFrom + relativedelta(days=1)
                elif grain == "month":
                    dateTo = dateFrom + relativedelta(months=1)
                elif grain == "date":
                    dateTo = dateFrom + relativedelta(years=1)

                formatoFecha = "%d-%m-%Y"
                dateFrom_str = dateFrom.strftime(formatoFecha)
                dateTo_str = dateTo.strftime(formatoFecha)

                entitiesReq = ["Aragon", dateFrom_str, dateTo_str, "Aragon"]
                print(entitiesReq)

                # If there is no number at all, get current population
                answer = browser.search(
                    {
                        "intents": [
                            "calendarRangeHolidays,",
                            "dateFrom",
                            "dateTo",
                            "tipoLocalizacion",
                        ],
                        "entities": entitiesReq,
                    }
                )

                print(answer)

                if len(answer) > 0 and answer != [{}]:
                    list_response = ""
                    answer.sort(
                        key=lambda x: datetime.strptime(x["answer4"], "%d-%m-%Y")
                    )
                    for x in answer:
                        descripcion = x["answer3"]
                        if descripcion == "":
                            descripcion = x["answer2"]

                        list_response += "\n\t- {} - {}".format(
                            x["answer6"], descripcion
                        )

                    dispatcher.utter_message(
                        "El {} es festivo en: {}".format(
                            clean_input(timeValue, ["el", "El"]), list_response
                        )
                    )
                else:
                    dispatcher.utter_message(
                        f"No se ha encontrado datos de festivos el {timeValue}"
                    )

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events


class ActionCalendarLocalHolidays(Action_Generic):
    def name(self):
        return "action_calendar_local_holidays"

    def run(self, dispatcher, tracker, domain):

        """Returns local holidays introducing a concrete place

            Parameters
            ----------
            dispatcher
            tracker
            domain

            Returns
            -------
            dispatcher str (return message)

            """

        events = super().run(dispatcher, tracker, domain)
		
        location = clean_input(
            tracker.get_slot("location"),
            prefix=[
                "localidad de ",
                "municipio de ",
                "provincia de",
                "poblacion de",
                "comarca de",
            ],
        )
        year_str = None
        try:
            year_str = tracker.get_slot("number")
        except:
            pass
        if year_str == None:
            year_str = str(datetime.now().year)
        print(year_str)

        try:
            location_type = ""
            if location is None:
                location = "Aragon"

            if location.lower() in ["aragon", "aragón"]:
                location_type = "Aragon"
            else:
                location_type = get_location_type(tracker.latest_message["text"])

            answer = browser.search(
                {
                    "intents": [
                        "calendarHolidaysLocationPlace",
                        "Year",
                        "tipoLocalizacion",
                    ],
                    "entities": [location, year_str, location_type],
                }
            )
            print(answer)
            if len(answer) > 0 and answer != [{}]:
                list_response = ""
                answer.sort(key=lambda x: datetime.strptime(x["answer4"], "%d-%m-%Y"))
                list_responseEventos = ""
                link='https://opendata.aragon.es/datos/catalogo/dataset/calendario-de-festivos-en-comunidad-de-aragon-'+year_str
                list_link = "Puede consultar más festivos en <a href='"+link+"' target='_blank'>ENLACE</a>"

                if len(answer) > 5:
                    answer = answer[:5]


                for x in answer:
                    if x["answer1"] == "Festivos":
                        descripcion = x["answer3"]
                        if descripcion == "":
                            descripcion = x["answer2"]
                        list_response += "\n\t- {} en {} - {}  ".format(
                            x["answer4"], x["answer6"], descripcion
                        )

                dispatcher.utter_message(
                    "Los festivos locales de {}{} en {} son:{} \n\n{}".format(
                        get_location_type_output(location_type),
                        location,
                        year_str,
                        list_response,
                        list_link
                    )
                )
            else:
                dispatcher.utter_message(
                    f"No se ha encontrado datos de festivos locales en {location} en {year_str}"
                )
        except (URLError, Exception) as ex:
            dispatcher.utter_message(str(ex))

        events.extend([ SlotSet("location", None), SlotSet("number", None)])
        return events
