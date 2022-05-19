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

    """Returns issues type.

        Parameters
        ----------
        message str

        Returns
        -------
        message str

        """

    return find_type(message, TRANSPORT_ISSUE_TYPES, "")


def get_issue_reason(message):

    """Returns issues reason.

        Parameters
        ----------
        message str

        Returns
        -------
        message str

        """


    return find_type(message, TRANSPORT_ISSUE_REASON, "")


def get_road_type(type):

    """Returns roads type string in lower format.

        Parameters
        ----------
        type str

        Returns
        -------
        type str

        """

    if type.lower().startswith("raa"):
        return "autonómica"
    elif type.strip() == "":
        return "sin clasificar"

    return type.lower()


def get_road_name(misc, location, text):

    """Returns roads name.

        Parameters
        ----------
        misc str
        location str
        text str

        Returns
        -------
        road_name str

        """

    road_name = None

    if misc is None:
        if location is not None:
            road_name = clean_input(
                location, ["carretera", "autovia", "autovía", "via", "vía"]
            )
    else:
        road_name = misc

    if road_name is None:
        try:
            entities = get_entities(text, duckling=False)
        except Exception as e:
            entities = None
        print(entities)
        if entities is not None:
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
        else:
            road_name = None

    return road_name

def getOriginValue(text):

    """Returns text variable is replaced by point and commas for empty space.

        Parameters
        ----------
        text str

        Returns
        -------
        text str

        """

    text = text.replace(".","")
    text = text.replace(",", "")
    return text