'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import os

from typing import Tuple, List, Dict, Any

from loguru import logger

from constants import GOODBYE_INTENT

from rasa.shared.constants import DEFAULT_MODELS_PATH
from rasa.core.agent import Agent
from rasa.model import get_latest_model
from rasa.utils.endpoints import EndpointConfig

import bot_statistics as bs
import datetime
import config 

here = os.path.dirname(__file__)


class Bot:
    """
    A convenient interface to work with a Rasa agent for a project and a model

    This includes chatting with the agent, correction and parsing for user inputs
    """

    def __init__(
        self, project: str = "GDA", model: str = "AOD", user_type: str = "user"
    ):
        self.project = project
        self.model = model
        self.user_type = user_type

        self.agent_path = os.path.join(
            here, DEFAULT_MODELS_PATH, self.project, self.model
        )

        if model == "smalltalk":
            self.action_endpoint = None
        else:
            self.action_endpoint = EndpointConfig(url=config.ACTION_URL_ENDPOINT)

        if os.path.exists(self.agent_path):
            self.agent = Agent.load(
                get_latest_model(self.agent_path), action_endpoint=self.action_endpoint
            )
        else:
            raise NotADirectoryError(
                "NLU or dialogue model not found, make sure training succeeded"
            )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.project!r}, {self.model!r})"

    def __str__(self):
        return f"Chatbot of the project {self.project} and model {self.model}"

    def is_ready(self):
        """
        Calls agent is_ready() method to check if agent is ready to talk
        :return: flag that indicates a pre-trained agent is enabled to chat
        """

        return self.agent.is_ready()

    @classmethod
    def load(cls, project: str, model: str):
        """
        Loads a Rasa agent for project [project] and model [model]
        :return: a Bot instance
        """

        return cls(project, model)

    async def chat(
        self,
        user_input: str,
        user_time: datetime,
        project: str = None,
        model: str = None,
        ssid: str = None,
        print_info: bool = False,
    ) -> Tuple[List, List, bool]:
        """
        Method to chat with a pre-trained agent
        :param user_input: text of the user
        :param user_time: timestamp of the user text
        :param project:
        :param model:
        :param ssid: id of the session, useful to answer the adecuate user
        :param print_info: useful information in command line, useful for debugging
        :return: agent answer, icons for weather intent and flag to end conversation
        """

        if project and model and (project, model) != (self.project, self.model):
            self.__init__(project, model)
            # If we had to reload another model, reset user_time to not count as response time
            # the time it takes to initialize the agent
            user_time = datetime.datetime.now()

        # Interpreted info
        info = await self.agent.interpreter.parse(user_input)
        if print_info:
            from pprint import pprint

            pprint(info)

        """if os.name != "nt":  # Windows can't use hunspell
            from utils import spell_checker

            # Get user input as string template and values of the entities to recover
            user_input_templated, entity_values = self.remove_entities(
                user_input, info["entities"]
            )

            # Correct user input, {} does not affect to spell checker
            corrected_input = spell_checker.correct_spell(user_input_templated)
            # Recover original values of the entities in position, format accepts tuples
            # From this: whatever {} more {} -> whatever entity_value1 more entity_value2
            corrected_input = corrected_input.format(*entity_values)

        else:"""
        # If Windows, corected input is the same as the original
        corrected_input = user_input

        # Getting bot answer and response time to calculate elapsed time since user
        # introduced the input text
        answer = await self.agent.handle_text(corrected_input, sender_id=ssid)
        tracker = self.agent.tracker_store.get_or_create_tracker(ssid)
        is_misunderstood = None
        metadata = tracker.latest_bot_utterance.data.get("custom")# to get information from actions. 
        if metadata and "understand_ckan" in metadata:
            is_misunderstood = metadata["understand_ckan"]

        #latest_action_name =  tracker.latest_action_name
        #print (f" latest_action_name :{latest_action_name}")
        response_time = datetime.datetime.now()

        current_state = tracker.current_state()
        print (f" current_state :{current_state}")

        buttons= [x.get("buttons", "") for x in answer]

        # Get only texts
        answer = [x.get("text", "") for x in answer]

        # Split answer into text and icons if neccessary
        if "weather" in corrected_input:
            answer, icons = self.parse_answer(answer)
        else:
            icons = []

        # Does the conversation ended?
        conversation_has_finished = (GOODBYE_INTENT in corrected_input)

        if conversation_has_finished:
            self.agent = Agent.load(
                get_latest_model(self.agent_path), action_endpoint=self.action_endpoint
            )

        # Saving data to Mongo
        bs.insert_data(
            info,
            answer,
            user_input,
            corrected_input,
            ssid,
            user_time,
            response_time,
            self.user_type,
            conversation_has_finished,
            is_misunderstood
        )

        return answer, icons, conversation_has_finished,buttons

    @staticmethod
    def parse_answer(answer: List[str]) -> Tuple[List, List]:
        """
        Parse answer of the chatbot if weather intent to split icons and text
        :param answer: answer of the chatbot
        :return: list with text of the answer and list of icons
        """

        openweather_template = "http://openweathermap.org/img/w/{}.png"

        return answer[0::2], [openweather_template.format(x) for x in answer[1::2]]

    @staticmethod
    def remove_entities(
        user_input: str, entities: List[Dict[str, Any]]
    ) -> Tuple[str, List[str]]:
        """
        Replace entities in string to avoid spell checker to correct these values
        Replacement with {} to later recovery with string.format() function
        :param user_input: input text from the user
        :param entities: entities extracted by diferent Rasa components
        :return: tuple with input updates without entities and the values of these entities
        """

        extracted_values = []

        entities = [d for d in entities if d["extractor"] == "ITAEntityExtractor"]
        for entity in entities:
            user_input = user_input.replace(entity["value"], "{}")
            extracted_values.append(entity["value"])

        return user_input, extracted_values
