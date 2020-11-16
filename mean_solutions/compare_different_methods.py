# -*- coding: utf-8 -*-
# @Time    : 2019-07-11 18:27
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

# @Update  : 2020.10.20


from mean_solutions import DuchiMechanism as DM
from mean_solutions import PiecewiseMechanism as PM
import numpy as np
import matplotlib.pyplot as plt


def run_tst():
    # generate the data in [-1,1]
    data = np.clip(np.random.normal(loc=0.2, scale=0.3, size=100000), a_min=-1, a_max=1)
    # get baseline
    m_base = np.average(data)

    epsilon_list, error_duchi, error_piecewise = [], [], []

    for i in range(1, 10):
        epsilon = 0.1 * i
        epsilon_list.append(epsilon)

        # initial the encoding method
        duchi = DM.Duchi(epsilon)
        piecewise = PM.PiecewiseMechanism(epsilon)

        # duchi's solution and its error
        duchi_data = [duchi.encode(value) for value in data]
        m_duchi = np.average(duchi_data)
        err_duchi = np.fabs(m_duchi-m_base)
        error_duchi.append(err_duchi)

        # piecewise solution and its error
        pm_data = [piecewise.encode(value) for value in data]
        m_piecewise = np.average(pm_data)
        err_pm = np.fabs(m_piecewise - m_base)
        error_piecewise.append(err_pm)

        print("epsilon = %.2f, err_duchi = %.4f, err_pm = %.4f" % (epsilon, err_duchi, err_pm))

    # draw the result
    plt.figure(figsize=[12, 5])
    plt.plot(epsilon_list, error_duchi, label="duchi")
    plt.plot(epsilon_list, error_piecewise, label="piecewise")
    plt.xlabel("epsilon")
    plt.ylabel("error")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    run_tst()



