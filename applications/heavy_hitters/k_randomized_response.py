# -*- coding: utf-8 -*-
# @Time    : 2020/5/9
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : k_randomized_response.py
# @Software: PyCharm


import numpy as np
from applications import heavy_hitters as example
import matplotlib.pyplot as plt


class GeneralizedRandomizedResponse:
    def __init__(self, bucket_size, epsilon):
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
        estimate_hist = (private_hist - len(private_bucket_list) * self.p_l) / (self.p_h - self.p_l)
        return estimate_hist

    def aggregate_histogram_by_matrix(self, private_bucket_list):
        """
        this method is to estimate the histogram by the inverse of tf_matrix
        """
        private_hist = np.zeros(shape=self.k)
        for private_bucket in private_bucket_list:
            private_hist[private_bucket] += 1
        tf_reverse = np.linalg.inv(self.__tf_matrix)
        estimated_hist = np.dot(tf_reverse, np.reshape(private_hist, newshape=(self.bucket_size, 1)))
        return np.reshape(estimated_hist, newshape=self.bucket_size)


def run_example():
    np.set_printoptions(threshold=40, linewidth=200, edgeitems=5)

    n = 10 ** 5
    bucket_size = 100
    epsilon = 1

    print("==========>>>>> in KRR")
    krr = GeneralizedRandomizedResponse(bucket_size=bucket_size, epsilon=epsilon)
    bucket_list, true_hist = example.generate_bucket(n=n, bucket_size=bucket_size, distribution_name='exp')
    print("this is buckets: ", bucket_list)
    print("this is true hist: ", true_hist)

    private_bucket_list = [krr.user_encode(item) for item in bucket_list]
    estimated_hist = krr.aggregate_histogram(private_bucket_list)
    print("this is estimate_hist", estimated_hist)

    index = range(bucket_size)
    plt.plot(index, true_hist)
    plt.plot(index, estimated_hist)
    plt.legend(['true', 'krr'])
    plt.show()


if __name__ == '__main__':
    run_example()