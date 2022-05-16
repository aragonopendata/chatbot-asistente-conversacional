"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from typing import Any, Dict, List

from utils import json

from bson.objectid import ObjectId
from bson import json_util as json_mongo
from mongo_connector.config import STORIES_COLL, INTERACTIONS_COLL

##################
## CRUD STORIES ##
##################


def create(project_id: str, model_id: str, story_list: List[str]):
    """
    Create a list of empty stories associated to model with id [model_id]
    :param project_id:
    :param model_id:
    :param story_list:
    :return:
    """
    for story in story_list:
        STORIES_COLL.update(
            {
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "name": story,
            },
            {
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "name": story,
            },
            upsert=True,
        )


def read(project_id: str, model_id: str) -> List[Dict[str, Any]]:
    """
    Get a list with every story name
    :return: list with the names
    """
    pipeline = [
        {
            "$lookup": {
                "from": "interactions",
                "localField": "_id",
                "foreignField": "story_id",
                "as": "interactions",
            }
        },
        {
            "$match": {
                "project_id": ObjectId(project_id),
            }
        },
        {"$project": {"name": 1, "interactions_length": {"$size": "$interactions"}}},
    ]

    return json.objectid_to_id(
        json.loads(json_mongo.dumps(STORIES_COLL.aggregate(pipeline)))
    )


def update(project_id: str, model_id: str, story_id: str, params: Dict[str, str]):
    """
    Update information of an story associated to model with id [model_id] with id [story_id]
    :param project_id:
    :param model_id:
    :param story_id:
    :param params: dictionary with data for the story
    :return:
    """
    if "name" in params:
        STORIES_COLL.update_one(
            {
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "_id": ObjectId(story_id),
            },
            {"$set": {"name": params["name"]}},
        )


def delete(project_id: str, model_id: str, story_id: str):
    """
    Delete information of story with id [story_id]
    :param project_id:
    :param model_id:
    :param story_id:
    :return:
    """
    STORIES_COLL.delete_one(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "_id": ObjectId(story_id),
        }
    )

    INTERACTIONS_COLL.delete_many(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "story_id": ObjectId(story_id),
        }
    )


############################
## CUD STORY INTERACTIONS ##
############################


def create_interaction(project_id: str, model_id: str, story_id: str):
    """
    Create a single interaction of the story [story_id]
    :param project_id:
    :param model_id:
    :param story_id:
    """
    # if all(k in params for k in ("text", "utter", "intent")):
    INTERACTIONS_COLL.insert_one(
        {
            "intent": "",
            "actions": [],
            "story_id": ObjectId(story_id),
            "model_id": ObjectId(model_id),
            "project_id": ObjectId(project_id),
            "text": "",
        }
    )


def read_interactions(
    project_id: str, story_id: str
) -> List[Dict[str, Any]]:
    """
    Gets every interaction associated to the story with id [story_id]
    :param project_id:
    :param story_id:
    :return:
    """

    return json.objectid_to_id(
        json.loads(
            json_mongo.dumps(
                INTERACTIONS_COLL.find(
                    {
                        "project_id": ObjectId(project_id),
                        "story_id": ObjectId(story_id),
                    },
                    {"project_id": 0, "model_id": 0, "story_id": 0},
                )
            )
        )
    )


def update_interaction(
    project_id: str,
    model_id: str,
    story_id: str,
    interaction_id: str,
    params: Dict[str, str],
):
    """
    Update of an interaction, whether its the text, the utter, an action
    :param project_id:
    :param model_id:
    :param story_id:
    :param interaction_id:
    :param params: dictionary with new data for interaction with id [interaction_id]
    :return:
    """
    INTERACTIONS_COLL.update_one({"_id": ObjectId(interaction_id)}, {"$set": params})


def delete_interaction(
    project_id: str, model_id: str, story_id: str, interaction_id: str
):
    """
    Deletes interaction information from interaction with id [interaction_id]
    :param project_id:
    :param model_id:
    :param story_id:
    :param interaction_id:
    :return:
    """
    INTERACTIONS_COLL.delete_one(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "story_id": ObjectId(story_id),
            "_id": ObjectId(interaction_id),
        }
    )


if __name__ == '__main__':
    from pprint import pprint

    pprint(read_interactions('5dbffabaa47f199730cc722c','5e45237b487d36cbd9f4d607'))

