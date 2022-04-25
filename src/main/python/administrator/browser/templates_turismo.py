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

        parameters = []
        parameters.append([Constants.nombrerestaurante(),restaurante])
        query = TemplatesTurismo.obtenerInformacionEstablecimientosRestaurantesCafeterias(restaurante,Constants.telefonorestaurante(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def fax_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        parameters = []
        parameters.append([Constants.nombrerestaurante(),restaurante])
        query = TemplatesTurismo.obtenerInformacionEstablecimientosRestaurantesCafeterias(restaurante,Constants.faxrestaurante(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def email_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        parameters = []
        parameters.append([Constants.nombrerestaurante(),restaurante])
        query = TemplatesTurismo.obtenerInformacionEstablecimientosRestaurantesCafeterias(restaurante,Constants.emailrestaurante(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def web_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        parameters = []
        parameters.append([Constants.nombrerestaurante(),restaurante])
        query = TemplatesTurismo.obtenerInformacionEstablecimientosRestaurantesCafeterias(restaurante,Constants.webrestaurante(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def direccion_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        parameters = []
        parameters.append([Constants.nombrerestaurante(),restaurante])
        columnas = []
        columnas.append(Constants.direccionrestaurante())
        columnas.append(Constants.codigopostalrestaurante())
        query = TemplatesTurismo.obtenerInformacionCompletaEstablecimientosRestaurantesCafeterias(restaurante,columnas,Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def info_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio
        parameters = []
        parameters.append([Constants.nombrerestaurante(),restaurante])
        columnas = []
        columnas.append(Constants.direccionrestaurante())
        columnas.append(Constants.telefonorestaurante())
        columnas.append(Constants.emailrestaurante())
        query = TemplatesTurismo.obtenerInformacionCompletaEstablecimientosRestaurantesCafeterias(restaurante,columnas,Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def info_restaurante_telefono(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        parameters = []
        parameters.append([Constants.nombrerestaurante(),restaurante])
        columnas = [Constants.direccionrestaurante(),Constants.telefonorestaurante(),Constants.emailrestaurante()]
        query = TemplatesTurismo.obtenerInformacionCompletaEstablecimientosRestaurantesCafeterias(restaurante,columnas,Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def list_restaurantes(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        municipio = TemplatesTurismo.bifString(municipio)
        query = "SELECT DISTINCT  ?answer0  ?etiqueta FROM " + Constants.urlei2a() + """ WHERE { ?id rdf:type	org:Organization . ?id <http://purl.org/dc/elements/1.1/title> ?answer0 . FILTER (?id like "%registro-cafeteria%") . ?id <http://www.w3.org/ns/org#linkedTo> ?etiqueta  . FILTER REGEX(?etiqueta  , """ + '"' + municipio + '"' + """, "i") ."""
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

        query = TemplatesTurismo.obtenerInformacionMunicipioRestaurante(municipio,Constants.urlei2a())
        return query

    @staticmethod
    def municipio_restaurante(query, restaurante) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        restaurante = TemplatesTurismo.bifString(restaurante)
        query = """SELECT DISTINCT  ?answer0  ?etiqueta FROM """ + Constants.urlei2a() + """ WHERE { ?id rdf:type	org:Organization . ?id <http://purl.org/dc/elements/1.1/title> ?etiqueta . FILTER (?id like "%registro-cafeteria%") . FILTER REGEX(?etiqueta, """ + '"' + restaurante + '"' + """, "i") . OPTIONAL {?id <http://www.w3.org/ns/org#linkedTo> ?answer0  . FILTER (?answer0 like "%municipio%") }"""
        return query

    # *************
    # Actividades
    # *************

    @staticmethod
    def obras_museo(query, museo) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        museo = TemplatesTurismo.bifStringLine(museo)
        query = """select ?answer0  ?etiqueta from """ + Constants.urlei2a() + """ where { ?id rdf:type schema:CreativeWork . FILTER (?id like "%coleccion-museos%") . ?id org:organization ?etiqueta. FILTER REGEX(?etiqueta, """ + '"' + museo + '"' + """, "i") . ?id schema:title ?answer0"""
        return query

    @staticmethod
    def museos_municipio(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        municipio = TemplatesTurismo.bifString(municipio)
        query = """select ?answer0 ?etiqueta from """ + Constants.urlei2a() + """ where {  ?id rdf:type org:Organization FILTER (?id like "%cultura-ocio/organizacion/museo%") . ?id<http://www.w3.org/ns/org#linkedTo> ?municipio FILTER (?municipio like "%municipio%") . ?municipio <http://purl.org/dc/elements/1.1/title> ?etiqueta . FILTER REGEX(?etiqueta, """ + '"' + municipio + '"' + """, "i") . ?id dc:title ?answer0 . """
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

        query = TemplatesTurismo.obtenerInformacionSenderos(municipio,Constants.urlei2a())
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

        parameters = []
        parameters.append([Constants.nombreguia(),guia])
        query = TemplatesTurismo.obtenerInformacionGuiasTuristicos(guia,Constants.telefonoguia(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def email_guia(query, guia) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        parameters = []
        parameters.append([Constants.nombreguia(),guia])
        query = TemplatesTurismo.obtenerInformacionGuiasTuristicos(guia,Constants.emailguia(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def web_guia(query, guia) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        parameters = []
        parameters.append([Constants.nombreguia(),guia])
        query = TemplatesTurismo.obtenerInformacionGuiasTuristicos(guia,Constants.webguia(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def info_guia(query, guia) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio
        
        parameters = []
        parameters.append([Constants.nombreguia(),guia])
        columnas = [Constants.emailguia(),Constants.telefonoguia(),Constants.webguia()]
        query = TemplatesTurismo.obtenerInformacionCompletaInformacionGuia(guia,columnas,Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def telefono_iturismo(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = TemplatesTurismo.obtenerInformacionOficinaTurismo(municipio,Constants.urlei2a())
        return query

    @staticmethod
    def direccion_iturismo(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query = TemplatesTurismo.obtenerInformacionOficinaTurismo(municipio,Constants.urlei2a())
        return query

    # *************
    # alojamiento
    # *************

    @staticmethod
    def telefono_alojamiento(query, alojamiento) -> str:

        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientos(3,Constants.urlei2a(),alojamiento)
        return query

    @staticmethod
    def email_alojamiento(query, alojamiento) -> str:

        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientos(4,Constants.urlei2a(),alojamiento)
        return query

    @staticmethod
    def fax_alojamiento(query, alojamiento) -> str:

        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientos(6,Constants.urlei2a(),alojamiento)
        return query

    @staticmethod
    def web_alojamiento(query, alojamiento) -> str:

        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientos(2,Constants.urlei2a(),alojamiento)
        return query

    @staticmethod
    def direccion_alojamiento(query, alojamiento) -> str:

        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientos(0,Constants.urlei2a(),alojamiento)
        return query

    @staticmethod
    def listado_alojamiento(query, municipio) -> str:

        query = TemplatesTurismo.obtenerInformacionQueryInicialListaAlojamientos(Constants.urlei2a(),municipio)
        return query

    @staticmethod
    def reserva_alojamiento(query, alojamiento) -> str:

        answers = [4,3]
        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientosAllInformation(answers,Constants.urlei2a(),alojamiento)
        return query

    @staticmethod
    def reserva_alojamiento_telephone(query, alojamiento) -> str:

        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientos(3,Constants.urlei2a(),alojamiento)
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

        query = TemplatesTurismo.obtenerInformacionQueryInicialCountAlojamientos(Constants.urlei2a(),municipio)
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

        query = TemplatesTurismo.obtenerInformacionQueryInicialAlojamientos(5,Constants.urlei2a(),alojamiento)
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

        parameters = []
        parameters.append([Constants.nombreagencia(),agencia])
        query = TemplatesTurismo.obtenerInformacionAgenciasViajes(agencia,Constants.telefonoagencia(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def email_agencia_viaje(query, agencia) -> str:

        parameters = []
        parameters.append([Constants.nombreagencia(),agencia])
        query = TemplatesTurismo.obtenerInformacionAgenciasViajes(agencia,Constants.emailagencia(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def web_agencia_viaje(query, agencia) -> str:

        parameters = []
        parameters.append([Constants.nombreagencia(),agencia])
        query = TemplatesTurismo.obtenerInformacionAgenciasViajes(agencia,Constants.webagencia(),Constants.urlei2a(),parameters)
        return query

    @staticmethod
    def direccion_agencia_viaje(query, agencia) -> str:

        parameters = []
        parameters.append([Constants.nombreagencia(),agencia])
        query = TemplatesTurismo.obtenerInformacionAgenciasViajes(agencia,Constants.direccionagencia(),Constants.urlei2a(),parameters)
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
            alojamiento = "%registro-alojamiento-hotelero%"
        elif tipo_alojamiento == "albergue":
            alojamiento = "%registro-albergue-refugio%"
        elif tipo_alojamiento == "apartamento":
            alojamiento = "%registro-apartamento-turistico%"
        elif tipo_alojamiento == "casa rural":
            alojamiento = "%registro-alojamientos-turismo-rural%"
        elif tipo_alojamiento == "camping":
            alojamiento = "%registro-camping-turistico%"

        query = TemplatesTurismo.obtenerInformacionQueryFinalAlojamientos(query,alojamiento)
        return query

    @staticmethod
    def extra_tipo_lugar(query, tipo_lugar) -> str:
        tipo_lugar = tipo_lugar.lower()

        if tipo_lugar == "provincia":
            query = query.replace("muncipio", "provincia")

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

    @staticmethod
    def obtenerInformacionEstablecimientosHotelero(location: str, columna: str, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT """ + columna + """ as ?answer0 ?registro_alojamiento_hotelero_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_alojamiento_hotelero rdf:type org:Organization . OPTIONAL {?registro_alojamiento_hotelero dc:identifier ?registro_alojamiento_hotelero_dc_identifier.} OPTIONAL {?registro_alojamiento_hotelero dc:title ?registro_alojamiento_hotelero_dc_title . } OPTIONAL {?registro_alojamiento_hotelero org:identifier ?registro_alojamiento_hotelero_org_identifier . } OPTIONAL {?registro_alojamiento_hotelero foaf:homepage ?registro_alojamiento_hotelero_foaf_homepage . } OPTIONAL {?registro_alojamiento_hotelero org:classification ?registro_alojamiento_hotelero_org_classification . } OPTIONAL {?registro_alojamiento_hotelero org:linkedTo ?registro_alojamiento_hotelero_org_linkedTo . } OPTIONAL {?registro_alojamiento_hotelero org:hasSite ?org_hasSite . } OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress . } OPTIONAL {?org_siteAddress vcard:street-address ?org_siteAddress_vcard_street_address . } OPTIONAL {?org_siteAddress vcard:postal-code ?org_siteAddress_vcard_postal_code . } OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel . } OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email . } OPTIONAL {?org_siteAddress vcard:locality ?org_siteAddress_vcard_locality . } OPTIONAL {?org_siteAddress vcard:fax ?org_siteAddress_vcard_fax . } FILTER (?registro_alojamiento_hotelero like "%registro-alojamiento-hotelero%") . """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter

        return query

    @staticmethod
    def obtenerInformacionEstablecimientosCamping(location: str, columna: str, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT """ + columna + """ as ?answer0 ?registro_camping_turistico_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_camping_turistico rdf:type org:Organization . ?registro_camping_turistico ns:wasUsedBy ?procedencia . ?procedencia ns:wasAssociatedWith <http://opendata.aragon.es/datos/catalogo/dataset/ga-od-core/68> . OPTIONAL {?registro_camping_turistico dc:identifier ?registro_camping_turistico_dc_identifier . } OPTIONAL {?registro_camping_turistico dc:title ?registro_camping_turistico_dc_title . } OPTIONAL {?registro_camping_turistico dc:description ?registro_camping_turistico_dc_description . } OPTIONAL {?registro_camping_turistico foaf:homepage ?registro_camping_turistico_foaf_homepage . } OPTIONAL {?registro_camping_turistico dc:date ?registro_camping_turistico_dc_date . } OPTIONAL {?registro_camping_turistico org:classification ?registro_camping_turistico_org_classification . } OPTIONAL {?registro_camping_turistico org:linkedTo ?registro_camping_turistico_org_linkedTo . } OPTIONAL {?registro_camping_turistico org:hasSite ?org_hasSite . } OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress . } OPTIONAL {?org_siteAddress vcard:street-address ?org_siteAddress_vcard_street_address . } OPTIONAL {?org_siteAddress vcard:postal-code ?org_siteAddress_vcard_postal_code . } OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel . } OPTIONAL {?org_siteAddress vcard:fax ?org_siteAddress_vcard_fax . } OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email . }"""
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter
        query += """}"""

        return query

    @staticmethod
    def obtenerInformacionEstablecimientosRestaurantesCafeterias(location: str, columna: str, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT """ + columna + """ as ?answer0 ?registro_cafeteria_restaurante_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_cafeteria_restaurante rdf:type org:Organization. OPTIONAL {?registro_cafeteria_restaurante dc:identifier ?registro_cafeteria_restaurante_dc_identifier . } OPTIONAL {?registro_cafeteria_restaurante dc:title ?registro_cafeteria_restaurante_dc_title . } OPTIONAL {?registro_cafeteria_restaurante dc:description ?registro_cafeteria_restaurante_dc_description . } OPTIONAL {?registro_cafeteria_restaurante foaf:homepage ?registro_cafeteria_restaurante_foaf_homepage . } OPTIONAL {?registro_cafeteria_restaurante dc:date ?registro_cafeteria_restaurante_dc_date . } OPTIONAL {?registro_cafeteria_restaurante org:classification ?registro_cafeteria_restaurante_org_classification . } OPTIONAL {?registro_cafeteria_restaurante org:linkedTo ?registro_cafeteria_restaurante_org_linkedTo . } OPTIONAL {?registro_cafeteria_restaurante org:hasSite ?org_hasSite . } OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress . } OPTIONAL {?org_siteAddress vcard:street-address ?org_siteAddress_vcard_street_address . } OPTIONAL {?org_siteAddress vcard:postal-code ?org_siteAddress_vcard_postal_code . } OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel . } OPTIONAL {?org_siteAddress vcard:fax ?org_siteAddress_vcard_fax . } OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email . } FILTER (?registro_cafeteria_restaurante like "%registro-cafeteria%") . """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter
        
        return query

    @staticmethod
    def obtenerInformacionCompletaEstablecimientosRestaurantesCafeterias(location: str, columnas: list, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT """
        index = 0
        for columna in columnas:
            query += columna + """ as ?answer""" + str(index) + " "
            index = index + 1
        query += """ ?registro_cafeteria_restaurante_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_cafeteria_restaurante rdf:type org:Organization. OPTIONAL {?registro_cafeteria_restaurante dc:identifier ?registro_cafeteria_restaurante_dc_identifier . } OPTIONAL {?registro_cafeteria_restaurante dc:title ?registro_cafeteria_restaurante_dc_title . } OPTIONAL {?registro_cafeteria_restaurante dc:description ?registro_cafeteria_restaurante_dc_description . } OPTIONAL {?registro_cafeteria_restaurante foaf:homepage ?registro_cafeteria_restaurante_foaf_homepage . } OPTIONAL {?registro_cafeteria_restaurante dc:date ?registro_cafeteria_restaurante_dc_date . } OPTIONAL {?registro_cafeteria_restaurante org:classification ?registro_cafeteria_restaurante_org_classification . } OPTIONAL {?registro_cafeteria_restaurante org:linkedTo ?registro_cafeteria_restaurante_org_linkedTo . } OPTIONAL {?registro_cafeteria_restaurante org:hasSite ?org_hasSite . } OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress . } OPTIONAL {?org_siteAddress vcard:street-address ?org_siteAddress_vcard_street_address . } OPTIONAL {?org_siteAddress vcard:postal-code ?org_siteAddress_vcard_postal_code . } OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel . } OPTIONAL {?org_siteAddress vcard:fax ?org_siteAddress_vcard_fax . } OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email . } FILTER (?registro_cafeteria_restaurante like "%registro-cafeteria%") . """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter
        
        return query


    @staticmethod
    def obtenerInformacionCountEstablecimientosRestaurantesCafeterias(location: str, columna: str, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT COUNT (DISTINCT """ + columna + """) as ?answer0 ?registro_cafeteria_restaurante_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_cafeteria_restaurante rdf:type org:Organization. OPTIONAL {?registro_cafeteria_restaurante dc:identifier ?registro_cafeteria_restaurante_dc_identifier . } OPTIONAL {?registro_cafeteria_restaurante dc:title ?registro_cafeteria_restaurante_dc_title . } OPTIONAL {?registro_cafeteria_restaurante dc:description ?registro_cafeteria_restaurante_dc_description . } OPTIONAL {?registro_cafeteria_restaurante foaf:homepage ?registro_cafeteria_restaurante_foaf_homepage . } OPTIONAL {?registro_cafeteria_restaurante dc:date ?registro_cafeteria_restaurante_dc_date . } OPTIONAL {?registro_cafeteria_restaurante org:classification ?registro_cafeteria_restaurante_org_classification . } OPTIONAL {?registro_cafeteria_restaurante org:linkedTo ?registro_cafeteria_restaurante_org_linkedTo . } OPTIONAL {?registro_cafeteria_restaurante org:hasSite ?org_hasSite . } OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress . } OPTIONAL {?org_siteAddress vcard:street-address ?org_siteAddress_vcard_street_address . } OPTIONAL {?org_siteAddress vcard:postal-code ?org_siteAddress_vcard_postal_code . } OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel . } OPTIONAL {?org_siteAddress vcard:fax ?org_siteAddress_vcard_fax . } OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email . } FILTER (?registro_cafeteria_restaurante like "%registro-cafeteria%") . """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter

        return query 

    @staticmethod
    def obtenerInformacionGuiasTuristicos(location: str, columna: str, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT """ + columna + """ as ?answer0 ?registro_guia_turismo_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_guia_turismo rdf:type org:Organization. ?registro_guia_turismo ns:wasUsedBy ?procedencia. ?procedencia ns:wasAssociatedWith <http://opendata.aragon.es/datos/catalogo/dataset/ga-od-core/69>. OPTIONAL {?registro_guia_turismo dc:identifier ?registro_guia_turismo_dc_identifier.} OPTIONAL {?registro_guia_turismo dc:title ?registro_guia_turismo_dc_title.} OPTIONAL {?registro_guia_turismo foaf:homepage ?registro_guia_turismo_foaf_homepage.} OPTIONAL {?registro_guia_turismo org:classification ?registro_guia_turismo_org_classification.} OPTIONAL {?registro_guia_turismo org:hasSite ?org_hasSite.} OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress.} OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel.} OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email.} """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter

        return query

    @staticmethod
    def obtenerInformacionCompletaInformacionGuia(location: str, columnas: list, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT """
        index = 0
        for columna in columnas:
            query += columna + """ as ?answer""" + str(index) + " "
            index = index + 1
        query += """ ?registro_guia_turismo_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_guia_turismo rdf:type org:Organization. ?registro_guia_turismo ns:wasUsedBy ?procedencia. ?procedencia ns:wasAssociatedWith <http://opendata.aragon.es/datos/catalogo/dataset/ga-od-core/69>. OPTIONAL {?registro_guia_turismo dc:identifier ?registro_guia_turismo_dc_identifier.} OPTIONAL {?registro_guia_turismo dc:title ?registro_guia_turismo_dc_title.} OPTIONAL {?registro_guia_turismo foaf:homepage ?registro_guia_turismo_foaf_homepage.} OPTIONAL {?registro_guia_turismo org:classification ?registro_guia_turismo_org_classification.} OPTIONAL {?registro_guia_turismo org:hasSite ?org_hasSite.} OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress.} OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel.} OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email.} """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter
        
        return query
    
    @staticmethod
    def obtenerInformacionAgenciasViajes(location: str, columna: str, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT """ + columna + """ as ?answer0 ?registro_agencias_viaje_dc_title as ?etiqueta FROM """ + urlei2a + """ WHERE { ?registro_agencias_viaje rdf:type org:Organization. ?registro_agencias_viaje ns:wasUsedBy ?procedencia. ?procedencia ns:wasAssociatedWith <http://opendata.aragon.es/datos/catalogo/dataset/ga-od-core/63>. OPTIONAL {?registro_agencias_viaje dc:identifier ?registro_agencias_viaje_dc_identifier.} OPTIONAL {?registro_agencias_viaje dc:title ?registro_agencias_viaje_dc_title.} OPTIONAL {?registro_agencias_viaje dc:description ?registro_agencias_viaje_dc_description.} OPTIONAL {?registro_agencias_viaje foaf:homepage ?registro_agencias_viaje_foaf_homepage.} OPTIONAL {?registro_agencias_viaje dc:date ?registro_agencias_viaje_dc_date.} OPTIONAL {?registro_agencias_viaje org:classification ?registro_agencias_viaje_org_classification.} OPTIONAL {?registro_agencias_viaje org:linkedTo ?registro_agencias_viaje_org_linkedTo.} OPTIONAL {?registro_agencias_viaje org:hasSite ?org_hasSite.} OPTIONAL {?org_hasSite org:siteAddress ?org_siteAddress.} OPTIONAL {?org_siteAddress vcard:street-address ?org_siteAddress_vcard_street_address.} OPTIONAL {?org_siteAddress vcard:postal-code ?org_siteAddress_vcard_postal_code.} OPTIONAL {?org_siteAddress vcard:tel ?org_siteAddress_vcard_tel.} OPTIONAL {?org_siteAddress vcard:email ?org_siteAddress_vcard_email.} """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter
 
        return query

    @staticmethod
    def obtenerInformacionOficinaTurismo(location: str, urlei2a: str) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT ?answer0 ?answer1 ?answer2 ?etiqueta FROM """ + urlei2a + """ where { ?id rdf:type org:Organization . FILTER (?id like "%registro-punto-informacion-turistica%" || ?id like "%registro-oficina-turismo%") . ?id dc:title ?answer0 . ?id org:hasSite ?site . OPTIONAL {?id org:linkedTo ?etiqueta .} FILTER (REGEX(?answer0, """ + '"' + location + '"' + """, "i")  || (?etiqueta like "%municipio%"  &&  REGEX(?etiqueta, """ + '"' + location + '"' + ""","i"))) . ?site org:siteAddress ?address . ?address vcard:street-address ?answer1 . ?site org:siteAddress ?address . ?address vcard:tel ?answer2 ."""
 
        return query

    @staticmethod
    def obtenerInformacionSenderos(location: str, urlei2a: str) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT ?description as ?answer0 ?etiqueta FROM """ + urlei2a + """ { ?id rdf:type vcard:Location FILTER (?id like "%/turismo/lugar/ruta%") . ?id vcard:fn ?etiqueta . ?id vcard:note ?description . FILTER REGEX(?description, """ + '"' + location + '"' + """, "i")"""
 
        return query

    @staticmethod
    def obtenerInformacionOficinasDeTurismo(location: str, columna: str, urlei2a: str, conditions : list) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT DISTINCT """ + columna + """ as ?answer0 ?senderos_turisticos_aragon_vcard_fn as ?etiqueta FROM """ + urlei2a + """ WHERE { ?senderos_turisticos_aragon rdf:type vcard:Location. ?senderos_turisticos_aragon ns:wasUsedBy ?procedencia. ?procedencia ns:wasAssociatedWith <http://opendata.aragon.es/datos/catalogo/dataset/ga-od-core/218>. OPTIONAL {?senderos_turisticos_aragon vcard:fn ?senderos_turisticos_aragon_vcard_fn.} """
        queryFilter = TemplatesTurismo.getQueryFilter(conditions)
        query += queryFilter
 
        return query

    @staticmethod
    def obtenerInformacionMunicipioRestaurante(location: str, urlei2a: str) -> str:

        location = TemplatesTurismo.bifString(location)

        query = """SELECT """
        query += "COUNT(DISTINCT ?answer0) as ?answer0"
        query += """ ?etiqueta FROM """ + urlei2a + """ WHERE {?id rdf:type	org:Organization . ?id <http://purl.org/dc/elements/1.1/title> ?answer0 . FILTER (?id like "%registro-cafeteria%") . ?id <http://www.w3.org/ns/org#linkedTo> ?etiqueta  . FILTER REGEX(?etiqueta  , """ + '"' + location + '"' + """, "i") . """
 
        return query

    @staticmethod
    def obtenerInformacionQueryInicialAlojamientos(answerPosition: int, urlei2a: str, location: str) -> str:

        location = TemplatesTurismo.bifString(location)
        query = """SELECT  DISTINCT ?answer""" + str(answerPosition) + """ as ?answer0 ?etiqueta FROM """ + urlei2a + """ where { ?id rdf:type org:Organization . ?id dc:title ?etiqueta . filter REGEX(?etiqueta, """ + '"' + location + '"' + """, "i")  . """
        return query  

    @staticmethod
    def obtenerInformacionQueryInicialAlojamientosAllInformation(answerPosition: list, urlei2a: str, location: str) -> str:

        location = TemplatesTurismo.bifString(location)
        index = 0
        query = """SELECT  DISTINCT """
        for row in answerPosition:
            query += "?answer""" + str(row) + """ as ?answer""" + str(index) + " "
            index = index + 1
        query += """ ?etiqueta FROM """ + urlei2a + """ where { ?id rdf:type org:Organization . ?id dc:title ?etiqueta . filter REGEX(?etiqueta, """ + '"' + location + '"' + """, "i")  . """
        return query

    @staticmethod
    def obtenerInformacionQueryInicialCountAlojamientos(urlei2a: str, location: str) -> str:

        location = TemplatesTurismo.bifString(location)
        query = """SELECT  COUNT(DISTINCT ?answer0) as ?answer0 FROM """ + urlei2a + """ where { ?id rdf:type org:Organization . ?id dc:title ?etiqueta . filter REGEX(?etiqueta, """ + '"' + location + '"' + """, "i")  . """
        return query

    @staticmethod
    def obtenerInformacionQueryFinalAlojamientos(query: str,tipoAlojamiento: str) -> str:
        
        query += """ FILTER (?id like """ + '"' + tipoAlojamiento + '"'+ """) . ?id org:hasSite ?site . OPTIONAL {?id foaf:homepage ?answer2 .} OPTIONAL {?id org:linkedTo ?answer5} . ?site org:siteAddress ?address . OPTIONAL {?address vcard:street-address ?answer0} . OPTIONAL {?address vcard:postal-code ?answer1} . OPTIONAL {?address vcard:tel ?answer3} . OPTIONAL {?address vcard:email ?answer4} . OPTIONAL {?address vcard:fax ?answer6}  ."""
        return query

    @staticmethod
    def obtenerInformacionQueryInicialListaAlojamientos(urlei2a: str, location: str) -> str:
        
        try:
            code = int(location)
            iscode = True
        except:
            iscode = False
            location = TemplatesTurismo.bifString(location)
        query = """SELECT  DISTINCT ?answer7 as ?answer0 """
        if iscode == False:
            query += """?etiqueta FROM """ + urlei2a
            query += """ where { {?id org:linkedTo ?etiqueta . Filter (?etiqueta like "%municipio%" && REGEX(?etiqueta, """
            query += '"' + location + '"' + """, "i"))} ?id dc:title ?answer7 """
        else:
            query += """?answer1 as ?etiqueta FROM """ + urlei2a
            query += """ where { ?id org:linkedTo ?etiqueta . FILTER (?answer1 like '""" + str(code) + """%') . """
            query += """?id dc:title ?answer7 """
        return query

    @staticmethod
    def getQueryFilter(conditions):

        query = ""
        if conditions != []:
            for row in conditions:
                key = row[0]
                value = row[1]
                value = TemplatesTurismo.bifString(value)
                query += """ FILTER regex(""" + key + """, """ + '"' + value + '"' + """, "i") . """
        return query

    @staticmethod
    def bifString(cadena: str) -> str:

        if cadena.lower().startswith("la "):
            cadena = cadena[3:]
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)

        return cadena

    @staticmethod
    def bifStringLine(cadena: str) -> str:

        if cadena.lower().startswith("la "):
            cadena = cadena[3:]
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
        cadena = cadena.replace(' ','[/w-]')

        return cadena       