# -*- coding: utf-8 -*-
# @Time    : 2020/12/17
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : useless.py.py
# @Software: PyCharm
# @Function: 

import numpy as np

class A:
    def __init__(self, a):
        self.a = a


class B(A):
    def __init__(self, b, a=1):
        super().__init__(a)
        self.b = b
        print(self.a)


b = B(a=3, b=2)
print(b.a, b.b)
