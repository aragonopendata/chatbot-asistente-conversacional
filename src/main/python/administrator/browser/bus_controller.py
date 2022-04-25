'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import requests
import pandas as pd
from functools import lru_cache

def parserPandas(parameter):

    return pd.DataFrame(parameter[1:], columns=parameter[0])

@lru_cache(maxsize=None)
def getJSONFromUrl(url):

    return requests.get(url).json()

@lru_cache(maxsize=None)
def getPandasStructure(url):

    data_json = getJSONFromUrl(url)
    df_data_json = parserPandas(data_json)
    return df_data_json


def getLocationDestiny(data, key, location):

    return data[data[key].str.contains(location.upper(), na=False)]

def getNotLocationDestiny(data, key, location):

    return data[~data[key].str.contains(location.upper(), na=False)]

def getLocationFromOriginToDestiny(
    data, keyOrigin, keyDestiny, locationOrigin, locationDestiny
):

    originData = data[data["DENO_RUTA"].str.contains(locationOrigin.upper(), na=False)]
    originDestiny = originData[
        originData["DENO_RUTA"].str.contains(locationDestiny.upper(), na=False)
    ]
    return originDestiny


def getRowFromIntegerValues(df, key, value):

    return df[df[key] == value]


def getDataframeSorted(df, key):

    return df.sort_values(by=[key])
