
from rasa_sdk.forms import FormAction,REQUESTED_SLOT
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import EventType, FollowupAction, SlotSet, ActiveLoop
from typing import List, Text
import re


from actions_module.utils import composeAnswer

form_messages = {
    "head_true": "Estos son los datos que hemos encontrado para",
    "head_false": "No hemos encontrado datos en"}

clean_slot = [SlotSet("time", None),
            SlotSet("place", None),
            SlotSet("resource_title", None),
            SlotSet("results", None),
            FollowupAction("action_listen")]

def filter_data_ckan(function_filter, find_in:str, results_from_ckan:list)-> object:
    """ Function to filter information extracted from CKAN once the
        forms have been executed 
        Selection of answers by location and year

    Parameters
    ----------
    function_filter: json
        selection criteria
    find_in: String
        Type of data send: resource or title
    results_from_ckan: list
        list of results extracted from CKAN

    Returns
    -------
    object

       Filtered results
    """

    if find_in == "resource":
        results_from_ckan = [results_from_ckan[0]] # solo el primer elemento

        filter_results = list(filter(function_filter, results_from_ckan[0]["resources"]))
        if filter_results:
            results_from_ckan[0]["resources"] = filter_results
            return {"apply_filter_no_data": False, "results_from_ckan":results_from_ckan}
        else:
            return {"apply_filter_no_data": True, "results_from_ckan": results_from_ckan}

    if find_in == "title":
        filter_results = list(filter(function_filter, results_from_ckan))
        if filter_results:
            return {"apply_filter_no_data": False, "results_from_ckan": filter_results}
        else:
            return {"apply_filter_no_data": True, "results_from_ckan": results_from_ckan}

class TimePlaceForm(FormAction):
    """Class to launch a form asking for year and location
    """

    def name(self) -> Text:
        return "timePlace_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        """A list of required slots that the form has to fill.
        Use `tracker` to request different list of slots
        depending on the state of the dialogue
        
        Parameters
        ----------
        tracker: json
            Request list of slots

        Returns
        -------
        List["Text"]

            Name of slots to extract        
        """
        
        return["time", "place"]

    def submit(self, dispatcher, tracker, domain):
        """ Main function where the time-place form is launched

        Parameters
        ----------
        dispatcher
        tracker
        domain

        Returns
        -------
        clean_slot
        """
        #Form itself
        time_filter = str(tracker.get_slot("time"))
        place_filter = str(tracker.get_slot("place"))

        results_from_ckan = tracker.get_slot("results") #Gets results from slot.
        find_in_resource_or_title= tracker.get_slot("resource_title")
        #Filtrado de results

        def function_filter(x):
            return re.search(f"({time_filter})" ,x["name"],flags=re.IGNORECASE) \
                and re.search(f"({place_filter})" ,x["name"],flags=re.IGNORECASE)

        filter_data = filter_data_ckan(function_filter, find_in_resource_or_title, results_from_ckan)

        message_title, _ = composeAnswer(filter_data.get("results_from_ckan"))
        if filter_data.get("apply_filter_no_data"):# resultsCkan is not None and resultsCkan:
            dispatcher.utter_message(text=f"{form_messages['head_false']} esta fecha {time_filter} ni en este lugar {place_filter}. Mostramos los datos sin filtrar\n {message_title}", json_message={"understand_ckan": "ckan"})
        else:
            dispatcher.utter_message(text=f"{form_messages['head_true']} la fecha {time_filter} y el lugar {place_filter} \n {message_title}", json_message={"understand_ckan": "ckan"})
        return clean_slot


class TimeForm(FormAction):
    """Class to launch a form asking for year
    """

    def name(self) -> Text:
        return "time_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        """A list of required slots that the form has to fill.
        Use `tracker` to request different list of slots
        depending on the state of the dialogue

        Parameters
        ----------
        tracker: json
            Request list of slots

        Returns
        -------
        List["Text"]

            Name of slots to extract        
        """
        return ["time"]

    def submit(self, dispatcher, tracker, domain):
        """ Main function where the time form is launched

        Parameters
        ----------
        dispatcher
        tracker
        domain

        Returns
        -------
        clean_slot
        """

        time_filter = str(tracker.get_slot("time"))

        results_from_ckan = tracker.get_slot("results") #Gets results from slot.
        find_in_resource_or_title= tracker.get_slot("resource_title")

        def function_filter(x):
            return re.search(f"({time_filter})" ,x["name"], flags=re.IGNORECASE)

        filter_data = filter_data_ckan(function_filter, find_in_resource_or_title, results_from_ckan)

        message_title, _ = composeAnswer(filter_data.get("results_from_ckan"))
        if filter_data.get("apply_filter_no_data"):# resultsCkan is not None and resultsCkan:
            dispatcher.utter_message(text=f"{form_messages['head_false']} esta fecha {time_filter}. Mostramos los datos sin filtrar\n {message_title}", json_message={"understand_ckan": "ckan"})
        else:
            dispatcher.utter_message(text=f"{form_messages['head_true']} esta fecha {time_filter} \n {message_title}", json_message={"understand_ckan": "ckan"})

        return clean_slot

class PlaceForm(FormAction):
    """Class to launch a form asking for location
    """

    def name(self) -> Text:
        return "place_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        """A list of required slots that the form has to fill.
        Use `tracker` to request different list of slots
        depending on the state of the dialogue

        Parameters
        ----------
        tracker: json
            Request list of slots

        Returns
        -------
        List["Text"]

            Name of slots to extract        
        """
        return["place"]

    def submit(self, dispatcher, tracker, domain):
        """ Main function where the time form is launched

        Parameters
        ----------
        dispatcher
        tracker
        domain

        Returns
        -------
        clean_slot
        """

         #Form itself
        place_filter = str(tracker.get_slot("place"))

        results_from_ckan = tracker.get_slot("results") #Gets results from slot.
        find_in_resource_or_title= tracker.get_slot("resource_title")
        def function_filter(x):
            return re.search(f"({place_filter})" ,x["name"], flags=re.IGNORECASE)

        filter_data = filter_data_ckan(function_filter, find_in_resource_or_title, results_from_ckan)

        message_title, _ = composeAnswer(filter_data.get("results_from_ckan"))
        if filter_data.get("apply_filter_no_data"):# resultsCkan is not None and resultsCkan:
            dispatcher.utter_message(text=f"{form_messages['head_false']} este lugar {place_filter}. Mostramos los datos sin filtrar\n {message_title}", json_message={"understand_ckan": "ckan"})
        else:
            dispatcher.utter_message(text=f"{form_messages['head_true']} este lugar {place_filter} \n {message_title}", json_message={"understand_ckan": "ckan"})

        return clean_slot
