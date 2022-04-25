'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
# -*- coding: utf-8 -*-


class Config:
    """Parámetros de configuración del módulo

    Returns:
        [type] -- [description]
    """

    @staticmethod
    def prefix() -> str:
        return (
            "PREFIX owl: <http://www.w3.org/2002/07/owl#> "
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
            "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
            "PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#> "
            "PREFIX locn: <http://www.w3.org/ns/locn#> "
            "PREFIX dbpedia: <http://dbpedia.org/ontology/> "
            "PREFIX openrec: <http://opendata.aragon.es/recurso/> "
            "PREFIX dbpprop: <http://dbpedia.org/property/> "
            "PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> "
            "PREFIX sch: <http://schema.org/> "
            "PREFIX addr: <http://www.w3.org/ns/locn#> "
            "PREFIX foaf: <http://xmlns.com/foaf/0.1/> "
            "PREFIX org: <http://www.w3.org/ns/org#> "
            "PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> "
            "PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> "
            "PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> "
            "PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> "
            "PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> "
            "PREFIX dc: <http://purl.org/dc/elements/1.1/> "
            "PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>"
        )

    @staticmethod
    def prefixAragon() -> str:
        return (
            "PREFIX owl: <http://www.w3.org/2002/07/owl#> "
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
            "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
            "PREFIX ei2a: <http://opendata.aragon.es/def/ei2av2#> "
            "PREFIX locn: <http://www.w3.org/ns/locn#> "
            "PREFIX dbpedia: <http://dbpedia.org/ontology/> "
            "PREFIX openrec: <http://opendata.aragon.es/recurso/> "
            "PREFIX dbpprop: <http://dbpedia.org/property/> "
            "PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> "
            "PREFIX sch: <http://schema.org/> "
            "PREFIX addr: <http://www.w3.org/ns/locn#> "
            "PREFIX foaf: <http://xmlns.com/foaf/0.1/> "
            "PREFIX org: <http://www.w3.org/ns/org#> "
            "PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> "
            "PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> "
            "PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> "
            "PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> "
            "PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> "
            "PREFIX dc: <http://purl.org/dc/elements/1.1/> "
            "PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>"
        )

    @staticmethod
    def graph() -> str:
        # si no se conoce dejar en blanco
        return ""

    @staticmethod
    def bbdd_url() -> str:
        # url de la base de datos virtuoso
        # return "http://172.27.38.119:7030/sparql"
        # return "http://localhost:7030/sparql"
        return "https://opendata.aragon.es/sparql"

    @staticmethod
    def intents() -> list:
        return [
            "ComarcaMunicipio",
            "SuperficieMunicipio",
            "HabitantesMunicipio",
            "SuperficieSecano",
            "SuperficieRegadio",
            "Poblacion",
            "TelefonoAyuntamiento",
            "CIFAyuntamiento",
            "EmailAyuntamiento",
            "Municipio",
            "FaxAyuntamiento",
            "DireccionAyuntamiento",
            "telefonoRestaurante",
            "faxRestaurante",
            "emailRestaurante",
            "webRestaurante",
            "direccionRestaurante",
            "restaurantesCiudad",
            "reservaRestaurante",
            "plazasRestaurante",
            "numRestaurantes",
            "municipioRestaurante",
            "obrasMuseo",
            "museosLocalidad",
            "municipioObra",
            "rutasOrigen",
            "rutasDestino",
            "rutasCamino",
            "guiasLocalidad",
            "telefonoGuia",
            "emailGuia",
            "webGuia",
            "informacionGuia",
            "telefonoTurismo",
            "direccionTurismo",
            "telefonoAlojamiento",
            "emailAlojamiento",
            "faxAlojamiento",
            "webAlojamiento",
            "direccionAlojamiento",
            "listadoAlojamiento",
            "telefonoAgenciaViajes",
            "emailAgenciaViajes",
            "webAgenciaViajes",
            "direccionAgenciaViajes",
            "listAgenciaViajes",
            "reservarAlojamiento",
            "numeroAlojamiento",
            "plazasAlojamiento",
            "ciudadAlojamiento",
            "categoriaAlojamiento",
            "alojamientoCiudad",
            "temporadaAlojamiento",
            "caravanasCamping",
            "parcelasCamping",
            "bungalowsCamping",
            "apartamentosCasaRural",
            "habitacionesDoblesCasaRural",
            "habitacionesSencillasCasaRural",
            "habitacionesHotel",
            "habitacionesBañoHotel",
            "habitacionessinBañoHotel",
            "camasHotel",
            "serviciosHotel",
            "habitacionesTerrazaHotel",
            "comarcasAgrariasLocalizacion",
            "municipioComarcasAgrarias",
            "villasLocalizacion",
            "municipioVilla",
            "infoVilla",
            "fincasCultivoLenoso",
            "fincasRegadioLenosas",
            "fincasSecanoLenosas",
            "hectareasAgriculturaEcologica",
            "hectareasOlivares",
            "hectareasVinedos",
            "hectareasFrutales",
            "hectareasHerbaceos",
            "hectareasRegadio",
            "hectareasSecano",
            "poblacionExtranjera",
            "numContenedoresVidrio",
            "kilosVidrioRecogidos",
            "hectareasZona",
            "numIncendios",
            "hectareasQuemadas",
            "numDepuradoras",
            "numeroAutonomos",
            "numParados",
            "numContratados",
            "numAccidentesLaborales",
            "rentaPerCapita",
            "empresasPorTrabajadores",
            "empresasPorSector",
            "empresasPorActividad",
            "usoSuelo",
            "hectareasTipoSuelo",
            "antiguedadEdificios",
            "transportIssues",
            "transportIssueType",
            "transportIssueWhere",
            "transportIssueReason",
            "transportIssueRestrictions",
            "transportRoads",
            "transportRoadSpeed",
            "transportRoadType",
            "transportRoadLocation",
            "transportRoadDescription",
            "transportRoadZones",
            "transportRoadBridges",
            "transportBridgesLocation",
            "transportRoadKmBridge",
            "transportBridgesKms",
            "transportRoBridLocations",
            "tipoIncidencia",
            "transportRoadLengthOrigen",
            "transportRoadLengthDestino",
            "calendarHolidaysDay",
            "calendarHolidaysWhen",
            "calendarHolidaysWhere",
            "calendarHolidaysLocationDay",
            "calendarHolidaysLocationPlace",
            "Year",
            "calendarHolidaysMonth",
            "Month",
            "tipoLocalizacion",
            "transportRoadNameLength",
            "calendarHolidays",
            "calendarRangeHolidays",
            "dateFrom",
            "dateTo",
            "autobus_location",
            "locdesde",
            "lochasta",
            "locactual",
            "typebuses",
            "horarioautobuses_desde",
            "horarioautobuses_hasta",
            "empresasTuristicasActivas",
            "empresasTuristicasActividades",
            "empresasTuristicasContacto",
            "empresasTuristicasDireccion",
        ]

    @staticmethod
    def subintents() -> list:
        return [
            "Year",
            "Cargo",
            "rutasDestino",
            "tipoAlojamiento",
            "tipoLugar",
            "tipoTemporada",
            "tipoHabitacion",
            "categoria",
            "tipoLocalizacion",
            "tipoArea",
            "sexo",
            "nombreArea",
            "tipoSuperficie",
            "sector",
            "numTrabajadores",
            "actividad",
            "tipoSuelo",
            "antiguedad",
        ]

    
    legacy = 'GA_OD_Core'

    '''@staticmethod
    def legacy(server):

        if server == 0:
            return 'GA_OD_Core'
        else:
            return 'GA_OD_Core_legacy'''

    urlIssues = "https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json"
    