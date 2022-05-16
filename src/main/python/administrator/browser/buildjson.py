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
        
        Parameters
        ----------
        result: Any
            Set of data result of the query
        bd_conector: String
            Connection to database

        Returns
        -------
        Union[List[Dict], str]

            Formatted results
        """

        if bd_conector is not "Virtuoso":
            return "Enviando resultados de peticion GET"
        response = []
        variables = result["head"]["vars"]
        results = result["results"]["bindings"]
        for r in results:
            content = {var: r[var]["value"] for var in variables if var in r}
            response.append(content)
        return response
