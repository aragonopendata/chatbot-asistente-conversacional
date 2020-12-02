'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import json
import requests
import pandas as pd
from functools import lru_cache

class jsonController:
    
    @lru_cache(maxsize=None)
    def getContent(self, url):

        self.url = url
        self.data = requests.get(url)
        self.data_json_structure = self.data.json()
        return self.data_json_structure

    def getJsonFormat(self, dictData):

        app_json = json.dumps(dictData)
        self.data_json = app_json

    @lru_cache(maxsize=None)
    def getJSONObject(self):

        return self.data_json
    
    @lru_cache(maxsize=None)
    def setListToPandas(self):

        self.df = pd.DataFrame(
            self.data_json_structure[1:], columns=self.data_json_structure[0]
        )
        return self.df

    def extract_values(self, obj, key):
        """Pull all values of specified key from nested JSON."""
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        """Agregar directo, habrá que controlar mirando que datos tiene el campo y filtrarlo."""
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        results = extract(obj, arr, key)
        return results
