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

from actions_module.transport.issues import *


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
    # @patch("rasa_sdk.Action")
    # def test_ActionBusLocation(self, action):
    #     action.return_value = ActionFake()
    #
    #     assert (
    #         self.generic(
    #             ActionBusLocation(),
    #             {"location": "Fraga"},
    #             {
    #                 "intent": {"name": "fax"},
    #                 "text": "que autobuses pasan por Fraga",
    #             },
    #         )
    #         == "Los autobuses que se pasan por Fraga son:"
    #         # TODO
    #     )

    # @patch("rasa_sdk.Action")
    # def test_ActionBusTimetable(self, action):
    #     action.return_value = ActionFake()
    #     assert (
    #         self.generic(
    #             ActionBusTimetable(),
    #             {"location": ""},
    #             {"text": "Qué horarios tiene el autobús que va desde Zaragoza a Huesca?"},
    #         )
    #         == "Los horarios de los autobuses que van de Zaragoza a Huesca son:\n\t-"
    #
    #         #TODO
    #     )

    # @patch("rasa_sdk.Action")
    # def test_ActionBusCompany(self, action):
    #     action.return_value = ActionFake()
    #     assert (
    #             self.generic(
    #                 ActionBusCompany(),
    #                 {"location": "Zuera"},
    #                 {"text": "¿Qué empresas dan servicio en Zuera?"},
    #             )
    #             == "Las empresas de autobuses que prestan servicio en Zuera son:\n\t- {}"
    #
    #         # TODO
    #     )

    @patch("rasa_sdk.Action")
    def test_ActionTransportIssues(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionTransportIssues(),
            {"location": "Calamocha"},
            {"text": "¿Existe alguna incidencia de tráfico en Calamocha?"},
        )

        assert (
            response == "No he encontrado incidencias de tráfico en Calamocha."
        ) or (len((response).splitlines()) >= 2)

    @patch("rasa_sdk.Action")
    def test_ActionTransportIssueType(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionTransportIssueType(),
            {"location": "Calamocha"},
            {
                "text": "¿Qué tipo de incidencias de tráfico hay en la localidad de Calamocha?"
            },
        )
        assert (
            response == "No he encontrado incidencias de tráfico en Calamocha."
        ) or (len((response).splitlines()) >= 2)

    @patch("rasa_sdk.Action")
    def test_ActionTransportIssueWhere(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionTransportIssueWhere(),
            {"location": "Calamocha"},
            {
                "text": "¿En qué tramos se encuentran las incidencias de tráfico de la localidad de Calamocha?"
            },
        )
        assert (
            response == "No he encontrado incidencias de tráfico en Calamocha."
        ) or (len((response).splitlines()) >= 2)

    @patch("rasa_sdk.Action")
    def test_ActionTransportIssueReasons(self, action):
        action.return_value = ActionFake()

        response = self.generic(
            ActionTransportIssueReasons(),
            {"location": "Calamocha"},
            {
                "text": "¿Cuáles son las causas de las incidencias de tráfico de la localidad de Calamocha?"
            },
        )
        assert (
            response
            == "No he encontrado incidencias de tráfico en Calamocha para informar de sus causas."
        ) or (len((response).splitlines()) >= 2)

    @patch("rasa_sdk.Action")
    def test_ActionTransportIssueReasonsAragon(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionTransportIssueReasons(),
            {"location": "Aragon"},
            {
                "text": "¿Qué está causando actualmente incidencias en la red de tráfico de Aragón?"
            },
        )

        assert (
            response
            == "No he encontrado incidencias de tráfico en Aragon para informar de sus causas."
        ) or (len((response).splitlines()) >= 2)

    @patch("rasa_sdk.Action")
    def test_ActionTransportIssueRestrictions(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionTransportIssueType(),
            {"location": "Aragon"},
            {"text": "Qué tipo de limitaciones en el tráfico hay activas?"},
        )
        assert (
            response == "No he encontrado restricciones de tráfico activas en Aragon."
        ) or (len((response).splitlines()) >= 2)

    @patch("rasa_sdk.Action")
    def test_ActionTransportIssueByReason(self, action):
        action.return_value = ActionFake()
        response = self.generic(
            ActionTransportIssueByReason(),
            {"location": "Cedrillas"},
            {
                "text": "Dime todas las incidencias de tráfico relativas a nieve en la localidad de Cedrillas"
            },
        )
        assert (
            response
            == "No he encontrado incidencias de tráfico por nieve en Cedrillas."
        ) or (len((response).splitlines()) >= 2)

    def generic(self, action, slot, message):
        print(message)
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(dispatcher.get_message())
        return dispatcher.get_message()
