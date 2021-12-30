

# Introduction


- 我的个人网站：[https://forestneo.com/](https://forestneo.com/)
- 欢迎关注我的知乎：[DPer](https://www.zhihu.com/people/sun-lin-83)
- 欢迎关注微信公众号：[《差分隐私》](https://forest-pic.oss-cn-beijing.aliyuncs.com/20200308122411.png)
- QQ学习交流群：779053117（微信交流群联系群主添加）

<img src="https://forest-pic.oss-cn-beijing.aliyuncs.com/20200308122411.png" alt="微信公众号" style="zoom: 33%;" />


本开源代码可用于科学研究
本项目主要包含两个部分：

- `basis.sunLDP`: original known as `sunDP`. This package can be used for developing LDP mechanisms. The detailed information is listed below.
- `basis.sunCrypt`: this package is not fully developed yet, but can be ued for understanding cryptographing algorithms, such as RSA and Paillier.

## sunLDP



The ldplib provides basic randomized functions.

- eps2p: turn the privacy budget to the probability by coin flipping
- discretization: used to discretize a continuous value
- RR: [Randomized Response: A Survey Technique for Eliminating Evasive Answer Bias](https://www.tandfonline.com/doi/abs/10.1080/01621459.1965.10480775)
- Unary Encoding: from paper [Locally Differentially Private Protocols for Frequency Estimation](https://dl.acm.org/doi/10.5555/3241189.3241247)
- SUE: symmetric unary encoding from paper [Locally Differentially Private Protocols for Frequency Estimation](https://dl.acm.org/doi/10.5555/3241189.3241247)
- OUE: optimized unary encodingfrom paper [Locally Differentially Private Protocols for Frequency Estimation](https://dl.acm.org/doi/10.5555/3241189.3241247)

### kvlib

Some basic encoding terms:

- `kv`: a kv pair denoted as $\langle k, v\rangle$, where $k\in \{0,1\}, v\in[-1,1]$.
- `kvl`: a list of key-value pairs, denoted by $[\langle k_1, v_1\rangle,\langle k_2, v_2\rangle...]$. The kvl is used to represent the $i-$th key-value or to represent a list of key-value pairs of one user.
- `kvt`: a $n\times d$ key-value table. A kvt is used to represent the kvl from $n$ users.

The kvlib main contains the following perturbation and analysis algorithms:

- `PrivBV`: [PrivKV: Key-Value Data Collection with Local Differential Privacy](https://ieeexplore.ieee.org/abstract/document/8835348/)
- `BiSample`: [BiSample: Bidirectional Sampling for Handling Missing Data with Local Differential Privacy.](https://www.researchgate.net/publication/339251866_BiSample_Bidirectional_Sampling_for_Handling_Missing_Data_with_Local_Differential_Privacy/stats)
- `SE`: from paper [Conditional Analysis for Key-Value Data with Local Differential Privacy](https://arxiv.org/abs/1907.05014)

### heavy_hitters

- `Hadamard Repsonse`: [Hadamard Response: Estimating Distributions Privately, Efficiently, and with Little Communication](http://arxiv.org/abs/1802.04705)
- `k-RR`: the k-randomized response
- `k-subset`:
- `RAPPOR`: [RAPPOR: Randomized Aggregatable Privacy-Preserving Ordinal Response](http://dl.acm.org/citation.cfm?doid=2660267.2660348)

### mean_solutions

- `duchi`: also known as the 1Bit Mechanism (noted that the input domain of 1Bit is [1,m], while the input domain of duchi is [-1,1]).
- `PM`: [Collecting and Analyzing Multidimensional Data with Local Differential Privacy](https://arxiv.org/abs/1907.00782)

# sunCrypt



