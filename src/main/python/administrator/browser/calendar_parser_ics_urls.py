"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import requests
import browser.calendar_parser as calendar_parser
from functools import lru_cache


@lru_cache(maxsize=None)
def parser(years):
    """  Extract all the calendars from CKAN of one specific year

    Parameters
    ----------
    year: Integer
        Year to extract

    Returns
    -------
    dataframe 

        Calendars of a specific year
    """

    year_data = {}
    for year in years:
        try:
            url = (
                "https://opendata.aragon.es/api/action/package_search?fq=(name:*calendario*"
                + str(year)
                + "%20AND%20type:dataset)&rows=1500&start=0"
            )
            results_general = requests.get(url).json()
            results_final = results_general["result"]["results"]
            final_results = {}
            for result in results_final:
                title = result["title"]
                extras = result["resources"]
                resources = {}
                index = 0
                for extra in extras:
                    extras_dict = {}
                    if extra["format"] == "ICS":
                        for element in extra.keys():
                            extras_dict[element] = extra[element]
                        resources[index] = extras_dict
                        index = index + 1
                final_results[title] = resources
            year_data[year] = final_results
        except:
            year_data[year] = {}
    return year_data
