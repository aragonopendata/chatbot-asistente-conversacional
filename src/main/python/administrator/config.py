"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import os
from logging.config import dictConfig

ACTION_URL_ENDPOINT = "http://rasa:5055/webhook"
NER_URL = "http://ner"

ONE_WORD_REQUEST = {"covid": "tienes información del covid",
                    "covid19": "tienes información del covid"
                    }

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)-8s %(name)-s - %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "simple",
            "stream": "ext://sys.stderr"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": "chatbot.log",
            "mode": "w"
        }
    },
    "root": {
        "level": os.getenv("RASA_DEBUG_LEVEL", default="INFO"),
        # "level": "DEBUG",

        "handlers": [
            "stderr",
            "stdout",
            "file"
        ]
    }
}

dictConfig(LOGGING_CONFIG)
