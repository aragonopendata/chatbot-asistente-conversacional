import json
import os
from abc import ABC, abstractmethod
import re


# shared global variables
UNK = "$UNK$"
NUM = "$NUM$"
NONE = "O"

DIGITS = "DIGITO"
URLS = "<URL>"
MENTIONS = "<USER>"
HASHTAGS = "<HASHTAG>"
OTHER = "<OTHER>"

# special error message
class MyIOError(Exception):
    def __init__(self, filename):
        # custom error message
        message = """
ERROR: Unable to locate file {}.

FIX: Have you tried running python build_vocabulary.py first?
This will build vocab file from your train, test and dev sets and
trimm your word vectors.
""".format(filename)
        super(MyIOError, self).__init__(message)

######################################################################################################################
class Dataset(ABC):
    #@abstractmethod
    def __init__(self, filename, delimiter=None,
                 processing_line=None,
                 processing_word=None,
                 processing_tag=None,
                 processing_char=None,
                 word2idx=None,
                 char2idx = None,
                 max_iter=None,
                 use_unk=True):
        """ Dataset constructor
        Args:
            filename: path to the file
            delimiter: (optional) file delimiter character if nedeed
            processing_words: (optional) function that takes a word as input
            processing_tags: (optional) function that takes a tag as input
            processing_char: (optional) function that takes a char as input
            max_iter: (optional) max number of sentences to yield
            is_train: (optional) if training set, it will load and save tagset
        """
        self.filename = filename
        self.delimiter = delimiter
        self.processing_line = processing_line
        self.processing_word = processing_word
        self.processing_tag = processing_tag
        self.processing_char = processing_char
        self.word2idx = word2idx
        self.char2idx = char2idx
        self.max_iter = max_iter
        self.use_unk = use_unk

        self.tag2idx = {}
        self.length = None

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

'''
def get_processing_word(vocab_words=None, vocab_chars=None,
                    lowercase=False, chars=False, allow_unk=True):
    """Return lambda function that transform a word (string) into list,
    or tuple of (list, id) of int corresponding to the ids of the word and
    its corresponding characters.

    Args:
        vocab: dict[word] = idx

    Returns:
        f("cat") = ([12, 4, 32], 12345)
                 = (list of char ids, word id)

    """
    def f(word):
        # 0. get chars of words
        if vocab_chars is not None and chars == True:
            char_ids = []
            for char in word:
                # ignore chars out of vocabulary
                if char in vocab_chars:
                    char_ids += [vocab_chars[char]]

        # 1. preprocess word
        if lowercase:
            word = word.lower()
        if word.isdigit():
            word = NUM

        # 2. get id of word
        if vocab_words is not None:
            if word in vocab_words:
                word = vocab_words[word]
            else:
                if allow_unk:
                    word = vocab_words[UNK]
                else:
                    raise Exception("Unknow key is not allowed. Check that "\
                                    "your vocab (tags?) is correct")

        # 3. return tuple char ids, word id
        if vocab_chars is not None and chars == True:
            return char_ids, word
        else:
            return word

    return f
'''
def preprocess_word(lowercase=False):
    """
     (Replacement for the get_preprocessing_word())
     Preprocess each token in as desired, returns cleaned word
     :return: f(word)
     """

    def f(word):
        if lowercase:
            word = word.lower()
        if word.isdigit():
            word = NUM

        return word

    return f


def process_line():
    """
    Line processing specially designed for Tweets and SocialMedia texts
    :return:
    """
    def f(line):
        # Replace number with a tag
        line = re.sub('(\d+)', DIGITS, line)

        # Multiple whitespaces
        line = re.sub(' +', ' ', line)

        # Replace links with a tag
        line = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', URLS, line)
        # Emails
        line = re.sub(r'[\w\.-]+@[\w\.-]+', OTHER, line)

        # Replace user mentions
        line = re.sub(r'@\w+', MENTIONS, line)

        # Replace hashtags
        line = re.sub(r'#\w+', HASHTAGS, line)

        # Special case (old tweets): '…'
        line = re.sub(r'…', '', line)

        return line
    return f
######################################################################################################################

def _pad_sequences(sequences, pad_tok, max_length):
    """
    Args:
        sequences: a generator of list or tuple
        pad_tok: the char to pad with

    Returns:
        a list of list where each sublist has same length
        sequence_padded -> Lista de secuencias(sentencias/palabras) paddeadas
        sequence_length -> Lista de longitudes originales de las secuencias
    """
    sequence_padded, sequence_length = [], []

    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:max_length] + [pad_tok]*max(max_length - len(seq), 0) #PADDING!!!
        sequence_padded +=  [seq_]
        sequence_length += [min(len(seq), max_length)]

    return sequence_padded, sequence_length


def pad_sequences(sequences, pad_tok, nlevels=1):
    """
    Args:
        sequences: a generator of list or tuple
        pad_tok: the char to pad with
        nlevels: "depth" of padding, for the case where we have characters ids

    Returns:
        a list of list where each sublist has same length
    """
    if nlevels == 1:
        max_length = max(map(lambda x : len(x), sequences))
        sequence_padded, sequence_length = _pad_sequences(sequences,
                                            pad_tok, max_length)

    elif nlevels == 2:
        max_length_word = max([max(map(lambda x: len(x), seq))
                               for seq in sequences])
        sequence_padded, sequence_length = [], []
        for seq in sequences:
            # all words are same length now
            sp, sl = _pad_sequences(seq, pad_tok, max_length_word)
            sequence_padded += [sp]
            sequence_length += [sl]

        max_length_sentence = max(map(lambda x : len(x), sequences))
        sequence_padded, _ = _pad_sequences(sequence_padded,
                [pad_tok]*max_length_word, max_length_sentence)
        sequence_length, _ = _pad_sequences(sequence_length, 0,
                max_length_sentence)

    return sequence_padded, sequence_length


def minibatches(data, minibatch_size):
    """
    Args:
        data: generator of (sentence, tags) tuples
        minibatch_size: (int)

    Yields:
        list of tuples
    """
    x_batch, y_batch = [], []
    for (x, y) in data: #x->words of a sentence([chars idx], word_idx), y->tags of the sentence(idx)
        if len(x_batch) == minibatch_size:
            yield x_batch, y_batch
            x_batch, y_batch = [], []

        if type(x[0]) == tuple:
            x = zip(*x)  #
        x_batch += [x]
        y_batch += [y]

    if len(x_batch) != 0:
        yield x_batch, y_batch


def get_chunk_type(tok, idx_to_tag):
    """
    Args:
        tok: id of token, ex 4
        idx_to_tag: dictionary {4: "B-PER", ...}

    Returns:
        tuple: "B", "PER"
    """
    tag_name = idx_to_tag[tok]
    tag_class = tag_name.split('-')[0]
    tag_type = tag_name.split('-')[-1]
    return tag_class, tag_type


def get_chunks(seq, tags):
    """Given a sequence of tags, group entities and their position

    Args:
        seq: [4, 4, 0, 0, ...] sequence of labels
        tags: dict["O"] = 4

    Returns:
        list of (chunk_type, chunk_start, chunk_end)

    Example:
        seq = [4, 5, 0, 3]
        tags = {"B-PER": 4, "I-PER": 5, "B-LOC": 3}
        result = [("PER", 0, 2), ("LOC", 3, 4)]
    """
    default = tags[NONE]
    idx_to_tag = {idx: tag for tag, idx in tags.items()}
    chunks = []
    chunk_type, chunk_start = None, None
    for i, tok in enumerate(seq):
        # End of a chunk 1
        if tok == default and chunk_type is not None:
            # Add a chunk.
            chunk = (chunk_type, chunk_start, i)
            chunks.append(chunk)
            chunk_type, chunk_start = None, None

        # End of a chunk + start of a chunk!
        elif tok != default:
            tok_chunk_class, tok_chunk_type = get_chunk_type(tok, idx_to_tag)
            if chunk_type is None:
                chunk_type, chunk_start = tok_chunk_type, i
            elif tok_chunk_type != chunk_type or tok_chunk_class == "B":
                chunk = (chunk_type, chunk_start, i)
                chunks.append(chunk)
                chunk_type, chunk_start = tok_chunk_type, i
        else:
            pass

    # end condition
    if chunk_type is not None:
        chunk = (chunk_type, chunk_start, len(seq))
        chunks.append(chunk)

    return chunks
