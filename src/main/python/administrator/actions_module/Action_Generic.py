"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import json
import os
from typing import List, Text

from random import randrange

from rasa_sdk import Action
from rasa_sdk.forms import REQUESTED_SLOT
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import EventType, FollowupAction, SlotSet, ActiveLoop
import sys

from actions_module.info_temas import InfoTemas

from actions_module.utils import *
from actions_module.message import Msgs


class Action_Generic(Action):
    """Superclass. Class which the rest of actions inherits from"""


    def __init__(self) -> None:
        """ Initialisation of the class (embedder) for semantic search"""
        self.understand_ckan = True

    def get_button_title(self, intent, entities):
        """ Call to the function get_button_title in intent_mapping

        Parameters
        ----------
        intent: json
            Detected intention
        entities: json
            List of entities found in user's question

        """
        return intent_mapping.get_button_title(intent, entities)

    def name(self):
       """ Property. Returns the name of the class"""
       return "Action_Generic"

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class.
            Try to identify the most proper intention

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

        # get the most likely intent
        try:
            intent_names, first_intent_names = self.get_intent_names(tracker)

            entities = tracker.latest_message.get("entities", [])
            entities = {e["entity"]: e["value"] for e in entities}
            buttons = generate_buttons_by_entity(first_intent_names, entities)

            themes_by_location = None
            if 'location' in entities:  # Location identified-> Entitities of this locality to this conversational frame
                idLocation = getIDMunicipio(entities['location'])
                if idLocation != '':
                    themes_by_location = getSubjectByIdMunicipio(idLocation)
                if themes_by_location is not None:
                    for result in themes_by_location:
                        ThemeName = result['id']['value'].split("#")[1]
                        if any(obj['subject'] == ThemeName for obj in intent_names):  #Only subject of the same conversational frame
                            if ThemeName in InfoTemas.themeDescription:
                                ThemeName = InfoTemas.themeDescription[ThemeName][1]
                            if ThemeName != "-":
                                button = {
                                    "title": ThemeName.capitalize() + " en " + result['locName']['value'] + " (" + str(result['nInstances']['value']) + ")",
                                    "payload": "/{intencion}{{\"subject_type\": \"{subject}\",\"loc_id\": \"{loc_id}\"}}".format(intencion="engagement.subject", subject=result['id']['value'],
                                                                                                                                 loc_id=result['id_location']['value'])
                                }
                                buttons.append(button)
            if len(buttons) <= 2:  # Location not identified -> Generic entities from conversational framework
                for intent_name in intent_names:
                    tema_desc = intent_name['subject'].split("/")[-1].replace("-", " ")
                    #tema_desc = intent_name['subject'].replace("_", " ")
                    buttons.append(
                        {
                            "title": tema_desc.capitalize(),
                            "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(
                                intencion='engagement.subject', subject=intent_name['subject'])
                        })
            dispatcher.utter_message(buttons=buttons,json_message={"understand_ckan": self.understand_ckan})
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sugg = Msgs.get_suggestion(tracker.latest_message['text'])
            if sugg == "":
                dispatcher.utter_message(text=Msgs.dont_understand[randrange(len(Msgs.dont_understand))],json_message={"understand_ckan": self.understand_ckan})
            else:
                dispatcher.utter_message(text=sugg,json_message={"understand_ckan": self.understand_ckan})
        return [ActiveLoop(None),SlotSet(REQUESTED_SLOT, None),SlotSet("results", None)]

    def get_intent_names(self, tracker):
        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        intent_name_sugery = intent_ranking[0]['name'].split('_')[0]  # Only suggests those with the same conversational frame tourims.grastronomy
        is_intent_name_list = '_list' in intent_ranking[0]['name']  # Only suggests those with the same conversational frame tourims.grastronomy

        try:
            intent_names = intent_theme[intent_ranking[0]['name'].split('.')[0]]
        except:
            pass
        if not is_intent_name_list:
            first_intent_names = list(
                    filter(lambda _: _.startswith(intent_name_sugery) and ("_list" not in _ and "number" not in _) and not _.startswith(('user', 'agent', 'greetings', 'weather', 'engagement')),
                           map(lambda _: _['name'], intent_ranking)))[1:4]
        else:
            first_intent_names = list(
                    filter(lambda _: ("_list" in _ or "number" in _) and not _.startswith(('user', 'agent', 'greetings', 'weather', 'engagement')),
                           map(lambda _: _['name'], intent_ranking)))[1:4]

        return intent_names,first_intent_names


