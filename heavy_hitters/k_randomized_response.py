# -*- coding: utf-8 -*-
# @Time    : 2020/5/9
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : k_randomized_response.py
# @Software: PyCharm


import numpy as np
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
        self.__tf_matrix = np.full(shape=(self.k, self.k), fill_value=self.p_l)
        for i in range(self.k):
            self.__tf_matrix[i][i] = self.p_h

    def user_encode(self, bucket):
        probability_list = self.__tf_matrix[bucket]
        return np.random.choice(a=range(self.k), p=probability_list)

    def aggregate_histogram(self, private_bucket_list):
        private_hist = np.zeros(shape=self.k)
        for private_bucket in private_bucket_list:
            private_hist[private_bucket] += 1
        print("this is private_hist: ", private_hist)
        n = len(private_bucket_list)
        estimate_counts = (private_hist - n * self.p_l) / (self.p_h - self.p_l)
        return estimate_counts


def run_example():
    np.random.seed(10)
    n = 10 ** 6
    bucket_size = 20
    epsilon = 1

    print("==========>>>>> in KRR")
    krr = kRR(bucket_size=bucket_size, epsilon=epsilon)
    bucket_list, true_hist = example.generate_bucket(n=n, bucket_size=bucket_size, distribution_name='exp')
    print("this is buckets: ", bucket_list)
    print("this is true hist: ", true_hist)

    private_bucket_list = [krr.user_encode(item) for item in bucket_list]
    estimate_hist = krr.aggregate_histogram(private_bucket_list)
    print("this is estimate_hist", estimate_hist)


if __name__ == '__main__':
    run_example()



