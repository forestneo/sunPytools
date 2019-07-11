#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 11:08
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm


from basis import basis_differential_privacy as dp
import numpy as np
import matplotlib.pyplot as plt

def encode(value, epsilon):
    value = dp.discretization(value=value, lower=-1, upper=1)
    value = dp.perturbation(value=value, perturbed_value=-value, epsilon=epsilon)
    value = (np.e**epsilon+1)/(np.e**epsilon-1) * value
    return value


def get_error(data, epsilon):
    mean_ori = np.average(data)
    encode_data = [encode(value, epsilon) for value in data]
    mean_est = np.average(encode_data)
    return np.fabs(mean_ori-mean_est)


if __name__ == '__main__':
    # 产生数据并归一化
    data = np.random.normal(loc=0.2, scale=0.3, size=100000)
    data = np.clip(data, -1, 1)

    epsilon_list = []
    err_list = []

    for i in range(50):
        # 设定 epsilon 从 0 到 1 变化
        epsilon = 0.02 * (i+1)
        error = get_error(data, epsilon)
        epsilon_list.append(epsilon)
        err_list.append(error)
        print(epsilon, error)

    # 画图
    fig = plt.figure(figsize=[12, 5])
    plt.plot(epsilon_list, err_list, label="error_with_epsilon")
    plt.xlabel("epsilon")
    plt.ylabel("error")
    plt.legend()
    plt.show()
