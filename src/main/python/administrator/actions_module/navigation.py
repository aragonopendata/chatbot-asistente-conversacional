'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import unidecode
import requests
from urllib.parse import unquote

import re


from rasa_sdk import Action
from browser.config import *
from SPARQLWrapper import SPARQLWrapper, JSON
from browser.logger import Log

class InfoTemas:
    descCat = dict()
    descCat["CultureLeisureAndTourism"] = ["Cultura, ocio y turismo", "turismo"]
    descCat["InfrastructureTransportAndRoads"] = ["Infraestructuras y transportes", "infraestructuras y transportes"]
    descCat["Health"] = ["Salud", "salud"]
    descCat["EducationResearchAndDevelopment"] = ["Investigación y desarrollo ", "investigacion"]
    descCat["CitizenRightsAndServices"] = ["Derechos civiles y servicios", "derechos civiles"]
    descCat["WaterAndHealth"] = ["Aguas", "aguas"]
    descCat["AssociationsFoundationsAndProfessionalColleges"] = ["Asociaciones, fundaciones y colegios profesionales", "colegios profesionales"]
    descCat["BusinessTradeAndAssociations"] = ["Asociaciones comerciales", "asociaciones comerciales"]
    descCat["LawAndJustice"] = ["Ley y justicia", "ley y justicia"]
    descCat["TerritoryAndTransport"] = ["Territorio y transporte", "territorio y transporte"]
    descCat["TouristCompanies"] = ["Compañías turísticas", "compañias turisticas"]
    descCat["TouristServices"] = ["Servicios turísticos", "servicios turisticos"]
    descCat["SystemsAndEducationalCenters"] = ["Centros educativos", "centros educativos"]
    descCat["ConsumerInformation"] = ["Información de consumo", "informacion de consumo"]
    descCat["Culture"] = ["Cultura", "cultura"]
    descCat["HousingAidsAndSubsidies"] = ["Ayudas alquiler", "ayudas alquiler"]
    descCat["Housing"] = ["Alquileres", "alquileres"]
    descCat["Business"] = ["Negocios", "negocios"]

    descTema = dict()

    descTema["dara_archivos_aragon"] = ["--. ", "-"]
    descTema["punto_informacion_turistica"] = ["Puedes preguntarme por oficinas de turismo. Dónde están, su teléfono, su  email, etc…", "puntos de información turística"]
    descTema["empresa_turismo_activo"] = ["--. ", "empresas de turismo activo"]
    descTema["alojamiento_hotelero"] = ["Puedes preguntarme por alojamiento hotelero. Dónde están, su teléfono, su  email, número de camas, categoría, tipos de habitaciones, etc…", "alojamientos hoteleros"]
    descTema["camping_turistico"] = ["Tengo información sobre campings. Dónde están, su teléfono, su  email, número de plazas, bungalows, etc…", "campings"]
    descTema["apartamento_turistico"] = ["Puedes preguntarme por apartamentos turisticos. Dónde están, su teléfono, su  email, etc…", "apartamentos turisticos"]
    descTema["sendero"] = ["Puedes preguntarme por senderos. De donde salen o a donde llegan.", "senderos"]
    descTema["alojamiento_rural"] = ["Tengo muchos datos de casas rurales. Dónde están, su teléfono, su  email, etc…", "casas rurales"]
    descTema["oficina_turismo"] = ["Puedes preguntarme por oficinas de turismo. Dónde están, su teléfono, su  email, etc…", "oficinas de turismo"]
    descTema["cafeteria_restaurante"] = ["Tengo mucha información de cafeterías y restaurantes. Dónde están, cómo reserevar, su teléfono, su  email, su web, etc…", "cafeterias y restaurantes"]
    descTema["albergue_refugio"] = ["Puedes preguntarme por albergues y refugios. Dónde están, su teléfono, su  email, etc…", "albergues y refugios"]
    descTema["agencia_viaje"] = ["Puedes preguntarme por agencias de viaje. Dónde están, su teléfono, su  email, etc…", "agencias de viaje"]
    descTema["dara_aragon"] = ["--. ", "-"]
    descTema["colecciones_museos_aragon"] = ["Puedes preguntarme por obras de arte. En qué museo están.", "obras de arte"]
    descTema["guia_turismo"] = ["Puedes preguntarme por guías turísticos. Dónde están, su teléfono, su  email, etc…", "guías turísticos"]
    descTema["alogamiento_hotelero"] = ["--. ", "-"]
    descTema["apartamento"] = ["Puedes preguntarme por apartamentos. Dónde están, su teléfono, su  email, etc…", "apartamentos"]
    descTema["camping"] = ["--. ", "campings"]
    descTema["simbolo"] = ["--. ", "-"]

    descTema["comarca"] = ["Puedes preguntarme por las comarcas. Qué municipos lo componen, quién es el presidente, etc…", "comarcas"]
    descTema["municipio"] = ["Puedes preguntarme por los municipios. Dónde está el ayuntamiento, su teléfono, fax,  quién es el alcalde, etc…", "municipios"]
    descTema["captacion"] = ["Tengo información de reciclaje de vidrio. Cuantos kilos de vidrio recogido en un año.", "reciclaje de vidrio"]
    descTema["miembro_pleno_municipal"]=["Puedes preguntarme por los miembros del pleno. Quienes son los concejales, el alcalde, etc..", "miembros del pleno"]
    descTema["sociedad_mercantil"] = ["Puedes preguntarme por los contratos de empleo. Cuantos contratos se hicieron por año y sexo.", "contratos de empleo"]
    descTema["arabus_parada"] = ["Puedes preguntarme por ....", "paradas de Arabus"]
    descTema["transporte_parada"] = ["Puedes preguntarme por ....", "paradas de transporte"]
    descTema["transportista"] = ["Puedes preguntarme por ....", "transportistas"]

    descTema["iaf_poligono_industrial"] = ["Puedes preguntarme por ....", "polígonos industriales"]

    allTemas = ["dara_archivos_aragon", "punto_informacion_turistica", "empresa_turismo_activo", "alojamiento_hotelero", "camping_turistico", "apartamento_turistico", "sendero", "alojamiento_rural", "oficina_turismo", "cafeteria_restaurante", "albergue_refugio", "agencia_viaje", "dara_aragon", "colecciones_museos_aragon", "guia_turismo", "alogamiento_hotelero", "apartamento", "camping", "simbolo", "comarca", "municipio", "cra_parada", "transporte_parada", "arabus_parada", "iaf_poligono_industrial", "transporte_expedicion_parada_horario", "transporte_concesion", "transporte_expedición", "transporte_ruta", "cra_datos_ruta", "itinerario_ruta", "concesion", "arabus_concesion", "servicio", "ruta", "parada", "expedicion_parada_y_horario", "expedicion", "transportista", "operador", "villas_y_tierras", "nucleo", "entidad_singular", "entidad_menor", "agrupacion_secretarial", "pozo", "iaa_contratos_gastos_anuales", "iaa_contrato_depuradora", "depuradora", "deposito", "conduccion", "colector", "captacion", "camara_limpia", "boca_de_riego", "sumidero", "hidrante", "emisario", "edar_en_construccion", "edar", "distribucion", "ramal", "potabilizadora", "llave_de_corte", "iaa_contrato", "iaa_contrato_depuradoras", "iaa_contrato_gastos_anuales", "cra_centro", "cra_localidad", "postgrado", "curso", "miembro_pleno", "modificacion_planeamiento_desarrollo", "planeamiento_general", "planeamiento_desarrollo", "planeamiento", "modificaciones_planeamiento_general", "miembro_pleno_comarcal", "miembro_pleno_villas_y_tierras", "ordenanza_general_nucleo", "ordenanza_general_consorcio", "ordenanza_fiscal_consorcio", "ordenanza_general_comarca", "periodo_legislatura", "proceso_electoral", "registro_llamada", "eleccion", "presupuesto", "noticia", "ordenanza_fiscal_villas_y_tierras", "ordenanza_fiscal_organismo_autonomo", "ordenanza_fiscal_mancomunidad", "ordenanza_fiscal_entidad_menor", "ordenanza_fiscal_diputacion", "ordenanza_fiscal_comarca", "ordenanza_fiscal_municipio", "ordenanza_general_villas_y_tierras", "ordenanza_general_organismo_autonomo", "ordenanza_general_mancomunidad", "ordenanza_general_entidad_menor", "ordenanza_general_diputacion", "ordenanza_general_municipio", "cargo", "miembro_pleno_organismo_autonomo", "miembro_pleno_mancomunidad", "miembro_pleno_entidad_menor", "miembro_pleno_consorcio", "miembro_pleno_municipal", "entidad", "direccion_de_interes", "diputacion", "modificaciones_planeamiento_desarrollo", "organizacion_auxiliar", "organizacion_complementaria", "mancomunidad", "fundacion", "consorcio", "plantilla", "sociedad_mercantil", "organismo_autonomo", "fianzas_datos_anuales_vivienda_y_rehabilitacion"]

#    nameTema = dict()
#    nameTema["guia_turismo"] = "?id ei2a:fullName ?name"
#    nameTema["sendero"] = "?id dc:title ?name"
#    nameTema["arabus_parada"] = "?id dc:title ?name"


class ActionListSubject(Action):
    def name(self):
        return "action_engagement_subject"

    def getentity(self, tracker, entName):
        for ent in tracker.latest_message['entities']:
            if entName == ent['entity']:
                return ent['value']

    def getsubject(self, tracker):
        subject = self.getentity(tracker, "subject_type")
        if subject is None:
            subject = self.getentity(tracker, 'misc')
        if subject is None:
            subject = self.getentity(tracker, 'location')
        if subject is None:
            subject = self.getentity(tracker, 'organization')
        if subject is None:
            subject = self.getentity(tracker, 'person')
        if subject is None:
            subject = ""

        return subject

    def replaceaccents(self, cadena):
        cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
        cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
        cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
        cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
        cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
        return cadena

    def getNearInstances(self, instance):
        sparql = SPARQLWrapper(Config.bbdd_url())
        # query = """
        #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        #     PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
        #     PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
        #     PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
        #     PREFIX dc: <http://purl.org/dc/elements/1.1/>
        #
        #     SELECT   ?id ?name
        #     WHERE {{  <{0}> geo:location ?id_location .
        #             <{0}> dc:type ?instance_type .
        #             ?id ?relation ?id_location .
        #             ?id dc:type ?type .
        #             ?id ei2a:organizationName  ?name .
        #             FILTER (?type=?instance_type)
        #          }}"""
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
            PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
            PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX org: <http://www.w3.org/ns/org#>
         
            SELECT ?id ?name  ?loc ?nameLoc ?id_comarca ?nameComarca
            WHERE {{  <{0}> geo:location ?id_location .
                  <{0}> dc:type ?instance_type .
                  ?id_location org:subOrganizationOf ?id_comarca
                   FILTER REGEX (str(?id_comarca),"comarca","i") .
                  ?loc org:subOrganizationOf ?id_comarca .
                  ?id_comarca ei2a:organizationName ?nameComarca.
                  ?id geo:location ?loc .
                  ?loc ei2a:organizationName ?nameLoc .
                  ?id dc:type ?type
                  FILTER (?type=?instance_type) .
                  ?id ei2a:organizationName  ?name .
               }}
        """
        query = query.format(instance)
        print(query)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    def getNearSubject(self, idEntidad):
        sparql = SPARQLWrapper(Config.bbdd_url())
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
            PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
            PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            
            SELECT   ?category ?id ?id_location ?locName (COUNT(*) as ?nInstances)
            WHERE {{  <{0}> geo:location ?id_location .
                    <{0}> dc:type ?instance_type .
                    ?instance_type rdf:type ?instance_category .
                    ?instance ?relation ?id_location .
                    ?id_location ei2a:organizationName ?locName .
                    ?instance dc:type ?id.
                    ?id rdf:type ?category
                    FILTER (?category=?instance_category)
                 }}
            GROUP BY ?category ?id ?id_location ?locName
            ORDER BY ?category ?id ?locName
        """
        query = query.format(idEntidad)
        print(query)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        butons = []
        firstid = ""
        if len(results["results"]["bindings"]) > 0:
            for i, result in enumerate(results["results"]["bindings"]):
                if firstid == result['id']['value']:
                    break
                if i == 0:
                    firstid = result['id']['value']
                nomTema = result['id']['value'].split("#")[1]
                if nomTema in InfoTemas.descTema:
                    nomTema = InfoTemas.descTema[nomTema][1]
                if nomTema != "-":
                    button = {
                        "title": nomTema.capitalize() +" en "+ result['locName']['value'] + " (" + str(result['nInstances']['value']) + ")",
                        "payload": "/{intencion}{{\"subject_type\": \"{subject}\",\"loc_id\": \"{loc_id}\"}}".format(intencion="engagement.subject", subject=result['id']['value'], loc_id=result['id_location']['value'])
                    }
                    butons.append(button)
        return butons

    def getName(self, result):
        if "name" in result:
            nameEntity = result['name']['value']
        else:
            nameEntity = result['id']['value'].split("#")[1]
        return nameEntity

    def buttonName(self, result):
        nameEntity = self.getName(result)

        tema = unquote(result['id']['value'].split("#")[1]) + ": " + unquote(nameEntity)
        button = {
            "title": tema,
            "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(intencion="engagement.subject", subject=result['id']['value'])
        }
        return button

    def run(self, dispatcher, tracker, domain):
        pagsize = 5
        hiddeProps = ["SIGNATURA", "RNUM", "ACTIVIDAD_SIGLA", "TITULARIDAD", "EXPEDIENTE_EJERCICIO", "EXPEDIENTE_NUMERO", "NACIONALIDAD", "FECHA_SOLICITUD", "PROVINCIA_ESTABLECIMIENTO", "MUNICIPIO_ESTABLECIMIENTO", "MODALIDAD_CAMPING", "MODALIDAD", "GRUPO", "SUBGRUPO", "POSITIONLIST", "TYPE", "GEOM",
                      "CLASSES", "PHOTOS", "SOURCE", "IDENTIFIER", "ISOFINTERESTTO", "TIPO ESTABLECIMIENTO", "CODIGO", "ELM_ID"]

        subject = self.getsubject(tracker)
        subject = unidecode.unidecode(subject)  # elimina acentos
        buttons = []
        for cat in InfoTemas.descCat:
#            if InfoTemas.descCat[cat][1] == subject:
            if subject in InfoTemas.descCat[cat][1]:
                subject = cat

        if subject in InfoTemas.descCat:  ## Nivel 1
            sparql = SPARQLWrapper(Config.bbdd_url())
            query = """
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
                PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
                PREFIX dc: <http://purl.org/dc/elements/1.1/>

                  SELECT   ?subject (count(*) as ?nInstances)
                  FROM <http://opendata.aragon.es/def/ei2a>
                  WHERE {{?subject rdf:type <http://opendata.aragon.es/def/ei2a/categorization#{0}> .
                         ?instance dc:type ?subject}}
                    order by ?subject                         
            """
            query = query.format(subject)
            print(query)
            Log.log_debug(query)
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            msg = "Tengo información sobre estos contenidos. ¿Qué te interesa? \n"
#            for result in results["results"]["bindings"]:
#                msg = msg + result['subject']['value'].split("#")[1].replace("_", " ").capitalize() + ", "
#            msg = msg[:-2] + ". O ver los temas generales:"
            for result in results["results"]["bindings"]:
                tema = result['subject']['value'].split("#")[1]
                if (tema not in InfoTemas.descTema) or (tema in InfoTemas.descTema and InfoTemas.descTema[tema][1] != "-"):
                    numEntities = int(result['nInstances']['value'])
                    if numEntities > 0:
                        buttons.append(
                            {
                                "title": tema.replace("_", " ").capitalize() + " (" + str(numEntities) + ")",
                                "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(intencion="engagement.subject", subject=tema)
                            })

            buttons.append(
                {
                    "title": "Ver los temas generales",
                    "payload": "/greetings.hello"
                })
            dispatcher.utter_message(text=msg, buttons=buttons)
        else:
            if "#" in subject and subject.split("#")[1] in InfoTemas.allTemas:  ## http://opendata.aragon.es/def/ei2a#transporte_expedicion_parada_horario -> transporte_expedicion_parada_horario
                subject = subject.split("#")[1]
            for cat in InfoTemas.descTema:
                if InfoTemas.descTema[cat][1] == subject:
                    subject = cat
            if subject in InfoTemas.allTemas:  ## Nivel 2
                msg = ""
                if subject in InfoTemas.descTema:
                    msg += InfoTemas.descTema[subject][0] + " O ver los temas generales."

                sparql = SPARQLWrapper(Config.bbdd_url())
                if not self.getentity(tracker, 'loc_id') is None:
                    geo = "?id  geo:location <{0}> . <{0}> ei2a:organizationName ?locName .".format(self.getentity(tracker, 'loc_id'))
                else:
                    geo = ""
                query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX dc: <http://purl.org/dc/elements/1.1/>
                    PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
                    PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>

                    SELECT *
                    WHERE {{?id dc:type ei2a:{0} . 
                    """ + geo + """ 
                            OPTIONAL{{ {{?id dc:title ?name }}
                                     UNION
                                    {{ ?id ei2a:organizationName  ?name }}
                                    UNION
                                    {{ ?id ei2a:fullName ?name }} 
                                     UNION
                                    {{ ?id ei2a:nameDocument  ?name }} }}                  
                    }}
                    ORDER BY ?name
                    """
                query = query.format(subject)
                print(query)
                Log.log_debug(query)
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                regNum = self.getentity(tracker, 'page')
                if not regNum:
                    regNum = 0
                else:
                    regNum = int(regNum)
                if len(results["results"]["bindings"]) > 0:
                    if subject in InfoTemas.descTema:
                        msg = "De " + InfoTemas.descTema[subject][1]
                        if "locName" in results["results"]["bindings"][0]:
                            msg = msg + " en " + results["results"]["bindings"][0]['locName']['value']
                        msg = msg + " tengo la siguiente información:"
                    else:
                        msg = "De \"" + subject + "\" tengo la siguiente información:"
                    if not self.getentity(tracker, 'loc_id') is None:
                        payloadstr =  "/{intencion}{{\"subject_type\": \"{subject}\", \"loc_id\": \"" + self.getentity(tracker, 'loc_id') + "\" ,\"page\": \"{page}\"}}"
                    else:
                        payloadstr =  "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}"
                    for i, result in enumerate(results["results"]["bindings"]):
                        if i < regNum:
                            continue
                        if i > regNum + pagsize - 1:
                            if regNum > 0:
                                buttons.append(
                                    {
                                        "title": "Mostrar " + str(pagsize) + " registros anteriores",
                                        "payload":payloadstr.format(intencion="engagement.subject", subject=subject, page=regNum - pagsize)
                                    })
                            buttons.append(
                                {
                                    "title": "Mostrar " + str(pagsize) + " registros más",
                                    "payload": payloadstr.format(intencion="engagement.subject", subject=subject, page=regNum + pagsize)
                                })
                            break
                        buttons.append(self.buttonName(result))
                    i = 0
                    result = results["results"]["bindings"][i]
                    if len(results["results"]["bindings"]) > 5:
                        while i < len(results["results"]["bindings"]):
                            letter = self.getName(result)[0].lower()
                            if letter in "abcdefghijklmnñopqrstuvwxyz":
                                buttons.append(
                                    {
                                        "title": letter,
                                        "payload": payloadstr.format(intencion="engagement.subject", subject=subject, page=i)
                                    })
                            while letter == self.getName(result)[0].lower() and i < len(results["results"]["bindings"]):
                                result = results["results"]["bindings"][i]
                                i = i + 1

                buttons.append(
                    {
                        "title": "Ver los temas generales",
                        "payload": "/greetings.hello"
                    })
                dispatcher.utter_message(text=msg, buttons=buttons)
            else:  ## Por ID entidad
                subject = self.getsubject(tracker)
                sparql = SPARQLWrapper(Config.bbdd_url())
                query = """
                    PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
                    PREFIX dc: <http://purl.org/dc/elements/1.1/>
                    PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>                    

                    SELECT *
                    WHERE
                    {{  OPTIONAL{{ {{<{0}> dc:title ?name }}
                        UNION
                            {{ <{0}> ei2a:organizationName  ?name }}
                        UNION
                            {{ <{0}> ei2a:fullName ?name }} 
                        UNION
                            {{ <{0}> ei2a:nameDocument ?name }} 
                        UNION
                            {{ <{0}> dc:identifier ?name }} 
                        UNION
                            {{ <{0}>  dc:type ?name }}  .                                                     
                        {{ <{0}> dc:source ?source }}
                        }}
                    }}
                """
                query = query.format(subject)
                print(query)
                Log.log_debug(query)
                sparql.setQuery(query)
                sparql.setReturnFormat(JSON)
                results = None
                try:
                    results = sparql.query().convert()
                except Exception:
                    pass
                if results is not None and len(results["results"]["bindings"]) > 0 and len(results["results"]["bindings"][0]) > 0:
                    msg = "De \"" + results["results"]["bindings"][0]['name']['value'] + "\" tengo la siguiente información: \n"
                    url = results["results"]["bindings"][0]['source']['value']
                    r = requests.get(url)
                    resSource = r.json()
                    if r.status_code == requests.codes.ok and len(resSource) == 2:
                        for i, prop in enumerate(resSource[0]):
                            if resSource[1][i] and str(resSource[1][i]) != "" and prop not in hiddeProps:
                                msg = msg + prop.capitalize().replace("_", " ") + ": " + str(resSource[1][i]) + "\n"
                    else:  # No tiene source válido, saco las propiedades de primer nivel
                        query = """
                            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                            PREFIX dc: <http://purl.org/dc/elements/1.1/>
                            PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
                            PREFIX sch: <http://www.w3.org/2000/01/rdf-schema#>

                            SELECT ?property ?value ?type ?range
                            FROM <http://opendata.aragon.es/def/ei2a>
                            WHERE {{<{0}> ?property ?value .
                                   OPTIONAL {{?property rdf:type ?type .
                                             ?property sch:range ?range}}      
                            }}
                        """
                        query = query.format(subject)
                        print(query)
                        Log.log_debug(query)
                        sparql.setQuery(query)
                        sparql.setReturnFormat(JSON)
                        results = sparql.query().convert()
                        oldmsg = ""
                        for i, res in enumerate(results["results"]["bindings"]):
                            label = res["property"]["value"].replace("/", "#").split("#")[-1]
                            newmsg = label.capitalize() + ": " + str(res["value"]["value"]) + "\n"
                            if newmsg != oldmsg and str(label).upper() not in hiddeProps:
                                msg = msg + newmsg
                            oldmsg = newmsg
                    # Instancias cercanas del mismo tipo
                    nearInstances = self.getNearInstances(subject)
                    if len(nearInstances["results"]["bindings"]) > 0:
                        msg = msg + "Otros datos cercanos que podrían interesarte:"
                        for i, result in enumerate(nearInstances["results"]["bindings"]):
                            if (result['id']['value'] != subject) and i < 6:
                                buttons.append(self.buttonName(result))
                    # Instancias cercanas del mismo tipo
                    buttons.extend(self.getNearSubject(subject))

                    buttons.append(
                        {
                            "title": "Ver los temas generales",
                            "payload": "/greetings.hello"
                        })
                    dispatcher.utter_message(text=msg, buttons=buttons)
                else:  ## Por Nombre de entidad

                    subject = self.getsubject(tracker)
                    sparql = SPARQLWrapper(Config.bbdd_url())
                    query = """
                        PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
                        PREFIX dc: <http://purl.org/dc/elements/1.1/>

                        SELECT *
                            WHERE
                           { 
                            {?id ei2a:organizationName ?name }
                               UNION
                            { ?id ei2a:fullName ?name } 
                               UNION
                            { ?id dc:title ?name}                        
                                FILTER regex (?name,\"""" + self.replaceaccents(subject) + "\", \"i\")}" + \
                    "   ORDER BY ?name "
                    print(query)
                    Log.log_debug(query)
                    sparql.setQuery(query)
                    sparql.setTimeout(60)
                    sparql.setReturnFormat(JSON)
                    try:
                        results = sparql.query().convert()
                    except Exception:
                        buttons.append(
                            {
                                "title": "Ver los temas generales",
                                "payload": "/greetings.hello"
                            })
                        dispatcher.utter_message("El servidor está sobrecargado en estos momentos, espere un poco y vuelva a intentarlo", buttons=buttons)
                        return []
                    regNum = self.getentity(tracker, 'page')
                    if not regNum:
                        regNum = 0
                    else:
                        regNum = int(regNum)
                    if len(results["results"]["bindings"]) > 0:
                        msg = "De \"" + subject + "\" tengo la siguiente información:"
                        i = 0
                        for result in results["results"]["bindings"]:
                            if i < regNum:
                                i = i + 1
                                continue
                            if i > regNum + pagsize - 1:
                                if regNum > 0:
                                    buttons.append(
                                        {
                                            "title": "Mostrar " + str(pagsize) + " registros anteriores",
                                            "payload": "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}".format(intencion="engagement.subject", subject=subject, page=regNum - pagsize)
                                        })
                                buttons.append(
                                    {
                                        "title": "Mostrar " + str(pagsize) + " registros más",
                                        "payload": "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}".format(intencion="engagement.subject", subject=subject, page=regNum + pagsize)
                                    })
                                break
                            tema = result['id']['value'].split("#")[1] + ": " + result['name']['value']
                            #                            if "museo" in result['id']['value'].split("#")[1] or "organizacion-complementaria" in result['id']['value'].split("#")[1]:
                            #                                continue
                            regsearch = r"\b(" + self.replaceaccents(subject) + r")\b"
                            if re.search(regsearch, result['name']['value'], re.IGNORECASE):
                                buttons.append(
                                    {
                                        "title": tema,
                                        "payload": "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}".format(intencion="engagement.subject", subject=result['id']['value'], page=regNum + pagsize)
                                    })
                                i = i + 1
                        buttons.append(
                            {
                                "title": "Ver los temas generales",
                                "payload": "/greetings.hello"
                            })
                        dispatcher.utter_message(text=msg, buttons=buttons)

                    else:
                        msg = "De momento no te puedo proporcionar información de este tema pero puedes ver los temas generales."
                        buttons.append(
                            {
                                "title": "Ver los temas generales",
                                "payload": "/greetings.hello"
                            })
                        dispatcher.utter_message(text=msg, buttons=buttons)

        return []
