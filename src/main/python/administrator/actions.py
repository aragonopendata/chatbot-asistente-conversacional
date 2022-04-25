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

from typing import *
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from browser.config import Config
from SPARQLWrapper import SPARQLWrapper, JSON
from browser.logger import Log
from actions_module.info_temas import InfoTemas

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
        query ="""
            PREFIX ei2a: <http://opendata.aragon.es/def/ei2av2#>
            PREFIX org: <http://www.w3.org/ns/org#>

            SELECT  DISTINCT ?category
            FROM <http://opendata.aragon.es/def/ei2av2>
            WHERE
            {
                ?b org:classification ?category
            }
        """

        # DELETE. Old category query to request a list of categories
        # query = """
        #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        #     PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
        #     PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>


        #     SELECT  DISTINCT ?category
        #     FROM <http://opendata.aragon.es/def/ei2a>
        #     WHERE {?a rdf:type ?category
        #            FILTER regex(str(?category),str(webCategory:))}
        #     order by ?category
        # """
        print(query)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def run(self, dispatcher, tracker, domain):
        hellomsg = ["Hola. Soy el asistente virtual de Aragón Open Data, estoy aquí para facilitarte a obtener información sobre los datos almacenados aquí",
        "Bienvenido a Aragón Open Data, soy un asistente virtual y estoy aquí para facilitarte a obtener información sobre los datos almacenados.",
        "Bienvenido, soy el asistente virtual del Aragón Open Data, tengo mucha información que seguro te resultará muy interesante."]
        if tracker.latest_message['text'] in ['ok']:
            msg = "De acuerdo. Te puedo proponer estos temas o si quieres me haces alguna pregunta adicional"
        else:
            msg = f'{hellomsg[random.randint(0, len(hellomsg)-1)]} Tengo información detallada de los siguientes temas que te pueden interesar. ¿Qué quieres saber?'

        resultsTemas = self.GetTemas()
        buttons = []
        ## Nivel 1
        for result in resultsTemas["results"]["bindings"]:
            #Ahora las categorías hay que recoger la URL entera, porque el prefijo varía
            cat = result['category']['value']
            # try:
            #     cat = result['category']['value'].split("#")[1]
            # except:
            #     cat = ""
            # if not cat:
            #     try:
            #        if result['category']['value'].index("/") > 0:
            #             cat = result['category']['value'].split("/")[-1]
            #     except:
            #         cat = ""
            if cat in InfoTemas.description_catalog:
                desCate = InfoTemas.description_catalog[cat][0]
                buttons.append(
                    {
                        "title":  desCate,
                        "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(intencion="engagement.subject", subject=cat)
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

            last_actions = [
                event["name"]
                for event in events
                if event["event"] == "action"
                and event["name"] != self.name()
                and all(
                    x != event["name"]
                    for x in ["action_listen", "action_name", "action_joke"]
                )
                and event["name"].startswith("action")
            ]
            if last_actions:
                # Last action executed in the conversation apart from this one
                # This action is discarded cause it may been executed more times
                last_action = last_actions[-1]

                # Class members within this script
                clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
                for classname, module in clsmembers:
                    # We have to look over classes that starts with 'Action' but it is not
                    # the 'Action' interface from 'rasa_sdk.interfaces'
                    if (
                        classname.startswith("Action")
                        and classname != "Action"
                        and module().name() == last_action
                    ):
                        module().run(dispatcher, tracker, domain)
            else:
                # There is no previous action to re execute
                dispatcher.utter_message(
                    f"No tengo constancia sobre ninguna pregunta concreta de una ciudad "
                    f"para devolverle la misma información de {location}"
                )
        else:
            dispatcher.utter_message("No se ha detectado ninguna localización conocida")

