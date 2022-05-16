# -*- coding: utf-8 -*-
from urllib.error import URLError
import urllib.parse as url_parser

#import spacy

from SPARQLWrapper import SPARQLWrapper, JSON

from browser.config import Config
from browser.templates_aragon import TemplatesAragon
from browser.templates_agriculture import TemplatesAgriculture
from browser.templates_transport import TemplatesTransport
from browser.templates_turismo import TemplatesTurismo
from browser.templates_calendar import TemplatesCalendar
from browser.templates_transport_bus import TemplatesTransportBus
from browser.buildjson import BuildJson
from browser.logger import Log

import datetime


class Browser:
    """Class uses to build queries to access Open Data Virtuoso databases
    """

    def __init__(self, bbdd_url: str = "") -> None:
        """ Initialisation of the class. 
            Variables
            Database connectors
            Queries' templates
         """
        self.__question = ""
        self.__intents = ""
        self.__entities = ""
        self.__query = ""
        self.__xml = ""
        self.__json = ""
        self.__ics = ""
        self.__transportdata = self.getTransportData()
        self.__calendarurls = self.getCalendarUrls()
        self.__transportbus = self.getTransportBusData()
        self.__petition = ""
        self.__bd_conector = "Virtuoso"
        self.url = ""
        if bbdd_url == "":
            self.__sparqlControler = SPARQLWrapper(Config.bbdd_url())
        else:
            self.__sparqlControler = SPARQLWrapper(bbdd_url)

        self.__sparqlControler.setTimeout(45)

        self._data_querys = {
            "ComarcaMunicipio" :  { "ComarcaMunicipio" : TemplatesAragon.comarca_del_municipio},
            "SuperficieMunicipio": {"SuperficieMunicipio": TemplatesAragon.superficie_municipio},
            "HabitantesMunicipio": {"HabitantesMunicipio": TemplatesAragon.habitantes_municipio},
            "SuperficieSecano" :
                {"SuperficieSecano": TemplatesAragon.superficie_secano ,
                 "Year":TemplatesAragon.year }  ,
            "SuperficieRegadio":
                { "SuperficieRegadio":TemplatesAragon.superficie_regadio,
                 "Year":TemplatesAragon.year },
            "Poblacion":
                    { "Poblacion":TemplatesAragon.poblacion ,
                     "Year" : TemplatesAragon.year_dataset  ,
                     "tipoLocalizacion" : TemplatesAragon.tipo_localizacion_poblacion  },
            "TelefonoAyuntamiento" : { "TelefonoAyuntamiento":TemplatesAragon.telefono_ayuntamiento },
            "CIFAyuntamiento": {"CIFAyuntamiento": TemplatesAragon.cif_ayuntamiento },
            "EmailAyuntamiento": { "EmailAyuntamiento":TemplatesAragon.email_ayuntamiento },
            "Cargo":
                { "Cargo" : TemplatesAragon.cargo  ,
                   "Municipio":TemplatesAragon.cargo_municipio} ,
            "FaxAyuntamiento": {"FaxAyuntamiento" : TemplatesAragon.fax_municipio },
            "DireccionAyuntamiento": { "DireccionAyuntamiento": TemplatesAragon.direccion_ayuntamiento },
            "telefonoRestaurante": {"telefonoRestaurante": TemplatesTurismo.telefono_restaurante },
            "faxRestaurante": {"faxRestaurante": TemplatesTurismo.fax_restaurante },
            "emailRestaurante": { "emailRestaurante":TemplatesTurismo.email_restaurante },
            "webRestaurante": { "webRestaurante":TemplatesTurismo.web_restaurante },
            "direccionRestaurante": {"direccionRestaurante": TemplatesTurismo.direccion_restaurante },
            "restaurantesCiudad": {"restaurantesCiudad": TemplatesTurismo.list_restaurantes },
            "reservaRestaurantes": {"reservaRestaurantes": TemplatesTurismo.info_restaurante },
            "reservaRestaurantesTelefono": {"reservaRestaurantesTelefono": TemplatesTurismo.info_restaurante_telefono},
            "numRestaurantes": {"numRestaurantes":TemplatesTurismo.numero_restaurantes },
            "municipioRestaurante": {"municipioRestaurante": TemplatesTurismo.municipio_restaurante },
            "museosLocalidad": {"museosLocalidad": TemplatesTurismo.museos_municipio },
            "rutasCamino": {"rutasCamino": TemplatesTurismo.rutas_camino },
            "telefonoGuia": {"telefonoGuia" :TemplatesTurismo.telefono_guia },
            "emailGuia": {"emailGuia":  TemplatesTurismo.email_guia },
            "webGuia": { "webGuia":TemplatesTurismo.web_guia },
            "informacionGuia": {"informacionGuia" : TemplatesTurismo.info_guia },
            "telefonoTurismo": {"telefonoTurismo":  TemplatesTurismo.telefono_iturismo },
            "direccionTurismo": {"direccionTurismo":  TemplatesTurismo.direccion_iturismo },
            "telefonoAlojamiento":
                {"telefonoAlojamiento": TemplatesTurismo.telefono_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            ,
            "emailAlojamiento":
                {"emailAlojamiento": TemplatesTurismo.email_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento } ,
            "faxAlojamiento":
                {"faxAlojamiento": TemplatesTurismo.fax_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
                ,
            "webAlojamiento":
                {"webAlojamiento": TemplatesTurismo.web_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento
            } ,
            "ciudadAlojamiento":
                {"ciudadAlojamiento": TemplatesTurismo.ciudad_alojamiento,
                 "tipoAlojamiento": TemplatesTurismo.extra_tipo_alojamiento}
            ,
            "direccionAlojamiento":
                { "direccionAlojamiento":TemplatesTurismo.direccion_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
                ,
            "listadoAlojamiento":
                { "listadoAlojamiento":TemplatesTurismo.listado_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento ,
                "tipoLugar":TemplatesTurismo.extra_tipo_lugar }
                ,
            "telefonoAgenciaViajes" : { "telefonoAgenciaViajes":TemplatesTurismo.telefono_agencia_viaje },
            "emailAgenciaViajes": {"emailAgenciaViajes": TemplatesTurismo.email_agencia_viaje },
            "webAgenciaViajes": { "webAgenciaViajes": TemplatesTurismo.web_agencia_viaje },
            "direccionAgenciaViajes": { "direccionAgenciaViajes":TemplatesTurismo.direccion_agencia_viaje },
            "reservarAlojamiento":
                {"reservarAlojamiento":  TemplatesTurismo.reserva_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
                ,
            "reservarAlojamiento_telefono":
                {"reservarAlojamiento_telefono": TemplatesTurismo.reserva_alojamiento_telephone ,
                 "tipoAlojamiento": TemplatesTurismo.extra_tipo_alojamiento}
            ,
            "numeroAlojamiento":
                {"numeroAlojamiento": TemplatesTurismo.count_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
                ,
            "alojamientoCiudad":
                {"alojamientoCiudad": TemplatesTurismo.ciudad_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
                ,
            "fincasCultivoLenoso": {"fincasCultivoLenoso": TemplatesAgriculture.fincas_cultivo_lenoso_municipio },
            "fincasRegadioLenosas": {"fincasRegadioLenosas": TemplatesAgriculture.fincas_cultivo_lenoso_regadio_municipio },
            "fincasSecanoLenosas": {"fincasSecanoLenosas": TemplatesAgriculture.fincas_cultivo_lenoso_secano_municipio },
            "fincasOlivarLenosas": {"fincasOlivarLenosas": TemplatesAgriculture.fincas_cultivo_lenoso_olivar_municipio},
            "hectareasAgriculturaEcologica": {
                "hectareasAgriculturaEcologica":TemplatesAgriculture.ecologica ,
                "Year":TemplatesAgriculture.year_reference ,
                "tipoLocalizacion":TemplatesAgriculture.tipo_localizacion_ecologica },
            "hectareasOlivares": {
                "hectareasOlivares":TemplatesAgriculture.olivares ,
                "Year":TemplatesAgriculture.year ,
                "tipoLocalizacion":TemplatesAgriculture.tipo_localizacion_cultivos },
            "hectareasVinedos":{
                "hectareasVinedos":TemplatesAgriculture.vinedos ,
                "Year":TemplatesAgriculture.year ,
                "tipoLocalizacion":TemplatesAgriculture.tipo_localizacion_cultivos },
            "hectareasFrutales": {
                "hectareasFrutales":TemplatesAgriculture.frutales ,
                "Year":TemplatesAgriculture.year ,
                "tipoLocalizacion":TemplatesAgriculture.tipo_localizacion_cultivos },
            "hectareasHerbaceos":{
                "hectareasHerbaceos":TemplatesAgriculture.herbaceos ,
                "Year":TemplatesAgriculture.year ,
                "tipoLocalizacion":TemplatesAgriculture.tipo_localizacion_cultivos },
            "hectareasRegadio":{
                "hectareasRegadio":TemplatesAgriculture.regadio ,
                "Year":TemplatesAgriculture.year ,
                "tipoLocalizacion":TemplatesAgriculture.tipo_localizacion_cultivos },
            "hectareasSecano": {
                "hectareasSecano":TemplatesAgriculture.secano ,
                "Year":TemplatesAgriculture.year ,
                "tipoLocalizacion":TemplatesAgriculture.tipo_localizacion_cultivos },
            "poblacionExtranjera":{
                "poblacionExtranjera":TemplatesAragon.poblacion_extranjeros,
                "Year":TemplatesAragon.year_dataset ,
                "tipoArea":TemplatesAragon.tipo_area_extranjeros ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "nombreArea":TemplatesAragon.area_filter_extranjeros ,
                "sexo":TemplatesAragon.sexo  },
            "numContenedoresVidrio": {
                "numContenedoresVidrio": TemplatesAragon.num_contenedores_vidrio ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "year": TemplatesAragon.year_dataset_max},
            "kilosVidrioRecogidos": {
                "kilosVidrioRecogidos":TemplatesAragon.kg_vidrio ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset},
            "hectareasZona": {
                "hectareasZona":TemplatesAragon.hectareas_zona ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset_max ,
                "tipoSuperficie":TemplatesAragon.tipo_superficie },
            "numIncendios":{
                "numIncendios": TemplatesAragon.num_incendios ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset_max },
            "hectareasQuemadas": {
                "hectareasQuemadas": TemplatesAragon.hectareas_quemadas ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset_max },
            "numDepuradoras": {
                "numDepuradoras": TemplatesAragon.num_depuradoras ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset },
            "numeroAutonomos": {
                "numeroAutonomos":TemplatesAragon.num_autonomos ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset ,
                "sexo":TemplatesAragon.sexo
            },
            "numParados": {
                "numParados": TemplatesAragon.num_parados,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset ,
                "sexo":TemplatesAragon.sexo,
                "sector":TemplatesAragon.sector
            },
            "numContratados": {
                "numContratados":TemplatesAragon.num_contratados ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset ,
                "sexo":TemplatesAragon.sexo
                },
            "numAccidentesLaborales": {
                "numAccidentesLaborales":TemplatesAragon.num_accidentes_laborales  ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset ,
                "sexo":TemplatesAragon.sexo
                },
            "rentaPerCapita":{
                "rentaPerCapita":TemplatesAragon.renta_per_capita ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset
                },
            "empresasPorTrabajadores": {
                "empresasPorTrabajadores":TemplatesAragon.empresas_por_trabajadores ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset,
                "numTrabajadores":TemplatesAragon.num_trabajadores
                },
            "empresasPorSector": {
                "empresasPorSector":TemplatesAragon.empresas_por_sector ,
                "tipoLocalizacion":TemplatesAragon.tipo_localizacion_general  ,
                "sector": TemplatesAragon.sector,
                "Year":TemplatesAragon.year_dataset_max,
                #"numTrabajadores":TemplatesAragon.sector
                },
            "empresasPorActividad":{
                "empresasPorActividad":TemplatesAragon.empresas_por_actividad ,
                "tipoLocalizacion": TemplatesAragon.tipo_localizacion_general  ,
                "actividad":TemplatesAragon.sector ,
                "Year":TemplatesAragon.year_dataset
                },
            "usoSuelo":{
                "usoSuelo":TemplatesAragon.uso_suelo ,
                "tipoLocalizacion": TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset
                },
            "hectareasTipoSuelo":{
                "hectareasTipoSuelo":TemplatesAragon.hectareas_tipo_suelo ,
                "tipoLocalizacion": TemplatesAragon.tipo_localizacion_general  ,
                "Year":TemplatesAragon.year_dataset,
                "tipoSuelo":TemplatesAragon.tipo_suelo
                },
            "antiguedadEdificios": {
                "antiguedadEdificios":TemplatesAragon.antiguedad_edificios ,
                "tipoLocalizacion": TemplatesAragon.tipo_localizacion_general  ,
                "antiguedad":TemplatesAragon.antiguedad
                },
            "empresasTuristicasActivas" : {"empresasTuristicasActivas" : TemplatesAragon.empresasActivas},
            "empresasTuristicasActividades": {"empresasTuristicasActividades": TemplatesAragon.empresasActivasActividades},
            "empresasTuristicasContacto": {"empresasTuristicasContacto": TemplatesAragon.empresasActivasContacto},
            "empresasTuristicasDireccion": {"empresasTuristicasDireccion": TemplatesAragon.empresasActivasDireccion}
        }

    def getTransportData(self):
        """ Return information about roads from GA_OD_CORE queries

        Returns
        -------
        json dictionary

            Data in json format.
        """
        return TemplatesTransport.getData()

    def getCalendarUrls(self):
        """ Return information from calendars

        Returns
        -------
        list of calendars

            List of calendars
        """
        return TemplatesCalendar.getUrls()

    def getTransportBusData(self):
        """ Return information about transport of passengers from GA_OD_CORE queries

        Returns
        -------
        json dictionary

            Data in json format.
        """
        return TemplatesTransportBus.getAllData()

    def search(self, json_input: dict) -> list:
        """Main method generate and search a query. search - extract results

        Parameters
        ----------
            json_input {dict} -- {"question": str, "intents": list, "entities": list}

                question to answer, list of intentions and list of entities

        Returns
        -------
            dict -- result of query transformed to dict in json model

                query results
        """
        
        self.generate_query(json_input)
        try:
            result = self.__execute_query()
            parse_query = url_parser.quote(self.__query)
            self.url = "https://opendata.aragon.es/sparql?default-graph-uri=&query={0}&format=text%2Fhtml&timeout=0&debug=on".format(
                parse_query
            )
            Log.log_debug("BROWSER_: Query's URL --> {0}".format(self.url))
            return result
        except URLError:
            raise URLError(
                "En este momento no puedo responderte a esta pregunta, intentalo de nuevo más tarde."
            )
        except Exception:
            raise Exception("En este momento no puedo responderte a esta pregunta.")

    def generate_query(self, json_input: dict) -> list:
        """Main method generate and search a query. generate_query --> Build the query

        Parameters
        ----------
            json_input {dict} -- {"question": str, "intents": list, "entities": list}
                
                question to answer, list of intentions and list of entities

        Returns
        -------
            list -- result of query transformed to dict in json model

        """
        self.__input_processor(json_input)
        self.__create_query()
        self.__special_replace(self.__query)
        return self.__query

    # *************
    # privates
    # *************

    def __special_replace(self,query):
        """Private method. Query customization for autonomous people and beds available

        Parameters
        ----------
            query: String
                
                Query to sent to open data

        Returns
        -------
            String
                Modified query

        """

        if self.__intents[0] == 'numeroAutonomos' and self.__entities[0] in [
            'Aragón',
            'Aragon',
        ]:
            query = query.replace('?answer0 ?etiqueta','?answer0 "Aragón" as ?etiqueta')
            query = query.replace('?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .','')
            query = query.replace('filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "[aáAÁ]r[aáAÁ]g[oóOÓ]n", "i")   . ','')

        if self.__intents[0] == 'camasHotel':
            query = query.replace("?profileField <http://harmonet.org/harmonise#fieldName>",'filter REGEX(?profileField, "plazas", "i")')
            query = query.replace("'Número total de camas'",'')

        self.__query = query

    def __input_processor(self, json_input: dict) -> None:
        """Private method. Fill private variables related to question, intents, entities

        Parameters
        ----------
            json_input: dict
                
               Split variables to buid the query

        """
        self.__question = json_input.get("question")
        self.__intents = json_input["intents"]
        self.__entities = json_input["entities"]
        self.__xml = ""
        self.__json = ""
        self.__ics = ""
        self.__query = ""

    def __execute_query(self):
        """Private method. Query execution

        Returns
        ----------
            result: json
                
               Returns the query in json format

        """
        if self.__xml != "":
            return self.__recieved_results(self.__xml)
        if self.__json != "":
            return self.__recieved_results(self.__json)
        if self.__ics != "":
            return self.__recieved_results(self.__ics)
        self.__sparqlControler.setQuery(self.__query)
        self.__sparqlControler.setReturnFormat(JSON)
        print(self.__query)
        print("****************")

        result = self.__sparqlControler.query().convert()
        result = BuildJson.build_json(result, self.__bd_conector)
        print(result)
        return result

    def __recieved_results(self, elements):
        """Private method. Read results and build a dictionry with the results

        Parameters
        ----------
            elements: list
                
               Returns the query in json format
        
        Returns
        -------
            json_dict
                Results in a json dictionary

        """
        result = []
        for case in elements:
            dict_case = {f"answer{str(i)}": case[list(case.keys())[i]] for i in range(len(case.keys()))}


            for position, entity in enumerate(self.__entities):
                dict_case[f"etiqueta{str(position)}"] = entity
            result.append(dict_case)
        return result

    def __create_query(self) -> None:
        """Private method. Query building

        """
        self.__query = TemplatesAragon.base_query()
        self.__run_cases()
        self.__query += "}"

    def _execute_querys_data(self) -> None:
        """Private method. Query execution

        """

        try:
            entities_num = 0

            main_action = self._data_querys[self.__intents[0]]
            for i in self.__intents:
                executes = main_action[i]
                if isinstance(executes, list):
                    for execute in executes:
                        self.__query = execute(self.__query, self.__entities[entities_num])
                        entities_num += 1
                else:
                    self.__query = executes(self.__query, self.__entities[entities_num])
                    entities_num += 1
        except:
            pass

    def __run_cases(self) -> None:
        """
            Private method. Depending on the intention, execute the proper query
        """
        entities_num = 0  # Para casos anidados

        self._execute_querys_data()

        if Config.intents()[103] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoads(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
            entities_num += 1
        elif Config.intents()[104] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoadSpeed(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
            entities_num += 1
        elif Config.intents()[105] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoadType(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
            entities_num += 1
        elif Config.intents()[106] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoadLocation(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
            entities_num += 1
        elif Config.intents()[107] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoadDescription(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
            entities_num += 1
        elif Config.intents()[108] in self.__intents[entities_num]:
            self.url = TemplatesTransport.getUrlZone(self.__entities[entities_num])
            self.__json = TemplatesTransport.getRoadZones(
                self.__entities[entities_num], self.url
            )
            entities_num += 1
        elif Config.intents()[109] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoadBridges(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=225"
            entities_num += 1
        elif Config.intents()[110] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getLocationBridges(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=225"
            entities_num += 1
        elif Config.intents()[111] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getPkBridge(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=225"
            entities_num += 1
        elif Config.intents()[112] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoadBridgesKm(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=225"
            entities_num += 1
        elif Config.intents()[113] in self.__intents[entities_num]:
            self.__json = TemplatesTransport.getRoadBridgesLocations(
                self.__entities[entities_num]
            )
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=225"
            entities_num += 1
        elif Config.intents()[114] in self.__intents[entities_num]:
            entities_num += 1
            if Config.intents()[101] in self.__intents[entities_num]:
                self.__xml = TemplatesTransport.getIssuesLocation(
                    self.__entities[0], self.__entities[1]
                )
                self.url = (
                    Config.urlIssues #"https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json"
                )
                entities_num += 1
        elif Config.intents()[115] in self.__intents[entities_num]:
            entities_num += 1
            if Config.intents()[116] in self.__intents[entities_num]:
                self.__json = TemplatesTransport.getRoadLength(
                    self.__entities[0], self.__entities[1]
                )
                self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
                entities_num += 1
        elif Config.intents()[117] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                urls = TemplatesCalendar.getShortFeriasyExposicionesAndSchool(
                    place, TemplatesCalendar.getYear(), self.__calendarurls
                )
                self.url = urls
                for url in urls:
                    all_party_days = TemplatesCalendar.getHolidayDay(
                        self.__entities[entities_num], url
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[118] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                urls = TemplatesCalendar.getShortFeriasyExposicionesAndSchool(
                    place, TemplatesCalendar.getYear(), self.__calendarurls
                )
                self.url = urls
                for url in urls:
                    all_party_days = TemplatesCalendar.getDateHolidayFromName(
                        self.__entities[entities_num], url
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[119] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                urls = TemplatesCalendar.getShortFeriasyExposicionesAndSchool(
                    place, TemplatesCalendar.getYear(), self.__calendarurls
                )
                self.url = urls
                for url in urls:
                    all_party_days = TemplatesCalendar.getDateHolidayWhere(
                        self.__entities[entities_num], url
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[120] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                urls = TemplatesCalendar.getShortFeriasyExposicionesAndSchool(
                    place, TemplatesCalendar.getYear(), self.__calendarurls
                )
                self.url = urls
                for url in urls:
                    all_party_days = TemplatesCalendar.getHolidaysDayLocation(
                        self.__entities[entities_num], url
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[121] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                urls = TemplatesCalendar.getShortFeriasyExposicionesAndSchool(
                    place, int(self.__entities[1]), self.__calendarurls
                )
                self.url = urls
                tipoLocalizacion = self.__entities[2]
                for url in urls:
                    all_party_days = TemplatesCalendar.getHolidaysDayLocationYearPlace(
                        self.__entities[entities_num], url, tipoLocalizacion, place
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[123] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                urls = TemplatesCalendar.getFeriasyExposicionesAndSchoolCalendarUrlTipo(
                    place,
                    TemplatesCalendar.getYear(),
                    self.__entities[2],
                    self.__calendarurls,
                )
                self.url = urls
                for url in urls:
                    all_party_days = TemplatesCalendar.getHolidaysMonths(
                        self.__entities[0],
                        self.__entities[1],
                        self.__entities[2],
                        url,
                        place,
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[126] in self.__intents[entities_num]:
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
            self.__json = TemplatesTransport.getRoadTotalLength(
                self.__entities[0]
            )
            entities_num += 1
        elif Config.intents()[127] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                urls = TemplatesCalendar.getFeriasyExposicionesAndSchoolCalendarUrlTipo(
                    place,
                    int(self.__entities[1]),
                    self.__entities[2],
                    self.__calendarurls,
                )
                self.url = urls
                for url in urls:
                    all_party_days = TemplatesCalendar.getHolidaysDayLocationYear(
                        self.__entities[entities_num], url, self.__entities[2], place
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[128] in self.__intents[entities_num]:
            places = TemplatesCalendar.getPlaces()
            all_party_days_all_territory = []
            for place in places:
                date_from = datetime.datetime.strptime(self.__entities[1], "%d-%m-%Y")
                urls = TemplatesCalendar.getFeriasyExposicionesAndSchoolCalendarUrlTipo(
                    place, date_from.year, self.__entities[3], self.__calendarurls
                )
                self.url = urls
                for url in urls:
                    all_party_days = TemplatesCalendar.getHolidaysRange(
                        self.__entities[entities_num],
                        self.__entities[1],
                        self.__entities[2],
                        self.__entities[3],
                        url,
                        place,
                    )
                    for all_party_day in all_party_days:
                        if all_party_day not in all_party_days_all_territory:
                            all_party_days_all_territory.append(all_party_day)
            self.__ics = all_party_days_all_territory
            entities_num += 1
        elif Config.intents()[131] in self.__intents[entities_num]:
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=148&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes="
            self.__json = TemplatesTransportBus.getBusToLocation(
                self.__entities[entities_num], self.__transportbus
            )
            entities_num += 1
        elif Config.intents()[132] in self.__intents[entities_num]:
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=148&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes="
            self.__json = TemplatesTransportBus.getBusesFronTownToTownWithoutAllDataCalculation(
                self.__entities[0], self.__entities[1], self.__transportbus
            )
            entities_num += 1
        elif Config.intents()[134] in self.__intents[entities_num]:
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=148&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes="
            self.__json = TemplatesTransportBus.getBusesFronTownToTownWithoutAllDataCalculation(
                self.__entities[0], self.__entities[1], self.__transportbus
            )
            entities_num += 1
        elif Config.intents()[135] in self.__intents[entities_num]:
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=148&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes="
            self.__json = TemplatesTransportBus.getCompaniesDataFromTown(
                self.__entities[0], self.__transportbus
            )
            entities_num += 1
        elif Config.intents()[136] in self.__intents[entities_num]:
            self.url = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=148&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes="
            self.__json = TemplatesTransportBus.getTimelineOfBusFrownTownToTown(
                self.__entities[0], self.__entities[1], self.__transportbus
            )
            entities_num += 1
