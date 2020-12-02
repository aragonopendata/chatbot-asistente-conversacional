'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from collections import defaultdict
from datetime import datetime
from pprint import pprint

import requests
from typing import List, Dict, Any, Tuple

from top_secret.api_keys import weather_api_key

##################
##### MONTHS #####
##################

map_months_es = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

map_months_en = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

months = {"es": map_months_es, "en": map_months_en}


def most_frequent_value(iterable: List) -> float:
    """
    Return the most frequent value of a list
    """
    return max(set(iterable), key=iterable.count)


def convert_ms_to_kmh(value: float) -> float:
    """
    Transform meters per second to kilometers per hour
    :param value: meters per second value
    :return: [value] transformed to kilometers per hour
    """
    return round(value * 3.6, 1)


class OpenWeatherParser:

    # Implemented languages
    VALID_LANGUAGES = ["es", "en"]

    def __init__(self, lang: str = "es"):
        self.url = "https://api.openweathermap.org/data/2.5/"
        self.units = "metric"
        if lang in self.VALID_LANGUAGES:
            self.lang = lang
        else:
            raise ValueError(
                "Lenguaje no disponible para consultar el tiempo atmosférico, los lenguajes diponibles son {}".format(
                    self.VALID_LANGUAGES
                )
            )

    def get_current_weather(
        self, location: str, country: str = "es"
    ) -> Tuple[str, str]:
        """
        Build of an informative message of the current weather in the location
        [location] placed in the country  [country]
        :param location:
        :param country:
        :return: current weather parsed into a readable message
        """

        weather_info = self.__query_weather(location, country)
        weather_info = self.__parse_current_weather(weather_info)
        return self.build_current_message(location, weather_info, self.lang)

    def get_forecast_weather(
        self, location: str, country: str = "es"
    ) -> List[Tuple[str, str]]:
        """
        Build a message for every forecasted day from today to a maximum of 5
        :param location:
        :param country:
        :return: a list of messages with the weather for each day
        """

        weather_info = self.__query_weather(location, country, kind="forecast")
        weather_info = self.__parse_forecast_weather(weather_info)
        return [
            self.build_forecast_message(location, day, info, self.lang)
            for day, info in weather_info.items()
        ]

    # TODO: Handle exception if status code is not 200
    def __query_weather(
        self, location: str, country: str = "es", kind: str = "weather"
    ) -> Dict[str, Any]:
        """
        Gets the information that answers a query to the OpenWeather API,
        wether is current or forecast weather
        :param location:
        :param country:
        :param kind: 'weather' for current, 'forecast' for forecast
        :return: a dictionary with the information
        """
        response = requests.get(
            self.url + kind,
            params={
                "q": f"{location},{country}",
                "lang": self.lang,
                "units": self.units,
                "appid": weather_api_key,
            },
        )

        response.raise_for_status()

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def __parse_current_weather(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        With the information of the request, we parse the content in a
        simpler dictionary to fasten message building
        :param data: request data
        :return: [data] minimized to what's relevant for us
        """
        data["weather"] = data["weather"][0]
        weather_info = {
            "temp": data["main"]["temp"],
            "condition": data["weather"]["description"],
            "wind_speed": convert_ms_to_kmh(data["wind"]["speed"]),
            "icon": data["weather"]["icon"],
        }

        return weather_info

    @staticmethod
    def __parse_forecast_weather(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        With the information of the request, we parse the content in a
        simpler dictionary to fasten message building. For that we need
        a middle dictionary with the data of all the days divided by hours,
        so for each day we keep the information and take the average of
        each feature: wind_speed, temperature, etc.
        :param data: request data
        :return: [data] minimized
        """
        parsed_data = defaultdict(lambda: defaultdict(list))
        for x in data["list"]:
            date = x["dt_txt"].split(" ")[0]
            parsed_data[date]["temp_min"].append(x["main"]["temp_min"])
            parsed_data[date]["temp_max"].append(x["main"]["temp_max"])
            parsed_data[date]["wind_speed"].append(x["wind"]["speed"])
            parsed_data[date]["conditions"].extend(
                [y["description"] for y in x["weather"]]
            )
            parsed_data[date]["icons"].extend(
                [y["icon"].replace("n", "d") for y in x["weather"]]
            )

        weather_info = {}

        for day, info in parsed_data.items():
            weather_info[day] = {}
            weather_info[day]["temp_max"] = round(max(info["temp_max"]), 1)
            weather_info[day]["temp_min"] = round(min(info["temp_min"]), 1)
            weather_info[day]["temp_mean"] = round(
                (weather_info[day]["temp_max"] + weather_info[day]["temp_min"]) / 2.0, 1
            )
            weather_info[day]["wind_speed"] = convert_ms_to_kmh(
                sum(info["wind_speed"]) / len(info["wind_speed"])
            )
            weather_info[day]["conditions"] = most_frequent_value(info["conditions"])
            weather_info[day]["icon"] = most_frequent_value(info["icons"])

        return weather_info

    @classmethod
    def build_current_message(
        cls, location: str, winfo: Dict[str, Any], lang: str
    ) -> Tuple[str, str]:
        """
        Build a message of the current message
        :param location: place searched
        :param winfo: weather information minimized
        :param lang: language of the output  message
        :return: a detailed message with the current weather data
        """
        if lang == "es":
            return (
                f"En {location} está actualmente {winfo['condition']}, "
                f"hace {winfo['temp']} grados centígrados y "
                f"viento a {winfo['wind_speed']} kilómetros por hora.",
                winfo["icon"],
            )
        elif lang == "en":
            return (
                f"In {location} is currently {winfo['condition']}, "
                f"with {winfo['temp']} degrees and "
                f"wind at {winfo['wind_speed']} kilometers per hour.",
                winfo["icon"],
            )
        else:
            return (
                "Lenguaje no disponible para consultar el tiempo atmosférico, los lenguajes diponibles son {}".format(
                    cls.VALID_LANGUAGES
                ),
                "",
            )

    @classmethod
    def build_forecast_message(
        cls, location: str, day: str, winfo: Dict[str, Any], lang: str
    ) -> Tuple[str, str]:
        """
        Builds a message with the info of the day [day]
        :param location: place searched
        :param day: day of month
        :param winfo: weather information minimized
        :param lang: language of the output message
        :return: a detailed message for the day [day]
        """
        date = datetime.strptime(day, "%Y-%m-%d")
        if lang == "es":
            date = f"{date.day} de {months['es'][date.month]} de {date.year}"
            return (
                f"El {date} en {location} estará {winfo['conditions']}. "
                f"Temperatura media: {winfo['temp_mean']} grados, "
                f"temperatura máxima: {winfo['temp_max']} grados, "
                f"temperatura mínima: {winfo['temp_min']} grados. "
                f"Velocidad de viento: {winfo['wind_speed']} kilómetros por hora.",
                winfo["icon"],
            )
        elif lang == "en":
            date = f"{date.day}, {months['en'][date.month]} of {date.year}"
            return (
                f"On {date} in {location} will be {winfo['conditions']}. "
                f"Average temperature: {winfo['temp_mean']} degrees, "
                f"maximum temperature: {winfo['temp_max']} degrees, "
                f"minimum temperature: {winfo['temp_min']} degrees. "
                f"Wind speed: {winfo['wind_speed']} kilometers per hour.",
                winfo["icon"],
            )
        else:
            return (
                "Lenguaje no disponible para consultar el tiempo atmosférico, los lenguajes diponibles son {}".format(
                    cls.VALID_LANGUAGES
                ),
                "",
            )
