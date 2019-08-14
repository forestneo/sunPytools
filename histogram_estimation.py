#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 10:16
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

import matplotlib.pyplot as plt
import numpy as np
from basis import basis_differential_privacy as sdp


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
    for i in range(len(user_vector)):
        user_vector[i] = sdp.random_response_basic(user_vector[i], epsilon=epsilon / 2)
    return user_vector


if __name__ == '__main__':
    # 生成数据
    users = generate_data(user_number=100000)

    # 得到原始数据的直方图
    original_hist = np.sum(users, axis=0)
    print("this is original hist: \n", original_hist)

    # 隐私参数
    epsilon = np.log(3)

    # aggregator收集并处理数据
    rr_user = np.asarray([random_response_for_hist(user, epsilon) for user in users])
    rr_sums = np.sum(rr_user, axis=0)
    print("this is the hist by the aggregator: \n", rr_sums)

    # aggregator校正数据
    estimate_hist = [sdp.random_response_adjust(rr_sum, len(users), epsilon/2) for rr_sum in rr_sums]
    print(np.sum(estimate_hist))

    # 展示原始数据的直方图
    print("this is estimated hist: \n", estimate_hist)

    # 画图
    fig = plt.figure(figsize=[12, 5])
    ax1 = fig.add_subplot(121)  # 2*2的图形 在第一个位置
    ax1.bar(range(len(original_hist)), original_hist)
    ax2 = fig.add_subplot(122)
    ax2.bar(range(len(estimate_hist)), estimate_hist)
    plt.show()