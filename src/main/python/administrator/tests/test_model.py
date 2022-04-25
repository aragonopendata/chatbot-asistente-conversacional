'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from logging import error
import unittest

import config
import mongo_connector.config as config_mongo
import asyncio
import os

from rasa.shared.constants import DEFAULT_MODELS_PATH
from rasa.core.agent import Agent
from rasa.model import get_latest_model
from rasa.utils.endpoints import EndpointConfig

"""
    Class for testing the model file.

    ask to database mongodb for last interaction and compare with the last interaction in the model file.
"""
@unittest.skip("skip")
class Test_Model(unittest.TestCase):

    project = "GDA"
    model = "AOD"
    action_endpoint = EndpointConfig(url=config.ACTION_URL_ENDPOINT)
    agent_path = os.path.join(
        os.getcwd() , DEFAULT_MODELS_PATH, project, model
    )
    agent = Agent.load( get_latest_model(agent_path), action_endpoint=action_endpoint)

    """test with a question and compare with intent of model
    """
    def test_intents_major(self):

        user_input="quien es el alcalde de zaragoza"

        info = asyncio.get_event_loop().run_until_complete( self.agent.interpreter.parse(user_input))
        assert (info["intent"]["name"] == "aragon.city_hall_major")
        assert (info["entities"][0]["entity"] == "location")
        assert (info["entities"][0]["value"] == "zaragoza")

    """ format
    """
    def test_intents_generic(self):
        data = [{"user_input":"quiero un albañil barato", "intent_name": "nlu_fallback" },{
            "user_input" : "Cuáles son las causas de las incidencias de tráfico de la localidad Huesca?",
            "intent_name" : "transport.issue_reasons" }]

        for data_item in data:
            print (data_item)
            self.generic(**data_item)

    def test_intents(self):
        self.evaluate_from_marco(marco="tourism")
        #self.evaluate_from_marco(marco="aragon")
        #self.evaluate_from_marco(marco="farming")
        #self.evaluate_from_marco(marco="transport")
        #self.evaluate_from_marco(marco="citizensinfo")

    def evaluate_from_marco(self, marco):
        collection = config_mongo.SESSIONS_COLL

        mongo_results = collection.aggregate([{ "$unwind" : "$interactions" },{
            "$project": {"interactions.intent_name": "$interactions.intent", "interactions.user_input": "$interactions.input_user"}  },{
            "$match": {"interactions.user_input": {"$regex": "^[^\/]" } }} ,   {
            "$match": {"interactions.intent_name":  {"$regex": "^tourism" }}},{
            "$group":{ "_id":"null" , "interaction": { "$addToSet":    "$interactions"  }}}
            ])
        mongo_results = list(mongo_results)
        if (len(list(mongo_results)) == 0):
            print(f"No hay ninguna interacción para el marco: {marco}")
        results = {}
        count=0
        errors=0
        print(f"Análisis del marco de conversacion de {marco}")
        for data_item in mongo_results[0].get("interaction"):
            #print (data_item)
            info , intent_name = self.generic_intents(**data_item)
            #print (data_item ,intent_name )
            predict = info["intent"]["name"]
            count=count+1
            if (predict != intent_name):
                results.update({predict: { "values":results.get(predict, 0) + 1}})
                predict_key = results.get(predict)
                if "intents" in predict_key.keys():
                    predict_key.get("intents").append(intent_name)
                else:
                    predict_key["intents"]= [intent_name]
                predict_key["intents"] = set(predict_key["intents"])
                errors=errors+1
                print (data_item , predict )

        print (f"numero de intenciones {results}")
        print (f"count {count} errors {errors}")
        print(f"######\nfin del análisis del marco de conversacion de  {marco}")


    def test_intents_fallback(self):

        self.generic("quiero un albañil barato", "nlu_fallback")


    def generic(self, user_input, intent_name):

        info = asyncio.get_event_loop().run_until_complete( self.agent.interpreter.parse(user_input))
        assert (info["intent"]["name"] == intent_name)

    def generic_intents(self, user_input, intent_name):

        return asyncio.get_event_loop().run_until_complete( self.agent.interpreter.parse(user_input)), intent_name

