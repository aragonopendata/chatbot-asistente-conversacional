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
from actions_module.gastronomy import (
    ActionRestaurantPhone,
    ActionRestaurantFax,
    ActionRestaurantEmail,
    ActionRestaurantWeb,
    ActionRestaurantAddress,
    ActionRestaurantsList,
    ActionRestaurantReservation,
    ActionRestaurantsSpots,
    ActionRestaurantLocation,
    ActionRestaurantNumber,
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


class ActionGastronomyMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionRestaurantPhone(self, action):
        action.return_value = ActionFake()
        # Ojo en este caso hay dos respuestas
        assert (
            self.generic(
                ActionRestaurantPhone(),
                {"location": "Lamarsalada"},
                {
                    "intent": {"name": "telefono"},
                    "text": "Cual es el teléfono del restaurante Lamarsalada",
                },
            )
            == "El teléfono de Lamarsalada es 976527171.\nEl teléfono de Lamarsalada es 976223498"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantFax(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionRestaurantFax(),
                {"location": "Pepito Casanova"},
                {"text": "Cual es el fax del restaurante Pepito Casanova"},
            )
            == "El fax de Pepito Casanova es 974345223"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantEmail(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantEmail(),
                {"location": "Fajardo"},
                {"text": "Cual es el email del restaurante Fajardo"},
            )
            == "El email de Fajardo es asadorfajardo@hotmail.com"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsWeb(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantWeb(),
                {"location": "Basho Cafe"},
                {"text": "Cual es la web del restaurane Basho Cafe"},
            )
            == "La web de Basho Cafe es www.bashogastro.com"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantAddress(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantAddress(),
                {"location": "Fajardo"},
                {"text": "Cual es la direccion del restaurante Fajardo"},
            )
            == "Fajardo está en AVDA. MONTAÑANA, 244, MONTAÑANA (50059)"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsList(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantsList(),
                {"location": "Bulbuente"},
                {"text": "que restaurantes hay en Bulbuente"},
            )
            == "Los establecimientos de hostelería de BULBUENTE son:\n\t- MESON DEL ACEITE\n\t- EL PARADOR DE BULBUENTE"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantReservation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantReservation(),
                {"location": "Fajardo"},
                {"text": "Como puedo reservar en Fajardo"},
            )
            == "Puedes reservar en FAJARDO mandando un email a asadorfajardo@hotmail.com, llamando a 976575763 o yendo a AVDA. MONTAÑANA, 244"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsSpots(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantsSpots(),
                {"location": "Fajardo"},
                {"text": "Cuantas plazas tiene el restaurante FAJARDO"},
            )
            == "Las plazas de FAJARDO son 56"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantLocation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantLocation(),
                {"location": "PALENQUE"},
                {"text": "Donde esta el restaurante PALENQUE"},
            )
            == "PALENQUE está en ZARAGOZA"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantNumber(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantNumber(),
                {"location": "Borja"},
                {"text": "Cuantos restaurantes hay en Borja"},
            )
            == "En Borja hay 7 sitios donde poder tomar algo"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantNumber2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantNumber(),
                {"location": "Segovia"},
                {"text": "Cuantos restaurantes hay en Segovia"},
            )
            == "Disculpa pero no encuentro cuantos restaurantes/bares hay en Segovia"
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
