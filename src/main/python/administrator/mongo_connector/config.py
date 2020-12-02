'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from pymongo import MongoClient
from pymongo.database import Database

# Parameters for MongoDB connection
URL = "mongodb"
PORT = 27017
DB_NAME = "rasa"

# Initialization of client and database
client = MongoClient(host=URL, port=PORT)
db = Database(client, DB_NAME)

# Projects and models collections
PROJECTS_COLL = db["projects"]
MODELS_COLL = db["models"]

# Intents and templates collections
INTENTS_COLL = db["intents"]
TEMPLATES_COLL = db["templates"]

# Entities and values collections
ENTITIES_COLL = db["entities"]
VALUES_COLL = db["values"]

# Stories collections
STORIES_COLL = db["stories"]
INTERACTIONS_COLL = db["interactions"]

# Sessions collection
SESSIONS_COLL = db["sessions"]
