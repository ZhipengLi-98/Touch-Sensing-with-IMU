import os
import utils
import feature
import numpy as np
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# vertical or horizontal
direct = "vertical"


def analyze(delay, finger):
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

    label_0 = 0
    label_1 = 0

    precision_list = []
    recall_list = []
    f1_list = []

    for leave in range(len(names)):
        X_train = []
        y_train = []
        X_test = []
        y_test = []

        for i in range(len(info)):
            label = 0
            if info[i][3] != -1:
                label = 1

            if label == 0:
                label_0 += 1
            else:
                label_1 += 1
            if info[i][1] == names[leave]:
                X_test.append(features[i])
                y_test.append(label)
            else:
                X_train.append(features[i])
                y_train.append(label)

        # clf = DecisionTreeClassifier(random_state=0)
        clf = SVC(gamma='auto')
        clf.fit(X_train, y_train)

        if len(X_test) == 0:
            print("No Data!")
        else:
            y_pred = clf.predict(X_test)
            precision, recall = feature.calc_precision_recall(y_test, y_pred)
            f1 = 2 * precision * recall / (precision + recall)
            precision_list.append(precision)
            recall_list.append(recall)
            f1_list.append(f1)

    precision_list = np.array(precision_list)
    recall_list = np.array(recall_list)
    f1_list = np.array(f1_list)

    pre_str = ""
    for v in precision_list:
        pre_str = pre_str + " " + str(v)
    rec_str = ""
    for v in recall_list:
        rec_str = rec_str + " " + str(v)
    f1_str = ""
    for v in f1_list:
        f1_str = f1_str + " " + str(v)
    print("Precision:", pre_str)
    print("Recall:", rec_str)
    print("F1:", f1_str)


if __name__ == "__main__":
    # ['index1', 'middle1', 'ring1', 'index3', 'middle3']
    analyze(4, "index1")
