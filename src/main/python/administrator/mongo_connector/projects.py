"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from datetime import datetime

from rasa.core.agent import Agent
from rasa.model import get_latest_model
from typing import List, Dict, Any

from utils import json
import os
import shutil

from constants import MODEL_PATH, TRAINING_DATA_DIR

from bson.objectid import ObjectId
from bson import json_util as json_mongo
from mongo_connector.config import (
    PROJECTS_COLL,
    MODELS_COLL,
    ENTITIES_COLL,
    INTENTS_COLL,
    INTERACTIONS_COLL,
    STORIES_COLL,
    TEMPLATES_COLL,
    VALUES_COLL,
)


###################
## CRUD PROJECTS ##
###################
def download_training_project():

    """ It downloads the training model """    

    shutil.make_archive("model", 'zip', TRAINING_DATA_DIR)
    
    
  
def create(project_list: List[str]):
    """
    Create a list of projects
    :param project_list: list
    :return:
    """
    for name in project_list:
        data = {"name": name}
        PROJECTS_COLL.update_one(data, {"$set": {"name": name}}, upsert=True)


def read() -> List[Dict[str, Any]]:
    """
    Read project data from database
    :return: project data
    """
    pipeline = [
        {
            "$lookup": {
                "from": "models",
                "localField": "_id",
                "foreignField": "project_id",
                "as": "models",
            }
        },
        {"$project": {"name": 1, "models_length": {"$size": "$models"}}},
    ]

    return json.objectid_to_id(
        json.loads(json_mongo.dumps(PROJECTS_COLL.aggregate(pipeline)))
    )


def read_project_name_from_id(project_id: str) -> str:
    """
    Read project name from its identifier
    :param project_id: identifier as string
    :return: name of the project with id [project_id]
    """
    return PROJECTS_COLL.find_one({"_id": ObjectId(project_id)})["name"]


def read_project_id_from_name(name: str) -> str:
    """
    Read project id from its name
    :param name: name of the project
    :return: id of the project with name [name]
    """
    return str(PROJECTS_COLL.find_one({"name": name})["_id"])


def update(project_id: str, params: Dict[str, str]):
    """
    Update project name
    :param project_id: id of the project
    :param params: dictionary with new data
    :return:
    """
    if "name" in params:
        PROJECTS_COLL.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    "name": params["name"],
                    "modified": True,
                    "timestamp": datetime.now(),
                }
            },
        )


def delete(project_id: str):
    """
    Delete project data
    :param project_id: id of the project
    :return:
    """
    project = PROJECTS_COLL.find_one({"_id": ObjectId(project_id)})
    if project:
        delete_models(project_id)
        # PROJECTS_COLL.delete_one(project)
        PROJECTS_COLL.update(
            project, {"$set": {"deleted": True, "timestamp": datetime.now()}}
        )
        dirpath = os.path.join(MODEL_PATH, project["name"])
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            shutil.rmtree(dirpath)


#################
## CRUD MODELS ##
#################


def create_model(project_id: str, model_list: List[str]):
    """
    Create new models from list [model_list]
    :param project_id: id of the project that the models are linked to
    :param model_list: list of new models, list of strings
    :return:
    """
    for model in model_list:
        data = {"name": model, "project_id": ObjectId(project_id)}
        MODELS_COLL.update_one(data, {"$set": data}, upsert=True)


def read_models(project_id: str) -> List[Dict[str, Any]]:
    """
    Read data of every model stored related to a project with id [project_id]
    :param project_id: id of the project
    :return: a list with the data of the models
    """
    pipeline = [
        {
            "$lookup": {
                "from": "stories",
                "localField": "_id",
                "foreignField": "model_id",
                "as": "stories",
            }
        },
        {"$match": {"project_id": ObjectId(project_id)}},
        {"$project": {"name": 1, "stories_length": {"$size": "$stories"}}},
    ]

    data = list(MODELS_COLL.aggregate(pipeline))
    project_name = read_project_name_from_id(project_id)
    for doc in data:
        model_name = read_model_name_from_id(doc["_id"])
        if os.path.exists(os.path.join(MODEL_PATH, project_name, model_name)):
            doc["last_trained_timestamp"] = datetime.fromtimestamp(
                os.path.getctime(
                    get_latest_model(os.path.join(MODEL_PATH, project_name, model_name))
                )
            ).isoformat()

    return json.objectid_to_id(json.loads(json_mongo.dumps(data)))


def read_model_name_from_id(model_id: str) -> str:
    """
    Gets model name from identifier
    :param model_id: id of the model
    :return: string with the model name
    """
    return MODELS_COLL.find_one({"_id": ObjectId(model_id)})["name"]


def read_model_id_from_name(name: str) -> str:
    """
    Gets model identifier from name
    :param name: name of the model
    :return: string with the model identifier
    """
    return str(MODELS_COLL.find_one({"name": name})["_id"])


def update_model(project_id: str, model_id: str, params: Dict[str, str]):
    """
    Updates the data of a model
    :param project_id: identifier of the model
    :param model_id: identifier of the model
    :param params: dictionary with new data for the model
    :return:
    """
    if "name" in params:
        MODELS_COLL.update_one(
            {"_id": ObjectId(model_id), "project_id": ObjectId(project_id)},
            {
                "$set": {
                    "name": params["name"],
                    "modified": True,
                    "timestamp": datetime.now(),
                }
            },
        )


def delete_models(project_id: str):
    """
    Delete all models related to a project with id [project_id]
    :param project_id: identifier of the project
    :return:
    """
    project = PROJECTS_COLL.find_one({"_id": ObjectId(project_id)})
    if project:
        MODELS_COLL.find({"project_id": ObjectId(project_id)})
        MODELS_COLL.update_many(
            {"project_id": ObjectId(project_id)},
            {"$set": {"deleted": True, "timestamp": datetime.now()}},
        )
        # if models:
        #     for model in models:
        #         delete_model(project["_id"], model["_id"])


def delete_model(project_id: str, model_id: str):
    """
    Delete model data
    :param project_id: identifier of the project
    :param model_id: identifier of the model
    :return:
    """
    model = MODELS_COLL.find_one(
        {"_id": ObjectId(model_id), "project_id": ObjectId(project_id)}
    )
    MODELS_COLL.delete_one(model)

    project = PROJECTS_COLL.find_one({"_id": ObjectId(project_id)})
    PROJECTS_COLL.update(project, {"$inc": {"models_length": -1}})

    # Delete all the data of the model
    query = {"project_id": ObjectId(project_id), "model_id": ObjectId(model_id)}

    INTERACTIONS_COLL.delete_many(query)
    TEMPLATES_COLL.delete_many(query)
    ENTITIES_COLL.delete_many(query)
    INTENTS_COLL.delete_many(query)
    STORIES_COLL.delete_many(query)
    VALUES_COLL.delete_many(query)

    dirpath = os.path.join(MODEL_PATH, project["name"], model["name"])
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)


############################
### ADDITIONAL FUNCTIONS ###
############################


def enabled_chat(project: str, model: str):
    """
    Is the model [model] of the project [project] ready to talk?
    :param project: project name
    :param model: model name
    :return: True if the model [model] of the project [project] has been trained and its ready to talk, False otherwise
    """
    model_path = os.path.join(MODEL_PATH, project, model)
    if os.path.exists(model_path) and len(os.listdir(model_path)) > 0:
        return Agent.load(get_latest_model(model_path)).is_ready()
    else:
        return False


if __name__ == "__main__":
    from pprint import pprint

    pprint(read_models("5daeca8bcbd35e35dcf7f563"))
