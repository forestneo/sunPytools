# -*- coding: utf-8 -*-
# @Time    : 2020/12/17
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : useless.py.py
# @Software: PyCharm
# @Function: 

import numpy as np


if __name__ == '__main__':
    a = np.zeros(shape=(12, 3))
    for i in range(12):
        a[i] = i
    # print(a)

    print(a.shape)
    b = np.resize(a, (-3, 2, a.shape[1]))
    # print(b)
    a.resize((-1, 2, a.shape[1]))
    print(a.shape)
    # print(b.shape)
    # c = np.reshape(a, (-5, 2, a.shape[1]))
    # # print(c)
    # print(c.shape)

