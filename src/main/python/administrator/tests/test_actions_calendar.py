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
from actions_module.calendar.events import *


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


class ActionCalendarMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionEventsByDate(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionEventsByDate(),
                {"date": "12-01-2020"},
                {"text": "Que eventos hay el 12 de enero"},
            )
            == "Los eventos del 12/01/2020 son:\n\t"
            # TODO
        )

    @patch("rasa_sdk.Action")
    def test_ActionEventsByDateLocation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionEventsByDateLocation(),
                {"location": "Zaragoza", "date": "29-01-2020"},
                {"text": "Que eventos hay en Zaragoza el 29 de enero?"},
            )
            == "Los eventos programados el 29-01-2020 en Zaragoza son:\n\t"
            # TODO
        )

    @patch("rasa_sdk.Action")
    def test_ActionEventLocation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionEventLocation(),
                {"misc": "Expocanina"},
                {"text": "Donde se realizara la feria Expocanina"},
            )
            == "Expocanina se realizará en Zaragoza\n\t"
            # TODO
        )

    @patch("rasa_sdk.Action")
    def test_ActionEventDates(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionEventDates(),
                {"misc": "Expocanina"},
                {"text": "En qué fechas se celebrará Expocanina?"},
            )
            == "Los fechas de Expocanina son:\n\t- {}"
            # TODO
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
