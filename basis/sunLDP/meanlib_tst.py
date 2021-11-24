# -*- coding: utf-8 -*-
# @Time    : 2021-11-22 20:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

"""
@ 2021.11.22 测试 meanlib.py
"""
import meanlib
import numpy as np
import pandas as pd


def tst_cmp(size_list, eps_list, mechanism_list, repeated_times=20):
    df = pd.DataFrame(columns=('size', 'epsilon', 'mechanism', 'error'))

    for size in size_list:
        data = np.clip(np.random.normal(loc=0.2, scale=0.3, size=size), a_min=-1, a_max=1)
        m_base = np.average(data)
        for epsilon in eps_list:
            for mechanism in mechanism_list:
                # print(size, epsilon, mechanism)
                err_list = []
                for i in range(repeated_times):
                    mech = mechanism(epsilon=epsilon)
                    data_encode = [mech.encode(v) for v in data]
                    m_esti = np.average(data_encode)
                    err_list.append(np.fabs(m_base-m_esti))
                record = {'size': size, 'epsilon':epsilon, 'mechanism': str(mechanism), 'error': np.average(np.array(err_list))}
                print(record)
                df = df.append(record, ignore_index=True)
    print(df)
    df.to_csv("meanlib_res.csv", index=None)


if __name__ == '__main__':
    size_list = [10**4, 5*10**4, 10**5]
    eps_list = [0.1, 0.5, 1, 5]
    mechanism_list = [meanlib.Duchi, meanlib.PiecewiseMechanism, meanlib.Laplace]
    tst_cmp(size_list, eps_list, mechanism_list)