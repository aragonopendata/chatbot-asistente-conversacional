"""
Auxiliar script just for internal debugging
Used to test models, test a set of questions at the same time, etc.
"""
import asyncio
import config
import os
import uuid
from pprint import pprint
from typing import List, NoReturn

from rasa.core.agent import Agent
from rasa.core.events import BotUttered, ActionExecuted, UserUttered, SlotSet
from rasa.core.trackers import DialogueStateTracker
from rasa.model import get_latest_model
from rasa.utils.endpoints import EndpointConfig
from scripts.questions import QUESTIONS, QUESTIONS_BAD


project = "GDA"
model = "AOD"

ultimo = None
session_id = uuid.uuid4().hex

using_ner = True
model_path = get_latest_model(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", project, model)
)

action_endpoint = EndpointConfig(url=config.ACTION_URL_ENDPOINT)

# Agent with pre-trained model loaded
agent = Agent.load(model_path, action_endpoint=action_endpoint)


def get_action(tracker: DialogueStateTracker):
    """
    Returns last action executed by the chatbot diferent of
    'action_listen' which executes in every interaction
    :param tracker: Rasa DialogueStateTracker
    :return: last action if exists, 'no action' otherwise
    """
    for event in reversed(tracker.events):
        if (
            isinstance(event, ActionExecuted)
            and not event.action_name == "action_listen"
        ):
            return event

    return "no action"


async def get_response(user_input: str) -> NoReturn:
    """
    Method to get the answer to the user input [user_input]
    :param user_input: the user input itself
    """
    info = await agent.interpreter.parse(user_input)
    pprint(info)

    answer = await agent.handle_text(user_input)
    answer = [x.get("text", "") for x in answer]
    tracker_store = agent.tracker_store.get_or_create_tracker(sender_id="default")
    for event in list(tracker_store.events)[-5:]:
    #event = tracker_store.events[-1]
        if (
            not isinstance(event, (BotUttered, SlotSet))
            # and not isinstance(event, UserUttered)
            and not (
                isinstance(event, ActionExecuted)
                and event.action_name == "action_listen"
            )
        ):
            if isinstance(event, UserUttered):
                print()
            print(event)

    print()
    for r in answer:
        print("Answer bot --> " + " ".join(r.split("\n")))


def chat() -> NoReturn:
    """
    Method to chat with the agent
    """

    a = input("User input --> ")

    while a != "/stop":
        asyncio.get_event_loop().run_until_complete(get_response(a))
        a = input("User input --> ")


async def test_questions(questions: List[str], formatCVS=False) -> NoReturn:
    """
    Evaluate every strig in the list [questions]
    :param questions: the list itself
    """
    for q in questions:
        if formatCVS == False:
            print("User input -->", q)
            answer = await agent.handle_text(q)
            answer = [x.get("text", "") for x in answer]

            print(
                "Intent bot -->", (await agent.interpreter.parse(q))["intent"]["name"]
            )
            tracker_store = agent.tracker_store.get_or_create_tracker(
                sender_id="default"
            )
            action = get_action(tracker_store)
            print("Action bot -->", action)
            for r in answer:
                print("Answer bot -->", " ".join(r.split("\n")))

            print()
        else:
            answer = await agent.handle_text(q)
            answer = [x.get("text", "") for x in answer]
            intent = (await agent.interpreter.parse(q))["intent"]["name"]
            tracker_store = agent.tracker_store.get_or_create_tracker(
                sender_id="default"
            )
            action = get_action(tracker_store)
            print(
                "{0};{1};{2};{3};{4}".format(
                    q, answer, intent, action.action_name, action.confidence
                )
            )


if __name__ == "__main__":
    chat()
    #asyncio.get_event_loop().run_until_complete(test_questions(QUESTIONS,formatCVS=False))
