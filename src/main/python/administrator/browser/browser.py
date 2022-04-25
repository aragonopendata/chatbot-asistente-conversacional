'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
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
    """[summary]
    """

    def __init__(self, bbdd_url: str = "") -> None:
 #       self.__nlp = spacy.blank("es")
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
        self.__peticion = ""
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
            #"plazasRestaurante": {"plazasRestaurante": TemplatesTurismo.plazas_restaurante },
            "numRestaurantes": {"numRestaurantes":TemplatesTurismo.numero_restaurantes },
            "municipioRestaurante": {"municipioRestaurante": TemplatesTurismo.municipio_restaurante },

            # Esta sacado la nueva consulta de 'obrasMuseo' pero he comentado porque se van eliminar los dato
            # en la siguiente versión de la Ontología.

            #"obrasMuseo": {"obrasMuseo": TemplatesTurismo.obras_museo },
            "museosLocalidad": {"museosLocalidad": TemplatesTurismo.museos_municipio },
            #"municipioObra": {"municipioObra": TemplatesTurismo.municipio_obra },
            #"rutasOrigen":
            #    {"rutasOrigen": TemplatesTurismo.rutas_con_origen ,
            #     "rutasDestino":TemplatesTurismo.extra_destino }
            #    ,
            #"rutasDestino": {"rutasDestino": TemplatesTurismo.rutas_con_destino },
            "rutasCamino": {"rutasCamino": TemplatesTurismo.rutas_camino },
            #"guiasLocalidad": {"guiasLocalidad": TemplatesTurismo.guia_municipio },
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

            #"listAgenciaViajes": { "listAgenciaViajes":TemplatesTurismo.list_agencia_viaje },
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
            #"plazasAlojamiento":
            #    {"plazasAlojamiento": TemplatesTurismo.plazas_alojamiento ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            "alojamientoCiudad":
                {"alojamientoCiudad": TemplatesTurismo.ciudad_alojamiento ,
                "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
                ,
            #"categoriaAlojamiento":
            #    { "categoriaAlojamiento": TemplatesTurismo.categoria_alojamiento ,
            #     "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            #"alojamientoCiudad":
            #    {"alojamientoCiudad": TemplatesTurismo.alojamiento_municipio ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento ,
            #    "categoria":TemplatesTurismo.extra_categoria }
            #    ,
            #"temporadaAlojamiento":
            #    {"temporadaAlojamiento":  TemplatesTurismo.temporada_alojamiento ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento ,
            #    "tipoTemporada":TemplatesTurismo.extra_tipo_temporada }
            #    ,
            #"caravanasCamping":
            #    { "caravanasCamping":  TemplatesTurismo.caravanas_camping ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            #"parcelasCamping":
            #    {"parcelasCamping": TemplatesTurismo.parcelas_camping ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            #"bungalowsCamping":
            #    { "bungalowsCamping":TemplatesTurismo.bungalows_camping ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            #apartamentosCasaRural":
            #    {"apartamentosCasaRural": TemplatesTurismo.apartamentos_casarural ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            #"habitacionesDoblesCasaRural":
            #    { "habitacionesDoblesCasaRural":TemplatesTurismo.habitacionesdobles_casarural ,
            #     "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            #"habitacionesSencillasCasaRural":
            #    {"habitacionesSencillasCasaRural": TemplatesTurismo.habitacionessencillas_casarural ,
            #     "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento }
            #    ,
            #"habitacionesHotel":
            #    { "habitacionesHotel": TemplatesTurismo.habitaciones_hotel ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento ,
            #    "tipoHabitacion":TemplatesTurismo.extra_tipo_habitacion }
            #    ,
            #"habitacionesBañoHotel":
            #    {"habitacionesBañoHotel": TemplatesTurismo.habitacionesbano_hotel ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento },

            #"habitacionessinBañoHotel":
            #    { "habitacionessinBañoHotel": TemplatesTurismo.habitacionessinbano_hotel ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento },
            #"camasHotel":
            #    { "camasHotel": TemplatesTurismo.camas_hotel ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento },
            #"serviciosHotel":
            #    {"serviciosHotel": TemplatesTurismo.servicios_hotel ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento },
            #"habitacionesTerrazaHotel":
            #    { "habitacionesTerrazaHotel": TemplatesTurismo.habitacionesterraza_hotel ,
            #    "tipoAlojamiento":TemplatesTurismo.extra_tipo_alojamiento },

            #"comarcasAgrariasLocalizacion": { "comarcasAgrariasLocalizacion":TemplatesAgriculture.comarca_agraria_municipio },
            #"municipioComarcasAgrarias": {"municipioComarcasAgrarias": TemplatesAgriculture.municipio_comarca_agraria },
            #"villasLocalizacion": { "villasLocalizacion": TemplatesAgriculture.villas_municipio },
            #"municipioVilla": {"municipioVilla": TemplatesAgriculture.municipio_villa },
            #"infoVilla": { "infoVilla":TemplatesAgriculture.info_villa },
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

        return TemplatesTransport.getData()

    def getCalendarUrls(self):

        return TemplatesCalendar.getUrls()

    def getTransportBusData(self):

        return TemplatesTransportBus.getAllData()

    def search(self, json_input: dict) -> list:
        """main method generate and search a query

        Arguments:
            json_input {dict} -- {"question": str, "intents": list, "entities": list}

        Returns:
            dict -- result of query transformed to dict in json model
        """
        self.generate_query(json_input)
        try:
            result = self.__execute_query()
            parse_query = url_parser.quote(self.__query)
            self.url = "https://opendata.aragon.es/sparql?default-graph-uri=&query={0}&format=text%2Fhtml&timeout=0&debug=on".format(
                parse_query
            )
            Log.log_debug("BROWSER_: Url de la query --> {0}".format(self.url))
            return result
        except URLError:
            raise URLError(
                "En este momento no puedo responderte a esta pregunta, intentalo de nuevo más tarde."
            )
        except Exception:
            raise Exception("En este momento no puedo responderte a esta pregunta.")

    def generate_query(self, json_input: dict) -> list:
        """main method generate and search a query

        Arguments:
            json_input {dict} -- {"question": str, "intents": list, "entities": list}

        Returns:
            dict -- result of query transformed to dict in json model
        """
        self.__input_processor(json_input)
        self.__create_query()
        self.__special_replace(self.__query)
        return self.__query

    # *************
    # privates
    # *************

    def __special_replace(self,query):

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
        self.__question = json_input.get("question")
        self.__intents = json_input["intents"]
        self.__entities = json_input["entities"]
        self.__xml = ""
        self.__json = ""
        self.__ics = ""
        self.__query = ""

    def __execute_query(self):
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
        result = []
        for case in elements:
            dict_case = {f"answer{str(i)}": case[list(case.keys())[i]] for i in range(len(case.keys()))}


            for position, entity in enumerate(self.__entities):
                dict_case[f"etiqueta{str(position)}"] = entity
            result.append(dict_case)
        return result

    def __create_query(self) -> None:
        self.__query = TemplatesAragon.base_query()
        self.__run_cases()
        self.__query += "}"

    def _execute_querys_data(self) -> None:

        try:
            entities_num = 0

            action_principal = self._data_querys[self.__intents[0]]
            for i in self.__intents:
                executes = action_principal[i]
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
        entities_num = 0  # Para casos anidados

        '''
        self._data_xmls = {
            "transportIssues": {
                "xml":   TemplatesTransport.getIssues,
                "url":"http://www.carreterasdearagon.es/xml-ultimas-incidencias.php" },
            "transportIssueType":  {
                "xml":   TemplatesTransport.getIssues,"url":"http://www.carreterasdearagon.es/xml-ultimas-incidencias.php" },
            "transportIssueWhere": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportIssueReason": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportIssueRestrictions": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoads": {
                "json":TemplatesTransport.getRoads,
                "url":"https://opendata.aragon.es/GA_OD_Core/preview?view_id=205" },
            "transportRoadSpeed": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadType": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadLocation": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadDescription": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadZones": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadBridges": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportBridgesLocation": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadKmBridge": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportBridgesKms": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoBridLocations": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "tipoIncidencia": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadLengthOrigen": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadLengthDestino": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarHolidaysDay": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarHolidaysWhen": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarHolidaysWhere": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarHolidaysLocationDay": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarHolidaysLocationPlace": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "Year": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarHolidaysMonth": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "Month": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "tipoLocalizacion": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "transportRoadNameLength": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarHolidays": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "calendarRangeHolidays": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "dateFrom": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "dateTo": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "autobus_location": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "locdesde": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "lochasta": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "locactual": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "servicio": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "horarioautobuses_desde": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }],
            "horarioautobuses_hasta": [{ TemplatesAragon.superficie_secano(self.__query,"year" ) }]

        }

        entities_num = 0  # Para casos anidados
        if Config.intents()[0] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.comarca_del_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[1] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.superficie_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[2] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.habitantes_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[3] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.superficie_secano(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if Config.subintents()[0] in self.__intents[entities_num]:
                self.__query = TemplatesAragon.year(
                    self.__query, self.__entities[entities_num]
                )
                entities_num += 1
        elif Config.intents()[4] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.superficie_regadio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if Config.subintents()[0] in self.__intents[entities_num]:
                self.__query = TemplatesAragon.year(
                    self.__query, self.__entities[entities_num]
                )
                entities_num += 1
        elif Config.intents()[5] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.poblacion(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if Config.subintents()[0] in self.__intents[entities_num]:
                self.__query = TemplatesAragon.year_dataset(
                    self.__query, self.__entities[entities_num]
                )
                entities_num += 1
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_poblacion(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[6] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.telefono_ayuntamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[7] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.cif_ayuntamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[8] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.email_ayuntamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[9] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.cargo_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if Config.subintents()[1] in self.__intents[entities_num]:
                self.__query = TemplatesAragon.cargo(
                    self.__query, self.__entities[entities_num]
                )
                entities_num += 1
        elif Config.intents()[10] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.fax_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[11] in self.__intents[entities_num]:
            print("ESTAMOS BIEN")
            self.__query = TemplatesAragon.direccion_ayuntamiento(
                self.__query, self.__entities[entities_num]
            )
            print(self.__query)
            entities_num += 1
        elif Config.intents()[12] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.telefono_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[13] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.fax_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[14] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.email_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[15] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.web_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[16] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.direccion_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[17] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.list_restaurantes(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[18] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.info_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[19] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.plazas_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[20] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.numero_restaurantes(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[21] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.municipio_restaurante(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[22] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.obras_museo(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[23] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.museos_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[24] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.municipio_obra(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[25] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.rutas_con_origen(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[2] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_destino(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[26] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.rutas_con_destino(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[27] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.rutas_camino(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[28] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.guia_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[29] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.telefono_guia(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[30] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.email_guia(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[31] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.web_guia(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[32] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.info_guia(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[33] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.telefono_iturismo(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[34] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.direccion_iturismo(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[35] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.telefono_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[36] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.email_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[37] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.fax_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[38] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.web_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[39] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.direccion_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[40] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.listado_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[4] in self.__intents[entities_num]:
                            self.__query = TemplatesTurismo.extra_tipo_lugar(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[41] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.telefono_agencia_viaje(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[42] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.email_agencia_viaje(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[43] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.web_agencia_viaje(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[44] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.direccion_agencia_viaje(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[45] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.list_agencia_viaje(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[46] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.reserva_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[47] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.count_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[48] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.plazas_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[49] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.ciudad_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[50] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.categoria_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[51] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.alojamiento_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[7] in self.__intents[entities_num]:
                            self.__query = TemplatesTurismo.extra_categoria(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[52] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.temporada_alojamiento(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[5] in self.__intents[entities_num]:
                            self.__query = TemplatesTurismo.extra_tipo_temporada(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[53] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.caravanas_camping(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[54] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.parcelas_camping(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[55] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.bungalows_camping(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[56] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.apartamentos_casarural(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[57] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.habitacionesdobles_casarural(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[58] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.habitacionessencillas_casarural(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[59] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.habitaciones_hotel(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[6] in self.__intents[entities_num]:
                            self.__query = TemplatesTurismo.extra_tipo_habitacion(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[60] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.habitacionesbano_hotel(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[61] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.habitacionessinbano_hotel(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[62] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.camas_hotel(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[63] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.servicios_hotel(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[64] in self.__intents[entities_num]:
            self.__query = TemplatesTurismo.habitacionesterraza_hotel(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[3] in self.__intents[entities_num]:
                    self.__query = TemplatesTurismo.extra_tipo_alojamiento(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[65] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.comarca_agraria_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[66] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.municipio_comarca_agraria(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[67] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.villas_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[68] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.municipio_villa(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[69] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.info_villa(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[70] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.fincas_cultivo_lenoso_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[71] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.fincas_cultivo_lenoso_regadio_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[72] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.fincas_cultivo_lenoso_secano_municipio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
        elif Config.intents()[73] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.ecologica(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.year(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                if len(self.__intents) > 2:
                    if Config.subintents()[8] in self.__intents[entities_num]:
                        self.__query = TemplatesAgriculture.tipo_localizacion_ecologica(
                            self.__query, self.__entities[entities_num]
                        )
                        entities_num += 1
        elif Config.intents()[74] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.olivares(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.year(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
            if len(self.__intents) > 2:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.tipo_localizacion_cultivos(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[75] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.vinedos(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.year(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
            if len(self.__intents) > 2:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.tipo_localizacion_cultivos(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[76] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.frutales(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.year(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
            if len(self.__intents) > 2:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.tipo_localizacion_cultivos(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[77] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.herbaceos(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.year(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
            if len(self.__intents) > 2:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.tipo_localizacion_cultivos(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[78] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.regadio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.year(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
            if len(self.__intents) > 2:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.tipo_localizacion_cultivos(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
        elif Config.intents()[79] in self.__intents[entities_num]:
            self.__query = TemplatesAgriculture.secano(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAgriculture.year(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[8] in self.__intents[entities_num]:
                            self.__query = TemplatesAgriculture.tipo_localizacion_cultivos(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[80] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.poblacion_extranjeros(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[0] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.year_dataset(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[9] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.tipo_area_extranjeros(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 3:
                                if (
                                    Config.subintents()[8]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.tipo_localizacion_general(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
                                    if len(self.__intents) > 4:
                                        if (
                                            Config.subintents()[11]
                                            in self.__intents[entities_num]
                                        ):
                                            self.__query = TemplatesAragon.area_filter_extranjeros(
                                                self.__query,
                                                self.__entities[entities_num],
                                            )
                                            entities_num += 1
                                            if len(self.__intents) > 5:
                                                if (
                                                    Config.subintents()[10]
                                                    in self.__intents[entities_num]
                                                ):
                                                    self.__query = TemplatesAragon.sexo(
                                                        self.__query,
                                                        self.__entities[entities_num],
                                                    )
                                                    entities_num += 1
        elif Config.intents()[81] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.num_contenedores_vidrio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    self.__query = TemplatesAragon.year_dataset_max(self.__query)
        elif Config.intents()[82] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.kg_vidrio(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[83] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.hectareas_zona(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    self.__query = TemplatesAragon.year_dataset_max(self.__query)
                    if len(self.__intents) > 2:
                        if Config.subintents()[12] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.tipo_superficie(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[84] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.num_incendios(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[85] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.hectareas_quemadas(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[86] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.num_depuradoras(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[87] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.num_autonomos(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 3:
                                if (
                                    Config.subintents()[10]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.sexo(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
        elif Config.intents()[88] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.num_parados(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 3:
                                if (
                                    Config.subintents()[10]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.sexo(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
                                    if len(self.__intents) > 4:
                                        if (
                                            Config.subintents()[13]
                                            in self.__intents[entities_num]
                                        ):
                                            self.__query = TemplatesAragon.sector(
                                                self.__query,
                                                self.__entities[entities_num],
                                            )
                                            entities_num += 1
        elif Config.intents()[89] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.num_contratados(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 3:
                                if (
                                    Config.subintents()[10]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.sexo(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
        elif Config.intents()[90] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.num_accidentes_laborales(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 3:
                                if (
                                    Config.subintents()[10]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.sexo(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
        elif Config.intents()[91] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.renta_per_capita(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[92] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.empresas_por_trabajadores(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 3:
                                if (
                                    Config.subintents()[14]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.num_trabajadores(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
        elif Config.intents()[93] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.empresas_por_sector(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    self.__query = TemplatesAragon.year_dataset_max(self.__query)
                    if len(self.__intents) > 2:
                        if Config.subintents()[13] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.sector(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[94] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.empresas_por_actividad(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[15] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.actividad(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 3:
                                if (
                                    Config.subintents()[0]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.year_dataset(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
        elif Config.intents()[95] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.uso_suelo(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        elif Config.intents()[96] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.hectareas_tipo_suelo(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[0] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.year_dataset(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
                            if len(self.__intents) > 2:
                                if (
                                    Config.subintents()[16]
                                    in self.__intents[entities_num]
                                ):
                                    self.__query = TemplatesAragon.tipo_suelo(
                                        self.__query, self.__entities[entities_num]
                                    )
                                    entities_num += 1
        elif Config.intents()[97] in self.__intents[entities_num]:
            self.__query = TemplatesAragon.antiguedad_edificios(
                self.__query, self.__entities[entities_num]
            )
            entities_num += 1
            if len(self.__intents) > 1:
                if Config.subintents()[8] in self.__intents[entities_num]:
                    self.__query = TemplatesAragon.tipo_localizacion_general(
                        self.__query, self.__entities[entities_num]
                    )
                    entities_num += 1
                    if len(self.__intents) > 2:
                        if Config.subintents()[17] in self.__intents[entities_num]:
                            self.__query = TemplatesAragon.antiguedad(
                                self.__query, self.__entities[entities_num]
                            )
                            entities_num += 1
        el
        '''
        self._execute_querys_data()

        '''if Config.intents()[98] in self.__intents[entities_num]:
            self.__xml = TemplatesTransport.getIssues(self.__entities[entities_num])
            self.url = Config.urlIssues #"https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json"
            entities_num += 1
        elif Config.intents()[99] in self.__intents[entities_num]:
            self.__xml = TemplatesTransport.getIssueType(self.__entities[entities_num])
            self.url = Config.urlIssues #"https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json"
            entities_num += 1
        elif Config.intents()[100] in self.__intents[entities_num]:
            self.__xml = TemplatesTransport.getIssueWhere(self.__entities[entities_num])
            self.url = Config.urlIssues #"https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json"
            entities_num += 1
        elif Config.intents()[101] in self.__intents[entities_num]:
            self.__xml = TemplatesTransport.getIssueReason(self.__entities[entities_num])
            self.url = Config.urlIssues #"https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json"
            entities_num += 1
        elif Config.intents()[102] in self.__intents[entities_num]:
            """It is necessary to modify"""
            self.__xml = TemplatesTransport.getIssueRestrictions(
                self.__entities[entities_num]
            )
            self.url = Config.urlIssues #"https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json"
            entities_num += 1'''
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
