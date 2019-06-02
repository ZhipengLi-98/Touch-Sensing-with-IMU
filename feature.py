import numpy as np
import utils
import math


def caln_sequence(X):
    X = np.array(X)
    X_std = np.std(X)
    X_min = np.min(X)
    X_max = np.max(X)
    X_mean = np.mean(X)
    X_var = np.var(X)
    X_sc = np.mean((X - X_mean) ** 3) / pow(X_std, 3)
    X_ku = np.mean((X - X_mean) ** 4) / pow(X_std, 4)
    if math.isnan(X_ku):
        print("Data Error!")
        X_ku = 0
    return [X_mean, X_min, X_max, X_sc, X_ku]


def calc_features(info, data):
    features = []
    for i in range(len(info)):
        gyr_x = data[i][:, 2]
        gyr_y = data[i][:, 3]
        gyr_z = data[i][:, 4]
        acc_x = data[i][:, 5]
        acc_y = data[i][:, 6]
        acc_z = data[i][:, 7]
        length = np.size(data[i], 0)
        gra_x = np.zeros(length)
        gra_y = np.zeros(length)
        gra_z = np.zeros(length)
        for j in range(length):
            gra = utils.qua_to_vec(data[i][j, 8:12])
            gra_x[j] = gra[0]
            gra_y[j] = gra[1]
            gra_z[j] = gra[2]
        feature = []
        # gyr = np.array([(gyr_x ** 2 + gyr_y ** 2 + gyr_z ** 2) ** 0.5])
        # acc = np.array([(acc_x ** 2 + acc_y ** 2 + acc_z ** 2) ** 0.5])
        # feature.extend(caln_sequence(gyr))
        # feature.extend(caln_sequence(acc))
        feature.extend(caln_sequence(acc_x))
        feature.extend(caln_sequence(acc_y))
        feature.extend(caln_sequence(acc_z))
        feature.extend(caln_sequence(gra_x))
        feature.extend(caln_sequence(gra_y))
        feature.extend(caln_sequence(gra_z))
        feature.extend(caln_sequence(gyr_x))
        feature.extend(caln_sequence(gyr_y))
        feature.extend(caln_sequence(gyr_z))
        features.append(feature)

    return features


def normalize_X(X_train, X_test):
    len_train = len(X_train)
    len_test = len(X_test)
    X_train = np.array(X_train).reshape(len_train, -1)
    X_test = np.array(X_test).reshape(len_test, -1)
    len_features = np.size(X_train, 1)
    for i in range(len_features):
        X_mean = np.mean(X_train[:,i])
        X_std = np.std(X_train[:,i])
        X_train[:,i] = (X_train[:,i] - X_mean) / X_std
        X_test[:,i] = (X_test[:,i] - X_mean) / X_std
    return X_train, X_test


def calc_precision_recall(y_test, y_pred):
    pre_a = 0
    pre_b = 0
    rec_a = 0
    rec_b = 0
    for i in range(len(y_test)):
        if y_test[i] == 1:
            rec_b += 1
            if y_test[i] == y_pred[i]:
                rec_a += 1
        if y_pred[i] == 1:
            pre_b += 1
            if y_test[i] == y_pred[i]:
                pre_a += 1
    if pre_b == 0:
        precision = 1
    else:
        precision = float(pre_a) / pre_b
    if rec_b == 0:
        recall = 1
    else:
        recall = float(rec_a) / rec_b
    return precision, recall

