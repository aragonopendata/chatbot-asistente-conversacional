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

    texts_to_find = ["title", "link", "description"]
    today = date.today()
    max_title = 15
    fin_tramo = "tramo."

    beautifulsoup = Beautifulsoup()

    xmlControllerVariable = xmlController()
    text = xmlControllerVariable.getXmlContent(
        "http://www.carreterasdearagon.es/xml-ultimas-incidencias.php"
    )
    execution = xmlControllerVariable.createFile("data.xml", text)
    objectXML = xmlControllerVariable.getXMLObject("data.xml")
    xmlControllerVariable.getDataInDictFormat()
    dataJsonFormat = xmlControllerVariable.getDataDictFormat()

    jsconControllerVariable = jsonController()
    jsconControllerVariable.getJsonFormat(dataJsonFormat)
    objectJSONData = jsconControllerVariable.getJSONObject()
    structuredData = {}
    for text_to_find in texts_to_find:
        if text_to_find != "description":
            structuredData[text_to_find] = jsconControllerVariable.extract_values(
                json.loads(objectJSONData), text_to_find
            )
        else:
            structuredData["title"].pop()
            structuredData["link"].pop()
            results = jsconControllerVariable.extract_values(
                json.loads(objectJSONData), text_to_find
            )
            structureData = []
            for result in results[:-1]:
                result = (
                    result.replace("<p>", "")
                    .replace("</p>", "")
                    .replace("&oacute;", "ó")
                    .replace("\n\n", "\n")
                    .replace("\n\n", "\n")
                    .split("\n")
                )
                list_keys = {}
                for element in result:
                    try:
                        key = element.split(":")[0]
                        value = element.split(":")[1]
                        list_keys[key] = value.strip()
                    except:
                        list_keys["main"] = element
                structureData.append(list_keys)
            structuredData[text_to_find] = structureData
            html = results[len(results) - 1]
            html = html.replace("\n", "")
            html = html.replace("<div></div>", "")
            html = html.replace("<div><div>", "<div>")
            soup = beautifulsoup.transformBeautifulSoup(html)
            contents = soup.contents
            for content in contents:
                try:
                    texto = content.text
                    texto = texto.replace("<div>", "").replace("</div>", "")
                    title = texto.split("(")[0].strip()
                    denominacion = texto.split("(")[1].split(")")[0].strip()
                    try:
                        tramo = (
                            texto.split("(")[1].split(")")[1].split(fin_tramo)[0]
                            + "tramo"
                        )
                        tipo = (
                            texto.split("(")[1]
                            .split(")")[1]
                            .split(fin_tramo)[1]
                            .split(".")[0]
                        )
                        causa = (
                            texto.split("(")[1]
                            .split(")")[1]
                            .split(fin_tramo)[1]
                            .split(".")[0]
                        )
                        observaciones = (
                            texto.split("(")[1]
                            .split(")")[1]
                            .split(fin_tramo)[1]
                            .split(".")[1]
                        )
                    except:
                        tramo = ""
                        words = ["CADENAS", "CORTADA", "PRECAUCIÓN", "CORTE","PELIGRO","FRONTERA"]
                        position = -1
                        fin = ""
                        for word in words:
                            position = texto.find(word)
                            if position > -1:
                                fin = word
                                break
                        tipo = fin
                        causa = fin
                        observaciones = texto.split("(")[1].split(")")[1]
                    data = {
                        "Denominacion": denominacion.strip(),
                        "Tramo": tramo.strip(),
                        "Tipo de Limitación": tipo.strip(),
                        "Causa": causa.strip(),
                        "Fecha": str(today),
                        "Observaciones": observaciones.strip(),
                    }
                    if len(title) < max_title:
                        structuredData["title"].append(title)
                        structuredData["link"].append(
                            "http://www.carreterasdearagon.es/#" + title
                        )
                        structuredData["description"].append(data)
                except:
                    pass
    return structuredData
