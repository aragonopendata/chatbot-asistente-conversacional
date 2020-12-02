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

from actions_module.transport.bus import *


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


class ActionTransportBusMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionBusLocation(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionBusLocation(),
                    {"location": "Zaragoza"},
                    {"text": "¿Qué autobuses van a Zaragoza?"},
                ).splitlines()
            )
            > 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionBusLocation2(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionBusLocation(),
                    {"location": "Borja"},
                    {"text": "¿Qué autobuses van a Borja?"},
                ).splitlines()
            )
            > 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionBusLocation3(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionBusLocation(),
                    {"location": "Segovia"},
                    {"text": "¿Qué autobuses van a Segovia?"},
                ).splitlines()
            )==1
        )

    @patch("rasa_sdk.Action")
    def test_ActionBusTimetable(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionBusTimetable(),
                    {},
                    {"text": "¿Qué autobuses van de Lecera a Zaragoza?"},
                ).splitlines()
            )
            > 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionBusTimetable2(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionBusTimetable(),
                    {},
                    {"text": "¿Qué autobuses van de Zaragoza a Borja?"},
                ).splitlines()
            )
            > 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionBusTimetable3(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionBusTimetable(),
                    {},
                    {"text": "¿Qué autobuses van de Borja a Zaragoza?"},
                ).splitlines()
            )
            > 2
        )

    @patch("rasa_sdk.Action")
    def test_ActionBusCompany(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionBusCompany(),
                    {"location": "Zaragoza"},
                    {"text": "¿Qué empresas dan servicio en Zaragoza?"},
                ).splitlines()
            )
            > 2
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
