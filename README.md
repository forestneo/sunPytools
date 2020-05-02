[toc]

# Introdcution
Useful tools for local differential privacy, which mainly consists of several parts:

- basis
    - ldplib: local differential privacy library
    - kvlib: key-value library
    - plib: probability library
    - mdlib: missing data library
- mean_solutions
    - duchi
    - piecewise


# ldplib

function list:

| 函数名称                                | 功能                          |
| --------------------------------------- | ----------------------------- |
| eps2p(epsilon, n=2)                     | to calculate the probability $p = \frac{e^\epsilon}{e^\epsilon+1}$ |
| discretization(value, lower=0, upper=1) | discretize a value $v\in[0,1]$ to $v\in\{0,1\}$ |
| random_response(bits: np.ndarray, p, q=None)                | the typical random response |
| unary_encoding(bits: np.ndarray, epsilon)                        |    UE                           |
| symmetric_unary_encoding(bits: np.ndarray, epsilon)                         |        SUE                       |
| optimized_unary_encoding(bits: np.ndarray, epsilon)                                       | OUE                              |

# kvlib

Some basic encoding terms:

- kv: a kv pair denoted as $\langle k, v\rangle$, where $k\in \{0,1\}, v\in[-1,1]$.
- kvl: a list of key-value pairs, denoted by $[\langle k_1, v_1\rangle,\langle k_2, v_2\rangle...]$. The kvl is used to represent the $i-$th key-value or to represent a list of key-value pairs of one user.
- kvt: a $n\times d$ key-value table. A kvt is used to represent the kvl from $n$ users.

The kvlib main contains the following perturbation and analysis algorithms:

- PrivBV: [PrivKV: Key-Value Data Collection with Local Differential Privacy](https://ieeexplore.ieee.org/abstract/document/8835348/)
- BiSample: [BiSample: Bidirectional Sampling for Handling Missing Data with Local Differential Privacy.](https://www.researchgate.net/publication/339251866_BiSample_Bidirectional_Sampling_for_Handling_Missing_Data_with_Local_Differential_Privacy/stats)
- SE: 
- 

# mdlib

This library is used in the paper: [BiSample: Bidirectional Sampling for Handling Missing Data with Local Differential Privacy.](https://www.researchgate.net/publication/339251866_BiSample_Bidirectional_Sampling_for_Handling_Missing_Data_with_Local_Differential_Privacy/stats)

# mean_solutions

- duchi: 
- pm: [Collecting and Analyzing Multidimensional Data with Local Differential Privacy](https://arxiv.org/abs/1907.00782)