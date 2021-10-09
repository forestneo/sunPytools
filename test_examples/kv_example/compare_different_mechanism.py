# -*- coding: utf-8 -*-
# @Time    : 2020/3/18
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : compare_different_mechanism.py
# @Software: PyCharm
# @Function: 

import numpy as np
import basis.sunLDP.kvlib as kvlib


def generate_kvt(n=10**6, d=100):
    """
    随机产生 kvtable
    """
    flist = np.arange(1, d) / d
    kvt = np.zeros(shape=[n, d-1, 2])
    for i in range(len(flist)):
        klist = np.random.binomial(n=1, p=flist[i], size=n)
        vlist = np.random.normal(loc=flist[i], scale=0.1, size=n).clip(-1, 1)
        kvt[:, i, 0] = klist
        kvt[:, i, 1] = vlist
    return kvt


def experiment_by_privkv(kvt, epsilon_k, epsilon_v):
    pass


def experiment_by_se(kvt, epsilon):
    pass




if __name__ == '__main__':
    kvt = generate_kvt(n=1000, d=3)
    print(kvt.shape)
    f_base, m_base = kvlib.kvt_get_baseline(kvt)
    print(f_base, m_base)