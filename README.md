[toc]

# Introdcution
Useful tools for differential privacy

mainly consists of two parts:
- basis
    - ldplib: local differential privacy library
    - kvlib: key-value library
    - plib: probability library
- mean_solutions
    - duchi
    - piecewise


# ldplib

function list:

| 函数名称                                | 功能                          |
| --------------------------------------- | ----------------------------- |
| eps2p(epsilon, n=2)                     | 计算概率                      |
| discretization(value, lower=0, upper=1) | 离散化                        |
| random_response(bits: np.ndarray, p, q=None)                | 随机响应 |
| unary_encoding(bits: np.ndarray, epsilon)                        |    UE                           |
| symmetric_unary_encoding(bits: np.ndarray, epsilon)                         |        SUE                       |
| optimized_unary_encoding(bits: np.ndarray, epsilon)                                       | OUE                              |
                          
## 函数介绍

### eps2p(epsilon, n=2)

此函数根据epsilon计算保持数据不变的概率，当输入数据包含n时，对应的概率为k-RR的概率。

```python
def eps2p(epsilon, n=2):
    return np.e ** epsilon / (np.e ** epsilon + n - 1)
```

### discretization(value, lower=0, upper=1)

此函数将数据value进行离散化，默认离散化结果为 {0，1}。

```python
def discretization(value, lower=0, upper=1):

    if value > upper or value < lower:
        raise Exception("the range of value is not valid in Function @Func: discretization")

    p = (value - lower) / (upper - lower)
    rnd = np.random.random()
    return upper if rnd < p else lower
```

### random_response(bits, p, q)

<img src="https://forest-pic.oss-cn-beijing.aliyuncs.com/20200128142113.png" style="zoom:67%;" />


在实现的过程中，为了效率更高，对于n位的一个输入，我们首先产生了一个 n 位的 flag 数组，其中1表示不反转，0表示翻转。然后根据公式(bits + flip_flags + 1) % 2 产生结果。

```python
def coin_flip(bits: np.ndarray, flip_flags: np.ndarray):
    if not (isinstance(bits, np.ndarray) or isinstance(flip_flags, np.ndarray)):
        raise Exception("Type Err: ", type(bits), type(flip_flags))
    if not bits.shape == flip_flags.shape:
        raise Exception("Length Err: ", bits.shape, flip_flags.shape)
    # the 1 in F is not to flip
    # B F B'
    # 1 1 1
    # 1 0 0
    # 0 1 0
    # 0 0 1
    return (bits + flip_flags + 1) % 2


def random_response(bits: np.ndarray, p, q=None):
    """
    :param bits: bits
    :param p: probability of 1->1
    :param q: probability of 0->1
    update: 2020.02.25
    """
    q = 1 - p if q is None else q
    if isinstance(bits, int):
        probability = p if bits == 1 else q
        return np.random.binomial(n=1, p=probability)

    if not isinstance(bits, np.ndarray):
        raise Exception("Type Err: ", type(bits))

    if len(bits.shape) != 1:
        raise Exception("Size Err: ", bits.shape)
    flip_flags = np.where(bits == 1, np.random.binomial(1, p, len(bits)), np.random.binomial(1, 1 - q, len(bits)))
    return coin_flip(bits, flip_flags)
```


# Key-Value library

| 基本名称                                | 含义                         |
| --------------------------------------- | ----------------------------- |
| kv_                     | KV pair                      |
| kvs |    a list of kv                     |
| kvt | kv_table: a list of kv list|


# mean_solutions