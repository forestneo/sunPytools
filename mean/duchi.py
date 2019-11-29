#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 11:08
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm


from basis import local_differential_privacy_library as dp
import numpy as np
import matplotlib.pyplot as plt


def encode_duchi(value, epsilon):
    value = dp.discretization(value=value, lower=-1, upper=1)
    value = dp.perturbation(value=value, perturbed_value=-value, epsilon=epsilon)
    value = (np.e**epsilon+1)/(np.e**epsilon-1) * value
    return value


def decode_duchi(value_list, epsilon):
    return np.average(value_list)


