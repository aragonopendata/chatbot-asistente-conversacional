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
