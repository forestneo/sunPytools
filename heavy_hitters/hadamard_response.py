# -*- coding: utf-8 -*-
# @Time    : 2020/5/9
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : hadamard_response.py
# @Software: PyCharm
# @Function: 

import numpy as np
import heavy_hitters.compare_methods as example


class HR:
    def __init__(self, bucket_size, epsilon):
        self.epsilon = epsilon
        # the size of buckets
        self.bucket_size = bucket_size
        # this is the K in paper
        self.private_bucket_size = int(2 ** np.ceil(np.log2(bucket_size+1)))
        self.K = self.private_bucket_size
        self.s = int(self.K / 2)

        # the probability
        self.__ph = np.e ** epsilon / (self.s * np.e ** epsilon + self.K - self.s)
        self.__pl = 1.0 / (self.s * np.e ** epsilon + self.K - self.s)

        # Generating the hadamard matrix
        self.__hadamard_matrix = np.array([1])
        for i in range(int(np.log2(self.K))):
            a = np.hstack([self.__hadamard_matrix, self.__hadamard_matrix])
            b = np.hstack([self.__hadamard_matrix, -self.__hadamard_matrix])
            self.__hadamard_matrix = np.vstack([a, b])

        # to store the output items together with corresponding probability, the shape is k*K
        self.probability_matrix = np.copy(self.__hadamard_matrix)[1:, :]
        self.probability_matrix = np.where(self.probability_matrix == 1, self.__ph, self.__pl)

    def user_encode(self, bucket):
        if bucket >= self.bucket_size:
            raise Exception("the input domain is wrong, bucket = %d, k = %d" % (bucket, self.bucket_size))
        a = range(self.K)
        p = self.probability_matrix[bucket]
        encode_item = np.random.choice(a=a, p=p)
        return encode_item

    def get_Cx(self, bucket):
        hadamard_line = self.__hadamard_matrix[bucket + 1]
        Cx = np.where(hadamard_line == 1)
        return Cx[0]

    def aggregate_histogram(self, private_bucket_list):
        private_hist = np.histogram(private_bucket_list, bins=range(self.private_bucket_size + 1))[0]
        hist = np.zeros(shape=self.bucket_size)
        for i in range(self.bucket_size):
            count = 0
            cx = np.where(self.__hadamard_matrix[i + 1] == 1)[0]
            for index in cx:
                count += private_hist[index]
            hist[i] = count

        n = len(private_bucket_list)
        estimate_hist = 2.0 * (np.e**self.epsilon + 1) / (np.e**self.epsilon - 1) * (hist - n / 2)
        return estimate_hist


def run_example():
    bucket_size = 4
    epsilon = 1
    n = 1000000

    # np.random.seed(10)
    hr = HR(bucket_size=bucket_size, epsilon=epsilon)

    bucket_list, true_hist = example.generate_bucket(n=n, bucket_size=bucket_size, distribution_name='uniform')
    print("this is buckets: ", bucket_list)
    print("this is true hist: ", true_hist)

    print("==========>>>>> in KRR")
    private_bucket_list = [hr.user_encode(item) for item in bucket_list]
    print("this is private buckets: ", private_bucket_list)
    estimate_hist = hr.aggregate_histogram(private_bucket_list)
    print("this is estimate_hist", estimate_hist)


if __name__ == '__main__':
    run_example()
