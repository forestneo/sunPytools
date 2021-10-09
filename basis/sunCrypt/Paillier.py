# -*- coding: utf-8 -*-
# @Time    : 2021-10-01 10:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
此文件用于测试 Paillier 算法的性质，为未完善版本
@ 2021.10.09
"""

import sympy


class Paillier:
    def __init__(self, p=0, q=0, g=0):
        self.__p = p
        self.__q = q
        self.__n = self.__p * self.__q
        self.__lambda = sympy.lcm(self.__p - 1, self.__q - 1)

        self.__g = g
        self.__u = 0
        if self.__g != 0:
            self.__u = sympy.mod_inverse(self.__L(g**self.__lambda % self.__n**2), self.__n)
        print("p,q,n,lambda,g,u = ", self.__p, self.__q, self.__n, self.__lambda, self.__g, self.__u)
        print("Paillier:: initialized")

    def __L(self, x):
        return (x-1) / self.__n

    def generate_key(self, key_bits=10):
        # choose p and q, and calculate n and lambda
        while True:
            self.__p = sympy.ntheory.generate.randprime(2**key_bits, 2**(key_bits+1))
            self.__q = sympy.ntheory.generate.randprime(2**key_bits, 2**(key_bits+1))
            self.__n = self.__p * self.__q
            if sympy.gcd(self.__n, (self.__p - 1) * (self.__q - 1)) == 1:
                break
        self.__lambda = sympy.lcm(self.__p - 1, self.__q - 1)

        # choose g
        while True:
            # self.__g = np.random.randint(1, self.__n**2)
            # TODO: 20210929: 生成随机数 g，此处为了方便直接生成素数
            self.__g = sympy.ntheory.generate.randprime(2, self.__n**2)
            self.__u = sympy.mod_inverse(self.__L(self.__g**self.__lambda % self.__n**2), self.__n)
            # TODO: 20210929: 跳出没有写
            break
        print("Paillier:: key generated")

    def encrypt(self, m, r=0):
        r = sympy.ntheory.randprime(3, self.__n) if r == 0 else r
        return self.__g ** m * r ** self.__n % (self.__n ** 2)

    def decrypt(self, c):
        return self.__L(c**self.__lambda % (self.__n**2)) * self.__u % self.__n

    def get_public_key(self):
        return self.__n, self.__g

    def get_private_key(self):
        return self.__lambda, self.__u

    def __str__(self):
        return "ttt"

    def is_validate(self):
        # TODO: 20210929:检测当前参数是否合规
        return True


if __name__ == '__main__':
    pai = Paillier(p=7, q=11, g=5652)
    # pai = Paillier()
    # pai.generate_key()
    x_1, x_2 = 13, 25

    # 加解密测试
    print("\n encrypt-decrypt test")
    y_1, y_2 = pai.encrypt(x_1, r=23), pai.encrypt(x_2, r=23) # r 可以不同
    x_1, x_2 = pai.decrypt(y_1), pai.decrypt(y_2)
    print(x_1, x_2)

    # 加法同态测试，即 [x_1] * [x_2] = [x_1 + x_2]
    print("\n homomorphic test 1")
    y_3 = y_1 * y_2
    x_3 = pai.decrypt(y_3)
    print(x_3)

    # 验证 [m_1]^m2 mod n^2 = [m_1 * m_2]
    print("\n homomorphic test 2")
    n = pai.get_public_key()[0]
    x_tmp_1 = pai.decrypt(pai.encrypt(x_1)**x_2 % n**2)
    x_tmp_2 = (x_1 * x_2) % n
    print(x_tmp_1, x_tmp_2)


