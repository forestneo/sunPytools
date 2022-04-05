# -*- coding: utf-8 -*-
# @Time    : 2022-02-07 17:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
the generalized randomized response mechanism, also known as krr
@ 2022.02.08 updated, add the LDPBase class
"""

from ldp_base import LDPBase
import numpy as np


class GRR(LDPBase):
    def __init__(self, epsilon, domain):
        self._check_epsilon(epsilon)
        self._epsilon = epsilon

        # domain 表示元素所在的空间，比如 domain = ['apple', 'banana', 'pear']
        self._domain = domain
        self._k = len(domain)

        # 高概率ph，低概率pl
        self._ph = np.e ** epsilon / (np.e ** epsilon + self._k - 1)
        self._pl = 1 / (np.e ** epsilon + self._k - 1)

        # 用于快速建立索引，比如{'apple':0, 'banana':1, 'pear':2}
        self._item_index = {item: index for index, item in enumerate(domain)}

    def randomize(self, value):
        value = self.__check_value(value)
        probability_arr = np.full(shape=self._k, fill_value=self._pl)
        probability_arr[self._item_index[value]] = self._ph
        return np.random.choice(a=self._domain, p=probability_arr)

    def __check_value(self, value):
        if value not in self._domain:
            raise Exception("ERR: the input value={} is not in the input domain={}.".format(value, self._domain))
        return value

    def estimate_hist(self, randomized_values):
        counts = np.zeros(shape=self._k)
        for value in randomized_values:
            counts[self._item_index[value]] += 1
        return (counts - len(randomized_values) * self._pl) / (self._ph - self._pl)


if __name__ == '__main__':
    domain = ['a', 'b', 'c']
    epsilon = 1
    krr = GRR(epsilon, domain)
    print(krr._item_index)
    encoded_list = []
    for i in range(1000):
        encoded_list.append(krr.randomize('c'))
    print(krr.estimate_hist(encoded_list))