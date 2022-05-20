"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from ast import Not
from httplib2 import Response

import unidecode
import requests
from urllib.parse import unquote


import re

from rasa_sdk import Action
from actions_utils import replace_accents
from browser.config import *
from browser.logger import Log
from SPARQLWrapper import SPARQLWrapper, JSON
from actions_module.utils import *
from actions_module.message import  Msgs
from actions_module.info_temas import InfoTemas



class ActionEngagementSubject(Action):
    """Class which offers differents proposals to citizens
        in order to engage the citizen
    """


    def name(self):
        """ Class property. Returns the name of the class"""

        return "action_engagement_subject"

    def __init__(self) -> None:
        """ Initialisation of the class (embedder) for citizen engagement """

        self.understand_ckan = True
        self.button_general_theme= {
                    "title": "Ver los temas generales",
                    "payload": "/greetings.hello"
                }

    def get_button_title(self, intent, entities):
        """ Performs the query provided on the CKAN of Aragon Open Data

        Parameters
        ----------
        intent: intent associated to the button
        entitities: List of ententies

        Returns
        -------
        list

            Names of buttons returned
        """
        return intent_mapping.get_button_title(intent, entities)

    def get_entity(self, tracker, entName):
        """ Get the proper entitiy and returns its value

        Parameters
        ----------
        tracker: All the information sent to the Assistant from the interface
        entName: Name of the entity to search

        Returns
        -------
        String

            Value of the searched entity
        """
        for ent in tracker.latest_message['entities']:
            if entName == ent['entity']:
                return ent['value']

    def get_subject(self, tracker):
        """ Get the value of the entity depending their category

        Parameters
        ----------
        tracker: All the information sent to the Assistant from the interface

        Returns
        -------
        String

            Value of the searched entity
        """
        subject = tracker.get_slot("subject_type")

        if subject is None:
            subject = self.get_entity(tracker, 'misc')
        if subject is None:
            subject = self.get_entity(tracker, 'location')
        if subject is None:
            subject = self.get_entity(tracker, 'organization')
        if subject is None:
            subject = self.get_entity(tracker, 'person')
        if subject is None:
            subject = ""

        return subject


    def get_near_instances(self,sparql, instance):
        """ Preparation of a query to extract subjects geographically close to the original entity

        Parameters
        ----------
        sparql: Connection to Virtuoso
        instance: location to be searched

        Returns
        -------
        json

            Value of the searched entity
        """
        instance_type = instance[:instance.rfind("/")]
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
            PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX org: <http://www.w3.org/ns/org#>

            SELECT  DISTINCT ?id ?name   ?loc ?nameLoc ?id_comarca ?nameComarca
            from <http://opendata.aragon.es/def/ei2av2>
            WHERE {{  <{0}> org:linkedTo ?loc
                     FILTER (REGEX(?loc, "municipio", "i")  ) .
                     <{0}> org:linkedTo ?id_comarca
                     FILTER (REGEX(?id_comarca, "comarca", "i")  ) .
                     ?id_comarca dc:title ?nameComarca .
                     ?id org:linkedTo ?id_loc .
                     ?id org:linkedTo ?id_comarca .
                     ?id dc:title ?name .
                     FILTER( STRSTARTS( str(?id), "{1}" ) ) .
                      ?id org:hasSite ?site .
                      ?site org:siteAddress ?address .
                      ?address vcard:locality ?nameLoc .
            }}
            ORDER BY ?id
        """

        query = query.format(instance,instance_type)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def get_near_subject(self, id_entidad):
        """ Preparation of a query to extract other instances with the same subject that the first one

        Parameters
        ----------
        id_entidad: selected element

        Returns
        -------
        json

            List of entities of the same topic
        """
        sparql = SPARQLWrapper(Config.bbdd_url())

        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
            PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
            PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>

            SELECT  ?category ?id ?id_location ?locName (COUNT(*) as ?nInstances)
            from <http://opendata.aragon.es/def/ei2av2>
            WHERE {{
                    <{0}> org:linkedTo ?id_location
                    FILTER (REGEX(?id_location, "municipio", "i")  ) .
                    <{0}> org:classification ?instance_category .
                    <{0}> org:hasSite ?site .
                    ?site org:siteAddress ?address .
                    ?address vcard:locality ?locName .
                    ?instance org:linkedTo  ?id_location
                    BIND( REPLACE( str(?instance), '\\\\/[^/]*$', '' ) AS ?id) .
                    ?instance org:classification  ?category
                    FILTER (?category=?instance_category)
                 }}
            GROUP BY ?category ?id ?id_location ?locName
           ORDER BY ?category ?id ?locName
        """

        query = query.format(id_entidad)
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
                nomTema = result['id']['value'].split("/")[-1]
                if nomTema in InfoTemas.themeDescription:
                    nomTema = InfoTemas.themeDescription[nomTema][1]
                if nomTema != "-":
                    button = {
                        "title": nomTema.capitalize() +" en "+ result['locName']['value'] + " (" + str(result['nInstances']['value']) + ")",
                        "payload": "/{intencion}{{\"subject_type\": \"{subject}\",\"loc_id\": \"{loc_id}\"}}".format(intencion="engagement.subject", subject=result['id']['value'], loc_id=result['id_location']['value'])
                    }
                    butons.append(button)
        return butons

    def get_name(self, result):
        """ Delete the prefix from a instance to get its name

        Parameters
        ----------
        result: Instance

        Returns
        -------
        String

            Name of the instance
        """
        return (
            result['name']['value']
            if "name" in result
            else result['id']['value'].split("/")[-1]
        )

    def button_name(self, result):
        """ Create the code to draw a button in the interfaz

        Parameters
        ----------
        result: Instance

        Returns
        -------
        json

            Information to send to the interfaz to build a button
        """
        nameEntity = self.get_name(result)
        tema = unquote(nameEntity)

        return {
            "title": tema,
            "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(intencion="engagement.subject", subject=result['id']['value'])
        }

    def run(self, dispatcher, tracker, domain):
        """ Main function of the class
            Execute the flow to answer the end-user questions
            and look for other suggestions closed to the answer
            Near instances: by subject and location

        Parameters
        ----------
        dispatcher:
        tracker: information that comes from front-end

        Returns
        -------
        json

            Answer of the chatbot to send to the end-user
        """
        evt = []   # Returned event to the agent
        page_size = 5
        hidde_props = ["SIGNATURA", "RNUM", "ACTIVIDAD_SIGLA", "TITULARIDAD", "EXPEDIENTE_EJERCICIO", "EXPEDIENTE_NUMERO", "NACIONALIDAD", "FECHA_SOLICITUD", "PROVINCIA_ESTABLECIMIENTO", "MUNICIPIO_ESTABLECIMIENTO", "MODALIDAD_CAMPING", "MODALIDAD", "GRUPO", "SUBGRUPO", "POSITIONLIST", "TYPE", "GEOM",
                      "CLASSES", "PHOTOS", "SOURCE", "IDENTIFIER", "ISOFINTERESTTO", "TIPO ESTABLECIMIENTO", "CODIGO", "ELM_ID"]

        subject = self.get_subject(tracker)
        subject = unidecode.unidecode(subject)  # Deletion of accents
        buttons = []

        # Searches the catalogue description to see if there is a category related to the text entered.
        # Pick up the category and select topics related to that word
        for cat in InfoTemas.description_catalog:
            if (subject or len(subject.strip())) and subject in InfoTemas.description_catalog[cat][1]:
                subject = cat
        sparql_connetion = SPARQLWrapper(Config.bbdd_url())

        if subject in InfoTemas.description_catalog:  ## Level 1
            results = self.get_theme_first_level(subject, sparql_connetion)
            msg = "Tengo información sobre estos contenidos. ¿Qué te interesa? \n"
            for result in results["results"]["bindings"]:
                tema = result['subject']['value']
                if (
                    tema not in InfoTemas.themeDescription
                    or InfoTemas.themeDescription[tema][1] != "-"
                ):
                    number_entities = int(result['nInstances']['value'])
                    if number_entities > 0:
                        buttons.append(
                            {
                                "title": tema.split('/')[-1].replace("-", " ").capitalize() + " (" + str(number_entities) + ")",
                                "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(intencion="engagement.subject", subject=tema)
                            })

            buttons.append(self.button_general_theme)

            dispatcher.utter_message(text=msg, buttons=buttons, json_message={"understand_ckan": self.understand_ckan})
        else:
            #if "#" in subject and subject.split("#")[1] in InfoTemas.allTemas:  ## http://opendata.aragon.es/def/ei2a#transporte_expedicion_parada_horario -> transporte_expedicion_parada_horario
            subject2=""
            if subject.split("/")[-1] in InfoTemas.allTemas:  ## http://opendata.aragon.es/def/ei2a#transporte_expedicion_parada_horario -> transporte_expedicion_parada_horario
                subject2 = subject.split("/")[-1]
            for cat in InfoTemas.themeDescription:
                if InfoTemas.themeDescription[cat][1] == subject2:
                    subject = cat
            if subject2 in InfoTemas.allTemas:  ## Level 2
                msg = ""
                if subject in InfoTemas.themeDescription:
                    msg += InfoTemas.themeDescription[subject][0] + " O ver los temas generales."

                results = self.get_themes_by_locations(tracker, subject, sparql_connetion)
                page_number = self.get_entity(tracker, 'page')
                if not page_number:
                    page_number = 0
                else:
                    page_number = int(page_number)
                if len(results["results"]["bindings"]) > 0:
                    if subject in InfoTemas.themeDescription:
                        msg = "De " + InfoTemas.themeDescription[subject][1]
                        if "locName" in results["results"]["bindings"][0]:
                            msg = msg + " en " + results["results"]["bindings"][0]['locName']['value']
                        msg = msg + " tengo la siguiente información:"
                    else:
                        msg = "De \"" + subject2 + "\" tengo la siguiente información:"
                    if not self.get_entity(tracker, 'loc_id') is None:
                        payload_str =  "/{intencion}{{\"subject_type\": \"{subject}\", \"loc_id\": \"" + self.get_entity(tracker, 'loc_id') + "\" ,\"page\": \"{page}\"}}"
                    else:
                        payload_str =  "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}"
                    for i, result in enumerate(results["results"]["bindings"]):
                        if i < page_number:
                            continue
                        if i > page_number + page_size - 1:
                            if page_number > 0:
                                buttons.append(
                                    {
                                        "title": "Mostrar " + str(page_size) + " registros anteriores",
                                        "payload":payload_str.format(intencion="engagement.subject", subject=subject, page=page_number - page_size)
                                    })
                            buttons.append(
                                {
                                    "title": "Mostrar " + str(page_size) + " registros más",
                                    "payload": payload_str.format(intencion="engagement.subject", subject=subject, page=page_number + page_size)
                                })
                            break
                        buttons.append(self.button_name(result))
                    i = 0
                    result = results["results"]["bindings"][i]
                    if len(results["results"]["bindings"]) > 5:
                        while i < len(results["results"]["bindings"]):
                            letter = str(self.get_name(result)[0].lower())
                            if letter in "0123456789abcdefghijklmnñopqrstuvwxyz":
                                buttons.append(
                                    {
                                        "title": letter,
                                        "payload": payload_str.format(intencion="engagement.subject", subject=subject, page=i)
                                    })
                            while letter == self.get_name(result)[0].lower() and i < len(results["results"]["bindings"]):
                                result = results["results"]["bindings"][i]
                                i = i + 1

                buttons.append(self.button_general_theme)
                dispatcher.utter_message(text=msg, buttons=buttons, json_message={"understand_ckan": self.understand_ckan})
            else:  ## By entity ID
                if subject or len(subject.strip()): #First search if we have some entity
                    subject = self.get_subject(tracker)
                    results = self.get_source_from_entity(subject, sparql_connetion)
                    if results is not None and len(results["results"]["bindings"]) > 0 and len(results["results"]["bindings"][0]) > 0:
                        msg = "De \"" + results["results"]["bindings"][0]['name']['value'] + "\" tengo la siguiente información: \n"
                        url=""
                        r = None
                        if "source" in results["results"]["bindings"][0]:
                            url = results["results"]["bindings"][0]['source']['value']
                        try:
                            r = requests.get(url)
                            resSource = r.json()
                        except Exception:
                            resSource = {}
                        # TODO At the moment it seems that it will never enter the source part of the ei2av2 version.
                        #  Habría que verificar que propiedad funciona como source y revisar esta primera parte del IF
                        if (r is not None and r.status_code == requests.codes.ok) and len(resSource) == 2:
                            for i, prop in enumerate(resSource[0]):
                                if resSource[1][i] and str(resSource[1][i]) != "" and prop not in hidde_props:
                                    msg = msg + prop.capitalize().replace("_", " ") + ": " + str(resSource[1][i]) + "\n"
                        else:  # It has no valid source, first level properties are extracted.
                            results = self.get_property_first_level(subject, sparql_connetion)
                            oldmsg = ""
                            for i, res in enumerate(results["results"]["bindings"]):
                                label = res["property"]["value"].replace("/", "#").split("#")[-1]
                                newmsg = label.capitalize() + ": " + str(res["value"]["value"]) + "\n"
                                if newmsg != oldmsg and str(label).upper() not in hidde_props:
                                    msg = msg + newmsg
                                oldmsg = newmsg
                        # Nearby instances of the same type
                        nearInstances = self.get_near_instances(sparql_connetion, subject)
                        if len(nearInstances["results"]["bindings"]) > 0:
                            msg = msg + "Otros datos cercanos que podrían interesarte:"
                            for i, result in enumerate(nearInstances["results"]["bindings"]):
                                if (result['id']['value'] != subject) and i < 6:
                                    buttons.append(self.button_name(result))
                        # Nearby instances of the same type
                        buttons.extend(self.get_near_subject(subject))

                        buttons.append(self.button_general_theme)

                        dispatcher.utter_message(text=msg, buttons=buttons,json_message={"understand_ckan": self.understand_ckan})
                    else:  ## By entity name. Search in ckan because it hasn't found anything in Open Data

                        evt = search_in_ckan(dispatcher, tracker,self.understand_ckan)

                        if not self.understand_ckan :
                            results = self.get_generals_themes(sparql_connetion, self.get_subject(tracker))

                            regNum = self.getentity(tracker, 'page')
                            if not regNum:
                                regNum = 0
                            else:
                                regNum = int(regNum)
                            if len(results["results"]["bindings"]) > 0:
                                i = 0

                                msg = self.pagination_result_opendata_ei2a(page_size, subject, buttons, results, regNum, i)

                            dispatcher.utter_message(text=msg, buttons=buttons, json_message={"understand_ckan": self.understand_ckan})

                else:
                    evt = search_in_ckan(dispatcher, tracker)

        return evt

    def get_generals_themes(self,  sparql_connetion, subject):
        """ Query to obtain the list of general themes in open data
            Search sub-categories

        Parameters
        ----------
        sparql_connection: Connection to database
        subject: Main category

        Returns
        -------
        json

            List of categories under a specific subject
        """

        query = """
                    PREFIX dc: <http://purl.org/dc/elements/1.1/>

                    SELECT *
                    from <http://opendata.aragon.es/def/ei2av2>
                    WHERE { ?id org:classification ?category .
                           OPTIONAL{ {?id dc:title ?name .}
                                      UNION
                                      {?id <http://schema.org/title> ?name }
                                      UNION
                                      {?id dc:identifier ?name }
                                      UNION
                                      {?id <http://schema.org/identifier> ?name }}
                            FILTER regex (?name,\"""" + replace_accents(subject) + "\", \"i\")}" + \
                          " ORDER BY ?name "

        Log.log_debug(query)
        sparql_connetion.setQuery(query)
        sparql_connetion.setTimeout(60)
        sparql_connetion.setReturnFormat(JSON)
        try:
            return sparql_connetion.query().convert()
        except Exception:
            return None



    def get_source_from_entity(self, subject, sparql):
        """ Query to obtain a list of instances from the same source
            #http://www.w3.org/ns/dcat#accessURL
            #http://www.w3.org/ns/dcat#landingPage
            #http://www.w3.org/1999/02/22-rdf-syntax-ns#resource

        Parameters
        ----------
        subject: Original instance
        sparql: Connection to database

        Returns
        -------
        json

            List of categories under a specific subject
        """

        query = """
                   PREFIX dc: <http://purl.org/dc/elements/1.1/>

                   SELECT DISTINCT ?name ?source
                   from <http://opendata.aragon.es/def/ei2av2>
                   WHERE {{ <{0}> org:classification ?category .
                           OPTIONAL {{ {{<{0}> dc:title ?name}}
                                     UNION
                                     {{<{0}> dc:identifier ?name}}
                                     UNION
                                     {{<{0}> <http://schema.org/identifier> ?name}}}} .
                           <{0}> <http://www.w3.org/ns/org#classification> ?category .
                           OPTIONAL {{ {{ <{0}> <http://www.w3.org/ns/dcat#accessURL> ?source }}
                              UNION
                              {{ <{0}> <http://www.w3.org/ns/dcat#landingPage> ?source }}
                            }}
                          }}
                    ORDER BY ?name
                """
        query = query.format(subject)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        try:
            return sparql.query().convert()
        except Exception:
            return None

    def get_themes_by_locations(self, tracker, subject, sparql):
        """ Given a specific instance, look for another instances located nearby the original one

        Parameters
        ----------
        tracker: information from user interface
        subject: Original instance
        sparql: Connection to database

        Returns
        -------
        json

            List of themes available close to the original instance
        """
        if self.get_entity(tracker, 'loc_id') is not None:
            geo =  "?id org:linkedTo  <{0}>.".format(self.get_entity(tracker, 'loc_id'))
        else:
            geo = ""


        query = """
                   PREFIX dc: <http://purl.org/dc/elements/1.1/>

                   SELECT DISTINCT  ?id  (IF(STRLEN(?name1)>0,?name1,IF(STRLEN(?name2)>0,?name2,IF(STRLEN(?name3)>0,?name3,?name4))) as ?name)
                   from <http://opendata.aragon.es/def/ei2av2>
                   WHERE {{ ?id org:classification ?category .
                    """ + geo + """
                          OPTIONAL {{?id dc:title ?name1 .}}
                          OPTIONAL {{?id <http://schema.org/title> ?name2 .}}
                          OPTIONAL {{?id dc:identifier ?name3 .}}
                           OPTIONAL{{?id <http://schema.org/identifier> ?name4 }}
                           FILTER (strstarts(str(?id), '{0}'))
                          }}
                    ORDER BY ?name
                """

        query = query.format(subject)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()


    def get_theme_first_level(self, subject, sparql):
        """ Get a list of first level topics

        Parameters
        ----------
        subject: Original instance
        sparql: Connection to database

        Returns
        -------
        json

            List of first level topics
        """
        query = """
            SELECT DISTINCT ?subject (count(*) as ?nInstances)
            FROM <http://opendata.aragon.es/def/ei2av2>
            {{
                ?instance <http://www.w3.org/ns/org#classification> <{0}>
                BIND( REPLACE( str(?instance), '\\\\/[^/]*$', '' ) AS ?subject)
            }}
            ORDER BY ?subject
        """
        query = query.format(subject)
        # print(query)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def get_property_first_level(self, subject, sparql):
        """ Get all first-level properties and their values from a instance

        Parameters
        ----------
        subject: Original instance
        sparql: Connection to database

        Returns
        -------
        json

            Map of proveperties and values
        """
        query = """
                SELECT ?property ?value
                FROM <http://opendata.aragon.es/def/ei2av2>
                WHERE {{<{0}> ?property ?value .
                }}
        """
        query = query.format(subject)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    def pagination_result_opendata_ei2a(self, pagsize, subject, buttons, results, regNum, i):
        """ Pagination of results. Distribute the information to show in different pages

        Parameters
        ----------
        pagsize: Size of the list of information to show
        subject: original instance
        buttons: Buttons to show to the user
        results: Results to send to the user
        regNum: Page to show
        i: index

        Returns
        -------
        json

           Output to show in the interface
        """
        msg = "De \"" + subject + "\" tengo la siguiente información:\n"
        for result in results["results"]["bindings"]:
            if i < regNum:
                i = i + 1
                continue
            if i > regNum + pagsize - 1:
                if regNum > 0:
                    buttons.append(
                    {
                        "title": "Mostrar " + str(pagsize) + " registros anteriores",
                        "payload": "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}".format(
                            intencion="engagement.subject", subject=subject,
                            page=regNum - pagsize)
                    })
                buttons.append(
                    {
                        "title": "Mostrar " + str(pagsize) + " registros más",
                        "payload": "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}".format(
                            intencion="engagement.subject", subject=subject,
                            page=regNum + pagsize)
                    })
                break
            tema = f'{result["id"]["value"].split("#")[1]}: {result["name"]["value"]}'
            regsearch = r"\b(" + replace_accents(subject) + r")\b"
            if re.search(regsearch, result['name']['value'], re.IGNORECASE):
                buttons.append(
                {
                    "title": tema,
                    "payload": "/{intencion}{{\"subject_type\": \"{subject}\", \"page\": \"{page}\"}}".format(
                        intencion="engagement.subject", subject=result['id']['value'],
                        page=regNum + pagsize)
                })
                i += 1
        buttons.append(buttons.append(self.button_general_theme))
        self.understand_ckan = False
        return msg
