'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from browser.calendarController import calendarController
import json
from datetime import datetime
import requests
from datetime import date, timedelta
import time
from functools import lru_cache

@lru_cache(maxsize=None)
def parser(ics_url_path):

    calendario = ics_url_path

    try:
        calendarcontroller = calendarController(calendario)
        calendar = calendarcontroller.getCalendar()
        events = calendarcontroller.getEvents()
        calendario_name = calendarcontroller.getTypeCalendar(calendario)
    except:
        calendarcontroller = (
            requests.get(calendario).text.replace("\r\n", "").strip().split("},")
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
            nombre_evento = calendarcontroller.getParameter(event, "SUMMARY")
            description = calendarcontroller.getParameter(event, "description")
            fecha_inicio = calendarcontroller.getParameter(event, "START")
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y%m%d")
            fecha_inicio = fecha_inicio.strftime("%d-%m-%Y")
            fecha_fin = calendarcontroller.getParameter(event, "END")
            fecha_fin = datetime.strptime(fecha_fin, "%Y%m%d")
            fecha_fin = fecha_fin.strftime("%d-%m-%Y")
            localizacion = calendarcontroller.getParameter(event, "LOCATION")
            data = {
                "calendario_name": calendario_name,
                "nombre": nombre_evento,
                "descripcion": description,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "localizacion": localizacion,
            }
        except:
            fecha_inicio = datetime.strptime(event["fecha"], "%d/%m/%Y")
            fecha_inicio = fecha_inicio.strftime("%d-%m-%Y")
            t = time.strptime(fecha_inicio, "%d-%m-%Y")
            next_day = date(t.tm_year, t.tm_mon, t.tm_mday) + timedelta(1)
            fecha_fin = next_day.strftime("%d-%m-%Y")
            if event["festividad"] == []:
                nombre_evento = ""
            else:
                nombre_evento = event["festividad"]
            data = {
                "calendario_name": "",
                "nombre": nombre_evento,
                "descripcion": "",
                "location": "",
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "localizacion": event["localidad"],
            }
        events_good_structure_dict[nombre_evento] = data
        events_good_structure.append(data)
    return [events_good_structure, events_good_structure_dict]
