'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import re
from browser.config import Config
from browser.constants import Constants
from browser.logger import Log


class TemplatesAragon:
    """[summary]
    """

    @staticmethod
    def lemmatizer(msg: str, nlp) -> str:
        lemmatize_msg = ""
        for token in nlp(msg):
            lemmatize_msg += token.lemma_ + " "
        return lemmatize_msg

    @staticmethod
    def selecting_max_year(grafo: str, answerpart: str) -> str:

        query = " { SELECT DISTINCT MAX(xsd:integer(?max)) as " + Constants.year_max()

        query += " FROM " + grafo

        query += " WHERE { "

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> "
            + Constants.fecha()
            + " . "
        )

        query += (
            "BIND(SUBSTR(STRDT(" + Constants.fecha() + ", xsd:string),38,4) as ?max) . "
        )

        query += answerpart

        query += " }}"
        return query

    @staticmethod
    def create_bif_contains(cadena: str, variable: str) -> str:
        #cadena = cadena.removeprefix('La ')# caso que los municipios se detectan como La Almunia y el la base de datos esta Almunia, La
        if cadena.lower().startswith("la "):
            cadena = cadena[3:]
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
        
        return " filter REGEX(lcase(REPLACE(str(" + variable + '),"_"," ")), "' + cadena + '", "i")  '
        

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
    def create_filter_regex_var(cadena: str, variable: str) -> str:
        query = " filter REGEX(" + variable + ", " + cadena + ")"
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

    @staticmethod
    def comarca_del_municipio(query, municipio) -> str:
        query += (
            Constants.municipio()
            + " aragopedia:enComarca "
            + Constants.comarca()
            + " . "
        )

        query += Constants.municipio() + " rdfs:label " + Constants.etiqueta()

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += Constants.comarca() + " rdfs:label " + Constants.answer0() + " . "
        return query

    @staticmethod
    def superficie_municipio(query, municipio) -> str:
        query += (
            Constants.municipio()
            + " aragopedia:areaTotal "
            + Constants.answer0()
            + " . "
        )
        query += Constants.municipio() + " rdfs:label " + Constants.etiqueta()

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )
        return query

    @staticmethod
    def habitantes_municipio(query, municipio) -> str:
        query = query.replace(
            Constants.answer0(), Constants.answer0() + " " + Constants.answer1()
        )

        query += (
            Constants.municipio()
            + " aragopedia:menPopulation "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.municipio()
            + " aragopedia:womenPopulation "
            + Constants.answer1()
            + " . "
        )

        query += Constants.municipio() + " rdfs:label " + Constants.etiqueta()

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )
        return query

    @staticmethod
    def superficie_secano(query, municipio) -> str:
        query += (
            Constants.municipio()
            + " aragopedia:hasObservation "
            + Constants.observacion()
            + " . "
        )
        query += Constants.municipio() + " rdfs:label " + Constants.etiqueta()

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.observacion()
            + " aragopedia:hectareasCultivosSecano "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def superficie_regadio(query, municipio) -> str:
        query += (
            Constants.municipio()
            + " aragopedia:hasObservation "
            + Constants.observacion()
            + " . "
        )

        query += Constants.municipio() + " rdfs:label " + Constants.etiqueta()

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.observacion()
            + " aragopedia:hectareasCultivosRegadio "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def poblacion(query, municipio) -> str:

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#poblacion> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def poblacion_extranjeros(query, municipio) -> str:

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )
        return query

    @staticmethod
    def telefono_ayuntamiento(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.municipio() + " " + Constants.aux0() + " ei2a:Ayuntamiento . "
        )

        query += (
            Constants.municipio() + " ei2a:organizationName " + Constants.etiqueta()
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += Constants.municipio() + " ei2a:phone " + Constants.answer0() + " . "
        return query

    @staticmethod
    def cif_ayuntamiento(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.municipio() + " " + Constants.aux0() + " ei2a:Ayuntamiento . "
        )

        query += (
            Constants.municipio() + " ei2a:organizationName " + Constants.etiqueta()
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += Constants.municipio() + " ei2a:CIF " + Constants.answer0() + " . "
        return query

    @staticmethod
    def email_ayuntamiento(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.municipio() + " " + Constants.aux0() + " ei2a:Ayuntamiento . "
        )

        query += (
            Constants.municipio() + " ei2a:organizationName " + Constants.etiqueta()
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += Constants.municipio() + " foaf:mbox " + Constants.answer0() + " . "
        return query

    @staticmethod
    def cargo_municipio(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.id_membresia()
            + " org:organization "
            + Constants.municipio()
            + " . "
        )

        query += (
            Constants.municipio() + " ei2a:organizationName " + Constants.etiqueta()
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )
        return query

    @staticmethod
    def fax_municipio(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.municipio() + " " + Constants.aux0() + " ei2a:Ayuntamiento . "
        )

        query += (
            Constants.municipio() + " ei2a:organizationName " + Constants.etiqueta()
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += Constants.municipio() + " org:hasSite " + Constants.sede() + " . "

        query += Constants.sede() + " org:siteAddress " + Constants.aux1() + " . "

        query += Constants.aux1() + " vcard:Fax " + Constants.answer0() + " . "
        return query

    @staticmethod
    def direccion_ayuntamiento(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        query += (
            Constants.municipio() + " " + Constants.aux0() + " ei2a:Ayuntamiento . "
        )

        query += (
            Constants.municipio() + " ei2a:organizationName " + Constants.etiqueta()
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += Constants.municipio() + " org:hasSite " + Constants.sede() + " . "

        query += Constants.sede() + " org:siteAddress " + Constants.aux1() + " . "

        query += Constants.aux1() + " vcard:hasAddress " + Constants.address() + " . "

        query += (
            Constants.address() + " vcard:street-address " + Constants.answer0() + " . "
        )
        return query

    @staticmethod
    def num_contenedores_vidrio(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_contenedores_vidrio() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        answerpart = (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#contenedores-de-vidrio> "
            + Constants.answer0()
            + " . "
        )

        query += answerpart

        query += TemplatesAragon.selecting_max_year(
            Constants.grafo_contenedores_vidrio(), answerpart
        )
        return query

    @staticmethod
    def kg_vidrio(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_contenedores_vidrio() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#kg-vidrio-domestico> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def hectareas_zona(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_hectareas_zona() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        answerpart = (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#superficie-has> "
            + Constants.answer0()
            + " . "
        )

        query += answerpart

        query += TemplatesAragon.selecting_max_year(
            Constants.grafo_contenedores_vidrio(), answerpart
        )
        return query

    @staticmethod
    def num_incendios(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_incendios() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#incendios> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def hectareas_quemadas(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_incendios() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#superficie-forestal-afectada> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def num_depuradoras(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_depuradoras() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#depuradoras> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def num_autonomos(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_autonomos() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#afiliaciones-en-alta> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def num_parados(query, municipio) -> str:

        query = query.replace("WHERE", " FROM " + Constants.grafo_parados() + " WHERE")

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#n-parados> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def num_contratados(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_contratados() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#numero-de-contratos> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def num_accidentes_laborales(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_accidentes_laborales() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#n-accidentes> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def renta_per_capita(query, municipio) -> str:

        query = query.replace("WHERE", " FROM " + Constants.grafo_renta() + " WHERE")

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#renta-disponible-bruta-per-capita> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def empresas_por_trabajadores(query, municipio) -> str:

        query = query.replace(
            "SELECT DISTINCT ?answer0", "SELECT DISTINCT SUM(?answer0) as ?answer0"
        )

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_trabajadores_empresa() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#numero-empresas> "
            + Constants.answer0()
            + " . "
        )
        return query

    @staticmethod
    def empresas_por_sector(query, municipio) -> str:

        query = query.replace(
            "SELECT DISTINCT ?answer0", "SELECT DISTINCT SUM(?answer0) as ?answer0"
        )

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_sector_empresa() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        answerpart = (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#numero-empresas> "
            + Constants.answer0()
            + " . "
        )

        query += answerpart

        query += TemplatesAragon.selecting_max_year(
            Constants.grafo_sector_empresa(), answerpart
        )
        return query

    @staticmethod
    def empresas_por_actividad(query, municipio) -> str:

        query = query.replace(
            "SELECT DISTINCT ?answer0", "SELECT DISTINCT SUM(?answer0) as ?answer0"
        )

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_actividad_empresa() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        answerpart = (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#numero-de-actividades> "
            + Constants.answer0()
            + " . "
        )

        query += answerpart

        query += TemplatesAragon.selecting_max_year(
            Constants.grafo_sector_empresa(), answerpart
        )
        return query

    @staticmethod
    def uso_suelo(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_uso_suelo() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        answerpart = (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#corine-land-cover-2000-nivel-5-descripcion> "
            + Constants.aux1()
            + " . "
        )

        query += answerpart

        query += (
            "BIND(SUBSTR(STRDT("
            + Constants.aux1()
            + ", xsd:string),80) as"
            + Constants.answer0()
            + ") . "
        )

        query += TemplatesAragon.selecting_max_year(
            Constants.grafo_uso_suelo(), answerpart
        )
        return query

    @staticmethod
    def hectareas_tipo_suelo(query, municipio) -> str:

        query = query.replace(
            "WHERE", " FROM " + Constants.grafo_hectareas_tipo_suelo() + " WHERE"
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        answerpart = (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#tiposuelo> "
            + Constants.answer0()
            + " . "
        )

        query += answerpart

        query += TemplatesAragon.selecting_max_year(
            Constants.grafo_hectareas_tipo_suelo(), answerpart
        )
        return query

    @staticmethod
    def antiguedad_edificios(query, municipio) -> str:

        query = query.replace(
            "WHERE",
            Constants.fecha()
            + " "
            + Constants.etiqueta2()
            + " FROM "
            + Constants.grafo_edificios_construccion()
            + " WHERE",
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(municipio, Constants.etiqueta()) + " . "
        )

        answerpart = (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/medida#numero-hogares> "
            + Constants.answer0()
            + " . "
        )

        query += answerpart

        query += TemplatesAragon.selecting_max_year(
            Constants.grafo_edificios_construccion(), answerpart
        )

        return query

    # *************
    # extra Queries
    # *************

    @staticmethod
    def year(query, year) -> str:

        query += Constants.observacion() + " aragopedia:year " + Constants.fecha()

        query += TemplatesAragon.create_bif_contains(year, Constants.fecha()) + " . "

        return query

    @staticmethod
    def year_dataset(query, year) -> str:

        Log.log_debug("QUERIES_: Entrando a year_dataset()")
        Log.log_debug("QUERIES_: Year entrante: {0} ".format(year))

        if year == "":
            query = TemplatesAragon.year_max_one_paramater(query)
        else:

            Log.log_debug("QUERIES_: query before replacing: {0} ".format(query))

            pos_init = query.find("{ SELECT")
            Log.log_debug("QUERIES_: posicion init: {0} ".format(pos_init))
            pos_end = query.find(" }}")
            Log.log_debug("QUERIES_: posicion end: {0} ".format(pos_end))
            subquery = query[pos_init : pos_end + 3]
            Log.log_debug("QUERIES_: subquery: {0} ".format(subquery))
            query = query.replace(subquery, "")

            Log.log_debug("QUERIES_: query post replace: {0} ".format(query))

            query += (
                Constants.municipio()
                + " <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> "
                + Constants.fecha()
                + " . "
            )

            query += (
                TemplatesAragon.create_bif_contains(year, Constants.fecha()) + " . "
            )

        return query

    

    @staticmethod
    def year_max_one_paramater(query) -> str:

        Log.log_debug("QUERIES_: Entrando a year_dataset_max()")
        Log.log_debug("QUERIES_: query: {0} ".format(query))

        query = query.replace(
            Constants.etiqueta() + "  FROM",
            Constants.etiqueta() + " " + Constants.fecha() + " FROM",
        )

        query += (
            Constants.municipio()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> "
            + Constants.fecha()
            + " . "
        )

        query += (
            TemplatesAragon.create_filter_regex_var(
                "STRDT(" + Constants.year_max() + ", xsd:string)", Constants.fecha()
            )
            + " . "
        )
        return query
    
    @staticmethod
    def year_dataset_max(query, cadena) -> str:

        Log.log_debug("QUERIES_: Entrando a year_dataset_max()")
        Log.log_debug("QUERIES_: query: {0} ".format(query))

        query = query.replace(
            Constants.etiqueta() + "  FROM",
            Constants.etiqueta() + " " + Constants.fecha() + " FROM",
        )

        query += (
                Constants.municipio()
                + " <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> "
                + Constants.fecha()
                + " . "
        )

        try:
            if int(cadena)>1900:
                query += (
                        TemplatesAragon.create_filter_regex_var(
                            "STRDT(" + str(cadena) + ", xsd:string)", Constants.fecha()
                        )
                        + " . "
                )
        except:
            query += (
                    TemplatesAragon.create_filter_regex_var(
                        "STRDT(" + Constants.year_max() + ", xsd:string)", Constants.fecha()
                    )
                    + " . "
            )

        return query
        #return TemplatesAragon.year_dataset_max(query)
   
    @staticmethod
    def cargo(query, cargo) -> str:

        query += Constants.id_membresia() + " org:role " + Constants.id_rol() + " . "

        query += Constants.id_rol() + ' ei2a:roleName "' + cargo.upper() + '" . '

        query += (
            Constants.id_membresia() + " org:member " + Constants.id_persona() + " . "
        )

        query += (
            Constants.id_persona() + " ei2a:fullName " + Constants.answer0() + " . "
        )
        return query

    @staticmethod
    def tipo_localizacion_poblacion(query, tipo_localizacion) -> str:
        tipo_localizacion = tipo_localizacion.lower()

        if tipo_localizacion == "aragon":
            query = query.replace(
                "WHERE", " FROM " + Constants.grafo_poblacion_aragon() + " WHERE"
            )
        elif tipo_localizacion == "municipio":
            query = query.replace(
                "WHERE", " FROM " + Constants.grafo_poblacion_municipio() + " WHERE"
            )
        elif tipo_localizacion == "provincia":
            query = query.replace(
                "WHERE", " FROM " + Constants.grafo_poblacion_provincia() + " WHERE"
            )
        elif tipo_localizacion == "comarca":
            query = query.replace(
                "WHERE", " FROM " + Constants.grafo_poblacion_comarca() + " WHERE"
            )
        return query

    @staticmethod
    def tipo_area_extranjeros(query, tipo_area) -> str:
        tipo_area = tipo_area.lower()

        if tipo_area == "continente":
            query = query.replace(
                "WHERE", " FROM " + Constants.grafo_extranjeros_continente() + " WHERE"
            )

            query += (
                Constants.municipio()
                + " <http://opendata.aragon.es/def/iaest/medida#personas> "
                + Constants.answer0()
                + " . "
            )
        elif tipo_area == "pais":
            query = query.replace(
                "WHERE", " FROM " + Constants.grafo_extranjeros_pais() + " WHERE"
            )

            query += (
                Constants.municipio()
                + " <http://opendata.aragon.es/def/iaest/medida#extranjeros> "
                + Constants.answer0()
                + " . "
            )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#nacionalidad-"
            + tipo_area
            + "-nombre> "
            + Constants.etiqueta2()
            + " . "
        )
        return query

    @staticmethod
    def tipo_localizacion_general(query, tipo_localizacion) -> str:
        tipo_localizacion = tipo_localizacion.lower()

        if tipo_localizacion == "aragon":
            query = query.replace("> WHERE", "A> WHERE")
        elif tipo_localizacion == "municipio":
            query = query.replace("> WHERE", "TM> WHERE")
        elif tipo_localizacion == "provincia":
            query = query.replace("> WHERE", "TP> WHERE")
        elif tipo_localizacion == "comarca":
            query = query.replace("> WHERE", "TC> WHERE")
        return query

    @staticmethod
    def area_filter_extranjeros(query, nombre_area) -> str:
        nombre_area = nombre_area.lower()

        query = query.replace(
            Constants.etiqueta2() + " . ",
            Constants.etiqueta2()
            + " . "
            + TemplatesAragon.create_bif_contains(nombre_area, Constants.etiqueta2())
            + " . ",
        )
        return query

    @staticmethod
    def sexo(query, sexo) -> str:
        sexo = sexo.lower()

        query = query.replace(
            "SELECT DISTINCT ?answer0", "SELECT DISTINCT SUM(?answer0) as ?answer0"
        )

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#sexo> "
            + Constants.aux1()
            + " . "
        )

        if sexo == "mujeres" or sexo == "hombres":
            query += TemplatesAragon.create_bif_contains(sexo, Constants.aux1()) + " . "
        return query

    @staticmethod
    def tipo_superficie(query: str, tipo_superficie: str) -> str:

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#corine-land-cover-2000-nivel-1-descripcion> "
            + Constants.aux1()
            + " . "
        )

        query += TemplatesAragon.create_bif_contains(tipo_superficie, Constants.aux1())
        return query

    @staticmethod
    def sector(query: str, sector: str) -> str:

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#sector-descripcion> "
            + Constants.etiqueta2()
            + " . "
        )

        query += TemplatesAragon.create_bif_contains(sector, Constants.etiqueta2())
        return query

    @staticmethod
    def num_trabajadores(query: str, trabajadores: str) -> str:

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#estrato> "
            + Constants.etiqueta2()
            + " . "
        )

        query += TemplatesAragon.create_bif_contains(
            trabajadores, Constants.etiqueta2()
        )
        return query

    @staticmethod
    def actividad(query: str, actividad: str) -> str:

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#rama-de-actividad> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(actividad, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def tipo_suelo(query: str, tipo_suelo: str) -> str:

        query = query.replace("tiposuelo", tipo_suelo + "-superficie")

        return query

    @staticmethod
    def antiguedad(query: str, antiguedad: str) -> str:

        query += (
            Constants.municipio()
            + " <http://opendata.aragon.es/def/iaest/dimension#ano-de-construccion> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAragon.create_bif_contains(antiguedad, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def empresasActivas(query: str, location: str) -> str:

        query += (

            '''
            ?emp rdf:type org:Organization .

            ?emp ei2a:organizationName ''' + Constants.answer0() + ' . ' +
    
            '''?emp dc:type ?tipo .
    
            FILTER regex(?tipo, "empresa_turismo_activo") .
    
            ?emp geo:location ?loc .
    
            ?loc ?b ''' + Constants.etiqueta() +

            ''' FILTER regex(''' + Constants.etiqueta() + ''', "''' + TemplatesAragon.create_bif_contains_only_change_cadena(location) + '") .'


        )

        return query

    @staticmethod
    def create_bif_contains_only_change_cadena(cadena: str) -> str:
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
        return cadena

    @staticmethod
    def empresasActivasActividades(query: str, location: str) -> str:

        query += (''''''
        )

        return query

    @staticmethod
    def empresasActivasContacto(query: str, location: str) -> str:

        query += (''''''
        )

        return query

    @staticmethod
    def empresasActivasDireccion(query: str, location: str) -> str:

        query += (''''''
        )

        return query
