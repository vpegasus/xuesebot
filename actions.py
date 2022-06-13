import typing
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import utils
from chitchat_response import CDial

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict

from process_data.keymap import *
from process_data.neokb import SearchDB

kb = SearchDB()
unrelated_lm = CDial()  # unrelated_lm: unrelated language model response generator


class ActionPersonIntro(Action):
    def __init__(self, ):
        pass

    def name(self) -> Text:
        return "action_person_intro"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        entity = tracker.get_slot('person')
        if entity:
            obj = await utils.call_potential_coroutine(
                kb.person(entity)
            )
            texts = [f'{inv_person_map.get(k)}:{v}' for k, v in obj.items() if inv_person_map.get(k)]
            texts = ','.join(texts)
            texts = entity + ' ' + texts
            dispatcher.utter_message(texts)
            return []

        dispatcher.utter_message(response="utter_ask_rephrase")
        return []


class ActionCityIntro(Action):
    def __init__(self, ):
        pass

    def name(self) -> Text:
        return "action_city_intro"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        entity = tracker.get_slot('city')
        if entity:
            obj = await utils.call_potential_coroutine(
                kb.city(entity)
            )
            texts = [f'{inv_city_map.get(k)}:{v}' for k, v in obj.items() if inv_city_map.get(k)]
            texts = ','.join(texts)
            texts = entity + ' ' + texts
            dispatcher.utter_message(texts)
            return []

        dispatcher.utter_message(response="utter_ask_rephrase")
        return []


class ActionForceIntro(Action):
    def __init__(self, ):
        pass

    def name(self) -> Text:
        return "action_force_intro"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        entity = tracker.get_slot('force')
        if entity:
            obj = await utils.call_potential_coroutine(
                kb.force(entity)
            )
            texts = [f'{inv_force_map.get(k)}:{v}' for k, v in obj.items() if inv_force_map.get(k)]
            texts = ','.join(texts)
            texts = entity + ' ' + texts
            dispatcher.utter_message(texts)
            return []

        dispatcher.utter_message(response="utter_ask_rephrase")
        return []


class ActionPersonAttr(Action):
    def __init__(self, ):
        pass

    def name(self) -> Text:
        return "action_person_attr"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        entity = tracker.get_slot('force')
        if entity:
            obj = await utils.call_potential_coroutine(
                kb.person(entity)
            )
            texts = [f'{inv_force_map.get(k)}:{v}' for k, v in obj.items() if inv_force_map.get(k)]
            texts = ','.join(texts)
            texts = entity + ' ' + texts
            dispatcher.utter_message(texts)
            return []

        dispatcher.utter_message(response="utter_ask_rephrase")
        return []


class ActionCityAttr(Action):
    def __init__(self, ):
        pass

    def name(self) -> Text:
        return "action_city_attr"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        entity = tracker.get_slot('force')
        if entity:
            obj = await utils.call_potential_coroutine(
                kb.person(entity)
            )
            texts = [f'{inv_force_map.get(k)}:{v}' for k, v in obj.items() if inv_force_map.get(k)]
            texts = ','.join(texts)
            texts = entity + ' ' + texts
            dispatcher.utter_message(texts)
            return []

        dispatcher.utter_message(response="utter_ask_rephrase")
        return []


class ActionForceAttr(Action):
    def __init__(self, ):
        pass

    def name(self) -> Text:
        return "action_force_attr"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        entity = tracker.get_slot('force')
        if entity:
            obj = await utils.call_potential_coroutine(
                kb.person(entity)
            )
            texts = [f'{inv_force_map.get(k)}:{v}' for k, v in obj.items() if inv_force_map.get(k)]
            texts = ','.join(texts)
            texts = entity + ' ' + texts
            dispatcher.utter_message(texts)
            return []

        dispatcher.utter_message(response="utter_ask_rephrase")
        return []


class ActionUnrelated(Action):
    def __init__(self, ):
        pass

    def name(self) -> Text:
        return "action_unrelated_topic"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        raw_text = tracker.latest_message
        texts = unrelated_lm.response(raw_text)
        dispatcher.utter_message(response=texts)
        # dispatcher.utter_message(response="utter_ask_rephrase")
        return []
