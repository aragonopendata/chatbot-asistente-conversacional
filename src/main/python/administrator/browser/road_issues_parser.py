'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from browser.XmlController import xmlController
from browser.JSONController import jsonController
import json
from browser.Beautifulsoup import Beautifulsoup
from datetime import date

def parser():

    url_nueva = 'https://idearagon.aragon.es/servicios/rest/services/CARRETERAS/INCIDENCIAS/MapServer/identify?geometry=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&geometryType=esriGeometryEnvelope&sr=3857&layers=all:1,2&layerDefs=&time=1641826020000&layerTimeOptions=&tolerance=2&mapExtent=-897063.9684100994,4899283.903359297,731546.1201941827,5305922.992317238&imageDisplay=256,256,96&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=json'

    structuredData = {}

    jsconControllerVariable = jsonController()
    data = jsconControllerVariable.getContentJSON(url_nueva)
    final_data = []
    titles = []
    links = []
    for register in data:
        row = register['attributes']
        data = {
            "Denominacion": row['AFECCION'].strip(),
            "Tramo": row['PK_INI'].strip(),
            "Tipo de Limitación": row['CAUSA'].strip(),
            "Localidades" : row['TRAMO'].strip(),
            "Causa": row['CAUSA'].strip(),
            "Fecha": row['FECHA'].strip(),
            "Observaciones": row['OBSERVACIONES'].strip(),
        }
        final_data.append(data)
        titles.append(row['VIA'].strip())
        links.append(url_nueva)

    structuredData["title"] = titles
    structuredData["link"] = links
    structuredData["description"] = final_data

    return structuredData
