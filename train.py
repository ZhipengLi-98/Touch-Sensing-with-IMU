import os
import utils
import feature
import numpy as np
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

# vertical or horizontal
direct = "vertical"


def read_data(delay, finger):
    names = []
    files = []

    posfiles = os.listdir("./data/")
    for f in posfiles:
        filepath = os.path.join("./data/", f)
        if os.path.isfile(filepath) and f.split(".")[-1] == "ext":
            direction, name, fingers = utils.get_file_info(f)
            if name not in names:
                names.append(name)
            if direction == direct and fingers == finger:
                files.append(filepath)

    negfiles = os.listdir("./negative/")
    for f in negfiles:
        filepath = os.path.join("./negative/", f)
        if os.path.isfile(filepath) == f.split(".")[-1] == "ext":
            direction, name, fingers = utils.get_file_info(f)
            if name not in names:
                names.append(name)
            if direction == "negative" and fingers == finger:
                files.append(filepath)

    # 10 frames -5, 4
    info, data = utils.input(files, 9 - delay, delay)

    # add negative
    # -14, -5
    info_neg, data_neg = utils.input(files, 14, -5)
    for i in info_neg:
        i[3] = -1
    info.extend(info_neg)
    data.extend(data_neg)

    features = feature.calc_features(info, data)

    return info, data, names, features


def train(info, features, finger):
    X_train = []
    y_train = []
    for i in range(len(info)):
        label = 0
        if info[i][3] != -1:
            label = 1
        X_train.append(features[i])
        y_train.append(label)
    clf = DecisionTreeClassifier(random_state=0)
    # clf = SVC(gamma='auto')
    clf.fit(X_train, y_train)

    joblib.dump(clf, "./dtree/" + direct + "_" + finger + ".model")
    # joblib.dump(clf, direct + "_" + finger + ".model")


def test(info, names, features, finger):
    clf = joblib.load("./dtree/" + direct + "_" + finger + ".model")
    # clf = joblib.load(direct + "_" + finger + ".model")
    accuracy_list = []
    precision_list = []
    recall_list = []
    f1_list = []

    for leave in range(len(names)):
        X_test = []
        y_test = []

        for i in range(len(info)):
            label = 0
            if info[i][3] != -1:
                label = 1

            if info[i][1] == names[leave]:
                X_test.append(features[i])
                y_test.append(label)

        if len(X_test) == 0:
            print("No data!")
        else:
            y_pred = clf.predict(X_test)
            accuracy, precision, recall = feature.calc_result(y_test, y_pred)
            f1 = 2 * precision * recall / (precision + recall)
            accuracy_list.append(accuracy)
            precision_list.append(precision)
            recall_list.append(recall)
            f1_list.append(f1)

    accuracy_list = np.array(accuracy_list)
    precision_list = np.array(precision_list)
    recall_list = np.array(recall_list)
    f1_list = np.array(f1_list)

    print(direct, finger)
    print("Accuracy: %0.3f(%0.3f)" % (accuracy_list.mean(), accuracy_list.std()))
    print("Precision: %0.3f(%0.3f)" % (precision_list.mean(), precision_list.std()))
    print("Recall: %0.3f(%0.3f)" % (recall_list.mean(), recall_list.std()))
    print("F1: %0.3f(%0.3f)" % (f1_list.mean(), f1_list.std()))


if __name__ == "__main__":
    # ['index1', 'middle1', 'ring1', 'index3', 'middle3']
    delay = 4
    finger = "index3"
    info, data, names, features = read_data(delay, finger)
    train(info, features, finger)
    test(info, names, features, finger)
