'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import re
import uuid
import json

import os
from collections import defaultdict

from fuzzywuzzy import fuzz
from tqdm import tqdm

from utils import rgb

dir_path = "data/nlu/intents/"
templates_path = "data/nlu/templates"


def fuzzy_test(string):
    texts = {}

    files = os.listdir("data/nlu/intents")

    for f in files:
        intent_name = os.path.splitext(f)[0]
        data = json.load(open(os.path.join("data/nlu/intents", f), encoding="utf8"))

        texts[intent_name] = []
        for example in data["rasa_nlu_data"]["common_examples"]:
            if fuzz.ratio(string, example["text"]) > 70:
                texts[intent_name].append(example["text"])

    for x in texts:
        if texts[x]:
            print(x)
            print(texts[x])


def parse_md(data, entities, intent, templates_length):
    print("Parsing " + intent[1])
    examples = list(map(lambda x: x.lstrip("- "), data[1:]))
    regex = r"\[(.*?)\]\((.*?)\)"
    for idx, example in enumerate(examples):
        matches = re.finditer(regex, example, re.MULTILINE)
        for match in matches:
            value = match.group(1)
            entity = match.group(2)
            example = example.replace(match.group(0), "${" + entity + "}")
            if example not in examples:
                entities[entity]["values"].add(value)
                entities[entity]["intent"].add(intent)

        examples[idx] = example

    examples = set(examples)
    regex = r"\${(\w+)}"
    for example in examples:
        matches = re.finditer(regex, example, re.MULTILINE)
        for match in matches:
            entity = match.group(1)
            templates_length[entity][intent] += 1
    # pprint(dict(templates_length))
    return examples, entities, templates_length


def rasa_to_ita():
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "weather"
        # "GDA",
        # "smalltalk",
    )
    templates_dir = os.path.join(data_dir)  # , "templates")

    entities = defaultdict(lambda: defaultdict(set))
    templates_length = defaultdict(lambda: defaultdict(int))
    for file in tqdm(os.listdir(templates_dir)):
        filename, extension = os.path.splitext(file)
        intent_name = os.path.splitext(os.path.basename(file))[0]
        intent_id = uuid.uuid4().hex
        if extension == ".md":
            with open(os.path.join(templates_dir, file), encoding="utf8") as md:
                lines = md.read().splitlines()
                examples, entities, templates_length = parse_md(
                    lines, entities, (intent_id, intent_name), templates_length
                )

        else:
            data = json.load(
                open(os.path.join(templates_dir, filename), encoding="utf8")
            )
            examples = [x["text"] for x in data["rasa_nlu_data"]["common_examples"]]

        ita_format = {
            "id": intent_id,
            "name": intent_name,
            "templates": [
                {"id": uuid.uuid4().hex, "name": example} for example in examples
            ],
            "templates_length": len(examples),
        }

        template_file = os.path.join(templates_dir, f'{intent_name}.json')
        json.dump(
            ita_format,
            open(template_file, mode="w", encoding="utf8"),
            indent=4,
            sort_keys=True,
        )

    entities_data = []
    with open(os.path.join(data_dir, "entities.json"), mode="w", encoding="utf8") as f:
        for entity_name in entities:
            red, green, blue = rgb.generate_color()
            entities_data.append(
                {
                    "id": uuid.uuid4().hex,
                    "name": entity_name,
                    "intents": [
                        {
                            "id": intent[0],
                            "name": intent[1],
                            "templates_length": templates_length[entity_name][intent],
                        }
                        for intent in entities[entity_name]["intent"]
                    ],
                    "intents_length": len(entities[entity_name]["intent"]),
                    "color": "#%02x%02x%02x" % (red, green, blue),
                    "text_color": rgb.get_text_color(red, green, blue),
                    "values": [
                        {"id": uuid.uuid4().hex, "name": name}
                        for name in entities[entity_name]["values"]
                    ],
                    "values_length": len(entities[entity_name]["values"]),
                }
            )

        json.dump(entities_data, f, sort_keys=True, indent=4)


def rasa_stories_to_ita_stories(filepath, filename="stories.md"):
    with open(os.path.join(filepath, filename), mode="r+") as f:
        content = []
        for line in f:
            if line.startswith("##"):
                # New story, create it
                content.append(
                    {
                        "id": uuid.uuid4().hex,
                        "interactions": [],
                        "name": line.split("##")[-1].strip(),
                    }
                )
            elif line.startswith("*"):
                # Parsing story
                intent = line.lstrip("*").strip()
                actions = []
                nextline = next(f, "").strip()
                while nextline.startswith("-"):
                    actions.append(
                        {"action": nextline.lstrip("- ")}
                        if "action_" in nextline
                        else {"utter": nextline.lstrip("- ")}
                    )
                    nextline = next(f, "").strip()

                content[-1]["interactions"].append(
                    {
                        "id": uuid.uuid4().hex,
                        "intent": intent,
                        "actions_module": actions,
                    }
                )

    json.dump(content, open(os.path.join(filepath, "stories.json"), mode="w"), indent=4)


def reformat_actions_in_stories(path, filename="stories.json"):
    data = json.load(open(os.path.join(path, filename)))
    for story in data:
        for interaction in story["interactions"]:
            utter = interaction["utter"]
            interaction.pop("utter")
            interaction["actions_module"] = [{"utter": utter}]

    json.dump(data, open(os.path.join(path, filename), mode="w"), indent=4)


def reformat_interactions(path, filename="stories.json"):
    data = json.load(open(os.path.join(path, filename)))
    for story in data:
        for interaction in story["interactions"]:
            for action in interaction["actions_module"]:
                action["type"] = "utter" if "utter" in action else "action"
                action["value"] = (
                    action["utter"] if "utter" in action else action["action"]
                )
                action.pop("utter", None)
                action.pop("action", None)

    json.dump(data, open(os.path.join(path, filename), mode="w"), indent=4)
