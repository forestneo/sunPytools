# -*- coding: utf-8 -*-
# @Time    : 2019-07-11 15:00
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

'''
Piecewise 有两种实现方法
第一种是原作者给出的，我由C++代码改成了python版本的代码，叫做 encode_piecewise(value, epsilon)
第二种是我给出的，叫做 encode_piecewise_mine(value, epsilon)
'''


import numpy as np
import matplotlib.pyplot as plt


# 作者的实现方法
def encode_piecewise(value, epsilon):
    """
    Piecewise Mechanism, from paper: Collecting and Analyzing Multidimensional Data with Local Differential Privacy
    """
    z = np.e**(epsilon/2)
    P1 = (value + 1) / (2 + 2 * z)
    P2 = z / (z + 1)
    P3 = (1 - value) / (2 + 2 * z)

    C = (z + 1) / (z - 1)
    g1 = (C + 1) * value / 2 - (C - 1) / 2
    g2 = (C + 1) * value / 2 + (C - 1) / 2

    rnd = np.random.random()
    if rnd < P1:
        result = -C + np.random.random() * (g1 - (-C))
    elif rnd < P1 + P2:
        result = (g2 - g1) * np.random.random() + g1
    else:
        result = (C - g2) * np.random.random() + g2
    return result


# 我的实现方法
def encode_piecewise_mine(value, epsilon):
    """
    Piecewise Mechanism, from paper: Collecting and Analyzing Multidimensional Data with Local Differential Privacy
    """
    C = (np.e**(epsilon/2)+1) / (np.e**(epsilon/2)-1)
    p = (np.e**epsilon - np.e**(epsilon/2)) / (2*np.e**(epsilon/2)+2)
    L = (C+1)/2 * value - (C-1)/2
    R = L + C - 1

    # 将数据分为两部分，一部分是仅仅在高概率，一部分是随机在所有数据中产生，仅在高概率的概率为 p_h
    p_h = (p - p / (np.e**epsilon)) * (C-1)

    rnd = np.random.random()
    if rnd <= p_h:
        rnd_v = np.random.uniform(L, R)
    else:
        rnd_v = np.random.uniform(-C, C)

    return rnd_v


def decode_piecewise(value_list, epsilon):
    return np.average(value_list)