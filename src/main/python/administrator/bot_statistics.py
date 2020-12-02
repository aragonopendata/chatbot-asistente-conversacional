'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
"""
Script to insert data in MongoDB used to calculate statistics
from every conversation that users has had with an agent
"""
from datetime import datetime

import matplotlib.pyplot as plt
from typing import Dict, Any, List, NoReturn

import mongo_connector.config as config
import spacy
import unidecode

#from nltk.corpus import stopwords
#from nltk.tokenize.toktok import ToktokTokenizer

#from wordcloud import WordCloud

from utils import frame

days_of_week = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
    7: "Domingo",
}
months_of_year = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

nlp = spacy.blank("es")


def remove_accents_msg(msg: str) -> str:
    """
    Removes accent from a string
    :param msg: string to be processed
    :return: [msg] without accents
    """
    return unidecode.unidecode(msg)


def remove_accents_tokens(tokens: List) -> List:
    """
    Removes accents from every token in a list
    :param tokens: the list itself
    :return: the list without accents
    """
    return [unidecode.unidecode(token) for token in tokens]

'''
def tokenize(msg: str) -> List:
    """
    Tokenizes an string
    :param msg: the string itself
    :return: the string tokenized using ToktokTokenizer
    """
    toktok = ToktokTokenizer()
    return toktok.tokenize(msg)
'''
'''
def remove_stopwords(tokens: List) -> List:
    """
    Returns the original list but removing every stopword, stopwords from
    the spanish corpus of NLTK
    :param tokens: the origina list
    :return: the list filtered
    """
    return [token for token in tokens if token not in stopwords.words("spanish")]
'''

def lemmatizer(msg: str) -> str:
    """
    Returns a lemmatized message, lemmatize is to get the root of the word,
    for example: jugaron -> jug, vivieron -> viv and so on
    :param msg: the message itself
    :return: the message lemmatized
    """
    return " ".join(nlp(msg))


def print_wordcloud(collection, field: str, output: str = "word_cloud.png") -> NoReturn:
    """
    Saves a wordclous using all he data stored in a collection, specifically
    the data stored in the field provided, into an output .png
    :param collection: MongoDB collection to retrieve data from
    :param field: field of the database
    :param output: file to store the resulted image
    :return:
    """
    documents = collection.find({}, {field: 1})
    all_lemmas = " ".join([doc.get(field) for doc in documents])

    wordcloud = WordCloud(background_color="white").generate(all_lemmas)

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(output, dpi=300)
    # plt.show()


def build_new_interaction(
    interpreted_info: Dict[str, Any],
    answer: List,
    user_input: str,
    corrected_user_input: str,
    user_time: datetime,
    response_time: datetime,
) -> Dict[str, Any]:
    """
    Function to create a new entro to the database wth all the relevant info
    created during an interaction with an agent
    :param interpreted_info: dictionary with entities and intent detected
    :param answer: response of the bot to the input of the user
    :param user_input: input of the user as types in the keyboard
    :param corrected_user_input: input the user after the spell checker
    :param user_time: time of the input of the user
    :param response_time: elapsed time between input and response
    """

    # Intent of the user input
    intent = interpreted_info.get("intent")
    # Time used to process the input and answer the user
    request_time = (response_time - user_time).total_seconds()

    return {
        "date_bot": response_time,
        "date_user": user_time,
        "entities": interpreted_info.get("entities"),
        "frame": frame.get_frame_by_intent(intent.get("name")),
        "input_user": user_input,
        "input_user_corrected": corrected_user_input,
        "intent": intent.get("name"),
        "intent_confidence": intent.get("confidence"),
        "is_misunderstood": intent.get("name") is None,
        "output_bot": " ".join(answer),
        "time_request": request_time,
    }


def insert_data(
    interpreted_info: Dict[str, Any],
    answer: List,
    user_input: str,
    corrected_user_input: str,
    ssid: str,
    user_time: datetime,
    response_time: datetime,
    user_type: str,
    conversation_has_finished: bool,
) -> NoReturn:
    """
    Inserts data into MongoDB for future statistics
    :param interpreted_info: dictionary with entities and intent detected
    :param answer: response of the bot to the input of the user
    :param user_input: input of the user as types in the keyboard
    :param corrected_user_input: input the user after the spell checker
    :param ssid: identifier of the user session to track every conversation
    :param user_time: time of the input of the user
    :param response_time: elapsed time between input and response
    :param user_type: admin or user
    :param conversation_has_finished: flag to indicate if a conversation has concluded
    """
    collection = config.SESSIONS_COLL

    # Is the session new?
    session = collection.find_one({"session_id": ssid})

    new_interaction = build_new_interaction(
        interpreted_info,
        answer,
        user_input,
        corrected_user_input,
        user_time,
        response_time,
    )

    # If new session, insert into database
    if session is None:
        collection.insert_one(
            {
                "session_id": ssid,
                "date_start": user_time,
                "disability_visual": False,
                "disability_auditory": False,
                "interactions": [new_interaction],
                "user_type": user_type,
                "is_timeout": False,
            }
        )
    else:
        new_data = {"$push": {"interactions": new_interaction}}
        if conversation_has_finished:
            new_data["$set"] = {"date_end": datetime.now()}

        collection.update({"session_id": ssid}, new_data)


def add_conversation_rate(ssid: str, score: int) -> NoReturn:
    """
    Updates a conversation with the id [ssid] with a score of [score]
    :param ssid: identifier of the session
    :param score: the score for the conversation if it exists
    """
    collection = config.SESSIONS_COLL
    session = collection.find_one({"session_id": ssid})

    if session:
        collection.update(session, {"$set": {"score": score}})


def add_timeout(ssid: str) -> NoReturn:
    """
    Sometimes timeout triggers if a long time has elapsed from
    last interaction with the agent
    :param ssid: identfier of the session
    """
    collection = config.SESSIONS_COLL
    session = collection.find_one({"session_id": ssid})

    if session:
        collection.update(
            session, {"$set": {"is_timeout": True, "date_end": datetime.now()}}
        )
