#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 10:16
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

import matplotlib.pyplot as plt
import numpy as np
from basis import local_differential_privacy_library as dp


def generate_data(buckets=100, user_number=10000):
    vector = np.zeros([user_number, buckets+1], dtype=int)
    for i in range(user_number):
        rnd = int(np.random.normal(loc=buckets / 2, scale=10))
        rnd = np.clip(rnd, 0, buckets)
        vector[i][rnd] = 1
    return vector


def random_response_for_hist(user_vector, epsilon):
    """
    每个用户对自己的数据进行random response操作
    :param user_vector: [0,0,0,0,...,0,0,1,0,0,...]
    :param epsilon: privacy budget
    :return: [1,0,0,1,1,...]
    """
    return dp.random_response_old(bits=user_vector, p=dp.eps2p(epsilon=epsilon / 2))


if __name__ == '__main__':
    # 生成数据
    data_list = generate_data(user_number=100000)

    # 得到原始数据的直方图
    original_hist = np.sum(data_list, axis=0)
    print("this is original hist: \n", original_hist)

    # 隐私参数
    epsilon = 1

    # aggregator收集并处理数据
    perturbed_data_list = np.asarray([random_response_for_hist(user, epsilon) for user in data_list])
    print("this is the hist by the aggregator: \n", np.sum(perturbed_data_list, axis=0))

    # aggregator校正数据
    # estimate_hist = [dp.random_response_adjust(rr_sum, len(data_list), epsilon / 2) for rr_sum in rr_sums]
    # print(np.sum(estimate_hist))

    estimate_hist = dp.random_response_reverse(data_list=perturbed_data_list, p=dp.eps2p(epsilon=epsilon / 2))

    # 展示原始数据的直方图
    print("this is estimated hist: \n", estimate_hist)

    # 画图
    fig = plt.figure(figsize=[12, 5])
    ax1 = fig.add_subplot(121)  # 2*2的图形 在第一个位置
    ax1.bar(range(len(original_hist)), original_hist)
    ax2 = fig.add_subplot(122)
    ax2.bar(range(len(estimate_hist)), estimate_hist)
    plt.show()