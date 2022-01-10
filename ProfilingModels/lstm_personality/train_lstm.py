import sys
sys.path.insert(0, '../source')
import get_data
from LSTM_model import LSTM_model
import logging
from sklearn.metrics import f1_score, precision_score, recall_score
import pickle
import numpy as np

# Features dimensions
TEXT_DIM = 53
LIWC_DIM = 64
LDA_DIM = 50
LOCATION_DIM = 886
MEDIA_DIM = 1000

learning_rate = 0.001
display_step = 1000
input_dimension = 177  # number of features


def main(args):
    #  arg[0]=n_hidden; arg[1]=windows_size; arg[2]=learning_rate; arg[3]=1/0 multi_layer
    labels = [0, 1, 2, 3]
    n_hidden = int(args[0])
    windows_size = int(args[1])
    learning_rate = float(args[2])
    if int(args[3]) == 1:
        multi_layer = True
    else:
        multi_layer = False
    batch_sizes = [32]

    model = LSTM_model(learning_rate=learning_rate,
                       n_hidden=n_hidden,
                       input_dimension=input_dimension,
                       output_dimension=2,
                       n_input=windows_size,
                       multi_layer=multi_layer)

    for label in labels:
        for batch_size in batch_sizes:
            train_input, test_input, train_output, test_output, users_mapping, test_uuids = \
                get_data.get_train_test_windows(windows_size, label)
            train_input, train_output = get_data.apply_oversampling(train_input, train_output, windows_size)
            model.update_params(batch_size=batch_size, label=label)
            predictions = model.train_one_label(train_input, train_output, batch_size, test_input, test_output)
            y_pred = get_prediction_from_lstm_output(predictions, windows_size, label)
            log_accuracy(get_test_groundtruth(label), y_pred, label)
            pickle.dump(y_pred, open("../predictions/%d_%d_%d.ckpt" % (n_hidden, windows_size, label), 'wb'))


def get_test_groundtruth(label):
    db = get_data.connect_to_database(get_data.MONGO_HOST, get_data.MONGO_PORT, get_data.MONGO_DB)
    try:
        test_groundtruth = pickle.load(open('../store/test_groundtruth_%d.pkl' % label, 'rb'))
        return test_groundtruth
    except FileNotFoundError:
        try:
            test_users_order = pickle.load(open('../store/test_users_order.pkl', 'rb'))
        except FileNotFoundError:
            test_users_order = db['users'].distinct('twitterUserName')
            pickle.dump(test_users_order, open('../store/test_users_order.pkl', 'wb'))

        test_groundtruth = list()
        for user in test_users_order:
            test_groundtruth.append(get_data.get_label_int(
                db['users'].find_one({'twitterUserName': user})['mbti'][label]))
        pickle.dump(test_groundtruth, open('../store/test_groundtruth_%d.pkl' % label, 'wb'))
        return test_groundtruth


def get_prediction_from_lstm_output(predictions, window_size, label):
    test_pred, user_windows_num = dict(), dict()
    db = get_data.connect_to_database(get_data.MONGO_HOST, get_data.MONGO_PORT, get_data.MONGO_DB)

    users_mapping = pickle.load(open('../store/window_%d/users_mapping_%d.pkl' % (window_size, label), 'rb'))
    test_uuids = pickle.load(open('../store/window_%d/test_uuids_%d.pkl' % (window_size, label), 'rb'))

    try:
        test_users_order = pickle.load(open('../store/test_users_order.pkl', 'rb'))
    except:
        test_users_order = db['users'].distinct('twitterUserName')
        pickle.dump(test_users_order, open('../store/test_users_order.pkl', 'wb'))

    target_labels = [1, 0, 0, 0]
    target_label = target_labels[label]

    for (prediction, user_uuid) in zip(predictions, test_uuids):
        real_name = users_mapping[user_uuid]
        if real_name not in test_pred:
            test_pred[real_name] = 0
            user_windows_num[real_name] = 0
        test_pred[real_name] = test_pred[real_name] + prediction
        user_windows_num[real_name] += 1

    y_pred = list()
    for user in test_users_order:
        if user in test_pred:
            if test_pred[user] > user_windows_num[user] / 2:
                y_pred.append(1)
            elif test_pred[user] < user_windows_num[user] / 2:
                y_pred.append(0)
            else:
                y_pred.append(target_label)
        else:
            y_pred.append(target_label)
    return y_pred



def log_accuracy(y_true, y_pred, label):
    logging.info("FINAL LABEL RESULTS ON TEST SET")
    logging.info("Label " + get_data.get_label_letter(label, 0) + ", Precision= " + \
                     "{:.3f}".format(precision_score(y_true, y_pred, pos_label=0)) + ", Recall= " + \
                     "{:.3f}".format(recall_score(y_true, y_pred, pos_label=0)) + ", F-measure= " + \
                     "{:.3f}".format(f1_score(y_true, y_pred, pos_label=0)))
    logging.info("Label " + get_data.get_label_letter(label, 1) + ", Precision= " + \
                 "{:.3f}".format(precision_score(y_true, y_pred, pos_label=1)) + ", Recall= " + \
                 "{:.3f}".format(recall_score(y_true, y_pred, pos_label=1)) + ", F-measure= " + \
                 "{:.3f}".format(f1_score(y_true, y_pred, pos_label=1)))


if __name__ == "__main__":
    main(sys.argv[1:])
