# -*- coding: utf-8 -*-
# @Time    : 2021-10-01 10:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
此文件用于测试 RSA 算法的性质，为未完善版本
@ 2021.10.09
"""

import sympy
import numpy as np


class RSA:
    def __init__(self, p=0, q=0, e=0, d=0):
        self.__p = p
        self.__q = q
        self.__n = self.__p * self.__q
        self.__phi = (self.__p-1) * (self.__q-1)
        self.__e = e
        self.__d = d

    def generate_key(self, key_bits=10):
        # choose p and q, and calculate n and phi
        # key_bits = key_bits / 2             # RSA 密钥的位数指的是 n 的位数
        self.__p = sympy.ntheory.generate.randprime(2 ** key_bits, 2 ** (key_bits + 1))
        self.__q = sympy.ntheory.generate.randprime(2 ** key_bits, 2 ** (key_bits + 1))
        self.__n = self.__p * self.__q
        self.__phi = (self.__p - 1) * (self.__q - 1)
        while True:
            # 暴力一点，直接选了一个素数当 e
            self.__e = sympy.ntheory.generate.randprime(2, self.__phi)
            self.__d = sympy.mod_inverse(self.__e, self.__phi)
            if sympy.gcd(self.__e, self.__phi) == 1:
                break

    def encrypt(self, m):
        # todo: 未加速，速度很慢
        return m**self.__e % self.__n

    def decrypt(self, c):
        # todo: 未加速，速度很慢
        return c**self.__d % self.__n

    def get_public_key(self):
        return self.__e, self.__n

    def get_private_key(self):
        return self.__d, self.__n

    def __str__(self):
        return "ttt"

    def is_validate(self):
        # todo: 检测当前参数是否合规
        return True


if __name__ == '__main__':
    rsa = RSA()
    rsa.generate_key()

    x = 12
    y = rsa.encrypt(x)
    print("the encrypted number is: ", y)
    x = rsa.decrypt(y)
    print("the decrypted result is: ", x)