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


def random_response_basic(bit, epsilon):
    if bit not in [0, 1]:
        raise Exception("The input value is not in [0, 1] @Func: random_response.")
    return perturbation(value=bit, perturbed_value=1 - bit, epsilon=epsilon)


def random_response_pq(bits, probability_p, probability_q):
    """
    This is the generalized version of random response. When p+q=1, this mechanism turns to be the basic random response.
    See this paper: Locally Differentially Private Protocols for Frequency Estimation
    :param bits: the original data.
    :param probability_p: the probability of 1->1
    :param probability_q: the probability of 0->1
    :return: the perturbed bis
    """
    if not isinstance(bits, np.ndarray):
        raise Exception("the input type is not illegal @Func: random_response_pq.")
    res = np.zeros([len(bits)])
    for i in range(len(bits)):
        if bits[i] == 1:
            flag = np.random.binomial(n=1, p=probability_p)
            res[i] = flag
        else:
            flag = np.random.binomial(n=1, p=probability_q)
            res[i] = flag
    # todo: this version is currently right, but need to optimized
    return res


def random_response_pq_reverse(sum_of_bits, num_of_records, probability_p, probability_q):
    """
    decoder for function @random_response_pq
    :param sum_of_bits:
    :param num_of_records:
    :param probability_p: the probability of 1->1
    :param probability_q: the probability of 0->1
    :return:
    """
    return (sum_of_bits - num_of_records * probability_q) / (probability_p - probability_q)


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


def random_response_adjust(sum, N, epsilon):
    """
    对random response的结果进行校正
    :param sum: 收到数据中1的个数
    :param N: 总的数据个数
    :return: 实际中1的个数
    """
    p = epsilon2probability(epsilon)
    return (sum + p*N - N) / (2*p - 1)


def my_test_for_random_response_pq():
    """
    To test following function @random_response_pq and function @random_response_pq_reverse
    :return:
    """
    original_data_list = np.random.binomial(1, 0.8, size=[1000000]).reshape([100000,10])
    # print(original_data_list)

    original_sum = np.sum(original_data_list, axis=0)
    print(original_sum)

    p, q = 0.8, 0.3
    perturbed_data_list = [random_response_pq(bits=original_data_list[i], probability_p=p, probability_q=q) for i in range(len(original_data_list))]
    perturbed_sum = np.sum(np.asarray(perturbed_data_list), axis=0)
    print(perturbed_sum)

    adjust_sum = random_response_pq_reverse(perturbed_sum, len(original_data_list), p, q)
    print(adjust_sum)


if __name__ == '__main__':
    my_test_for_random_response_pq()
    pass




