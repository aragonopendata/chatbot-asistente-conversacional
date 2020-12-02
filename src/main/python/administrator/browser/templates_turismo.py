'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import re
from browser.config import Config
from browser.constants import Constants


class TemplatesTurismo:
    """[summary]
    """

    @staticmethod
    def lemmatizer(msg: str, nlp) -> str:
        lemmatize_msg = ""
        for token in nlp(msg):
            lemmatize_msg += token.lemma_ + " "
        return lemmatize_msg

    @staticmethod
    def create_bif_contains(cadena: str, variable: str) -> str:
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
        query = ""
        query += " filter REGEX(" + variable + ', "' + cadena + '", "i")'
        return query

    @staticmethod
    def create_filter_greater(cadena: int, variable: str) -> str:
        query = (
            " filter (<http://www.w3.org/2001/XMLSchema#integer> ("
            + variable
            + ") >= "
            + str(cadena)
            + ")"
        )

        return query

    @staticmethod
    def base_query() -> str:
        base = (
            Config.prefix()
            + "SELECT DISTINCT "
            + Constants.answer0()
            + " "
            + Constants.etiqueta()
        )
        if Config.graph() != "":
            base += " FROM <" + Config.graph() + ">"
        base += " WHERE { "
        return base

    # *************
    # gastronomia
    # *************

    @staticmethod
    def telefono_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#telephone> "
            + Constants.telephone()
            + " . "
        )

        query += (
            Constants.telephone()
            + " <http://harmonet.org/harmonise#number> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def fax_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#fax> "
            + Constants.fax()
            + " . "
        )

        query += (
            Constants.fax()
            + " <http://harmonet.org/harmonise#number> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def email_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#email> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def web_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#url> "
            + Constants.url()
            + " . "
        )

        query += (
            Constants.url()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def direccion_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = query.replace(
            Constants.answer0(),
            Constants.answer0() + " " + Constants.answer1() + Constants.answer2(),
        )

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#postCode> "
            + Constants.answer1()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.answer2()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#streetAddress> "
            + Constants.street_address()
            + " . "
        )

        query += (
            Constants.street_address()
            + " <http://harmonet.org/harmonise#streetName> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def info_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio
        query = query.replace(
            Constants.answer0(),
            Constants.answer0() + " " + Constants.answer1() + " " + Constants.answer2(),
        )

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )
        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#streetAddress> "
            + Constants.street_address()
            + " . "
        )

        query += (
            Constants.street_address()
            + " <http://harmonet.org/harmonise#streetName> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#email> "
            + Constants.answer1()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#telephone> "
            + Constants.telephone()
            + " . "
        )

        query += (
            Constants.telephone()
            + " <http://harmonet.org/harmonise#number> "
            + Constants.answer2()
            + " . "
        )
        return query

    @staticmethod
    def info_restaurante_telefono(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = query.replace(
            Constants.answer0(),
            Constants.answer0() + " " + Constants.answer1(),
        )

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )
        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
                Constants.location()
                + " <http://harmonet.org/harmonise#address> "
                + Constants.address()
                + " . "
        )

        query += (
                Constants.address()
                + " <http://harmonet.org/harmonise#streetAddress> "
                + Constants.street_address()
                + " . "
        )

        query += (
                Constants.street_address()
                + " <http://harmonet.org/harmonise#streetName> "
                + Constants.answer0()
                + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#telephone> "
            + Constants.telephone()
            + " . "
        )

        query += (
            Constants.telephone()
            + " <http://harmonet.org/harmonise#number> "
            + Constants.answer1()
            + " . "
        )
        return query

    @staticmethod
    def list_restaurantes(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.answer0()
            + "."
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def plazas_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + Constants.field_name()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(
                "Número de plazas", Constants.field_name()
            )
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )

        query += (
                ' filter REGEX(?profileField, "places", "i") .'
        )

        return query

    @staticmethod
    def numero_restaurantes(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = query.replace(
            "DISTINCT " + Constants.answer0(),
            "COUNT (DISTINCT" + Constants.answer0() + ") AS " + Constants.answer0(),
        )

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.answer0()
            + "."
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def municipio_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.restaurante()
            + " "
            + Constants.aux0()
            + " ei2a:cafeteria_restaurante . "
        )

        query += (
            Constants.restaurante()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(restaurante, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.restaurante()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.answer0()
            + " . "
        )
        return query

    # *************
    # Actividades
    # *************

    @staticmethod
    def obras_museo(query, museo) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.museo()
            + " "
            + Constants.aux0()
            + " ei2a:colecciones_museos_aragon. "
        )

        query += Constants.museo() + " ei2a:isOfInterestTo " + Constants.obras() + " . "

        query += (
            Constants.obras() + " ei2a:organizationName " + Constants.etiqueta() + "."
        )

        query += (
            TemplatesTurismo.create_bif_contains(museo, Constants.etiqueta()) + " . "
        )

        query += Constants.museo() + " ei2a:nameDocument " + Constants.answer0() + " . "
        return query

    @staticmethod
    def museos_municipio(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.museo()
            + " "
            + Constants.aux0()
            + " ei2a:colecciones_museos_aragon. "
        )

        query += Constants.museo() + " ei2a:isOfInterestTo " + Constants.obras() + " . "

        query += (
            Constants.obras() + " ei2a:organizationName " + Constants.answer0() + "."
        )

        query += (
            Constants.museo()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.municipio()
            + " . "
        )

        query += (
            Constants.municipio()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def municipio_obra(query, obra) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.museo()
            + " "
            + Constants.aux0()
            + " ei2a:colecciones_museos_aragon. "
        )

        query += Constants.museo() + " ei2a:isOfInterestTo " + Constants.obras() + " . "

        query += (
            Constants.obras() + " ei2a:organizationName " + Constants.answer0() + ". "
        )

        query += (
            Constants.museo() + " ei2a:nameDocument " + Constants.etiqueta() + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(obra, Constants.etiqueta()) + " . "
        )
        return query

    @staticmethod
    def rutas_con_origen(query, municipio) -> str:
        query += Constants.ruta() + " " + Constants.aux0() + " ei2a:ruta . "

        query += (
            Constants.ruta()
            + " <http://vocab.gtfs.org/terms#originStop> "
            + Constants.origen()
            + " . "
        )

        query += (
            Constants.origen()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + ". "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.ruta()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def rutas_con_destino(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += Constants.ruta() + " " + Constants.aux0() + " ei2a:ruta . "

        query += (
            Constants.ruta()
            + " <http://vocab.gtfs.org/terms#destinationStop> "
            + Constants.destino()
            + " . "
        )

        query += (
            Constants.destino()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + ". "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.ruta()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def rutas_camino(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = query.replace(Constants.etiqueta(), "")

        query += Constants.ruta() + " " + Constants.aux0() + " ei2a:ruta . "

        query += (
            Constants.ruta()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.answer0()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.answer0()) + " . "
        )

        query += (
            Constants.ruta()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.etiqueta()
            + " . "
        )
        return query

    @staticmethod
    def guia_municipio(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += Constants.guia() + " " + Constants.aux0() + " ei2a:guia_turismo . "

        query += Constants.guia() + " <location> " + Constants.location() + " . "

        query += (
            Constants.location()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += Constants.guia() + " ei2a:fullName " + Constants.answer0() + " . "
        return query

    @staticmethod
    def telefono_guia(query, guia) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += Constants.guia() + " " + Constants.aux0() + " ei2a:guia_turismo . "

        query += Constants.guia() + " ei2a:fullName " + Constants.etiqueta() + " . "

        query += (
            TemplatesTurismo.create_bif_contains(guia, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.guia()
            + " <http://xmlns.com/foaf/0.1/phone> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def email_guia(query, guia) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += Constants.guia() + " " + Constants.aux0() + " ei2a:guia_turismo . "

        query += Constants.guia() + " ei2a:fullName " + Constants.etiqueta() + " . "

        query += (
            TemplatesTurismo.create_bif_contains(guia, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.guia()
            + " <http://xmlns.com/foaf/0.1/mbox> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def web_guia(query, guia) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += Constants.guia() + " " + Constants.aux0() + " ei2a:guia_turismo . "

        query += Constants.guia() + " ei2a:fullName " + Constants.etiqueta() + " . "

        query += (
            TemplatesTurismo.create_bif_contains(guia, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.guia()
            + " <http://xmlns.com/foaf/0.1/homepage> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def info_guia(query, guia) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio
        query = query.replace(
            Constants.answer0(),
            Constants.answer0()
            + " "
            + Constants.answer1()
            + " "
            + Constants.answer2()
            + " "
            + Constants.answer3(),
        )

        query += Constants.guia() + " " + Constants.aux0() + " ei2a:guia_turismo . "

        query += Constants.guia() + " ei2a:fullName " + Constants.etiqueta() + " . "

        query += (
            TemplatesTurismo.create_bif_contains(guia, Constants.etiqueta()) + " . "
        )

        query += (
            "OPTIONAL { "
            + Constants.guia()
            + " <http://xmlns.com/foaf/0.1/homepage> "
            + Constants.answer0()
            + " . } "
        )

        query += (
            "OPTIONAL { "
            + Constants.guia()
            + " <http://xmlns.com/foaf/0.1/mbox> "
            + Constants.answer1()
            + " . } "
        )

        query += (
            "OPTIONAL { "
            + Constants.guia()
            + " <http://xmlns.com/foaf/0.1/phone> "
            + Constants.answer2()
            + " . } "
        )

        query += (
            "OPTIONAL { "
            + Constants.guia()
            + " <location> "
            + Constants.location()
            + " . "
        )
        query += (
            Constants.location()
            + " ei2a:organizationName "
            + Constants.answer3()
            + " . }"
        )
        return query

    @staticmethod
    def telefono_iturismo(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = query.replace(
            Constants.answer0(),
            Constants.answer0() + " " + Constants.answer1() + " " + Constants.answer2(),
        )

        query += (
            "VALUES "
            + Constants.aux1()
            + " { ei2a:punto_informacion_turistica  ei2a:oficina_turismo } "
        )

        query += (
            Constants.infoturismo()
            + " "
            + Constants.aux0()
            + " "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.infoturismo()
            + " <http://www.w3.org/ns/org#hasSite> "
            + Constants.site()
            + " . "
        )

        query += (
            Constants.site()
            + " <http://www.w3.org/ns/org#siteAddress> "
            + Constants.site_address()
            + " . "
        )

        query += (
            Constants.site_address()
            + " <http://www.w3.org/2006/vcard/ns#hasAddress> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#locality> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#street-address> "
            + Constants.answer1()
            + " . "
        )

        query += (
            Constants.infoturismo()
            + " ei2a:organizationName "
            + Constants.answer0()
            + " . "
        )

        query += (
            "OPTIONAL {"
            + Constants.infoturismo()
            + " foaf:phone "
            + Constants.answer2()
            + " } ."
        )
        return query

    @staticmethod
    def direccion_iturismo(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = query.replace(
            Constants.answer0(), Constants.answer0() + " " + Constants.answer1()
        )

        query += (
            "VALUES "
            + Constants.aux1()
            + " { ei2a:punto_informacion_turistica  ei2a:oficina_turismo } "
        )

        query += (
            Constants.infoturismo()
            + " "
            + Constants.aux0()
            + " "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.infoturismo()
            + " <http://www.w3.org/ns/org#hasSite> "
            + Constants.site()
            + " . "
        )

        query += (
            Constants.site()
            + " <http://www.w3.org/ns/org#siteAddress> "
            + Constants.site_address()
            + " . "
        )

        query += (
            Constants.site_address()
            + " <http://www.w3.org/2006/vcard/ns#hasAddress> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#locality> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#street-address> "
            + Constants.answer1()
            + " . "
        )

        query += (
            Constants.infoturismo()
            + " ei2a:organizationName "
            + Constants.answer0()
            + " . "
        )
        return query

    # *************
    # alojamiento
    # *************

    @staticmethod
    def telefono_alojamiento(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#telephone> "
            + Constants.telephone()
            + " . "
        )

        query += (
            Constants.telephone()
            + " <http://harmonet.org/harmonise#number> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def email_alojamiento(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#email> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def fax_alojamiento(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#fax> "
            + Constants.fax()
            + " . "
        )

        query += (
            Constants.fax()
            + " <http://harmonet.org/harmonise#number> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def web_alojamiento(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#url> "
            + Constants.url()
            + " . "
        )

        query += (
            Constants.url()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def direccion_alojamiento(query, alojamiento) -> str:

        query = query.replace(
            Constants.answer0(),
            Constants.answer0() + " " + Constants.answer1() + Constants.answer2(),
        )

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#postCode> "
            + Constants.answer1()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.answer2()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#streetAddress> "
            + Constants.street_address()
            + " . "
        )

        query += (
            Constants.street_address()
            + " <http://harmonet.org/harmonise#streetName> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def listado_alojamiento(query, municipio) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def reserva_alojamiento(query, alojamiento) -> str:

        query = query.replace(
            Constants.answer0(), Constants.answer0() + " " + Constants.answer1()
        )

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#email> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#telephone> "
            + Constants.telephone()
            + " . "
        )

        query += (
            Constants.telephone()
            + " <http://harmonet.org/harmonise#number> "
            + Constants.answer1()
            + " . "
        )
        return query

    @staticmethod
    def reserva_alojamiento_telephone(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
                Constants.telecoms()
                + " <http://harmonet.org/harmonise#telephone> "
                + Constants.telephone()
                + " . "
        )

        query += (
                Constants.telephone()
                + " <http://harmonet.org/harmonise#number> "
                + Constants.answer0()
                + " . "
        )

        return query

    @staticmethod
    def reserva_alojamiento_email(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#telecoms> "
            + Constants.telecoms()
            + " . "
        )

        query += (
            Constants.telecoms()
            + " <http://harmonet.org/harmonise#email> "
            + Constants.answer0()
            + " . "
        )

        return query

    @staticmethod
    def count_alojamiento(query, municipio):

        query = query.replace(
            "DISTINCT " + Constants.answer0(),
            "COUNT (DISTINCT " + Constants.answer0() + ") AS " + Constants.answer0(),
        )

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def plazas_alojamiento(query, alojamiento):

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + Constants.aux1()
            + " ."
        )

        query += (
            TemplatesTurismo.create_bif_contains("Número de plazas", Constants.aux1())
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def ciudad_alojamiento(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def categoria_alojamiento(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#award> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1()
            + " <http://harmonet.org/harmonise#awardingBody> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def alojamiento_municipio(query, municipio) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://harmonet.org/harmonise#address> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://harmonet.org/harmonise#city> "
            + Constants.city()
            + " . "
        )

        query += (
            Constants.city()
            + " <http://harmonet.org/harmonise#languageText> "
            + Constants.language()
            + " . "
        )

        query += (
            Constants.language()
            + " <http://harmonet.org/harmonise#text> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def temporada_alojamiento(query, alojamiento) -> str:

        query = query.replace(
            Constants.answer0(), Constants.answer0() + " " + Constants.answer1()
        )

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#schedule> "
            + Constants.schedule()
            + " . "
        )

        query += (
            Constants.schedule()
            + " <http://harmonet.org/harmonise#season>  "
            + "temporada . "
        )

        query += (
            Constants.schedule()
            + " <http://harmonet.org/harmonise#dateRange> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1()
            + " <http://harmonet.org/harmonise#endDate> "
            + Constants.answer1()
            + " . "
        )

        query += (
            Constants.aux1()
            + " <http://harmonet.org/harmonise#startDate> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def caravanas_camping(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de plazas de mobile homes'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def parcelas_camping(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de parcelas'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def bungalows_camping(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de parcelas'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def apartamentos_casarural(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de apartamentos'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitacionesdobles_casarural(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de habitaciones dobles'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitacionessencillas_casarural(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de habitaciones sencillas'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitaciones_hotel(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    # Reutilizar en las siguientes funciones.

    @staticmethod
    def habitaciones_hotel_protege(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " protege:profile "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " protege:profileField "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " protege:fieldValue "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitacionesbano_hotel(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de habitaciones con baño'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitacionesbano_hotel_protege(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " protege:profile "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " protege:profileField "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " protege:fieldName "
            + "'Número de habitaciones con baño'  . "
        )

        query += (
            Constants.profile_field()
            + " protege:fieldValue "
            + Constants.answer0()
            + " . "
        )
        return query


    @staticmethod
    def habitacionesterraza_hotel(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de habitaciones con terraza'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitacionesterraza_hotel_protege(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " protege:profile "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " protege:profileField "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " protege:fieldName "
            + "'Número de habitaciones con terraza'  . "
        )

        query += (
            Constants.profile_field()
            + " protege:fieldValue "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitacionessinbano_hotel(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número de habitaciones sin baño'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def habitacionessinbano_hotel_protege(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " protege:profile "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " protege:profileField "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " protege:fieldName "
            + "'Número de habitaciones sin baño'  . "
        )

        query += (
            Constants.profile_field()
            + " protege:fieldValue "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def camas_hotel(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#profile> "
            + Constants.profile()
            + " . "
        )

        query += (
            Constants.profile()
            + " <http://harmonet.org/harmonise#profileField> "
            + Constants.profile_field()
            + " . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldName> "
            + "'Número total de camas'  . "
        )

        query += (
            Constants.profile_field()
            + " <http://harmonet.org/harmonise#fieldValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def servicios_hotel(query, alojamiento) -> str:

        query += (
            Constants.alojamiento()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(alojamiento, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#service> "
            + Constants.servicios()
            + " . "
        )

        query += (
            Constants.servicios()
            + " <http://harmonet.org/harmonise#serviceName> "
            + Constants.servicios_name()
            + " . "
        )

        query += (
            Constants.servicios_name()
            + " <http://harmonet.org/harmonise#referencedValue> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1()
            + " <http://harmonet.org/harmonise#domainValue> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def telefono_agencia_viaje(query, agencia) -> str:

        query += Constants.agencia() + " " + Constants.aux0() + " ei2a:agencia_viaje . "

        query += (
            Constants.agencia()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(agencia, Constants.etiqueta()) + " . "
        )

        query += Constants.agencia() + " ei2a:phone " + Constants.answer0() + " . "
        return query

    @staticmethod
    def email_agencia_viaje(query, agencia) -> str:

        query += Constants.agencia() + " " + Constants.aux0() + " ei2a:agencia_viaje . "

        query += (
            Constants.agencia()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(agencia, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.agencia()
            + " <http://xmlns.com/foaf/0.1/mbox> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def web_agencia_viaje(query, agencia) -> str:
        query += Constants.agencia() + " " + Constants.aux0() + " ei2a:agencia_viaje . "

        query += (
            Constants.agencia()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(agencia, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.agencia()
            + " <http://xmlns.com/foaf/0.1/homepage> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def direccion_agencia_viaje(query, agencia) -> str:

        query = query.replace(
            Constants.answer0(),
            Constants.answer0() + " " + Constants.answer1() + " " + Constants.answer2(),
        )

        query += Constants.agencia() + " " + Constants.aux0() + " ei2a:agencia_viaje . "

        query += (
            Constants.agencia()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(agencia, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.agencia()
            + " <http://www.w3.org/ns/org#hasSite> "
            + Constants.site()
            + " . "
        )

        query += (
            Constants.site()
            + " <http://www.w3.org/ns/org#siteAddress> "
            + Constants.site_address()
            + " . "
        )

        query += (
            Constants.site_address()
            + " <http://www.w3.org/2006/vcard/ns#hasAddress> "
            + Constants.address()
            + " . "
        )

        query += (
            "OPTIONAL { "
            + Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#postal-code> "
            + Constants.answer1()
            + " . }"
        )

        query += (
            "OPTIONAL { "
            + Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#region> "
            + Constants.answer2()
            + " . }"
        )

        query += (
            Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#street-address> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def list_agencia_viaje(query, localidad) -> str:

        query += Constants.agencia() + " " + Constants.aux0() + " ei2a:agencia_viaje . "

        query += (
            Constants.agencia()
            + " <http://opendata.aragon.es/def/ei2a#organizationName> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.agencia()
            + " <http://www.w3.org/ns/org#hasSite> "
            + Constants.site()
            + " . "
        )

        query += (
            Constants.site()
            + " <http://www.w3.org/ns/org#siteAddress> "
            + Constants.site_address()
            + " . "
        )

        query += (
            Constants.site_address()
            + " <http://www.w3.org/2006/vcard/ns#hasAddress> "
            + Constants.address()
            + " . "
        )

        query += (
            Constants.address()
            + " <http://www.w3.org/2006/vcard/ns#locality> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesTurismo.create_bif_contains(localidad, Constants.etiqueta())
            + " . "
        )
        return query

    # *************
    # extra Queries
    # *************

    @staticmethod
    def extra_destino(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.ruta()
            + " <http://vocab.gtfs.org/terms#destinationStop> "
            + Constants.destino()
            + " . "
        )

        query += (
            Constants.destino()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location2()
            + " . "
        )

        query += (
            Constants.location2()
            + " ei2a:organizationName "
            + Constants.etiqueta2()
            + ". "
        )

        query += (
            TemplatesTurismo.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def extra_tipo_alojamiento(query, tipo_alojamiento) -> str:

        alojamiento = ""
        tipo_alojamiento = tipo_alojamiento.lower()

        if tipo_alojamiento == "hotel":
            alojamiento = "alojamiento_hotelero"
            #alojamiento = "alojamiento_rural"
        elif tipo_alojamiento == "albergue":
            alojamiento = "albergue_refugio"
        elif tipo_alojamiento == "apartamento":
            alojamiento = "apartamento_turistico"
        elif tipo_alojamiento == "casa rural":
            alojamiento = "alojamiento_rural"
            query = query.replace(
                "http://harmonet.org/harmonise",
                "http://protege.stanford.edu/rdf/HTOv4002",
            )
        elif tipo_alojamiento == "camping":
            alojamiento = "camping_turistico"

        query += (
            Constants.alojamiento()
            + " "
            + Constants.aux0()
            + " ei2a:"
            + alojamiento
            + " . "
        )
        return query

    @staticmethod
    def extra_tipo_lugar(query, tipo_lugar) -> str:
        tipo_lugar = tipo_lugar.lower()

        if tipo_lugar == "provincia":
            query = query.replace("city", "province")

        return query

    @staticmethod
    def extra_tipo_temporada(query, tipo_temporada) -> str:
        tipo_temporada = tipo_temporada.lower()

        if tipo_temporada == "alta":
            query = query.replace(
                "temporada",
                "<http://opendata.aragon.es/def/ei2a#season-list-value-temporada_alta>",
            )
        elif tipo_temporada == "media":
            query = query.replace(
                "temporada",
                "<http://opendata.aragon.es/def/ei2a#season-list-value-temporada_media>",
            )
        elif tipo_temporada == "baja":
            query = query.replace(
                "temporada",
                "<http://opendata.aragon.es/def/ei2a#season-list-value-temporada_baja>",
            )

        return query

    @staticmethod
    def extra_tipo_habitacion(query, tipo_habitacion) -> str:
        tipo_habitacion = tipo_habitacion.lower()

        '''
        
        Las comparaciones tendría que ser con s y sin s.
        
        '''

        if (tipo_habitacion == "sencillas" or tipo_habitacion == "sencilla"):
            query += ("filter REGEX(" +
                      Constants.profile_field()
                      + ',"sencilla","i")'
                      + " . "
                      )
        elif (tipo_habitacion == "dobles" or tipo_habitacion == "doble"):
            query += ("filter REGEX(" +
                      Constants.profile_field()
                      + ',"doble","i")'
                      + " . "
                      )
        elif (tipo_habitacion == "triples" or tipo_habitacion == "triple"):
            query += ("filter REGEX(" +
                      Constants.profile_field()
                      + ',"triple","i")'
                      + " . "
                      )
        elif (tipo_habitacion == "cuadruples" or tipo_habitacion == "cuadruple"):
            query += ("filter REGEX(" +
                Constants.profile_field()
                + ',"doble","i")'
                + " . "
            )
        elif (tipo_habitacion == "suits" or tipo_habitacion == "suit"):
            query += ("filter REGEX(" +
                      Constants.profile_field()
                      + ',"suit","i")'
                      + " . "
                      )
        elif tipo_habitacion == "total":
            query += ("filter REGEX(" +
                      Constants.profile_field()
                      + ',"tot","i")'
                      + " . "
                      )
        return query

    @staticmethod
    def extra_tipo_habitacion_protege(query, tipo_habitacion) -> str:

        tipo_habitacion = tipo_habitacion.lower()

        query += (" filter REGEX(?profileField, " + '"' + tipo_habitacion + '"' + """, "i") . """ )

        return query

    @staticmethod
    def extra_categoria(query, categoria) -> str:

        query = query.replace(
            "DISTINCT " + Constants.answer0(),
            Constants.answer0() + " " + Constants.answer1(),
        )

        query += (
            Constants.alojamiento()
            + " <http://harmonet.org/harmonise#award> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1()
            + " <http://harmonet.org/harmonise#awardingBody> "
            + Constants.answer1()
            + " . "
        )

        query += (
            TemplatesTurismo.create_filter_greater(categoria, Constants.answer1())
            + " . "
        )
        return query
