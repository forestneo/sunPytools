# -*- coding: utf-8 -*-
# @Time    : 2021/3/3
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : bv_library.py
# @Software: PyCharm
# @Function: 

import numpy as np
import basis.sunLDP.ldplib as ldplib
'''
The bit vector mechanism
'''

class BitVector:
    def __init__(self, random_values: np.ndarray, t: float, data_range: list):
        self.r = random_values
        self.s = len(random_values)
        self.t = t

        self.L = data_range[0]
        self.U = data_range[1]
        self.u = self.U - self.L

    def encode(self, v):
        bv = np.zeros(shape=self.s, dtype=int)
        for i in range(self.s):
            if self.r[i] - t <= v <= self.r[i] + self.t:
                bv[i] = 1
        return bv

    def estimate_distance(self, private_data1: np.ndarray, private_data2: np.ndarray):
        d_h = np.sum(np.fabs(private_data1 - private_data2))
        d_e = d_h * self.u / (2 * self.s)
        return d_e


class RandomBitVector:
    def __init__(self, random_values: np.ndarray, data_range: list, p=1.0):
        self.s = len(random_values)
        self.r = random_values
        self.L = data_range[0]
        self.U = data_range[1]
        self.u = self.U - self.L
        self.p = p

    def encode(self, v):
        bv = np.where(v >= self.r, 1, 0)
        return ldplib.random_response(bit_array=bv, p=(self.p+1)/2)

    def estimate_distance(self, private_data1, private_data2):
        d_h = np.sum(np.fabs(private_data1 - private_data2))
        d_e = (d_h / self.s - ((1-self.p**2)/2)) * self.u / self.p**2
        return d_e


class PMRandomizedBitVector:
    def __init__(self, random_values: np.ndarray, data_range: list, triangle=1.0, epsilon=0.0):
        self.triangle = triangle
        self.epsilon = epsilon
        self.s = len(random_values)
        self.r = random_values
        self.L = data_range[0]
        self.U = data_range[1]
        self.u = self.U - self.L
        self.RBV = RandomBitVector(random_values=random_values, data_range=data_range, p=1)

    def encode(self, v):
        v = v + np.random.laplace(loc=0, scale=self.triangle/self.epsilon)
        return self.RBV.encode(v)

    def estimate_distance(self, private_data1, private_data2):
        return self.RBV.estimate_distance(private_data1, private_data2)


if __name__ == '__main__':
    length = 10000
    np.random.seed(0)
    data_range = [-10, 20]
    random_values = np.random.uniform(low=data_range[0], high=data_range[1], size=length)
    print(random_values)
    print(min(random_values), max(random_values))
    t = 4

    BV = BitVector(random_values=random_values, t=t, data_range=data_range)
    RBV = RandomBitVector(random_values=random_values, data_range=data_range, p=0.9)
    PMRBV = PMRandomizedBitVector(random_values=random_values, data_range=data_range, triangle=1, epsilon=10)
    method = BV

    data_pair = [
        [1, 3],
        [2, 3],
        [4, 6],
        [4, 8],
    ]

    for a, b in data_pair:
        p_a = method.encode(a)
        p_b = method.encode(b)
        de_true = np.fabs(a - b)
        de_esti = method.estimate_distance(p_a, p_b)
        print(a, b, de_true, de_esti)

    pass
