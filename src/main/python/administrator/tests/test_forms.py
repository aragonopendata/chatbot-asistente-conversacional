"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch
import unittest
import asyncio

from data_test_forms import datos, data_calendar , data_drugs, data_pac
from actions_module.filter_forms import TimePlaceForm, TimeForm ,PlaceForm


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
    active_loop = {"name":True}
    latest_action_name = {"name":"action_listen"}

    def __init__(self):
        self.slots = {"location": "SOBRARBE"}

    def get_slot(self, name):
        return self.slots[name]

    def set_slot(self, slot):
        self.slots = slot

    def get_active_loop(self ):
        return self.active_loop

    def set_active_loop(self, active_loop):
        self.active_loop= active_loop

    def set_latest_message(self, message):
        self.latest_message = message

    def set_entities(self, entities):
        self.entities = entities

    def copy(self):
        return self


class ActionFormTest(unittest.TestCase):

    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarioNoEncuentraDatos(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimePlaceForm(),
                { "time":"2020", "place":"Alcañiz","resource_title":"title", "results":datos},
                {"text": "Calendario escolar Aragón" }
             )
        )

        self.assertTrue( "No hemos encontrado datos en esta fecha" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan")

    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarioEncuentraDatosTitulo(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimePlaceForm(),
                { "time":"2022", "place":"zaragoza","resource_title":"title","results":datos},
                {"text": "Calendario escolar Aragón" }
             )
        )

        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan")

    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarScool(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimeForm(),
                { "time":"2020","resource_title":"title","results":data_calendar},
                {"text": "Calendario escolar Aragón" }
             )
        )
        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan")

    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarScool_NoData(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimeForm(),
                { "time":"1950","resource_title":"title","results":data_calendar},
                {"text": "Calendario escolar Aragón" }
             )
        )
        self.assertTrue( "No hemos encontrado datos en esta fecha" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan")

    @patch("rasa_sdk.Action")
    def test_ActionResponseDrugs(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimePlaceForm(),
                { "time":"2020", "place":"zaragoza","resource_title":"resource","results":data_drugs},
                {"text": "Farmacias de guardia" }
             )
        )

        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue(  results[1]["understand_ckan"] == "ckan")

    @patch("rasa_sdk.Action")
    def test_ActionResponsePacTitle(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimeForm(),
                { "time":"2020","resource_title":"title","results":data_pac},
                {"text": "PAC" }
             )
        )

        self.assertTrue( "Política Agraria Común PAC 2020 Aragón" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan")

    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarioEncuentraDatosRecursos(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimePlaceForm(),
                { "time":"2022", "place":"huesca","resource_title":"resource","results":datos},
                {"text": "Calendario escolar Aragón" }
             )
        )

        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue(  results[1]["understand_ckan"] == "ckan" )

    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarioEncuentraDatosRecursosTime(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimeForm(),
                { "time":"2022", "resource_title":"resource","results":datos},
                {"text": "Calendario Aragón" }
             )
        )

        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue( results[1]["understand_ckan"]== "ckan" )


    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarioEncuentraDatosTituloTime(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                TimeForm(),
                { "time":"2022","resource_title":"title","results":datos},
                {"text": "Calendario Aragón" }
             )
        )

        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan")

    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarioEncuentraDatosRecursosLocation(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                PlaceForm(),
                { "place":"aragon", "resource_title":"resource","results":datos},
                {"text": "Calendario escolar Aragón" }
             )
        )

        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan" )


    @patch("rasa_sdk.Action")
    def test_ActionResponseCalendarioEncuentraDatosTituloLocation(self, action):
        action.return_value = ActionFake()
        results = asyncio.get_event_loop().run_until_complete(
            self.genericAsinc(
                PlaceForm(),
                { "place":"aragon","resource_title":"title","results":datos},
                {"text": "Calendario escolar Aragón" }
             )
        )

        self.assertTrue( "He encontrado en Aragón Open Data" in results[0])
        self.assertTrue( results[1]["understand_ckan"] == "ckan")



    async def genericAsinc(self, action, slot, message):
        #print(f"mensaje de entrada ***> \n{message}\n<")
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        await action.run(dispatcher, tracker, None)
        #print(f"mesaje de salida ***> \n{dispatcher.get_message()}\n<")
        #print(f"text de salida ***> \n{dispatcher.get_text()}\n<")
        return dispatcher.get_text(), dispatcher.get_json_message()

