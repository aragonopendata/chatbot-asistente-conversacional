import csv
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
        niter = 0
        with open(self.filename, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            for row in csv_reader:
                words, tags = [], []
                if niter == 0:
                    #print("CSV Header: ", row)
                    niter += 1
                else:
                    sentence, tag = row[0], row[1]
                    tokens = sentence.strip().split(' ')  #Tokenization
                    for token in tokens:
                        if self.processing_word is not None:  #OJO! Podemos tener tokens vacíos = ''
                            word = self.processing_word(token)
                        else:
                            word = token

                        if word in self.word2idx:
                            #words += [self.word2idx[word]]
                            word_id = self.word2idx[word]
                        elif self.use_unk:
                            # words += [self.word2idx['UNK']]
                            word_id = self.word2idx[UNK]
                        else:
                            word_id = 0

                        #Process chars
                        if self.char2idx is not None:
                            char_ids = []
                            for char in word:
                                if char in self.char2idx:  # ignore chars out of vocabulary
                                    char_ids += [self.char2idx[char]]
                            words += [(char_ids, word_id)]
                        else:
                            words += [word_id]

                    # Get tag idx
                    tag = self.process_tag(tag)
                    tags += [tag]

                    niter += 1
                    yield words, tags
                    #words, tag = [], []

    def __len__(self):
        """Iterates once over the corpus to set and store length"""
        if self.length is None:
            with open(self.filename, encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
                self.length = sum(1 for _ in csv_reader)

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