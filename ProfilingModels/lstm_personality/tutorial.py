import sys
sys.path.insert(0, '../source')
import tensorflow as tf
from tensorflow.contrib import rnn
import get_data
import logging

# Features dimensions
TEXT_DIM = 53
LIWC_DIM = 64
LDA_DIM = 50
LOCATION_DIM = 886
MEDIA_DIM = 1000

# MBTI labels
I_E = 0
S_N = 1
T_F = 2
J_P = 3


# Parameters
learning_rate = 0.001
training_iters = 10000
display_step = 1000
input_dimension = TEXT_DIM + LIWC_DIM + LDA_DIM + LOCATION_DIM + MEDIA_DIM  # number of features
output_dimension = 2  # number of labels
n_hidden = 256
n_input = 2  # number of time periods
batch_size = 15

# logging.info('Run LSTM with {%d} training_iters, \n{%d} output_dimension, \n{%d} n_hidden layers, \n{%d} periods, \n{%d} batch_size' %
#              (training_iters, output_dimension, n_hidden, n_input, batch_size))

x = tf.placeholder(tf.float32, [None, n_input, input_dimension])
y = tf.placeholder(tf.float32, [None, output_dimension])


# RNN output node weights and biases
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, output_dimension]))
}
biases = {
    'out': tf.Variable(tf.random_normal([output_dimension]))
}


def RNN(x, weights, biases, multi_layer = False):
    rnn_cell = rnn.BasicLSTMCell(n_hidden)
    if multi_layer:
        rnn_cell = rnn.MultiRNNCell([rnn_cell] * 2)
    rnn_cell = rnn.DropoutWrapper(rnn_cell, 0.8)
    x = tf.unstack(x, n_input, 1)
    outputs, states = rnn.static_rnn(rnn_cell, x, dtype=tf.float32)
    # there are n_input outputs but
    # we only want the last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

pred = RNN(x, weights, biases)

# Loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)
# Model evaluation
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(pred, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Initializing the variables
init = tf.global_variables_initializer()

train_input, test_input, train_output, test_output = get_data.get_train_test_windows(n_input, 0)
with tf.Session() as session:
    session.run(init)
    step = 0
    loss_total = 0
    acc_total = 0
    offset = 0
    while step < training_iters:
        input_batch, output_batch = get_data.get_batch(train_input, train_output, batch_size)
        _, acc, loss, prediction = session.run([optimizer, accuracy, cost, pred], \
                                                feed_dict={x: input_batch, y: output_batch})
        if step % display_step == 0:
            print("Iter= " + str(step + 1) + ", Average Loss= " + \
                  "{:.6f}".format(loss) + ", Average Accuracy= " + \
                  "{:.2f}%".format(100 * acc))
        step += 1

    _, acc, loss, prediction = session.run([optimizer, accuracy, cost, pred],{x: test_input, y: test_output})
    print('Epoch {:2d} Average Accuracy on test set {:3.1f}%'.format(training_iters + 1, 100 * acc))
    session.close()