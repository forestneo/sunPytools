#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/16 12:41
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Site    : forestneo.com
# @Software: PyCharm

from basis import local_differential_privacy_library as dp
import numpy as np


def my_test_for_random_response_pq():
    """
    To test following function @random_response_pq and function @random_response_pq_reverse
    :return:
    """
    original_data_list = np.random.binomial(1, 0.8, size=[1000000]).reshape([100000,10])
    # print(original_data_list)

    original_sum = np.sum(original_data_list, axis=0)
    print(original_sum)

    p, q = 0.9, 0.1
    perturbed_data_list = [dp.random_response_old(bits=original_data_list[i], p=p, q=q) for i in range(len(original_data_list))]
    perturbed_sum = np.sum(np.asarray(perturbed_data_list), axis=0)
    print(perturbed_sum)

    adjust_sum = dp.random_response_reverse(data_list=np.asarray(perturbed_data_list), p=p, q=q)
    print(adjust_sum)


if __name__ == '__main__':
    my_test_for_random_response_pq()
    pass