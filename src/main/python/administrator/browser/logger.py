'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import logging


class Log:
    @staticmethod
    def log_debug(mensaje: str):
        logging.basicConfig(filename="chatbot.log", filemode="w", level=logging.DEBUG)
        logging.debug(mensaje)
