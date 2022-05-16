"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
"""
Command line beautifier, makes standard output colourful
"""


class Colors(object):
    TEST_PASSED = "\033[92m"
    TEST_FAILED = "\033[91m"
    ENDC = "\033[0m"


class Symbols(object):
    TICK_MARK = "\u2714"
    FAIL_MARK = "\u2718"


def text_with_color(*args, color):
    return color + " ".join(str(s) for s in args) + Colors.ENDC


def print_passed(*args):
    print(text_with_color("[PASS]", *args, Symbols.TICK_MARK, color=Colors.TEST_PASSED))


def print_failed(*args):
    print(text_with_color("[FAIL]", *args, Symbols.FAIL_MARK, color=Colors.TEST_FAILED))
