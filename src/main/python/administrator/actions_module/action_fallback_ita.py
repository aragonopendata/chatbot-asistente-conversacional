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
        """ When a proper anwser it is not found
            The response is searched in CKAN through semantic analysis

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
        List[EventType]

            Formatted answer
        """
        return search_in_ckan( dispatcher, tracker)
