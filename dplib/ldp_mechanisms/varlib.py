# -*- coding: utf-8 -*-
# @Time    : 2021-11-22 10:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

import numpy as np
import pandas as pd
import meanlib

"""
@ 2021.11.22 测试不同方法
"""


def tst_cmp(size_list, eps_list, mechanism_list, repeated_times=20):
    df = pd.DataFrame(columns=('size', 'epsilon', 'mechanism', 'error'))
    for size in size_list:
        data = np.clip(np.random.normal(loc=0.2, scale=0.3, size=size), a_min=-1, a_max=1)
        # data = [-1, 0, 1]
        # print(data)
        var_base = np.var(data)
        for epsilon in eps_list:
            for mechanism in mechanism_list:
                # print(size, epsilon)
                err_list = []
                for i in range(repeated_times):
                    mech = mechanism(epsilon=epsilon)
                    x_encode = [mech.encode(v) for v in data]
                    # print("x_encode = ", x_encode)
                    x2_encode = [mech.encode(v**2) for v in data]
                    # print("x2_encode = ", x2_encode)
                    esti_x2 = np.average(x2_encode)
                    esti_x = np.average(x_encode)
                    var_esti = esti_x2 - esti_x**2
                    # print(esti_x2, esti_x)
                    err_list.append(np.fabs(var_base - var_esti))
                # print(err_list)
                record = {'size': size, 'epsilon': epsilon, 'mechanism': str(mechanism), 'error': np.average(err_list)}
                print(record)
                df = df.append(record, ignore_index=True)
    print(df)
    df.to_csv("varlib_res.csv", index=None)


if __name__ == '__main__':
    size_list = [10**4, 5*10**4, 10**5, 5*10**5]
    eps_list = [0.1, 0.5, 1, 5, 10]
    mechanism_list = [meanlib.Duchi, meanlib.PiecewiseMechanism, meanlib.Laplace]
    tst_cmp(size_list, eps_list, mechanism_list)



