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

class PiecewiseMechanism:
    def __init__(self, epsilon):
        self.epsilon = epsilon

    def encode(self, v):
        """
        Piecewise Mechanism, from paper: Collecting and Analyzing Multidimensional Data with Local Differential Privacy
        """
        z = np.e ** (self.epsilon / 2)
        P1 = (v + 1) / (2 + 2 * z)
        P2 = z / (z + 1)
        P3 = (1 - v) / (2 + 2 * z)

        C = (z + 1) / (z - 1)
        g1 = (C + 1) * v / 2 - (C - 1) / 2
        g2 = (C + 1) * v / 2 + (C - 1) / 2

        rnd = np.random.random()
        if rnd < P1:
            result = -C + np.random.random() * (g1 - (-C))
        elif rnd < P1 + P2:
            result = (g2 - g1) * np.random.random() + g1
        else:
            result = (C - g2) * np.random.random() + g2
        return result

    # 我的实现方法
    def encode_piecewise_mine(self, value):
        """
        Piecewise Mechanism, from paper: Collecting and Analyzing Multidimensional Data with Local Differential Privacy
        """
        C = (np.e**(self.epsilon/2)+1) / (np.e**(self.epsilon/2)-1)
        p = (np.e**self.epsilon - np.e**(self.epsilon/2)) / (2*np.e**(self.epsilon/2)+2)
        L = (C+1)/2 * value - (C-1)/2
        R = L + C - 1

        p_h = (p - p / (np.e**self.epsilon)) * (C-1)

        rnd = np.random.random()
        if rnd <= p_h:
            rnd_v = np.random.uniform(L, R)
        else:
            rnd_v = np.random.uniform(-C, C)

        return rnd_v

