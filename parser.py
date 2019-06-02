import os
import numpy as np
import math
import random
import utils


def parse_frames(imu, frames, j):
    factors_list = []
    left_gap = 500
    right_gap = 100
    i = j
    while i > 0 and int(imu[j][0]) - int(imu[i][0]) < left_gap:
        i = i - 1
    begin_j = i
    i = j
    while i + 1 < len(imu) and int(imu[i][0]) - int(imu[j][0]) < right_gap:
        i = i + 1
    end_j = i
    k = 1
    for i in range(begin_j, end_j + 1):
        for v in imu[i]:
            if (math.isnan(float(v))):
                print('no imu data')
                return [], -1
        factors = [v for v in imu[i]]
        while k + 1 < len(frames) and int(frames[k][0]) < int(imu[i][0]):
            k = k + 1
        duration = (float)(int(frames[k][0]) - int(frames[k - 1][0]))
        if duration > 50:
            print('no hand data')
            return [], -1
        t = (float)(int(frames[k][0]) - int(imu[i][0])) / duration
        v0 = np.array([float(v) for v in frames[k - 1]])
        v1 = np.array([float(v) for v in frames[k]])
        v = v0 * t + v1 * (1.0 - t)
        factors.extend(v)
        factors_list.append(factors)

    return factors_list, j - begin_j


def parse_dir(dir):
    files = os.listdir(dir)
    vision = [] * 10

    for i in range(0, len(files)):
        path = os.path.join(dir, files[i])
        if path[-3:] == 'txt':
            input = open(path, 'r')

            if path[-5] == 'U':
                IMU = input.readlines()
            else:
                vision[int(path[-5]) - int('0')] = input.readlines()
            input.close()

    imu = []
    for line in IMU:
        line = line.strip('\n')
        tags = line.split()
        imu.append(tags)

    fout = open(dir[2:] + '.txt', 'w')
    fout_ext = open(dir[2:] + '.ext', 'w')

    print(dir[2:])

    for i in range(10):
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
            if (start <= t and t <= end):
                if (int(imu[j - 1][-1]) == 0 and int(imu[j][-1]) == 1 and int(imu[j + 1][-1]) == 1):
                    candidate.append(j)
        tap = [v for v in candidate]
        for j in range(len(candidate) - 1):
            j0 = candidate[j]
            j1 = candidate[j + 1]
            t0 = int(imu[j0][0])
            t1 = int(imu[j1][0])
            if (t1 - t0 < 100):  # tapping too close
                if (j0 in tap):
                    tap.remove(j0)
                if (j1 in tap):
                    tap.remove(j1)

        cnt = 0
        for j in candidate:
            factors_list, key = parse_frames(imu, frames, j)
            if key == -1:  # no hand data
                continue

            key = min(key, len(factors_list))

            factors = factors_list[key]

            palm_z = float(factors[18])
            if (palm_z < 0):  # wrong marker direction
                continue

            cnt = cnt + 1

            fout.write(str(i))
            for v in factors:
                fout.write(' ')
                fout.write(str(v))
            fout.write('\n')

            fout_ext.write(str(i) + ' ' + str(len(factors_list)) + ' ' + str(key) + '\n')
            for factors in factors_list:
                fout_ext.write(str(factors[0]))
                for k in range(1, len(imu[j])):
                    fout_ext.write(' ')
                    fout_ext.write(str(factors[k]))
                fout_ext.write('\n')

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
                    left -=1
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

                temp = np.array(factors).reshape(len(factors). -1)
                # [2, cols - 1)
                # check the imu data
                for i in range(2, np.size(temp, 1) - 1):
                    t = [float(j) for j in temp[:, i]]
                    if np.var(t) == 0:
                        flag = False

                if flag:
                    cnt += 1
                    fout.write(str(-1) + " " + str(len(factors)) + " " + str(key) + "\n")
                    for factor in factors:
                        fout.write(str(factor[0]))
                        for i in range(1, len(factors)):
                            fout.write(" ")
                            fout.write(str(factors[i]))
                        fout.write("\n")


def positive_parser():
    files = os.listdir("./data/")
    for i in range(len(files)):
        path = os.path.join("./data/", files[i])
        if os.path.isdir(path):
            if (files[i] + '.txt') in files and (files[i] + '.ext') in files:
                continue
            direction, name, finger = utils.get_file_info(files[i])
            # TODO: why this?
            if name == 'xcy' and finger == 'ring1' and direction == 'vertical':
                parse_dir(path)


def negative_parser():
    files = os.listdir("./negative/")
    for i in range(len(files)):
        path = os.path.join("./negative/", files[i])
        if os.path.isfile(path) and files[i][-3:] == 'txt':
            if (files[i][:-3] + '.ext') in files:
                continue
            parse_negative(path)


if __name__ == "__main__":
    negative_parser()
