"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from typing import Any, Dict, List, Text, Optional

from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

import json
import requests

import config

from rasa.shared.nlu.constants import (
    TEXT
)

class ITAEntityExtractor(EntityExtractor):
    """Searches for structured entities: location, persons, organisations and miscellany"""

    provides = ["entities"]

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None):
        super(ITAEntityExtractor, self).__init__(component_config)
        self.__URL = config.NER_URL
        self.__PORT = 4999
        self.__NER_ENDPOINT = f"{self.__URL}:{str(self.__PORT)}/ner"

    def train(
        self, training_data: TrainingData, cfg: RasaNLUModelConfig, **kwargs: Any
    ) -> None:
        """Not needed, because the the model is pretrained"""
        pass
    
    
    def process(self, message: Message, **kwargs: Any) -> None:
        extracted = self.add_extractor_name(self.extract_entities(message))
        message.set(
            "entities", message.get("entities", []) + extracted, add_to_output=True
        )
    """
    def process(self,  messages :List[Message]) -> List[Message]:
        for message in messages:
            extracted = self.add_extractor_name(self.extract_entities(message))
            message.set(
                "entities", message.get("entities", []) + extracted, add_to_output=True
            )    
        return messages
    """
    def extract_entities(self, message: Message) -> List[Dict[Text, Any]]:
        datos= ""
        if "text" in dir(message):
            datos = message.text
        elif message.get(TEXT):
            datos = message.get(TEXT)
        else:
            datos = message
        try:
            response = requests.get(
                url=self.__NER_ENDPOINT,
                params={"words": datos, "plain": False, "duck": False},
            )
            content = json.loads(response.content)

            return content["entities"]
        except Exception as err:
            print("[WARN] NER exception" )
            print( err)
            return []

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Pass because a pre-trained model is already persisted"""
        pass
