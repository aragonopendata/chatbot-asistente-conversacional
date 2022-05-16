"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from pprint import pprint

from mongo_connector.config import *

new_db = Database(client, "pruebas")

collection = new_db["hierarchy"]


def fill_hierarchy():
    pipeline = [
        {
            "$lookup": {
                "from": "models",
                "localField": "_id",
                "foreignField": "project_id",
                "as": "models",
            }
        },
        {"$unwind": {"path": "$models"}},
        {
            "$lookup": {
                "from": "intents",
                "localField": "models._id",
                "foreignField": "model_id",
                "as": "models.intents",
            }
        },
        {
            "$lookup": {
                "from": "entities",
                "localField": "models._id",
                "foreignField": "model_id",
                "as": "models.entities",
            }
        },
        {
            "$lookup": {
                "from": "stories",
                "localField": "models._id",
                "foreignField": "model_id",
                "as": "models.stories",
            }
        },
        {"$group": {"_id": "$_id", "models": {"$push": "$models"}}},
        {
            "$project": {
                "name": 1,
                "models.name": 1,
                "models._id": 1,
                "models.intents.name": 1,
                "models.intents._id": 1,
                "models.entities.name": 1,
                "models.entities._id": 1,
                "models.entities.color": 1,
                "models.entities.text_color": 1,
                "models.entities.intents.name": 1,
                "models.entities.intents.id": 1,
                "models.stories.name": 1,
                "models.stories._id": 1,
            }
        },
    ]

    data = list(PROJECTS_COLL.aggregate(pipeline))

    for doc in data:
        for model in doc["models"]:
            for entity in model["entities"]:
                entity["values"] = list(
                    VALUES_COLL.find(
                        {"entity_id": entity["_id"]},
                        {"project_id": 0, "model_id": 0, "entity_id": 0},
                    )
                )

            for intent in model["intents"]:
                intent["templates"] = list(
                    TEMPLATES_COLL.find(
                        {"intent_id": intent["_id"]},
                        {"project_id": 0, "model_id": 0, "intent_id": 0},
                    )
                )

            for story in model["stories"]:
                story["interactions"] = list(
                    INTERACTIONS_COLL.find(
                        {"story_id": story["_id"]},
                        {"project_id": 0, "model_id": 0, "story_id": 0, "id": 0},
                    )
                )

    collection.insert_one(data)


if __name__ == "__main__":
    fill_hierarchy()
