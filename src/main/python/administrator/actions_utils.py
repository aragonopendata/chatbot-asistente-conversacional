'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import json
from datetime import datetime
import requests
from duckling import Duckling
from pprint import pprint
from typing import Dict, Any, List, Union

import re

duckling = Duckling()
duckling.load(languages=["es"])

#########################
# NUMBERS & MONTHS MAPS #
#########################

map_numbers_es = {
    "un": 1,
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
}

map_numbers_en = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

numbers = {"es": map_numbers_es, "en": map_numbers_en}

LINKERS = ["el", "la", "en", "de", "y", "por", "del", "con"]

ACCOMMODATION_TYPES = [
    "hotel",
    "camping",
    "albergue",
    "refugio",
    "apartamento",
    "casa rural",
]

ACCOMMODATION_TYPES_PLURAL = [
    "hoteles",
    "campings",
    "albergues",
    "refugios",
    "apartamentos",
    "casas rurales",
]

GASTRONOMY_TYPES = [
    "cafeteria",
    "bar",
    "restaurante",
    "pizzeria",
    "sidreria",
    "tasca",
    "pub",
    "asador",
]

PLACE_TYPE = ["provincia", "comarca", "municipio"]

SEASON_TYPE = ["alta", "media", "baja"]

ROOM_TYPE = ["sencillas", "dobles", "triples", "cuadruples", "suits","sencilla", "doble", "triple", "cuadruple", "suit"]

CROP_TYPE = [
    "frutales",
    "frutal",
    "herbaceos",
    "leñoso",
    "olivares",
    "olivar",
    "oliva",
    "regadio",
    "secano",
    "uva",
    "viñedos",
    "viñedo",
    "rustica",
    "rustico",
]

SURFACE_TYPE = [
    "superficies artificiales",
    "superficies de agua",
    "zonas agricolas",
    "zonas forestales con vegetacion natural y espacios abiertos",
    "zonas humedas",
    "superficie rustica",
]

SECTOR_TYPE = ["servicios", "industria", "agricultura", "construccion"]

EMPLOY_SECTOR_TYPE = [
    "industria y energia",
    "sin empleo anterior",
    "construccion",
    "agricultura",
    "ganaderia y pesca",
    "servicios",
]

PERSON_TYPE = ["mujeres", "hombres", "personas"]


def accommodation_list_string() -> str:
    """
    Returns a list with every acommodation available
    """
    return "No se ha detectado ningún tipo de alojamiento válido. Los disponibles son los siguientes:\n\t- {}".format(
        "\n\t- ".join(ACCOMMODATION_TYPES)
    )


def accommodation_plural_list_string() -> str:
    """
    Returns a list with every acommodation available in plural
    """
    return "No se ha detectado ningún tipo de alojamiento válido. Los disponibles son los siguientes:\n\t- {}".format(
        "\n\t- ".join(ACCOMMODATION_TYPES_PLURAL)
    )


def get_accommodation_type(message: str) -> str:
    """
    Returns an acommodation match in the string [message] or default value
    """
    return find_type(message, ACCOMMODATION_TYPES, "hotel")


def get_accommodation_type_plural(message: str) -> str:
    """
    Returns a plural acommodation match in the string [message] or default value
    """
    return find_type(message, ACCOMMODATION_TYPES_PLURAL, "hoteles")


def get_location_type(message: str) -> str:
    """
    Returns a place type in the string [message] or default value
    """
    return find_type(message, PLACE_TYPE, "municipio")


def get_season(message: str) -> str:
    """
    Returns season type in the string [message] or None
    """
    return find_type(message, SEASON_TYPE, None)


def get_room_type(message: str) -> str:
    """
    Returns room type in the string [message] or None
    """
    return find_type(message, ROOM_TYPE, None)


def get_crop_type(message: str) -> str:
    """
    Returns crop type in string [message] or None
    """
    return find_type(message, CROP_TYPE, None)


def get_sector_type(message: str) -> str:
    """
    Returns sector type in string [message] or None
    """
    return find_type(message, SECTOR_TYPE, None)


def get_employ_sector_type(message: str) -> str:
    """
    Returns employ sector in string [message] or empty string
    """
    return find_type(message, EMPLOY_SECTOR_TYPE, "")


def get_person_type(message: str) -> str:
    """
    Return person type in string [message] or default
    """
    return find_type(message, PERSON_TYPE, "personas")


def get_surface_type(message: str) -> str:
    """
    Returns surface type in string [message] or empty string
    """
    return find_type(message, SURFACE_TYPE, "")


def find_type(message: str, type_list: List, default: Any) -> Union[List, str, None]:
    """
    Returns the element in type_list that appears in message or returns default value
    :param message: string to search in
    :param type_list: list with elements to look for in the string
    :param default: default value if no element is found
    :return: match in string or default
    """
    a, b = "áéíóú", "aeiou"
    trans = str.maketrans(a, b)
    messageclean = message.lower().translate(trans)
    for c_type in type_list:
        if c_type in messageclean:
            return c_type
    return default


def get_singular_or_plural(acc_type: str, get_plural: bool = False) -> str:
    """
    Returns the correspondent plural or singular to [acc_type]
    :param acc_type: acommodation type
    :param get_plural: flag to indicate if singular or plural has to be searched
    :return: plural for [acc_type] if [get_plural] is True, singular otherwise
    """
    if get_plural:
        return ACCOMMODATION_TYPES_PLURAL[ACCOMMODATION_TYPES.index(acc_type)]
    else:
        return ACCOMMODATION_TYPES[ACCOMMODATION_TYPES_PLURAL.index(acc_type)]


def get_location_type_output(location_type: str) -> str:
    """
    Returns a formatted string depending on [location_type] value
    :param location_type: type of location
    :return: string formatted
    """
    if location_type.lower() == "municipio":
        return "el municipio de "
    elif location_type.lower() == "provincia":
        return "la provincia de "
    elif location_type.lower() == "comarca":
        return "la comarca de "
    else:
        return ""


def get_accommodation_type_output(accommodation_type: str, start: bool = False) -> str:
    """
    Returns a formatted string depending on [accommodation_type] value
    :param accommodation_type: type of acommodation
    :return: string formatted
    """
    if accommodation_type.lower() == "casa rural":
        return "La casa rural" if start else "de la casa rural"
    else:
        return (
            "El " + accommodation_type.lower()
            if start
            else "del " + accommodation_type.lower()
        )


def get_land_type(message: str) -> Union[str, None]:
    """
    Returns type of land or None
    :param message: message to find typ eof land in
    :returns: 'rústico' or 'urbano' or None if not find
    """
    tipo = find_type(message, ["rustico", "rusticos", "rustica", "rusticas"], None)
    if tipo is None:
        tipo = find_type(message, ["urbano", "urbanos", "urbana", "urbanas"], None)
        if tipo is not None:
            return "urbano"
        else:
            return None
    else:
        return "rustico"


def number_to_date(number):
    """
    Returns a parsed date from a string of 4 numbers
    Example:
        "0411" -> "04/11"
        "1007" -> "10/07"
         "912" -> "09/12"

    :param number: string that represents a date by day and month all together
    :return: the string parsed with the format "day/month"
    """
    day = number[0:2] if len(number) == 4 else f"0{number[0]}"
    month = number[2:4]

    return f"{day}/{month}"


def extract_days(msg: str, lang: str = "es") -> int:
    """
    Extract days as a number from temporary expressions
    :param msg: text
    :param lang: language of the last user message
    :return: an integer representing number of days detected in the message
    """
    parsed = duckling.parse(input_str=msg, language=lang, dim_filter="time")
    # pprint(parsed)
    if len(parsed) > 0:
        duck_value = parsed[0]["value"]
        if duck_value["type"] == "value":
            parsed_date = duck_value["value"].split("T")[0]
        elif duck_value["type"] == "interval":
            parsed_date = duck_value["to"]["value"].split("T")[0]
        else:
            print("OTRA VAINA")
            return -1

        days = (
            datetime.strptime(parsed_date, "%Y-%m-%d").date() - datetime.now().date()
        ).days
    else:
        days = None

    return days


def extract_value(path: str) -> str:
    """
    Extracts the last part of a path splitted by slashes /
    Virtuoso has some inner paths and we need the value, set at the end of the path

    Example:
         {  'answer0': 'mosaico-de-prados-o-praderas-con-espacios-significativos-de-vegetacion-natural-y-semi-natural',
            'etiqueta': 'http://opendata.aragon.es/recurso/territorio/Municipio/Huesca',
            'fecha': 'http://reference.data.gov.uk/id/year/2000'
         }
            ->
            if looking in 'etiqueta' it returns 'Huesca'
            if looking in 'fecha' it returns '2000'

    :param path: text with a path from Virtuoso to an object
    :returns: the last part of the path or empty string
    """
    if path is not None and path != "":
        parts = path.split("/")
        return parts[-1].replace("_", " ")
    return ""


def build_virtuoso_response(
    template: str, data: List[Dict[str, Any]], is_title: bool = False
):
    """
    Auxiliary function to build a response based on the Virtuoso response
    It is used with data that comes from a direct relation
    Example of relations:
        ('person', 'phone', '987654321')
        ('hotel', 'address', 'Steet Whatever, N23')

    :param template: template to fill with the data
    :param data: dictionary with the data from Virtuoso
    :param is_title: flag to do some extra formatting

    :returns: template formatted with the data from the dictionary
    """

    return "\n".join(
        [
            template.format(
                title(x["etiqueta"]),
                # Some locations come splitted with a comma, put the after comma at the beginning
                # title(" ".join(x["etiqueta"].split(", ")[::-1])),
                title(x["answer0"]) if is_title else x["answer0"],
            )
            for x in data
        ]
    )


def title(data: str) -> str:
    """
    Returns the string data with every word capitalize except from linkers like prepositions or articles
    It is used to show an human legible form of the string
    Example:
        "The phone of GEORGE OF THE JUNGLE is 987654321"
    Returns
        "The phone of George of the Jungle is 987654321"

    :param data: string to format
    :return: the string special capitalised version
    """
    data = str.lower(data)
    return " ".join(
        [x.capitalize() if str.lower(x) not in LINKERS else x for x in data.split(" ")]
    )


def get_entities(text: str, duckling=True) -> List[Dict[str, Any]]:
    """
    After a petition to a NER hosted as a REST API,
    returns the entities detected in the text [text]

    Example:
        "Zaragoza is between Barcelona and Madrid"
    Return:
        [{'confidence': 1.0,
          'end': 8,
          'entity': 'location',
          'start': 0,
          'value': 'Zaragoza'}
          {'confidence': 1.0,
          'end': 29,
          'entity': 'location',
          'start': 20,
          'value': 'Barcelona'}
          {'confidence': 1.0,
          'end': 40,
          'entity': 'location',
          'start': 34,
          'value': 'Jacetania'}]

    :param text: string to look entities in
    :return: entities found in the text
    """
    response = requests.get(
        "http://ner:4999/ner",
        params={"words": text, "plain": True, "duck": duckling},
    )
    content = json.loads(response.content)
    return content["entities"]


def get_duckling_entities(text) -> List[Dict[str, Any]]:
    """
    After a petition to a NER hosted as a REST API,
    returns the entities detected in the text [text]
    including duckling ones

    Example:
        "In march of 2012 in Zaragoza rained a lot"
    Return:
        [{'duckValue': {'grain': 'month',
                'type': 'value',
                'value': '2012-03-01T00:00:00.000+01:00',
                'values': []},
          'end': 16,
          'entity': 'time',
          'start': 3,
          'value': '12 of march of 2012'}
          {'confidence': 1.0,
          'end': 28,
          'entity': 'location',
          'start': 20,
          'value': 'Zaragoza'}]

    :param text: string to look entities in
    :return: entities found in the text
    """
    response = requests.get(
        "http://ner:4999/ner", params={"words": text, "plain": True, "duck": True}
    )
    content = json.loads(response.content)
    return content["entities"]

def get_duckling_numbers(text) :
    numbers = []
    entities = get_duckling_entities(text)

    for ent in entities:
        if ent["entity"] == "number":
            duckValue = ent["duckValue"]
            numbers.append(int(duckValue["value"]))

    return numbers

def clean_input(
    text: str,
    prefix: List[str] = ACCOMMODATION_TYPES,
    invalid_words: List[str] = ["el", "las", "los", "la", "de"],
) -> Union[str, None]:
    """
    Clean the input of some entities that NER extract with unnecessary words

    Example:
        'hotel Palafox'
    Return:
        'Palafox'

    :param text: text to clean
    :param prefix: list of words to remove from text
    :param invalid_words: list of invalid words, sometimes the text left
                          is an article, so we don't want to return it
    :return: text cleaned or None
    """
    try:
        if text is not None:
            a, b = "áéíóú", "aeiou"
            trans = str.maketrans(a, b)
            text = text.replace("_", " ")
            retry = True
            while retry:
                retry = False
                if prefix != None:
                    for c_type in prefix:
                        if text.lower().translate(trans).startswith(c_type):
                            text = text[len(c_type) :]
                            text = text.strip()
                            retry = True
                            break

                if invalid_words != None:
                    for c_type in invalid_words:
                        if text.lower().translate(trans).startswith(c_type):
                            text = text[len(c_type) :]
                            text = text.strip()
                            retry = True
                            break

            # if clean_message.lower() in invalid_words:
            #    return None
            if text.strip() == "":
                return None

            return text.strip()
        else:
            return None
    except Exception:
        return text

def replaceaccents(cadena):
    if cadena.lower().startswith("la "):
        cadena = cadena[3:]
    cadena = re.sub(r"[aáAÁ]", "[aáAÁ]", cadena)
    cadena = re.sub(r"[eéEÉ]", "[eéEÉ]", cadena)
    cadena = re.sub(r"[iíIÍ]", "[iíIÍ]", cadena)
    cadena = re.sub(r"[oóOÓ]", "[oóOÓ]", cadena)
    cadena = re.sub(r"[uúUÚ]", "[uúUÚ]", cadena)
    return cadena

def filter_response(
    answer: List[Dict[str, Any]],
    label: str,
    field: str = "etiqueta",
    exact: bool = True,
):
    """
    Returns a Virtuoso answer filtered by the value of a label, it can be
    specified a exact matching what this means is that if not a exact match
    was found it returns an empty list or the answer itself

    :param answer: dictionary with the answer of the database
    :param label: value to look in the dictionary
    :param field: key of the dictionary to look in the value [label]
    :param exact: flag to strict filter
    :return: dictionary filtered
    """
    valid_values = []
    regsearch = r"\b(" + replaceaccents(label) + r")\b"

    if answer is not None:
        for x in answer:
            if field in x and re.search(regsearch, x[field], re.IGNORECASE):
                etiqueta = x['etiqueta']
                if etiqueta.find(', la') > -1:
                    x['etiqueta'] = label
                valid_values.append(x)

    if valid_values == [] and not exact:
        valid_values = answer
    return valid_values


def get_province_code(location: str) -> str:
    """
    Returns the postal code of the location [location]
    :param location: string with the location
    :return: the postal code of the location if is 'Zaragoza', 'Huesca' or 'Teruel'
    """
    if location.lower() == "zaragoza":
        return "50"
    elif location.lower() == "huesca":
        return "22"
    elif location.lower() == "teruel":
        return "44"
    return ""

def get_year(lista_terms):

    main_terms_to_find = ['más','años']
    terms = lista_terms.split(' ')
    results = []
    for term in main_terms_to_find:
        if term in terms:
            results.append(True)
        else:
            results.append(False)

    if results[1] == True:

        position = 0
        for term in terms:
            if term == main_terms_to_find[1]:
                break
            else:
                position = position + 1

        year = int(terms[position - 1])
        if results[0] == True:
            year = year + 1

        return year

    else:

        year = 0

if __name__ == "__main__":
    from pprint import pprint

    duck_data = duckling.parse(
        "Hoteles de dos estrellas", language="es", dim_filter="number"
    )
    pprint(duck_data)
