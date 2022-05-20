"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
class InfoTemas:
    description_catalog = {
        'http://datos.gob.es/kos/sector-publico/sector/sector-publico': ["Sector Público", "sector publico"],
        'http://datos.gob.es/kos/sector-publico/sector/medio-ambiente': ["Medio Ambiente", "medio ambiente"],
        'http://datos.gob.es/kos/sector-publico/sector/turismo': [
            "Turismo",
            "turismo",
        ],
        'https://www.geonames.org/ontology#REST': [
            "Restauración",
            "restauracion",
        ],
        'https://www.geonames.org/ontology#A.ADMD': [
            "Consorcios y Agrupaciones",
            "consorcios",
        ],
        'https://www.geonames.org/ontology#L.INDS': ["Industria", "industria"],
        'https://www.geonames.org/ontology#P.PPLL': [
            "Organizaciones",
            "organizaciones",
        ],
        'https://www.geonames.org/ontology#HTL': [
            "Alojamientos Hosteleros",
            "alojamientos",
        ],
        'http://opendata.aragon.es/kos/promotor': ["Promotores", "promotores"],
        'https://www.geonames.org/ontology#A.ADM1': [
            "Organismos",
            "organismos",
        ],
        'https://www.geonames.org/ontology#LIBR': ["Bibliotecas", "bibliotecas"],
        'https://www.geonames.org/ontology#MUS': ["Museos", "museos"],
        'https://www.geonames.org/ontology#CTRM': [
            "Centros de Salud",
            "centros salud",
        ],
        'http://datos.gob.es/kos/sector-publico/sector/deporte': [
            "Asociaciones Deportivas",
            "asociaciones deportivas",
        ],
        'http://datos.gob.es/kos/sector-publico/sector/cultura-ocio': ["Patrimonio Cultural", "cultura"],
        'http://opendata.aragon.es/kos/oficina-consumidor': ["Oficina Consumidor", "consumidor"],
        'http://datos.gob.es/kos/sector-publico/sector/ciencia-tecnologia': ["Aguas", "aguas"],
        'https://www.geonames.org/ontology#AGRC': ["Sector Agrario", "sector agrario"],
        'https://www.geonames.org/ontology#SCH': ["Centros educativos", "educacion"],
        'http://datos.gob.es/kos/sector-publico/sector/salud': ["Sector Salud", "salud"],
        'https://www.geonames.org/ontology#A.ADM3': ["Comarcas", "comarcas"],
        'https://www.geonames.org/ontology#P.PPL': ["Datos agregados", "agregados"],
        'https://www.geonames.org/ontology#A.ADM2': ["Explotaciones Ganaderas", "explotaciones ganaderas"],
        'https://www.geonames.org/ontology#SNTR': ["Centros Salud Mental", "salud mental"],
    }

    themeDescription = {
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-punto-informacion-turistica': [
            "Puedes preguntarme por oficinas de turismo. Dónde están, su teléfono, su  email, etc…",
            "puntos de información turística",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-empresas-turismo-activo': ["--. ", "empresas de turismo activo"],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamiento-hotelero': [
            "Puedes preguntarme por alojamiento hotelero. Dónde están, su teléfono, su  email, número de camas, categoría, tipos de habitaciones, etc…",
            "alojamientos hoteleros",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-camping-turistico': [
            "Tengo información sobre campings. Dónde están, su teléfono, su  email, número de plazas, bungalows, etc…",
            "campings",
        ],
        'http://opendata.aragon.es/recurso/turismo/organizacion/registro-apartamento-turistico': [
            "Puedes preguntarme por apartamentos turisticos. Dónde están, su teléfono, su  email, etc…",
            "apartamentos turisticos",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-alojamientos-turismo-rural': [
            "Tengo muchos datos de casas rurales. Dónde están, su teléfono, su  email, etc…",
            "casas rurales",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-oficina-turismo': [
            "Puedes preguntarme por oficinas de turismo. Dónde están, su teléfono, su  email, etc…",
            "oficinas de turismo",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-cafeteria-restaurante': [
            "Tengo mucha información de cafeterías y restaurantes. Dónde están, cómo reserevar, su teléfono, su  email, su web, etc…",
            "cafeterias y restaurantes",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-albergue-refugio': [
            "Puedes preguntarme por albergues y refugios. Dónde están, su teléfono, su  email, etc…",
            "albergues y refugios",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-agencias-viaje': [
            "Puedes preguntarme por agencias de viaje. Dónde están, su teléfono, su  email, etc…",
            "agencias de viaje",
        ],
        'http://opendata.aragon.es/recurso/cultura-ocio/documento/coleccion-museos': [
            "Puedes preguntarme por obras de arte. En qué museo están.",
            "obras de arte",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/registro-guia-turismo': [
            "Puedes preguntarme por guías turísticos. Dónde están, su teléfono, su  email, etc…",
            "guías turísticos",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/documento/simbolo': ["--. ", "-"],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/comarca': [
            "Puedes preguntarme por las comarcas. Qué municipos lo componen, quién es el presidente, etc…",
            "comarcas",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/municipio': [
            "Puedes preguntarme por los municipios. Dónde está el ayuntamiento, su teléfono, fax,  quién es el alcalde, etc…",
            "municipios",
        ],
        'http://opendata.aragon.es/recurso/ciencia-tecnologia/dispositivo-iot/captacion': [
            "Tengo información de reciclaje de vidrio. Cuantos kilos de vidrio recogido en un año.",
            "reciclaje de vidrio",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/sociedad-mercantil': [
            "Puedes preguntarme por los contratos de empleo. Cuantos contratos se hicieron por año y sexo.",
            "contratos de empleo",
        ],
        'http://opendata.aragon.es/recurso/sector-publico/organizacion/poligono-industrial': [
            "Puedes preguntarme por ....",
            "polígonos industriales",
        ],
    }


    allTemas = ["certificacion-energetica","dominio","proteccion-datos","direccion-interes","fundacion","organismo-autonomo","organizacion-complementaria","sociedad-mercantil","sucursal","unidad-organizativa",
        "inaga-terreno-cinegetico-no-cinegeticos-aragon",
        "registro-agencias-viaje", "registro-alojamientos-turismo-rural", "registro-camping-turistico", "registro-empresas-turismo-activo", "registro-guia-turismo", "registro-oficina-turismo", "registro-punto-informacion-turistica", "registro-apartamento-turistico",
        "registro-cafeteria-restaurante",
        "agrupacion-secretarial", "consorcio",
        "poligono-industrial",
        "entidad-menor", "entidad-singular", "nucleo",
        "registro-albergue-refugio", "registro-alojamiento-hotelero",
        "promotor",
        "organismo",
        "definicion-biblioteca",
        "museo",
        "asociacion", "federacion",
        "patrimonio", "ruta-cultural",
        "oficina-consumidor",
        "edar",
        "sgt-agricultura-comarca-agraria", "sgt-agricultura-oficinas-comarcales",
        "centro-educativo",
        "hospital",
        "instalacion-sanitaria",
        "comarca",
        "municipio",
        "diputacion",
        "centro-salud-mental"]
