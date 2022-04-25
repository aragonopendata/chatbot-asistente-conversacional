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
from actions_module.activities import (
    #ActionMuseumWorks,
    ActionMuseumsLocation,
    #ActionLocationWork,
    #ActionRoutesOut,
    #ActionRoutesIn,
    ActionRoutesThrough,
    #ActionRoutesFromTo,
    #ActionTourGuideName,
    ActionTourGuidePhone,
    ActionTourGuideEmail,
    ActionTourGuideWeb,
    ActionTourGuideContactInfo,
    ActionTourOfficePhone,
    ActionTourOfficeLocation,
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


class ActionActivitieMock(unittest.TestCase):
    """@patch("rasa_sdk.Action")
    def test_ActionMuseumWorks(self, action):
        action.return_value = ActionFake()

        assert (
            len(
                self.generic(
                    ActionMuseumWorks(),
                    {"location": "Pablo Gargallo"},
                    {"text": "Que obras tiene el museo Pablo Gargallo"},
                )
            )
        ) > 200"""

    # TODO devuelve datos aparentemente incorrectos
    @patch("rasa_sdk.Action")
    def test_ActionMuseumsLocation(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionMuseumsLocation(),
                    {"location": "Zaragoza"},
                    {"text": "que museos hay en Zaragoza"},
                )
            )
        ) >= 2

    """@patch("rasa_sdk.Action")
    def test_ActionRoutesOut(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionRoutesOut(),
                        {"location": "Jaca"},
                        {"text": "cuales son las rutas que salen de Jaca"},
                    )
                ).splitlines()
            )
            >= 5
        )"""

    """@patch("rasa_sdk.Action")
    def test_ActionRoutesIn(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionRoutesIn(),
                        {"location": "Jaca"},
                        {"text": "cuales son las rutas que llegan a Jaca"},
                    )
                ).splitlines()
            )
            >= 5
        )"""

    @patch("rasa_sdk.Action")
    def test_ActionRoutesThrough(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionRoutesThrough(),
                        {"location": "Jaca"},
                        {"text": "cuales son las rutas que pasan por Jaca"},
                    )
                ).splitlines()
            )
            >= 2
        )

    # TODO falla el test
    @patch("rasa_sdk.Action")
    def _test_ActionRoutesFromTo(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionRoutesFromTo(),
                        {"location": "Jaca"},
                        {"text": "que rutas empiezan Pamplona y terminan en Jaca"},
                    )
                ).splitlines()
            )
            > 1
        )

    """@patch("rasa_sdk.Action")
    def test_ActionTourGuideName(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionTourGuideName(),
                        {"location": "RIBERA BAJA DEL EBRO"},
                        {
                            "text": "Dime guias de turismo de la comarca RIBERA BAJA DEL EBRO"
                        },
                    )
                ).splitlines()
            )
            >= 3
        )"""

    # TODO Como el nombre esta guardado en formato Apellidos Nombre si hacemos la conslta con Nombre Apellidos no se encuentra nada
    @patch("rasa_sdk.Action")
    def test_ActionTourGuidePhone(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTourGuidePhone(),
                {"person": "Hernández Royo"},
                {"text": "cual es el telefono de la guia turistica Hernández Royo", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "El teléfono de Hernández Royo Ana Elisa es 976-178273 / 615-084875"
        )

    # TODO Como el nombre esta guardado en formato Apellidos Nombre si hacemos la conslta con Nombre Apellidos no se encuentra nada
    @patch("rasa_sdk.Action")
    def test_ActionTourGuideEmail(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTourGuideEmail(),
                {"person": "Hernández Royo"},
                {"text": "cual es el email de la guia turistica Hernández Royo", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "El email de Hernández Royo Ana Elisa es sastago40@hotmail.com"
        )

    # TODO Como el nombre esta guardado en formato Apellidos Nombre si hacemos la conslta con Nombre Apellidos no se encuentra nada
    @patch("rasa_sdk.Action")
    def test_ActionTourGuideWeb(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTourGuideWeb(),
                {"person": "ALCÁZAR RODRÍGUEZ JOSÉ LUÍS"},
                {"text": "cual es la web del guia turistico ALCÁZAR RODRÍGUEZ JOSÉ LUÍS", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "La web de Alcázar Rodríguez José Luís es www.accion21.es"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTourGuideContactInfo(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTourGuideContactInfo(),
                {"person": "Dalda Abril Hilario"},
                {
                    "text": "cual es la direccion de contacto del guia turistico Dalda Abril Hilario", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La información de contacto de Dalda Abril Hilario es dalda.hilario@gmail.es, 978-700381 / 651-300984, DALDA ABRIL HILARIO"
        )


    @patch("rasa_sdk.Action")
    def test_ActionTourGuideContactInfo2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTourGuideContactInfo(),
                {"person": "Sanz Vitalla Pedro"},
                {
                    "text": "cual es la direccion de contacto del guia turistico Sanz Vitalla Pedro", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La información de contacto de Sanz Vitalla Pedro es piter_hu@hotmail.com, 696-145752 / 606-654695, SANZ VITALLA PEDRO"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTourOfficePhone(self, action):
        action.return_value = ActionFake()

        assert (
            len(
                (
                    self.generic(
                        ActionTourOfficePhone(),
                        {"location": "Zaragoza"},
                        {"text": "Teléfonos de las oficinas de turismo de Zaragoza"},
                    )
                ).splitlines()
            )
            >= 1
        )

        assert (
            len(
                (
                    self.generic(
                        ActionTourOfficePhone(),
                        {"location": "Teruel"},
                        {"text": "Teléfonos de las oficinas de turismo de Teruel"},
                    )
                ).splitlines()
            )
            >= 1
        )

    @patch("rasa_sdk.Action")
    def test_ActionTourOfficeLocation(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionTourOfficeLocation(),
                        {"location": "Zaragoza"},
                        {"text": "Dirección de las oficinas de turismo de Zaragoza"},
                    )
                ).splitlines()
            )
            >= 1
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
