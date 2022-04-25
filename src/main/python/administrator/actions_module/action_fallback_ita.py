'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from typing import List
from rasa_sdk import Action
from actions_module.utils import *



class Action_Fallback_ita(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self):
        return "action_fallback_ita"

    def get_button_title(self, intent, entities):
        return intent_mapping.get_button_title(intent, entities)

    def run(self, dispatcher, tracker, domain)-> List[EventType]:
        return search_in_ckan( dispatcher, tracker)
