# -*- coding: utf-8 -*-
# @Time    : 2019-07-11 18:27
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

#

from mean import duchi
from mean import piecewise
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # 产生数据并归一化
    data = np.random.normal(loc=0.2, scale=0.3, size=100000)
    data = np.clip(data, -1, 1)

    mean_ori = np.average(data)
    print("original mean: ", mean_ori)

    # 存放结果
    epsilon_list, error_duchi, error_piecewise = [], [], []

    for i in range(1, 50):
        epsilon = 0.02 * i
        epsilon_list.append(epsilon)

        # duchi's solution
        duchi_data = [duchi.encode_duchi(value, epsilon) for value in data]
        mean_duchi = np.average(duchi_data)
        err_duchi = np.fabs(mean_duchi-mean_ori)
        error_duchi.append(err_duchi)

        # piecewise solution
        pm_data = [piecewise.encode_piecewise_mine(value, epsilon) for value in data]
        mean_pm = np.average(pm_data)
        err_pm = np.fabs(mean_pm-mean_ori)
        print(epsilon, err_duchi, err_pm)

        error_piecewise.append(err_pm)

    # 画图
    fig = plt.figure(figsize=[12, 5])
    plt.plot(epsilon_list, error_duchi, label="duchi")
    plt.plot(epsilon_list, error_piecewise, label="piecewise")
    plt.xlabel("epsilon")
    plt.ylabel("error")
    plt.legend()
    plt.show()

