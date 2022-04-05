# -*- coding: utf-8 -*-
# @Time    : 2021-10-09 10:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
@ 2021.10.09 整合了之前的 Duchi 方法和 PM 方法
@ 2021.11.22 添加Laplace机制
@ 2021.12.31 整合统一接口ValueEncoder
"""

import numpy as np
import dplib.ldp_mechanisms.ldplib as ldplib


class Duchi:
    def __init__(self, epsilon):
        self.__epsilon = epsilon
        self.__C = (np.e ** epsilon + 1) / (np.e ** epsilon - 1)

    def encode(self, v):
        value = ldplib.discretization(value=v, lower=-1, upper=1)
        value = ldplib.perturbation(value=value, perturbed_value=-value, epsilon=self.__epsilon)
        return self.__C * value


class PiecewiseMechanism:
    def __init__(self, epsilon):
        self.__epsilon = epsilon

    def encode_author(self, v):
        """
        Piecewise Mechanism, from paper: Collecting and Analyzing Multidimensional Data with Local Differential Privacy
        """
        z = np.e ** (self.__epsilon / 2)
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
        C = (np.e ** (self.__epsilon / 2) + 1) / (np.e ** (self.__epsilon / 2) - 1)
        p = (np.e ** self.__epsilon - np.e ** (self.__epsilon / 2)) / (2 * np.e ** (self.__epsilon / 2) + 2)
        L = (C+1)/2 * value - (C-1)/2
        R = L + C - 1

        p_h = (p - p / (np.e ** self.__epsilon)) * (C - 1)

        rnd = np.random.random()
        if rnd <= p_h:
            rnd_v = np.random.uniform(L, R)
        else:
            rnd_v = np.random.uniform(-C, C)
        return rnd_v


class Laplace:
    def __init__(self, epsilon):
        self.__epsilon = epsilon
        self.__laplace_scale = 2 / self.__epsilon

    def encode(self, v):
        return v + np.random.laplace(loc=0, scale=self.__laplace_scale)


class ValueEncoder:
    """
    整合的统一接口，后面有其他新方法，都可以调用这个接口：
    @method: 编码方法
    @parameters_dict: 对应编码的参数，用字典表示，比如
    如：encoder = ValueEncoder(method='duchi', parameters_dict={'epsilon':1})，表示用duchi方法，隐私预算为1
    """
    def __init__(self, method, parameters_dict):
        self.method = None
        self.parameters_dict = parameters_dict
        if str.lower(method) == 'laplace':
            self.method = Laplace(self.parameters_dict['epsilon'])
        elif str.lower(method) == 'duchi':
            self.method = Duchi(self.parameters_dict['epsilon'])
        elif str.lower(method) == 'piecewise':
            self.method = PiecewiseMechanism(self.parameters_dict['epsilon'])
        else:
            raise Exception("ERR, method = %s not supported!" % str.lower(method))

    def encode(self, v):
        if v > 1 or v < -1:
            raise Exception("ERR, input range error, v = %.2f" % v)
        return self.method.encode(v)


if __name__ == '__main__':
    data = np.clip(np.random.normal(loc=0.2, scale=0.3, size=10**3), a_min=-1, a_max=1)
    encoder = ValueEncoder(method='duchi', parameters_dict={'epsilon': 5})
    encoded_data = [encoder.encode(v) for v in data]
    print(np.average(data), np.average(encoded_data))
