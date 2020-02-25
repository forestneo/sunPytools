[toc]

# 20200202

## update random response

old version:

```python
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

new version:

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


result compare:

```python
a = np.random.binomial(1, p=0.5, size=1000)

time_s = time.perf_counter()
for i in range(1000):
random_response_old(B=a, p=0.9)
time_e = time.perf_counter()
print("old version = ", (time_e - time_s))

time_s = time.perf_counter()
for i in range(1000):
random_response(bits=a, p=0.9)
time_e = time.perf_counter()
print("new version = ", (time_e - time_s))
```

result

```
old version =  2.055327879
new version =  0.06653766500000025
```



# 
