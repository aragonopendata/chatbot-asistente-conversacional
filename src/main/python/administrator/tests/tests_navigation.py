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

from actions_module.navigation import ActionEngagementSubject
from actions import ActionHello
from actions_module.message import Msgs

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


class ActionHelloTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.maxDiff = None

    @patch("rasa_sdk.Action")
    def test_ActionHello_ShowCategories(self, action):
        """
            Testea la acción de bienvenida, cuando el usario dice hola
            Reconoce la intención de Bienvenida
            Muestra un listado con todas las categorias
    """
        action.return_value = ActionFake()

        results = self.generic(
            ActionHello(),
            {"subject_type":""},
            {
                "text": "Hola",
            }
            )

        resultsTemas = ActionHello.GetTemas(self)
        #Mensaje de bienvenida
        self.assertTrue("Aragón Open Data" in results[0], f"valor devuelto:{results[0]}")
        #Número de categorias devueltas. Nº de botones. Tiene que haber 24, porque el sector-publico  que no es URL se elimina
        self.assertEqual( len(results[2]), len(resultsTemas["results"]["bindings"]) - 1)

    def generic(self, action, slot, message):
        print(f"<*** Mensaje de entrada ***> \n{message}\n<")
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(f"<*** Mensaje de salida ***> \n{dispatcher.get_message()}\n<")
        print(f"<*** Texto de salida ***> \n{dispatcher.get_text()}\n<")
        return dispatcher.get_text(), dispatcher.get_json_message(), dispatcher.get_buttons()


class ActionListSubjectTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.maxDiff = None


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_TurismoThemesFromWord(self, action):
        """
            El usuario introduce la palabra turismo e identifica que ese palabra
            corresponde a la categoría de turismo y saca todos los temas relacionados con
            turismo
        """
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"turismo"},
            {
                "text": "turismo",
                "entities": [{"entity":"subject_type",
                              "value":"turismo"}]
            }
            )

        #Mensaje de bienvenida
        self.assertTrue("Tengo información sobre estos contenidos" in results[0], f"valor devuelto:{results[0]}")
        #Número de categorias devueltas. Nº de botones. Tiene que haber 24, porque el sector-publico  que no es URL se elimina
        self.assertEqual( len(results[2]), 9)


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_SectorPublicoThemes(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"http://datos.gob.es/kos/sector-publico/sector/sector-publico"},
            {
                "text": "/engagement.subject{\"subject_type\": \"http://datos.gob.es/kos/sector-publico/sector/sector-publico\"}",
            }
            )

        self.assertTrue( "Tengo información sobre estos contenidos" in results[0], f"valor devuelto:{results[0]}")
        self.assertEqual( len(results[2]), 11)

    @patch("rasa_sdk.Action")
    def test_ActionEngagement_MedioAmbienteThemes(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"http://datos.gob.es/kos/sector-publico/sector/medio-ambiente"},
            {
                "text": "/engagement.subject{\"subject_type\": \"http://datos.gob.es/kos/sector-publico/sector/medio-ambiente\"}",
            }
            )

        self.assertTrue( "Tengo información sobre estos contenidos" in results[0], f"valor devuelto:{results[0]}")
        self.assertEqual( len(results[2]), 2)


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_CertenergeticaTemaShowEntidades(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"http://opendata.aragon.es/recurso/sector-publico/documento/certificacion-energetica"},
            {
                "text": "/engagement.subject{\"subject_type\": \"http://opendata.aragon.es/recurso/sector-publico/documento/certificacion-energetica\"}",
                "entities": [{"entity":"subject_type",
                              "value":"http://opendata.aragon.es/recurso/sector-publico/documento/certificacion-energetica"}]
            }
            )

        self.assertTrue( "tengo la siguiente información" in results[0], f"valor devuelto:{results[0]}")
        self.assertEqual( len(results[2]), 8)


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_EntidadCertEnergeticaShowProperties(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"http://opendata.aragon.es/recurso/sector-publico/documento/certificacion-energetica/2013hevu-000000147"},
            {
                "text": "/engagement.subject{\"subject_type\": \"http://opendata.aragon.es/recurso/sector-publico/documento/certificacion-energetica/2013hevu-000000147\"}\"}",
                "entities": [{"entity":"subject_type",
                              "value":"http://opendata.aragon.es/recurso/sector-publico/documento/certificacion-energetica/2013hevu-000000147"}]
            }
            )

        self.assertTrue( "tengo la siguiente información" in results[0], f"valor devuelto:{results[0]}")


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_AlojamientoRuralTemaShowEntidades(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural"},
            {
                "text": "/engagement.subject{\"subject_type\": \"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural\"}",
                "entities": [{"entity":"subject_type",
                              "value":"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural"}]
            }
            )

        self.assertTrue( "De casas rurales" in results[0], f"valor devuelto:{results[0]}")
        self.assertEqual( len(results[2]), 29)


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_EntidadCasaRuralShowProperties(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural/cr-huesca-09-001"},
            {
                "text": "/engagement.subject{\"subject_type\": \"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural/cr-huesca-09-001\"}\"}",
                "entities": [{"entity":"subject_type",
                              "value":"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural/cr-huesca-09-001"}]
            }
            )

        self.assertTrue( "tengo la siguiente información" in results[0], f"valor devuelto:{results[0]}")
        self.assertGreaterEqual( len(results[2]), 8)


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_ShowEntitiesLisRuralTourismtPlusLocation(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"subject_type":"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural",
            "loc_id":"http://opendata.aragon.es/recurso/sector-publico/organizacion/municipio/labata"},
            {
                "text": "/engagement.subject{\"subject_type\": \"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural\",\"loc_id\": \"http://opendata.aragon.es/recurso/sector-publico/organizacion/municipio/labata\"}",
                "entities": [{"entity":"subject_type",
                              "value":"http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural"},
                              {"entity":"loc_id",
                              "value":"http://opendata.aragon.es/recurso/sector-publico/organizacion/municipio/labata"}]
            }
            )

        self.assertTrue( "tengo la siguiente información" in results[0], f"valor devuelto:{results[0]}")
        self.assertGreaterEqual( len(results[2]), 2)


    @patch("rasa_sdk.Action")
    def test_ActionEngagement_ShowTourismThemesFromTourismWord(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"location": "Zaragoza","subject_type":"turismo"},
            {
                "text": "Oficinas de turismo en Zaragoza",
                "entities": [{"entity":"subject_type",
                              "value":"turismo"}]
            }
            )

        self.assertTrue("Tengo información sobre estos contenidos. ¿Qué te interesa?" in results[0], f"valor devuelto:{results[0]}")
        self.assertGreaterEqual( len(results[2]), 9)
        self.assertTrue( results[1]["understand_ckan"])


    # @patch("rasa_sdk.Action")
    # def test_ActionListSubjectFestivosAragon(self, action):
    #     action.return_value = ActionFake()

    #     results = self.generic(
    #         ActionEngagementSubject(),
    #         {"location": "Zaragoza","subject_type":""},
    #         {
    #             "text": "Festivos en Aragon",
    #             "entities": [{"entity":""}]
    #         }
    #         )

    #     assert "He encontrado en Aragón Open Data" in results[0]
    #     assert "ckan" == results[1]["understand_ckan"]

    @patch("rasa_sdk.Action")
    def test_ActionListSubjectAlbaniles(self, action):
        action.return_value = ActionFake()

        results = self.generic(
            ActionEngagementSubject(),
            {"location": "Zaragoza","subject_type":"albañiles"},
            {
                "text": "Albañiles",
                "entities": [{"entity":"subject_type",
                              "value":"albañiles"}]
                ,
                "intent": {"name": "fallback"},

            }
            )

        self.assertTrue (results[0] in Msgs.dont_understand)
        self.assertFalse  (results[1]["understand_ckan"] )


    def generic(self, action, slot, message):
        print(f"<*** Mensaje de entrada ***> \n{message}\n<")
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(f"<*** Mensaje de salida ***> \n{dispatcher.get_message()}\n<")
        print(f"<*** Texto de salida ***> \n{dispatcher.get_text()}\n<")
        print(f"<*** CKAN ***> \n{dispatcher.get_json_message()}\n<")
        return dispatcher.get_text(), dispatcher.get_json_message(), dispatcher.get_buttons()

