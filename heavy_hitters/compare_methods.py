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
import heavy_hitters.k_random_response as KRR
import heavy_hitters.hadamard_response as HR


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


def get_err(true_hist, estimate_hist, method='max'):
    if method == 'max':
        return np.max(np.fabs(true_hist - estimate_hist))
    if method == 'average':
        return np.average(np.fabs(true_hist - estimate_hist))
    if method == 'l1':
        return np.sum(np.fabs(true_hist - estimate_hist))
    if method == 'l2':
        return np.sqrt(np.sum((true_hist - estimate_hist)**2))
    else:
        raise Exception("The input method is not allowed, method = ", method)


def run_example():
    config = {
        'bucket_size': 100,
        'epsilon': 1,
        'n': 1000000,
        'method': 'l1'
    }

    bucket_list, true_hist = generate_bucket(n=config['n'], bucket_size=config['bucket_size'], distribution_name='uniform')
    bucket_list = np.asarray(bucket_list)
    print("true hist = ", true_hist)

    print("\n==========>>>>> in HR")
    hr = HR.HR(bucket_size=config['bucket_size'], epsilon=config['epsilon'])
    hr_private_bucket_list = [hr.encode_item(bucket) for bucket in bucket_list]
    hr_histogram = hr.decode_histogram(private_bucket_list=hr_private_bucket_list)
    hr_error = get_err(true_hist, hr_histogram, config['method'])
    # print("HR resul", hr_histogram)
    print("HR error", hr_error)

    print("\n==========>>>>> in RAPPOR")
    rappor = RAPPOR.RAPPOR(bucket_size=config['bucket_size'], epsilon=config['epsilon'])
    rappor_private_bucket_list = [rappor.encode_item(bucket) for bucket in bucket_list]
    rappor_histogram = rappor.decode_histogram(private_bucket_list=rappor_private_bucket_list)
    rappor_error = get_err(true_hist, rappor_histogram, config['method'])
    # print("RAPPOR resul", rappor_histogram)
    print("RAPPOR error", rappor_error)

    print("\n==========>>>>> in KRR")
    krr = KRR.kRR(bucket_size=config['bucket_size'], epsilon=config['epsilon'])
    krr_private_bucket_list = [krr.encode_item(item) for item in bucket_list]
    krr_histogram = krr.decode_histogram(krr_private_bucket_list)
    krr_error = get_err(true_hist, krr_histogram, config['method'])
    # print("krr result  ", krr_histogram)
    print("krr error   ", krr_error)
    print(config)


if __name__ == '__main__':
    run_example()