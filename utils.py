import numpy as np


def get_file_info(file):
    direction = file.split(".")[0].split("_")[0]
    name = file.split(".")[0].split("_")[1]
    finger = file.split(".")[0].split("_")[2]
    return direction, name, finger


# convert quaternion to 3 div vector
def qua_to_vec(q):
    return [float(2 * (q[1] * q[3] - q[0] * q[2])),
            float(2 * (q[0] * q[1] + q[2] * q[3])),
            float(2 * (0.5 - q[1] ** 2 - q[2] ** 2))]


def input(files, cut_l=-1, cut_r=-1):
    info = []
    data = []
    for file in files:
        with open(file, "r") as f:
            lines = f.readlines()
            lines = [line.strip("\n") for line in lines]

            direction, name, finger = get_file_info(file.split("/")[-1])

            i = 0
            while i < len(lines):
                tags = lines[i].split()
                label, length, key = int(tags[0]), int(tags[1]), int(tags[2])
                info.append([direction, name, finger, label, length, key])

                i += 1
                frames = []
                for j in range(i, i + length):
                    tags = lines[j].split()
                    frame = [float(v) for v in tags]
                    temp = j - i - key
                    if cut_l == -1 or (-cut_l <= temp and temp <= cut_r):
                        frames.append(frame)

                frame_length = len(frames)
                frames = np.array(frames).reshape(frame_length, -1)
                data.append(frames)

                i += length

    return info, data
