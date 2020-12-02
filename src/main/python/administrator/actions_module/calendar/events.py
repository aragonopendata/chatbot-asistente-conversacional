'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from actions_module.calendar.utils import *
from urllib.error import URLError


from actions_module.Action_Generic import Action_Generic 

# class ActionEventsByDate(Action_Generic):
#     def name(self):
#         return "action_calendar_events_by_date"
#
#     def run(self, dispatcher, tracker, domain):
#        super().run(dispatcher, tracker, domain)
		
#         date = tracker.get_slot("date")
#
#         if date is not None:
#             try:
#                 answer = browser.search(
#                     {"intents": ["calendarEventsByDate"], "entities": [date]}
#                 )
#
#                 if len(answer) > 0:
#                     link = None
#                     if len(answer) > 5:
#                         answer = answer[0:5]
#                         link = browser.url
#                         print(link)
#
#                     list_response = "\n\t- ".join([x["answer0"] for x in answer])
#                     if link is not None:
#                         list_answer = "{} \n\n Puedes consultar el listado de eventos en el siguiente enlace {}".format(
#                             list_response, link
#                         )
#                     else:
#                         list_answer = list_response
#
#                     dispatcher.utter_message(
#                         "Los eventos del {} son:\n\t- {}".format(date, list_answer)
#                     )
#                 else:
#                     dispatcher.utter_message(f"No he encontrado eventos el {date}.")
#             except (URLError, Exception) as ex:
#                 dispatcher.utter_message(str(ex))
#         else:
#             dispatcher.utter_message(
#                 "Perdona pero no he detectado ninguna fecha en la que buscar eventos."
#             )


# class ActionEventsByDateLocation(Action_Generic):
#     def name(self):
#         return "action_calendar_events_by_date_location"
#
#     def run(self, dispatcher, tracker, domain):
#       super().run(dispatcher, tracker, domain)
#		
#         date = tracker.get_slot("date")
#         location = tracker.get_slot("location")
#
#         if date is not None or location is not None:
#             try:
#                 location_type = "Aragon"
#                 if location.lower() in ["aragon", "aragón"]:
#                     location_type = "Aragon"
#                 else:
#                     location_type = get_location_type(tracker.latest_message["text"])
#
#                 answer = browser.search(
#                     {
#                         "intents": [
#                             "calendarEventsByDate",
#                             "calendarEventsLocation",
#                             "tipoLocalizacion",
#                         ],
#                         "entities": [date, location, location_type],
#                     }
#                 )
#
#                 if len(answer) > 0:
#                     link = None
#                     if len(answer) > 5:
#                         answer = answer[0:5]
#                         link = browser.url
#                         print(link)
#
#                     list_response = "\n\t- ".join([x["answer0"] for x in answer])
#                     if link is not None:
#                         list_answer = "{} \n\n Puedes consultar el listado de eventos en el siguiente enlace {}".format(
#                             list_response, link
#                         )
#                     else:
#                         list_answer = list_response
#
#                     dispatcher.utter_message(
#                         "Los eventos programados el {} en {}{} son:\n\t- {}".format(
#                             date,
#                             get_location_type_output(location_type),
#                             location,
#                             list_answer,
#                         )
#                     )
#                 else:
#                     dispatcher.utter_message(f"No he encontrado eventos el {date}.")
#             except (URLError, Exception) as ex:
#                 dispatcher.utter_message(str(ex))
#         else:
#             dispatcher.utter_message(
#                 "Perdona pero no he detectado ninguna fecha ni lugar en los que buscar eventos."
#             )


# class ActionEventLocation(Action_Generic):
#     def name(self):
#         return "action_calendar_event_location"
#
#     def run(self, dispatcher, tracker, domain):
#        super().run(dispatcher, tracker, domain)
		
#         misc = tracker.get_slot("misc")
#
#         if misc is not None:
#             try:
#                 answer = browser.search(
#                     {"intents": ["calendarEventLocation"], "entities": [misc]}
#                 )
#
#                 if len(answer) > 0:
#
#                     dispatcher.utter_message(
#                         "El evento {} se realizara en {} ".format(
#                             misc, answer[0]["etiqueta"]
#                         )
#                     )
#
#                 else:
#                     dispatcher.utter_message(
#                         f"Perdona no he encontrado el evento {misc}."
#                     )
#             except (URLError, Exception) as ex:
#                 dispatcher.utter_message(str(ex))
#         else:
#             dispatcher.utter_message(
#                 "Perdona pero no he detectado ningún evento del que proporcionar su localización."
#             )


##FUSIONADO en action_calendar_when
# class ActionEventDates(Action_Generic):
#     def name(self):
#         return "action_calendar_event_dates"
#
#     def run(self, dispatcher, tracker, domain):
#        super().run(dispatcher, tracker, domain)
		
#         misc = tracker.get_slot("misc")
#
#         if misc is not None:
#             try:
#                 answer = browser.search(
#                     {"intents": ["calendarEventDate"], "entities": [misc]}
#                 )
#
#                 if len(answer) > 0:
#                     link = None
#                     if len(answer) > 5:
#                         answer = answer[0:5]
#                         link = browser.url
#                         print(link)
#
#                     list_response = "\n\t- ".join([x["answer0"] for x in answer])
#                     if link is not None:
#                         list_answer = "{} \n\n Puedes consultar el listado de fechas del evento en el siguiente enlace {}".format(
#                             list_response, link
#                         )
#                     else:
#                         list_answer = list_response
#
#                     dispatcher.utter_message(
#                         "Los fechas del evento {} son:\n\t- {}".format(
#                             misc, list_answer
#                         )
#                     )
#                 else:
#                     dispatcher.utter_message(
#                         f"No he encontrado datos del evento {misc}."
#                     )
#             except (URLError, Exception) as ex:
#                 dispatcher.utter_message(str(ex))
#         else:
#             dispatcher.utter_message(
#                 "Perdona pero no he detectado ninguna eventos para proporcionar sus fechas."
#             )
