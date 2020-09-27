# -*- coding: utf-8 -*-
# @Time    : 2020/9/1
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm


import numpy as np
import heavy_hitters.compare_methods as example


def cosine_similarity(arr_1: np.ndarray, arr_2: np.ndarray):
    return np.dot(arr_1, arr_2) / (np.linalg.norm(arr_1) * np.linalg.norm(arr_2))


def euclidean_similarity(arr_1: np.ndarray, arr_2: np.ndarray):
    return np.sqrt(np.sum((arr_1 - arr_2) ** 2))


class SuccinctHistogram:
    def __init__(self, epsilon, d, m):
        """
        需要给定m，或者 n 和 beta
        :param epsilon:
        :param d:
        :param m:
        :param n:
        :param beta:
        """
        self.epsilon = epsilon
        self.d = d
        self.__p = np.e ** epsilon / (np.e ** epsilon + 1)

        self.onehot_matrix = np.eye(d)
        print("onehot matrix generated")

        # """ this is m in succinct histogram"""
        # gamma = np.sqrt((np.log(2*d / beta)) / (epsilon**2 * n))
        # m = np.log(d+1) * np.log(2/beta) / (gamma ** 2)
        # self.m = int(np.ceil(m))

        self.m = m

        # generate a d*m matrix phi
        self.phi = 1/np.sqrt(self.m) * np.random.choice(a=[-1, 1], size=[d, self.m])
        print("matrix phi generated!")

        self.C = (np.e**epsilon + 1) / (np.e**epsilon - 1)
        print("*"*10, " Succint Histogram initialized!")

    def user_encode(self, value):
        if not 0 <= value < self.d:
            raise Exception("Error, the input is not in the input domain, ", value)
        # onehot_arr = self.onehot_matrix[value]
        # d_x = onehot_arr.dot(self.phi)
        # print("dx = ", d_x)
        d_x = self.phi[value]
        return self.__basic_randomizer(d_x)

    def __basic_randomizer(self, x):
        j = np.random.randint(low=0, high=self.m)
        if not np.all(x == 0):
            z_j = np.random.choice([self.C * self.m * x[j], -self.C * self.m * x[j]], p=[self.__p, 1 - self.__p])
        else:
            z_j = np.random.choice([-self.C * np.sqrt(self.m), self.C * self.m])
        return j, z_j

    def FO(self, z_hat):
        f = np.zeros(shape=self.d)
        for bucket in range(self.d):
            onehot_arr = self.onehot_matrix[bucket]
            f[bucket] = np.inner(onehot_arr.dot(self.phi), z_hat)
        return f

    def PROT_FO(self, users_data):
        n = len(users_data)
        z_sum = np.zeros(shape=self.m)
        print("start encoding")
        for i in range(n):
            j, z_j = self.user_encode(users_data[i])
            z_sum[j] = z_sum[j] + z_j
        print("start decoding")
        z_hat = z_sum / n
        return self.FO(z_hat=z_hat)


def run_example():
    epsilon = 1
    n = 10 ** 6
    bucket_size = 1000
    m = 500000

    # np.random.seed(10)

    bucket_list, true_hist = example.generate_bucket(n=n, bucket_size=bucket_size, distribution_name='exp')

    true_distribution = true_hist / sum(true_hist)
    print(true_distribution[:10])
    example.draw_distribution(true_distribution)

    SH = SuccinctHistogram(epsilon=epsilon, d=bucket_size, m=m)
    estimated_hist = SH.PROT_FO(users_data=bucket_list)
    estimated_distribution = estimated_hist / sum(estimated_hist)
    example.draw_distribution(estimated_distribution)

    print(estimated_distribution[:10])


if __name__ == '__main__':
    run_example()




