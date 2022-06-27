import datetime as dt
from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import pathlib

ALLOWED_PIZZA_TYPES = ["margaritha", "salami", "prosciutto", "quattro formaggi"]
ALLOWED_PIZZA_SIZES = ["small", "medium", "large"]


class ActionShowTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")
        return []

class ActionRepeatOrder(Action):

    def name(self) -> Text:
        return "action_repeat_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pizza_type = tracker.get_slot("pizza_type")
        pizza_size = tracker.get_slot("pizza_size")
        if not pizza_type or not pizza_size:
            dispatcher.utter_message(text=f"I don't know your order.")
        else:
            dispatcher.utter_message(text=f"Your ordered a {pizza_size} size pizza {pizza_type}!")
        return []

class ValidatePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pizza_form"

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Validate `pizza_type` value."""

        if slot_value.lower() not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(text=f"We don't offer this pizza. You can choose between Pizza Margaritha, Pizza Salami, Pizza Prosciutto and Pizza Quattro Formaggi.")
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"{slot_value} is a great choice!.")
        return {"pizza_type": slot_value}

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We sadly don't offer the requested size.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"You picked a {slot_value} pizza.")
        return {"pizza_size": slot_value}