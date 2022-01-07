# -*- coding: utf-8 -*-
# @Time    : 2022-01-07 17:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

import numpy as np


class laplace:
    def __init__(self, epsilon, sensitivity):
        self.__epsilon = epsilon
        self.__sensitivity = sensitivity
        self.__lap_scale = sensitivity / epsilon

    def laplace(self, query_result: float) -> float:
        return query_result + np.random.laplace(loc=0, scale=self.__lap_scale)


def run_example():
    a = 1
    lap = laplace(epsilon=10, sensitivity=1)
    res = [lap.laplace(a) for _ in range(100)]
    print(np.average(res))


if __name__ == '__main__':
    run_example()
