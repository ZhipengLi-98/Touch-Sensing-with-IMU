import os
import utils

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

    # 10 frames
    # info, data = utils.input(files, 9 - delay, delay)

    # add negative
    # -14, -5
    info_neg, data_neg = utils.input(files, 14, -5)
    print(len(data_neg))


if __name__ == "__main__":
    # ['index1', 'middle1', 'ring1', 'index3', 'middle3']
    analyze(4, "index1")
