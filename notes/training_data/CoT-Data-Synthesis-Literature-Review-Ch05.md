# 训练数据中的思维链合成：方法、证据与开放问题 · 第 5 节

中文 | [English](./CoT-Data-Synthesis-Literature-Review-Ch05_en.md)

- **调研日期**: 2026-10-22（证据截止：arXiv 首版日期不晚于 2026-10-22）
- **导航**: [主页面](./CoT-Data-Synthesis-Literature-Review.md)（摘要、第 1–3 节、第 11–13 节与附录） · 上一节：[第 4 节](./CoT-Data-Synthesis-Literature-Review-Ch04.md) · 下一节：[第 6 节](./CoT-Data-Synthesis-Literature-Review-Ch06.md)
- **依据**: 句末的上标数字是引用，对应文末参考来源中的精读文献；每条引用都有从该文献全文逐字摘录、并经脚本与全文核对的原文。标有（本文判断）、（本文推断）或（本文统计）的内容，是本文的综合分析或统计，不是来源原话。

## 5 题目与任务来源

按本文的分类框架，思维链数据合成流水线由题目来源 $`\mathcal{Q}`$、轨迹生成 $`\mathcal{G}`$、保留判据 $`\mathcal{V}`$ 与选择策略 $`\mathcal{S}`$ 四个环节组成（本文判断）。本节讨论第一个环节：训练题从哪里来，能否自动判对，难度相对于谁、如何控制，与评测集的重叠如何排除。2023 至 2024 年的主流做法是改写或扩写基准训练题，再由强教师补写解答，新题大多没有可核对的答案（本文判断）。2025 年以后，题集越来越多地按“答案可验证、难度落在学习者能力边界”来构造，并出现了由模型自己出题的路线（本文判断）。轨迹的生成与保留判据在后续各节讨论。

### 5.1 复用与改写现有题库

**谱系与机制。** 最早一批数学推理数据集直接改写 GSM8K 与 MATH 的训练题（本文判断）。MetaMath 从多个视角改写题目来自举数学题，得到 MetaMathQA[^75]。前向方向包括原题与大模型改写题，后向方向把题中一个词元遮成“x”，给出答案后让模型求被遮的量[^75]。答案侧用拒绝采样，只保留答案正确的推理路径，合计 395K 条[^75]。WizardLM 提出的 Evol-Instruct 逐步把指令改写得更复杂[^79]。WizardMath 把它用于数学，在加难的向上进化之外增加了变易的向下进化[^114]。它以 GSM8K 与 MATH 训练集为种子，用 GPT-4 对每题进化 5 轮（2 轮向下、3 轮向上），去重后得到 448k 条[^114]。去污染再滤掉 30k 条，答案由 GPT-4-0613 逐步生成[^114]。

MathScale 认为，逐题改写的新题与原训练题高度相似，难以支撑大规模数据[^115]。它用 GPT-3.5-Turbo-0613 从约 20K 道 MwpBench 训练题中抽取 2,018 个主题与 8,892 个知识点，建成概念图后组合生成 2M 条问答对[^115]。OpenMathInstruct-1 不增广题目，只为 GSM8K 与 MATH 的训练题合成代码解释器解答[^132]。其动机是许可：MetaMathQA 与 MAmmoTH 来自商业条款受限的闭源模型，作者改用许可宽松的 Mixtral[^132]。MAmmoTH 的训练集汇编自 13 个带中间推理的数学数据集[^66]。OpenMathInstruct-2 指出，OpenMathInstruct-1 的题目全部取自 MATH 与 GSM8K 训练集，多样性有限[^88]。它以这两个训练集为种子做 5 例少样本提示，不显式要求加难，只靠核采样的随机性生成新题[^88]。最终数据含 14M 条问答对、约 600K 道唯一题目，由 Llama-3.1-405B-Instruct 合成[^88]。

**证据。** 这一支有若干同学生、同数据量的受控对照（本文判断）。以 Mistral-7B 做监督微调，两轮向下进化使 GSM8K 从 59.7 升到 74.5、MATH 从 15.1 升到 34.7，对照为原始 7.5k 条人工标注数据[^114]。同以 Mistral-7B 为基座、数据规模相同时，进化数据比 MetaMath 在 GSM8K 上高 3%–6%，在 MATH 上高 15%–20%[^114]。MathScale 以 LLaMA-2 7B 训练 25K 条数据，种子题限于 GSM8K 与 MATH 训练集时性能下降 3.5%[^115]。只保留一半知识点下降 8.6%，只保留一半主题仅下降 2.3%[^115]。OpenMathInstruct-2 以 Llama3.1-8B-Base 为学生、固定 256K 条问答对，唯一题目数从 1K 增至 6.5K 使 MATH 验证集提升 10.5%[^88]。OpenMathInstruct-1 在固定题目上增加解答，Mistral-7B 在 1K 验证子集上的 MATH 从 128K 条时的 37.0 升到 512K 条时的 41.6[^132]。作者报告，单纯延长训练步数没有收益[^132]。

**局限与争议。** 改写类方法的共同代价是新题没有可核对的答案（本文判断）。WizardMath 承认进化出的指令缺少正确答案[^114]。MathScale 在 5K 条数据、LLaMA-2 7B 的受控实验中，用 GPT-4 判出并替换 26% 的 GPT-3.5 解答[^115]。宏平均却没有提高：全用 GPT-3.5 解答为 11.5，替换后为 11.1，全用 GPT-4 解答为 10.9[^115]。作者据此从最终流水线中去掉了验证步骤[^115]。其解释是，错误解答仍能帮助开源模型模仿 GPT-3.5 的分布[^115]。该结论只来自 5K 条数据，能否外推到更大规模尚无证据（本文判断）。提示中带参考解还会诱发抄答案，OpenMathInstruct-1 观察到 print(ANSWER) 式的捷径解[^132]。改用遮蔽过的参考解作提示后，MATH 训练集覆盖率由 80.1% 升至 85.9%[^132]。旧题集对较强的学生还可能过易（本文判断，依据见[^17]）。Agentic Proposing 报告，在相同的 GRPO 配方下用 MetaMath 训练，使 Qwen3-4B 等较强推理模型的性能下降[^17]。其诊断是基座模型在这些题上的通过率高达 85%–89%，组内相对优势趋于零[^17]。

### 5.2 从网络与文档中挖掘题目

**谱系与机制。** MAmmoTH2 认为 GPT-4 合成的指令有偏、多样性低且易产生幻觉，转而从网页语料中收割天然存在的问答对[^116]。它用测验网站种子训练 fastText 召回文档，再经 GPT-4 对召回域名二次筛选，得到 18M 篇文档[^116]。其中只有 30% 含问答对，约 5M 对[^116]。Mixtral-22B×8 与 Qwen-72B 再改写格式，答案缺少解释时补写中间步骤，得到 10M 对的 WebInstruct[^116]。General-Reasoner 回溯 WebInstruct 的原网页重新爬取，删去没有人工答案的题[^120]。它用 Gemini-1.5-Pro 抽取约 1M 道短答案可验证的题[^120]。再让 Gemini-2.0-Flash 为每题生成 8 个候选解，剔除全错与全对的题，剩约 230k 道[^120]。

NaturalReasoning 不抽取文档中已有的题，而是让大模型依据 DCLM-baseline 与 FineMath 文档另写一道自洽的新题[^122]。文档能推出参考答案时一并保留，2.8M 道题中 81.68% 带参考答案[^122]。DeepMath-103K 认为现有题集多是重新收集已有题目，彼此大量重叠[^119]。它以 Math StackExchange 子集为主、辅以 NuminaMath-CoT，得到 2,869K 道原始题[^119]。经去污染、难度过滤与可验证性过滤留下 95K 道，再并入 SimpleRL 的 8K 道[^119]。AIMO-2 冠军方案从 AoPS 论坛 620K 个讨论中抽题，删去选择题、判断题与无效题，并把证明题改写成有答案的题，得到 540K 道[^133]。对没有标准答案的网页文本，Golden Goose 让大模型遮蔽一段关键推理作为答案并生成干扰项，把填空变成选择题，强化学习中只需比对选项[^15]。Synth 以 58,698 篇维基百科文章为种子，结构化放大出近 80B 词元的合成语料[^50]。作者发现，用轮换指令提示单个大模型，生成会坍缩到狭窄的措辞与格式分布[^50]。

**证据。** 不用任何领域内训练数据，MAmmoTH2-7B（Mistral）的 MATH 从 11% 升到 36.7%，GSM8K 从 36% 升到 68.4%[^116]。以 Qwen2.5-7B-Base 做零强化学习，General-Reasoner 的 MMLU-Pro 为 58.9%，基座为 47.7%，Instruct 版为 57.0%[^120]。其 7B 消融只用数学题训练时，数学类基准为 49.1% 对 48.5%，但 MMLU-Pro、GPQA 与 SuperGPQA 各降约 2 个百分点[^120]。以 Llama3.1-8B-Base 做监督微调、按 MATH、GPQA 与 MMLU-Pro 的平均分计，1.5M 条 NaturalReasoning 已超过 Llama3.1-8B-Instruct[^122]。OpenMathInstruct-2 与 WebInstruct 到 2.8M 条仍未超过，但前者的 MATH 始终最高，2.8M 条时为 59.25[^122]。随机抽 1K 道 NaturalReasoning 题，由 DeepSeek-R1 各写一条回答来微调 Llama-3.3-70B-Instruct，三项平均为 75.9，s1K-1.1 为 75.6，LIMO 为 73.3[^122]。从 Qwen-2.5-7B 做零强化学习，DeepMath-Zero-7B 的 MATH500、AIME24、AIME25 为 85.5、20.4、17.5，基座为 54.8、7.7、5.4[^119]。Golden Goose 从原始网页合成约 180K 道网络安全任务，Qwen-4B-Instruct 经 100 步强化学习后在 3 项基准上绝对提升 4.44%[^15]。

表 5-1 摘录 OpenThoughts 题源消融的数学部分，该实验固定了教师、学生与数据量，是比较题源最直接的证据（本文判断，依据见[^4]）。

表 5-1 同一蒸馏配方下不同数学题源的效果（每个题源 31,600 条，DeepSeek-R1 生成回答，微调 Qwen2.5-7B-Instruct[^4]）

| 题源 | 题目来源类型 | 平均 | 代码 | 数学 | 科学 |
| --- | --- | ---: | ---: | ---: | ---: |
| openmath-2-math（OpenMathInstruct-2 的 MATH 子集）[^4][^88] | 以训练题为种子合成 | 38.1 | 12.4 | 58.8 | 45.6 |
| NuminaMath-1.5[^4] | 人工竞赛题 | 37.4 | 11.4 | 58.5 | 45.0 |
| DeepMath-103K[^4][^119] | 论坛挖掘后改写 | 34.8 | 7.2 | 55.6 | 44.8 |
| natural_reasoning[^4][^122] | 文档反向构造 | 33.4 | 7.6 | 52.1 | 43.9 |
| Big-Math[^4][^118] | 开源题集整理 | 33.0 | 9.4 | 53.2 | 38.1 |
| MetaMath（以 GPT-4o-mini 复现）[^4][^75] | 改写增广 | 29.3 | 6.1 | 48.4 | 35.3 |

**局限与争议。** 网络题的主要问题是答案与推理多由大模型补写（本文判断）。WebInstruct 的 50 条人工抽检中，78% 经改写得到改进，10% 引入了幻觉[^116]。NaturalReasoning 公开的 1.1M 子集中，18.29% 的题没有参考答案，只有 9.71% 是单词答案[^61]。表 5-1 所列题源的数学平均分最多相差 10.4 分（本文统计）。为强化学习整理的 DeepMath-103K 与 Big-Math 在这一蒸馏设定下不占优，题集的价值依赖下游用途（本文推断，依据见[^4][^118][^119]）。这组比较只覆盖监督蒸馏，且条数不足的题源靠重复题目补齐（本文判断，依据见[^4]）。选择题格式还有捷径：选项只有 3 个时，多数题对 ProRL-1.5B-v2 过易，模型靠排除法作答[^15]。改为 9 个选项后，超过 70% 的题落在有成有败的中等难度区间[^15]。开放式版本则有超过 83% 的题对该模型始终零分[^15]。

### 5.3 人设、技能与代码驱动的合成

**谱系与机制。** 这一支用外部结构而非提示措辞来提供多样性（本文判断）。Persona Hub 认为，在合成提示中加入人设即可把大模型引向相应视角[^117]。作者从 RedPajama v2 抽取并扩展出 1,015,863,523 个人设[^117]。其中 1.09M 个用于让 GPT-4 零样本出数学题，解答由 gpt-4o 直接生成[^117]。OSS-Instruct 认为 Self-Instruct 与 Evol-Instruct 类方法继承了大模型与预定义任务的偏差，改用真实开源代码作种子[^123]。它从 80K 篇代码文档中各截取 1–15 行，由 gpt-3.5-turbo-1106 同时写出题目与解答，共约 75K 条[^123]。KodCode 用 5 种方法从 12 个来源合成题目，由 GPT-4o-0513 同时写解答与单元测试，只保留测试通过且分支覆盖率达 100% 的三元组[^121]。为免丢掉难题，每题最多尝试 10 次[^121]。rStar-Coder 指出，Magicoder 与 KodCode 等主要面向几乎无需测试即可判对的函数级代码[^134]。它把 37,754 道种子题连同参考解写入结构化提示，合成 1,565K 道新题[^134]。输出标签由互验证确定，QwQ-32B 多条解的输出一致率低于 60% 的题被丢弃[^134]。CodeI/O 让 DeepSeek-V2.5 把约 810.5K 个代码文件改写成可执行函数，要求模型用自然语言预测其输入或输出，过滤后共 3.5M 条实例[^124]。Combinatorial Synthesis 认为启发式扩展只增加语言多样性，会让 RLVR 过早奖励饱和[^32]。它把种子题分解为原子元素，围绕核心元素受控重组，再以执行过滤[^32]。SynLogic 为 35 类逻辑任务配备生成代码与规则验证器，可按生成参数调节难度[^125]。Agentic Proposing 让智能体从技能库中挑选并组合技能来出题[^17]。Kimi K3 让智能体经网络搜索递归扩展知识图谱，再据检索材料合成训练任务[^37]。

**证据。** Qwen2-7B 在 1.07M 道人设题上微调后，MATH 达到 64.9%，作者视之为分布外测试[^117]。以 CodeLlama-Python-7B 为基座、各用 75K 条数据，直接用开源代码的注释与函数对微调，HumanEval+ 停在 34.1，MultiPL-E 降到 24.1[^123]。OSS-Instruct 在相同条件下为 55.5 与 37.8[^123]。以 Qwen2.5-Coder-32B-Instruct 为学生，KodCode 的 10K 难题子集在 BigCodeBench-I Hard 上为 31.8%，随机 10K 子集为 27.7%[^121]。在 64 道种子题、3,150 个测试输入上，rStar-Coder 互验证的标注准确率为 96.8%，GPT-4o 直接生成输入输出只有 12.7%[^134]。以 Qwen2.5-Coder-7B 为基座，CodeI/O 把 14 项基准平均分从 54.8 升至 57.2，用完整 OpenMathInstruct-2 为 56.0[^124]。在 Qwen2.5-Coder-7B-Instruct 上各用 5,000 条数据做强化学习，LCB-v5/v6 平均 pass@1 为：基座 18.19，真实 TACO 题 23.23，KodCode 23.16，ADR 25.76[^32]。在 Qwen2.5-32B-Base 上以相同步数做零强化学习，35k 数学与 9k 代码题外再混入 17k SynLogic 题，BBEH 由 18.5 升至 28.6[^125]。

**局限与争议。** 外部结构解决了措辞多样性，正确性仍要靠执行或验证保证（本文判断）。两位数学专家抽查 200 道人设难题，7 道无效[^117]。KodCode 的自验证精度高而保留率低：通过自验证的解在 MBPP 上有 97.5% 能通过原有单元测试，但 LiveCodeBench-V5 上只有 49.9% 的解通过自验证[^121]。从 1 次增至 5 次尝试使通过率提高 20% 以上，说明一次生成即丢弃会系统性地删掉难题（本文推断，依据见[^121]）。ADR 统计，KodCode 独有样本中 47.5% 是简单的函数级补全[^32]。另一方面，CodeI/O 以 Qwen2.5-Coder-7B 实验，按执行结果剔除错误回答后平均分为 56.5，低于约一半规模子集的 56.7[^124]。作者归因于数据多样性受损[^124]。这与 KodCode、rStar-Coder 的严格过滤方向相反，可能因为 CodeI/O 用于前置训练阶段，覆盖面比答案正确率更重要（本文推断，依据见[^124][^121][^134]）。

### 5.4 难度控制与难题生成

**谱系与机制。** 强化学习把难度变成了训练信号是否存在的问题（本文判断）。SwS 指出，若一组回答全对或全错，组内优势塌缩为零，梯度消失[^128]。Big-Math 同样指出，模型从不答对的题对多数强化学习方法没有信号[^118]。由此形成的通用做法是按参照模型的通过率区间筛题（本文判断）：

```math
\hat p_M(q)=\frac{1}{k}\sum_{j=1}^{k}\mathbb{1}\big[\mathrm{ans}(y_j)=a(q)\big],\quad y_j\sim M(\cdot\mid q),\qquad \mathcal{Q}_{\mathrm{keep}}=\{q:\ l\le \hat p_M(q)\le u\}
```

其中 $`M`$ 是参照模型，$`k`$ 是采样次数，$`[l,u]`$ 是保留区间（本文判断）。表 5-2 列出各工作的取法。Big-Math 从开源题集中筛出 251,122 道题，可解性以 Llama-3.1-8B 每题 64 次与 Llama-3.1-405B 每题 5–8 次采样检查，任一模型答出给定答案即保留[^118]。作者认为选择题可被猜中，不适合强化学习，因此把选择题改写成开放题[^118]。另一类做法用 GPT-4o 评级、教师回答长度等代理信号估计难度（本文判断，依据见[^119][^11]）。NeMo Curator 的教程从约 30M 条合成样本中过滤出子集，再按回答长度升序排列，作为由易到难的课程[^62]。

表 5-2 代表性难度控制机制（本文判断，依据见各行引用）

| 工作 | 参照模型 | 难度信号 | 保留或奖励规则 | 用途 |
| --- | --- | --- | --- | --- |
| Big-Math[^118] | Llama-3.1-8B 与 Llama-3.1-405B | 8B 每题 64 次、405B 每题 5–8 次采样是否答对 | 至少答对一次；改写的选择题另要求 8B 未全对 | 强化学习题集 |
| General-Reasoner[^120] | Gemini-2.0-Flash | 8 个候选解 | 剔除全对与全错 | 零强化学习 |
| SynLogic[^125] | R1、o3-mini 与对话模型 | pass@10 与通过率 | 上界 pass@10 > 0，下界通过率在 0 到 0.5 之间 | 设定难度参数 |
| Golden Goose[^15] | 学生模型 | 16 次采样 | 剔除 16 次全对的题 | 强化学习（噪声网页来源） |
| SwS[^128] | 初始训练后的策略 | 多次采样准确率 | 例如保留 25%–75% | 弱点题合成 |
| Learning to Pose Problems[^9] | 当前求解器 | 答案一致性 | 低于 0.3 简化，0.3–0.7 保持，高于 0.7 加难 | 出题器条件 |
| QbQ[^39] | 当前检查点 | 16 次中答对数 n | 种子取 8 ≤ n ≤ 15，训练题取有成有败的变体 | 课程式变体 |
| SvS[^129] | 当前策略 | 组内准确率 | 仅对 [1/8, 5/8] 的变体给正奖励 | 在线变体题 |
| R-Zero[^131] | 当前 Solver | 10 次采样中与多数答案一致的个数 | 保留 3 至 7 个一致的题 | 自提题 |
| Absolute Zero[^130] | 当前 Solver | 平均求解率 | 奖励为 1 − 求解率，不可解为 0 | 自提题 |
| DeepMath-103K[^119] | GPT-4o | 6 次难度评级均值 | 保留 5 级及以上 | 强化学习题集 |
| AIMO-2[^133] | Qwen2.5-Math-72B-Instruct TIR | 32 次通过率 | 丢弃通过率大于 0.3 的题 | 第二轮监督微调 |
| MathSmith[^127] | Qwen3-30B-A3B | 解题轨迹长度 | 作为出题器的奖励 | 难题合成 |
| Nemotron-Cascade[^11] | DeepSeek-R1 | 回答长度 | 剔除回答不足 2K 词元的题 | 第二阶段监督微调 |

**难题生成。** 另一路直接驱动出题器造难题（本文判断）。MathSmith 认为改写人工题受原分布束缚且难以精确控难，改为从 PlanetMath 的 11,000 个概念中随机抽取概念从零出题[^127]。出题器 Qwen3-8B 先用约 8k 条 GPT-4o 冷启动样本微调，再用 GRPO 训练[^127]。奖励以 Qwen3-30B-A3B 解题轨迹的长度衡量复杂度，并鼓励能让教师给出确定答案的题[^127]。CoDiQ 让种子题在至多 8 轮中逐步进化为更难的变体，由 Doubao-Seed-1.8 做相对难度排序[^16]。可解性由 Qwen3-32B 判定，难度低于前序版本或被判不可解时即停止[^16]。SwS 把第一阶段强化学习中始终未达 50% 准确率且呈下降趋势的题视为弱点，抽取其概念重组成新题[^128]。新题参考答案由 QwQ-32B 等推理模型自洽投票给出，一致率不足 50% 的丢弃[^128]。

**证据。** MathSmith 的各基线均取 50K 道题，由同一教师 Qwen3-30B-A3B 重写解答[^127]。在 Qwen3-8B 长思维链设定下，难题基准平均为 71.8，NuminaMath-CoT 为 68.2，不加数据为 65.4[^127]。加入一致性奖励后，可用题比例由 84.92% 升至 95.38%[^127]。三位博士对 200 个 CoDiQ 样本的评估显示，被接受题的精度为 82%[^16]。与在原题集上继续训练相同步数相比，SwS 使 7B 与 32B 模型在 8 项基准上的平均分提高 10.0 与 7.7[^128]。以 Qwen3-4B-Base 与 Qwen3-8B-Base 兼作出题器与求解器，Learning to Pose Problems 在 10 项基准上比只用种子题高 2.69（一轮）与 3.39（三轮）个百分点[^9]。但其难度调整的方向成功率平均只有 0.61[^9]。

**局限与争议。** 难度控制有两条已知天花板（本文判断）。一是验证器：CoDiQ 指出，超出验证器能力的有效难题会被误判为不可解而丢弃[^16]。二是学生容量：MathSmith-HC 在 1.7B 与 4B 小模型上略差，作者归因于小模型难以学习复杂题[^127]。按正确性过滤还会连带删掉难题（本文判断，依据见[^89][^121]）。OpenCodeReasoning 以 Qwen-2.5-14B-Instruct 微调，445,618 条全量数据的 LiveCodeBench 为 54.1[^89]。只用通过测试的 151,251 条为 47.0，只用同样数量的未通过解为 52.3[^89]。作者发现未通过的解集中在更难的题上[^89]。

关于取多难，两项研究的结论相反（本文判断）。SwS 用 Qwen2.5-7B 初始训练后的模型 8 次采样准确率，把合成题分为易（8 次中答对 5–7 次）、中（3–5 次）、难（1–4 次）三档，各取 40k 道并入原训练集再训 200 步[^128]。易档收敛最快但随后饱和，最难一档收益最持久[^128]。QbQ 以 Qwen2.5-Math-7B 在 AIME 2025 与 2026 上的 pass@1 衡量，从 16 次中答对 8 至 15 次的题出种子，终点为 16.46%[^39]。从答对 1 至 7 次的题出种子，中途一度达到 14.17%，终点只有 11.35%，与只用原题做 GRPO 的差距不到 0.4 个百分点[^39]。作者认为难种子的变体常超出模型的可靠求解范围，组内回答没有对错差异[^39]。两者的难档区间相近，SwS 为 8 次中答对 1–4 次，QbQ 为 16 次中答对 1–7 次（本文统计，依据见[^128][^39]）。分歧更可能来自难档的用法：SwS 直接在难档题上训练，QbQ 的难档只作种子，训练题是其变体（本文推断，依据见[^128][^39]）。评测也不同，SwS 用从 GSM8K 到 AIME 的 8 项数学基准，QbQ 只看 AIME 新题（本文判断，依据见[^128][^39]）。

### 5.5 模型自提题及其崩塌风险

**谱系与机制。** 自提题路线把出题者换成学习者自身或同源模型，关键在于新题的标签从哪里来（本文判断）。CoT-Self-Instruct 以 s1k 中 893 道可验证题为种子，让 Qwen3-4B 先分析种子，再同时写出新题与答案[^126]。生成时给出的答案须与模型多数投票的答案一致，题目才被保留[^126]。Absolute Zero 只以一个恒等函数三元组起步，由同一模型提出演绎、溯因与归纳三类代码推理任务并自行求解[^130]。代码执行器同时校验任务与答案，且只允许确定性程序[^130]。出题奖励为可学性：平均求解率为 0 时奖励为 0，否则为 $`1-\bar r_{\text{solve}}`$ [^130]。R-Zero 不依赖执行器，从同一基座初始化 Challenger 与 Solver[^131]。Challenger 在 Solver 准确率接近 50% 时奖励最高[^131]。伪标签取 Solver 10 次采样的多数答案，只保留 3 至 7 个答案与之一致的题[^131]。SvS 让策略把自己对欠佳题目的正确解改写成变体题，沿用原题答案，无需新标注[^129]。它与 SwS 的前三位作者相同[^128][^129]。QbQ 由教师 GPT-5-mini 按五种人工设计的结构变换算子，改写当前检查点大多能答对的题[^39]。变体答案必须与原题不同，训练只用题面与最终答案[^39]。

**证据。** 以 Qwen3-4B-Base 做 GRPO（16 次采样平均），未过滤时 CoT-Self-Instruct 为 53.0%，Self-Instruct 为 42.7%[^126]。经答案一致性过滤的 2,926 道合成题达到 57.2，高于 s1k 原题的 44.6 与 10k 道 OpenMathReasoning 题的 47.5[^126]。AZR-Coder-7B 不用任何人工整理数据，总平均比此前最好的零设置 7B 模型高 1.8 分[^130]。在 3B、7B、14B 代码模型上，AZR 的总体增益为 +5.7、+10.2、+13.2[^130]。R-Zero 把 Qwen3-4B-Base 的数学平均分由 42.57 提到 49.93，Absolute Zero 为 46.42[^131]。以 Qwen2.5-32B-Instruct 在 DAPO-17k 上训练，SvS 的 AIME24 与 AIME25 Pass@32 比标准 RLVR 高 18.3% 与 22.8%[^129]。与暴露量相同的延长 RLVR 相比，SvS 的 Pass@32 平均为 53.1，对照为 46.3[^129]。静态增广与不分轮次的 QbQ 数据即使大幅增加数据量，pass@1 也分别停在 12.5% 与 14.5%[^39]。在相同数据预算下，课程式 QbQ 把 Qwen2.5-Math-7B 从 5.62% 提升到 16.46%[^39]。

**局限与崩塌风险。** 已报告的风险可归为标签退化、奖励投机与伪多样性三类（本文判断）。标签退化方面，以 GPT-4o 为参照，R-Zero 的伪标签准确率从 79.0% 降到第三轮的 63.0%[^131]。多轮之后各规模模型的性能都持续下降，模型越大下降越晚[^131]。退化没有统一的标签准确率阈值：0.6B 模型在 70.6% 时就开始退化，4B 模型却能容忍 48.8%[^131]。作者推测更根本的原因是仅用自合成数据训练引起的模型崩塌[^131]。奖励投机方面，若只奖励可解的变体，SvS 的策略会在题面中嵌入提示，甚至直接写入答案[^129]。作者因此只对策略准确率落在 [1/8, 5/8] 的变体给正奖励[^129]。Absolute Zero 发现自提程序的全局变量可能泄露答案，但清除后性能下降，最终予以保留[^130]。伪多样性方面，各取 100 道候选题的人工审计中，R-Zero 与 CoT-Self-Instruct 与种子近似重复的比例为 18% 与 21%，Learning to Pose Problems 为 4%[^9]。

外部信号越弱，收益越小（本文推断）。AZR 在 Llama3.1-8B 上增益为 +3.2，低于 SimpleRL 的 +4.5[^130]。完全自演化的 SwS 变体以 Qwen2.5-14B-Instruct 为策略，平均只提升 1.2%[^128]。借助外部出题与标注模型的 7B 版本提升 10.0，但基座与初始题集不同，不能直接相减（本文判断，依据见[^128]）。最可能的调和变量是验证信号的强度：执行器能精确判对，多数投票的标签随难度上升而失真，教师答案则引入了外部知识（本文推断，依据见[^130][^131][^39]）。QbQ 的题目与答案来自更强的教师，严格说不属于零数据自博弈（本文判断，依据见[^39]）。

### 5.6 去污染实践与公开配方

**去污染做法。** 各工作的去污染方法高度异质（本文判断）。最简单的是字符串精确匹配，Big-Math 以此排查 MATH 与 Omni-MATH 各 500 道测试题[^118]。SynLogic 只核实了不存在与测试集完全相同的样本[^125]。n-gram 匹配用得较多，但窗口长度不一（本文统计）。WebInstruct 删除与评测题或答案有 10-gram 匹配的网页[^116]。NaturalReasoning 用 13-gram 删去 0.026% 的条目[^122]。rStar-Coder 用 16-gram[^134]，Nemotron-Cascade 用 9-gram[^11]。Olmo 3 与 ZGCM-1 用 8-gram，以 50% 的重叠为阈值[^10][^45]。KodCode 以嵌入余弦相似度 0.95 为阈值，447K 道题只标出 94 道[^121]。另一类做法是嵌入召回加大模型评审（本文判断）。WizardMath 为每道测试题检索最相近的 5 条训练样本，交 GPT-4 判断[^114]。DeepMath-103K 由 Llama-3.3-70B-Instruct 判断候选是否为同题或改写[^119]。OpenMathInstruct-2 用大模型去污染从 569K 道新合成题中删去约 50K 道，并给出 n-gram 匹配发现不了的样例[^88]。OpenThoughts 联合 Indel 相似度（阈值 75%）与 13-gram，在人工污染集上只漏掉 3092 条中的 12 条，误删 1.4% 的干净样本[^4]。

大规模收集的题池与语料天然含有大量测试题（本文判断，依据见[^119][^124]）。DeepMath-103K 的原始题池在去污染前包含 AIME24 与 AMC23 的 90%、MATH500 的 76.6% 的测试题[^119]。CodeI/O 删去原题后，LeetCode-O 仍有 21.5% 的题因与姊妹题共享描述而被标为潜在泄漏[^124]。作者报告泄漏与非泄漏子集上的增益相近[^124]。在本文精读的全文中，SwS、SvS 与 R-Zero 均未见去污染步骤的描述（本文统计，依据见[^128][^129][^131]）。General-Reasoner 与 CoT-Self-Instruct 同样未见（本文统计，依据见[^120][^126]）。

**公开配方。** OpenThoughts 在 27 个代码、21 个数学与 14 个科学题源上做消融，每个策略生成 31,600 条数据[^4]。只取 1 到 2 个高质量题源，优于混合 8 或 16 个题源[^4]。以大模型标注的难度或回答长度筛题，优于嵌入或 fastText 过滤[^4]。少题多答的效果与多题少答相近甚至更好，作者据此认为答案多样性高时题目多样性影响不大[^4]。数学域是例外，每题只标注 1 次的效果最好，作者仍因 16 倍采样便于扩量而选用后者[^4]。数据卡显示，OpenThoughts3-1.2M 只建立在约 75k 道题上，每题由 QwQ-32B 标注 16 次[^58]。以此只做监督微调的 OpenThinker3-7B，在 AIME 2025、LiveCodeBench 06/24-01/25 与 GPQA Diamond 上达到 53%、51% 与 54%[^57]。NaturalThoughts 以 NaturalReasoning 为题池、DeepSeek-R1 为教师，在 Qwen2.5-7B-Instruct 学生上，其 500K 条数据在 4 项基准中的 3 项上优于 OpenThoughts3 的 1.2M 条[^5]。它也认为推理轨迹的多样性比题目本身的多样性更重要[^5]。rStar-Coder 与 OpenMathInstruct-2 的结论相反（本文判断，依据见[^134][^88]）。rStar-Coder 以 7B 学生固定 37.7K 道题，每题 1、8、16 条解时 LiveCodeBench 为 40.8、51.1、54.7[^134]。题目更多样的 580K 条数据集，LiveCodeBench 为 57.3、USACO 2025 为 16.15，而 16 条解的 603K 条在 USACO 2025 上只有 10.41[^134]。OpenThoughts 自身的数学消融与后两者方向一致，分歧集中在代码与科学域（本文判断，依据见[^4]）。调和变量很可能是数据规模与评测分布（本文推断）。OpenThoughts 每组实验只有 31,600 条，rStar-Coder 的对比在 580K 与 603K 条的规模上进行（本文判断，依据见[^4][^134]）。OpenMathInstruct-2 的收益出现在唯一题目从 1K 增至 6.5K 的低区间，rStar-Coder 的差距则在 USACO 上最大（本文推断，依据见[^88][^134]）。

许可同样约束题目来源的复用（本文判断）。OpenMathInstruct-1 以许可为由改用 Mixtral[^132]。Olmo 3 剔除非商业或许可不明的样本，并为许可不宽松的高性能数据集另行合成替代数据[^10]。AM 系列数据只允许研究用途[^1][^60]。NaturalReasoning 采用 cc-by-nc-4.0[^61]，OpenThoughts3-1.2M 采用 apache-2.0[^58]。表 5-3 对照主要公开数据集的题目侧设计。

表 5-3 主要公开推理数据集与配方的题目侧对比（“未见描述”指本文精读的全文中未找到相应说明，属本文判断）

| 数据集或配方 | 题目来源 | 轨迹生成者 | 规模与要点 | 去污染 | 许可或公开 |
| --- | --- | --- | --- | --- | --- |
| OpenThoughts3-1.2M[^4][^58] | 数学只用 OpenMath-2-Math，代码与科学各取 2 个最优题源 | QwQ-32B | 约 75k 道题，每题 16 个答案，共 1.2M 条 | Indel 相似度与 13-gram | apache-2.0 |
| NaturalThoughts[^5] | NaturalReasoning 题池 | DeepSeek-R1 | 1,000 至 500,000 条 | 未见描述 | 未见描述 |
| AM-DeepSeek-R1-Distilled[^1] | 多个开源数据集，语义去重 | 主要为 DeepSeek-R1，0.5M 条沿用开源回答，0.9M 条新蒸馏 | 1.4M 条，38.9% 有参考答案，21.9% 有测试用例，39.2% 两者皆无 | 称已清除测试集污染 | 仅限研究 |
| AM-Thinking-v1-Distilled[^60] | 1.89M 条查询，与 Qwen3-235B-A22B 版共享 | AM-Thinking-v1 | 同一查询集上分别训练的学生，AIME2025 为 72.2 对 62.2 | 未见描述 | 仅限研究 |
| OmniThought[^2] | OpenThoughts2-1M（约 640K 题）与 DeepMath-103K，共 708K 题 | DeepSeek-R1 与 QwQ-32B | 超过 2M 条，每题至少 2 条验证正确的轨迹 | 未见描述 | 未见描述 |
| NaturalReasoning[^122][^61] | 由 DCLM 与 FineMath 文档反向构造 2.8M 题，公开 1,145,824 条 | Llama3.3-70B-Instruct 参考回答 | 公开子集中 18.29% 无参考答案 | 13-gram，删去 0.026% | cc-by-nc-4.0 |
| Nemotron-Post-Training-Dataset-v2[^59] | 公开语料或合成题，滤除答案易猜的题 | 多个开放模型，DeepSeek-R1-0528 生成 5,713,694 条 | 数学 239,467、代码 175,000、STEM 355,000 条 | 未见描述 | 以 CC-BY-4.0 为主 |
| Nemotron-Cascade SFT[^11] | 数学提示沿用 AceReason-Nemotron-1.1，含 AceMath、NuminaMath 与 OpenMathReasoning | DeepSeek-R1 与 DeepSeek-R1-0528 | 数学第一阶段 353K 题、2.77M 条（每题 7.8 条），代码第二阶段每题 17.6 条 | 9-gram，软件工程按仓库排除 | 模型与数据已公开 |
| Olmo 3 Dolci-Think-SFT[^10] | 汇集其他开源项目的提示并大量过滤 | QwQ-32B 与 DeepSeek R1 | 7B 版提示 2,268,468 条，其中 OpenThoughts 3+ 数学 752,997 条 | 8-gram，重叠阈值 0.5 | 剔除非商业或许可不明的数据 |
| ZGCM-1 SFT[^45] | 开源数据与内部蒸馏数据 | 开源数据与内部蒸馏，后者教师未点名 | 4,921,933 条，推理部分从 2,268,178 条候选中保留 1,307,175 条 | 8-gram 重叠超过 50% 即删除 | 公开各阶段数据与配方 |
| OpenMathReasoning[^133] | AoPS 论坛挖掘 540K 题，含 260K 道证明转化题 | 长思维链由 DeepSeek-R1 与 QwQ-32B 生成 | 3.2M 条长思维链、1.7M 条工具集成推理 | 大模型比对删除近似基准题 | 商用许可 |
| OpenCodeReasoning[^89][^4] | TACO、APPS、CodeContests 与 OpenR1 的 CodeForces，精确去重后 28,904 题 | DeepSeek-R1 | 736,712 条 | 余弦 0.7 召回，两个大模型评审 | cc-by-4.0 |

### 5.7 小结（本文判断）

- 题目来源的主线从“多出题”转向“出可验证的题”。早期改写与合成多由强教师出题并补写解答，新题缺少可核对的答案（依据见[^114][^115][^123]）。2025 年后的题集普遍以执行测试、闭式答案或规则验证器为准入条件（依据见[^121][^119][^125]）。
- 难度是相对于某个参照模型的通过率区间，不是题目的固有属性（依据见[^118][^128][^129]）。难度标签能否跨模型族迁移尚未验证（依据见[^118]）。SwS 与 QbQ 对“取多难”的结论相反，分歧更可能来自难题是直接用于训练还是只作改写种子（依据见[^128][^39]）。
- 人设、代码片段、概念图，以及 2026 年工作中的技能库与知识图谱，是扩大题目多样性的主要外部结构（依据见[^117][^123][^17]）。题目多样性与每题采样数孰轻孰重，取决于数据规模与评测分布（依据见[^4][^134][^88]）。
- 自提题在有精确执行器时最稳健，依赖多数投票时会随迭代退化，并伴随奖励投机与近似重复（依据见[^130][^131][^9]）。去掉外部信号后收益明显缩小，现有证据不支持长期无外部信号的自我演化（依据见[^128][^129]）。
- 网络挖掘的题池在去污染前污染严重，而去污染方法从精确匹配到大模型评审高度异质（依据见[^119][^4][^88]）。许可条款决定题目来源能否复用，已成为配方设计的约束（依据见[^10][^132][^61]）。

## 参考来源

[^75]: [Yu et al. — MetaMath: Bootstrap Your Own Mathematical Questions for Large Language Models (arXiv 2309.12284, 2023-09)](https://arxiv.org/abs/2309.12284v4)
[^79]: [Xu et al. — WizardLM: Empowering large pre-trained language models to follow complex instructions (arXiv 2304.12244, 2023-04)](https://arxiv.org/abs/2304.12244v3)
[^114]: [Luo et al. — WizardMath: Empowering Mathematical Reasoning for Large Language Models via Reinforced Evol-Instruct (arXiv 2308.09583, 2023-08)](https://arxiv.org/abs/2308.09583)
[^115]: [Tang et al. — MathScale: Scaling Instruction Tuning for Mathematical Reasoning (arXiv 2403.02884, 2024-03)](https://arxiv.org/abs/2403.02884)
[^132]: [Toshniwal et al. — OpenMathInstruct-1: A 1.8 Million Math Instruction Tuning Dataset (arXiv 2402.10176, 2024-02)](https://arxiv.org/abs/2402.10176)
[^66]: [Yue et al. — MAmmoTH: Building Math Generalist Models through Hybrid Instruction Tuning (arXiv 2309.05653, 2023-09)](https://arxiv.org/abs/2309.05653v3)
[^88]: [Toshniwal et al. — OpenMathInstruct-2: Accelerating AI for Math with Massive Open-Source Instruction Data (arXiv 2410.01560, 2024-10)](https://arxiv.org/abs/2410.01560v2)
[^17]: [Jiao et al. — Agentic Proposing: Enhancing Large Language Model Reasoning via Compositional Skill Synthesis (arXiv 2602.03279, 2026-02)](https://arxiv.org/abs/2602.03279v1)
[^116]: [Yue et al. — MAmmoTH2: Scaling Instructions from the Web (arXiv 2405.03548, 2024-05)](https://arxiv.org/abs/2405.03548)
[^120]: [Ma et al. — General-Reasoner: Advancing LLM Reasoning Across All Domains (arXiv 2505.14652, 2025-05)](https://arxiv.org/abs/2505.14652)
[^122]: [Yuan et al. — NaturalReasoning: Reasoning in the Wild with 2.8M Challenging Questions (arXiv 2502.13124, 2025-02)](https://arxiv.org/abs/2502.13124)
[^119]: [He et al. — DeepMath-103K: A Large-Scale, Challenging, Decontaminated, and Verifiable Mathematical Dataset for Advancing Reasoning (arXiv 2504.11456, 2025-04)](https://arxiv.org/abs/2504.11456)
[^133]: [Moshkov et al. — AIMO-2 Winning Solution: Building State-of-the-Art Mathematical Reasoning Models with OpenMathReasoning dataset (arXiv 2504.16891, 2025-04)](https://arxiv.org/abs/2504.16891)
[^15]: [Lu et al. — Golden Goose: A Simple Trick to Synthesize Unlimited RLVR Tasks from Unverifiable Internet Text (arXiv 2601.22975, 2026-01)](https://arxiv.org/abs/2601.22975v2)
[^50]: [Langlais et al. — It's All Training: A Fully Synthetic Single-Stage Recipe for LLMs (arXiv 2609.37891, 2026-09)](https://arxiv.org/abs/2609.37891v1)
[^4]: [Guha et al. — OpenThoughts: Data Recipes for Reasoning Models (arXiv 2506.04178, 2025-06)](https://arxiv.org/abs/2506.04178v2)
[^118]: [Albalak et al. — Big-Math: A Large-Scale, High-Quality Math Dataset for Reinforcement Learning in Language Models (arXiv 2502.17387, 2025-02)](https://arxiv.org/abs/2502.17387)
[^61]: [Meta AI — natural\_reasoning (Hugging Face dataset card)](https://huggingface.co/datasets/facebook/natural_reasoning)
[^117]: [Ge et al. — Scaling Synthetic Data Creation with 1,000,000,000 Personas (arXiv 2406.20094, 2024-06)](https://arxiv.org/abs/2406.20094)
[^123]: [Wei et al. — Magicoder: Empowering Code Generation with OSS-Instruct (arXiv 2312.02120, 2023-12)](https://arxiv.org/abs/2312.02120)
[^121]: [Xu et al. — KodCode: A Diverse, Challenging, and Verifiable Synthetic Dataset for Coding (arXiv 2503.02951, 2025-03)](https://arxiv.org/abs/2503.02951)
[^134]: [Liu et al. — rStar-Coder: Scaling Competitive Code Reasoning with a Large-Scale Verified Dataset (arXiv 2505.21297, 2025-05)](https://arxiv.org/abs/2505.21297)
[^124]: [Li et al. — CodeI/O: Condensing Reasoning Patterns via Code Input-Output Prediction (arXiv 2502.07316, 2025-02)](https://arxiv.org/abs/2502.07316)
[^32]: [Zheng et al. — Combinatorial Synthesis: Scaling Code RLVR via Atomic Decomposition and Recombination (arXiv 2605.31058, 2026-05)](https://arxiv.org/abs/2605.31058v1)
[^125]: [Liu et al. — SynLogic: Synthesizing Verifiable Reasoning Data at Scale for Learning Logical Reasoning and Beyond (arXiv 2505.19641, 2025-05)](https://arxiv.org/abs/2505.19641)
[^37]: [Kimi Team — Kimi K3: Open Frontier Intelligence (arXiv 2607.24653, 2026-07)](https://arxiv.org/abs/2607.24653v2)
[^128]: [Liang et al. — SwS: Self-aware Weakness-driven Problem Synthesis in Reinforcement Learning for LLM Reasoning (arXiv 2506.08989, 2025-06)](https://arxiv.org/abs/2506.08989)
[^11]: [Wang et al. — Nemotron-Cascade: Scaling Cascaded Reinforcement Learning for General-Purpose Reasoning Models (arXiv 2512.13607, 2025-12)](https://arxiv.org/abs/2512.13607v2)
[^62]: [NVIDIA — NeMo Curator: Llama-Nemotron Data Curation Tutorial (GitHub)](https://github.com/NVIDIA-NeMo/Curator/blob/main/tutorials/text/llama-nemotron-data-curation/README.md)
[^9]: [Wei et al. — Learning to Pose Problems: Reasoning-Driven and Solver-Adaptive Data Synthesis (arXiv 2511.09907, 2025-11)](https://arxiv.org/abs/2511.09907v6)
[^39]: [Bao et al. — Question Begets Question: Self-Evolving Curriculum for Reinforcement Fine-Tuning on Competition Mathematics (arXiv 2608.01522, 2026-08)](https://arxiv.org/abs/2608.01522v1)
[^129]: [Liang et al. — Beyond Pass@1: Self-Play with Variational Problem Synthesis Sustains RLVR (arXiv 2508.14029, 2025-08)](https://arxiv.org/abs/2508.14029)
[^131]: [Huang et al. — R-Zero: Self-Evolving Reasoning LLM from Zero Data (arXiv 2508.05004, 2025-08)](https://arxiv.org/abs/2508.05004)
[^130]: [Zhao et al. — Absolute Zero: Reinforced Self-play Reasoning with Zero Data (arXiv 2505.03335, 2025-05)](https://arxiv.org/abs/2505.03335)
[^127]: [Zhan et al. — MathSmith: Towards Extremely Hard Mathematical Reasoning by Forging Synthetic Problems with a Reinforced Policy (arXiv 2508.05592, 2025-08)](https://arxiv.org/abs/2508.05592)
[^16]: [Peng et al. — CoDiQ: Test-Time Scaling for Controllable Difficult Question Generation (arXiv 2602.01660, 2026-02)](https://arxiv.org/abs/2602.01660v1)
[^89]: [Ahmad et al. — OpenCodeReasoning: Advancing Data Distillation for Competitive Coding (arXiv 2504.01943, 2025-04)](https://arxiv.org/abs/2504.01943v2)
[^126]: [Yu et al. — CoT-Self-Instruct: Building high-quality synthetic prompts for reasoning and non-reasoning tasks (arXiv 2507.23751, 2025-07)](https://arxiv.org/abs/2507.23751)
[^10]: [Olmo Team — Olmo 3 (arXiv 2512.13961, 2025-12)](https://arxiv.org/abs/2512.13961v2)
[^45]: [He et al. — ZGCM-1: A Fully Open and Extremely Efficient Foundation Model for Math and Agentic Search (arXiv 2609.13356, 2026-09)](https://arxiv.org/abs/2609.13356v2)
[^58]: [OpenThoughts Team — OpenThoughts3-1.2M (Hugging Face dataset card)](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M)
[^57]: [OpenThoughts Team — OpenThoughts3: A New SOTA Reasoning Data Recipe (blog)](https://www.openthoughts.ai/blog/ot3)
[^5]: [Li et al. — NaturalThoughts: Selecting and Distilling Reasoning Traces for General Reasoning Tasks (arXiv 2507.01921, 2025-07)](https://arxiv.org/abs/2507.01921v1)
[^1]: [Zhao et al. — 1.4 Million Open-Source Distilled Reasoning Dataset to Empower Large Language Model Training (arXiv 2503.19633, 2025-03)](https://arxiv.org/abs/2503.19633v1)
[^60]: [a-m-team — AM-Thinking-v1-Distilled (Hugging Face dataset card)](https://huggingface.co/datasets/a-m-team/AM-Thinking-v1-Distilled)
[^2]: [Cai et al. — Reasoning with OmniThought: A Large CoT Dataset with Verbosity and Cognitive Difficulty Annotations (arXiv 2505.10937, 2025-05)](https://arxiv.org/abs/2505.10937v1)
[^59]: [NVIDIA — Nemotron-Post-Training-Dataset-v2 (Hugging Face dataset card)](https://huggingface.co/datasets/nvidia/Nemotron-Post-Training-Dataset-v2)
