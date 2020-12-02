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
from actions_module.calendar.holiday import *


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


class ActionCalendarHolidaysMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_year(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": "Aragon"},
            {"text": "Dime los festivos de Aragon en el 2020"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_date(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": None},
            {"text": "Que festividad se celebra el 5 de marzo de 2020"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Month(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionCalendarEvents(),
            {"location": "provincia de Zaragoza"},
            {"text": "¿Qué fiestas hay en marzo en la provincia de Zaragoza?"},
        )
        assert response.count("\n") > 5

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Month_municipio(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionCalendarEvents(),
            {"location": "Zaragoza"},
            {"text": "Qué días son fiestas en Zaragoza este mes?"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Month_provincia(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionCalendarEvents(),
            {"location": "provincia de Zaragoza"},
            {"text": "Qué días son fiestas en la provincia de Zaragoza este mes?"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Range(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": None},
            {"text": "¿Qué fiestas hay entre 2-3-2020 y el 4-10-2020?"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarEvents_Range_provincia(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarEvents(),
            {"location": "Zaragoza"},
            {
                "text": "¿Qué fiestas hay entre 2-3-2020 y el 4-10-2020 en la provincia de Zaragoza? "
            },
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysWhen(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionCalendarHolidaysWhen(),
                {"misc": "SANTA BARBARA"},
                {"text": "Cuando se celebra la festividad de la SANTA BARBARA?"},
            )
            == "SANTA BARBARA se celebra el 04-12-2020 en Camañas"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysWhen_2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionCalendarHolidaysWhen(),
                {"misc": "Expocanina"},
                {"text": "En que fechas se celebrara Expocanina?"},
            )
            == "Expocanina se celebra el 01-02-2020 en ZARAGOZA"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysWhen_3(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionCalendarHolidaysWhen(),
                {"misc": "Feria del Mueble"},
                {"text": "Cuando se celebra la Feria del Mueble?"},
            )
            == "Feria del Mueble se celebra el 21-01-2020 en ZARAGOZA"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionCalendarWhere(),
                {"misc": "SANTA BARBARA"},
                {"text": "¿Donde se celebra la festividad de SANTA BARBARA?"},
            )
            == "SANTA BARBARA tiene lugar en Camañas el 04-12-2020"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere1(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": "Santa Ana"},
            {"text": "¿Donde se celebra la festividad de Santa Ana?"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere2(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": None},
            {"text": "¿Donde es festivo el 5 de marzo?"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere3(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": None},
            {"text": "¿Donde es festivo el 25 de julio?"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarWhere4(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionCalendarWhere(),
            {"misc": None},
            {"text": "¿Donde es festivo el 5 de marzo?"},
        )
        assert response.count("\n") > 1

    @patch("rasa_sdk.Action")
    def test_ActionCalendarHolidaysLocation(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                self.generic(
                    ActionCalendarLocalHolidays(),
                    {"location": "provincia de Teruel"},
                    {
                        "text": "Cuales son las fiestas locales de la provincia de Teruel"
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
