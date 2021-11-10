# -*- coding: utf-8 -*-
# @Time    : 2020/5/1
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : mdlib.py
# @Software: PyCharm
# @Function: 

import basis.sunLDP.ldplib as ldplib
import numpy as np


def remove_null_value(vl: np.ndarray):
    return vl[vl == vl]


def generate_data(mr=0.3, size=10**5):
    # generate data that belongs to [-1,1]
    data = np.random.random_sample(size=size) * 2 - 1
    # generate missing values
    mr_flag = np.random.binomial(1, p=mr, size=size)
    data[mr_flag == 1] = np.nan
    return data


def get_baseline(vl: np.ndarray):
    vl_val = remove_null_value(vl)
    return 1 - len(vl_val) / len(vl), np.average(vl_val)


class BiSampleMD:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.__p = np.e**epsilon / (np.e**epsilon + 1)

    def user_encode(self, val):
        if np.isnan(val):
            return np.random.binomial(1, p=0.5), np.random.binomial(1, p=1-self.__p)

        s = np.random.binomial(1, p=0.5) # sampling direction
        if s == 1:
            # positive sampling
            b = np.random.binomial(1, p=(np.e**self.epsilon - 1) / (np.e**self.epsilon + 1) * val / 2 + 0.5)
        else:
            # negative sampling
            b = np.random.binomial(1, p=(1 - np.e**self.epsilon) / (np.e**self.epsilon + 1) * val / 2 + 0.5)
        return s, b

    def aggregate_mean(self, p_val_lst):
        val_lst = np.asarray(p_val_lst)

        pos_lst = val_lst[val_lst[:, 0] == 1]
        neg_lst = val_lst[val_lst[:, 0] == 0]
        pos_val = pos_lst[:, 1]
        neg_val = neg_lst[:, 1]

        f_pos = 1.0 * sum(pos_val) / len(pos_val)
        f_neg = 1.0 * sum(neg_val) / len(neg_val)

        m = (f_pos - f_neg) / (f_pos + f_neg + 2*self.__p - 2)
        mr = (1 - f_pos - f_neg) / (2*self.__p - 1)
        return mr, m


def my_example():
    vl = generate_data(mr=0.3, size=10**5)
    mr, m = get_baseline(vl)
    print(vl)
    print("data size = ", len(vl))

    epsilon = 1
    bisample = BiSampleMD(epsilon=epsilon)
    p_vl_lst = [bisample.user_encode(val) for val in vl]
    est_mr, est_m = bisample.aggregate_mean(p_vl_lst)

    print("true result: mr = %.6f, m = %.6f" % (mr, m))
    print("este result: mr = %.6f, m = %.6f" % (est_mr, est_m))


if __name__ == '__main__':
    my_example()