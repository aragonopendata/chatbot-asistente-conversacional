'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
import sys
from io import StringIO


class Capturing(list):
    """
    Auxiliar class to capture standard output and reduce execution time.
    Printing is an expensive operation

    The class is used as a context manager.
    Example:
        code...
        with Capturing():
            ... whichever expensive code with lot of stdout prints ...

        more code...
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout
