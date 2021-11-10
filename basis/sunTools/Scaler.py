# -*- coding: utf-8 -*-
# @Time    : 2021-10-09 10:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
This script is used for data scaling

@ 2021.10.09: initialized
"""


class Normalizer:
    """
    将输入范围的数据归一化到输出范围
    """
    def __init__(self, input_domain, output_domain=(0,1)):
        self.input_min, self.input_max = input_domain[0], input_domain[1]
        self.output_min, self.output_max = output_domain[0], output_domain[1]
        self.slope = (output_domain[1] - output_domain[0]) / (input_domain[1] - input_domain[0])

    def normalize(self, v):
        if v > self.input_max or v < self.input_min:
            raise Exception("ERR: input out of range! input = %.2f, range = [%.2f, %.2f]" % (v, self.input_min, self.input_max))
        return self.slope * v + self.output_min - self.slope * self.input_min

    def de_normalize(self, v):
        return (v - self.output_min + self.slope * self.input_min) / self.slope


if __name__ == '__main__':
    input_domain = [0, 100]
    output_domain = [-1, 1]

    normalizer = Normalizer(input_domain, output_domain)
    print(normalizer.normalize(50))
    print(normalizer.de_normalize(0.5))