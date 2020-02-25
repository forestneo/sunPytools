# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 13:31
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm


import numpy as np
from basis import local_differential_privacy_library as dp


def mean_estimation_experiment():
    # generated data
    data = np.clip(np.random.normal(loc=0.5, scale=0.2, size=[100000]), 0, 1)
    print("this is generated data\n", data)

    discretized_data = [dp.discretization(value=value, lower=0, upper=1) for value in data]
    print("this is discretized data\n", discretized_data)

    mean = np.average(data)
    print("the mean_solutions of original data is: ", mean)

    mean_d = np.average(discretized_data)
    print("the mean_solutions of discretized data is: ", mean_d)

    epsilon = 1

    # dp_data = [dp.random_response_old(B=value, p=dp.eps2p(epsilon)) for value in discretized_data]
    dp_data = [dp.random_response(bits=value, p=dp.eps2p(epsilon)) for value in discretized_data]
    est_one = dp.random_response_reverse(data_list=np.asarray(dp_data), p=dp.eps2p(epsilon))
    est_mean = est_one / len(dp_data)

    print("the estimated mean_solutions is: ", est_mean)


if __name__ == '__main__':
    mean_estimation_experiment()




