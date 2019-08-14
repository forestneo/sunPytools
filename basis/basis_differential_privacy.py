# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 12:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

#
import numpy as np


def epsilon2probability(epsilon, n=2):
    return np.e ** epsilon / (np.e ** epsilon + n - 1)


def discretization(value, lower, upper):
    """discretiza values
    :param value: value that needs to be discretized
    :param lower, the lower bound of discretized value
    :param upper: the upper bound of discretized value
    :return: the discretized value
    """
    if value > upper or value < lower:
        raise Exception("the range of value is not valid in Function @Func: discretization")

    p = (value - lower) / (upper - lower)
    rnd = np.random.random()
    return upper if rnd < p else lower


def perturbation(value, perturbed_value, epsilon):
    """
    perturbation, (random response is a kind of perturbation)
    :param value: the original value
    :param perturbed_value: the perturbed value
    :param epsilon: privacy budget
    :return: dp version of perturbation
    """
    p = epsilon2probability(epsilon)
    rnd = np.random.random()
    return value if rnd < p else perturbed_value


def random_response(value, epsilon):
    if value not in [0, 1]:
        raise Exception("The input value is not in [0, 1] @Func: random_response")
    return perturbation(value=value, perturbed_value=1-value, epsilon=epsilon)


def random_response_adjust(sum, N, epsilon):
    """
    对random response的结果进行校正
    :param sum: 收到数据中1的个数
    :param N: 总的数据个数
    :return: 实际中1的个数
    """
    p = epsilon2probability(epsilon)
    return (sum + p*N - N) / (2*p - 1)


def coin_flip(bits, epsilon):
    """
    the coin flip process for bit array, it is random response with length = len(bits).
    :param bits: the original data
    :param epsilon: privacy budget
    :return: the perturbed data
    example, bits = [1,1,0,0], flags = [0,1,0,1], res = [0,1,1,0]
    """
    flags = np.random.binomial(n=1, p=epsilon2probability(epsilon), size=len(bits))
    res = 1 - (bits + flags) % 2
    return res


if __name__ == '__main__':
    pass




