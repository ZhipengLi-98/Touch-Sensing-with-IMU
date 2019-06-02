from train import *
from feature import *
import numpy as np
import utils


datas = []


def classify(clf, data):
    if len(datas) >= 10:
        datas.pop(0)
        datas.append(data)
        data = []
        length = len(datas)
        for i in range(length):
            tags = datas[i].split()
            data.append([float(v) for v in tags])
        data = np.array(data).reshape(length, -1)

        gyr_x = data[:, 2]
        gyr_y = data[:, 3]
        gyr_z = data[:, 4]
        acc_x = data[:, 5]
        acc_y = data[:, 6]
        acc_z = data[:, 7]
        gra_x = np.zeros(length)
        gra_y = np.zeros(length)
        gra_z = np.zeros(length)
        for i in range(length):
            gra = utils.qua_to_vec(data[i, 8:12])
            gra_x[i] = gra[0]
            gra_y[i] = gra[1]
            gra_z[i] = gra[2]
        features = []
        features.extend(caln_sequence(acc_x))
        features.extend(caln_sequence(acc_y))
        features.extend(caln_sequence(acc_z))
        features.extend(caln_sequence(gra_x))
        features.extend(caln_sequence(gra_y))
        features.extend(caln_sequence(gra_z))
        features.extend(caln_sequence(gyr_x))
        features.extend(caln_sequence(gyr_y))
        features.extend(caln_sequence(gyr_z))

        for v in features:
            if math.isnan(v):
                return 0
        return clf.predict([feature][0])
    else:
        datas.append(data)
        return 0

