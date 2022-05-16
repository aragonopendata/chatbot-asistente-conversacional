import os
import logging
from enum import Enum
import numpy as np
import json
from gensim.models.keyedvectors import KeyedVectors

class TASKS(Enum):
    NER = 1
    SA = 2


UNK = '<unk>'


class Config():
    def __init__(self, config_path, load=True):
        self.path = config_path

        if os.path.exists(self.path):
            self.initialize()
        else:
            raise FileNotFoundError

        # directory for training outputs
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)

        # create instance of logger
        self.logger = get_logger(self.path_log)

        # load if requested (default)
        if load:
            self.load()

    def initialize(self):
        with open(self.path, 'r') as f:
            config = json.load(f)
            #General config
            self.dir_output = config['dir_output']
            self.model_name = config['model_name']
            self.dir_model = self.dir_output + self.model_name
            self.path_log = self.dir_output + "log.txt"

            # Embeddings
            self.dim_word = config['dim_word']  # Dim pretrained word embeddings
            self.dim_char = config['dim_char']  # Dim word embeddings

            ## Word embeddings
            self.use_pretrained = True  # False is not implemented
            self.type_pretrained = config['type_pretrained']
            self.filename_glove = config['filename_glove']
            if self.type_pretrained == 'binary':
                self.bin = config['bin']
            if 'use_unk' in config:
                self.use_unk = config['use_unk']
            else:
                self.use_unk = False # Assumming our model has no built-in UNK
            print('Use UNK = {}'.format(self.use_unk))

            ## Char embeddings
            self.use_chars = config['use_chars']  # if char embedding, training is 3.5x slower on CPU
            if self.use_chars == True:
                self.filename_chars = config['filename_chars']

            # Dataset
            directory = config['dir_dataset']
            if  'filename_train' in config:
                self.filename_train = directory + config['filename_train']
            if 'filename_dev' in config:
                self.filename_dev = directory + config['filename_dev']
            if 'filename_test' in config:
                self.filename_test = directory + config['filename_test']

            self.delimiter = config['delimiter']
            self.max_iter = None  # if not None,500 max number of examples in Dataset

            self.filename_tags = config['filename_tags']
            self.ntags = config['ntags']

            # Training parameters
            self.train_embeddings = config['train_embeddings']  # Wordembeddings
            self.nepochs = config['nepochs']
            self.dropout = config['dropout']
            self.batch_size = config['batch_size']
            self.opt_method = config['opt_method']
            self.lr = config['lr']
            self.lr_decay = config['lr_decay']
            # clip             = -1 # if negative, no clipping
            if 'clip' in config:
                self.clip = config['clip']
            else:
                self.clip = -1

            self.nepoch_no_imprv = config['nepoch_no_imprv']

            # Model hyperparameters
            self.layers = config['layers']
            self.hidden_size_char = config['hidden_size_char'] # lstm on chars
            if self.layers == 1:
                self.hidden_size_lstm = config['hidden_size_lstm']  # lstm on word embeddings
            elif self.layers == 2:
                self.hidden_size_lstm = config['hidden_size_lstm']
                self.hidden_size_lstm2 = config['hidden_size_lstm2']  # lstm 2nd layer
            elif self.layers > 2:
                self.hidden_sizes = config['hidden_sizes']

            if 'output_file' in config:
                self.output_file = config['output_file']

            if 'use_crf' in config:
                self.use_crf = config['use_crf']
            #flask port
            if 'port' in config:
                self.port = config['port']
            if 'dictionaries' in config:
                self.dictionaries = config['dictionaries']



    def load(self):
        """Loads word embeddings and char vocabulary
        """
        if self.use_pretrained:
            if self.type_pretrained == "text":
                self.embeddings, self.word2idx = get_text_embeddings(self.filename_glove, self.dim_word, self.dim_word)
            elif self.type_pretrained == "binary":
                self.embeddings, self.word2idx = get_bin_embeddings(self.filename_glove, self.bin, self.dim_word, self.use_unk)
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

        # Sets char default vocabulary
        if self.use_chars:
            self.char2idx = get_vocabulary_char(self.filename_chars)
            self.nchars = len(self.char2idx)


def get_logger(filename):
    """Return a logger instance that writes in filename

    Args:
        filename: (string) path to log.txt

    Returns:
        logger: (instance of logger)
    """
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)

    return logger


def get_vocabulary_char(path):
    """Loads char vocabulary from a file

    :param path: file path
    :return: dictionary:{char:idx}
    """
    try:
        d = {}
        with open(path, 'r', encoding="utf8") as f:
            for idx, char in enumerate(f):
                char = char.strip('\n')
                d[char] = idx
    except IOError:
        print(IOError)
        exit(IOError)
    return d


def get_text_embeddings(path, original_embedding_dim, embedding_dim, append_unk=False):
    """ Load embeddings

    :param path: file path
    :param embedding_dim:
    :return: Embeddings matrix, Word2Idx
    """
    if os.path.isfile(os.path.splitext(path)[0]+".matrix.npy"):
        matrix = np.load(os.path.splitext(path)[0]+".matrix.npy")
        with open(os.path.splitext(path)[0]+".w2i", 'r') as f:
                word_to_idx = json.load(f)
    else:
        glove_vocab = []
        embedding_matrix = []
        #vocab_len = sum(1 for line in open('glove_wiki/vocab.txt', encoding="utf8"))
        with open(path, 'r',  encoding="utf8") as f:
            for idx, line in enumerate(f):
                try:
                    line = line.strip().split()
                    word = line[0]
                    vector = [float(x) for x in line[1:]]  #gets embedding for the given word (vector is a list of floats)

                    if len(vector) < original_embedding_dim:
                        print("Something very weird happen at index " + str(idx))
                        continue

                    if word not in glove_vocab:
                        embedding_matrix.append(vector[0:embedding_dim])
                        glove_vocab.append(word)

                    '''
                    try:
                        word_to_idx[word]
                        print("Word " + word + " has already been saved before at " + str(word_to_idx[word]))
                    except KeyError:
                        word_to_idx[word] = idx
                    '''
                except Exception as e:
                    print("Something very weird happen at index " + str(idx))
                    print(str(e))
                    continue

            if append_unk:
                embedding_matrix.append(np.random.uniform(-1.0, 1.0, (1, embedding_dim))[0]) # UNK
                glove_vocab.append(UNK)

            # w2i & i2w
            word_to_idx = {word:idx for idx, word in enumerate(glove_vocab)}
    #        idx_to_word = {idx:word for idx, word in enumerate(glove_vocab)}

            # Convert embedding matrix to array
            matrix = np.reshape(embedding_matrix, [-1, embedding_dim]).astype(np.float32) # vocab_size x embedding_dim

            np.save(os.path.splitext(path)[0]+".matrix", matrix)
            with open(os.path.splitext(path)[0]+".w2i", 'w') as file:
                file.write(json.dumps(word_to_idx))

    return matrix, word_to_idx

def get_bin_embeddings(embed_bin_file, binary=True, embedding_dim=300, append_unk=True):
    # Load embeddings
    model = KeyedVectors.load_word2vec_format(embed_bin_file, binary=binary)
    w2v_vocab = model.vocab
    matrix = model.vectors

    if append_unk:
        # embedding_matrix.append(np.random.uniform(-1.0, 1.0, (1, embedding_dim))[0])  # UNK
        unk_init = np.random.uniform(-1.0, 1.0, (1, embedding_dim))[0]
        np.vstack([matrix, unk_init])
        w2v_vocab['<unk>'] = len(w2v_vocab) + 1

    # w2i & i2w
    word_to_idx = {word: idx for idx, word in enumerate(w2v_vocab)}
    return matrix, word_to_idx
