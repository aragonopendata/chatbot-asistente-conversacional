import browser.bus_controller as bus_controller
from browser.config import Config
import pandas as pd
import copy

def parser():
    """  Extract information about passenger transport routes from GA_OD_CORE and 
    insert the information in a frame

    Returns
    -------
    dataframe 

        Return all the routes loaded in GA_OD_CORE
    """

    url_expeditions = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=148&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Expediciones"
    url_expeditions_scheduling = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=149&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Expediciones%20paradas%20y%20horarios"
    url_stops = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=150&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Paradas"
    url_routes = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=151&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Rutas"
    url_concession = "https://opendata.aragon.es/" + Config.legacy + "/download?view_id=147&formato=json&name=Transporte%20público%20interurbano%20de%20viajeros%20por%20carretera%20en%20Aragón&nameRes=Concesiones"

    all_df_data = {}

    try:
        df_expeditions = bus_controller.getPandasStructure(url_expeditions)
        df_expeditions_scheduling = bus_controller.getPandasStructure(
            url_expeditions_scheduling
        )
        df_stops = bus_controller.getPandasStructure(url_stops)
        df_routes = bus_controller.getPandasStructure(url_routes)
        df_concessions = bus_controller.getPandasStructure(url_concession)

        cod_routes = []
        for expedition in df_expeditions.values:
            cod_routes.append(expedition[0][0:13])

        df_expeditions['COD_RUTA'] = cod_routes

        #New code added to the final version code
        
        df_expeditions.columns = map(str.upper, df_expeditions.columns)
        df_expeditions_scheduling.columns = map(str.upper, df_expeditions_scheduling.columns)
        df_stops.columns = map(str.upper, df_stops.columns)
        df_routes.columns = map(str.upper, df_routes.columns)
        df_concessions.columns = map(str.upper, df_concessions.columns)        
        
        all = copy.deepcopy(df_routes)
        all = all.merge(df_expeditions, on='COD_RUTA', how='left')
        all['COD_EXPEDICION'] = all['COD_EXP']
        all = all.merge(df_expeditions_scheduling, on='COD_EXPEDICION', how='left')
        all = all.merge(df_stops, on='COD_PARADA', how='left')
        all['COD_CONCE'] = all['COD_CONCESION']
        all = all.merge(df_concessions, on='COD_CONCE', how='left')
        all.sort_values(by=['COD_RUTA', 'ORDEN_PARADA'], inplace=True)

        all_df_data = {
            "expediciones": df_expeditions,
            "expediciones_horarios": df_expeditions_scheduling,
            "paradas": df_stops,
            "rutas": df_routes,
            "concesiones": df_concessions,
            "all_data": all,
        }

    except:

        pass

    return all_df_data
