'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from browser.JSONController import jsonController
import json
from functools import lru_cache

@lru_cache(maxsize=None)
def parser():

    webs = {}
    webs["carreteras"] = "https://opendata.aragon.es/GA_OD_Core/preview?view_id=205"
    # webs['dominio_publico'] = 'https://opendata.aragon.es/GA_OD_Core/preview?view_id=224'
    # webs['zona_afeccion'] = 'https://opendata.aragon.es/GA_OD_Core/preview?view_id=226'
    # webs['zona_servidumbre'] = 'https://opendata.aragon.es/GA_OD_Core/preview?view_id=227'
    webs["puentes"] = "https://opendata.aragon.es/GA_OD_Core/preview?view_id=225"

    data = {}
    for key in webs.keys():
        try:
            jsoncontroller = jsonController()
            jsoncontent = jsoncontroller.getContent(webs[key])
            data_pandas_format = jsoncontroller.setListToPandas()
            data[key] = data_pandas_format
        except:
            pass

    return data
