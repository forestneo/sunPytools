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


