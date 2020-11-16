# -*- coding: utf-8 -*-
# @Time    : 2020/11/2
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : marginal_release_ldp.py
# @Software: PyCharm
# @Function: 

import numpy as np
import basis.local_differential_privacy_library as ldplib
np.set_printoptions(precision=2, linewidth=200)


class MGR_OH:
    """
    MarGinal Release with One-Hot Encoding
    """
    @staticmethod
    def encode(item, epsilon):
        p_h = np.e ** epsilon / (np.e ** epsilon + 2)
        p_l = 1 / (np.e ** epsilon + 2)
        ret_res = np.array([-1, 0, 1])
        probability = np.where(ret_res == item, p_h, p_l)
        return np.random.choice(a=ret_res, p=probability)

    @staticmethod
    def encode_pair(item_pair, epsilon):
        return [MGR_OH.encode(item=item_pair[0], epsilon=epsilon / 2), MGR_OH.encode(item=item_pair[1], epsilon=epsilon / 2)]

    @staticmethod
    def encode_pair_by_onehot(item_pair, epsilon):
        index = int((item_pair[0]+1) * item_pair[1]+1)
        arr = np.zeros(shape=9)
        arr[index] = 1
        return ldplib.random_response(bit_array=arr, p=ldplib.eps2p(epsilon=epsilon/2))

    @staticmethod
    def encode_mg(item_pair, epsilon):
        arr = np.zeros(shape=4)
        if item_pair[0] in [0, 1] and item_pair[1] in [0, 1]:
            arr[2*item_pair[0] + item_pair[1]] = 1
        return ldplib.random_response(bit_array=arr, p=ldplib.eps2p(epsilon=epsilon/2))

    @staticmethod
    def constructing_transfer_matrix(epsilon):
        p_high = np.e ** epsilon / (np.e ** epsilon + 2)
        p_low = 1 / (np.e ** epsilon + 2)

        p_h = p_high * p_high
        p_m = p_high * p_low
        p_l = p_low * p_low

        tf = np.full(shape=(9, 9), fill_value=p_l)
        for i in range(9):
            tf[i][i] = p_h

        middle_list = [
            [1, 2, 3, 6],
            [0, 2, 4, 7],
            [0, 1, 5, 8],
            [0, 4, 5, 6],
            [1, 3, 5, 7],
            [2, 3, 4, 8],
            [0, 3, 7, 8],
            [1, 4, 6, 8],
            [2, 5, 6, 7]
        ]
        for i, lst in enumerate(middle_list):
            for value in lst:
                tf[i][value] = p_m
        return tf

    @staticmethod
    def state_count(data_table):
        cnt_table = np.zeros(shape=(3, 3))
        for record in data_table:
            cnt_table[record[0] + 1][record[1] + 1] = cnt_table[record[0] + 1][record[1] + 1] + 1
        return cnt_table

    @staticmethod
    def margins(cnt_table):
        if not cnt_table.shape == (3, 3):
            raise Exception("The shape of cnt_table is wrong: ", cnt_table.shape)
        s = np.sum(cnt_table, axis=1)
        for i in range(cnt_table.shape[0]):
            cnt_table[i] = cnt_table[i] / s[i]
        return cnt_table

    @staticmethod
    def state_count_estimating(private_count, epsilon):
        tf = MGR_OH.constructing_transfer_matrix(epsilon=epsilon / 2)
        tf_r = np.linalg.inv(tf)
        estimate_cnt = np.dot(private_count, tf_r)
        return estimate_cnt


def generate_data(size=10000, col=2):
    a = np.random.choice(a=[-1, 0, 1], p=[0.1, 0.4, 0.5], size=(size, col))
    print(a)
    np.savetxt("data.txt", a, fmt='%d')


def run_tst():
    data_table = np.loadtxt("data.txt", dtype=int)
    print("input data.shape = ", data_table.shape)
    counts = MGR_OH.state_count(data_table)
    print("this is the true count: ", counts.flatten())
    mg_true = MGR_OH.margins(counts.reshape((3, 3)))
    print("this is the true maginal: \n", mg_true)

    epsilon = 20
    print("epsilon = ", epsilon)
    private_data_table = [MGR_OH.encode_pair(item_pair, epsilon) for item_pair in data_table]
    private_count = MGR_OH.state_count(private_data_table)
    private_counts = MGR_OH.state_count_estimating(private_data_table, epsilon)
    print("this is the private count: ", private_counts.flatten())
    print("this is the estimate maginal: \n", )


if __name__ == '__main__':
    # generate_data(size=100000, col=2)
    run_tst()

    # epsilon = 2
    # table1 = np.array([[1024,  4067,  4936],
    #           [3993, 16001, 20150],
    #           [4954, 19917, 24958]])
    # table2 = np.array([[6222, 8795, 9908],
    #           [9063, 12588, 13995],
    #           [9774, 14221, 15434]])
    # cnt1 = table1.flatten()
    # cnt2 = table2.flatten()
    # print(cnt1, cnt2)
    #
    # tf = MGR.constructing_transfer_matrix(epsilon=epsilon/2)
    # print(np.dot(cnt1, tf))
    # print(cnt2)


