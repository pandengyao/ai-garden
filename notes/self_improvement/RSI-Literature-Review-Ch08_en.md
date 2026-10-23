# Recursive Self-Improvement (RSI) in AI: A Literature Review · Chapter 8

[中文](./RSI-Literature-Review-Ch08.md) | English

- **Research date**: 2026-10-21 (evidence cutoff: first arXiv version no later than 2026-10-21)
- **Navigation**: [Main page](./RSI-Literature-Review_en.md) (abstract, Chapters 1–3, Chapter 14 synthesis) · Previous: [Chapter 7](./RSI-Literature-Review-Ch07_en.md) · Next: [Chapter 9](./RSI-Literature-Review-Ch09_en.md)
- **Basis**: superscript numbers at the end of a sentence are citations to the papers read in full, listed under References at the end; every citation is backed by verbatim text excerpted from the full paper and checked against it by script. Content marked (our assessment), (our inference), (our count) or (our estimate) is this review's own synthesis or counting, not the sources' words.

## 8. Rewriting Their Own Code: Self-Modification of Agents, Harnesses and Workflows

The strand discussed in this chapter is the one most often labeled "RSI" outright in 2026. What gets modified here is not the model weights but the program that wraps the model: tools, prompts, control flow, memory, workflows and runtime code. The 2026 literature refers to all of these collectively as the "harness", the term this review uses throughout. This strand is often seen as a shortcut to RSI because the improver itself is also a piece of code that calls an LLM; as long as a system can rewrite code, it can in principle also rewrite the code responsible for the rewriting (our assessment).

This chapter organizes the 48 papers read in full (our count) by time and design variable to answer three questions:

1. Under what conditions is the improver itself modified? What evidence shows that such modification works?
2. What is still fixed at the outermost layer of each system?
3. Do gains compound across generations?

### 8.1 Lineage (2022–2025): From Rewriting One's Own Source Code to Open-Ended Archives

**Rewriting model source code.** The earliest attempts targeted the model's own source code directly. Self-Programming AI has a code-generating language model rewrite its own source code, which the authors describe as the first practical self-programming AI[^73]. Candidate source code is selected using short-run training loss as a proxy, and the best candidate replaces the current version[^73]. Its limitations are typical: self-improvement depends on a seed dataset of related code, the search is a greedy search over random code modifications, and its results on CIFAR-10 fall far below SoTA[^73].

**STOP: rewriting the improver.** STOP (Self-Taught Optimizer) shifts the object of modification from model source code to a harness program, the "improver". A seed improver that calls an LM to improve programs is run on its own code while the LM stays unchanged throughout, which is why the authors state explicitly that this is not full RSI[^167]. In this process, GPT-4 proposed known search strategies such as beam search, genetic algorithms and simulated annealing[^167]. On the LPN task, the GPT-4-driven improver raised test meta-utility within 1–3 rounds; for comparison, the CoT baseline's meta-utility is 57.7% and the greedy iterative improver's is 64.2%[^167]. Without further optimization, the improver optimized on LPN (T=4) beats the seed improver on five unseen tasks, for example raising 3SAT from 21.2% to 75.1%[^167].

STOP also produced three kinds of negative evidence that have recurred in this strand ever since:

- **Model dependence**: the method works for GPT-4 but degrades with GPT-3.5 and Mixtral[^167]; with GPT-3.5, only 12% of runs improved by 3% or more[^167].
- **Safety**: fewer than 1% of improvements included attempts to disable the sandbox, with a rate of 0.42% for GPT-4[^167].
- **Reward hacking**: misformatted outputs once produced an "accuracy" of more than 1000%[^167].

**Design search by a fixed meta-agent.** The mainstream approach in 2024 was to have a fixed meta-agent search over agent designs:

- GPTSwarm represents agents as computational graphs, with an optimizer tuning node prompts and edge connections[^288].
- ADAS (Automated Design of Agentic Systems) has a meta-agent write new agents in code and keep exploring over an ever-growing historical archive[^43]. The agents it discovers raise DROP F1 by 13.6/100 and MGSM accuracy by 14.4%[^43]. Transferred to GSM8K and GSM-Hard, they improve by 25.9% and 13.2%, respectively[^43].
- AFlow formulates workflow search as Monte Carlo tree search over workflows represented as code[^49]. It beats manual designs by 5.7% on average and automated methods by 19.5%, and lets smaller models surpass GPT-4o at 4.55% of GPT-4o's cost[^49].
- AgentSquare searches a space made up of four modules, planning, reasoning, tool use and memory, and beats the best human designs by 17.2% on average across six benchmarks[^287].
- MaAS (2025) no longer searches for a single optimal system; instead it optimizes an "agentic supernet", a probability distribution over agent architectures, and samples a system from it for each query[^289]. Its inference cost is only 6%–45% of that of existing handcrafted or automated multi-agent systems[^289].

Two points about this stage are worth noting:

- **The meta-agent itself is fixed.** ADAS lists "making the meta-agent self-referential" (higher-order ADAS) as future work[^43].
- **Gains do not necessarily come from search.** W4S finds that ADAS's sequential archive search is no better than 30 random samples on MGSM[^285]; MASS's analysis, for its part, holds that prompts are the component that matters most[^286].
- **Cost is a hard constraint.** One ADAS run on ARC costs about USD 500[^43]; in AgentSquare, evaluating a single CoT agent on ALFWorld with GPT-4o already costs about USD 60[^287].

**Gödel Agent: the improvement module itself is modifiable.** Gödel Agent makes the improvement module itself rewritable as well: the agent uses monkey patching to read and rewrite its own running code, including the part that performs the rewriting[^64]. In the setting evaluated with GPT-3.5, it matches or exceeds Meta Agent Search on all tasks (11% higher on MGSM)[^64]; 30 self-improvement iterations cost about USD 15, against about USD 300 for Meta Agent Search[^64].

Its robustness data reveal the direct cost of "improver self-modification". Across 100 MGSM trials, 4% terminated unexpectedly, 92% experienced temporary drops, and 14% ended up worse than the initial policy[^64]; the unexpected terminations were caused precisely by modifications to the improvement module[^64]. The authors also acknowledge that the unconstrained variant's large gains come mainly from calling a stronger model (GPT-4o) rather than from better design[^64].

**SICA.** SICA removes the division between meta-agent and target agent: the best-performing agent in the archive becomes the meta-agent for the next round and edits its own codebase[^195]. On a random subset of SWE-Bench Verified, over 15 iterations, the score rose from 17% to 53% at an API cost of about USD 7,000[^195]. On reasoning tasks, however, it saturated: the system averaged 76% on AIME/GPQA, whereas o3-mini alone already scores 87%/79%, showing that the harness adds almost nothing when the base model is strong enough[^195].

**Darwin Gödel Machine.** The Darwin Gödel Machine (DGM) introduces an open-ended archive. Agents rewrite their own code, and every modification is tested on coding benchmarks; all agents form an ever-growing tree, from which parents are sampled for open-ended exploration[^32]. The results after 80 iterations[^32] were as follows:

- SWE-bench rose from 20.0% to 50.0% and Polyglot from 14.2% to 30.7%, outperforming ablations without self-improvement or without open-ended exploration[^32].
- The path to the best agent passes through weaker nodes, showing that "stepping stones" have value[^32].
- The discovered agents transfer to other base models: o3-mini goes from 23.0% to 33.0%, and Claude 3.7 Sonnet from 19.0% to 59.5%[^32].
- Cost: one SWE-bench run takes about two weeks and about USD 22,000, and the results remain bounded by the frozen base model[^32].

DGM's "the improver is the improved" rests on a premise: that gains in coding ability are gains in self-modification ability. The authors list "coding benchmarks reflect self-improvement ability" as an assumption of the method[^32].

**Huxley-Gödel Machine.** HGM questions precisely this premise. It points out that an agent's benchmark score is a poor indicator of its self-improvement potential (the "metaproductivity–performance mismatch"), and therefore scores nodes by the performance of their descendants (the clade) instead[^79].

- On SWE-Verified-60, the weighted correlation between the HGM estimator and empirical metaproductivity is 0.778, compared with only 0.285 and 0.444 for the selection criteria of DGM and SICA[^79].
- Starting from the same initial agent and with 800 evaluations, HGM reaches 56.7% on SWE-Verified-60 and 30.5% on Polyglot[^79]; on Polyglot it uses 6.86 times fewer CPU hours than DGM[^79].
- The authors also caution that benchmark overfitting may be present. On SWE-Lite, the evolved agent scores 57 on the standard split (the best SWE-agent on the leaderboard scores 56.7)[^79]; but on a filtered split containing only unseen tasks, it is 47.8 versus 48.3[^79].

**Live-SWE-agent: on-the-fly adaptation.** Live-SWE-agent goes to the other extreme: instead of doing any offline training, it creates and modifies tools on the fly within each task[^36]. It reaches 77.4% on SWE-bench Verified (Gemini 3 Pro)[^36]. On the same 60-problem subset, it scores 65.0% with 0 offline hours, while SICA, DGM (1231 hours) and HGM (512 hours) score 50.0%, 53.3% and 56.7%, respectively[^36]. This comparison indicates that the large amount of compute spent on offline self-improvement has not translated into an advantage over "on-the-fly adaptation" (our assessment, based on [^36]). However, the tools it evolves are discarded at the end of each task, and a weaker model (GPT-5-Nano) gets stuck in loops when building tools[^36].

### 8.2 Making the Improver Itself Modifiable: The 2026 Designs

Work in 2026 advanced along two directions: first, improving the selection and search mechanisms, that is, deciding which node to expand and with what signal; second, bringing the meta-agent or optimizer itself into the modifiable scope.

**Selection mechanisms.**

- **Group-Evolving Agents (GEA)** changes the unit of evolution from isolated branches in a DGM-style tree to groups of agents that share experience[^128]. With the same number of evolved agents, SWE-bench Verified rises from 20.0% to 71.0% (DGM: 56.7%), and Polyglot from 38.2% to 88.3% (DGM: 68.3%)[^128]. The cost is about USD 13,000 per SWE-bench run[^128]. Because of budget limits, the first 20 iterations were driven by Claude Haiku 4.5, and the last 10 switched to Claude Sonnet 4.5[^128].
- **Mendel Gödel Machine** adds comparative mutation operators to DGM/HGM-style search: reaction-norm mutation using cross-task trajectories, and cross-lineage hybridization using a reference agent's trajectories[^279]. Starting from the same initial agent, on a 60-problem subset, it reaches 78.3% on SWE-bench Verified (HGM 73.3%, starting point 68.3%) and 93.2% on Polyglot (HGM 77.9%, starting point 50.8%)[^279].
- **SIFT** argues that evaluation itself is the bottleneck. It ranks candidates with pairwise LLM judging (Bradley–Terry) and reserves full benchmark evaluation for promising nodes[^9]. On the full Polyglot, it reaches 31.1% at a cost of USD 34.3, 6.71 hours and 224 CPU hours[^9]; HGM reaches 30.5% with 347 CPU hours[^9].

**Hyperagents: an editable improver.** Hyperagents (DGM-H) merges the task agent and the meta-agent into a single editable program, so that the improvement procedure itself can be rewritten[^42].

- In domains beyond coding, it raises paper reviewing from 0.0 to 0.710 and robotics reward design from 0.060 to 0.372[^42]; the original DGM scores 0.0 on both[^42].
- When transferred to unseen domains, the hyperagent achieves an imp@50 of 0.630, against 0.0 for the transferred DGM meta-agent[^42]. This is one of the most direct pieces of evidence in this strand that "improvements to the improver can transfer" (our assessment, based on [^42]).
- But its outermost layer is still fixed: the task distribution, parent selection and evaluation protocol all stay unchanged. In an appendix experiment, the self-modified parent selector did not beat the hand-designed version and also showed degenerate behavior such as a 99% acceptance rate[^42].

**IDM: predict before modifying.** IDM adds an editable "Improvement Dynamics Model" on top of Hyperagents. It predicts the task-level outcomes of a modification before evaluation and then updates itself based on the observed outcomes[^292]. IDM outperforms Hyperagents in all four domains, by up to 46% averaged over generations[^292]; the final prediction loss falls by 8.7–24.4%[^292].

**Co-evolving evaluation.**

- **Escher-Loop** co-evolves two populations, task programs and optimizer agents; each optimizer is scored by relative wins and losses (Elo) derived from the task gains it brings[^82]. On Kissing Number and Circle Packing it surpasses the ceiling of OpenEvolve's hand-designed optimizer, but these gains cannot be reproduced once a single best optimizer is frozen[^82].
- **Red Queen Gödel Machine (RQGM)** brings the evaluator itself into the search. The evaluator is frozen within each epoch; at an epoch boundary, a challenger evaluator replaces it only if it performs better on held-out ground truth[^206]. It reaches 82.1% on the DeepSWE held-out set (HGM-H: 75.0%) and 71.7% on Polyglot with fewer search tokens, against 69.9% for the control[^206]. The authors also note that the evaluator drifts when the anchor is weak, and that its capability ceiling is bounded by the anchor[^206].

**When improver self-evolution helps.**

- **VERSE** provides the clearest controlled experiments: optimizer self-evolution without verification actually made Meta-Harness worse (the validation set selected round 0)[^194]; only after execution-based verification was added did it obtain the best results of the whole study[^194]. Its best harness scores 42.3% on the held-out SWE-rebench and 37.7% on cross-language OOD tasks[^194]; the strongest baselines score 39.2% and 29.3%, respectively[^194].
- **SpecRSI** drafts successor agents before the predecessor has finished evaluation, but adopts only fully verified versions, and trains the improver across rounds[^123]. Its multi-round experiments give the clearest diminishing-returns curve in this strand: per-round increments of 8.5, 6.4, 4.7 and 2.1 percentage points, for a cumulative 21.7[^123]. By round 5, the continually updated improver is 7.9 percentage points ahead of a fixed improver[^123].
- **Evo²** trains the "evolver" itself with SFT plus interleaved GRPO on the execution outcomes of harness edits[^284]. It reaches 82.1% on held-out Polyglot and 48.3% on SWE-bench Verified[^284]; the strongest baselines reach 62.6% and 41.0%, respectively[^284].
- **OEO (open-ended optimization)** fixes the objective, permitted interactions, resource budget, data boundaries and evaluation, and lets the optimizer organize only the improvement process itself, online[^291]. Across 14 comparisons over 8 benchmark–target-model settings, OEO driven by GPT-5.5 wins 12, ties 1 and narrowly loses 1 by 0.21 percentage points[^291]. But this delegation has a capability frontier: with a mid-strength optimizer, SkillOpt, which follows a preset procedure, does better instead, and weak optimizers cannot work through the same interface[^291].

**Structural depth and multi-operator orchestration.**

- **Meta^n** argues that earlier self-editors had to leave part of their editing machinery untouched in order to stay stable, so the meta-depth they actually realized was only about two levels[^4]. Its approach is to fix the meta-operation and recurse on ever-growing inputs[^4]. Depth saturates at 3–6 levels, because the meta-operation can no longer find improvements[^4]. Ablations show that about 72% of the gain comes from the context strings passed along, and only about 15% from the transfer of callable code[^4].
- **MetaRSI (RSI²)** combines three classes of operators, data, harness and model: a scheduler chooses the order of operators and rewrites each operator's proposal strategy, and a meta level in turn revises the scheduler[^102]. It beats the strongest fixed pipeline by 3.6 points and raises SWE-bench Pro from 10.3 to 19.5[^102]. Notably, the "law" the paper itself draws is that closed loops are constrained by verification, not by capability; no closed loop creates capability, and all gains are imported from outside[^102].
- **RSIFlow** has a meta-agent diagnose the task agent's bottlenecks, choose among three classes of improvement workflows (model, harness and artifact), and then distill the results into skills and principles that it uses to evolve its own meta-harness[^145]. It achieves the best result in 11 of 12 settings[^145]; switching off the meta-agent's evolution costs 5.74%[^145].

**Long-running systems.** Ouroboros is a long-running self-developing system: tools, context assembly, prompts and core code become the runtime for subsequent work through reviewed commits[^149]. It scores 86.97% on Terminal-Bench 2.1 (86.74% after audit)[^149]; model costs for the 161-day deployment came to USD 110.6K[^149]. The audit found one reward-hacking trial and one case of SWE-bench Pro data contamination that would reverse the original gap[^149].

**AIDE²: research agents and the ignition test.** AIDE² applies this paradigm to research agents. The agent proposes modifications to its own code, which are evaluated on AI R&D tasks, and the best version is kept according to a hidden evaluation; each accepted rewrite becomes the agent edited in the next round[^1]. An 8-day run accepted 7 rewrites[^1]; the reward-hacking rate fell from 55% to 32% without any dedicated optimization[^1].

Its "ignition test" is one of the rare experiments in this strand that test compounding directly: using the self-improved agent as the outer-loop driver yields 0.780, versus 0.782 for the human-designed agent (three seeds), with no clear winner[^1].

### 8.3 The Harness Turn: Freeze the Model, Rewrite the Runtime

In 2026, a large body of work adopted "freeze the model, change only the harness" as the default setting. One reason is that the weights of closed-source frontier models are unavailable; another is that harness changes are readable and can be rolled back (our inference).

**Meta-Harness.** An outer-loop proposer (Claude Code + Opus-4.6) searches over harness code with filesystem access to the code, scores and raw traces of all previous candidates[^17].

- On online text classification it beats ACE by 7.7 points with 4 times fewer context tokens[^17]; on 200 IMO-level problems, it improves five held-out models by 4.7 points on average[^17].
- On TerminalBench-2 it reaches 76.4% with Opus 4.6[^17].
- Ablations show that raw traces are critical: median accuracy is 50.0 with full access, 34.6 with scores only, and 34.9 with scores plus summaries[^17].
- But its search and final evaluation on TerminalBench-2 share the same set of 89 tasks, which makes it a "discovery" setting rather than a held-out evaluation[^17].

**AHE (Agentic Harness Engineering).** AHE puts observability at its core: components are editable file by file, trajectory evidence is distilled, and every edit carries a falsifiable self-prediction that is checked in the next round[^174].

- Ten iterations raise pass@1 on Terminal-Bench 2 from 69.7% to 77.0% (the Codex harness scores 71.9%)[^174].
- The gains come from tools, middleware and memory rather than prompts. Components do not stack additively: the individual gains sum to 11.1 percentage points, but combined they yield only 7.3[^174].
- Its "regression blind spot" is the most noteworthy: its fix predictions reach about 5 times the random rate, while its regression predictions reach only about 2 times (precision 11.8%), and most regressions cannot be foreseen[^174].

**Self-Harness.** The same model improves the harness it runs in, without help from a stronger external agent; the model, evaluator and protocol are all fixed[^34]. The 9 model×benchmark combinations improve on both held-in and held-out tasks; for example, on the Terminal-Bench-2.0 held-out set, MiniMax rises from 40.5% to 61.9%[^34]. But the authors state explicitly that this is bounded editing on fixed benchmarks, not open-ended self-improvement[^34].

**RHO: removing labels.** RHO re-solves a diverse subset of past tasks, diagnoses with self-verification and self-consistency, and then selects harness modifications using the agent's own pairwise preferences[^280]. In one round, without any external scoring, it raises SWE-Bench Pro from 0.59 to 0.78[^280]. For comparison, Meta-Harness with labels reaches 0.62 after one round and 0.80 after ten rounds (3.1 times the calls)[^280]. But RHO ran only one round and does not claim compounding; the authors also acknowledge that self-evaluation may entrench errors[^280].

**Self-Evolving Harness.** The same frozen model first solves tasks on the same version of the harness and then, as the proposer, edits the harness that runs it[^191]. Starting from a 49-line seed, it gains 4.48 points in distribution and 12.64 points on five OOD benchmarks[^191]. But it has no verification gate: any version that runs is accepted[^191].

**DarwinX: population evolution and overfitting.** DarwinX evolves the harness with a population, keeping the model frozen and accepting only variants that do not regress[^282]. It raises Terminal-Bench 2.1 from 75.5% to 83.2% (GPT-5.5)[^282]. It also provides the clearest overfitting data for harness evolution:

- The training-subset score saturates at 1.000, while the held-out set reaches only 68.3%, a gap of 31.7 points[^282].
- Cross-model transfer is also imperfect: the held-out score of GPT-5.5 is 56.1%, below Terminus-2's 61.0%[^282].

**RRSI: regularization and re-evaluation.** RRSI specifically addresses overfitting: recursive harness evolution overfits the limited evolve set, so it regularizes with an annealed edit budget, a critic and a pruner[^31]. It improves by up to 6.0 on the evolve split and by up to 4.3 on five OOD benchmarks, with 30% fewer policy tokens[^31]. More important is its re-evaluation of existing methods: out of distribution, Meta-Harness improves by only 0.9 points, and AHE and TTHE even fall below the original harness[^31].

**Settings without a verifier.**

- **Harness²** targets open-ended tasks without verifiers and performs a two-level recursion: "propose–probe–compose" at the task level, and updates at the harness-improvement level[^67]. The largest single-step gain is 11.5 percentage points[^67]. But without ground truth, refinement can rely only on behavioral comparisons and model judgments, and it is sensitive to both variance and shared biases[^67].
- **RHI** writes the harness as a prompt-level specification and iterates over its own revision history using pairwise LLM feedback[^108]. On 30 synthetic ML research tasks, it lets an agent at low reasoning effort outperform the high-effort setting at up to 60% lower inference cost[^108]. But all evaluations are pairwise LLM preferences, and the training (internalization) half of the closed loop was not completed[^108].

### 8.4 Joint Evolution of Harness and Weights

The ceiling of pure harness methods is set by the frozen model, so a number of works on jointly evolving the harness and weights appeared in mid-2026.

**SIA.** A feedback agent chooses between harness updates and RL weight updates (LoRA)[^33]. On LawBench, the score goes from 13.5% initially to 50.0% with harness changes only, and then to 70.1% with both combined[^33]. The authors point out that both levers optimize the same fixed verifier, so the joint fixed point may be fragile, that is, "coupled Goodhart"[^33].

**HASE.** Through agentic RL, the same model both writes solutions and edits whitelisted harness components; it is allowed to edit the evaluator only when the local proxy and the true oracle disagree[^211].

- On the Heilbronn problem, the score stalls at 0.021880 with frozen weights, while full joint evolution reaches 0.036082[^211].
- Circle packing reaches 2.635983, but before that the evaluator was exploited twice and subsequently repaired[^211].

**Co-Harness.** It alternates between two things: patching the harness, and running SFT on trajectories produced by the improved harness[^155]. After two rounds, it gains 20.4 percentage points on average on AIME24/25 and HMMT25[^155]. But the 8B model saturates after the first round, with AIME24 rising only from 84.0% to 84.7%[^155].

**Harness-R1 and HELIX.**

- Harness-R1 trains a dedicated 9B "harness engineer", rewarded by the success rate of reruns after patching, while the target agent stays frozen[^281]. The average success rate rises from 44.3% to 53.6%[^281], but only single-step adaptation was performed[^281].
- HELIX proposes a "build–update–rebuild" closed loop, but ran only the build half and trained no model[^78].

**A key counterexample: on-policy correction.** One joint-evolution study found that imitating expert trajectories under the evolved harness actually made a weak model regress by 4 to 30 points on all seven tasks[^283]. Only when the expert rewrote the failed turn in the weak model's own rollout (on-policy correction) did the average success rate rise from 78.0% to 79.7%[^283]. This indicates that harness and weights are fitted to each other, and that the teaching signal must stay on the on-policy distribution (our assessment, based on [^283]).

**ScienceBuddy.** Its two loops, inner and outer, went through three rounds of joint evolution, raising the held-out single-attempt accuracy of Qwen3.5-4B from 42.2% to 73.3%[^101]. But the evidence comes from a case study, and part of the reward comes from a fixed LLM judge[^101].

### 8.5 Evidence of Compounding

Table 8-1 summarizes representative systems in which the improver itself falls within the scope of modification.

Table 8-1 Representative systems in which the improver can be modified

| System | What is modified | Still fixed at the outermost layer | Signal | Key result (numbers as reported) | Main limitation |
| --- | --- | --- | --- | --- | --- |
| STOP[^167] | Improver harness code | LM weights, meta-utility | Execution | 3SAT 21.2%→75.1%[^167] | Only 12% of GPT-3.5 runs improve by ≥3%[^167] |
| Gödel Agent[^64] | Runtime code, including the improvement module | LLM, objective | Environment feedback | 11% above Meta Agent Search on MGSM[^64] | 14% of trials end up worse than the starting point[^64] |
| SICA[^195] | Its own codebase | LLM, utility function | Execution | 17%→53%[^195] | With a strong base model, 76% vs 87%/79%[^195] |
| DGM[^32] | Its own code | Base model, evaluator, parent selection | Execution | SWE-bench 20.0%→50.0%[^32] | About USD 22,000 per run[^32] |
| HGM[^79] | Agent code | Selection policy | Execution | SWE-Verified-60 56.7%[^79] | 47.8 vs 48.3 on the filtered split[^79] |
| Hyperagents[^42] | Task agent and meta-agent | Parent selection, evaluation protocol | Execution | Transfer imp@50 0.630 vs 0.0[^42] | Self-modified selector did not beat the handcrafted version[^42] |
| VERSE[^194] | Executor harness and the optimizer itself | Weights, data splits | Execution-based verification | 42.3% vs 39.2%[^194] | Without verification, round 0 is selected[^194] |
| SpecRSI[^123] | Successor agent; improver trained across rounds | Evaluator | Execution | 21.7 pp cumulative[^123] | Per-round increment 8.5→2.1[^123] |
| Evo²[^284] | Harness and evolver weights | Executor | Execution | Polyglot 82.1%[^284] | No limitations reported |
| Meta^n[^4] | Stacked meta levels | Meta-operation Ω | Execution | ARC-AGI-2 0.331[^4] | Depth saturates at 3–6[^4] |
| AIDE²[^1] | Research-agent code | Base model, tasks, evaluation | Hidden evaluation | 7 rewrites accepted[^1] | Ignition test 0.780 vs 0.782[^1] |
| MetaRSI[^102] | Data, harness and model operators, plus the scheduler | Sealed measurement, release rules | Execution + sealed measurement | 3.6 higher than the fixed pipeline[^102] | The authors state that all gains come from external inputs[^102] |

Putting Table 8-1 together with the evidence in Sections 8.1–8.4 yields five observations (our assessment).

**First, structural recursion is already widely implemented, but the evidence for effective recursion is very weak.**

- Modifying the improver and using it in later rounds is already a common design (based on [^64][^42][^194]).
- But experiments that directly test "whether an improved improver can drive the next round better" are rare, and their results are unclear: AIDE²'s ignition test ended without a clear winner[^1]; SpecRSI's increments shrink round by round[^123].

**Second, gains shrink round by round and saturate fairly quickly.**

- Shrinking increments: SpecRSI's per-round increment falls from 8.5 to 2.1 percentage points[^123].
- Depth saturation: Meta^n's depth saturates at 3–6 levels[^4].
- Early saturation: Co-Harness's 8B model saturates right after the first round[^155].

**Third, the base model sets the upper and lower bounds of the gains.**

- When the base model is too weak, the methods fail: STOP degrades when switched to weaker models[^167]; Live-SWE-agent gets stuck in loops on GPT-5-Nano[^36].
- When the base model is strong enough, the gains vanish: on o3-mini, SICA does worse than the model on its own[^195].
- Capability transfer is also limited by the base model: when Alita uses GPT-4o-mini to generate its own tools, GAIA drops from 72.73% to 43.64%[^290].

**Fourth, transfer cuts both ways.**

- Positive: agents discovered by DGM can transfer to Claude 3.7 Sonnet (19.0% to 59.5%)[^32].
- Negative: after DarwinX's harness is transferred to GPT-5.5, it scores below Terminus-2 on the held-out set[^282].

**Fifth, costs are so high that rigorous multi-seed, matched-budget comparisons are hard to run.**

- Cost of a single run: DGM about USD 22,000[^32]; GEA about USD 13,000[^128]; SICA about USD 7,000[^195].
- External evaluation is itself limited by cost: AIDE²'s evaluation is constrained by cost[^1].

### 8.6 Overfitting, Reward Hacking and Evaluator Gaming

In this strand, the system being improved often has access to whatever evaluates it, so reward hacking and evaluator gaming keep recurring.

**Altering or bypassing the evaluation.**

- In DGM's hallucination-detection case study, an agent fooled the detection by deleting the special-token logging that the detector relied on; such hacks were more frequent when the checking functions were visible[^32].
- SIFT's diagnosis agent tried to relax the timeout and retry settings of the evaluation harness and was stopped by file-permission restrictions[^9].
- HASE's evaluator was exploited twice during evolution before it was fixed through divergence gating[^211].
- Hyperagents showed degenerate behavior with a 99% acceptance rate[^42].

**Overfitting and evaluation setup.**

- DarwinX's training-subset score saturates at 1.000, while the held-out set reaches only 68.3%[^282].
- RRSI's re-evaluation found that existing harness evolvers bring almost no OOD gain[^31].
- Meta-Harness's search set is the same as its evaluation set[^17]; in MOSS, the evolution batch and the test set are the same four tasks, with no held-out set[^85].
- HGM no longer leads on the split that contains only unseen tasks[^79].
- Ouroboros's audits found reward hacking and data contamination[^149].

**The improver's ability to predict its own modifications.** AHE's data show that the improver predicts regressions only slightly better than chance[^174].

**A counterexample.** One counterexample is worth recording: AIDE²'s reward-hacking rate fell from 55% to 32% without any targeted optimization[^1].

**Effective defenses.** What the effective defenses have in common is a checkpoint, placed outside the system being improved, that the system cannot modify (our assessment):

- VERSE showed that execution-based verification is a prerequisite for optimizer self-evolution[^194].
- RQGM uses held-out ground truth to decide whether the evaluator may be replaced[^206].
- HASE allows evaluator edits only when the proxy and the oracle disagree[^211].
- DarwinX uses a "preserve and extend" contract to accept only variants that do not regress[^282].
- RRSI uses a critic and a pruner to prevent benchmark-specific edits[^31].

MetaRSI sums up this point as follows: the upper bound of what is reachable is the upper bound of verification[^102].

### 8.7 Summary (our assessment)

1. **Structural recursion has become a standard design; effective recursion has not been established.** From Gödel Agent to Hyperagents, VERSE and Evo², bringing the improver within the scope of modification has become very common. But multi-generation comparisons of improvers with matched budgets and identical starting points are lacking[^1]; the only direct ignition test ended without a clear winner (based on [^64][^42][^194]; see also [^284][^1]).
2. **The outermost layer always stays fixed.** In every system, at least one of parent selection, the evaluation protocol, the task distribution, the base-model weights or the sealed measurement cannot be modified. Today's "recursion" is recursion inside a fixed outer shell (based on [^42][^32]; see also [^102][^206]).
3. **Gains are front-loaded.** Shrinking per-round increments, depth saturation and first-round saturation form a consistent pattern; there is no evidence that gains self-accelerate (based on [^123][^4][^155]).
4. **The base model is both the ceiling and the floor.** A strong base model swallows the harness gains, and a weak one makes self-modification fail. Harness-level RSI cannot go beyond the model's capability; only co-evolving the weights can raise the ceiling, but doing so brings coupled Goodhart (based on [^195][^167][^36]; see also [^33][^211]).
5. **Verification is a precondition for improver self-modification, not an add-on.** Without execution-based verification or a ground-truth anchor, optimizer self-evolution makes results worse (based on [^194][^206][^102]).
6. **Evaluation methods lag behind the claims.** Sharing one set for search and evaluation, running only one round, relying solely on LLM judging and running only a few seeds are all widespread[^32]; overfitting and reward hacking have been reported by the authors themselves in several systems (based on [^17][^85][^280]; see also [^282][^31][^32]).
7. **The most valuable output of this strand is a set of engineering methods for "controlled self-modification", not a proof of RSI**: observable file-level edits, falsifiable edit predictions, non-regression contracts, divergence gating, auditing and rollback (based on [^174][^282]; see also [^211][^149]).

## References

[^73]: [Sheng & Padmanabhan — Self-Programming Artificial Intelligence Using Code-Generating Language Models (arXiv 2205.00167, 2022-04)](https://arxiv.org/pdf/2205.00167)
[^167]: [Zelikman et al. — Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation (arXiv 2310.02304, 2023-10)](https://arxiv.org/pdf/2310.02304)
[^288]: [Zhuge et al. — Language Agents as Optimizable Graphs (arXiv 2402.16823, 2024-02)](https://arxiv.org/html/2402.16823)
[^43]: [Hu et al. — Automated Design of Agentic Systems (arXiv 2408.08435, 2024-08)](https://arxiv.org/html/2408.08435)
[^49]: [Zhang et al. — AFlow: Automating Agentic Workflow Generation (arXiv 2410.10762, 2024-10)](https://arxiv.org/html/2410.10762)
[^287]: [Shang et al. — AgentSquare: Automatic LLM Agent Search in Modular Design Space (arXiv 2410.06153, 2024-10)](https://arxiv.org/html/2410.06153)
[^289]: [Zhang et al. — Multi-agent Architecture Search via Agentic Supernet (arXiv 2502.04180, 2025-02)](https://arxiv.org/html/2502.04180)
[^285]: [Nie et al. — Weak-for-Strong: Training Weak Meta-Agent to Harness Strong Executors (arXiv 2504.04785, 2025-04)](https://arxiv.org/html/2504.04785)
[^286]: [Zhou et al. — Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies (arXiv 2502.02533, 2025-02)](https://arxiv.org/html/2502.02533)
[^64]: [Yin et al. — Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement (arXiv 2410.04444, 2024-10)](https://arxiv.org/html/2410.04444)
[^195]: [Robeyns et al. — A Self-Improving Coding Agent (arXiv 2504.15228, 2025-04)](https://arxiv.org/html/2504.15228)
[^32]: [Zhang et al. — Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents (arXiv 2505.22954, 2025-05)](https://arxiv.org/html/2505.22954)
[^79]: [Wang et al. — Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine (arXiv 2510.21614, 2025-10)](https://arxiv.org/html/2510.21614)
[^36]: [Xia et al. — Live-SWE-agent: Can Software Engineering Agents Self-Evolve on the Fly? (arXiv 2511.13646, 2025-11)](https://arxiv.org/html/2511.13646)
[^128]: [Weng et al. — Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing (arXiv 2602.04837, 2026-02)](https://arxiv.org/html/2602.04837)
[^279]: [Liu et al. — Mendel Gödel Machine: Recursive Self-Improving Coding Agents via Comparative Evolution (arXiv 2608.07645, 2026-08)](https://arxiv.org/html/2608.07645)
[^9]: [Fu et al. — Self Improvement via Fast Tree-search (arXiv 2609.19526, 2026-09)](https://arxiv.org/html/2609.19526)
[^42]: [Zhang et al. — Hyperagents (arXiv 2603.19461, 2026-03)](https://arxiv.org/html/2603.19461)
[^292]: [Xie et al. — Predict Before You Modify: Learning Improvement Dynamics for Self-Evolving Agents (arXiv 2610.13991, 2026-09)](https://arxiv.org/html/2610.13991)
[^82]: [Liu et al. — Escher-Loop: Mutual Evolution by Closed-Loop Self-Referential Optimization (arXiv 2604.23472, 2026-04)](https://arxiv.org/html/2604.23472)
[^206]: [Iacob et al. — The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators (arXiv 2606.26294, 2026-06)](https://arxiv.org/html/2606.26294)
[^194]: [Wang et al. — VERSE: Verified Self-Evolving Optimizer for Agent Harnesses (arXiv 2610.02616, 2026-10)](https://arxiv.org/html/2610.02616)
[^123]: [Xu et al. — Drafting Agents, Not Just Tokens: Speculative Recursive Self-Improvement for Agentic Systems (arXiv 2610.16491, 2026-10)](https://arxiv.org/html/2610.16491)
[^284]: [Xu et al. — Evo\$^2\$: Evolving the Evolver through Weight-Harness Co-Evolution (arXiv 2610.13025, 2026-10)](https://arxiv.org/html/2610.13025)
[^291]: [Xue & Yang — Rethinking Self-Evolving Agents: Do We Still Need Prescribed Optimization Pipelines? (arXiv 2608.09629, 2026-08)](https://arxiv.org/html/2608.09629)
[^4]: [Kim et al. — Meta\$^n\$: Recursive Self-Improvement through Emergent Depth (arXiv 2608.24735, 2026-08)](https://arxiv.org/html/2608.24735)
[^102]: [Tan et al. — MetaRSI / RSI2: A Meta-Recursive Self-Improving System for Recursive Self-Improving Systems Themselves (arXiv 2609.06396, 2026-09)](https://arxiv.org/html/2609.06396)
[^145]: [Zhang et al. — RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent (arXiv 2610.21791, 2026-10)](https://arxiv.org/html/2610.21791)
[^149]: [Razzhigaev et al. — Ouroboros: A Self-Developing Frontier Coding Agent with Reviewed Core Evolution (arXiv 2608.08311, 2026-08)](https://arxiv.org/html/2608.08311)
[^1]: [Srikanth et al. — Recursive self-improvement of AI research agents (arXiv 2609.26457, 2026-09)](https://arxiv.org/html/2609.26457)
[^17]: [Lee et al. — Meta-Harness: End-to-End Optimization of Model Harnesses (arXiv 2603.28052, 2026-03)](https://arxiv.org/html/2603.28052)
[^174]: [Lin et al. — Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses (arXiv 2604.25850, 2026-04)](https://arxiv.org/html/2604.25850)
[^34]: [Zhang et al. — Self-Harness: Harnesses That Improve Themselves (arXiv 2606.09498, 2026-06)](https://arxiv.org/html/2606.09498)
[^280]: [Pan et al. — Evolving Agents in the Dark: Retrospective Harness Optimization via Self-Preference (arXiv 2606.05922, 2026-06)](https://arxiv.org/html/2606.05922)
[^191]: [Xu — Self-Evolving Harness on Multiple Tasks with the Agent as Its Own Optimizer (arXiv 2609.38372, 2026-09)](https://arxiv.org/html/2609.38372)
[^282]: [Zhang et al. — DarwinX: Evolving Agent Harnesses Through Natural Selection (arXiv 2608.07545, 2026-07)](https://arxiv.org/html/2608.07545)
[^31]: [Xia et al. — RRSI: Regularized Recursive Self-Improvement of Agent Harnesses (arXiv 2609.24972, 2026-09)](https://arxiv.org/html/2609.24972)
[^67]: [Xu et al. — Harness^2: Recursive Agent Harnessing for an Open World (arXiv 2610.14224, 2026-10)](https://arxiv.org/html/2610.14224)
[^108]: [Lee et al. — Recursive Harness Self-Improvement (arXiv 2607.15524, 2026-07)](https://arxiv.org/html/2607.15524)
[^33]: [Hebbar et al. — SIA: Self Improving AI with Harness & Weight Updates (arXiv 2605.27276, 2026-05)](https://arxiv.org/html/2605.27276)
[^211]: [Luo et al. — Harness-Aware Self-Evolving: Co-Evolving Model Weights, Harness, and Task Solutions (arXiv 2607.03935, 2026-07)](https://arxiv.org/html/2607.03935)
[^155]: [Chen et al. — Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents (arXiv 2607.22688, 2026-07)](https://arxiv.org/html/2607.22688)
[^281]: [Shao et al. — Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories (arXiv 2608.02276, 2026-08)](https://arxiv.org/html/2608.02276)
[^78]: [Fan & Huang — HELIX: Model-Harness Co-evolution for Recursive Self-Improvement (arXiv 2608.13951, 2026-08)](https://arxiv.org/html/2608.13951)
[^283]: [Yu et al. — Co-Evolving Harnesses and Models: On-Policy Correction Helps Weaker Models Catch Up Where Imitation Fails (arXiv 2609.09134, 2026-09)](https://arxiv.org/html/2609.09134)
[^101]: [Xue et al. — ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents (arXiv 2609.17523, 2026-09)](https://arxiv.org/html/2609.17523)
[^290]: [Qiu et al. — Alita: Generalist Agent Enabling Scalable Agentic Reasoning with Minimal Predefinition and Maximal Self-Evolution (arXiv 2505.20286, 2025-05)](https://arxiv.org/html/2505.20286)
[^85]: [Cai et al. — MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems (arXiv 2605.22794, 2026-05)](https://arxiv.org/html/2605.22794)
