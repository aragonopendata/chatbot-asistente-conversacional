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

import asyncio
import secrets
import uuid
from flask.helpers import make_response
import requests
import bot_statistics as bs
import datetime
import sys

from gevent.pywsgi import WSGIServer
from bot import Bot

from mongo_connector import projects, stories, entities, intents

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

bot = Bot(user_type="admin")


#################################
############ INTENTS ############
#################################

# TODO: Entidades desde los textos de las interacciones, formato MD []()


@app.route("/projects/<project>/models/<model>/intents", methods=["GET", "POST"])
@swag_from("specs/intents/intents_get.yml", methods=["GET"])
@swag_from("specs/intents/intents_post.yml", methods=["POST"])
def intents_get(project, model):
    if request.method == "POST" and type(request.get_json()) is list:
        intents.create(
            intent_list=request.get_json(), project_id=project, model_id=model
        )

    return jsonify(intents.read(project_id=project, model_id=model))


@app.route(
    "/projects/<project>/models/<model>/intents/<id_intent>",
    methods=["GET", "DELETE", "PATCH"],
)
@swag_from("specs/intents/intent_get.yml", methods=["GET"])
@swag_from("specs/intents/intent_delete.yml", methods=["DELETE"])
@swag_from("specs/intents/intent_patch.yml", methods=["PATCH"])
def intent_get(project, model, id_intent):
    if request.method == "DELETE":
        intents.delete(intent_id=id_intent, project_id=project, model_id=model)
        entities.remove_intent(intent_id=id_intent, project_id=project, model_id=model)
        return jsonify(intents.read(project_id=project, model_id=model))

    if request.method == "PATCH":
        intents.update(
            intent_id=id_intent,
            params=request.get_json(),
            project_id=project,
            model_id=model,
        )

    # return jsonify(intents.read_data_by_id(project_id=project, model_id=model, intent_id=id_intent))
    return jsonify(intents.read(project_id=project, model_id=model))


@app.route(
    "/projects/<project>/models/<model>/intents/<id_intent>/templates",
    methods=["GET", "POST"],
)
@swag_from("specs/intents/intent_new_templates.yml", methods=["POST"])
def intent_template_create(project, model, id_intent):
    if type(request.get_json()) is list:
        intents.create_templates(
            intent_id=id_intent,
            template_list=request.get_json(),
            project_id=project,
            model_id=model,
        )

    return jsonify(
        intents.read_templates(intent_id=id_intent, project_id=project, model_id=model)
    )


@app.route(
    "/projects/<project>/models/<model>/intents/<id_intent>/templates/<id_template>",
    methods=["PATCH", "DELETE"],
)
@swag_from("specs/intents/intent_patch_template.yml", methods=["PATCH"])
@swag_from("specs/intents/intent_delete_template.yml", methods=["DELETE"])
def intent_template_update(project, model, id_intent, id_template):
    if request.method == "DELETE":
        intents.delete_template(
            intent_id=id_intent,
            template_id=id_template,
            project_id=project,
            model_id=model,
        )

    if request.method == "PATCH":
        intents.update_template(
            intent_id=id_intent,
            template_id=id_template,
            params=request.get_json(),
            project_id=project,
            model_id=model,
        )

    return jsonify(
        intents.read_templates(intent_id=id_intent, project_id=project, model_id=model)
    )


@app.route(
    "/projects/<project>/models/<model>/intents/<id_intent>/examples", methods=["GET"]
)
@swag_from("specs/intents/intent_examples.yml", methods=["GET"])
def intent_templates_examples(project, model, id_intent):
    return jsonify(intents.read_examples(intent_id=id_intent, project_id=project))


@app.route(
    "/projects/<project>/models/<model>/intents/<id_intent>/templates/<id_template>/examples",
    methods=["GET"],
)
@swag_from("specs/intents/intent_template_examples.yml", methods=["GET"])
def intent_template_examples(project, model, id_intent, id_template):
    return jsonify(
        intents.read_examples(
            intent_id=id_intent, template_id=id_template, project_id=project
        )
    )


##################################
############ ENTITIES ############
##################################


@app.route("/projects/<project>/models/<model>/entities", methods=["GET", "POST"])
@swag_from("specs/entities/entities_get.yml", methods=["GET"])
@swag_from("specs/entities/entities_post.yml", methods=["POST"])
def entities_get(project, model):
    if request.method == "POST":
        if type(request.get_json()) is list:
            entities.create(
                project_id=project, model_id=model, entity_list=request.get_json()
            )

    return jsonify(entities.read(project_id=project, model_id=model))


@app.route(
    "/projects/<project>/models/<model>/entities/<id_entity>",
    methods=["GET", "DELETE", "PATCH"],
)
@swag_from("specs/entities/entity_get.yml", methods=["GET"])
@swag_from("specs/entities/entity_patch.yml", methods=["PATCH"])
@swag_from("specs/entities/entity_delete.yml", methods=["DELETE"])
def entity_get(project, model, id_entity):
    if request.method == "DELETE":
        entities.delete(project_id=project, model_id=model, entity_id=id_entity)
        return jsonify(entities.read(project_id=project, model_id=model))

    if request.method == "PATCH":
        entities.update(
            project_id=project,
            model_id=model,
            entity_id=id_entity,
            params=request.get_json(),
        )

    # return jsonify(entities.read_data_by_id(project_id=project, model_id=model, entity_id=id_entity))
    return jsonify(entities.read(project_id=project, model_id=model))


@app.route(
    "/projects/<project>/models/<model>/entities/<id_entity>/values",
    methods=["GET", "POST"],
)
@swag_from("specs/entities/entity_get_values.yml", methods=["GET"])
@swag_from("specs/entities/entity_add_values.yml", methods=["POST"])
def entity_values(project, model, id_entity):
    if request.method == "POST":
        if type(request.get_json()) is list:
            entities.create_values(
                project_id=project,
                model_id=model,
                entity_id=id_entity,
                value_list=request.get_json(),
            )

    return jsonify(entities.read_values(project_id=project, entity_id=id_entity))


@app.route(
    "/projects/<project>/models/<model>/entities/<id_entity>/values/<id_value>",
    methods=["DELETE", "PATCH"],
)
@swag_from("specs/entities/entity_delete_value.yml", methods=["DELETE"])
@swag_from("specs/entities/entity_patch_value.yml", methods=["PATCH"])
def entity_value_update(project, model, id_entity, id_value):
    if request.method == "DELETE":
        entities.delete_value(
            project_id=project, model_id=model, entity_id=id_entity, value_id=id_value
        )

    if request.method == "PATCH":
        entities.update_value(
            project_id=project,
            model_id=model,
            entity_id=id_entity,
            value_id=id_value,
            params=request.get_json(),
        )

    return jsonify(entities.read_values(project_id=project, entity_id=id_entity))


#################################
############ STORIES ############
#################################


@app.route("/projects/<project>/models/<model>/stories", methods=["GET", "POST"])
@swag_from("specs/stories/stories_get.yml", methods=["GET"])
@swag_from("specs/stories/stories_post.yml", methods=["POST"])
def stories_get(project, model):
    if request.method == "POST":
        stories.create(project, model, request.get_json())

    return jsonify(stories.read(project_id=project, model_id=model))


@app.route(
    "/projects/<project>/models/<model>/stories/<id_story>",
    methods=["GET", "DELETE", "PATCH"],
)
@swag_from("specs/stories/story_get.yml", methods=["GET"])
@swag_from("specs/stories/story_patch.yml", methods=["PATCH"])
@swag_from("specs/stories/story_delete.yml", methods=["DELETE"])
def story_create(project, model, id_story):
    if request.method == "DELETE":
        stories.delete(project_id=project, model_id=model, story_id=id_story)
        return jsonify(stories.read(project_id=project, model_id=model))

    if request.method == "PATCH":
        stories.update(
            project_id=project,
            model_id=model,
            story_id=id_story,
            params=request.get_json(),
        )

    # return jsonify(stories.read_by_id(project_id=project, model_id=model, story_id=id_story))
    return jsonify(stories.read(project_id=project, model_id=model))


@app.route(
    "/projects/<project>/models/<model>/stories/<id_story>/interactions",
    methods=["GET", "POST"],
)
@swag_from("specs/stories/story_get_interactions.yml", methods=["GET"])
@swag_from("specs/stories/story_post_interactions.yml", methods=["POST"])
def story_new_interaction(project, model, id_story):
    if request.method == "POST":
        stories.create_interaction(
            project_id=project, model_id=model, story_id=id_story
        )

    return jsonify(
        stories.read_interactions(project_id=project, story_id=id_story)
    )


@app.route(
    "/projects/<project>/models/<model>/stories/<id_story>/interactions/<id_interaction>",
    methods=["PATCH", "DELETE"],
)
@swag_from("specs/stories/story_patch_interaction.yml", methods=["PATCH"])
@swag_from("specs/stories/story_delete_interaction.yml", methods=["DELETE"])
def story_patch_interaction(project, model, id_story, id_interaction):
    if request.method == "PATCH":
        stories.update_interaction(
            project_id=project,
            model_id=model,
            story_id=id_story,
            interaction_id=id_interaction,
            params=request.get_json(),
        )

    if request.method == "DELETE":
        stories.delete_interaction(
            project_id=project,
            model_id=model,
            story_id=id_story,
            interaction_id=id_interaction,
        )

    return jsonify(
        stories.read_interactions(project_id=project, story_id=id_story)
    )


################################
############ AGENTS ############
################################
@app.route("/projects/download", methods=["GET"])
@swag_from("specs/projects/projects_download.yml", methods=["GET"])
def download_projects():
    if request.method == "GET":

        from trainer import RasaTrainer
        project_id = projects.read_project_id_from_name("GDA")
        model_id = projects.read_model_id_from_name("AOD")
        rasa_trainer = RasaTrainer(project_id=project_id, model_id=model_id)
        try:
            rasa_trainer.generate()
        except:
            pass
        projects.download_training_project()
        with open("model.zip", "rb") as f:
            headers = {"Content-Disposition": "attachment; filename=model.zip"}
            return make_response(( f.read(), headers))



@app.route("/projects", methods=["GET", "POST"])
@swag_from("specs/projects/projects_get.yml", methods=["GET"])
@swag_from("specs/projects/projects_post.yml", methods=["POST"])
def get_projects():
    if request.method == "POST":
        projects.create(request.get_json())
    return jsonify(projects.read())


@app.route("/projects/<project>", methods=["DELETE", "PATCH"])
@swag_from("specs/projects/project_delete.yml", methods=["DELETE"])
@swag_from("specs/projects/project_update.yml", methods=["PATCH"])
def delete_project(project):
    if request.method == "DELETE":
        projects.delete(project_id=project)

    if request.method == "PATCH":
        projects.update(project_id=project, params=request.get_json())

    return jsonify(projects.read())


@app.route("/projects/<project>/models", methods=["GET", "POST", "DELETE"])
@swag_from("specs/projects/project_models_get.yml", methods=["GET"])
@swag_from("specs/projects/project_models_post.yml", methods=["POST"])
# @swag_from('specs/projects/project_models_delete.yml', methods=['DELETE'])
def agents_get_models(project):
    session["sid"] = uuid.uuid4().hex
    if request.method == "POST":
        projects.create_model(project_id=project, model_list=request.get_json())

    if request.method == "DELETE":
        projects.delete_models(project_id=project)

    return jsonify(projects.read_models(project_id=project))


@app.route("/projects/<project>/models/<model>", methods=["DELETE", "PATCH"])
@swag_from("specs/projects/project_model_delete.yml", methods=["DELETE"])
@swag_from("specs/projects/project_model_update.yml", methods=["PATCH"])
def agent_delete_model(project, model):
    if request.method == "DELETE":
        projects.delete_model(project_id=project, model_id=model)

    if request.method == "PATCH":
        projects.update_model(
            project_id=project, model_id=model, params=request.get_json()
        )

    return jsonify(projects.read_models(project_id=project))


@app.route("/projects/<project>/models/<model>/load", methods=["GET"])
@swag_from("specs/projects/project_agent_load.yml", methods=["GET"])
def agent_load(project, model):
    try:
        global bot
        bot = bot.load(
            project=projects.read_project_name_from_id(project),
            model=projects.read_model_name_from_id(model),
        )
        return jsonify({"msg": "Bot successfully loaded"})
    except Exception as ex:
        return jsonify({"msg": ex})


@app.route("/projects/<project>/models/<model>/chats", methods=["POST"])
@swag_from("specs/projects/project_agent_talk.yml", methods=["POST"])
def agent_talk(project, model):
    request_data = request.get_json()
    answer, icons, conversation_has_finished = asyncio.get_event_loop().run_until_complete(
        bot.chat(
            project=projects.read_project_name_from_id(project),
            model=projects.read_model_name_from_id(model),
            user_input=request_data["text"],
            user_time=datetime.datetime.now(),
            ssid=session["sid"]
            # print_info=True,
        )
    )

    # If timeout popped, we return an empty answer,
    # gui won't matter about this but we avoid errors
    # Session id is resetted for next conversation
    last_session_id = session["sid"]
    if request_data["timeout"]:
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

    return jsonify(
        {
            "answer": answer,
            "icons": icons,
            "conversation_ended": conversation_has_finished,
            "session_id": last_session_id,
        }
    )


@app.route("/projects/<project>/models/<model>/score", methods=["GET", "POST"])
@swag_from("specs/projects/score_conversation.yml", methods=["POST"])
def conversation_rating(project, model):
    request_data = request.get_json()
    bs.add_conversation_rate(request_data["session_id"], request_data["score"])

    return jsonify({"msg": "Score inserted"})


#################
#### ACTIONS ####
#################


@app.route("/actions", methods=["GET"])
@swag_from("specs/actions/actions_get.yml", methods=["GET"])
def get_actions():
    response = requests.get("http://rasa:5055/actions")

    response.raise_for_status()
    content = response.json()

    return jsonify([x["name"] for x in content])


##############################
########### MAIN #############
##############################


@app.route("/")
def hello_world():
    return ""


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
