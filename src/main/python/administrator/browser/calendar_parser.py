from browser.calendarController import calendarController
import json
from datetime import datetime
import requests
from datetime import date, timedelta
import time
from functools import lru_cache

@lru_cache(maxsize=None)
def parser(ics_url_path):
    """  Extract all the calendars from a specific url (ics format)

    Parameters
    ----------
    ics_url_path: String
        Url where the calendar is located

    Returns
    -------
    dataframe 

        Calendars from a specific url
    """

    calendar_url = ics_url_path

    try:
        calendarcontroller = calendarController(calendar_url)
        calendar = calendarcontroller.getCalendar()
        events = calendarcontroller.getEvents()
        calendar_name = calendarcontroller.getTypeCalendar(calendar_url)
    except:
        calendarcontroller = (
            requests.get(calendar_url).text.replace("\r\n", "").strip().split("},")
        )
        events = []
        for element in calendarcontroller:
            element = element + "}"
            if element[0] == "[":
                element = element[1:].replace(" ", "")
            try:
                events.append(eval(element.replace(" ", "")))
            except:
                events.append(eval(element.replace(" ", "")[:-2]))
    events_good_structure_dict = {}
    events_good_structure = []
    for event in events:
        try:
            event_name = calendarcontroller.getParameter(event, "SUMMARY")
            description = calendarcontroller.getParameter(event, "description")
            start_date = calendarcontroller.getParameter(event, "START")
            start_date = datetime.strptime(start_date, "%Y%m%d")
            start_date = start_date.strftime("%d-%m-%Y")
            end_date = calendarcontroller.getParameter(event, "END")
            end_date = datetime.strptime(end_date, "%Y%m%d")
            end_date = end_date.strftime("%d-%m-%Y")
            location = calendarcontroller.getParameter(event, "LOCATION")
            data = {
                "calendario_name": calendar_name,
                "nombre": event_name,
                "descripcion": description,
                "fecha_inicio": start_date,
                "fecha_fin": end_date,
                "localizacion": location,
            }
        except:
            start_date = datetime.strptime(event["fecha"], "%d/%m/%Y")
            start_date = start_date.strftime("%d-%m-%Y")
            t = time.strptime(start_date, "%d-%m-%Y")
            next_day = date(t.tm_year, t.tm_mon, t.tm_mday) + timedelta(1)
            end_date = next_day.strftime("%d-%m-%Y")
            if event["festividad"] == []:
                event_name = ""
            else:
                event_name = event["festividad"]
            data = {
                "calendario_name": "",
                "nombre": event_name,
                "descripcion": "",
                "location": "",
                "fecha_inicio": start_date,
                "fecha_fin": end_date,
                "localizacion": event["localidad"],
            }
        events_good_structure_dict[event_name] = data
        events_good_structure.append(data)
    return [events_good_structure, events_good_structure_dict]
