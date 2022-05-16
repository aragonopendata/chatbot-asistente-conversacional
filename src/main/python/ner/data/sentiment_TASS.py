#import csv
import xml.etree.ElementTree as ET

from data.data_utils import Dataset
from configuration.config_json import UNK


class SentimentDataset(Dataset):
    """Class that iterates over Sentiment Dataset: <sentence, label>

    __iter__ method yields a tuple (words, tags) for each sentence/doc
        words: list of raw words
        tags: list of raw tags

    If processing_word and processing_tag are not None,
    optional preprocessing is appplied (usually set in Config class) and defined in data_utils.py

    Example:
        ```python
        data = SentimentDataset(filename)
        for sentence, tags in data:
            pass
        ```
    """

    def __iter__(self):
        tweets = ET.parse(self.filename)
        for tweet in tweets.findall('/tweet'):
            words, tags = [], []
            content = tweet.find('content')
            tweetid = tweet.find('tweetid')
            sentiment = tweet.find('sentiment').find('polarity').find('value')
            #print("Content = {0} --> Tag = {1}".format(content.text, sentiment.text))

            sentence = content.text
            tag = sentiment.text
            tokens = sentence.strip().split(' ')  # Tokenization
            for token in tokens:
                if self.processing_word is not None:  # OJO! Podemos tener tokens vacíos = ''
                    word = self.processing_word(token)
                else:
                    word = token

                if word in self.word2idx:
                    # words += [self.word2idx[word]]
                    word_id = self.word2idx[word]
                elif self.use_unk:
                    # words += [self.word2idx['UNK']]
                    word_id = self.word2idx[UNK]
                else:
                    word_id = 0

                # Process chars
                if self.char2idx is not None:
                    char_ids = []
                    for char in word:
                        if char in self.char2idx:  # ignore chars out of vocabulary
                            char_ids += [self.char2idx[char]]
                        else:
                            char_ids += [len(self.char2idx)+1]
                    words += [(char_ids, word_id)]
                else:
                    words += [word_id]

            # Get tag idx
            tag = self.process_tag(tag)
            tags += [tag]

            yield words, tags

    def __len__(self):
        """Iterates once over the corpus to set and store length"""
        if self.length is None:
            tweets = ET.parse(self.filename)
            self.length = sum(1 for _ in tweets.findall('./tweet'))

        return self.length

    def process_tag(self, tag):
        """Process tag (if needed) and gets tag index

        :param tag: str
        :return: Tag idx
        """
        if tag not in self.tag2idx.keys():
            self.tag2idx[tag] = len(self.tag2idx)
        return self.tag2idx[tag]

    def set_tagset(self, tagset):
        self.tag2idx = tagset

    def get_tagset(self):
        return self.tag2idx