[toc]

# 20200226

## update random response

the old version:

```python
def random_response_old(bits, p, q=None):
    """
    random response
    :param bits: can be int or np.ndarray
    :param p: Pr[1->1]
    :param q: Pr[0->1]
    :return: the perturbed bits
    """
    q = 1-p if q is None else q
    if isinstance(bits, int):
        probability = p if bits == 1 else q
        return np.random.binomial(n=1, p=probability)
    elif isinstance(bits, np.ndarray):
        bits = np.array(bits)
        for i in range(len(bits)):
            probability = p if bits[i] == 1 else q
            bits[i] = np.random.binomial(n=1, p=probability)
        return bits
    else:
        raise Exception(type(bits), bits, p, q)
```

new version:

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
    return (bits + flip_flags + 1) % 2
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
