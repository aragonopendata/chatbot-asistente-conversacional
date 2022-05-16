#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from numpy.testing._private.utils import assert_equal
from browser import Browser


class Test_generate_query_dataset(unittest.TestCase):
    buscador = Browser()

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.maxDiff = None


    def test_surface_burned_question(self):

        results = self.buscador.search(
        {"question": "cuantas hectareas se quemaron en Zaragoza en el año 2010",
         "intents": ["hectareasQuemadas", "tipoLocalizacion", "Year"],
         "entities": ["Zaragoza","municipio", "2010" ]})
        self.assertTrue  (results ,[{'answer0': '3.28', 'etiqueta': 'http://opendata.aragon.es/recurso/territorio/Municipio/Zaragoza', 'fecha': 'http://reference.data.gov.uk/id/year/2010'}])


    def test_surface_burned_sparql(self):

        results = self.buscador.generate_query(
            {
                "question": "cuantas hectareas se quemaron en Zaragoza en el año 2010",
                "intents": ["hectareasQuemadas", "tipoLocalizacion", "Year"],
                "entities": ["Zaragoza","municipio", "2010" ],
            }
        )
        self.assertEqual (results, 'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2av2#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT ?answer0 ?etiqueta ?fecha FROM <http://opendata.aragon.es/graph/datacube/04-040017TM> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .  filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "Z[aáAÁ]r[aáAÁ]g[oóOÓ]z[aáAÁ]", "i")   . ?municipio <http://opendata.aragon.es/def/iaest/medida#superficie-forestal-afectada> ?answer0 . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha .  filter REGEX(?fecha, STRDT(2010, xsd:string)) . }')

    @unittest.skip("revisad")
    def test_surface_artificial_question(self):

        results = self.buscador.search(
        {"question": "cuantas hectareas de superficies artificiales hay la provincia de Zaragoza",
         "intents": ["hectareasZona", "tipoLocalizacion", "tipoSuperficie"],
         "entities": ["Zaragoza","municipio", "superficies-artificiales" ]})
        self.assertTrue  (results ,[{'answer0': '12129.5', 'etiqueta': 'http://opendata.aragon.es/recurso/territorio/Municipio/Zaragoza'}])


    #def test_surface_artificial_sparql(self):

        results = self.buscador.generate_query(
        {"question": "cuantas hectareas de superficies artificiales hay la provincia de Zaragoza",
        "intents": ["hectareasZona", "tipoLocalizacion","tipoSuperficie"],
        "entities": ["Zaragoza","municipio","superficies-artificiales" ]})

        self.assertEqual (results, 'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT ?answer0 ?etiqueta  FROM <http://opendata.aragon.es/graph/datacube/04-040009TM> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .  filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "Z[aáAÁ]r[aáAÁ]g[oóOÓ]z[aáAÁ]", "i")   . ?municipio <http://opendata.aragon.es/def/iaest/medida#superficie-has> ?answer0 . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha_uri . BIND(xsd:integer(SUBSTR(STRDT(?fecha_uri , xsd:string),38,4)) as ?fecha_int ) .  filter(?fecha_int = ?fecha ) .  { SELECT DISTINCT MAX(xsd:integer(?max)) as ?fecha FROM <http://opendata.aragon.es/graph/datacube/04-040009TM> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha . BIND(SUBSTR(STRDT(?fecha, xsd:string),38,4) as ?max) . ?municipio <http://opendata.aragon.es/def/iaest/medida#superficie-has> ?answer0 .  }}?municipio <http://opendata.aragon.es/def/iaest/dimension#corine-land-cover-2000-nivel-1-descripcion> ?aux1 .  filter REGEX(lcase(REPLACE(str(?aux1),"_"," ")), "s[uúUÚ]p[eéEÉ]rf[iíIÍ]c[iíIÍ][eéEÉ]s-[aáAÁ]rt[iíIÍ]f[iíIÍ]c[iíIÍ][aáAÁ]l[eéEÉ]s", "i")  }')


    def test_surface_artificial_aragon_question(self):

        results = self.buscador.search(
        {"question": "cuantas hectareas de superficies artificiales hay la provincia de Zaragoza",
        "intents": ["hectareasZona", "tipoLocalizacion", "tipoSuperficie"],
        "entities": ["Aragon","Aragon", "superficies-artificiales" ]})
        self.assertTrue  (results ,[{'answer0': '40260.6', 'etiqueta': 'http://opendata.aragon.es/recurso/territorio/ComunidadAutonoma/Aragón'}])

    @unittest.skip("revisad")
    def test_surface_artificial_aragon_sparql(self):

        results = self.buscador.generate_query(
        {"question": "cuantas hectareas de superficies artificiales hay la provincia de Zaragoza",
        "intents": ["hectareasZona", "tipoLocalizacion","tipoSuperficie"],
        "entities": ["Aragon","Aragon","superficies-artificiales" ]})

        self.assertEqual (results, 'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT ?answer0 ?etiqueta  FROM <http://opendata.aragon.es/graph/datacube/04-040009A> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .  filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "[aáAÁ]r[aáAÁ]g[oóOÓ]n", "i")   . ?municipio <http://opendata.aragon.es/def/iaest/medida#superficie-has> ?answer0 . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha_uri . BIND(xsd:integer(SUBSTR(STRDT(?fecha_uri , xsd:string),38,4)) as ?fecha_int ) .  filter(?fecha_int = ?fecha ) .  { SELECT DISTINCT MAX(xsd:integer(?max)) as ?fecha FROM <http://opendata.aragon.es/graph/datacube/04-040009A> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha . BIND(SUBSTR(STRDT(?fecha, xsd:string),38,4) as ?max) . ?municipio <http://opendata.aragon.es/def/iaest/medida#superficie-has> ?answer0 .  }}?municipio <http://opendata.aragon.es/def/iaest/dimension#corine-land-cover-2000-nivel-1-descripcion> ?aux1 .  filter REGEX(lcase(REPLACE(str(?aux1),"_"," ")), "s[uúUÚ]p[eéEÉ]rf[iíIÍ]c[iíIÍ][eéEÉ]s-[aáAÁ]rt[iíIÍ]f[iíIÍ]c[iíIÍ][aáAÁ]l[eéEÉ]s", "i")  }')


    def test_hectareas_rustico_zaragoza_question(self):
    #el ultimo dato de suelo rustico para zaragoza no hay datos.
        results = self.buscador.search(
        {"question": "Cuantas hectareas de suelo rustico hay en Zaragoza",
        "intents": ["hectareasZona", "tipoLocalizacion", "tipoSuperficie"],
        "entities": ["Zaragoza","municipio", "rustico"  ]})
        self.assertEqual  (results ,[])

    @unittest.skip("revisad")
    def test_hectareas_rustico_zaragoza_sparql(self):

        results = self.buscador.generate_query(
        {"question": "Cuantas hectareas de suelo rustico hay en Zaragoza",
        "intents": ["hectareasRustico", "tipoLocalizacion", "tipoSuperficie"],
        "entities": ["Zaragoza","municipio" , "rustico" ]})

        self.assertEqual (results, 'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT ?answer0 ?etiqueta  FROM <http://opendata.aragon.es/graph/datacube/04-040009TM> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .  filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "Z[aáAÁ]r[aáAÁ]g[oóOÓ]z[aáAÁ]", "i")   . ?municipio <http://opendata.aragon.es/def/iaest/medida#superficie-has> ?answer0 . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha_uri . BIND(xsd:integer(SUBSTR(STRDT(?fecha_uri , xsd:string),38,4)) as ?fecha_int ) .  filter(?fecha_int = ?fecha ) .  { SELECT DISTINCT MAX(xsd:integer(?max)) as ?fecha FROM <http://opendata.aragon.es/graph/datacube/04-040009TM> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha . BIND(SUBSTR(STRDT(?fecha, xsd:string),38,4) as ?max) . ?municipio <http://opendata.aragon.es/def/iaest/medida#superficie-has> ?answer0 .  }}?municipio <http://opendata.aragon.es/def/iaest/dimension#corine-land-cover-2000-nivel-1-descripcion> ?aux1 .  filter REGEX(lcase(REPLACE(str(?aux1),"_"," ")), "r[uúUÚ]st[iíIÍ]c[oóOÓ]", "i")  }')

    @unittest.skip("revisar")
    def test_empresas_por_sector_sparql(self):
        # no hay datos a nivel municipio/ comarca
        results = self.buscador.generate_query(
        {"question": "Cuantas empresas por el sector de la mineria hay en Zaragoza",
        "intents": ["empresasPorSector", "tipoLocalizacion", "sector"],
        "entities": ["Zaragoza","municipio" , "construccion" ]})

        self.assertEqual (results, 'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2a#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT SUM(?answer0) as ?answer0 ?etiqueta  FROM <http://opendata.aragon.es/graph/datacube/05-050102TM> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .  filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "Z[aáAÁ]r[aáAÁ]g[oóOÓ]z[aáAÁ]", "i")   . ?municipio <http://opendata.aragon.es/def/iaest/medida#numero-empresas> ?answer0 . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha_uri . BIND(xsd:integer(SUBSTR(STRDT(?fecha_uri , xsd:string),38,4)) as ?fecha_int ) .  filter(?fecha_int = ?fecha ) .  { SELECT DISTINCT MAX(xsd:integer(?max)) as ?fecha FROM <http://opendata.aragon.es/graph/datacube/05-050102TM> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha . BIND(SUBSTR(STRDT(?fecha, xsd:string),38,4) as ?max) . ?municipio <http://opendata.aragon.es/def/iaest/medida#numero-empresas> ?answer0 .  }}?municipio <http://opendata.aragon.es/def/iaest/dimension#sector-descripcion> ?etiqueta2 .  filter REGEX(lcase(REPLACE(str(?etiqueta2),"_"," ")), "m[iíIÍ]n[eéEÉ]r[iíIÍ][aáAÁ]", "i")  }')

    def test_empresas_por_sector_pesca_aragon_dato(self):

        # tipo de sectores -> [construccion, agricultura-ganaderia-y-pesca, industria-y-energia, servicios]
        results = self.buscador.search(
        {"question": "Cuantas hectareas de suelo rustico hay en Zaragoza",
        "intents": ["empresasPorSector", "tipoLocalizacion", "sector"],
        "entities": ["Aragon","Aragon" , "pesca" ]})
        self.assertEqual (results, [{'answer0': '228367', 'etiqueta': 'http://opendata.aragon.es/recurso/territorio/ComunidadAutonoma/Aragón'}])


    def test_empresas_por_sector_pesca_aragon_sparql(self):

        # tipo de sectores -> [construccion, agricultura-ganaderia-y-pesca, industria-y-energia, servicios]
        results = self.buscador.generate_query(
        {"question": "Cuantas hectareas de suelo rustico hay en Zaragoza",
        "intents": ["empresasPorSector", "tipoLocalizacion", "sector"],
        "entities": ["Aragon","Aragon" , "pesca" ]})

        self.assertEqual (results, 'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2av2#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT SUM(?answer0) as ?answer0 ?etiqueta  FROM <http://opendata.aragon.es/graph/datacube/05-050102A> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .  filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "[aáAÁ]r[aáAÁ]g[oóOÓ]n", "i")   . ?municipio <http://opendata.aragon.es/def/iaest/medida#numero-empresas> ?answer0 .  { SELECT DISTINCT MAX(xsd:integer(?max)) as ?fecha FROM <http://opendata.aragon.es/graph/datacube/05-050102A> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha . BIND(SUBSTR(STRDT(?fecha, xsd:string),38,4) as ?max) . ?municipio <http://opendata.aragon.es/def/iaest/medida#numero-empresas> ?answer0 .  }}?municipio <http://opendata.aragon.es/def/iaest/dimension#sector-descripcion> ?etiqueta2 .  filter REGEX(lcase(REPLACE(str(?etiqueta2),"_"," ")), "p[eéEÉ]sc[aáAÁ]", "i")  }')

    """ dataset vacio
    def test_trabajadores_por_empresas_sparql(self):

        results = self.buscador.generate_query(
        {"question": "cuantos trabajadores hay en Aragon",
        "intents": ["empresasPorTrabajadores", "tipoLocalizacion", "numTrabajadores"],
        "entities": ["Aragon" ]})
        self.assertEqual (results, '')
    """
    # el motor de ejecucion de sparl:
    # se establece que intenciones puedo ejecutar
    # intents -> son las queries que se pueden construir
    # tiene que llevar pareja una entidad
    def test_uso_del_suelo_sparql(self):

        results = self.buscador.generate_query(
        {"question": "que uso del suelo se dio en Aragon",
        "intents": ["usoSuelo", "tipoLocalizacion"],
        "entities": ["aragon","aragon"]})
        self.assertEqual (results, 'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ei2a: <http://opendata.aragon.es/def/ei2av2#> PREFIX locn: <http://www.w3.org/ns/locn#> PREFIX dbpedia: <http://dbpedia.org/ontology/> PREFIX openrec: <http://opendata.aragon.es/recurso/> PREFIX dbpprop: <http://dbpedia.org/property/> PREFIX aragopedia: <http://opendata.aragon.es/def/Aragopedia#> PREFIX sch: <http://schema.org/> PREFIX addr: <http://www.w3.org/ns/locn#> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX org: <http://www.w3.org/ns/org#> PREFIX vcard: <http://www.w3.org/2006/vcard/ns#> PREFIX sdmx-dimension: <http://purl.org/linked-data/sdmx/2009/dimension#> PREFIX iaest-medida: <http://opendata.aragon.es/def/iaest/medida#> PREFIX iaest-dimension: <http://opendata.aragon.es/def/iaest/dimension#> PREFIX protege: <http://protege.stanford.edu/rdf/HTOv4002#> PREFIX dc: <http://purl.org/dc/elements/1.1/> PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>SELECT DISTINCT ?answer0 ?etiqueta  FROM <http://opendata.aragon.es/graph/datacube/04-040012A> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta .  filter REGEX(lcase(REPLACE(str(?etiqueta),"_"," ")), "[aáAÁ]r[aáAÁ]g[oóOÓ]n", "i")   . ?municipio <http://opendata.aragon.es/def/iaest/dimension#corine-land-cover-2000-nivel-5-descripcion> ?aux1 . BIND(SUBSTR(STRDT(?aux1, xsd:string),80) as?answer0) .  { SELECT DISTINCT MAX(xsd:integer(?max)) as ?fecha FROM <http://opendata.aragon.es/graph/datacube/04-040012A> WHERE { ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?etiqueta . ?municipio <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> ?fecha . BIND(SUBSTR(STRDT(?fecha, xsd:string),38,4) as ?max) . ?municipio <http://opendata.aragon.es/def/iaest/dimension#corine-land-cover-2000-nivel-5-descripcion> ?aux1 .  }}}')
