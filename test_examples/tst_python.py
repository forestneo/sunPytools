# -*- coding: utf-8 -*-
# @Time    : 2020/3/6
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : tst_python.py
# @Software: PyCharm
# @Function: 

import numpy as np

a = np.asarray([1,0,1,1,0,0])
b = np.asarray([1,2,3,4,5,6])
c = np.asarray([11,12,13,14,15,16])
c = np.where(a==1, b, c)
print(c)


np.random.la