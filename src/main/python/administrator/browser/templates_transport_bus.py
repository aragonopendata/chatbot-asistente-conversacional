'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import re
from browser.config import Config
from browser.constants import Constants
import browser.bus_parser as bus_parser
import requests
import browser.bus_controller as bus_controller
import datetime
import pandas as pd
from functools import lru_cache

class TemplatesTransportBus:
    """[summary]
    """

    @staticmethod
    @lru_cache(maxsize=None)
    def getAllData() -> list:

        return bus_parser.parser()

    @staticmethod
    def getBusToLocation(location, all_data) -> list:

        rutas = all_data["rutas"]
        # routes_location = bus_controller.getLocationDestiny(rutas,'DESTINO',location)
        routes_location = TemplatesTransportBus.getRoutesQuick(all_data, location, "")
        routes_location = TemplatesTransportBus.getListTransformedToDict(
            routes_location.columns, routes_location.values
        )
        return routes_location

    @staticmethod
    def getBusesFronTownToTown(location_orig, location_dest, all_data) -> list:

        all_data = TemplatesTransportBus.getAllData()

        routes_location = TemplatesTransportBus.getRoutesQuick(
            all_data, location_orig, location_dest
        )

        # rutas = all_data['rutas']
        # routes_location = bus_controller.getLocationFromOriginToDestiny(rutas, 'ORIGEN', 'DESTINO', location_orig,
        #                                                                location_dest)
        routes_location = TemplatesTransportBus.getListTransformedToDict(
            routes_location.columns, routes_location.values
        )
        return routes_location

    @staticmethod
    def getBusesFronTownToTownWithoutAllDataCalculation(
        location_orig, location_dest, all_data
    ) -> list:

        rutas = all_data["rutas"]

        routes_location = TemplatesTransportBus.getRoutesQuick(
            all_data, location_orig, location_dest
        )

        # routes_location = bus_controller.getLocationFromOriginToDestiny(rutas, 'ORIGEN', 'DESTINO', location_orig,
        #                                                                location_dest)
        routes_location = TemplatesTransportBus.getListTransformedToDict(
            routes_location.columns, routes_location.values
        )
        return routes_location

    @staticmethod
    def getBusesFronTownToTownWithoutAllDataCalculationWithoutDictionario(
        location_orig, location_dest, all_data
    ) -> list:

        rutas = all_data["rutas"]

        routes_location = TemplatesTransportBus.getRoutesQuick(
            all_data, location_orig, location_dest
        )

        # routes_location = bus_controller.getLocationFromOriginToDestiny(rutas, 'ORIGEN', 'DESTINO', location_orig,
        #                                                                location_dest)
        return routes_location

    @staticmethod
    def getCompaniesDataFromTown(location, all_data) -> list:

        concesiones = all_data["concesiones"]
        routes_concesiones = bus_controller.getLocationDestiny(
            concesiones, "NOMCONCE", location
        )
        routes_concesiones = TemplatesTransportBus.getListTransformedToDict(
            routes_concesiones.columns, routes_concesiones.values
        )
        return routes_concesiones

    '''@staticmethod
    def getTimelineOfBusFrownTownToTown(location_orig, location_dest, all_data) -> list:

        routes_location = TemplatesTransportBus.getBusesFronTownToTownWithoutAllDataCalculationWithoutDictionario(
            location_orig, location_dest, all_data
        )
        paradas = all_data["paradas"]
        expediciones = all_data["expediciones"]
        results = []
        for routes in routes_location.values:
            especificaciones_especificas = bus_controller.getLocationDestiny(
                expediciones, "COD_EXP", routes[1]
            )
            for parada_especifia in especificaciones_especificas.values:
                timelines = bus_controller.getRowFromIntegerValues(
                    all_data["expediciones_horarios"],
                    "COD_EXPEDICION",
                    parada_especifia[0],
                )
                timelines = bus_controller.getDataframeSorted(timelines, "ORDEN_PARADA")
                for timeline in timelines.values:
                    paradas_list = bus_controller.getRowFromIntegerValues(
                        paradas, "COD_PARADA", timeline[2]
                    )
                    parada = paradas_list.values[0]
                    data = TemplatesTransportBus.getRegisterTransformedToDict(
                        paradas_list.columns, paradas_list.values
                    )
                    try:
                        data_format = TemplatesTransportBus.getStringDataInDateFormat(
                            timeline[3]
                        )
                        hora = ""
                        if data_format.hour < 10:
                            hora = '0' + str(data_format.hour)
                        else:
                            hora = str(data_format.hour)
                        minutos = ""
                        if data_format.minute < 10:
                            minutos = '0' + str(data_format.minute)
                        else:
                            minutos = str(data_format.minute)
                        segundos = ""
                        if data_format.second < 10:
                            segundos = '0' + str(data_format.second)
                        else:
                            segundos = str(data_format.second)
                        time_str_format = (
                            str(hora)
                            + ":"
                            + str(minutos)
                            + ":"
                            + str(segundos)
                        )
                    except:
                        time_str_format = ""
                    data["horario"] = time_str_format
                    data["ruta"] = routes[2]
                    data["expedicion"] = parada_especifia[1]
                    if data not in results:
                        try:
                            if parada[2].upper() == location_orig.upper():
                                results.append(data)
                        except:
                            pass
        return results'''

    @staticmethod
    def getTimelineOfBusFrownTownToTown(location_orig, location_dest, all_data) -> list:

        routes_location = TemplatesTransportBus.getBusesFronTownToTownWithoutAllDataCalculationWithoutDictionario(
            location_orig, location_dest, all_data
        )

        results = []

        for rutas in routes_location.values:

            data = {}

            data_format = TemplatesTransportBus.getStringDataInDateFormat(
                rutas[11]
            )
            hora = ""
            if data_format.hour < 10:
                hora = '0' + str(data_format.hour)
            else:
                hora = str(data_format.hour)
            minutos = ""
            if data_format.minute < 10:
                minutos = '0' + str(data_format.minute)
            else:
                minutos = str(data_format.minute)
            segundos = ""
            if data_format.second < 10:
                segundos = '0' + str(data_format.second)
            else:
                segundos = str(data_format.second)
            time_str_format = (
                    str(hora)
                    + ":"
                    + str(minutos)
                    + ":"
                    + str(segundos)
            )

            data["horario"] = time_str_format
            data["ruta"] = rutas[2]
            data["expedicion"] = rutas[6]

            results.append(data)

        return results

    @staticmethod
    def getListTransformedToDict(headers, list_results) -> dict:

        results = []
        for result in list_results:
            i = 0
            result_values = {}
            for element in result:
                result_values[headers[i]] = element
                i = i + 1
            results.append(result_values)
        return results

    @staticmethod
    def getRegisterTransformedToDict(headers, list_results) -> dict:

        i = 0
        result_values = {}
        for element in list_results[0]:
            result_values[headers[i]] = element
            i = i + 1
        return result_values

    @staticmethod
    def getStringDataInDateFormat(date_time_str):

        date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S")
        return date_time_obj

    @staticmethod
    def getRoutes(all_matrix, location_origin, location_dest):

        results = []
        paradas = all_matrix["paradas"]
        expediciones_paradas = all_matrix["expediciones_horarios"]
        expediciones = all_matrix["expediciones"]
        rutas = all_matrix["rutas"]
        exist_registers_paradas = paradas[
            paradas["NUCLEO"].str.contains(location_origin.upper(), na=False)
        ]
        headers = [
            "COD_CONCESION",
            "COD_RUTA",
            "DENO_RUTA",
            "ORIGEN",
            "DESTINO",
            "RNUM",
        ]
        for exist in exist_registers_paradas.values:
            cod_parada = exist[0]
            exist_registers_expediciones = expediciones_paradas[
                expediciones_paradas["COD_PARADA"] == cod_parada
            ]
            for exp in exist_registers_expediciones.values:
                exp_cod = exp[0]
                exist_registers_paradas_exp = expediciones_paradas[
                    expediciones_paradas["COD_EXPEDICION"] == exp_cod
                ]
                if location_dest != "":
                    for exp_paradas in exist_registers_paradas_exp.values:
                        cod_parada_nuevo = exp_paradas[2]
                        exist_registers_paradas = paradas[
                            paradas["COD_PARADA"] == cod_parada_nuevo
                        ]
                        try:
                            nucleo = exist_registers_paradas.values[0][2]
                            if nucleo.upper() == location_dest.upper():
                                exp_route_string = exp[0][0:13]
                                register = rutas[
                                    rutas["COD_RUTA"].str.contains(
                                        exp_route_string.upper(), na=False
                                    )
                                ]
                                actual_data = []
                                for register_data in register.values[0]:
                                    actual_data.append(register_data)
                                if actual_data not in results:
                                    results.append(actual_data)
                        except:
                            pass
                else:
                    try:
                        exp_route_string = exp[0][0:13]
                        register = rutas[
                            rutas["COD_RUTA"].str.contains(
                                exp_route_string.upper(), na=False
                            )
                        ]
                        actual_data = []
                        for register_data in register.values[0]:
                            actual_data.append(register_data)
                        if actual_data not in results:
                            results.append(actual_data)
                    except:
                        pass
        results = pd.DataFrame(results, columns=headers)
        return results

    '''@staticmethod
    def getRoutesQuick(all_matrix, location_origin, location_dest):

        results = []
        headers = [
            "COD_CONCESION",
            "COD_RUTA",
            "DENO_RUTA",
            "ORIGEN",
            "DESTINO",
            "RNUM",
        ]
        all_data = all_matrix['all_data']
        rows = bus_controller.getLocationDestiny(all_data,'NUCLEO',location_origin)
        rutas = pd.unique(rows['COD_RUTA'])
        if location_dest != "":
            rutas_data = all_data[all_data['COD_RUTA'].isin(rutas)]
            rows = bus_controller.getLocationDestiny(rutas_data, 'NUCLEO', location_dest)
            conexiones = pd.unique(rows['COD_RUTA'])
        else:
            conexiones = rutas
        rutas = all_matrix['rutas']
        rutas = rutas[rutas['COD_RUTA'].isin(conexiones)]
        for register_data in rutas.values:
            if location_dest != "":
                # comprobar la dirección.
                ruta_data = all_data[all_data['COD_RUTA'] == register_data[1]]
                position_origin = bus_controller.getLocationDestiny(ruta_data, 'NUCLEO', location_origin)
                orden_parada_origen = position_origin.values[0][14]
                position_destiny = bus_controller.getLocationDestiny(ruta_data, 'NUCLEO', location_dest)
                orden_parada_destino = position_destiny.values[0][14]
                if orden_parada_origen < orden_parada_destino:
                    results.append(register_data)
                else:
                    pass
            else:
                results.append(register_data)
        results = pd.DataFrame(results, columns=headers)
        return results'''

    def getRoutesQuick(all_matrix, location_origin, location_dest):

        results = []
        '''headers = [
            "COD_CONCESION",
            "COD_RUTA",
            "DENO_RUTA",
            "ORIGEN",
            "DESTINO",
            #"RNUM",
        ]'''
        headers = all_matrix['all_data'].columns.values.tolist()
        all_data = all_matrix['all_data']
        rows = bus_controller.getLocationDestiny(all_data, 'NUCLEO', location_origin)
        rutas = pd.unique(rows['COD_RUTA'])
        if location_dest != "":
            rutas_data = all_data[all_data['COD_RUTA'].isin(rutas)]
            rows = bus_controller.getLocationDestiny(rutas_data, 'NUCLEO', location_dest)
            conexiones = pd.unique(rows['COD_RUTA'])
        else:
            conexiones = rutas
        rutas = all_matrix['rutas']
        rutas = rutas[rutas['COD_RUTA'].isin(conexiones)]
        results = pd.DataFrame()
        for register_data in rutas.values:
            rutas_all_data = bus_controller.getLocationDestiny(all_data, 'COD_CONCESION', register_data[0])
            results = results.append(rutas_all_data)
        results = bus_controller.getLocationDestiny(results, 'NUCLEO', location_origin)
        rutas = pd.unique(results['COD_RUTA'])
        if location_dest != "":
            rutas_data = all_data[all_data['COD_RUTA'].isin(rutas)]
            results = bus_controller.getLocationDestiny(rutas_data, 'NUCLEO', location_dest)
            results = bus_controller.getNotLocationDestiny(results, 'ORIGEN', location_dest)
        return results
