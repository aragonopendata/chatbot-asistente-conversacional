import re
from browser.config import Config
from browser.constants import Constants


class TemplatesAgriculture:
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

        return "".join(f'{token.lemma_} ' for token in nlp(msg))

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

        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
        query = ""
        query += f' filter REGEX({variable}' + ', "' + cadena + '", "i")'
        return query

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

        return (
            " filter (<http://www.w3.org/2001/XMLSchema#integer> ("
            + variable
            + ") >= "
            + str(cadena)
            + ")"
        )

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
    def comarca_agraria_municipio(query, municipio) -> str:

        """ This function added the necessary code to get the county from the agrarian village applying in the database. 
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """

        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:comarca_agraria . "
        )

        query += (
            Constants.comarca()
            + " ei2a:organizationName "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.etiqueta() + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def municipio_comarca_agraria(query, comarca_agraria) -> str:

        """ This function added the necessary code to get the village from the county applying in the database. 
        
        Parameter
        ----------
            query str
            comarca_agraria str
        
        Returns
        ---------
            query str
            """


        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:comarca_agraria . "
        )

        query += (
            Constants.comarca()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(
                comarca_agraria, Constants.etiqueta()
            )
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.answer0() + " . "
        )
        return query

    @staticmethod
    def villas_municipio(query, municipio) -> str:

        """ This function added the necessary code to get the fields from the villages applying in the database. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:villas_y_tierras . "
        )

        query += (
            Constants.comarca()
            + " ei2a:organizationName "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.etiqueta() + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def municipio_villa(query, villa) -> str:

        """ This function added the necessary code to get the village from the town applying in the database. 
        
        Parameter
        ----------
            query str
            villa str
        
        Returns
        ---------
            query str
            """
        
        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:villas_y_tierras . "
        )

        query += (
            Constants.comarca()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(villa, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.answer0() + " . "
        )
        return query

    @staticmethod
    def info_villa(query, villa) -> str:

        """ This function added the necessary code to get the village info. 
        
        Parameter
        ----------
            query str
            villa str
        
        Returns
        ---------
            query str
            """

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

        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:villas_y_tierras . "
        )

        query += (
            Constants.comarca()
            + " ei2a:organizationName "
            + Constants.etiqueta()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(villa, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.answer0() + " . "
        )

        query += (
            Constants.comarca()
            + " <http://opendata.aragon.es/def/ei2a#phone> "
            + Constants.answer1()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://xmlns.com/foaf/0.1/mbox> "
            + Constants.answer2()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://opendata.aragon.es/def/ei2a#CIF> "
            + Constants.answer3()
            + " . "
        )
        return query

    @staticmethod
    def fincas_cultivo_lenoso_municipio(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_cultivo_lenoso" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:cultivo_lenoso . "
        )

        query += (
            Constants.comarca()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.etiqueta() + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )
        return query

    @staticmethod
    def fincas_cultivo_lenoso_secano_municipio(query, municipio) -> str:

        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:cultivo_lenoso . "
        )

        query += (
            Constants.comarca()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.etiqueta() + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://opendata.aragon.es/def/ei2a#dryOrIrrigated> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains("Secano", Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def fincas_cultivo_lenoso_olivar_municipio(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_cultivo_lenoso_olivar" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:cultivo_lenoso . "
        )

        query += (
            Constants.comarca()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.etiqueta() + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://opendata.aragon.es/def/ei2a#dryOrIrrigated> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains("Olivar", Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def fincas_cultivo_lenoso_regadio_municipio(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_cultivo_lenoso_regadio" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query += (
            Constants.comarca() + " " + Constants.aux0() + " ei2a:cultivo_lenoso . "
        )

        query += (
            Constants.comarca()
            + " <http://purl.org/dc/elements/1.1/title> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.location()
            + " . "
        )

        query += (
            Constants.location()
            + " <http://www.w3.org/2003/01/geo/wgs84_pos#location> "
            + Constants.aux1()
            + " . "
        )

        query += (
            Constants.aux1() + " ei2a:organizationName " + Constants.etiqueta() + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta())
            + " . "
        )

        query += (
            Constants.comarca()
            + " <http://opendata.aragon.es/def/ei2a#dryOrIrrigated> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains("Regadío", Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def ecologica(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_ecologica" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """

        
        query += (
            Constants.aux0()
            + " <http://opendata.aragon.es/def/iaest/medida#superficie-total-agricultura-ecologica> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def olivares(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_olivares" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query += (
            Constants.aux0()
            + " <http://opendata.aragon.es/def/iaest/medida#hectareas-en-tierras-labradas-con-cultivo-olivar> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def vinedos(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_viñedos" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """
        
        query += (
            Constants.aux0()
            + " <http://opendata.aragon.es/def/iaest/medida#hectareas-en-tierras-labradas-con-cultivo-vinedo> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def frutales(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_frutales" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """

        
        query += (
            Constants.aux0()
            + " <http://opendata.aragon.es/def/iaest/medida#hectareas-en-tierras-labradas-con-cultivos-frutales> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def herbaceos(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_herbaceos" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """        
        
        query += (
            Constants.aux0()
            + " <http://opendata.aragon.es/def/iaest/medida#hectareas-en-tierras-labradas-con-cultivos-herbaceos> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def regadio(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_regadio" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """        
        
        query += (
            Constants.aux0()
            + " <http://opendata.aragon.es/def/iaest/medida#hectareas-en-tierras-labradas-de-regadio> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    @staticmethod
    def secano(query, municipio) -> str:

        """ This function added the necessary code to get the "fincas_secano" of village. 
        
        Parameter
        ----------
            query str
            municipio str
        
        Returns
        ---------
            query str
            """        
        
        query += (
            Constants.aux0()
            + " <http://opendata.aragon.es/def/iaest/medida#hectareas-en-tierras-labradas-de-secano> "
            + Constants.answer0()
            + " . "
        )

        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refArea> "
            + Constants.etiqueta2()
            + " . "
        )

        query += (
            TemplatesAgriculture.create_bif_contains(municipio, Constants.etiqueta2())
            + " . "
        )
        return query

    # *************
    # extra Queries
    # *************

    @staticmethod
    def year(query, year) -> str:

        """ This function added the necessary code to include year control. 
        
        Parameter
        ----------
            query str
            year str
        
        Returns
        ---------
            query str
            """

        
        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> "
            + Constants.etiqueta()
        )

        query += (
            TemplatesAgriculture.create_bif_contains(year, Constants.etiqueta()) + " . "
        )
        return query

    @staticmethod
    def year_reference(query, year) -> str:

        """ This function added the necessary code to include year control. 
        
        Parameter
        ----------
            query str
            year str
        
        Returns
        ---------
            query str
            """        
        
        query += (
            Constants.aux0()
            + " <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> "
            + Constants.etiqueta()
        )

        query += (
            f" filter REGEX( ?etiqueta , <http://reference.data.gov.uk/id/year/{year}> )  "

        )
        return query
    @staticmethod
    def tipo_localizacion_ecologica(query, tipo_localizacion) -> str:
        
        """ This function added the necessary code to get the localization ecological type.  
        
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
                "WHERE",
                " FROM " + Constants.grafo_agricultura_ecologica_aragon() + " WHERE",
            )
        elif tipo_localizacion == "municipio":
            query = query.replace(
                "WHERE",
                " FROM " + Constants.grafo_agricultura_ecologica_municipio() + " WHERE",
            )
        elif tipo_localizacion == "provincia":
            query = query.replace(
                "WHERE",
                " FROM " + Constants.grafo_agricultura_ecologica_provincia() + " WHERE",
            )
        elif tipo_localizacion == "comarca":
            query = query.replace(
                "WHERE",
                " FROM " + Constants.grafo_agricultura_ecologica_comarca() + " WHERE",
            )
        return query

    @staticmethod
    def tipo_localizacion_cultivos(query, tipo_localizacion) -> str:
        
        """ This function added the necessary code to get the localization crops type.  
        
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
                "WHERE",
                " FROM " + Constants.grafo_agricultura_cultivos_aragon() + " WHERE",
            )
        elif tipo_localizacion == "municipio":
            query = query.replace(
                "WHERE",
                " FROM " + Constants.grafo_agricultura_cultivos_municipio() + " WHERE",
            )
        elif tipo_localizacion == "provincia":
            query = query.replace(
                "WHERE",
                " FROM " + Constants.grafo_agricultura_cultivos_provincia() + " WHERE",
            )
        elif tipo_localizacion == "comarca":
            query = query.replace(
                "WHERE",
                " FROM " + Constants.grafo_agricultura_cultivos_comarca() + " WHERE",
            )
        return query
