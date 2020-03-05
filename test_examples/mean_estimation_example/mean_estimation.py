# -*- coding: utf-8 -*-
# @Time    : 2019-07-11 18:27
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm


from mean_solutions import duchi
from mean_solutions import piecewise
import numpy as np
import matplotlib.pyplot as plt


def get_mean_from_table(value_table: np.ndarray, epsilon, en_mtd, de_mtd):
    """
    :param value_table: the value table
    :param epsilon:
    :param en_mtd: the encoding method
    :param de_mtd: the decoding method
    :return:
    """
    [n, d] = value_table.shape
    index_list = [[] for i in range(d)]
    for i in range(n):
        index = np.random.randint(d)
        index_list[index].append(en_mtd(value_table[i][index], epsilon))

    mean_list = [[] for i in range(d)]
    for i in range(d):
        mean_list[i] = de_mtd(index_list[i], epsilon)
    return np.asarray(mean_list)


def my_run_tst():
    # np.random.seed(10)
    value_table = np.random.normal(loc=0.2, scale=0.2, size=[100000, 10])
    value_table = np.clip(value_table, -1, 1)
    m_base = np.mean(value_table, axis=0)

    # 存放结果
    epsilon_list, error_duchi, error_piecewise = [], [], []

    for i in range(1, 10):
        epsilon = 0.02 * i
        epsilon_list.append(epsilon)

        m_est_duchi = get_mean_from_table(value_table=value_table, epsilon=epsilon, en_mtd=duchi.encode_duchi,
                                          de_mtd=duchi.decode_duchi)
        m_est_pm = get_mean_from_table(value_table=value_table, epsilon=epsilon, en_mtd=piecewise.encode_piecewise,
                                       de_mtd=piecewise.decode_piecewise)
        print(epsilon, m_est_duchi, m_est_pm)
        error_duchi.append(np.average(np.fabs(m_est_duchi-m_base)))
        error_piecewise.append(np.average(np.fabs(m_est_pm-m_base)))
    # 画图
    fig = plt.figure(figsize=[12, 5])
    plt.plot(epsilon_list, error_duchi, label="duchi")
    plt.plot(epsilon_list, error_piecewise, label="piecewise")
    plt.xlabel("epsilon")
    plt.ylabel("error")
    plt.legend()
    plt.show()


def my_run_tst_2():
    # 产生数据并归一化
    data = np.random.normal(loc=0.2, scale=0.3, size=100000)
    data = np.clip(data, -1, 1)

    mean_ori = np.average(data)
    print("original mean_solutions: ", mean_ori)

    # 存放结果
    epsilon_list, error_duchi, error_piecewise = [], [], []

    for i in range(1, 10):
        epsilon = 0.1 * i
        epsilon_list.append(epsilon)

        # duchi's solution
        duchi_data = [duchi.encode_duchi(value, epsilon) for value in data]
        mean_duchi = np.average(duchi_data)
        err_duchi = np.fabs(mean_duchi-mean_ori)
        error_duchi.append(err_duchi)

        # piecewise solution
        pm_data = [piecewise.encode_piecewise_mine(value, epsilon) for value in data]
        mean_pm = np.average(pm_data)
        err_pm = np.fabs(mean_pm-mean_ori)
        print(epsilon, err_duchi, err_pm)

        error_piecewise.append(err_pm)

    # 画图
    fig = plt.figure(figsize=[12, 5])
    plt.plot(epsilon_list, error_duchi, label="duchi")
    plt.plot(epsilon_list, error_piecewise, label="piecewise")
    plt.xlabel("Epsilon")
    plt.ylabel("Estimation Error")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    my_run_tst()



