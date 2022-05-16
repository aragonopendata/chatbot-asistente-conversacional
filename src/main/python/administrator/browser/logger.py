"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import logging


class Log:

    """ This class stores all the information which the Chatbot application is generating. 
    Parameter
    ---------
        mensaje str"""

    @staticmethod
    def log_debug(mensaje: str):
        logging.basicConfig(filename="chatbot.log", filemode="w", level=logging.DEBUG)
        logging.debug(mensaje)
