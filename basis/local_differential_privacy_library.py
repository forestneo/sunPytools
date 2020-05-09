# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 12:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

#
import numpy as np


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


def k_random_response_new(item, k, epsilon):
    if not item < k:
        raise Exception("the input domain is wrong, item = %d, k = %d." % (item, k))
    p_l = 1 / (np.e ** epsilon + k - 1)
    p_h = np.e ** epsilon / (np.e ** epsilon + k - 1)
    respond_probability = np.full(shape=k, fill_value=p_l)
    respond_probability[item] = p_h
    perturbed_item = np.random.choice(a=range(k), p=respond_probability)
    return perturbed_item


def random_response(bit_array: np.ndarray, p, q=None):
    """
    :param bit_array:
    :param p: probability of 1->1
    :param q: probability of 0->1
    update: 2020.03.06
    :return: 
    """
    q = 1-p if q is None else q
    if isinstance(bit_array, int):
        probability = p if bit_array == 1 else q
        return np.random.binomial(n=1, p=probability)
    return np.where(bit_array == 1, np.random.binomial(1, p, len(bit_array)), np.random.binomial(1, q, len(bit_array)))


def unary_encoding(bit_array: np.ndarray, epsilon):
    """
    the unary encoding, the default UE is SUE
    update: 2020.02.25
    """
    if not isinstance(bit_array, np.ndarray):
        raise Exception("Type Err: ", type(bit_array))
    return symmetric_unary_encoding(bit_array, epsilon)


def symmetric_unary_encoding(bit_array: np.ndarray, epsilon):
    p = eps2p(epsilon / 2) / (eps2p(epsilon / 2) + 1)
    q = 1 / (eps2p(epsilon / 2) + 1)
    return random_response(bit_array, p, q)


def optimized_unary_encoding(bit_array: np.ndarray, epsilon):
    p = 1 / 2
    q = 1 / (eps2p(epsilon) + 1)
    return random_response(bit_array, p, q)


if __name__ == '__main__':
    pass
