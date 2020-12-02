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
from actions_module.aragon import (
    ActionLandUses,
    ActionComarca,
    ActionLandType,
    ActionBuildingAge,
    ActionPopulation,
    ActionCityHallAddress,
    ActionCityHallFax,
    ActionCityHallCIF,
    ActionCityHallPhone,
    ActionCityHallEmail,
    ActionMajor,
    ActionCouncilors,
    ActionNumberContainers,
    ActionGlassKgs,
    ActionSurfaceType2,
    ActionFires,
    ActionSurfaceBurned,
    ActionTreatmentPlants,
    ActionCorpsSector,
    ActionSelfEmployed,
    ActionCorpsSize,
    ActionUnemployment,
    ActionContracts,
    ActionWorkAccidents,
    ActionPerCapitaIncome,
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
    def test_ActionLandUses(self, action):
        action.return_value = ActionFake()

        assert (
            len(
                (
                    self.generic(
                        ActionLandUses(),
                        {"location": "Zaragoza", "number": ""},
                        {"text": "Que usos se la dio al suelo en Zaragoza"},
                    )
                ).splitlines()
            )
            >= 8
        )

        assert (
            self.generic(
                ActionLandUses(),
                {"location": "Zaragoza", "number": "2004"},
                {"text": "Que usos se la dio al suelo en Zaragoza en 2004"},
            )
            == "No se han encontrado datos de los usos que se le da al suelo de Zaragoza en 2004"
        )

        assert (
            self.generic(
                ActionLandUses(),
                {"location": "Aragon", "number": "2000"},
                {"text": "Que usos se la dio al suelo en Aragon en 2000"},
            )
            != "No se han encontrado datos de Aragon en 2000"
        )

    @patch("rasa_sdk.Action")
    def test_ActionComarca(self, action):
        action.return_value = ActionFake()
        poblaciones = [
            {
                "p": "Fraga",
                "r": "Fraga se encuentra en la comarca Bajo Cinca/baix Cinca",
            },
            {
                "p": "Teruel",
                "r": "Teruel se encuentra en la comarca Comunidad de Teruel",
            },
        ]

        for pob in poblaciones:
            assert (
                self.generic(
                    ActionComarca(),
                    {"location": pob["p"]},
                    {"text": "a que comarca pertenece la poblacion de " + pob["p"]},
                )
                == pob["r"]
            )

    # TODO comarca no devuelve suma
    @patch("rasa_sdk.Action")
    def test_ActionLandType(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionLandType(),
                {"location": "Zaragoza", "number": ""},
                {"text": "Cuantas hectareas de suelo rustico hay en Zaragoza"},
            )
            == "En 2016 las hectáreas de suelo rustico en el municipio de Zaragoza son 87293.5\n"
        )
        assert (
            self.generic(
                ActionLandType(),
                {"location": "Huesca", "number": ""},
                {
                    "text": "Cuantas hectareas de suelo rustico hay en la provincia de Huesca"
                },
            )
            == "En 2016 las hectáreas de suelo rustico en la provincia de Huesca son 1554730.0\n"
        )
        # TODO REVISAR respuesta
        """
        assert (
            self.generic(
                ActionLandType(),
                {"location": "Teruel", "number": ""},
                {"text": "Cuantas hectareas de suelo rustico hay en la comarca Teruel"},
            )
            == "Lo siento pero no he encontrado datos del suelo rustico en Teruel en mi base de conocimiento"
        )
        """
        assert (
            self.generic(
                ActionLandType(),
                {"location": "Aragón", "number": "2014"},
                {"text": "Cuantas hectareas de suelo rustico hay en Aragon en 2014 "},
            )
            == "En 2014 las hectáreas de suelo rustico en Aragón son 4721970.0\n"
        )

    # TODO revisar cuando se devuelva bien la respuesta de la query
    @patch("rasa_sdk.Action")
    def test_ActionBuildingAge(self, action):
        action.return_value = ActionFake()
        poblaciones = ["Zaragoza", "Huesca", "Teruel"]

        assert (
            len(
                (
                    self.generic(
                        ActionBuildingAge(),
                        {"location": "Zaragoza"},
                        {
                            "text": "Cual es la fecha de construcción de los edificios de Zaragoza"
                        },
                    )
                ).splitlines()
            )
            >= 13
        )

        assert (
            len(
                (
                    self.generic(
                        ActionBuildingAge(),
                        {"location": "Huesca"},
                        {
                            "text": "Cual es la fecha de construcción de los edificios de Huesca"
                        },
                    )
                ).splitlines()
            )
            >= 13
        )
        assert (
            len(
                (
                    self.generic(
                        ActionBuildingAge(),
                        {"location": "Teruel"},
                        {
                            "text": "Cual es la fecha de construcción de los edificios de la comarca de Teruel"
                        },
                    )
                ).splitlines()
            )
            >= 13
        )

    @patch("rasa_sdk.Action")
    def test_ActionPopulation(self, action):
        action.return_value = ActionFake()
        assert (
                self.generic(
                    ActionPopulation(),
                    {"location": "Teruel", "number": "2005"},
                    {"text": "cuantos habitantes habia en la comarca de Teruel en 2005"},
                )
                == "La población en la comarca de Comunidad De Teruel en 2005 es de 44806 habitantes"
        )
        assert (
            self.generic(
                ActionPopulation(),
                {"location": "Zaragoza", },
                {"text": "Cuantos habitantes hay en Zaragoza en 2018"},
            )
            == "La población en el municipio de Zaragoza en 2018 es de 666880 habitantes"
        )
        assert (
            self.generic(
                ActionPopulation(),
                {"location": "Teruel"},
                {"text": "cuantos habitantes habia en la provincia de Teruel en 2005"},
            )
            == "La población en la provincia de Teruel en 2005 es de 141091 habitantes"
        )



        assert (
            self.generic(
                ActionPopulation(),
                {"location": "Aragon", "number": "2011"},
                {"text": "cuantos habitantes habia en la Aragon en 2011"},
            )
            == "La población en Aragón en 2011 es de 1346293 habitantes"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCityHallAddress(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionCityHallAddress(),
                {"location": "Zaragoza", "number": "","organization":"ayuntamiento de Zaragoza"},
                {"text": "Cual es la direccion del ayuntamiento de Zaragoza"},
            )
            == "El ayuntamiento de Zaragoza está en Pza. del Pilar, 18"
        )

        assert (
            self.generic(
                ActionCityHallAddress(),
                {"location": "Fraga", "number": "","organization":"ayuntamiento de Fraga"},
                {"text": "Cual es la direccion del ayuntamiento de Fraga"},
            )
            == "El ayuntamiento de Fraga está en Pso. Barron 1"
        )
        assert (
            self.generic(
                ActionCityHallAddress(),
                {"location": "Teruel", "number": "2014","organization":"ayuntamiento de Teruel"},
                {"text": "Cual es la direccion del ayuntamiento de Teruel"},
            )
            == "El ayuntamiento de Teruel está en Pza. Catedral, 1"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCityHallFax(self, action):
        action.return_value = ActionFake()
        poblaciones = ["Zaragoza", "Fraga", "Teruel"]

        assert (
            self.generic(
                ActionCityHallFax(),
                {"location": poblaciones[0], "number": ""},
                {"text": "Cual es fax del ayuntamiento de " + poblaciones[0]},
            )
            == "El fax del ayuntamiento de Zaragoza es 976 399 304"
        )

        assert (
            self.generic(
                ActionCityHallFax(),
                {"location": poblaciones[1], "number": ""},
                {"text": "Cual es el fax del ayuntamiento de " + poblaciones[1]},
            )
            == "El fax del ayuntamiento de Fraga es 974 473 081"
        )
        assert (
            self.generic(
                ActionCityHallFax(),
                {"location": poblaciones[2], "number": "2014"},
                {"text": "Cual es el fax del ayuntamiento de " + poblaciones[2]},
            )
            == "El fax del ayuntamiento de Teruel es 978 603 715"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCityHallCIF(self, action):
        action.return_value = ActionFake()
        poblaciones = ["Zaragoza", "Fraga", "Teruel"]

        assert (
            self.generic(
                ActionCityHallCIF(),
                {"location": poblaciones[0], "number": ""},
                {"text": "Cual es el CIF del ayuntamiento de " + poblaciones[0]},
            )
            == "El CIF del ayuntamiento de Zaragoza es P-5030300-G"
        )

        assert (
            self.generic(
                ActionCityHallCIF(),
                {"location": poblaciones[1], "number": ""},
                {"text": "Cual es el CIF del ayuntamiento de " + poblaciones[1]},
            )
            == "El CIF del ayuntamiento de Fraga es P-2215500-F"
        )
        assert (
            self.generic(
                ActionCityHallCIF(),
                {"location": poblaciones[2], "number": "2014"},
                {"text": "Cual es el CIF del ayuntamiento de " + poblaciones[2]},
            )
            == "El CIF del ayuntamiento de Teruel es P-4422900-C"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCityHallPhone(self, action):
        action.return_value = ActionFake()
        poblaciones = ["Zaragoza", "Fraga", "Teruel"]

        assert (
            self.generic(
                ActionCityHallPhone(),
                {"location": poblaciones[0], "number": ""},
                {"text": "Cual es la direccion del ayuntamiento de " + poblaciones[0]},
            )
            == "El teléfono del ayuntamiento de Zaragoza es 976 721 100"
        )

        assert (
            self.generic(
                ActionCityHallPhone(),
                {"location": poblaciones[1], "number": ""},
                {"text": "Cual es la direccion del ayuntamiento de " + poblaciones[1]},
            )
            == "El teléfono del ayuntamiento de Fraga es 974 470 050"
        )
        assert (
            self.generic(
                ActionCityHallPhone(),
                {"location": poblaciones[2], "number": "2014"},
                {"text": "Cual es la direccion del ayuntamiento de " + poblaciones[2]},
            )
            == "El teléfono del ayuntamiento de Teruel es 978 619 900"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCityHallEmail(self, action):
        action.return_value = ActionFake()
        poblaciones = ["Zaragoza", "Fraga", "Teruel"]

        assert (
            self.generic(
                ActionCityHallEmail(),
                {"location": poblaciones[0], "number": ""},
                {"text": "Cual es el email del ayuntamiento de " + poblaciones[0]},
            )
            == "El email del ayuntamiento de Zaragoza es gabinetealcaldia@zaragoza.es"
        )

        assert (
            self.generic(
                ActionCityHallEmail(),
                {"location": poblaciones[1], "number": ""},
                {"text": "Cual es el email del ayuntamiento de " + poblaciones[1]},
            )
            == "El email del ayuntamiento de Fraga es ayuntamiento@fraga.org"
        )
        assert (
            self.generic(
                ActionCityHallEmail(),
                {"location": poblaciones[2], "number": "2014"},
                {"text": "Cual es el email del ayuntamiento de " + poblaciones[2]},
            )
            == "El email del ayuntamiento de Teruel es alcaldia.aytoteruel@teruel.net"
        )

    @patch("rasa_sdk.Action")
    def test_ActionMajor(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionMajor(),
                {"location": "Monzon"},
                {"text": "Como se llama el alcalde de Monzon"},
            )
            == "El alcalde de Monzon es Isaac Claver Ortigosa"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCouncilors(self, action):
        action.return_value = ActionFake()

        assert (
            len(
                (
                    self.generic(
                        ActionCouncilors(),
                        {"location": "Monzon"},
                        {"text": "Como se llaman los concejales  de Monzon"},
                    )
                ).splitlines()
            )
            >= 6
        )

    @patch("rasa_sdk.Action")
    def test_ActionNumberContainers(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionNumberContainers(),
                {"location": "Zaragoza"},
                {"text": "¿Cuántos contenedores de vidrio hay en Zaragoza"},
            )
            == "En el municipio de Zaragoza hay 1721 contenedores de vidrio"
        )
        assert (
            self.generic(
                ActionNumberContainers(),
                {"location": "Teruel"},
                {"text": "¿Cuántos contenedores de vidrio hay en la comarca de Teruel"},
            )
            == "En la comarca de Comunidad de Teruel hay 299 contenedores de vidrio"
        )

        assert (
            self.generic(
                ActionNumberContainers(),
                {"location": "Aragon"},
                {"text": "¿Cuántos contenedores de vidrio hay Aragon"},
            )
            == "En Aragón hay 6287 contenedores de vidrio"
        )

    @patch("rasa_sdk.Action")
    def test_ActionGlassKgs(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionGlassKgs(),
                {"location": "Zaragoza", "number": "2011"},
                {"text": "Cuántos kilos de vidrio se recogieron en 2011 en Zaragoza"},
            )
            == "En el municipio de Zaragoza en 2011 se recogieron 7723760 kilógramos de vidrio"
        )

        assert (
            self.generic(
                ActionGlassKgs(),
                {"location": "Teruel", "number": "2011"},
                {
                    "text": "Cuántos kilos de vidrio se recogieron en 2011 en la comarca de Teruel"
                },
            )
            == "En la comarca de Comunidad de Teruel en 2011 se recogieron 950310 kilógramos de vidrio"
        )

        assert (
            self.generic(
                ActionGlassKgs(),
                {"location": "Aragon", "number": "2011"},
                {"text": "Cuántos kilos de vidrio se recogieron en 2011 en Aragon"},
            )
            == "En Aragón en 2011 se recogieron 23231250 kilógramos de vidrio"
        )

    # TODO revisar Aragon cuando revuelva resultados
    @patch("rasa_sdk.Action")
    def test_ActionSurfaceType2(self, action):
        action.return_value = ActionFake()
        superficies = [
            "superficies artificiales",
            "superficies de agua",
            "zonas agricolas",
            "zonas forestales con vegetacion natural y espacios abiertos",
            "zonas humedas",
        ]

        assert (
            self.generic(
                ActionSurfaceType2(),
                {"location": "Zaragoza"},
                {
                    "text": "cuantas hectareas de superficies artificiales hay la provincia de Zaragoza"
                },
            )
            == "En la provincia de Zaragoza hay 25833.1 hectareas de superficies artificiales"
        )

        assert (
            self.generic(
                ActionSurfaceType2(),
                {"location": "Teruel"},
                {
                    "text": "cuantas hectareas de superficies de agua hay la comarca de Teruel"
                },
            )
            == "En la comarca de Comunidad de Teruel hay 129.668 hectareas de superficies de agua"
        )

        assert (
            self.generic(
                ActionSurfaceType2(),
                {"location": "Zaragoza"},
                {"text": "cuantas hectareas de zonas humedas en Zaragoza"},
            )
            == "En el municipio de Zaragoza hay 27.7697 hectareas de zonas humedas"
        )

        assert (
            self.generic(
                ActionSurfaceType2(),
                {"location": "Zaragoza"},
                {
                    "text": "cuantas hectareas de zonas agricolas hay la provincia de Zaragoza"
                },
            )
            == "En la provincia de Zaragoza hay 1073480.0 hectareas de zonas agricolas"
        )

        assert (
            self.generic(
                ActionSurfaceType2(),
                {"location": "Aragon"},
                {
                    "text": "cuantas hectareas de zonas forestales con vegetacion natural y espacios abiertos hay en Aragon"
                },
            )
            == "En Aragón hay 2370790.0 hectareas de zonas forestales con vegetacion natural y espacios abiertos"
        )

    @patch("rasa_sdk.Action")
    def test_ActionFires(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionFires(),
                {"location": "Zaragoza", "number": "2010"},
                {"text": "Cuantos incendios hubo en Zaragoza en 2010"},
            )
            == "En el municipio de Zaragoza hubo 10 incendios durante el año 2010"
        )

        assert (
            self.generic(
                ActionFires(),
                {"location": "Teruel", "number": "2010"},
                {"text": "Cuantos incendios hubo en la comarca de Teruel en 2010"},
            )
            == "En la comarca de Comunidad de Teruel hubo 11 incendios durante el año 2010"
        )

        assert (
            self.generic(
                ActionFires(),
                {"location": "Aragon", "number": "2010"},
                {"text": "Cuantos incendios hubo en Aragon en 2010"},
            )
            == "En Aragón hubo 342 incendios durante el año 2010"
        )

    @patch("rasa_sdk.Action")
    def test_ActionSurfaceBurned(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionSurfaceBurned(),
                {"location": "Zaragoza", "number": "2010"},
                {"text": "cuantas hectareas se quemaron en Zaragoza en el año 2010"},
            )
            == "En el municipio de Zaragoza se quemaron 3.28 hectáreas durante el año 2010"
        )

        assert (
            self.generic(
                ActionSurfaceBurned(),
                {"location": "Teruel", "number": "2010"},
                {
                    "text": "cuantas hectareas se quemaron la comarca de Teruel en el año 2010"
                },
            )
            == "En la comarca de Comunidad de Teruel se quemaron 22.06 hectáreas durante el año 2010"
        )

        assert (
            self.generic(
                ActionSurfaceBurned(),
                {"location": "Aragon", "number": "2010"},
                {"text": "cuantas hectareas se quemaron en Aragon en el año 2010"},
            )
            == "En Aragón se quemaron 1144.03 hectáreas durante el año 2010"
        )

    @patch("rasa_sdk.Action")
    def test_ActionTreatmentPlants(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionTreatmentPlants(),
                {"location": "Zaragoza", "number": "2014"},
                {
                    "text": "cuantas depuradoras habia en la provincia de Zaragoza en el año 2014"
                },
            )
            == "En la provincia de Zaragoza había 82 plantas depuradoras en 2014"
        )

        assert (
            self.generic(
                ActionTreatmentPlants(),
                {"location": "Aragon", "number": "2014"},
                {"text": "cuantas depuradoras había en Aragón en el año 2014"},
            )
            == "En Aragón había 187 plantas depuradoras en 2014"
        )

    # TODO revisar
    @patch("rasa_sdk.Action")
    def test_ActionCorpsSector(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionCorpsSector(),
                {"location": "Zaragoza"},
                {
                    "text": "Cuántas empresas del sector servicios hay en la provincia de Zaragoza"
                },
            )
            == "En la provincia de Zaragoza hay 1150116 empresas del sector servicios"
        )

        assert (
            self.generic(
                ActionCorpsSector(),
                {"location": "Aragon"},
                {"text": "Cuántas empresas del sector servicios hay en Aragon"},
            )
            == "En Aragón hay 1667893 empresas del sector servicios"
        )

    @patch("rasa_sdk.Action")
    def test_ActionSelfEmployed(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionSelfEmployed(),
                {"location": "Aragon"},
                {
                    "text": "¿Cuántos autónomos hay dados de alta en marzo del 2012 en Aragon?"
                },
            )
            == "En marzo del 2012 había 103638 autónomos dados de alta en Aragón"
        )

        assert (
            self.generic(
                ActionSelfEmployed(),
                {"location": "Teruel"},
                {
                    "text": "¿Cuántos hombres autónomos hay dados de alta en marzo del 2012 en la comarca de Teruel?"
                },
            )
            == "En marzo del 2012 había 2546 hombres autónomos dados de alta en la comarca de Comunidad de Teruel"
        )

        assert (
            self.generic(
                ActionSelfEmployed(),
                {"location": ""},
                {
                    "text": "¿Cuántos mujeres autónomas hay dadas de alta en marzo del 2012?"
                },
            )
            == "En marzo del 2012 había 34458 mujeres autónomas dadas de alta en Aragón"
        )

    @patch("rasa_sdk.Action")
    def test_ActionCorpsSize(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionCorpsSize(),
                {"location": "Teruel"},
                {
                    "text": "Empresas de 1 a 9 trabajadores en marzo de 2012 en la provincia de Teruel"
                },
            )
            == "En 03 de 2012 había en la provincia de Teruel 4254 empresas de 1 a 9 trabajadores"
        )

    # TODO los datos que salen no tienen sentido
    @patch("rasa_sdk.Action")
    def _test_ActionUnemployment(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionUnemployment(),
                {"location": "Zaragoza", "number": "2011"},
                {
                    "text": "¿Cuántos parados hay en el sector servicios en provincia de Zaragoza en 2011?"
                },
            )
            == "En 2011 había 6454377 parados en la provincia de Zaragoza"
        )

        assert (
            self.generic(
                ActionUnemployment(),
                {"location": "Aragón"},
                {"text": "¿Cuántos hombres parados hay en Aragón en  2011?"},
            )
            == ""
        )

        assert (
            self.generic(
                ActionUnemployment(),
                {"location": "Aragón"},
                {"text": "¿Cuántos mujeres paradas hay en Aragón en 2011?"},
            )
            == ""
        )

    @patch("rasa_sdk.Action")
    def test_ActionContracts(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionContracts(),
                {"location": "Jacetania", "number": "2012"},
                {
                    "text": "¿Cuántos nuevos contratos hubo en marzo en marzo de 2012 en la comarca la Jacetania?"
                },
            )
            == "En marzo de 2012 se contrataron 416 personas en la comarca de La Jacetania"
        )
        assert (
            self.generic(
                ActionContracts(),
                {"location": "Jacetania", "number": "2012"},
                {
                    "text": "¿Cuántos nuevos  contratos de hombres hubo en marzo en marzo de 2012 en la comarca la Jacetania?"
                },
            )
            == "En marzo de 2012 se contrataron 201 hombres en la comarca de La Jacetania"
        )
        assert (
            self.generic(
                ActionContracts(),
                {"location": "Jacetania", "number": "2012"},
                {
                    "text": "¿Cuántos nuevos contratos de mujeres hubo en marzo en marzo de 2012 en la comarca la Jacetania?"
                },
            )
            == "En marzo de 2012 se contrataron 215 mujeres en la comarca de La Jacetania"
        )

    @patch("rasa_sdk.Action")
    def test_ActionWorkAccidents(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionWorkAccidents(),
                {"location": "Zaragoza", "number": "2011"},
                {
                    "text": "¿Cuántos accidentes laborales en 2011 en la municipio de Zaragoza?"
                },
            )
            == "En 2011 hubo 2066 accidentes laborales en el municipio de Zaragoza"
        )

        assert (
            self.generic(
                ActionWorkAccidents(),
                {"location": "Zaragoza", "number": "2011"},
                {
                    "text": "¿Cuántos accidentes laborales en 2011 en la provincia de Zaragoza?"
                },
            )
            == "En 2011 hubo 10 accidentes laborales en la provincia de Zaragoza"
        )
        assert (
            self.generic(
                ActionWorkAccidents(),
                {"location": "Teruel", "number": "2011"},
                {
                    "text": "¿Cuántos accidentes laborales en 2011 en la comarca de Teruel?"
                },
            )
            == "En 2011 hubo 133 accidentes laborales en la comarca de Comunidad de Teruel"
        )
        assert (
            self.generic(
                ActionWorkAccidents(),
                {"location": "Aragon", "number": "2011"},
                {"text": "¿Cuántos accidentes laborales en 2011 en Aragon?"},
            )
            == "En 2011 hubo 73 accidentes laborales en Aragón"
        )

    @patch("rasa_sdk.Action")
    def test_ActionPerCapitaIncome(self, action):
        action.return_value = ActionFake()

        assert (
            self.generic(
                ActionPerCapitaIncome(),
                {"location": "Zaragoza"},
                {
                    "text": "¿Cual fue la renta per capita en 2011 en la municipio de Zaragoza?"
                },
            )
            == "En 2011 la renta per capita fue de 17272.7 en el municipio de Zaragoza"
        )

        assert (
            self.generic(
                ActionPerCapitaIncome(),
                {"location": "Zaragoza", "number": "2011"},
                {
                    "text": "¿Cual fue la renta per capita en 2011 en la provincia de Zaragoza?"
                },
            )
            == "En 2011 la renta per capita fue de 15901.2 en la provincia de Zaragoza"
        )
        assert (
            self.generic(
                ActionPerCapitaIncome(),
                {"location": "Teruel", "number": "2011"},
                {
                    "text": "¿Cual fue la renta per capita en 2011 en la comarca de Teruel?"
                },
            )
            == "En 2011 la renta per capita fue de 16471.3 en la comarca de Comunidad de Teruel"
        )
        assert (
            self.generic(
                ActionPerCapitaIncome(),
                {"location": "Aragon", "number": "2011"},
                {"text": "¿Cual fue la renta per capita en 2011 en Aragon?"},
            )
            == "En 2011 la renta per capita fue de 15731.0 en Aragón"
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
