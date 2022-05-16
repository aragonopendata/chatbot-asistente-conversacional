#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import patch
import unittest
from actions_module.accommodation import (
    ActionAccommodationInfo,
    ActionAccommodationList,
    ActionAccommodationReservation,
    ActionAccommodationCategory,
    ActionAccommodationCategoryHigher,
    #ActionAccommodationServices,
    ActionAccommodationNumber,
    #ActionAccommodationNumberRooms,
    #ActionAccommodationNumberRoomsBathroom,
    #ActionAccommodationNumberBeds,
    ActionAccommodationLocation,
    ActionAccommodationsIn,
    #ActionAccommodationSeason,
    #ActionAccommodationRoomsType,
    #ActionApartmentsRuralHouse,
    #ActionApartmentsRooms,
    #ActionAccommodationSize,
    #ActionBungalowsCamping,
    #ActionCaravansCamping,
    #ActionPlotsCamping,
    ActionTravelAgencyInfo,
    #ActionTravelAgencyList,
)


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


class ActionAccomodationMock(unittest.TestCase):
    @patch("rasa_sdk.Action")
    def test_ActionAccommodationInfo(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "El Molino"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual es el web del camping El Molino", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "No he encontrado la información del camping El Molino."

        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "Valle de Tena"},
                {
                    "intent": {"name": "fax"},
                    "text": "Cual es el FAX del camping Valle de Tena", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El fax del camping VALLE DE TENA es 974482551."

        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "Boston"},
                {
                    "intent": {"name": "phone"},
                    "text": "Cual es el teléfono del hotel Boston" , "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El teléfono del hotel EUROSTARS BOSTON es 976599192."
        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "CORONAS"},
                {
                    "intent": {"name": "email"},
                    "text": "Cual es el email del casa rural CORONAS", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El email de la casa rural CORONAS es casacoronas@gmail.com."
        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "ORDESA"},
                {
                    "intent": {"name": "email"},
                    "text": "Cual es el email del casa rural ORDESA", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "No he encontrado la información de la casa rural ORDESA."
        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "CASA MONTSE"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual la Web de los apartamentos CASA MONTSE", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La web del apartamento CASA MONTSE es www.ordesa.net/casa-montse."
        )
        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "REFUGIO DE PINETA"},
                {
                    "intent": {"name": "address"},
                    "text": "Cual la direccion del albergue REFUGIO DE PINETA", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La dirección del albergue REFUGIO DE PINETA es PINETA."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationInf2(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"accomodation_name": "El Molino"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual es el web del camping El Molino", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "No he encontrado la información del camping El Molino."

        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"accomodation_name": "Valle de Tena"},
                {
                    "intent": {"name": "fax"},
                    "text": "Cual es el FAX del camping Valle de Tena", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El fax del camping VALLE DE TENA es 974482551."

        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"accomodation_name": "Boston"},
                {
                    "intent": {"name": "phone"},
                    "text": "Cual es el teléfono del hotel Boston" , "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El teléfono del hotel EUROSTARS BOSTON es 976599192."
        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"accomodation_name": "CORONAS"},
                {
                    "intent": {"name": "email"},
                    "text": "Cual es el email del casa rural CORONAS", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El email de la casa rural CORONAS es casacoronas@gmail.com."
        )
        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"accomodation_name": "CASA MONTSE"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual la Web de los apartamentos CASA MONTSE", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La web del apartamento CASA MONTSE es www.ordesa.net/casa-montse."
        )
        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"accomodation_name": "REFUGIO DE PINETA"},
                {
                    "intent": {"name": "address"},
                    "text": "Cual la direccion del albergue REFUGIO DE PINETA", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La dirección del albergue REFUGIO DE PINETA es PINETA."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationList(self, action):
        action.return_value = ActionFake()
        self.generic(
            ActionAccommodationList(),
            {"location": "Zaragoza"},
            {"text": "lista de campings que hay en el municipio de Zaragoza"},
        )
        self.generic(
            ActionAccommodationList(),
            {"location": "Zaragoza"},
            {"text": "lista de campings que hay en el provincia de Zaragoza"},
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationList2(self, action):
        action.return_value = ActionFake()
        self.generic(
            ActionAccommodationList(),
            {"accomodation_name": "Zaragoza"},
            {"text": "lista de campings que hay en el municipio de Zaragoza"},
        )
        self.generic(
            ActionAccommodationList(),
            {"accomodation_name": "Zaragoza"},
            {"text": "lista de campings que hay en el provincia de Zaragoza"},
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationReservation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "Valle de Tena"},
                {"text": "como puedo reservar el camping Valle de Tena" , "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en camping VALLE DE TENA mandando un email a correo@campipngvalledetena.com o llamando al 974480977."
        )

        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "Boston"},
                {"text": "cual es la categoría del hotel Boston",   "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en hotel EUROSTARS BOSTON mandando un email a direccion@eurostarsboston.com o llamando al 976599192."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "CORONAS"},
                {"text": "como puedo reservar la casa rural CORONAS", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en casa rural CASA EL PAJAR DE CORONAS llamando al 974343072."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "CASA MONTSE"},
                {"text": "como puedo reservar el los apartamentos CASA MONTSE" , "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en apartamento CASA MONTSE mandando un email a casa-montse@ordesa.com o llamando al 974486243."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "REFUGIO DE PINETA"},
                {"text": " como puedo reservar el albergue REFUGIO DE PINETA", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en albergue REFUGIO DE PINETA mandando un email a refugiopineta@hotmail.com o llamando al 974501203."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationReservation2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"accomodation_name": "Valle de Tena"},
                {"text": "como puedo reservar el camping Valle de Tena" , "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en camping VALLE DE TENA mandando un email a correo@campipngvalledetena.com o llamando al 974480977."
        )

        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"accomodation_name": "Boston"},
                {"text": "cual es la categoría del hotel Boston",   "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en hotel EUROSTARS BOSTON mandando un email a direccion@eurostarsboston.com o llamando al 976599192."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"accomodation_name": "CORONAS"},
                {"text": "como puedo reservar la casa rural CORONAS", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en casa rural CASA EL PAJAR DE CORONAS llamando al 974343072."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"accomodation_name": "CASA MONTSE"},
                {"text": "como puedo reservar el los apartamentos CASA MONTSE" , "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en apartamento CASA MONTSE mandando un email a casa-montse@ordesa.com o llamando al 974486243."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"accomodation_name": "REFUGIO DE PINETA"},
                {"text": " como puedo reservar el albergue REFUGIO DE PINETA", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Puedes reservar en albergue REFUGIO DE PINETA mandando un email a refugiopineta@hotmail.com o llamando al 974501203."
        )

    """@patch("rasa_sdk.Action")
    def test_ActionAccommodationCategory(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationCategory(),
                {"location": "Boston"},
                {"text": "cual es la categoría del hotel Boston",   "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Eurostars Boston-eurostars tiene 4 estrellas."
        )"""

    """@patch("rasa_sdk.Action")
    def test_ActionAccommodationCategoryHigher(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationCategoryHigher(),
                {"location": "Zaragoza", "number": 5},
                {"text": "que hoteles tienen 5 estrellas en La provincia de Zaragoza","entities":
                [{'confidence': 0.9, 'depth': 0, 'duckValue': {'type': 'value', 'value': 5.0}, 'end': 20,
                  'entity': 'number', 'start': 19, 'value': '5'},
                 {'confidence': 1.0, 'depth': 0, 'end': 36, 'entity': 'misc', 'start': 34, 'value': 'La'},
                 {'confidence': 1.0, 'depth': 0, 'dictionary': 'extra', 'end': 46, 'entity': 'location', 'start': 37,
                  'value': 'provincia'},
                 {'confidence': 1.4651487731933595, 'depth': 0, 'end': 58, 'entity': 'location', 'start': 50,
                  'value': 'Zaragoza'}]}
            )
            == "La lista de hoteles con categoria mayor de 5 en Zaragoza es:\n\t- PALAFOX-PALAFOX HOTELES\n\t- REINA PETRONILA -PALAFOX"
        )"""

    """@patch("rasa_sdk.Action")
    def test_ActionAccommodationRooms(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationRoomsType(),
                {"location": "Boston", "organization":None},
                {
                    "intent": {"name": "4p"},
                    "text": "cuantas habitaciones para 4 personas tiene el hotel Boston", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "En hotel EUROSTARS BOSTON-EUROSTARS hay 285 habitaciones cuádruples."
        )"""
    @patch("rasa_sdk.Action")
    def test_ActionAccommodationNumber(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationNumber(),
                {"location": "Torla"},
                {"text": "Cuantas casas rurales hay en Torla", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "En el municipio de Torla hay 1 casas rurales"
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationNumber2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationNumber(),
                {"accomodation_name": "Torla"},
                {"text": "Cuantas casas rurales hay en Torla", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "En el municipio de Torla hay 1 casas rurales"
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationLocation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationLocation(),
                {"location": "Palafox"},
                {"text": "donde esta el hotel Palafox", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "PALAFOX está en barbastro."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationLocation2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationLocation(),
                {"accomodation_name": "Palafox"},
                {"text": "donde esta el hotel Palafox", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "PALAFOX está en barbastro."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationsIn(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationsIn(),
                {"location": "Tarazona"},
                {"text": "Listado de hoteles de Tarazona", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "En Tarazona te puedes alojar en los siguientes hoteles\n\t- ENCANTO TARAZONA\n\t- ENCANTO TARAZONA\n\t- ENCANTO TARAZONA"
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationsIn2(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationsIn(),
                {"accomodation_name": "Tarazona"},
                {"text": "Listado de hoteles de Tarazona", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "En Tarazona te puedes alojar en los siguientes hoteles\n\t- ENCANTO TARAZONA\n\t- ENCANTO TARAZONA\n\t- ENCANTO TARAZONA"
        )

    """@patch("rasa_sdk.Action")
    def test_ActionAccommodationRoomsType(self, action):
        action.return_value = ActionFake()
        import re

        message = self.generic(
                ActionAccommodationRoomsType(),
                {"location": "Boston", "organization": None},
                {"text": "Habitaciones sencillas en el hotel Boston", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
        assert (
           message.startswith('En hotel EUROSTARS BOSTON-EUROSTARS hay')
           and message.endswith("habitaciones sencillas.")
           and bool(re.search(r"\d",message ))
        )"""

    """@patch("rasa_sdk.Action")
    def test_ActionBungalowsCamping(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionBungalowsCamping(),
                {"location": "Camping Gavin"},
                {"text": "Cuantas bungalows tiene el Camping Gavin", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Camping Gavin, S.l.-gavin tiene 114 bungalows."
        )"""

    """@patch("rasa_sdk.Action")
    def test_ActionCaravansCamping(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionCaravansCamping(),
                {"location": "Camping Ainsa"},
                {"text": "Cuantas plazas para caravanas tiene el Camping Ainsa" , "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Camping Ainsa, S.l.-ainsa tiene 16 plazas para caravanas."
        )"""

    """@patch("rasa_sdk.Action")
    def test_ActionPlotsCamping(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionPlotsCamping(),
                {"location": "Camping Ainsa"},
                {"text": "Cuantas parcelas tiene el Camping Ainsa", "intent_ranking": [{"name": "aragon.ranking_fake"}]},
            )
            == "Camping Ainsa, S.l.-ainsa tiene 125 parcelas."
        )"""

    @patch("rasa_sdk.Action")
    def test_ActionTravelAgencyInfo(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "ORDESA"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual es la web de la agencia de viajes ORDESA",   "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "Lo siento pero no he encontrado la web de la agencia de viajes ORDESA"
        )

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "BALCÓN DEL PIRINEO RURAL ORDESA"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual es la web de la agencia de viajes BALCÓN DEL PIRINEO RURAL ORDESA",   "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "Lo siento pero no he encontrado la web de la agencia de viajes BALCÓN DEL PIRINEO RURAL ORDESA"
        )

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "phone"},
                    "text": "Cual es el teléfono de la agencia de viajes LAS FEIXAS TREKKING",   "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El teléfono de la agencia de viajes LAS FEIXAS TREKKING, S.L. es 661472073."
        )

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "email"},
                    "text": "Cual es el email de la agencia de viajes LAS FEIXAS TREKKING",  "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El email de la agencia de viajes LAS FEIXAS TREKKING, S.L. es lasfeixas@gmail.com."
        )
        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual la Web de la agencia de viajes LAS FEIXAS TREKKING", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La web de la agencia de viajes LAS FEIXAS TREKKING, S.L. es https://lasfeixas.com."
        )
        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "address"},
                    "text": "Cual la direccion de la agencia de viajes LAS FEIXAS TREKKING, S.L.", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La dirección de la agencia de viajes LAS FEIXAS TREKKING, S.L. es C/ Calvario, 22."
        )

    @patch("rasa_sdk.Action")
    def test_ActionTravelAgencyInfo2(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"accomodation_name": "ORDESA"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual es la web de la agencia de viajes ORDESA",   "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "Lo siento pero no he encontrado la web de la agencia de viajes ORDESA"
        )

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"accomodation_name": "BALCÓN DEL PIRINEO RURAL ORDESA"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual es la web de la agencia de viajes BALCÓN DEL PIRINEO RURAL ORDESA",   "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "Lo siento pero no he encontrado la web de la agencia de viajes BALCÓN DEL PIRINEO RURAL ORDESA"
        )

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"accomodation_name": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "phone"},
                    "text": "Cual es el teléfono de la agencia de viajes LAS FEIXAS TREKKING",   "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El teléfono de la agencia de viajes LAS FEIXAS TREKKING, S.L. es 661472073."
        )

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"accomodation_name": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "email"},
                    "text": "Cual es el email de la agencia de viajes LAS FEIXAS TREKKING",  "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "El email de la agencia de viajes LAS FEIXAS TREKKING, S.L. es lasfeixas@gmail.com."
        )
        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"accomodation_name": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual la Web de la agencia de viajes LAS FEIXAS TREKKING", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La web de la agencia de viajes LAS FEIXAS TREKKING, S.L. es https://lasfeixas.com."
        )
        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"accomodation_name": "LAS FEIXAS TREKKING"},
                {
                    "intent": {"name": "address"},
                    "text": "Cual la direccion de la agencia de viajes LAS FEIXAS TREKKING, S.L.", "intent_ranking": [{"name": "aragon.ranking_fake"}]
                },
            )
            == "La dirección de la agencia de viajes LAS FEIXAS TREKKING, S.L. es C/ Calvario, 22."
        )

    """@patch("rasa_sdk.Action")
    def test_ActionTravelAgencyList(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionTravelAgencyList(),
                {"location": "Barbastro"},
                {"text": "que agencias de Viajes hay que Barbastro", "intent_ranking": [{"name": "aragon.ranking_fake"}] },
            )
            == "En Barbastro hay las siguientes agencias de viaje \n\t- ENOARTE, ENOLOGIA Y TURISMO S.L.\n\t- TORNAMON VIAJES, S.L.\n\t- GUARA TOURS S.L.\n\t- EL CÍRCULO TRAVEL"
        )"""

    @staticmethod
    def generic(action, slot, message,entities=None):
        print(message)
        dispatcher = Dispatcher()
        tracker = Tracker()
        tracker.set_slot(slot)
        tracker.set_latest_message(message)
        action.run(dispatcher, tracker, None)
        print(dispatcher.get_message())
        return dispatcher.get_message() #.rstrip(".")
