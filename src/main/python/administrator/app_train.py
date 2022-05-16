"""
Chat train, it trains the model applying data from the MongoDB database
"""

import sys

from flask import Flask, jsonify
from flask_compress import Compress
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

from trainer import RasaTrainer

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

Compress(app)
CORS(app)


@app.route("/projects/<project>/models/<model>/train", methods=["GET"])
def train(project, model):
    rasa_trainer = RasaTrainer(project_id=project, model_id=model)
    try:
        rasa_trainer.train()
    except Exception:
        return jsonify({"msg": "Trained incomplete"})
    finally:
        del rasa_trainer

    return jsonify({"msg": "Trained successfully"})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5008
    server = WSGIServer(("0.0.0.0", port), app)
    try:
        print(f"Serving on port {port}...")
        server.serve_forever()
    except Exception as e:
        exit(0)
