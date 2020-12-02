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
    ActionMuseumWorks,
    ActionMuseumsLocation,
    ActionLocationWork,
    ActionRoutesOut,
    ActionRoutesIn,
    ActionRoutesThrough,
    ActionRoutesFromTo,
    ActionTourGuideName,
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


class ActionActivitieMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
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
        ) > 200

    # TODO devuelve datos aparentemente incorrectos
    @patch("rasa_sdk.Action")
    def test_ActionMuseumsLocation(self, action):
        action.return_value = ActionFake()
        self.generic(
            ActionMuseumsLocation(),
            {"location": "Zaragoza"},
            {"text": "que museos hay en Zaragoza"},
        )

    @patch("rasa_sdk.Action")
    def _test_ActionLocationWork(self, action):
        action.return_value = ActionFake()
        # TODO el NER develve amanecer como location y se espera misc
        self.generic(
            ActionLocationWork(),
            {"misc": ""},
            {"text": "¿Dónde se encuentra la escultura de El Amanecer?"},
        )

        # TODO se muestra un museo que no tiene nada que ver con goya, sin embargo en la lita que devuelve el browser si que esta el museo goya, no se si es problema de la bd o de la query
        self.generic(
            ActionLocationWork(),
            {"misc": "Desastres de la Guerra"},
            {
                "text": "Dónde estan las representaciones artísticas de Desastres de la Guerra"
            },
        )

    @patch("rasa_sdk.Action")
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
        )

    @patch("rasa_sdk.Action")
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
        )

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
            > 5
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

    @patch("rasa_sdk.Action")
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
        )

    # TODO Como el nombre esta guardado en formato Apellidos Nombre si hacemos la conslta con Nombre Apellidos no se encuentra nada
    @patch("rasa_sdk.Action")
    def test_ActionTourGuidePhone(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTourGuidePhone(),
                {"person": "Hernández Royo"},
                {"text": "cual es el telefono de la guia turistica Hernández Royo"},
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
                {"text": "cual es el email de la guia turistica Hernández Royo"},
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
                {"person": "Dalda Abril Hilario"},
                {"text": "cual es la web del guia turistico Dalda Abril Hilario"},
            )
            == "La web de Dalda Abril Hilario es www.elandador.es"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTourGuideContactInfo(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionTourGuideContactInfo(),
                {"person": "Dalda Abril Hilario"},
                {
                    "text": "cual es la direccion de contacto del guia turistico Dalda Abril Hilario"
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
                    "text": "cual es la direccion de contacto del guia turistico Sanz Vitalla Pedro"
                },
            )
            == "La información de contacto de Sanz Vitalla Pedro es piter_hu@hotmail.com, 696-145752 / 606-654695, HOYA DE HUESCA/PLANA DE UESCA, SANZ VITALLA PEDRO"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTourOfficePhone(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionTourOfficePhone(),
                {"location": "Zaragoza"},
                {"text": "Teléfonos de las oficinas de turismo de Zaragoza"},
            )
            == "No encuentro el número de télefono de ninguna de las oficinas de Zaragoza"
        )

        assert (
            self.generic(
                ActionTourOfficePhone(),
                {"location": "Teruel"},
                {"text": "Teléfonos de las oficinas de turismo de Teruel"},
            )
            == "Teléfonos de las oficinas de turismo de Teruel:\n\t- PUNTO DE INFORMACION EN DINOPOLIS (POLIGONO LOS PLANOS, S/N (JUNTO A DINOPOLIS)) 978619903"
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
            >= 7
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
