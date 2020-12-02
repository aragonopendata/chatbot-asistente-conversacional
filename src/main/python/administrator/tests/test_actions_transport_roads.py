'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch, MagicMock
import unittest
import rasa_sdk

from actions_module.transport.road import *


class ActionFake:
    def __init__(self):
        self._message = ""


class Dispatcher:
    def __init__(self):
        self._message = ""

    def utter_message(self, message):
        self._message = message

    def get_message(self):
        return self._message


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


class ActionTrasnportMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadList(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionTransportRoadList(),
                    {"location": "Zaragoza"},
                    {"text": "¿Qué carreteras hay en la provincia de Zaragoza?"},
                ).splitlines()
            )
            > 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadSpeed(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadSpeed(),
                {"misc": "A-220", "location": "carretera A-220"},
                {"text": "¿a qué velocidad se puede ir por la carretera A-220?"},
            )
            == "La velocidad máxima de la carretera A-220 es 90 kilómetros por hora."
            # TODO
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadType(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadType(),
                {"misc": "A-220", "location": "carretera A-220"},
                {"text": "¿Qué tipo de carretera es la carretera A-220?"},
            )
            == "La carretera A-220 es:\n\t- autonómica\n\t- accesos"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadLocation(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionTransportRoadLocation(),
                    {"location": "Belchite"},
                    {"text": "¿Por qué carreteras puedo llegar a Belchite?"},
                )
            )
            > 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadDescription(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadDescription(),
                {"misc": "A-220", "location": "carretera A-220"},
                {"text": "¿Cuál es la descripción de la carretera A-220?"},
            )
            == "La descripción de la carretera A-220 es La Almunia de Doña Godina por Cariñena a Belchite."
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadZones(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadZones(),
                {"misc": "A-220", "location": "carretera A-220"},
                {"text": "¿Qué tipo de zonas hay cercanas a la carretera A-220?"},
            )
            == "Los zonas cercanas a la carretera A-220 son:\n\t- Zona de dominio público"
            # TODO
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadBridge(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionTransportRoadBridge(),
            {"misc": "A-220", "location": "carretera A-220"},
            {"text": "¿Qué puentes hay en la carretera A-220?"},
        )

        assert (response == "No he encontrado puentes en la carretera A-220.") or (
            len((response).splitlines()) >= 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadBridgeLocation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadBridgeLocation(),
                {"location": "Cariñena"},
                {"text": "¿Qué puentes hay en la localidad de Cariñena?"},
            )
            == "Los puentes que hay en Cariñena son:\n\t- 0A-0220-0016+500\n\t- 0A-0220-0021+060\n\t- 0A-0220-0021+250\n\t- 0A-0220-0026+700"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadBridgeKm(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadBridgeKm(),
                {"location": "Cariñena"},
                {
                    "text": "En qué punto kilométrico se encuentra el puente de Cariñena?"
                },
            )
            == "Los puentes de Cariñena se encuentran en los puntos kilométricos:\n\t- 16.500000 de la carretera A-220\n\t- 21.060000 de la carretera A-220\n\t- 21.250000 de la carretera A-220\n\t- 26.700000 de la carretera A-220"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadBridgesKms(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadBridgesKms(),
                {"misc": "A-220", "location": "carretera A-220"},
                {
                    "text": "¿En qué puntos kilométricos se encuentran los puentes de la carretera A-220?"
                },
            )
            == "Los puentes de la carretera A-220 están en los puntos kilométricos:\n\t- 16.500000\n\t- 21.060000\n\t- 21.250000\n\t- 26.700000\n\t- 37.600000"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadBridgesLocations(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadBridgesLocations(),
                {"misc": "A-220", "location": "carretera A-220"},
                {
                    "text": "¿En qué localidades se encuentran los puentes de la carretera A-220?"
                },
            )
            == "Los puentes de la carretera A-220 están en las siguientes localidades:\n\t- CARIÑENA\n\t- VILLANUEVA DE HUERVA"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadNameLength(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadLength(),
                {"misc": "A-220", "location": "carretera A-220"},
                {"text": "¿Que longitud tiene la carretera A-220?"},
            )
            == "La carretera A-220 tiene 67.50913694011999 kilómetros de longitud."
            # TODO
        )

    @patch("rasa_sdk.Action")
    def test_ActionTransportRoadLength(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTransportRoadLength(),
                {"misc": None},
                {
                    "text": "¿Cuántos kilómetros tiene la carretera de Daroca a Belchite?"
                },
            )
            == "La longitud de la carretera entre Daroca y Belchite es de 77.84 kilómetros"
        )

    def generic(self, action, slot, message):
        print(message)
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(dispatcher.get_message())
        return dispatcher.get_message()
