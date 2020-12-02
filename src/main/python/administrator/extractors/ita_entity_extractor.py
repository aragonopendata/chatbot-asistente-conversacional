'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from typing import Any, Dict, List, Text, Optional

from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.training_data import Message, TrainingData

import json
import requests

import config


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

    def extract_entities(self, message: Message) -> List[Dict[Text, Any]]:
        try:
            response = requests.get(
                url=self.__NER_ENDPOINT,
                params={"words": message.text, "plain": False, "duck": False},
            )
            content = json.loads(response.content)

            return content["entities"]
        except Exception:
            print("[WARN] NER exception")
            return []

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Pass because a pre-trained model is already persisted"""
        pass
