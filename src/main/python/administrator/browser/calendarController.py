'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import jicson
import requests


class calendarController:
    def __init__(self, url):

        try:
            self.calendar_variable = jicson.fromWeb(url, auth="base64_authtoken")
        except:
            self.calendar_variable = ""

    def getCalendar(self):

        return self.calendar_variable

    def getMainKey(self):

        return list(self.calendar_variable.keys())[0]

    def getMainKeyEvents(self):

        return list(self.calendar.keys())[len(self.calendar.keys()) - 1]

    def getCalendar(self):

        try:
            mainKey = self.getMainKey()
            self.calendar = self.calendar_variable[mainKey][0]
            return self.calendar_variable[mainKey][0]
        except:
            return []

    def getEvents(self):

        try:
            mainKey = self.getMainKeyEvents()
            self.events = self.calendar[mainKey]
            return self.calendar[mainKey]
        except:
            return []

    def getParameter(self, event, parameter):

        for key in event.keys():
            if key.upper().find(parameter.upper()) > -1:
                return event[key].replace("\n", "").replace("\r", "").replace("\\", "")

    def getTypeCalendar(self, calendario):

        calendario_name = ""
        if calendario.find("ar-") > -1:
            calendario_name = "Aragon"
        else:
            if calendario.find("hu-") > -1:
                calendario_name = "Huesca"
            else:
                if calendario.find("za-") > -1:
                    calendario_name = "Zaragoza"
                else:
                    if calendario.find("te-") > -1:
                        calendario_name = "Teruel"
                    else:
                        calendario_name = "Aragón"

        return calendario_name
