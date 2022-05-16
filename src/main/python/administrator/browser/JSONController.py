"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import json
import requests
import pandas as pd
from functools import lru_cache

class jsonController:
    
    """ This class controls all  the operation related by JSON. """


    @lru_cache(maxsize=None)
    def getContent(self, url):
        """ This function gives the content of a web site in JSON structre. 
        Parameter:
        ----------
            url str

        Returns
        ---------
            self.data_json_structure json

            """

        self.url = url
        self.data = requests.get(url)
        self.data_json_structure = self.data.json()
        return self.data_json_structure

    @lru_cache(maxsize=None)
    def getContentJSON(self, url):
        """ This function gives the content of a web site in JSON structure converting to utf-8 format. 
        Parameter
        ----------
            url str

        Returns
        ---------
            self.data_json_structure['results'] json

            """

        self.url = url
        self.data = requests.get(url)
        self.data_json_structure = json.loads(
        requests.get(url).content.decode("utf-8"))
        return self.data_json_structure['results']

    def getJsonFormat(self, dictData):
        """ This function transform a dictionary to JSON format. 
        Parameter
        ----------
            dictData dict
        
        Returns
        ---------
            self.data_json json
            """

        app_json = json.dumps(dictData)
        self.data_json = app_json

    @lru_cache(maxsize=None)
    def getJSONObject(self):
        """ Return the data of the class. 

        Returns
        ---------
            self.data_json json

            """

        return self.data_json
    
    @lru_cache(maxsize=None)
    def setListToPandas(self):
        """ This function transform a list to Pandas. 

        Returns
        ---------
            self.df pandas

            """

        self.df = pd.DataFrame(
            self.data_json_structure
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
