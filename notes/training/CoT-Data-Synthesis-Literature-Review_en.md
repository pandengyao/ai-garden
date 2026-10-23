# Chain-of-Thought Synthesis for Training Data: Methods, Evidence, and Open Problems

[中文](./CoT-Data-Synthesis-Literature-Review.md) | English

- **Research date**: 2026-10-22 (evidence cutoff: first arXiv version no later than 2026-10-22)
- **Scope**: how chain-of-thought traces for training are built: supervised fine-tuning and distillation data, including agentic trajectories and on-policy distillation; reinforcement learning is covered only for question construction and difficulty control. Mainly arXiv. Keyword search and citation expansion produced 13,589 candidate papers; 2,591 were coded on title and abstract, 1,527 were included, and 237 sources were read in full (our count). Section 2 describes the search and screening method.
- **Structure**: the review spans 8 pages. This page holds the abstract, Sections 1–3 (introduction, search method, taxonomy), Sections 11–13 (synthesis, open problems, conclusion) and the appendices; Sections 4–10 each have their own page, listed in the "Sections 4–10" section of this page.
- **Basis**: superscript numbers at the end of a sentence are citations to the sources read in full, listed under References at the end; every citation is backed by verbatim text excerpted from the source's full text and checked against it by script. Content marked (our assessment), (our inference) or (our count) is this review's own synthesis or counting, not the sources' words.

## Abstract

Reasoning traces (chains of thought) have become the most expensive and most widely reused component of post-training data for large language models. Following a systematic literature-review protocol, we searched work published between January 2022 and October 2026. From 13,589 candidate papers we coded 2,591 and included 1,527 (our count). We read 237 sources in full and extracted verbatim evidence from each (our count).

We propose a taxonomy organized around the data pipeline. Along it we review representative methods and controlled experimental findings in five areas: question and task sources, trace generation, verification and labelling, selection and scaling, and agentic trajectory synthesis. Risks of synthetic reasoning data are discussed separately. The analysis shows three things:

- The field has shifted from collecting more questions toward sampling many traces per question and selecting them for the student, and in 2026 it moved rapidly toward on-policy distillation. Task diversity, by contrast, is the bottleneck for code and agentic data.
- Four common intuitions each have well-designed counterexamples: stronger teachers are better, answer-correct traces are better, more data is better, and verification always helps. Whether each holds depends on student scale, the teacher-student distribution gap, and the training budget.
- Answer-conditioned generation, length penalties, and recursive self-training can damage data in ways that answer accuracy does not reveal.

We close by tabulating six contradictory findings together with testable reconciling variables, and by identifying seven open problems.

**Key words**: chain of thought; reasoning data synthesis; knowledge distillation; supervised fine-tuning; on-policy distillation; data selection; large language models

## 1 Introduction

### 1.1 Background

Wei et al. found that giving a series of intermediate reasoning steps in the prompt significantly improves the ability of large language models to perform complex reasoning[^68]. This finding soon extended from an inference-time technique to a source of training signal. Distilling Step-by-Step uses the rationales produced by a large model as additional supervision in a multi-task framework to train small models[^73], and the fine-tuned 770M T5 model outperformed the 540B PaLM under few-shot prompting[^73]. STaR has the model generate rationales for questions, regenerates them with the correct answer as a hint when the answer is wrong, fine-tunes only on the rationales that end in a correct answer, and iterates[^82]. Orca, in turn, learns directly from GPT-4's explanation traces and step-by-step thought processes[^67].

In early 2025, long chain of thought (long CoT) raised both the scale and the importance of this direction. DeepSeek-R1 collected about 600k reasoning-related training samples[^80], plus about 200k samples unrelated to reasoning[^80]. One of its conclusions directly drove later data work: distilling a stronger model into small models works very well, whereas small models that rely on large-scale reinforcement learning (RL) need enormous compute and do not necessarily reach the performance of distillation[^80].

Subsequent work moved toward two extremes in data scale (our assessment):

- **Small and curated.** s1 tested three selection criteria (difficulty, diversity and quality) on 1,000 questions[^86]. LIMO proposed the "less is more" reasoning hypothesis[^72].
- **Large scale.** After more than 1,000 ablation experiments, OpenThoughts scaled its data to 1.2M samples[^4].

By 2026, the field had seen three changes (our assessment).

1. **Models with fully open data recipes appeared.** Olmo 3 published how its reasoning supervised fine-tuning (SFT) data was constructed[^10]. ZGCM-1 open-sourced the data and data recipes of every stage[^45].
2. **The object of synthesis expanded from single-turn problem solving to multi-turn agentic trajectories.** OpenThoughts-Agent provides a fully open pipeline for curating agent data[^34].
3. **Offline trace distillation is gradually giving way to on-policy distillation.** Qwen3 uses both off-policy and on-policy strong-to-weak distillation for its small models[^70]. Ask to Distill points out that on-policy distillation works with very few training questions[^56]. By our count of the corpus, included papers whose abstracts mention on-policy distillation numbered only 2 in the second half of 2025 but already 79 in the first half of 2026 (our count).

At the same time, several conclusions in this field conflict with each other. After scaling to 1.2M samples, OpenThoughts claimed "more-is-more"[^57]. ZGCM-1, by contrast, found that after pruning about half of the candidate pool, the mean over six benchmarks rose from 67.78 to 68.83[^45].

On teacher choice:

- OpenThoughts found that QwQ-32B is weaker than DeepSeek-R1 on the target benchmarks yet is the better teacher[^4].
- AM ran a comparison on the same 1.89 million queries[^60]. A student trained on data distilled from AM-Thinking-v1 scored 84.3 on AIME2024, while one trained on data distilled from DeepSeek-R1 scored only 70.9[^60].

On verification:

- OpenThoughts tried several verification and answer-filtering methods, and none brought a significant improvement[^4].
- AM's entire pipeline, however, is built on verification that differs by question type[^1].

We argue that most of these conflicts are not a matter of one side being right and the other wrong, but of differing experimental conditions (our assessment).

### 1.2 Existing Surveys and the Position of This Review

Existing surveys cover this field from different angles and can be divided into four categories by how they are organized (our assessment).

**First category: organized by reasoning method, with data construction as just one section.** An early survey of mathematical reasoning divides fine-tuning methods into several branches, such as in-context example selection, generating intermediate steps, learning answer verifiers, augmenting datasets and teacher-student distillation[^221]. The survey "From System 1 to System 2" groups the construction of reasoning models into five core methods: structure search, reward modeling, self-improvement, macro actions and reinforcement fine-tuning[^222]. One focus of the survey on reinforced reasoning is automated data construction[^224]. It describes how reasoning annotation shifted from human annotation to automatic annotation by LLMs[^224]. The survey on efficient reasoning addresses the verbosity cost of long CoT[^223] and divides methods into three types: model-based, reasoning-output-based and input-prompt-based[^223]. The survey on long CoT, in turn, is organized around three characteristics: deep reasoning, extensive exploration and feasible reflection[^77].

**Second category: synthetic data as the object.** The survey on LLM-driven synthetic data organizes the literature by the general workflow of data generation[^76]. A survey of synthetic data for text and code selects literature from January 2020 to April 2025 with a PRISMA-style process[^226] and gives a taxonomy of three types of pipelines: prompt-based, retrieval-augmented and iterative self-refinement[^226]. The survey on synthetic-data best practices points out that synthetic data may contain rephrased versions of benchmark questions, which defeats token-level decontamination[^227]. The survey on knowledge distillation of LLMs divides knowledge elicitation strategies into labeling, expansion, curation, feature, feedback and self-knowledge generation, among others[^84].

**Third category: dedicated to a single paradigm or data form.** The survey on on-policy distillation organizes the literature along three dimensions: the states the student visits, the information used to construct supervision, and the updates the supervision induces[^225]. It points out that training the student on histories given by the teacher leaves the student without supervision on the histories it encounters when it generates on its own[^225]. The survey on CoT fine-tuning uses the "Six Thinking Hats" framework to classify CoT fine-tuning methods[^229]. The survey on agent data represents agent data as a quadruple of environment, task signal, interaction realization and an optional verifier[^230], and notes that the literature is shifting toward execution-grounded correctness and difficulty relative to the learner[^230].

**Fourth category: the two works closest to this review.**

- The survey of DeepSeek-R1 replications summarizes the SFT and RL data used in open-source replications[^228] and lists the sizes of a series of open-source datasets, from DeepSeek-R1's 800k to LIMO's 817 samples[^228]. It also notes that only the technical reports of Light-R1 and LIMO explicitly mention decontamination against common reasoning benchmarks[^228].
- A 2026 introductory survey of post-training reasoning data describes itself as synthesizing more than 150 public studies and system reports[^231]. It organizes the literature around four questions, "what data objects exist, what makes data useful, how to construct it, and how to scale it"[^231], and states that the authors did not rerun the training recipes or audit contamination[^231].

This review differs from the above work in three respects (our assessment):

1. **The data pipeline as the axis.** This review organizes the literature by the stages "question sources, trace generation, verification, selection and scale", rather than by reasoning method or training paradigm.
2. **Literature scale and verifiability.** Following a systematic-review protocol, we searched and screened 2,591 candidate papers, included 1,527, and read 237 sources in full with verbatim evidence extraction (our count).
3. **A focus on controlled evidence.** For the many controlled experiments of 2025–2026, we record the teacher, student, benchmarks and data scale in a uniform way, and present contradictory conclusions side by side.

### 1.3 Contributions and Structure

This review makes four contributions (our assessment):

1. **Taxonomy.** We propose a taxonomy organized around the data pipeline (Section 3).
2. **A stage-by-stage review.** We review representative methods and controlled experimental findings in five areas, namely question sources, trace generation, verification, selection and scale, and agentic trajectories (Sections 5–9), and use Section 4 to review how the field developed in 2022–2024.
3. **Failure modes and contradictions.** We summarize the main failure modes of synthetic reasoning data and compile several sets of contradictory findings together with testable reconciling variables (see Sections 10 and 11, our assessment).
4. **A verifiable method record.** We record the entire search, screening and coding process (Section 2).

This review does not discuss inference-time CoT prompting techniques, nor work that only evaluates without constructing training data (our assessment). Multimodal CoT data is outside the scope of this review (our assessment).

## 2 Literature Search and Research Methods

This review organizes search, screening and evidence extraction according to the general procedure of a systematic literature review (our assessment). The search logs, per-paper screening records and the list of included papers are not published with this page; this section gives the rules and counts for each step.

### 2.1 Research Questions

This review is organized around four questions (our assessment):

- **RQ1**: For the reasoning traces used in SFT and distillation, where do the questions come from, and who generates the traces?
- **RQ2**: What checks decide whether a trace is retained, and what are the costs and errors of each kind of check?
- **RQ3**: For data volume, samples per question, length and mixture ratio, which choices are supported by controlled experiments, and which conclusions conflict?
- **RQ4**: In what ways can synthetic reasoning data fail, and how strong is the evidence for existing mitigations?

### 2.2 Search Strategy

The search sources were the arXiv API (title and abstract fields) and the Semantic Scholar Graph API (citing papers and citation counts), covering 2022-01-01 to 2026-10-22 (our count). For keyword search, we wrote one or more groups of queries for each of the nine directions of the predefined taxonomy, 64 groups in total (our count). The raw hits of all query groups totaled 13,327, which gave 9,593 papers after deduplication (our count).

To offset the dependence of keyword search on wording, we selected representative seed papers in each direction, 23 in total (our count), and retrieved all of their citing papers that have arXiv IDs through Semantic Scholar. This step yielded 9,306 distinct papers (our count). For those not covered by keyword search, we retrieved metadata under the rule "the title contains a topic term, the paper cites several seeds, or it has at least 150 citations", adding 3,975 papers (our count).

The recall check used as its benchmark the 84 arXiv papers cited in the earlier survey plus 62 landmark papers of the field, 146 in total (our count). With keyword search alone, recall was 79% (our count); after adding citation expansion, recall rose to 86% (our count). The 20 papers still not recalled were added to the candidate pool directly by ID (our count). The merged candidate pool totaled 13,589 papers (our count).

### 2.3 Screening and Coding

**Prefilter.** The candidate pool first went through a rule-based prefilter: titles and abstracts were scored with topic regular expressions and ranked together with subject category, citation count and the number of seeds cited (our assessment). The cutoff was set after reading samples from each score band, and highly cited papers with a topic term in the title, as well as all recall-benchmark papers, were kept unconditionally. In total, 2,591 papers entered manual coding and screening (our count).

**Codebook.** Screening followed a uniform codebook, with judgments based on titles and abstracts only. Included papers were coded in five fields (category, importance tier, trace generator, retention criterion and domain), and the reason for exclusion was recorded for excluded papers (our assessment). The screening set was split into 9 blocks interleaved by citation rank and handled by 9 parallel LLM coding agents, about 288 papers per block (our count).

**Audit.** After merging, we ran three audits (our assessment):

1. Check the decisions on all recall-benchmark papers.
2. Re-examine, one by one, the papers that were "excluded but have at least 150 citations or a topic term in the title" (our assessment).
3. Check papers that were cut at the prefilter stage but are highly cited and have a topic term in the title.

In total, the audits manually reclassified 7 papers (our count). Among them, Textbooks Are All You Need[^112] had originally been classed as general pretraining data; because its practice of synthesizing "textbooks and exercises" is a direct precursor of reasoning data synthesis, it was reclassified as included (our assessment). The 15 unscreened, highly cited papers found by the third audit are all multimodal CoT work, which falls within the scope this review explicitly excludes (our count).

Table 2-1 Literature search and screening process (our count)

| Stage | Count (papers) |
| --- | ---: |
| Keyword search: raw hits of 64 query groups | 13,327 |
| Keyword search: after deduplication | 9,593 |
| Citation expansion: citing papers of 23 seeds (deduplicated) | 9,306 |
| Citation expansion: added to the pool by rule | 3,975 |
| Added after the recall check | 20 |
| Added manually (found during checks after the search) | 1 |
| Candidate pool total | 13,589 |
| Entered coding and screening after the rule-based prefilter | 2,591 |
| Excluded | 1,064 |
| Included (Tier A 149, Tier B 390, Tier C 988) | 1,527 |
| Read in full with verbatim evidence extraction (including the 84 arXiv papers and 7 dataset cards, blogs, etc. from the earlier survey) | 237 |

Among the exclusion reasons, inference-time techniques (which produce no training data) account for 240 papers, narrow-domain applications 222, pure RL algorithms 153, pure evaluation 128 and other reasons 321 (our count).

### 2.4 Full-Text Reading and Evidence Extraction

The set read in full consists of two parts (our assessment):

- The 91 sources already read in full in the earlier survey, comprising 84 arXiv papers and 7 dataset cards, blogs and code-repository documents (our count).
- The 146 papers added in this round, selected by category from Tiers A and B (our count). The selection principle was that the foundational work, highly cited representative work and recent progress of 2026 in every direction are all covered.

After the full texts of all papers were fetched, they were assigned by eight themes to parallel LLM evidence-extraction agents (our assessment). Every claim had to come with a quote that matches the original text verbatim, and it was used only after a script had checked the quote against the full text. Every number in the body of this review can be found in the verbatim quotes from the corresponding paper (our assessment).

Throughout the text, sentences tagged (our assessment), (our inference) or (our count) are syntheses or calculations by the authors of this review based on the evidence, not conclusions of the cited papers.

### 2.5 Corpus Overview

Figure 2-1 shows the distribution of included papers over time (our count):

- 28 papers in 2022, 76 in 2023 and 184 in 2024 (our count).
- In 2025 the number surged to 606, and 2026 already has 633 as of October 22 (our count).

The growth occurred mainly after the release of DeepSeek-R1 in 2025 (our inference). Within this, the "trace generation" area had 118 papers in the first half of 2026 alone (our count). Included papers whose abstracts mention on-policy distillation numbered only 2 in the second half of 2025, rose to 79 in the first half of 2026, and stand at 109 for the second half (not yet complete) (our count). This shows that within one year the direction went from a marginal method to one of the main directions (our assessment).

![Figure 2-1 Included papers by half-year and category, and the number of them that mention on-policy distillation](./img/CoT-Data-Synthesis-Literature-Review-growth.png)

*Figure 2-1 Included papers by half-year and category, and the number of them that mention on-policy distillation (our count; coded from titles and abstracts, with the second half of 2026 up to October 22).*

Table 2-2 Distribution of included papers by category and tier (our count; coded from titles and abstracts)

| Category | Included papers | Tier A | Tier B | Tier C |
| --- | ---: | ---: | ---: | ---: |
| R Recipes and datasets | 92 | 24 | 30 | 38 |
| Q Question synthesis | 104 | 15 | 47 | 42 |
| G Trace generation | 427 | 32 | 64 | 331 |
| V Verification and labeling | 156 | 11 | 23 | 122 |
| S Selection, scale and length | 231 | 10 | 69 | 152 |
| T Teacher-student mechanism analysis | 174 | 12 | 52 | 110 |
| A Agentic trajectories | 130 | 14 | 52 | 64 |
| F Risks and failures | 145 | 12 | 31 | 102 |
| Y Surveys and position papers | 68 | 19 | 22 | 27 |
| Total | 1527 | 149 | 390 | 988 |

From the coding results (our count):

- **Trace generators.** In the "trace generation" category, 154 papers have the model itself generate the traces, more than the 113 that have a stronger teacher generate them (our count).
- **Retention criteria.** Answer matching is the retention criterion in 82 papers, while 55 explicitly apply no correctness filtering (our count).
- **Domain distribution.** General reasoning accounts for 683 papers, mathematics 356, multi-domain 189 and agents 154, while code and science have only 49 and 17, respectively (our count).

Math questions have reference answers that can be matched automatically; this may be the main reason the literature in this area concentrates on mathematics (our inference).

Table 2-3 Distribution of trace generators among the papers in each category (our count; coded from abstracts, "not applicable" means the paper does not involve trace generation)

| Category | Teacher model | The model itself | Search | Mixed | Human | Not applicable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| R | 47 | 14 | 0 | 15 | 1 | 15 |
| Q | 48 | 33 | 0 | 3 | 0 | 20 |
| G | 113 | 154 | 26 | 111 | 2 | 21 |
| V | 13 | 77 | 8 | 7 | 0 | 51 |
| S | 84 | 69 | 2 | 17 | 3 | 56 |
| T | 70 | 21 | 5 | 21 | 2 | 55 |
| A | 54 | 32 | 5 | 16 | 0 | 23 |

Table 2-4 Distribution of retention criteria adopted by the papers in each category (our count; coded from abstracts)

| Category | Answer matching | Execution/testing | Process reward | LLM judge | Formal | Mixed | No filtering | Not applicable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R | 15 | 8 | 0 | 2 | 5 | 15 | 9 | 38 |
| Q | 28 | 16 | 0 | 4 | 2 | 3 | 9 | 42 |
| G | 82 | 7 | 5 | 18 | 2 | 14 | 55 | 244 |
| V | 17 | 10 | 68 | 21 | 14 | 12 | 1 | 13 |
| S | 54 | 0 | 0 | 1 | 0 | 5 | 26 | 145 |
| T | 23 | 0 | 0 | 0 | 0 | 1 | 17 | 133 |
| A | 16 | 18 | 1 | 7 | 0 | 13 | 5 | 70 |

### 2.6 Limitations

The search and screening of this review have four limitations (our assessment):

- The search relies mainly on arXiv, so work that was formally published but never posted as a preprint may be missed.
- Screening relied only on titles and abstracts, and tiering and coding were done by multiple LLM agents; although they were audited, inconsistent judgments may remain.
- Much of the 2026 literature has not yet been peer-reviewed, and the robustness of its conclusions remains to be tested.
- Citation counts are taken from Semantic Scholar, and the counts for recent preprints are generally on the low side.

## 3 Problem Definition and Taxonomy

### 3.1 Basic Objects

**Definition 1 (CoT training sample)**: A training sample is a triple $`(q, r, a)`$ (our assessment).

- $`q`$ is the question or task description, $`r`$ is the reasoning trace, and $`a`$ is the final answer.
- In agentic settings, $`r`$ extends to a multi-turn sequence in which thinking, tool calls and environment observations alternate.
- A survey of agent data represents such data as a quadruple consisting of an environment specification, a task signal, an interaction implementation and an optional verifier[^230].

**Definition 2 (synthesis pipeline)**: A CoT data synthesis pipeline is a mapping from the question source to the training set (our assessment):

```math
\mathcal{D} = \mathcal{S}\Big(\big\{(q, r, a) : q \in \mathcal{Q},\ r \sim \mathcal{G}(\cdot \mid q),\ \mathcal{V}(q, r, a) = 1\big\}\Big)
```

- $`\mathcal{Q}`$ is the question source.
- $`\mathcal{G}`$ is the trace generator, which can be a stronger teacher model, the model itself or a search process.
- $`\mathcal{V}`$ is the retention criterion, that is, the verifier.
- $`\mathcal{S}`$ is the selection strategy over data volume, difficulty, length and mixture ratio (our assessment).

Under this definition, the training objective is usually to minimize the student's negative log-likelihood on the retained traces (our assessment):

```math
\mathcal{L}_{\mathrm{SFT}}(\theta) = -\mathbb{E}_{(q, r, a) \sim \mathcal{D}} \sum_{t} \log p_\theta\big(y_t \mid y_{<t}, q\big), \quad y = (r, a)
```

**On-policy distillation changes this structure (our assessment).** Traces are no longer pre-generated by $`\mathcal{G}`$ but sampled by the student itself. The teacher provides token-level supervision only on the states the student visits. A survey of on-policy distillation points out that when the student trains on reference answers or teacher-generated responses, it learns on histories supplied by another source, whereas at generation time it relies on its own earlier predictions[^225]. This is exactly the mismatch that on-policy methods aim to eliminate[^225].

### 3.2 Taxonomy

Existing work has proposed several classifications.

- A resource index for long CoT classifies datasets by construction method into four types: human annotation, direct distillation, search-based distillation and verified distillation[^63].
- An introductory survey of post-training reasoning data orders data by its "verification contract": where feedback enters, what becomes trainable, and which fields make the signal auditable[^231].
- A survey of reinforced reasoning describes how reasoning annotation shifted from human annotation to automatic annotation by LLMs[^224].

Building on this, we construct a taxonomy organized by the stages of the data pipeline (see Figure 3-1 and Table 3-1; our assessment). The two dimensions of the taxonomy are "pipeline stage" and "signal source". The stages correspond to $`\mathcal{Q}`$, $`\mathcal{G}`$, $`\mathcal{V}`$ and $`\mathcal{S}`$ in Definition 2. The signal source distinguishes human, stronger teacher, the model itself, search and environment execution, and is reflected in the contents of the boxes in Figure 3-1 and in the coding of Tables 2-3 and 2-4 (our assessment).

![Figure 3-1 The taxonomy of this review](./img/CoT-Data-Synthesis-Literature-Review-taxonomy.png)

*Figure 3-1 The taxonomy of this review (our assessment).*

Table 3-1 Typical designs and representative work for each stage of the taxonomy (our assessment; see the corresponding sections for the specific conclusions of the representative work)

| Stage | Core question | Typical designs | Section |
| --- | --- | --- | --- |
| Question sources $`\mathcal{Q}`$ | Where questions come from, whether answers can be judged correct automatically, and how difficulty is controlled | Reusing and rewriting existing question banks; mining from the web and documents; synthesizing from personas, skills or code; controlling difficulty by pass rate; questions self-posed by the model | 5 |
| Trace generation $`\mathcal{G}`$ | Who writes the reasoning process | Offline distillation from a stronger teacher; rejection sampling by the model itself; tree search and evolution; on-policy distillation; off-policy guidance in RL | 6 |
| Retention criteria $`\mathcal{V}`$ | What kind of trace counts as acceptable | Answer matching; code execution and testing; process rewards and step labeling; generative verifiers and judge models; formal verification | 7 |
| Selection and scale $`\mathcal{S}`$ | Which traces to keep, how many, and how long | Small curated sets and scaling up; samples per question and repeated epochs; difficulty bands and curricula; length and compression; teacher-student fit | 8 |
| Agentic trajectories | How multi-turn tool-interaction data is constructed | Environment and task synthesis; execution by strong agents; judging success by environment reward, tests or the final answer | 9 |
| Risks | In what ways synthetic data can fail | Model collapse; unfaithful traces; reduced monitorability; trait transfer and contamination; extraction of reasoning traces and anti-distillation | 10 |

### 3.3 Pipelines in Six Technical Reports

Comparing six representative technical reports from 2024–2025 against this taxonomy reveals two branches (our assessment): one distills a stronger teacher, and the other relies on the model's own rejection sampling or RL.

**The teacher-distillation branch.**

- **Tülu 3.** Conditioned on about 250K Persona Hub personas, it generates questions targeting instruction following, mathematics and code[^232]. Multi-step math solutions are generated by GPT-4o, and code by claude-3-5-sonnet[^232]. Decontamination uses 8-gram matching[^232]. In the leave-one-out ablation of Tülu 3 8B SFT, removing the math data lowers GSM from 76.2 to 64.1 and MATH from 31.5 to 23.5[^232].
- **STILL-2.** It uses two o1-like systems, DeepSeek-R1-Lite-Preview and QwQ-32B-preview, as teachers[^233]. Just 3.9K preprocessed distillation samples bring the student to 46.7% on AIME and 90.2% on MATH-OAI[^233]; the backbone model scores 13.3 and 80.0, respectively[^233].
- **O1 Replication Journey Part 2.** With supervised fine-tuning on only tens of thousands of long CoTs distilled from O1, the base model already surpasses O1-preview on AIME[^234]. The authors also point out that the distilled model is necessarily bounded by the teacher's capability, so there is an implicit ceiling effect[^234].

**The self-generation and RL branch.**

- **DeepSeekMath.** Its SFT data totals 776K samples, with solutions in three formats: chain-of-thought, program-of-thought and tool-integrated[^235]. The RL stage uses about 144K questions, sampling 64 outputs per question[^235]. Its unified-paradigm analysis finds that Online RFT, which samples from the real-time policy, significantly outperforms RFT, which samples from the initial SFT model[^235]. But RL improves only Maj@K, not Pass@K[^235].
- **Qwen2.5-Math.** It iteratively improves responses with rejection sampling guided by a reward model[^236], and the final CoT training set contains 2000K English samples and 500K Chinese samples[^236]. The RL stage keeps only the questions for which 2 to 5 of 8 responses are correct, 66K questions in total[^236].
- **Kimi k1.5.** It uses the pass rate over 10 samples from the supervised fine-tuned model as a proxy for question difficulty[^237]. To avoid false positives caused by "reaching the correct answer through incorrect reasoning", it excludes multiple-choice, true/false and proof questions[^237]. In manual spot checks, the accuracy of the conventional reward model is about 84.4, versus 98.5 for the CoT reward model[^237].

Table 3-2 Comparison of the reasoning-data pipelines in six technical reports (based on the citations in each row)

| Report | Question source | Trace generator | Retention criterion | Scale |
| --- | --- | --- | --- | --- |
| Tülu 3 | Public datasets plus persona-driven synthetic questions | GPT-4o (math), claude-3-5-sonnet (code) | Binary verifier in the RL stage; 8-gram decontamination | About 30,000 prompts with reference answers for RL[^232] |
| STILL-2 | Competition math, code and science questions | DeepSeek-R1-Lite-Preview, QwQ-32B-preview | Answer correctness and rule-based cleaning | 3.9K distillation samples[^233] |
| O1 Replication Journey Part 2 | Competition-level math questions | O1 | No detailed description found (our assessment) | Tens of thousands of long CoTs[^234] |
| DeepSeekMath | GSM8K, MATH and others | Annotated solutions and policy sampling | Scored by a reward model in the RL stage | 776K samples for SFT; about 144K questions for RL[^235] |
| Qwen2.5-Math | Annotated and synthetic questions | The current strongest model itself | Answer matching or weighted voting, then the top k by reward model[^236] | 2000K English and 500K Chinese samples[^236] |
| Kimi k1.5 | STEM, competition and general reasoning questions | The RL policy | Pass-rate difficulty; CoT reward model[^237] | About 800K CoT-annotated samples to train the reward model[^237] |

The two branches correspond to the same trade-off (our assessment):

- Distillation has a low startup cost but is bounded by the teacher's ceiling[^234].
- Self-generation and RL can surpass the teacher but depend more on verifiers and question coverage[^237].
- DeepSeekMath's Maj@K and Pass@K results suggest that the gains from RL may come more from sharpening the existing output distribution than from expanding the capability boundary[^235].

### 3.4 Commonalities and Gaps in Public Pipelines

Within this taxonomy, the typical supervised fine-tuning data pipeline in open-source replications can be described as follows (our assessment):

- Questions are taken from benchmark training sets or web crawls[^228].
- They go through multiple rounds of filtering by deduplication, rejection sampling and verification against reference answers[^228].
- Verification methods differ by domain: math questions commonly use Math Verify, code questions use execution or unit tests, and general tasks use LLM-as-judge[^228].

A survey of CoT fine-tuning divides the acquisition of CoT data into two types, human annotation and automatic annotation[^229]. In automatic annotation, a common practice is to use an answer verifier to discard CoTs whose final answers conflict with the reference answers[^229].

However, a correct answer does not guarantee a correct reasoning process. A survey of synthetic data points out that LLMs may arrive at correct answers through incorrect explanations, and vice versa[^226]. This point runs through the following sections (our assessment):

- Section 7 discusses to what extent verifiers can close this gap.
- Section 8 discusses whether traces with wrong answers still have training value.
- Section 10 discusses why traces with correct answers may still be unfaithful.

## Sections 4–10

Sections 4–10 each have their own page:

- [4 Historical Development: From Rationale Distillation to Long Chain of Thought](./CoT-Data-Synthesis-Literature-Review-Ch04_en.md)
- [5 Question and Task Sources](./CoT-Data-Synthesis-Literature-Review-Ch05_en.md)
- [6 Trace Generation: Teachers, Self, and Search](./CoT-Data-Synthesis-Literature-Review-Ch06_en.md)
- [7 Verification and Labeling: What Counts as an Acceptable Trace](./CoT-Data-Synthesis-Literature-Review-Ch07_en.md)
- [8 Selection, Scale and Length](./CoT-Data-Synthesis-Literature-Review-Ch08_en.md)
- [9 Synthesis of Agentic Trajectories](./CoT-Data-Synthesis-Literature-Review-Ch09_en.md)
- [10 Risks and Failure Modes](./CoT-Data-Synthesis-Literature-Review-Ch10_en.md)

## 11 General Discussion: Contradictory Conclusions and Reconciling Variables

The preceding sections discussed the individual stages of the pipeline separately. Viewed together, these conclusions include six groups that clearly conflict with one another (our assessment).

This section proceeds as follows: it first juxtaposes the evidence on both sides together with the experimental conditions, and then gives the variables most likely to explain the disagreement (our assessment). These reconciling variables are all our inferences and can be tested with controlled experiments (our assessment).

### 11.1 Whether More Data Is Better or Less but Curated Data Is Better

**Evidence for scaling up.**

- After scaling up to 1.2M samples, OpenThoughts claims that "more is more"[^57].
- NaturalThoughts finds that scaling up the data by random sampling is a strong baseline, with performance growing steadily[^5].

**Evidence for less but curated data.**

- Using only very few samples, LIMO reaches 63.3% on AIME24 and 95.6% on MATH500[^72].
- The 5% of the data selected by LESS often outperforms training on the full dataset[^164].
- With only 10% of the data, Select2Reason matches or exceeds full-data fine-tuning[^173].
- After ZGCM-1 prunes about half of the candidate pool, its average over six benchmarks rises from 67.78 to 68.83[^45].

**We argue that three variables most likely explain this disagreement (our inference).**

1. **Whether the base model already has the relevant knowledge.** LIMO's hypothesis explicitly presupposes that "domain knowledge has been fully encoded during pre-training"[^72]. Under this premise, a small number of demonstrations merely activates existing capabilities (our inference).
2. **Whether the candidate pool has already been prefiltered by the teacher.** If the candidate pool has already been prefiltered by the teacher, the marginal value of the remaining data is already relatively low, and pruning shows its effect more easily (our inference).
3. **Whether the comparison controls the training budget.** Most subset comparisons give every subset the same number of epochs, so a subset actually receives fewer optimization steps (our assessment, based on [^173][^164]). The results of DataRepetition show that under a fixed update budget this changes the conclusion[^18]; Olmo3-7B trained for 128 epochs on 400 long-CoT samples scores 12 to 26 percentage points higher than when trained for 1 epoch on 51,200 samples[^18].

In addition, a survey of open-source replications points out that cross-project comparisons confound the dataset with the starting checkpoint[^228]. Only the DeepSeek-R1 distillation series and AM fine-tune from base models; the remaining methods rely on stronger Instruct models[^228].

### 11.2 Whether a Stronger Teacher Is Better

**Evidence for "the stronger the teacher, the better".**

- AM compares three teachers on the same batch of queries[^180]. The student trained on data distilled from AM-Thinking-v1 scores 84.3 on AIME2024, while the one trained on data distilled from DeepSeek-R1 scores only 70.9[^180].
- RevisitCapacityGap finds that when the performance gap between candidate teachers is large, the stronger teacher is often preferable[^22].

**Evidence for "a stronger teacher is not necessarily better".**

- OpenThoughts finds that QwQ-32B, although weaker than DeepSeek-R1 on the target reasoning benchmarks, is the better teacher[^4].
- In distillation during the pre-training stage, further strengthening the teacher may cause the distillation gains to saturate or even reverse[^30].
- Ask to Distill finds that for a Qwen3-4B student, the teacher-gap recovery rate is 82.9% with a 4B teacher but only 32.8% with the stronger 30B-A3B teacher[^56].
- PerSyn finds that the router assigns more questions to smaller teachers, such as Qwen2.5-3B-Instruct[^181].

**We argue that three variables most likely explain this disagreement (our inference).**

1. **The gap between candidate teachers.**
2. **Student scale.**
3. **How close the teacher and the student are in thinking patterns and distribution.**

There is direct evidence for all three variables:

- Research on the learnability gap of small models shows that students with no more than 3B parameters cannot consistently benefit from long CoT or from distillation from large models[^71].
- RSR argues that the key to distillation is "the fit between the data and the student"[^13].
- ForcedReasoning observes that the strongest teachers write the most compressed traces, and compressed traces happen to omit exactly the steps that weaker students cannot fill in on their own[^64].
- A systematic study of on-policy distillation gives two conditions for success[^144], namely that the student and the teacher have compatible thinking patterns, and that the teacher can provide new capabilities the student has not yet seen.

### 11.3 Whether Verification and Filtering Help

**Evidence that filtering helps.**

- AM's pipeline is built on verification that differs by question type: math questions are checked against reference answers, code questions are run against test cases, and other tasks rely on a reward model[^1].
- After AgentTuning's agentic trajectories are filtered, results on two sets of evaluations rise from 1.34 to 1.96 and from 0.47 to 0.65, respectively[^186].

**Evidence that filtering does not help.**

- OpenThoughts tried several verification and answer-filtering methods, and none brought a significant improvement[^4].
- OpenResearcher fixes the student, the training recipe and the evaluation protocol, and varies only the trajectories used for fine-tuning[^202]. Using only correct trajectories yields 54.81%, using only incorrect trajectories yields 55.06%, and mixing them yields 54.46%[^202].

**We argue that two reconciling variables are the most likely (our inference).**

1. **Student scale.** The OpenThoughts appendix provides a key point: verification hurts at the 7B scale and helps at the 32B scale[^4].
2. **What the filtered-out data itself is.** In agentic settings, if the rejected data consists of format or execution errors, filtering helps. If it consists of well-formatted long search trajectories that fall short only on the final answer, filtering brings almost no benefit (our inference, based on [^186][^202]).

### 11.4 Whether Traces with Correct Answers Are Better

**Evidence for "correct answers are better".**

- Work such as ShapeOfThought treats answer correctness as a commonly used retention criterion[^12].
- Early rejection-sampling pipelines almost all use final-answer matching as the retention condition (our assessment, based on Sections 4 and 5).

**Evidence for "whether the answer is correct makes little difference".**

- A model trained only on incorrect reasoning traces can reach 97.7% of the accuracy obtained by training on correct samples[^54].
- Training on long-CoT samples with wrong answers yields accuracy only 3.2% lower than training on samples that are all correct[^169].
- ShapeOfThought finds that CoTs generated by a stronger model but all leading to wrong answers can likewise improve reasoning ability[^12].

By contrast, structure matters more than content[^169]; when the reasoning steps of 67% of the training samples are shuffled, the model's accuracy on AIME 2024 drops by 13.3%[^169].

**Answer-conditioned generation causes harm that correctness filtering cannot see.** When the teacher is shown the reference answer and asked to derive it, the resulting CoTs pass correctness filtering yet hurt distillation[^184]. On MATH-500, such data lowers the student's accuracy from 95.1 to 78.9[^184].

Our inference is that "a correct answer" is only a weak proxy for data quality (our inference). Three things really affect learning (our inference, based on [^169][^184][^12]):

- whether the reasoning structure is complete;
- whether the generation process is anchored to the answer;
- whether the trace is close to the student's distribution.

### 11.5 Finding More Questions or Sampling More per Question

**Evidence for "sampling more per question".** OpenThoughts3 annotates each question 16 times with QwQ-32B, obtaining 1.2M samples[^58].

**Evidence for "finding more questions".**

- rStar-Coder ran a controlled comparison[^134]. Using 37.7K seed questions with 16 solutions each (603K in total) yields 54.7 on LiveCodeBench and 10.41 on USACO 2025[^134]. A 580K dataset with more diverse questions yields 57.3 and 16.15, respectively[^134].
- OpenThoughts-Agent finds that repeatedly using a few of the best data sources yields diminishing returns in the largest-scale training runs[^34]. They therefore expand the set of data sources to increase diversity[^34].

**Our inference (our inference).** The answer space of single-turn math reasoning is relatively large, and sampling more per question can provide enough exploration. For code and agentic tasks, the bottleneck lies more in the diversity of questions and task descriptions.

### 11.6 Whether On-Policy Self-Distillation Helps

**Evidence that it helps.** On Qwen3-1.7B, OPSD raises the average over three competition-math benchmarks from 37.1 to 43.4[^141].

**Evidence that it hurts.**

- For thinking models, self-distillation with privileged context lowers avg@16 accuracy by up to 17% in relative terms[^145].
- Another study observes performance drops of up to 40%, caused by the suppression of epistemic verbalization[^146].

**We argue that there are three possible moderating variables (our inference).**

1. whether thinking mode is enabled at inference time;
2. how much privileged context the teacher receives;
3. the evaluation budget.

### 11.7 A Common Structure

Taking the six groups of contradictions together, most of the conclusions depend on "where the student stands relative to the data" (our assessment). This position is reflected in three aspects:

- student scale;
- the distribution gap between the student and the data;
- how much the student has already mastered.

ShapeOfThought argues that constructing datasets closer to the model's distribution is the key[^12]. RSR measures fit by the student's token ranks and surprisal on the trace[^13]. ForcedReasoning argues that the value of reasoning data as a supervision signal depends on the model reading it[^64].

These three threads point in the same direction: the quality of CoT data is not a property of the data itself but a relationship between the data and the student (our assessment).

This yields a methodological recommendation (our assessment). When reporting the effect of CoT data, one should at least report the following together:

- the student's scale and initial capability;
- results after SFT;
- results after SFT followed by RL.

The reason is that looking only at post-SFT scores may lead to choosing the wrong data (our assessment). Research on diverse traces shows that data with slightly lower average accuracy after SFT may do better after RL[^48]. Selecting SFT data by the diversity of reasoning routes raises the pass@8 of OLMo3-7B by 16.9 points in environments unseen during SFT[^48].

Table 11-1 Six groups of contradictory conclusions and possible reconciling variables (the reconciling variables are our inferences)

| ID | Proposition | Supporting evidence | Opposing evidence | Possible reconciling variables |
| --- | --- | --- | --- | --- |
| C1 | The more data, the better | OpenThoughts scales to 1.2M samples and claims "more is more"[^57]; random scaling up is a strong baseline[^5] | Pruning about half of the candidate pool is better[^45]; 5% or 10% subsets can match or exceed the full data[^164][^173] | Whether the base model's knowledge is complete; whether the candidate pool has been prefiltered; whether the update budget is controlled[^18] |
| C2 | A stronger teacher is better | The stronger teacher wins in a same-question comparison[^180]; choose the stronger one when the teacher gap is large[^22] | QwQ-32B beats DeepSeek-R1[^4]; a 4B teacher has a higher recovery rate than 30B-A3B[^56]; small teachers are assigned more questions[^181] | Gap between candidate teachers; student scale[^71]; whether teacher and student are compatible in distribution and thinking patterns[^144] |
| C3 | Verification and filtering help | Multi-level verification differentiated by question type[^1]; agent metrics improve after filtering[^186] | Verification and answer filtering bring no significant gain[^4]; using only incorrect trajectories is almost the same as using only correct ones[^202] | Student scale (harmful at 7B, helpful at 32B)[^4]; the nature of the filtered-out data |
| C4 | Traces with correct answers are better | Answer correctness as the conventional retention criterion[^12] | Using only incorrect traces retains 97.7% of the effect[^54]; with wrong answers, only 3.2% lower[^169] | Completeness of the reasoning structure[^169]; whether generation is anchored to the answer[^184]; closeness of distribution[^12] |
| C5 | Sampling more per question is enough | 16 annotations per question yield 1.2M samples[^58] | Data with diverse questions beats 16 solutions per question[^134]; repeating a few data sources yields diminishing returns[^34] | Size of the answer space; task type (single-turn reasoning versus code and agents) |
| C6 | On-policy self-distillation helps | Qwen3-1.7B average rises from 37.1 to 43.4[^141] | Thinking models drop by up to 17% in relative terms[^145]; drops of up to 40%[^146] | Whether thinking mode is enabled; the amount of privileged context; evaluation budget |

## 12 Open Problems and Research Outlook

Drawing on the preceding sections, we argue that the following seven questions cannot yet be answered with sufficient evidence (our assessment).

### 12.1 The Three Scaling Axes Lack a Comparison Within the Same Framework

Scaling up has three axes: sampling more per question, finding more questions, and repeated training (our assessment).

- Sampling more per question: OpenThoughts3 annotates each question 16 times[^58].
- Finding more questions: data with diverse questions beats 16 solutions per question[^134].
- Repeated training: under a fixed update budget, repeated training beats scaling up[^18].

Each of these three axes has its own evidence, but in the literature we searched, no work has yet compared all three at once under a fixed generation and training budget (our assessment).

### 12.2 "Whether Filtering Helps" Lacks Experiments with Student Scale as the Independent Variable

Among the existing evidence, only the OpenThoughts appendix gives two scale points: verification hurts at the 7B scale and helps at the 32B scale[^4]. Determining the shape of how the benefit of filtering varies with student scale requires controlled experiments at more scale points (our assessment).

### 12.3 Whether Compressed Traces from Frontier Closed Models Can Be Used as Training Data

This question still lacks public experiments (our assessment):

- ForcedReasoning states explicitly that it did not directly test post-training distillation[^64].
- REP neither elicits hidden reasoning from closed commercial models nor uses their outputs for distillation[^65]. The reason is that major service providers restrict reverse engineering, automated extraction of outputs, and the use of their outputs to train competing models[^65].

This question is therefore constrained by both methodology and licensing (our assessment).

### 12.4 The Proportion of Real Data Needed to Avoid Model Collapse Lacks Empirical Evidence on Reasoning Data

Theoretical work has given conclusions in the form of thresholds:

- One statistical analysis argues that the amount of synthetic data should be exponentially smaller than that of real data[^206].
- Another work gives a minimum threshold for the ratio of human data to synthetic data[^47].

But these conclusions rest on simplified models (our assessment). Whether collapse occurs on answer-verified reasoning traces, and under what conditions, has not been directly tested by any of the literature discussed in Section 10 (our assessment).

### 12.5 Whether Step-Level Filtering Beats Answer Filtering Lacks a Cost-Aligned Comparison

Step-level signals have three common sources, each with known flaws:

- **Off-the-shelf process reward models.** On algorithmic reasoning traces, plugging in an external process reward model brings very little gain[^46].
- **Formal labels.** Formal verification can construct step-level labels efficiently[^3], but it applies only to tasks that can be formalized (our assessment).
- **Consensus methods.** When many candidates share the same faulty reasoning pattern, consensus instead amplifies the error[^23].

At the same labeling cost, there is not yet a direct comparison of whether step-level filtering outperforms answer filtering (our assessment).

### 12.6 Self-Improving Data Synthesis Lacks Complete Records of Cost and Robustness

A recursive data synthesis framework revises its skills, prompts and workflows after each batch of data[^53]. It adopts a candidate proposal only when that proposal can produce harder valid tasks within a limited increase in cost[^53]. The authors state explicitly that this threshold guarantees neither higher cost efficiency nor improvement on unseen tasks[^53].

The pseudo-label accuracy of R-Zero falls from an initial 79.0% to 63.0% in the third round[^131]. This shows that self-improvement loops need independent robustness evaluation (our assessment).

### 12.7 How Should a "Dataset" Be Defined and Released in the On-Policy Era

When the training signal comes from "question plus teacher plus scoring rubric" rather than from fixed traces, what must be released for reproduction is not only the data but also the teacher and the scoring rubric (our assessment).

The on-policy distillation survey notes that gains in consistency or immediate accuracy may coincide with lower solution coverage, weakened existing capabilities or smaller gains from subsequent training[^225]. The introductory survey of post-training reasoning data likewise states that its authors did not independently rerun the training recipes, audit contamination or validate every verifier[^231].

We argue that auditable generation records (questions, teacher, sampling parameters, verifier version, filtering logs) should become part of data releases (our assessment).

## 13 Conclusion

Taking the data pipeline as its axis, this review has surveyed methods for constructing chains of thought in the training data of large language models, covering the following stages:

- question sources;
- trace generation;
- verification and labeling;
- selection, scale and length;
- synthesis of agentic trajectories.

This review has also discussed the risks of synthetic reasoning data separately. The research has gone through four stages (our assessment):

1. **2022–2023:** The two routes of bootstrapping and distillation were established[^82][^73].
2. **Around 2024:** Process supervision and large-scale question augmentation became the focus[^74][^75].
3. **2025:** Long CoT distillation and small curated sets developed in parallel[^80][^86].
4. **2026:** The field shifted toward controlled recipe experiments and on-policy training[^4][^34][^56].

This review reaches three main conclusions (our assessment).

**First, the way to scale up depends on the task.** Scaling up single-turn reasoning data relies mainly on sampling multiple traces per question and then selecting among them[^58][^4]. For code and multi-turn agentic data, the bottleneck lies more in the diversity of questions and tasks[^134][^34].

**Second, all three common intuitions about quality have well-designed counterexamples** (our assessment, based on Section 11). The three intuitions are: a stronger teacher is better, traces with correct answers are better, and more data is better. Whether they hold depends on student scale, the distribution gap between the student and the data, and the training budget.

**Third, the most insidious risks cannot be detected.** These risks come from three sources:

- answer-conditioned generation[^184];
- length penalties[^36];
- recursive self-training[^131].

The damage they cause cannot be detected from answer accuracy alone (our assessment).

Data quality depends on the relationship between the data and the student, not on the data itself (our assessment). On this premise, future data work needs to do three things (our assessment):

- also report the student conditions;
- also report results at two points in time, after SFT and after reinforcement learning;
- also release the process records of generation and filtering.

## Appendix A Index of Public Chain-of-Thought Datasets and Recipes

Table A-1 Representative public chain-of-thought datasets and recipes (numbers as given in the dataset cards or the original papers)

| Dataset/recipe | Trace generator | Scale | Verification and filtering | License |
| --- | --- | --- | --- | --- |
| OpenThoughts3-1.2M[^58] | QwQ-32B | 850,000 math questions, 250,000 code questions and 100,000 science questions, each annotated 16 times[^58] | No answer filtering[^4] | apache-2.0[^58] |
| AM-Thinking-v1-Distilled[^60] | AM-Thinking-v1 / Qwen3-235B-A22B | 1.89 million shared queries[^60] | Verification differentiated by question type[^60] | Research only[^60] |
| AM-DeepSeek-R1-Distilled[^1] | Mainly DeepSeek-R1 | 1.4 million questions and their responses[^1] | Reference answers, test cases, reward model[^1] | Research only[^1] |
| OmniThought[^2] | DeepSeek-R1, QwQ-32B | 708K questions, more than 2 million traces[^2] | LLM judge; removed only if the answer is wrong[^2] | — |
| NaturalThoughts / NaturalReasoning[^5][^61] | DeepSeek-R1 | Question bank of 2.8 million questions[^5]; public subset of 1.1 million questions[^61] | Model disagreement as a difficulty proxy[^5] | cc-by-nc-4.0[^61] |
| Nemotron-Post-Training-v2[^59] | Several open-source models | See the dataset card[^59] | Filtered by question quality and complexity[^59] | Mainly CC-BY-4.0[^59] |
| Nemotron-Cascade[^11] | DeepSeek-R1-0528 | 7.8–17.6 traces per question[^11] | 9-gram decontamination[^11] | Public[^11] |
| Dolci-Think-SFT (Olmo 3)[^10] | QwQ-32B, DeepSeek R1 | 2,268,468 prompts[^10] | 6 types of heuristic filtering[^10] | Non-commercial licenses filtered out[^10] |
| ZGCM-1[^45] | Unnamed teacher model | 4,921,933 SFT samples[^45] | Rule-based filtering plus model-based grading[^45] | Fully open source[^45] |
| OpenMathInstruct-2[^88] | Llama-3.1-405B-Instruct | 14M question-solution pairs (about 600K questions)[^88] | Imprecise filtering suffices[^88] | — |
| OpenCodeReasoning[^89] | DeepSeek-R1 | 736,712 traces, 28,904 questions[^89] | Execution filtering (ablation)[^89] | — |
| Synth[^50] | Fine-tuned small auxiliary models | Nearly 80B tokens[^50] | Symbolic recomputation (arithmetic parts)[^50] | CC BY 4.0[^50] |

## Appendix B Quick Reference to Representative Methods

Table B-1 Quick reference to representative methods (the one-sentence mechanisms are summarized by this review)

| Method | Year | Stage | One-sentence mechanism |
| --- | --- | --- | --- |
| STaR[^82] | 2022 | Bootstrapped generation | On a wrong answer, regenerates the rationale with the answer given; keeps only traces with correct answers, and iterates |
| TRICE[^90] | 2023 | Bootstrapped generation | Treats rationales as latent variables and samples from the posterior with MCMC-EM |
| Evol-Instruct[^79] | 2023 | Questions | Evolves instructions along two directions, depth and breadth |
| MetaMath[^75] | 2023 | Questions | Rewrites questions from multiple perspectives |
| Math-Shepherd[^85] | 2023 | Verification | Automatically labels step quality by continuation success rate |
| ReST-EM[^81] | 2023 | Bootstrapped generation | Sampling, binary filtering and fine-tuning, repeated in a loop |
| rStar-Math[^78] | 2025 | Search and verification | MCTS plus code execution; keeps only executable steps |
| s1[^86] | 2025 | Selection | Selects 1,000 samples by difficulty, diversity and quality |
| OpenThoughts[^4] | 2025 | Full pipeline | A recipe obtained from more than 1,000 ablations |
| GoldenGoose[^15] | 2026 | Questions | Turns web text into masked multiple-choice questions |
| FORT-Searcher[^33] | 2026 | Questions | Uses an adversarial agent to detect and fix retrieval shortcuts |
| MIMIC[^46] | 2026 | Generation and verification | Translates instrumented execution states into CoT, which serves as a process reward |
| StepLengthConfounding[^21] | 2026 | Selection | Removes the confounding effect of step length on likelihood-based selection signals |
| DeGMatch[^55] | 2026 | Selection | Removes group-level gradient principal components before doing target matching |
| DataRepetition[^18] | 2026 | Scale | Under a fixed update budget, repeated training beats expanding the data |
| BehavioralEssence[^54] | 2026 | Selection | Long CoT distillation mainly transfers behaviors rather than facts |
| SSR[^19] | 2026 | Risk mitigation | Generates a skeleton first and then reasons, reducing answer anchoring |
| W2S-OPD[^38] | 2026 | On-policy | Builds a proxy teacher in logit space from two weak models |
| A2D[^56] | 2026 | On-policy | Learns to pose questions for distillation without relying on reference answers |
| Distilling Step-by-Step[^73] | 2023 | Trace generation | Trains small models with rationales from a large model as extra supervision in a multi-task framework |
| GKD[^139] | 2023 | On-policy | Supervises token by token with the teacher distribution on sequences generated by the student itself |
| ReST-MCTS\*[^136] | 2024 | Search | Tree search guided by process rewards collects higher-quality reasoning traces for self-training |
| OmegaPRM[^155] | 2024 | Verification | Automatically collects step-level process supervision data with Monte Carlo tree search |
| Persona Hub[^117] | 2024 | Questions | Drives the generation of diverse synthetic data with large-scale personas |
| LESS[^164] | 2024 | Selection | Uses low-rank gradient similarity to retrieve the instruction data most influential for a target capability |
| SWE-smith[^195] | 2025 | Agents | Synthesizes executable software engineering task instances at scale |
| LUFFY[^140] | 2025 | Trace generation | Introduces high-quality off-policy reasoning traces as guidance in reinforcement learning |
| OPSD[^141] | 2026 | On-policy | The student, given privileged context, acts as its own teacher for on-policy self-distillation |
| ExOPD[^142] | 2026 | On-policy | Treats on-policy distillation as a reward and extrapolates the reward |

## References

[^68]: [Wei et al. — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (arXiv 2201.11903, 2022-01)](https://arxiv.org/abs/2201.11903v6)
[^73]: [Hsieh et al. — Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes (arXiv 2305.02301, 2023-05)](https://arxiv.org/abs/2305.02301v2)
[^82]: [Zelikman et al. — STaR: Bootstrapping Reasoning With Reasoning (arXiv 2203.14465, 2022-03)](https://arxiv.org/abs/2203.14465v2)
[^67]: [Mukherjee et al. — Orca: Progressive Learning from Complex Explanation Traces of GPT-4 (arXiv 2306.02707, 2023-06)](https://arxiv.org/abs/2306.02707v1)
[^80]: [DeepSeek-AI — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (arXiv 2501.12948, 2025-01)](https://arxiv.org/abs/2501.12948v2)
[^86]: [Muennighoff et al. — s1: Simple test-time scaling (arXiv 2501.19393, 2025-01)](https://arxiv.org/abs/2501.19393v3)
[^72]: [Ye et al. — LIMO: Less is More for Reasoning (arXiv 2502.03387, 2025-02)](https://arxiv.org/abs/2502.03387v3)
[^4]: [Guha et al. — OpenThoughts: Data Recipes for Reasoning Models (arXiv 2506.04178, 2025-06)](https://arxiv.org/abs/2506.04178v2)
[^10]: [Olmo Team — Olmo 3 (arXiv 2512.13961, 2025-12)](https://arxiv.org/abs/2512.13961v2)
[^45]: [He et al. — ZGCM-1: A Fully Open and Extremely Efficient Foundation Model for Math and Agentic Search (arXiv 2609.13356, 2026-09)](https://arxiv.org/abs/2609.13356v2)
[^34]: [Raoof et al. — OpenThoughts-Agent: Data Recipes for Agentic Models (arXiv 2606.24855, 2026-06)](https://arxiv.org/abs/2606.24855v1)
[^70]: [Yang et al. — Qwen3 Technical Report (arXiv 2505.09388, 2025-05)](https://arxiv.org/abs/2505.09388v1)
[^56]: [Sun et al. — Ask to Distill: Learning to Synthesize Data for On-Policy Distillation (arXiv 2610.27450, 2026-10)](https://arxiv.org/abs/2610.27450v1)
[^57]: [OpenThoughts Team — OpenThoughts3: A New SOTA Reasoning Data Recipe (blog)](https://www.openthoughts.ai/blog/ot3)
[^60]: [a-m-team — AM-Thinking-v1-Distilled (Hugging Face dataset card)](https://huggingface.co/datasets/a-m-team/AM-Thinking-v1-Distilled)
[^1]: [Zhao et al. — 1.4 Million Open-Source Distilled Reasoning Dataset to Empower Large Language Model Training (arXiv 2503.19633, 2025-03)](https://arxiv.org/abs/2503.19633v1)
[^221]: [Ahn et al. — Large Language Models for Mathematical Reasoning: Progresses and Challenges (arXiv 2402.00157, 2024-01)](https://arxiv.org/abs/2402.00157)
[^222]: [Li et al. — From System 1 to System 2: A Survey of Reasoning Large Language Models (arXiv 2502.17419, 2025-02)](https://arxiv.org/abs/2502.17419)
[^224]: [Xu et al. — Towards Large Reasoning Models: A Survey of Reinforced Reasoning with Large Language Models (arXiv 2501.09686, 2025-01)](https://arxiv.org/abs/2501.09686)
[^223]: [Sui et al. — Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models (arXiv 2503.16419, 2025-03)](https://arxiv.org/abs/2503.16419)
[^77]: [Chen et al. — Towards Reasoning Era: A Survey of Long Chain-of-Thought for Reasoning Large Language Models (arXiv 2503.09567, 2025-03)](https://arxiv.org/abs/2503.09567v5)
[^76]: [Long et al. — On LLMs-Driven Synthetic Data Generation, Curation, and Evaluation: A Survey (arXiv 2406.15126, 2024-06)](https://arxiv.org/abs/2406.15126v1)
[^226]: [Nadas et al. — Synthetic Data Generation Using Large Language Models: Advances in Text and Code (arXiv 2503.14023, 2025-03)](https://arxiv.org/abs/2503.14023)
[^227]: [Liu et al. — Best Practices and Lessons Learned on Synthetic Data (arXiv 2404.07503, 2024-04)](https://arxiv.org/abs/2404.07503)
[^84]: [Xu et al. — A Survey on Knowledge Distillation of Large Language Models (arXiv 2402.13116, 2024-02)](https://arxiv.org/abs/2402.13116v4)
[^225]: [Song & Zheng — A Survey of On-Policy Distillation for Large Language Models (arXiv 2604.00626, 2026-04)](https://arxiv.org/abs/2604.00626)
[^229]: [Chen et al. — Putting on the Thinking Hats: A Survey on Chain of Thought Fine-tuning from the Perspective of Human Reasoning Mechanism (arXiv 2510.13170, 2025-10)](https://arxiv.org/abs/2510.13170)
[^230]: [Zeng et al. — What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents (arXiv 2608.27260, 2026-08)](https://arxiv.org/abs/2608.27260)
[^228]: [Zhang et al. — 100 Days After DeepSeek-R1: A Survey on Replication Studies and More Directions for Reasoning Language Models (arXiv 2505.00551, 2025-05)](https://arxiv.org/abs/2505.00551)
[^231]: [Li et al. — A Primer in Post-Training Reasoning Data: What We Know About How It Works (arXiv 2606.02113, 2026-06)](https://arxiv.org/abs/2606.02113)
[^112]: [Gunasekar et al. — Textbooks Are All You Need (arXiv 2306.11644, 2023-06)](https://arxiv.org/abs/2306.11644)
[^63]: [Awesome-Long-Chain-of-Thought-Reasoning — curated repository index (GitHub, LightChen233)](https://github.com/LightChen233/Awesome-Long-Chain-of-Thought-Reasoning)
[^232]: [Lambert et al. — Tulu 3: Pushing Frontiers in Open Language Model Post-Training (arXiv 2411.15124, 2024-11)](https://arxiv.org/abs/2411.15124)
[^233]: [Min et al. — Imitate, Explore, and Self-Improve: A Reproduction Report on Slow-thinking Reasoning Systems (arXiv 2412.09413, 2024-12)](https://arxiv.org/abs/2412.09413)
[^234]: [Huang et al. — O1 Replication Journey -- Part 2: Surpassing O1-preview through Simple Distillation, Big Progress or Bitter Lesson? (arXiv 2411.16489, 2024-11)](https://arxiv.org/abs/2411.16489)
[^235]: [Shao et al. — DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (arXiv 2402.03300, 2024-02)](https://arxiv.org/abs/2402.03300)
[^236]: [Yang et al. — Qwen2.5-Math Technical Report: Toward Mathematical Expert Model via Self-Improvement (arXiv 2409.12122, 2024-09)](https://arxiv.org/abs/2409.12122)
[^237]: [Kimi Team — Kimi k1.5: Scaling Reinforcement Learning with LLMs (arXiv 2501.12599, 2025-01)](https://arxiv.org/abs/2501.12599)
[^5]: [Li et al. — NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks (arXiv 2507.01921, 2025-07)](https://arxiv.org/abs/2507.01921v1)
[^164]: [Xia et al. — LESS: Selecting Influential Data for Targeted Instruction Tuning (arXiv 2402.04333, 2024-02)](https://arxiv.org/abs/2402.04333)
[^173]: [Yang et al. — Select2Reason: Efficient Instruction-Tuning Data Selection for Long-CoT Reasoning (arXiv 2505.17266, 2025-05)](https://arxiv.org/abs/2505.17266)
[^18]: [Kopiczko et al. — Data Repetition Beats Data Scaling in Long-CoT Supervised Fine-Tuning (arXiv 2602.11149, 2026-02)](https://arxiv.org/abs/2602.11149v2)
[^180]: [Tian et al. — Not All Correct Answers Are Equal: Why Your Distillation Source Matters (arXiv 2505.14464, 2025-05)](https://arxiv.org/abs/2505.14464)
[^22]: [Kajitsuka et al. — Revisiting the Capacity Gap in Chain-of-Thought Distillation from a Practical Perspective (arXiv 2604.08880, 2026-04)](https://arxiv.org/abs/2604.08880v2)
[^30]: [Lu & Liu — Strong Teacher Not Needed? On Distillation in LLM Pretraining (arXiv 2605.23857, 2026-05)](https://arxiv.org/abs/2605.23857v1)
[^181]: [Zhang et al. — Find Your Optimal Teacher: Personalized Data Synthesis via Router-Guided Multi-Teacher Distillation (arXiv 2510.10925, 2025-10)](https://arxiv.org/abs/2510.10925)
[^71]: [Li et al. — Small Models Struggle to Learn from Strong Reasoners (arXiv 2502.12143, 2025-02)](https://arxiv.org/abs/2502.12143v3)
[^13]: [Yang et al. — Which Reasoning Trajectories Teach Students to Reason Better? A Simple Metric of Informative Alignment (arXiv 2601.14249, 2026-01)](https://arxiv.org/abs/2601.14249v5)
[^64]: [Luo et al. — Capable yet Parsimonious: Extracting and Characterizing Hidden Chain-of-Thought in Frontier Models (arXiv 2609.26637, 2026-09)](https://arxiv.org/abs/2609.26637v1)
[^144]: [Li et al. — Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe (arXiv 2604.13016, 2026-04)](https://arxiv.org/abs/2604.13016)
[^186]: [Zeng et al. — AgentTuning: Enabling Generalized Agent Abilities for LLMs (arXiv 2310.12823, 2023-10)](https://arxiv.org/abs/2310.12823)
[^202]: [Li et al. — OpenResearcher: A Fully Open Pipeline for Long-Horizon Deep Research Trajectory Synthesis (arXiv 2603.20278, 2026-03)](https://arxiv.org/abs/2603.20278)
[^12]: [Chandra et al. — Shape of Thought: When Distribution Matters More than Correctness in Reasoning Tasks (arXiv 2512.22255, 2025-12)](https://arxiv.org/abs/2512.22255v2)
[^54]: [Yu et al. — Facts Don't Speak Louder than Words: The Behavioral Essence of Long-CoT Distillation (arXiv 2610.17607, 2026-10)](https://arxiv.org/abs/2610.17607v1)
[^169]: [Li et al. — LLMs Can Easily Learn to Reason from Demonstrations Structure, not content, is what matters! (arXiv 2502.07374, 2025-02)](https://arxiv.org/abs/2502.07374)
[^184]: [Lee et al. — Answer-Conditioned Chains of Thought Degrade Verifiable-Reasoning Distillation in Large Language Models (arXiv 2607.14552, 2026-07)](https://arxiv.org/abs/2607.14552)
[^58]: [OpenThoughts Team — OpenThoughts3-1.2M (Hugging Face dataset card)](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M)
[^134]: [Liu et al. — rStar-Coder: Scaling Competitive Code Reasoning with a Large-Scale Verified Dataset (arXiv 2505.21297, 2025-05)](https://arxiv.org/abs/2505.21297)
[^141]: [Zhao et al. — Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models (arXiv 2601.18734, 2026-01)](https://arxiv.org/abs/2601.18734)
[^145]: [Kaur et al. — Rethinking On-Policy Self-Distillation for Thinking Models (arXiv 2607.05184, 2026-07)](https://arxiv.org/abs/2607.05184)
[^146]: [Kim et al. — Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? (arXiv 2603.24472, 2026-03)](https://arxiv.org/abs/2603.24472)
[^48]: [Zhang et al. — Selecting Diverse SFT Traces Improves Post-RL Generalization (arXiv 2609.33780, 2026-09)](https://arxiv.org/abs/2609.33780v1)
[^65]: [Lu et al. — Hidden Thoughts Are Not Secret: Reasoning Trace Exposure in LLMs (arXiv 2606.00642, 2026-05)](https://arxiv.org/abs/2606.00642v2)
[^206]: [Seddik et al. — How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model Collapse (arXiv 2404.05090, 2024-04)](https://arxiv.org/abs/2404.05090)
[^47]: [Marchi et al. — Preventing Model Collapse: A Fisher-Rao Perspective on the Dynamics of Training with Synthetic Data (arXiv 2609.18878, 2026-09)](https://arxiv.org/abs/2609.18878v1)
[^46]: [Zhang et al. — The Imitation Game: When LLMs Learn to Reason Like Programs via Code-Centric Reasoning Data Synthesis (arXiv 2609.16076, 2026-09)](https://arxiv.org/abs/2609.16076v1)
[^3]: [Kamoi et al. — Efficient PRM Training Data Synthesis via Formal Verification (arXiv 2505.15960, 2025-05)](https://arxiv.org/abs/2505.15960v3)
[^23]: [Ling et al. — Correct Prediction, Wrong Steps? Consensus Reasoning Knowledge Graph for Robust Chain-of-Thought Synthesis (arXiv 2604.14121, 2026-04)](https://arxiv.org/abs/2604.14121v5)
[^53]: [Zhang et al. — Recursive Harness Self-Improvement for Frontier Reasoning Data Synthesis (arXiv 2610.03548, 2026-10)](https://arxiv.org/abs/2610.03548v1)
[^131]: [Huang et al. — R-Zero: Self-Evolving Reasoning LLM from Zero Data (arXiv 2508.05004, 2025-08)](https://arxiv.org/abs/2508.05004)
[^74]: [Lightman et al. — Let's Verify Step by Step (arXiv 2305.20050, 2023-05)](https://arxiv.org/abs/2305.20050v1)
[^75]: [Yu et al. — MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models (arXiv 2309.12284, 2023-09)](https://arxiv.org/abs/2309.12284v4)
[^36]: [Little — Length Penalties Make Chain-of-Thought Less Monitorable (arXiv 2607.09786, 2026-07)](https://arxiv.org/abs/2607.09786v4)
[^2]: [Cai et al. — Reasoning with OmniThought: A Large CoT Dataset with Verbosity and Cognitive Difficulty Annotations (arXiv 2505.10937, 2025-05)](https://arxiv.org/abs/2505.10937v1)
[^61]: [Meta AI — natural\_reasoning (Hugging Face dataset card)](https://huggingface.co/datasets/facebook/natural_reasoning)
[^59]: [NVIDIA — Nemotron-Post-Training-Dataset-v2 (Hugging Face dataset card)](https://huggingface.co/datasets/nvidia/Nemotron-Post-Training-Dataset-v2)
[^11]: [Wang et al. — Nemotron-Cascade: Scaling Cascaded Reinforcement Learning for General-Purpose Reasoning Models (arXiv 2512.13607, 2025-12)](https://arxiv.org/abs/2512.13607v2)
[^88]: [Toshniwal et al. — OpenMathInstruct-2: Accelerating AI for Math with Massive Open-Source Instruction Data (arXiv 2410.01560, 2024-10)](https://arxiv.org/abs/2410.01560v2)
[^89]: [Ahmad et al. — OpenCodeReasoning: Advancing Data Distillation for Competitive Coding (arXiv 2504.01943, 2025-04)](https://arxiv.org/abs/2504.01943v2)
[^50]: [Langlais et al. — It's All Training: A Fully Synthetic Single-Stage Recipe for LLMs (arXiv 2609.37891, 2026-09)](https://arxiv.org/abs/2609.37891v1)
[^90]: [Du Phan et al. — Training Chain-of-Thought via Latent-Variable Inference (arXiv 2312.02179, 2023-11)](https://arxiv.org/abs/2312.02179v1)
[^79]: [Xu et al. — WizardLM: Empowering large pre-trained language models to follow complex instructions (arXiv 2304.12244, 2023-04)](https://arxiv.org/abs/2304.12244v3)
[^85]: [Wang et al. — Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations (arXiv 2312.08935, 2023-12)](https://arxiv.org/abs/2312.08935v3)
[^81]: [Singh et al. — Beyond Human Data: Scaling Self-Training for Problem-Solving with Language Models (arXiv 2312.06585, 2023-12)](https://arxiv.org/abs/2312.06585v4)
[^78]: [Guan et al. — rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking (arXiv 2501.04519, 2025-01)](https://arxiv.org/abs/2501.04519v1)
[^15]: [Lu et al. — Golden Goose: A Simple Trick to Synthesize Unlimited RLVR Tasks from Unverifiable Internet Text (arXiv 2601.22975, 2026-01)](https://arxiv.org/abs/2601.22975v2)
[^33]: [Deng et al. — FORT-Searcher: Synthesizing Shortcut-Resistant Search Tasks for Training Deep Search Agents (arXiv 2606.12087, 2026-06)](https://arxiv.org/abs/2606.12087v2)
[^21]: [Wang et al. — On the Step Length Confounding in LLM Reasoning Data Selection (arXiv 2604.06834, 2026-04)](https://arxiv.org/abs/2604.06834v1)
[^55]: [Lee et al. — DeGMatch: Target-Aware Reasoning Data Selection via Deconfounded Gradient Matching (arXiv 2610.24963, 2026-10)](https://arxiv.org/abs/2610.24963v1)
[^19]: [Peng et al. — Measuring and Mitigating Post-hoc Rationalization in Reverse Chain-of-Thought Generation (arXiv 2602.14469, 2026-02)](https://arxiv.org/abs/2602.14469v4)
[^38]: [Yu et al. — Weak-to-Strong On-Policy Distillation (arXiv 2607.26246, 2026-07)](https://arxiv.org/abs/2607.26246v2)
[^139]: [Agarwal et al. — On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes (arXiv 2306.13649, 2023-06)](https://arxiv.org/abs/2306.13649)
[^136]: [Zhang et al. — ReST-MCTS\*: LLM Self-Training via Process Reward Guided Tree Search (arXiv 2406.03816, 2024-06)](https://arxiv.org/abs/2406.03816)
[^155]: [Li et al. — Making Large Language Models Better Reasoners with Step-Aware Verifier (arXiv 2206.02336, 2022-06)](https://arxiv.org/abs/2206.02336)
[^117]: [Ge et al. — Scaling Synthetic Data Creation with 1,000,000,000 Personas (arXiv 2406.20094, 2024-06)](https://arxiv.org/abs/2406.20094)
[^195]: [Yang et al. — SWE-smith: Scaling Data for Software Engineering Agents (arXiv 2504.21798, 2025-04)](https://arxiv.org/abs/2504.21798)
[^140]: [Yan et al. — Learning to Reason under Off-Policy Guidance (arXiv 2504.14945, 2025-04)](https://arxiv.org/abs/2504.14945)
[^142]: [Yang et al. — Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation (arXiv 2602.12125, 2026-02)](https://arxiv.org/abs/2602.12125)
