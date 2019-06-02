import os
import numpy as np
import math
import random


def parse_frames(imu, frames, right):
    factors = []
    left_gap = 500
    right_gap = 100
    left = right
    while left > 0 and int(imu[right][0]) - int(imu[left][0]) < left_gap:
        left -= 1
    begin = left
    left = right
    while left + 1 < len(imu) and int(imu[left][0]) - int(imu[right][0]) < right_gap:
        left += 1
    end = left
    k = 1
    for i in range(begin, end + 1):
        for v in imu[i]:
            if math.isnan(float(v)):
                print("No IMU data!")
                return [], -1
        factor = [v for v in imu[i]]
        while k + 1 < len(frames) and int(frames[k][0]) < int(imu[i][0]):
            k += 1
        duration = (float)(int(frames[k][0]) - int(frames[k - 1][0]))
        if duration > 50:
            print("No Hand Data!")
            return [], -1
        t = (float)(int(frames[k][0]) - int(imu[i][0])) / duration
        v0 = np.array([float(v) for v in frames[k - 1]])
        v1 = np.array([float(v) for v in frames[k]])
        v = v0 * t + v1 * (1.0 - t)
        factor.extend(v)
        factors.append(factor)

    return factors, right - begin


def parse_dir(path):
    print(path)
    vision = [None] * 10
    data = []
    with open(path, "r") as f:
        if path[-5] == "U":
            data = f.readlines()
        else:
            vision[int(path[-5]) - 0] = f.readlines()
    imu = []
    for line in data:
        line = line.strip('\n')
        tags = line.split()
        imu.append(tags)

    with open(path, "w") as f:
        with open(path[: -4] + ".ext", "w") as fout:
            for i in range(10):
                if not vision[i] == None:
                    frames = []
                    for line in vision[i]:
                        line = line.strip('\n')
                        tags = line.split()
                        frames.append(tags)
                    start = int(frames[0][0])
                    end = int(frames[-1][0])
                    candidate = []
                    for j in range(1, len(imu) - 1):
                        t = int(imu[j][0])
                        if start <= t and t <= end:
                            if int(imu[j - 1][-1]) == 0 and int(imu[j][-1]) == 1 and int(imu[j + 1][-1]) == 1:
                                candidate.append(j)
                    tap = [v for v in candidate]
                    for j in range(len(candidate) - 1):
                        j0 = candidate[j]
                        j1 = candidate[j + 1]
                        t0 = int(imu[j0][0])
                        t1 = int(imu[j1][0])
                        if t1 - t0 < 100:  # tapping too close
                            if j0 in tap:
                                tap.remove(j0)
                            if j1 in tap:
                                tap.remove(j1)

                    cnt = 0
                    for j in candidate:
                        factors_list, key = parse_frames(imu, frames, j)
                        if key == -1:  # no hand data
                            continue

                        key = min(key, len(factors_list))
                        factors = factors_list[key]
                        palm_z = float(factors[18])
                        if palm_z < 0:  # wrong marker direction
                            continue

                        cnt = cnt + 1
                        f.write(str(i))
                        for v in factors:
                            f.write(' ')
                            f.write(str(v))
                        f.write('\n')

                        fout.write(str(i) + ' ' + str(len(factors_list)) + ' ' + str(key) + '\n')
                        for factors in factors_list:
                            fout.write(str(factors[0]))
                            for k in range(1, len(imu[j])):
                                fout.write(' ')
                                fout.write(str(factors[k]))
                            fout.write('\n')
                    print(i, cnt)


# choose random moment in negative files
def parse_negative(path):
    print(path)
    with open(path, "r") as f:
        with open(path[: -3] + "ext", "w") as fout:
            lines = f.readlines()
            data = []
            for line in lines:
                line = line.strip("\n")
                data.append(line.split())
            length = len(data)

            # left_gap, right_gap: timestamp gap
            left_gap = 500
            right_gap = 100
            samples = 170
            cnt = 0

            while cnt < samples:
                right = random.randint(left_gap, length - right_gap - 1)
                left = right
                while left > 0 and int(data[right][0]) - int(data[left][0]) < left_gap:
                    left -= 1
                begin = left
                left = right
                while left + 1 < len(data) and int(data[left][0]) - int(data[right][0]) < right_gap:
                    left += 1
                end = left

                factors = []
                key = right - begin
                flag = True

                for i in range(begin, end + 1):
                    for j in data[i]:
                        if math.isnan(float(j)):
                            print("No IMU data!")
                            flag = False
                    factors.append([j for j in data[i]])

                temp = np.array(factors).reshape(len(factors), -1)
                # [2, cols - 1)
                # check the imu data
                for i in range(2, np.size(temp, 1) - 1):
                    t = [float(j) for j in temp[:, i]]
                    if np.var(t) == 0:
                        flag = False

                if flag:
                    cnt += 1
                    # Important
                    fout.write(str(-1) + " " + str(len(factors)) + " " + str(key) + "\n")
                    for factor in factors:
                        fout.write(str(factor[0]))
                        for i in range(1, len(factors)):
                            fout.write(" ")
                            fout.write(str(factors[i]))
                        fout.write("\n")


def positive_parser():
    files = os.listdir("./data/")
    for f in files:
        path = os.path.join("./data/", f)
        if os.path.isfile(path):
            if f[:-3] + "ext" in files:
                continue
            parse_dir(path)


def negative_parser():
    files = os.listdir("./negative/")
    for f in files:
        path = os.path.join("./negative/", f)
        if os.path.isfile(path) and f[-3:] == "txt":
            if f[: -3] + "ext" in files:
                continue
            parse_negative(path)


if __name__ == "__main__":
    positive_parser()
