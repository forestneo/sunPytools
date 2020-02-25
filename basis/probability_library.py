# -*- coding: utf-8 -*-
# @Time    : 2020/2/2
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : probability_library.py
# @Software: PyCharm
# @Function: 

import numpy as np


def is_probability(p):
    return bool(np.random.binomial(1, p))


def hit_probability(p_list: np.ndarray):
    '''
    :param p_list: a list of probability
    :return: the index
    for example, pl = [0.1, 0.7, 0.2]
    then we return 0 with probability 0.1, return 1 with probability 0.7
    '''
    rnd = np.random.random()
    for index in range(len(p_list)):
        if rnd < np.sum(p_list[0:index + 1]):
            return index
    raise Exception("Err: ", rnd, p_list)


if __name__ == '__main__':
    pass
