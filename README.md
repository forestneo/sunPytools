[toc]

# Introdcution
Useful tools for differential privacy

mainly consists of two parts:
- basis
- mean





add histogram


# ldplib

function list:

| 函数名称                                | 功能                          |
| --------------------------------------- | ----------------------------- |
| eps2p(epsilon, n=2)                     | 计算概率                      |
| discretization(value, lower=0, upper=1) | 离散化                        |
| random_response(B, p, q)                | 随机响应，也叫 Unary Encoding |
| SUE(B, epsilon)                         |                               |
| OUE(B, epsilon)                         |                               |
|                                         |                               |
|                                         |                               |
|                                         |                               |

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

### random_response(B, p, q)

<img src="https://forest-pic.oss-cn-beijing.aliyuncs.com/20200128142113.png" style="zoom:67%;" />

# Key-Value library
