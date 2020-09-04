# -*- coding: utf-8 -*-
# @Time    : 2020/5/5
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : rappor.py
# @Software: PyCharm
# @Function: 

import numpy as np
import heavy_hitters.compare_methods as example


class RAPPOR:
    def __init__(self, bucket_size, epsilon):
        # the probability of 1->1
        self.p = np.e ** (epsilon/2) / (np.e ** (epsilon/2) + 1)
        # the size of buckets
        self.bucket_size = bucket_size

    def user_encode(self, bucket):
        if bucket >= self.bucket_size:
            raise Exception("Error, the input domain is wrong, bucket = %d, k = %d" % (bucket, self.bucket_size))
        # onehot encoding
        private_bucket = np.zeros(self.bucket_size)
        private_bucket[bucket] = 1
        # random response
        return np.where(private_bucket == 1, np.random.binomial(1, self.p, self.bucket_size),
                        np.random.binomial(1, 1 - self.p, self.bucket_size))

    def decode_histogram(self, private_bucket_list):
        private_bucket_list = np.asarray(np.asarray(private_bucket_list))
        item_count = private_bucket_list.shape[0]
        private_counts = np.sum(private_bucket_list, axis=0)
        estimate_counts = (private_counts + item_count * self.p - item_count) / (2*self.p - 1)
        return estimate_counts


def run_example():
    bucket_size = 5
    epsilon = 1

    print("==========>>>>> in RAPPOR")
    rappor = RAPPOR(bucket_size=bucket_size, epsilon=epsilon)
    bucket_list, true_hist = example.generate_bucket(n=10000, bucket_size=bucket_size, distribution_name='uniform')
    print("this is buckets: ", bucket_list)
    print("this is true hist: ", true_hist)

    private_bucket_list = [rappor.user_encode(item) for item in bucket_list]
    estimate_hist = rappor.decode_histogram(private_bucket_list)
    print("this is estimate_hist", estimate_hist)


if __name__ == '__main__':
    run_example()