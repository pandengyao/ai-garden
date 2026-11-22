# Entropy, Cross Entropy, and KL Divergence

[中文](./Entropy-Cross-Entropy-and-KL-Divergence.md) | English

- **Source**: **Personal mathematics note.**
- **Published**: 2026-10-30

1. **Entropy**: the uncertainty inherent in the true distribution.
1. **Cross entropy**: the average information content when using the predicted distribution $`Q`$ to describe the true distribution $`P`$.
1. **KL divergence**: the additional information cost of using $`Q`$ instead of $`P`$.

| Concept | Formula | What it measures | A lower value means | Role in machine learning |
| --- | --- | --- | --- | --- |
| **Information content** | $`I(x)=-\log P(x)`$ | A single event | The event is more common and carries less information | Measures how surprising an event is |
| **Entropy** | $`H(P)=-\sum_x P(x)\log P(x)`$ | A probability distribution | The distribution is more certain | Describes the uncertainty inherent in the data |
| **Cross entropy** | $`H(P,Q)=-\sum_x P(x)\log Q(x)`$ | The true distribution $`P`$ and the predicted distribution $`Q`$ | The predicted distribution better matches the true distribution | A commonly used loss function for classification |
| **KL divergence** | $`D_{KL}(P\Vert Q)=\sum_x P(x)\log\frac{P(x)}{Q(x)}`$ | The discrepancy between two probability distributions | The two distributions are closer | Measures how far the predicted distribution deviates from the true distribution |
| **Key relationship** | $`H(P,Q)=H(P)+D_{KL}(P\Vert Q)`$ | The relationship among the three quantities | — | When the true distribution $`P`$ is fixed, minimizing cross entropy is equivalent to minimizing KL divergence |

When the true distribution $`P`$ is fixed:

```math
\boxed{
\min_Q H(P,Q)
\Longleftrightarrow
\min_Q D_{KL}(P\Vert Q)
}
```
