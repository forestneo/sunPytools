# -*- coding: utf-8 -*-
# @Time    : 2021/3/26
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : useless.py
# @Software: PyCharm
# @Function: 
import numpy as np

eps = 2
s = 1000
a = np.e**eps / (np.e**eps + 1)
b = 1 / (np.e**eps + 1)
delta = a**s - np.e**eps * b**s
print("s = ", s)
print("a = ", a)
print("b = ", b)
print(delta)
