"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
import requests
from lxml import etree
import os
import xmltodict
from functools import lru_cache

class xmlController:

    """ This class controls all  the operation related by XML. """

    @lru_cache(maxsize=None)
    def getXmlContent(self, url):

        """ This function gives the content of a web site in JSON structre. 
        Parameter:
        ----------
            url str
            """

        self.url = url
        data = requests.get(url)
        return data.text

    def createFile(self, filename, text):

        """ This function stores the text variable in the file (it is  stored at filename file).
        Parameter:
        ----------
            filename str
            text str

        Returns
        ----------
            0 int

            """

        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        return 0

    def removeFile(self, filename):

        """ This function remove the file (it is  stored at filename file).
        Parameter:
        ----------
            filename str
            """

        os.remove(filename)

    def getXMLObject(self, filename):

        """ This function transforms the filename's value in a XML structure.
        Parameter:
        ----------
            filename str

        Returns
        ----------
            xmltree self.tree

            """

        tree = etree.parse(filename)
        self.removeFile(filename)
        self.tree = tree

    def getDataInDictFormat(self):

        """ This function transforms from a XML variable to a dictionarly.
        Returns
        ----------
            self.dataDictFormat dict

            """
        self.dataDictFormat = xmltodict.parse(
            etree.tostring(self.tree).decode("utf-8"), dict_constructor=dict
        )

    def getDataDictFormat(self):

        """ This function recovers the self.dataDictFormat variable's value. """

        return self.dataDictFormat
