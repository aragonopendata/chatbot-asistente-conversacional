'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import json
import unicodedata
from random import randrange

from rasa_sdk import Action
import sys
from browser.config import Config
from SPARQLWrapper import SPARQLWrapper, JSON
from browser.logger import Log
from actions_module.navigation import InfoTemas


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


class Msgs:
    dontunderstand = ["Perdona, tengo problemas para responder la pregunta, reformula la pregunta", "Lo siento, pero no te he entendido ¿Puedes escribir la pregunta de otra forma?",
                      "Perdón, pero no he entendido bien lo que me quieres preguntar. ¿Puedes preguntarlo de otra forma?", "Creo que no te he entendido bien, lo siento, pregúntamelo de otra forma."]

    @staticmethod
    def getSuggestion(userQuestion):
        with open('data/suggestions.json', encoding="utf-8") as json_file:
            suggestions = json.load(json_file)
        for word in userQuestion.split():
            for sugg in suggestions:
                if strip_accents(word.lower()) in sugg['key']:
                    return sugg['suggestion']
        return ""


class Action_Generic(Action):
    intent_thema = {'aragon': [{'intencion': 'engagement.subject', 'subject': 'comarca'},
                               {'intencion': 'engagement.subject', 'subject': 'municipio'},
                               {'intencion': 'engagement.subject', 'subject': 'cafeteria_restaurante'},
                               {'intencion': 'engagement.subject', 'subject': 'iaf_poligono_industrial'},

                               ],
                    'citizentsinfo': [{'intencion': 'engagement.subject', 'subject': 'ayudas alquiler'},
                                      {'intencion': 'engagement.subject', 'subject': 'alquileres'},
                                      {'intencion': 'engagement.subject', 'subject': 'negocios'},
                                      {'intencion': 'engagement.subject', 'subject': 'informacion de consumo'},
                                      {'intencion': 'engagement.subject', 'subject': 'colegios profesionales'},
                                      {'intencion': 'engagement.subject', 'subject': 'asociaciones comerciales'}
                                      ],
                    'engagement': [{'intencion': 'engagement.subject', 'subject': 'Cultura'}],
                    'farming': [{'intencion': 'engagement.subject', 'subject': 'pozo'},
                                {'intencion': 'engagement.subject', 'subject': 'boca_de_riego'}],
                    'gda': [{'intencion': 'engagement.subject', 'subject': 'Ley y justicia'},
                            {'intencion': 'engagement.subject', 'subject': 'Derechos civiles'},
                            {'intencion': 'engagement.subject', 'subject': 'Salud'},
                            {'intencion': 'engagement.subject', 'subject': 'investigacion'},
                            {'intencion': 'engagement.subject', 'subject': 'Aguas'}],
                    'tourism': [{'intencion': 'engagement.subject', 'subject': 'punto_informacion_turistica'},
                                {'intencion': 'engagement.subject', 'subject': 'empresa_turismo_activo'},
                                {'intencion': 'engagement.subject', 'subject': 'alojamiento_hotelero'},
                                {'intencion': 'engagement.subject', 'subject': 'camping_turistico'},
                                {'intencion': 'engagement.subject', 'subject': 'apartamento_turistico'},
                                {'intencion': 'engagement.subject', 'subject': 'sendero'},
                                {'intencion': 'engagement.subject', 'subject': 'alojamiento_rural'},
                                {'intencion': 'engagement.subject', 'subject': 'oficina_turismo'},
                                {'intencion': 'engagement.subject', 'subject': 'cafeteria_restaurante'},
                                {'intencion': 'engagement.subject', 'subject': 'albergue_refugio'},
                                {'intencion': 'engagement.subject', 'subject': 'guia_turismo'},
                                {'intencion': 'engagement.subject', 'subject': 'alogamiento_hotelero'},
                                {'intencion': 'engagement.subject', 'subject': 'apartamento'},
                                {'intencion': 'engagement.subject', 'subject': 'albergue_refugio'},
                                {'intencion': 'engagement.subject', 'subject': 'camping'},
                                ],
                    'transport': [{'intencion': 'engagement.subject', 'subject': 'transporte_parada'},
                                  {'intencion': 'engagement.subject', 'subject': 'transporte_ruta'}]
                    }

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv("data/intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(";")}
        )

    def name(self):
        return "Action_Generic"

    def run(self, dispatcher, tracker, domain):
        # get the most likely intent
        try:
            intent_ranking = tracker.latest_message.get("intent_ranking", [])
            intent_name_sugery = intent_ranking[0]['name'].split('_')[0]  # solo sugiere las del mismo marco tourims.grastronomy
            iSintent_name_list = '_list' in intent_ranking[0]['name']  # solo sugiere las del mismo marco tourims.grastronomy

            try:
                intent_names = self.intent_thema[intent_ranking[0]['name'].split('.')[0]]
            except:
                pass
            if not iSintent_name_list:
                first_intent_names = list(
                    filter(lambda _: _.startswith(intent_name_sugery) and ("_list" not in _ and "number" not in _) and not _.startswith(('user', 'agent', 'greetings', 'weather', 'engagement')),
                           map(lambda _: _['name'], intent_ranking)))[1:4]
            else:
                first_intent_names = list(
                    filter(lambda _: ("_list" in _ or "number" in _) and not _.startswith(('user', 'agent', 'greetings', 'weather', 'engagement')),
                           map(lambda _: _['name'], intent_ranking)))[1:4]

            entities = tracker.latest_message.get("entities", [])
            entities = {e["entity"]: e["value"] for e in entities}
            entities_json = json.dumps(entities)

            buttons = []
            messages = []
            for intent in first_intent_names:
                try:
                    btntitle, message = self.get_button_title(intent, entities)
                    if btntitle and not ("{" in btntitle) and str(btntitle).lower() != intent:
                        buttons.append(
                            {
                                "title": btntitle,
                                "payload": "/{}{}".format(intent, entities_json),
                            }
                        )
                except:
                    pass

            # if buttons == []:
            #    message_title = "Perdona no entiendo lo que me pides, reformula la pregunta."
            '''
            buttons.append(
                {
                    "title": "Ver mas preguntas de este tema",
                    "payload": "/{}".format(intent_name),
                })
            '''

            temasbyMuncicipio = None
            if 'location' in entities:  # Identificado un municipio -> entidades de ese municipio del MC
                idLocation = self.getIDMunicipio(entities['location'])
                if idLocation != '':
                    temasbyMuncicipio = self.getSubjectByIdMunicipio(idLocation)
                if temasbyMuncicipio is not None:
                    for i, result in enumerate(temasbyMuncicipio):
                        nomTema = result['id']['value'].split("#")[1]
                        if any(obj['subject'] == nomTema for obj in intent_names):  # Solo saco los del mismo MC en el que estoy
                            if nomTema in InfoTemas.descTema:
                                nomTema = InfoTemas.descTema[nomTema][1]
                            if nomTema != "-":
                                button = {
                                    "title": nomTema.capitalize() + " en " + result['locName']['value'] + " (" + str(result['nInstances']['value']) + ")",
                                    "payload": "/{intencion}{{\"subject_type\": \"{subject}\",\"loc_id\": \"{loc_id}\"}}".format(intencion="engagement.subject", subject=result['id']['value'],
                                                                                                                                 loc_id=result['id_location']['value'])
                                }
                                buttons.append(button)
            if len(buttons) <= 2:  # No identificado el municipio -> entidades genéricas del MC
                for intent_name in intent_names:
                    temaDesc = intent_name['subject'].replace("_", " ")
                    buttons.append(
                        {
                            "title": temaDesc.capitalize(),
                            "payload": "/{intencion}{{\"subject_type\": \"{subject}\"}}".format(
                                intencion='engagement.subject', subject=intent_name['subject'])
                        })

            dispatcher.utter_message(buttons=buttons)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sugg = Msgs.getSuggestion(tracker.latest_message['text'])
            if sugg == "":
                dispatcher.utter_message(text=Msgs.dontunderstand[randrange(len(Msgs.dontunderstand))])
            else:
                dispatcher.utter_message(text=sugg)
        return []

    def getIDMunicipio(self, nombreMunicipio):
        sparql = SPARQLWrapper(Config.bbdd_url())
        query = """
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
             PREFIX dc: <http://purl.org/dc/elements/1.1/>
             PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
             PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
            
            
            select ?idMunicipio
            where {{
                    ?idMunicipio dc:type ei2a:municipio .
                    ?idMunicipio ei2a:organizationName "{0}" .
                   }}
            """
        query = query.format(str(nombreMunicipio).upper())
        print(query)
        Log.log_debug(query)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            return results["results"]["bindings"][0]['idMunicipio']['value']
        else:
            return ''

    def getSubjectByIdMunicipio(self, idMunicipio):
        sparql = SPARQLWrapper(Config.bbdd_url())
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#>
            PREFIX webCategory: <http://opendata.aragon.es/def/ei2a/categorization#>
            PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            
            SELECT    ?id ?id_location ?locName (COUNT(*) as ?nInstances)
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

    def get_button_title(self, intent, entities) -> str:

        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (self.intent_mappings.entities == entities.keys()) & (
            default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent
        message = ""
        if 'location' not in entities:
            entities = {'location': '...'}
            btntitle = button_title.format(**entities)
            message = btntitle[0].upper() + btntitle[1:]
            return None, message
        else:
            btntitle = button_title.format(**entities)
            return btntitle[0].upper() + btntitle[1:], ""


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self):
        return "action_fallback_ita"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv("data/intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(";")}
        )

    def run(self, dispatcher, tracker, domain):
        # get the most likely intent
        try:
            intent_ranking = tracker.latest_message.get("intent_ranking", [])
            try:

                intent_names = Action_Generic.intent_thema[intent_ranking[0]['name'].split('.')[0]]
            except:
                pass
            print(intent_ranking)
            valid_intents = []
            # elegir un criterio por ejemplo que la diferencia con la conficence del primer intent sea mayor que loque se quiera, que el valor de confidenc sea mayor a  o cuaqluier otro criterio
            if len(intent_ranking) > 1:
                valid_intents.append(intent_ranking[0])
                for intent in intent_ranking[1:]:
                    if intent.get("confidence") > 0.05:
                        valid_intents.append(intent)
                    # diff_intent_confidence = intent_ranking[0].get("confidence") - intent.get("confidence")
                    # if diff_intent_confidence < 0.01:
                    #   valid_intents.append(intent)

            first_intent_names = [
                intent.get("name", "")
                for intent in valid_intents
                if not str(intent.get("name", "")).startswith("user") and not str(intent.get("name", "")).startswith(
                    "agent") and not str(intent.get("name", "")).startswith("weather") and not str(
                    intent.get("name", "")).startswith("greetings")  # filtrar los intends que queramos
            ]
            print(first_intent_names)
            message_title = "Perdona, no te he entendido correctamente, elije una opcion si esta lo que querías decirme o reformula la pregunta: "

            entities = tracker.latest_message.get("entities", [])
            entities = {e["entity"]: e["value"] for e in entities}
            print(entities)
            entities_json = json.dumps(entities)

            buttons = []

            for intent in first_intent_names:
                # message_title +="\n"+self.get_button_title(intent, entities)

                # message_title+="\n"+self.get_button_title(intent, entities)+"  #  "+"/{}{}".format(intent, entities_json)
                try:
                    btntitle = self.get_button_title(intent, entities)
                    if not ("{" in btntitle):
                        buttons.append(
                            {
                                "title": btntitle,
                                "payload": "/{}{}".format(intent, entities_json),
                            }
                        )
                except:
                    pass

            idlocation = ''
            ag = Action_Generic()
            if 'location' in entities:  # Identificado un municipio -> entidades de ese municipio del MC
                idLocation = ag.getIDMunicipio(entities['location'])
                if idLocation != '':
                    temasbyMuncicipio = ag.getSubjectByIdMunicipio(idLocation)
                if temasbyMuncicipio is not None:
                    for i, result in enumerate(temasbyMuncicipio):
                        nomTema = result['id']['value'].split("#")[1]
                        if any(obj['subject'] == nomTema for obj in intent_names):  # Solo saco los del mismo MC en el que estoy
                            if nomTema in InfoTemas.descTema:
                                nomTema = InfoTemas.descTema[nomTema][1]
                            if nomTema != "-":
                                button = {
                                    "title": nomTema.capitalize() + " en " + result['locName']['value'] + " (" + str(result['nInstances']['value']) + ")",
                                    "payload": "/{intencion}{{\"subject_type\": \"{subject}\",\"loc_id\": \"{loc_id}\"}}".format(intencion="engagement.subject", subject=result['id']['value'],
                                                                                                                                 loc_id=result['id_location']['value'])
                                }
                                buttons.append(button)
            if buttons == []:
                sugg = Msgs.getSuggestion(tracker.latest_message['text'])
                if sugg == "":
                    message_title = Msgs.dontunderstand[randrange(len(Msgs.dontunderstand))]
                else:
                    message_title = sugg

            buttons.append(
                {
                    "title": "Ver todos los temas",
                    "payload": "/greetings.hello",
                })
            dispatcher.utter_message(text=message_title, buttons=buttons)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sugg = Msgs.getSuggestion(tracker.latest_message['text'])
            if sugg == "":
                dispatcher.utter_message(text=Msgs.dontunderstand[randrange(len(Msgs.dontunderstand))])
            else:
                dispatcher.utter_message(text=sugg)

        return []

    def get_button_title(self, intent, entities):

        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (self.intent_mappings.entities == entities.keys()) & (
            default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        print(utterances)
        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent

        btntitle = button_title.format(**entities)
        return btntitle[0].upper() + btntitle[1:]
