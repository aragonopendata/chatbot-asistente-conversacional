"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from pprint import pprint
from typing import Dict, Text, Any, List
from urllib.error import URLError

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from datetime import datetime

from browser.browser import Browser


from actions_utils import (
    find_type,
    clean_input,
    build_virtuoso_response,
    title,
    get_entities,
    get_sector_type,
    get_person_type,
    get_land_type,
    get_duckling_entities,
    extract_value,
    get_surface_type,
    get_employ_sector_type,
    get_location_type,
    get_location_type_output,
)

browser = Browser()


def getEntitiesByType(entities, type):

    """Returns a list with entities with type entity type

        Parameters
        ----------
        entities: list
            List of entities
        type: text

        Returns
        -------
        toreturn list

        """

    toreturn = []
    for ent in entities:
        if ent["entity"] == type:
            toreturn.append(ent)
    return toreturn


def getYearFromEntities(entities):

    """Returns the year from the entities

        Parameters
        ----------
        entities: list
            List of entities

        Returns
        -------
        year_str int

            Get the year from the entities
        """

    year_str = ""
    try:
        print(entities)
        # buscamos primero en number y luego en time
        for ent in entities:
            if ent["entity"] == "number":
                year_str = ent["value"]
                break

        if year_str == "":
            for ent in entities:
                if ent["entity"] == "time":
                    duckValue = ent["duckValue"]
                    if duckValue["grain"] == "year":
                        v = duckValue["value"]
                        year_str = v[0 : v.index("-")]
                        break

    except:
        pass
    return year_str


def getDateFromEntities(entities, grain="day"):

    """Returns the year from the entities

        Parameters
        ----------
        entities: list
            List of entities
        grain: text

        Returns
        -------
        ent int (sometimes None)

            Get the year from the entities
        """

    try:
        for ent in entities:
            if ent["entity"] == "time":
                duckValue = ent["duckValue"]
                if duckValue["grain"] == grain:
                    return ent
    except:
        pass
    return None

def getReplaceTexts(text):

    """Returns the text converted to lower format

        Parameters
        ----------
        text: str
            List of entities over the user's question

        Returns
        -------
        text str

            text converted to lower string
        """
    
    text = text.lower()

    return text