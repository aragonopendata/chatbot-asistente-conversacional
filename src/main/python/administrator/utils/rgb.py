'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
"""
Auxiliar functions to create a random rgb tuple and calculate
which color should be shown on top of it, wether is black or white
depending on background darkness

For simplicity, colors are set aws red, green and blue values
defined by integers between 0 and 255
"""
import random

from typing import Tuple

# White and black constants
WHITE = "#ffffff"
BLACK = "#000000"


def get_text_color(r: int, g: int, b: int) -> str:
    """
    Returns WHITE or BLACK following the formula found here:
    https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color
    """
    value = (r * 299 + g * 587 + b * 114) / 1000

    return WHITE if value < 127 else BLACK


def generate_color() -> Tuple[int, int, int]:
    """
    Generates a random color
    """
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue
