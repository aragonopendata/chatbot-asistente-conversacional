'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import os
from pprint import pprint

from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database

from mongo_connector.projects import read_model_id_from_name, read_project_id_from_name
from trainer import load_smalltalk_domain

here = os.path.dirname(__file__)
parent = os.path.dirname(here)

SMALLTALK_DIR = os.path.join(parent, "data", "smalltalk")

client = MongoClient("mongodb://mongodb:27017")
db = Database(client, "rasa")


def smalltalk_domain():
    domain = load_smalltalk_domain()
    domain = domain.as_dict()
    return domain


def insert_smalltak_stories():
    domain = smalltalk_domain()
    data = {}
    with open(os.path.join(SMALLTALK_DIR, "stories.md")) as md:
        content = md.readlines()
        content = [x.replace("\n", "") for x in content]
        content = filter(lambda x: x.strip() != "", content)

        for line in content:
            line = line.strip()
            if line.startswith("##"):
                story_name = line.lstrip("## ")
                data[story_name] = {}

            if line.startswith("*"):
                intent_name = line.lstrip("*")
                data[story_name]["intent"] = intent_name

            if line.startswith("-"):
                action = line.lstrip("- ")

                if action.startswith("utter"):
                    templates = [x.get("text") for x in domain["templates"][action]]
                    data[story_name]["actions"] = [
                        {"type": "utter", "value": template} for template in templates
                    ]
                else:
                    data[story_name]["actions"] = [{"type": "action", "value": action}]

                # if 'actions' in data[story_name]:
                #     data[story_name]["actions"].append(new_action)
                # else:

    pprint(data)

    insert_data(data)


def insert_data(data):
    project_id = ObjectId(read_project_id_from_name("GDA"))
    model_id = ObjectId(read_model_id_from_name("smalltalk"))
    for story in data:
        result = db["stories"].insert_one(
            {
                "name": data[story]["intent"]
                if "intent" in data[story]
                else "fallback",
                "project_id": project_id,
                "model_id": model_id,
            }
        )

        story_id = result.inserted_id

        db["interactions"].insert_one(
            {
                "intent": data[story]["intent"] if "intent" in data[story] else None,
                "actions": data[story]["actions"],
                "story_id": story_id,
                "project_id": project_id,
                "model_id": model_id,
            }
        )


if __name__ == "__main__":
    insert_smalltak_stories()
