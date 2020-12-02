'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import pickle
import os

"""
#######################################
# RETRIEVE PRIVATE KEYS FOR API CALLS #
#######################################
"""

f = open(os.path.dirname(__file__) + "/hidden.pickle", mode="rb")

data = pickle.load(f)
f.close()

# WEATHER
languages = ["es", "en"]
weather_api_key = data["weather_api_key"]

# NER
dandelion_token = data["dandelion_token"]

# LANGUAGE DETECTOR
language_detector_key = data["languaje_detector_key"]

# MOVIE DATABASES APIS
omdb_api_key = data["omdb_api_key"]
themoviedb_api = data["themoviedb_api"]
