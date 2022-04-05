# -*- coding: utf-8 -*-
# @Time    : 2022-01-07 17:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
The randomized mechanism for differential privacy
"""
from dp_base import DPBase
import numpy as np


class RandomizedResponseMechanism(DPBase):
    def __init__(self, epsilon, delta=0.0, sensitivity=1, domain=(0, 0)):
        self.__epsilon, self.__delta = self._check_epsilon_delta(epsilon, delta)
        self.__domain = domain
        self.__p = np.e**epsilon / (np.e**epsilon + 1)

    def randomize(self, value):
        value = self.__check_value(value)
        # todo

    def __check_value(self, value):
        if self.__domain[0] <= value <= self.__domain[1]:
            return value
        raise ValueError("ERR: the input value={} is not in domain={}.".format(value, self.__domain))

    def get_privacy_budget(self):
        return self.__epsilon, self.__delta


def run_example():
    a = 1
    rr = RandomizedResponseMechanism(epsilon=10)
    res = [rr.randomize(a) for _ in range(100)]


if __name__ == '__main__':
    run_example()
