# -*- coding: utf-8 -*-
# @Time    : 2020/3/4
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : run_frequency_estimation.py
# @Software: PyCharm
# @Function: 

import numpy as np
import basis.sunLDP.local_differential_privacy_library as ldplib


def run(data):
    """
    this is a frequency estimation example
    """
    frequency = np.sum(data) / len(data)
    print("data volume is ", len(data))
    print("baseline frequency = ", frequency)

    epsilon = 1
    p = ldplib.eps2p(epsilon)
    perturbed_data = ldplib.random_response(bit_array=data, p=p)
    f = np.sum(perturbed_data) / len(perturbed_data)
    estimated_frequency = (f + p - 1) / (2 * p - 1)
    print("estimated frequency = ", estimated_frequency)
    print("estimation error = ", np.fabs(estimated_frequency-frequency))


if __name__ == '__main__':
    data = np.loadtxt("data.txt")
    run(data)
