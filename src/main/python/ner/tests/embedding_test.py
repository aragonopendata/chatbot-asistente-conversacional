"""
    Use of word embeddings without need to build 'fixed' vocabulary previously
    Script based on NB from: https://github.com/monk1337/word_embedding-in-tensorflow/blob/master/Use%20Pre-trained%20word_embedding%20in%20Tensorflow.ipynb

    '''
    Check also:
        - https://stackoverflow.com/questions/45113130/how-to-add-new-embeddings-for-unknown-words-in-tensorflow-training-pre-set-fo
        - https://stackoverflow.com/questions/49239941/what-is-unk-in-the-pretrained-glove_wiki-vector-files-e-g-glove_wiki-6b-50d-txt
        - https://stats.stackexchange.com/questions/202544/handling-unknown-words-in-language-modeling-tasks-using-lstm
    '''
"""

import os
import numpy as np
from data.data_utils import pad_sequences

embed_txt_file = "/../resources/glove_wiki/vectors.txt"

original_embedding_dim = 500
embedding_dim = 300


def main():
    texts = ['hola caracola',
                 'esto es una prueba sencilla',
                 'no sé qué más añadir a esta frase tan larga']

    # Load embeddings
    glove_vocab = []
    embedding_matrix = []
    #vocab_len = sum(1 for line in open('glove_wiki/vocab.txt', encoding="utf8"))
    with open(os.path.dirname(__file__) + embed_txt_file, 'r',  encoding="utf8") as f:
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

        embedding_matrix.append(np.random.uniform(-1.0, 1.0, (1, embedding_dim))[0]) # UNK
        glove_vocab.append('UNK')
        #word_to_idx['UNK'] =  len(glove_vocab)
        #idx_to_word[len(glove_vocab)] = 'UNK'

        # w2i & i2w
        word_to_idx = {word:idx for idx, word in enumerate(glove_vocab)}
        idx_to_word = {idx:word for idx, word in enumerate(glove_vocab)}

        # Convert embedding matrix to array
        #embedding_matrix1 = np.array(embedding_matrix)
        embedding_matrix3 = np.reshape(embedding_matrix, [-1, embedding_dim]).astype(np.float32) # vocab_size x embedding_dim

    # Encode sentence into ids to further get embedded
    enc_data = []
    for sentence in texts:
        enc_sent = []
        for word in sentence.split(): #Whitespace sep
            if word in glove_vocab:
                enc_sent.append(word_to_idx[word])
            else:
               enc_sent.append(word_to_idx['UNK'])
        enc_data.append(enc_sent)

    # Padding
    enc_data, sequence_lengths = pad_sequences(enc_data, 0)


    # Use it in TF
    import tensorflow  as tf
    tf.reset_default_graph()

    sentences = tf.placeholder(tf.int32, shape=[None, None])

    _word_embeddings = tf.Variable(
            embedding_matrix3,
            dtype=tf.float32,
            trainable=False)

    word_embeddings = tf.nn.embedding_lookup(_word_embeddings, sentences)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for embedding_vector in enc_data:
            print(sess.run(word_embeddings, feed_dict={sentences: [embedding_vector]}))


if __name__ == "__main__":
    main()
