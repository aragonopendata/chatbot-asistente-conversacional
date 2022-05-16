"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
"""
Definition of every needed function for entity management
Covering CRUD operations (create, get, patch, delete)
"""
from typing import List, Dict, Any, Set

from mongo_connector import intents
from utils import json
import re

from utils.rgb import get_text_color, generate_color

from bson import json_util as json_mongo
from bson.objectid import ObjectId
from mongo_connector.config import ENTITIES_COLL, VALUES_COLL, TEMPLATES_COLL


#########################
##### CRUD ENTITIES #####
#########################


def create(project_id: str, model_id: str, entity_list: List[str]):
    """
    Create a new entity
    :param entity_list: list with entities names
    :return:
    """
    from mongo_connector import intents

    for entity_name in entity_list:
        red, green, blue = generate_color()
        intent_list = intents.list_with_entity(project_id, model_id, entity_name)
        # Si se mete una entidad dos veces se actualizará el color del texto y el background con otros aleatorios
        ENTITIES_COLL.update_one(
            {
                "name": entity_name,
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
            },
            {
                # No se incluye values length porque si ya existe, no queremos pisar este campo
                "$set": {
                    "color": "#%02x%02x%02x" % (red, green, blue),
                    "intents": intent_list,
                    "name": entity_name,
                    "text_color": get_text_color(red, green, blue),
                    "project_id": ObjectId(project_id),
                    "model_id": ObjectId(model_id),
                }
            },
            upsert=True,
        )


def read(project_id: str, model_id: str) -> List[Dict[str, Any]]:
    """
    Return information from entities
    :return: data of the entities
    """
    pipeline = [
        {
            "$lookup": {
                "from": "values",
                "localField": "_id",
                "foreignField": "entity_id",
                "as": "values",
            }
        },
        {
            "$match": {
                "project_id": ObjectId(project_id),
            }
        },
        {
            "$project": {
                "name": 1,
                "color": 1,
                "intents": 1,
                "text_color": 1,
                "intents_length": {"$size": "$intents"},
                "values_length": {"$size": "$values"},
            }
        },
    ]

    data = list(ENTITIES_COLL.aggregate(pipeline))

    for doc in data:
        intent_list = doc["intents"]
        entity = doc["name"]
        regx = re.compile(r"\${" + entity + "}", re.IGNORECASE)
        for intent in intent_list:
            intent["templates_length"] = TEMPLATES_COLL.count_documents(
                {"intent_id": intent["id"], "name": {"$regex": regx}}
            )

    return json.objectid_to_id(json.loads(json_mongo.dumps(data)))


def read_id_from_name(project_id: str, name: str) -> str:
    """
    Returns an string representation of the identifier of an entity with name [name]
    :param name: name of the entity
    :return: id of the entity
    """
    return str(
        ENTITIES_COLL.find_one({"project_id": ObjectId(project_id), "name": name})[
            "_id"
        ]
    )


def update(project_id: str, model_id: str, entity_id: str, params: Dict[str, str]):
    """
    Update information of the entity with id [entity_id]
    :param params: json with new information
    :return:
    """

    new_data = {}
    if "name" in params:
        new_data["name"] = params["name"]

    if "color" in params:
        color = params["color"]
        new_data["color"] = color
        h = color.lstrip("#")
        red, green, blue = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
        new_data["text_color"] = get_text_color(red, green, blue)

    ENTITIES_COLL.update_one(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "_id": ObjectId(entity_id),
        },
        {"$set": new_data},
    )


def delete(project_id: str, model_id: str, entity_id: str):
    """
    Deletes the data of the entity with id [entity_id]
    :return:
    """
    ENTITIES_COLL.delete_one(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "_id": ObjectId(entity_id),
        }
    )

    VALUES_COLL.delete_many(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "entity_id": ObjectId(entity_id),
        }
    )


#####################################################
############### CRUD ENTITIES VALUES ################
#####################################################


def create_values(project_id: str, model_id: str, entity_id: str, value_list: List):
    """
    Add a list of values to the entity with id [entity_id]
    :param value_list: list of values
    :return:
    """
    for value in value_list:
        VALUES_COLL.update(
            {
                "name": value,
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "entity_id": ObjectId(entity_id),
            },
            {
                "name": value,
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "entity_id": ObjectId(entity_id),
            },
            upsert=True,
        )


def read_values(project_id: str, entity_id: str) -> List[Dict[str, Any]]:
    """
    Return data from an entity with id [entity_id]
    :return: entity data
    """

    return json.objectid_to_id(
        json.loads(
            json_mongo.dumps(
                VALUES_COLL.find(
                    {
                        "project_id": ObjectId(project_id),
                        "entity_id": ObjectId(entity_id),
                    },
                    {"project_id": 0, "model_id": 0, "entity_id": 0},
                )
            )
        )
    )


def update_value(
    project_id: str,
    model_id: str,
    entity_id: str,
    value_id: str,
    params: Dict[str, str],
):
    """
    Update value name for the entity with id [entity_id]
    :param params: dictionary with new name
    :return:
    """
    if "name" in params:
        VALUES_COLL.update_one(
            {
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "entity_id": ObjectId(entity_id),
                "_id": ObjectId(value_id),
            },
            {"$set": {"name": params["name"]}},
        )


def delete_value(project_id: str, model_id: str, entity_id: str, value_id: str):
    """
    Deletion of the value with id [value_id] from the entit with id [entity_id]
    :param entity_id: id of the entity
    :param value_id: id of the value
    :return:
    """
    VALUES_COLL.delete_one(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "entity_id": ObjectId(entity_id),
            "_id": ObjectId(value_id),
        }
    )

    ENTITIES_COLL.update_one(
        {
            "_id": ObjectId(entity_id),
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
        },
        {"$inc": {"values_length": -1}},
    )


############################
### ADDITIONAL FUNCTIONS ###
############################


def remove_intent(project_id: str, model_id: str, intent_id: str):
    """
    Remove all entity dependencies with the intent with id [intent_id]
    :return:
    """
    ENTITIES_COLL.update_many(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "intents.id": ObjectId(intent_id),
        },
        {
            "$pull": {"intents": {"id": ObjectId(intent_id)}},
            "$inc": {"intents_length": -1},
        },
    )


def get_entities_from_text(text: str) -> Set[str]:
    """
    Get entities in a text that looks like ${entity}
    :param text: text to look in
    :return: list with found entities, only entity name, not ${}
    """
    matches = re.finditer(r"\${([\w ]+)}", text, re.MULTILINE)

    entities = set()

    for match in matches:
        entities.add(match.group(1))

    return entities


def update_templates_count(
    project_id: str, model_id: str, entity_name: str, intent_id: str, increment: int
):
    """
    Increment or decrement count of templates of intent with id [intent_id] for entity [entity_name]
    :param entity_name: entity name
    :param increment: number to add to the count
    :return:
    """

    query = {
        "project_id": ObjectId(project_id),
        "model_id": ObjectId(model_id),
        "name": entity_name,
    }
    result = ENTITIES_COLL.find_one(query)

    # If the entity does not exist, create it
    if not result:
        print(f"Creando entidad {entity_name}")
        create(project_id, model_id, [entity_name])
        return

    query["intents.id"] = ObjectId(intent_id)
    operator = {"$inc": {"intents.$.templates_length": increment}}
    result = ENTITIES_COLL.find_one(query)
    if not result:
        # Si no existe, sustituimos el operador de incrementar por el de set a 1
        # Primer template de la intencion en el que aparece la entidad
        # Quitamos de la query el match sobre el array ya que no está
        query.pop("intents.id")
        operator = {
            "$push": {
                "intents": {
                    "id": ObjectId(intent_id),
                    "name": intents.read_name_by_id(project_id, intent_id),
                    "templates_length": increment,
                }
            },
            "$inc": {"intents_length": 1},
        }

    ENTITIES_COLL.update_one(query, operator)

    result = ENTITIES_COLL.find_one(query)

    # Si la intención de la lista se ha quedado con templates_length igual a 0
    # significa que ya no hay ningún template en esa intención que incluya la entidad
    # por lo que se borra de la lista de intenciones
    if result and increment < 0:
        for intent in result["intents"]:
            if intent["id"] == ObjectId(intent_id) and intent["templates_length"] <= 0:
                remove_intent(project_id, model_id, intent_id)
                break
