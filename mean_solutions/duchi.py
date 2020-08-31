#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/26 11:08
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm


from basis import local_differential_privacy_library as ldplib
import numpy as np
import matplotlib.pyplot as plt


class Duchi:
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.C = (np.e**epsilon+1)/(np.e**epsilon-1)

    def encode(self, v):
        if not -1 <= v <= 1:
            raise Exception("The input domain is [-1, 1], while the input is ", v)
        value = ldplib.discretization(value=v, lower=-1, upper=1)
        value = ldplib.perturbation(value=value, perturbed_value=-value, epsilon=self.epsilon)
        return self.C * value


def encode_duchi(value, epsilon):
    value = ldplib.discretization(value=value, lower=-1, upper=1)
    value = ldplib.perturbation(value=value, perturbed_value=-value, epsilon=epsilon)
    value = (np.e**epsilon+1)/(np.e**epsilon-1) * value
    return value


def decode_duchi(value_list, epsilon):
    return np.average(value_list)


