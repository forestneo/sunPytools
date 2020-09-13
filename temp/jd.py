# -*- coding: utf-8 -*-
# @Time    : 2020/9/11
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

import numpy as np

# 未优化版本
def f(w, h, t, top):
    if w * h == t:
        return 0
    # 折不到了
    if w * h < t:
        return top

    # 遍历当前所有可能
    f_list = []
    for _w in range(1, w):
        f_list.append(f(w-_w, h, t, top))
    for _h in range(1, h):
        f_list.append(f(w, h-_h, t, top))
    return min(f_list) + 1


w = 4
h = 2
top = w * h
