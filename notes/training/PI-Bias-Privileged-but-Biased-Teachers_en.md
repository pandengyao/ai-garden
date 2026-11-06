# Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation

[中文](./PI-Bias-Privileged-but-Biased-Teachers.md) | English

- **Source**: [Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation](https://arxiv.org/abs/2608.04794v1)
- **Paper**: [arXiv:2608.04794](https://arxiv.org/abs/2608.04794)
- **Published**: 2026-08-05
- **Scope**: A plain-language explainer based on arXiv v1 (submitted 2026-08-05, the only version so far), not a full translation. The authors are Sarthak Harne, Chinmay Karkar, Yash Pandya, Ahmed Awadallah and Akshay Nambi, from Microsoft Research. The paper says the code is provided with the supplementary material, and the arXiv page has no link to a public repository.

## In One Sentence

Self-distillation (SD) is a training method in which the same model, shown one extra piece of privileged information (PI, such as a reference solution), acts as the teacher for its own question-only self and corrects that student token by token along the solution the student wrote. It needs no reward and no larger teacher model, and it works on simple question answering. This paper proposes no new method; it is a diagnostic study: the authors carry SD over unchanged to hard question-answering, math, coding and multi-turn tool-calling tasks, look at what the model actually learns when trained with SD alone, and then trace the cause of the failure link by link. The cause is that a teacher that has seen one reference solution only pulls the student toward "the way that one solution is written"; "getting it right" is not part of its objective.

Main findings: when Qwen3-8B is trained with self-distillation alone on these four kinds of hard tasks, the training loss keeps falling, but scores do not rise, and most of them drop. With the SDPO training recipe (a published self-distillation method), the largest drop is in multi-turn tool calling in think mode (thinking at length before answering): 3.51 percentage points on average ("points" below), and 7.0 points on one item. With the recipe of another method, OPSD, math in think mode drops 4.28 points on average. The problem starts with the teacher: on math, the teacher's PI bias score (how much more willing the model becomes to continue with a piece of text after seeing the solution) for the solution it saw is 0.52; for another correct solution to the same question, it is only about 0.02 or lower in all three domains tested.

---

## 1. Key Terms

| Term | In plain words |
| --- | --- |
| Self-distillation (SD) | The same model is both student and teacher; the teacher sees one extra piece of privileged information and tells the student, token by token, what to write |
| Privileged information (PI) | Extra information shown only to the teacher during training, such as a reference solution, a hint or unit-test error messages; it is not available at test time |
| RLVR / GRPO | Reinforcement learning that uses a program's right-or-wrong verdict as the reward; GRPO is one widely used algorithm for it |
| token | The smallest unit a model reads and writes, roughly a word or part of a word |
| Solution (rollout) | One complete response that the model generates on its own for a question |
| Loss | The number training tries to push down; in self-distillation it is the gap between the student's and the teacher's distributions at each position |
| KL / JSD | Measures of how far apart two probability distributions are (such measures are called divergences); larger means farther apart. JSD is a symmetric version of KL |
| Entropy | How unsure the model is at each step; higher means more hesitant |
| think / instruct mode | Two ways to use Qwen3: think thinks at length before answering, instruct answers directly |
| EMA teacher | At each step the teacher's parameters move only a small step toward the student's latest parameters, like "a student who lags half a beat behind" |
| Transfer test | Other datasets not used for training, used to see whether the learned skill carries over elsewhere |
| Hesitation words | Words like wait, maybe and perhaps that signal uncertainty; the paper calls them uncertainty markers |
| on-path / off-path | Positions in a solution that follow the reference solution's route / positions that stray from it |
| PI bias score | A metric this paper proposes: how much more willing the model becomes to continue with a given piece of text after seeing the PI |

## 2. What Problem It Tackles

The mainstream way to improve the reasoning of large models is RLVR (reinforcement learning with verifiable rewards; its best-known algorithm is GRPO, from the DeepSeekMath paper by Shao et al., 2024, [arXiv 2402.03300](https://arxiv.org/abs/2402.03300)): the model solves a problem, a program checks the final answer, a right answer gets 1 point and a wrong one gets 0, and the model is trained on that score. The paper sums up three drawbacks:

- **Too coarse**: a solution of thousands of tokens gets a single score, so every token receives the same credit.
- **Too sparse**: on hard problems the model may never get one right; when all solutions in a group get the same score (all right or all wrong), there is no difference within the group and so no learning signal.
- **Too expensive**: every update needs scores from a verifier, plus many sampled solutions.

Self-distillation wants a denser signal without bringing in a separate, larger teacher model. It works like this:

1. The **student** (the model itself) sees only the question and writes its own solution.
2. The **teacher** is still the same model (or a slow-moving copy of its parameters), but its input has one extra piece of privileged information, such as a reference solution, a hint or unit-test error messages. Privileged information is available only during training, not at test time.
3. At every token the student wrote, the teacher gives the probability distribution for "if I could see the solution, how would I write the next token?".
4. Training pulls the student's distribution at every position toward the teacher's.

An analogy (the analogy is mine, not the paper's): a student works on a problem while "a copy of themselves flipping through the answer book" sits beside them, and for every word the student writes, that copy says "what the answer book would write here". Every token gets feedback, with no reward and no larger model needed.

The approaches side by side (I put this table together from Sections 1 and 2 of the paper):

| Approach | How it works | Problem |
| --- | --- | --- |
| RLVR (e.g. GRPO) | A program scores right or wrong, and training follows the score | The signal is too coarse, too sparse and too expensive |
| Standard distillation | A separate, larger teacher model gives a distribution per token, and the student moves toward it | Dense signal, but you need a separate, larger teacher |
| Self-distillation | The model itself, having seen privileged information, acts as the teacher and corrects the student token by token | No reward and no larger teacher needed; but nearly all positive results come from simple tasks |

**Optional: the self-distillation loss (Eq. (1) in the paper).** You can skip it without losing the thread.

```math
\mathcal{L}_{\text{SD}}(\theta)=\mathbb{E}_{(x,r)}\,\mathbb{E}_{\hat y\sim \mathrm{sg}(p_S)}\left[\frac{1}{|\hat y|}\sum_{t=1}^{|\hat y|} D\Big(\mathrm{sg}\big(p_T(\cdot\mid x,r,\hat y_{<t})\big)\;\Big\|\;p_S(\cdot\mid x,\hat y_{<t})\Big)\right]
```

- $`x`$ is the question, $`r`$ is the PI, and $`\hat y`$ is the solution the student wrote itself.
- $`p_T`$ is the next-token distribution that the teacher, having seen the PI, gives at position $`t`$, and $`p_S`$ is the student's distribution.
- $`D`$ measures how far apart the two distributions are, and $`\mathrm{sg}`$ means no gradient flows back through the teacher's side, so only the student is updated.

The whole formula says "at every token the student wrote, move the student toward the teacher", and it contains no reward term at all.

Two representative methods (the "SDPO recipe" and "OPSD recipe" below refer to their training setups):

- **SDPO** (Hübotter et al., 2026, [arXiv 2601.20802](https://arxiv.org/abs/2601.20802)): the teacher sees feedback, which can be an earlier correct solution or environment output such as unit-test errors. The original paper reports matching or beating GRPO on SciKnowEval, ToolAlpaca and LiveCodeBench with several times less compute.
- **OPSD** (Zhao et al., 2026, [arXiv 2601.18734](https://arxiv.org/abs/2601.18734)): the teacher sees the reference solution, and its parameters stay fixed at the initial model. The original paper reports beating GRPO and off-policy distillation on AIME and HMMT.

The authors argue that these positive results almost all come from narrow, low-difficulty settings, such as short multiple-choice science-knowledge questions. Another group of works uses SD as a low-weight auxiliary term in reinforcement learning, with the reward still doing the main work. Nobody has tested "SD alone on hard tasks".

The question the paper sets out to answer: **on hard tasks, trained with SD alone and no reward at all, is the model really optimizing for "getting it right", or for a proxy that happens to correlate with "getting it right" only on easy problems?**

## 3. Experimental Results

### 3.1 How the experiments were set up

**First, a reproduction in the original simple setting.** Using SDPO's official code and the hyperparameters it reported, the authors train Qwen3-8B on SciKnowEval (science-knowledge question answering), with the full solution as PI, and get the same trends as the original paper (Figure 1 in the paper): in biology and physics the loss falls and validation accuracy rises (biology about 0.31 → about 0.5, physics about 0.65 → about 0.8, read off the plot), and responses get shorter too. The authors take this to mean the implementation is sound, and every later experiment runs on this code.

**Then the same setup, unchanged, on four hard domains** (Section 4 of the paper, Appendix Table 6):

| Domain | Training data | In-domain test | Transfer tests (datasets not trained on) |
| --- | --- | --- | --- |
| General QA | MMLU-Pro (2,000 questions) | MMLU-Pro | GPQA-Diamond; SciKnowEval biology, chemistry, materials, physics |
| Math | DAPO-Math (2,000 problems) | DAPO-Math | AIME24, AIME25, OlympiadBench |
| Coding | CodeForces (2,000 problems) | CodeForces | MBPP+, HumanEval+, CodeElo, LiveCodeBench v6 |
| Multi-turn tool calling | BFCL v3 multi-turn (100 tasks) | BFCL v3 multi-turn | BFCL v4 multi-turn: base, missing function, missing parameter, long context |

Other settings:

- **Model**: mainly Qwen3-8B, tested in both think and instruct modes; Qwen3-32B is also tested on general QA.
- **PI**: by default, a full reference solution. This solution is actually one of the model's own earlier correct solutions, with the thinking removed. Two "weaker" kinds of PI are also tested: a hint of 1 to 2 sentences, and a skill card of about 500 tokens written for each problem category (it covers general methods, common formulas and common pitfalls, without revealing the answer).
- **Training objective**: only Eq. (1); the loss has no reward and no verifier. $`D`$ is the symmetric JSD, as in SDPO.
- **Two measures to keep training stable**: first, per-token clipping of the gap between the teacher's and the student's distributions, because without clipping, the half of the tokens with the largest loss on MMLU-Pro account for 98.5% of the loss, so a few tokens would dominate the gradient; second, the teacher's parameters follow the student very slowly (EMA, α=0.001; SDPO originally used 0.01).
- **Recipe**: the main experiments use the SDPO recipe; general QA and math are also redone with the OPSD recipe.
- **Baselines and metrics**: each trained model is compared only with its own version before training; no other training method is run. Math and QA use accuracy, coding uses the fraction of test cases passed, and tool calling uses the BFCL success rate; each score is the average over 4 samples per problem.
- **Other hyperparameters and compute**: learning rate 1e-5 (1e-6 for coding and tool calling), 32 problems per batch, 3 epochs; all experiments run on one machine with 8 NVIDIA B200 GPUs (Appendix B).

### 3.2 During training: the loss falls, validation does not rise

The authors say the training curves look almost the same across the four domains and both modes (Figure 2 of the paper plots Qwen3-8B's curves on the four domains):

| Metric | How it changes | Notes |
| --- | --- | --- |
| Training loss | Falls steadily | Measured by the loss, the student gets closer and closer to the teacher |
| Validation accuracy | Flat or falling | "Resembling the teacher" did not turn into "solving the problems" |
| Student entropy | Rises in most domains | Entropy measures how unsure the model is at each step. A model that is really getting better should become more certain; here it becomes more hesitant |
| Response length | Shorter in most domains; on math from about 10,000 to about 7,000 tokens (read off the plot; tool calling is the exception, see Section 6) | Getting shorter is good in short QA; on reasoning problems it fits with "less trial and error before reaching a conclusion" |

The authors' view: each signal alone has a harmless explanation, but all four appearing together points to a systematic problem. The only exception is tool calling in instruct mode, where validation improves slightly; Section 3.3 gives the reason.

### 3.3 Scores with the SDPO recipe: think mode drops in all four domains

Table 1 of the paper (SDPO recipe, average score per domain, %; before training → after training, change in parentheses, in points):

| Domain | think mode | instruct mode |
| --- | --- | --- |
| General QA | 60.93 → 59.37 (−1.56) | 52.62 → 51.05 (−1.57) |
| Math | 63.38 → 63.10 (−0.28) | 34.82 → 33.02 (−1.80) |
| Coding | 47.62 → 47.32 (−0.30) | 40.80 → 41.74 (+0.94) |
| Multi-turn tool calling | 51.36 → 47.85 (−3.51) | 28.90 → 33.58 (+4.68) |

How to read the table:

- **think mode**: all four domains drop, and tool calling drops the most, with its "missing function" sub-item down 7 points.
- **The two positive numbers**: both are in instruct mode, and the authors count neither as a real improvement. Tool calling +4.68: the training set has only 100 tasks and responses are very short (about 300 tokens on average), so the causal chain of Section 4 cannot play out. Coding +0.94 comes mainly from a +12.6 on MBPP+ alone, while the other four items all drop.

### 3.4 Same result with the OPSD recipe

General QA and math are redone with the OPSD recipe (one sampled solution per step, a fixed reference solution, and a teacher fixed at the initial model). Table 2 of the paper (change in average score per domain, points):

| Domain | think mode | instruct mode |
| --- | --- | --- |
| General QA | −1.96 | −0.65 |
| Math | −4.28 | −0.44 |

Of the 20 "test set × mode" cells, 18 show no improvement. The two recipes differ in how the gap is computed (the direction of the divergence), how the teacher's parameters are updated, how many solutions are sampled per step and how clipping is done, yet the results are the same. From this the authors conclude that the problem lies in Eq. (1), which both share, and not in some implementation detail.

### 3.5 Ruling out failed optimization, buggy code and recipe problems

- **Failed optimization?** No. The loss falls smoothly, so the optimization itself succeeds.
- **Buggy code?** No. The same code reproduces the original paper's gains on SciKnowEval, and the only thing that changes is task difficulty (there is a doubt about this point, see Section 6).
- **A problem specific to one recipe?** No. SDPO and OPSD give the same result.

The authors' conclusion: what remains can only be the objective function itself.

### 3.6 Same result across response length, problem difficulty and model size

The authors rule out, one by one, several "maybe the conditions were just wrong" explanations (Section 7 of the paper, Tables 4 and 5; the length and difficulty groups both use Qwen3-8B in think mode):

| Suspicion | How it was tested | Result |
| --- | --- | --- |
| Solutions too long, so the signal is spread thin? | Math problems split by response length into three bins, each trained separately: short (1318 to 4364 tokens), medium (4387 to 11939), long (11972 to 16384) | All three bins end below the pre-training average of 63.4, by −1.1, −0.8 and −1.6. In-domain DAPO-Math rises slightly in every bin (+1.4, +1.0, +0.6), but 8 of the 9 transfer-test cells drop, and the remaining 1 rises only 0.1. The short bin, where supervision is least spread out, is not clearly better either |
| Problems too hard, so the student cannot solve them at all? | MMLU-Pro split by the pre-training model's mean accuracy over 8 samples into easy (0.75 to 0.875), medium (0.375 to 0.625) and hard (0.125 to 0.25) bins, each trained separately | All three bins end below the pre-training average of 60.9, by −3.6, −1.4 and −1.6; the easiest bin actually drops the most |
| Model too small? | The SDPO paper reported that the gains from self-distillation grow with model size, so Qwen3-32B is trained on MMLU-Pro | Higher starting point (64.7, versus 60.9 for 8B); after training, think −0.6 and instruct −1.4; neither the training-curve signatures nor the PI bias score weaken |

Adding the two reasoning modes (Section 3.3) and the three PI forms (Section 4, link 1), the authors conclude that the result does not change across response length, problem difficulty, model size, reasoning mode or PI content.

### 3.7 Why it does work on simple tasks

The authors argue that the causal chain in Section 4 does not contradict earlier successes; it even predicts where success shows up. Simple tasks (such as four-option multiple-choice science questions) have three features:

1. Responses are short and the answer is one of a few options, so one reference solution more or less covers the whole range of "all correct answers";
2. Almost no exploration is needed, so there is little trial and error to penalize;
3. Few tokens are unrelated to correctness.

So on such tasks, writing along the lines of one solution, even with high PI bias, is about the same as learning to get it right. Once responses get longer and answers become open-ended, all three features weaken at once, and "writing like it" and "getting it right" come apart.

An analogy (the analogy is mine, not the paper's): a multiple-choice question has only A/B/C/D, so copying the option from that one solution counts as getting it right; a proof problem has many solutions, and writing along the lines of one of them does not mean you can prove it.

## 4. Why This Happens: A Five-Link Causal Chain

The authors trace the root cause to two design choices: a teacher conditioned on PI, and dense per-token supervision. Together they decouple the loss from "whether the answer is right".

First, an analogy that strings the whole chain together (the analogy is mine, not the paper's). A student works on a long math problem; the teacher beside them has seen one particular reference solution, and for every word the student writes, the teacher says "what the reference solution would write here":

1. The student uses a different, equally correct method, and the teacher still drags it toward the way that one solution is written;
2. The teacher does not care whether the student ends up right or wrong on this problem, only whether it looks like that solution;
3. What the teacher corrects most is function words, punctuation and hesitation words like "wait" and "maybe", while the key numbers and formulas get corrected less;
4. When the student tries a side path and then comes back, the teacher thinks "this step is not in the solution" and penalizes it the most;
5. In the end the student learns "to write like it", not "to get it right": less sure at every step, and stopping earlier.

```text
The teacher accepts only one solution → the loss cannot tell right from wrong → effort goes to unimportant tokens → trial and error is penalized → the student becomes "blunt"
```

Each link below was measured in the same set of Qwen3-8B training runs (with the full solution as PI).

### Link 1: the teacher memorizes "that one solution"

The authors designed the PI bias score to measure how much more willing the model becomes to continue with a given piece of text after seeing the PI. The method: when the student has written up to position $`t`$, a candidate text $`w`$ is appended, and both the teacher that has seen the solution $`y^\star`$ and the student that has not are asked "how likely are you to write this next?". The difference between their average log-probabilities is how far the PI pushes the model toward $`w`$. It needs only forward passes, no training.

**Optional: the formula for the PI bias score (Eq. (2) in the paper).** You can skip it without losing the thread.

```math
\mathrm{PS}_t(w)=\frac{1}{K}\sum_{k=1}^{K}\log\frac{p_T(w_k\mid x,y^\star,y_{<t})}{p_S(w_k\mid x,y_{<t})}
```

The authors test four kinds of candidate text (Figure 3 of the paper; the values are printed on the figure, kept here to two decimal places):

| Candidate text $`w`$ | If the teacher understood "right and wrong", it should be... | Measured: math / general QA / coding |
| --- | --- | --- |
| $`y^\star`$: the solution the teacher saw | High | **0.52 / 0.34 / 0.39** |
| $`y'`$: another correct solution to the same question | About as high as $`y^\star`$ | 0.02 / −0.01 / 0.00 |
| $`\tilde y`$: a correct solution to a different question | Low | 0.01 / 0.00 / 0.09 |
| $`y^-`$: a wrong solution to the same question | Low | 0.01 / 0.00 / −0.03 |

Only "the one it saw" scores high. Another correct solution to the same question scores about the same as the solution to an unrelated question (on coding, even lower). The authors' conclusion: **what the teacher encodes is not "correctness" but that one specific solution trajectory**, including its wording and the order of its steps.

**Would a vaguer PI work?** On math, the authors replace the full solution with hints and skill cards. The bias does go away, and the scores of all candidate texts cluster near 0 (all below 0.06 in absolute value), but the teacher also barely pushes the student anymore, and scores actually get worse. Table 3 of the paper (math, Qwen3-8B think mode, average score over four tests, %):

| PI form | Average of four tests (63.38 before training) | Change |
| --- | --- | --- |
| Full solution | 63.10 | −0.28 |
| Hint | 58.25 | −5.13 |
| Skill card | 59.92 | −3.46 |

Both ends fail: too specific, and the teacher only teaches "write it like this one"; too vague, and the teacher can teach nothing. From this the authors argue that the bias is a cause and not just a side effect: as the specificity of the PI changes, the bias changes with it, and neither end learns anything. (This set of experiments has a possible confound, see Section 6.)

### Link 2: the loss cannot tell whether the student got it right or wrong

Since the teacher recognizes only one trajectory, it has no way to judge whether the student's own solution is right. If this objective were really teaching problem solving, the loss should be larger where the student is wrong. The measurements say otherwise (Figures 4a to 4c of the paper):

- For both correct and wrong solutions, the average per-token loss is around 3.5×10⁻⁴ and the KL around 0.03; the two curves overlap throughout training, and the KL for wrong solutions is even slightly lower.
- The only metric that separates the two groups points the opposite way: the gap between the teacher's and the student's log-probabilities (absolute value) falls from about 3 to below 1 in the first 10 steps, then settles at **about 0.7 for correct solutions and about 0.45 for wrong ones**.

In other words, the learning pressure is greatest exactly on problems the student already got right. It is like a grader who marks up the correct papers the most and the wrong ones less (the analogy is mine, not the paper's). A loss that cannot tell success from failure can keep falling while accuracy does not move at all; the authors see this as the explanation for what Section 3.2 shows.

### Link 3: effort goes to tokens that do not decide the answer

The authors sort every token into 9 categories and count where the loss falls. Figure 4d of the paper (share of the total loss by token type, in one representative training step):

| Token type | Share of total loss |
| --- | --- |
| Stop words (function words like the and of), hesitation words (wait, maybe, perhaps), punctuation, whitespace | Together **55.4%** (27.4% + 11.7% + 14.6% + 1.7%) |
| Content words | 35.3% |
| Numbers, math symbols | Together 1.3% |
| Other, special tokens | Together 8.0% |

To rule out "a category has a big share just because it has many tokens", the authors also compute the average loss per token for each category (Figure 5 of the paper): hesitation words are highest, followed by stop words and content words, and numbers and special tokens are lowest. The average per-token loss of hesitation words is about 10× that of numbers (read off the plot).

In plain words: more than half of the loss goes to tone and wording, such as whether to say "wait" here, or whether to use a comma or a period; the numbers and math symbols that directly decide the answer get only 1.3% between them. The authors argue that this unifies two earlier observations: OPSD found that style tokens have higher divergence than math tokens, and Kim et al. found that SD changes the probabilities of "epistemic markers" (words that express uncertainty) by an order of magnitude more than ordinary tokens. Both describe the same loss budget being taken up mostly by these low-information tokens, and this holds throughout training, not just at the start.

### Link 4: trial and error is penalized as if it were an error

A reasoning model tries a few paths before reaching a conclusion, so even a correct solution has parts in the middle that reasonably stray from the reference solution. A teacher that has seen $`y^\star`$ cannot tell "a useful detour" from "an error".

Within each solution, the authors rank positions by "how likely the student is, at this point, to continue by writing $`y^\star`$": the top 1/4 are called on-path (following the reference route) and the bottom 1/4 off-path (straying from the reference route). To avoid mixing up "straying" and "being wrong", they first look only at correct solutions (Figure 4e of the paper; the numbers for wrong solutions appear only in the text):

| | Off-path positions | On-path positions |
| --- | --- | --- |
| Correct solutions, peak KL | About 0.31 | About 0.08 (a 4× gap) |
| Wrong solutions, peak KL | About 0.47 | About 0.10 |

On problems the student ends up getting right, what the objective penalizes most is exactly the exploration, which amounts to treating the search that reasoning needs as an error. The authors' explanation is that this is also why responses get shorter: every extra step of thinking is penalized, so the model reaches its conclusion earlier. Kim et al. observed that "the more information the teacher sees, the shorter and more confident the student's reasoning, and the worse it does on hard problems", but did not explain why; the authors argue that this link supplies the mechanism.

### Link 5: the student becomes "blunt", not "sharp"

The mean log-probability difference between teacher and student (signed) starts at about 3.1, drops to about −0.65 around step 15, and stays near 0 from step 30 on (Figure 4f of the paper). Looking at this curve alone, the student seems to have caught up with the teacher. The authors give two reasons why it has not:

1. **The mean is 0, but the spread did not shrink**: the ±1 standard deviation band stays at about ±1 throughout and does not narrow along with the mean. This is positive and negative values cancelling out, not convergence. It is like two people scoring item by item: you are 1 point higher on this item and 1 point lower on that one, so the average difference is 0, yet every item still differs by 1 point (the analogy is mine, not the paper's).
2. **The student became more hesitant**: in most domains the student's entropy rises, and so does the teacher's perplexity on the student's solutions. If the student had really learned the teacher's distribution, it should have become more certain and easier for the teacher to predict.

The authors' conclusion: the gap shrinks not because the student learned but because it collapsed. In the end the student is "flatter" than at the start: at each step it spreads probability more evenly across the candidate tokens and wraps up earlier, yet it does not solve more problems. This brings us back to the training signatures seen in Section 3.2: shorter responses and flat validation scores.

## 5. Limitations the Authors Acknowledge

- **Diagnosis only, no prescription.** This is an observational study: it only characterizes the objective's problems and proposes no fix.
- **Only one model family tested.** Just the Qwen3 family, two sizes (8B and 32B) and four domains; the authors draw no conclusions about other architectures.
- **Some gaps are smaller than random noise.** Each score is an average over 4 samples, and in some domains the score changes are smaller than the variation between runs.
- **The PI bias score has its limits.** It is a log-probability ratio computed at sampled positions, and the result depends on how the other correct solution, the unrelated question's solution and the wrong solution are chosen. It complements the conditional mutual information analysis of RLSD (a work that analyzes this kind of objective theoretically, see Section 7), but it does not actually estimate that mutual information.
- **The weak PI was generated by another model.** The hints and skill cards were generated by a different model, so the weak-PI results may partly reflect how well they were generated.
- **Methods that combine SD with rewards were not tested.** Whether methods that keep the verifiable reward and use the teacher only to adjust the weights of individual tokens (such as RLSD) can fix this paper's problem is something the authors explicitly say their experiments cannot answer, because they did not run that setting.
- **They do not claim self-distillation is ineffective in general.** The authors' conclusion is only this: in these settings, a PI-conditioned per-token objective used alone does not yield a learning signal aligned with task correctness.

## 6. Points Worth Noticing While Reading

Below are points I noticed while reading the paper that it does not discuss at length, offered for reference.

### How strong the evidence is

- **Most individual drops are small.** Many cells change by 1 to 2 points, while the error ranges after ± in the tables are between 1 and 8 points, for example AIME24 is 67.5±7.7 → 66.0±7.8; the paper also does not say whether this ± is a standard deviation or a confidence interval. The validation curves in Figure 2 look like they swing a lot, but the y-axis is very narrow; the MMLU-Pro curve, for example, stays between about 0.595 and 0.605 (read off the plot). The strength of the conclusion comes mainly from the consistency of "almost no gains anywhere", not from any single clear drop.
- **No reward-based baseline.** The tables compare only "before training" and "SD only"; GRPO was not run on the same four domains with the same data. Qwen3-8B already starts fairly high (79.1% on DAPO-Math in think mode), and without this positive reference there is no way to tell how much of the result is "SD's objective is wrong" and how much is "this data is hard to improve on anyway".
- **Only the first link of the causal chain involves an intervention.** Changing the PI form actively changes a condition; the other four links are observational statistics from the same training runs. For example, "penalizing trial and error makes responses shorter" is a reasonable explanation, but no experiment tests it directly, such as removing the loss at off-path positions and checking whether responses still get shorter. Link 5 says the teacher's perplexity also rises, but the paper gives only that one sentence, with no figure or numbers.
- **In the only intervention experiment in the causal chain, the hints and skill cards are handed to the teacher as a "correct solution".** Appendix D.2 says that both hints and skill cards are put into the hint template before they go to the teacher; the rewritten hint template for the math domain (Listing 11) begins with `Here is the correct solution for the above question:`. The hint and skill-card experiments happen to be all on math (Table 3). The teacher is told "this is the correct solution" but sees one or two sentences of hint or a skill card, which may affect the weak-PI results; the paper does not discuss this.
- **The paper is inconsistent about whether the reproduction and the hard tasks used the same setup.** Section 4 of the paper says the reproduction used SDPO's reported hyperparameters, and also says that to keep training stable on hard data, the EMA coefficient was changed from SDPO's 0.01 to 0.001 and aggressive per-token clipping was added; yet the introduction and Section 5.2 say the code, the teacher and the clipping are the same on both sides. The paper does not make clear exactly which setup the reproduction used, and the "ruling out buggy code" point (Section 3.5) rests precisely on "only the task difficulty changed".
- **Not every domain shows all four training signatures.** The text says these signatures are consistent across the four domains and both modes, but in Figure 2 the tool-calling (BFCL) responses get longer, from about 1,000 to about 1,400 tokens, and the entropy on MMLU-Pro stays roughly flat, slightly down, about 0.42 → about 0.40 (all read off the plot). Judging from response length, Figure 2 should be showing think mode (the paper says BFCL responses in instruct mode average only about 300 tokens); the paper does not give the training curves for instruct mode.

### Small issues in the manuscript (none affect the main conclusions)

- **The coding-domain average.** Section 5.2 says that averaged over test sets and both modes, coding scores still drop. But by Table 1, think mode is −0.30 and instruct mode +0.94, so the average over the two modes is +0.32.
- **The lengths of hints and skill cards are given in several ways.** Skill cards: Section 4 says about 500 tokens, Appendix A.2 says about 500 words, and the generation prompt in Appendix D.4 asks for 250 to 400 words. Hints: Section 4 and Appendix A.2 say one to two sentences, while the generation prompt in Appendix D.3 says at most 1 to 3 sentences.

## 7. Relation to Related Work

The authors set their results side by side with two earlier works:

| Work | Conclusion | Relation to this paper |
| --- | --- | --- |
| RLSD (Yang et al., 2026, [arXiv 2604.03128](https://arxiv.org/abs/2604.03128)) | Proves theoretically that OPSD's loss contains an irreducible conditional mutual information term $`I(Y_t;R\mid X,Y_{<t})`$: the teacher fits a single PI-conditioned trajectory rather than the distribution of all correct solutions, and it teaches this "leak" to the student | The authors see it as stopping at theory; this paper's PI bias score is its experimental counterpart |
| Kim et al. (2026, [arXiv 2603.24472](https://arxiv.org/abs/2603.24472)) | The more information the teacher sees, the shorter and more confident the student's reasoning and the faster in-domain optimization, but scores on out-of-distribution and harder problems drop by up to about 40% (Qwen3 and DeepSeek-R1-Distill series) | Describes only the phenomenon; link 4 in Section 4 of this paper gives the mechanism |
| This paper | SD alone does not improve hard tasks, because of a causal chain that runs from PI bias to a blunted student | The authors see the two works above as two ends of the same mechanism |

**How it relates to methods that keep the reward.** The authors sum up the division of labor in this kind of work: the verifiable reward handles only right and wrong, not how things are written; the SD term handles how things are written and hardly cares about right and wrong. RLSD's fix: whether a token is rewarded or penalized is still decided by the verifier's right-or-wrong verdict, and the teacher is used only to adjust how much weight each token gets. This keeps the per-token density and drops the biased term. The authors ran no experiments on whether this combination fixes this paper's problem (see Section 5). Their judgment: the bias enters at the very first link (the teacher accepts only one trajectory), so the most targeted fix is to make the dense objective reflect the set of "all correct continuations", not just one of them.

**Other works.**

- SDPO (Hübotter et al., 2026) and OPSD (Zhao et al., 2026) are the two recipes this paper uses; Section 2 covers how they work and what their original papers reported, and Section 3.7 covers how the authors explain the difference between the two sets of results.
- When the paper's introduction presents the practice of "showing privileged information to a self-teacher", it cites SDFT (Shenfeld et al., 2026, [arXiv 2601.19897](https://arxiv.org/abs/2601.19897)).
- One more concurrent work that the paper does not cite but that reaches a similar conclusion: DAPD (Wu et al., 2026, [arXiv 2608.01735](https://arxiv.org/abs/2608.01735)) finds from a different angle that OPSD teaches the model to "force out an answer even when it cannot work one out", and that the longer it trains, the lower its scores. Both papers trace the problem to "the teacher that has seen the solution"; DAPD also offers a fix, while this paper only diagnoses.

## 8. Summary

The paper's conclusion is direct: **on hard tasks, PI-conditioned per-token self-distillation used alone teaches "writing like that one solution", not "getting it right".** The teacher has seen one reference solution, and the per-token targets it gives are led by how that one trajectory is written. The student learns from them, the loss cannot tell right from wrong, effort goes to function words, punctuation and hesitation words, trial and error gets penalized, and in the end the student becomes "flatter" and stops earlier, without solving more problems.

The evidence comes from many settings: four domains, two reasoning modes, two recipes and three PI forms, plus different response lengths and problem difficulties and two sizes, 8B and 32B; scores almost nowhere go up. But most individual drops are 1 to 2 points, only the Qwen3 family was tested, the authors offer no fix, and they certainly do not claim self-distillation is ineffective in general. Their advice to practitioners: a falling SD loss does not show that the model has learned anything; look at validation accuracy, since only it can tell the two cases apart. Before training, you can screen the PI with the PI bias score at low cost, with only forward passes for the four candidate texts on a small number of prefixes: if the teacher scores "the solution it saw" far above "another correct solution", it is passing on a trajectory, not a skill; if all four candidate texts score very low, this PI passes on nothing. The specificity of the PI is also not a hyperparameter where "just pick a middle value" works: full solutions, skill cards and one- or two-sentence hints were all tried, and none of them worked.

---

## Where Things Are in the Paper

| In this note | In the paper |
| --- | --- |
| Problem and motivation, the self-distillation loss | Sections 1 and 2; Eq. (1) in Section 3 |
| Experimental setup | Section 4; Appendix A (Table 6), Appendix B (Table 7) |
| Reproduction in the original simple setting | Section 4, Figure 1 |
| Training signatures | Sections 5 and 5.1, Figure 2 |
| Scores for the two recipes, explanations ruled out | Section 5.2, Tables 1 and 2 |
| Response length, problem difficulty, model size | Section 7, Tables 4 and 5 |
| Why it works on simple tasks | Section 8 |
| Overview of the causal chain | Section 1, Section 3 (two properties), start of Section 6 |
| Link 1: PI bias score, weak PI | Section 6.1, Eq. (2), Figure 3, Table 3, Appendix C, Appendix E |
| Link 2: the loss cannot tell right from wrong | Section 6.2, Figures 4a to 4c |
| Link 3: which tokens the loss falls on | Section 6.3, Figure 4d, Figure 5 |
| Link 4: trial and error is penalized | Section 6.4, Figure 4e |
| Link 5: the student becomes "blunt" | Section 6.5, Figure 4f |
| Limitations the authors acknowledge, practical advice, combining with rewards | Section 8 |
| Relation to related work | End of Section 1, Section 2 |
| How hints and skill cards are built, and their templates | Appendix A.2, Appendix C, Appendices D.2 to D.4 |
