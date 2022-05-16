import requests
import pandas as pd
from functools import lru_cache

def parserPandas(parameter):

    return pd.DataFrame(parameter[1:], columns=parameter[0])

@lru_cache(maxsize=None)
def getJSONFromUrl(url):
    """ Get a JSON form a specific URL

    Parameters
    ----------
    url: String
        url to execute

    Returns
    -------
    json 

        Set of data return by a specific URL
    """
    return requests.get(url).json()

@lru_cache(maxsize=None)
def getPandasStructure(url):
    """  Get a DataFrame form a specific URL

    Parameters
    ----------
    url: String
        url to execute

    Returns
    -------
    dataframe 

        Set of data return by a specific URL
    """

    data_json = getJSONFromUrl(url)
    df_data_json = parserPandas(data_json)
    return df_data_json


def getLocationDestiny(data, key, location):
    """  Extract all the routes which destination is the location
    Parameters
    ----------
    data: dataframe
        set of data
    key: Integer
        Index of the row to extract in a dataset
    location: String
        Name of the destination location to search 

    Returns
    -------
    Dataframe 

        Set of routes with the same destination
    """

    return data[data[key].str.contains(location.upper(), na=False)]

def getNotLocationDestiny(data, key, location):
    """  Extract all the routes without destination
    Parameters
    ----------
    data: dataframe
        set of data
    key: Integer
        Index of the row to extract in a dataset
    location: String
        Name of the location

    Returns
    -------
    Dataframe 

        Set of routes without destination
    """

    return data[~data[key].str.contains(location.upper(), na=False)]

def getLocationFromOriginToDestiny(
    data, keyOrigin, keyDestiny, locationOrigin, locationDestiny
):
    """  Extract all the routes with a specific origin a destination
    Parameters
    ----------
    data: dataframe
        set of data
    keyOrigin: Integer
        Index of the row that contains the origin
    keyDestiny: Integer
        Index of the row that contains the destination
    locationOrigin: String
        Name of the origin location
    locationDestiny: String
        Name of the destination location

    Returns
    -------
    DataFrame 

        Set of routes which start in locationOrigin and finish in locationDestiny
    """

    originData = data[data["DENO_RUTA"].str.contains(locationOrigin.upper(), na=False)]
    originDestiny = originData[
        originData["DENO_RUTA"].str.contains(locationDestiny.upper(), na=False)
    ]
    return originDestiny


def getRowFromIntegerValues(df, key, value):
    """  Get a row from a dataframe from index
    Parameters
    ----------
    df: dataframe
    key: Integer
        Index of the row to be extracted
    value: Integer
        Value to compare

    Returns
    -------
    dataframe 

        Return the row with a specific value
    """

    return df[df[key] == value]


def getDataframeSorted(df, key):
    """  Sort a dataframe by key
    Parameters
    ----------
    df: dataframe
    key: String
        Name of the column to sort

    Returns
    -------
    dataframe 

        Return a sorted dataframe
    """

    return df.sort_values(by=[key])
