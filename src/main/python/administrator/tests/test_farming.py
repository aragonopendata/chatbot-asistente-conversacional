'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch
import unittest
from actions_module.farming import (
    #ActionFarmingRegionsCity,
    #ActionFarmingRegions,
    #ActionFarmingVillasCity,
    #ActionFarmingVillas,
    ActionFarmingFarmCropSize,
    ActionFarmingEcological,
    #ActionFarmingVillasInfo,
    ActionFarmingFarmCrop,
)


class ActionFake:
    def __init__(self):
        self._message = ""


class Dispatcher:
    def __init__(self):
        self._message = ""
        self._text = ""

    def utter_message(self, message="", text="", buttons="", json_message=""):
        self._message = message
        self._buttons = buttons
        self._text = text
        self._buttons = buttons
        self._json_message = json_message

    def get_message(self):
        return self._message

    def get_text(self):
        return self._text

    def get_buttons(self):
        return self._buttons

    def get_json_message(self):
        return self._json_message

class Tracker:
    latest_message = {"intent": "nada"}

    def __init__(self):
        self._slot = {"location": "SOBRARBE"}

    def get_slot(self, name):
        return self._slot[name]

    def set_slot(self, slot):
        self._slot = slot

    def set_latest_message(self, message):
        self.latest_message = message


class ActionFarmingMock(unittest.TestCase):
    '''@patch("rasa_sdk.Action")
    def _test_ActionFarmingRegionsCity(self, action):
        action.return_value = ActionFake()

        self.generic(
            ActionFarmingRegionsCity(),
            {"location": "SOBRARBE"},
            {"text": "Cuales son las comarcas agrarias del SOBRARBE"},
        )'''

    '''@patch("rasa_sdk.Action")
    def _test_ActionFarmingRegions(self, action):
        action.return_value = ActionFake()
        self.assertEqual (
            self.generic(
                ActionFarmingRegions(),
                {"location": "Calatayud"},
                {"text": "A que municipio pertenece la comarca agraria Calatayud"},
            )
            , "La comarca agraría Calatayud pertenece al municipio de CALATAYUD"
        )'''

    '''@patch("rasa_sdk.Action")
    def test_ActionFarmingVillasCity(self, action):
        action.return_value = ActionFake()
        self.assertEqual (
            self.generic(
                ActionFarmingVillasCity(),
                {"location": "SOBRARBE"},
                {"text": "Cuales son las villas y tierras del municipio SOBRARBE"},
            )
            , "Las villas y tierras del municipio SOBRARBE son\n\t- MANC. FORESTAL DE LINAS DE BROTO, BROTO Y FRAGEN\n\t- MANC. FORESTAL VALLE DE BROTO\n\t- MANC. FORESTAL BUESA-BROTO\n\t- MANC. VALLE DE VIO Y SOLANA\n\t- MANC. FORESTAL SIN, SEÑES Y SERVETO"
        )'''

    '''@patch("rasa_sdk.Action")
    def test_ActionFarmingVillas(self, action):
        action.return_value = ActionFake()
        self.assertEqual (
            self.generic(
                ActionFarmingVillas(),
                {"location": "MANC. FORESTAL SIN, SEÑES Y SERVETO"},
                {
                    "text": "A que municipio pertenece la villa MANC. FORESTAL SIN, SEÑES Y SERVETO"
                },
            )
            , "La villa MANC. FORESTAL SIN, SEÑES Y SERVETO pertenece al municipio de  SOBRARBE"
        )'''

    '''@patch("rasa_sdk.Action")
    def test_ActionFarmingVillasInfo(self, action):
        action.return_value = ActionFake()
        self.assertEqual (
            self.generic(
                ActionFarmingVillasInfo(),
                {"location": "MANC. FORESTAL SIN, SEÑES Y SERVETO"},
                {
                    "text": "Informacion sobre la villa MANC. FORESTAL SIN, SEÑES Y SERVETO"
                },
            )
            , "Los datos de la villa MANC. FORESTAL SIN, SEÑES Y SERVETO son:\n\t- localización: SOBRARBE\n\t- teléfono: 974 504 022\n\t- email: aytotellasin@aragob.es\n\t- cif: P-2200044-B"
        )'''

    @patch("rasa_sdk.Action")
    def test_ActionFarmingCropSize(self, action):
        action.return_value = ActionFake()

        # TIMEOUT SPARQL
        # self.generic(ActionFarmingFarmCrop(), {"location": "VALDEJALON"},{"text": "¿Qué fincas son de secano en el VALDEJALON?"})
        # self.generic(ActionFarmingFarmCrop(), {"location": "CINCA MEDIO"},{"text": "¿Qué fincas tienen cultivo leñoso en el CINCA MEDIO?"})
        # self.generic(ActionFarmingFarmCrop(), {"location": "CINCA MEDIO"},{"text": "Fincas de cultivo regadio en el CINCA MEDIO"})

    @patch("rasa_sdk.Action")
    def test_ActionFarmingFarmCropSize2(self, action):
        action.return_value = ActionFake()
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Aragón", "number": 1989},
                {"text": "Hectáreas de olivares en Aragon en 1989"},
            )
            , "En Aragón se cultivaron 40648 hectáreas de olivares en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Jacetania", "number": 1989},
                {"text": "Hectáreas de olivares en la comarca de Jacetania en 1989"},
            )
            , "En la comarca de Jacetania se cultivaron 0 hectáreas de olivares en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Zaragoza", "number": 1989},
                {"text": "Hectáreas de olivares en el municipio de Zaragoza en 1989"},
            )
            , "En el municipio de Zaragoza se cultivaron 62 hectáreas de olivares en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Teruel", "number": 1989},
                {"text": "Hectáreas de olivares en la provincia de Teruel en 1989"},
            )
            , "En la provincia de Teruel se cultivaron 20900 hectáreas de olivares en el año 1989"
        )

        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Aragón", "number": 1989},
                {"text": "Hectáreas de viñedos en Aragon en 1989"},
            )
            , "En Aragón se cultivaron 53853 hectáreas de viñedos en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Jacetania", "number": 1989},
                {"text": "Hectáreas de viñedos en la comarca de Jacetania en 1989"},
            )
            , "En la comarca de Jacetania se cultivaron 15 hectáreas de viñedos en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Zaragoza", "number": 1989},
                {"text": "Hectáreas de viñedos en el municipio de Zaragoza en 1989"},
            )
            , "En el municipio de Zaragoza se cultivaron 71 hectáreas de viñedos en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Teruel", "number": 1989},
                {"text": "Hectáreas de viñedos en la provincia de Teruel en 1989"},
            )
            , "En la provincia de Teruel se cultivaron 5396 hectáreas de viñedos en el año 1989"
        )

        # para el resto de cultivos hago solo una pregunta
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Aragón", "number": 1989},
                {"text": "Hectáreas de frutales en Aragon en 1989"},
            )
            , "En Aragón se cultivaron 107059 hectáreas de frutales en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Jacetania", "number": 1989},
                {"text": "Hectáreas de herbáceos en la comarca de Jacetania en 1989"},
            )
            , "En la comarca de Jacetania se cultivaron 21864 hectáreas de herbaceos en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Zaragoza", "number": 1989},
                {"text": "Hectáreas de regadío en el municipio de Zaragoza en 1989"},
            )
            , "En el municipio de Zaragoza se cultivaron 12529.0 hectáreas de regadio en el año 1989"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingFarmCropSize(),
                {"location": "Teruel", "number": 1989},
                {"text": "Hectáreas de secano en la provincia de Teruel en 1989"},
            )
            , "En la provincia de Teruel se cultivaron 378553.0 hectáreas de secano en el año 1989"
        )
    @unittest.skip("revisad")
    @patch("rasa_sdk.Action")
    def test_ActionFarmingEcological(self, action):
        action.return_value = ActionFake()
        self.assertEqual (
            self.generic(
                ActionFarmingEcological(),
                {"location": "Aragon", "number": "2013"},
                {"text": "Hectáreas de agricultura ecológica en Aragon en 2013"},
            )
            , "En Aragón se cultivaron 56907.7 hectáreas en el año 2013"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingEcological(),
                {"location": "Teruel", "number": "2013"},
                {
                    "text": "Hectáreas de agricultura ecológica en la provincia Teruel en 2013"
                },
            )
            , "En la provincia de Teruel se cultivaron 11031.6 hectáreas en el año 2013"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingEcological(),
                {"location": "Jacetania", "number": "2013"},
                {
                    "text": "Hectáreas de agricultura ecológica en la comarca Jacetania en 2013"
                },
            )
            , "En la comarca de Jacetania se cultivaron 812.56 hectáreas en el año 2013"
        )
        self.assertEqual (
            self.generic(
                ActionFarmingEcological(),
                {"location": "Zaragoza", "number": "2013"},
                {"text": "Hectáreas de agricultura ecológica en Zaragoza en 2013"},
            )
            , "En el municipio de Zaragoza se cultivaron 1447.17 hectáreas en el año 2013"
        )

    @staticmethod
    def generic(action, slot, message):
        print(message)
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(dispatcher.get_message())
        return dispatcher.get_message().rstrip(".")
