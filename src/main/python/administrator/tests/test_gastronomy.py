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
    #ActionRestaurantsSpots,
    ActionRestaurantLocation,
    ActionRestaurantNumber,
)


class ActionFake:
    def __init__(self):
        self._message = ""


class Dispatcher:
    def __init__(self):
        self._message = ""
        self._text = ""

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
    def test_ActionRestaurantPhone2(self, action):
        action.return_value = ActionFake()
        # Ojo en este caso hay dos respuestas
        assert (
            self.generic(
                ActionRestaurantPhone(),
                {"gastronomy_name": "Lamarsalada"},
                {
                    "intent": {"name": "telefono"},
                    "text": "Cual es el teléfono del restaurante Lamarsalada",
                },
            )
            == "El teléfono de Lamarsalada es 976527171.\nEl teléfono de Lamarsalada es 976223498"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantEmail(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantEmail(),
                {"location": "Fajardo"},
                {"text": "Cual es el email del restaurante Fajardo","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "El email de Fajardo es asadorfajardo@hotmail.com"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantEmail2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantEmail(),
                {"gastronomy_name": "Fajardo"},
                {"text": "Cual es el email del restaurante Fajardo","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "El email de Fajardo es asadorfajardo@hotmail.com"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsList(self, action):
        action.return_value = ActionFake()
        assert ( "Hay cantidad de sitios donde disfrutar tomando algo en Bulbuente. Algunos de ellos, son:"   in
            self.generic(
                ActionRestaurantsList(),
                {"location": "Bulbuente"},
                {"text": "que restaurantes hay en Bulbuente","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsList2(self, action):
        action.return_value = ActionFake()
        assert ( "Hay cantidad de sitios donde disfrutar tomando algo en Bulbuente. Algunos de ellos, son:"   in
            self.generic(
                ActionRestaurantsList(),
                {"gastronomy_name": "Bulbuente"},
                {"text": "que restaurantes hay en Bulbuente","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsList3(self, action):
        action.return_value = ActionFake()
        assert ( "Hay cantidad de sitios donde disfrutar tomando algo en Zuera. Algunos de ellos, son:"   in
            self.generic(
                ActionRestaurantsList(),
                {"location": "Zuera"},
                {"text": "que restaurantes hay en Zuera","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsWeb(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantWeb(),
                {"location": "Basho Cafe"},
                {"text": "Cual es la web del restaurane Basho Cafe","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "La web de Basho Cafe es www.bashogastro.com"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantsWeb2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantWeb(),
                {"gastronomy_name": "Basho Cafe"},
                {"text": "Cual es la web del restaurane Basho Cafe","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "La web de Basho Cafe es www.bashogastro.com"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantAddress(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionRestaurantAddress(),
                        {"location": "El Torreon"},
                        {"text": "Cual es la direccion del restaurante El Torreon","intent_ranking": [{"name": "aragon.ranking_fake"}]},
                    )
            ).splitlines()
            )
            == 1
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantAddress2(self, action):
        action.return_value = ActionFake()
        assert (
            len(
                (
                    self.generic(
                        ActionRestaurantAddress(),
                        {"gastronomy_name": "El Torreon"},
                        {"text": "Cual es la direccion del restaurante El Torreon","intent_ranking": [{"name": "aragon.ranking_fake"}]},
                    )
            ).splitlines()
            )
            == 1
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantReservation(self, action):
        action.return_value = ActionFake()
        assert ( "asadorfajardo@hotmail.com" in
            self.generic(
                ActionRestaurantReservation(),
                {"location": "Fajardo"},
                {"text": "Como puedo reservar en Fajardo","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            #== "Puedes reservar en FAJARDO mandando un email a asadorfajardo@hotmail.com, llamando a 976575763 o yendo a AVDA. MONTAÑANA, 244"
        )
    
    @patch("rasa_sdk.Action")
    def test_ActionRestaurantReservation2(self, action):
        action.return_value = ActionFake()
        assert ( "asadorfajardo@hotmail.com" in
            self.generic(
                ActionRestaurantReservation(),
                {"gastronomy_name": "Fajardo"},
                {"text": "Como puedo reservar en Fajardo","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            #== "Puedes reservar en FAJARDO mandando un email a asadorfajardo@hotmail.com, llamando a 976575763 o yendo a AVDA. MONTAÑANA, 244"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantLocation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantLocation(),
                {"location": "PALENQUE"},
                {"text": "Donde esta el restaurante PALENQUE","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "PALENQUE está en zaragoza"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantLocation2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantLocation(),
                {"gastronomy_name": "PALENQUE"},
                {"text": "Donde esta el restaurante PALENQUE","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "PALENQUE está en zaragoza"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantNumber(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantNumber(),
                {"location": "Borja"},
                {"text": "Cuantos restaurantes hay en Borja","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "En Borja hay 6 sitios donde poder tomar algo"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantNumber2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantNumber(),
                {"location": "Segovia"},
                {"text": "Cuantos restaurantes hay en Segovia","intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Disculpa pero no encuentro cuantos restaurantes/bares hay en Segovia"
        )

    @patch("rasa_sdk.Action")
    def test_ActionRestaurantNumber3(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionRestaurantNumber(),
                {"gastronomy_name": "Segovia"},
                {"text": "Cuantos restaurantes hay en Segovia","intent_ranking": [{"name": "aragon.ranking_fake"}]},
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
