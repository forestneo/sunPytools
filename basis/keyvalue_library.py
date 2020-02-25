# -*- coding: utf-8 -*-
# @Time    : 2019-11-01 10:37
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm


import numpy as np
import basis.local_differential_privacy_library as ldplib
from mean_solutions.duchi import encode_duchi


def kvlist_get_baseline(kv_list: np.ndarray, discretization=False):
    if not isinstance(discretization, bool):
        raise Exception("type error")
    f = np.average(kv_list[:, 0])

    value_list = []
    for kv in kv_list:
        if int(kv[0]) == 1 and discretization is True:
            value_list.append(ldplib.discretization(kv[1], lower=-1, upper=1))
        elif int(kv[0]) == 1 and discretization is False:
            value_list.append(kv[1])
        else:
            pass
    m = np.average(np.asarray(value_list))
    return f, m


def kvt_get_baseline(kvt: np.ndarray, discretization=False):
    if not isinstance(kvt, np.ndarray):
        raise Exception("type error of kvt: ", type(kvt))

    n, d = kvt.shape[0], kvt.shape[1]
    f_list, m_list = np.zeros([d]), np.zeros([d])

    for i in range(d):
        kv_list = kvt[:, i]
        f, m = kvlist_get_baseline(kv_list, discretization=discretization)
        f_list[i], m_list[i] = f, m
    return f_list, m_list


def kv_en_privkv(kv, epsilon1, epsilon2, set_value=None):
    k, v = int(kv[0]), kv[1]
    if k == 1:
        k = ldplib.perturbation(value=k, perturbed_value=1-k, epsilon=epsilon1)
        if k == 1:
            discretize_v = ldplib.discretization(v, -1, 1)
            p_k, p_v = 1, ldplib.perturbation(value=discretize_v, perturbed_value=-discretize_v, epsilon=epsilon2)
        else:
            p_k, p_v = 0, 0
    else:
        k = ldplib.perturbation(value=k, perturbed_value=1 - k, epsilon=epsilon1)
        if k == 1:
            v = np.random.uniform(low=-1, high=1) if set_value is None else set_value
            discretize_v = ldplib.discretization(v, -1, 1)
            p_k, p_v = 1, ldplib.perturbation(value=discretize_v, perturbed_value=-discretize_v, epsilon=epsilon2)
        else:
            p_k, p_v = 0, 0
    return [p_k, p_v]


def kv_de_privkv(p_kv_list: np.ndarray, epsilon_k, epsilon_v):
    if not isinstance(p_kv_list, np.ndarray):
        raise Exception("type error of p_kv_list: ", type(p_kv_list))

    p1 = np.e ** epsilon_k / (1 + np.e ** epsilon_k)
    p2 = np.e ** epsilon_v / (1 + np.e ** epsilon_v)

    k_list = p_kv_list[:, 0]
    v_list = p_kv_list[:, 1]

    f = (np.average(k_list) + p1-1) / (2*p1 - 1)
    # the [0] is because np.where() returns a tuple (x,y), x is the list and y it the type of elements of the array
    n1 = len(np.where(v_list == 1)[0])
    n2 = len(np.where(v_list == -1)[0])

    n_all = n1 + n2
    n1_star = (p2-1) / (2*p2-1) * n_all + n1 / (2*p2-1)
    n2_star = (p2-1) / (2*p2-1) * n_all + n2 / (2*p2-1)
    n1_star = np.clip(n1_star, 0, n_all)
    n2_star = np.clip(n2_star, 0, n_all)
    m = (n1_star - n2_star) / n_all

    return f, m


def kv_en_state_encoding(kv, epsilon):
    """
    The unary encoding, also known as k-random response, is used in user side. It works as follows
    First, key value data is mapped into {0, 1, 2}. Basically, [0,0]->1; [1,-1]->0; [1,1]->2;
    Then the k-rr is used to report.
    :param kv: key value data, in which k in {0,1} and value in [-1,1]
    :param epsilon: privacy budget
    :return: the encoded key value data, the res is in {0,1,2}
    """
    k, v = kv[0], ldplib.discretization(value=kv[1], lower=-1, upper=1)
    unary = k * v + 1
    return ldplib.k_random_response(unary, values=[0, 1, 2], epsilon=epsilon)


def kv_de_state_encoding(p_kv_list: np.ndarray, epsilon):
    """
    This is used in the server side. The server collects all the data and then use this function to calculate f and m.
    :param p_kv_list: the encoded kv list
    :param epsilon: the privacy budget
    :return: the estimated frequency and mean_solutions.
    """
    if not isinstance(p_kv_list, np.ndarray):
        raise Exception("type error of p_kv_list: ", type(p_kv_list))

    zero = len(np.where(p_kv_list == 1)[0])  # [0,0]
    pos = len(np.where(p_kv_list == 2)[0])  # [1,1]
    neg = len(np.where(p_kv_list == 0)[0])  # [1,-1]
    cnt_all = zero + pos + neg

    # adjust the true count
    cnt = np.asarray([zero, pos, neg])
    p = np.e ** epsilon / (2 + np.e ** epsilon)

    est_cnt = (2 * cnt - cnt_all * (1 - p)) / (3 * p - 1)

    f = (est_cnt[1] + est_cnt[2]) / cnt_all
    m = (est_cnt[1] - est_cnt[2]) / (est_cnt[1] + est_cnt[2])
    return f, m


def kv_en_f2m(kv, epsilon_k, epsilon_v, method, set_value=0):
    v = kv[1] if kv[0] == 1 else set_value
    p_k = ldplib.random_response_old(bits=int(kv[0]), p=ldplib.eps2p(epsilon_k))
    p_v = method(v, epsilon_v)
    return p_k, p_v


def kv_de_f2m(p_kv_list: np.ndarray, epsilon_k, set_value=0):
    if not isinstance(p_kv_list, np.ndarray):
        raise Exception("type error of p_kv_list: ", type(p_kv_list))
    f = np.average(p_kv_list[:, 0])
    p = ldplib.eps2p(epsilon=epsilon_k)
    f = (p-1+f) / (2*p-1)
    m_all = np.average(p_kv_list[:, 1])
    m = (m_all - (1 - f) * set_value) / f
    return f, m


def my_run_tst():
    # initial random seed, optional
    np.random.seed(10)

    # generate 100000 kv pairs with f=0.7 and m=0.3
    kv_list = [[np.random.binomial(1, 0.7), np.clip(a=np.random.normal(loc=0.3, scale=0.2), a_min=-1, a_max=1)] for _ in
               range(100000)]
    kv_list = np.asarray(kv_list)
    kv_list[:, 1] = kv_list[:, 1] * kv_list[:, 0]
    f_base, m_base = kvlist_get_baseline(kv_list=np.asarray(kv_list))
    print("this is the baseline f=%.4f, m=%.4f" % (f_base, m_base))

    epsilon = 2

    # the PrivKV method
    pirvkv_kv_list = [kv_en_privkv(kv, epsilon1=epsilon/2, epsilon2=epsilon/2) for kv in kv_list]
    f_privkv, m_privkv = kv_de_privkv(p_kv_list=np.asarray(pirvkv_kv_list), epsilon_k=epsilon/2, epsilon_v=epsilon/2)
    print("this is the privkv f=%.4f, m=%.4f" % (f_privkv, m_privkv))

    # the StateEncoding method
    se_kv_list = [kv_en_state_encoding(kv, epsilon) for kv in kv_list]
    f_se, m_se = kv_de_state_encoding(p_kv_list=np.asarray(se_kv_list), epsilon=epsilon)
    print("this is the se f=%.4f, m=%.4f" % (f_se, m_se))

    # the f2m-duchi method
    f2m_kv_list = [kv_en_f2m(kv=kv, epsilon_k=epsilon/2, epsilon_v=epsilon/2, method=encode_duchi) for kv in kv_list]
    f_f2m, m_f2m = kv_de_f2m(p_kv_list=np.asarray(f2m_kv_list), epsilon_k=epsilon/2)
    print("this is the f2m f=%.4f, m=%.4f" % (f_f2m, m_f2m))


if __name__ == '__main__':
    my_run_tst()

