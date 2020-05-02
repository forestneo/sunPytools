# -*- coding: utf-8 -*-
# @Time    : 2020/3/18
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : data_processor.py
# @Software: PyCharm


import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("ratings_small.csv")
    print(df.head())
