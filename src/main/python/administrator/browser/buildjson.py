'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
# -*- coding: utf-8 -*-

"""
"results": [
        {
            "label": "",
            "url": "",
            "uri": "",
            "image": "",
            "score": "",
            "source": "",
            "id": "",
            "type": "",
            "docs": [
                {
                    "label": "",
                    "url": "",
                    "uri": "",
                    "image": "",
                    "score": "",
                    "source": "",
                    "id": "",
                    "type": ""
                }
            ]
        }
    ]
"""

from typing import List, Dict, Any, Union

"""
{'head': 
{'link': [], 'vars': ['answer0']},
 'results': 
 {'distinct': False, 
 'ordered': True, 
 'bindings': [
     {'answer0': {
        'type': 'typed-literal', 
        'datatype': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 
        'value': '387442'}}, 
    {'answer0': {
        'type': 'typed-literal', 
        'datatype': 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 
        'value': '367438'}}]}}
"""


class BuildJson:
    """
    Class used for building a valid JSON for Python with the
    answer of the question made to the Virtuoso DB

    It only purposes is to parse an answer of the database into
    an structured and standard format: JSON
    """

    @staticmethod
    def build_json(result: Any, bd_conector: str) -> Union[List[Dict], str]:
        """
        Return a dictionary with the information found in the database
        """

        if bd_conector is "Virtuoso":
            response = []
            variables = result["head"]["vars"]
            resultados = result["results"]["bindings"]
            for r in resultados:
                content = {}
                for var in variables:
                    if var in r:
                        content[var] = r[var]["value"]
                response.append(content)
            return response
        else:
            return "Enviando resultados de peticion GET"
