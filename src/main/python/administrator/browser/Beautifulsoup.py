import json
import requests
from bs4 import BeautifulSoup


class Beautifulsoup:
    """Python library for pulling data out of HTML and XML files
    """

    def transformBeautifulSoup(self, page):
        soup = BeautifulSoup(page, "html.parser")
        self.soup = soup
        return soup

    def getPrintPrettyStructure(self):
        return self.soup.prettify()

    def findTag(self, tag):
        return self.soup.find(tag)

    def findTags(self, tag):
        return self.soup.find_all(tag)

    def findClasses(self, tag):
        return self.soup.find(class_=tag)

    def findClass(self, tag):
        return self.soup.find_all(class_=tag)

    def findId(self, idValue):
        return self.soup.find(id=idValue)

    def findIds(self, idValue):
        return self.soup.find_all(id=idValue)

    def getTextData(self, findClass):
        return self.findClass.get_text()
