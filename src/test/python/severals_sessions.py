"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import requests
import time
from cmd import *
from pymongo import MongoClient
from pprint import pprint



NODE_URL = "http://127.0.0.1:3001"
BACKEND_URL = "http://127.0.0.1:5006"
CHAT_ROOM_URL = "http://127.0.0.1:5000"
ACTION_SERVER_URL = "http://127.0.0.1:5055"
NER_SERVER_URL = (
    "http://127.0.0.1:4999/ner?words=Quien es el alcalde de Añon.&other=True"
)
MONGO_URL = "mongodb://127.0.0.1:27017/"

response_ok="El alcalde de Zaragoza es Jorge Antonio Azcon Navarro"


def test_chat_room():
    """
    Test of chat room: connectivity, agent status and input processing
    """
    response = requests.get(CHAT_ROOM_URL)
    if response.status_code == 200:
        #print_passed("Chat room is running")
        pass
    else:
        print_failed("Error in administrator Flask server")
        exit(-1)

    response_status = requests.get(CHAT_ROOM_URL + "/status")
    json_response = response_status.json()
    if json_response["status"] == 200:
        #print_passed("Chat room agent is running")
        pass
    else:
        print_failed("Error chat room agent, agent not ready")
        exit(-1)

    cookies_dict = response.cookies.get_dict()
    if cookies_dict:
        response = requests.post(
            CHAT_ROOM_URL + "/chat",
            cookies=cookies_dict,
            json={"text": "Quien es el alcalde de Zaragoza", "timeout": False},
        )
        if response.status_code == 200:
            json_response = response.json()
            if len(json_response["answer"]) > 0 and json_response["answer"][1]== response_ok:
                #print_passed("Chat room input is running")
                pass
            else:
                print_failed("Error chat room input,{json_response["answer"][1]} ")
                exit(-1)
        else:
            print_failed(f"Error chat room input, status code={response.status_code}")
            exit(-1)
