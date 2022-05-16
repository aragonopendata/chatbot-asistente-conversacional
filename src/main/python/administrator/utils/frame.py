"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
# Available frames ATM
from typing import Union

FRAMES = ["aragon", "citizensinfo", "engagement", "farming", "tourism", "transport"]


def get_frame_by_intent(intent_name: Union[str, None]) -> str:
    """
    Get the frame of the intent [intent_name], the first part
    of the intent until the first dot . represents the frame
    """
    if intent_name is not None:
        # AttributeError: 'NoneType' object has no attribute 'split'
        # This should not happen

        try:
            frame = intent_name.split(".")[0]
            return frame if frame in FRAMES else "smalltalk"
        except AttributeError:
            return "Unknown"

    return "Unknown"
