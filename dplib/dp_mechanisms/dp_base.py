# -*- coding: utf-8 -*-
# @Time    : 2022-01-07 17:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
base class for differential privacy
"""
import abc


class DPBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def randomize(self, value):
        """ the randomize function """
        raise NotImplementedError

    @classmethod
    def _check_epsilon_delta(cls, epsilon, delta):
        if not (epsilon >= 0 and 0 <= delta <= 1 and epsilon+delta > 0):
            raise ValueError("the range of epsilon and delta is wrong, epsilon={}, delta={}".format(epsilon, delta))
        return float(epsilon), float(delta)

    @abc.abstractmethod
    def get_privacy_budget(self):
        """
        return the privacy budget
        """
        raise NotImplementedError
