'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
"""
Definition of every needed function for intent management
Covering CRUD operations
"""

from typing import List, Dict, Any, Tuple

from utils import json
import re

from mongo_connector import entities

from bson.objectid import ObjectId
from bson import json_util as json_mongo
from mongo_connector.config import INTENTS_COLL, TEMPLATES_COLL, ENTITIES_COLL

from fuzzywuzzy import fuzz
from collections import defaultdict


##############################################
################ CRUD INTENTS ################
##############################################


def create(project_id: str, model_id: str, intent_list: List[str]):
    """
    Create a new intent if does not exist yet
    :param intent_list: list with intents
    :return:
    """

    for intent_name in intent_list:
        INTENTS_COLL.update_one(
            {
                "name": intent_name,
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
            },
            {"$set": {"name": intent_name}},
            upsert=True,
        )


def read(project_id: str, model_id: str) -> List[Dict[str, Any]]:
    """
    Get the information of every stored intent
    :return: a dictionary with every intent and its related data
    """
    pipeline = [
        {
            "$lookup": {
                "from": "templates",
                "localField": "_id",
                "foreignField": "intent_id",
                "as": "templates",
            }
        },
        {
            "$match": {
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
            }
        },
        {"$project": {"name": 1, "templates_length": {"$size": "$templates"}}},
    ]

    return json.objectid_to_id(
        json.loads(json_mongo.dumps(INTENTS_COLL.aggregate(pipeline)))
    )


def read_id_by_name(project_id: str, intent_name: str) -> str:
    """
    Retuirn identifier for the intent with name [intent_name]
    :param intent_name: name of the intent
    :return: identifier for the intent
    """
    return str(
        INTENTS_COLL.find_one(
            {"name": intent_name, "project_id": ObjectId(project_id)}
        )["_id"]
    )


def read_name_by_id(project_id: str, intent_id: str) -> str:
    """
    Gets name of the intent
    :param intent_id: identifier of the intent
    :return: name associated to thge identifier
    """
    return INTENTS_COLL.find_one(
        {"_id": ObjectId(intent_id), "project_id": ObjectId(project_id)}
    )["name"]


def update(project_id: str, model_id: str, intent_id: str, params: Dict[str, Any]):
    """
    Rename an intent
    :param intent_id: id of the intent
    :param params: body request
    :return:
    """
    if "name" in params:
        INTENTS_COLL.update_one(
            {
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "_id": ObjectId(intent_id),
            },
            {"$set": {"name": params["name"]}},
        )


def delete(project_id: str, model_id: str, intent_id: str):
    """
    Delete an intent
    :param intent_id: id of the intent
    :return:
    """

    INTENTS_COLL.delete_one(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "_id": ObjectId(intent_id),
        }
    )

    TEMPLATES_COLL.delete_many(
        {
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "intent_id": ObjectId(intent_id),
        }
    )


######################################################
############### CUD INTENTS TEMPLATES ################
######################################################


def create_templates(
    project_id: str, model_id: str, intent_id: str, template_list: List[str]
):
    """
    Add every template from a list
    :param template_list: lit of examples
    :param intent_id: id of the intent
    :return:
    """

    for template in template_list:
        # intent_name = read_name_by_id(project_id, model_id, intent_id)
        result = TEMPLATES_COLL.update_one(
            {
                "name": template,
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "intent_id": ObjectId(intent_id),
            },
            {"$set": {"name": template}},
            upsert=True,
        )

        # If new template, update entities, user may insert already existing templates
        # so we avoid to do work already done
        if not result.matched_count:
            # Para cada entidad que aparece en el texto, hay que actualizar el templates_length
            for entity in entities.get_entities_from_text(template):
                entities.update_templates_count(
                    project_id, model_id, entity, intent_id, 1
                )


def read_templates(
    project_id: str, model_id: str, intent_id: str = None
) -> List[Dict[str, Any]]:
    """
    Get templates of every intent or an specific one with id [intent_id]
    :param intent_id: id of the intent
    :return:
    """
    data = {"project_id": ObjectId(project_id), "model_id": ObjectId(model_id)}

    if intent_id:
        data["intent_id"] = ObjectId(intent_id)

    return json.objectid_to_id(
        json.loads(
            json_mongo.dumps(
                TEMPLATES_COLL.find(data, {"project_id": 0, "model_id": 0})
            )
        )
    )


def update_template(
    project_id: str,
    model_id: str,
    intent_id: str,
    template_id: str,
    params: Dict[str, str],
):
    """
    Update information of a template of an intent
    :param intent_id: index of the intent
    :param template_id: index of the template
    :param params: json with new data
    :return:
    """

    if "name" in params:
        template = TEMPLATES_COLL.find_one(
            {
                "_id": ObjectId(template_id),
                "project_id": ObjectId(project_id),
                "model_id": ObjectId(model_id),
                "intent_id": ObjectId(intent_id),
            }
        )

        old_text = template["name"]
        new_text = params["name"]
        TEMPLATES_COLL.update_one(template, {"$set": {"name": new_text}})

        entity_set_old = entities.get_entities_from_text(old_text)
        entity_set_new = entities.get_entities_from_text(new_text)
        for entity in (
            entity_set_old - entity_set_new
        ):  # Old entities, no longer in text
            entities.update_templates_count(project_id, model_id, entity, intent_id, -1)

        for entity in entity_set_new - entity_set_old:  # New entities in text
            entities.update_templates_count(project_id, model_id, entity, intent_id, 1)


def delete_template(project_id: str, model_id: str, intent_id: str, template_id: str):
    """
    Delete a text example from an intent
    :param intent_id: id of the intent
    :param template_id: index of the template to delete
    :return:
    """

    TEMPLATES_COLL.delete_one(
        {
            "_id": ObjectId(template_id),
            "project_id": ObjectId(project_id),
            "model_id": ObjectId(model_id),
            "intent_id": ObjectId(intent_id),
        }
    )


#######################################################
############## EXAMPLES FROM TEMPLATES ################
#######################################################


def read_examples(
    project_id: str, intent_id: str, template_id: str = None
) -> List[Dict[str, Any]]:
    """
    Get every example generated from intent [intent_id]'s templates or from an specific template with id [template_id]
    :param intent_id: id of the intent
    :param template_id: id of the template
    :return: examples generated
    """
    query = {"project_id": ObjectId(project_id), "intent_id": ObjectId(intent_id)}
    if template_id:
        query["_id"] = ObjectId(template_id)

    templates = TEMPLATES_COLL.find(query)
    entities_data = [x["name"] for x in ENTITIES_COLL.find()]
    examples = []

    for template in templates:
        text = template["name"]
        intent_name = read_name_by_id(project_id, str(template["intent_id"]))

        matches = re.finditer(r"\${([\w ]+)}", text, re.MULTILINE)

        entity_list = []

        for match in matches:
            if match.group(1) in entities_data:
                # Get entity id from name
                entity_id = entities.read_id_from_name(project_id, match.group(1))
                entity_values = [
                    x["name"] for x in entities.read_values(project_id, entity_id)
                ]
                entity_list.append((match.group(0), match.group(1), entity_values))

        rasa_examples = [{"text": text, "intent": intent_name, "entities": list()}]

        if len(entity_list) > 0:
            examples += examples_from_templates(
                rasa_examples, intent_name, entity_list, 0
            )
        else:
            examples += rasa_examples

    return examples


def examples_from_templates(
    rasa_examples: List[Dict[str, Any]],
    intent_name: str,
    entity_list: [List[Tuple]],
    index: int,
):
    """
    Append every example generated from a list of templates
    :param rasa_examples: templates to generate examples from
    :param intent_name: name of the intent
    :param entity_list: list of entities to use for example generation
    :param index: actual id in entities list, works as end condition
    :return: a list with all the examples generated
    """

    # If every entity is processed, return the example list
    if index == len(entity_list):
        return rasa_examples
    else:

        # Match (${entity}) and entity value
        match = entity_list[index][0]
        entity = entity_list[index][1]
        values = entity_list[index][2]

        # List initialization
        examples = []

        # Iterate through every template
        for example in rasa_examples:
            example_entities = example["entities"]
            start = example["text"].index(match)

            # Iterate through entity values
            for value in values:
                # Append example generated substituting the match with the value
                new_example = {
                    "text": example["text"].replace(match, value, 1),
                    "intent": intent_name,
                    "entities": example_entities
                    + [
                        {
                            "entity": entity,
                            "value": value,
                            "start": start,
                            "end": start + len(value),
                        }
                    ],
                }
                examples.append(new_example)

        index = index + 1
        return examples_from_templates(examples, intent_name, entity_list, index)


########################
## INTENT RECOMMENDER ##
########################


def recommend(project_id: str, model_id: str, text: str) -> List[str]:
    """
    Recommend which intents have similar templates to [text]
    :param text: texto to look similarities
    :return: list with intents
    """
    intents = defaultdict(lambda: defaultdict(int))

    templates = read_templates(project_id, model_id)

    for example in templates:
        intent_name = read_name_by_id(project_id, example["intent_id"]["$oid"])
        ratio = fuzz.token_sort_ratio(text, example["name"])
        if ratio > 70:
            intents[intent_name]["times"] += 1
            intents[intent_name]["ratio"] += ratio

        if intent_name in intents:
            intents[intent_name]["mean_ratio"] = intents[intent_name].get(
                "ratio"
            ) / intents[intent_name].get("times")

    return sorted(intents, key=lambda x: intents.get(x).get("mean_ratio"), reverse=True)


##########################
## ADDITIONAL FUNCTIONS ##
##########################


def list_with_entity(
    project_id: str, model_id: str, entity_name: str
) -> List[Dict[str, Any]]:
    """
    Gets a list of dicitonaries with every intent id, name and count of templates that have the entity [entity_name]
    :param entity_name: entity name that is being looked for
    :return: list with intents found and its count of occurrences
    """
    pattern = "${" + entity_name + "}"
    intents = set()
    templates = read_templates(project_id, model_id)
    for template in templates:
        if pattern in template["name"]:
            intents.add(template["intent_id"])

    result = []
    for intent_id in list(intents):
        result.append(
            {"id": ObjectId(intent_id), "name": read_name_by_id(project_id, intent_id)}
        )

    return result
