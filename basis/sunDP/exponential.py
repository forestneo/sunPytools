# -*- coding: utf-8 -*-
# @Time    : 2022-01-07 15:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

import numpy as np


class Exponential:
    def __init__(self, epsilon, sensitivity, range, func_score):
        self.epsilon = epsilon
        self.sensitivity = sensitivity
        self.range = range
        self.func_score = func_score

    def exponential(self, data):
        # calculate scores
        scores = np.asarray([self.func_score(item, data) for item in self.range])
        probabilities = np.exp(self.epsilon * scores / (2 * self.sensitivity))
        probabilities = probabilities / np.linalg.norm(probabilities, ord=1)
        return np.random.choice(self.range, size=1, p=probabilities)[0]


def score(x, data: list):
    return data.count(x) / 200


def run_example():
    np.random.seed(0)
    data = list(np.random.choice(a=['a', 'b', 'c'], size=1000, replace=True, p=[0.5, 0.3, 0.2]))
    EXP = Exponential(epsilon=1, sensitivity=1, range=['a', 'b', 'c'], func_score=score)
    res = [EXP.exponential(data) for i in range(10000)]
    print(res.count('a'), res.count('b'), res.count('c'))


if __name__ == '__main__':
    run_example()
