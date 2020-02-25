# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 12:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

#
import numpy as np
import basis.probability_library as pl
import time

def eps2p(epsilon, n=2):
    return np.e ** epsilon / (np.e ** epsilon + n - 1)


def discretization(value, lower=0, upper=1):
    if value > upper or value < lower:
        raise Exception("the range of value is not valid in Function @Func: discretization")

    p = (value - lower) / (upper - lower)
    rnd = np.random.random()
    return upper if rnd < p else lower


def perturbation(value, perturbed_value, epsilon):
    return value if pl.is_probability(eps2p(epsilon)) else perturbed_value


def random_response_old(B, p, q=None):
    """
    random response
    :param B: can be int or np.ndarray
    :param p: Pr[1->1]
    :param q: Pr[0->1]
    :return: the perturbed bits
    """
    q = 1-p if q is None else q
    if isinstance(B, int):
        probability = p if B == 1 else q
        return np.random.binomial(n=1, p=probability)
    elif isinstance(B, np.ndarray):
        B = np.array(B)
        for i in range(len(B)):
            probability = p if B[i] == 1 else q
            B[i] = np.random.binomial(n=1, p=probability)
        return B
    else:
        raise Exception(type(B), B, p, q)


def random_response_reverse(data_list, p, q=None):
    """
    decoder for function @random_response_old
    :return:
    """

    if not isinstance(data_list, np.ndarray):
        raise Exception("the type of data is wrong, ", type(data_list))
    q = 1 - p if q is None else q
    if len(data_list.shape) == 1:
        sum_of_bits = np.sum(data_list)
        size = len(data_list)
        return (sum_of_bits - size * q) / (p - q)
    elif len(data_list.shape) == 2:
        nd_sum = np.sum(data_list, axis=0)
        size = data_list.shape[0]
        return (nd_sum - size * q) / (p - q)
    else:
        raise Exception("The shape of input data cannot be processed! ", data_list.shape)


def k_random_response(value, values, epsilon):
    """
    the k-random response
    :param value: current value
    :param values: the possible value
    :param epsilon: privacy budget
    :return:
    """
    if not isinstance(values, list):
        raise Exception("The values should be list")
    if value not in values:
        raise Exception("Errors in k-random response")
    p = np.e ** epsilon / (np.e ** epsilon + len(values) - 1)
    if np.random.random() < p:
        return value

    values.remove(value)
    return values[np.random.randint(low=0, high=len(values))]


def coin_flip(bits: np.ndarray, flip_flags: np.ndarray):
    if not (isinstance(bits, np.ndarray) or isinstance(flip_flags, np.ndarray)):
        raise Exception("Type Err: ", type(bits), type(flip_flags))
    if not bits.shape == flip_flags.shape:
        raise Exception("Length Err: ", bits.shape, flip_flags.shape)
    # the 1 in F is not to flip
    # B F B'
    # 1 1 1
    # 1 0 0
    # 0 1 0
    # 0 0 1
    return (bits + flip_flags + 1) % 2


def random_response(bits: np.ndarray, p, q=None):
    """
    :param bits: bits
    :param p: probability of 1->1
    :param q: probability of 0->1
    update: 2020.02.25
    """
    q = 1 - p if q is None else q
    if isinstance(bits, int):
        probability = p if bits == 1 else q
        return np.random.binomial(n=1, p=probability)

    if not isinstance(bits, np.ndarray):
        raise Exception("Type Err: ", type(bits))

    if len(bits.shape) != 1:
        raise Exception("Size Err: ", bits.shape)
    flip_flags = np.where(bits == 1, np.random.binomial(1, p, len(bits)), np.random.binomial(1, 1 - q, len(bits)))
    return coin_flip(bits, flip_flags)


def unary_encoding(bits: np.ndarray, epsilon):
    """
    the unary encoding, the default UE is SUE
    update: 2020.02.25
    """
    if not isinstance(bits, np.ndarray):
        raise Exception("Type Err: ", type(bits))
    if not (len(np.where(a==1)[0]) == 1 and np.sum(bits) == 1):
        raise Exception("Input Err: ", bits)
    return symmetric_unary_encoding(bits, epsilon)


def symmetric_unary_encoding(bits: np.ndarray, epsilon):
    p = eps2p(epsilon / 2) / (eps2p(epsilon / 2) + 1)
    q = 1 / (eps2p(epsilon / 2) + 1)
    return random_response(bits, p, q)


def optimized_unary_encoding(bits: np.ndarray, epsilon):

    p = 1 / 2
    q = 1 / (eps2p(epsilon) + 1)
    return random_response(bits, p, q)


def test_frequency_estimation():
    """
    this is a frequency estimation example
    """
    users = np.random.binomial(n=1, p=0.8, size=100000)
    print(users)

if __name__ == '__main__':
    test_frequency_estimation()
