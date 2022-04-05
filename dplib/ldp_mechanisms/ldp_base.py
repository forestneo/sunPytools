# -*- coding: utf-8 -*-
# @Time    : 2022-01-07 17:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
base class for local differential privacy
"""
import abc


class LDPBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def randomize(self, value):
        """
        the randomize function
        """
        raise NotImplementedError

    @classmethod
    def _check_epsilon(cls, epsilon):
        if not (epsilon >= 0):
            raise ValueError("ERR: the range of epsilon={} is wrong.".format(epsilon))
        return epsilon

    @abc.abstractmethod
    def _check_value(self, value):
        """
        to check if the input value is valid
        """
        raise NotImplementedError
