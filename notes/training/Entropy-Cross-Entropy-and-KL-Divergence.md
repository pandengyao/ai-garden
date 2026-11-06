# 熵、交叉熵与 KL 散度

中文 | [English](./Entropy-Cross-Entropy-and-KL-Divergence_en.md)

- **原文链接**: **个人数学笔记。**
- **发布日期**: 2026-10-30

1. **熵（Entropy）**：真实分布自身的不确定性。
1. **交叉熵（Cross Entropy）**：用预测分布 $`Q`$ 描述真实分布 $`P`$ 的平均信息量。
1. **KL 散度（KL Divergence）**：使用 $`Q`$ 代替 $`P`$ 所增加的额外信息代价。

| 概念 | 数学公式 | 衡量对象 | 越小表示 | 机器学习中的意义 |
| --- | --- | --- | --- | --- |
| **信息量（Information）** | $`I(x)=-\log P(x)`$ | 单个事件 | 事件越常见，信息量越少 | 衡量一个事件带来的惊讶程度 |
| **熵（Entropy）** | $`H(P)=-\sum_x P(x)\log P(x)`$ | 一个概率分布 | 分布越确定 | 描述数据本身的不确定性 |
| **交叉熵（Cross Entropy）** | $`H(P,Q)=-\sum_x P(x)\log Q(x)`$ | 真实分布 $`P`$ 与预测分布 $`Q`$ | 预测分布越符合真实分布 | 分类任务中常用的损失函数 |
| **KL 散度（KL Divergence）** | $`D_{KL}(P\Vert Q)=\sum_x P(x)\log\frac{P(x)}{Q(x)}`$ | 两个概率分布之间的差异 | 两个分布越接近 | 衡量预测分布相对真实分布的偏离程度 |
| **核心关系** | $`H(P,Q)=H(P)+D_{KL}(P\Vert Q)`$ | 三者之间的关系 | — | 当真实分布 $`P`$ 固定时，最小化交叉熵等价于最小化 KL 散度 |

当真实分布 $`P`$ 固定时：

```math
\boxed{
\min_Q H(P,Q)
\Longleftrightarrow
\min_Q D_{KL}(P\Vert Q)
}
```
