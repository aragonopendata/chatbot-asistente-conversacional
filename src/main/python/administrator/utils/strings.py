"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import os
import re

a = b = c = d = "adsa"
query = ""
query += "lo " + a + " que " + b + " sea " + c + " loko " + d

STRING_START = r"\w+ = \""
STRING_CONCATENATION_OPERATOR = r"\w+ \+= \""


def operator_to_fstring(filename):

    """
    It transform the filename text to fstring format
    :param filename: file
    :return:
    """

    f = open(filename)
    if f.mode == "r":
        contents = f.read().splitlines()
        for idx, line in enumerate(contents):
            if re.match(STRING_START, line) or re.match(
                STRING_CONCATENATION_OPERATOR, line
            ):
                print(f"{idx}:", line)


if __name__ == "__main__":
    operator_to_fstring(os.path.realpath(__file__))
