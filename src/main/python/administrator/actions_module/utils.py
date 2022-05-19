from datetime import datetime
import json
import os
import random
import sys
from typing import Tuple
from actions_module.info_temas import InfoTemas
from actions_module.message import Msgs
from ckan_connector.ckanSearch import CKANSearch
from browser.logger import Log
from itertools import groupby
from operator import itemgetter
import unidecode
import re
from browser.config import Config
from rasa_sdk.events import EventType, FollowupAction, SlotSet, ActiveLoop

from SPARQLWrapper import SPARQLWrapper, JSON

from actions_module.intent_mapping import IntentMapping

#ckan_object = CKANSearch()
ckan_object =  None # load lazzy

from actions_utils import (
    get_duckling_numbers,
)

from browser.browser import Browser

browser = Browser()

intent_mapping = IntentMapping()

intent_theme = {'aragon': [{'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/comarca'},
                               {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/municipio'},
                               {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-cafeteria-restaurante'},
                               {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/poligono-industrial'},

                               ],
                    'citizentsinfo': [#{'intencion': 'engagement.subject', 'subject': 'ayudas alquiler'},
                                      #{'intencion': 'engagement.subject', 'subject': 'alquileres'},
                                      #{'intencion': 'engagement.subject', 'subject': 'negocios'},
                                      {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/kos/oficina-consumidor'},
                                      #{'intencion': 'engagement.subject', 'subject': 'colegios profesionales'},
                                      #{'intencion': 'engagement.subject', 'subject': 'asociaciones comerciales'}
                                      ],
                    'engagement': [{'intencion': 'engagement.subject', 'subject': 'http://datos.gob.es/kos/sector-publico/sector/cultura-ocio'}],
                    #'farming': [{'intencion': 'engagement.subject', 'subject': 'pozo'},
                    #            #{'intencion': 'engagement.subject', 'subject': 'boca_de_riego'}
                    #            ],
                    'gda': [#{'intencion': 'engagement.subject', 'subject': 'Ley y justicia'},
                            #{'intencion': 'engagement.subject', 'subject': 'Derechos civiles'},
                            {'intencion': 'engagement.subject', 'subject': 'http://datos.gob.es/kos/sector-publico/sector/salud'},
                            #{'intencion': 'engagement.subject', 'subject': 'investigacion'},
                            {'intencion': 'engagement.subject', 'subject': 'http://datos.gob.es/kos/sector-publico/sector/ciencia-tecnologia'}],
                    'tourism': [{'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-punto-informacion-turistica'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-empresas-turismo-activo'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamiento-hotelero'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-camping-turistico'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/turismo/organizacion/registro-apartamento-turistico'},
                                #{'intencion': 'engagement.subject', 'subject': 'sendero'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-oficina-turismo'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-cafeteria-restaurante'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-albergue-refugio'},
                                {'intencion': 'engagement.subject', 'subject': 'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-guia-turismo'},
                                #{'intencion': 'engagement.subject', 'subject': 'alogamiento_hotelero'},
                                #{'intencion': 'engagement.subject', 'subject': 'apartamento'},
                                #{'intencion': 'engagement.subject', 'subject': 'albergue_refugio'},
                                #{'intencion': 'engagement.subject', 'subject': 'camping'},
                                ],
                    'transport': [{'intencion': 'engagement.subject', 'subject': 'transporte_parada'},
                                  {'intencion': 'engagement.subject', 'subject': 'transporte_ruta'}]
                    }

def getYear(message):
    numbers = get_duckling_numbers(message)
    try:
        return str(numbers[0]) if numbers != [] else str(datetime.now().year - 1)
    except Exception as e:
        return str(datetime.now().year - 1)


def getYearValuePerDefect(message, valuePerDefect):
    numbers = get_duckling_numbers(message)
    try:
        return str(numbers[0]) if numbers != [] else valuePerDefect
    except Exception as e:
        return valuePerDefect


def getOriginValue(text):
    return text.replace(".", "").replace(",", "")


def getCorrectRegister(lista, location):
    words = location.split(' ')
    number_words = len(words)
    element_return = []
    for row in lista:
        length_find = sum(word in row['etiqueta'] for word in words)
        if length_find == number_words:
            element_return.append(row)
            break
    return element_return


def eliminaTildes(text):
    text = text.replace('Á', 'A')
    text = text.replace('É', 'E')
    text = text.replace('Í', 'I')
    text = text.replace('Ó', 'O')
    text = text.replace('Ú', 'U')
    return text

def strategy3(question: str, complete_question=True, bert_distance=True):
    """Strategy 3 execution

        Parameters
        ----------
        question: string
            User's question

        complete_question: bool
            Search by bert use the complete question or not

        bert_distance: bool
            Determine if bert_distance is used to select the most proper answer

        Returns
        -------
        str
            Returns the most proper answer from tasks
        list
            List of tags relate to the first result
        """

    Log.log_debug("**strategy3. Estrategy 3 **")
    Log.log_debug(" * question: {0}".format(question))

    # Find the most (5) suitable answer by tag
    global ckan_object
    if ckan_object is None:
        ckan_object = CKANSearch()
    resultsCkan = ckan_object.question_by_tags(question, complete_question, bert_distance)
    message_title = None
    tag_list = []
    # Results evaluations. Search the year and province (Zaragoza, Huesca, Teruel) ir order to activate
    # a form
    form, resource_title = resultsEvaluation(resultsCkan)# return  form and title or resource to filter

    if resultsCkan is not None and len(resultsCkan) > 0:
        message_title, tag_list = composeAnswer(resultsCkan)

    return resultsCkan, message_title, tag_list, form, resource_title

def composeAnswer(resultsCkan):
    first_result = resultsCkan[0]
    tag_list = first_result["tags"]
    url_package = first_result["opendata_url"]

    message_title = f'🗨 He encontrado en Aragón Open Data 🔎 <b> {first_result["title"] } \
                    </b> y te ofrece los siguientes datos:\n'
    resources = first_result["resources"]
    if resources is not None and len(resources) > 0:
        resources_sorted = sorted(resources, key=itemgetter('name'))

        count=0
        # TODO. Pendiente paginar los recursos. ¿Cómo lo hacemos?
        group=groupby(resources_sorted, key=itemgetter('name'))

        for key, value in group:
            count += 1
            #si hay más de 5 resultados metosmo un div oculto y un boton para mostrarlo
            if count==5:
                message_title += "\n<button  class='btn btn-success col-12 col-lg-auto fallback_more' style='margin: 2px; padding-top: 0.175rem; padding-right: 0.75rem; padding-bottom: 0.275rem; padding-left: 0.75rem; background-color: #1a5b9c'  onclick =\"this.nextSibling.style.display='block';this.style.display='none'\" >Ver todos los resultados< / button >"
                message_title += "<div style=\"padding-top:0;display:none\">"
            message_title += '\n\t💡 ' + key.replace(':',' ') + " \t"
            for k in value:
                url = k["url"]
                # message_title += k["format"] + f" ({url})\t"
                # message_title +="<a href='"+url+"' target='_blank'>" + k["format"] +"</a>\t"
                message_title += "<a href=\"{0}\" target='_blank'>{1}</a>  ".format(unidecode.unidecode(url), k["format"])
        if count >= 5:
            message_title += "</div>"

    # message_title += f"\n\n\t- " + f" Seleccione {url_package} para ver más información\n"
    message_title += (
        '\n\nEstos datos fueron publicados por el/la <b>'
        + first_result["organization"]["title"]
        + "</b>"
    )

    # TODO Falta poner el mensaje de Frequency
    extra_list = first_result["extras"]
    res = next((sub for sub in extra_list if sub['key'] == "Frequency"), None)
    # Si existe el mensaje de Frequency
    if res is not None and res.get('value'):
        message_title += ' y su actualización es <b>' + res.get('value') + "</b>"
    message_title += ", si quieres conocer más información de estos recursos accede a "
    message_title += "<a href='" + url_package + "' target='_blank'>" + "Aragón Open Data " + "</a>\t\n"
    print(message_title)
    if len(resultsCkan) > 1:
        message_title += '\n🗨 Y además, también he encontrado en Aragón Open Data más recursos relacionados: \n'
        for result in resultsCkan:
            url_package = result["opendata_url"]
            # message_title += f"\n\t💡 " + package["title"] + f". Seleccione el {url_package}"
            message_title += (
                '\n\t💡 '
                + "<a href='"
                + url_package
                + "' target='_blank'>"
                + result["title"].replace(':', ' -')
                + "</a>"
            )
    message_title += '\n\n🗨 Espero que te haya parecido interesante la respuesta. ¡también me puedes seguir preguntando!'
    return message_title, tag_list

def resultsEvaluation(resultsCkan:list):
    """
        Results evaluation from Strategy 3

        Parameters
        ----------
        resultsCkan: list
            Different answers searched in CKAN

        Returns
        -------
        list
            List of tags relate to the first result
    """

    Log.log_debug("**Strategy 3. Results Evaluation **")
    bYearGlobal = False
    bProvGlobal = False
    resource_title = None
    if resultsCkan is not None and resultsCkan:
        #Evaluate text from different results
        if len(resultsCkan) > 1:
            for result in resultsCkan:
                bYearGlobal = any( [bYearGlobal, analyzeYearExpression( result["title"])])
                bProvGlobal = any( [bProvGlobal , analyzeProvinceExpression( result["title"])])
            if bYearGlobal or bProvGlobal:
                resource_title="title"

        # Depending of evaluation expressions a specific form will be launched
        if not(bYearGlobal) and not(bProvGlobal):
            #If both expressions are false, evaluate resources from the first result
            # Resources evaluation
            result = resultsCkan[0]
            for resource in result["resources"]:
                bYearGlobal = any( [bYearGlobal, analyzeYearExpression( resource["description"])])
                bProvGlobal = any( [bProvGlobal , analyzeProvinceExpression( resource["description"])])
            if bYearGlobal or bProvGlobal:
                resource_title="resource"

        #TODO How to send the answer in a slot ???
        #TODO How to choose the proper answer from result or from resources
        if bYearGlobal and bProvGlobal:
            return "timePlace_form", resource_title #Launch time and place form
        elif bYearGlobal:
            return "time_form", resource_title #Launch time form
        elif bProvGlobal:
            return "place_form", resource_title #Launch place form
    #Any Other case, proceed with standar answer
    return None, None

def analyzeYearExpression(title:str) -> (bool):
    """
       Analyze if there is a year inside a title

        Parameters
        ----------
        title: str
            Text to Evaluate

        Returns
        -------
        bool:
            true if a year expression has been found

    """

    #"^(19|20)\d{2}$"

    return re.search("(19|20)\d{2}", title) is not None

def analyzeProvinceExpression(title:str) -> (bool):
    """
       Analyze if there is a province name inside a title

        Parameters
        ----------
        title: str
            Text to Evaluate

        Returns
        -------
        bool:
            true if a province name (Zaragoza, Huesca o Teruel) expression has been found

    """
    return re.search("(zaragoza|huesca|teruel)", title.lower()) is not None

def select_buttons_strategy3( tag_list, tracker):
    buttons = []

    # Recoge el texto que se ha devuelto en la estrategia 3. message title
    # Explora los tags para identificar intenciones relacionadas
    if tag_list is not None and len(tag_list) > 0:
        # Extrae el listado de tags y lo pasa todo a minuscula
        tag_list_lw = list(map(str.lower, tag_list))
        if 'ei2a' in tag_list_lw:
            # Revisa todos los tags para poder iniciar la búsqueda de intenciones
            button_list = intent_mapping.get_intent_mappings().button  # Carga las posibles preguntas (botones)
            # Recorre elemento a elemento la lista de tags
            tag_list_lw = list(filter(lambda x: x not in [
                'ei2a',
                'municipio',
                'aragón',
                'registro' ], tag_list_lw))# Borra de la lista la etiqueta ei2a, municipio, registro, aragón

            # Selecciona todas aquellas intenciones que en la pregunta
            # tienen alguna etiqueta de las listadas
            selected_intents = intent_mapping.get_intent_mappings()[
                    button_list.str.contains("|".join(tag_list_lw), na=False, flags=re.IGNORECASE,
                                                regex=True)].intent.tolist()
            # Si no tiene una entidad de tipo location, entonces selecciona aleatoriamente
            # una de las 3 capitales de provincia
            entities = tracker.latest_message.get("entities", [])
            entities = {e["entity"]: e["value"] for e in entities}
            if not entities or 'location' not in entities.keys():
                entities["location"] = random.choice(['Zaragoza', 'Huesca', 'Teruel'])

            if selected_intents is not None and len(selected_intents) > 0:
                # Busca los botones para cada una de las intenciones seleccionadas
                entities_json = json.dumps(entities)
                for intent in selected_intents:
                    try:
                        btntitle = intent_mapping.get_button_title(intent, entities)
                        if "{" not in btntitle:
                            buttons.append(
                                {
                                    "title": btntitle,
                                    "payload": "/{}{}".format(intent, entities_json),
                                }
                            )
                    except:
                        pass
        return buttons
    else:
        # Si la estrategia 3 no devuelve ningún tags muestra el botón de ver todos los temas
        buttons.append(
            {
                "title": "Ver todos los temas",
                "payload": "/greetings.hello",
            })
    return buttons

def getIDMunicipio( nombreMunicipio):
    sparql = SPARQLWrapper(Config.bbdd_url())
    query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
            PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>


        select ?idMunicipio
        from <http://opendata.aragon.es/def/ei2a>
        where {{
                ?idMunicipio dc:type ei2a:municipio .
                ?idMunicipio ei2a:organizationName "{0}" .
                }}
        """
    query = query.format(str(nombreMunicipio).upper())
    Log.log_debug(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if len(results["results"]["bindings"]) > 0:
        return results["results"]["bindings"][0]['idMunicipio']['value']
    else:
        return ''

def getSubjectByIdMunicipio( idMunicipio):
    sparql = SPARQLWrapper(Config.bbdd_url())
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
        PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
        PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>

        SELECT    ?id ?id_location ?locName (COUNT(*) as ?nInstances)
        from <http://opendata.aragon.es/def/ei2a>
        WHERE {{  <{0}> geo:location ?id_location .
                <{0}> dc:type ?instance_type .
                ?instance ?relation ?id_location .
                ?id_location ei2a:organizationName ?locName .
                ?instance dc:type ?id.
                FILTER (?id_location = <{0}>)
                }}
        GROUP BY  ?id ?id_location ?locName
        ORDER BY  ?id ?locName
        """
    query = query.format(idMunicipio)
    print(query)
    Log.log_debug(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if len(results["results"]["bindings"]) > 0:
        return results["results"]["bindings"]
    else:
        return None

def no_results(tracker,dispatcher):
    sugg = Msgs.get_suggestion(tracker.latest_message['text'])
    if sugg == "":
        dispatcher.utter_message(text=Msgs.dont_understand[random.randrange(len(Msgs.dont_understand))],json_message={"understand_ckan": False})
    else:
        dispatcher.utter_message(text=sugg,json_message={"understand_ckan": False})

def set_buttons_title_no_ckan_answer( tracker):
    intent_ranking = list(filter( lambda x : x["name"] not in ["nlu_fallback", "time", "place"], tracker.latest_message.get("intent_ranking", [])))
    try:
        intent_names = intent_theme[intent_ranking[0]['name'].split('.')[0]]
    except:
        pass

    valid_intents = []
    # elegir un criterio por ejemplo que la diferencia con la conficence del primer intent sea mayor
    # que lo que se quiera, que el valor de confidenc sea mayor a  o cuaqluier otro criterio
    if len(intent_ranking) > 1:
        valid_intents.append(intent_ranking[0])
        valid_intents.extend(
            intent
            for intent in intent_ranking[1:]
            if intent.get("confidence") > 0.05
        )

    first_intent_names = [
        intent.get("name", "")
        for intent in valid_intents
        if not str(intent.get("name", "")).startswith("user") and not str(intent.get("name", "")).startswith(
            "agent") and not str(intent.get("name", "")).startswith("weather") and not str(
            intent.get("name", "")).startswith("greetings")  # filtrar los intent que queramos
    ]

    message_title = "Perdona, no te he entendido correctamente, elije una opcion si esta lo que querías decirme o reformula la pregunta: "


    entities = tracker.latest_message.get("entities", [])
    entities = {e["entity"]: e["value"] for e in entities}

    buttons = generate_buttons_by_entity(first_intent_names, entities)


    if 'location' in entities:  # Identificado un municipio -> entidades de ese municipio del MC
        idLocation = getIDMunicipio(entities['location'])
        if idLocation != '':
            temas_por_muncicipio = getSubjectByIdMunicipio(idLocation)
            if temas_por_muncicipio is not None:
                for tema_por_municipio in temas_por_muncicipio:
                    nomTema = tema_por_municipio['id']['value'].split("#")[1]
                    if any(obj['subject'] == nomTema for obj in
                            intent_names):  # Solo saco los del mismo MC en el que estoy
                        if nomTema in InfoTemas.themeDescription:
                            nomTema = InfoTemas.themeDescription[nomTema][1]
                        if nomTema != "-":
                            buttons.append( {
                                "title": f"{nomTema.capitalize() } en {tema_por_municipio['locName']['value'] } ( {tema_por_municipio['nInstances']['value']})",
                                "payload": "/{intencion}{{\"subject_type\": \"{subject}\",\"loc_id\": \"{loc_id}\"}}".format(
                                    intencion="engagement.subject",
                                    subject=tema_por_municipio['id']['value'],
                                    loc_id=tema_por_municipio['id_location']['value'])
                            })
    if buttons == []:
        sugg = Msgs.get_suggestion(tracker.latest_message['text'])
        if sugg == "":
            message_title = Msgs.dont_understand[random.randrange(len(Msgs.dont_understand))]
        else:
            message_title = sugg

    buttons.append(
        {
            "title": "Ver todos los temas",
            "payload": "/greetings.hello",
        })

    return message_title, buttons

def generate_buttons_by_entity(first_intent_names, entities):


    entities_json = json.dumps(entities)

    buttons = []

    for intent in first_intent_names:
        try:
            btntitle, _  = intent_mapping.get_button_title(intent, entities)#(intent, entities)
            if (
                btntitle
                and "{" not in btntitle
                and str(btntitle).lower() != intent
                ):
                buttons.append({"title": btntitle, "payload": f"/{intent}{entities_json}"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    return buttons


def search_in_ckan( dispatcher, tracker, understand_ckan=False):
    # get the most likely intent
    try:
        # Llama a la estrategia 3.1 Búsqueda por tags y bert
        question = tracker.latest_message.get("text")
        results_ckan, message_title ,tag_list ,form ,resource_title  = strategy3(question, True, True)
        evt = [SlotSet("results", results_ckan), SlotSet("resource_title", resource_title)]


        buttons = []
        #print("Form::: ", form)
        if form:
            evt.append(FollowupAction(form)) #Llamamos al formulario desde la accion
        else:
            # si entra en la intencion de time y no estan activado el formulario de
            #if (tracker.active_loop.get("name"))
            intent = tracker.latest_message.get("intent", [])# si no esta activado el formulario descarta la intencion de time y place
            if  intent.get("name") in ["time", "place"]:
                evt.extend([
                    SlotSet("place", None),
                    SlotSet("time", None),
                    SlotSet("results", None),
                    SlotSet("resource_title", None),
                    FollowupAction("action_listen")])
            #evt.append(SlotSet("time", None), SlotSet("place", None),FollowupAction("action_listen")) #Llamamos al formulario desde la accion
            if not message_title:
                # No ha obtenido ningún resultado, por lo que utiliza la aproximación por intenciones y entidades
                # recibidas en el tracker
                understand_ckan = False
                message_title, buttons  = set_buttons_title_no_ckan_answer(tracker)
                #return [] si devolvemos una lista vacia, el bot no responde al usuario
            else:
                # Recoge el texto que se ha devuelto en la estrategia 3. message title
                # Explora los tags para identificar intenciones relacionadas
                understand_ckan = "ckan"
                buttons = select_buttons_strategy3( tag_list, tracker)
            dispatcher.utter_message(text=message_title, buttons=buttons , json_message={"understand_ckan": understand_ckan})
        return evt

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        no_results(tracker, dispatcher)