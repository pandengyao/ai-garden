# OPD 中的 Forward KL 与 Reverse KL

中文 | [English](./Forward-and-Reverse-KL-in-OPD_en.md)

- **原文链接**: [**GKD**](https://arxiv.org/abs/2306.13649v3) · [**MiniLLM**](https://arxiv.org/abs/2306.08543v1)
- **整理日期**: 2026-11-06

## 1. 一句话理解

> **Forward KL：老师给高概率的 token，学生别给得太低。**
>
> **Reverse KL：老师给低概率的 token，学生别给得太高。**

前者更像**防漏学**，后者更像**防高估**。这是纠偏倾向，不是严格分工；“老师认可”只表示概率较高，不保证客观正确。

## 2. 数学上，区别是按谁的概率加权

在**同一个前缀** $`h`$ 下，记老师分布为 $`p(a\mid h)`$，学生分布为 $`q(a\mid h)`$，$`a`$ 表示下一个 token。以下省略共同的前缀条件，默认师生比较的是同一组 token 事件。

### Forward KL：按老师概率加权

```math
D_{\mathrm{KL}}(p\Vert q)
=
\sum_a p(a)\log\frac{p(a)}{q(a)}.
```

权重是 $`p(a)`$：老师越重视的 token，学生越不能忽略。常称为 **mode-covering（覆盖模式）**。

### Reverse KL：按学生概率加权

```math
D_{\mathrm{KL}}(q\Vert p)
=
\sum_a q(a)\log\frac{q(a)}{p(a)}
=
\mathbb{E}_{a\sim q}
\left[\log q(a)-\log p(a)\right].
```

权重是 $`q(a)`$：重点检查学生经常选择的 token，老师是否也认可。常称为 **mode-seeking（寻找模式）**。

**两者不是分别学习老师的高概率和低概率 token，而是用不同权重衡量整张概率表的差异。**

## 3. 一个例子

假设词表只有三个 token：

| token | 老师概率 | 学生概率 |
| --- | ---: | ---: |
| A | $`49\%`$ | $`89\%`$ |
| B | $`49\%`$ | $`1\%`$ |
| C | $`2\%`$ | $`10\%`$ |

**示例说明：数字仅用于教学，不是实验结果。**

- **Forward KL 更强调 B 的问题**：老师给了很高概率，学生却几乎不选，属于“漏学”。
- **Reverse KL 更强调 C 的问题**：老师只给了很低概率，学生却明显高估，属于“过度偏好”。

因此，**“Reverse KL 向老师的低概率 token 对齐”**只能理解为：**把学生对这些 token 的过高概率压下来**，而不是鼓励学生生成老师低概率的 token。

## 4. 与 OPD 的关系

OPD（On-Policy Distillation）的基本流程是：**学生生成回答，老师在学生实际经过的前缀上提供反馈，再更新学生。**

要区分两个独立维度：

| 维度 | 决定什么 |
| --- | --- |
| On-policy / Off-policy | 训练轨迹和前缀来自哪里 |
| Forward KL / Reverse KL | 在同一个前缀下，怎样比较师生分布 |

所以，**学生生成轨迹之后，既可以使用 Forward KL，也可以使用 Reverse KL**。Forward KL 按老师概率加权，不代表训练前缀必须由老师生成。

Reverse KL 的期望恰好按学生分布取样，因此容易接到学生采样流程上。一个常见的逐 token 反馈信号是：

```math
r_t=\log p(a_t\mid h_t)-\log q(a_t\mid h_t).
```

老师概率高于学生时，信号为正；低于学生时，信号为负。**这是反馈信号，不是完整训练算法；不能直接把采样得到的对数概率差当作普通监督损失。**

## 5. 两个边界条件

- **理想终点相同**：如果学生能完整表示老师分布，两种 KL 都在 $`q=p`$ 时达到最小值 $`0`$。覆盖模式与寻找模式描述的是受限拟合或近似优化时的倾向，不意味着 Reverse KL 必然只保留一个答案。
- **完整 KL 非负，单项不一定非负**：某个 token 的贡献或采样得到的 log-probability 差可以为负，不代表公式出错。

## 参考资料

**[1] GKD：On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes。支持学生轨迹与不同散度目标的组合。** [**论文页面**](https://arxiv.org/abs/2306.13649v3)

**[2] MiniLLM: Knowledge Distillation of Large Language Models。讨论 Reverse KL 及避免高估老师低概率区域的动机。** [**论文页面**](https://arxiv.org/abs/2306.08543v1)
