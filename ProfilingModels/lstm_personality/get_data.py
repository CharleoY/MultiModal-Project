from pymongo import MongoClient
import numpy as np
import random
from sklearn.decomposition import NMF
import logging
import os
import pickle
import uuid
from imblearn.over_sampling import SMOTE

###
# Mongo params
MONGO_PORT = 27017
MONGO_HOST = '172.29.29.30'
MONGO_DB = 'mbti_research_fs'
# Features full dimensions
TEXT_DIM = 53
LIWC_DIM = 64
LDA_DIM = 50
LOCATION_DIM = 886
MEDIA_DIM = 1000
PERIODS = 10
###
features_dim = TEXT_DIM + LIWC_DIM + LDA_DIM + LOCATION_DIM


def init_logging(filename = None):
    if filename is None:
        filename = 'logs/%s.log' % str(uuid.uuid4())
    else:
        filename = 'logs/' + filename + '.log'
    print ('logs located in %s' % filename)
    logging.basicConfig(filename=filename, filemode='w+', level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    return logging


def connect_to_database(host, port, db_name):
    # connects to mongo
    client = MongoClient(host, port)
    return client[db_name]


def get_labels_stats(train_output, test_output, mbti_position):
    # train_set
    train_zero, train_one = 0, 0
    for train_label in train_output:
        if train_label == [1, 0]:
            train_zero += 1
        else:
            train_one += 1
    logging.info('Stats for %s/%s label in train set. Number: %d/%d, percentage: %.2f, %.2f' %
                 (get_label_letter(mbti_position, 0), get_label_letter(mbti_position, 1),
                  train_zero, train_one,
                  train_zero/(train_zero + train_one), train_one/(train_zero + train_one)))

    # train_set
    test_zero, test_one = 0, 0
    for test_label in test_output:
        if test_label == [1, 0]:
            test_zero += 1
        else:
            test_one += 1
    logging.info('Stats for %s/%s label in test set. Number: %d/%d, percentage: %.2f, %.2f' %
                 (get_label_letter(mbti_position, 0), get_label_letter(mbti_position, 1),
                  test_zero, test_one,
                  test_zero / (test_zero + test_one), test_one / (test_zero + test_one)))


def download_window_data(window_size, label):
    try:
        train_input = pickle.load(open('../store/window_%d/train_input_%d.pkl' % (window_size, label), 'rb'))
        train_output = pickle.load(open('../store/window_%d/train_output_%d.pkl' % (window_size, label), 'rb'))
        test_input = pickle.load(open('../store/window_%d/test_input_%d.pkl' % (window_size, label), 'rb'))
        test_output = pickle.load(open('../store/window_%d/test_output_%d.pkl' % (window_size, label), 'rb'))
        users_mapping = pickle.load(open('../store/window_%d/users_mapping_%d.pkl' %
                                         (window_size, label), 'rb'))
        test_uuids = pickle.load(open('../store/window_%d/test_uuids_%d.pkl' %
                                      (window_size, label), 'rb'))
        logging.info('Found {%d} train samples, {%d} test samples for {%d} period-window' %
                     (len(train_input), len(test_output), window_size))
        get_labels_stats(train_output, test_output, label)
        return train_input, test_input, train_output, test_output, users_mapping, test_uuids
    except:
        raise FileNotFoundError('There is no prepared window data!')


def convert_mbti_to_vector(mbti, mbti_position):
    """
    convert mbti to 2-dimensional vector representation
    the label is argmax of 2-dim vector
    labels_zero = ['E', 'N', 'F', 'P']
    labels_one = ['I', 'S', 'T', 'J']
    """
    mbti_vector = list()
    if mbti[0] == 'I':
        mbti_vector.append([0, 1])
    if mbti[0] == 'E':
        mbti_vector.append([1, 0])
    if mbti[1] == 'S':
        mbti_vector.append([0, 1])
    if mbti[1] == 'N':
        mbti_vector.append([1, 0])
    if mbti[2] == 'T':
        mbti_vector.append([0, 1])
    if mbti[2] == 'F':
        mbti_vector.append([1, 0])
    if mbti[3] == 'J':
        mbti_vector.append([0, 1])
    if mbti[3] == 'P':
        mbti_vector.append([1, 0])

    return mbti_vector[mbti_position]


def get_label_letter(mbti_position, label):
    mbti = ['EI', 'NS', 'FT', 'PJ']
    return mbti[mbti_position][label]


def get_label_int(mbti_letter):
    labels_0 = ['E', 'N', 'F', 'P']
    if mbti_letter in labels_0:
        return 0
    else:
        return 1


def split_data_to_train_test():
    # split ALL users (table: users) into train(0.8) and test(0.2) sets based on the distribution of their MBTI
    db = connect_to_database(MONGO_HOST, MONGO_PORT, MONGO_DB)
    mbti_types = db['users'].distinct('mbti')
    for mbti in mbti_types:
        users = db['users'].find({'mbti': mbti})
        randoms = list()
        for i in range(users.count()):
            randoms.append(random.uniform(0, 1))
        for (user, p) in zip(users, randoms):
            if p < 0.8:
                user['set'] = 'train'
            else:
                user['set'] = 'test'
            db['users'].update({'_id': user['_id']}, user)


def get_batch(input_data, output_data, batch_size, offset):
    if offset + batch_size >= len(output_data):
        batch_size = len(output_data) - offset - 1
    indexes = range(offset, offset + batch_size)
    input_batch, output_batch = list(), list()

    for i in indexes:
        input_batch.append(input_data[i])
        output_batch.append(output_data[i])

    return input_batch, output_batch


def fill_missed_modality(period, label):
    """get all users with activity in current period
    build the matrix and do it factorization
    need to know the order of features to write them into database then
    store all features in one vector as a result"""
    db = connect_to_database(MONGO_HOST, MONGO_PORT, MONGO_DB)
    modalities = ['text', 'liwc', 'lda', 'media', 'location']
    modalities_dimensions = [26, 32, 25, 44, 50]
    period_users = list()  # all active users in any social network for this period
    for modality in modalities:
        logging.info('Get users for %s modalitity' % modality)
        users = db['fs_%s_%d_%d' % (modality, period, label)].distinct('_id')
        for user in users:
            if user not in period_users:
                period_users.append(user)

    users_features = list()  # the order of users will be the same as in users list
    features_order = dict()  # the order of features will be the same for (modality, label)
    for modality in modalities:
        features_order[modality] = list()
    incomplete_dimensions = 0

    for user in period_users:
        feature_vector = list()
        for modality, dimension in zip(modalities, modalities_dimensions):
            features = db['fs_%s_%d_%d' % (modality, period, label)].find_one({'_id': user})
            if features is None:
                feature_vector.extend([0] * dimension)
                incomplete_dimensions += 1
            else:
                if len(features_order[modality]) == 0:
                    features_order[modality] = list(features.keys())
                    features_order[modality].remove('_id')
                for feature_name in features_order[modality]:
                    if features[feature_name] < 0:  # FIXME it happens only for sentiment score here
                        feature_vector.append((-1.0) * features[feature_name])
                    else:
                        feature_vector.append(features[feature_name])
        users_features.append(np.array(feature_vector))

    logging.info("Found {%d} incomplete dimensions" % incomplete_dimensions)
    R = np.array(users_features)
    model = NMF(init='random', random_state=42)
    W = model.fit_transform(R)
    H = model.components_
    transformed_data = np.dot(W, H)

    db_restore = connect_to_database(MONGO_HOST, MONGO_PORT, MONGO_DB)
    for user in period_users:
        sum_dimension = 0
        user_position = period_users.index(user)
        for modality, dimension in zip(modalities, modalities_dimensions):
            features = db['fs_%s_%d_%d' % (modality, period, label)].find_one({'_id': user})
            if features is None:
                features_to_db = dict()
                features_to_db['_id'] = user
                for (feature, index) in zip(features_order, range(0, dimension)):
                    features_to_db[feature] = transformed_data[user_position][sum_dimension + index]
                db_restore['fs_%s_%d_%d' % (modality, period, label)].insert(features_to_db)
                logging.info("Modality {%s} was restore for user {%s}" % (modality, user))

            sum_dimension += dimension


def store_modalities_in_one_vector(modalities, period, label):
    db = connect_to_database(MONGO_HOST, MONGO_PORT, MONGO_DB + '_restore')
    users = db['fs_%s_%d_%d' % (modalities[0], period, label)].distinct('_id')
    for user in users:
        user_vector = dict()
        for modality in modalities:
            modality_vector = db['fs_%s_%d_%d' % (modality, period, label)].find_one({'_id': user})
            del modality_vector['_id']
            for feature in modality_vector:
                user_vector[feature] = modality_vector[feature]
        user_vector['_id'] = user
        db['period_%d_%d' % (period, label)].insert(user_vector)


def input_output_generation(train_input, test_input, train_output, test_output, n_periods):
    # get data from train/test inputs and prepare it for LSTM format
    # input data - list of lists of vectors, one for each period
    train_i, test_i = list(), list()
    train_o, test_o = list(), list()
    users_num = 0

    logging.info('Generation train/test input/output')
    for user in train_input:
        train_i.append(list())
        for period in range(0, n_periods):
            train_i[len(train_i) - 1].append(train_input[user][period + 1])
        train_o.append(train_output[user])
        users_num += 1

    users_num = 0
    for user in test_input:
        test_i.append(list())
        for period in range(0, n_periods):
            test_i[users_num].append(test_input[user][period + 1])
        test_o.append(test_output[user])
        users_num += 1

    return train_i, test_i, train_o, test_o


def apply_oversampling(train_i, train_o, n_periods):
    logging.info('Applying oversampling')
    train_size = len(train_i)
    smote = SMOTE(random_state=42)
    for p in range(0, n_periods):
        input_vectors, output_vectors = list(), list()
        for i in range(0, train_size):
            input_vectors.append(train_i[i][p])
            output_vectors.append(np.argmax(train_o[i]))
        _input, _output = smote.fit_sample(input_vectors, output_vectors)
        for i in range(train_size, len(_input)):
            if len(train_i) < len(_input):
                train_i.append(list())
            train_i[i].append(list(_input[i]))
    for i in range(len(train_o), len(_output)):
        if _output[i] == 0:
            train_o.append([1, 0])
        else:
            train_o.append([0, 1])
    return train_i, train_o



def get_train_test_windows(n_periods, label, store=True):
    try:
        return download_window_data(n_periods, label)
    except FileNotFoundError:
        logging.info("There is no prepared data for window-periods")
    # find users, that posts in every window of [n_periods] periods
    # 1 2 3 4 -> from this will return all users that posts in [1, 2], [2, 3].
    # will give uuid for every user to avoid the duplication of ids
    # will return test/train sets for period windows
    db = connect_to_database(MONGO_HOST, MONGO_PORT, MONGO_DB)
    users_mapping = dict()  # map md5(user) -> user
    train_output, test_output = dict(), dict()  # dict md5(user) -> MBTI_vector
    train_input, test_input = dict(), dict()  # dict md5(user) -> dict period -> features
    test_uuids = list()  # list to know the order of uuid of test users
    logging.info('Begin to collect data for %d-windows %d label' % (n_periods, label))
    # get all users

    features_order = list()
    for i in range(1, PERIODS):
        if i + n_periods > PERIODS + 1:
            break
        logging.info('Getting data for %d period in the beginning' % i)
        window_users = dict()
        for p in range(0, n_periods):
            period_users = db['period_%d_%d' % (p+i, label)].find()
            for user in period_users:
                if user['_id'] not in window_users:
                    window_users[user['_id']] = 1
                else:
                    window_users[user['_id']] += 1

        for user in window_users:
            if window_users[user] != n_periods:
                continue

            new_id = str(uuid.uuid4())
            users_mapping[new_id] = user
            user = db['users'].find_one({'twitterUserName': user})
            if user is None:
                logging.error('Find None user')
                continue

            if user['set'] == 'train':
                train_input[new_id] = dict()
                train_output[new_id] = dict()
                window_period = 1
                for p in range(i, i + n_periods):
                    features = db['period_%d_%d' % (p, label)].find_one({'_id': user['twitterUserName']})
                    if len(features_order) == 0:
                        features_order = list(features.keys())
                        features_order.remove('_id')

                    train_input[new_id][window_period] = list()
                    for feature in features_order:
                        train_input[new_id][window_period].append(features[feature])
                    window_period += 1
                train_output[new_id] = convert_mbti_to_vector(user['mbti'], label)
            else:
                test_input[new_id] = dict()
                test_output[new_id] = dict()
                window_period = 1
                for p in range(i, i + n_periods):
                    features = db['period_%d_%d' % (p, label)].find_one({'_id': user['twitterUserName']})
                    if len(features_order) == 0:
                        features_order = list(features.keys())
                        features_order.remove('_id')
                    test_input[new_id][window_period] = list()
                    for feature in features_order:
                            test_input[new_id][window_period].append(features[feature])
                    window_period += 1
                test_output[new_id] = convert_mbti_to_vector(user['mbti'], label)
                test_uuids.append(new_id)

    logging.info("Found {%d} train samples, {%d} test samples for {%d} period-window" %
                 (len(train_input), len(test_output), n_periods))

    train_input, test_input, train_output, test_output = input_output_generation(train_input, test_input,
                                                                                 train_output, test_output, n_periods)
    get_labels_stats(train_output, test_output, label)
    if store:
        logging.info('Saving data...')
        if not os.path.exists('../store/window_%d' % n_periods):
            os.makedirs('../store/window_%d' % n_periods)
        pickle.dump(train_input, open('../store/window_%d/train_input_%d.pkl' % (n_periods, label), 'wb'))
        pickle.dump(train_output, open('../store/window_%d/train_output_%d.pkl' % (n_periods, label), 'wb'))
        pickle.dump(test_input, open('../store/window_%d/test_input_%d.pkl' % (n_periods, label), 'wb'))
        pickle.dump(test_output, open('../store/window_%d/test_output_%d.pkl' % (n_periods, label), 'wb'))
        pickle.dump(users_mapping, open('../store/window_%d/users_mapping_%d.pkl' % (n_periods, label), 'wb'))
        pickle.dump(test_uuids, open('../store/window_%d/test_uuids_%d.pkl' % (n_periods, label), 'wb'))
        logging.info('Data successfully saved')

    return train_input, test_input, train_output, test_output, users_mapping, test_uuids
