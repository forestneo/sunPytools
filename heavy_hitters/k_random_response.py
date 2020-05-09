# -*- coding: utf-8 -*-
# @Time    : 2020/5/9
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : k_random_response.py
# @Software: PyCharm


import numpy as np
import basis.local_differential_privacy_library as ldplib
import heavy_hitters.compare_methods as example

class kRR:
    def __init__(self, bucket_size, epsilon):
        # the probability of 1->1
        # the size of buckets
        self.bucket_size = bucket_size
        self.epsilon = epsilon
        self.k = bucket_size
        self.p_h = np.e ** epsilon / (np.e ** epsilon + self.k - 1)
        self.p_l = 1 / (np.e ** epsilon + self.k - 1)

    def encode_item(self, bucket):
        if bucket >= self.bucket_size:
            raise Exception("the input domain is wrong, bucket = %d, k = %d" % (bucket, self.bucket_size))
        return ldplib.k_random_response_new(item=bucket, k=self.k, epsilon=self.epsilon)

    def decode_histogram(self, private_bucket_list):
        private_hist = np.histogram(private_bucket_list, range(self.k+1))[0]
        n = len(private_bucket_list)
        estimate_counts = (private_hist - n * self.p_l) / (self.p_h - self.p_l)
        return estimate_counts


if __name__ == '__main__':
    bucket_size = 5
    epsilon = 1

    print("==========>>>>> in KRR")

    krr = kRR(bucket_size=bucket_size, epsilon=epsilon)
    bucket_list, true_hist = example.generate_bucket(n=10000, bucket_size=bucket_size, distribution_name='uniform')
    print("this is buckets: ", bucket_list)
    print("this is true hist: ", true_hist)

    private_bucket_list = [krr.encode_item(item) for item in bucket_list]
    estimate_hist = krr.decode_histogram(private_bucket_list)
    print("this is estimate_hist", estimate_hist)



