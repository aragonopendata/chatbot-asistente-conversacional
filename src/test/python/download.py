'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
"""
Main application with every routing needed to handle data
for projects, models, intent, entities, stories and interactions
along with a talk method to chat with a pre-trained agent
"""
import sys
import asyncio
import secrets
import uuid
from flask.helpers import make_response
import requests
from gevent.pywsgi import WSGIServer
import shutil
from flask import Flask, jsonify, request, session

from flask_compress import Compress
from flask_cors import CORS
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.config["JSON_AS_ASCII"] = False
# app.config["APPLICATION_ROOT"] = "/loginchat"

# Initialize extensions
Compress(app)
CORS(app, supports_credentials=True)
Swagger(app)

@app.route("/projects/download", methods=["GET"])
def download_projects():
    if request.method == "GET":
        
        shutil.make_archive("model", 'zip', "./src/test/python/")
        with open("model.zip", "rb") as f:
            headers = {"Content-Disposition": "attachment; filename=model.zip"}
            return make_response(( f.read(), headers))         
  
        
    


@app.route("/")
def hello_world():
    return "hello world"


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5006
    root = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else "/"
    app.config["APPLICATION_ROOT"] = root
    server = WSGIServer(("0.0.0.0", port), app)
    try:
        print(f"Serving on port {port}...")
        server.serve_forever()
    except Exception as e:
        exit(0)
