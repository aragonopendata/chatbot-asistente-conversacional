"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
"""
Chat application, it serves a chat room with a pre-trained agent
ready to talk about diferent topics about Aragon:
It currently covers tourism, accommodation, citizen info, farming,
activities, environment and a little smalltalk

The app covers also the scoring of a conversation and a status route
to debug agent status
"""

import asyncio
import logging
import secrets

import  os

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


import bot_statistics as bs
import datetime
import sys
import uuid
import config
from bot import Bot

from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, jsonify, request, session
from flask_compress import Compress
from flask_cors import CORS
from loguru import logger

from utils.middleware import PrefixMiddleware

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["JSON_AS_ASCII"] = False
app.config["DEBUG"] = True
app.url_map.strict_slashes = False

# Initialize extensions
Compress(app)
CORS(app, supports_credentials=True)
print("starting...")
bot = Bot()
print("initing..")

# create a custom handler
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


@app.route("/status", methods=["GET"])
def status():
    ready = bot.is_ready()
    if ready:
        logger.info("Agent ready to talk")
        return jsonify({"status": 200, "information": "Agent ready to talk"})
    else:
        logger.error("Agent not ready")
        return jsonify({"status": 500, "information": "Agent not ready"})


@app.route("/score", methods=["GET", "POST"])
def conversation_rating():
    request_data = request.get_json()
    bs.add_conversation_rate(request_data["session_id"], request_data["score"])

    return jsonify({"msg": "Score inserted"})


@app.route("/chat", methods=["POST"])
def chat():
    request_data = request.get_json()
    text=request_data["text"]
    if (not str(text).startswith(("/"))):
        a, b = 'áéíóú', 'aeiou'
        trans = str.maketrans(a, b)
        textlower = str(text).lower()
        textlower = textlower.translate(trans)
        textlower = textlower.strip()
        if textlower in  config.ONE_WORD_REQUEST:
            text= config.ONE_WORD_REQUEST[textlower]

    answer, icons, conversation_has_finished,buttons = asyncio.get_event_loop().run_until_complete(
        bot.chat(
            user_input=text,
            user_time=datetime.datetime.now(),
            ssid=session["sid"]
            # print_info=True,
        )
    )

    # If timeout popped, we return an empty answer,
    # gui won't matter about this but we avoid errors
    # Session id is resetted for next conversation
    last_session_id = session["sid"]
    if "timeout" in request_data and request_data["timeout"]:
        bs.add_timeout(session["sid"])
        session["sid"] = uuid.uuid4().hex
        return jsonify(
            {
                "answer": answer,
                "conversation_ended": True,
                "session_id": last_session_id,
            }
        )

    if conversation_has_finished:
        session["sid"] = uuid.uuid4().hex

    if len(buttons)>0:
        buttons=buttons[0]

    if str(answer).find('{name}')>-1:
        answer[0] = answer[0].replace('{name}','')

    return jsonify(
        {
            "answer": answer,
            "icons": icons,
            "buttons":buttons,
            "conversation_ended": conversation_has_finished,
            "session_id": last_session_id,
        }
    )


@app.route("/", methods=["GET"])
def index():
    session["sid"] = uuid.uuid4().hex
    return render_template("index.html")


def init_logger():
    logger.start(
        "app_chat.log", level="INFO"
    )  # , format="[{time}] {level} - {message}")
    logger.level("INFO", color="<blue>")
    app.logger.addHandler(InterceptHandler())


if __name__ == "__main__":
    ''' 
    geventOpt = {'GATEWAY_INTERFACE': 'CGI/1.1',
                'SCRIPT_NAME': '',
                'wsgi.version': (1, 0),
                'wsgi.multithread': True, 
                'wsgi.multiprocess': True,
                'wsgi.run_once': False}
    '''
    #init_logger()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    root = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else ""
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=root)
    server = WSGIServer(("0.0.0.0", port), app)#, environ=geventOpt)
    try:
        print(
            f"Serving on port {port}"
            + (f" and application root '{root}'..." if root else "...")
        )
        server.serve_forever()
    except Exception as e:
        exit(0)
