"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import pandas as pd

class IntentMapping:
    """Class to map intention with actions
    """

    def __init__(self) -> None:
        """ Initialisation of the class """


        self.understand_ckan = True

        self.intent_mappings = pd.read_csv("data/intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(";")}
        )

    def get_intent_mappings(self):
        return self.intent_mappings

    def get_button_title(self, intent, entities) -> str:

        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (self.intent_mappings.entities == entities.keys()) & (
            default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent
        message = ""
        if 'location' not in entities:
            entities = {'location': '...'}
            btntitle = button_title.format(**entities)
            message = btntitle[0].upper() + btntitle[1:]
            return None, message
        else:
            btntitle = button_title.format(**entities)
            return btntitle[0].upper() + btntitle[1:], ""