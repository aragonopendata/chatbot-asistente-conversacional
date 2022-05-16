"""
Wrapper for Python json module, Spanish needs to set
an utf8 encoding so to avoid each call o have it we
have wrapped the functions with default encoding,
sorting keys an indent for visualization.

Values:
    encoding: 'utf8'
    sort_keys = True
    indent = 4

Along the wrapped function there is a usefull function
to transform 'ObjectId' items from mongo to our standard
used in the GUI, which is the kye 'id'
"""

import json

from typing import Dict, Any

INDENT = 4
SORT_KEYS = True
ENCODING = "utf8"


def dump(data: Dict[str, Any], filename: str):
    """
    Wrap for json.dump function with our default parameters
    """
    json.dump(
        data,
        open(filename, mode="w", encoding=ENCODING),
        sort_keys=SORT_KEYS,
        indent=INDENT,
    )


def loads(data: Dict[str, Any]):
    """
    Wrap for loads function with 'utf8' encoding
    """
    return json.loads(data, encoding=ENCODING)


def objectid_to_id(data: Dict):
    """
    Function that transform 'ObjectId' Mongo key to an 'id' key
    in order to work with the standard set in the GUI
    """
    if all(isinstance(n, dict) for n in data):
        for item in data:
            # Get ObjectId as id to comunicate with GUI
            if "_id" in item:
                item["id"] = str(item.pop("_id").pop("$oid"))
            elif "id" in item:
                item["id"] = str(item.pop("id").pop("$oid"))

            for key, value in item.items():
                # Every item with ObjectId from Mongo -> transform to basic id
                if "_id" in key:
                    item[key] = value["$oid"]
                elif type(item[key]) is list:
                    # If the key it is a list of whatever, call recursively
                    # transformation will apply to dictionaries with '_id' or 'id' keys
                    item[key] = objectid_to_id(item[key])

    return data
