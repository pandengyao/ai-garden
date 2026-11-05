# A Model That Teaches Itself (OPSD)

[中文](./On-Policy-Self-Distillation.md) | English

- **Source**: [Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models](https://arxiv.org/abs/2601.18734v3)
- **Paper**: [arXiv:2601.18734](https://arxiv.org/abs/2601.18734)
- **Official resources**: [siyan-zhao/OPSD](https://github.com/siyan-zhao/OPSD)
- **Published**: 2026-01-26
- **Scope**: A plain-language explainer based on arXiv v3 (2026-03-20), not a full translation. The authors are from UCLA, HKU and Meta Superintelligence Labs. The figures are the paper's own, and the table numbers come from the paper; values marked "about" in the captions are approximate readings from the curves.

## In One Sentence

The same model plays two roles: a "student" that sees only the problem, and a "teacher" that has seen the reference solution. The student writes its own solution, the teacher grades it token by token, telling the student "this is how I would write this step", and the student moves toward the teacher. No separate larger teacher model is needed, and there is no need to sample each problem many times as reinforcement learning does.

On competition math with Qwen3 at 1.7B, 4B and 8B, it matches or slightly beats GRPO (a mainstream reinforcement learning method) while generating far fewer tokens.

## 1. What Problem It Solves

There are three common ways to make an LLM better at math reasoning, and each has a flaw:

| Method | How it works | Flaw |
| --- | --- | --- |
| SFT (supervised fine-tuning) | Have the model copy reference solutions | It trains on someone else's reasoning but must write its own at test time, so the two don't match (exposure bias), and it generalizes poorly |
| RL such as GRPO | Have the model solve each problem 8 times, scoring 1 for right and 0 for wrong | Expensive; it only says right or wrong at the end, not which step went wrong; when all 8 are right or all wrong the scores don't differ and the work is wasted |
| On-policy distillation | The student writes, and a stronger model guides it token by token | Works well, but needs a separate, larger teacher model |

The authors ask: today's models already reason fairly well, so can a model **teach itself**?

## 2. Core Idea: The Self That Saw the Answer Teaches the Self That Didn't

The inspiration is how people learn. After getting a problem wrong, you open the answer, understand why each step goes the way it does, then find the step where you went astray. The authors' judgment is that **understanding a ready-made correct solution is easier than coming up with one from scratch** (much like "verification is easier than generation"). So the same model, once it has seen the answer, can serve as a competent "grader".

How it works (paper Figures 1 and 2):

![OPSD overview](./img/On-Policy-Self-Distillation-fig1-overview.png)

*Figure 1 (from the paper): take a problem x and reference solution y\* from the dataset and build two prompts for the same model. The student sees only x and samples a solution ŷ; the teacher sees x and y\* and gives a next-token distribution at every position of ŷ. The training objective is the per-token distribution gap, and gradients flow only through the student side.*

1. **Student prompt**: just the problem, for example "find the derivative of f(x)=3x²+2x−5 at x=2".
2. **Teacher prompt**: the problem + a reference solution ("first find f′(x)=6x+2, then substitute to get 14") + one guiding sentence, "after understanding the reference solution, please try to solve this problem using your own approach".
3. The student writes a complete solution its own way.
4. Feed the student's solution, unchanged, into the "teacher" prompt and run one forward pass. The teacher **doesn't write anything itself**; at each position it only gives the probability distribution of "if it were me, what the next token would most likely be".
5. Training objective: make the student's probability distribution at each position as close as possible to the teacher's. Gradients update only the student side.

![Student and teacher prompt example](./img/On-Policy-Self-Distillation-fig2-prompts.png)

*Figure 2 (from the paper): the red box at the top is the student prompt and the green box below is the teacher prompt. The teacher additionally has the reference solution and the bold guiding sentence.*

Teacher and student share **the same parameters**; the only difference is whether the prompt contains the answer. Hence "self-distillation"; and because training uses what the student wrote itself, it is "on-policy".

## 3. How It Compares with Other Methods

The paper's Table 1, in plain terms:

| Criterion | SFT | GRPO | On-policy distillation | OPSD |
| --- | --- | --- | --- | --- |
| Trains on its own outputs (not copied ones) | No | Yes | Yes | Yes |
| Feedback on every token (not just final right or wrong) | Yes | No | Yes | Yes |
| Low sampling cost | Yes | No | Yes | Yes |
| No external teacher model | Yes | Yes | No | Yes |

OPSD is the only one with all four.

One more key difference: GRPO and STaR (another self-training method) only reward "the whole problem solved", so a wrong answer gives no learning signal. OPSD can still tell the student, token by token, "the teacher would write this differently here" even when the final answer is wrong, so the signal never vanishes (the paper derives this in Appendix D).

## 4. The Details That Make It Work

### 4.1 Downweighting filler words: per-token clipping

The authors found that teacher and student disagree most not on math content but on filler and connective words such as "wait", "hmm", "so" and "maybe". The paper's Table 5 reports the mean per-token KL over 10 problems for three token categories (a larger value means teacher and student disagree more on that kind of token, so there is more for the student to learn):

| Student mode | Teacher mode | 1.7B style | 1.7B math | 1.7B other | 4B style | 4B math | 4B other | 8B style | 8B math | 8B other |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Thinking off | Thinking off | 0.68 | 0.12 | 0.11 | 0.61 | 0.06 | 0.10 | 0.56 | 0.05 | 0.11 |
| Thinking on | Thinking off | 0.51 | 0.10 | 0.17 | 0.41 | 0.05 | 0.18 | 0.33 | 0.05 | 0.15 |
| Thinking on | Thinking on | 0.51 | 0.09 | 0.08 | 0.50 | 0.04 | 0.09 | 0.42 | 0.04 | 0.08 |
| **Thinking off** | **Thinking on** | **0.85** | **0.14** | 0.25 | **0.92** | **0.10** | 0.29 | **0.79** | **0.06** | 0.25 |

*Table 5 (paper Appendix B): "style" tokens are words like maybe, wait, so and therefore, and "math" tokens are words like equation, factor, sum and root; the full word lists are in the paper's Appendix C.*

In every row, the KL on style tokens is about 5–13 times that on math tokens. Left alone, the model would spend its effort learning a speaking style.

The fix: cap each vocabulary entry's contribution to the divergence at each position at a threshold τ, and clip anything above it.

![Effect of per-token clipping](./img/On-Policy-Self-Distillation-fig4-kl-clipping.png)

*Figure 4 (from the paper, Qwen3-1.7B, AIME24): the red dashed line is without clipping and the blue solid line is with it. Without clipping, accuracy starts falling after step 25 and drops to about 49 at step 100, below the 51.5 before training; with clipping it climbs steadily to about 57.*

### 4.2 The teacher is frozen at the starting model

The student changes during training, but the teacher stays the initial version and is never updated. The authors say this is more stable and also acts as a constraint that keeps the model from drifting too far from where it started.

### 4.3 The student "answers directly", the teacher "thinks while answering"

Qwen3 has a thinking mode that can be on or off. The authors tried all four combinations and found that **student with thinking off, teacher with thinking on** gives the strongest signal on math tokens (the bold row of Table 5 above: for all three sizes, this row has the highest math-token KL) and the best final results, so all later experiments use it.

### 4.4 Forward KL to measure the gap

There are several formulas for "how far apart student and teacher are". On Qwen3-1.7B, AIME25 (paper Table 3, Avg@12, %):

| Divergence | Before training | Step 50 | Step 100 |
| --- | --- | --- | --- |
| Forward KL | 36.7 | **43.9** | 41.1 |
| Reverse KL | 36.7 | 37.5 | 35.0 |
| JSD | 36.7 | 36.9 | 39.0 |

Forward KL is clearly best, so the paper uses it throughout. Note that step 100 falls back from step 50.

### 4.5 Full-vocabulary matching vs matching only the sampled token

- Full vocabulary: at each position, compare teacher and student probabilities for every candidate token. More information, but higher memory use.
- Sampled token only: look only at the token the student actually wrote, take the difference between the probabilities teacher and student give it as a reward, and update as in reinforcement learning. Saves memory.

On Qwen3-4B with a 2048-token student generation length (paper Table 4, pass@8, %):

| Variant | AIME25 | HMMT25 |
| --- | --- | --- |
| Full-vocabulary matching | **84.1** | **60.0** |
| Sampled token only | 82.1 | 57.3 |

Full vocabulary is better, at the cost of memory.

## 5. Results

**Setup**: Qwen3-1.7B / 4B / 8B (instruct versions), trained on the math subset of OpenThoughts (up to 30 thousand problems with worked solutions), and tested on three math competitions: AIME 2024, AIME 2025 and HMMT 2025. Each problem is sampled 12 times and the mean accuracy is reported (Avg@12). All training uses LoRA on 8 A100 or H100 GPUs.

**Training cost** (paper Table 6):

| Setting | GRPO | OPSD |
| --- | --- | --- |
| Samples per problem | 8 | 1 |
| Max tokens per sample | 16,000 | 1,024 |
| Training steps | 500 | 100 |

**Main results** (paper Table 2, Avg@12, %):

| Model | Method | AIME24 | AIME25 | HMMT25 | Average |
| --- | --- | --- | --- | --- | --- |
| Qwen3-8B | Base | 75.8 | 65.6 | 43.9 | 61.8 |
| | +SFT | 72.3 | 64.2 | 42.9 | 59.8 |
| | +GRPO | 76.4 | 68.9 | **46.7** | 64.0 |
| | +OPSD | **77.8** | **70.8** | 45.8 | **64.8** |
| Qwen3-4B | Base | 74.9 | 66.4 | 42.2 | 61.2 |
| | +SFT | 70.2 | 62.3 | 43.4 | 58.6 |
| | +GRPO | 75.6 | 68.1 | 44.4 | 62.7 |
| | +OPSD | **76.4** | **68.3** | **46.1** | **63.6** |
| Qwen3-1.7B | Base | 51.5 | 36.7 | 23.1 | 37.1 |
| | +SFT | 48.4 | 36.3 | 22.7 | 35.8 |
| | +GRPO | 51.1 | 38.3 | 23.7 | 37.7 |
| | +OPSD | **57.2** | **43.9** | **29.2** | **43.4** |

How to read the table:

- **OPSD has the best average at all three sizes**. 1.7B gains the most (37.1 → 43.4, +6.3); at 4B and 8B it is about 1 point above GRPO. GRPO is slightly better on HMMT25 at 8B.
- **SFT actually lowers scores**. The authors' explanation: the dataset's reference solutions are concise, and after learning to copy them the model also thinks for less at test time. OPSD uses the same data, but instead of copying, it has "the self that saw the answer" judge, so it avoids this problem.
- **Why GRPO falls short**: Figure 3 shows that within 100 steps, more than half of GRPO's batches have "all 8 right or all 8 wrong", so rewards don't differ, the gradient is zero and the compute is wasted.

**Fewer tokens**: at the same number of training steps, OPSD generates far fewer tokens than GRPO yet scores higher (Figure 3).

![Training efficiency of OPSD vs GRPO](./img/On-Policy-Self-Distillation-fig3-token-efficiency.png)

*Figure 3 (from the paper, Qwen3-1.7B): the first three panels show accuracy on the three test sets over training steps, blue for OPSD and red for GRPO. The fourth panel puts cumulative generated tokens on the x-axis: OPSD pushes the average above 42 with about 3 million tokens, while GRPO is still around 38 after about 26 million. The rightmost panel is the share of GRPO batches where "all 8 answers in a group get the same reward", mostly between 55% and 95%; those batches give no gradient.*

**Longer generation is not better**: whether the student writes 1024 or 4096 tokens per sample makes no consistent difference. The authors explain that early tokens are the forks in the reasoning and matter most; the longer the text, the easier the later part is for the teacher to predict, so it carries less signal.

![Effect of student generation length](./img/On-Policy-Self-Distillation-fig5-gen-length.png)

*Figure 5 (from the paper, Qwen3-1.7B): blue is 1024 tokens and red is 4096. On AIME25, 1024 reaches its peak earlier; on AIME24, 4096 jumps to about 58.6 at step 50 but then falls back. Which is better differs between the two test sets, which is why the authors say longer generation brings no consistent gain.*

## 6. Limitations the Authors Acknowledge

- Only tested up to 8B; whether it still works on larger models is unknown.
- It doesn't use the signal of whether the student's final answer is right, only distribution matching. Adding answer verification might help.
- **It fails when problems are too hard**: if a problem exceeds the model's comprehension, it can't understand the answer even after seeing it, so it can't be a competent teacher. The authors suggest curriculum learning, raising problem difficulty as the model improves.
- The clipping threshold τ was not tuned; tuning it might do better.

## 7. Points Worth Noticing While Reading

The following are points noticed while reading the paper that it does not discuss at length, offered for reference:

- **Best checkpoints are reported**: OPSD is evaluated every 20 steps and the best score within 100 steps is reported; GRPO reports its peak within 500 steps. Both pick the best on the test set, and no variance across runs is given. A gap of about 1 point at 4B and 8B may not exceed random variation.
- **The advantage shrinks on larger models**: 1.7B gains 6 points, while 4B and 8B are only about 1 point above GRPO. The paper has no data on whether the advantage holds at larger scale.
- **Most ablations use only 1.7B**: the divergence, generation length and clipping ablations are all on Qwen3-1.7B; the full-vocabulary vs sampled-token comparison is on 4B and uses pass@8 rather than the main table's Avg@12.
- **Scores fall back later in training**: forward KL is 43.9 at step 50 and drops to 41.1 at step 100. The method converges quickly but may regress with longer training, so early stopping is needed.
- **The GRPO setup works against it**: the authors say most GRPO batches on this data get identical rewards. That means the data is either too easy or too hard for Qwen3, and with data of better-suited difficulty GRPO might perform differently.

## 8. Summary

The idea behind OPSD is simple: **use one model, one copy seeing the answer and one not, and let the one that saw it guide the other token by token**. It gets several benefits at once: training on the model's own outputs, feedback on every token, a single sample per problem, and no extra teacher model.

On competition math, it matches or slightly beats GRPO with far less generation, and the gain is especially large on small models. It requires the model to be capable enough to understand the reference solution, so it suits problems "at the edge of the model's ability".

Two concurrent works take a similar approach: [SDPO](https://arxiv.org/abs/2601.20802) shows the teacher environment feedback as the "answer"; [SDFT](https://arxiv.org/abs/2601.19897) applies the same self-distillation to continual learning.
