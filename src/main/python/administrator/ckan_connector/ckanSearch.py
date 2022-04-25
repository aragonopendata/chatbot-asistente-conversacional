'''
  Asistente conversacional Aragón Open Data_v1.0.0
  Copyright © 2020 Gobierno de Aragón (España)
  Author: Instituto Tecnológico de Aragón (ita@itainnova.es)
  All rights reserved
'''
from __future__ import unicode_literals

import json
import logging
import string
import sys
import urllib.request
from urllib.parse import urlparse

import jellyfish
import nltk
import numpy as np
import pandas as pd
import scipy
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
import unidecode

URL_BASE = 'https://opendata.aragon.es/api/action/'
URL_OPENDATA_BASE = 'https://opendata.aragon.es/datos/catalogo/dataset/'
OPENDATA_URL_COLUMN = "opendata_url"
TAGL = 'tag_list'
TAGS = 'tag_show'
PACKAGE = 'package_search'
LIMIT_DS = 5        # Number of datasets to extract
MAX_DIST = 3        # Threshold levering distance
MAX_ROWS = 1000
BERT_THRESHOLD = 0.35  # Threshold to calculate bert distance. More than this threshold, sort by visits
LANGUAGE = "spanish"
SPECIFIC_SW_AOD = ['informacion', 'información', 'info', 'datos', 'aragon', 'aragón', 'zaragoza', 'huesca', 'teruel']


class CKANSearch:
    """Class which makes queries on CKAN in Aragón Open Data
       API'S Doc: https://opendata.aragon.es/herramientas/apis
       Connection string: https://opendata.aragon.es/api/action
    """

    def __init__(self):
        """ Initialisation of the class (embedder) for semantic search"""
        logging.basicConfig(level=logging.INFO)
        logging.info("Class initialization - CKANSearch")
        self.embedder = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        # bert-base-nli-mean-tokens
        # https://www.sbert.net/
        nltk.download('stopwords')
        nltk.download('punkt')
        self.nlp = spacy.load("es_core_news_sm")  # efficiency --> "es_core_news_sm"  # accuracy --> es_dep_news_trf

    @staticmethod
    def query_ckan(url_string):
        """ Performs the query provided on the CKAN of Aragon Open Data

        Parameters
        ----------
        url_string: String
            url of the query to execute

        Returns
        -------
        json dictionary

            Query result in json format.
            If the query failed it returns None
        """

        try:
            logging.info("** query_ckan **")
            logging.info(f" * Query to execute: {url_string}")
            response = urllib.request.urlopen(url_string)  # Ejecuta la consulta
            if response.code == 200:
                # Carga la respuesta para buscar las etiqueta y almacena las etiquetas en una lista
                response_dict = json.loads(response.read())
                logging.debug("Query Result:")
                logging.debug(response_dict)
                return response_dict
            else:
                logging.debug("Response of the query is not 200")
                return None
        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

    def get_tags(self, entity_list):
        """Returns all tags associated with entities provided over the user's question

        Parameters
        ----------
        entity_list: list
            List of entities over the user's question

        Returns
        -------
        list

            list of string with all the tags associated to the entity
        """

        logging.info("** get_tags **")
        logging.info(" * Entity List: {0}".format(entity_list))
        tag_list = []  # Tag list
        try:
            for ent in entity_list:  # Scroll through the list of labels
                if isinstance(ent, str):
                    entvalue = ent
                else:
                    entvalue = ent["value"]
                logging.debug(f"Entity: {entvalue}")
                url_string = URL_BASE + TAGL + '?query=' + urllib.parse.quote_plus(
                    entvalue)  # Build the query to search associated tags
                response_dict = self.query_ckan(url_string)
                if response_dict is not None and response_dict['success'] is True:
                    # When a result is provided
                    tag_list += response_dict['result']
                else:
                    logging.debug(f"No results for entity: {entvalue}")

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            tag_list = []

        return tag_list

    def get_all_tags(self):
        """Returns a list of all stored tags in the provided url

        Returns
        -------
        list

            list of string with all stored tags
        """
        logging.info("** get_all_tags **")

        tag_list = []  # Lista de etiquetas
        try:
            url_string = URL_BASE + TAGL
            response_dict = self.query_ckan(url_string)
            if response_dict is not None and response_dict['success'] is True:
                tag_list = response_dict['result']
            else:
                logging.warning("Something wrong is happening because no results")

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            tag_list = []

        return tag_list

    def get_packages(self, tag_name, filtering=False):
        """Returns all packages associated with the selected tag

        Parameters
        ----------
        tag_name: string
            Name of the tag to search packages

        filtering: bool
            Filtering selected datased by url or not

        Returns
        -------
        list

            list of packages
        """

        logging.info("** get_packages **")
        logging.info(" * Searched tag: {0}".format(tag_name))
        ds_list = []
        try:
            # url_string = URL_BASE + TAGS + '?id=' + urllib.parse.quote_plus(tag_name) + '&include_datasets=true'
            url_string = URL_BASE + PACKAGE + '?rows=' + str(MAX_ROWS) +'&fq=tags:' + \
                         urllib.parse.quote_plus('"' + tag_name + '"')

            response_dict = self.query_ckan(url_string)
            if response_dict is not None and response_dict['success'] is True:
                pck_list = response_dict['result']['results']
                # Scroll down for the packages collecting more important information
                # id, title, type, state, url, notes, tags
                for package in pck_list:
                    ds_info = dict(
                        id=package['id'],
                        title=package['title'],
                        name=package['name'],
                        type=package['type'],
                        state=package['state'],
                        url=package['url'],
                        notes=package['notes'],
                        tags=[d['name'] for d in package["tags"] if 'name' in d],
                        created=package['metadata_created'],
                        updated=package['metadata_modified'][:10],
                        visits=package['tracking_summary']['total'],
                        recent_visits=package['tracking_summary']['recent'],
                        organization=package['organization'],
                        resources=package['resources'],
                        extras=package['extras'],
                        distance=0,
                    )

                    if ds_info not in ds_list:
                        ds_list.append(ds_info)
            else:
                logging.debug("No packages associated to the tag {0}".format(tag_name))

            if len(ds_list) and filtering:
                # Filtering by URL
                ds_list = self.filtering_packages_by_url(ds_list)

        except Exception as exc:
            logging.error(
                f'Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}'
            )

            ds_list = []
        logging.debug("Number of returned packages {0}".format(len(ds_list)))
        return ds_list

    def get_packages_from_question(self, question, filtering=False):
        """Performing a query over package_search to determine by fuzzy which are the closest packages

        Parameters
        ----------
        question: string
            Question asked by the user

        filtering: bool
            Filtering selected datased by url or not

        Returns
        -------
        list

            list of packages
        """

        logging.info("** get_packages_from_question **")
        logging.info(" * Question: {0}".format(question))
        ds_list = []
        try:
            url_string = URL_BASE + PACKAGE + '?q=' + "'" + urllib.parse.quote_plus(question) + "'" + '~' + '&rows=' \
                         + str(MAX_ROWS)
            response_dict = self.query_ckan(url_string)
            if response_dict is not None and response_dict['success'] is True:
                pck_list = response_dict['result']['results']
                # Scroll down for the packages collecting more important information
                # id, title, type, state, url, notes, tags
                for package in pck_list:
                    ds_info = dict(
                        id=package['id'],
                        title=package['title'],
                        name=package['name'],
                        type=package['type'],
                        state=package['state'],
                        url=package['url'],
                        notes=package['notes'],
                        tags=[d['name'] for d in package["tags"] if 'name' in d],
                        created=package['metadata_created'],
                        updated=package['metadata_modified'][:10],
                        visits=package['tracking_summary']['total'],
                        recent_visits=package['tracking_summary']['recent'],
                        organization=package['organization'],
                        resources=package['resources'],
                        extras=package['extras'],
                        distance=0,
                    )

                    if ds_info not in ds_list:
                        ds_list.append(ds_info)
            else:
                logging.debug("No packages associated to the question {0}".format(question))

            if len(ds_list) and filtering:
                # Filtering by URL
                ds_list = self.filtering_packages_by_url(ds_list)

        except Exception as exc:
            logging.error(
                f'Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}'
            )

            ds_list = []
        logging.debug("Number of returned packages {0}".format(len(ds_list)))
        return ds_list

    @staticmethod
    def filtering_packages_by_url(packages_list):
        """Filtering selected dataset by URL [opendata.aragon.es, www.aragon.es]

        Parameters
        ----------
        packages_list: list
            List of packages to filtering

        Returns
        -------
        list

            list of packages only
        """

        logging.info("** filtering_packages_by_url **")

        try:
            # Convertir a DataFrame
            ds_df = pd.DataFrame(packages_list)
            # Filtering by the following URLs:  opendata.aragon.es o www.aragon.es
            output_df = ds_df.loc[ds_df['url'].str.contains("opendata.aragon.es")
                                  | ds_df['url'].str.contains("www.aragon.es")]
            ds_list = [] if output_df.empty else list(output_df.T.to_dict().values())

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

        return ds_list

    @staticmethod
    def get_minimum_levensthein_distance(elem, string_list):
        """Calculate the levensthein distance between 2 string

        Parameters
        ----------
        elem: string
            Name of the entity to calculate distance

        string_list: list
            List of tags in order to chose the closest one

        Returns
        -------
        list

            list of packages
        """

        logging.info("** get_minimum_levensthein_distance **")
        logging.info(" * Entity: {0}".format(elem))

        best_match = None
        best_distance = 10 ** 20
        try:
            for current_string in string_list:
                current_score = jellyfish.levenshtein_distance(elem.lower(), current_string.lower())
                if current_score < best_distance:
                    best_distance = current_score
                    best_match = current_string

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

        return best_match, best_distance

    def get_best_package_bert_distance(self, question, selected_pcks):
        """Select which package is the properest to the question using bert

        Parameters
        ----------
        question: string
            User's question

        selected_pcks: list
            List of packages found related to the question

        Returns
        -------
        dict

            Returns the most suitable package
        """

        logging.info("** get_best_package_bert_distance **")
        logging.info(" * question: {0}".format(question))

        try:
            packages_df = pd.DataFrame(selected_pcks)  # Convert list into Dataframe

            # Create corpus with packages notes
            corpus = packages_df['title'].tolist()
            corpus = list(map(lambda item: item.lower(), corpus))
            corpus_empeddings = self.embedder.encode(corpus)
            queries = [question.lower()]
            queries_embedding = self.embedder.encode(queries)

            # for query, query_embedding in zip(queries, queries_embedding):
            # The distance metric to use.If a string, the distance function can be ‘braycurtis’, ‘canberra’,
            # ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, ‘euclidean’, ‘hamming’, ‘jaccard’,
            # ‘jensenshannon’, ‘kulsinski’, ‘mahalanobis’, ‘matching’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’,
            # ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘wminkowski’, ‘yule’.

            # Calculating distance between question and notes. 0 is identical, 1 very different
            distances = scipy.spatial.distance.cdist([queries_embedding[0]], corpus_empeddings, "cosine")
            n = LIMIT_DS
            len_array = distances.shape[1]
            if len_array < LIMIT_DS:
                n = len_array
            logging.debug(" Distances: {0}".format(distances))
            idx_dist = distances.argsort()      # Array of index in ascending order
            # result = np.where(distances == np.amin(distances))  # Get index of minimum element
            # logging.debug(" Searching best distance: {0}".format(result))

            # Takes the index of the closest one an select the proper package
            # index = result[1][0]
            # if minimum distance is upper the threshold --> Take dataspaces sorted by visits
            similar_pck = []
            if distances[0][idx_dist[0][0]] < BERT_THRESHOLD:
                for i in range(n):
                    elem = selected_pcks[idx_dist[0][i]]
                    elem['distance'] = distances[0][idx_dist[0][i]]
                    similar_pck += [elem]       # Sort by distance
            else:
                for i in range(n):
                    elem = selected_pcks[i]
                    elem['distance'] = distances[0][i]
                    similar_pck += [elem]                 # Sort by visits


            logging.debug("Selected package: {0}".format(similar_pck))
            return similar_pck
        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

    @staticmethod
    def clean_stop_words(sentence, language, add_extra_stopwords=False):
        """Clean all stop words from a provided string

        Parameters
        ----------
        sentence: str
            Sentence to be cleaned

        language: str
            Question's language

        add_extra_stopwords: bool
            To delete generic words from questions

        Returns
        -------
        list

            Returns a list of words without stop words

        """
        try:
            stop_words = stopwords.words(language)
            if add_extra_stopwords:
                stop_words.extend(SPECIFIC_SW_AOD)

            # split into words
            word_tokens = word_tokenize(sentence)

            # remove punctuation from each word
            table = str.maketrans('', '', string.punctuation)
            word_stripped = [w.translate(table) for w in word_tokens]

            # important_words = filter(lambda x: x not in stopwords.words('spanish'), words)
            return [
                w
                for w in word_stripped
                if w.lower() not in stop_words and w.isalpha()
            ]

        except Exception as exc:
            logging.error(
                f'Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}'
            )

            raise exc

    def lemmatizer(self, sentence: str) -> list:
        """Lemmatize sentence's words

        Parameters
        ----------
        sentence: str
            Sentence to be lemmatized

        Returns
        -------
        list

            Returns a list of lemmatized words

        """
        try:
            sentence_lemma = self.nlp(sentence)

            return [token.lemma_ for token in sentence_lemma]
        except Exception as exc:
            logging.error(
                f'Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}'
            )

            return list(sentence.split(' '))
            #raise exc

    def select_best_packages(self, ds_list, question, bert_distance):
        """ Once all queries have been done, best packages are selected

        Parameters
        ----------
        ds_list: list
            Packages searched in CKAN

        question: string
            User's question

        bert_distance: bool
            Determine if bert_distance is used to select the most proper answer

        Returns
        -------
        list

            Returns the most suitable packages
        """

        logging.info("** select_best_packages **")
        logging.info(" * bert_distance: {0}".format(bert_distance))

        try:
            selected_package = []
            # Delete duplicates
            packages_df = pd.DataFrame(ds_list)
            # packages_df = packages_df.drop_duplicates()
            packages_df = packages_df.drop_duplicates(subset=['id'],
                                                      keep='first')
            packages_df = packages_df.sort_values(['updated', 'visits'], ascending=[False, False])
            ds_list = list(packages_df.T.to_dict().values())
            # Sorted dataframe
            if len(ds_list) > 1:  # If too much packages were found, select the most suitable
                logging.info("Too much packages found --> Select the most suitable")
                if bert_distance:
                    selected_package += self.get_best_package_bert_distance(question, ds_list)
                else:
                    # Select the LIMIT_DS from the packages
                    selected_package += ds_list[:LIMIT_DS]
                ds_list = selected_package
            elif len(ds_list) == 0:
                logging.info("Not packages found")
                return None  # Not packages found

            return ds_list

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

    @staticmethod
    def select_columns(ds_list, col_array):
        """ Extract specific columns from array of dictionaris

        Parameters
        ----------
        ds_list: list
            Packages searched in CKAN

        col_array: list
            List of columns

        Returns
        -------
        list

            Returns the the same list but with specified columns
        """

        logging.info("** select_columns **")
        logging.info(" * col_array: {0}".format(''.join(col_array)))

        try:
            ds_df = pd.DataFrame(ds_list)
            # Verify if columns exists
            selected_cols = [
                col_name for col_name in col_array if col_name in ds_df.columns
            ]

            if len(selected_cols):
                select_df = ds_df[col_array]
                return list(select_df.T.to_dict().values())
            else:
                logging.warning("These column names {0} are not on dataframe".format(''.join(col_array)))
                return None
        except Exception as exc:
            logging.error(
                f'Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}'
            )

            raise exc

    @staticmethod
    def create_opendata_url(ds_list):
        """ Add a new column to de selected packages with OpenData URLE

        Parameters
        ----------
        ds_list: list
            Packages searched in CKAN

        Returns
        -------
        list

            Returns the the same list but with a new column
        """

        logging.info("** create_opendata_url **")

        try:
            ds_df = pd.DataFrame(ds_list)

            ds_df[OPENDATA_URL_COLUMN] = URL_OPENDATA_BASE + ds_df["name"]
            return list(ds_df.T.to_dict().values())

        except Exception as exc:
            logging.error(
                f'Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}'
            )

            return None

    def question(self, question, entity_list, bert_distance=False):
        """Main function. Searches in Open Data the most suitable dataset to a specific question an its entities

        Parameters
        ----------
        question: string
            User's question

        entity_list: list
            List of entities inside the question

        bert_distance: bool
            Determine if bert_distance is used to select the most proper answer

        Returns
        -------
        list

            Returns the most suitable packages
        """
        logging.info("** question **")
        logging.info(" * question: {0}".format(question))
        logging.info(" * entity_list: {0}".format(entity_list))
        logging.info(" * bert_distance: {0}".format(bert_distance))

        try:
            entities = entity_list

            # Step 1. Extract all tags related to entities
            # Scroll through the list of entities by consulting the CKAN for the various labels.
            tag_list = self.get_tags(entities)

            selected_tag = ""
            if len(tag_list) == 1:
                # If only one tag is selected, It proceeds with packages selection
                selected_tag = tag_list[0]
            elif len(tag_list) > 1:
                # Step 2. If there are more than one tag, select the best one
                # No tags. Search between all tags
                # Calculating levensthein distance between an entity and the tag_list
                # if len(tag_list) == 0:
                #    tag_list = self.get_all_tags()
                level_distance = []
                for ent in entity_list:
                    nearest_tag, minimum_distance = self.get_minimum_levensthein_distance(ent['value'], tag_list)
                    if minimum_distance <= MAX_DIST:  # Adding to level_distance list when is down the limit
                        level_distance += [{'entity': ent['value'], 'tag': nearest_tag, 'distance': minimum_distance}]
                # Select the tag with minimum distance
                if len(level_distance):
                    # It selects the tag with the minimum distance
                    level_distance_sorted = sorted(level_distance, key=lambda k: k['distance'], reverse=True)
                    selected_tag = level_distance_sorted[0]['tag']

            # Step 3. If any tag has been found --> Search the most suitable packages to the question
            ds_list = []
            if not selected_tag.strip():
                logging.info("No tag found so search the most suitable package for the list of entities")
                # ds_list = self.get_packages_from_question(question)
                for entity in entity_list:
                    ent_value = entity["value"]
                    ds_list += self.get_packages_from_question(ent_value)
            else:
                logging.info("Search the associated packages to the selected tag")
                ds_list = self.get_packages(selected_tag)
                if len(ds_list) == 0:
                    logging.warning("No packages were found so look for the most suitable package for the question")
                    # ds_list = self.get_packages_from_question(question)
                    for entity in entity_list:
                        ent_value = entity["value"]
                        ds_list += self.get_packages_from_question(ent_value)

            selected_ds = None
            if len(ds_list):
                selected_ds = self.select_best_packages(ds_list, question, bert_distance)

            if selected_ds is not None:
                # Selecting only URL and title
                selected_ds = self.select_columns(selected_ds, ["name", "title", "url"])

            if selected_ds is not None:
                # Create Open Data URL for every selected package
                selected_ds = self.create_opendata_url(selected_ds)

            return selected_ds  # List only name, title, url and opendata_url

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

    def question_only_packages(self, question, entity_list, bert_distance=False):
        """Main function. Searches in Open Data the most suitable dataset
           from the provided user's question and the entity

        Parameters
        ----------
        question: string
            User's question

        entity_list: list
            List of entities inside the question

        bert_distance: bool
            Determine if bert_distance is used to select the most proper answer

        Returns
        -------
        list

            Returns the most suitable packages
        """
        logging.info("** question_only_packages **")
        logging.info(" * question: {0}".format(question))
        logging.info(" * bert_distance: {0}".format(bert_distance))

        try:

            ds_list = []
            # Search from the list of entities directly in the package
            for entity in entity_list:
                ent_value = entity["value"]
                ds_list += self.get_packages_from_question(ent_value)

            # If no packages are found, search by question
            # if len(ds_list) == 0:
            #     ds_list = self.get_packages_from_question(question)

            selected_ds = None
            if len(ds_list):
                selected_ds = self.select_best_packages(ds_list, question, bert_distance)

            if selected_ds is not None:
                # Selecting only URL and title
                selected_ds = self.select_columns(selected_ds, ["name", "title", "url"])

            if selected_ds is not None:
                # Create Open Data URL for every selected package
                selected_ds = self.create_opendata_url(selected_ds)

            return selected_ds  # List only name, title, url and opendata_url

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

    def question_by_package_complete(self, question, complete_question=True, bert_distance=False):
        """Main function Estrategy 1. Searches in Open Data the most suitable dataset
           from the provided user's question (eleminating stop word)

        Parameters
        ----------
        question: string
            User's question

        complete_question: bool
            Search by bert use the complete question or not

        bert_distance: bool
            Determine if bert_distance is used to select the most proper answer

        Returns
        -------
        list

            Returns the most suitable packages
        """
        logging.info("** question_by_package_complete. Estrategy 1 **")
        logging.info(" * question: {0}".format(question))
        logging.info(" * bert_distance: {0}".format(bert_distance))

        try:
            sentence_list = self.clean_stop_words(question, LANGUAGE)
            q = ' '.join(sentence_list)

            logging.info("Words in question {0}".format(q))

            ds_list = self.get_packages_from_question(q)

            selected_ds = None
            if len(ds_list):
                if complete_question:
                    selected_ds = self.select_best_packages(ds_list, question, bert_distance)
                else:
                    selected_ds = self.select_best_packages(ds_list, q, bert_distance)

            if selected_ds is not None:
                # Selecting only URL and title
                selected_ds = self.select_columns(selected_ds, ["name", "title", "url"])

            if selected_ds is not None:
                # Create Open Data URL for every selected package
                selected_ds = self.create_opendata_url(selected_ds)

            return selected_ds  # List only name, title, url and opendata_url

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

    def question_by_package_words(self, question, complete_question=True, bert_distance=False):
        """Main function Estrategy 2. Searches in Open Data the most suitable dataset
           from the separated words which take part user's question (eleminating stop word)

        Parameters
        ----------
        question: string
            User's question

        complete_question: bool
            Search by bert use the complete question or not

        bert_distance: bool
            Determine if bert_distance is used to select the most proper answer

        Returns
        -------
        list

            Returns the most suitable packages
        """
        logging.info("** question_by_package_words. Estrategy 2 **")
        logging.info(" * question: {0}".format(question))
        logging.info(" * bert_distance: {0}".format(bert_distance))

        try:
            sentence_list = self.clean_stop_words(question, LANGUAGE)
            q = ' '.join(sentence_list)

            logging.info("Words in question {0}".format(sentence_list))

            ds_list = []
            for word in sentence_list:
                ds_list += self.get_packages_from_question(word)

            selected_ds = None
            if len(ds_list):
                if complete_question:
                    selected_ds = self.select_best_packages(ds_list, question, bert_distance)
                else:
                    selected_ds = self.select_best_packages(ds_list, q, bert_distance)

            if selected_ds is not None:
                # Selecting only URL and title
                selected_ds = self.select_columns(selected_ds, ["name", "title", "url"])

            if selected_ds is not None:
                # Create Open Data URL for every selected package
                selected_ds = self.create_opendata_url(selected_ds)

            return selected_ds  # List only name, title, url and opendata_url

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc

    def question_by_tags(self, question, complete_question=True, bert_distance=False):
        """Main function Estrategy 3. Searches in Open Data the most suitable tags from words which take part in
        question and search packages related to this packages

        Parameters
        ----------
        question: string
            User's question

        complete_question: bool
            Search by bert use the complete question or not

        bert_distance: bool
            Determine if bert_distance is used to select the most proper answer

        Returns
        -------
        list

            Returns the most suitable packages
        """
        logging.info("** question_by_tags. Estrategy 3 **")
        logging.info(" * question: {0}".format(question))
        logging.info(" * bert_distance: {0}".format(bert_distance))

        try:
            clean_question = self.clean_stop_words(question, LANGUAGE, False)
            clean_q = ' '.join(clean_question)

            sentence_list = self.clean_stop_words(question, LANGUAGE, True)

            #Sentence lemmatizer
            sentence_lemma = self.lemmatizer(' '.join(sentence_list))

            #Join original list & lemmas
            complete_list = list(set(sentence_list) | set(sentence_lemma))

            # Review all list and delete accent
            plain_list = []
            for term in complete_list:
                plain_term = unidecode.unidecode(term)
                if term != plain_term:
                    plain_list += [term]
            if len(plain_list) > 0:
                complete_list += plain_list

            logging.info("Words in question {0}".format(complete_list))

            tag_list = self.get_tags(complete_list)
            aux_list = set(tag_list)
            tag_list = list(aux_list)

            ds_list = []
            if (tag_list is not None) and len(tag_list) > 0:
                for selected_tag in tag_list:
                    ds_list += self.get_packages(selected_tag)
            else:
                ds_list += self.get_packages_from_question(clean_q, False)

            selected_ds = None
            if len(ds_list):
                if complete_question:
                    selected_ds = self.select_best_packages(ds_list, question, bert_distance)
                else:
                    selected_ds = self.select_best_packages(ds_list, clean_q, bert_distance)

            # Remove duplicates - No funciona
            # aux_ds = [dict(t) for t in {tuple(d.items()) for d in selected_ds}]
            # selected_ds = aux_ds

            if selected_ds is not None:
                # Selecting only URL and title
                selected_ds = self.select_columns(selected_ds, ["name", "title", "url", "resources", "organization",
                                                                "updated", "distance", "visits", "tags", "extras"])

            if selected_ds is not None:
                # Create Open Data URL for every selected package
                selected_ds = self.create_opendata_url(selected_ds)

            return selected_ds  # List only name, title, url and opendata_url

        except Exception as exc:
            #logging.error("Unexpected error:", sys.exc_info()[0])
            logging.error(f"Error type: {type(exc)}; Error args: {exc.args}; Error Message;{exc}")
            raise exc
