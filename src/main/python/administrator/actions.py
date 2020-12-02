'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import inspect
import random
import sys

from actions_utils import extract_days
from functools import lru_cache
from open_weather_parser import OpenWeatherParser
from typing import *
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from browser.config import Config
from SPARQLWrapper import SPARQLWrapper, JSON
from browser.logger import Log
from actions_module.navigation import InfoTemas

import json

class ActionFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            "No entiendo lo que quiere decir, pruebe reformulando su mensaje"
        )

        return []



################################
############# Welcome #############
################################

class ActionHello(Action):



    def name(self):
        return "action_hello"

    @lru_cache()
    def GetTemas(self):
        sparql = SPARQLWrapper(Config.bbdd_url())
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
            PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>


            SELECT  DISTINCT ?category
            FROM <http://opendata.aragon.es/def/ei2a>
            WHERE {?a rdf:type ?category
                   FILTER regex(str(?category),str(webCategory:))}
            order by ?category   
        """
        print(query)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        resultsTemas = sparql.query().convert()
        return resultsTemas

    def run(self, dispatcher, tracker, domain):
        hellomsg = ["Hola. Soy el asistente virtual de Aragón Open Data, estoy aquí para facilitarte a obtener información sobre los datos almacenados aquí",
        "Bienvenido a Aragón Open Data, soy un asistente virtual y estoy aquí para facilitarte a obtener información sobre los datos almacenados.",
        "Bienvenido, soy el asistente virtual del Aragón Open Data, tengo mucha información que seguro te resultará muy interesante."]
        msg = hellomsg[random.randint(0, len(hellomsg)-1)] + " Tengo información detallada de los siguientes temas que te pueden interesar. ¿Qué quieres saber?"
        resultsTemas = self.GetTemas()
        buttons = []
        ## Nivel 1
        for result in resultsTemas["results"]["bindings"]:
            desCate = result['category']['value'].split("#")[1]
            if desCate in InfoTemas.descCat:
                desCate = InfoTemas.descCat[result['category']['value'].split("#")[1]][0]
            buttons.append(
                {
                    "title":  desCate,
                    "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(intencion="engagement.subject", subject=result['category']['value'].split("#")[1])
                })

        dispatcher.utter_message(text=msg, buttons=buttons)

        return []




################################
############# JOKE #############
################################


class ActionJoke(Action):
    def name(self):
        return "action_joke"

    def run(self, dispatcher, tracker, domain):
        with open("data/jokes/jokes_es.txt", encoding="utf8") as f:
            lines = f.readlines()
            dispatcher.utter_message(
                lines[random.randint(0, len(lines)-1)].lstrip("- ").rstrip("\n")
            )
            f.close()

        return []


####################################
########### USER NAME ##############
####################################


# class ActionName(Action):
#     def name(self):
#         return "action_name"
#
#     def run(self, dispatcher, tracker, domain):
#         names = (
#             open("data/lookup/nombres.txt", "r", encoding="utf8").read().splitlines()
#         )
#         names_lower = [x.lower() for x in names]
#         msg = tracker.latest_message["text"].lower()
#         match = ""
#         for original, lower in zip(names, names_lower):
#             if lower in msg and len(lower) > len(match):
#                 match = original
#
#         return [SlotSet("name", match)]


#######################################
########### ANOTHER CITY ##############
#######################################


class ActionAnotherCity(Action):
    def name(self):
        return "action_another_city"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot("location")
        if location is not None:
            # Get events from tracker
            events = tracker.events

            # Get actions_module that are not default 'action_listen' nor this action
            last_actions = [
                event["name"]
                for event in events
                if event["event"] == "action"
                and event["name"] != self.name()
                and not any(
                    x == event["name"]
                    for x in ["action_listen", "action_name", "action_joke"]
                )
                # To avoid previous utterances
                and event["name"].startswith("action")
            ]

            # Exists a previous action to ask for another city?
            if len(last_actions) > 0:
                # Last action executed in the conversation apart from this one
                # This action is discarded cause it may been executed more times
                last_action = last_actions[-1]

                # Class members within this script
                clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
                for classname, module in clsmembers:
                    # We have to look over classes that starts with 'Action' but it is not
                    # the 'Action' interface from 'rasa_sdk.interfaces'
                    if classname.startswith("Action") and classname != "Action":
                        # When we find the actions_module that was executed excluding this one
                        if module().name() == last_action:
                            module().run(dispatcher, tracker, domain)
            else:
                # There is no previous action to re execute
                dispatcher.utter_message(
                    f"No tengo constancia sobre ninguna pregunta concreta de una ciudad "
                    f"para devolverle la misma información de {location}"
                )
        else:
            dispatcher.utter_message("No se ha detectado ninguna localización conocida")


##################################
########### WEATHER ##############
##################################

# TODO: Iconos del tiempo
class ActionWeather(Action):
    def __init__(self):
        self.parser = OpenWeatherParser()

    def name(self):
        return "action_weather"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        location = tracker.get_slot("location")

        if location is None:
            dispatcher.utter_message(
                "No se ha detectado ninguna localización, vuelva a intentarlo especificando una ciudad."
            )

            return []

        days = extract_days(message)
        print(days)

        if days is not None:
            if days < 0 or days > 4:
                dispatcher.utter_message(
                    "No puedo predecir días previos o posteriores a 5 días vista."
                )

                return []
            else:
                forecast_info = self.parser.get_forecast_weather(location)
                response, icon = forecast_info[days]

        else:
            response, icon = self.parser.get_current_weather(location)

        dispatcher.utter_message(response)
        if icon:
            dispatcher.utter_message(icon)

        return [SlotSet("location", None), SlotSet("days", None), SlotSet("when", None)]


class ActionWeatherPeriod(Action):
    def __init__(self):
        self.parser = OpenWeatherParser()

    def name(self):
        return "action_weather_period"

    def run(self, dispatcher, tracker, domain):

        message = tracker.latest_message["text"]

        location = tracker.get_slot("location")
        # location = extract_location_weather(message) if location is None else location

        if location is None:
            dispatcher.utter_message(
                "No se ha detectado ninguna localización, vuelva a intentarlo especificando una ciudad."
            )

            return []

        days = extract_days(message)

        if days is not None:
            if days < 0 or days > 4:
                dispatcher.utter_message(
                    "No puedo predecir días anteriores al dia de hoy o posteriores a 5 días vista."
                )
                return []
            else:
                for message, icon in self.parser.get_forecast_weather(location)[1:days]:
                    dispatcher.utter_message(message)
                    dispatcher.utter_message(icon)

        else:
            dispatcher.utter_message(
                "No he detectado una expresión temporal valida. Revise su ortografía."
            )

        return [SlotSet("location", None), SlotSet("days", None), SlotSet("when", None)]
