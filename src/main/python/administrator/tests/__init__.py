'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import os

from rasa.constants import DEFAULT_MODELS_PATH
from rasa.core.agent import Agent
from rasa.model import get_latest_model
from rasa.utils.endpoints import EndpointConfig


try:
    action_endpoint = EndpointConfig(url="http://rasa:5055/webhook")
    agent = Agent.load(
        get_latest_model(os.path.join(DEFAULT_MODELS_PATH, "GDA", "AOD")),
        action_endpoint=action_endpoint,
    )

    interpreter = agent.interpreter
except:
    pass

# with open(
#    os.path.join(os.path.dirname(os.path.dirname(__file__)), "browser", "data.json"),
#    encoding="utf8",
# ) as f:
#    SPARQL_DATA = json.load(f)
