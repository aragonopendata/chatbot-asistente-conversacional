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
