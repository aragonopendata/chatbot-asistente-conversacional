from data.data_utils import Dataset

from configuration.config_json import UNK


class CoNLLDataset(Dataset):
    """Class that iterates over CoNLL Dataset: (word, label)
       End of sentence (group of words) is found when analyzed file's line is empty.

       __iter__ method yields a tuple (words, tags) for each sentence/doc
           words: list of raw words
           tags: list of raw tags

       If processing_word and processing_tag are not None,
       optional preprocessing is appplied (usually set in Config class) and defined in data_utils.py

       Example:
           ```python
           data = CoNLLDataset(filename)
           for sentence, tags in data:
               pass
           ```
       """

    def __iter__(self):
        niter = 0
        num_lines = 0
        with open(self.filename, encoding="utf8") as f:
            words, tags = [], []
            for line in f:  #Itera por líneas del fichero
                num_lines += 1
                line = line.strip()
                if len(line) == 0 or line.startswith("-DOCSTART-") or line.isspace():  #Final o inicio de sentencia/documento
                    if len(words) != 0:
                        niter += 1
                        if self.max_iter is not None and niter > self.max_iter:
                            break
                        yield words, tags
                        words, tags = [], []
                else:
                    #print("Line {}".format(num_lines))
                    ls = line.split(' ')
                    word, tag = ls[0],ls[1]
                    if self.processing_word is not None:
                        word = self.processing_word(word)
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
                        words += [(char_ids, word_id)]
                    else:
                        words += [word_id]

                    # Get tag idx
                    if self.processing_tag is not None:
                        tag = self.processing_tag(tag)
                    else:
                        tag = self.process_tag(tag)

                    #words += [word_id]
                    tags += [tag]
            else: # EOF
                #print("Hit EOF!")
                if len(words) != 0:  # Hay palabras/tags pendientes
                    niter += 1
                    yield words, tags
                    #words, tags = [], []

    def __len__(self):
        """Iterates once over the corpus to set and store length"""
        if self.length is None:
            self.length = 0
            for _ in self:
                self.length += 1

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