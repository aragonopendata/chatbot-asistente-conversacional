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

from rasa.shared.constants import DEFAULT_CONFIG_PATH
from rasa.shared.core.domain import Domain

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
    #jvea convert json to  md

    from rasa.nlu.convert import convert_training_data

    from mongo_connector import intents

    total = 0
    examples = []
    #f = open("kk.txt", "w")
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
                        "elements": "./data/lookup/municipiosaragon.txt"
                    },
                    {
                        "name": "gastronomy_name",
                        "elements": "./data/lookup/restaurantes.txt"
                    },
                    {
                        "name": "accomodation_name_big",
                        "elements": "./data/lookup/hoteles.txt"
                    },
                    {
                        "name": "accomodation_name",
                        "elements": "./data/lookup/hoteles.txt"
                    }],

                "entity_synonyms": [],
            }

        },
        os.path.join(TRAINING_NLU_DATA_DIR, f"training_data.json"),
    )

    #f.write(fall)
    #f.close()
    #@jvea convert json to  md
    import yaml

    forms = open(    DEFAULT_FORMS_PATH, mode="r", encoding="utf8" )
    forms_dict_training_data = yaml.load(forms, Loader=yaml.FullLoader)

    rules = open(    DEFAULT_RULES_PATH, mode="r", encoding="utf8" )
    rules_dict_training_data = yaml.load(rules, Loader=yaml.FullLoader)

    #print("form training data")
    #print(forms_dict_training_data)

    convert_training_data(
        data_file=os.path.join(TRAINING_NLU_DATA_DIR, f"training_data.json") ,
        out_file=os.path.join(TRAINING_NLU_DATA_DIR, f"training_data.md"),
         output_format="md", language="es")

    print(f" remove {TRAINING_NLU_DATA_DIR}/training_data.json")
    os.remove(f"{TRAINING_NLU_DATA_DIR}/training_data.json")

    print("training data -> "+os.path.join(TRAINING_NLU_DATA_DIR, f"training_data.md"))
    convertNluMd2Yaml()

    cur_yaml=None

    with open(os.path.join(TRAINING_NLU_DATA_DIR, f"training_data.yml"),'r' , encoding="utf8" ) as yamlfile:
        cur_yaml = yaml.safe_load(yamlfile) # Note the safe_load
        #print("file training data")
        #print(cur_yaml)
        cur_yaml["nlu"].extend(forms_dict_training_data["nlu"])
        cur_yaml.update(rules_dict_training_data)
        #print("add to file training data")
        #print(cur_yaml)
        #cur_yaml['xxx'].update(forms_dict_training_data)

    if cur_yaml:
        with open(os.path.join(TRAINING_NLU_DATA_DIR, f"training_data.yml"),'w', encoding="utf8" ) as yamlfile:
            yaml.safe_dump(cur_yaml, yamlfile,default_flow_style=False, sort_keys=False) # Also note the safe_dump
            #print("add to file training data")
            #print(cur_yaml)

    forms.close()
    rules.close()

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


def convertMd2Yaml():
    """ transform markdown to yaml files
    """
    """
    command = f"rasa data convert core -f yaml --data={TRAINING_NLU_DATA_DIR} --out={TRAINING_NLU_DATA_DIR}"
    print("convertMd2Yaml->" +command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line)
    process.wait()

    os.remove(f"{TRAINING_NLU_DATA_DIR}/stories.md")
    print(f"delete file {TRAINING_NLU_DATA_DIR}/stories.md" )
    os.rename(f"{TRAINING_NLU_DATA_DIR}/stories_converted.yml", f"{TRAINING_NLU_DATA_DIR}/stories.yml")
    print(f"rename to file {TRAINING_NLU_DATA_DIR}/stories.yml" )





    forms = open(    DEFAULT_FORMS_PATH, mode="r", encoding="utf8" )
    story_dict_training_data = yaml.load(forms, Loader=yaml.FullLoader)


    cur_yaml=None

    with open(os.path.join(TRAINING_NLU_DATA_DIR, f"stories.yml"),'r' , encoding="utf8" ) as yamlfile:
        cur_yaml = yaml.safe_load(yamlfile) # Note the safe_load
        print("file training data")
        #print(cur_yaml)
        cur_yaml["stories"].append(story_dict_training_data["stories"][0])
    #solo tenemos reglas de formularios
    os.remove(f"{TRAINING_NLU_DATA_DIR}/stories.yml")
    """
    import yaml
    forms = open(    DEFAULT_FORMS_PATH, mode="r", encoding="utf8" )
    story_dict_training_data = yaml.load(forms, Loader=yaml.FullLoader)
    forms.close()

    if story_dict_training_data:

        with open(os.path.join(TRAINING_NLU_DATA_DIR, f"stories.yml"),'w', encoding="utf8" ) as yamlfile:
            yaml.safe_dump(story_dict_training_data["stories"], yamlfile,default_flow_style=False, sort_keys=False) # Also note the safe_dump
        #print("add to file story")
        #print(cur_yaml)

    forms.close()


def convertNluMd2Yaml():
    """ transform markdown to yaml files
    """

    #shutil.rmtree(f"{TRAINING_NLU_DATA_DIR}/../../last_trained", ignore_errors=True)
    command = f"rasa data convert nlu -f yaml --data={TRAINING_NLU_DATA_DIR} --out={TRAINING_NLU_DATA_DIR}"
    print("convertNluMd2Yaml->" +command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
        print(line)
    process.wait()
    #shutil.copytree(TRAINING_DATA_DIR, f"{TRAINING_NLU_DATA_DIR}/../../last_trained/")
    os.remove(f"{TRAINING_NLU_DATA_DIR}/training_data.md")
    os.rename(f"{TRAINING_NLU_DATA_DIR}/training_data_converted.yml", f"{TRAINING_NLU_DATA_DIR}/training_data.yml")


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

        #print("[INFO] Deleting temporary training directory")
        #shutil.rmtree(TRAINING_DATA_DIR, ignore_errors=True)

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

        self.generate(fixed_model_name)
        self.training(fixed_model_name)

    def generate(self, fixed_model_name: Optional[str] = None) -> NoReturn:
        """
        Generate files to create a model, creating default output folder 'data/training'
        """
        from rasa import train

        print(f"[INFO] Creating temporary training directory in {TRAINING_NLU_DATA_DIR}")
        try:
            os.makedirs(TRAINING_NLU_DATA_DIR)
        except OSError as exc:
            if exc.errno != errno.EEXIST or not os.path.isdir(
                TRAINING_NLU_DATA_DIR
            ):
                raise

        print("[INFO] Generating Markdown story format")
        #intent_list, templates, action_list ,forms = self._generate_story_file()
        intent_list, templates, action_list ,forms = self._generate_rules_file()
        print(
            f"[INFO] Story file generated with {len(intent_list)} intents, {len(templates)} templates and {len(action_list)} actions"
        )

        # print("[INFO] Merging stories with smalltalk")
        # self._merge_stories()
        print("[INFO] Generating chatbot domain")
        self._generate_domain_file(
            intents=intent_list, templates=templates, actions=action_list, forms=forms
        )

        convertMd2Yaml()
        #convertNluMd2Yaml()
        print(f"[INFO] list files in {TRAINING_NLU_DATA_DIR}")
        for file in os.listdir(TRAINING_NLU_DATA_DIR):
            print(f"[INFO] {file}")

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
        print(f"[INFO] training_files  {TRAINING_NLU_DATA_DIR}")
        print(f"[INFO] Domain  {os.path.join(TRAINING_DATA_DIR, DEFAULT_DOMAIN_PATH)}")
        print(f"[INFO] fixed_model_name  {fixed_model_name}")
        print(f"[INFO] output  {os.path.join(MODEL_PATH, self.project_name, self.model_name)}")


    def training(self, fixed_model_name: Optional[str] = None) -> NoReturn:
        """
        Trains a model, creating a .tar.gz in the default output folder 'models'
        """
        from rasa import train

        train(
            domain=os.path.join(TRAINING_DATA_DIR, DEFAULT_DOMAIN_PATH),
            config=self.pipeline,
            output=os.path.join(MODEL_PATH, self.project_name, self.model_name),
            training_files=TRAINING_NLU_DATA_DIR
        )



    # noinspection PyShadowingNames
    def _generate_domain_file(
        self, intents: list, templates: dict, actions: list, forms:dict
    ) -> NoReturn:

        """
        Generated the domain file for an agent, merging it with the already trained
        domain of the smalltalk set of intents
        :return:
        """



        from rasa.shared.core.slots import TextSlot
        from rasa.shared.core.domain import Domain

        # Get entities that appears in any intent to be trained
        entities = set()
        for entity in self.entities_data:
            if any(
                intent in [x["name"] for x in entity["intents"]] for intent in intents
            ):
                entities.add(entity["name"])
        # convert entities to slots
        slots=[TextSlot(entity) for entity in list(entities)]

        print("add slots to domain")
        import yaml
        with open(
            DEFAULT_FORMS_PATH, mode="r", encoding="utf8"
        ) as forms_2:
            forms_dict = yaml.load(forms_2, Loader=yaml.FullLoader)
            print(forms_dict["slots"])
            #slots= slots + forms_dict["slots"]
            for slot in forms_dict["slots"]:
                print(forms_dict["slots"][slot])

                slots.append(TextSlot(slot,auto_fill=forms_dict["slots"][slot]["auto_fill"],influence_conversation=forms_dict["slots"][slot]["influence_conversation"] ))
        print("all slots", slots)
        # read forms slots to add to domain

        # Save domain
        domain_path = os.path.join(TRAINING_DATA_DIR, DEFAULT_DOMAIN_PATH)
        domain = Domain(
            intents=intents,
            entities=list(entities),
            #templates=dict(templates),@jvea
            slots=slots,
            action_names=[*dict(templates)] + actions,
            #form_names=[], @jvea
            responses=dict(templates),
            forms=dict(forms)
        )

        domain.persist(domain_path)

    def _generate_story_file(self) -> Tuple[List[str], Dict[str, List[Any]], List[str], Dict[str, List[Any]]]:
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

        import yaml

        with open(
            DEFAULT_FORMS_PATH, mode="r", encoding="utf8"
        ) as forms:
            forms_dict = yaml.load(forms, Loader=yaml.FullLoader)
            templates_dict  = {**forms_dict["responses"], **templates_dict}
            #print ("template->")
            #print (templates_dict)

            #print ("intent->")
            #print (intent)
            #read_intent = {}
            #print (f'intent-> add {forms_dict["nlu"]["intent"]}')
            for intent in forms_dict["nlu"]:
                intents_set.add(intent["intent"])
            '''
            for intent in forms_dict["nlu"]:
                #print (intent)
                #read_intent=
                print (f'intent-> add {intent[intent]}')
                intents_set.add( intent["intent"])
                print (f'intent-> add {intent["intent"]}')
                #for text in intent["examples"]:
                #    print (text)
                #    intent.add(text)
            #print (templates_dict)
            '''
        print ("Generate file story in -> "+os.path.join(TRAINING_NLU_DATA_DIR, "stories.md"))
        #print ("forms")
        #print (forms_dict["forms"])

        #print ("intents_set")
        #print (list(intents_set))

        #print ("actions_set")
        #print (list(actions_set))

        return list(intents_set), templates_dict, list(actions_set), forms_dict["forms"]


    def _generate_rules_file(self) -> Tuple[List[str], Dict[str, List[Any]], List[str], Dict[str, List[Any]]]:
        """
        Generates a stories file with a format readable for Rasa
        :return:
        """
        import yaml

        cur_yaml=None
        with open(
           DEFAULT_RULES_PATH, mode="r", encoding="utf8"
        ) as file_rules:
            cur_yaml = yaml.load(file_rules, Loader=yaml.FullLoader)


        from mongo_connector import intents

        intents_set = set()
        templates_dict = defaultdict(list)
        actions_set = set()

        #rules=[]
        #cur_yaml = {"rules":rules}
        rules = cur_yaml["rules"]
        print ("*** create rules ")
        print (f"rules {rules}")
        # For each story, dump in md format
        for story in self.stories_data:
            interactions = story["interactions"]
            if interactions and len(interactions) > 0:

                # Dump every interaction of the story
                for interaction in interactions:
                    if all([interaction[x] for x in ["intent", "actions"]]):

                        intent = interaction["intent"]
                        text = interaction.get("text", None)
                        actions = interaction["actions"]


                        # Add intent to the set
                        intents_set.add(intent)

                        last_action = ""
                        for action in actions:
                            # If it is an utter, save template into the dict for the domain creation
                            # Write the utter into the story markdown file
                            if action["type"] == "utter":
                                template = "utter_" + intent
                                rules.append({"rule":f"rule {intent}","steps":[{"intent":intent},{"action":"utter_" + intent}]})
                                templates_dict[template].append(
                                    {"text": action["value"]}
                                )
                                if last_action != template:
                                    last_action = template
                            # If it is an action, save it to the story file
                            elif action["type"] == "action":
                                actions_set.add(action["value"])
                                rules.append({"rule":f"rule {intent}","steps":[{"intent":intent},{"action":actions[0]["value"]}]})

                    elif interaction["intent"] is None:  # Is fallback
                        action = interaction["actions"][0]

                        templates_dict["utter_default"].append(
                            {"text": action["value"]}
                        )


        actions_set.add("action_fallback_ita")

        with open(os.path.join(TRAINING_NLU_DATA_DIR, f"rules.yml"),'w', encoding="utf8" ) as yamlfile:
            yaml.safe_dump(cur_yaml, yamlfile,default_flow_style=False, sort_keys=False)


        with open(
            DEFAULT_FORMS_PATH, mode="r", encoding="utf8"
        ) as forms:
            forms_dict = yaml.load(forms, Loader=yaml.FullLoader)
            templates_dict  = {**forms_dict["responses"], **templates_dict}
            actions_set |= set(forms_dict["actions"]) # add set list
            #print ("template->")
            #print (templates_dict)

            #print ("intent->")
            #print (intent)
            #read_intent = {}
            #print (f'intent-> add {forms_dict["nlu"]["intent"]}')
            for intent in forms_dict["nlu"]:
                intents_set.add(intent["intent"])
            '''
            for intent in forms_dict["nlu"]:
                #print (intent)
                #read_intent=
                print (f'intent-> add {intent[intent]}')
                intents_set.add( intent["intent"])
                print (f'intent-> add {intent["intent"]}')
                #for text in intent["examples"]:
                #    print (text)
                #    intent.add(text)
            #print (templates_dict)
            '''
        print ("Generate file rules in -> "+os.path.join(TRAINING_NLU_DATA_DIR, "rules.yml"))
        #print ("forms")
        #print (forms_dict["forms"])

        #print ("intents_set")
        #print (list(intents_set))

        #print ("actions_set")
        #print (list(actions_set))
        if forms_dict["forms"]:
            myform = forms_dict["forms"]
        else:
            myform = {}
        return list(intents_set), templates_dict, list(actions_set), myform

    @staticmethod
    def _merge_stories() -> NoReturn:
        """ Rewrites stories file to include the smalltalk data """
        with open(
            os.path.join(TRAINING_NLU_DATA_DIR, "stories.md"), mode="a", encoding="utf8"
        ) as f:
            f.write(open(SMALLTALK_STORIES_PATH, encoding="utf8").read())
