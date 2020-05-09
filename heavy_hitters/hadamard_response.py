# -*- coding: utf-8 -*-
# @Time    : 2020/5/9
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : hadamard_response.py
# @Software: PyCharm
# @Function: 

import numpy as np


class HR:
    def __init__(self, bucket_size, epsilon):
        # the probability of 1->1
        self.p = np.e ** (epsilon/2) / (np.e ** (epsilon/2) + 1)
        # the size of buckets
        self.bucket_size = bucket_size
        self.private_bucket_size = 0
        pass

    def encode_item(self, bucket):
        if bucket >= self.bucket_size:
            raise Exception("the input domain is wrong, bucket = %d, k = %d" % (bucket, self.bucket_size))


    def decode_frequency(self, private_bucket_lst):
        # todo

        pass

if __name__ == '__main__':
    pass