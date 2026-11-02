# On-Policy Distillation (OPD): New Papers from August to October 2026, and the GitHub Paper Lists

[中文](./On-Policy-Distillation-Literature-Review.md) | English

- **Research date**: 2026-11-02 (evidence cutoff: arXiv IDs up to 2610; the latest paper was submitted on 2026-10-30)
- **Scope**: on-policy distillation (OPD) papers first submitted to arXiv in August–October 2026, and the GitHub repositories that collect OPD papers. Of 704 candidates, classified one by one from their abstracts, 540 are core papers that meet the OPD definition and 136 are related work.
- **Structure**: this page is the survey itself; one-line summaries and key results for all 676 papers are in the [paper catalog](./On-Policy-Distillation-Literature-Review-Papers_en.md).
- **Basis**: classification relies only on abstracts and comments, not full texts. Every per-paper number in the text has been checked against that paper's arXiv abstract; paper counts come from this survey's classification of the candidates.

## Conclusions

1. **The field is hot and still accelerating.** Of 704 candidates, 540 are core OPD papers (meeting C1+C2 in Section 1): 128 in August, 200 in September and 212 in October. Another 136 are related work, 35 of them industrial technical reports that use OPD.
2. **This quarter's biggest theme is "what OPD actually does", and most answers run against intuition.** On data, 1 query, 4 prompts or 8 prompts come close to full-data results. On supervision density, applying teacher supervision to only 0.05%–1% of tokens matches full-token training. On the signal, one paper replaces the teacher signal with a fixed negative advantage and does about as well. On transfer, reverse-KL OPD transfers skills, not facts. On sampling, for most teacher-student pairs, distilling on offline samples from the initial student works better. On merging, in a controlled comparison multi-teacher OPD is no more accurate than SFT merging, yet uses 14.8–23.1× the training GPU-hours of SFT. See Section 2.
3. **On-policy self-distillation (OPSD) is the largest branch and the most disputed.** Here the same model, given privileged information such as a reference answer, acts as the teacher; 236 core papers, 44%, fall in this group. Meanwhile more than ten analysis papers find that a correct reference answer does not reliably help and a solution to a different problem works just as well, that OPSD works only within a narrow compatibility window, and that on multi-turn agent tasks it does worse than plain GRPO. See Section 3.
4. **The relationship between OPD and RL is now fairly clear.** OPD followed by RL beats training the two jointly. Even when OPD brings no immediate accuracy gain, doing it before RL raises RL's final ceiling. Joint training is unstable because the two signals' gradient magnitudes differ by a wide margin. See Section 5.
5. **Multi-teacher OPD (MOPD) has become a common way for industry to merge expert models**: technical reports for NVIDIA Nemotron 3.5, Xiaomi MiMo-V2.6, AMD Instella-MoE, Motif 3 and SenseTime SenseNova-U1.5 all use it. New academic papers focus on three problems: uneven signal scales across domains, misallocated token budgets, and teacher routing. On the other side, one paper proves that within a shared basin MOPD is, to second order, exactly Fisher merging, and another gives a closed-form solution that needs no training at all. See Section 4.
6. **GitHub has three large, active paper lists**: chrisliu298, thinkwee and nick7nlp. But their coverage of the last three months overlaps little, and none has yet added papers from mid-to-late October. Of the 75 core papers rated importance 3 here, 23 appear in no list. See Section 8.

## 1 Scope and Method

**Inclusion criteria** follow the definition used by thinkwee/AwesomeOPD. A paper counts as OPD only if it meets both conditions:

- C1: during training, the student samples trajectories from its own current policy;
- C2: a teacher supervises those student trajectories, in the form of per-token logits / log-probs / KL, a sequence-level reward, a discriminator score or verbal feedback.

OPSD is a special case of OPD: teacher and student are the same model, but the teacher also receives privileged context (a reference answer, feedback, hints, a longer context and so on).

**The candidate pool (704 papers)** has two parts:

- arXiv full-text search with 6 queries: `"on-policy distillation"`, `"on-policy self-distillation"`, `"self-distillation" AND "on-policy"`, `"OPD" AND distillation`, `"on-policy" AND "distill"`, `"self-distillation" AND privileged`, keeping results from 2608 on.
- Entries from 2608 on in 8 GitHub lists. 41 of these cannot be found by the keyword search and were added from the lists.

The search was rerun on November 2, adding 2 papers from October 30. The 296 results that the keyword filter dropped were also rechecked by keyword, and no OPD paper turned up.

**Classification**: each paper's abstract and comments were read to label relevance (core / related / irrelevant), method direction, domain, teacher type, importance (1–3) and a one-line summary. The full results are in the [paper catalog](./On-Policy-Distillation-Literature-Review-Papers_en.md).

**Limitations**:

- Classification relies only on abstracts. The abstract of Xiaomi's MiMo-V2.6 technical report does not mention OPD, but the thinkwee and kissshhot lists both include it as an MOPD practice based on the full text, so this survey reclassifies it as related work.
- Two withdrawn papers stay in the catalog but are not cited here: 2608.04408 (v2/v3 withdrawn, with the comments field reading "false information") and 2609.38777 (wrong template; the authors plan to resubmit).
- Importance ratings are subjective.

## 2 Mechanism Analysis: What OPD Actually Does

This quarter, 71 papers make analysis or theory their main contribution, and another 48 carry an analysis label. Most of them refute or revise common assumptions.

### 2.1 Data: very few prompts are needed

| Paper | Finding |
| --- | --- |
| [2609.04172](https://arxiv.org/abs/2609.04172) Rethinking OPD II: One Training Example | A single query recovers most of full-data OPD's gain. Measured by semantic clusters, one query covers 71.5% of the full-data state space by step 300; with 16 semantically different queries, coverage reaches 98.9% and results match full data. The authors' explanation: OPD has far more data than it needs, and what limits it is how fast the algorithm absorbs it. This repo has [a note with the full paper and a Chinese translation](./One-Shot-On-Policy-Distillation_en.md) |
| [2609.14193](https://arxiv.org/abs/2609.14193) Data-Free OPD | 8 real prompts work about as well as 17k problems; with no seed examples and only 64 self-generated questions, it matches full-data OPD. In the multi-teacher setting, 1k generated questions are worth about 7k real post-training examples |
| [2609.37377](https://arxiv.org/abs/2609.37377) Beyond Prompt Count | 4 DAPO prompts match the math score of 3840 DeepMath prompts. But whether a prompt helps depends on the teacher: changing only the teacher can swap the relative effectiveness of math and code prompts. Targeted prompt selection is not reliably better than uniform random sampling either |
| [2608.16647](https://arxiv.org/abs/2608.16647) Every Coin Has Two Sides | Training difficulty barely matters, and even problems the teacher itself cannot solve are useful. OPD transfers reasoning behavior, not specific answers. How strongly it transfers depends on whether teacher and student share an origin: same-origin pairs approach the teacher across languages and domains, while cross-origin pairs mostly fit the training distribution |

### 2.2 Supervision density: a handful of tokens is enough

- [2609.04565](https://arxiv.org/abs/2609.04565) Extremely Sparse Supervision: supervising only 1–2 tokens per reasoning trajectory (about 0.05% of all tokens) matches or beats full-token training in most cases. The result holds across 9 teacher-student configurations.
- [2609.24432](https://arxiv.org/abs/2609.24432) 1% of Tokens Can Be Enough: selects tokens by the noise in gradient estimation, using a signal-to-noise-style information-efficiency ratio (IER). At token budgets of 0.1%–1%, it matches or exceeds full OPD without token selection.
- [2609.33791](https://arxiv.org/abs/2609.33791) Do We Really Need KL Divergence?: OPD does not have to use KL. Scoring each token ±1, +1 where the teacher's probability is above the student's and −1 where it is below, reproduces the training mode of reverse-KL OPD. What decides the outcome is whether the few tokens with large teacher-student disagreement are updated toward the teacher.
- A caution: [2609.22109](https://arxiv.org/abs/2609.22109) shows that when token selectors are compared under one shared learning rate, the selector and the learning rate get entangled. With LoRA on GSM8K, the gap between dense and sparse supervision is 10.1 percentage points at learning rate 1e-4 but only 5.1 at 5e-5; of the 6 pairwise significance calls between selectors, 2 flip between adjacent learning rates.

### 2.3 The signal: what does the teacher contribute?

- [2608.31046](https://arxiv.org/abs/2608.31046) Does OPD Really Distill?: teacher supervision is quite noisy, and noisier for larger teachers, yet the student is insensitive to that noise. OPD's gain comes mainly from pushing down the student's low-probability tokens. Replacing the teacher's advantages with one fixed negative advantage performs about as well. The supervision-free method built on this, OPSA, raises Avg@32 on AIME24 by 35.41 points over the base model and by 16.77 points over OPD.
- [2610.03185](https://arxiv.org/abs/2610.03185) Gains and Collapse: from an RL view, the teacher acts as an implicit reward model. OPD makes correct answers easier to sample but does not expand the student's capability boundary; when the implicit reward diverges from quality, it amplifies verbose, repetitive answers, which amounts to reward hacking.
- [2610.03529](https://arxiv.org/abs/2610.03529) Divergence controls entropy: proves that forward KL pushes the student's entropy above the teacher's while reverse KL lowers it. So the low entropy of OPD students comes from per-token reverse KL, not from on-policy sampling itself.
- [2610.09639](https://arxiv.org/abs/2610.09639) OPD Teaches New Skills but Not New Knowledge: on controlled synthetic tasks, reverse-KL OPD reliably transfers compositional skill but almost no factual knowledge; switching to forward KL restores factual transfer.
- [2610.39020](https://arxiv.org/abs/2610.39020) Distilling the Shape of Uncertainty: OPD teaches the student not only which candidate tokens to consider but also where to keep reasoning paths open. The authors characterize the latter by the sequence of per-token entropies, and interventions show it causally drives OPD's gains. The entropy shape correlation (ESC) measured before distillation picks the best teacher for both students.
- [2609.35210](https://arxiv.org/abs/2609.35210) A mechanistic-interpretability analysis with sparse crosscoders: OPD neither creates new features nor carries over the teacher's. For over 98% of the student's frequently used features, the firing rate changes by no more than 20%.
- [2610.13205](https://arxiv.org/abs/2610.13205): a stronger expert is not necessarily a better teacher. Policy differences induced by task training (RL / SFT) transfer reliably, while differences that come only from scale barely transfer.

### 2.4 Is on-policy sampling necessary?

- [2610.11291](https://arxiv.org/abs/2610.11291) When Do We Need OPD?: Semi-OPD, which samples once offline from the initial student, beats OPD in 14 of 17 teacher-student pairs (1.5B–235B), with up to 13.6% higher accuracy and up to 11.4× faster training. OPD pays off only when the teacher's and student's output-token overlap is high. The reason: for misaligned pairs, the student's trajectory drifts further from the teacher the longer it runs, weakening the distillation signal.
- [2609.35259](https://arxiv.org/abs/2609.35259) On-Policy or Off-Policy?: a controlled experiment that varies the rollout policy, the KL direction and the learning rate separately. The rollout policy turns out not to play a central role: forward KL is robust to the rollout policy, and only reverse KL prefers student samples; the learning rate determines forgetting and update sparsity.
- [2610.33740](https://arxiv.org/abs/2610.33740): a theoretical explanation from distribution matching: OPD has the edge when the model is close to the target distribution and loses out when it is far.
- [2610.30844](https://arxiv.org/abs/2610.30844): the sample complexity of reverse-KL distillation. Online, if only the probability of the sampled action can be observed, substantially more data may be needed; offline, both kinds of feedback need data of the same order.

### 2.5 Failure modes

| Symptom | Paper | Key points |
| --- | --- | --- |
| Length inflation | [2609.20511](https://arxiv.org/abs/2609.20511) When EOS Tokens Disagree | The base student and the post-trained teacher put their stopping probability on different EOS tokens. OPD suppresses the student's preferred termination token without transferring the teacher's. Aligning the decoding stop set alone is not enough; functionally equivalent EOS tokens have to be treated as one semantic stop action |
| Small models do not learn "when to stop" | [2609.37326](https://arxiv.org/abs/2609.37326) Solving Without Stopping | Solving ability transfers, but in thinking mode "when to end the reasoning" does not: the teacher signals a stop almost only where the student already stops. Also, the student's single-attempt ceiling never exceeds what it could reach with many attempts before training |
| Fails on problems the student gets wrong | [2610.18011](https://arxiv.org/abs/2610.18011) Correcting or Continuing? | When training only on problems the student currently fails, all 8 configurations decline (two-sided sign test p=0.0078) even as the training KL keeps falling; when training is not concentrated on failures, the same pipeline gains 4.6 percentage points |
| Learning signal vanishes early | [2610.11247](https://arxiv.org/abs/2610.11247) | After 200 steps, OPD with a large teacher cuts the loss by only 25.1%, against 96.2% with a self-RL teacher. Student representations barely change (linear CKA above 0.98 at every layer) |
| Degenerate agreement | [2608.09836](https://arxiv.org/abs/2608.09836) Mismatch Matters | The student can reach near-perfect token agreement with the teacher through repetitive loops. The authors instead handle two kinds of mismatch: tokens the student generates that the teacher thinks should not appear, and tokens the teacher prefers that the student rarely samples |
| Loss of diversity | [2608.29846](https://arxiv.org/abs/2608.29846) IDA-OPD, [2608.11829](https://arxiv.org/abs/2608.11829) | Sampled-token OPD can raise pass@1 while pass@k stalls; it can improve results at small sampling budgets while lowering pass@K at large ones. The latter proposes TAS@K for choosing a teacher before training |
| Gains depend on pipeline order | [2609.31900](https://arxiv.org/abs/2609.31900) | OPD's effect depends on teacher-student compatibility, not just teacher scale. Strengthening the student with RLVR first and then distilling from the same teacher makes it regress; conversely, adapting the teacher with RLVR and warming up the student with SFT raises average accuracy from 29.2% to 43.8% |
| Warm-up | [2608.06802](https://arxiv.org/abs/2608.06802) Simple-OPD | Warm-up mainly transfers a teacher-compatible thinking pattern: warming up on incorrect teacher rollouts works about as well as on correct ones, and LoRA trained to near saturation beats full-parameter SFT |

### 2.6 Scaling

[2609.32722](https://arxiv.org/abs/2609.32722) Scaling Properties of Same-Family OPD: early in training, accuracy rises roughly linearly with the square root of the reverse KL. In every weak-to-strong pair, the student's peak exceeds the teacher's. At a matched score, smaller teachers transfer better, so a teacher's score alone does not define its supervision value. The authors also fit power laws for how the peak scales with student and teacher parameter counts.

## 3 On-Policy Self-Distillation (OPSD): The Most Papers, the Most Disputes

### 3.1 Analyses that question the privileged information

| Paper | Conclusion |
| --- | --- |
| [2608.18271](https://arxiv.org/abs/2608.18271) Rethinking PI in OPSD | The benefit of a correct reference answer is inconsistent; on several math benchmarks, a solution to a different problem works better |
| [2608.09228](https://arxiv.org/abs/2608.09228) OP²SD | Replacing the reference with another problem and its solution, with everything else unchanged, still performs on par with OPSD. What mainly matters is that the reference changes the context the teacher works in, not the answer itself |
| [2609.20612](https://arxiv.org/abs/2609.20612) What Does PI Add? | Reference-free distillation already explains most of Qwen3-1.7B's improvement; replacing direct-answer rollouts with long thinking rollouts turns the gains into losses |
| [2608.04794](https://arxiv.org/abs/2608.04794) Privileged, but Biased | On hard tasks, the per-token loss keeps falling while validation accuracy does not improve and instead degrades. The cause is that the teacher's target is pulled toward that one particular reference trajectory |
| [2608.09263](https://arxiv.org/abs/2608.09263) | Privileged likelihood answers "how does the prediction change when the context gets richer", not "how does the expected outcome change when a token changes". On AIME 2025, the score separates correct from incorrect rollouts at about chance level (AUC 0.505) |
| [2609.39118](https://arxiv.org/abs/2609.39118) Diagnosing OPSD | On 0.6B–8B models, OPSD works only in a narrow compatibility window; outside it, it produces ineffective length growth, steady degradation or even behavioral collapse |
| [2610.18613](https://arxiv.org/abs/2610.18613) Does self-distillation improve reasoning? | Rechecks SDPO and OPSD on code, science, tool use and math: the gains are largely explained by overfitting or by transfer of existing reasoning behavior, and self-distillation gradients align only weakly with policy gradients |
| [2610.13744](https://arxiv.org/abs/2610.13744) (NeurIPS 2026 FLLMPT workshop oral) | A privileged teacher that only scores can neither locate errors nor push down erroneous tokens. Only when the teacher first writes a critique and then scores based on it does the signal locate and correct errors |
| [2609.29051](https://arxiv.org/abs/2609.29051) From Self-Distillation to Self-Practice | On multi-turn agents, OPSD-trained students act as if they had privileged information they never saw, falling short of plain RL and, in the worst case, of the untrained base model. The fix moves the privileged instruction into sampling and keeps the original GRPO loss; on AppWorld and SWE-bench Verified it improves on GRPO by 7%–58% |
| [2608.25936](https://arxiv.org/abs/2608.25936) One Symptom, Three Levers | A review that treats "collapse" as a symptom governed by three levers: which tokens the signal is applied to, what the teacher is shown, and how the guidance decays over time |

The related-work paper [2610.05872](https://arxiv.org/abs/2610.05872) beats OPSD in continual learning with an off-policy weight-grafting method.

### 3.2 Directions for improvement: change what the teacher sees

- **Show less**: [2609.25623](https://arxiv.org/abs/2609.25623) finds that intermediate abstractions such as a "strategy name" or a "method-agnostic framing" beat the full reference solution by 1.4–1.6 points, with an order of magnitude fewer hint tokens. [2609.32201](https://arxiv.org/abs/2609.32201) replaces per-problem gold answers with a few general instructions written for the student's common mistakes, and out-of-distribution accuracy is 4–17 points higher in 7 of 8 experiments.
- **Use soft privileges**: [2608.02948](https://arxiv.org/abs/2608.02948) uses rubrics as privileged information to extend OPSD to open-ended generation, outperforming RL that uses rubrics as rewards.
- **Drop privileges entirely**: [2608.06296](https://arxiv.org/abs/2608.06296) U-OPSD gets a pseudo-solution by majority vote, improving Qwen3 4B and 8B over the base by 8.5% and 10.7%. [2608.27448](https://arxiv.org/abs/2608.27448) TTPO does label-free test-time training: rollouts that agree with the vote go through OPSD, those that disagree are penalized with grouped RL, and it matches labeled OPSD. [2610.22080](https://arxiv.org/abs/2610.22080) SRD extracts supervision from unverified peer solutions, raising Qwen3-8B's avg@12 on AIME24–26 from 21.39 to 54.44. [2610.38681](https://arxiv.org/abs/2610.38681) WISD builds a weaker copy of the model by quantization or pruning and learns from the contrast, raising Qwen3.5-4B on HMMT 2025 from 57.7% to 70.5%.
- **Weaken the student instead of strengthening the teacher**: [2608.14144](https://arxiv.org/abs/2608.14144) lets the teacher see the original image and the student a strongly augmented view in vision tasks, recovering 96% of the gain of privileged methods.
- **Fit the teacher to the student**: [2610.10447](https://arxiv.org/abs/2610.10447) JOLT derives the necessary and sufficient condition for a privileged teacher's distillation update to be a positive multiple of the student's reward gradient, and on that basis jointly trains the teacher and student roles. [2608.01735](https://arxiv.org/abs/2608.01735) DAPD applies two-way anchoring against "privilege illusion" (the student learns to rely on privileged information that is absent at inference).

## 4 Multi-Teacher OPD (MOPD) and Capability Merging

MOPD works like this: first train several domain experts with RL, then have one student receive per-token supervision from each domain's expert on its own trajectories.

**Industrial practice**: of the 35 technical reports that use OPD, 21 use it to merge several experts, usually as the last step of post-training. Examples:

- [2610.38095](https://arxiv.org/abs/2610.38095) NVIDIA Nemotron 3.5 Super: trains specialized teachers, then runs MOPD; it reaches 51.78% on SWE-bench Pro, beating Nemotron 3 Ultra with about 1/4.6 of its active parameters.
- [2610.11959](https://arxiv.org/abs/2610.11959) Xiaomi MiMo-V2.6: MOPD2, i.e. multi-prefix multi-teacher OPD (according to the thinkwee and kissshhot lists' excerpts from the full text).
- [2608.09119](https://arxiv.org/abs/2608.09119) Motif 3: 6 expert teachers trained with RL, plus 1 software-engineering teacher trained with SFT.
- [2609.00791](https://arxiv.org/abs/2609.00791) AMD Instella-MoE.
- [2609.11929](https://arxiv.org/abs/2609.11929) SenseTime SenseNova-U1.5: a unified multimodal model.
- [2609.23377](https://arxiv.org/abs/2609.23377) Alibaba's SWE agent: reaches 86.19% on SWE-bench Pro V2.

The full list is in the "Technical reports" section of the [paper catalog](./On-Policy-Distillation-Literature-Review-Papers_en.md).

**Known problems and fixes**:

| Problem | Paper | Approach and result |
| --- | --- | --- |
| Uneven signal scales across domains | [2609.35347](https://arxiv.org/abs/2609.35347) DN-MOPD | Instruction-following feedback is several times more spread out than math feedback and dominates the update direction. Normalizing each domain by its measured spread beats MOPD on 6 benchmarks at 3 scales |
| Misallocated token budgets | [2608.19098](https://arxiv.org/abs/2608.19098) Open-MOPD | Standard MOPD captures only 35.6% of the available headroom, not because of gradient conflict but because the token budget is misallocated. The fixes raise it to 83.4%, and the full training recipe is open-sourced |
| Domain scheduling | [2608.24987](https://arxiv.org/abs/2608.24987) D³-MOPD | Reuses the reverse-KL signal already produced in training to adjust each domain's sampling share online. It closes 97% of the teacher-student gap (63% for vanilla) with about 3× fewer rollout steps |
| Teacher routing | [2609.30837](https://arxiv.org/abs/2609.30837) MOPD-Router, [2610.13521](https://arxiv.org/abs/2610.13521) | Picks a teacher from the whole pool per token, or has non-routed teachers act as cross-domain reviewers |
| What to transfer | [2610.10460](https://arxiv.org/abs/2610.10460) Δ-MOPD, [2609.14708](https://arxiv.org/abs/2609.14708) | Transfers not the teacher's final policy but only its shift relative to the model before post-training |
| Task interference | [2609.34605](https://arxiv.org/abs/2609.34605) PMOPD | Each task's parameter updates concentrate in its own low-dimensional subspace; gradients that interfere with protected subspaces are projected out |

**Questioning whether MOPD is needed**:

- [2610.04272](https://arxiv.org/abs/2610.04272): in a controlled same-base experiment, SFT, soft labels, teacher-prefix mixing and MOPD reach nearly identical accuracy, but MOPD uses 14.8–23.1× SFT's training GPU-hours. When SFT baselines are trained on rejection-sampled data, the on-policy gains reported in published papers shrink substantially.
- [2610.26525](https://arxiv.org/abs/2610.26525): within a shared basin, the MOPD objective is, to second order, exactly Fisher merging. The first-stage closed-form merge alone matches or beats full multi-teacher distillation.
- [2610.22236](https://arxiv.org/abs/2610.22236) Training-Free OPD: when experts share a base model, distillation has a layer-wise least-squares closed-form solution that needs only forward passes over a few hundred rollouts.
- [2609.39405](https://arxiv.org/abs/2609.39405): merging OPD task vectors with RL task vectors can beat both; in cross-task merging, OPD task vectors beat RL task-vector merging in 7 of 8 comparisons.

## 5 Combining OPD and RL

- **Order**: [2609.04108](https://arxiv.org/abs/2609.04108) Sequential Beats Joint finds that OPD followed by RL consistently beats pure OPD, pure RLVR and every joint scheme. The explanation: OPD widens the student's coverage of teacher-supported solutions, then RL sharpens within that range; training them jointly makes them interfere. When to switch to RL is decided by OPD's validation score.
- **OPD as preparation for RL**: [2609.28145](https://arxiv.org/abs/2609.28145) RL Starts before RL finds that students initialized with OPD reach higher final RL performance than direct RL or SFT+RL, even when OPD brings almost no immediate accuracy gain. Reverse KL is better before RL but is overtaken by forward KL after RL; under both objectives, student rollouts beat teacher rollouts.
- **Why joint training is unstable**: [2609.34849](https://arxiv.org/abs/2609.34849) uses an NTK analysis and finds that the reward gradient can exceed the distillation gradient by orders of magnitude, and the two can conflict in direction at the same token; once their gradient-norm ratio passes an empirical threshold, naive mixing can lead to persistent training collapse.
- **Fusion methods**: [2608.24696](https://arxiv.org/abs/2608.24696) OPDVR gates the implicit reward with a ReLU according to whether the trajectory is correct, turning OPD into an RLVR method. [2609.32674](https://arxiv.org/abs/2609.32674) finds that the student's own actions are more useful on successful trajectories and teacher replacements more useful on failed ones, so it reinforces on successful trajectories and distills on failed ones. [2610.40576](https://arxiv.org/abs/2610.40576) PIVOT inserts teacher corrections into student rollouts and applies KL to those segments; on hard logic games, avg@8 rises from the best baseline's 19.5% to 35.6%. [2609.08798](https://arxiv.org/abs/2609.08798) OPRD uses only the weak teacher's shift direction to amplify the verifier gradient, letting the student surpass the teacher.

## 6 Improvements to the Objective, the Teacher and the Rollout

These three kinds of method papers total 200 (counted by first label); only those whose abstracts report large gains are listed here.

- **Token weighting**: [2609.38025](https://arxiv.org/abs/2609.38025) Dr. OPD treats each token's weight as a bilevel optimization variable with a closed-form update. In the strong-to-weak setting, the average math score is 9.7 points above vanilla OPD, and the smaller student surpasses the larger teacher.
- **Teacher continuation**: [2608.16333](https://arxiv.org/abs/2608.16333) has the teacher continue from intermediate states of the student's trajectory to write a full repair path; it beats vanilla OPD by 13.4 points on ALFWorld. [2609.22254](https://arxiv.org/abs/2609.22254) AC-OPD adaptively chooses how long the teacher's continuation runs. [2610.27467](https://arxiv.org/abs/2610.27467) minimally edits the student's failed attempts into correct targets; replacing these with student-agnostic gold solutions lowers retention from 0.916 to 0.744.
- **Rollout proposals**: [2610.36477](https://arxiv.org/abs/2610.36477) MPOPD generates rollouts from a geometric mixture of the student and teacher distributions. It beats OPD consistently on 16 benchmarks, with 6.91 higher average math accuracy and 41% shorter generations. [2610.07874](https://arxiv.org/abs/2610.07874) mixes a weaker negative policy into rollouts to give the student an explicit negative signal.
- **Branching**: [2610.13481](https://arxiv.org/abs/2610.13481) BranchOPD resamples branches from shared prefixes at decision points where the student is uncertain or teacher and student disagree. Math avg@16 is 18.55 points above vanilla OPD, and ALFWorld 13.8 points higher.
- **Saving compute**: [2610.21337](https://arxiv.org/abs/2610.21337) STOPD truncates rollouts at random and uses inverse-probability weighting to keep the expected gradient unchanged; generated tokens drop by 25%–48% and training is 1.3–2.2× faster. [2609.35505](https://arxiv.org/abs/2609.35505) LSPD's fully off-policy variant matches OPD using only the first 25% of rollout batches.
- **Distilling a whole distribution**: [2610.06804](https://arxiv.org/abs/2610.06804) OPPD distills the sharpening effect of a sequence-level power distribution into a single generation. It gains 23.0 points on MATH500, beats GRPO at the same budget by 3.8–5.4 points, and adds another 9.3 points when applied after GRPO.

## 7 Application Domains

Core papers by domain: general LLM 271, agents 99, multimodal understanding 63, generation 29, other applications 26, safety and privacy 18, embodied 13, diffusion language models 10, quantization and pruning 10, speculative decoding 1.

**Agents (99 papers).** In multi-turn interaction, one wrong action changes every state that follows, which makes the problem different from single-turn reasoning.

- [2609.40285](https://arxiv.org/abs/2609.40285) PivotOPD (NVIDIA): over half of the failed trajectories contain one early pivotal mistake, usually still recoverable. It teaches the correct action at that step with reverse KL and recovery actions in the following turns with forward KL; ALFWorld +5.5%, SWE-Bench Verified +3.2%.
- [2610.25034](https://arxiv.org/abs/2610.25034) finds "distillation overshoot": the student first surpasses the teacher, then falls back. SPOD masks teacher supervision that conflicts with the student's successful choices and ends up as much as 20.0 points above the teacher.
- [2610.28586](https://arxiv.org/abs/2610.28586): the problem is not only compounding error but the "myopia" of the teacher's per-token scoring. Repairing the teacher's scorer before OPD wins all 12 combinations, by 12.8 success points on average.
- [2610.31918](https://arxiv.org/abs/2610.31918): splits on-policy into two levels, the "interaction history" and the "current action prefix". Student histories paired with teacher action prefixes give the strongest signal; following the student at both levels does worst.
- [2610.19820](https://arxiv.org/abs/2610.19820) ActionOPD: distills a black-box teacher at the level of semantic actions, without requiring teacher and student to share a model family or vocabulary.
- [2610.08077](https://arxiv.org/abs/2610.08077): distills hindsight experience into foresight before acting. With a 2B model where 98% of groups all fail, RLVR ends at 0% success, while adding this distillation reaches 60.6%.

**Multimodal and generation.** [2610.20989](https://arxiv.org/abs/2610.20989) finds on VLMs that OPD works only when the teacher stays reliable on student trajectories: on ChartQA it comes close to full-data SFT with 10% of the data, but on Geometry3K it trails by 7.9 points, mainly because answers are left unfinished. For diffusion and flow models, the cross-family [2608.03316](https://arxiv.org/abs/2608.03316) Any-OPD aligns teacher and student in a frozen visual representation space, and [2608.24646](https://arxiv.org/abs/2608.24646) is best in 19 of 20 settings while using 40%–63% fewer training GPU-hours than DiffusionNFT.

**Architecture transfer and compression**:

- [2609.31947](https://arxiv.org/abs/2609.31947) attention linearization: with only 3B training tokens, needle-in-a-haystack retrieval recovers to 100%.
- [2609.26708](https://arxiv.org/abs/2609.26708) sub-3-bit quantization: MATH-500 retention rises from 35% to 70%.
- Distilling autoregressive models into diffusion language models: [2609.35362](https://arxiv.org/abs/2609.35362) d-OPD, [2610.17397](https://arxiv.org/abs/2610.17397) JustOPD.
- Cross-tokenizer: [2610.08448](https://arxiv.org/abs/2610.08448) finds that strictly 1:1-aligned positions already cover most tokens; [2609.10154](https://arxiv.org/abs/2609.10154) finds that cross-family OPD still fails even after the tokenizers are aligned, and proposes transferring only the "within-family likelihood shift".

**Safety and privacy**:

- [2609.33136](https://arxiv.org/abs/2609.33136): the first membership-inference attack on OPD, with mean AUROC 0.875.
- [2610.07654](https://arxiv.org/abs/2610.07654): a backdoored safety teacher passes its backdoor to the student through OPD. A 3% poisoning rate yields an attack success rate of up to 70%; the common top-k KL speeds up backdoor transfer.
- [2608.21500](https://arxiv.org/abs/2608.21500) SecOPD: against the SOTA adaptive prompt-injection attack PISmith, the attack success rate is 9.0%, compared with 94.0% for the previous best defense, Meta-SecAlign.

**Speculative decoding**: only 1 core paper, [2610.37778](https://arxiv.org/abs/2610.37778) Multi-Draft OPD, for parallel diffusion drafters. The earlier Draft-OPD (2605.29343) falls outside this survey's time window.

## 8 OPD Paper Lists on GitHub

The data below was retrieved through the GitHub API on 2026-11-02. "Recent entries" counts the papers in a README with arXiv IDs from 2608 to 2610 (deduplicated by ID).

### 8.1 Main lists

| Repository | Stars | Created | Last commit | Size | Recent entries (2608/2609/2610) | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| [chrisliu298/awesome-on-policy-distillation](https://github.com/chrisliu298/awesome-on-policy-distillation) | 903 | 2026-03-22 | 2026-10-06 | The badge says 800 entries; the README has 748 arXiv IDs | 299 (112/154/33) | Widest coverage. Split into core papers, related work, domain extensions (agents, multimodal, speech, diffusion and flow, embodied, speculative decoding), technical reports and frameworks, plus two taxonomy tables (by teacher type and by goal), a Start Here reading path and a roundup of blogs and tutorials. One English sentence per entry. CC0 license |
| [thinkwee/AwesomeOPD](https://github.com/thinkwee/AwesomeOPD) | 882 | 2026-04-27 | 2026-10-18 | 12 sections, about 490 entries by badge totals; the README has 462 arXiv IDs | 127 (90/29/8) | The most explicit inclusion criteria: C1, student self-sampling, plus C2, teacher supervision of the student's samples; papers that fall short are noted in each section's Strictness notes, and rejected papers and the reasons are recorded in the changelog. Each entry has stars, date and institution, plus a collapsible table of technical details (loss and divergence, data, teacher access, granularity). Swept monthly, with the changelog summarizing each month's through-line. Has a Curator's Picks reading order |
| [nick7nlp/Awesome-LLM-On-Policy-Distillation](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation) | 592 | 2026-04-05 | 2026-10-13 | 362 entries, 134 with code | 127 (43/45/39) | The companion reading list for an OPD survey (arXiv 2604.00626), organized by research question, with a paragraph summary per paper. It has a companion search site, [OPDHub](https://nick7nlp.github.io/OPDHub/); `resources/` holds a method comparison, a loss taxonomy, key equations, a code index, an evaluation guide and a machine-readable `catalog.json`. Of the three large lists, it has the most October entries |
| [Jingchensun/Awesome-Multimodal-OPD](https://github.com/Jingchensun/Awesome-Multimodal-OPD) | 38 | 2026-06-18 | 2026-11-01 | 158 entries (image 57, video 15, audio 16, generation 45, embodied 25), 61 with code | 69 (34/35/0) | Multimodal OPD and OPSD only. Sorted by GitHub stars, with a Chinese/English interactive reader; `papers.json` gives each paper a four-point summary and marks whether it strictly counts as OPD. The most commits in the last 30 days (30) |
| [DjangoJungle/Awesome_MOPD](https://github.com/DjangoJungle/Awesome_MOPD) | 16 | 2026-08-04 | 2026-10-22 | 69 entries | 38 (8/19/11) | Multi-teacher OPD (MOPD) only, split into foundations, methods, analysis and applications, with a separate list of technical reports that use MOPD |
| [HJSang/awesome-OPSD](https://github.com/HJSang/awesome-OPSD) | 0 | 2026-10-06 | 2026-10-07 | 60 entries, 31 with code | 25 (10/13/2) | OPSD only, with method notes on each entry, plus `data/papers.json` and `papers.bib` |
| [kissshhot/Awesome-OPD](https://github.com/kissshhot/Awesome-OPD) | 26 | 2026-07-31 | 2026-10-10 | 114 entries | 37 (6/19/12) | Chinese and English summaries for each entry; `docs/SOURCE_AUDIT.md` records the paper version each entry was checked against |
| [hhlxm/Awesome_OPD](https://github.com/hhlxm/Awesome_OPD) | 0 | 2026-10-25 | 2026-11-01 | 34 entries | 13 (3/7/3) | A longer English TL;DR per paper, grouped into general OPD, agent OPD, efficient OPD, latent OPD and OPSD, with archived PDFs |

### 8.2 Inactive or partly relevant lists

| Repository | Notes |
| --- | --- |
| [Jianglin954/awesome-on-policy-distillation](https://github.com/Jianglin954/awesome-on-policy-distillation) | 113 entries, last commit 2026-04-13 |
| [AnhaoZhao-LLMer/On_Policy_Distillation_Paper_List](https://github.com/AnhaoZhao-LLMer/On_Policy_Distillation_Paper_List) | 176 arXiv IDs, last commit 2026-06-08 |
| [china10s/awesome-opd](https://github.com/china10s/awesome-opd) | 122 entries, last commit 2026-05-15 |
| [miracle-techlink/opd-papers](https://github.com/miracle-techlink/opd-papers) | Multimodal OPD, 34 entries, last commit 2026-05-15 |
| [zsxm1998/awesome-perception-aware-rlvr](https://github.com/zsxm1998/awesome-perception-aware-rlvr) | 36 stars; reproductions and evaluations of perception-aware RLVR and OPD in VLMs, including 24 papers from the last three months |
| [yingyingxia666/awesome-agentic](https://github.com/yingyingxia666/awesome-agentic) | A large Chinese-language list of LLM RL papers (over 910), with OPD as one of its directions; last commit 2026-09-11 |
| [MAC-AutoML/Awesome-Self-Distillation](https://github.com/MAC-AutoML/Awesome-Self-Distillation), [ahmedheakl/Awesome-Self-Distillation](https://github.com/ahmedheakl/Awesome-Self-Distillation) | Self-distillation in the broad sense; no entries after 2608 |
| [Tebmer/Awesome-Knowledge-Distillation-of-LLMs](https://github.com/Tebmer/Awesome-Knowledge-Distillation-of-LLMs) | 1318 stars; the companion list for a 2024 survey on knowledge distillation of LLMs, not specific to OPD |

### 8.3 How the lists overlap

| List | Recent entries | Only in this list |
| --- | --- | --- |
| chrisliu298 | 299 | 131 |
| thinkwee | 127 | 8 |
| nick7nlp | 127 | 25 |
| Jingchensun (multimodal) | 69 | 20 |
| DjangoJungle (MOPD) | 38 | 9 |
| kissshhot | 37 | 1 |
| HJSang (OPSD) | 25 | 3 |
| hhlxm | 13 | 2 |

- Pairwise overlap: chrisliu298 and thinkwee share 97 papers, chrisliu298 and nick7nlp 78, thinkwee and nick7nlp 47; only 42 appear in all three.
- The union of the 8 lists is 409 papers. 368 of them are also found by this survey's arXiv keyword search; the other 41 are not (their abstracts lack phrases like "on-policy distillation", e.g. EviSD, Woodpecker Distillation and the MiMo-V2.6 technical report) and were added to the candidate pool from the lists.
- Of this survey's 540 core papers, 186 appear in no list. Most of the late-October papers cited in Sections 2–7 are among them, e.g. 2610.22236, 2610.25034, 2610.28586, 2610.36477, 2610.38681 and 2610.39020; 2610.26525 is listed only by DjangoJungle.

### 8.4 How to use them

- Getting started: read thinkwee's Curator's Picks and chrisliu298's Start Here, then nick7nlp's `resources/reading-order.md`.
- Technical details of a paper (loss, teacher access, granularity): see thinkwee's collapsible tables.
- Everything in one direction: use chrisliu298's matching subsection plus a topic list (Jingchensun for multimodal, DjangoJungle for multi-teacher, HJSang for OPSD).
- Keyword search and filtering: use nick7nlp's OPDHub or Jingchensun's interactive reader.
- Machine-readable data: nick7nlp's `resources/catalog.json`, Jingchensun's `papers.json`, HJSang's `data/papers.json` and `papers.bib`.
- None of the three large lists has added papers from mid-to-late October yet, so the newest papers have to come from arXiv searches.

## 9 Reading Order for Newcomers

Most of this quarter's papers build on the following baselines, so read them first:

1. The Thinking Machines blog post [On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/) (2025-10)
2. GKD (2306.13649) and MiniLLM (2306.08543)
3. Rethinking OPD (2604.13016): this repo has [a note with the full paper and a Chinese translation](./Rethinking-On-Policy-Distillation_en.md)
4. OPSD (2601.18734)
5. The OPD survey A Survey of On-Policy Distillation for Large Language Models (2604.00626)

Then read this quarter's papers in this order:

1. Boundaries first: 2609.04172 (one query is enough) → 2610.11291 (when on-policy is needed) → 2610.09639 (skills, not knowledge) → 2608.31046 (does it really distill?)
2. Then failure modes: 2609.20511 (EOS mismatch) → 2610.18011 (fails on problems the student gets wrong) → 2609.31900 (pipeline order)
3. For OPSD: 2608.18271 → 2609.20612 → 2609.29051 → 2610.13744
4. For MOPD: 2608.19098 → 2609.35347 → 2610.04272 → 2610.26525
5. For combining OPD and RL: 2609.04108 → 2609.28145
6. For agents: 2609.40285 → 2610.25034 → 2610.28586 → 2610.31918
