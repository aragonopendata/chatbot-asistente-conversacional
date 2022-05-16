"""
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
"""
from ckan_connector.ckanSearch import CKANSearch
from time import time
import logging

OPENDATA_URL_COLUMN = "opendata_url"

questions = []
questions += ["Que informacion tienes sobre sociedad de la información?"]
questions += ["Qué información tienes sobre administración electrónica?"]
questions += ["Qué Información de transporte tienes?"]
questions += ["De qué información de transporte dispones?"]
questions += ["Qué información de transporte hay en Aragón?"]
questions += ["Qué información de transporte hay en Aragón Open"]
questions += ["Info transporte Aragon"]
questions += ["Información de transporte en Aragón"]
questions += ["De qué datos de movilidad dispones?"]
questions += ["Datos movilidad Aragón"]
questions += ["Qué información de movilidad tienes?"]
questions += ["Cuántos accidentes de tráfico ha habido en Aragón?"]
questions += ["Tienes información de accidentes de tráfico?"]
questions += ["Qué empresas de autobuses hay en Aragón?"]
questions += ["Qué rutas de transporte hay en Aragón?"]
questions += ["Qué horarios de rutas de transporte hay en Aragón?"]
questions += ["Qué información hay sobre agricultura en Aragón?"]
questions += ["Qué información hay sobre agricultura"]
questions += ["Tienes datos de la PAC"]
questions += ["información de la PAC en Aragón?"]
questions += ["Qué tipos de cultivos hay en Aragón?"]
questions += ["Qué datos tienes sobre el sector agrario"]
questions += ["Qué información hay sobre ganadería en Aragón?"]
questions += ["Qué explotaciones ganaderas hay en Aragón?"]

questions_esp = []
questions_esp += ["horario de farmacias"]
questions_esp += ["Horario de farmacias en Aragón"]
questions_esp += ["Información del coronavirus en Aragón"]
questions_esp += ["Datos del Covid"]
questions_esp += ["Datos de afiliados a la Seguridad Social en Aragón"]
questions_esp += ["afiliados"]
questions_esp += ["Qué datos de convenios hay en Aragón?"]
questions_esp += ["que datos de contratación hay en Aragón?"]
questions_esp += ["Qué licitaciones hay? "]
questions_esp += ["Que festivos hay en Aragón?"]
questions_esp += ["Días festivos en Aragón?"]
questions_esp += ["Cual es el catálogo de datos abiertos del gobierno de Aragón"]
questions_esp += ["Qué información tienes de presupuestos?"]
questions_esp += ["consumidor"]
questions_esp += ["Tienes información de contratos del Gobierno de Aragón?"]
questions_esp += ["Cual es el calendario escolar?"]
questions_esp += ["Qué información tienes de abastecimientos?"]
questions_esp += ["Qué información tienes de saneamientos?"]
questions_esp += ["tienes información sobre empleo público?"]
questions_esp += ["que museos hay en Aragón?"]
questions_esp += ["tines datos de los expedientes INAGA?"]
questions_esp += ["que información tienes sobre los proyectos Erasmus?"]
questions_esp += ["cómo solicitar una licencia?"]
questions_esp += ["hay datos de las elecciones"]
questions_esp += ["que son las ordenanzas municipales"]
questions_esp += ["Qué senderos hay en Aragón?"]
questions_esp += ["cuales son los poligonos industriales que hay en Aragón?"]
questions_esp += ["Días festivos en Aragón 2021?"]
questions_esp += ["Cual es el calendario escolar 2021?"]
questions_esp += ["Datos de Covid en Aragón / Datos de Coronavirus"]
questions_esp += ["Cual es el Calendario Escolar en Aragón 2021"]
questions_esp += ["alojamientos"]
questions_esp += ["Municipios de Aragón"]
questions_esp += ["Información sobre los municipios de Aragón"]

questions_ei2a = []
questions_ei2a += ["Que informacion tienes sobre sociedad de la información?"]
questions_ei2a += ["Qué Información de transporte tienes?"]
questions_ei2a += ["Qué información de transporte hay en Aragón?"]
questions_ei2a += ["Info transporte Aragon"]
questions_ei2a += ["Información de transporte en Aragón"]
questions_ei2a += ["Qué rutas de transporte hay en Aragón?"]
questions_ei2a += ["consumidor"]
questions_ei2a += ["Qué información tienes de abastecimientos?"]
questions_ei2a += ["Qué información tienes de saneamientos?"]
questions_ei2a += ["hay datos de las elecciones"]
questions_ei2a += ["que son las ordenanzas municipales"]
questions_ei2a += ["Qué senderos hay en Aragón?"]
questions_ei2a += ["alojamientos"]
# No es la primera opción
questions_ei2a += ["Información sobre los municipios de Aragón"]
questions_ei2a += ["Qué información de transporte hay en Aragón Open"]
questions_ei2a += ["Qué empresas de autobuses hay en Aragón?"]
questions_ei2a += ["Qué horarios de rutas de transporte hay en Aragón?"]
questions_ei2a += ["Qué tipos de cultivos hay en Aragón?"]
questions_ei2a += ["Horario de farmacias en Aragón"]
questions_ei2a += ["Cual es el catálogo de datos abiertos del gobierno de Aragón"]
questions_ei2a += ["ué información tienes de presupuestos?"]
questions_ei2a += ["Tienes información de contratos del Gobierno de Aragón?"]
questions_ei2a += ["tines datos de los expedientes INAGA?"]


logging.basicConfig(level=logging.INFO)

ckan_object = CKANSearch()


def estrategia3_bert(questions_set):

    print("ESTRATEGIA 3.1. Búsqueda de tags próximas a palabras de la pregunta + bert con pregunta completa")

    for question in questions_set:
        start_time = time()
        results = ckan_object.question_by_tags(question, True, True)
        elapsed_time = time() - start_time

        if results is not None:
            if len(results) == 0:
                logging.info("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
                print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
            else:
                for package in results:
                    logging.info(
                        "Question [{0} - {3}] --> URL: {1} [{2}] TAGS: {5}\tDISTANCE: {4}\tVISITS: {6}\tUPDATE: {7}".format(
                            question, package['title'],
                            package[OPENDATA_URL_COLUMN],
                            elapsed_time, package['distance'], package['tags'],
                            package['visits'], package['updated']))
                    print("Question [{0} - {3}] --> URL: {1} [{2}] TAGS: {5}\tDISTANCE: {4}\tVISITS: {6}\tUPDATE: {7}".format(
                        question, package['title'],
                        package[OPENDATA_URL_COLUMN],
                        elapsed_time, package['distance'], package['tags'],
                        package['visits'], package['updated']))
        else:
            logging.info("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
            print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))


class TestClassCKAN:
    #  entity_list = [
    # {'confidence': 1.0, 'dictionary': 'person', 'end': 4, 'entity': 'person', 'start': 0, 'value': 'Dame',
    # 'extractor': 'ITAEntityExtractor'},
    #  {'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'COVID-19',
    #  'extractor': 'ITAEntityExtractor'}]

    def test_estrategia1_bert(self):

        print("ESTRATEGIA 1.1. Pregunta completa + bert (sin stopwords)")

        for question in questions_esp:
            start_time = time()
            results = ckan_object.question_by_package_complete(question, True, True)
            elapsed_time = time() - start_time

            if results is not None:
                if len(results) == 0:
                    print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
                else:
                    for package in results:
                        print("Question [{0} - {3}] --> URL: {1} [{2}]".format(question, package['title'],
                                                                               package[OPENDATA_URL_COLUMN],
                                                                               elapsed_time))
            else:
                print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))

    def test_estrategia1_bert_stopwords(self):

        print("ESTRATEGIA 1.2. Pregunta completa + bert (con stopwords)")
        for question in questions_esp:
            start_time = time()
            results = ckan_object.question_by_package_complete(question, False, True)
            elapsed_time = time() - start_time

            if results is not None:
                if len(results) == 0:
                    print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
                else:
                    for package in results:
                        print("Question [{0} - {3}] --> URL: {1} [{2}]".format(question, package['title'],
                                                                               package[OPENDATA_URL_COLUMN],
                                                                               elapsed_time))
            else:
                print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))

    def test_estrategia1_scope(self):

        print("ESTRATEGIA 1.3. Pregunta completa + scope")

        for question in questions_esp:
            start_time = time()
            results = ckan_object.question_by_package_complete(question, False, False)
            elapsed_time = time() - start_time

            if results is not None:
                if len(results) == 0:
                    print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
                else:
                    for package in results:
                        print("Question [{0} - {3}] --> URL: {1} [{2}]".format(question, package['title'],
                                                                               package[OPENDATA_URL_COLUMN],
                                                                               elapsed_time))
            else:
                print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))

    def test_estrategia3_vector(self):
        print("ESTRATEGIA 3.1. Búsqueda de tags próximas a palabras de la pregunta + bert con pregunta completa")

        # print("VECTOR QUESTIONS - Preguntas generalizadas")
        # estrategia3_bert(questions)

        # print("VECTOR QUESTIONS_ESP - Preguntas especializadas")
        # estrategia3_bert(questions_esp)

        print("VECTOR QUESTIONS_ESP - Preguntas EI2A")
        estrategia3_bert(questions_ei2a)

    def test_estrategia3_bert_stopwords(self):
        print("ESTRATEGIA 3.2. Búsqueda de tags próximas a palabras de la pregunta + bert (con stopwords)")
        for question in questions_esp:
            start_time = time()
            results = ckan_object.question_by_tags(question, False, True)
            elapsed_time = time() - start_time

            if results is not None:
                if len(results) == 0:
                    print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
                else:
                    for package in results:
                        print("Question [{0} - {3}] --> URL: {1} [{2}]".format(question, package['title'],
                                                                               package[OPENDATA_URL_COLUMN],
                                                                               elapsed_time))
            else:
                print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))

    def test_estrategia3_scope(self):

        print("ESTRATEGIA 3.3. Búsqueda de tags próximas a palabras de la pregunta + bert con pregunta completa + "
              "scope")

        for question in questions_esp:
            start_time = time()
            results = ckan_object.question_by_tags(question, False, False)
            elapsed_time = time() - start_time

            if results is not None:
                if len(results) == 0:
                    print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))
                else:
                    for package in results:
                        print("Question [{0} - {3}] --> URL: {1} [{2}]".format(question, package['title'],
                                                                               package[OPENDATA_URL_COLUMN],
                                                                               elapsed_time))
            else:
                print("Question [{0} - {1}] --> SIN RESULTADOS]".format(question, elapsed_time))

    def test_ckan_question_covid_exacto(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'COVID-19',
                        'extractor': 'ITAEntityExtractor'}]


        result = ckan_object.question("dame información sobre COVID-19", entity_list)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        assert ('https://opendata.aragon.es/datos/catalogo/dataset/publicaciones-y-anuncios-relacionados-con-el-'
                'coronavirus-en-aragon' == result[0][OPENDATA_URL_COLUMN])

    def test_ckan_question_covid_incompleto(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'covid',
                        'extractor': 'ITAEntityExtractor'}]


        result = ckan_object.question("Dame información sobre covid", entity_list)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        assert ('https://opendata.aragon.es/datos/catalogo/dataset/'
                'publicaciones-y-anuncios-relacionados-con-el-coronavirus-en-aragon' == result[0][OPENDATA_URL_COLUMN])

    def test_ckan_question_covid_tag_not_found(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'covid19',
                        'extractor': 'ITAEntityExtractor'}]


        result = ckan_object.question("Dame información sobre covid19", entity_list)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        assert ('https://opendata.aragon.es/datos/catalogo/dataset/'
                'publicaciones-y-anuncios-relacionados-con-el-coronavirus-en-aragon' == result[0][OPENDATA_URL_COLUMN])

    def test_ckan_question_somport(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'Somport',
                        'extractor': 'ITAEntityExtractor'}]

        result = ckan_object.question("Está abierta la carretera de Somport", entity_list, True)

        print("***** CALCULO DE DISTANCIAS USANDO BERT *****")
        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        # assert ('https://opendata.aragon.es/datos/catalogo/dataset/
        # publicaciones-y-anuncios-relacionados-con-el-coronavirus-en-aragon' == url)

        print("***** CALCULO DE DISTANCIAS POR SCORE *****")
        result = ckan_object.question("Está abierta la carretera de Somport", entity_list, False)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        # assert ('https://opendata.aragon.es/datos/catalogo/dataset/
        # publicaciones-y-anuncios-relacionados-con-el-coronavirus-en-aragon' == url)

        result = ckan_object.question("Hay nieve en Somport", entity_list, True)

        print("***** CALCULO DE DISTANCIAS USANDO BERT *****")
        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        result = ckan_object.question("Hay nieve en  Somport", entity_list, True)

        print("***** CALCULO DE DISTANCIAS USANDO BERT *****")
        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'Formigal',
                        'extractor': 'ITAEntityExtractor'}]

        result = ckan_object.question("Está abierto Formigal", entity_list, True)

        print("***** CALCULO DE DISTANCIAS USANDO BERT *****")
        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        result = ckan_object.question("Esta abierto Formigal", entity_list, True)

        print("***** CALCULO DE DISTANCIAS USANDO BERT *****")
        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

    def test_ckan_question_covid_2_entidades(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'Dame',
                        'extractor': 'ITAEntityExtractor'},
                       {'confidence': 1.0, 'end': 28, 'entity': 'misc',  'start': 20, 'value': 'covid',
                        'extractor': 'ITAEntityExtractor'}]

        result = ckan_object.question("Dame información sobre covid", entity_list)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

    def test_ckan_question_zaragoza(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc',  'start': 20, 'value': 'Zaragoza',
                        'extractor': 'ITAEntityExtractor'}]

        result = ckan_object.question("Que me puedes contar de Zaragoza", entity_list)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

    def test_ckan_question_zaragoza_only_question(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'Zaragoza',
                        'extractor': 'ITAEntityExtractor'}]

        result = ckan_object.question_only_packages("Que me puedes contar de Zaragoza", entity_list, True)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        result = ckan_object.question_only_packages("Que me puedes contar de Zaragoza", entity_list, False)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL:{0} - {1} [{2}]".format(package['name'], package['title'], package[OPENDATA_URL_COLUMN]))

    def test_ckan_question_empleo_exacto(self):
        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'empleo',
                        'extractor': 'ITAEntityExtractor'}]

        result = ckan_object.question("información sobre empleo", entity_list)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        result = ckan_object.question_only_packages("información sobre empleo", entity_list, True)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL:{0} - {1} [{2}]".format(package['name'], package['title'], package[OPENDATA_URL_COLUMN]))

        entity_list = [{'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'Información',
                        'extractor': 'ITAEntityExtractor'},
                       {'confidence': 1.0, 'end': 28, 'entity': 'misc', 'start': 20, 'value': 'empleo',
                        'extractor': 'ITAEntityExtractor'}]

        result = ckan_object.question("Información sobre empleo", entity_list)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL: {0} [{1}]".format(package['title'], package[OPENDATA_URL_COLUMN]))

        result = ckan_object.question_only_packages("Información sobre empleo", entity_list, True)

        if result is not None:
            print("Número de paquetes devueltos:" + str(len(result)))
            for package in result:
                print("URL:{0} - {1} [{2}]".format(package['name'], package['title'], package[OPENDATA_URL_COLUMN]))


    def test_search_label_ei2a(self):

        start_time = time()

        results = ckan_object.get_packages("EI2A", False)
        elapsed_time = time() - start_time

        if results is not None:
            if len(results) == 0:
                logging.info("Nothing to show")
                print("Nothing to show")
            else:
                package_list = ckan_object.create_opendata_url(results)
                for package in package_list:
                    logging.info(
                            "Question [{0} - {3}] --> URL: {1} [{2}] TAGS: {5}\tDISTANCE: {4}\tVISITS: {6}\tUPDATE: {7}".format(
                                'EI2A', package['title'],
                                package[OPENDATA_URL_COLUMN],
                                elapsed_time, package['distance'], package['tags'],
                                package['visits'], package['updated']))
                    print("Question [{0} - {3}] --> URL: {1} [{2}] TAGS: {5}\tDISTANCE: {4}\tVISITS: {6}\tUPDATE: {7}".format(
                            'EI2A', package['title'],
                            package[OPENDATA_URL_COLUMN],
                            elapsed_time, package['distance'], package['tags'],
                            package['visits'], package['updated']))
        else:
            logging.info("Question [{0} - {1}] --> SIN RESULTADOS]".format("EI2A", elapsed_time))
            print("Question [{0} - {1}] --> SIN RESULTADOS]".format("EI2A", elapsed_time))