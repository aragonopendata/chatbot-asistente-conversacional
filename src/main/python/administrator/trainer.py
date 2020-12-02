'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import errno
import logging

from typing import Optional, List, Dict, Any, Tuple, NoReturn
from tqdm import tqdm

from rasa.constants import DEFAULT_CONFIG_PATH
from rasa.core.domain import Domain

from mongo_connector import entities, projects, stories, intents
from utils import json

from collections import defaultdict
from constants import *
import os
import subprocess
import shutil

logger = logging.getLogger(__name__)

here = os.path.dirname(__file__)


def generate_rasa_training_data(project_id, intent_list, desc="smalltalk") -> int:
    """
    Creates a temporary directory to store the intents needed to train
    :return: the total of examples to be trained
    """

    from mongo_connector import intents

    total = 0
    examples = []
    f = open("kk.txt", "w")
    fall="intent,button,entities"

    for intent in tqdm(intent_list, desc=f"[INFO] Processing {desc}"):
        try:
            intent_id = intents.read_id_by_name(project_id, intent)
            exa = intents.read_examples(project_id, intent_id)
            examples.extend(exa)
            total = len(examples)
            if len(exa) > 0:
                exa0 = exa[0]
                fall = fall + "\n" + intent + "," + exa0["text"] + ","
        except TypeError as ex:
            # Intent does not exist, maybe it is not created but in stories or vice versa
            continue
    json.dump(
        {
            "rasa_nlu_data": {
                "common_examples": examples,
                "regex_features": [],
                "lookup_tables": [
                    {
                        "name": "location",
                        "elements": "data/lookup/municipiosaragon.txt"
                    },
                    {
                        "name": "gastronomy_name",
                        "elements": "data/lookup/restaurantes.txt"
                    },
                    {
                        "name": "accomodation_name_big",
                        "elements": "data/lookup/hoteles.txt"
                    },
                    {
                        "name": "accomodation_name",
                        "elements": "data/lookup/hoteles.txt"
                    }
                ],
                "entity_synonyms": [],
            }
        },
        os.path.join(TRAINING_NLU_DATA_DIR, f"training_data.json"),
    )
    f.write(fall)
    f.close()
    return total


def load_smalltalk_domain() -> Domain:
    """
    Returns the domain of smalltalk
    :return: smalltalk's domain
    """

    return Domain.load(SMALLTALK_DOMAIN_PATH)


def split():
    shutil.rmtree(f"{TRAINING_NLU_DATA_DIR}/../../last_trained", ignore_errors=True)
    command = f"rasa data split nlu -u {TRAINING_NLU_DATA_DIR} --out {TRAINING_NLU_DATA_DIR}"
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line)
    process.wait()
    shutil.copytree(TRAINING_DATA_DIR, f"{TRAINING_NLU_DATA_DIR}/../../last_trained/")
    os.remove(f"{TRAINING_NLU_DATA_DIR}/test_data.json")
    return

def evaluate(MODEL_PATH, project_name, model_name):
    print("[INFO] Evaluating model")
    command = f"rasa test nlu -u {TRAINING_NLU_DATA_DIR}/../../last_trained/nlu/test_data.json --model {os.path.join(MODEL_PATH, project_name, model_name)}"
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line)
    process.wait()

class RasaTrainer:
    """ A very simple class to train Rasa both NLU and Core models """

    def __init__(self, project_id, model_id, pipeline=DEFAULT_CONFIG_PATH):

        # Project and model id and names
        self.project_id = project_id
        self.model_id = model_id

        self.project_name = projects.read_project_name_from_id(self.project_id)
        self.model_name = projects.read_model_name_from_id(self.model_id)

        # Load entities data
        self.entities_data, self.stories_data = self.__load_data()

        # Pipeline and policy config for training
        self.pipeline = os.path.join(here, pipeline)

    def __del__(self):
        """
        Remove directory where training data is stored to release some disk space
        :return:
        """
        import shutil

        print("[INFO] Deleting temporary training directory")
        shutil.rmtree(TRAINING_DATA_DIR, ignore_errors=True)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.project_name!r}, {self.model_name!r})"

    def __str__(self):
        return f'RasaTrainer of the project "{self.project_name}" and model "{self.model_name}"'

    def __load_data(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Loads full entities and stories data, gluing entities with values and
        stories with interactions to maximise access efficiency
        """
        entities_data = entities.read(self.project_id, self.model_id)
        for entity in entities_data:
            entity["values"] = entities.read_values(self.project_id, entity["id"])

        stories_data = stories.read(self.project_id, self.model_id)
        if stories_data:
            for story in stories_data:
                story["interactions"] = stories.read_interactions(
                    self.project_id, story["id"]
                )

        return entities_data, stories_data

    def train(self, fixed_model_name: Optional[str] = None) -> NoReturn:
        """
        Trains a model, creating a .tar.gz in the default output folder 'models'
        """
        from rasa import train

        print("[INFO] Creating temporary training directory")
        try:
            os.makedirs(TRAINING_NLU_DATA_DIR)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(TRAINING_NLU_DATA_DIR):
                pass
            else:
                raise

        print("[INFO] Generating Markdown story format")
        intent_list, templates, action_list = self._generate_story_file()
        print(
            f"[INFO] Story file generated with {len(intent_list)} intents, {len(templates)} templates and {len(action_list)} actions"
        )

        # print("[INFO] Merging stories with smalltalk")
        # self._merge_stories()
        print("[INFO] Generating chatbot domain")
        self._generate_domain_file(
            intents=intent_list, templates=templates, actions=action_list
        )

        print("[INFO] Generating training data")
        total = generate_rasa_training_data(
            project_id=self.project_id, intent_list=intent_list, desc="Aragón OpenData"
        )
        print(f"[INFO] Total examples = {total}")

        #print("[INFO] Split train and test data")
        #split()


        # print("[INFO] Combining data with smalltalk")
        # copy_smalltalk_intents(project_id=self.project_id)

        print(f"[INFO] Training model {self.__str__()}")
        train(
            domain=os.path.join(TRAINING_DATA_DIR, DEFAULT_DOMAIN_PATH),
            config=self.pipeline,
            output=os.path.join(MODEL_PATH, self.project_name, self.model_name),
            training_files=TRAINING_NLU_DATA_DIR,
            fixed_model_name=fixed_model_name,
        )
        #evaluate(MODEL_PATH, self.project_name, self.model_name)


    # noinspection PyShadowingNames
    def _generate_domain_file(
        self, intents: list, templates: dict, actions: list
    ) -> NoReturn:
        """
        Generated the domain file for an agent, merging it with the already trained
        domain of the smalltalk set of intents
        :return:
        """
        from rasa.core.slots import TextSlot
        from rasa.core.domain import Domain

        # Get entities that appears in any intent to be trained
        entities = set()
        for entity in self.entities_data:
            if any(
                intent in [x["name"] for x in entity["intents"]] for intent in intents
            ):
                entities.add(entity["name"])

        # Save domain
        domain_path = os.path.join(TRAINING_DATA_DIR, DEFAULT_DOMAIN_PATH)
        domain = Domain(
            intents=intents,
            entities=list(entities),
            templates=dict(templates),
            slots=[TextSlot(entity) for entity in list(entities)],
            action_names=[*dict(templates)] + actions,
            form_names=[],
        )

        domain.persist(domain_path)

    def _generate_story_file(self) -> Tuple[List[str], Dict[str, List[Any]], List[str]]:
        """
        Generates a stories file with a format readable for Rasa
        :return:
        """
        from mongo_connector import intents

        intents_set = set()
        templates_dict = defaultdict(list)
        actions_set = set()

        # Persist dicionary data as Rasa Markdown story format
        with open(
            os.path.join(TRAINING_NLU_DATA_DIR, "stories.md"), mode="w", encoding="utf8"
        ) as md:
            # For each story, dump in md format
            for story in self.stories_data:
                interactions = story["interactions"]
                if interactions and len(interactions) > 0:
                    # Write header story
                    md.write(f'## Story {story["name"]}\n')

                    # Dump every interaction of the story
                    for interaction in interactions:
                        if all([interaction[x] for x in ["intent", "actions"]]):
                            intent = interaction["intent"]
                            text = interaction.get("text", None)
                            actions = interaction["actions"]

                            # Add intent to the set
                            intents_set.add(intent)

                            # Write intent into story
                            md.write(f"*{intent}\n")
                            # Iterate over actions_module
                            last_action = ""
                            for action in actions:
                                # If it is an utter, save template into the dict for the domain creation
                                # Write the utter into the story markdown file
                                if action["type"] == "utter":
                                    template = "utter_" + intent
                                    templates_dict[template].append(
                                        {"text": action["value"]}
                                    )
                                    if last_action != template:
                                        md.write(f"\t- {template}\n")
                                        last_action = template
                                # If it is an action, save it to the story file
                                elif action["type"] == "action":
                                    actions_set.add(action["value"])
                                    md.write(f"\t- {action['value']}\n")

                        elif interaction["intent"] is None:  # Is fallback
                            action = interaction["actions"][0]

                            templates_dict["utter_default"].append(
                                {"text": action["value"]}
                            )
                            md.write("\t- utter_default\n")

                md.write("\n")
        actions_set.add("action_fallback_ita")
        return list(intents_set), templates_dict, list(actions_set)

    @staticmethod
    def _merge_stories() -> NoReturn:
        """ Rewrites stories file to include the smalltalk data """
        with open(
            os.path.join(TRAINING_NLU_DATA_DIR, "stories.md"), mode="a", encoding="utf8"
        ) as f:
            f.write(open(SMALLTALK_STORIES_PATH, encoding="utf8").read())
