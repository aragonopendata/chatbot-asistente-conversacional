import jicson
import requests


class calendarController:
    """Class which works with calendars loaded in memory
    """

    def __init__(self, url):
        """ Initialisation of the class to work wint calendars"""

        try:
            self.calendar_variable = jicson.fromWeb(url, auth="base64_authtoken")
        except:
            self.calendar_variable = ""

    def getMainKey(self):
        """ Get a list of keys of of a specific calendar

        Returns
        -------
        list

            keys of a calendar
        """

        return list(self.calendar_variable.keys())[0]

    def getMainKeyEvents(self):
        """ Get a list of keys of the named events in a calendar
        Returns
        -------
        list

            list of keys of an event
        """

        return list(self.calendar.keys())[len(self.calendar.keys()) - 1]

    def getCalendar(self):
        """ Get a calendar

        Returns
        -------
        dict

            active calendar
        """

        try:
            mainKey = self.getMainKey()
            self.calendar = self.calendar_variable[mainKey][0]
            return self.calendar_variable[mainKey][0]
        except:
            return []

    def getEvents(self):
        """ Get events from a calendar

        Returns
        -------
        dict

            Events on a calendar
        """

        try:
            mainKey = self.getMainKeyEvents()
            self.events = self.calendar[mainKey]
            return self.calendar[mainKey]
        except:
            return []

    def getParameter(self, event, parameter):
        """ Gets an event for a specific key

        Parameters
        ----------
        event: dict
            event to find
        parameter: String
            key of the event to find

        Returns
        -------
        dict

            returns information of the searched event
        """

        for key in event.keys():
            if key.upper().find(parameter.upper()) > -1:
                return event[key].replace("\n", "").replace("\r", "").replace("\\", "")

    def getTypeCalendar(self, calendar):
        """ Gets the name or the type of a calendar

        Parameters
        ----------
        calendar: dict
            active calendar

        Returns
        -------
        String

            returns the name or the type of a calendar
        """
        calendar_name = ""
        if calendar.find("ar-") > -1:
            calendar_name = "Aragon"
        else:
            if calendar.find("hu-") > -1:
                calendar_name = "Huesca"
            else:
                if calendar.find("za-") > -1:
                    calendar_name = "Zaragoza"
                else:
                    if calendar.find("te-") > -1:
                        calendar_name = "Teruel"
                    else:
                        calendar_name = "Aragón"

        return calendar_name
