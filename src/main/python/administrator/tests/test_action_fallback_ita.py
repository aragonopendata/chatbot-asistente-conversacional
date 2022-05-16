#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch
import unittest
import json

from numpy.lib.function_base import place
from actions_module.message import Msgs
from actions_module.action_fallback_ita import  Action_Fallback_ita


class ActionFake:
    def __init__(self):
        self._message = ""
        self._text = ""
        self._json_message = ""


class Dispatcher:
    def __init__(self):
        self._message = ""
        self._text = ""
        self._buttons = ""
        self._json_message = ""

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
    entities=[]


    def __init__(self):
        self._slot = {"location": "SOBRARBE"}

    def get_slot(self, name):
        return self._slot[name]

    def set_slot(self, slot):
        self._slot = slot

    def set_latest_message(self, message):
        self.latest_message = message
    def set_entities(self, entities):
        self.entities = entities


class ActionDefaultAskAffirmationTest(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionDefaultAskAffirmation(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            Action_Fallback_ita(),
            {"location": "Teruel"},
            {
                "text": "Quiero teléfono de un albañil barato en Teruel"
            },
            )

        self.assertTrue (results[0] in Msgs.dont_understand, f"resultado {results[0]}" )
        #self.assertEqual( results[1]["understand_ckan"] == "ckan", f"resultado {results[1]}" )


    def generic(self, action, slot, message):
        print(f"mensaje de entrada ***> \n{message}\n<")
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(f"mensaje de salida::: \n{dispatcher.get_message()}\n<")
        print(f"text de salida::: \n{dispatcher.get_text()}\n<")
        return dispatcher.get_text(), dispatcher.get_json_message()


    def genericWithoutSlot(self, action, message):
        print(f"mensaje de entrada::: \n{message}\n<")
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(f"mesaje de salida::: \n{dispatcher.get_message()}\n<")
        print(f"text de salida::: \n{dispatcher.get_text()}\n<")
        return dispatcher.get_text(), dispatcher.get_json_message()
