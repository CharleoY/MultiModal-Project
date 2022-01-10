import sys
sys.path.insert(0, '../source')
import tensorflow as tf
from tensorflow.contrib import rnn
import get_data
import logging
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score


class LSTM_model:
    def __init__(self, learning_rate, n_hidden, n_input, input_dimension,
                 output_dimension, display_step=1000, multi_layer=False):
        # technical detailes
        self.logger = get_data.init_logging('%d_%d' % (n_hidden, n_input))
        self.MBTI_labels = ['E_I', 'S_N', 'T_F', 'J_P']
        self.n_hidden = n_hidden
        self.learning_rate = learning_rate

        self.training_iters = None
        self.display_step = display_step
        self.input_dimension = input_dimension  # number of features
        self.output_dimension = output_dimension  # number of labels

        self.n_input = n_input  # number of time periods
        self.batch_size = None
        self.multi_layer = multi_layer

        self.x = tf.placeholder(tf.float32, [None, self.n_input, self.input_dimension], name='x')
        self.y = tf.placeholder(tf.float32, [None, self.output_dimension], name='y')

        # RNN output node weights and biases
        self.weights = {
            'out': tf.Variable(tf.random_normal([self.n_hidden, self.output_dimension]), name='weigths')
        }
        self.biases = {
            'out': tf.Variable(tf.random_normal([self.output_dimension]), name='biases')
        }
        self.pred, self.cost, self.optimizer, self.accuracy = self.set_optimizers()

    def update_params(self, batch_size, label):
        self.batch_size = batch_size
        self.label = label

    def RNN(self):
        if not self.multi_layer:
            rnn_cell = rnn.LSTMCell(self.n_hidden)
        else:
            rnn_cell_f = rnn.BasicLSTMCell(self.n_hidden)
            rnn_cell_s = rnn.BasicLSTMCell(self.n_hidden)
            rnn_cell = rnn.MultiRNNCell([rnn_cell_f, rnn_cell_s])
        rnn_cell = rnn.DropoutWrapper(rnn_cell, 0.8)
        x = tf.unstack(self.x, self.n_input, 1)
        outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)
        # there are n_input outputs but
        # we only want the last output
        return tf.matmul(outputs[-1], self.weights['out']) + self.biases['out']

    def set_optimizers(self):
        pred = self.RNN()
        # Loss and optimizer
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=self.y))
        optimizer = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate).minimize(cost)
        # Model evaluation
        correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(pred, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return pred, cost, optimizer, accuracy

    def train_one_label(self, train_input, train_output, batch_size, test_input, test_output):
        self.logger.info('Train model with: learning_rate=%s\n'
                         'n_hidden=%d\n'
                         'time_periods=%d\n'
                         'batch_size=%d\n'
                         'is_multi_layer=%s\n'
                         'label=%s' % (str(self.learning_rate), self.n_hidden, self.n_input,
                                       self.batch_size, str(self.multi_layer), self.MBTI_labels[self.label]))

        init = tf.global_variables_initializer()
        with tf.Session() as session:
            saver = tf.train.Saver()
            session.run(init)
            epoch = 0
            offset = 0
            epochs = 1

            while epoch < epochs:
                input_batch, output_batch = get_data.get_batch(train_input, train_output, batch_size, offset)
                session.run([self.optimizer], \
                                feed_dict={self.x: input_batch, self.y: output_batch})
                offset += batch_size + 1
                if offset >= len(train_output) - 1:
                    # Calculate batch accuracy
                    acc, pred = session.run([self.accuracy, self.pred], feed_dict={self.x: test_input, self.y: test_output})
                    # Calculate batch loss
                    loss = session.run(self.cost, feed_dict={self.x: input_batch, self.y: output_batch})
                    y_true = tf.argmax(test_output, 1).eval()
                    y_pred = tf.argmax(pred, 1).eval()
                    self.logger.info("Epoch= " + str(epoch + 1) + ", Average Loss= " + \
                                         "{:.6f}".format(loss) + ", Average Accuracy= " + \
                                         "{:.2f}".format(100 * acc))
                    self.logger.info("Label " + get_data.get_label_letter(self.label, 0) + ", Precision= " + \
                                     "{:.3f}".format(precision_score(y_true, y_pred, pos_label=0)) + ", Recall= " + \
                                     "{:.3f}".format(recall_score(y_true, y_pred, pos_label=0)) + ", F-measure= " + \
                                     "{:.3f}".format(f1_score(y_true, y_pred, pos_label=0)))
                    self.logger.info("Label " + get_data.get_label_letter(self.label, 1) + ", Precision= " + \
                                     "{:.3f}".format(precision_score(y_true, y_pred, pos_label=1)) + ", Recall= " + \
                                     "{:.3f}".format(recall_score(y_true, y_pred, pos_label=1)) + ", F-measure= " + \
                                     "{:.3f}".format(f1_score(y_true, y_pred, pos_label=1)))
                    epoch += 1
                    offset = 0

            save_path = saver.save(session, "../models/%d_%d_%d" %
                                   (self.n_hidden, self.n_input, self.label))
            print("Model saved in file: %s" % save_path)
            session.close()
            return y_pred


