"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import re
from browser.config import Config
from browser.constants import Constants
from browser.logger import Log


class TemplatesAragon:
    """[summary]
    """

    @staticmethod
    def lemmatizer(msg: str, nlp) -> str:

        """ This function lemmatizes the message. 
        Parameter
        ----------
            msg str
            nlp 
        
        Returns
        ---------
            str
            """

        lemmatize_msg = ""
        for token in nlp(msg):
            lemmatize_msg += token.lemma_ + " "
        return lemmatize_msg

    @staticmethod
    def selecting_max_year(grafo: str, answerpart: str) -> str:

        """ This function gets the maiximum year of a graph. 
        Parameter
        ----------
            grafo str
            answerpart str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function does some regex transformation from a concrete text (cadena). 
        Parameter
        ----------
            cadena: str
            variable: str
        
        Returns
        ---------
            query str
            """

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

        """ This function add the greater condition to the final query. 
        Parameter
        ----------
            cadena: int
            variable: str
        
        Returns
        ---------
            str
            """

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

        """ This function added the necessary code to do the regex using the string and the variable. 
        Parameter
        ----------
            cadena str
            variable str
        
        Returns
        ---------
            query str
            """

        query = " filter REGEX(" + variable + ", " + cadena + ")"
        return query

    @staticmethod
    def base_query() -> str:

        """ This function prepares the initial instruction of sparql query
        
        Returns
        ---------
            base str
            """

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
        
        """ This function added the necessary code to get the county from the village applying in the database. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the area of a village. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the population of a village. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the dryland area of a village. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the population of a village. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """        
        
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

        """ This function gets the foreign population a village. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the telephone number of the city hall. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query = TemplatesAragon.obtenerInformacionAyuntamiento(Constants.telefonoayuntamiento(),municipio,Constants.urlei2a(),Constants.urlei2adatoscatalogo(),Constants.typecolumnaddress(),Constants.telefonoayuntamientoproperty(),Constants.telefonoayuntamientovalue())
        return query

    @staticmethod
    def cif_ayuntamiento(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        """ This function gets the CIF number of the city hall. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query = TemplatesAragon.obtenerInformacionAyuntamiento(Constants.cifayuntamiento(),municipio,Constants.urlei2a(),Constants.urlei2adatoscatalogo(),Constants.typecolumnmunicipio(),Constants.cifayuntamientoproperty(),Constants.cifayuntamientovalue())
        return query

    @staticmethod
    def email_ayuntamiento(query, municipio) -> str:
        # municipio = municipio.upper()  # En el campo esta en mayusculas el municipio

        """ This function gets the email of the city hall. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """        
        
        query = TemplatesAragon.obtenerInformacionAyuntamiento(Constants.emailayuntamiento(),municipio,Constants.urlei2a(),Constants.urlei2adatoscatalogo(),Constants.typecolumnaddress(),Constants.emailayuntamientoproperty(),Constants.emailayuntamientovalue())
        return query

    @staticmethod
    def cargo_municipio(query, municipio) -> str:

        """ This function gets the city halls positions. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query = TemplatesAragon.obtenerMunicipio(query,municipio)
        return query

    @staticmethod
    def fax_municipio(query, municipio) -> str:

        """ This function gets the fax number of the city hall. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """       
        
        query = TemplatesAragon.obtenerInformacionAyuntamiento(Constants.faxayuntamiento(),municipio,Constants.urlei2a(),Constants.urlei2adatoscatalogo(),Constants.typecolumnaddress(),Constants.faxayuntamientoproperty(),Constants.faxayuntamientovalue())
        return query

    @staticmethod
    def direccion_ayuntamiento(query, municipio) -> str:

        """ This function gets the city hall address.
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query = TemplatesAragon.obtenerInformacionAyuntamiento(Constants.direccionayuntamiento(),municipio,Constants.urlei2a(),Constants.urlei2adatoscatalogo(),Constants.typecolumnaddress(),Constants.direccionayuntamientoproperty(),Constants.direccionayuntamientovalue())
        return query
        
    @staticmethod
    def num_contenedores_vidrio(query, municipio) -> str:

        """ This function gets the number of glasses containers of a concrete town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the total glasses kilograms recovered in a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the total hectarea of an area. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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
            Constants.grafo_hectareas_zona(), answerpart
        )
        return query

    @staticmethod
    def num_incendios(query, municipio) -> str:

        """ This function gets the number of fires of a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the number of burned area in a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the telephone number of the city hall. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the total number of autonomous of a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the total number of unemployed. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the total number of employed in a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the total number of work accidents in a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the rent per capita of a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the list of companies with its number of employees. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """        
        
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

        """ This function gets the number of companies grouped by areas. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the number of companies grouped by actvities. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the total number of ground which is using in a town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """        
        
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

        """ This function gets the number of hectares per every floor type. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the existing number of buildings per year for the town. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function controls to recover the information of a concrete year. 
        Parameter
        ----------
            query str
            year str
        
        Returns
        ---------
            query str
            """
        
        query += Constants.observacion() + " aragopedia:year " + Constants.fecha()

        query += TemplatesAragon.create_bif_contains(year, Constants.fecha()) + " . "

        return query

    @staticmethod
    def year_dataset(query, year) -> str:

        """ This function controls to recover the information of a concrete year from the database. 
        Parameter
        ----------
            query str
            year str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function controls to recover the maximum value of a parameter. 
        Parameter
        ----------
            query str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function get the maximum year of the database. 
        Parameter
        ----------
            query str
            cadena str
        
        Returns
        ---------
            query str
            """
        
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

    @staticmethod
    def cargo(query, cargo) -> str:

        """ This function gets the position of a concrete user. 
        Parameter
        ----------
            query str
            cargo str
        
        Returns
        ---------
            query str
            """
        
        query = TemplatesAragon.obtenerCargo(cargo,Constants.urlei2a())
        return query

    @staticmethod
    def tipo_localizacion_poblacion(query, tipo_localizacion) -> str:
        
        """ This function gets the type of location of a population. 
        Parameter
        ----------
            query str
            tipo_localizacion str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the number of foreigner depending on the type of area. 
        Parameter
        ----------
            query str
            tipo_area str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the localization type in general. 
        Parameter
        ----------
            query str
            tipo_localizacion str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the population of an area filter by foreigners. 
        Parameter
        ----------
            query str
            nombre_area str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function gets the population of an area filter by sex. 
        Parameter
        ----------
            query str
            sexo str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function gets the diferent types of surfaces. 
        Parameter
        ----------
            query str
            tipo_superficie str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function adds the diferent types of fields in the query. 
        Parameter
        ----------
            query str
            tipo_superficie str
        
        Returns
        ---------
            query str
            """        
        
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

        """ This function adds number of employees in the query. 
        Parameter
        ----------
            query str
            trabajadores str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function adds the activity in the query. 
        Parameter
        ----------
            query str
            actividad str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function adds the floors type in the query. 
        Parameter
        ----------
            query str
            tipo_suelo str
        
        Returns
        ---------
            query str
            """                
        
        query = query.replace("tiposuelo", tipo_suelo + "-superficie")

        return query

    @staticmethod
    def antiguedad(query: str, antiguedad: str) -> str:

        """ This function adds the antiquity in the query. 
        Parameter
        ----------
            query str
            antiguedad str
        
        Returns
        ---------
            query str
            """
        
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

        """ This function adds the active companies. 
        Parameter
        ----------
            query str
            location str
        
        Returns
        ---------
            query str
            """
        
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
        
        """ This function replace a strings value using several regex functions. 
        Parameter
        ----------
            cadena str
        
        Returns
        ---------
            cadena str
            """
        
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
        return cadena

    @staticmethod
    def empresasActivasActividades(query: str, location: str) -> str:

        """ This function adds the contact of the activities of active companies in the query. 
        Parameter
        ----------
            query str
            location str
        
        Returns
        ---------
            query str
            """        

        query += (''''''
        )

        return query

    @staticmethod
    def empresasActivasContacto(query: str, location: str) -> str:

        """ This function adds the contact of the active companies in the query. 
        Parameter
        ----------
            query str
            location str
        
        Returns
        ---------
            query str
            """        
        
        query += (''''''
        )

        return query

    @staticmethod
    def empresasActivasDireccion(query: str, location: str) -> str:

        """ This function adds the address value of the active companies in the query. 
        Parameter
        ----------
            query str
            location str
        
        Returns
        ---------
            query str
            """        
        
        query += (''''''
        )

        return query

    def bifMunicipio(cadena: str) -> str:

        """ This function replace the towns value applying some regex operations. 
        Parameter
        ----------
            query str
            location str
        
        Returns
        ---------
            query str
            """                
        
        if cadena.lower().startswith("la "):
            cadena = cadena[3:]
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)

        return cadena

    def obtenerInformacionAyuntamiento(columna: str, location: str, urlei2a: str, datoscatalogo : str, type: str, property : str, value : str) -> str:

        """ This function all the information of city hall. 
        Parameter
        ----------
            columna str
            location str
            urlei2a str
            datoscatalogo str
            type str
            property str
            value str
        
        Returns
        ---------
            query str
            """                
        
        location = TemplatesAragon.bifMunicipio(location)

        query = """SELECT DISTINCT """ + columna + """ as ?answer0 ?etiqueta FROM """ + urlei2a + """ WHERE { ?municipio rdf:type org:Organization. ?municipio ns:wasUsedBy ?procedencia . ?procedencia ns:wasAssociatedWith """ + datoscatalogo + """ . ?municipio org:hasSite ?org_hasSite. ?org_hasSite org:siteAddress ?org_siteAddress . """ + type + " " + value + " " + property + """ . ?org_siteAddress vcard:locality ?etiqueta . filter REGEX(lcase(REPLACE(str(?etiqueta ),"_"," ")), """ + '"' + location + '"' + """, "i") """

        return query

    def obtenerCargo(cargo: str, urlei2a: str) -> str:

        """ This function gets all the positions of the city hall 
        Parameter
        ----------
            cargo str
            urlei2a str
        
        Returns
        ---------
            query str
            """    

        query = """select ?answer as ?answer0 ?etiqueta FROM """ + urlei2a 
                
        query2 = """ where { ?alcalde foaf:name ?answer . ?alcalde org:holds ?cargo . ?cargo org:role ?cargo2 . ?cargo2 dc:title """
                
        query3 = '"' + cargo.upper() + '"' + """ ."""

        query = query + query2 + query3

        return query

    def obtenerMunicipio(query: str,location: str) -> str:

        """ This function gets all the positions of the city hall of a concrete location 
        Parameter
        ----------
            query str
            location str
        
        Returns
        ---------
            query str
            """        
        
        location = TemplatesAragon.bifMunicipio(location)

        query += """ ?cargo org:postIn ?municipio . ?municipio dc:title ?etiqueta filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), """ + '"' + location + '"' + """, "i") """
                
        return query
