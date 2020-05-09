# -*- coding: utf-8 -*-
# @Time    : 2020/5/5
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : compare_methods.py
# @Software: PyCharm
# @Function:

import numpy as np
import heavy_hitters.rappor as RAPPOR


def generate_distribution(distribution_name, length):
    if distribution_name == "uniform":
        return np.full(shape=length, fill_value=1.0/length)
    elif distribution_name == "gauss":
        prob_list = [0]
        return prob_list
    else:
        raise Exception("the distribution is not contained")


def generate_bucket(n, bucket_size, distribution_name):
    distribution = generate_distribution(distribution_name, length=bucket_size)
    bucket_list = np.random.choice(range(bucket_size), n, p=distribution)
    hist = np.histogram(bucket_list, bins=range(bucket_size+1))
    return bucket_list, hist[0]


def run_example():
    bucket_size = 5
    bucket_list, true_hist = generate_bucket(n=100, bucket_size=bucket_size, distribution_name='uniform')
    bucket_list = np.asarray(bucket_list)
    print(np.asarray(bucket_list))
    print("true hist = ", true_hist)

    epsilon = 1
    rappor = RAPPOR.RAPPOR(bucket_size=bucket_size, epsilon=epsilon)
    private_bucket_list = [rappor.encode_item(bucket) for bucket in bucket_list]
    rappor_histogram = rappor.decode_histogram(private_bucket_list=private_bucket_list)
    print(rappor_histogram)
    print(sum(rappor_histogram))

if __name__ == '__main__':
    run_example()