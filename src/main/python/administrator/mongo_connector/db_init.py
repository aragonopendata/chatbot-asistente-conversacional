'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import json
import os

from pymongo import MongoClient
from pymongo.database import Database

client = MongoClient("mongodb://mongodb:27017")
db = Database(client, "rasa")

here = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(here)

COLLECTIONS_TO_DROP = [
    "projects",
    "models",
    "intents",
    "templates",
    "entities",
    "values",
    "stories",
    "interactions",
]


def create_mongo_db():

    print(f"[INFO] Dropping every collection but 'sessions' in {db.name} database")
    for collection in COLLECTIONS_TO_DROP:
        db.drop_collection(collection)

    project_collection = db["projects"]
    model_collection = db["models"]
    with open(os.path.join(parent, "projects.json"), encoding="utf8") as f:
        data = json.load(f)
        print(f"[INFO] Creating {db.name}...")
        for project in data:
            print(f"[INFO] Dumping project {project['id']} data...")
            result = project_collection.insert_one(
                {
                    "name": project["name"],
                    # "models_length": len(project["models"]),
                }
            )
            project_id = result.inserted_id
            for model in project["models"]:
                print(f"\t[INFO] Dumping model {model['name']}...")
                result = model_collection.insert_one(
                    {"name": model["name"], "project_id": project_id}
                )
                model_id = result.inserted_id

                intents_objectid = dump_intents_and_templates(
                    project_id, model_id, project["id"], model["id"]
                )
                dump_entities_and_values(
                    project_id, model_id, project["id"], model["id"], intents_objectid
                )
                dump_stories_and_interactions(
                    project_id, model_id, project["id"], model["id"]
                )

            print("\t[INFO] Models dumped successfully")
        print("[INFO] Projects dumped successfully")


def dump_intents_and_templates(project_id, model_id, project_name, model_name):
    data_path = os.path.join(parent, "data", project_name, model_name)

    intent_collection = db["intents"]
    template_collection = db["templates"]

    intents_objectid = {}

    print("\t\t[INFO] Dumping intents and templates")
    for file in os.listdir(os.path.join(data_path, "templates")):
        intent_data = json.load(open(os.path.join(data_path, "templates", file)))

        templates = intent_data.pop("templates", None)
        intent_data["project_id"] = project_id
        intent_data["model_id"] = model_id
        intent_data.pop("templates_length", None)
        intent_data.pop("is_erasable", None)
        intent_data.pop("id", None)

        result = intent_collection.insert_one(intent_data)
        intent_id = result.inserted_id

        intents_objectid[intent_data["name"]] = intent_id

        for template in templates:
            template["project_id"] = project_id
            template["model_id"] = model_id
            template["intent_id"] = intent_id
            # template["intent_name"] = intent_data["name"]
            template.pop("id", None)

            template_collection.insert_one(template)
    print("\t\t[INFO] Intents and templates dumped successfully")

    return intents_objectid


def dump_entities_and_values(
    project_id, model_id, project_name, model_name, intents_objectid
):
    data_path = os.path.join(parent, "data", project_name, model_name)

    entity_collection = db["entities"]
    values_collection = db["values"]

    print("\t\t[INFO] Dumping entities and values...")
    with open(os.path.join(data_path, "entities.json"), encoding="utf8") as f:
        entities_data = json.load(f)
        for entity in entities_data:
            values = entity.pop("values", None)
            entity["project_id"] = project_id
            entity["model_id"] = model_id
            entity.pop("id", None)
            entity.pop("values_length", None)

            for intent in entity["intents"]:
                intent["id"] = intents_objectid.get(intent["name"])
                # intent.pop("name")

            result = entity_collection.insert_one(entity)
            entity_id = result.inserted_id

            for value in values:
                value["project_id"] = project_id
                value["model_id"] = model_id
                value["entity_id"] = entity_id
                # value["entity_name"] = entity["name"]
                value.pop("id", None)

                values_collection.insert_one(value)
    print("\t\t[INFO] Entities and values dumped successfully")


def dump_stories_and_interactions(project_id, model_id, project_name, model_name):
    data_path = os.path.join(parent, "data", project_name, model_name)

    story_collection = db["stories"]
    interactions_collection = db["interactions"]

    print("\t\t[INFO] Dumping stories and interactions...")
    with open(os.path.join(data_path, "stories.json"), encoding="utf8") as f:
        stories_data = json.load(f)
        for story in stories_data:
            interactions = story.pop("interactions", None)
            story["project_id"] = project_id
            story["model_id"] = model_id
            # story["interactions_length"] = len(interactions)
            story.pop("id", None)

            result = story_collection.insert_one(story)
            story_id = result.inserted_id

            for interaction in interactions:
                interaction["story_id"] = story_id
                interaction["model_id"] = model_id
                interaction["project_id"] = project_id
                interaction.pop("id", None)

                interactions_collection.insert_one(interaction)
    print("\t\t[INFO] Stories and interactions dumped successfully")


if __name__ == "__main__":
    create_mongo_db()
