from browser.JSONController import jsonController
from browser.config import Config
import json
from functools import lru_cache

@lru_cache(maxsize=None)
def parser():

    """ This function parses the road web site and it recoves the key value to visualize at the web site. 
    
        Parameter
        -------------
            in --> empty

        Returns
        -------------
            data dict
    
    """

    webs = {}
    webs["carreteras"] = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=205"
    # webs['dominio_publico'] = 'https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=224'
    # webs['zona_afeccion'] = 'https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=226'
    # webs['zona_servidumbre'] = 'https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=227'
    webs["puentes"] = "https://opendata.aragon.es/" + Config.legacy + "/preview?view_id=225"

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
