'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import browser.bus_controller as bus_controller
import pandas as pd
import copy

def parser():

    expediciones_url = "https://opendata.aragon.es/GA_OD_Core/download?view_id=148&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Expediciones"
    expediciones_horarios_url = "https://opendata.aragon.es/GA_OD_Core/download?view_id=149&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Expediciones%20paradas%20y%20horarios"
    paradas_url = "https://opendata.aragon.es/GA_OD_Core/download?view_id=150&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Paradas"
    rutas_url = "https://opendata.aragon.es/GA_OD_Core/download?view_id=151&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Rutas"
    concesiones_url = "https://opendata.aragon.es/GA_OD_Core/download?view_id=147&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Concesiones"

    all_df_data = {}

    try:
        df_expediciones = bus_controller.getPandasStructure(expediciones_url)
        df_expediciones_horarios = bus_controller.getPandasStructure(
            expediciones_horarios_url
        )
        df_paradas = bus_controller.getPandasStructure(paradas_url)
        df_rutas = bus_controller.getPandasStructure(rutas_url)
        df_concesiones = bus_controller.getPandasStructure(concesiones_url)

        cod_rutas = []
        for expedicion in df_expediciones.values:
            cod_rutas.append(expedicion[0][0:13])

        df_expediciones['COD_RUTA'] = cod_rutas

        all = copy.deepcopy(df_rutas)
        all = all.merge(df_expediciones, on='COD_RUTA', how='left')
        all['COD_EXPEDICION'] = all['COD_EXP']
        all = all.merge(df_expediciones_horarios, on='COD_EXPEDICION', how='left')
        all = all.merge(df_paradas, on='COD_PARADA', how='left')
        all['COD_CONCE'] = all['COD_CONCESION']
        all = all.merge(df_concesiones, on='COD_CONCE', how='left')
        all.sort_values(by=['COD_RUTA', 'ORDEN_PARADA'], inplace=True)

        all_df_data = {
            "expediciones": df_expediciones,
            "expediciones_horarios": df_expediciones_horarios,
            "paradas": df_paradas,
            "rutas": df_rutas,
            "concesiones": df_concesiones,
            "all_data": all,
        }

    except:

        pass

    return all_df_data
