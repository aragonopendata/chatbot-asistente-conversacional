'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from browser.browser import Browser

if __name__ == "__main__":
    buscador = Browser()
    # #Info general
    # buscador.search({"question":"A qué comarca pertenece el municipio Zaragoza","intents":["ComarcaMunicipio"], "entities":["Teruel"]} )
    # buscador.search({"question": "Cuál es la superficie de Zaragoza", "intents": ["SuperficieMunicipio"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuántos habitantes hay en Añon", "intents": ["HabitantesMunicipio"], "entities": ["Añon"]})
    # buscador.search({"question": "Cuál es la superficie total de secano en Zaragoza en el año 2006", "intents": ["SuperficieSecano", "Year"], "entities": ["Zaragoza", "2008"]})
    # buscador.search({"question": "Cuál es la superficie total de regadío en Zaragoza en el año 2006", "intents": ["SuperficieRegadio", "Year"], "entities": ["Zaragoza", "2006"]})
    # buscador.search({"question": "Cuál es la superficie total de regadío en Zaragoza en el año 2006", "intents": ["SuperficieRegadio", "Year"], "entities": ["Zaragoza", "2006"]})
    # # buscador.search({"question": "Cuál era la población de Añon en el año 2012", "intents": ["Poblacion", "Year"], "entities": ["Añon", "2012"]})
    # buscador.search({"question": "Cuál es el CIF del ayuntamiento de Zaragoza", "intents": ["CIFAyuntamiento"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuál es el teléfono del ayuntamiento de Zaragoza", "intents": ["TelefonoAyuntamiento"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuál es el email del ayuntamiento de Zaragoza", "intents": ["EmailAyuntamiento"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Quién es el alcalde del municipio de Zaragoza", "intents": ["Municipio", "Cargo"], "entities": ["Zaragoza", "Alcalde"]})
    # buscador.search({"question": "Quiénes son los concejales del municipio de Zaragoza", "intents": ["Municipio", "Cargo"],"entities": ["Zaragoza", "Concejal"]})
    # buscador.search({"question": "Cuál es el fax del ayuntamiento de Zaragoza", "intents": ["FaxAyuntamiento"],"entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuál es la dirección del ayuntamiento de Zaragoza", "intents": ["DireccionAyuntamiento"], "entities": ["Zaragoza"]})
    #
    #
    # # Gastronomía
    # buscador.search(
    #     {"question": "Cuál es el telefono del restaurante/cafetería Ginos Grancasa", "intents": ["telefonoRestaurante"],
    #                  "entities": ["Las vegas"]})
    # buscador.search(
    #     {"question": "Cuál es el fax del restaurante/cafetería Ginos Grancasa", "intents": ["faxRestaurante"],
    #      "entities": ["EL FUELLE"]})
    # buscador.search(
    #     {"question": "Cuál es el email del restaurante/cafetería Ginos Grancasa", "intents": ["emailRestaurante"],
    #      "entities": ["KIKO"]})
    # buscador.search(
    #     {"question": "Cuál es la pagina web del restaurante/cafetería Ginos Grancasa", "intents": ["webRestaurante"],
    #      "entities": ["el torreon"]})
    # buscador.search(
    #     {"question": "Cuál es la direccion del restaurante/cafetería Ginos Grancasa", "intents": ["direccionRestaurante"],
    #      "entities": ["Olimpia"]})
    # buscador.search(
    #     {"question": "Restaurantes/cafeterías en Zaragoza", "intents": ["restaurantesCiudad"],
    #      "entities": ["Zaragoza"]})
    # buscador.search(
    #     {"question": "Como puedo reservar en el restaurante Ginos Grancasa", "intents": ["reservaRestaurante"],
    #      "entities": ["EL TORREON"]})
    # buscador.search(
    #     {"question": "Cuantas plazas tiene el restaurante Ginos Grancasa", "intents": ["plazasRestaurante"],
    #      "entities": ["Olimpia"]})
    # buscador.search(
    #     {"question": "Restaurantes en el municipio Zaragoza", "intents": ["numRestaurantes"],
    #      "entities": ["Zaragoza"]})
    # buscador.search(
    #     {"question": "Ciudad del restaurante Ginos Grancasa", "intents": ["municipioRestaurante"],
    #      "entities": ["cuchara"]})
    #
    # # Actividades
    # buscador.search(
    #     {"question": "Que obras tiene el museo diocesano de Jaca", "intents": ["obrasMuseo"],
    #                  "entities": ["Museo Diocesano de Jaca"]})
    # buscador.search(
    #     {"question": "Que museos hay en Zaragoza", "intents": ["museosLocalidad"],
    #                  "entities": ["Zaragoza"]})
    # buscador.search(
    #     {"question": "Donde se encuentra la obra Abrazo en la puerta dorada", "intents": ["municipioObra"],
    #                  "entities": ["Abrazo en la puerta dorada"]})
    # buscador.search(
    #     {"question": "Que rutas salen de Fraga", "intents": ["rutasOrigen"],
    #                  "entities": ["Teruel"]})

    # buscador.search(
    #     {"question": "Que rutas llegan a Borja", "intents": ["rutasDestino"],
    #                  "entities": ["Borja"]})
    # buscador.search(
    #     {"question": "Que rutas pasan por Utebo", "intents": ["rutasCamino"],
    #                  "entities": ["Utebo"]})
    # buscador.search(
    #     {"question": "Que rutas salen de Teruel y llega a Zaragoza", "intents": ["rutasOrigen", "rutasDestino"],
    #                  "entities": ["Teruel", "Zaragoza"]})
    # buscador.search(
    #     {"question": "Que guías de turismo hay en Borja", "intents": ["guiasLocalidad"],
    #                  "entities": ["Borja"]})
    # buscador.search(
    #     {"question": "Cual es el telefono del guia de turismo RAMOS MONGE DIEGO", "intents": ["telefonoGuia"],
    #                  "entities": ["RAMOS MONGE DIEGO"]})
    # buscador.search(
    #     {"question": "Cual es el email del guia de turismo RAMOS MONGE DIEGO", "intents": ["emailGuia"],
    #                  "entities": ["RAMOS MONGE DIEGO"]})
    # buscador.search(
    #     {"question": "Cual es la web del guia de turismo SOLANAS AÍSA BLANCA", "intents": ["webGuia"],
    #                  "entities": ["SOLANAS AÍSA BLANCA"]})
    # buscador.search(
    #     {"question": "Cual es la informacion de contacto del guia turistico AMBROJ  MARTÍN MARÍA JESÚS", "intents": ["informacionGuia"],
    #                  "entities": ["AMBROJ  MARTÍN MARÍA JESÚS"]})
    # buscador.search(
    #     {"question": "Cual es el telefono de la oficina de turismo de Zaragoza", "intents": ["telefonoTurismo"],
    #                  "entities": ["Teruel"]})
    # buscador.search(
    #     {"question": "Donde esta la oficina de turismo de Huesca", "intents": ["direccionTurismo"],
    #                  "entities": ["zARAGOZA"]})
    #
    # # Alojamientos
    # buscador.search({"question": "Cual es el telefono del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
    #
    # buscador.search({"question": "Cual es el telefono del albergue FUNDACION ASISTENCIAL ATADES HUESCA",
    #                  "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["FUNDACION ASISTENCIAL ATADES HUESCA", "albergue"]})
    #
    # buscador.search({"question": "Cual es el telefono del apartamento APARTAMENTOS FORATATA",
    #                  "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["APARTAMENTOS FORATATA", "apartamento"]})
    #
    # buscador.search({"question": "Cual es el telefono de la casa rural CASA RURAL MONTE PERDIDO",
    #                  "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA RURAL MONTE PERDIDO", "casa rural"]})
    #
    # buscador.search({"question": "Cual es el telefono del camping CAMPING PINETA, S.L.-PINETA",
    #                  "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING PINETA, S.L.-PINETA", "camping"]})
    #
    # buscador.search({"question": "Cual es el fax del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["faxAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
    #
    # buscador.search({"question": "Cual es el fax del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["faxAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
    #
    # buscador.search({"question": "Cual es el fax del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["faxAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "Cual es el fax de la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["faxAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
    #
    # buscador.search({"question": "Cual es el fax del camping CAMPING LECINA, S.C.-LECINA",
    #                  "intents": ["faxAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING LECINA, S.C.-LECINA", "camping"]})
    #
    # buscador.search({"question": "Cual es el email del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["emailAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
    #
    # buscador.search({"question": "Cual es el email del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["emailAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
    #
    # buscador.search({"question": "Cual es el email del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["emailAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "Cual es el email de la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["emailAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
    #
    # buscador.search({"question": "Cual es el email del camping CAMPING LECINA, S.C.-LECINA",
    #                  "intents": ["emailAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING LECINA, S.C.-LECINA", "camping"]})
    #
    # buscador.search({"question": "Cual es la página web del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["webAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Palafox", "hotel"]})
    #
    # buscador.search({"question": "Cual es la página web del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["webAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
    #
    # buscador.search({"question": "Cual es la página web del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["webAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "Cual es la página web de la casa rural CASA RURAL MONTE PERDIDO",
    #                  "intents": ["webAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA RURAL MONTE PERDIDO", "casa rural"]})
    #
    # buscador.search({"question": "Cual es la página web del camping CAMPING LECINA, S.C.-LECINA",
    #                  "intents": ["webAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING LECINA, S.C.-LECINA", "camping"]})
    #
    # buscador.search({"question": "Cual es la direccion del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["direccionAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
    #
    # buscador.search({"question": "Cual es la direccion del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["direccionAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
    #
    # buscador.search({"question": "Cual es la direccion del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["direccionAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "Cual es la direccion de la casa rural CASA RURAL MONTE PERDIDO",
    #                  "intents": ["direccionAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA RURAL MONTE PERDIDO", "casa rural"]})
    #
    # buscador.search({"question": "Cual es la direccion del camping CAMPING LECINA, S.C.-LECINA",
    #                  "intents": ["direccionAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING LECINA, S.C.-LECINA", "camping"]})
    #
    # buscador.search({"question": "Dime el listado de hoteles en Zaragoza", "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Bajo Cinca", "hotel", "comarca"]})
    # #
    # buscador.search({"question": "Dime el listado de albergues en Tarazona",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["50", "albergue", "provincia"]})
    #
    # buscador.search({"question": "Dime el listado de apartamentos en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["50", "apartamento", "provincia"]})
    #
    # buscador.search({"question": "Dime el listado de casas rurales en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["50", "casa rural", "provincia"]})
    #
    # buscador.search({"question": "Dime el listado de campings en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Huesca", "camping", "municipio"]})
    #
    # buscador.search({"question": "Cual es el telefono de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["telefonoAgenciaViajes"],
    #                  "entities": ["ALMOZARA VIAJES"]})
    #
    # buscador.search({"question": "Cual es el email de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["emailAgenciaViajes"],
    #                  "entities": ["ALMOZARA VIAJES"]})
    #
    # buscador.search({"question": "Cual es la pagina web de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["webAgenciaViajes"],
    #                  "entities": ["TULAVIAJES"]})
    #
    # buscador.search({"question": "Cual es la direccion de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["direccionAgenciaViajes"],
    #                  "entities": ["ALMOZARA VIAJES"]})
    #
    # buscador.search({"question": "Dime las agencias de viajes de Zaragoza",
    #                  "intents": ["listAgenciaViajes"],
    #                  "entities": ["Zaragoza"]})
    #
    # buscador.search({"question": "Como puedo reservar el albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
    #
    # buscador.search({"question": "Como puedo reservar el camping CAMPING LECINA, S.C.-LECINA",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING PINETA, S.L.-PINETA", "camping"]})
    #
    # buscador.search({"question": "Como puedo reservar el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "Como puedo reservar la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
    #
    # buscador.search({"question": "Como puedo reservar el hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
    #
    # buscador.search({"question": "Numero de hoteles en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "hotel"]})
    #
    # buscador.search({"question": "Numero de casas rurales en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "casa rural"]})
    #
    # buscador.search({"question": "Numero de apartamentos en Panticosa",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Panticosa", "apartamento"]})
    #
    # buscador.search({"question": "Numero de campings en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "camping"]})
    #
    # buscador.search({"question": "Numero de albergues en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "albergue"]})
    #
    # buscador.search({"question": "Numero de plazas del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["plazasAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})
    #
    # buscador.search({"question": "Numero de plazas del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["plazasAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "Numero de plazas de la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["plazasAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
    #
    # buscador.search({"question": "En que ciudad se encuentra el camping CAMPING PINETA, S.L.-PINETA",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING PINETA, S.L.-PINETA", "camping"]})
    #
    # buscador.search({"question": "En que ciudad se encuentra el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "En que ciudad se encuentra la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})
    #
    # buscador.search({"question": "En que ciudad se encuentra el hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["palafox", "hotel"]})
    #
    # buscador.search({"question": "Cual es la categoria del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["categoriaAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})
    #
    # buscador.search({"question": "Cual es la categoria del hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["categoriaAlojamiento", "tipoAlojamiento"],
    #                   "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})
    #
    # buscador.search({"question": "Hoteles en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "hotel"]})
    #
    # buscador.search({"question": "Casas rurales en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "casa rural"]})
    #
    # buscador.search({"question": "Apartamentos en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "apartamento"]})
    #
    # buscador.search({"question": "Campings en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "camping"]})
    #
    # buscador.search({"question": "Cuando es temporada alta en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "alta"]})
    #
    # buscador.search({"question": "Cuando es temporada baja en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "baja"]})
    #
    # buscador.search({"question": "Cuando es temporada media en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "media"]})
    #
    # buscador.search({"question": "Cuando es temporada alta en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS", "camping", "alta"]})
    #
    # buscador.search({"question": "Cuando es temporada baja en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS", "camping", "baja"]})
    #
    # buscador.search({"question": "Cuando es temporada media en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS", "camping", "media"]})
    #
    # buscador.search({"question": "Cuando es temporada baja en la casa rural CASA LOS CEREZOS",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["CASA LOS CEREZOS", "casa rural", "baja"]})
    #
    # buscador.search({"question": "Cuando es temporada alta en el hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["Palafox", "hotel", "alta"]})
    #
    # buscador.search({"question": "Cuando es temporada baja en el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["palafox", "hotel", "baja"]})
    #
    # buscador.search({"question": "Cuando es temporada media en el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "media"]})
    #
    # buscador.search({"question": "Cuantas plazas para caravanas hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #                  "intents": ["caravanasCamping", "tipoAlojamiento"],
    #                  "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})
    #
    # buscador.search(
    #     {"question": "Cuantas parcelas hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #      "intents": ["parcelasCamping", "tipoAlojamiento"],
    #      "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})
    #
    # buscador.search(
    #     {"question": "Cuantos bungalows hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #      "intents": ["bungalowsCamping", "tipoAlojamiento"],
    #      "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})
    #
    # buscador.search(
    #     {"question": "Cuantos apartamentos tiene la casa rural CASA RURAL MORILLO",
    #      "intents": ["apartamentosCasaRural", "tipoAlojamiento"],
    #      "entities": ["CASA RURAL MORILLO", "casa rural"]})
    #
    # buscador.search(
    #     {"question": "Cuantos habitaciones sencillas tiene la casa rural CASA RURAL MONTE PERDIDO",
    #      "intents": ["habitacionesSencillasCasaRural", "tipoAlojamiento"],
    #      "entities": ["CASA RURAL MONTE PERDIDO", "casa rural"]})
    #
    # buscador.search(
    #     {"question": "Cuantos habitaciones dobles tiene la casa rural CASA RURAL MORILLO",
    #      "intents": ["habitacionesDoblesCasaRural", "tipoAlojamiento"],
    #      "entities": ["CASA RURAL MORILLO", "casa rural"]})
    #
    # buscador.search(
    #     {"question": "Cuantos habitaciones tiene el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "total"]})
    #
    # buscador.search(
    #     {"question": "Cuantos habitaciones con baño tiene el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #      "intents": ["habitacionesBañoHotel", "tipoAlojamiento"],
    #      "entities": ["Palafox", "hotel"]})
    #
    # buscador.search(
    #     {"question": "Cuantos habitaciones sin baño tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["habitacionessinBañoHotel", "tipoAlojamiento"],
    #      "entities": ["SANDSTONE GUESTHOUSE 3", "hotel"]})
    #
    # buscador.search(
    #     {"question": "Cuantas camas tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["camasHotel", "tipoAlojamiento"],
    #      "entities": ["Palafox", "hotel"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones cuadruples tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["SANDSTONE GUESTHOUSE 3", "hotel", "cuadruple"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones dobles tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["palafox", "hotel", "dobles"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones sencillas tiene el hotel GRAN HOTEL",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["Palafox", "hotel", "sencillas"]})
    #
    # buscador.search(
    #     {"question": "Cuantas suits tiene el hotel GRAN HOTEL",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["palafox", "hotel", "suits"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones triples tiene el hotel SOMMOS HOTEL BENASQUE",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["SOMMOS HOTEL BENASQUE", "hotel", "triples"]})
    #
    # buscador.search(
    #     {"question": "Que servicios tiene el hotel BALNEARIO GRAN HOTEL CASCADA",
    #      "intents": ["serviciosHotel", "tipoAlojamiento"],
    #      "entities": ["palafox", "hotel"]})
    #
    # buscador.search(
    #     {"question": "Que hoteles  con categoria 2 o superior hay en Zaragoza",
    #      "intents": ["alojamientoCiudad", "tipoAlojamiento", "categoria"],
    #      "entities": ["Zaragoza", "hotel", "2"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones con terraza tiene el hotel SOMMOS HOTEL BENASQUE",
    #      "intents": ["habitacionesTerrazaHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["SOMMOS HOTEL BENASQUE", "hotel"]})
    #
    #
    #
    # ##############
    # # agricultura #
    # ##############
    #
    # buscador.search(
    #     {"question": "Cuales son las comarcas agrarias del SOBRARBE",
    #      "intents": ["comarcasAgrariasLocalizacion"],
    #      "entities": ["SOBRARBE"]})
    # #
    # buscador.search(
    #     {"question": "A que municipio pertenece la comarca agraria Calatayud",
    #      "intents": ["municipioComarcasAgrarias"],
    #      "entities": ["Calatayud"]})
    #
    # buscador.search(
    #     {"question": "Cuales son las villas y tierras del municipio",
    #      "intents": ["villasLocalizacion"],
    #      "entities": ["SOBRARBE"]})
    #
    # buscador.search(
    #     {"question": "A que municipio pertenece la villa MANC. FORESTAL SIN, SEÑES Y SERVETO",
    #      "intents": ["municipioVilla"],
    #      "entities": ["MANC. FORESTAL SIN, SEÑES Y SERVETO"]})
    #
    # buscador.search(
    #     {"question": "Informacion sobre la villa MANC. FORESTAL SIN, SEÑES Y SERVETO",
    #      "intents": ["infoVilla"],
    #      "entities": ["MANC. FORESTAL SIN, SEÑES Y SERVETO"]})
    #
    # buscador.search(
    #     {"question": "Que fincas tienen cultivo leñoso en el CINCA MEDIO",
    #      "intents": ["fincasCultivoLenoso"],
    #      "entities": ["Zuera"]})
    #
    # # buscador.search(
    # #     {"question": "Fincas de cultivo leñoso de secano en el VALDEJALON",
    # #      "intents": ["fincasSecanoLenosas"],
    # #      "entities": ["CINCA MEDIO"]})
    #
    # # buscador.search(
    # #     {"question": "Fincas de cultivo leñoso de regadio en el CINCA MEDIO",
    # #      "intents": ["fincasRegadioLenosas"],
    # #      "entities": ["CINCA MEDIO"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de agricultura ecologica en Aragon en 2013",
    #      "intents": ["hectareasAgriculturaEcologica", "Year", "tipoLocalizacion"],
    #      "entities": ["Aragon", "", "Aragon"]})
    # #
    # buscador.search(
    #     {"question": "Hectareas de agricultura ecologica en Teruel en 2013",
    #      "intents": ["hectareasAgriculturaEcologica", "Year", "tipoLocalizacion"],
    #      "entities": ["Teruel", "2013", "provincia"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de agricultura ecologica en Jacetania en 2013",
    #      "intents": ["hectareasAgriculturaEcologica", "Year", "tipoLocalizacion"],
    #      "entities": ["Jacetania", "2013", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de agricultura ecologica en Zaragoza en 2013",
    #      "intents": ["hectareasAgriculturaEcologica", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "2013", "municipio"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de olivares en Aragon en 1989",
    #      "intents": ["hectareasOlivares", "Year", "tipoLocalizacion"],
    #      "entities": ["Aragon", "", "Aragon"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de olivares en la comarca de Jacetania en 1989",
    #      "intents": ["hectareasOlivares", "Year", "tipoLocalizacion"],
    #      "entities": ["Jacetania", "1989", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de olivares en el municipio de Zaragoza en 1989",
    #      "intents": ["hectareasOlivares", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "1989", "municipio"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de olivares en la provincia de Teruel en 1989",
    #      "intents": ["hectareasOlivares", "Year", "tipoLocalizacion"],
    #      "entities": ["Teruel", "1989", "provincia"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de viñedos en Aragon en 1989",
    #      "intents": ["hectareasVinedos", "Year", "tipoLocalizacion"],
    #      "entities": ["Aragon", "1989", "Aragon"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de viñedos en la comarca de Jacetania en 1989",
    #      "intents": ["hectareasVinedos", "Year", "tipoLocalizacion"],
    #      "entities": ["Jacetania", "1989", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de viñedos en el municipio de Zaragoza en 1989",
    #      "intents": ["hectareasVinedos", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "1989", "municipio"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de viñedos en la provincia de Teruel en 1989",
    #      "intents": ["hectareasVinedos", "Year", "tipoLocalizacion"],
    #      "entities": ["Teruel", "1989", "provincia"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de frutales en Aragon en 1989",
    #      "intents": ["hectareasFrutales", "Year", "tipoLocalizacion"],
    #      "entities": ["Aragon", "1989", "Aragon"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de frutales en la comarca de Jacetania en 1989",
    #      "intents": ["hectareasFrutales", "Year", "tipoLocalizacion"],
    #      "entities": ["Jacetania", "1989", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de frutales en el municipio de Zaragoza en 1989",
    #      "intents": ["hectareasFrutales", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "1989", "municipio"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de frutales en la provincia de Teruel en 1989",
    #      "intents": ["hectareasFrutales", "Year", "tipoLocalizacion"],
    #      "entities": ["Teruel", "1989", "provincia"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de herbaceos en Aragon en 1989",
    #      "intents": ["hectareasHerbaceos", "Year", "tipoLocalizacion"],
    #      "entities": ["Aragon", "1989", "Aragon"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de herbaceos en la comarca de Jacetania en 1989",
    #      "intents": ["hectareasHerbaceos", "Year", "tipoLocalizacion"],
    #      "entities": ["Jacetania", "1989", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de herbaceos en el municipio de Zaragoza en 1989",
    #      "intents": ["hectareasHerbaceos", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "1989", "municipio"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de herbaceos en la provincia de Teruel en 1989",
    #      "intents": ["hectareasHerbaceos", "Year", "tipoLocalizacion"],
    #      "entities": ["Teruel", "1989", "provincia"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de regadio en Aragon en 1989",
    #      "intents": ["hectareasRegadio", "Year", "tipoLocalizacion"],
    #      "entities": ["Aragon", "1989", "Aragon"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de regadio en la comarca de Jacetania en 1989",
    #      "intents": ["hectareasRegadio", "Year", "tipoLocalizacion"],
    #      "entities": ["Jacetania", "1989", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de regadio en el municipio de Zaragoza en 1989",
    #      "intents": ["hectareasRegadio", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "1989", "municipio"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de regadio en la provincia de Teruel en 1989",
    #      "intents": ["hectareasRegadio", "Year", "tipoLocalizacion"],
    #      "entities": ["Teruel", "1989", "provincia"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de secano en Aragon en 1989",
    #      "intents": ["hectareasSecano", "Year", "tipoLocalizacion"],
    #      "entities": ["Aragon", "1989", "Aragon"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de secano en la comarca de Jacetania en 1989",
    #      "intents": ["hectareasSecano", "Year", "tipoLocalizacion"],
    #      "entities": ["Jacetania", "1989", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de secano en el municipio de Zaragoza en 1989",
    #      "intents": ["hectareasSecano", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "1989", "municipio"]})
    #
    # buscador.search(
    #     {"question": "Hectareas de secano en la provincia de Teruel en 1989",
    #      "intents": ["hectareasSecano", "Year", "tipoLocalizacion"],
    #      "entities": ["Teruel", "1989", "provincia"]})
    #

    ############
    ##ARAGON
    ############


    #buscador.search(
    #    {"question": "Cual es la poblacion en la provincia de Teruel en 2005",
    #     "intents": ["Poblacion", "Year", "tipoLocalizacion"],
    #     "entities": ["Teruel", "", "provincia"]})
    #
    # buscador.search(
    #     {"question": "Cual es la poblacion en la comarca de Jacetania en 2005",
    #      "intents": ["Poblacion", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "", "comarca"]})
    #
    # buscador.search(
    #     {"question": "Cual es la poblacion en el municipio de Zaragoza en 2005",
    #      "intents": ["Poblacion", "Year", "tipoLocalizacion"],
    #      "entities": ["Zaragoza", "", "municipio"]})

    # buscador.search(
    #     {"question": "Cuantas personas viven en la provincia de Teruel provenientes de America en el año 2005",
    #      "intents": ["poblacionExtranjera", "Year", "tipoArea", "tipoLocalizacion", "nombreArea", "sexo"],
    #      "entities": ["Teruel", "2005",  "continente", "provincia", "africa","hombres"]})
    #
    # buscador.search(
    #     {"question": "Cuantos contenedores de vidrio hay en Aragon",
    #      "intents": ["numContenedoresVidrio", "tipoLocalizacion"],
    #      "entities": ["Aragon", "Aragon"]})
    #
    # buscador.search(
    #     {"question": "Cuantos kilos de vidrio se recogieron en Aragon en 2012",
    #      "intents": ["kilosVidrioRecogidos", "tipoLocalizacion", "Year"],
    #      "entities": ["Aragon", "Aragon", "2011"]})
    #
    # buscador.search(
    #     {"question": "Cuantas hectareas de superficies artificiales hay en aragon",
    #      "intents": ["hectareasZona", "tipoLocalizacion", "tipoSuperficie"],
    #      "entities": ["Aragon", "Aragon", "superficies-artificiales"]})
    #
    # buscador.search(
    #     {"question": "cuantos incendios hubo en aragon en 2012",
    #      "intents": ["numIncendios", "tipoLocalizacion", " Year"],
    #      "entities": ["Aragon", "Aragon", "2012"]})
    #
    # buscador.search(
    #     {"question": "cuantas hectareas se quemaron en aragon en 2012",
    #      "intents": ["hectareasQuemadas", "tipoLocalizacion", " Year"],
    #      "entities": ["Aragon", "Aragon", "2012"]})
    #
    # buscador.search(
    #     {"question": "cuantas depuradoras hay aragon en 2012",
    #      "intents": ["numDepuradoras", "tipoLocalizacion", " Year"],
    #      "entities": ["Aragon", "Aragon", "2012"]})
    #
    # buscador.search(
    #     {"question": "Cuantos hombres autonomos hay dados de alta en el marzo del 2012 en Aragon",
    #      "intents": ["numeroAutonomos", "tipoLocalizacion", " Year", "sexo"],
    #      "entities": ["Teruel", "provincia", "2012-03", "hombres"]})
    #
    #buscador.search(
    #    {"question": "Cuantos hombres parados hay en el sector servicios en 2012 en Aragon",
    #     "intents": ["numParados", "tipoLocalizacion", " Year", "sexo", "sector"],
    #     "entities": ["Aragon", "Aragon", "2011", "hombres", "servicios"]})
    #
    #
    # buscador.search(
    #     {"question": "Cuantos hombres contratados en marzo en 2012 en Aragon",
    #      "intents": ["numContratados", "tipoLocalizacion", " Year", "sexo",],
    #      "entities": ["Jacetania", "comarca", "2012-03", "hombres"]})
    #
    # buscador.search(
    #     {"question": "Cuantos accidentes laborales hubo en 2012 en Aragon",
    #      "intents": ["numAccidentesLaborales", "tipoLocalizacion", " Year", "sexo",],
    #      "entities": ["Jacetania", "comarca", "2012", ""]})
    #
    # buscador.search(
    #     {"question": "Cual es la renta per capita en 2012 en Aragon",
    #      "intents": ["rentaPerCapita", "tipoLocalizacion", " Year"],
    #      "entities": ["Jacetania", "comarca", "2012"]})
    #
    # buscador.search(
    #     {"question": "Empresas entre 1-9 trabajadores en marzo de 2012 en Teruel",
    #      "intents": ["empresasPorTrabajadores", "tipoLocalizacion", " Year", "numTrabajadores"],
    #      "entities": ["Teruel", "provincia", "2012-03", "10-a-19"]})
    #
    # buscador.search(
    #     {"question": "Empresas del sector servicios en Teruel",
    #      "intents": ["empresasPorSector", "tipoLocalizacion", "sector"],
    #      "entities": ["Zaragoza", "provincia", "industria"]})
    #
    # buscador.search(
    #     {"question": "Empresas dedicadas a la hosteleria  en la provincia de Teruel",
    #      "intents": ["empresasPorActividad", "tipoLocalizacion", "actividad", "Year"],
    #      "entities": ["Teruel", "provincia", "hosteleria", "2012"]})
    #
    # buscador.search(
    #     {"question": "Que uso se le da al suelo en la provincia de Teruel",
    #      "intents": ["usoSuelo", "tipoLocalizacion", "Year"],
    #      "entities": ["Teruel", "comarca", ""]})
    #
    # buscador.search(
    #     {"question": "Cuantas hectareas de suelo rustico hay en la provincia de Teruel",
    #      "intents": ["hectareasTipoSuelo", "tipoLocalizacion", "Year", "tipoSuelo"],
    #      "entities": ["Teruel", "comarca", "", "rustico"]})
    #
    # buscador.search(
    #     {
    #         "question": "Cuantos edificios de mas de 50 años hay en la provincia de Teruel",
    #         "intents": ["antiguedadEdificios", "tipoLocalizacion", "antiguedad"],
    #         "entities": ["Zaragoza", "comarca", ""],
    #     })
    #
    from datetime import datetime
    now = datetime.now()
    print(now)

    result = buscador.search(
        {"question": "Qué carreteras",
         "intents": ["calendarHolidaysWhere"],
         "entities": ["Zaragoza"]})

    print(str(result))

    now = datetime.now()
    print(now)