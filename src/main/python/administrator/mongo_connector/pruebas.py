# Parameters for MongoDB connection
from pprint import pprint

from pymongo import MongoClient
from pymongo.database import Database

from mongo_connector import entities, stories

URL = "mongodb"
PORT = 27017
DB_NAME = "rasa"

# Initialization of client and database
client = MongoClient(host=URL, port=PORT)
db = Database(client, DB_NAME)


project_id = "5daeca8bcbd35e35dcf7f563"
model_id = "5daeca8ccbd35e35dcf7f8bb"


def templates_test():

    """ It verifies template process funcionality """

    intent_name = "intent1"
    result = db["intents"].update_one(
        {"name": intent_name}, {"$set": {"name": intent_name}}, upsert=True
    )
    print(result.matched_count)
    input("Press Enter to continue...")

    db["intents"].update_one({"name": intent_name}, {"$inc": {"templates_length": 1}})

    input("Press Enter to continue...")

    db["intents"].update_one(
        {"name": intent_name}, {"$set": {"name": intent_name + "NUEVO"}}, upsert=True
    )


def read_all_entities():

    """ It reads all the entities values 
    
    Return
    -------

    entities_data dict
    
    """

    entities_data = list(entities.read(project_id, model_id))
    for entity in entities_data:
        entity["values"] = entities.read_values(project_id, entity["id"])

    return entities_data


def read_all_stories():

    """ It reads all the stories valus 
    
    Return
    -------

    entities_data dict
    
    """

    stories_data = list(stories.read(project_id, model_id))
    for story in stories_data:
        story["interactions"] = stories.read_interactions(
            project_id, model_id, story["id"]
        )

    return stories_data


if __name__ == "__main__":
    print("Ya se harán pruebas")
    pprint(read_all_stories())
    # testing_smalltalk_domain()
