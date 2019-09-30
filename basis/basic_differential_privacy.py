# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 12:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

#
import numpy as np


def epsilon2probability(epsilon, n=2):
    return np.e ** epsilon / (np.e ** epsilon + n - 1)


def discretization(value, lower=0, upper=1):
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


def random_response(data, p, q=None):
    """
    random response
    :param data: can be int or np.ndarray
    :param p: Pr[1->1]
    :param q: Pr[0->1]
    :return: the perturbed bits
    """
    q = 1-p if q is None else q
    if isinstance(data, int):
        probability = p if data == 1 else q
        return np.random.binomial(n=1, p=probability)
    elif isinstance(data, np.ndarray):
        for i in range(len(data)):
            probability = p if data[i] == 1 else q
            data[i] = np.random.binomial(n=1, p=probability)
        return data
    else:
        raise Exception(type(data), data, p, q)


def random_response_reverse(data_list, p, q=None):
    """
    decoder for function @random_response_pq
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


if __name__ == '__main__':
    # a = np.asarray([1, 1, 1, 0, 0, 1, 0])
    # print(random_response_pq(bits=a, probability_p=1, probability_q=0.9))
    original_data = np.random.binomial(n=1, p=0.6, size=1000000).reshape(100000, 10)
    print("original sum: ", np.sum(original_data, axis=0))
    pp = 0.8
    pq = 0.2
    perturbed_data = np.asarray([random_response(data=original_data[i], p=pp, q=pq) for i in range(original_data.shape[0])])
    print("estimated sum: ", random_response_reverse(data_list=perturbed_data, p=pp, q=pq))
