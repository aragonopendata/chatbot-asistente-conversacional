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
from actions_module.accommodation import (
    ActionAccommodationInfo,
    ActionAccommodationList,
    ActionAccommodationReservation,
    ActionAccommodationCategory,
    ActionAccommodationCategoryHigher,
    ActionAccommodationServices,
    ActionAccommodationNumber,
    ActionAccommodationNumberRooms,
    ActionAccommodationNumberRoomsBathroom,
    ActionAccommodationNumberBeds,
    ActionAccommodationLocation,
    ActionAccommodationsIn,
    ActionAccommodationSeason,
    ActionAccommodationRoomsType,
    ActionApartmentsRuralHouse,
    ActionApartmentsRooms,
    ActionAccommodationSize,
    ActionBungalowsCamping,
    ActionCaravansCamping,
    ActionPlotsCamping,
    ActionTravelAgencyInfo,
    ActionTravelAgencyList,
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
                {"location": "Valle de Tena"},
                {
                    "intent": {"name": "fax"},
                    "text": "Cual es el FAX del camping Valle de Tena",
                },
            )
            == "El fax del camping CAMPING VALLE DE TENA, S.L.-VALLE DE TENA es 974482551."

        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "Boston"},
                {
                    "intent": {"name": "phone"},
                    "text": "Cual es el teléfono del hotel Boston",
                },
            )
            == "El teléfono del hotel EUROSTARS BOSTON-EUROSTARS es 976599192."
        )

        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "Casa Jaime"},
                {
                    "intent": {"name": "email"},
                    "text": "Cual es el email del casa rural Casa Jaime",
                },
            )
            == "El email de la casa rural CASA JAIME es mbalet@hotmail.es."
        )
        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "Casa Modesto"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual la Web de los apartamentos Casa Modesto",
                },
            )
            == "La web del apartamento CASA MODESTO es www.apartamentoscasamodesto.com."
        )
        assert (
            self.generic(
                ActionAccommodationInfo(),
                {"location": "Hermanos Nerin"},
                {
                    "intent": {"name": "address"},
                    "text": "Cual la direccion del albergue Hermanos Nerin",
                },
            )
            == "La dirección del albergue HERMANOS NERIN, S.C. es C/. FRANCIA, TORLA (22376)."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationList(self, action):
        action.return_value = ActionFake()
        self.generic(
            ActionAccommodationList(),
            {"location": "Zaragoza"},
            {"text": "lista de camping que hay en la provincia de Zaragoza"},
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationReservation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "Valle de Tena"},
                {"text": "como puedo reservar el camping Valle de Tena"},
            )
            == "Puedes reservar en camping CAMPING VALLE DE TENA, S.L.-VALLE DE TENA mandando un email a correo@campipngvalledetena.com o llamando al 974480977."
        )

        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "Boston"},
                {"text": "cual es la categoría del hotel Boston"},
            )
            == "Puedes reservar en hotel EUROSTARS BOSTON-EUROSTARS mandando un email a direccion@eurostarsboston.com o llamando al 976599192."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "Casa Jaime"},
                {"text": "como puedo reservar la casa rural Casa Jaime"},
            )
            == "Puedes reservar en casa rural CASA JAIME mandando un email a mbalet@hotmail.es o llamando al 654176203."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "PUERTA DE ORDESA"},
                {"text": "como puedo reservar el los apartamentos PUERTA DE ORDESA"},
            )
            == "Puedes reservar en apartamento PUERTA DE ORDESA mandando un email a amayatv@hotmail.com o llamando al 974505101."
        )
        assert (
            self.generic(
                ActionAccommodationReservation(),
                {"location": "ANZÁNIGO"},
                {"text": " como puedo reservar el albergue ANZÁNIGO"},
            )
            == "Puedes reservar en albergue ANZÁNIGO, S.L. mandando un email a info@anzanigo.com o llamando al 974348040."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationCategory(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationCategory(),
                {"location": "Boston"},
                {"text": "cual es la categoría del hotel Boston"},
            )
            == "Eurostars Boston-eurostars tiene 4 estrellas."
        )

    @patch("rasa_sdk.Action")
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
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationRooms(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationRoomsType(),
                {"location": "Boston"},
                {
                    "intent": {"name": "4p"},
                    "text": "cuantas habitaciones para 4 personas tiene el hotel Boston",
                },
            )
            == "El número de habitaciones cuadruples del hotel Boston es 285."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationServices(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationServices(),
                {"location": "PARIS CENTRO"},
                {"text": "que servicios proporciona el hotel PARIS CENTRO"},
            )
            == "Los servicios de PARIS CENTRO son:\n\t- Restaurante"
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationNumber(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationNumber(),
                {"location": "Torla"},
                {"text": "Cuantas casas rurales hay en Torla"},
            )
            == "En el municipio de Torla hay 19 casas rurales"
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationNumberRooms(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationNumberRooms(),
                {"location": "Boston"},
                {"text": "Cuantas habitaciones tiene el hotel Boston"},
            )
            == "En Eurostars Boston-eurostars hay 313 habitaciones."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationNumberRoomsBathroom(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationNumberRoomsBathroom(),
                {"location": "LOS HERREROS"},
                {"text": "Cuantas habitaciones sin baño hay el hotel LOS HERREROS"},
            )
            == "En Los Herreros hay 5 habitaciones sin baño."
        )
        assert (
            self.generic(
                ActionAccommodationNumberRoomsBathroom(),
                {"location": "LOS HERREROS"},
                {"text": "Cuantas habitaciones con baño hay el hotel LOS HERREROS"},
            )
            == "En Los Herreros hay 15 habitaciones con baño."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationNumberBeds(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationNumberBeds(),
                {"location": "Zaragoza"},
                {"text": "Cuantas plazas hoteleras hay en Zaragoza"},
            )
            == "Lo siento pero no tengo información del número de camas del hotel Zaragoza."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationLocation(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationLocation(),
                {"location": "Palafox"},
                {"text": "donde esta el hotel Palafox"},
            )
            == "PALAFOX está en BARBASTRO."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationsIn(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationsIn(),
                {"location": "Tarazona"},
                {"text": "Listado de hoteles de Tarazona"},
            )
            == "En Tarazona te puedes alojar en los siguientes hoteles\n\t- CONDES DE VISCONTI\n\t- LA MERCED DE LA CONCORDIA\n\t- BRUJAS IRUES\n\t- PALACETE DE LOS ARCEDIANOS\n\t- SANTA AGUEDA"
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationSeason(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationSeason(),
                {"location": "CAMPING VALLE DE TENA"},
                {"text": "Temporada baja en el camping CAMPING VALLE DE TENA"},
            )
            == "En CAMPING VALLE DE TENA, S.L.-VALLE DE TENA es temporada baja desde 01/10 hasta 30/11."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationRoomsType(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationRoomsType(),
                {"location": "Boston"},
                {"text": "Habitaciones sencillas en el hotel Boston"},
            )
            == "En EUROSTARS BOSTON-EUROSTARS hay 28 habitaciones sencillas."
        )

    @patch("rasa_sdk.Action")
    def test_ActionAccommodationRoomsType(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationRoomsType(),
                {"location": "Boston"},
                {"text": "Habitaciones sencillas en el hotel Boston"},
            )
            == "En hotel EUROSTARS BOSTON-EUROSTARS hay 28 habitaciones sencillas."
        )

    @patch("rasa_sdk.Action")
    def test_ActionApartmentsRuralHouse(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionApartmentsRuralHouse(),
                {"location": "CASA BROTO"},
                {"text": "Cuantos apartamentos tiene Casa Broto"},
            )
            == "Casa Broto tiene 1 apartamentos."
        )

    @patch("rasa_sdk.Action")
    def test_ActionApartmentsRooms(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionApartmentsRooms(),
                {"location": "CASA JAIME"},
                {"text": "Cuantas habitaciones dobles tiene Casa Jaime"},
            )
            == "Casa Jaime tiene 5 habitaciones dobles."
        )

    @patch("rasa_sdk.Action")
    def test_ActionRuralHouseSize(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionAccommodationSize(),
                {"location": "Casa del Cura"},
                {"text": "Cuantas plazas tiene la casa rural Casa del Cura"},
            )
            == "La casa rural CASA DEL CURA tiene 4 plazas."
        )

    @patch("rasa_sdk.Action")
    def test_ActionBungalowsCamping(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionBungalowsCamping(),
                {"location": "Camping Gavin"},
                {"text": "Cuantas bungalows tiene el Camping Gavin"},
            )
            == "Camping Gavin, S.l.-gavin tiene 114 bungalows."
        )

    @patch("rasa_sdk.Action")
    def test_ActionCaravansCamping(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionCaravansCamping(),
                {"location": "Camping Ainsa"},
                {"text": "Cuantas plazas para caravanas tiene el Camping Ainsa"},
            )
            == "Camping Ainsa, S.l.-ainsa tiene 16 plazas para caravanas."
        )

    @patch("rasa_sdk.Action")
    def test_ActionPlotsCamping(self, action):
        action.return_value = ActionFake()
        assert (
            self.generic(
                ActionPlotsCamping(),
                {"location": "Camping Ainsa"},
                {"text": "Cuantas parcelas tiene el Camping Ainsa"},
            )
            == "Camping Ainsa, S.l.-ainsa tiene 125 parcelas."
        )

    @patch("rasa_sdk.Action")
    def test_ActionTravelAgencyInfo(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "Unión del Valle Viajes"},
                {
                    "intent": {"name": "phone"},
                    "text": "Cual es el teléfono de la agencia de viajes Unión del Valle Viajes",
                },
            )
            == "El teléfono de la agencia de viajes UNIÓN DEL VALLE VIAJES es 628-158516."
        )

        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "Viaser"},
                {
                    "intent": {"name": "email"},
                    "text": "Cual es el email de la agencia de viajes Viaser",
                },
            )
            == "El email de la agencia de viajes VIASER es info@viaserviajes.com."
        )
        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "Viajar por Aragon"},
                {
                    "intent": {"name": "web"},
                    "text": "Cual la Web de la agencia de viajes Viajar por Aragon",
                },
            )
            == "La web de la agencia de viajes VIAJAR POR ARAGON es www.viajarporaragon.com."
        )
        assert (
            self.generic(
                ActionTravelAgencyInfo(),
                {"location": "Viajes Male"},
                {
                    "intent": {"name": "address"},
                    "text": "Cual la direccion de la agencia de viajes Viajes Male",
                },
            )
            == "La dirección de la agencia de viajes VIAJES MALE, S.L.L. es Avda. La Jota, 57, ZARAGOZA (50014)."
        )

    @patch("rasa_sdk.Action")
    def test_ActionTravelAgencyList(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionTravelAgencyList(),
                {"location": "Barbastro"},
                {"text": "que agencias de Viajes hay que Barbastro"},
            )
            == "En Barbastro hay las siguientes agencias de viaje \n\t- ENOARTE, ENOLOGIA Y TURISMO S.L.\n\t- TORNAMON VIAJES, S.L.\n\t- GUARA TOURS S.L.\n\t- EL CÍRCULO TRAVEL"
        )

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
