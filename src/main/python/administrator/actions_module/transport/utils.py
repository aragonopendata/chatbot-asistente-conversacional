'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from pprint import pprint
from urllib.error import URLError

from rasa_sdk import Action
from rasa_sdk.events import SlotSet

from browser.browser import Browser

browser = Browser()


from actions_utils import (
    find_type,
    clean_input,
    build_virtuoso_response,
    title,
    get_entities,
    get_location_type,
    get_sector_type,
    get_person_type,
    get_land_type,
    get_duckling_entities,
    extract_value,
    get_surface_type,
    get_employ_sector_type,
    get_location_type_output,
)

TRANSPORT_ISSUE_TYPES = ["alerta", "incidencia", "incidente", "problema"]

TRANSPORT_ISSUE_TYPES = ["alertas", "incidencias", "incidentes", "problemas"]
TRANSPORT_ISSUE_REASON = [
    "semáforos",
    "circulación ",
    "meteorología adversa",
    "hielo",
    "nieve",
    "avería",
    "obras",
    "calzada mal en estado",
    "irrupción de peatón en calzada",
    "pérdida de carga",
    "inundaciones",
    "incendio",
    "otros problemas",
    "cadenas",
    "desprendimientos",
    "precaucion",
    "peligro",
]


def get_issue_type(message):
    return find_type(message, TRANSPORT_ISSUE_TYPES, "")


def get_issue_reason(message):
    return find_type(message, TRANSPORT_ISSUE_REASON, "")


def get_road_type(type):
    if type.lower().startswith("raa"):
        return "autonómica"
    elif type.strip() == "":
        return "sin clasificar"

    return type.lower()


def get_road_name(misc, location, text):
    road_name = None

    if misc is None:
        if location is not None:
            road_name = clean_input(
                location, ["carretera", "autovia", "autovía", "via", "vía"]
            )
    else:
        road_name = misc

    if road_name is None:
        entities = get_entities(text, duckling=False)
        print(entities)
        for ent in entities:
            if (ent["entity"] == "location" or ent["entity"] == "misc") and ent[
                "depth"
            ] == 0:
                value = clean_input(
                    ent["value"],
                    [
                        "carretera de",
                        "población de",
                        "localidad de",
                        "ciudad de",
                        "carretera",
                    ],
                )
                if value != None:
                    road_name = value.strip()
                    break

    return road_name

def getOriginValue(text):

    text = text.replace(".","")
    text = text.replace(",", "")
    return text