# -*- coding: utf-8 -*-
# @Time    : 2022-01-07 17:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
The laplace mechanism for differential privacy
"""
from dp_base import DPBase
import numpy as np


class LaplaceMechanism(DPBase):
    def __init__(self, epsilon, delta=0.0, sensitivity=1):
        self.__epsilon, self.__delta = self._check_epsilon_delta(epsilon, delta)
        self.__sensitivity = sensitivity
        self.__lap_scale = sensitivity / epsilon

    def randomize(self, value):
        value = self.__check_value(value)
        return value + np.random.laplace(loc=0, scale=self.__lap_scale)

    @staticmethod
    def __check_value(value):
        if value >= 0 or value < 0:
            return value
        raise ValueError("ERR: the input value={} is invalid.".format(value))

    def get_privacy_budget(self):
        return self.__epsilon, self.__delta

    def get_sensitivity(self):
        return self.__sensitivity


def run_example():
    a = 1
    lap = LaplaceMechanism(epsilon=10, sensitivity=1)
    res = [lap.randomize(a) for _ in range(100)]
    print(np.average(res))


if __name__ == '__main__':
    run_example()
