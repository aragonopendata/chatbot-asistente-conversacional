"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import os

from rasa.shared.constants import DEFAULT_MODELS_PATH, DEFAULT_DATA_PATH, DEFAULT_DOMAIN_PATH

here = os.path.dirname(__file__)

# Directory name where data is stored
DATA_DIR = os.path.join(here, DEFAULT_DATA_PATH)


# Default training directories
TRAINING_DATA_DIR = os.path.join(DATA_DIR, "training")
TRAINING_NLU_DATA_DIR = os.path.join(TRAINING_DATA_DIR, "nlu")

# Default path and files where data of a model is stored
DEFAULT_TEMPLATES_PATH = "templates"
DEFAULT_ENTITIES_PATH = "entities.json"
DEFAULT_STORIES_PATH = "stories.json"
DEFAULT_FORMS_PATH = "forms.yml"
DEFAULT_RULES_PATH = "rules.yml"
DEFAULT_INTENTS_PATH = "intents.json"
DEFAULT_PROJECTS_PATH = "projects.json"

# Rasa models storage
MODEL_PATH = os.path.join(here, DEFAULT_MODELS_PATH)

DEFAULT_MODEL_PATH= os.path.join(DATA_DIR, "GDA", "AOD")

# Smalltalk paths
SMALLTALK_DATA_PATH = os.path.join(DATA_DIR, "smalltalk")
SMALLTALK_INTENTS_PATH = os.path.join(SMALLTALK_DATA_PATH, "intents")
SMALLTALK_STORIES_PATH = os.path.join(SMALLTALK_DATA_PATH, "stories.md")
#SMALLTALK_STORIES_PATH_YAML = os.path.join(SMALLTALK_DATA_PATH, "stories_converted.yml")
SMALLTALK_DOMAIN_PATH = os.path.join(SMALLTALK_DATA_PATH, DEFAULT_DOMAIN_PATH)
DEFAULT_FORMS_PATH = os.path.join(DEFAULT_MODEL_PATH, DEFAULT_FORMS_PATH)
DEFAULT_RULES_PATH = os.path.join(DEFAULT_MODEL_PATH, DEFAULT_RULES_PATH)

# Goodbye intent name, used to end a conversation
GOODBYE_INTENT = "greetings.bye"


