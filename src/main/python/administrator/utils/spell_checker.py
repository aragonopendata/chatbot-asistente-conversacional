"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
"""
Spell checker script, its only function it is to correct
the spelling of every word in a tring and return those words
joined in one simple string

Hunspell package can only be used in Unix systems and the steps
to install it are the follwoings:
    1.- apt-get update && apt-get upgrade -y
    2.- apt-get install build-essential dkms -y
    3.- apt-get install libhunspell-dev -y
    4.- apt-get install libreoffice hunspell-es -y
    5.- apt-get install libreoffice hyphen-es -y
    6.- pip install hunspell (in your favourite Python environment)

In step 4 and 5 you should write libreoffice dictionaries of your language
"""
from typing import List

import hunspell

# Load the speller with Spanish dictionaries
spell_checker = hunspell.HunSpell(
    "/usr/share/hunspell/es_ES.dic", "/usr/share/hunspell/es_ES.aff"
)

WORDS = ["email", "e-mail", "mail", "website", "url"]

# Add custom words to the dictionary
for word in WORDS:
    spell_checker.add(word)


def correct_spell(words: str) -> str:
    """
    Return a string with words of the list [words] corrected
    :param words: string to split
    :return: the string but corrected
    """
    if isinstance(words, str):
        words = words.split()

    corrected = []
    for w in words:
        ok = spell_checker.spell(w)  # check spelling
        if not ok:
            suggestions = spell_checker.suggest(w)
            if len(suggestions) > 0:  # there are suggestions
                best = suggestions[0]
                corrected.append(best)
            else:
                corrected.append(w)  # there's no suggestion for a correct word
        else:
            corrected.append(w)  # this word is correct

    return " ".join(corrected)
