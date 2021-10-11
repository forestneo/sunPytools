# -*- coding: utf-8 -*-
# @Time    : 2021-10-09 10:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
@ 2021.10.09 整合了之前的 Duchi 方法和 PM 方法
"""

import numpy as np
import basis.sunLDP.ldplib as ldplib


class Duchi:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.C = (np.e**epsilon+1)/(np.e**epsilon-1)

    def encode(self, v):
        if not -1 <= v <= 1:
            raise Exception("Error, The input domain is [-1, 1], while the input is ", v)
        value = ldplib.discretization(value=v, lower=-1, upper=1)
        value = ldplib.perturbation(value=value, perturbed_value=-value, epsilon=self.epsilon)
        return self.C * value


class PiecewiseMechanism:
    def __init__(self, epsilon):
        self.epsilon = epsilon

    def encode_author(self, v):
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
    def encode(self, value):
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


if __name__ == '__main__':
    print("hello")