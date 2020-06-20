# -*- coding: utf-8 -*-
# @Time    : 2020/5/29
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : k_subset.py
# @Software: PyCharm
# @Function: 

import numpy as np

class kRR:
    def __init__(self, bucket_size, epsilon, k):
        self.bucket_size = bucket_size
        self.epsilon = epsilon

        # the k represents the length of output
        self.k = k


    def encode_item(self, bucket):
        pass

    def decode_histogram(self, private_bucket_list):
        pass

if __name__ == '__main__':
    pass