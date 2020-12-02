'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from browser import Browser

if __name__ == "__main__":
    buscador = Browser()
    # #Info general
    # buscador.search({"question":"A qué comarca pertenece el municipio Zaragoza","intents":["ComarcaMunicipio"], "entities":["Teruel"]} )
    # buscador.search({"question": "Cuál es la superficie de Zaragoza", "intents": ["SuperficieMunicipio"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuántos habitantes hay en Añon", "intents": ["HabitantesMunicipio"], "entities": ["Añon"]})
    # buscador.search({"question": "Cuál es la superficie total de secano en Zaragoza en el año 2006", "intents": ["SuperficieSecano", "Year"], "entities": ["Zaragoza", "2006"]})
    # buscador.search({"question": "Cuál es la superficie total de regadío en Zaragoza en el año 2006", "intents": ["SuperficieRegadio", "Year"], "entities": ["Zaragoza", "2006"]})
    # buscador.search({"question": "Cuál era la población de Añon en el año 2012", "intents": ["Poblacion", "Year"], "entities": ["Añon", "2012"]})
    # buscador.search({"question": "Cuál es el CIF del ayuntamiento de Zaragoza", "intents": ["CIFAyuntamiento"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuál es el teléfono del ayuntamiento de Zaragoza", "intents": ["TelefonoAyuntamiento"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuál es el email del ayuntamiento de Zaragoza", "intents": ["EmailAyuntamiento"], "entities": ["Zaragoza"]})
    # buscador.search({"question": "Quién es el alcalde del municipio de Zaragoza", "intents": ["Municipio", "Cargo"], "entities": ["Zaragoza", "Alcalde"]})
    # buscador.search({"question": "Quiénes son los concejales del municipio de Zaragoza", "intents": ["Municipio", "Cargo"],"entities": ["Zaragoza", "Concejal"]})
    # buscador.search({"question": "Cuál es el fax del ayuntamiento de Zaragoza", "intents": ["FaxAyuntamiento"],"entities": ["Zaragoza"]})
    # buscador.search({"question": "Cuál es la dirección del ayuntamiento de Zaragoza", "intents": ["DireccionAyuntamiento"], "entities": ["Zaragoza"]})

    # Gastronomía
    # buscador.search(
    #     {"question": "Cuál es el telefono del restaurante/cafetería Ginos Grancasa", "intents": ["telefonoRestaurante"],
    #                  "entities": ["Ginos Grancasa"]})
    # buscador.search(
    #     {"question": "Cuál es el fax del restaurante/cafetería Ginos Grancasa", "intents": ["faxRestaurante"],
    #      "entities": ["Pista Grande"]})
    # buscador.search(
    #     {"question": "Cuál es el email del restaurante/cafetería Ginos Grancasa", "intents": ["emailRestaurante"],
    #      "entities": ["Ginos Grancasa"]})
    # buscador.search(
    #     {"question": "Cuál es la pagina web del restaurante/cafetería Ginos Grancasa", "intents": ["webRestaurante"],
    #      "entities": ["MUERDE LA PASTA - GRANCASA"]})
    # buscador.search(
    #     {"question": "Cuál es la direccion del restaurante/cafetería Ginos Grancasa", "intents": ["direccionRestaurante"],
    #      "entities": ["Ginos Grancasa"]})
    # buscador.search(
    #     {"question": "Restaurantes/cafeterías en Zaragoza", "intents": ["restaurantesCiudad"],
    #      "entities": ["Zaragoza"]})
    # buscador.search(
    #     {"question": "Como puedo reservar en el restaurante Ginos Grancasa", "intents": ["reservaRestaurante"],
    #      "entities": ["Ginos Grancasa"]})
    # buscador.search(
    #     {"question": "Cuantas plazas tiene el restaurante Ginos Grancasa", "intents": ["plazasRestaurante"],
    #      "entities": ["Ginos Grancasa"]})
    # buscador.search(
    #     {"question": "Restaurantes en el municipio Zaragoza", "intents": ["numRestaurantes"],
    #      "entities": ["Zaragoza"]})
    # buscador.search(
    #     {"question": "Ciudad del restaurante Ginos Grancasa", "intents": ["municipioRestaurante"],
    #      "entities": ["GINOS GRANCASA"]})

    # Actividades
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
    #     {"question": "Cual es la informacion de contacto del guia turistico SOLANAS AÍSA BLANCA", "intents": ["informacionGuia"],
    #                  "entities": ["AMBROJ  MARTÍN MARÍA JESÚS"]})
    # buscador.search(
    #     {"question": "Cual es el telefono de la oficina de turismo de Zaragoza", "intents": ["telefonoTurismo"],
    #                  "entities": ["Teruel"]})
    # buscador.search(
    #     {"question": "Donde esta la oficina de turismo de Zaragoza", "intents": ["direccionTurismo"],
    #                  "entities": ["Zaragoza"]})

    # Alojamientos
    # buscador.search({"question": "Cual es el telefono del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})

    # buscador.search({"question": "Cual es el telefono del albergue FUNDACION ASISTENCIAL ATADES HUESCA",
    #                  "intents": ["telefonoAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["FUNDACION ASISTENCIAL ATADES HUESCA", "albergue"]})

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

    # buscador.search({"question": "Cual es el fax del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["faxAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})

    # buscador.search({"question": "Cual es el fax del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["faxAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})

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

    # buscador.search({"question": "Cual es la página web del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["webAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})

    # buscador.search({"question": "Cual es la página web del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["webAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})

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

    # buscador.search({"question": "Cual es la direccion del hotel HOTEL & SPA REAL VILLA ANAYET", "intents": ["direccionAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})

    # buscador.search({"question": "Cual es la direccion del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["direccionAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})

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

    # buscador.search({"question": "Dime el listado de hoteles en Zaragoza", "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["50", "hotel", "provincia"]})

    # buscador.search({"question": "Dime el listado de hoteles en Zaragoza", "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Zaragoza", "hotel", "municipio"]})

    # buscador.search({"question": "Dime el listado de albergues en Tarazona",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["50", "albergue", "provincia"]})

    # buscador.search({"question": "Dime el listado de albergues en Tarazona",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Jatiel", "albergue", "municipio"]})

    # buscador.search({"question": "Dime el listado de apartamentos en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["50", "apartamento", "provincia"]})

    # buscador.search({"question": "Dime el listado de apartamentos en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Zaragoza", "apartamento", "municipio"]})
    #
    # buscador.search({"question": "Dime el listado de casas rurales en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["50", "casa rural", "provincia"]})

    # buscador.search({"question": "Dime el listado de casas rurales en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Zaragoza", "casa rural", "municipio"]})
    #
    # buscador.search({"question": "Dime el listado de campings en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Zaragoza", "camping", "provincia"]})

    # buscador.search({"question": "Dime el listado de campings en Zaragoza",
    #                  "intents": ["listadoAlojamiento", "tipoAlojamiento", "tipoLugar"],
    #                  "entities": ["Zaragoza", "camping", "municipio"]})

    # buscador.search({"question": "Cual es el telefono de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["telefonoAgenciaViajes"],
    #                  "entities": ["ALMOZARA VIAJES"]})

    # buscador.search({"question": "Cual es el email de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["emailAgenciaViajes"],
    #                  "entities": ["ALMOZARA VIAJES"]})

    # buscador.search({"question": "Cual es la pagina web de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["webAgenciaViajes"],
    #                  "entities": ["TULAVIAJES"]})

    # buscador.search({"question": "Cual es la direccion de la agencia de viajes ALMOZARA VIAJES",
    #                  "intents": ["direccionAgenciaViajes"],
    #                  "entities": ["ALMOZARA VIAJES"]})

    # buscador.search({"question": "Dime las agencias de viajes de Zaragoza",
    #                  "intents": ["listAgenciaViajes"],
    #                  "entities": ["Zaragoza"]})

    # buscador.search({"question": "Como puedo reservar el albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})

    # buscador.search({"question": "Como puedo reservar el camping CAMPING LECINA, S.C.-LECINA",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING PINETA, S.L.-PINETA", "camping"]})

    # buscador.search({"question": "Como puedo reservar el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})

    # buscador.search({"question": "Como puedo reservar la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})

    # buscador.search({"question": "Como puedo reservar el hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["reservarAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})

    # buscador.search({"question": "Numero de hoteles en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "hotel"]})

    # buscador.search({"question": "Numero de casas rurales en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "casa rural"]})

    # buscador.search({"question": "Numero de apartamentos en Panticosa",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Panticosa", "apartamento"]})

    # buscador.search({"question": "Numero de campings en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "camping"]})

    # buscador.search({"question": "Numero de albergues en Zaragoza",
    #                  "intents": ["numeroAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "albergue"]})

    # buscador.search({"question": "Numero de plazas del albergue EXPLOTACIONES HOTELERAS VILLANUA, S.L.",
    #                  "intents": ["plazasAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["EXPLOTACIONES HOTELERAS VILLANUA, S.L.", "albergue"]})

    # buscador.search({"question": "Numero de plazas del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["plazasAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})

    # buscador.search({"question": "Numero de plazas de la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["plazasAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})

    # buscador.search({"question": "En que ciudad se encuentra el camping CAMPING PINETA, S.L.-PINETA",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CAMPING PINETA, S.L.-PINETA", "camping"]})

    # buscador.search({"question": "En que ciudad se encuentra el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})

    # buscador.search({"question": "En que ciudad se encuentra la casa rural CASA ARBOLEDA-LAFUENTE",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["CASA ARBOLEDA-LAFUENTE", "casa rural"]})

    # buscador.search({"question": "En que ciudad se encuentra el hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["ciudadAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})

    # buscador.search({"question": "Cual es la categoria del apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["categoriaAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento"]})

    # buscador.search({"question": "Cual es la categoria del hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["categoriaAlojamiento", "tipoAlojamiento"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel"]})

    # buscador.search({"question": "Hoteles en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "hotel"]})

    # buscador.search({"question": "Casas rurales en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "casa rural"]})

    # buscador.search({"question": "Apartamentos en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "apartamento"]})

    # buscador.search({"question": "Campings en la ciudad de Zaragoza",
    #                  "intents": ["alojamientoCiudad", "tipoAlojamiento"],
    #                  "entities": ["Zaragoza", "camping"]})

    # buscador.search({"question": "Cuando es temporada alta en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "alta"]})

    # buscador.search({"question": "Cuando es temporada baja en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "baja"]})

    # buscador.search({"question": "Cuando es temporada media en el apartamento BALCÓN DEL PIRINEO RURAL ORDESA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["BALCÓN DEL PIRINEO RURAL ORDESA", "apartamento", "media"]})

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

    # buscador.search({"question": "Cuando es temporada baja en la casa rural CASA LOS CEREZOS",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["CASA LOS CEREZOS", "casa rural", "baja"]})
    #
    # buscador.search({"question": "Cuando es temporada alta en el hotel HOTEL & SPA REAL VILLA ANAYET",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["HOTEL & SPA REAL VILLA ANAYET", "hotel", "alta"]})
    #
    # buscador.search({"question": "Cuando es temporada baja en el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "baja"]})
    #
    # buscador.search({"question": "Cuando es temporada media en el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #                  "intents": ["temporadaAlojamiento", "tipoAlojamiento", "tipoTemporada"],
    #                  "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "media"]})

    # buscador.search({"question": "Cuantas plazas para caravanas hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #                  "intents": ["caravanasCamping", "tipoAlojamiento"],
    #                  "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})

    # buscador.search(
    #     {"question": "Cuantas parcelas hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #      "intents": ["parcelasCamping", "tipoAlojamiento"],
    #      "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})

    # buscador.search(
    #     {"question": "Cuantos bungalows hay en el camping CAMPING DE LOS BAÑOS, S.L.-DE LOS BAÑOS",
    #      "intents": ["bungalowsCamping", "tipoAlojamiento"],
    #      "entities": ["CAMPING AINSA, S.L.-AINSA", "camping"]})

    # buscador.search(
    #     {"question": "Cuantos apartamentos tiene la casa rural CASA RURAL MORILLO",
    #      "intents": ["apartamentosCasaRural", "tipoAlojamiento"],
    #      "entities": ["CASA RURAL MORILLO", "casa rural"]})

    # buscador.search(
    #     {"question": "Cuantos habitaciones sencillas tiene la casa rural CASA RURAL MONTE PERDIDO",
    #      "intents": ["habitacionesSencillasCasaRural", "tipoAlojamiento"],
    #      "entities": ["CASA RURAL MONTE PERDIDO", "casa rural"]})

    # buscador.search(
    #     {"question": "Cuantos habitaciones dobles tiene la casa rural CASA RURAL MORILLO",
    #      "intents": ["habitacionesDoblesCasaRural", "tipoAlojamiento"],
    #      "entities": ["CASA RURAL MORILLO", "casa rural"]})

    # buscador.search(
    #     {"question": "Cuantos habitaciones tiene el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["HOTEL GOLF & SPA REAL BADAGUAS-JACA", "hotel", "total"]})

    # buscador.search(
    #     {"question": "Cuantos habitaciones con baño tiene el hotel HOTEL GOLF & SPA REAL BADAGUAS-JACA",
    #      "intents": ["habitacionesBañoHotel", "tipoAlojamiento"],
    #      "entities": ["ANTIGUA POSADA RODA", "hotel"]})

    # buscador.search(
    #     {"question": "Cuantos habitaciones sin baño tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["habitacionessinBañoHotel", "tipoAlojamiento"],
    #      "entities": ["SANDSTONE GUESTHOUSE 3", "hotel"]})

    # buscador.search(
    #     {"question": "Cuantas camas tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["camasHotel", "tipoAlojamiento"],
    #      "entities": ["SANDSTONE GUESTHOUSE 3", "hotel"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones cuadruples tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["SANDSTONE GUESTHOUSE 3", "hotel", "cuadruple"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones dobles tiene el hotel SANDSTONE GUESTHOUSE 3",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["SANDSTONE GUESTHOUSE 3", "hotel", "dobles"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones sencillas tiene el hotel GRAN HOTEL",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["GRAN HOTEL", "hotel", "sencillas"]})
    #
    # buscador.search(
    #     {"question": "Cuantas suits tiene el hotel GRAN HOTEL",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["GRAN HOTEL", "hotel", "suits"]})
    #
    # buscador.search(
    #     {"question": "Cuantas habitaciones triples tiene el hotel SOMMOS HOTEL BENASQUE",
    #      "intents": ["habitacionesHotel", "tipoAlojamiento", "tipoHabitacion"],
    #      "entities": ["SOMMOS HOTEL BENASQUE", "hotel", "triples"]})

    # buscador.search(
    #     {"question": "Que servicios tiene el hotel BALNEARIO GRAN HOTEL CASCADA",
    #      "intents": ["serviciosHotel", "tipoAlojamiento"],
    #      "entities": ["BALNEARIO GRAN HOTEL CASCADA", "hotel"]})

    buscador.search(
        {
            "question": "Que hoteles  con categoria 2 o superior hay en Zaragoza",
            "intents": ["alojamientoCiudad", "tipoAlojamiento", "categoria"],
            "entities": ["Zaragoza", "hotel", "2"],
        }
    )

    buscador.search(
        {
            "question": "Cuantas habitaciones con terraza tiene el hotel SOMMOS HOTEL BENASQUE",
            "intents": [
                "habitacionesTerrazaHotel",
                "tipoAlojamiento",
                "tipoHabitacion",
            ],
            "entities": ["SOMMOS HOTEL BENASQUE", "hotel"],
        }
    )
