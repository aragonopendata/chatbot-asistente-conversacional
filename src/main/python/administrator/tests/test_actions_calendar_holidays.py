"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch, MagicMock
import unittest
import rasa_sdk
from actions_module.calendar.holiday import *


class ActionFake:
    def __init__(self):
        self._message = ""


class Dispatcher:
    def __init__(self):
        self._message = ""
        self._text = ""
        self._buttons = ""

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


class ActionCalendarHolidaysMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_year(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": "Aragon"},
            {"text": "Dime los festivos de Aragon en el 2020", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") > 1)

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_date(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": None},
            {"text": "Que festividad se celebra el 6 de Diciembre", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") >= 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Month(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionCalendarEvents(),
            {"location": "provincia de Zaragoza"},
            {"text": "¿Qué fiestas hay en Julio en la provincia de Zaragoza?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") > 1 , f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Month_municipio(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionCalendarEvents(),
            {"location": "Zaragoza"},
            {"text": "Qué días son fiestas en Zaragoza este mes?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue(
            response.count("\n") >= 1 or
            response in "No se ha encontrado datos para el municipio de Zaragoza en este mes",
                f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Month_provincia(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionCalendarEvents(),
            {"location": "provincia de Zaragoza"},
            {"text": "Qué días son fiestas en la provincia de Zaragoza este mes?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") > 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Range(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": None},
            {"text": "¿Qué fiestas hay entre 2-3-2020 y el 4-10-2020?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") > 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Range_provincia(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": "Zaragoza"},
            {
                "text": "¿Qué fiestas hay entre 2-3-2020 y el 4-10-2020 en la provincia de Zaragoza? ", "intent_ranking": [{"name": "aragon.ranking_fake"}]
            },
        )
        self.assertTrue( response.count("\n") > 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysWhen(self, action):
        action.return_value = ActionFake()
        self.assertTrue (
            len(self.generic(
                ActionCalendarHolidaysWhen(),
                {"misc": "SANTA BÁRBARA"},
                {"text": "Cuando se celebra la festividad de la SANTA BÁRBARA?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            ))>=1
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysWhen_2(self, action):
        action.return_value = ActionFake()
        self.assertTrue (
            len(self.generic(
                ActionCalendarHolidaysWhen(),
                {"misc": "Expocanina"},
                {"text": "En que fechas se celebrara Expocanina?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            ))>=1
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysWhen_3(self, action):
        action.return_value = ActionFake()
        self.assertTrue (
            len(self.generic(
                ActionCalendarHolidaysWhen(),
                {"misc": "Feria del Mueble"},
                {"text": "Cuando se celebra la Feria del Mueble?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            ))>=1
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere(self, action):
        action.return_value = ActionFake()
        self.assertTrue (
            len(self.generic(
                ActionCalendarWhere(),
                {"misc": "SANTA BARBARA"},
                {"text": "¿Donde se celebra la festividad de SANTA BARBARA?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            ))>=1
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere1(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": "Santa Ana"},
            {"text": "¿Donde se celebra la festividad de Santa Ana?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") >= 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere2(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": None},
            {"text": "¿Donde es festivo en 6 de Diciembre?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") >= 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere3(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": None},
            {"text": "¿Donde es festivo el 26 de Diciembre?", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") >= 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere4(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": None},
            {"text": "Donde es festivo el 8 de Diciembre", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
        )
        self.assertTrue( response.count("\n") >= 1, f"resultado {response }")

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysLocation(self, action):
        action.return_value = ActionFake()
        self.assertTrue (
            len(
                self.generic(
                    ActionCalendarLocalHolidays(),
                    {"location": "provincia de Teruel"},
                    {
                        "text": "Cuales son las fiestas locales de la provincia de Teruel",
                        "intent_ranking": [{"name": "aragon.ranking_fake"}]
                    },
                )
            )
            > 1
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
