# -*- coding: utf-8 -*-
# @Time    : 2022-02-07 17:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
the piecewise mechanism,
from paper "Collecting and Analyzing Multidimensional Data with Local Differential Privacy"
link: https://arxiv.org/abs/1907.00782

@ 2022.02.08 updated, add the LDPBase class
"""

from ldp_base import LDPBase
import numpy as np


class PMBase(LDPBase):
    def __init__(self, epsilon):
        self._epsilon = self._check_epsilon(epsilon)

        z = np.e ** (self._epsilon / 2)
        self._C = (z + 1) / (z - 1)

    def randomize(self, value):
        v = self._check_value(value)
        z = np.e ** (self._epsilon / 2)

        P1 = (v + 1) / (2 + 2 * z)
        P2 = z / (z + 1)
        P3 = (1 - v) / (2 + 2 * z)

        g1 = (self._C + 1) * v / 2 - (self._C - 1) / 2
        g2 = (self._C + 1) * v / 2 + (self._C - 1) / 2

        rnd = np.random.random()
        if rnd < P1:
            result = -self._C + np.random.random() * (g1 - (-self._C))
        elif rnd < P1 + P2:
            result = (g2 - g1) * np.random.random() + g1
        else:
            result = (self._C - g2) * np.random.random() + g2
        return result

    def randomize2(self, value, minor=1e-10):
        """
        此方法原理没问题，并且更加易于理解
        但是当epsilon非常大的时候（比如epsilon=100），这个方法可能出问题，问题的原因在于计算的C=1，进而导致P_h=0
        minor的作用就是防止C=1时候C-1=0，进而导致p_h=0
        """
        value = self._check_value(value)

        C = self._C
        p = (np.e ** self._epsilon - np.e ** (self._epsilon / 2)) / (2 * np.e ** (self._epsilon / 2) + 2)
        L = (C+1)/2 * value - (C-1)/2
        R = L + C - 1
        p_h = (p - p / (np.e ** self._epsilon)) * (C + minor - 1)

        rnd = np.random.random()
        if rnd <= p_h:
            rnd_v = np.random.uniform(L, R)
        else:
            rnd_v = np.random.uniform(-C, C)
        return rnd_v

    def _check_value(self, value):
        if not -1 <= value <= 1:
            raise ValueError("the input value={} is not in domain=[-1,1].".format(value))
        return value


class PiecewiseMechanism(LDPBase):
    def __init__(self, epsilon, domain):
        self._domain = domain
        self._epsilon = epsilon
        self._pm_encoder = PMBase(epsilon=epsilon)

    def _transform(self, value):
        """transform v in self.domain to v' in [-1,1]"""
        value = self._check_value(value)
        a, b = self._domain
        return (2*value - b - a) / (b - a)

    def _transform_T(self, value):
        """inverse of self._transform"""
        a, b = self._domain
        return (value * (b-a)+a+b)/2

    def randomize(self, value):
        value = self._transform(value)
        value = self._pm_encoder.randomize(value)
        value = self._transform_T(value)
        return value

    def _check_value(self, value):
        if not self._domain[0] <= value <= self._domain[1]:
            raise ValueError("the input value={} is not in domain={}".format(value, self._domain))
        return value


def myrun():
    domain = (90, 200)
    # data = np.clip(np.random.laplace(loc=100, scale=20, size=10), domain[0], domain[1])
    pm_encoder = PiecewiseMechanism(epsilon=100, domain=domain)
    a = 200
    print(pm_encoder.randomize(a))


if __name__ == '__main__':
    myrun()
