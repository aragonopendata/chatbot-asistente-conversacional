import os
import json
import tensorflow as tf
from abc import ABC, abstractmethod


class Model(ABC):
    """ Base model
        Defines generic functions used for all type of models
        Defines methods to be implemented for each model.

        Code based in original implementation from:
        https://github.com/guillaumegenthial/sequence_tagging/blob/master/model/base_model.py
    """
    def __init__(self, config):
        """ Init model """
        self.config = config
        self.logger = config.logger
        self.sess   = None
        self.optimizer = None
        self.saver  = None
        self.sumaries = None
        self.file_writer = None

    @abstractmethod
    def build(self):
        pass

    def set_optimizer(self, method, lr):
        self.logger.info("Setting optimization algorithm: " + method)
        method = method.lower()

        with tf.variable_scope("train_step"):
            if method == 'adam': # sgd method
                self.optimizer = tf.train.AdamOptimizer(lr)
            elif method == 'adagrad':
                self.optimizer = tf.train.AdagradOptimizer(lr)
            elif method == 'sgd':
                self.optimizer = tf.train.GradientDescentOptimizer(lr)
            elif method == 'rmsprop':
                self.optimizer = tf.train.RMSPropOptimizer(lr)
            else:
                raise NotImplementedError("Unknown method {}".format(method))

    def train(self, train, dev):
        """ Performs training with (hand-crafted) early stopping and lr exponential decay
        It evaluates performance each epoch
        """
        best_score = 0
        nepoch_no_imprv = 0  # for early stopping
        self.add_summary()  # for tensorboard

        for epoch in range(self.config.nepochs):
            self.logger.info("Epoch {:} out of {:}".format(epoch + 1, self.config.nepochs))

            score = self.run_epoch(train, dev, epoch)  #ToDo score -> metrics{acc, f1...}
            self.config.lr *= self.config.lr_decay  # decay learning rate

            # early stopping and saving best parameters
            if score >= best_score:
                nepoch_no_imprv = 0
                self.save_session()
                best_score = score
                self.logger.info("New best score!")
            else:
                nepoch_no_imprv += 1
                if nepoch_no_imprv >= self.config.nepoch_no_imprv:
                    self.logger.info("EARLY STOPPING: {} epochs without improvement".format(nepoch_no_imprv))
                    #self.logger.info("BEST SCORE (f1) GOT: {} ".format(best_score))
                    break

        self.logger.info("BEST SCORE (f1) GOT: {} ".format(best_score))

    @abstractmethod
    def run_epoch(self):
        pass

    def evaluate(self, test):
        """ Evaluates model over the test dataset and displays metrics """
        self.logger.info("Testing model over test set")
        metrics = self.run_evaluate(test)
        #msg = " - ".join(["{} {:04.2f}".format(k, v) for k, v in metrics.items()])
        self.logger.info("Metrics:\n" + str(metrics))

    @abstractmethod
    def run_evaluate(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    def initialize_session(self):
        """ Creates tf session and initializes variables """
        self.logger.info("Initializing tf session")
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()


    def save_session(self):
        """ Saves session = variables -> weights """
        if not os.path.exists(self.config.dir_model):
            os.makedirs(self.config.dir_model)
        self.saver.save(self.sess, self.config.dir_model)

    def restore_session(self, dir_model):
        """ Reload weights into session from checkpoint files """
        self.logger.info("Reloading the latest trained model...")
        self.saver.restore(self.sess, dir_model)

    def add_summary(self):
        """ Used for Tensorboard.
            It needs a TF graph to collect summary data from.
            See: https://www.tensorflow.org/tensorboard/r1/summaries
        """
        self.sumaries      = tf.summary.merge_all()
        self.file_writer = tf.summary.FileWriter(self.config.dir_output, self.sess.graph)

    def save_tags(self, tags):
        json.dump(tags, open(self.config.filename_tags, 'w'))

    def restore_tags(self):
        return json.load(open(self.config.filename_tags, 'r'))