import re
from browser.config import Config
from browser.constants import Constants
import browser.road_issues_parser as road_issues_parser
import browser.roads_parser as roads_parser
import numpy as np
import requests
import copy
from functools import lru_cache

class TemplatesTransport:
    """[summary]
    """

    @staticmethod
    @lru_cache(maxsize=None)
    def getData() -> list:

        """ This function return all the information about roads. 
        
        Returns
        ---------
            data list
            """

        data = roads_parser.parser()
        return data

    @staticmethod
    def getIssues(location) -> str:

        """ This function return a list of issues of a town. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """

        location = TemplatesTransport.getReplaceTildes(location)
        if location == "Aragon" or location == "":
            information_location = TemplatesTransport.getIssuesAragon()
        else:
            data = road_issues_parser.parser()
            titles = data["title"]
            descriptions = data["description"]
            information_location = []
            index = 0
            for descripcion_data in descriptions:
                if "Localidades" in descripcion_data:
                    localidades = descripcion_data["Localidades"]
                    localidades = TemplatesTransport.getReplaceTildes(localidades)
                    position = localidades.upper().find(location.upper())
                    if position > -1:
                        if descripcion_data["Tramo"] != "":
                            information_location.append(
                                {
                                    "clave": titles[index],
                                    "Tipo de Limitacion": descripcion_data[
                                        "Tipo de Limitación"
                                    ],
                                    "Tramo": descripcion_data["Tramo"],
                                    "Causa": descripcion_data["Causa"],
                                }
                            )
                        else:
                            information_location.append(
                                {
                                    "clave": titles[index],
                                    "Tipo de Limitacion": descripcion_data[
                                        "Tipo de Limitación"
                                    ],
                                    "Tramo": descripcion_data["Observaciones"],
                                    "Causa": descripcion_data["Causa"],
                                }
                            )
                else:
                    if "Denominacion" in descripcion_data:
                        localidades = descripcion_data["Denominacion"]
                        localidades = TemplatesTransport.getReplaceTildes(localidades)
                        position = localidades.upper().find(location.upper())
                        if position > -1:
                            if descripcion_data["Tramo"] != "":
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Tipo de Limitacion": descripcion_data[
                                            "Tipo de Limitación"
                                        ],
                                        "Tramo": descripcion_data["Tramo"],
                                        "Causa": descripcion_data["Causa"],
                                    }
                                )
                            else:
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Tipo de Limitacion": descripcion_data[
                                            "Tipo de Limitación"
                                        ],
                                        "Tramo": descripcion_data["Observaciones"],
                                        "Causa": descripcion_data["Causa"],
                                    }
                                )
                index = index + 1
        return information_location

    @staticmethod
    def getIssueType(location) -> str:

        """ This function return a list of issues of a town depending on type of issue. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """
        
        location = TemplatesTransport.getReplaceTildes(location)
        if location == "Aragon" or location == "":
            information_location = TemplatesTransport.getIssuesTypeAragon()
        else:
            data = road_issues_parser.parser()
            descriptions = data["description"]
            information_location = []
            types = []
            for descripcion_data in descriptions:
                try:
                    if descripcion_data["Tipo de Limitación"] not in types:
                        types.append(descripcion_data["Tipo de Limitación"])
                except:
                    pass
            quantityTypes = np.zeros(len(types))
            for descripcion_data in descriptions:
                if "Localidades" in descripcion_data:
                    localidades = descripcion_data["Localidades"]
                    localidades = TemplatesTransport.getReplaceTildes(localidades)
                    position = localidades.upper().find(location.upper())
                    if position > -1:
                        index = 0
                        for type in types:
                            if descripcion_data["Tipo de Limitación"] == type:
                                break
                            else:
                                index = index + 1
                        quantityTypes[index] = quantityTypes[index] + 1
                else:
                    if "Denominacion" in descripcion_data:
                        localidades = descripcion_data["Denominacion"]
                        localidades = TemplatesTransport.getReplaceTildes(localidades)
                        position = localidades.upper().find(location.upper())
                        if position > -1:
                            index = 0
                            for type in types:
                                if descripcion_data["Tipo de Limitación"] == type:
                                    break
                                else:
                                    index = index + 1
                            quantityTypes[index] = quantityTypes[index] + 1
            index = 0
            for quantity in quantityTypes:
                if quantity > 0:
                    information_location.append(
                        {"Tipo de limitacion": types[index], "quantity": quantity}
                    )
                index = index + 1
        return information_location

    @staticmethod
    def getIssueWhere(location) -> str:

        """ This function return a list of issues of a town. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """        
        
        location = TemplatesTransport.getReplaceTildes(location)
        if location == "Aragon" or location == "":
            information_location = TemplatesTransport.getIssuesAragon()
        else:
            data = road_issues_parser.parser()
            descriptions = data["description"]
            titles = data["title"]
            information_location = []
            index = 0
            for descripcion_data in descriptions:
                if "Localidades" in descripcion_data:
                    localidades = descripcion_data["Localidades"]
                    localidades = TemplatesTransport.getReplaceTildes(localidades)
                    position = localidades.upper().find(location.upper())
                    if position > -1:
                        if descripcion_data["Tramo"] != "":
                            information_location.append(
                                {
                                    "clave": titles[index],
                                    "Tramo": descripcion_data["Tramo"],
                                }
                            )
                        else:
                            information_location.append(
                                {
                                    "clave": titles[index],
                                    "Tramo": descripcion_data["Observaciones"],
                                }
                            )
                else:
                    if "Denominacion" in descripcion_data:
                        localidades = descripcion_data["Denominacion"]
                        localidades = TemplatesTransport.getReplaceTildes(localidades)
                        position = localidades.upper().find(location.upper())
                        if position > -1:
                            if descripcion_data["Tramo"] != "":
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Tramo": descripcion_data["Tramo"],
                                    }
                                )
                            else:
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Tramo": descripcion_data["Observaciones"],
                                    }
                                )
                index = index + 1
        return information_location

    @staticmethod
    def getIssueReason(location, reason) -> str:

        """ This function return a list of issues of a concrete reason in a town. 
        Parameter
        ----------
            location str
            reason str
        
        Returns
        ---------
            information_location list
            """
        
        location = TemplatesTransport.getReplaceTildes(location)
        if location == "Aragon" or location == "":
            information_location = TemplatesTransport.getIssuesAragon()
        else:
            data = road_issues_parser.parser()
            titles = data["title"]
            descriptions = data["description"]
            information_location = []
            index = 0
            for descripcion_data in descriptions:
                if "Localidades" in descripcion_data:
                    localidades = descripcion_data["Localidades"]
                    localidades = TemplatesTransport.getReplaceTildes(localidades)
                    position = localidades.upper().find(location.upper())
                    if position > -1:
                        if descripcion_data["Causa"].upper().find(reason.upper()) > -1:
                            if descripcion_data["Tramo"] != "":
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Tramo": descripcion_data["Tramo"],
                                        "Causa": descripcion_data["Causa"],
                                    }
                                )
                            else:
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Tramo": descripcion_data["Observaciones"],
                                        "Causa": descripcion_data["Causa"],
                                    }
                                )
                else:
                    if "Denominacion" in descripcion_data:
                        localidades = descripcion_data["Denominacion"]
                        localidades = TemplatesTransport.getReplaceTildes(localidades)
                        position = localidades.upper().find(location.upper())
                        if position > -1:
                            if (
                                descripcion_data["Causa"].upper().find(reason.upper())
                                > -1
                            ):
                                if descripcion_data["Tramo"] != "":
                                    information_location.append(
                                        {
                                            "clave": titles[index],
                                            "Tramo": descripcion_data["Tramo"],
                                            "Causa": descripcion_data["Causa"],
                                        }
                                    )
                                else:
                                    information_location.append(
                                        {
                                            "clave": titles[index],
                                            "Tramo": descripcion_data["Observaciones"],
                                            "Causa": descripcion_data["Causa"],
                                        }
                                    )
                index = index + 1
        return information_location

    @staticmethod
    def getIssueRestrictions(location) -> str:

        """ This function return a list of restriction issues of a town. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """        
        
        location = TemplatesTransport.getReplaceTildes(location)
        if location == "Aragon" or location == "":
            information_location = TemplatesTransport.getIssuesAragon()
        else:
            data = road_issues_parser.parser()
            descriptions = data["description"]
            information_location = []
            for descripcion_data in descriptions:
                if "Localidades" in descripcion_data:
                    localidades = descripcion_data["Localidades"]
                    localidades = TemplatesTransport.getReplaceTildes(localidades)
                    position = localidades.upper().find(location.upper())
                    if position > -1:
                        information_location.append(
                            {"Observaciones": descripcion_data["Observaciones"]}
                        )
                else:
                    if "Denominacion" in descripcion_data:
                        localidades = descripcion_data["Denominacion"]
                        localidades = TemplatesTransport.getReplaceTildes(localidades)
                        position = localidades.upper().find(location.upper())
                        if position > -1:
                            information_location.append(
                                {"Observaciones": descripcion_data["Observaciones"]}
                            )
        return information_location

    @staticmethod
    def getIssuesAragon(issue='') -> str:

        """ This function return a list of issues of Aragon. Is is possible to concrete the type of issue. 
        Parameter
        ----------
            issue
        
        Returns
        ---------
            information_location list
            """        
        
        data = road_issues_parser.parser()
        titles = data["title"]
        descriptions = data["description"]
        information_location = []
        index = 0
        for descripcion_data in descriptions:
            if issue == '':
                try:
                    if descripcion_data["Tramo"] != "":
                        information_location.append(
                            {
                                "clave": titles[index],
                                "Denominacion": descripcion_data["Denominacion"],
                                "Tipo de Limitacion": descripcion_data[
                                    "Tipo de Limitación"
                                ],
                                "Tramo": descripcion_data["Tramo"],
                                "Causa": descripcion_data["Causa"],
                            }
                        )
                    else:
                        information_location.append(
                            {
                                "clave": titles[index],
                                "Denominacion": descripcion_data["Denominacion"],
                                "Tipo de Limitacion": descripcion_data[
                                    "Tipo de Limitación"
                                ],
                                "Tramo": descripcion_data["Observaciones"],
                                "Causa": descripcion_data["Causa"],
                            }
                        )
                except:
                    pass
            else:
                try:
                    causa = descripcion_data["Tipo de Limitación"]
                    causa = TemplatesTransport.getReplaceTildes(causa.lower())
                    issue_copy = copy.deepcopy(issue)
                    issue_copy = TemplatesTransport.getReplaceTildes(issue_copy.lower())
                    position_causa = causa.strip().upper().find(issue_copy.upper())
                    if position_causa > -1:
                        if descripcion_data["Tramo"] != "":
                            information_location.append(
                                {
                                    "clave": titles[index],
                                    "Denominacion": descripcion_data[
                                        "Denominacion"
                                    ],
                                    "Tipo de Limitacion": descripcion_data[
                                        "Tipo de Limitación"
                                    ],
                                    "Tramo": descripcion_data["Tramo"],
                                }
                            )
                        else:
                            information_location.append(
                                {
                                    "clave": titles[index],
                                    "Denominacion": descripcion_data[
                                        "Denominacion"
                                    ],
                                    "Tipo de Limitacion": descripcion_data[
                                        "Tipo de Limitación"
                                    ],
                                    "Tramo": descripcion_data["Observaciones"],
                                }
                            )
                except:
                    pass
            index = index + 1
        return information_location

    @staticmethod
    def getIssuesTypeAragon() -> str:

        """ This function return a list of issues type of Aragon. 

        Returns
        ---------
            information_location list
            """        
        
        data = road_issues_parser.parser()
        descriptions = data["description"]
        information_location = []
        types = []
        for descripcion_data in descriptions:
            try:
                if descripcion_data["Tipo de Limitación"] not in types:
                    types.append(descripcion_data["Tipo de Limitación"])
            except:
                pass
        quantityTypes = np.zeros(len(types))
        for descripcion_data in descriptions:
            try:
                index = 0
                for type in types:
                    if descripcion_data["Tipo de Limitación"] == type:
                        break
                    else:
                        index = index + 1
                quantityTypes[index] = quantityTypes[index] + 1
            except:
                pass
        index = 0
        for quantity in quantityTypes:
            information_location.append(
                {"Tipo de limitacion": types[index], "quantity": quantity}
            )
            index = index + 1
        return information_location

    @staticmethod
    def getRoads(location) -> list:

        """ This function return a list of roads. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        roads = data["carreteras"]
        information_location = []
        if (
            location.upper() == "ARAGON"
            or location.upper() == "ARAGÓN"
            or location == ""
        ):
            for result in roads.values:
                information_location.append(
                    {"codigo_carretera": result[2], "tramo": result[3]}
                )
        else:
            results = roads[roads["provincia"].str.contains(location.upper())]
            for result in results.values:
                information_location.append(
                    {"codigo_carretera": result[2], "tramo": result[3]}
                )
        return information_location

    @staticmethod
    def getRoadSpeed(road) -> list:

        """ This function return a list of roads speed. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """

        data = TemplatesTransport.getData()
        road = TemplatesTransport.getGoodRoadName(road)
        roads = data["carreteras"]
        information_location = []
        results = roads[roads["coddenofic"].str.contains(road.upper())]
        for result in results.values:
            if result[14].upper() == road.upper():
                information_location.append(
                    {
                        "codigo_carretera": result[2],
                        "tramo": result[5],
                        "velocidad": result[8],
                    }
                )
        return information_location

    @staticmethod
    def getRoadType(road) -> list:

        """ This function return a list of roads type. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData() # data = roads_parser.parser()
        road = TemplatesTransport.getGoodRoadName(road)
        roads = data["carreteras"]
        information_location = []
        results = roads[roads["coddenofic"].str.contains(road.upper())]
        for result in results.values:
            if result[14].upper() == road.upper():
                information_location.append(
                    {"codigo_carretera": result[2], "tipo": result[4]}
                )
        return information_location

    @staticmethod
    def getRoadLocation(location) -> list:

        """ This function return a list of roads location. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        roads = data["carreteras"]
        information_location = []
        if (
            location.upper() == "ARAGON"
            or location.upper() == "ARAGÓN"
            or location == ""
        ):
            for result in roads.values:
                information_location.append(
                    {"codigo_carretera": result[2], "tramo": result[3]}
                )
        else:
            results = roads[roads["itinerario"].str.contains(location)]
            for result in results.values:
                information_location.append(
                    {
                        "codigo_carretera": result[2],
                        "itinerario": result[3],
                        "longitud": result[1],
                        "tramo": result[5],
                    }
                )
        return information_location

    @staticmethod
    def getRoadDescription(road) -> list:

        """ This function return a list of roads description. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        road = TemplatesTransport.getGoodRoadName(road)
        roads = data["carreteras"]
        information_location = []
        results = roads[roads["coddenofic"].str.contains(road.upper())]
        for result in results.values:
            if result[14].upper() == road.upper():
                information_location.append(
                    {
                        "codigo_carretera": result[2],
                        "itinerario": result[3],
                        "tipo": result[4],
                        "longitud": result[1],
                        "tramo": result[5],
                    }
                )
        return information_location

    @staticmethod
    def getRoadZones(road, url) -> str:

        """ This function return the zone of a road. 
        Parameter
        ----------
            road str
            url str
        
        Returns
        ---------
            information_location list
            """        
        
        road = TemplatesTransport.getGoodRoadName(road)
        data_values = requests.get(url).json()
        for data in data_values:
            carretera = data[2]
            if carretera.upper() == road.upper():
                return [{"Zona": data[5]}]
        return [{"Zona": ""}]

    @staticmethod
    def getRoadBridges(road) -> str:

        """ This function return a list of roads. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        road = TemplatesTransport.getGoodRoadName(road)
        roads = data["puentes"]
        information_location = []
        results = roads[roads["carretera"].str.contains(road.upper())]
        for result in results.values:
            if result[8].upper().upper() == road.upper():
                information_location.append(
                    {"localidad": result[7], "pk": result[9], "carretera": result[8]}
                )
        return information_location

    @staticmethod
    def getLocationBridges(location) -> list:

        """ This function return a list of bridges of a town. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()

        roads = data["puentes"]

        provincia_localidad_location = copy.deepcopy(location)

        location = location.split('/')[1]

        information_location = []
        if (
            location.upper() == "ARAGON"
            or location.upper() == "ARAGÓN"
            or location == ""
        ):
            for result in roads.values:
                kms = "%.3f" % float(result[9])
                information_location.append(
                    {"codigo_carretera": result[8] + " km " + kms, "tramo": result[3]}
                )
        else:
            provincia_localidad = provincia_localidad_location.split('/')[0]
            if provincia_localidad.upper() == 'PROVINCIA':
                results = roads[roads["provincia"].str.contains(location)]
                for result in results.values:
                    kms = "%.3f" % float(result[9])
                    information_location.append(
                        {"denominacion": result[8] + " km " + kms, "carretera": result[8], "pk": result[9]}
                    )
            else:
                results = roads[roads["localidad"].str.contains(location.upper())]
                for result in results.values:
                    kms = "%.3f" % float(result[9])
                    information_location.append(
                        {"denominacion": result[8] + " km " + kms, "carretera": result[8], "pk": result[9]}
                    )
        return information_location

    @staticmethod
    def getPkBridge(location) -> list:

        """ This function return a list of pk of bridges of a town. 
        Parameter
        ----------
            location str
        
        Returns
        ---------
            information_location list
            """

        data = TemplatesTransport.getData()
        roads = data["puentes"]
        information_location = []
        if (
            location.upper() == "ARAGON"
            or location.upper() == "ARAGÓN"
            or location == ""
        ):
            for result in roads.values:
                information_location.append(
                    {"codigo_carretera": result[2], "tramo": result[3]}
                )
        else:
            results = roads[roads["localidad"].str.contains(location.upper())]
            for result in results.values:
                information_location.append({"pk": result[9], "carretera": result[8]})
        return information_location

    @staticmethod
    def getRoadBridgesKm(road) -> list:

        """ This function return a list of bridges of a road. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        road = TemplatesTransport.getGoodRoadName(road)
        roads = data["puentes"]
        information_location = []
        results = roads[roads["carretera"].str.contains(road.upper())]
        for result in results.values:
            if result[8].upper().upper() == road.upper():
                information_location.append(
                    {"localidad": result[7], "pk": result[9], "carretera": result[8]}
                )
        return information_location

    @staticmethod
    def getRoadBridgesLocations(road) -> list:

        """ This function return a list of bridges locations of a road. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        road = TemplatesTransport.getGoodRoadName(road)
        roads = data["puentes"]
        information_location = []
        results = roads[roads["carretera"].str.contains(road)]
        for result in results.values:
            if result[8].upper().upper() == road.upper():
                information_location.append(
                    {"localidad": result[7], "carretera": result[8]}
                )
        return information_location

    @staticmethod
    def getkmsRoad(road) -> list:

        """ This function return the kilometers of a road. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            information_location list
            """        
        
        road = TemplatesTransport.getGoodRoadName(road)
        data = roads_parser.parser()
        roads = data["puentes"]
        information_location = []
        results = roads[roads["carretera"].str.contains(road.upper())]
        for result in results.values:
            if result[8].upper().upper() == road.upper():
                information_location.append(
                    {"localidad": result[7], "carretera": result[8]}
                )
        return information_location

    @staticmethod
    def getIssuesLocation(issue_type, location) -> list:

        """ This function return a list of issues in a concrete location. 
        Parameter
        ----------
            issue_type str
            location str
        
        Returns
        ---------
            information_location list
            """        
        
        data = road_issues_parser.parser()
        titles = data["title"]
        descriptions = data["description"]
        information_location = []
        if issue_type != '':
            index = 0
            if location != "Aragon" and location != "" and location != "Aragón":
                for descripcion_data in descriptions:
                    if "Localidades" in descripcion_data:
                        localidades = descripcion_data["Localidades"]
                        position = localidades.upper().find(location.upper())
                        if position > -1:
                            causa = descripcion_data["Tipo de Limitación"]
                            causa = TemplatesTransport.getReplaceTildes(causa.lower())
                            issue_copy = copy.deepcopy(issue_type)
                            issue_copy = TemplatesTransport.getReplaceTildes(issue_copy.lower())
                            position_causa = causa.strip().upper().find(issue_copy.upper())
                            if position_causa > -1:
                                if descripcion_data["Tramo"] != "":
                                    information_location.append(
                                        {
                                            "clave": titles[index],
                                            "Denominacion": descripcion_data[
                                                "Denominacion"
                                            ],
                                            "Tipo de Limitacion": descripcion_data[
                                                "Tipo de Limitación"
                                            ],
                                            "Tramo": descripcion_data["Tramo"],
                                        }
                                    )
                                else:
                                    information_location.append(
                                        {
                                            "clave": titles[index],
                                            "Denominacion": descripcion_data[
                                                "Denominacion"
                                            ],
                                            "Tipo de Limitacion": descripcion_data[
                                                "Tipo de Limitación"
                                            ],
                                            "Tramo": descripcion_data["Observaciones"],
                                        }
                                    )
                    else:
                        if "Denominacion" in descripcion_data:
                            localidades = descripcion_data["Denominacion"]
                            position = localidades.upper().find(location.upper())
                            if position > -1:
                                causa = descripcion_data["Tipo de Limitación"]
                                causa = TemplatesTransport.getReplaceTildes(causa.lower())
                                issue_copy = copy.deepcopy(issue_type)
                                issue_copy = TemplatesTransport.getReplaceTildes(issue_copy.lower())
                                position_causa = causa.strip().upper().find(issue_copy.upper())
                                if position_causa > -1:
                                    if descripcion_data["Tramo"] != "":
                                        information_location.append(
                                            {
                                                "clave": titles[index],
                                                "Denominacion": descripcion_data[
                                                    "Denominacion"
                                                ],
                                                "Tipo de Limitacion": descripcion_data[
                                                    "Tipo de Limitación"
                                                ],
                                                "Tramo": descripcion_data["Tramo"],
                                            }
                                        )
                                    else:
                                        information_location.append(
                                            {
                                                "clave": titles[index],
                                                "Denominacion": descripcion_data[
                                                    "Denominacion"
                                                ],
                                                "Tipo de Limitacion": descripcion_data[
                                                    "Tipo de Limitación"
                                                ],
                                                "Tramo": descripcion_data["Observaciones"],
                                            }
                                        )
                    index = index + 1
            else:
                information_location = TemplatesTransport.getIssuesAragon(issue_type)
        else:
            index = 0
            if location != "Aragon" and location != "" and location != "Aragón":
                for descripcion_data in descriptions:
                    if "Localidades" in descripcion_data:
                        localidades = descripcion_data["Localidades"]
                        position = localidades.upper().find(location.upper())
                        if position > -1:
                            if descripcion_data["Tramo"] != "":
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Denominacion": descripcion_data[
                                            "Denominacion"
                                        ],
                                        "Tipo de Limitacion": descripcion_data[
                                            "Tipo de Limitación"
                                        ],
                                        "Tramo": descripcion_data["Tramo"],
                                    }
                                )
                            else:
                                information_location.append(
                                    {
                                        "clave": titles[index],
                                        "Denominacion": descripcion_data[
                                            "Denominacion"
                                        ],
                                        "Tipo de Limitacion": descripcion_data[
                                            "Tipo de Limitación"
                                        ],
                                        "Tramo": descripcion_data["Observaciones"],
                                    }
                                )
                    else:
                        if "Denominacion" in descripcion_data:
                            localidades = descripcion_data["Denominacion"]
                            position = localidades.upper().find(location.upper())
                            if position > -1:
                                if descripcion_data["Tramo"] != "":
                                    information_location.append(
                                        {
                                            "clave": titles[index],
                                            "Denominacion": descripcion_data[
                                                "Denominacion"
                                            ],
                                            "Tipo de Limitacion": descripcion_data[
                                                "Tipo de Limitación"
                                            ],
                                            "Tramo": descripcion_data["Tramo"],
                                        }
                                    )
                                else:
                                    information_location.append(
                                        {
                                            "clave": titles[index],
                                            "Denominacion": descripcion_data[
                                                "Denominacion"
                                            ],
                                            "Tipo de Limitacion": descripcion_data[
                                                "Tipo de Limitación"
                                            ],
                                            "Tramo": descripcion_data["Observaciones"],
                                        }
                                    )
                    index = index + 1

            else:
                for descripcion_data in descriptions:
                    information_location.append(
                    {
                        "clave": titles[index],
                        "Denominacion": descripcion_data[
                            "Denominacion"
                        ],
                        "Tipo de Limitacion": descripcion_data[
                            "Tipo de Limitación"
                        ],
                        "Tramo": descripcion_data["Observaciones"],
                    }
                    )

        return information_location

    @staticmethod
    def getRoadLength(orig, dst) -> list:

        """ This function return the distance of a road between two town. 
        Parameter
        ----------
            orig str
            dst str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        roads = data["carreteras"]
        information_location = []
        results = roads[roads["itinerario"].str.contains(orig)]
        for result in results.values:
            exist = result[3].upper().find(dst.upper())
            if exist > -1:
                information_location.append(
                    {"carretera": result[2], "kilometros": result[1]}
                )
        return information_location

    @staticmethod
    def getUrlZone(road) -> str:

        """ This function return the urls zone of a road. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            information_location list
            """        
        
        road = TemplatesTransport.getGoodRoadName(road)
        urls = [
            "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=224",
            "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=226",
            "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=227",
        ]
        for url in urls:
            data_values = requests.get(url).json()
            for data in data_values:
                carretera = data[2]
                if carretera.upper() == road.upper():
                    return url

    @staticmethod
    def getRoadTotalLength(road) -> list:

        """ This function return total length of a road. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            information_location list
            """        
        
        data = TemplatesTransport.getData()
        road = TemplatesTransport.getGoodRoadName(road)
        roads = data["carreteras"]
        information_location = []
        results = roads[roads["codigo"].str.contains(road.upper())]
        meters = 0
        for result in results.values:
            if result[2].upper().upper() == road.upper():
                meters = meters + float(result[1])
        kms = meters / 1000
        kms_dos_decimales = "%.3f" % kms
        information_location.append({"carretera": road, "kilometros": kms_dos_decimales})
        return information_location

    @staticmethod
    def getGoodRoadName(road) -> str:

        """ This function does the joining process.
        Parameter
        ----------
            road str
        
        Returns
        ---------
            road str
            """        

        if road.find("-") == -1:
            return road[0] + "-" + road[1:]
        else:
            return road

    @staticmethod
    def getReplaceTildes(tipo):

        """ This function does the replace some road characters. 
        Parameter
        ----------
            road str
        
        Returns
        ---------
            road str
            """        
        
        return (
            tipo.replace("á", "a")
            .replace("ó", "o")
            .replace("í", "i")
            .replace("é", "e")
            .replace("ú", "u")
        )
