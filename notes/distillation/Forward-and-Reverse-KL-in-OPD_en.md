# Forward KL and Reverse KL in OPD

[中文](./Forward-and-Reverse-KL-in-OPD.md) | English

- **Source**: [**GKD**](https://arxiv.org/abs/2306.13649v3) · [**MiniLLM**](https://arxiv.org/abs/2306.08543v1)
- **Compiled**: 2026-11-06

## 1. The one-sentence intuition

> **Forward KL: do not give too little probability to tokens the teacher considers likely.**
>
> **Reverse KL: do not give too much probability to tokens the teacher considers unlikely.**

The former is more about **avoiding omissions**; the latter is more about **avoiding overestimation**. These are tendencies, not exclusive roles. "Teacher-approved" only means higher probability, not guaranteed objective correctness.

## 2. Mathematically, the difference is whose probabilities supply the weights

At **the same prefix** $`h`$, let the teacher distribution be $`p(a\mid h)`$ and the student distribution be $`q(a\mid h)`$, where $`a`$ denotes the next token. We omit the shared prefix condition below and assume that teacher and student are compared over the same token events.

### Forward KL: weighted by teacher probabilities

```math
D_{\mathrm{KL}}(p\Vert q)
=
\sum_a p(a)\log\frac{p(a)}{q(a)}.
```

The weight is $`p(a)`$: the more probability the teacher assigns to a token, the less the student can afford to neglect it. This is commonly called **mode-covering**.

### Reverse KL: weighted by student probabilities

```math
D_{\mathrm{KL}}(q\Vert p)
=
\sum_a q(a)\log\frac{q(a)}{p(a)}
=
\mathbb{E}_{a\sim q}
\left[\log q(a)-\log p(a)\right].
```

The weight is $`q(a)`$: the focus is on whether tokens the student often selects are also favored by the teacher. This is commonly called **mode-seeking**.

**They do not separately learn the teacher's high- and low-probability tokens; they use different weights to measure discrepancies across the entire probability distribution.**

## 3. An example

Suppose the vocabulary contains only three tokens:

| token | Teacher probability | Student probability |
| --- | ---: | ---: |
| A | $`49\%`$ | $`89\%`$ |
| B | $`49\%`$ | $`1\%`$ |
| C | $`2\%`$ | $`10\%`$ |

**Example note: these numbers are illustrative, not experimental results.**

- **Forward KL puts more emphasis on the problem with B**: the teacher assigns high probability, but the student almost never selects it—an omission.
- **Reverse KL puts more emphasis on the problem with C**: the teacher assigns low probability, but the student substantially overestimates it—an excessive preference.

Thus, **"Reverse KL aligns with the teacher's low-probability tokens"** can only mean **reducing the student's excessive probability on those tokens**, not encouraging the student to generate tokens the teacher considers unlikely.

## 4. The connection to OPD

The basic on-policy distillation (OPD) workflow is: **the student generates responses, the teacher provides feedback at prefixes the student actually visits, and the student is then updated.**

Distinguish two independent dimensions:

| Dimension | What it determines |
| --- | --- |
| On-policy / Off-policy | Where training trajectories and prefixes come from |
| Forward KL / Reverse KL | How teacher and student distributions are compared at the same prefix |

Therefore, **either Forward KL or Reverse KL can be used on student-generated trajectories**. Weighting by teacher probabilities in Forward KL does not require teacher-generated training prefixes.

The expectation in Reverse KL is taken under the student distribution, so it naturally fits a student-sampling workflow. One common per-token feedback signal is:

```math
r_t=\log p(a_t\mid h_t)-\log q(a_t\mid h_t).
```

The signal is positive when the teacher probability exceeds the student probability and negative when it is lower. **This is a feedback signal, not a complete training algorithm; the sampled log-probability difference cannot simply be treated as an ordinary supervised loss.**

## 5. Two caveats

- **The ideal endpoint is the same**: if the student can fully represent the teacher distribution, both KL directions reach their minimum of $`0`$ at $`q=p`$. Mode-covering and mode-seeking describe tendencies under restricted approximation or approximate optimization; Reverse KL does not necessarily retain only one answer.
- **The full KL is nonnegative, but individual terms need not be**: a token contribution or a sampled log-probability difference can be negative without indicating an error in the formula.

## References

**[1] GKD: On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes. Supports combining student trajectories with different divergence objectives.** [**Paper**](https://arxiv.org/abs/2306.13649v3)

**[2] MiniLLM: Knowledge Distillation of Large Language Models. Discusses Reverse KL and the motivation to avoid overestimating low-probability regions of the teacher distribution.** [**Paper**](https://arxiv.org/abs/2306.08543v1)
