# -*- coding: utf-8 -*-
# @Time    : 2020/5/5
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : compare_methods.py
# @Software: PyCharm
# @Function:

import numpy as np
from applications import heavy_hitters as KRR, heavy_hitters as HR
import matplotlib.pyplot as plt


def generate_distribution(distribution_name, domain):
    if distribution_name == "uniform":
        return np.full(shape=domain, fill_value=1.0 / domain)
    elif distribution_name == "gauss":
        u = domain / 2
        sigma = domain / 6
        x = np.arange(1, domain+1)
        fx = 1 / (np.sqrt(2*np.pi) * sigma) * np.e**(- (x-u)**2 / (2 * sigma**2))
        return fx / sum(fx)
    elif distribution_name == "exp":
        lmda = 2
        prob_list = np.array([lmda * np.e**(-lmda * x) for x in np.arange(1, domain+1)/10])
        return prob_list / sum(prob_list)
    else:
        raise Exception("the distribution is not contained")


def generate_bucket(n, bucket_size, distribution_name):
    distribution = generate_distribution(distribution_name, domain=bucket_size)
    bucket_list = np.random.choice(range(bucket_size), n, p=distribution)
    hist = np.histogram(bucket_list, bins=range(bucket_size+1))
    return bucket_list, hist[0]


def draw_distribution(distribution):
    index = np.arange(len(distribution))
    plt.plot(index, distribution)
    plt.show()


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
        'error_method': 'l1'
    }

    bucket_list, true_hist = generate_bucket(n=config['n'], bucket_size=config['bucket_size'], distribution_name='uniform')
    bucket_list = np.asarray(bucket_list)
    print("true hist = ", true_hist)

    print("\n==========>>>>> in HR")
    hr = HR.HR(bucket_size=config['bucket_size'], epsilon=config['epsilon'])
    hr_private_bucket_list = [hr.user_encode(bucket) for bucket in bucket_list]
    hr_histogram = hr.aggregate_histogram(private_bucket_list=hr_private_bucket_list)
    hr_error = get_err(true_hist, hr_histogram, config['error_method'])
    # print("HR resul", hr_histogram)
    print("HR error", hr_error)

    print("\n==========>>>>> in RAPPOR")
    rappor = rappor.RAPPOR(bucket_size=config['bucket_size'], epsilon=config['epsilon'])
    rappor_private_bucket_list = [rappor.user_encode(bucket) for bucket in bucket_list]
    rappor_histogram = rappor.aggregate_histogram(private_bucket_list=rappor_private_bucket_list)
    rappor_error = get_err(true_hist, rappor_histogram, config['error_method'])
    # print("RAPPOR resul", rappor_histogram)
    print("RAPPOR error", rappor_error)

    print("\n==========>>>>> in KRR")
    krr = KRR.GeneralizedRandomizedResponse(bucket_size=config['bucket_size'], epsilon=config['epsilon'])
    krr_private_bucket_list = [krr.user_encode(item) for item in bucket_list]
    krr_histogram = krr.aggregate_histogram(krr_private_bucket_list)
    krr_error = get_err(true_hist, krr_histogram, config['error_method'])
    # print("krr result  ", krr_histogram)
    print("krr error   ", krr_error)
    print(config)


if __name__ == '__main__':
    # run_example()
    dist = generate_distribution(distribution_name='exp', domain=20)
    print(dist)
    draw_distribution(dist)
