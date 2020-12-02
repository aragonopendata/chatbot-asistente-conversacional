'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from datetime import datetime

from actions_utils import (
    get_duckling_numbers,
)

from browser.browser import Browser

browser = Browser()


def getYear(message):
    numbers = get_duckling_numbers(message)
    if numbers != []:
        return str(numbers[0])
    else:
        return str(datetime.now().year - 1)
     

def getYearValuePerDefect(message,valuePerDefect):
    numbers = get_duckling_numbers(message)
    
    if numbers != []:
        return str(numbers[0])
    else:
        return valuePerDefect


def getOriginValue(text):

    return text.replace(".","").replace(",", "")


def getCorrectRegister(lista,location):

    words = location.split(' ')
    number_words = len(words)
    element_return = []
    for row in lista:
        length_find = 0
        for word in words:
            if word in row['etiqueta']:
                length_find = length_find + 1
        if length_find == number_words:
            element_return.append(row)
            break
    return element_return

def eliminaTildes(text):

    text = text.replace('Á','A')
    text = text.replace('É','E')
    text = text.replace('Í','I')
    text = text.replace('Ó','O')
    text = text.replace('Ú','U')
    return text