'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import requests
from lxml import etree
import os
import xmltodict
from functools import lru_cache

class xmlController:

    @lru_cache(maxsize=None)
    def getXmlContent(self, url):

        self.url = url
        data = requests.get(url)
        return data.text

    def createFile(self, filename, text):

        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        return 0

    def removeFile(self, filename):

        os.remove(filename)

    def getXMLObject(self, filename):

        tree = etree.parse(filename)
        self.removeFile(filename)
        self.tree = tree

    def getDataInDictFormat(self):

        self.dataDictFormat = xmltodict.parse(
            etree.tostring(self.tree).decode("utf-8"), dict_constructor=dict
        )

    def getDataDictFormat(self):

        return self.dataDictFormat
