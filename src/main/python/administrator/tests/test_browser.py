'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from browser import Browser


class ActionBrowser(unittest.TestCase):
    buscador = Browser()

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.maxDiff = None

    """def test_Hotel_Categoria(self):

        results = self.buscador.search(
            {
                "question": "Que hoteles  con categoria 2 o superior hay en Zaragoza",
                "intents": ["alojamientoCiudad", "tipoAlojamiento", "categoria"],
                "entities": ["Zaragoza", "hotel", "2"],
            }
        )
        self.assertTrue (len(results ) >40)"""

    """def test_Hotel_Terraza(self):

        results =  self.buscador.search(
        {
            "question": "Cuantas habitaciones con terraza tiene el hotel SOMMOS HOTEL BENASQUE",
            "intents": [
                "habitacionesTerrazaHotel",
                "tipoAlojamiento",
                "tipoHabitacion",
            ],
            "entities": ["SOMMOS HOTEL BENASQUE", "hotel"],
        }
        )
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""


    def test_comarca(self):
       results =  self.buscador.search({"question":"A qué comarca pertenece el municipio Teruel","intents":["ComarcaMunicipio"], "entities":["Teruel"]} )
       self.assertTrue  (results[0].get("answer0") == "Comunidad de Teruel")


    def test_superficie(self):
       results =  self.buscador.search({"question": "Cuál es la superficie de Zaragoza", "intents": ["SuperficieMunicipio"], "entities": ["Zaragoza"]})
       self.assertTrue  (float(results[0].get("answer0"))  > 100 )#973.7

    def test_Habitantes(self):
       results =  self.buscador.search({"question": "Cuántos habitantes hay en Añon", "intents": ["HabitantesMunicipio"], "entities": ["Añon"]})
       self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_Secano(self):
       results =  self.buscador.search({"question": "Cuál es la superficie total de secano en Zaragoza en el año 2006", "intents": ["SuperficieSecano", "Year"], "entities": ["Zaragoza", "2006"]})
       self.assertTrue  (float(results[0].get("answer0"))  > 10000 )#16778.8

    def test_regadio(self):
       results =  self.buscador.search({"question": "Cuál es la superficie total de regadío en Zaragoza en el año 2006", "intents": ["SuperficieRegadio", "Year"], "entities": ["Zaragoza", "2006"]})
       self.assertTrue  (float(results[0].get("answer0"))  > 10000 )#14643

    def test_poblacion(self):
       results =  self.buscador.search({"question": "Cuál era la población de Añon en el año 2019", "intents": ["Poblacion", "Year"], "entities": ["Añon", "2019"]})
       self.assertTrue  (int(results[0].get("answer0")) ) # 2012 ->213 2019-> 231

    def test_cif_ayuntamiento(self):
       results =  self.buscador.search({"question": "Cuál es el CIF del ayuntamiento de Zaragoza", "intents": ["CIFAyuntamiento"], "entities": ["Zaragoza"]})
       self.assertTrue  (len(results[0].get("answer0"))  > 7)#P-5030300-G

    def test_tlf_ayuntamiento(self):
       results =  self.buscador.search({"question": "Cuál es el teléfono del ayuntamiento de Zaragoza", "intents": ["TelefonoAyuntamiento"], "entities": ["Zaragoza"]})
       self.assertTrue (len(results[0].get("answer0"))  >= 9)

    def test_email_ayuntamiento(self):
       results =  self.buscador.search({"question": "Cuál es el email del ayuntamiento de Zaragoza", "intents": ["EmailAyuntamiento"], "entities": ["Zaragoza"]})
       self.assertTrue  ("@" in results[0].get("answer0"))

    def test_alcalde_ayuntamiento(self):
       results =  self.buscador.search({"question": "Quién es el alcalde del municipio de Zaragoza", "intents": ["Cargo", "Municipio"], "entities": ["Alcalde", "Zaragoza"]})
       self.assertTrue (len(results[0].get("answer0"))  > 10)#'JORGE ANTONIO AZCON NAVARRO'

    def test_concejales_ayuntamiento(self):
       results =  self.buscador.search({"question": "Quiénes son los concejales del municipio de Zaragoza", "intents": ["Cargo", "Municipio"],"entities": ["Concejal", "Zaragoza"]})
       self.assertTrue  (len(results[0].get("answer0"))  > 10)

    def test_fax_ayuntamiento(self):
        results =  self.buscador.search({"question": "Cuál es el fax del ayuntamiento de Zaragoza", "intents": ["FaxAyuntamiento"],"entities": ["Zaragoza"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 8)

    def test_address_ayuntamiento(self):
        results =  self.buscador.search({"question": "Cuál es la dirección del ayuntamiento de Zaragoza", "intents": ["DireccionAyuntamiento"], "entities": ["Zaragoza"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#'PZA. DEL PILAR, 18'

    # Gastronomía
    def test_restaurant_tlf(self):
        results = self.buscador.search(
        {"question": "Cuál es el telefono del restaurante/cafetería Ginos Grancasa", "intents": ["telefonoRestaurante"],
                      "entities": ["Ginos Grancasa"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 8)

    def test_restaurant_fax(self):
        results = self.buscador.search(
        {"question": "Cuál es el fax del restaurante/cafetería Ginos Grancasa", "intents": ["faxRestaurante"],
        "entities": ["Pista Grande"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_restaurant_email(self):
        results = self.buscador.search(
        {"question": "Cuál es el email del restaurante/cafetería Ginos Grancasa", "intents": ["emailRestaurante"],
        "entities": ["Ginos Grancasa"]})
        self.assertTrue  ("@" in results[0].get("answer0"))

    def test_restaurant_web(self):
        results = self.buscador.search(
        {"question": "Cuál es la pagina web del restaurante/cafetería Ginos Grancasa", "intents": ["webRestaurante"],
          "entities": ["MUERDE LA PASTA - GRANCASA"]})
        self.assertTrue  ("WWW" in results[0].get("answer0").upper())

    def test_restaurant_address(self):
        results = self.buscador.search({"question": "Cuál es la direccion del restaurante/cafetería Ginos Grancasa", "intents": ["direccionRestaurante"],
          "entities": ["Ginos Grancasa"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)

    def test_restaurant_ciudad(self):
        results = self. buscador.search(
        {"question": "Restaurantes/cafeterías en Zaragoza", "intents": ["restaurantesCiudad"],
        "entities": ["Zaragoza"]})
        print(results)
        self.assertTrue  (len(results)  > 2)#'LOS AMIGOS'

    """
    def test_restaurant_reserva(self):
        results = self.buscador.search(
         {"question": "Como puedo reservar en el restaurante Ginos Grancasa", "intents": ["reservaRestaurante"],
          "entities": ["Ginos Grancasa"]})
        print(results)
        self.assertTrue  (int(results[0].get("answer0"))  > 1)#NoneType ??
    """

    """def test_restaurant_plazas(self):
        results = self.buscador.search(
        {"question": "Cuantas plazas tiene el restaurante Ginos Grancasa", "intents": ["plazasRestaurante"],
          "entities": ["Ginos Grancasa"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""


    def test_restaurant_numero(self):
        results = self.buscador.search(
        {"question": "Restaurantes en el municipio Zaragoza", "intents": ["numRestaurantes"],
         "entities": ["Zaragoza"]})
        self.assertTrue  (int(results[1].get("answer0"))  > 1)

    def test_restaurant_municipio(self):
        results = self.buscador.search(
            {"question": "Ciudad del restaurante Ginos Grancasa", "intents": ["municipioRestaurante"],
            "entities": ["GINOS GRANCASA"]})
        self.assertTrue ( "ZARAGOZA" in results[0].get("answer0").upper())#'ZARAGOZA'

    # Actividades

    """def test_actividades_obras(self):
        results = self.buscador.search(
        {"question": "Que obras tiene el museo diocesano de Jaca", "intents": ["obrasMuseo"],
        "entities": ["Museo Diocesano de Jaca"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#Abrazo en la puerta dorada"""

    def test_actividades_museos(self):
        results = self.buscador.search(
        {"question": "Que museos hay en Zaragoza", "intents": ["museosLocalidad"],
                      "entities": ["Zaragoza"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#IES Ramon y Cajal de Huesca'

    """def test_actividades_obra_lugar(self):
        results = self.buscador.search(
         {"question": "Donde se encuentra la obra Abrazo en la puerta dorada", "intents": ["municipioObra"],
                      "entities": ["Abrazo en la puerta dorada"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#DAN Centro de Arte y Naturaleza Fundacion Beulas"""


    """def test_actividades_rutas_origen(self):
        results = self.buscador.search(
        {"question": "Que rutas salen de Fraga", "intents": ["rutasOrigen"],
                      "entities": ["Teruel"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#018 TERUEL-ZARAGOZA (POR MONREAL DEL CAMPO)"""

    """def test_actividades_rutas_destino(self):
        results = self.buscador.search(
         {"question": "Que rutas llegan a Borja", "intents": ["rutasDestino"],
                      "entities": ["Borja"]})
        self.assertTrue  ("BORJA" in (results[0].get("answer0")).upper() )#NOVILLAS-BORJA"""

    def test_actividades_rutas_camino(self):
        results = self.buscador.search(
         {"question": "Que rutas pasan por Utebo", "intents": ["rutasCamino"],
                      "entities": ["Jaca"]})
        self.assertTrue  ("JACA" in (results[2].get("answer0")).upper()  )#'001 ZARAGOZA - UTEBO - MONZALBARBA - ZARAGOZA'

    """def test_actividades_rutas_origen_destino(self):
        results = self.buscador.search(
         {"question": "Que rutas salen de Teruel y llega a Zaragoza", "intents": ["rutasOrigen", "rutasDestino"],
                      "entities": ["Teruel", "Zaragoza"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#'018 TERUEL-ZARAGOZA (POR MONREAL DEL CAMPO)'"""

    """def test_actividades_rutas_guias(self):
        results = self.buscador.search(
         {"question": "Que guías de turismo hay en Borja", "intents": ["guiasLocalidad"],
                      "entities": ["Borja"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#DEL RIO SANTA CECILIA Mª. NOELIA'"""

    def test_actividades_rutas_guias_tlf(self):
        results = self.buscador.search(
        {"question": "Cual es el telefono del guia de turismo RAMOS MONGE DIEGO", "intents": ["telefonoGuia"],
                     "entities": ["RAMOS MONGE DIEGO"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#'91-4096916 / 658-994863'

    def test_actividades_rutas_guias_email(self):
        results = self. buscador.search(
        {"question": "Cual es el email del guia de turismo RAMOS MONGE DIEGO", "intents": ["emailGuia"],
                     "entities": ["RAMOS MONGE DIEGO"]})
        self.assertTrue  ("@" in results[0].get("answer0"))

    def test_actividades_guias_web(self):
        results = self.buscador.search(
        {"question": "Cual es la web del guia de turismo SOLANAS AÍSA BLANCA", "intents": ["webGuia"],
                     "entities": ["SOLANAS AÍSA BLANCA"]})
        self.assertTrue  ("WWW" in results[0].get("answer0").upper()) #www.llevartehuesca.es

    # test que falla si el nombre del guia no se introduce exactamente igual que esta en la base de datos "2 espacios en blanco" correctamente
    def test_actividades_guias_contacto(self):
        results = self.buscador.search(
        {"question": "Cual es la informacion de contacto del guia turistico AMBROJ  MARTÍN MARÍA JESÚS", "intents": ["informacionGuia"],
                     "entities": ["AMBROJ  MARTÍN MARÍA JESÚS"]})
        self.assertTrue  ("@" in results[0].get("answer0"))# and ("AMBROJ MARTÍN MARÍA JESÚS" in results[0].get("etiqueta"))#NoneType

    def test_actividades_guias_tlf(self):
        results = self.buscador.search(
        {"question": "Cual es el telefono de la oficina de turismo de Teruel", "intents": ["telefonoTurismo"],
                     "entities": ["Teruel"]})
        self.assertTrue  ("TERUEL" in results[0].get("answer0").upper())##OFICINA DE TURISMO DE TERUEL

    def test_actividades_oficina_direccion(self):
        results = self.buscador.search(
        {"question": "Donde esta la oficina de turismo de Zaragoza", "intents": ["direccionTurismo"],
                     "entities": ["Zaragoza"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#'OFICINA DE TURISMO DE ARAGON'

    #  Alojamientos

    def test_alojamientos_hotel_direccion(self):
        results = self.buscador.search({"question": "Cual es el telefono del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamientos_hotel_tlf(self):
        results = self.buscador.search({"question": "Cual es el telefono del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 8)

    def test_alojamientos_albergue_tlf(self):
        results = self.buscador.search({"question": "Cual es el telefono del albergue REFUGIO VIADOS",
                     "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
                     "entities": ["REFUGIO VIADOS", "albergue"]})
        self.assertTrue  (len(results) == 1)

    def test_alojamientos_apartamento_tlf(self):
        results = self.buscador.search({"question": "Cual es el telefono del apartamento APARTAMENTOS FORATATA",
                     "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
                     "entities": ["APARTAMENTOS FORATATA", "apartamento"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#974488152 / 636654293'

    def test_alojamientos_casa_tlf(self):
        results = self.buscador.search({"question": "Cual es el telefono de la casa rural PUYUELO",
                     "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
                     "entities": ["PUYUELO", "casa rural"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamientos_camping_tlf(self):
        results = self.buscador.search({"question": "Cual es el telefono del camping PINETA",
                     "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
                     "entities": ["PINETA", "camping"]})
        self.assertTrue  (len(results)  == 1)

    def test_alojamientos_hotel_fax(self):
        results = self.buscador.search({"question": "Cual es el fax del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["faxAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamientos_albergue_fax(self):
        results = self.buscador.search({"question": "Cual es el fax del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
                     "intents": ["faxAlojamiento", "tipoAlojamiento"],
                     "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
        self.assertTrue  (len(results) == 0)

    def test_alojamientos_apartamento_fax(self):
        results = self.buscador.search({"question": "Cual es el fax del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["faxAlojamiento", "tipoAlojamiento"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamientos_casa_fax(self):
        results = self.buscador.search({"question": "Cual es el fax de la casa rural CASA ARBOLEDA-LAFUENTE",
                     "intents": ["faxAlojamiento", "tipoAlojamiento"],
                     "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)


    def test_alojamientos_camping_fax(self):
        results = self.buscador.search({"question": "Cual es el FAX del camping Valle de Tena",
                     "intents": ["faxAlojamiento", "tipoAlojamiento"],
                     "entities": ["Valle de Tena", "camping"]})
        self.assertTrue  (int(results[0].get("answer0"))  >= 1)

    """def test_alojamientos_camping_web(self):
        results = self.buscador.search({"question": "Cual es la página web del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["webAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  ("WWW" in results[0].get("answer0").upper())"""

    def test_alojamientos_hotel_web(self):
        results = self.buscador.search({"question": "Cual es la página web del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["webAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue ("WWW" in results[0].get("answer0").upper())

    def test_alojamientos_albergue_web(self):
        results = self.buscador.search({"question": "Cual es la página web del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
                     "intents": ["webAlojamiento", "tipoAlojamiento"],
                     "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
        self.assertTrue  (len(results) == 0 )#www.alberguetriton.es'


    def test_alojamientos_apartamento_web(self):
        results = self.buscador.search({"question": "Cual es la página web del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["webAlojamiento", "tipoAlojamiento"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
        self.assertTrue  ("WWW" in results[0].get("answer0").upper() ) #www.balconpirineos.com

    def test_alojamientos_casa_web(self):
        results = self.buscador.search({"question": "Cual es la página web de la casa rural EVA Y MARIA CAS RURAL",
                     "intents": ["webAlojamiento", "tipoAlojamiento"],
                     "entities": ["EVA Y MARIA CAS RURAL", "casa rural"]})
        self.assertTrue  ("WWW" in results[0].get("answer0").upper())

    def test_alojamientos_camping_web(self):
        results = self.buscador.search({"question": "Cual es la página web del camping PINETA",
                     "intents": ["webAlojamiento", "tipoAlojamiento"],
                     "entities": ["PINETA", "camping"]})
        self.assertTrue  ("WWW" in results[0].get("answer0").upper())

    def test_alojamientos_hotel_direccion(self):
        results = self.buscador.search({"question": "Cual es la direccion del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["direccionAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)  # 'PLAZA ARAGON, 8'

    def test_alojamientos_albergue_direccion(self):
        results = self.buscador.search({"question": "Cual es la direccion del albergue REFUGIO DE PINETA es PINETA",
                     "intents": ["direccionAlojamiento", "tipoAlojamiento"],
                     "entities": ["REFUGIO DE PINETA es PINETA", "albergue"]})
        self.assertTrue  (len(results)  >= 0)#'PLAZA MEDIODÍA, 1'

    def test_alojamientos_apartamento_direccion(self):
        results = self.buscador.search({"question": "Cual es la direccion del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["direccionAlojamiento", "tipoAlojamiento"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#C/ VITA, S/N'

    def test_alojamientos_casa_direccion(self):
        results = self.buscador.search({"question": "Cual es la direccion de la casa rural CORONAS",
                     "intents": ["direccionAlojamiento", "tipoAlojamiento"],
                     "entities": ["CORONAS", "casa rural"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 8)#C/. LA IGLESIA, 7

    def test_alojamientos_camping_direccion(self):
        results = self.buscador.search({"question": "Cual es la direccion del camping Valle de Tena, S.C.-LECINA",
                     "intents": ["direccionAlojamiento", "tipoAlojamiento"],
                     "entities": ["Valle de Tena", "camping"]})
        self.assertTrue  (len(results[0].get("answer0"))>=1)

    def test_alojamientos_hoteles_provincia(self):
        results = self.buscador.search({"question": "Dime el listado de hoteles en Zaragoza", "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["50", "hotel", "provincia"]})
        self.assertTrue  (len(results)  >2)#APARTAHOTEL BELCHITE

    def test_alojamientos_hoteles_ciudad(self):
        results = self.buscador.search({"question": "Dime el listado de hoteles en Zaragoza", "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["Zaragoza", "hotel", "municipio"]})
        self.assertTrue  (len(results)  > 2)

    def test_alojamientos_albergues_provincia(self):
        results = self.buscador.search({"question": "Dime el listado de albergues en Tarazona",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["50", "albergue", "provincia"]})
        self.assertTrue  (len(results)  > 2)

    def test_alojamientos_albergues_ciudad(self):
        results = self.buscador.search({"question": "Dime el listado de albergues en Tarazona",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["Jatiel", "albergue", "municipio"]})
        self.assertTrue  (len(results)  >= 1)

    def test_alojamientos_apartamentos_provincia(self):
        results = self.buscador.search({"question": "Dime el listado de apartamentos en Zaragoza",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["50", "apartamento", "provincia"]})
        self.assertTrue  (len(results)  > 2)

    def test_alojamientos_apartamentos_ciudad(self):
        results = self.buscador.search({"question": "Dime el listado de apartamentos en Zaragoza",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["Zaragoza", "apartamento", "municipio"]})
        self.assertTrue  (len(results)  > 2)

    def test_alojamientos_casa_provincia(self):
        results = self.buscador.search({"question": "Dime el listado de casas rurales en Zaragoza",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["50", "casa rural", "provincia"]})
        self.assertTrue  (len(results)  > 2)

    def test_alojamientos_casa_municipio(self):
        results = self.buscador.search({"question": "Dime el listado de casas rurales en Zaragoza",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["Zaragoza", "casa rural", "municipio"]})
        self.assertTrue  (len(results)  >= 0)
    """
    #PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT ?answer0 ?etiqueta WHERE { ?alojamiento <http://opendata.aragon.es/def/ei2a#organizationName> ?answer0 . ?alojamiento <http://harmonet.org/harmonise#location> ?location . ?location <http://harmonet.org/harmonise#address> ?address . ?address <http://harmonet.org/harmonise#province> ?province . ?province <http://harmonet.org/harmonise#languageText> ?language . ?language <http://harmonet.org/harmonise#text> ?etiqueta .  filter REGEX(?etiqueta, "Z[aáAÁ]r[aáAÁ]g[oóOÓ]z[aáAÁ]", "i") . ?alojamiento ?aux0 ei2a:camping_turistico . }
    #
    #  test falla porque no devuelve la ciudad sino el codigo de ciudad
    def test_alojamientos_campings_provincia(self):
        results = self.buscador.search({"question": "Dime el listado de campings en Zaragoza",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["Zaragoza", "camping", "provincia"]})
        self.assertTrue  (len(results)  > 2)
    """

    def test_alojamientos_campings_municipio(self):
        results = self.buscador.search({"question": "Dime el listado de campings en Zaragoza",
                     "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
                     "entities": ["Zaragoza", "camping", "municipio"]})
        self.assertTrue  (len(results)  >= 1)

    def test_turismo_agencia_tlf(self):
        results = self.buscador.search({"question": "Cual es el telefono de la agencia de viajes GOYA TOURS, S.L.",
                     "intents": ["telefonoAgenciaViajes"],
                     "entities": ["GOYA TOURS, S.L."]})
        self.assertTrue  (len(results)  == 1)#976-282875

    def test_turismo_agencia_email(self):
        results = self.buscador.search({"question": "Cual es el email de la agencia de viajes GOYA TOURS, S.L.",
                     "intents": ["emailAgenciaViajes"],
                     "entities": ["GOYA TOURS, S.L."]})
        self.assertTrue  ("@" in results[0].get("answer0"))

    def test_turismo_agencia_web(self):
        results = self.buscador.search({"question": "Cual es la pagina web de la agencia de viajes BYPAULA, S.L.",
                     "intents": ["webAgenciaViajes"],
                     "entities": ["BYPAULA, S.L."]})
        self.assertTrue  ("WWW" in results[0].get("answer0").upper())

    def test_turismo_agencia_direccion(self):
        results = self.buscador.search({"question": "Cual es la direccion de la agencia de viajes TOURISM MARKETING SOLUTIONS, S.L.",
                     "intents": ["direccionAgenciaViajes"],
                     "entities": ["TOURISM MARKETING SOLUTIONS, S.L."]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#'Avda. Pablo Gargallo,15, Andador Menaya'

    """def test_turismo_agencias_ciudad(self):
        results = self.buscador.search({"question": "Dime las agencias de viajes de Zaragoza",
                     "intents": ["listAgenciaViajes"],
                     "entities": ["Zaragoza"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 10)#'ROSA MARINA'"""

    def test_turismo_agencia_reserva(self):
        results = self.buscador.search({"question": "Como puedo reservar el albergue ALBERGUE DE SIN",
                     "intents": ["reservarAlojamiento", "tipoAlojamiento"],
                     "entities": ["ALBERGUE DE SIN", "albergue"]})
        self.assertTrue  ("@" in results[0].get("answer0"))#info@alberguetriton.es

    def test_alojamiento_camping_reserva(self):
        results = self.buscador.search({"question": "Como puedo reservar el camping PINETA",
                     "intents": ["reservarAlojamiento", "tipoAlojamiento"],
                     "entities": ["PINETA", "camping"]})
        self.assertTrue  ("@" in results[0].get("answer0"))#info@campingpineta.com'

    def test_alojamiento_apartamento_reserva(self):
        results = self.buscador.search({"question": "Como puedo reservar el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["reservarAlojamiento", "tipoAlojamiento"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
        self.assertTrue  ("@" in results[0].get("answer0"))#balconpirineo@gmail.com

    def test_alojamiento_casa_reserva(self):
        results = self.buscador.search({"question": "Como puedo reservar la casa rural CASA ARBOLEDA-LAFUENTE",
                     "intents": ["reservarAlojamiento", "tipoAlojamiento"],
                     "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
        self.assertTrue  ("@" in results[0].get("answer0"))#'turismo_rural@terra.es'

    def test_alojamiento_hotel_reserva(self):
        results = self.buscador.search({"question": "Como puedo reservar el hotel HOTEL & SPA REAL VILLA ANAYET",
                     "intents": ["reservarAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  ("@" in results[0].get("answer0"))#direccion@hotelrealvillaanayet'

    def test_alojamiento_hoteles_numero(self):
        results = self.buscador.search({"question": "Numero de hoteles en Zaragoza",
                     "intents": ["numeroAlojamiento", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "hotel"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 15)

    def test_alojamiento_casas_numero(self):
        results = self.buscador.search({"question": "Numero de casas rurales en Zaragoza",
                     "intents": ["numeroAlojamiento", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "casa rural"]})
        self.assertTrue  (int(results[0].get("answer0")) == 0)# 1


    def test_alojamiento_apartamentos_numero(self):
        results = self.buscador.search({"question": "Numero de apartamentos en Panticosa",
                     "intents": ["numeroAlojamiento", "tipoAlojamiento"],
                     "entities": ["Panticosa", "apartamento"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamiento_campings_numero(self):
        results = self.buscador.search({"question": "Numero de campings en Zaragoza",
                     "intents": ["numeroAlojamiento", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "camping"]})
        self.assertTrue  (len(results)  >= 1 )

    """def test_alojamiento_albegues_numero(self):
        results = self.buscador.search({"question": "Numero de albergues en Zaragoza",
                     "intents": ["numeroAlojamiento", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "albergue"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_albegues_plazas_numero(self):
        results = self.buscador.search({"question": "Numero de plazas del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
                     "intents": ["plazasAlojamiento", "tipoAlojamiento"],
                     "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamiento_apartamento_plazas_numero(self):
        results = self.buscador.search({"question": "Numero de plazas del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["plazasAlojamiento", "tipoAlojamiento"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamiento_casa_plazas_numero(self):
        results = self.buscador.search({"question": "Numero de plazas de la casa rural CASA ARBOLEDA-LAFUENTE",
                     "intents": ["plazasAlojamiento", "tipoAlojamiento"],
                     "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    def test_alojamiento_camping_localiza(self):
        results = self.buscador.search({"question": "En que ciudad se encuentra el camping PINETA",
                     "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
                     "entities": ["PINETA", "camping"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 5)#BIELSA

    def test_alojamiento_apartamento_localiza(self):
        results = self.buscador.search({"question": "En que ciudad se encuentra el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 4)#BUESA

    def test_alojamiento_casa_localiza(self):
        results = self.buscador.search({"question": "En que ciudad se encuentra la casa rural CASA ARBOLEDA-LAFUENTE",
                     "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
                     "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
        self.assertTrue  (len(results[0].get("answer0"))  > 5)#LUPIÑÉN

    def test_alojamiento_hotel_localiza(self):
        results = self.buscador.search({"question": "En que ciudad se encuentra el hotel HOTEL & SPA REAL VILLA ANAYET",
                     "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  ("CANFRANC" in  results[0].get("answer0").upper())#'CANFRANC-ESTACION'

    """def test_alojamiento_apartamento_localiza_categoria(self):
        results = self.buscador.search({"question": "Cual es la categoria del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["categoriaAlojamiento", "tipoAlojamiento"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamiento_hotel_localiza_categoria(self):
        results = self.buscador.search({"question": "Cual es la categoria del hotel HOTEL & SPA REAL VILLA ANAYET",
                     "intents": ["categoriaAlojamiento", "tipoAlojamiento"],
                     "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    def test_alojamiento_hoteles_ciudad(self):
        results = self.buscador.search({"question": "Hoteles en la ciudad de Zaragoza",
                     "intents": ["alojamientoCiudad", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "hotel"]})
        self.assertTrue  (len(results)  > 2)


    def test_alojamiento_casas_ciudad(self):
        results = self.buscador.search({"question": "Casas rurales en la ciudad de Zaragoza",
                     "intents": ["alojamientoCiudad", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "casa rural"]})
        self.assertTrue  (len(results)>= 0)#LA CIGÜEÑA

    def test_alojamiento_apartamentos_ciudad(self):
        results = self.buscador.search({"question": "Apartamentos en la ciudad de Zaragoza",
                     "intents": ["alojamientoCiudad", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "apartamento"]})
        self.assertTrue  (len(results)> 2)# 'MY WAY AWAY'

    def test_alojamiento_campings_ciudad(self):
        results = self.buscador.search({"question": "Campings en la ciudad de Zaragoza",
                     "intents": ["alojamientoCiudad", "tipoAlojamiento"],
                     "entities": ["Zaragoza", "camping"]})
        self.assertTrue  (len(results)>= 1)#'UTE CAMPING CIUDAD DE ZARAGOZA-CAMPING CIUDAD DE ZARAGOZA'


    """def test_alojamiento_apartamento_temporada(self):
        results = self.buscador.search({"question": "Cuando es temporada alta en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "alta"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

        results = self.buscador.search({"question": "Cuando es temporada baja en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "baja"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

        results = self.buscador.search({"question": "Cuando es temporada media en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
                     "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                     "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "media"]})

        self.assertTrue  (int(results[0].get("answer0"))  > 1)


    def test_alojamiento_camping_temporada(self):
        results = self.buscador.search({"question": "Cuando es temporada alta en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
                        "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                        "entities": ["CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS", "camping", "alta"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)
        results = self.buscador.search({"question": "Cuando es temporada baja en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
                        "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                        "entities": ["CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS", "camping", "baja"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)
        results = self.buscador.search({"question": "Cuando es temporada media en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
                        "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                        "entities": ["CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS", "camping", "media"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)


    def test_alojamiento_casa_temporada(self):

        results = self.buscador.search({"question": "Cuando es temporada baja en la casa rural CASA LOS CEREZOS",
                        "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                        "entities": ["CASA LOS CEREZOS", "casa rural", "baja"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)

    def test_alojamiento_hotel_temporada(self):
        results = self.buscador.search({"question": "Cuando es temporada alta en el hotel HOTEL & SPA REAL VILLA ANAYET",
                        "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                        "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel", "alta"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)
        results = self.buscador.search({"question": "Cuando es temporada baja en el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
                        "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                        "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "baja"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)
        results = self.buscador.search({"question": "Cuando es temporada media en el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
                        "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
                        "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "media"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""


    """def test_alojamiento_camping_plazas_caravanas(self):
        results = self.buscador.search({"question": "Cuantas plazas para caravanas hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
                        "intents": ["caravanasCamping", "tipoAlojamiento"],
                        "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_camping_plazas_parcelas(self):
        results = self.buscador.search(
            {"question": "Cuantas parcelas hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
            "intents": ["parcelasCamping", "tipoAlojamiento"],
            "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""


    """def test_alojamiento_camping_plazas_bungalows(self):
        results = self.buscador.search(
        {"question": "Cuantos bungalows hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
         "intents": ["bungalowsCamping", "tipoAlojamiento"],
         "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_casa_apartamentos_numero(self):
        results = self.buscador.search(
        {"question": "Cuantos apartamentos tiene la casa rural CASA RURAL MORILLO",
         "intents": ["apartamentosCasaRural", "tipoAlojamiento"],
         "entities": ["CASA RURAL MORILLO", "casa rural"]})
        self.assertTrue  (int(results[0].get("answer0"))  >= 1)"""

    """def test_alojamiento_casa_habitaciones_sencillas(self):
        results = self.buscador.search(
        {"question": "Cuantos habitaciones sencillas tiene la casa rural CASA RURAL MONTE PERDIDO",
         "intents": ["habitacionesSencillasCasaRural", "tipoAlojamiento"],
         "entities": ["CASA RURAL MONTE PERDIDO", "casa rural"]})
        self.assertTrue  (int(results[0].get("answer0"))  >= 1)"""

    """def test_alojamiento_casa_habitaciones_dobles(self):
        results = self.buscador.search(
        {"question": "Cuantos habitaciones dobles tiene la casa rural CASA RURAL MORILLO",
         "intents": ["habitacionesDoblesCasaRural", "tipoAlojamiento"],
         "entities": ["CASA RURAL MORILLO", "casa rural"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_dobles(self):
        results = self.buscador.search(
        {"question": "Cuantos habitaciones tiene el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
         "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
         "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "total"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_aseo(self):
        results = self.buscador.search(
        {"question": "Cuantos habitaciones con baño tiene el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
         "intents": ["habitacionesBañoHotel", "tipoAlojamiento"],
         "entities": ["ANTIGUA POSADA RODA", "hotel"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_no_aseo(self):
        results = self.buscador.search(
        {"question": "Cuantos habitaciones sin baño tiene el hotel SANDSTONE GUESTHOUSE 3",
         "intents": ["habitacionessinBañoHotel", "tipoAlojamiento"],
         "entities": ["SANDSTONE GUESTHOUSE 3", "hotel"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_camas(self):
        results = self.buscador.search(
        {"question": "Cuantas camas tiene el hotel SANDSTONE GUESTHOUSE 3",
         "intents": ["camasHotel", "tipoAlojamiento"],
         "entities": ["SANDSTONE GUESTHOUSE 3", "hotel"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_cuadruples(self):
        results = self.buscador.search(
        {"question": "Cuantas habitaciones cuadruples tiene el hotel SANDSTONE GUESTHOUSE 3",
         "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
         "entities": ["SANDSTONE GUESTHOUSE 3", "hotel", "cuadruple"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_dobles(self):
        results = self.buscador.search(
        {"question": "Cuantas habitaciones dobles tiene el hotel SANDSTONE GUESTHOUSE 3",
         "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
         "entities": ["SANDSTONE GUESTHOUSE 3", "hotel", "dobles"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_sencillas(self):
        results = self.buscador.search(
        {"question": "Cuantas habitaciones sencillas tiene el hotel GRAN HOTEL",
         "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
         "entities": ["GRAN HOTEL", "hotel", "sencillas"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_suits(self):
        results = self.buscador.search(
        {"question": "Cuantas suits tiene el hotel GRAN HOTEL",
         "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
         "entities": ["GRAN HOTEL", "hotel", "suits"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_habitaciones_triples(self):
        results = self.buscador.search(
        {"question": "Cuantas habitaciones triples tiene el hotel SOMMOS HOTEL BENASQUE",
         "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
         "entities": ["SOMMOS HOTEL BENASQUE", "hotel", "triples"]})
        self.assertTrue  (int(results[0].get("answer0"))  > 1)"""

    """def test_alojamiento_hotel_servicio(self):
        results = self.buscador.search(
        {"question": "Que servicios tiene el hotel BALNEARIO GRAN HOTEL CASCADA",
         "intents": ["serviciosHotel", "tipoAlojamiento"],
         "entities": ["BALNEARIO GRAN HOTEL CASCADA", "hotel"]})
        self.assertTrue  (len(results)  >= 1)#Restaurante"""

    '''def test_agricultura_comarca(self):
        results = self.buscador.search(
        {"question": "Cuales son los municipios que pertenecen a la comarca agraria de LA JACETANIA",
         "intents": ["comarcasAgrariasLocalizacion"],
         "entities": ["LA JACETANIA"]})
        self.assertTrue  (len(results)  >= 10)'''

    '''def test_agricultura_municipio(self):
        results = self.buscador.search(
        {"question": "A que comarcaca agraria pertenece Calatayud",
         "intents": ["municipioComarcasAgrarias"],
         "entities": ["Calatayud"]})
        self.assertTrue  (len(results)  >= 1)#SOBRARBE'''

    '''def test_agricultura_villasLocalizacion(self):
        results = self.buscador.search(
        {"question": "A que villas pertenece FRIAS DE ALBARRACIN",
         "intents": ["villasLocalizacion"],
         "entities": ["FRIAS DE ALBARRACIN"]})
        self.assertTrue  (len(results)  >= 1)#COMUNIDAD DE ALBARRACIN'''

    '''def test_agricultura_villasMunicipio(self):
        results = self.buscador.search(
        {"question": "Que municipios tienen la COMUNIDAD DE ALBARRACIN",
         "intents": ["municipioVilla"],
         "entities": ["COMUNIDAD DE ALBARRACIN"]})
        self.assertTrue  (len(results)  >= 10)#COMUNIDAD DE ALBARRACIN'''

    '''def test_agricultura_villasInfo(self):
        results = self.buscador.search(
        {"question": "Que informacion tienes de la villa COMUNIDAD DE ALBARRACIN",
         "intents": ["infoVilla"],
         "entities": ["COMUNIDAD DE ALBARRACIN"]})
        self.assertTrue  (len(results)  >= 10)#COMUNIDAD DE ALBARRACIN'''

    def test_agricultura_fincasCultivoLenoso(self):
        results = self.buscador.search(
        {"question": "dame los nombres de las fincas de cultivos leñosos de zaragoza",
         "intents": ["fincasCultivoLenoso"],
         "entities": ["ZARAGOZA"]})
        self.assertTrue  (len(results)  >= 100)

    def test_agricultura_fincasRegadio(self):
        results = self.buscador.search(
        {"question": "dame los nombres de las fincas de regadio de Borja",
         "intents": ["fincasRegadioLenosas"],
         "entities": ["Borja"]})
        self.assertTrue  (len(results)  >= 500)

    def test_agricultura_fincasSecanoLenosa(self):
        results = self.buscador.search(
        {"question": "dame los nombres de las fincas de secano de Borja",
         "intents": ["fincasSecanoLenosas"],
         "entities": ["Borja"]})
        self.assertTrue  (len(results)  >= 100)
    # too slow query
    """"
    def test_agricultura_fincasfincasOlivarLenosas(self):
        results = self.buscador.search(
        {"question": "dame los nombres de las fincas de olivar de VALDEJALON",
         "intents": ["fincasOlivarLenosas"],
         "entities": ["VALDEJALON"]})
        self.assertTrue  (len(results)  >= 200)
    """

    def test_agricultura_hectareasAgriculturaEcologica(self):
        results = self.buscador.search(
        {"question": "dame las hectareas de agicultura ecologica destinadas en aragon el 2015",
         "intents": ["hectareasAgriculturaEcologica","Year","tipoLocalizacion"],
         "entities": ["Aragon","2015","Aragon"]})
        self.assertEqual  (len(results)  ,  1, results)

    def test_agricultura_hectareasOlivares(self):
        results = self.buscador.search(
        {"question": "dame las hectareas de olivares  destinadas en aragon ",
         "intents": ["hectareasOlivares","tipoLocalizacion"],
         "entities": ["aragon","aragon"]})
        self.assertTrue  (len(results)  > 1 )

    def test_agricultura_hectareasOlivares_1999(self):
        results = self.buscador.search(
        {"question": "dame las hectareas de agicultura ecologica destinadas en aragon el 1999",
         "intents": ["hectareasOlivares","tipoLocalizacion","Year"],
         "entities": ["aragon","aragon","1999"]})

        self.assertTrue  (results[0].get("answer0" ) == "51414")




