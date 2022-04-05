# -*- coding: utf-8 -*-
# @Time    : 2022-02-08 22:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
the duchi's solution towards mean estimation
@ 2022.02.08 updated, add the LDPBase class
"""

from ldp_base import LDPBase
import numpy as np


class DuchiMechanism(LDPBase):
    def __init__(self, epsilon, domain=(-1, 1)):
        self._espilon = self._check_epsilon(epsilon)
        self._domain = domain
        self._p = np.e ** epsilon / (np.e**epsilon + 1)

    def _check_value(self, value):
        if not self._domain[0] <= value <= self._domain[1]:
            raise ValueError("ERR: The input value={} is not in tht input domain={}.".format(value, self._domain))
        return value

    def randomize(self, value):
        value = self._check_value(value)
        # assume the domain is [a, b], the discretization and rr process is
        # P[y=a] = ((1-2p)*v + (ap+bp-a))/(b-a)
        a, b = self._domain
        rnd_p = ((1-2*self._p)*value + (a*self._p+b*self._p-a))/(b-a)
        rnd = np.random.random()
        value = a if rnd <= rnd_p else b

        # after the perturbation process, the expectation of y is
        # E[y] = (2p-1)x + (b+a)(1-p)
        # thus, adjust is needed
        value = (value - (b+a)*(1-self._p)) / (2*self._p-1)
        return value


if __name__ == '__main__':
    domain = (100, 200)
    a = DuchiMechanism(epsilon=0.001, domain=domain)
    data = np.clip(np.random.laplace(loc=130, scale=20, size=10**5), domain[0], domain[1])
    print(np.average(data))

    p_data = [a.randomize(v) for v in data]
    print(max(p_data), min(p_data))
    print(np.average(p_data))
