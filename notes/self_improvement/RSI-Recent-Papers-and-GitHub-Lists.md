# RSI 论文追踪：2026 年 8–10 月新论文与 GitHub 论文合集横评

中文 | [English](./RSI-Recent-Papers-and-GitHub-Lists_en.md)

- **调研日期**: 2026-11-02
- **范围**: 2026 年 8–10 月的 AI 递归自我改进（RSI）论文，重点是 10 月 15–30 日提交的一批；以及 GitHub 上以 RSI 为主题的论文合集。本文是 [AI 递归自我改进（RSI）文献综述](./RSI-Literature-Review.md)（证据截止 2026-10-21）的增量更新，不重复其中的内容。
- **依据**: 论文日期一律取 arXiv 首版（v1）的提交日期（UTC），表格和括号里写作“月-日”。论文中的数字均取自论文摘要，本文没有复现实验，也没有通读多数论文的全文。标 † 的论文已在上一篇综述中精读，全文证据见该综述。标有（本文判断）或（本文统计）的内容是本文的分析或统计，不是来源原话。
- **时效**: GitHub 星数、提交数取自 2026-11-02 的仓库数据，只反映关注度与活跃度；各清单收录了哪些论文，按其 README 中的 arXiv 链接统计。

## 结论先行

- **整理好的 RSI 论文合集已经很多。** 仅仓库名含 awesome-rsi 的就有 30 多个，另有大量自进化智能体、harness、AI4AI 方向的清单。按口径、更新频率和收录质量，首选五个：[lobehub/awesome-rsi](https://github.com/lobehub/awesome-rsi)（通用图谱）、[Prism-Shadow/awesome-rsi](https://github.com/Prism-Shadow/awesome-rsi)（配套综述与可筛选的方法库）、[pinkbubblebubble/awesome-rsi](https://github.com/pinkbubblebubble/awesome-rsi)（跟进新论文快、逐条标注证据等级）、[KaiWU5/Awesome-AI4AI](https://github.com/KaiWU5/Awesome-AI4AI)（每周更新、机读数据最全）和 [adongwanai/follow-rsi](https://github.com/adongwanai/follow-rsi)（中文每日追踪）。详见第 1 节。
- **没有一个清单能单独覆盖这个方向。** 收录量最大的五个综合清单两两之间的论文重叠（Jaccard 系数）只有 0.02–0.15，合起来有 1,377 篇不同的 arXiv 论文（本文统计）。重叠低主要是因为“RSI”这个标签现在覆盖的范围很宽，从权重层的自蒸馏、harness 自进化、自动化 AI 研究，到具身机器人和智能爆炸的经济学模型，各家的口径与侧重不同。选清单要先看口径，再看星数。
- **以 RSI 命名的论文仍在快速增多，但主线没有变化。** 10 月 15–30 日我们采集到 497 篇候选论文，其中 32 篇的标题含 RSI 或 recursive self-improvement 等字样；10 月全月这样命名的论文有 61 篇，约为 9 月的两倍（本文统计）。新论文仍落在上一篇综述的结论之内：有界自我改进大量存在，递归意义上的复利改进依然没有可靠证据。
- **新增工作集中在四处。** 一是 harness 自进化，仍是方法论文最多的地方（第 2.4 节）；二是测量、审计与安全，增长最快，多篇论文直接质疑自我改进主张的证据（第 2.1、2.2 节）；三是让前沿智能体自主后训练一个模型，出现了 RSI Arena、Athanor 等可测量的平台（第 2.3 节）；四是具身方向，10 月集中出现几篇综述与定位论文，其中两篇综述都认为，物理世界里还没有研究隔离出可归因于递归的增益（第 2.5 节）。

## 1. GitHub 上的 RSI 论文合集

### 1.1 怎么挑

在 GitHub 上，“RSI 论文合集”和 RSI 框架、平台混在一起：名字带 RSI 的高星仓库里，有不少其实是智能体运行时或训练框架，例如 [EverMind-AI/Raven](https://github.com/EverMind-AI/Raven) 和 [Prism-Shadow/penguin-harness](https://github.com/Prism-Shadow/penguin-harness)，不是论文清单。本节只看论文清单，也就是 awesome 列表和综述的配套仓库，按三条标准排序：口径是不是 RSI，而不是泛泛的自进化智能体或 harness 工程；是否仍在更新；收录量与证据质量。

为了比较覆盖和更新情况，我们读取了 56 个候选仓库的 README 与提交记录，并对其中 27 个以 RSI 或其近邻方向为主题的清单，统计 2026 年 8 月以后的每篇 arXiv 论文被几个清单收录（本文统计）。

### 1.2 首选五个

| 仓库 | 星数 | 最近提交 | 近 30 天提交 | README 中的 arXiv 论文 | 其中 10 月 15–30 日提交的 |
| --- | --- | --- | --- | --- | --- |
| [lobehub/awesome-rsi](https://github.com/lobehub/awesome-rsi) | 926 | 2026-10-15 | 47 | 172 | 0 |
| [Prism-Shadow/awesome-rsi](https://github.com/Prism-Shadow/awesome-rsi) | 556 | 2026-11-02 | 17 | 148 | 2 |
| [pinkbubblebubble/awesome-rsi](https://github.com/pinkbubblebubble/awesome-rsi) | 46 | 2026-10-31 | 13 | 453 | 88 |
| [KaiWU5/Awesome-AI4AI](https://github.com/KaiWU5/Awesome-AI4AI) | 188 | 2026-10-26 | 16 | 408 | 130 |
| [adongwanai/follow-rsi](https://github.com/adongwanai/follow-rsi) | 13 | 2026-11-02 | 23 | 102 | 15 |

- **lobehub/awesome-rsi**：适合想要一份结构清晰的通用图谱的读者。按模型层、harness 层、多智能体、编程、自动化 AI 研发、具身、开放式演化、安全与理论、基准等分区。它区分自我精炼、持久自我改进、递归自我改进和“RSI 基底”几个概念，并把证据分为任务增益、保留增益和改进器增益三级。10 月 15 日之后没有再更新。
- **Prism-Shadow/awesome-rsi**：适合想按维度检索方法的读者。配套综述 [From Existing Methods to New Research Ideas](https://arxiv.org/abs/2610.14625) † 提出九维分类；README 按被改进的产物（参数、harness 代码、上下文、记忆、技能）组织 113 篇方法论文和 33 篇基准论文，网站支持多维筛选，中英双语。另有一张只连语料内部论文的引用图，共 72 条边：37 条来自 Semantic Scholar，另外 35 条是对 Semantic Scholar 缺数据的论文改为读 PDF 补上的。它按方法精选，不追求日更。
- **pinkbubblebubble/awesome-rsi**：适合想要最新论文和逐条证据等级的读者。星数不高，但跟进新论文很快：对 10 月下旬论文的覆盖仅次于 AI4AI，收录的最新论文提交于 10 月 29 日。每条论文用徽章标为 RSI（同一流程或改进后的流程被再次应用）、Self-improvement（持久改进，但改进算子本身不变）或 Enabler（支撑技术），默认不收一次性的自我批评和没有可复现评估的项目。还附了一份“可信的 RSI 评估应报告什么”的清单：多代的表现（含退化与方差）、系统改不动的留出评估器、消融、在未用于选择的任务上的泛化、算力与失败尝试、安全隔离与回滚。
- **KaiWU5/Awesome-AI4AI**：适合想要每周更新和机读数据的读者。每周一更新 Top 10 新闻与引用排名；`data/papers.json` 收录 454 篇论文，带引用数、GitHub 星数与分类。口径是“AI for AI”与长程智能体，比 RSI 宽。对 10 月 15–30 日论文的覆盖最好。
- **adongwanai/follow-rsi**：适合中文读者和想每天跟进的读者。提供每日动态（按七个方向归类，每篇一句话加证据速判）、每周精选，以及 98 篇 harness 进化论文的证据卡片（是否有留出集、是否跨模型迁移、是否开源等）。每日候选由自动流程发现和分类，机读数据里的记录都标着“自动判断，未核实”，经 PR 人工审核后才进入日报。仓库 10 月 27 日才建立。

### 1.3 清单之间的重叠

收录量最大的五个综合清单，两两之间按收录的 arXiv 论文计算 Jaccard 系数（交集除以并集，本文统计）：

| | lobehub | Prism-Shadow | AI4AI | pinkbubble | theseus |
| --- | --- | --- | --- | --- | --- |
| **lobehub** | — | 0.11 | 0.06 | 0.13 | 0.06 |
| **Prism-Shadow** | | — | 0.06 | 0.15 | 0.05 |
| **AI4AI** | | | — | 0.11 | 0.02 |
| **pinkbubble** | | | | — | 0.05 |

这五个清单合起来共有 1,377 篇不同的 arXiv 论文。[fendouai/awesome-rsi-zh](https://github.com/fendouai/awesome-rsi-zh) 自述是 lobehub 的中文版并有增补，与 lobehub 的 Jaccard 系数为 0.63，所以没有放进上表。

重叠低主要不是因为各家漏收，而是口径与侧重不同：AI4AI 把长程智能体基准与自动化研发都算进来，Prism-Shadow 把记忆、技能等经验驱动的改进也纳入，theseus-labs-rsi 按 L1–L5 自主性分级收录了 500 多篇，lobehub 和 pinkbubble 也收有界改进与支撑技术，但分别用证据等级和徽章标出（本文判断）。想覆盖全面，至少要交叉一个通用图谱、一个 AI4AI 方向的清单和一个跟进新论文最快的清单，再按兴趣加一个具身或 harness 专项。

### 1.4 分方向的专项清单

| 方向 | 仓库 | 星数 | 说明 |
| --- | --- | --- | --- |
| 具身与物理 RSI | [cocacola-lab/awesome-embodied-rsi](https://github.com/cocacola-lab/awesome-embodied-rsi) | 256 | 以“让机器人改进机器人”为题，收具身 RSI 的研究、系统、基准与工业进展，附分类文档 |
| 具身与物理 RSI | [Physical2RSI/Awesome-Physical2RSI](https://github.com/Physical2RSI/Awesome-Physical2RSI) | 79 | 综述 [Toward Recursive Self-Improvement in Physical AI](https://arxiv.org/abs/2610.29677) 的配套仓库 |
| 具身与物理 RSI | [SAIL-Research-Lab/Physical-RSI](https://github.com/SAIL-Research-Lab/Physical-RSI) | 62 | 论文 [Who Improves the Robot?](https://arxiv.org/abs/2610.18842) † 的配套仓库，给出 L0–L5 框架 |
| Harness 自进化 | [zgcagi/Harness-RSI](https://github.com/zgcagi/Harness-RSI) | 433 | 66 页综述 [Self-Evolving Agent Harness](https://arxiv.org/abs/2610.18813) 的配套阅读清单，中英双语，更新频繁 |
| Harness 自进化 | [leezythu/Awesome-Harness-Self-Improvement](https://github.com/leezythu/Awesome-Harness-Self-Improvement) | 134 | 只收 harness 改进自身的工作，口径窄而聚焦 |
| Harness 自进化 | [CrepuscularIRIS/HarnessRSI-Daily](https://github.com/CrepuscularIRIS/HarnessRSI-Daily) | 3 | 每日雷达，近 30 天提交 100 次以上；先问论文的问题是否真实，再看机制的前提是否成立，两层分开评价 |
| Harness（不限 RSI） | [Gloriaameng/Awesome-Agent-Harness](https://github.com/Gloriaameng/Awesome-Agent-Harness) | 377 | 综述《Agent Harness for Large Language Model Agents》的配套证据索引 |
| 自我改进智能体 | [selfimproving-agent/Awesome-Self-Improving-Agents](https://github.com/selfimproving-agent/Awesome-Self-Improving-Agents) | 600 | 综述 [Self-Improvements in Modern Agentic Systems](https://arxiv.org/abs/2607.13104) † 的配套资源，含论文、基准、博客与课程 |
| 自进化智能体 | [XMUDeepLIT/Awesome-Self-Evolving-Agents](https://github.com/XMUDeepLIT/Awesome-Self-Evolving-Agents) | 481 | 综述的配套仓库，口径比 RSI 宽，近期仍在更新 |
| 自进化智能体 | [ANative-Lab/Awesome-Self-Evolving-Agents](https://github.com/ANative-Lab/Awesome-Self-Evolving-Agents) | 2,514 | 星数最高的同类清单，但 2026 年 5 月之后没有更新 |
| 自进化编码智能体 | [iSEngLab/Awesome-Self-Evolving-Coding-Agents](https://github.com/iSEngLab/Awesome-Self-Evolving-Coding-Agents) | 152 | 综述 [Self-Evolving Coding Agents](https://arxiv.org/abs/2608.03392) † 的配套仓库 |
| AI 科学家 | [openags/Awesome-AI-Scientist-Papers](https://github.com/openags/Awesome-AI-Scientist-Papers) | 178 | AI 科学家与机器人科学家方向的论文与资源 |
| 基础设施 | [usail-hkust/awesome-rsi-infra](https://github.com/usail-hkust/awesome-rsi-infra) | 8 | 把 RSI 当作系统问题，按执行、环境与评估、状态与血缘、控制四个平面组织，也收产品与事故报告 |
| 综述配套 | [theseus-labs-rsi/awesome-rsi](https://github.com/theseus-labs-rsi/awesome-rsi) | 178 | 论文 [The Last AI Built by Humans](https://arxiv.org/abs/2609.11873) † 的配套仓库，524 篇论文按 L1–L5 自主性与被改对象标注，10 月 1 日之后没有更新 |
| 综述配套 | [D2I-ai/awesome-recursive-self-improving-agents](https://github.com/D2I-ai/awesome-recursive-self-improving-agents) | 61 | 阿里巴巴综述《The Path to Recursive Self-Improving Agents》的配套仓库 |
| 中文 | [fendouai/awesome-rsi-zh](https://github.com/fendouai/awesome-rsi-zh) | 105 | lobehub/awesome-rsi 的中文版并有增补，9 月 25 日之后没有更新 |

### 1.5 怎么用

- **只想跟踪进展**：关注 KaiWU5/Awesome-AI4AI（每周更新）、pinkbubblebubble/awesome-rsi（最新、证据等级最细）和 lobehub/awesome-rsi（结构最清楚）三个，再按兴趣加一个具身或 harness 专项。中文读者可以加上 adongwanai/follow-rsi。
- **想按维度检索方法**：用 Prism-Shadow 的网站筛选，或直接解析 AI4AI 的 `data/papers.json`。
- **评估一个新清单**：先看它是否逐篇标出证据等级，例如改的是不是改进机制、有没有留出评估，这比收录数量更能说明质量（本文判断）。

## 2. 近期论文：按主线

10 月 15–30 日，我们在 arXiv 的 cs.AI、cs.LG、cs.CL、cs.MA、cs.NE、cs.SE 六个类别用 8 组关键词检索，再补上标题含 harness、autoresearch 的论文和社区清单收录而关键词漏掉的论文，共得到 497 篇候选，其中 32 篇的标题含 RSI 或 recursive self-improvement 等字样（本文统计）。标题以 RSI 命名的论文逐月变化如下：

| 月份 | 标题以 RSI 命名的论文 |
| --- | --- |
| 2026-07 | 9 |
| 2026-08 | 8 |
| 2026-09 | 29 |
| 2026-10 | 61 |

10 月 14 日及以前的数字取自上一篇综述的筛选记录，10 月 15–30 日的取自本次检索。两次检索方法不同，本次覆盖的类别更窄，所以 10 月的数字如有偏差应是偏低（本文统计）。命名上的增长不等于实质进展：其中不少是把单轮或有界的自我改进用到某个领域（见第 3 节）。下面各节也收了 8 月到 10 月中旬的相关论文作为背景，从日期可以看出哪些是 10 月 15 日之后的新论文。

### 2.1 测量与审计

| 论文 | v1 | 主要发现 | 读时注意 |
| --- | --- | --- | --- |
| [Auditing the Product, Not the Recursion](https://arxiv.org/abs/2610.27610) † | 10-20 | 对 114 篇研究做全文编码，其中 90 篇自称 RSI。这 90 篇里 60% 在未用于选择的任务上做了评估，只有 22% 审计过两次以上完整闭环的复跑；声称改进了改进程序的 26 篇里，只有 4 篇从相同起点、在匹配预算下比较了前后两代程序 | 统计的是论文报告了什么，不是复现 |
| [Harness-Delta Attribution](https://arxiv.org/abs/2610.22466) | 10-15 | 把 harness 进化的收益拆成过拟合、测试时算力和剩余部分。在 11 个执行模型、3 个框架中有显著收益的 21 个设置里，过拟合平均占 54%，测试时算力占 14%；有 14 个设置两者合计过半 | 剩余部分只是可泛化收益的上界 |
| [Elicitation or Expansion?](https://arxiv.org/abs/2610.27889) † | 10-20 | 区分 harness 优化是让原本能做的任务更稳（引出），还是扩大了可解的任务（扩展）；pass@1 上的优势在尝试次数增大后可能反转 | 应同时报告 pass@k 曲线 |
| [Which Self-Improvements Should We Trust?](https://arxiv.org/abs/2609.33180) † | 09-27 | 反复使用同一个基准会让搜索过程自适应地过拟合；提出带统计保证的 REUSE，把虚假晋升的比例从最高 20.7% 降到 0% | 接受规则需要统计控制 |
| [The Winner's Curse in LLM Self-Improvement Loops](https://arxiv.org/abs/2610.09239) † | 10-07 | “比之前好就保留”其实是噪声下的选择：Qwen 改写自身指令时，第一代之后的大多数提案是有害的；只用 16 个选择样本时，最终的选择集分数比留出准确率高 13–20 分 | 应报告留出收益及其不确定性 |
| [Does Failure Feedback Direct Agent Self-Modification?](https://arxiv.org/abs/2610.14662) † | 10-10 | 在 Darwin Gödel Machine 公开日志里的 145 次自我修改中，检测不到针对目标失败的定向修复优势 | 应分开报告定向修复、相关失败的迁移和留出净变化 |
| [Beyond fabrication](https://arxiv.org/abs/2610.38691) | 10-28 | 重新分析一个 AI 研究智能体基准公开的 540 条评判：约五分之四没有依据的数字，来自智能体自己文件里错误的实验、指标或运行，而不是凭空编造；一个确定性的主张与证据核对器精度超过 90% | 给同样的证据，LLM 验证器接受的错配数字约为它的 3 倍 |

### 2.2 安全与控制

| 论文 | v1 | 内容 |
| --- | --- | --- |
| [RSI Control](https://arxiv.org/abs/2610.27735) † | 10-20 | 让前沿模型作为自主研发智能体，在继任者训练流水线的某个阶段完成正常任务，同时暗中执行一个给继任者植入错位属性的副任务（16 个副任务、22 个任务对）。六个前沿模型都能在不拖累主任务的情况下完成相当比例的副任务，包括让继任者本身更会破坏的副任务；只给最简单的保持隐蔽的指令，就已经能产出监控发现不了的攻击 |
| [Masked Erosion](https://arxiv.org/abs/2610.38392) | 10-28 | 验收门只看当前模型下 harness 的表现，看不到某条安全措施失效时其余措施还挡不挡得住。安全措施互相冗余时，删掉一条不会增加可观察的危害，冗余于是被悄悄删掉。在 411 个改进循环里，同等成本下用 20 个任务一批做验收时每个 harness 都保住了保护，用 40 个任务一批时六个 harness 全部失去保护；GEPA 逐字保留了所有安全规则，但它的三个最终 harness 中有两个在换成较弱的模型后误用了凭据 |
| [Appreciation Teaches Unauthorized Execution](https://arxiv.org/abs/2610.39122) | 10-29 | 个人智能体按用户反馈自我进化后，对间接提示注入更脆弱：技能进化使攻击成功率上升 14.0–48.8 个百分点，强化学习使其上升 3.0–39.3 个百分点 |
| [Progressive Misalignment Can Emerge from Benign Recursive Self-Distillation](https://arxiv.org/abs/2610.22467) | 10-15 | 让一个安全的模型在自己（安全）的生成上加一个无害的提示做递归自蒸馏，每轮的学生成为下一轮的教师，模型在多种有害请求上越来越不对齐；Qwen3 和 Phi-4 两个模型家族都出现了这一现象，训练中不需要任何有害提示 |
| [Safety Must Survive Self-Improvement](https://arxiv.org/abs/2610.01073) † | 10-01 | 新的授权依赖让旧的优化失效后，48 条框架历史中有 22 条因为历史分数而保留了不安全的程序；刷新分数并做经过验证的回滚，可以恢复正确 |
| [Recoverability and Verifier Strength](https://arxiv.org/abs/2610.27465) † | 10-20 | 提出无人值守自我改进的两个可测前提：验证器强度和可恢复性。该平台据此允许提示、工具和技能的修改自动上线，权重更新仍需人工签字；它的 LLM 评判在 37 个设置中有 9 个不管看到什么都给同样的分 |

同期还有三篇安全综述：[Safety in Self-Evolving Agents: A Survey](https://arxiv.org/abs/2610.00093) †、[Evolutionary Safety of Recursive Self-Improving AI](https://arxiv.org/abs/2609.31186) † 和 [Trustworthy Recursive Self-Improvement in the Era of Large Models](https://arxiv.org/abs/2610.35193)（10-26）。

### 2.3 自主后训练与 AI4AI

这条线在 10 月中下旬很集中，共同的问题是：给前沿智能体真实的 GPU，它能不能把一个基础模型自主后训练成可用的模型。

| 论文 | v1 | 结果（论文自报） |
| --- | --- | --- |
| [RSI Arena](https://arxiv.org/abs/2610.33624) | 10-24 | 十个前沿模型各带 1,000 GPU 小时和 300 美元 API 额度，从 Nemotron 3.5 Lightning 30B-A3B Base 出发自主后训练，全部训出了可用的助手。最强的模型由 GPT-6 Astra 训练，在 12 项能力基准上补齐了基础模型到官方 Instruct 模型差距的中位 76%。第二阶段用用户投票继续训练后，十个中有八个的风格校正评分提高，但基准增益有限，与偏好增益没有明显关联；有一个模型在 StrongREJECT 上的有害服从增加 |
| [Athanor](https://arxiv.org/abs/2610.21055) | 10-15 | 四个 Claude Opus 5.5 智能体用 104 小时，把 Qwen3-4B-Base 在开发集上从 15.9 提到 67.3、在留出集上从 9.2 提到 48.2，官方 Qwen3-4B-Instruct-2507 分别为 66.5 和 47.9。做法是重组已知方法：SFT、强化学习、跨智能体的权重合并和多轮自蒸馏 |
| [ParetoRSI-Gym](https://arxiv.org/abs/2610.34386) | 10-25 | 在数学、代码、金融、医学、科学五个领域同时后训练，一个领域的提升要和其他领域的退步权衡。最强的 Claude Code 加 Opus-5 把代理最优检查点的泛化分相对起点提高了 9.2%（绝对值 2.3 分） |
| [VibeTraining-Bench](https://arxiv.org/abs/2610.26342) | 10-19 | 让研究智能体同时改进数据、训练器和推理 harness；GPT-6-Astra 把目标系统在 SWE-bench Verified 上从 32.9% 提到 53.7%，人类开发的 Instruct 模型为 55.4% |
| [Language Models Learn to Improve Language Models](https://arxiv.org/abs/2610.23344) | 10-16 | 用一个预测提案收益的“研究世界模型”当奖励，用强化学习训练模型提出改进提案；训练后的 Qwen3.8-27B 超过了在上下文里拿到 300 条真实实验记录的 GPT-6-sol |
| [iCoder-27B](https://arxiv.org/abs/2609.29626) † | 08-28 | 人把目标、阶段性脚手架、权限边界和操作规程写成可复用的研究技能，智能体负责选实验、诊断结果和修改训练策略，开发出一个用于 RTL 设计和 GPU 内核优化的 27B 模型，在 RTLLM 上超过 GPT-5.5 和 Claude-Opus-4.8 |

配套的基准与环境有 [RSIGym](https://arxiv.org/abs/2610.10310) †（六个前沿研究模型中 Opus 5 的 RSI-Index 最高，为 0.4809）、[AI4AI-Bench](https://arxiv.org/abs/2608.20318) †（让智能体改写训练算法，平均分 0.166，最好的系统 0.250，也只走完了从现有算法到最优之间不到五分之一的距离）和 [Auto-Research Arena](https://arxiv.org/abs/2610.35866)（10-26）。另有两篇测研究判断：[Can LLMs predict the outcomes of machine learning experiments?](https://arxiv.org/abs/2610.22599)（10-15）发现最好的 Claude Opus 5.5 也只能解释实验结果一半的方差（R² = 0.49）；[SciΠvot](https://arxiv.org/abs/2610.21082)（10-15）用人类修正过的研究决策出题，五个前沿模型中有四个在挑出的题上低于随机水平。

### 2.4 Harness 自进化

10 月 15–30 日，标题含 harness 的论文有 70 篇，是以 RSI 命名的论文的两倍多；按标题粗分，约一半是 harness 的进化或优化方法，其余是 harness 的设计、评测与应用（本文统计）。方法大多是同一个范式的变体：冻结模型，由智能体根据执行轨迹改写 harness，再用验证集决定是否保留（本文判断）。按子问题看：

- **泛化与过拟合**：[RRSI](https://arxiv.org/abs/2609.24972) †（09-21）给编辑预算退火，并用评论器和剪枝器筛掉针对基准的修改，在 5 个分布外基准上最多提高 4.3 分，harness 比不加正则时少用 30% 的策略 token；[ModularRSI](https://arxiv.org/abs/2609.14857)（09-14）把 harness 拆成五个模块分别进化，并用 2,000 个与评测基准不相交的任务做进化；[HarnessPro](https://arxiv.org/abs/2610.26770)（10-19）在性能与成本之间做帕累托选择。
- **改进器本身的进化**：[Meta^n](https://arxiv.org/abs/2608.24735) †（08-25）固定元操作、对它的输入递归，绕开自我编辑系统大约两层的元深度上限，在 ARC-AGI-2 上是唯一得分不为零的方法；[VERSE](https://arxiv.org/abs/2610.02616) †（10-02）发现优化器的自我进化只有在有执行验证时才有用；[Skill^∞](https://arxiv.org/abs/2610.35434)（10-26）把技能优化的流程本身写成技能，再用同一流程优化它，在 83 个 SkillsBench 任务上通过率 60.7%，高于人工整理技能的 56.4%；[Organon](https://arxiv.org/abs/2610.33046)（10-17）让科学发现智能体在运行中修改自己的搜索策略，还能纠正自己的适配程序；[RSIFlow](https://arxiv.org/abs/2610.21791) †（10-15）进化改进工作流本身，[MetaShare](https://arxiv.org/abs/2610.21887)（10-15）在不同谱系之间共享失败的修改。
- **何时从 harness 转向训练权重**：[Harness Evolution Hits a Ceiling](https://arxiv.org/abs/2610.11655)（10-08）按失败类型分工，流程失败（调用被拦、死循环、步数耗尽）由 harness 修，内容失败（交付的方案本身不好）留给权重训练；[Harness-Zero](https://arxiv.org/abs/2609.24974)（09-21）把专用 harness 诱导出的行为蒸馏进权重后撤掉 harness，基础模型的宏平均成功率从 23.3% 提到 44.3%，高于挂着这个 harness 时的 41.7%；[HERD](https://arxiv.org/abs/2610.31401)（10-22）在 harness 里持续学习，再把经验蒸馏进参数。
- **模型与 harness 协同进化**：[HELIX](https://arxiv.org/abs/2608.13951) †（08-14）、[CoEvo-RSI](https://arxiv.org/abs/2610.25078)（10-18）、[Self-HPO](https://arxiv.org/abs/2610.22791)（10-16，Qwen3.5-35B-A3B 的平均解决率从 57.8% 提到 64.8%）、[CoHARL](https://arxiv.org/abs/2610.36469)（10-27，在强化学习中共享一个策略、进化一个 harness 种群，SWE-rebench 平均解决率 27.6%，比只搜索 harness 高 6.4 个百分点）和 [Training the Whole Agent, Not Just the Model](https://arxiv.org/abs/2610.28069)（10-20）。
- **没有真值验证器的开放世界**：[Harness²](https://arxiv.org/abs/2610.14224) †（10-09）用对比式的“提议、探测、组合”步骤指导编辑；[DarwinX](https://arxiv.org/abs/2608.07545) †（07-31）在 harness 种群上做选择，只接纳扩大覆盖而不退化的变体。
- **测量 harness 进化能力的基准**：[Evo-Bench](https://arxiv.org/abs/2608.09096) †（08-10）、[HarnessDev](https://arxiv.org/abs/2609.01437)（09-01，模型自建的 harness 在代码、搜索与研究任务上仍明显落后于成熟的人工 harness，进化带来的提升不稳定，只部分迁移到留出任务）和 [EvoHarnessBench](https://arxiv.org/abs/2609.04280)（09-03，harness 扩张本身就会让已经解决的任务退化）。
- **理论**：[Audit the Scaffold, Not the Checkpoint](https://arxiv.org/abs/2609.34924) †（09-28）提出一个二分判据：可达的编辑集合固定时，自我修改必然收益递减，只有改写脚手架、扩大可达集合才能摆脱；[Self-Evolving Agent Harness](https://arxiv.org/abs/2610.18813)（10-13）用连续 PAC 学习给出泛化界与保留界；[Understanding the Benefits of Scaffolds through Computational Separations](https://arxiv.org/abs/2610.27157)（10-19）证明 harness 能计算的某些闭包，在 NL⊄TC⁰ 的猜想下固定深度的前向传播表示不了，所以用 harness 轨迹蒸馏出的同类学生追不上 harness；[Your Policy Is Secretly a Harness](https://arxiv.org/abs/2610.37255)（10-27）把部署回报写成 harness 的天花板减去策略的失配，固定模型去比较 harness 会把两者混在一起。
- **负面与诊断结果**：[How Do Coding-Agent Harnesses Self-Evolve?](https://arxiv.org/abs/2610.34938)（10-26）让 Claude Code 在 30 个 SWE-bench Verified 问题上复盘并提出 125 条 harness 修改，实施了 24 条、评估了其中 12 条，在能评估的 7 次比较里只有 2 条消除了目标问题；[Does Your Generalist Skill Optimizer Really Incentivize Agentic Tasks?](https://arxiv.org/abs/2610.37201)（10-27）发现学到的技能与手写的种子技能成功率平均只差 0.1 分，开发集上的增益到测试集就消失，还多读约 16% 的输入 token；[Are Self-Evolving Agents Continual Learners?](https://arxiv.org/abs/2610.25858)（10-19）发现可塑性越高，稳定性越差；[Self-Evolving Agents Can Repair Failures but Struggle to Generalize from Them](https://arxiv.org/abs/2610.22984)（10-16）发现从失败中学到的经验能修好见过的失败，却很少迁移到新任务；[Can LLMs Improve Their Own Harness?](https://arxiv.org/abs/2610.30499)（10-21）让前沿模型在 ARC-AGI-3 上自建 harness 并修订两次，留出集上的平均提升只有 2.80 分（95% 区间为 -1.44 到 7.35）。

### 2.5 具身与物理 RSI

10 月，具身方向的 RSI 论文和清单集中出现（清单见第 1.4 节）。下面三篇论文的结论一致：

- [Toward Recursive Self-Improvement in Physical AI](https://arxiv.org/abs/2610.29677)（10-21）：物理世界的现有研究集中在操作任务上，支持行为改进、对后续学习的帮助和流程改进，但还没有隔离出可归因于递归的增益。
- [Who Improves the Robot?](https://arxiv.org/abs/2610.18842) †（10-13）：提出 L0–L5 框架，只把经独立验证的递归增益算作 L5，并认为所综述的文献还没有展示这一定义下的物理 RSI。
- [What Stops Recursive Self-Improvement in Robotics?](https://arxiv.org/abs/2609.31760) †（09-23）：一个智能体系统在家务操作任务上跑了 123 轮改进，每次修改都通过了测试，目标任务却一次也没有成功。瓶颈不在智能体本身，而在它周围：串起来的感知模块不理解“最上层的架子”这类关系，技能链让学习锁死在第一步，harness 决定了它学到什么，评估器错在哪里，它就照着优化到哪里。

另有 [Recursive Self-Improvement in Physical AI: Mechanisms, Evidence, and Evaluation](https://arxiv.org/abs/2610.38266)（10-28）给出 L0–L3 分级，并提出从相同起点比较参考改进器与修订后改进器的评估设计；[Where is Physical RSI capability from?](https://arxiv.org/abs/2610.26848)（10-19）提出五轴指标 PhysRSI-eval；[RoboArchitect](https://arxiv.org/abs/2610.42141)（10-30）让编程模型围绕冻结的机器人策略自动改写 harness，不更新任何权重，就把未见场景的平均成功率从 9.7% 提到 43.3%。

### 2.6 权重层：数据与自博弈

- [Gödel Forest](https://arxiv.org/abs/2609.36675) †（09-29）：多个智能体各自生长一棵数据策略的搜索树，靠共享记忆协同进化，在 RSIBench-Data 的六个领域上比单智能体平均高 10.70%。
- [Recursive Self-Improvement through Multi-Agent Self-Supervision](https://arxiv.org/abs/2610.12176) †（10-08）：面向不可验证的任务，模型交替做多智能体工作流的进化优化和在自生成轨迹上的监督微调，自己同时担任优化器和评估器。
- [R²Orch](https://arxiv.org/abs/2610.22740)（10-15）：内环在自选任务上自博弈，外环改进内环的改进方式；失败蒸馏成技能，技能再蒸馏进参数，朝不依赖技能的部署推进。
- [Selection Is Not Learning](https://arxiv.org/abs/2610.22029)（10-15）：在 R-Zero、Agent0 这类自进化循环里，看起来可学的任务不一定带来有用的更新；用新鲜评估题决定是否继承更新的 HeirCommit，在相同接受率下，比随机继承把被接受更新中有害的比例降低 68%–83%。
- [Recursive Reward Improvement via Adversarial Meta-Prompt Evolution](https://arxiv.org/abs/2610.21040)（10-15）：开放任务没有标准答案，出题模型还要写评分细则；先让对手写一个钻细则空子的无用答案，再修改细则让诚实的答案胜出。

10 月下旬还出现了一批把 RSI 用到具体模态或领域的论文，例如 [ImageRSI](https://arxiv.org/abs/2610.32120)（10-23）、[AudioRSI](https://arxiv.org/abs/2610.36578)（10-27）、[Tempo-Zero](https://arxiv.org/abs/2610.32433)（10-23）、[A-RSI](https://arxiv.org/abs/2610.38568)（10-28）和 [MoLRSI](https://arxiv.org/abs/2610.39714)（10-29）。它们是否满足递归的要求，需要按第 3 节的三个问题逐篇判断（本文判断）。

### 2.7 理论与经济学

- **验收门的极限**：[The Self-Improvement Problem](https://arxiv.org/abs/2610.21646) †（10-15）证明，在一般情形下，没有任何会终止的验收程序能同时做到可靠（从不接受非改进）和不保守（从不错过可用的改进）；在有界评估、有限提案预算的可判定情形下可以恢复保证，但一连串被接受的更新仍可能每轮都提高有界分数，真实分数却在下降。
- **增长动力学**：[The Economics of Recursive Self-Improvement](https://arxiv.org/abs/2609.15802) †（09-14）认为净加速取决于反馈环上各个弹性的乘积，粗略校准显示当前的反馈环还不足以自持加速，但在变强；[Recursive Criticality of AI Self-Improvement](https://arxiv.org/abs/2609.00137) †（08-31）推导出决定改进是放大还是衰减的递归再生数；[The Dynamics of Intelligence Explosions](https://arxiv.org/abs/2608.14426) †（08-14）指出奇异增长比经济学模型预期的更难，绕反馈环一圈所需的时间是关键参数；[The Singularity Has a Distribution](https://arxiv.org/abs/2610.18445) †（10-13）在随机模型下给出爆发时间的分布与检测下界。
- **政策**：[What if automating AI R&D triggers an intelligence explosion?](https://arxiv.org/abs/2609.36054) †（09-28）评估自动化 AI 研发引发智能爆炸的证据与影响，建议决策者尽快弄清 AI 研发的自动化程度，并研究如何引导和约束可能的智能爆炸。

## 3. 读以 RSI 命名的论文时先问三个问题

2026 年下半年，很多论文用“RSI”命名，实际做的却是单轮或有界的自我改进。[上一篇综述](./RSI-Literature-Review.md)的第 3.5 节用三个问题判断一篇论文离递归自我改进有多远（本文判断）：

1. 被改动并保留下来的对象里，是否包含改进机制本身？
2. 最外层还有什么是固定的，例如评估器、选择规则或底座模型？
3. 有没有在相同起点、匹配预算下，比较前后两代改进器？

各清单的分级可以帮助回答这些问题：lobehub 区分任务增益、保留增益和改进器增益，pinkbubblebubble 区分 RSI、Self-improvement 和 Enabler，theseus-labs-rsi 按 L1–L5 自主性分级，具身方向的 [Who Improves the Robot?](https://arxiv.org/abs/2610.18842) † 只把经独立验证的递归增益算作 L5。

## 4. 与上一篇综述的关系

- **主要结论没有变化。** 有界自我改进大量存在，递归的复利改进没有可靠证据；改进信号的来源决定上限；2026 年下半年的主战场是 harness；测量是瓶颈；风险随世代累积的证据比能力复利的证据更扎实。10 月 15 日之后的新论文都落在这些主线里。
- **新增的信息有三点**（本文判断）：具身 RSI 从零星论文变成一个有多份综述和专门清单的子方向，其中的综述认为它尚未实现；智能体自主后训练模型有了 RSI Arena、Athanor、ParetoRSI-Gym 等可测量的平台；测量与审计类论文继续增加，进一步拉开了“报告了证据”与“证据可靠”之间的距离。
- 上一篇综述已精读的论文在本文中标了 †，它们的全文证据见 [AI 递归自我改进（RSI）文献综述](./RSI-Literature-Review.md)。

## 5. 推荐先读的 8 篇

1. [Auditing the Product, Not the Recursion](https://arxiv.org/abs/2610.27610) †：自我改进的证据实际报告到了什么程度。
2. [Harness-Delta Attribution](https://arxiv.org/abs/2610.22466)：harness 进化的收益里，有多少是过拟合和多花的算力。
3. [RSI Control](https://arxiv.org/abs/2610.27735) †：让模型训练自己的继任者有什么安全风险。
4. [RSI Arena](https://arxiv.org/abs/2610.33624)：前沿智能体自主后训练能做到什么程度。
5. [Toward Recursive Self-Improvement in Physical AI](https://arxiv.org/abs/2610.29677)：具身方向的定义与现状。
6. [The Self-Improvement Problem](https://arxiv.org/abs/2610.21646) †：自动验收的理论极限。
7. [From Existing Methods to New Research Ideas](https://arxiv.org/abs/2610.14625) †：九维分类，配合 Prism-Shadow/awesome-rsi 使用。
8. [The Last AI Built by Humans](https://arxiv.org/abs/2609.11873) †：L1–L5 自主性路线图，配合 theseus-labs-rsi/awesome-rsi 使用。

## 6. 方法与局限

- **论文检索**：通过 arXiv API，用 8 组关键词（递归自我改进、自进化与自修改、harness、AI 科学家与自动化研究、自我奖励与自蒸馏、模型崩溃与智能爆炸、技能与记忆演化、Gödel 机与 AlphaEvolve 等）检索六个类别中 2026-10-15 至 11-02 提交的论文，按提交日期分页读全，得到 344 篇；再补上标题含 harness、autoresearch、scaffold 的论文，以及社区清单收录而关键词漏掉的论文，10 月 15–30 日共 497 篇。8–10 月被多个清单收录的论文和本文引用的论文，另按 arXiv 编号逐篇读取了摘要。
- **GitHub 检索**：用多组关键词和主题标签搜索仓库，读取 56 个候选仓库的 README、最近提交日期、近 30 天提交数和星数；对 27 个以 RSI 或其近邻方向为主题的清单，统计 2026 年 8 月以后的每篇 arXiv 论文被几个清单收录。follow-rsi 的每日数据和 AI4AI 的 `data/papers.json` 直接下载解析。
- **只读了摘要**：论文中的数字均为论文自报、取自摘要；本文没有复现任何实验，也没有通读多数论文的全文。
- **收录统计可能偏低**：清单的统计只看 README 里的 arXiv 链接，把条目放在网站数据里的清单会被低估；11 月 1–2 日提交的论文大多还没被清单收录。
- **快照**：星数、提交数是 2026-11-02 的数据，会变化。GitHub 搜索不是穷举，新建不久、星数为 0 的仓库可能遗漏。
