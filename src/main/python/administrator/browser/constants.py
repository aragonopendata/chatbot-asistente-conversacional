'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
# -*- coding: utf-8 -*-
from datetime import datetime

class Constants:
    @staticmethod
    def answer0() -> str:
        return "?answer0"

    @staticmethod
    def answer1() -> str:
        return "?answer1"

    @staticmethod
    def answer2() -> str:
        return "?answer2"

    @staticmethod
    def municipio() -> str:
        return "?municipio"

    @staticmethod
    def etiqueta() -> str:
        return "?etiqueta"

    @staticmethod
    def comarca() -> str:
        return "?comarca"

    @staticmethod
    def fecha() -> str:
        return "?fecha"

    @staticmethod
    def observacion() -> str:
        return "?observacion"

    @staticmethod
    def aux0() -> str:
        return "?aux0"

    @staticmethod
    def aux1() -> str:
        return "?aux1"

    @staticmethod
    def id_membresia() -> str:
        return "?idMembresia"

    @staticmethod
    def id_rol() -> str:
        return "?idrol"

    @staticmethod
    def id_persona() -> str:
        return "?idPersona"

    @staticmethod
    def sede() -> str:
        return "?sede"

    @staticmethod
    def address() -> str:
        return "?address"

    @staticmethod
    def restaurante() -> str:
        return "?restaurant"

    @staticmethod
    def location() -> str:
        return "?location"

    @staticmethod
    def telecoms() -> str:
        return "?telecoms"

    @staticmethod
    def telephone() -> str:
        return "?telephone"

    @staticmethod
    def fax() -> str:
        return "?fax"

    @staticmethod
    def url() -> str:
        return "?url"

    @staticmethod
    def language() -> str:
        return "?language"

    @staticmethod
    def street_address() -> str:
        return "?streetAddress"

    @staticmethod
    def city() -> str:
        return "?city"

    @staticmethod
    def profile() -> str:
        return "?profile"

    @staticmethod
    def profile_field() -> str:
        return "?profileField"

    @staticmethod
    def field_name() -> str:
        return "?fieldName"

    @staticmethod
    def museo() -> str:
        return "?museo"

    @staticmethod
    def obras() -> str:
        return "?obras"

    @staticmethod
    def ruta() -> str:
        return "?ruta"

    @staticmethod
    def origen() -> str:
        return "?origen"

    @staticmethod
    def destino() -> str:
        return "?destino"

    @staticmethod
    def location2() -> str:
        return "?location2"

    @staticmethod
    def etiqueta2() -> str:
        return "?etiqueta2"

    @staticmethod
    def guia() -> str:
        return "?guia"

    @staticmethod
    def answer3() -> str:
        return "?answer3"

    @staticmethod
    def infoturismo() -> str:
        return "?infoturismo"

    @staticmethod
    def site() -> str:
        return "?site"

    @staticmethod
    def site_address() -> str:
        return "?siteAddress"

    @staticmethod
    def bd_conector() -> list:
        return ["Virtuoso", "GET"]

    @staticmethod
    def alojamiento() -> str:
        return "?alojamiento"

    @staticmethod
    def agencia() -> str:
        return "?agencia"

    @staticmethod
    def schedule() -> str:
        return "?schedule"

    @staticmethod
    def servicios() -> str:
        return "?servicios"

    @staticmethod
    def servicios_name() -> str:
        return "?serviciosName"

    @staticmethod
    def finca() -> str:
        return "?finca"

    @staticmethod
    def grafo_agricultura_ecologica_aragon() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040018A>"

    @staticmethod
    def grafo_agricultura_ecologica_municipio() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040018TM>"

    @staticmethod
    def grafo_agricultura_ecologica_comarca() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040018TC>"

    @staticmethod
    def grafo_agricultura_ecologica_provincia() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040018TP>"

    @staticmethod
    def grafo_agricultura_cultivos_aragon() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010051A>"

    @staticmethod
    def grafo_agricultura_cultivos_municipio() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010051TM>"

    @staticmethod
    def grafo_agricultura_cultivos_comarca() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010051TC>"

    @staticmethod
    def grafo_agricultura_cultivos_provincia() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010051TP>"

    @staticmethod
    def grafo_poblacion_aragon() -> str:
        return "<http://opendata.aragon.es/graph/datacube/03-030001A>"

    @staticmethod
    def grafo_poblacion_comarca() -> str:
        return "<http://opendata.aragon.es/graph/datacube/03-030001TC>"

    @staticmethod
    def grafo_poblacion_provincia() -> str:
        return "<http://opendata.aragon.es/graph/datacube/03-030001TP>"

    @staticmethod
    def grafo_poblacion_municipio() -> str:
        return "<http://opendata.aragon.es/graph/datacube/03-030001TM>"

    @staticmethod
    def grafo_extranjeros_continente() -> str:
        return "<http://opendata.aragon.es/graph/datacube/03-030012>"

    @staticmethod
    def grafo_extranjeros_pais() -> str:
        return "<http://opendata.aragon.es/graph/datacube/03-030070>"

    @staticmethod
    def grafo_contenedores_vidrio() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040014>"

    @staticmethod
    def year_max() -> str:
        return "?fecha"

    @staticmethod
    def grafo_hectareas_zona() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040009>"

    @staticmethod
    def grafo_incendios() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040017>"

    @staticmethod
    def grafo_depuradoras() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040019>"

    @staticmethod
    def grafo_autonomos() -> str:
        return "<http://opendata.aragon.es/graph/datacube/05-050006>"

    @staticmethod
    def grafo_parados() -> str:
        return "<http://opendata.aragon.es/graph/datacube/05-050203>"

    @staticmethod
    def grafo_contratados() -> str:
        return "<http://opendata.aragon.es/graph/datacube/05-050301>"

    @staticmethod
    def grafo_accidentes_laborales() -> str:
        return "<http://opendata.aragon.es/graph/datacube/05-0709-070902>"

    @staticmethod
    def grafo_renta() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010064>"

    @staticmethod
    def grafo_trabajadores_empresa() -> str:
        return "<http://opendata.aragon.es/graph/datacube/05-050103>"

    @staticmethod
    def grafo_sector_empresa() -> str:
        return "<http://opendata.aragon.es/graph/datacube/05-050102>"

    @staticmethod
    def grafo_actividad_empresa() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010076>"

    @staticmethod
    def grafo_uso_suelo() -> str:
        return "<http://opendata.aragon.es/graph/datacube/04-040012>"

    @staticmethod
    def grafo_hectareas_tipo_suelo() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010019>"

    @staticmethod
    def grafo_edificios_construccion() -> str:
        return "<http://opendata.aragon.es/graph/datacube/01-010005>"
