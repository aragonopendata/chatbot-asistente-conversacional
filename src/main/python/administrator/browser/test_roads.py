"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from browser.browser import Browser

if __name__ == "__main__":
    buscador = Browser()
    
    result = buscador.search(
        {
            "question": "Cuántos kilómetros tiene la carretera ",
            "intents": ["transportRoadLengthOrigen", "transportRoadLengthDestino"],
            "entities": ["Fago", "Villarreal"],
        }
    )

    print(str(result))
