# OpenThoughts：推理模型的数据配方

中文 | [English](./OpenThoughts-Data-Recipes-for-Reasoning-Models_en.md)

- **原文链接**: [OpenThoughts: Data Recipes for Reasoning Models](https://arxiv.org/abs/2506.04178v2)
- **论文**: [arXiv:2506.04178](https://arxiv.org/abs/2506.04178)
- **发布日期**: 2025-06-04
- **译注**: “主要结论”是为本笔记写的摘要，不属于原文，数字均取自论文；“全文翻译”是 arXiv v2 版的非官方全文中译，含正文、附录、全部图表和参考文献。原文以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可发布，本译文沿用同一许可，格式上的改动列在“全文翻译”一节的开头。英文版的“主要结论”译自中文摘要，其余是原文转成的 Markdown。

## 主要结论

- **问题**：推理模型进步很快，但最先进的模型往往依赖几乎不公开任何信息的专有数据集，推理训练的最佳配方仍有许多悬而未决的问题。OpenThoughts 项目的目标是做出用于训练推理模型的开源数据集；此前发布的 OpenThoughts2-1M 训练出的 OpenThinker2-32B，是第一个用公开推理数据训练、在 AIME 和 LiveCodeBench 等标准推理基准上达到 DeepSeek-R1-Distill-32B 水平的模型。
- **方法**：把推理 SFT 数据的构建拆成六步流水线（问题来源、问题混合、问题过滤、去重与每题多次采样、答案过滤、教师模型选择），共做了 1,000 多次受控实验。每一步单独消融，其余步骤保持不变：每种策略生成 31,600 条数据，微调 Qwen2.5-7B-Instruct，按 8 个数学、代码和科学基准的平均分选出最优策略，再进入下一步。AIME 2025、HMMT 02/25、HLE 的多选题子集和 LiveCodeBench 06/24-01/25 作为留出基准，流水线实验结束后才评测。
- **结果**：把各步的最优策略扩大到 1.2M 条样本（850,000 条数学、250,000 条代码、100,000 条科学），以 QwQ-32B 为教师，得到 OpenThoughts3-1.2M；在其上微调 Qwen2.5-7B-Instruct 得到 OpenThinker3-7B。按表 1，它在 AIME 2025、LiveCodeBench 06/24-01/25 和 GPQA Diamond 上分别得到 53.3、51.7 和 53.7，比 DeepSeek-R1-Distill-Qwen-7B 高 15.3、17.2 和 20.5 个百分点；12 项任务的平均分为 55.3，比 R1-Distill-7B 高 12.4 分，比次优的开放数据模型 Nemotron-Nano-8B 高 2.1 分，是 7B 规模上最好的开放数据推理模型。
- **每题多次采样是有效的扩量手段**：让教师模型为每个问题采样多个答案，能把一个数据源的规模扩大至少 16 倍，规模扩大带来显著收益。在代码和科学上，去重方式与采样次数的各种组合结果相近；数学上精确去重加每题 4 个答案最好，16 个答案次之。最终流水线对所有领域都每题采样 16 个答案，数学和科学做精确去重，代码不去重。论文据此认为，至少在答案多样性提高时，问题多样性的收益可能有限。
- **更强的模型不一定是更好的教师**：QwQ-32B 在目标推理基准上的分数低于 DeepSeek-R1（DeepSeek-R1 在 CodeElo、GPQA Diamond 和 JEEBench 上分别高出 9%、8% 和 23%），作为教师却在所有领域都更好：与用 DeepSeek-R1 作教师相比，代码和数学数据的平均准确率分别高 1.9% 和 2.6%。
- **问题来源重质量、轻多样性**：不同来源之间差距很大，最强和最弱的代码数据集相差 17.2 分；简单的合成方法与更复杂或人工整理的流水线不相上下，有时还更好。只用排名前 1 或 2 的高质量来源，好过混合 8 个或 16 个来源：只用两个最好的代码来源，比混合 16 个来源在所有基准上的平均准确率高 5%。
- **按 LLM 的判断筛问题**：最好的两种问题过滤方法，一是让 LLM（GPT-4o-mini）评估难度、保留最难的题，在代码上最好；二是让 LLM 直接作答、保留回答最长的题，在数学和科学上最好（最终用 GPT-4.1-mini）。与随机过滤相比，数学和代码的平均分分别提高 4% 和 6%。在所有领域，基于 LLM 的过滤都好过 fastText 和 embedding 这类预训练数据常用的过滤方法。
- **答案过滤没有带来收益**：试过的验证和答案过滤方法（如 GPT 验证、多数一致、按长度或语言筛选）都没有明显提升。数学上，随机过滤基线胜过其他所有过滤方法；在所有领域，不过滤（使用全部样本，不控制计算量）与各种过滤方法表现相近，所以最终流水线不做答案过滤。
- **附录里的其他发现**：从推理轨迹中删去“wait”“but wait”这类自我反思，平均长度从 11,593 降到 328 个 token，下游平均性能相对下降 49.1%；只保留不超过 2,048 个 token 的样本，也会相对下降 33.3%，说明长推理和自我反思都不可少（附录 H.3）。Llama-3.1-8B-Instruct 用 100K 条 OpenThoughts3 样本微调后也大幅提升，如 AMC23 从 15.8 升到 75.2，但整体仍不如 Qwen2.5-7B-Instruct（附录 G.1）。在一项法律推理任务上，用 R1 标注、只靠多数投票验证（不用专家标签）的数据微调 Qwen2.5-7B，准确率达到 0.819，超过 R1 本身的 0.739（附录 J）。蒸馏出的推理模型在只改动题目细节、不改变题目结构的 AIW 变体上表现波动很大，泛化仍有缺陷（附录 N）。
- **代价与局限**：推理 SFT 削弱了 Qwen2.5 原有的安全对齐：Harmbench 上的有害率从 Qwen2.5-7B-Instruct 的 14.5 升到 OpenThinker3-7B 的 55.5，后者没有经过任何专门的安全调优，也没有用以对齐为目标的数据训练（附录 L）。论文没有探索强化学习数据集，也没有尝试分阶段 SFT 或课程学习。

## 全文翻译

**格式改动**：原文的各级标题都降了一级，放在本节之下；图片取自 arXiv 源文件（矢量图渲染为 PNG），标题处的 logo 未收录；表 1、表 31 中的 logo 换成文字，开放数据图标换成 🟢🔴🟡，竖线分隔列显示为 ‖；表中灰色下标的标准误写成“± 值”；合并单元格和旋转表头改为普通 Markdown 表格，Takeaway 框改为引用块，交叉引用改为纯文本；arXiv HTML 版的每个提示词框（图 16–37）都漏掉了第一行，这里按 arXiv 源文件补上，与 PDF 一致。中文版把提示词逐行译成了中文，模板变量和代码保持原样（代码注释译出），固定的输出字段（如 QUESTION:、SOLUTION:）和要求模型原样输出的字符串保留英文；提示词里引用的外部材料保留英文，包括图 22 和图 24 的示例原文、图 28 的正负例题，以及图 29 的 AoPS 难度标准和例题。图 15 的网页示例、参考文献，以及模型和数据集名称也保留英文。

Etash Guha\*$`^{1,2}`$, Ryan Marten\*$`^{3}`$, Sedrick Keh\*$`^{4}`$, Negin Raoof\*$`^{5}`$, Georgios Smyrnis\*$`^{6}`$, Hritik Bansal$`^{\zeta 7}`$, Marianna Nezhurina$`^{\zeta 8,9,16}`$, Jean Mercat$`^{\zeta 4}`$, Trung Vu$`^{\zeta 3}`$, Zayne Sprague$`^{\zeta 6}`$, Ashima Suvarna$`^{7}`$, Benjamin Feuer$`^{10}`$, Liangyu Chen$`^{1}`$, Zaid Khan$`^{11}`$, Eric Frankel$`^{2}`$, Sachin Grover$`^{12}`$, Caroline Choi$`^{1}`$, Niklas Muennighoff$`^{1}`$, Shiye Su$`^{1}`$, Wanjia Zhao$`^{1}`$, John Yang$`^{1}`$, Shreyas Pimpalgaonkar$`^{3}`$, Kartik Sharma$`^{3}`$, Charlie Cheng-Jie Ji$`^{3}`$, Yichuan Deng$`^{2}`$, Sarah Pratt$`^{2}`$, Vivek Ramanujan$`^{2}`$, Jon Saad-Falcon$`^{1}`$, Jeffrey Li$`^{2}`$, Achal Dave, Alon Albalak$`^{13}`$, Kushal Arora$`^{4}`$, Blake Wulfe$`^{4}`$, Chinmay Hegde$`^{10}`$, Greg Durrett$`^{6}`$, Sewoong Oh$`^{2}`$, Mohit Bansal$`^{11}`$, Saadia Gabriel$`^{7}`$, Aditya Grover$`^{7}`$, Kai-Wei Chang$`^{7}`$, Vaishaal Shankar, Aaron Gokaslan$`^{14}`$, Mike A. Merrill$`^{1}`$, Tatsunori Hashimoto$`^{1}`$, Yejin Choi$`^{1}`$, Jenia Jitsev$`^{8,9,16}`$, Reinhard Heckel$`^{15}`$, Maheswaran Sathiamoorthy$`^{3}`$, Alexandros G. Dimakis$`^{\dagger 3,5}`$, Ludwig Schmidt$`^{\dagger 1}`$

$`^{1}`$Stanford University, $`^{2}`$University of Washington, $`^{3}`$BespokeLabs.ai, $`^{4}`$Toyota Research Institute, $`^{5}`$UC Berkeley, $`^{6}`$UT Austin, $`^{7}`$UCLA, $`^{8}`$JSC, $`^{9}`$LAION, $`^{10}`$NYU, $`^{11}`$UNC Chapel Hill, $`^{12}`$ASU, $`^{13}`$Lila Sciences, $`^{14}`$Cornell Tech, $`^{15}`$TUM, $`^{16}`$Open-Ψ (Open-Sci) Collective

\*、† 表示同等贡献，ζ 表示其他核心贡献者。顺序随机决定。

### 摘要

推理模型在许多涉及数学、代码和科学的基准上取得了快速进展。然而，关于推理的最佳训练配方仍存在许多悬而未决的问题，因为最先进的模型往往依赖专有数据集，而这些数据集几乎没有任何公开信息。为解决这一问题，OpenThoughts 项目的目标是创建用于训练推理模型的开源数据集。经过初步探索，我们的 OpenThoughts2-1M 数据集催生了 OpenThinker2-32B，这是首个基于公开推理数据训练、并在 AIME 和 LiveCodeBench 等标准推理基准上达到 DeepSeek-R1-Distill-32B 水平的模型。随后，我们通过 1,000+ 次受控实验，系统地研究了我们数据生成流水线的每个步骤，从而进一步改进了数据集，并由此得到了 OpenThoughts3。将该流水线扩展到 1.2M 个样本，并使用 QwQ-32B 作为教师模型，我们得到了 OpenThinker3-7B 模型，它取得了最先进的结果：在 AIME 2025 上达到 **53%**，在 LiveCodeBench 06/24-01/25 上达到 **51%**，在 GPQA Diamond 上达到 **54%**——与 DeepSeek-R1-Distill-Qwen-7B 相比，分别提升了 15.3、17.2 和 20.5 个百分点。我们所有的数据集和模型均可在 [openthoughts.ai](https://openthoughts.ai) 上获取。

![图 1](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig01.png)

*图 1：**OpenThoughts3 在各个数据规模上都优于现有的 SFT 推理数据集**。所有模型均基于 Qwen-2.5-7B-Instruct 微调。我们在 AIME 2025（左）、LiveCodeBench 06/24-01/25（中）和 GPQA Diamond（右）上，与大型 SFT 数据集（AM、Nemotron Nano）以及精心构建的小型数据集（s1.1、LIMO）进行了比较。所有评估基准的扩展曲线见图 8。*

### 1 引言

近期的模型，如 DeepSeek-R1 (Guo et al., 2025) 和 o3 (OpenAI, 2024)，已在基于推理的领域（包括数学、编程和科学）中展现出强大的性能。这些模型通常以一个强大的基座模型为起点，再通过监督微调（SFT）或强化学习（RL）等一系列后训练技术引入推理能力。这一后训练过程使这些模型具备在推理阶段输出长思维链（或称“思考 token”）的能力，这些思维链能够引导模型得出正确答案。然而，前沿推理模型的完整配方并未公开，这使得构建推理模型的研究变得困难。

| | 基准 | **OpenThoughts3-7B** | DS-R1-Qwen-7B | NemoNano-1M | AM-1.4M | OpenR1-Distill-7B | SFT vs. RL | Nemotron-Nano-8B | AceReason-7B | Skywork-7B | 基座模型 | Qwen2.5-7B-Instruct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 基座模型 | Qwen | Qwen-M | Qwen | Qwen | Qwen-M | ‖ | Llama | R1-Distill | R1-Distill | ‖ | N/A |
| | 训练集规模 | 1.2M | 800K | 1M | 1.4M | 350K | ‖ | 3.9M | 57K | 119K | ‖ | N/A |
| | 方法 | SFT | SFT | SFT | SFT | SFT | ‖ | SFT/RL | RL | RL | ‖ | N/A |
| | 由我们训练 | 是 | 否 | 是 | 是 | 否 | ‖ | 否 | 否 | 否 | ‖ | N/A |
| | 开放数据 | 🟢 | 🔴 | 🟢 | 🟢 | 🟢 | ‖ | 🟢 | 🟡 | 🟡 | ‖ | N/A |
| | 平均 | **55.3** | 42.9 | 47.3 | 42.1 | 47.2 | ‖ | 53.2 | 52.9 | 51.6 | ‖ | 24.0 |
| *数学* | AIME24 | **69.0** | 51.3 | 55.0 | 28.3 | 57.7 | ‖ | 62.0 | **71.0** | **68.3** | ‖ | 15.0 |
| | AMC23 | **93.5** | 92.0 | 87.0 | 82.2 | 87.0 | ‖ | **94.0** | **93.8** | 91.0 | ‖ | 53.0 |
| | MATH500 | 90.0 | 88.0 | 86.8 | 87.4 | 88.0 | ‖ | 89.4 | 89.8 | **90.2** | ‖ | 70.8 |
| *代码* | CodeElo | 31.0 | 19.9 | 28.6 | 21.0 | 30.1 | ‖ | 30.9 | 32.9 | **37.0** | ‖ | 5.5 |
| | LCB 05/23-05/24 | 64.5 | 48.7 | 58.0 | 54.5 | 37.9 | ‖ | **68.0** | 60.5 | 60.4 | ‖ | 36.2 |
| | CodeForces | **32.2** | 21.1 | 28.3 | 24.8 | 29.3 | ‖ | **32.9** | **30.9** | **32.5** | ‖ | 10.2 |
| *科学* | GPQA-D | 53.7 | 33.2 | 52.9 | 48.3 | **58.9** | ‖ | 52.9 | 52.9 | 50.2 | ‖ | 24.6 |
| | JEEBench | **72.4** | 50.4 | 61.0 | 61.1 | 68.7 | ‖ | 70.7 | 64.3 | 55.3 | ‖ | 33.9 |
| *留出* | HMMT 02/25 | **42.7** | 25.0 | 24.7 | 19.0 | 25.7 | ‖ | 26.7 | 33.3 | 32.7 | ‖ | 2.0 |
| | HLE 选择题 | 10.2 | 12.4 | 2.1 | 9.5 | 12.4 | ‖ | 12.0 | 10.9 | 10.7 | ‖ | **12.7** |
| | AIME25 | **53.3** | 38.0 | 41.3 | 28.7 | 39.7 | ‖ | 48.0 | 50.7 | 47.3 | ‖ | 8.0 |
| | LCB 06/24-01/25 | **51.7** | 34.5 | 42.2 | 40.3 | 30.7 | ‖ | **50.9** | 44.3 | 43.8 | ‖ | 16.3 |

*表 1：**OpenThinker3-7B 在各领域均优于所有开放数据的 7B 和 8B 推理模型**。我们的模型在主要实验期间未作测量的留出基准（如 HMMT 和 AIME25）上同样表现良好。表中，Qwen 表示以 Qwen-2.5-7B-Instruct 为起点训练的模型，Qwen-M 对应 Qwen-2.5-Math-Base，Llama 对应 Llama-3.1-8B-Instruct，R1-Distill 对应 DeepSeek-R1-Distill-Qwen-7B。“基座模型”表示训练策略的起始检查点。“方法”表示模型的优化算法。在每一行中，我们将与得分最高的模型相差在两个标准误以内的数值加粗。*

在 SFT 数据构建上进行创新是打造推理模型的一种强有力的方法 (Abdin et al., 2024; Lin et al., 2024)。例如，R1-Distill 系列模型表明，无需任何 RL 步骤，就有可能得到最先进的中小规模推理模型（在 AIME 上达到 51%，在 GPQA 上达到 33%），而这仅基于在一个大规模、精心构建的“问题-思考 token-答案”三元组数据集上进行的监督微调，其中思考 token 和答案由一个推理教师模型生成。现有工作，如 SkyT1 (NovaSky-Team, 2025b) 和 S1 (Muennighoff et al., 2025)，采用了与典型指令微调几乎相同的模型架构和训练设置，却仍通过专注于改进训练数据集实现了性能提升。这些例子凸显了构建高质量 SFT 数据的重要性：它是撬动推理性能的一个关键杠杆。

然而，这些项目大多只探索了可能的设计选择中的一小部分，例如依赖人工编写的问题，或使用 DeepSeek-R1 作为唯一的教师模型。复现推理模型需要在一个庞大的设计空间中探索生成推理问答对的各种策略 (Face, 2025)。由于教师模型推理和模型训练的成本高昂，这种探索对许多研究者而言代价过高，难以承受。在缺乏这些昂贵实验的情况下，许多论文依赖已有的启发式方法和直觉来指导其数据设计选择。

OpenThoughts 项目的目标是揭开 SFT 数据构建过程的神秘面纱，更深入地理解哪些因素造就了强大的推理 SFT 数据集，从而挑战关于数据质量的既有观念。为实现这一目标，OpenThoughts-114K 研究了结合自动验证来扩展 Sky-T1 流水线 (NovaSky-Team, 2025b) 如何提升下游性能。OpenThoughts2-1M 在这些收益的基础上，通过增强问题多样性（包括采用合成问题生成策略）扩大了数据规模。

为了在 OpenThoughts2-1M 的基础上进一步改进，我们对用于提升推理能力的数据构建技术开展了实证研究。通过在三个数据领域（数学、代码和科学）上进行的超过 **1,000** 次消融实验，我们开发出一条简单、可扩展且性能优异的流水线，如图 2 所示。我们扩大该流水线的规模，产出了 **OpenThoughts3-1.2M**，并在其上微调 Qwen2.5-7B-Instruct，得到 **OpenThinker3-7B**。如表 1 所示，由此得到的 OpenThinker3-7B 在多个推理基准上是 7B 规模下最先进的开放数据模型，在 12 项任务上平均比 R1-Distill-7B 模型高出 12.4 分，并比次优的开放数据模型（Nemotron-Nano-8B）高出 2.1 分。我们向社区发布了我们的模型和数据成果，并分享了本研究中的若干关键发现。我们的部分洞见包括：

1. 从教师模型为每个问题采样多个答案是一种有效的技术，可将数据源的规模扩大至少 16×。数据集规模的增大带来了显著的性能提升。
2. 性能更好的模型不一定是更好的教师模型。QwQ-32B 是比 DeepSeek-R1 更强的教师模型，尽管它在目标推理基准上的得分更低。
3. 我们尝试了大量验证和答案过滤方法，但没有一种带来显著的性能提升。
4. 从少数（排名前 1 或 2 的）高质量来源中选择问题，相比以多样性为优化目标（即使用排名前 8 或 16 的来源），能带来更好的下游性能。
5. 按 LLM 标注的难度或 LLM 回答长度来过滤问题，能取得比预训练数据构建中典型的、使用嵌入或 `fastText` 的过滤器更好的结果。

### 2 相关工作

Gemini (Gemini-Team et al., 2023)、QwQ (Qwen-Team, 2025) 和 DeepSeek-R1 (Guo et al., 2025) 等模型让用户能够看到长推理轨迹，它们的发布开启了通过蒸馏更大模型的推理轨迹来训练小模型的可能性。DeepSeek 在发布 DeepSeek-R1 的同时，还发布了强大的蒸馏模型（例如 DeepSeek-R1-Distill-Qwen-7B），展示了这一策略的巨大潜力。此后，许多开放数据工作尝试复现这些模型，通过从 QwQ-32B (NovaSky-Team, 2025b) 或 DeepSeek-R1 (Bespoke-Labs, 2025) 等教师模型进行蒸馏来构建 SFT 推理数据集。

许多数据集面向数学、代码和科学领域，以培养推理能力。OpenR1(Face, 2025)、OpenMathReasoning (Moshkov et al., 2025) 和 OpenCodeReasoning (Ahmad et al., 2025) 等数据集从 CodeForces、AoPS 和 StackOverflow 等公共论坛和竞赛网站收集问题，而 Natural Reasoning (Yuan et al., 2025) 等其他数据集则使用大型预训练语料库作为种子数据来生成推理轨迹。S1 (Muennighoff et al., 2025) 和 LIMO (Ye et al., 2025) 等工作侧重于人工构建由具有挑战性的高质量提示词组成的小型（约 1K 个样本）数据集。

在实践中，许多推理项目（例如 DeepMath-103K (He et al., 2025b)、OpenR1 (Face, 2025) 和 Nvidia Nemotron (Adler et al., 2024)）在数据来源、过滤和扩展等多个阶段引入了创新。在 SFT 之外，AceReason (Chen et al., 2025) 和 Skywork-OR1 (He et al., 2025a) 等工作构建了用于强化学习的推理数据集。

### 3 OpenThoughts 项目

我们发起 OpenThoughts 项目，旨在通过探索推理 SFT 数据集中丰富的设计空间来创建最先进的开放推理数据集，并特别关注如何找出能够激发推理的最佳问题及其对应答案。从 BespokeStratos-17K (Bespoke-Labs, 2025) 开始，我们已历经四代发布，最终推出了 OpenThoughts3-1.2M 和 OpenThinker3-7B。我们通过 [openthoughts.ai](https://openthoughts.ai) 与社区共享开放成果。

| 模型 | AIME24 | AIME25 | GPQA-D | LCB 05/23-05/24 |
| --- | --- | --- | --- | --- |
| Bespoke-Stratos-7B | 14.3 | 12.7 | 31.8 | 27.4 |
| OpenThinker-7B | 29.3 | 25.3 | 44.1 | 38.8 |
| OpenThinker2-7B | 60.7 | 38.7 | 47.0 | 56.3 |
| OpenThinker3-7B | **69.0** | **53.3** | **53.7** | **64.5** |

*表 2：**OpenThinker 模型的演进**。一代又一代的数据配方在各个领域上持续提升了性能。关于 BespokeStratos-17K、OpenThoughts-114K 和 OpenThoughts2-1M 的更多细节见附录 C。*

**OpenThoughts-114K** (OpenThoughts-Team, 2025) 证明了扩展强大的数据集生成策略的有效性。我们以 BespokeStratos-17K 为起点，从与 SkyT1 数据流水线 (NovaSky-Team, 2025b) 相同的问题来源中采样更多问题来扩大其规模，这些来源包括 TACO (Li et al., 2023b)、Apps (Hendrycks et al., 2021a)、CodeContests (Li et al., 2022) 等。该数据集包含 114K 个问题，涵盖数学（89K）、代码（20K）、科学（4K）和谜题（1K），其回答蒸馏自 DeepSeek-R1。我们的工具利用答案匹配和单元测试来验证数学和代码回答，过滤掉答案错误的推理轨迹。

**OpenThoughts2-1M** (OpenThoughts-Team, 2025) 是我们首次扩展到 1M 行规模的尝试，纳入了 AutoMathText (Zhang et al., 2024)、OpenR1 (Face, 2025) 和 CodeFeedback (Chaudhary, 2023) 等新的问题来源。由此得到的数据集训练出了一个可与 R1-Distill-32B 相媲美的最先进模型，该模型在 AIME25 上甚至比后者高出 6% (Guo et al., 2025)。OpenThoughts2-1M 数据集利用了来自 OpenR1-Math (Face, 2025) 的 600K 个经过验证的样本，以及来自更广泛的数学和代码问题来源的 200K 个未经验证的样本。我们通过遍历 26 个问题来源并从表现最好的来源中采样，选出了这些来源。

**OpenThoughts3-1.2M** 是本文的重点，它是我们从此前各版 OpenThoughts 数据集以及对数据集流水线设计空间的系统性探索（第 4 节）中所获洞见的集大成者。下一节将详细介绍该流水线以及最终数据集的构成。

### 4 OpenThoughts3 数据流水线

![图 2](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig02.png)

*图 2：**OpenThoughts 实验流水线旨在构建最强的推理数据集配方**。我们研究了：（1）从现有数据集和新生成的数据集中获取问题；（2）混合来自表现最佳来源的问题；（3）使用 `fastText` 或 LLM 过滤出高质量问题；（4）对问题去重并为每个问题采样多个答案；（5）使用 LLM 验证或多数一致过滤掉低质量答案；以及（6）选择最佳教师模型。*

本节介绍我们用于构建 OpenThoughts3-1.2M 的实验流水线。我们首先概述用于以受控方式比较各种数据策略的训练和评估设置。这些实验对流水线的每个步骤分别进行独立的消融，我们再根据下游性能选出表现最佳的策略。第 4.1 节至第 4.6 节详细描述了流水线的各个阶段。

**训练**。我们的目标是为 SFT 推理创建由问题-回答对组成的最佳数据集。最佳数据集就是能训练出性能最高的模型的数据集。为了系统地实现这一目标，我们逐一对流水线的每个步骤进行消融，在保持流水线其余部分不变的同时，隔离出给定策略的效果。在每个实验中，我们使用完整的流水线为每种数据策略生成 31,600 个数据点，并在每个数据集上微调 Qwen2.5-7B-Instruct (Qwen2.5-Team, 2024)。我们的实验所采用的数据集规模既足够小，具有成本效益，又足够大，能够提供有意义的信号。我们选择 31,600 作为 10K 与 100K 之间的对数尺度中点，因为 √10 ≈ 3.16。这些实验为最终 OpenThoughts3 流水线的设计选择提供了依据。附录 D 包含超参数和训练设置的详细信息。

**评估设置**。我们在一组包含数学、代码和科学问题的推理基准上评估我们的模型。按领域划分，这些基准为：数学方面有 AIME24 (MAA, 2024)、AMC23 (MAA, 2023) 和 MATH500 (Hendrycks et al., 2021b)；代码方面有 CodeElo (Quan et al., 2025)、CodeForces (Penedo et al., 2025) 和 LiveCodeBench 05/23-05/24 (Jain et al., 2024)；科学方面有 GPQA Diamond (Rein et al., 2024) 和 JEEBench (Arora et al., 2023)。我们根据每个模型在这八项任务上的平均表现为其评分。Evalchemy (Raoof et al., 2025) 是我们的主要评估工具，我们对每个基准都使用其提供的默认设置。关于评估设置的更多细节见附录 E。我们还通过移除高相似度的样本，针对我们的基准对数据集进行去污染。该过程的细节见附录 F。为了衡量泛化能力，我们的流水线实验排除了一组留出基准，这些基准仅在流水线实验全部结束后才进行测量。这组留出基准包括 AIME 2025 (MAA, 2025)、HMMT 02/25 (Balunović et al., 2025)、Humanity’s Last Exam（多项选择题子集）(Phan et al., 2025) 和 LiveCodeBench 06/24-01/25 (Jain et al., 2024)。

**流水线**。在每个流水线步骤中，我们根据所有领域的平均基准得分选出表现最佳的方法，然后基于这一选择进入流水线实验的下一步。除非另有说明，答案均以 DeepSeek-R1 作为教师模型生成。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 代码问题来源 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| StackExchange-CodeGolf\* | **38.8 ± 0.4** | 25.3 ± 0.6 | **50.9 ± 1.1** | 40.7 ± 0.5 |
| OpenCodeReasoning | **38.4 ± 0.3** | **27.5 ± 0.4** | 47.9 ± 0.7 | 40.7 ± 0.6 |
| KodCode-V1 | 37.7 ± 0.3 | 23.9 ± 0.4 | **49.8 ± 0.7** | 40.4 ± 0.3 |
| … | … | … | … | … |
| bugdaryan/sql-create-… | 21.6 ± 0.6 | 7.0 ± 0.7 | 34.1 ± 1.4 | 24.7 ± 0.9 |
| 数学问题来源 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| OpenMath-2-Math | **38.1 ± 0.3** | **12.4 ± 0.2** | **58.8 ± 1.0** | **45.6 ± 0.2** |
| NuminaMath-1.5 | 37.4 ± 0.5 | 11.4 ± 0.5 | **58.5 ± 1.0** | **45.0 ± 1.2** |
| MathPile\* | 36.2 ± 0.5 | 11.5 ± 0.7 | 55.1 ± 0.9 | 44.6 ± 1.1 |
| … | … | … | … | … |
| Lap1official/Math\* | 24.4 ± 0.3 | 7.3 ± 0.3 | 38.6 ± 1.0 | 28.5 ± 0.3 |
| 科学问题来源 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| StackExchange-Physics\* | **34.3 ± 0.4** | **11.9 ± 0.5** | **50.9 ± 0.8** | 43.2 ± 0.7 |
| OrganicChemistry-PDF\* | **34.0 ± 0.3** | 8.4 ± 0.3 | **52.1 ± 0.7** | **45.3 ± 0.8** |
| CQADupStack-Physics | 33.3 ± 0.4 | 7.4 ± 0.3 | **51.9 ± 1.1** | **44.1 ± 0.9** |
| … | … | … | … | … |
| AdapterOcean/biology\_dataset… | 21.9 ± 0.4 | 3.1 ± 0.3 | 41.3 ± 1.1 | 21.1 ± 0.8 |

*表 3：**评估问题来源和生成策略**。我们仅展示每个领域得分前 3 的来源；各来源的说明见第 R.1 节，完整结果见表 32、33 和 34。每一行代表一个不同的问题来源。问题质量对性能影响很大，使最强与最弱的代码数据集之间产生了 17.2 的差距。符号 \* 表示我们采用程序化生成策略创建的新数据集。灰色下标表示标准误，我们将与得分最高的数据策略相差在两个标准误以内的数值加粗。*

#### 4.1 问题来源

我们数据生成流水线的第一步，是为每个数据领域寻找问题。我们可以将问题来源技术大致分为三类：（1）完全合成——由现有 LLM 在很少甚至没有种子材料的情况下生成问题。例子包括 CodeAlpaca (Chaudhary, 2023) 和 CamelChemistry (Li et al., 2023a)。这类方法通常是用模板提示 LLM 生成多个问题。（2）半合成——LLM 以 CommonCrawl 或 FineWeb (Penedo et al., 2024a) 等现有数据源为种子来构造问题。例子包括 TigerLabMath (Yue et al., 2024) 和 AutoMathText (Zhang et al., 2024)。（3）非合成——由人类编写问题。例子包括 StackExchange 和 ShareGPTCode。这些问题通常来自在线论坛、竞赛、聊天机器人交互以及其他来源。

我们的实验涵盖 27 个不同的代码问题来源、21 个数学问题来源和 14 个科学问题来源。这些来源的详细说明见第 R.1 节。我们消融实验的第一步，是使用每个来源各生成 31,600 个问题。对于产生的数据点较少的来源，我们会重复其中的问题，直到达到所需数量。对于所有由我们生成且需要 LLM 的来源，我们都使用 GPT-4o-mini。最后，我们使用 DeepSeek-R1 为每个问题生成回答，即使该问题已有现成的答案。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 代码问题混合策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 前 1 个代码来源 | 39.9 ± 0.6 | 23.1 ± 1.0 | **54.5 ± 0.8** | **43.1 ± 1.2** |
| 前 2 个代码来源 | **41.3 ± 0.4** | **27.3 ± 0.3** | **54.7 ± 0.9** | **42.1 ± 1.0** |
| 前 4 个代码来源 | 38.6 ± 0.4 | 24.2 ± 0.6 | 52.2 ± 0.8 | 39.8 ± 0.9 |
| 前 8 个代码来源 | 37.0 ± 0.4 | 21.8 ± 0.3 | 51.9 ± 1.2 | 37.7 ± 0.6 |
| 前 16 个代码来源 | 36.4 ± 0.4 | 20.8 ± 0.4 | 50.1 ± 0.9 | 39.1 ± 1.0 |

*表 4：**混合不同的代码问题来源**。我们的实验表明，仅选择两个最佳问题来源的效果优于混合更多问题来源。科学和数学数据领域也有类似的结果。包括数学和科学数据集在内的完整结果见表 35、36 和 37。*

实验结果见表 3。在代码方面，来自 StackExchange 的 CodeGolf 问题和来自 OpenCodeReasoning (Ahmad et al., 2025) 的竞赛编程问题表现良好，在代码基准上的平均得分分别为 25.3 和 27.5。在数学方面，openmath-2-math (Toshniwal et al., 2024) 中由 LLM 生成的问题和 NuminaMath (LI et al., 2024) 中由人类编写的问题均得分最高，在各数学基准上的平均得分分别为 58.8 和 58.5。最后，在科学方面，得分最高的问题生成策略是来自 StackExchange 的物理问题和由 LLM 从有机化学教科书中提取的问题，它们在科学基准上的平均得分分别为 43.2 和 45.3。各问题生成策略之间没有呈现出明显的规律——简单的合成方法与更复杂的或人工构建的流水线表现相当，有时甚至更好。这些表现最好的问题来源为流水线的后续阶段奠定了基础。

#### 4.2 问题混合

从各种问题来源中获得高质量问题之后，接下来的挑战是如何有效地组合它们——我们应该依赖单一的表现最佳的策略，还是融合多个表现强劲的策略，以最大化下游性能？这种混合策略是许多生成流水线中的关键设计选择 (Yue et al., 2024; Moshkov et al., 2025; Lambert et al., 2024)。直观上，向混合中加入更多问题来源，会带来纳入较低质量策略的风险，以此换取更高的多样性。我们的实验旨在评估，额外的问题多样性是否值得在问题质量上做出这种权衡。

为简单起见，我们将流水线上一步（第 4.1 节）的排名作为选择候选数据集的启发式依据。我们的混合策略选取排名前 N 的数据集，从每个来源中随机采样 31,600/N 个问题，并将它们拼接成规模为 31,600 的数据集。我们对 N ∈ {1, 2, 4, 8, 16} 的取值进行了扫描。代码领域的结果见表 4，而其他结果见第 S.2 节。我们的实验表明，混合大量问题来源会降低性能：在所有数据领域中，至多混合两个来源时结果最好。使用两个高质量的代码问题来源而非 16 种策略，可使所有基准上的平均准确率提高 5%。这一结果表明，下游性能受益于源数据质量的提升，而非混合多个问题来源所带来的多样性。

> **要点：** 我们使用 OpenMath-2-Math 作为唯一的数学问题来源，使用 CodeGolf 和 OpenCodeReasoning 作为代码问题来源，并使用 StackExchangePhysics 和 OrganicChemistry-PDFs 作为科学问题来源。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 数学问题过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 基于回答长度的选择（GPT-4.1-mini） | **41.9 ± 0.3** | **13.4 ± 0.3** | **66.0 ± 0.8** | **48.6 ± 0.4** |
| 基于回答长度的选择（GPT-4.1-nano） | 39.4 ± 0.3 | 11.0 ± 0.4 | **64.5 ± 0.7** | 44.3 ± 0.7 |
| AskLLM 选择 | 36.3 ± 0.4 | 9.5 ± 0.5 | 58.1 ± 1.1 | 43.8 ± 0.6 |
| FastText（正例：Numina；负例：Lap1official） | 35.6 ± 0.4 | 11.0 ± 0.2 | 54.9 ± 1.1 | 43.5 ± 0.8 |
| … | … | … | … | … |
| 代码问题过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 基于难度的选择 | **43.0 ± 0.5** | 27.7 ± 0.4 | **56.0 ± 1.3** | **46.4 ± 0.7** |
| 基于回答长度的选择（GPT-4.1-nano） | **42.2 ± 0.4** | 26.6 ± 0.5 | **55.4 ± 1.3** | **46.0 ± 0.2** |
| AskLLM 选择 | 41.6 ± 0.5 | **28.8 ± 0.5** | 52.1 ± 1.2 | **45.2 ± 0.8** |
| 基于回答长度的选择（GPT-4o-mini） | 40.8 ± 0.5 | 25.6 ± 0.5 | 53.1 ± 0.9 | **45.2 ± 1.1** |
| … | … | … | … | … |

*表 5：**问题过滤为提取高质量问题提供了一种有效工具**。使用基于 LLM 的方法从问题来源中找出最佳问题，效果优于 `fastText` 和基于嵌入的过滤器等经典过滤方法。本表展示了表现最好的策略。包括科学数据集在内的完整结果列于表 38、39 和 40。*

#### 4.3 问题过滤

由于每个数据源可能包含数百万个潜在问题，为每个可能的问题都生成回答并在其上训练，成本高得不可行。因此，下一步是从每个来源中选出一个高质量的问题子集。在已有文献中，各种各样的过滤策略都一致地提升了数据集的整体质量 (Soldaini et al., 2024; Su et al., 2024; Li et al., 2024; Wettig et al., 2025; Penedo et al., 2024a; Gao et al., 2020; Shum et al., 2025)。我们以第 4.2 节中的最佳问题来源为起点，广泛探索了各种过滤方法来选出更高质量的问题，包括 `fastText` 分类器、难度评分和嵌入距离。这些过滤方法的详细描述见第 R.2 节。这些实验在数学和代码上的结果列于表 5，而科学领域的结果见第 S.3 节（表 40）。

表现最好的两种问题过滤方法是基于难度的过滤和回答长度过滤。基于难度的过滤让一个 LLM（GPT-4o-mini）评估每个问题的难度，然后保留最难的问题。基于难度的过滤是代码领域的最佳策略。与此同时，回答长度过滤让 LLM 直接回答每个问题，然后选出 LLM 生成的回答最长的那些问题。回答长度过滤在数学和科学领域表现最好。在数学和代码领域，使用最佳问题过滤策略相比随机过滤基线，平均分别提升了 4% 和 6%。我们在回答长度过滤中测试了 GPT-4o-mini 和 GPT-4.1-nano 等不同的 LLM，发现使用更强的模型进行回答长度过滤，通常优于使用较弱的模型。在所有领域中，使用基于 LLM 的过滤方法都优于基于嵌入的过滤器和 `fastText` 过滤器等经典过滤方法。

> **要点：** 对于代码问题，我们使用 GPT-4o-mini 进行基于难度的过滤；对于数学和科学问题，我们使用 GPT-4.1-mini 进行回答长度过滤。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 科学答案生成策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 精确去重 + 16× 采样 | **36.2 ± 0.5** | 9.0 ± 0.4 | **54.5 ± 1.0** | 49.7 ± 1.2 |
| 模糊去重 + 16× 采样 | **36.1 ± 0.4** | **10.9 ± 0.2** | 52.9 ± 1.3 | 48.8 ± 0.5 |
| 精确去重 + 4× 采样 | **35.8 ± 0.5** | **10.6 ± 0.7** | 51.8 ± 1.0 | 49.6 ± 1.2 |
| 不去重 + 4× 采样 | **35.8 ± 0.4** | 10.0 ± 0.4 | **55.2 ± 0.8** | 45.4 ± 0.9 |
| 不去重 + 16× 采样 | **35.7 ± 0.4** | 7.6 ± 0.5 | **53.8 ± 1.0** | **50.9 ± 0.5** |
| 不去重 + 1× 采样 | **35.5 ± 0.3** | 9.3 ± 0.3 | **54.2 ± 1.1** | 46.9 ± 0.2 |
| 精确去重 + 1× 采样 | 35.0 ± 0.4 | 7.6 ± 0.4 | **54.0 ± 1.2** | 47.5 ± 0.5 |
| 模糊去重 + 4× 采样 | 34.9 ± 0.4 | 7.4 ± 0.5 | **55.0 ± 1.0** | 46.0 ± 0.7 |
| 模糊去重 + 1× 采样 | 34.2 ± 0.3 | 5.8 ± 0.4 | 52.5 ± 0.7 | 49.5 ± 0.4 |

*表 6：**去重和对教师模型的重复采样提供了一个扩展规模的维度**。使用较少的问题并进行更多次标注，与对较多问题进行较少次标注相比，表现相近甚至更好。在哪些类型的去重能提升性能方面，似乎并没有明显的趋势。包括数学和代码数据集在内的完整结果见表 41、42 和 43。*

#### 4.4 去重与每个问题采样多个答案

去重是提升数据集质量的一种有力策略 (Li et al., 2024; Lee et al., 2022; Penedo et al., 2024b; Fang et al., 2025; Liu et al., 2024)。我们的消融实验研究了问题去重对下游推理性能的影响。我们探索了三种严格程度的去重：不去重、精确匹配去重，以及使用基于阈值的字符串相似度的模糊去重。更多细节见第 R.3 节。

去重通过减少重复来提升问题多样性；与之相对应，提升答案多样性的一种自然做法，是多次查询教师模型以引出不同的回答。这一策略以较低的问题多样性换取较高的答案多样性，并提供了扩展数据规模的另一个维度。我们探索了每个问题采样多个答案的三个水平：1×、4× 和 16×。

为了处理源数据集中天然存在的重复问题与每个问题需要多次查询教师模型这一需求之间的相互影响，我们针对每个领域扫描了去重程度（无、模糊、精确）与多答案采样（1×、4×、16×）的所有组合。这次扫描中科学领域的结果列于表 6，而数学和代码的结果见第 S.4 节（表 41 和表 42）。对于代码和科学数据，去重与多答案生成的各种组合得到的结果相近。例如，在代码领域，不去重、每个问题 1× 答案的基线，平均比精确去重、每个问题 16× 答案的方案低 0.7 分。与此同时，在数学领域，精确去重、每个问题 4× 答案的方案表现最好，每个问题 16× 答案则是次优选项。在后续步骤中我们采用次优选项，因为它具有更好的可扩展性。与第 4.2 节类似，这里的结果表明，至少在答案多样性增加时，对于我们用来衡量性能的推理数据集而言，问题多样性的益处可能有限。因此，对于数学和科学，我们选择最优策略，即精确去重、每个问题 16× 答案。对于代码，我们采用次优策略，即不去重、每个问题 16× 答案。

> **要点：** 我们的最终流水线在所有领域中都对每个问题使用 16× 答案。它对数学和科学使用精确去重，对代码则不去重。

#### 4.5 答案过滤

验证或移除低质量标注是许多推理数据流水线中的常见步骤。直观上，移除可能不正确的数据应当能提升下游性能。我们的实验探索了多种答案过滤技术。为了确保过滤后仍能得到规模为 31,600 的数据集，我们先生成 63,200 个答案，应用每种答案过滤策略，然后从过滤后的数据集中采样 31,600 个问答对。我们的消融实验还包括一个不做过滤的基线；该基线没有控制计算量，因为它包含 63,200 个问题。

| 数学答案过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| --- | --- | --- | --- | --- |
| 不过滤（未控制计算量） | **41.9 ± 0.4** | **15.2 ± 0.5** | **65.6 ± 0.9** | 46.4 ± 0.7 |
| 随机过滤 | **41.6 ± 0.4** | **14.9 ± 0.4** | **64.8 ± 0.9** | 46.7 ± 0.5 |
| 最短答案选择 | **41.1 ± 0.4** | **14.8 ± 0.4** | 63.7 ± 1.1 | 46.7 ± 0.7 |
| 移除非英语答案 | **41.1 ± 0.5** | **14.2 ± 0.5** | 63.1 ± 1.0 | **48.6 ± 1.0** |
| … | … | … | … | … |
| GPT 验证 | 40.0 ± 0.5 | 13.1 ± 0.3 | 61.4 ± 1.1 | **48.3 ± 1.1** |
| 移除长段落 | 38.0 ± 0.4 | 5.7 ± 0.2 | **64.5 ± 0.9** | 46.8 ± 1.0 |

*表 7：**过滤答案并未优于完全不过滤**。使用多数一致过滤或基于回答长度的过滤等验证技术，并未比在全部样本上训练带来提升。包括代码和科学数据集在内的完整结果见表 45、46 和 44。*

表 7 展示了各过滤方法在数学数据集上的结果，代码和科学数据集的结果见第 S.5 节。对于数学数据集，随机过滤基线优于所有其他过滤方法。对于代码问答对，`fastText` (Joulin et al., 2017) 分类器是最佳的答案过滤方法。该 `fastText` 分类器的正样本来自由 DeepSeek-R1 作答的 CodeForces (Penedo et al., 2025) 问题，负样本来自由 GPT-4o-mini 作答的 CodeForces 问题。对于科学，保留最长的前 8 个答案是最强的问答过滤策略。然而，在所有领域中，不过滤策略（在不控制计算量的情况下使用全部样本训练）带来的性能都与所有其他过滤方法相近。这一结果表明，无论在哪个领域，答案过滤的益处都不够显著，不足以证明减少数据集中的样本数量是合理的。因此，在流水线的后续步骤中，我们选择跳过这一环节。

> **要点：** 我们不进行答案过滤，因为没有任何过滤策略优于使用全部答案的基线。

#### 4.6 教师模型

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 代码教师模型 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| Qwen/QwQ-32B | **44.2 ± 0.5** | **29.5 ± 0.3** | **58.7 ± 1.1** | 44.6 ± 1.0 |
| deepseek-ai/DeepSeek-R1 | 42.3 ± 0.5 | 27.2 ± 0.5 | 54.7 ± 1.4 | **46.5 ± 0.3** |
| microsoft/Phi-4-reasoning-plus | 29.0 ± 0.4 | 0.5 ± 0.1 | 52.1 ± 1.2 | 37.2 ± 0.6 |
| 数学教师模型 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| Qwen/QwQ-32B | **44.2 ± 0.4** | 10.9 ± 0.4 | **71.6 ± 1.1** | **53.2 ± 0.4** |
| deepseek-ai/DeepSeek-R1 | 41.6 ± 0.4 | **14.9 ± 0.4** | 64.8 ± 0.9 | 46.7 ± 0.5 |
| microsoft/Phi-4-reasoning-plus | 30.6 ± 0.6 | 7.1 ± 0.4 | 49.0 ± 1.6 | 38.2 ± 0.9 |

*表 8：**使用较弱的教师模型优于使用较强的教师模型**。在所有领域中，QwQ-32B 都是最强的教师模型，尽管它本身是比 DeepSeek-R1 更弱的模型。更多结果见表 49。*

前面的实验一直使用 DeepSeek-R1 作为教师模型，因为这是许多推理数据集的标准做法。然而，可作为教师的推理模型有许多候选，包括 DeepSeek R1、Phi-4-Reasoning-Plus-14B (Abdin et al., 2025) 和 QwQ-32B。我们的实验衡量了为每种策略选择不同教师模型对下游的影响，如第 4.5 节所述。对于我们研究的所有教师模型，采样超参数均保持不变。该实验的结果见表 8。在所有领域中，使用 QwQ-32B 作为教师模型都优于所有其他教师模型；在代码和数学上，与使用 DeepSeek-R1 作为教师模型相比，平均准确率分别提升了 1.9% 和 2.6%。而这是在 QwQ-32B 的平均得分低于 DeepSeek-R1 的情况下取得的。例如，DeepSeek-R1 在 CodeElo、GPQA Diamond 和 JEEBench 上分别比 QwQ-32B 高出 9%、8% 和 23%。各教师模型实测性能的比较见表 29。

> **要点：** 我们使用 QwQ-32B 作为教师模型。

### 5 将我们的流水线扩展至 OpenThoughts3-1.2M

数据集扩展对于取得强劲性能起着关键作用。我们通过依次确定流水线每一步的最佳策略，并绘制其在 316 到 31.6k 个样本范围内的性能，来考察我们的流水线的扩展效果。图 3 表明，随着我们逐步叠加流水线各阶段的最佳选择，扩展行为随之改善。此外，图 3 还显示出规模与性能之间存在很强的正相关。这表明，进一步扩大数据集规模可能会带来更大的收益。

![图 3](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig03.png)

*图 3：**扩展每个流水线步骤中的最优策略**。在各个数据集规模上，流水线中后续阶段构建的数据集都会使扩展曲线上移。最大的提升来自问题来源的选择、问题过滤策略以及教师模型的选择。与科学上的性能相比，数学和代码上的平均性能呈现出更清晰的扩展趋势——最终的“Teacher Model”曲线并非科学上表现最好的曲线，这是我们的设计选择所致：我们依据跨领域的平均性能来选择最佳策略。*

因此，我们将第 4 节中的各条数据流水线混合起来并扩大规模，构建出 OpenThoughts3-1.2M，即我们规模为 1.2M 的数据集。OpenThoughts3-1.2M 包含 850,000 个数学数据点、250,000 个代码数据点和 100,000 个科学数据点。我们参照训练 OpenThinker2 所用的 OpenThoughts2-1M 混合数据确定了这一比例，该模型表现出强劲且均衡的性能，与 DeepSeek-R1-Distill 系列模型相当。为了达到每个领域的目标样本数，我们反向推算，估计在流水线起始阶段需要多少问题。例如，这要求我们把输入过滤阶段的数学问题数量从 1M 增加到 3M。随后，我们在流水线的每个阶段都应用性能最高的策略；若性能相同，则选择更易于扩展的方案。OpenThoughts3-1.2M 的这一构建过程如图 4 所示。

如表 1 所示，无论采用何种优化算法（SFT、RL 或二者兼用），OpenThinker3-7B 都是 7B 规模上最好的开放数据推理模型。OpenThinker3-7B 也能很好地泛化到在整个流水线过程中始终被留出的评估上，在 HMMT、AIME25 和 LCB 06/24-01/25 上取得了最高分数。关于扩展的更多结果见附录 G。

![图 4](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig04.png)

*图 4：**OpenThoughts3-1.2M 完整数据流水线**。我们的完整数据集以从数学、代码和科学领域获取大量问题为起点。下一步是过滤这些问题、对数学和科学问题进行去重、随机采样问题，然后为每个问题生成多个答案。我们的最终数据集包含 1.2M 个数据点。*

### 6 结论

通过迭代式的实验，我们的流水线揭示了关于有效构建 SFT 推理数据的若干关键洞见。这些发现共同塑造了我们的最终流水线，使我们得以构建 OpenThoughts3-1.2M——一个由科学、数学和代码数据组成的、最先进的开放数据 SFT 推理数据集。我们在这些数据上训练得到的最终模型 OpenThinker3-7B，是同等模型规模下最先进的（SOTA）开放数据推理模型。

这项工作存在若干局限性。我们没有探索用于强化学习的数据集，而强化学习是构建推理模型的一种标准训练范式。在 SFT 范畴内，我们也没有探索使用分阶段 SFT 或课程学习来进一步提升性能。尽管如此，我们相信这项工作能够为社区在开放推理模型上的持续进展奠定有价值的基础。

本项目还引出了若干有待进一步研究的开放方向：

1. 在我们流水线的每一步中，我们选择的是能使整体平均基准性能最大化的策略，而不是针对每个领域分别优化。这一选择假设存在一定程度的跨域迁移；例如，在数学数据上训练能够提升科学性能。然而，一旦将不同领域混合，这种迁移是否依然存在尚不清楚。
2. 我们发现扩展数据能够提升下游性能。当学生模型的性能逼近教师模型时，这一情况会如何变化？模型最终会进入平台期，还是会超越教师模型、实现弱到强泛化，仍是一个开放问题。
3. 我们的结果表明，如果答案多样性较高，有限的问题多样性对性能的影响相对较小。一个关键的开放问题是：这种相互作用在不同领域、数据集规模和模型规模下会如何表现。

### 致谢

我们感谢 Alex Fang、Matthew Wallingford、Jiaqi Zeng、Oleksii Kuchaiev、Asad Aali、Benjamin Burchfiel 和 Russ Tedrake 在项目各个阶段提供的有益讨论与支持。我们还要感谢 Adam R. Klivans、Mike Garrison 和 Satya Kotari 在算力与基础设施方面提供的支持。此外，我们还要感谢各超级计算设施及其团队提供的支持，尤其感谢来自 Juelich Supercomputer Center（JSC，德国）的 Damian Alvarez 和 Mathis Bode，以及来自 CINECA（意大利）的 Laura Morselli。

本研究得到了以下支持：Toyota Research Institute（TRI）；通过 UT Austin 的 Center for Generative AI（CGAI）和 Texas Advanced Computing Center（TACC）提供的 Vista GPU 集群；TU Dresden 的 NHR Center 的高性能计算机；以及由 Leibniz Supercomputing Centre（LRZ）通过 Munich Center for Machine Learning 提供的 AI Systems 计算资源。

本研究还得到了 NSF 资助项目 AF 1901292、CNS 2148141、IFML CCF 2019844，以及 UT Austin Machine Learning Lab（MLL）和 Onassis Foundation（奖学金编号：F ZS 056-1/2022-2023）所提供研究捐赠的支持。AGD 在开展本工作的部分时间里任职于 UT Austin。HB 部分得到了 AFOSR MURI 资助项目 FA9550-22-1-0380 的支持。MN 和 JJ 感谢 Federal Ministry of Education and Research of Germany（BMBF）在资助编号 01IS24085C（OPENHAFM）和资助项目 16HPC117K（MINERVA）下提供的资助、在资助编号 01IS22094B（WestAI - AI Service Center West）下提供的部分资助，以及欧盟分别通过 EuroHPC Joint Undertaking 计划在资助编号 101182737（MINERVA）下、通过 Digital Europe Programme 在资助编号 101195233（openEuroLLM）下提供的联合资助。

没有 Gauss Centre for Supercomputing e.V. 通过 John von Neumann Institute for Computing（NIC）在 Juelich Supercomputing Centre（JSC）的超级计算机 JUWELS Booster 上提供的支持，这项工作就不可能完成。我们还感谢：EuroHPC Joint Undertaking 通过 EuroHPC Extreme Access 资助项目 EHPC-EXT-2023E02-068 为本项目提供了 EuroHPC 超级计算机 LEONARDO 的访问权限，该超级计算机由 CINECA（意大利）和 LEONARDO 联盟托管；由 JSC 授予并运营、由 Helmholtz Data Federation（HDF）支持的 JUST 存储资源；通过 WestAI 计算资助项目“Measuring and enhancing advanced reasoning capabilities of foundation models via local model deployment”（westai0007）在 JSC 提供的计算资源；以及通过 JSC 在 JURECA 上提供的计算资源。

### 参考文献

- Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad Awan, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat Behl, et al. Phi-3 technical report: A highly capable language model locally on your phone. *arXiv preprint arXiv:2404.14219*, 2024.
- Marah Abdin, Sahaj Agarwal, Ahmed Awadallah, Vidhisha Balachandran, Harkirat Behl, Lingjiao Chen, Gustavo de Rosa, Suriya Gunasekar, Mojan Javaheripi, Neel Joshi, et al. Phi-4-reasoning technical report. *arXiv preprint arXiv:2504.21318*, 2025.
- Bo Adler, Niket Agarwal, Ashwath Aithal, Dong H Anh, Pallab Bhattacharya, Annika Brundyn, Jared Casper, Bryan Catanzaro, Sharon Clay, Jonathan Cohen, et al. Nemotron-4 340b technical report. *arXiv preprint arXiv:2406.11704*, 2024.
- Wasi Uddin Ahmad, Sean Narenthiran, Somshubra Majumdar, Aleksander Ficek, Siddhartha Jain, Jocelyn Huang, Vahid Noroozi, and Boris Ginsburg. Opencodereasoning: Advancing data distillation for competitive coding. *arXiv preprint arXiv:2504.01943*, 2025. URL <https://arxiv.org/abs/2504.01943>.
- Daman Arora, Himanshu Singh, and Mausam. Have llms advanced enough? a challenging problem solving benchmark for large language models. In Houda Bouamor, Juan Pino, and Kalika Bali (eds.), *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pp. 7527–7543, Singapore, December 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.emnlp-main.468. URL <https://aclanthology.org/2023.emnlp-main.468>.
- Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola Jovanović, and Martin Vechev. Matharena: Evaluating llms on uncontaminated math competitions, February 2025. URL <https://matharena.ai/>.
- Akhiad Bercovich, Itay Levy, Izik Golan, Mohammad Dabbah, Ran El-Yaniv, Omri Puny, Ido Galil, Zach Moshe, Tomer Ronen, Najeeb Nabwani, et al. Llama-nemotron: Efficient reasoning models. *arXiv preprint arXiv:2505.00949*, 2025.
- Bespoke-Labs. Bespoke-stratos: The unreasonable effectiveness of reasoning distillation. [www.bespokelabs.ai/blog/bespoke-stratos-the-unreasonable-effectiveness-of-reasoning-distillation](https://www.bespokelabs.ai/blog/bespoke-stratos-the-unreasonable-effectiveness-of-reasoning-distillation), 2025. Accessed: 2025-01-22.
- Sahil Chaudhary. Code alpaca: An instruction-following llama model for code generation. <https://github.com/sahil280114/codealpaca>, 2023.
- Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He, Jianhui Pang, Dian Yu, Linfeng Song, Qiuzhi Liu, Mengfei Zhou, Zhuosheng Zhang, et al. Do not think that much for 2+ 3=? on the overthinking of o1-like llms. *arXiv preprint arXiv:2412.21187*, 2024.
- Yang Chen, Zhuolin Yang, Zihan Liu, Chankyu Lee, Mohammad Shoeybi, Bryan Catanzaro, and Wei Ping. Acereason-nemotron: Advancing math and code reasoning through reinforcement learning. *arXiv preprint*, 2025.
- Yihe Deng, Hritik Bansal, Fan Yin, Nanyun Peng, Wei Wang, and Kai-Wei Chang. Openvlthinker: An early exploration to complex vision-language reasoning via iterative self-improvement. *arXiv preprint arXiv:2503.17352*, 2025.
- Ricardo Dominguez-Olmedo, Vedant Nanda, Rediet Abebe, Stefan Bechtold, Christoph Engel, Jens Frankenreiter, Krishna Gummadi, Moritz Hardt, and Michael Livermore. Lawma: The power of specialization for legal tasks. In *International Conference on Learning Representations (ICLR)*, 2025.
- Hugging Face. Open r1: A fully open reproduction of deepseek-r1, January 2025. URL <https://github.com/huggingface/open-r1>.
- Alex Fang, Hadi Pouransari, Matt Jordan, Alexander Toshev, Vaishaal Shankar, Ludwig Schmidt, and Tom Gunter. Datasets, documents, and repetitions: The practicalities of unequal data quality, 2025. URL <https://arxiv.org/abs/2503.07879>.
- Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, Shawn Presser, and Connor Leahy. The Pile: An 800gb dataset of diverse text for language modeling. *arXiv preprint arXiv:2101.00027*, 2020.
- Gemini-Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. *arXiv preprint arXiv:2312.11805*, 2023.
- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. *arXiv preprint arXiv:2501.12948*, 2025.
- Jujie He, Jiacai Liu, Chris Yuhao Liu, Rui Yan, Chaojie Wang, Peng Cheng, Xiaoyu Zhang, Fuxiang Zhang, Jiacheng Xu, Wei Shen, Siyuan Li, Liang Zeng, Tianwen Wei, Cheng Cheng, Bo An, Yang Liu, and Yahui Zhou. Skywork open reasoner 1 technical report. *arXiv preprint arXiv:2505.22312*, 2025a.
- Zhiwei He, Tian Liang, Jiahao Xu, Qiuzhi Liu, Xingyu Chen, Yue Wang, Linfeng Song, Dian Yu, Zhenwen Liang, Wenxuan Wang, Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu. Deepmath-103k: A large-scale, challenging, decontaminated, and verifiable mathematical dataset for advancing reasoning. *arXiv preprint arXiv:2504.11456*, 2025b. URL <https://arxiv.org/abs/2504.11456>.
- Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob Steinhardt. Measuring coding challenge competence with apps. *NeurIPS*, 2021a.
- Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. *NeurIPS*, 2021b.
- Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination free evaluation of large language models for code. *arXiv preprint arXiv:2403.07974*, 2024.
- Armand Joulin, Edouard Grave, Piotr Bojanowski, and Tomas Mikolov. Bag of tricks for efficient text classification. In *Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers*, pp. 427–431. Association for Computational Linguistics, April 2017.
- Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman, Lester James V Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, et al. Tulu 3: Pushing frontiers in open language model post-training. *arXiv preprint arXiv:2411.15124*, 2024.
- Katherine Lee, Daphne Ippolito, Andrew Nystrom, Chiyuan Zhang, Douglas Eck, Chris Callison-Burch, and Nicholas Carlini. Deduplicating training data makes language models better. In Smaranda Muresan, Preslav Nakov, and Aline Villavicencio (eds.), *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 8424–8445, Dublin, Ireland, May 2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.acl-long.577. URL <https://aclanthology.org/2022.acl-long.577/>.
- Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. Camel: Communicative agents for "mind" exploration of large scale language model society, 2023a.
- Jeffrey Li, Alex Fang, Georgios Smyrnis, Maor Ivgi, Matt Jordan, Samir Gadre, Hritik Bansal, Etash Guha, Sedrick Keh, Kushal Arora, Saurabh Garg, Rui Xin, Niklas Muennighoff, Reinhard Heckel, Jean Mercat, Mayee Chen, Suchin Gururangan, Mitchell Wortsman, Alon Albalak, Yonatan Bitton, Marianna Nezhurina, Amro Abbas, Cheng-Yu Hsieh, Dhruba Ghosh, Josh Gardner, Maciej Kilian, Hanlin Zhang, Rulin Shao, Sarah Pratt, Sunny Sanyal, Gabriel Ilharco, Giannis Daras, Kalyani Marathe, Aaron Gokaslan, Jieyu Zhang, Khyathi Chandu, Thao Nguyen, Igor Vasiljevic, Sham Kakade, Shuran Song, Sujay Sanghavi, Fartash Faghri, Sewoong Oh, Luke Zettlemoyer, Kyle Lo, Alaaeldin El-Nouby, Hadi Pouransari, Alexander Toshev, Stephanie Wang, Dirk Groeneveld, Luca Soldaini, Pang Wei Koh, Jenia Jitsev, Thomas Kollar, Alexandros G. Dimakis, Yair Carmon, Achal Dave, Ludwig Schmidt, and Vaishaal Shankar. Datacomp-lm: In search of the next generation of training sets for language models. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (eds.), *Advances in Neural Information Processing Systems*, volume 37, pp. 14200–14282. Curran Associates, Inc., 2024. URL <https://proceedings.neurips.cc/paper_files/paper/2024/file/19e4ea30dded58259665db375885e412-Paper-Datasets_and_Benchmarks_Track.pdf>.
- Jia LI, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Costa Huang, Kashif Rasul, Longhui Yu, Albert Jiang, Ziju Shen, Zihan Qin, Bin Dong, Li Zhou, Yann Fleureau, Guillaume Lample, and Stanislas Polu. Numinamath. [https://huggingface.co/AI-MO/NuminaMath-1.5](https://github.com/project-numina/aimo-progress-prize/blob/main/report/numina_dataset.pdf), 2024.
- Rongao Li, Jie Fu, Bo-Wen Zhang, Tao Huang, Zhihong Sun, Chen Lyu, Guang Liu, Zhi Jin, and Ge Li. Taco: Topics in algorithmic code generation dataset. *arXiv preprint arXiv:2312.14852*, 2023b.
- Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. Competition-level code generation with alphacode. *arXiv preprint arXiv:2203.07814*, 2022.
- Zhenghao Lin, Zhibin Gou, Yeyun Gong, Xiao Liu, Yelong Shen, Ruochen Xu, Chen Lin, Yujiu Yang, Jian Jiao, Nan Duan, et al. Rho-1: Not all tokens are what you need. *arXiv preprint arXiv:2404.07965*, 2024.
- Zhengzhong Liu, Bowen Tan, Hongyi Wang, Willie Neiswanger, Tianhua Tao, Haonan Li, Fajri Koto, Yuqi Wang, Suqi Sun, Omkar Pangarkar, Richard Fan, Yi Gu, Victor Miller, Liqun Ma, Liping Tang, Nikhil Ranjan, Yonghao Zhuang, Guowei He, Renxi Wang, Mingkai Deng, Robin Algayres, Yuanzhi Li, Zhiqiang Shen, Preslav Nakov, and Eric Xing. Llm360 k2-65b: Scaling up fully transparent open-source llms. 2024.
- MAA. Amc 2023 problems, 2023. URL <https://artofproblemsolving.com/wiki/index.php/2023_AMC_12A_Problems>. Accessed: 2025-05-11.
- MAA. Aime 2024 problems, 2024. URL <https://artofproblemsolving.com/wiki/index.php/2024_AIME_I_Problems>. Accessed: 2025-05-11.
- MAA. Aime 2025 problems, 2025. URL <https://artofproblemsolving.com/wiki/index.php/2025_AIME_I_Problems>. Accessed: 2025-05-11.
- Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel Li, Steven Basart, Bo Li, et al. Harmbench: A standardized evaluation framework for automated red teaming and robust refusal. *arXiv preprint arXiv:2402.04249*, 2024.
- Ivan Moshkov, Darragh Hanley, Ivan Sorokin, Shubham Toshniwal, Christof Henkel, Benedikt Schifferer, Wei Du, and Igor Gitman. Aimo-2 winning solution: Building state-of-the-art mathematical reasoning models with openmathreasoning dataset. *arXiv preprint arXiv:2504.16891*, 2025.
- Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple test-time scaling, 2025. URL <https://arxiv.org/abs/2501.19393>.
- Marianna Nezhurina, Lucia Cipolina-Kun, Mehdi Cherti, and Jenia Jitsev. Alice in wonderland: Simple tasks showing complete reasoning breakdown in state-of-the-art large language models. *arXiv preprint arXiv:2406.02061*, 2024.
- NovaSky-Team. Think less, achieve more: Cut reasoning costs by 50 <https://novasky-ai.github.io/posts/reduce-overthinking>, 2025a. Accessed: 2025-01-23.
- NovaSky-Team. Sky-t1: Train your own o1 preview model within 450. <https://novasky-ai.github.io/posts/sky-t1>, 2025b. Accessed: 2025-01-09.
- OpenAI. Openai o3 and o4-mini system card, 2024. URL <https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf>. Accessed: 2025-05-11.
- OpenThoughts-Team. Open Thoughts. <https://open-thoughts.ai>, February 2025.
- Guilherme Penedo, Hynek Kydlíček, Loubna Ben allal, Anton Lozhkov, Margaret Mitchell, Colin Raffel, Leandro Von Werra, and Thomas Wolf. The fineweb datasets: Decanting the web for the finest text data at scale. In *The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2024a. URL <https://openreview.net/forum?id=n6SCkn2QaG>.
- Guilherme Penedo, Hynek Kydlíček, Loubna Ben allal, Anton Lozhkov, Margaret Mitchell, Colin Raffel, Leandro Von Werra, and Thomas Wolf. The fineweb datasets: Decanting the web for the finest text data at scale. In *The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track*, 2024b. URL <https://openreview.net/forum?id=n6SCkn2QaG>.
- Guilherme Penedo, Anton Lozhkov, Hynek Kydlíček, Loubna Ben Allal, Edward Beeching, Agustín Piqueres Lajarín, Quentin Gallouédec, Nathan Habib, Lewis Tunstall, and Leandro von Werra. Codeforces. <https://huggingface.co/datasets/open-r1/codeforces>, 2025.
- Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang, Mohamed Shaaban, John Ling, and Sean Shi et. al. Humanity’s last exam, 2025. URL <https://arxiv.org/abs/2501.14249>.
- Xiangyu Qi, Yi Zeng, Tinghao Xie, Pin-Yu Chen, Ruoxi Jia, Prateek Mittal, and Peter Henderson. Fine-tuning aligned language models compromises safety, even when users do not intend to!, 2023. URL <https://arxiv.org/abs/2310.03693>.
- Shanghaoran Quan, Jiaxi Yang, Bowen Yu, Bo Zheng, Dayiheng Liu, An Yang, Xuancheng Ren, Bofei Gao, Yibo Miao, Yunlong Feng, et al. Codeelo: Benchmarking competition-level code generation of llms with human-comparable elo ratings. *arXiv preprint arXiv:2501.01257*, 2025.
- Qwen-Team. Qwq-32b: Embracing the power of reinforcement learning, March 2025. URL <https://qwenlm.github.io/blog/qwq-32b/>.
- Qwen2.5-Team. Qwen2.5 technical report. *arXiv preprint arXiv:2412.15115*, 2024.
- Negin Raoof, Etash Kumar Guha, Ryan Marten, Jean Mercat, Eric Frankel, Sedrick Keh, Hritik Bansal, Georgios Smyrnis, Marianna Nezhurina, Trung Vu, Zayne Rea Sprague, Mike A Merrill, Liangyu Chen, Caroline Choi, Zaid Khan, Sachin Grover, Benjamin Feuer, Ashima Suvarna, Shiye Su, Wanjia Zhao, Kartik Sharma, Charlie Cheng-Jie Ji, Kushal Arora, Jeffrey Li, Aaron Gokaslan, Sarah M Pratt, Niklas Muennighoff, Jon Saad-Falcon, John Yang, Asad Aali, Shreyas Pimpalgaonkar, Alon Albalak, Achal Dave, Hadi Pouransari, Greg Durrett, Sewoong Oh, Tatsunori Hashimoto, Vaishaal Shankar, Yejin Choi, Mohit Bansal, Chinmay Hegde, Reinhard Heckel, Jenia Jitsev, Maheswaran Sathiamoorthy, Alex Dimakis, and Ludwig Schmidt. Evalchemy: Automatic evals for llms, 2025.
- David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman. GPQA: A graduate-level google-proof q&a benchmark. In *First Conference on Language Modeling*, 2024. URL <https://openreview.net/forum?id=Ti67584b98>.
- Paul Röttger, Hannah Rose Kirk, Bertie Vidgen, Giuseppe Attanasio, Federico Bianchi, and Dirk Hovy. Xstest: A test suite for identifying exaggerated safety behaviours in large language models. *arXiv preprint arXiv:2308.01263*, 2023.
- Kashun Shum, Yuzhen Huang, Hongjian Zou, Ding Qi, Yixuan Liao, Xiaoxin Chen, Qian Liu, and Junxian He. Predictive data selection: The data that predicts is the data that teaches. *arXiv preprint arXiv:2503.00808*, 2025.
- Luca Soldaini, Rodney Kinney, Akshita Bhagia, Dustin Schwenk, David Atkinson, Russell Authur, Ben Bogin, Khyathi Chandu, Jennifer Dumas, Yanai Elazar, Valentin Hofmann, Ananya Jha, Sachin Kumar, Li Lucy, Xinxi Lyu, Nathan Lambert, Ian Magnusson, Jacob Morrison, Niklas Muennighoff, Aakanksha Naik, Crystal Nam, Matthew Peters, Abhilasha Ravichander, Kyle Richardson, Zejiang Shen, Emma Strubell, Nishant Subramani, Oyvind Tafjord, Evan Walsh, Luke Zettlemoyer, Noah Smith, Hannaneh Hajishirzi, Iz Beltagy, Dirk Groeneveld, Jesse Dodge, and Kyle Lo. Dolma: an open corpus of three trillion tokens for language model pretraining research. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 15725–15788, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.840. URL <https://aclanthology.org/2024.acl-long.840/>.
- Dan Su, Kezhi Kong, Ying Lin, Joseph Jennings, Brandon Norick, Markus Kliegl, Mostofa Patwary, Mohammad Shoeybi, and Bryan Catanzaro. Nemotron-cc: Transforming common crawl into a refined long-horizon pretraining dataset, 2024. URL <https://arxiv.org/abs/2412.02595>.
- Yang Sui, Yu-Neng Chuang, Guanchu Wang, Jiamu Zhang, Tianyi Zhang, Jiayi Yuan, Hongyi Liu, Andrew Wen, Shaochen Zhong, Hanjie Chen, et al. Stop overthinking: A survey on efficient reasoning for large language models. *arXiv preprint arXiv:2503.16419*, 2025.
- Shubham Toshniwal, Wei Du, Ivan Moshkov, Branislav Kisacanin, Alexan Ayrapetyan, and Igor Gitman. Openmathinstruct-2: Accelerating ai for math with massive open-source instruction data. *arXiv preprint arXiv:2410.01560*, 2024.
- Zijun Wang, Haoqin Tu, Yuhan Wang, Juncheng Wu, Jieru Mei, Brian R Bartoldson, Bhavya Kailkhura, and Cihang Xie. Star-1: Safer alignment of reasoning llms with 1k data. *arXiv preprint arXiv:2504.01903*, 2025.
- Alexander Wettig, Kyle Lo, Sewon Min, Hannaneh Hajishirzi, Danqi Chen, and Luca Soldaini. Organize the web: Constructing domains enhances pre-training data curation. *arXiv preprint arXiv:2502.10341*, 2025.
- Yixin Ye, Zhen Huang, Yang Xiao, Ethan Chern, Shijie Xia, and Pengfei Liu. Limo: Less is more for reasoning, 2025. URL <https://arxiv.org/abs/2502.03387>.
- Weizhe Yuan, Jane Yu, Song Jiang, Karthik Padthe, Yang Li, Dong Wang, Ilia Kulikov, Kyunghyun Cho, Yuandong Tian, Jason E Weston, and Xian Li. Naturalreasoning: Reasoning in the wild with 2.8m challenging questions, 2025. URL <https://arxiv.org/abs/2502.13124>.
- Xiang Yue, Tuney Zheng, Ge Zhang, and Wenhu Chen. Mammoth2: Scaling instructions from the web. *Advances in Neural Information Processing Systems*, 2024.
- Yifan Zhang, Yifan Luo, Yang Yuan, and Andrew Chi-Chih Yao. Autonomous data selection with language models for mathematical texts. *arXiv preprint arXiv:2402.07625*, 2024.

### 附录 A 资源链接

我们将模型和数据集作为 Hugging Face 上一个合集的一部分发布。我们的 OpenThinker3-7B 模型见 <https://huggingface.co/open-thoughts/OpenThinker3-7B>，数据集见 <https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M>。我们的代码库将发布于 <https://github.com/open-thoughts/open-thoughts>。我们还发布了一篇与本工作配套的博客文章，地址为 <https://www.open-thoughts.ai/blog/ot3>。

### 附录 B 贡献

所有作者均按姓氏字母顺序排列。

#### 基础设施

**数据生成框架**：Etash Guha, Sedrick Keh, Ryan Marten, Mike A. Merrill, Negin Raoof, Georgios Smyrnis, Zayne Sprague, Trung Vu

**Curator**：Charlie Cheng-Jie Ji, Ryan Marten, Jean Mercat, Marianna Nezhurina, Shreyas Pimpalgaonkar, Mahesh Sathiamoorthy, Kartik Sharma, Georgios Smyrnis, Trung Vu

**训练框架**：Etash Guha, Reinhard Heckel, Jenia Jitsev, Sedrick Keh, Ryan Marten, Marianna Nezhurina, Negin Raoof, Georgios Smyrnis

**Evalchemy**：Hritik Bansal, Yichuan Deng, Benjamin Feuer, Eric Frankel, Sachin Grover, Etash Guha, Reinhard Heckel, Jenia Jitsev, Sedrick Keh, Ryan Marten, Jean Mercat, Marianna Nezhurina, Negin Raoof, Jon Saad-Falcon, Georgios Smyrnis, Zayne Sprague, Shiye Su, Ashima Suvarna, John Yang

**日志与数据库**：Etash Guha, Sedrick Keh, Ryan Marten, Negin Raoof

#### 实验

**数据生成**：Etash Guha, Sedrick Keh, Ryan Marten, Negin Raoof, Georgios Smyrnis

**训练运行**：Etash Guha, Reinhard Heckel, Sedrick Keh, Ryan Marten, Marianna Nezhurina, Negin Raoof, Georgios Smyrnis, Shiye Su, Wanjia Zhao

**评估**：Benjamin Feuer, Etash Guha, Jenia Jitsev, Sedrick Keh, Ryan Marten, Jean Mercat, Negin Raoof, Georgios Smyrnis, Ashima Suvarna, Wanjia Zhao

**延伸分析与消融实验**：Hritik Bansal, Liangyu Chen, Caroline Choi, Yichuan Deng, Benjamin Feuer, Eric Frankel, Sachin Grover, Etash Guha, Reinhard Heckel, Zaid Khan, Ryan Marten, Jean Mercat, Mike A. Merrill, Niklas Muennighoff, Vivek Ramanujan, Zayne Sprague, Ashima Suvarna, Wanjia Zhao

#### 写作

Hritik Bansal, Liangyu Chen, Alexandros G. Dimakis, Benjamin Feuer, Etash Guha, Reinhard Heckel, Jenia Jitsev, Sedrick Keh, Zaid Khan, Ryan Marten, Jean Mercat, Mike A. Merrill, Niklas Muennighoff, Marianna Nezhurina, Sarah Pratt, Negin Raoof, Ludwig Schmidt, Georgios Smyrnis, Ashima Suvarna, Wanjia Zhao

#### 领导与指导

**指导**：Alon Albalak, Kushal Arora, Mohit Bansal, Kai-Wei Chang, Yejin Choi, Achal Dave, Alexandros G. Dimakis, Greg Durrett, Saadia Gabriel, Aaron Gokaslan, Aditya Grover, Tatsunori Hashimoto, Reinhard Heckel, Chinmay Hegde, Jenia Jitsev, Jeffrey Li, Mike A. Merrill, Sewoong Oh, Maheswaran Sathiamoorthy, Ludwig Schmidt, Vaishaal Shankar, Blake Wulfe

**项目协调**：Alexandros G. Dimakis, Etash Guha, Ryan Marten, Ludwig Schmidt

### 附录 C Bespoke-Stratos 与 OpenThoughts 1 & 2

如第 3 节所述，OpenThoughts 项目由一系列连续发布的版本组成，始于 BespokeStratos-17K (Bespoke-Labs, 2025)，此后历经四代模型和数据集。

BespokeStratos-17K 沿用了与 SkyT1 (NovaSky-Team, 2025b) 相同的数据来源，但将标注模型换成了 R1，并使用 gpt-4o-mini 进行验证、过滤掉错误的解答。关于 BespokeStratos-17K 的更多细节，可参见原始博客文章。[^1]

我们最初发布的 OpenThoughts 和 OpenThoughts2 记录在 <https://www.openthoughts.ai/> 上；该网站还链接到主 GitHub 仓库 <https://github.com/open-thoughts/open-thoughts> 和 Hugging Face 组织 <https://huggingface.co/open-thoughts>，所有资源和代码都存放在那里。

![图 5](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig05.png)

*图 5：**OpenThoughts-114K 数据配方**。OpenThoughts1 的构建方式是：从四个领域中分别获取问题，用 DeepSeek-R1 补全答案，进行验证（数学、谜题和代码——不包括科学），并进行混合。*

![图 6](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig06.png)

*图 6：**OpenThoughts2-1M 数据配方**。OpenThoughts2-1M 通过加入新的问题生成策略，在 OpenThoughts-114K 的基础上进行了改进。其中既包括 OpenR1 和 CodeFeedback 等已有数据集，也包括我们自己生成的数据集，例如 AutoMathText。将其与去重相结合，我们最终得到了规模为 1M 的数据集。*

OpenThoughts-114K [^2] 在 Sky-T1 流水线的基础上扩大了规模，并做了一些小的调整，例如使用 DeepSeek-R1 作为标注模型，以及使用 LLM 评判进行验证。OpenThoughts-114K 的完整流水线如图 5 所示，具体细节在博客文章中有所概述。鉴于 OpenThoughts-114K 的成功，扩大数据集规模是顺理成章的下一步。OpenThoughts2-1M [^3] 扩大数据规模的主要手段，是在数学和代码领域引入更多的问题生成策略。这些问题生成策略既包括 Glaive、ShareGPTCode 和 OpenR1-Math 等已有数据集，也包括我们自己生成的数据集，例如 AutoMathText。完整的流水线如图 6 所示。同样，更具体的细节可参见博客文章。

### 附录 D 训练细节

#### D.1 训练框架

我们使用 LlamaFactory 进行训练。该仓库已公开，地址为 <https://github.com/hiyouga/LLaMA-Factory>。

#### D.2 超参数

对于图 1 中的不同规模，我们为每个规模使用不同的超参数。一般而言，我们希望使用更大的 batch size 和更大的学习率，但在较小的数据集上这样做会导致训练步数过少。我们进行了超参数扫描，以便在每个模型规模下找到一组合适的超参数。最终我们得到了 4 组超参数——微型（用于 0.3K 规模）、小型（用于 1K、3K 规模）、中型（用于 10K、30K 规模）和大型（用于 100K 及以上规模）。除 epoch 数、batch size、学习率和序列打包（packing）外，这些超参数组完全相同。

对于所有超参数组，我们都基于 DeepSpeed v3 进行训练，使用余弦学习率，预热为 0.1，权重衰减为 0，并使用 betas 为 0.9 和 0.999 的 AdamW 优化器。各超参数组之间的具体差异见下方表 9。

| 超参数组 | 数据集规模 | 学习率 | Batch Size | Epoch 数 | 序列打包 |
| --- | --- | --- | --- | --- | --- |
| 微型 | \< 1K | 1e-5 | 32 | 13 | 否 |
| 小型 | 1K - 3.16K | 2e-5 | 96 | 7 | 否 |
| 中型 | 3.16K - 31.6K | 4e-5 | 128 | 5 | 否 |
| 大型 | > 31.6K | 8e-5 | 512 | 5 | 是 |

*表 9：**不同超参数组的设置及其对应的数据集规模**。*

如上方表 9 所示，微型、小型和中型组在训练时不使用样本打包，而大型组在训练时使用打包。对于大型超参数组，我们使用打包以节省计算时间。另一方面，对于微型、小型和中型组，我们不使用打包，因为我们希望有更多的训练步数。我们将在下文第 D.3 节中表明，是否使用打包并不会显著影响我们的性能。

除打包外，我们还调整了部分超参数以优化训练速度。我们使用不带内存卸载的 DeepSpeed v3。此外，我们使用持久化的 dataloader worker，并设置 num\_workers=4。我们用这些设置进行了小规模测试，以确保它们不会对性能产生负面影响。

#### D.3 序列打包

我们研究了序列打包在多种推理和编程基准上对模型性能的影响。序列打包将多个训练样本拼接成单个序列，以提高计算效率，但可能会影响学习动态。表 10 比较了在一个序列较短的数据集上使用与不使用打包训练的模型。总体而言，我们看到加入打包并不会对性能产生负面影响。这一观察与 Face (2025) 报告的部分发现相反，他们发现在其实验设置下打包会对性能产生负面影响。我们认为，这种性能下降很可能归因于将长序列截断成多个部分；而在 Llama Factory 的打包实现中，打包以贪心方式实现，并且只有较短的序列才会被打包在一起。

| 配置 | AIME24 | AMC23 | MATH500 | JEE | GPQA-D | LCB | CodeElo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AM100K | 18.7 | **62.0** | **79.6** | 45.6 | **46.5** | **34.7** | **6.3** |
| *不使用序列打包* | **22.0** | **62.0** | 77.6 | **46.4** | 34.7 | 31.7 | 5.3 |

*表 10：**使用与不使用序列打包训练的模型的性能比较**。打包表现出好坏参半的效果。*

#### D.4 对话模板

我们探索的另一个维度是对话模板。更具体地说，它指的是如何通过提示让推理模型生成思考 token。这通常以专门模板的形式出现。例如，R1 模板用 `<think>` 和 `</think>` 包裹思考 token。在表 11 中，我们将这一 R1 模板与 SkyT1 模板进行了比较，后者使用 `<|begin_of_thought|>` 和 `<|end_of_thought|>`，并且最初被用于在 OpenThoughts-114k 上训练初版 OpenThinker-7B。从表 11 可以看出，两种不同对话模板的结果大致相当，这表明只要存在对话模板，模板本身可能并没有那么重要（完全移除对话模板的消融实验见下文第 D.5 节）。为简单起见，我们在所有流水线实验中都沿用由 `<think>` 和 `</think>` 构成的 R1 对话模板。

| 模型 | AIME24 | AIME25 I | AMC23 | MATH500 | GPQA-D | LCB 05/23-05/24 |
| --- | --- | --- | --- | --- | --- | --- |
| OpenThinker-7B | 31.3 | **28.0** | 72.0 | **84.4** | 42.9 | **41.8** |
| 使用 R1 模板 | **32.7** | 22.0 | **72.5** | 83.8 | **43.9** | 33.6 |

*表 11：**使用与不使用 R1 模板的 OpenThinker-7B 模型在不同基准上的性能比较**。该表显示，使用更简单的 `<think>` 和 `</think>` token 来代替更复杂的 SkyT1 token（`<|begin_of_thought|>` 和 `<|end_of_thought|>`），在大多数基准上能取得相当或略有提升的性能。*

#### D.5 系统提示词

在本小节中，我们研究完全去除对话模板、仅直接对模型进行提示的效果。我们在表 12 中报告了结果。我们的评估揭示了几项关键发现。第一，显式开启推理能在数学和科学推理任务上稳定地提升性能，在 AIME 基准上的提升尤为显著（在 AIME25 上为 45.3% vs. 2.0%）。第二，即使显式关闭推理，仍有许多回答以 `<think>` token 开头（1681/3127），这表明模型已经学会默认启用推理机制。第三，不同系统提示词的选择会产生因任务而异的影响：虽然“开启推理”有助于数学任务，但完全去除系统提示词有时能取得更好的结果（在 AIME24 上为 70.0% vs. 61.3%），这表明显式指令偶尔可能会限制模型自然的推理模式。

| 模型/配置 | AIME24 | AIME25 | AMC23 | MATH500 | GPQA-D | LCB 05/23-05/24 |
| --- | --- | --- | --- | --- | --- | --- |
| *Llama-3.1-Nemotron-Nano-8B（本文）* | | | | | | |
| 开启推理 | 61.3 | 45.3 | 94.0 | 89.0 | 55.9 | 68.4 |
| 关闭推理 | 4.0 | 2.0 | 38.0 | 48.8 | 34.7 | 67.1 |
| 无系统提示词 | 70.0 | 42.7 | 94.0 | 88.8 | 23.2 | 67.2 |
| *Llama-3.1-Nemotron-Nano-8B（官方）* | | | | | | |
| 开启推理 | – | 47.1 | – | 95.4 | 54.1 | – |
| 关闭推理 | – | 0.0 | – | 36.6 | 39.4 | – |

*表 12：**开启推理与不开启推理时在各推理基准上的性能比较**。对现有模型开启推理能大幅提升性能。然而，完全不使用系统提示词也能取得与“开启推理”相近的良好表现。*

### 附录 E 评估细节

所有基准上的模型评估均使用我们统一的多 GPU 评估框架 **Evalchemy** (Raoof et al., 2025) 完成。Evalchemy 将每个任务划分为相互独立的分片，并行运行这些分片（通过数据并行分片），并将每个分片的指标以流式方式传回中央协调器进行实时汇总。这一架构确保了一致的生成设置以及对模型检查点和采样参数的可复现记录，并使我们能够计算多次重复运行下的平均模型准确率和标准误。我们使用 Evalchemy 缓存长思维链任务（例如 AIME、LiveCodeBench、GPQA Diamond）的完整模型生成结果，从而减少了冗余的推理开销，并便于分析失败案例。

对于每个基准，我们报告：

- AIME24、AIME25、AMC23 和 HMMT：10 次运行的平均准确率和 SEM
- LiveCodeBench：6 次运行的平均准确率和 SEM
- CodeForces、CodeElo、GPQA Diamond、JEEBench 和 HLE：3 次运行的平均准确率和 SEM
- MATH500：在包含 500 个样本的完整集合上进行单次评估

所有运行均使用统一的生成配置：temperature = 0.7、top\_p = 1.0 以及 max\_new\_tokens = 32,768。

具有长 CoT 的推理模型通常会在给出最终答案之前生成多步解释。回答通常以 `<think>` token 开头，包含中间推理步骤，并以 `</think>` token 结尾，表示推理过程结束。最终答案位于该块之后。对于代码生成问题，最终答案通常标记在带有语言标签的围栏代码块中。

我们对所用的每个基准分别作简要介绍。

1. **AIME24**：2024 年举办的一项面向高中生的数学竞赛。其中包含 30 道不同难度的题目。答案为 0 到 999 之间的单个整数。
2. **AIME25**：2025 年举办的一项面向高中生的数学竞赛。其中包含 30 道不同难度的题目。答案为 0 到 999 之间的单个整数。
3. **AMC23**：2023 年举办的一项面向高中生的数学竞赛。它由 40 道不同难度的题目组成。答案均为数值。
4. **MATH500**：由 500 道多样化的题目组成，涉及概率、代数、三角学和几何。
5. **CodeForces**：由 453 道来自 CodeForces 平台的真实编程题组成。该基准衡量基于单元测试的执行准确率，并采用可与人类相比较的 Elo 评分。
6. **CodeElo**：由 391 道真实编程题组成，这些题目从多种竞赛中构建而来。该基准衡量基于单元测试的执行准确率，并采用经过难度校准的 Elo 评分。
7. **LiveCodeBench**：一个由真实编程任务组成的基准，这些任务评估模型利用单元测试反馈来生成、执行、验证并迭代修复解答的能力。LiveCodeBench 05/23-05/24 子集包含 511 道于 2023 年 5 月至 2024 年 5 月间发布的题目，而 06/24-01/25 子集包含 369 道于 2024 年 5 月至 2025 年 1 月间发布的题目。
8. **GPQA Diamond**：来自 Graduate-Level Google-Proof Q&A Benchmark（GPQA）的一组 198 道高难度题目。题目均为多项选择题。
9. **JEEBench**：包含 515 道涵盖物理、化学和数学科目的题目，这些题目收集自 2016 年至 2023 年举行的 Joint Entrance Examination (JEE): Advanced。题目形式包括多项选择题和数值题。
10. **HMMT**：来自 2025 年 2 月举行的 HMMT 高中数学竞赛的 30 道题目。题目涵盖组合数学、数论、代数和几何。
11. **HLE**：Humanity’s Last Exam（HLE）基准中由 512 道纯文本多项选择题构成的子集。

| **基准** | **领域 / 描述** | **问题数量** |
| --- | --- | --- |
| **代码生成** | | |
| CodeElo (Quan et al., 2025) | 以可与人类相比较的 Elo 评分评估代码生成。 | 391 |
| CodeForces (Penedo et al., 2025) | 对竞赛级代码生成进行基准评测。 | 453 |
| LiveCodeBench 05/23-05/24 (Jain et al., 2024) | 包含迭代修复的全面代码基准。 | 511 |
| LiveCodeBench 06/24-01/25 (Jain et al., 2024) | 包含迭代修复的全面代码基准。 | 369 |
| **数学问题求解** | | |
| AIME 24 (MAA, 2024) | 2024 年 AIME 数学推理数据集。 | 30 |
| AIME 25 (MAA, 2025) | 2025 年 AIME 数学推理数据集。 | 30 |
| AMC 23 (MAA, 2023) | 2023 年 AMC 数学推理数据集。 | 40 |
| HMMT (Balunović et al., 2025) | 高中数学竞赛。 | 30 |
| MATH500 (Hendrycks et al., 2021b) | 出自“Let’s Verify Step by Step”的 500 题子集。 | 500 |
| **科学任务** | | |
| GPQA Diamond (Rein et al., 2024) | 研究生水平、防 Google 搜索的问答基准。 | 198 |
| JEEBench (Arora et al., 2023) | IIT JEE-Advanced 工科入学考试试题。 | 515 |
| **通用任务** | | |
| HLE (Phan et al., 2025) | 由学科专家编写的问题。 | 512 |

*表 13：**我们在跨越多个数据领域的 12 个任务上进行评估**。我们在其中 8 个任务上验证实验，并将其余 4 个任务（AIME 2025、LiveCodeBench 06/24-01/25、HMMT、HLE）保留为留出集。*

### 附录 F 去污染

来自评估数据集的污染是一个重要问题，因为它有可能导致关于训练集实际效用的误导性结果。可以预期，以某种形式包含评估题目的训练数据会提升在这些相同题目上的性能。这种效应可能会影响我们实验的结论。为避免这一问题，我们依据两种不同的标准，针对我们的评估集进行去污染。

我们使用的第一种方法是每个训练样本与每个评估样本之间的 Indel 相似度。该相似度指的是使一个样本与另一个样本相匹配所需插入或删除的字符数，并且是相对于样本长度计算的。更准确地说，我们考虑一对字符串之间的归一化 Indel 相似度得分，其计算基于最长公共子序列（LCS）指标：

```math
\text{indel}_{\text{sim}}=100\times\frac{\text{LCS}_{\text{length}}(s_{1},s_{2})}{\max(|s_{1}|,|s_{2}|)} \qquad (1)
```

就该指标而言，我们认为两个字符串之间 75% 的相似度即表明存在污染。

我们的第二种方法是基于 N-gram 的相似度指标。在这一设置下，我们首先使用与 Qwen2-7B-Instruct 模型相同的分词器，对训练样本和评估样本分别进行分词。然后，我们考察每个样本中的 N-gram 集合，其中 N = 13。如果发现两个样本之间共享某个 N-gram，我们就认为该训练样本被污染。

在我们的流水线中，如果一个训练样本被我们的任一方法标记为被污染，我们就认为它被污染并将其丢弃。各方法的阈值是根据经验选定的，目的是同时最小化假阴性（被污染但未被检测出的样本）和假阳性（被标记为被污染、但实际上与评估样本无关的样本）。

我们通过严格的实验对去污染方案进行了系统的调优。我们的测试平台是一个人工污染的数据集；理想的去污染方案能够将被污染的题目从正常题目中准确地过滤出来。

**被污染数据集的构建**。我们的实验需要一个由被污染题目和未被污染题目组成的数据集。我们从多个来源构建了这一数据集。

1. 我们选取测试集（MATH500、GPQA Diamond、LiveCodeBench），并从每个测试集中采样原题。
2. 我们从测试集中采样题目，并施加三类改动。第一类改动是将题目嵌入更长的上下文中，例如“Please help me solve this problem: ”。第二类改动是将若干词语替换为同义词、将数值表达式替换为等价表达式，以及替换变量名。最后一类改动是通过调整分段、句子顺序和标点来改变题目的格式。
3. 我们通过人工编写完全原创的题目，加入未被污染的题目。

总体而言，我们的数据集包含 3092 个被污染样本和 3000 个未被污染样本。我们对去污染算法进行了调优，使其产生几乎为 0 的假阴性（将被污染的题目标记为已去污染），同时不会产生过多假阳性。我们最终的去污染方案的结果见图 7。我们最终的去污染算法在 3092 个人工污染的条目中仅漏掉 12 道题目，对应 99.6% 的真阴性率。降低模糊字符串匹配的阈值或 n-gram 计数中的 n，会显著提高假阳性率，进而可能影响下游性能。该去污染方案仅丢弃了 1.4% 的未被污染样本。

![图 7](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig07.png)

*图 7：**我们的去污染算法能够准确识别被污染的样本**。我们的去污染算法的真阴性准确率为 99.6%。该算法丢弃的未被污染样本也极少。*

### 附录 G 补充扩展实验

![图 8](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig08.png)

*图 8：**在 OpenThoughts3-1.2M 中规模逐渐增大的子集上微调 Qwen-2.5-7B-Instruct 后的下游模型性能**。在多种多样的数学（AIME、AMC、MATH、HMMT）、代码（LiveCodeBench、CodeElo、CodeForces）和科学（JEEBench、HLE）基准上，OpenThoughts3-1.2M 都优于现有的推理数据集。HMMT、AIME 2025、LiveCodeBench 06/24-01/25 和 HLE 是“留出”的，这意味着在实验过程中，我们没有用它们来评估任何中间模型以指导我们的数据配方。*

研究扩展趋势能让我们观察一个数据配方在不同规模下是否保持一致，并有助于判断进一步扩大规模是否有前景。图 8 显示，在各个规模和各个基准上，OpenThoughts3 配方都全面优于其他推理数据集策略。

在所研究的许多基准上，性能持续提升，直至 1M 的规模。然而，一些基准在最大规模下趋于饱和（AMC23、MATH500），另一些基准则对规模没有响应（HLE）。将推理数据集扩展到超过 1M 的更大规模，是一个令人兴奋的未来方向。

扩展曲线并不总是呈现平滑的性能提升，而是会出现回落和跃升。我们的实验流程在训练和评估中都存在方差，因此即使数据集固定，下游性能也会有所波动。然而，我们在实验中发现，在固定数据集上重新训练和重新评估模型，并不能完全解释这些回落和跃升。

为了进一步研究扩展趋势，我们首先分离出每个领域的数据，并测量其在域内评估基准上的平均性能。这与第 4 节中流水线实验的设置相同，在这些实验中，数据配方是针对每个领域（数学、代码和科学）分别进行扫描的。

图 9 显示，各个单独领域的配方在超出流水线实验所用的最大数据集规模 31.6K 之后，仍能在又一个数量级的范围内良好地扩展。我们选择这些规模，是为了以半个数量级的分辨率研究扩展行为。

我们加入“No Pipeline”作为朴素基线，以展示由第 4 节中大量实验所确定的数据配方带来的全部收益。“No Pipeline”是通过对流水线第一阶段（第 4.1 节）中所有候选问题来源的 31.6K 个样本取并集而构建的。因此，“No Pipeline”不包含仅从高质量来源中选择问题这一步，不进行问题过滤，使用 DeepSeek-R1 而非 QwQ-32B 作为教师模型，不对每个问题采样多个答案，也不进行任何基于答案的过滤。图 3 进一步逐步拆解了这些选择各自带来的收益。

![图 9](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig09.png)

*图 9：**在每个领域内，OpenThoughts3 数据配方相对于基线都表现出强劲的扩展性**。数学性能为 AIME24、AMC32 和 MATH500 上的平均值。代码性能为 LCB 05/23-05/24、CodeElo 和 CodeForces 上的平均值。科学性能为 GPQA Diamond 和 JEEBench 上的平均值。OpenThoughts3 数学子集和科学子集的最大规模分别为 250K 和 100K。*

#### G.1 基座模型

| 基座模型 | AIME24 | AIME25 | AMC23 | MATH500 | GPQA-D | LCB 05/23-05/24 |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen-2.5-7B-Instruct | **54.3** | **41.0** | **86.8** | **89.0** | **51.0** | 43.7 |
| | **(+39.3)** | **(+33.0)** | (+33.3) | (+18.4) | **(+27.3)** | (+10.7) |
| Llama-3.1-8B-Instruct | 37.0 | 30.3 | 75.2 | 83.8 | 45.1 | **44.4** |
| | (+32.3) | (+30.0) | **(+59.4)** | **(+40.6)** | (+19.3) | **(+31.3)** |

*表 14：**在 OpenThoughts3 的 100k 个样本上微调时，不同基座模型之间的性能比较**。该表展示了微调后的模型取得的绝对性能分数，括号中为相对于各自基座模型的提升。在 OpenThoughts3 数据上训练后，两个微调模型在所有基准上都表现出大幅提升。虽然 Llama-3.1-8B-Instruct 在 AMC23、MATH500 和 LCB 05/23-05/24 上的提升更大，但使用 Qwen-2.5-7B-Instruct 能取得整体最佳性能。*

我们使用 Llama-3.1-8B-Instruct 模型在 OpenThoughts3 上进行训练。该实验表明，我们观察到的扩展收益并不仅限于 Qwen 模型，而且我们的数据集确实具有可扩展性和泛化性。该实验的结果见表 14。总体而言，我们发现在某些数据集上，Llama 模型相比 Qwen 模型获得了更显著的性能提升。这在部分数学数据集上最为突出，例如 AMC23（从 15.8 提升至 75.2）和 MATH500（从 43.2 提升至 83.8），不过起点更强的 Qwen 模型整体表现仍然更好。未来，我们希望将这项研究进一步扩展到更强的模型，例如近期的 Qwen 3 系列模型。

### 附录 H 补充数据配方实验

由于篇幅所限，我们无法在正文中展示全部数据构建消融实验。本节讨论几个有趣的实验，它们让我们对改进推理模型的工具有了更深入的认识。

#### H.1 验证

验证在 OpenThoughts-114K 中发挥了很大作用。我们将在以下各节中考察验证对 OpenThoughts-114K 产生了怎样的影响。

##### H.1.1 验证对原始 OpenThoughts 的影响

验证在 OpenThoughts-114K 和 OpenThoughts2 中扮演了重要角色。然而，OpenThoughts3 并不依赖任何形式的验证。一个自然的问题是：从实证上看，验证对最初的 OpenThoughts 实验究竟有多重要。表 15 展示了这项研究的结果。我们在 OpenThoughts-114K 的未验证版本上分别训练了一个 7B 模型和一个 32B 模型，并评估了未验证模型与原始模型之间的差异。我们的结果表明，验证在 7B 规模上可能损害性能，但在 32B 规模上则有所帮助。

##### H.1.2 移除证明类问题

| 模型 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| --- | --- | --- | --- | --- |
| OpenThinker-32B | **64.5 ± 0.3** | **45.8 ± 0.3** | **83.7 ± 1.0** | **63.7 ± 0.2** |
| OpenThinker-32B-Unverified | 62.1 ± 0.3 | 43.8 ± 0.4 | 81.4 ± 0.9 | 60.5 ± 0.3 |
| OpenThinker-7B-Unverified | **45.0 ± 0.4** | **24.2 ± 0.3** | **64.6 ± 0.9** | **46.9 ± 0.6** |
| OpenThinker-7B | 41.9 ± 0.6 | 21.8 ± 0.5 | 62.0 ± 1.9 | 41.9 ± 0.6 |

*表 15：**验证对原始 OpenThinker 模型的影响**。我们看到，验证在 7B 模型规模上有害，而在 32B 模型规模上有益。*

我们进一步探究验证对 OpenThoughts-114K 的影响。OpenThoughts-114K 中的部分数学问题是证明类问题。这一特点可能会降低我们数值验证的准确性。一个简单的问题是：移除证明类问题能否因验证更加准确而提升下游性能。表 16 给出了这项消融实验的结果。尽管证明类问题无法用我们的方法加以验证，移除它们仍会降低相关基准上的性能。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 数据集 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| OpenThinker-7B | **41.9 ± 0.6** | **21.8 ± 0.5** | **62.0 ± 1.9** | 41.9 ± 0.6 |
| OpenThinker-7B（不含证明题） | 39.4 ± 1.3 | 15.2 ± 2.9 | **60.4 ± 1.0** | **44.2 ± 0.3** |

*表 16：**包含与不包含证明类问题的 OpenThoughts 对比**。剔除证明类问题会使整体性能平均下降 5.6 个百分点。*

##### H.1.3 基于提取的数学验证

我们探索的另一种验证策略是根据答案的正确性来过滤问答对。对于具有已知标准答案的数学样本，我们将模型生成的答案与参考答案进行比较，并丢弃回答错误的样本。然而，模型的最终答案往往嵌在复杂的数学表达式中，提取并评估这一答案并非易事。

为解决这一问题，我们尝试了两种答案提取方法：（i）使用 Hugging Face 的 Math-Verify 工具包；（ii）使用基于 LLM 的提取器（OpenThinker-7B）。

我们分别用这两种方法过滤 OpenThoughts-114K 数据集，并训练下游模型。在评估时，我们再次将 Math-Verify 与 Hendrycks et al. (2021b) 的默认答案提取器进行比较。表 17 汇总了在数据生成与评估所用验证器的不同组合下，AIME25 和 MATH500 这两个基准上的结果。

| 提取方法（训练） | 数据集规模 | 提取方法（评测） | AIME25 | MATH500 |
| --- | --- | --- | --- | --- |
| LLM 评判 | 114K | Hendrycks-Math（默认） | 31.3 | 84.4 |
| LLM 评判 | 114K | HF Math-Verify | **44.0** | **89.0** |
| Math-Verify | 83K | Hendrycks-Math（默认） | 23.0 | 55.0 |
| Math-Verify | 83K | HF Math-Verify | 22.7 | 82.2 |

*表 17：**数学答案验证策略的比较**。我们分别依据基于 LLM 或基于 Math-Verify 的答案正确性来过滤 OpenThoughts-114K 数据集。所得模型同时使用 Hendrycks 和 Math-Verify 两种答案提取工具进行评估。*

##### H.1.4 基于 LLM 生成单元测试的验证

我们研究了利用 LLM 生成的单元测试来过滤代码样本的效果。在由 45,000 个问答对构成的初始数据池中，我们使用 GPT4o-mini 来（1）检测哪些答案包含 Python 代码，以及（2）为每个 Python 样本生成一个独立、可执行的单元测试。随后，我们仅对这些 Python 样本应用“验证”过滤器，非 Python 样本则保持不变。接着，我们在两个各含 16,000 个样本的独立子集上微调 Qwen2.5-7B-Instruct：一个子集经过过滤，只包含生成的测试能够通过的样本；另一个子集则不经过滤、随机抽取。表 18 所示的结果表明，基于 LLM 生成单元测试的验证并不能提高下游代码生成的准确率。

| SFT 数据集 | 基准 | | |
| --- | --- | --- | --- |
| 数据集 | LiveCodeBench | CodeElo | CodeForces |
| 经单元测试验证 | 36.0 | 9.4 | 10.4 |
| 未过滤（随机抽样） | **38.5** | **10.7** | **13.54** |

*表 18：**使用 LLM 生成的单元测试进行代码数据验证的效果**。在 16,000 个代码样本上训练的模型的下游性能：一组经过过滤，只包含通过 LLM 生成单元测试验证的样本；另一组未经过滤。未观察到基于验证的过滤带来任何提升。*

#### H.2 教师模型

在本节中，我们研究将 Claude 3.7（启用思考模式）用作标注模型。首先，我们表明 Claude 的思考轨迹有助于在代码、数学和通用问答上取得更好的性能。在全部三类基准上，更长的思考轨迹都带来了更好的结果。随后我们展示，使用 Claude 3.7 重新标注 S1K Muennighoff et al. (2025) 数据集（数学）以及我们的科学或代码数据，实际上会导致比使用 R1 更差的性能。

![图 10(a)](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig10a.png)

(a) AIME 24

![图 10(b)](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig10b.png)

(b) LiveCodeBench

![图 10(c)](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig10c.png)

(c) GPQA Diamond

*图 10：**在三个基准上，Claude 3.7 的准确率随思考 token 预算的增大而持续提升**。每个子图绘制了多次独立运行（AIME 24 为 5 次，LCB 和 GPQA Diamond 为 3 次）的平均准确率（标记点）及 ±1 个标准误（误差棒）。横轴为思考 token 数，采用对数刻度；答案预算在 AIME 24 上为 1 024 个 token，在 LCB 和 GPQA Diamond 上为 4 096 个 token，且不计入思考 token 预算。AIME 24：准确率从不思考基线的 18.0%（红色菱形）上升到允许模型使用 62 976 个思考 token 时的 51.3%。LCB：性能从 60.5% 稳步攀升，在 28 672 个思考 token 时达到 70.4%。GPQA Diamond：准确率从不思考时的 60.1% 增加到 12 288 个 token 时的 ≈ 76%，此后曲线趋于平稳，说明超过该预算后收益递减。*

**启用思考模式的 Claude 3.7**。Claude 3.7 的 API 接口允许用户为思考 token 的数量设置预算。这使我们能够研究基准性能如何随测试时计算量的增加而演变。图 10 表明，对于所测试的所有任务类型（数学推理、编程和问答），增加测试时间都是有益的。这一点在数学推理和编程上尤为明显；GPQA Diamond 上的性能则更早达到饱和。

**Claude 与 R1 作为代码标注模型的对比**。为评估 Claude 3.7 作为代码标注模型的表现，我们选取 OpenThoughts-114K 数据集，用 Claude 重新标注了从 OpenThoughts-114K 中随机抽取的 10K 个编程问题并加以验证，得到 5.8K 个经过验证的样本。我们将其与 OpenThoughts 的数学和科学部分混合，使所得数据集中代码、数学和科学部分的比例与 OpenThoughts 1 相同。这样就把代码标注模型从 R1 换成了 Claude。表 19 显示，在该实验中，Claude 作为代码标注模型的表现略差。

| 代码标注模型 | AIME24 | GPQA | MATH500 | LiveCodeBench |
| --- | --- | --- | --- | --- |
| R1 | 0.233 | 0.399 | **0.816** | **0.341** |
| Claude | **0.266** | **0.404** | 0.806 | 0.323 |

*表 19：**将代码标注模型从 R1 切换为 Claude 后的得分**。*

**Claude 与 R1 作为科学标注模型的对比**。为评估 Claude 3.7 作为科学标注模型的表现，我们选取 OpenThoughts 1 数据集，用 Claude 重新标注并验证了 OpenThoughts 1 中的科学部分；与上文对代码的处理类似，我们将科学标注模型从 R1 换成了 Claude。表 20 中的结果表明，在这一设置下，Claude 作为科学标注模型的表现略差。

| 科学标注模型 | AIME24 | AIME25 | AMC23 | MATH500 | GPQA | LiveCodeBench |
| --- | --- | --- | --- | --- | --- | --- |
| Claude 3.7 | 0.3733 | 0.2733 | 0.740 | 0.840 | **0.2138** | 0.4207 |
| R1 | **0.3867** | **0.2933** | **0.765** | **0.872** | 0.2121 | **0.4586** |

*表 20：**将科学标注模型从 R1 切换为 Claude 后的得分**。*

**Claude、R1 与 Gemini 作为 S1 标注模型的对比**。为进一步评估数学方面的标注模型，我们选取 S1K 数据集 (Muennighoff et al., 2025)，并用 Claude 和 R1 重新标注了其中的答案和推理轨迹。表 21 显示，使用 R1 标注时性能要好得多。然而，Claude 的标注并未带来同样显著的提升。

| 模型 | AIME24 | AIME25 | MATH500 | GPQA |
| --- | --- | --- | --- | --- |
| Gemini [simplescaling/s1K](https://huggingface.co/datasets/simplescaling/s1K) | **56.7** | 26.7 | 93.0 | 59.6 |
| R1 [simplescaling/s1K-1.1](https://huggingface.co/datasets/simplescaling/s1K-1.1) | **56.7** | **60.0** | **95.4** | **63.6** |
| Claude-3-7 [simplescaling/s1K-claude-3-7-sonnet](https://huggingface.co/datasets/simplescaling/s1K-claude-3-7-sonnet) | 40.0 | – | 87.0 | 51.5 |

*表 21：**将标注模型从 Gemini 切换为 R1 或 Claude 后的得分**。*

#### H.3 压缩推理轨迹

| 设置 | 平均长度 | AIME24 | MATH500 | GPQA | LCB 05/23-05/24 | 平均 |
| --- | --- | --- | --- | --- | --- | --- |
| 基线 | 11593 | **34.0** | **84.0** | **45.6** | **40.7** | **51.4** |
| 无自我反思 | 328 | 5.0 | 61.8 | 31.5 | 19.2 | 26.3 (-49.1%) |
| 过滤 > 2048 | 1343 | 16.7 | 70.2 | 32.3 | 26.9 | 34.2 (-33.3%) |
| 过滤 > 4096 | 2305 | 18.3 | 74.6 | 42.6 | 31.7 | 39.9 (-22.3%) |
| 过滤 > 8192 | 4775 | 22.0 | 79.6 | 44.4 | 30.3 | 42.3 (-17.6%) |

*表 22：**评估压缩推理轨迹对下游性能的作用**。第一行展示了在默认 OpenThoughts3 数据集（12K 个样本）上训练的模型的性能，该数据集的平均推理轨迹长度为 11.5K 个 token。第二行报告了移除自我反思能力后的性能，此时平均轨迹长度降至 0.3K 个 token。后续各行展示了一种过滤策略的结果，该策略会移除推理轨迹长度超过特定阈值（2048、4096 或 8192 个 token）的样本。总体而言，这些结果凸显了自我反思和长推理结构对于在多样化评估基准上取得强劲性能的重要性。*

到目前为止，我们是在预测最终答案之前的长推理轨迹（最长 16K 个 token）上进行监督微调的。近期工作 (Chen et al., 2024; NovaSky-Team, 2025a) 强调了长推理轨迹带来的高昂推理成本，以及推理模型过度思考的倾向。在本节中，我们研究在训练中缩减推理轨迹会如何影响下游性能。我们采用两种方法：（a）从推理轨迹中移除自我反思成分；（b）过滤掉推理轨迹长度超过指定阈值的样本。

为考察第一种方法，我们从 OpenThoughts3 数据集中随机抽取了一个包含 12K 个样本的子集，并确保每个样本都包含完整的思考过程（即推理轨迹中出现了 `<\think>`）。推理轨迹通常很长，原因在于模型的自我反思行为：模型会（重新）分析先前的解法，并为问题提出替代思路。为探究自我反思的作用，我们参照 Deng et al. (2025) 的方法，从推理轨迹中移除“wait”、“but wait”和“but the question”等关键词。这使平均推理轨迹长度从 11.6K 个 token 降至 0.3K 个 token。我们在表 22 中给出了结果。值得注意的是，我们观察到，移除自我反思会使模型在多种下游基准上的性能平均相对下降 49.1%。这些发现表明，自我反思和长篇推理结构对于增强 OpenThoughts3 模型的推理能力至关重要。

我们缩减推理轨迹的第二种方法是过滤掉长度超过给定阈值（例如 2048、4096 或 8192 个 token）的样本。该方法既缩短了推理轨迹的长度，也缩小了数据集的整体规模，同时保留了留存轨迹中的自我反思能力。我们在表 22 中给出了结果。我们观察到，与默认数据集相比，在过滤后数据集上训练的模型的下游性能显著下降。具体而言，filtered-2048 设置使下游基准上的相对性能下降了 33.3%。此外，更高的过滤阈值带来了更好的模型性能。这表明数据集中存在长推理结构是有益的，而仅靠自我反思不足以实现强大的推理性能。尽管如此，事后减少过度思考的能力仍是一个活跃且高度相关的研究领域 (Sui et al., 2025)。

#### H.4 由弱问题导致表现不佳的 SFT 数据集

在对现有 SFT 推理数据集进行基准评测时，我们在来自多个可用来源的完整样本集上微调模型。在我们固定的基准套件上评估下游性能后，我们观察到各数据集的质量差异很大。

| | 基准 | SYNTHETIC-1-SFT-Data | KodCode-V1-SFT-R1 | 全量 vs. 受控 | code\_codegolf | code\_kodcode | code\_stack\_exchange | code\_understanding | real\_world\_swe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 训练集规模 | 894K | 268K | ‖ | 31.6K | 31.6K | 31.6K | 31.6K | 31.6K |
| | 方法 | SFT | SFT | ‖ | SFT | SFT | SFT | SFT | SFT |
| | 平均 | **42.6** | 26.9 | ‖ | 37.3 | 36.2 | 27.3 | 26.9 | 29.8 |
| *数学* | AIME24 | **40.7** | 15.0 | ‖ | 17.7 | 20.3 | 14.0 | 15.7 | 12.3 |
| | AMC23 | **78.5** | 50.5 | ‖ | 58.0 | 56.3 | 52.2 | 50.7 | 52.2 |
| | MATH500 | **87.6** | 71.8 | ‖ | 77.0 | 72.8 | 74.0 | 70.0 | 72.4 |
| | MMLUPro | **31.0** | 28.0 | ‖ | 30.6 | 28.2 | 25.2 | 25.6 | 24.4 |
| *代码* | CodeElo | **17.2** | 7.4 | ‖ | 14.4 | 12.5 | 3.8 | 2.6 | 7.8 |
| | LCB 05/23-05/24 | **48.3** | 39.1 | ‖ | 44.4 | 43.9 | 9.3 | 0.6 | 15.9 |
| | CodeForces | **21.8** | 10.5 | ‖ | 17.2 | 15.3 | 4.4 | 3.2 | 8.4 |
| *科学* | GPQA-D | **45.1** | 31.6 | ‖ | 42.6 | 41.6 | 33.7 | 42.4 | 38.6 |
| | JEEBench | **57.2** | 31.0 | ‖ | 38.8 | 39.3 | 29.5 | 31.9 | 36.3 |

*表 23：**性能比较：全量数据集与受控消融研究**。SYNTHETIC-1-SFT-Data（894K）以 **42.6** 的平均分取得最高性能，显著优于所有受控数据集。在规模受控的 31.6K 数据集中，code\_codegolf 是最佳基线（平均分 37.3），code\_kodcode 也取得了有竞争力的性能（平均分 36.2）。竖线将全量混合数据集与样本量受控的消融实验分隔开来。*

为进一步探究，我们在从每个原始数据集中随机采样的 31,600 个问答对构成的小子集上进行微调，并使用 DeepSeek-R1 重新标注这些问题，所用流程与我们流水线问题来源阶段（第 4.1 节）中所述的流程相同。我们再次观察到下游性能存在显著差异，这似乎主要源于各问题来源在质量和性质上的差异。

#### H.5 叠加域外迁移带来的增益

在第 4 节针对数据集流水线开展实验的过程中，我们清楚地看到推理能力能够跨域迁移。例如，当模型仅在数学推理数据上微调时，其科学评估得分也会提高。我们经常在候选流水线选项之间观察到如此显著的域外性能增益，以至于域内平均性能最高的模型与总体平均性能最高的模型并不是同一个。

我们研究了当所有领域混合在一起时，这些由跨域迁移带来的增益是否依然存在。为此，我们从流水线实验中答案过滤（第 4.5 节）部分选取了以下数据集：在域内科学评估上表现最强的科学推理数据集（最长答案过滤）、在域外科学评估上表现最强的代码推理数据集（最长答案过滤），以及在域外科学评估上表现最弱的代码推理数据集（最短答案过滤）。

随后，我们比较了由该科学数据集分别与两个不同代码数据集组合而成的混合数据集的下游科学性能。两个代码数据集在 GPQA Diamond 得分上的巨大差异，在与强科学数据集混合后并未显现。换言之，在代码数据集上观察到的域外迁移增益，会在混入域内科学数据后消失。

| 微调数据集 | JEE | GPQA-D | LCB 05/23-05/24 | CodeElo | CodeForces |
| --- | --- | --- | --- | --- | --- |
| 科学 | 48.7 | 48.8 | 21.8 | 6.3 | 7.9 |
| 代码（高 GPQA） | 46.6 | 47.3 | 44.6 | 15.9 | 18.9 |
| 代码（低 GPQA） | 44.3 | 36.7 | 45.8 | 15.1 | 19.7 |
| 科学 + 代码（高 GPQA） | 50.4 | 52.7 | 20.2 | 15.3 | 17.6 |
| 科学 + 代码（低 GPQA） | 51.1 | 52.7 | 20.7 | 14.6 | 19.6 |

*表 24：**域外（代码到科学的迁移）增益在与域内（科学）数据集混合后不再保持**。单独的数据集（中线以上）只包含来自该领域的 31K 个样本，混合数据集（中线以下）则包含代码和科学两类共 62K 个样本。将在科学评估上表现强的代码数据集与强科学数据集组合时，下游模型的 GPQA-D 得分与混入在科学评估上表现弱的代码数据集时相比没有差异。*

### 附录 I 模型推理性能分析

#### I.1 不同数学难度下的性能

在开发 OpenThoughts 的过程中，我们探索了使用语言模型按难度过滤数学数据中的问题。我们以 GPT-4o-mini 作为标注模型，将 Sky-T1 NovaSky-Team (2025b) 中的难度标注提示词应用于 Bespoke-Stratos 中的数学问题。该提示词借助示例题目，按 1-10 的等级对问题进行评判，其中一级对应初学者级别的问题，十级对应最难的 IMO 题目。

我们发现，GPT-4o-mini 能够可靠地预测 DeepSeek-R1 会正确回答哪些问题。在最低难度级别（一级）上，R1 的得分超过 75%，而在最高难度级别（十级）上，R1 的得分低于 57%（图 11）。这增强了我们的信心：LLM 标注的难度标签可用于过滤出最难的（因而可能对训练最有用的）问题。

![图 11](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig11.png)

*图 11：GPT-4o-mini 能够可靠地判断问题的相对难度。DeepSeek R1 在最难的问题（难度十级）上的表现明显更差。*

#### I.2 按代码难度划分的性能扩展

在测试 OpenThoughts3 的扩展情况时（见正文图 1），我们注意到在 100K 规模下，所有代码基准上的性能都略有下降。为了更细致地研究这一现象，我们考察了 LiveCodeBench 05/23-05/24，并展示了各难度级别对平均准确率的贡献。我们原本预期会看到简单类别趋于饱和，而困难类别的性能处于很低的水平。出人意料的是，在图 12 中，我们观察到模型在中等和困难任务上的准确率实际上都随规模扩大呈现出良好的上升趋势，而上述轻微下降完全出现在简单类别中。

![图 12](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig12.png)

*图 12：随着数据集规模增大，OpenThoughts3 在 LiveCodeBench 05/23-05/24 上的性能扩展情况。图中展示了每一类问题上的性能贡献。*

#### I.3 按最长、最短、多数进行采样

在采样多个回答时，我们有多种聚合策略来预测最终答案（数值或选择题选项）：（1）“最短”：将最短回答中的答案作为最终答案；（2）“最长”：将最长回答中的答案作为最终答案；（3）“多数”：将多数预测作为最终答案。

我们的实验表明，在不同模型和数据集上，*最短回答策略始终优于最长回答策略*。虽然多数投票往往能取得最佳的整体性能，但最短策略提供了一种有效的单回答选择方法，其表现通常既优于原始采样，也优于最长回答选择。

在 AIME24 数学推理数据集上（表 25），多数投票总体上取得了最佳性能，但对大多数模型而言，最短回答策略仍优于最长策略。如表 1 所示，虽然多数投票取得了最高分（例如 DeepSeek-R1-Distill-Qwen-7B 为 76.67%），但最短策略（66.67%）显著优于最长策略（36.67%）。

| **模型** | **最短** | **最长** | **多数投票** | **原始** |
| --- | --- | --- | --- | --- |
| DeepSeek-R1-Distill-Qwen-7B | 66.67 | 36.67 | **76.67** | 55.00 |
| OpenThinker-7B | **43.33** | 13.33 | **43.33** | 30.33 |
| simplescaling-s1-32B | 40.00 | 30.00 | **46.67** | 35.00 |
| NovaSky-Sky-T1-32B | 30.00 | 26.67 | **43.33** | 30.67 |

*表 25：**AIME24 数据集上各采样策略的性能比较**。“原始”指所有采样结果的平均通过率。*

在 GPQA Diamond 科学推理数据集上，这一趋势更加明显。表 26 展示了我们最全面的一组实验的结果，这组实验的运行次数更多。在大多数模型上，最短策略始终优于最长策略，提升幅度在 7-11 个百分点之间。

| **模型** | **运行次数** | **最短** | **最长** | **多数投票** | **原始** |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-R1-Distill-Qwen-7B | 43 | **51.01** | 43.94 | 29.80 | 48.81 |
| OpenThinker-7B | 81 | **44.44** | 39.39 | 24.75 | 42.28 |
| simplescaling-s1-32B | 44 | **50.00** | 48.99 | 30.30 | 52.79 |
| NovaSky-Sky-T1-32B | 65 | 40.91 | **42.42** | 27.78 | 49.99 |

*表 26：**GPQA Diamond 数据集上的性能比较（高运行次数实验）**。*

**回答长度分析**。在考察回答长度与正确性之间的关系时，一个有趣的规律浮现出来。表 27 展示了原始采样中正确回答与错误回答的平均 token 长度。在大多数模型上，*错误回答往往明显长于正确回答*，这表明冗长的推理实际上可能意味着不确定性或容易出错的推理路径。

| **数据集** | **模型** | **正确** | **错误** | **差值** |
| --- | --- | --- | --- | --- |
| AIME24 | DeepSeek-R1-Distill-Qwen-7B | 7,817 | 18,198 | +10,381 |
| | OpenThinker-7B | 8,966 | 19,517 | +10,551 |
| | simplescaling-s1-32B | 5,048 | 7,481 | +2,433 |
| | NovaSky-Sky-T1-32B | 1,802 | 3,327 | +1,525 |
| GPQA Diamond | DeepSeek-R1-Distill-Qwen-7B | 5,034 | 6,622 | +1,588 |
| | OpenThinker-7B | 7,471 | 8,772 | +1,301 |
| | simplescaling-s1-32B | 3,617 | 3,790 | +173 |
| | NovaSky-Sky-T1-32B | 911 | 896 | -15 |

*表 27：**平均回答长度比较：正确回答与错误回答**。*

最短回答策略的优越性表明，简洁的推理往往能抓住最直接、最正确的求解路径。较长的回答可能意味着模型不确定、在探索多种方法，或迷失在不必要的复杂性之中。这一发现对实际部署具有重要意义，因为如果停止生成全部样本，选择最短回答在计算上是高效的，而且其效果往往优于更复杂的聚合方法。

不过需要指出的是，最短策略并非普遍最优。对于一些模型，例如在某些数据集上的 NovaSky-Sky-T1-32B，其他策略的表现可能更好，这表明最优采样策略可能因模型而异。此外，当计算资源允许生成并聚合多个回答时，多数投票有时能取得最高性能。

### 附录 J 在法律推理中通过蒸馏超越教师模型

在本工作中，我们主要关注数学、科学和编程方面的推理。然而，推理同样可以使其他领域受益，例如法律推理。对于这类领域，开箱即用的推理模型可以通过微调得到显著提升。

我们考虑 Lawma 基准 (Dominguez-Olmedo et al., 2025) 中的一个分类任务，具体而言，我们考虑的任务是将最高法院某份判决意见的意识形态倾向分类为保守、自由或无法确定。这是一项具有挑战性的任务，因为通用模型在该任务上的表现相对较差，例如 GPT4 的表现仅略高于 50%。Dominguez-Olmedo et al. (Dominguez-Olmedo et al., 2025) 提供了 5.44K 个带标签的训练样本以及 1.52K 个带标签的测试样本。

我们考虑三种数据生成策略：i/ 我们在按如下方式得到的数据集上微调 Qwen2.5-7B：选取 2K 个样本，每个样本由 R1 进行 5x 独立标注，并通过多数投票进行验证。只保留结果与多数一致的推理轨迹（10K 条中的 8.3K 条），其余的则被过滤掉。该策略不使用所提供的专家标签。ii/ 我们在按如下方式得到的数据集上微调 Qwen2.5-7B：选取 2K 个样本，每个样本由 R1 进行 5× 独立标注，并用专家标签进行验证，最终得到 7.36K 个经过验证的样本。iii/ 我们在按如下方式得到的数据集上微调 Qwen2.5-7B：选取全部 5.4K 个样本，每个样本由 R1 标注一次，并用专家提供的标签进行验证，最终得到 4.02K 个经过验证的样本。

表 28 列出了在不同数据生成策略下，将最高法院判决意见的意识形态倾向预测为保守、自由或无法确定的准确率。可以看出，所有经过微调的 Qwen2.5-7B 模型都以显著优势超过了规模大得多的标注模型（即 R1）。

这些结果表明，利用像 R1 这样的强教师模型进行微调，再辅以验证，可以为专门任务（例如这一法律推理任务）得到强大的模型。有趣的是，不使用专家标签、而是基于共识/多数验证的微调，其效果几乎与使用专家标签进行验证一样好。

| **模型 / 设置** | **准确率** |
| --- | --- |
| Qwen2.5-7B（未微调） | 0.271 |
| Qwen2.5-7B 在 2K 个样本上微调（由 R1 进行 5× 标注，经多数投票验证） | 0.819 |
| Qwen2.5-7B 在 5.4K 个样本上微调（已标注，已验证） | 0.820 |
| Qwen2.5-7B 在 2K 个样本上微调（由 R1 进行 5× 标注，已验证） | **0.828** |
| R1（标注模型）准确率 | 0.739 |

*表 28：**不同微调设置下的模型性能比较**。*

### 附录 K 所有教师模型的消融实验

我们在表 29 中报告了所有教师模型的基准结果。我们的结果表明，尽管 QwQ-32B 是更强的教师模型，DeepSeek-R1 却是性能最好的模型。Phi-4-Reasoning-Plus 在某些基准上表现也很强，但在代码上表现不佳。这是因为它经常无法输出 Evalchemy 用于提取代码的代码标签，例如 "“‘python"。一个值得注意的数字是，OpenThinker3-7B 在 JEEBench 上超过了 QwQ-32B，这展示了弱到强泛化的一个孤例。

| | 基准 | **OpenThinker3-7B** | deepseek-reasoner | Qwen/QwQ-32B | microsoft/Phi-4-reasoning-plus |
| --- | --- | --- | --- | --- | --- |
| | 平均 | 55.3 | **65.3** | 64.2 | 45.2 |
| *数学* | AIME24 | 69.0 | **76.0** | **78.3** | **76.0** |
| | AMC23 | 93.5 | **98.8** | **98.8** | 96.2 |
| | MATH500 | 90.0 | 89.6 | **90.6** | 84.0 |
| *代码* | CodeElo | 31.0 | **53.7** | 44.3 | 2.4 |
| | LCBv2 | 64.5 | 75.2 | **88.6** | 0.8 |
| | CodeForces | 32.2 | **47.4** | **46.7** | 3.5 |
| *科学* | GPQA-D | 53.7 | **73.7** | 65.0 | 66.8 |
| | JEEBench | 72.4 | **92.3** | 69.9 | 83.5 |
| *留出* | HMMT | 42.7 | 43.0 | 47.7 | **53.0** |
| | HLE | 10.2 | **14.3** | 10.3 | 7.1 |
| | AIME25 | 53.3 | 60.0 | 62.7 | **68.0** |
| | LCBv5 | 51.7 | 60.2 | **67.2** | 0.5 |

*表 29：**OpenThinker3-7B 与各教师模型的比较**。我们看到，从实证结果来看，DeepSeek-R1 总体上是最好的模型，而我们实际使用的教师模型 QwQ-32B 的实证表现则更差。Phi-4-Reasoning-Plus 在代码评测上的实证表现较差，因为它输出代码时不带代码标签，Evalchemy 会将这种输出判为错误。*

### 附录 L OpenThinker 模型的安全性分析

| **模型** | **Harmbench (↓)** | **XSTEST (↓)** |
| --- | --- | --- |
| Qwen2.5-7B-Instruct | 14.5 | 4.4 |
| DeepSeek-R1-Distill-Qwen-7B | 30.5 | 2.4 |
| OpenThinker-7B | 36.8 | 4.4 |
| OpenThinker2-7B | 42.8 | 2.4 |
| OpenThinker3-7B | 55.5 | 5.6 |

*表 30：**OpenThinker 模型在安全性与过度拒绝基准上的性能**。此处我们报告有害率和过度拒绝率。*

在增强开源模型推理能力的过程中，我们力求确保自己的模型拒绝回应不安全的请求，同时遵从良性请求。为此，我们在以下基准上评估 Openthinker 模型的安全能力：

- **XSTEST** Röttger et al. (2023) 由 250 个在句法上与不安全提示词相似的安全提示词组成。我们依据 GPT-4o 将回答判定为拒绝还是遵从，来报告过度拒绝率。
- **Harmbench** Mazeika et al. (2024) 由 400 个基于有害行为的提示词组成，这些有害行为包括网络犯罪、未经授权的入侵、处理受版权保护的材料以及错误信息/虚假信息等。我们使用 GPT-4o 作为评估器，并将获得最高分 5 分的案例所占的比例报告为有害率。

从表 30 中我们观察到，针对推理的监督微调会在无意中削弱 Qwen2.5 模型原有的安全对齐，这与先前的发现 Qi et al. (2023) 一致。在 OpenThinker 系列模型中，OpenThinker-7B 的有害率相对较低（36.8），过度拒绝率处于中等水平（4.4）。在下一代模型中，OpenThinker2-7B 的过度拒绝率略有改善（2.4），但代价是有害性上升（42.8）。OpenThinker3-7B 延续了这一趋势，有害性得分达到最高（55.5），过度拒绝率也小幅上升（5.6）。值得注意的是，OpenThinker3-7B 在训练时没有使用任何显式的安全微调或以对齐为重点的数据，这很可能是其安全性能下降的原因之一。

有趣的是，对比表 30 和 1，我们发现推理能力与安全性之间存在明显的权衡。这些发现凸显了在推理模型中平衡安全性与实用性的挑战 Wang et al. (2025); Bercovich et al. (2025)。OpenThoughts 的后续工作若能引入专门针对安全性的数据集，将有助于在保持其强大推理能力的同时缓解这些风险。

### 附录 M 现有前沿模型的评测

表 31 展示了可通过 API 访问的模型的基准结果。Gemini-2.5-pro 表现最强，尽管它的部分答案为空（因而是错误的），原因是其思考过程过长时会耗尽 token 预算（这在 JEEBench 上尤为明显）。Claude 3.7 的 token 预算设为 32K。o3 使用其默认的中等推理强度。我们的 OpenThinker3-7B 模型平均而言优于分隔线右侧的模型。

| | | gemini-2.5-pro-preview-05-06 | o4-mini-2025-04-16 | o3-2025-04-16 | deepseek-reasoner | claude-3-7-sonnet-thinking | ‖ | gpt-4.1-mini | xai/grok-3 | gpt-4.1-2025-04-14 | gpt-4.1-nano |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | API 提供商 | Google | OpenAI | OpenAI | DeepSeek | Anthropic | ‖ | OpenAI | xAI | OpenAI | OpenAI |
| | 平均 | **69.6** | 67.2 | 67.0 | 63.4 | 56.3 | ‖ | 53.0 | 50.7 | 47.4 | 35.3 |
| *数学* | AIME24 | **92.3** | 81.0 | 80.7 | 76.0 | 47.0 | ‖ | 48.3 | 60.0 | 50.7 | 31.0 |
| | AMC23 | **100.0** | 99.0 | 97.5 | 99.0 | 73.2 | ‖ | 87.5 | 89.8 | 83.2 | 71.7 |
| | MATH500 | **93.8** | 90.8 | 86.0 | 91.6 | 78.2 | ‖ | 88.0 | 85.0 | 83.6 | 79.2 |
| *代码* | CodeElo | **59.5** | 52.9 | 35.2 | 32.1 | 58.4 | ‖ | 29.5 | 29.8 | 31.1 | 8.4 |
| | LCB 05/23-05/24 | 73.7 | 64.8 | **79.2** | 76.6 | 72.0 | ‖ | 72.1 | 32.7 | 65.6 | 39.5 |
| | CodeForces | **57.5** | 55.4 | 37.5 | 47.4 | 56.3 | ‖ | 37.2 | 35.8 | 35.4 | 14.5 |
| *科学* | GPQA-D | **82.5** | 77.9 | 80.0 | 73.7 | 80.8 | ‖ | 64.3 | 66.5 | 34.5 | 46.0 |
| | JEEBench | 44.6 | 80.8 | 86.2 | **88.5** | 71.4 | ‖ | 73.4 | **88.5** | 78.3 | 55.7 |
| *未见* | HMMT | **76.7** | 58.0 | 62.3 | 43.0 | 28.0 | ‖ | 29.7 | 33.3 | 18.7 | 10.0 |
| | HLE | 15.8 | 16.3 | **22.7** | 14.3 | 14.4 | ‖ | 9.5 | 8.6 | 8.4 | 12.6 |
| | AIME25 | **76.3** | 72.3 | 70.3 | 60.0 | 39.7 | ‖ | 41.3 | 50.0 | 33.0 | 23.3 |
| | LCB 06/24-01/25 | 62.3 | 57.5 | **66.8** | 59.0 | 55.7 | ‖ | 55.2 | 28.3 | 46.6 | 31.5 |

*表 31：**当前基于 API 的前沿模型的性能**。当前的开源推理模型与前沿推理模型之间仍存在显著差距。竖线表示按平均基准性能划分的界线，用以区分表现不及和表现优于 OpenThinker3-7B 的模型。差距最大的是 CodeElo、CodeForces 和 GPQA Diamond 等基准。Gemini-2.5-pro 是性能最强的模型。*

### 附录 N 推理鲁棒性测试：Alice in Wonderland 评测

在此，我们以关于 Alice in Wonderland 问题的工作 (Nezhurina et al., 2024) 为基础，这类问题采用简单问题模板的各种变体，这些变体既不改变问题结构，也不改变解答结构。给定一个问题实例 $`P`$ 及其对应的解答 $`S`$、推理（即抽象解答）$`R`$ 和最终答案 $`A`$，对问题陈述施加的推理不变扰动 $`P^{*}_{i}`$ 将具有解答 $`S^{*}_{i}`$ 和答案 $`A^{*}_{i}`$。$`i`$ 表示扰动的任意编号；视问题模板而定，一个问题可以有无穷多个扰动，例如当所变化的变量可取任意自然数时。重要的是，$`P^{*}_{i}`$ 将与原始模板 $`P`$ 具有相同的抽象解答（或推理）$`R`$。具备强泛化能力的模型在求解该问题的所有保持结构的变体时，应表现出相近的性能。

我们通过测量模型对推理不变的问题扰动的敏感度，来检验模型的泛化能力。我们的评测设置遵循 Nezhurina et al. (2024)：将采样温度设为 0.1，采样 100 次，并将最大输出 token 数设为 30720。假设模型在每个变体上的回答服从 β-二项分布，我们求出其均值（平均正确回答率）和方差 σ²。我们将每个模型在每个问题变体上的正确回答率可视化为柱形，并配以相应的误差线来表示方差（图 13）。尽管平均性能有所提升（与非推理模型相比，见图 14），蒸馏推理模型在简单的任务变体上仍表现出大幅波动，这与 Nezhurina et al. (2024) 中的观察结果一致，见图 13。

从图 14 可以清楚地看出，推理模型明显且大幅地优于与之对应的常规 LLM，表现出更高的平均正确回答率。尽管明显的泛化缺陷依然存在，但与以往最先进的（SOTA）LLM 相比，推理模型在各 AIW 问题上都有大幅提升，其中中等规模的推理模型（32B）大幅优于以最大规模训练的 LLM（例如 Llama 3.1 405B 或 DeepSeek v3 671B）。

> **要点：** 蒸馏推理模型虽然相比标准 LLM 有大幅提升，但仍存在泛化缺陷，这一点从其在问题模板的各种自然的、保持问题与解答结构不变的变体上出现的剧烈性能波动中可以明显看出。

![图 13](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig13.png)

*图 13：**蒸馏推理模型表现出泛化缺陷**。所有蒸馏推理模型在 AIW Friends 变体 1-6 Nezhurina et al. (2024) 上都表现出剧烈的性能波动，尽管这些变体完全没有改变问题结构。这表明其存在泛化缺陷。这种波动在同等程度上影响仅经 SFT 训练的推理模型（例如 S1.1 32B、LIMO-32B）和经 SFT+RL 训练的推理模型（例如 Light-R1-32B、QwQ 32B）。较小规模的模型（例如 OpenThinker3-7B）表现不如较大规模的模型（例如 OpenThinker-32B），整体正确回答率更低。较大规模的 32B 模型虽然整体正确回答率更高，但波动剧烈，例如 OpenThinker-32B 在变体 2 和 3 上接近 1，而在变体 1 上则降至接近 0。作为参照，图中还给出了 o1-preview 和 o3-mini，它们的波动小得多，整体正确回答率也更高。蒸馏模型在简单问题上仍不具备鲁棒的零样本泛化能力。图例中的数字为提示词 ID，参见 Nezhurina et al. (2024) 和 [AIW 仓库](https://github.com/LAION-AI/AIW/blob/main/prompts/prompts.json)。*

![图 14](./img/OpenThoughts-Data-Recipes-for-Reasoning-Models-fig14.png)

*图 14：**推理模型优于常规 LLM**。尽管存在剧烈波动，较大规模的蒸馏推理模型仍与作为其蒸馏来源的常规语言模型明显拉开了差距。图中所示为在 AIW Friends、AIW Plus 和 AIW Circles Colleagues 问题 Nezhurina et al. (2024) 的所有变体上取平均的正确回答率。32B 规模的较大推理模型集中分布在正确回答率较高的区间（唯一的例外是 R1-Qwen-32B）。常规 LLM，包括规模最大的 Llama 3.1 405B 和 DeepSeek v3 671B，都局限在正确回答率低于 0.2 的低区间内。作为参照，我们展示了闭源推理模型 o3-mini 和 o1-preview，它们仅有轻微波动，并稳定处于 0.7% 以上的高性能区间。*

### 附录 O 计算资源需求

这项工作的计算需求主要来自三个方面：标注、训练和评估。使用 QwQ-32B 标注 OpenThoughts3-1.2M 需要在 16 个 1xNvidia GH200 节点上耗费 22,000 H100 GPU 小时。训练 OpenThinker3-7B 的单次运行需要在 128 个节点上耗费 25,000 A100 GPU 小时，每个节点配备 4x Nvidia A100 GPU（共 512 块 GPU）。对 OpenThinker3-7B 进行一次评估运行需要在 16 个 1xNvidia GH200 节点上耗费 32 GPU 小时。在整个流水线实验过程中，通过 DeepSeek API 标注每个规模为 31,600 的数据集，API 费用约为 \$300。

### 附录 P 从网络获取推理轨迹

在本工作中，我们使用标注模型生成推理轨迹。作为一种替代方案，我们还尝试了先从网络上寻找推理轨迹，再用语言模型对其进行处理，使其转换为适合 SFT 的形式。这一做法参照了 Yue et al. (2024)，该工作正是以这种方式生成指令微调数据的。

我们在 DCLM-RefinedWeb (Li et al., 2024) 中搜索长推理轨迹。DCLM-RefinedWeb 是一个大型文本语料库，其数据源自 CommonCrawl 文本，并经过了启发式过滤和去重。我们训练了一个 FastText 分类器，以 OpenThoughts-114K 中的推理轨迹作为正样本数据，以等量的 DCLM-RefinedWeb 文本作为负样本数据。随后，我们检查了一些被该 FastText 分类器判定为与推理轨迹最相似的序列（示例见图 15），发现它们与 OpenThoughts-114K 中的长推理轨迹并不相似。这表明，CommonCrawl 并不包含大量与当前推理模型所用推理轨迹相似的长推理轨迹。虽然 CommonCrawl 可能包含有用的问题和答案，这些问答既可以作为基础，用于构建指令微调所需的有效指令-答案对，也可以作为推理轨迹所依据的问题和答案，但 CommonCrawl 似乎并不包含很多长推理轨迹。

```text
Algebra 1
Published by Prentice Hall
ISBN 10: 0133500403
ISBN 13: 978-0-13350-040-0

Chapter 4 - An Introduction to Functions
Chapter Review - 4-2 Patterns and Linear Functions
Page 282:8

Domain: 0, 1, 2, 3
Range: 18, 21, 24, 27

Work Step by Step:
The relationship is between the number of snacks
purchased and the total cost.
If 0 snack is purchased, then the cost is 18.
If 1 snack is purchased, then the cost is 21.
If 2 snacks are purchased, the cost is 24.
If 3 snacks are purchased, then the cost is 27.
We can see a pattern in the range:
each cost term is separated by 3.
So, we can assume that each snack costs 3.00.
Update this answer! Update this answer
```

*图 15：**在 DCLM-Baseline 中找到的推理轨迹示例**。这是在 DCLM-Baseline 中找到的一个推理轨迹示例。这段文本与现代推理模型产生的推理轨迹并不相似。*

### 附录 Q 现有资产的许可证

- **Qwen-2.5-7B-Instruct** 模型采用 Apache 2.0 许可证分发，如 [Qwen-2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) 所示。
- **Open2Math** 数据集采用 Creative Commons Attribution 4.0 许可证分发，如 [openmath-2-math](https://huggingface.co/datasets/ai2-adapt-dev/openmath-2-math) 所示。
- **StackExchange CodeGolf** 数据集采用 cc-by-sa 4.0 许可证分发，如 [StackExchange Data Dump](https://archive.org/details/stackexchange) 所示。
- **OpenCodeReasoning** 数据集采用 cc-by-4.0 许可证分发，如 [OpenCodeReasoning](https://huggingface.co/datasets/nvidia/OpenCodeReasoning) 所示。
- **StackExchange Physics** 数据集采用 cc-by-sa 4.0 许可证分发，如 [StackExchange Data Dump](https://archive.org/details/stackexchange) 所示。
- **OpenAI 模型**依据 [OpenAI Terms of Use](https://openai.com/policies/row-terms-of-use/) 分发。
- **QwQ-32B** 模型采用 Apache license 2.0 分发，如 [QwQ-32B](https://huggingface.co/Qwen/QwQ-32B) 所示。
- **SCP-116K** 数据集采用 cc-by-nc-sa-4.0 许可证分发，如 [SCP-116K](https://huggingface.co/datasets/EricLu/SCP-116K) 所示。
- **Organic Chemistry**（Jonathan Clayden、Nick Greeves 和 Stuart Warren 著）保留所有权利。
- **Organic Chemistry/Fourth Edition**（Francis A. Carey 著）保留所有权利。
- **Organic Chemistry**（John McMurry 著）采用 Creative Commons Attribution Non-Commercial ShareAlike 4.0 International License 分发。
- **Principles of Organic Chemistry**（James Flack Norris 著）受标准版权保护
- **Organic Chemistry**（Robert V. Hoffman 著）保留所有权利
- **March’s Advanced Organic Chemistry**（Michael B. Smith 和 Jerry March 著）保留所有权利。
- **Essentials of Organic Chemistry**（Paul M. Dewick 著）保留所有权利。
- **Fundamentals of Organic Chemistry**（John McMurry 著）保留所有权利。
- **Advanced Organic Chemistry**（Francis A. Carrey 和 Richard J. Sundberg 著）保留所有权利。
- **Introduction to Organic Chemistry** 没有许可证。
- **Principles and Techniques**（作者不详）采用 NCERT - Educational Use Permitted 分发。
- **Organic Chemistry**（Francis A. Carey 著）保留所有权利。
- **A Concise Textbook of Organic Chemistry**（C. G. Lyons、S. McClintock 和 Nora Lumb 著）保留所有权利。
- **The Practical Methods of Organic Chemistry**（Ludwig Gatterman 著）保留所有权利，并适用 Community Resource - Educational Use。
- **Modern Methods of Organic Synthesis**（W. Carruthers 和 Iain Coldham 著）保留所有权利。
- **Organic Chemistry**（J. Clayden、Greeves、Warren 和 Wothers 著）保留所有权利。
- **Techniques in Organic Chemistry**（Jerry R. Mohrig、Christina Hammond 和 Paul Schatz 著）保留所有权利。
- **Organic Chemistry**（David J. Hart、Christopher Hadad、Leslie Craine 和 Harold Hart 著）保留所有权利。
- **Basics of Organic Chemistry: A Textbook for Undergraduate Students**（Anshul Bansal 著）保留所有权利。
- **Advanced Organic Synthesis**（Richard Monson 著）保留所有权利。
- **Chemistry**（Rice University 著）受 Creative Commons Attribution 4.0 International License 约束。

### 附录 R 流水线细节

在本节中，我们将更详细地介绍我们流水线的各个步骤，这些步骤已在第 4 节中简要描述过。

#### R.1 问题生成策略

下面逐一介绍我们生成问题的不同方式。

##### R.1.1 代码问题生成策略

首先，我们详细介绍所有的代码问题生成策略：

- **StackExchange CodeGolf**（问题数量：85.9K）：StackExchange 上一个关于编程谜题的论坛，专门追求字符数尽可能少的解答。
- **OpenCodeReasoning**（问题数量：459K）一个迄今为止规模很大的、面向编程的基于推理的合成数据集，包含 735,255 个 Python 样本，覆盖 28,319 个互不相同的竞赛编程问题
- **cognitivecomputations/dolphin-coder**（问题数量：101K）：由 LeetCode 问题演化而来的合成问题。
- **m-a-p/CodeFeedback-Filtered-Instruction**（问题数量：150K）：经 LLM 过滤的合成编程问题与真实编程问题的混合。
- **KodCode/KodCode-V1**（问题数量：384K）：完全合成且多样化的编程数据集，其中的问题涵盖从算法到特定软件包知识的各类内容。
- **Multilingual-Multimodal-NLP/McEval-Instruct**（问题数量：35.8K）：关于代码理解、补全和生成的多语言代码数据集。
- **christopher/rosetta-code**（问题数量：75.4K）：关于基础编程练习的多语言代码数据集。
- **glaiveai/glaive-code-assistant-v3**（问题数量：946K）：使用 Glaive 的合成数据生成平台生成的代码问题及其解答。
- **StackExchange CodeReview**（问题数量：183K）：来自 codereview.meta.stackexchange.com 的代码审查问题。
- **prithivMLmods/Coder-Stat**（问题数量：41.9K）：用于分析编码模式、错误类型和性能指标的编程数据集。我们使用 GPT-4o-mini 和图 16 中的提示词，将代码及其相关错误转换为一个供 LLM 求解的问题。
- **OpenCoder-LLM/opc-sft-stage2**：由 python 文档、教学材料等内容生成的合成 python 问题的混合。我们同时使用 OpenCoder-LLM/opc-sft-stage2 和 OpenCoder-LLM/opc-sft-stage1。具体而言，我们使用 OpenCoder-LLM/opc-sft-stage2 的 package\_instruct 子集，以及 OpenCoder-LLM/opc-sft-stage1 的 filtered\_infinity\_instruct、largescale\_diverse\_instruct 和 realuser\_instruct 子集。
- **ise-uiuc/Magicoder-OSS-Instruct-75K**（问题数量：73.4K）：使用 gpt-3.5-turbo-1106 生成的编程指令微调数据集。
- **codeparrot/apps**（问题数量：3.7K）：用于根据自然语言规格说明生成代码的 Python 数据集。
- **ajibawa-2023/Code-290k-ShareGPT**（问题数量：283K）：人类向 ChatGPT 提出的有关代码的问题。
- **nampdn-ai/tiny-codes**（问题数量：>1M）：编程问题数据集，这些问题是使用 LLM 将教科书内容转换而成的。
- **bigcode/commitpackft**（问题数量：>1M）：使用 LLM 将 GitHub 上的提交（commit）转换而成的编程问题。具体而言，我们考察 Python、C++、Java、C、C#、CSS、JavaScript、Shell 和 Ruby 的提交。我们使用 GPT-4o-mini 和图 17 中的提示词，让 GPT-4o-mini 将一对提交信息与代码转换为一个问题
- **deepmind/code\_contests**（问题数量：8.8K）：竞赛编程问题。
- **SenseLLM/ReflectionSeq-GPT**（问题数量：9.7K）：一个 Python 数据集，其中的问题是借助 LLM、利用编译器反馈构造而成的。
- **MatrixStudio/Codeforces-Python-Submissions**（问题数量：538K）：来自 CodeForces 网站的编程问题集合。
- **bigcode/self-oss-instruct-sc2-exec-filter-50k**（问题数量：47.6K）：通过使用 LLM 将 GitHub 上的代码片段转换为高难度问题而生成的问题。
- **Magpie-Align/Magpie-Qwen2.5-Coder-Pro-300K-v0.1**（问题数量：299K）：通过让 Qwen2.5 Coder 32B Instruct 生成编程问题而得到的编程问题。
- **PrimeIntellect/real-world-swe-problems**（问题数量：69.6K）：由 PrimeIntellect 生成的真实软件工程（SWE）问题。
- **StackExchange StackOverflow**：来自 StackOverflow 在线论坛的编程问题。
- **cfahlgren1/react-code-instructions**（问题数量：70.4K）：由 LLM 生成的有关 React 框架的问题。
- **PrimeIntellect/stackexchange-question-answering**（问题数量：309K）：基于 StackExchange StackOverflow 构建的问题。
- **PrimeIntellect/synthetic-code-understanding**（问题数量：59.9K）：用于教会 LLM 预测代码片段输出的编程问题。
- **bugdaryan/sql-create-context-instruction**（问题数量：78.6K）：来自 WikiSQL 和 Spider 论坛的 SQL 编程问题。

```text
请根据下面的错误与代码对，为语言模型生成一个问题或任务。

错误类型：{{original_status}}
代码：{{original_src}}

只写出新的问题和任务，不要包含“下面是指令”之类的话。在问题中附上代码，并让任务听起来像是人类会向语言模型提出的请求。
```

*图 16：**Coder Stat 提示词**。*

```text
请根据下面的指令与代码对，为语言模型生成一个问题或任务。

指令：{{message}}
代码：{{old_contents}}

只写出新的问题和任务，不要包含“下面是指令”之类的话。在问题中
附上代码，并让任务听起来像是人类会向语言模型提出的请求。
```

*图 17：**CommitPack 提示词**。*

##### R.1.2 数学问题生成策略

我们还详细介绍所有的数学问题生成策略：

- **ai2-adapt-dev/openmath-2-math**（问题数量：>1M）：OpenMathInstruct2 的 MATH 子集。
- **AI-MO/NuminaMath-1.5**（问题数量：853K）：从竞赛数学题来源中扫描得到的数学问题。
- **GAIR/MathPile**（问题数量：99.5K）：数学文本片段，作为用 GPT-4o-mini 生成数学问题的种子信息。具体而言，MathPile 包含关于各类数学主题的非结构化文本。GPT-4o-mini 使用图 18 中的提示词，将每段文本转换为一个问题。
- **MetaMath-AIME**（问题数量：>1M）：应用于 NuminaMATH 中 AIME 和 AOPS 部分的 MetaMath 流水线。由于原始的 MetaMath 数据集基于 GSM8K 和 MATH 训练集，我们使用 GPT-4o-mini 复现了这一流水线。
- **math-ai/AutoMathText**（问题数量：>1M）：数学文本片段，作为用 GPT-4o-mini 生成数学问题的种子信息。具体而言，math-ai/AutoMathText 包含关于各类数学主题的非结构化文本。GPT-4o-mini 使用图 18 中的提示词，将每段文本转换为一个问题。
- **OpenMathInstruct2-AIME**（问题数量：>1M）：应用于 NuminaMath 中 AIME 和 AOPS 部分的 OpenMathInstruct 流水线。我们只执行 OpenMathInstruct 流水线中的问题增强部分，并使用 GPT-4o-mini 进行增强。
- **zwhe99/DeepMath-103K**（问题数量：95.9K）：从多个不同来源构建、并按难度过滤的数学问题。
- **TIGER-Lab/MathInstruct**（问题数量：256K）：现有数学数据集的混合，其中包含借助 LLM 和 Common-Crawl 生成的问题。
- **nvidia/OpenMathInstruct-2**（问题数量：>1M）：源自 MATH 和 GSM8K 训练集的合成问题。
- **ddrg/named\_math\_formulas**（问题数量：>1M）：数学文本片段，作为用 GPT-4o-mini 生成数学问题的种子信息。具体而言，我们取出每个公式，将其放入图 19 的提示词中，并让 GPT-4o-mini 构造一个问题。
- **facebook/natural\_reasoning**（问题数量：>1M）：从预训练语料库 DCLM 和 FineMath 回译得到的高质量、具有挑战性的推理问题。
- **SynthLabsAI/Big-Math-RL-Verified**（问题数量：45.6K）：经过严格过滤的可验证数学问题。
- **Asap7772/hendrycks-math-mc-llama**（问题数量：79.9K）：未提供详细信息。
- **TIGER-Lab/MATH-plus**（问题数量：847K）：MetaMath、MATH-orca 以及一些额外的、借助 GPT-4 对 MATH 进行增强的数据集的混合。
- **ibivibiv/math\_instruct**（问题数量：>1M）：未提供相关信息。
- **BAAI/InfinityMATH**（问题数量：99.9K）：一个面向程序化数学推理的可扩展指令微调数据集。
- **ajibawa-2023/Maths-College**（问题数量：937K）：涵盖大学数学多个不同领域的问题。
- **MetaMath**（问题数量：>1M）：我们对 MetaMath 的复现。原始的 MetaMath 是用 GPT-3.5-turbo 构建的。在我们的流水线中，我们将其替换为 GPT-4o-mini。
- **allenai/math\_qa**（问题数量：29.7K）：源自 AQuA-RAT 的数学应用题。
- **deepmind/math\_dataset**（问题数量：1M）：大致为中小学水平的数学问题。具体而言，我们使用来自 algebra\_\_linear\_2d\_composed、probability\_\_swr\_p\_level\_set、polynomials\_\_evaluate\_composed、polynomials\_\_simplify\_power、calculus\_\_differentiate\_composed 和 probability\_\_swr\_p\_sequence 子集的问题。
- **Lap1official/Math**（问题数量：>1M）：未提供相关信息。

```text
请把下面这段数学文本改写成一道答案可量化或可验证的题目，例如可以
出现在 USAMO 或 Putnam 竞赛中的题目。

文本：{{text}}

只写出新的问题或任务，不要包含“下面是指令”之类的话。你可以从文本中
提取一道题，也可以根据文本另拟一道新题。让题目听起来像是人类会向语言模型提出的问题。
```

*图 18：**AutoMathText 提示词**。*

```text
请把下面这段数学文本改写成一道答案可量化或可验证的题目，例如可以
出现在 USAMO 或 Putnam 竞赛中的题目。

文本：{{formula}

只写出新的问题或任务，不要包含“下面是指令”之类的话。你可以从文本中
提取一道题，也可以根据文本另拟一道新题。让题目听起来像是人类会向语言模型提出的问题。
```

*图 19：**公式**。*

##### R.1.3 科学问题生成策略

我们还详细介绍所有的科学问题生成策略：

- **StackExchange Physics**（问题数量：547K）：来自 Physics StackExchange 论坛 <https://physics.stackexchange.com> 的问题。
- **有机化学 PDF 流水线**（问题数量：46.2K）：由 LLM 从 SCP PDF 以及更多有机化学教科书中提取的有机化学问题。我们以 SCP-116k 中的 PDF 为起点，同时加入有机化学教科书、习题解答手册等资料。我们使用 gemini/gemini-2.0-flash-lite-preview-02-05 和图 24 中的提示词，从 PDF 中提取文本。随后，GPT-4o-mini 使用图 23 中的提示词，从所提取文本的每一页中提取问题和答案。接着，GPT-4o-mini 使用图 22 中的提示词，将问题精炼为更清晰的问题。然后，GPT-4o-mini 使用图 21 中的提示词，过滤掉与数学、科学和代码无关的问题。我们使用结构化解码来获取一个布尔值形式的分类结果，以及一个字符串形式的推理。之后，GPT-4o-mini 再使用图 20 中的提示词，进一步过滤掉与有机化学无关的问题。在有机化学过滤中，我们采用了与数学、科学和代码问题相同的结构化解码技术。
- **mteb/cqadupstack-physics**（问题数量：38.3K）：一个面向物理学的社区问答研究数据集。我们使用图 25 中的提示词，借助 GPT-4o-mini 将每段非结构化文本转换为一个问题
- **Camel-AI/Physics**（问题数量：>1M）：我们对 Camel 流水线中物理问题的复现。我们使用 GPT-4o-mini 从零开始复现了这一流水线。
- **Josephgflowers/Par-Four-Fineweb-Edu-Fortified-Chemistry-Physics-Astronomy-Math-Reason**（问题数量：988K）：由 LLM 根据 FineWeb 上的科学文本生成的问题。我们使用图 25 中的提示词，借助 GPT-4o-mini 将每段非结构化文本转换为一个问题。
- **millawell/wikipedia\_field\_of\_science**（问题数量：304K）：由 LLM 根据 Wikipedia 科学类文章生成的问题。我们使用图 25 中的提示词，借助 GPT-4o-mini 将每段非结构化文本转换为一个问题。
- **zeroshot/arxiv-biology**（问题数量：1.2K）：由 LLM 利用 Arxiv 生物学论文生成的问题。我们从原始来源中获取摘要，并使用图 26 中的提示词，借助 GPT-4o-mini 将摘要转换为一个问题。
- **Camel-AI/Chemistry**（问题数量：>1M）：我们对 Camel 流水线中化学问题的复现。我们使用 GPT-4o-mini 从零开始复现了这一流水线。
- **StackExchange Biology**（问题数量：60.3K）：来自 Biology StackExchange 论坛 <https://biology.stackexchange.com> 的问题。
- **Camel-AI/Biology**（问题数量：>1M）：我们对 Camel 流水线中生物学问题的复现。我们使用 GPT-4o-mini 从零开始复现了这一流水线。
- **AdapterOcean/biology\_dataset\_standardized\_unified**：（问题数量：22K）未提供相关信息。

```text
请回答是或否：这道题是有机化学题吗？
问题：
{{problem}}
```

*图 20：**有机化学过滤**。*

```text
请回答是或否：这道题是可以作答的高难度科学、数学或编程题吗？如果题目引用了你看不到的内容（图、公式、附加文本），那它就无法作答。
请给出你的理由。
问题：
{{improved_question_solution}}
```

*图 21：**代码、数学和科学问题过滤提示词**。*

```text
你是一位正在出考题的老师。
我会给你一道题，以及这道题提取自的原文。
你要确保这道题可以作答，也就是有足够的上下文来回答它。
为此，你要查看提取出的原文，确保当前这道题的表述没有缺少任何内容。如果有缺失，就先给出补充的文本，再重述题目，但一定要始终把题目本身放在最后。
因为你是在出考题的老师，所以绝不能在补充文本或题目中写出答案。

下面是这项任务的一个示例：
提取出的题目：Calculate the chemical amount (in mol or mmol) of nitric acid that reacts with the
5.000 g sample of this mineral.
提取出的原文：A sample of a different mineral is analysed by the same methods. This mineral also contains only Pb2, CO3, OH, and O2 ions.
When a 5.000 g sample of this mineral is treated with 25.00 mL of 2.000 mol L nitric acid
(HNO3), 0.5214 g of carbon dioxide is released, and 0.01051 mol of the acid remains.
When subjected to thermal decomposition, 5.000 g of this mineral loses 0.5926 g.
(g) Calculate the chemical amount (in mol or mmol) of nitric acid that reacts with the
5.000 g sample of this mineral.

你应该回复我：

A sample of a different mineral is analysed by the same methods. This mineral also contains only Pb2, CO3, OH, and O2 ions.
When a 5.000 g sample of this mineral is treated with 25.00 mL of 2.000 mol L nitric acid
(HNO3), 0.5214 g of carbon dioxide is released, and 0.01051 mol of the acid remains.
When subjected to thermal decomposition, 5.000 g of this mineral loses 0.5926 g. Calculate the chemical amount (in mol or mmol) of nitric acid that reacts with the
5.000 g sample of this mineral.

---

题目如下：{{extracted_question}}
提取出的原文如下：{{output_extraction}}

---

不要包含“下面是改进后的题目”之类的填充语。只写相关信息和题目本身。如果有选项，要列出全部选项。
如果你看到了答案，也不要写进去。这是考试，所以绝对不能在题目中给出最终答案。
```

*图 22：**问题精炼提示词**。*

```text
从下面这份 pdf 中提取出的文本里，抽取题目、答案选项和答案。

按以下格式回复：
QUESTION: “文本中的题目及所有相关上下文，不含答案和选项”（例如，如果题目是“Elvis Presley (a) 最喜欢的三明治是什么？(b) 最讨厌的歌是哪首？(c) 生日是哪天？”，你就应该写出一道题“QUESTION: Elvis Presley 最喜欢的三明治是什么……”，再写出另一道题“QUESTION: Elvis Presley 最讨厌的歌是哪首？……”，依此类推。）
ANSWER CHOICES: “选项 1” ||| “选项 2” ……（如果没有选项，就写 "free response"；如果有选项，请把它们写出来，例如 "A: 0.57 ||| B: John Hancock ||| ..." 等。）
SOLUTION: “正确的选项”或“自由作答题的答案”。如果无法确定正确答案，就写 "NO ANSWER DETECTED"

重要的是，每个 QUESTION: 都必须自成一体，也就是说，单独读到 "QUESTION: ..." 时，你也应该能够回答它。以“Elvis Presley (a) 最喜欢的三明治是什么？(b) 最讨厌的歌是哪首？(c) 生日是哪天？”为例，你不应该写“QUESTION: 最喜欢的三明治？”，因为这样没有意义，而应该写“QUESTION: Elvis Presley 最喜欢的三明治是什么？”
说清楚一点：所有带子问题的题目，都要拆开重述成一道道独立的题，并附上回答每道题所需的全部相关信息。
只拆分子问题。也就是说，只拆分带有 (a) (b) 和 (c) 或 (1) (2) 和 (3) 这类标记的题目；没有标记表明包含多个部分或子问题的题目，请不要拆分。
我们正在建立一个从 pdf 中自动提取题目的题库，所以务必做对。
---
提取出的文本：

{{output_extraction}}
```

*图 23：**问题提取提示词**。*

```text
提取这份 PDF 中的全部文本，包括图片中的所有文字。提取结果的示例可能像这样：
html><body><table><tr><td>2</td><td>1 1</td><td>1 6</td><td>-14</td></tr><tr><td rowspan="2"></td><td>2 3</td><td>7</td><td>14 0</td></tr><tr><td>1</td><td></td><td></td></tr></table></body></html>

Notice that the final sum is zero, telling us that 2 is a zero.  But the nice thing about synthetic division, is that long division, the other coefficients are the coefficients of the quotient polynomial.

The Remainder Theorem states that when dividing a polynomial by a factor of the form $(x-a)$ there is a quotient polynomial and a constant remainder.  The remainder is P(a) since $P(x)=(x-a)\cdot Q(x)+r\Rightarrow P(a)=(a-a)Q(a)+r=r.$ .

# Miscellaneous Facts;

It is obvious in any polynomial that $\mathrm(0)$ is the y-intercept and equally as obvious that $\mathrm(1)$ is the sum of all the coefficients.

# Problems:

1. Given the cubic polynomial $P(x)=x^-7x^-4x+28$ .  Two of the zeros are additive inverses.  Find the zeros.
3. If $\mathrm(\mathbf)$ is a polynomial with rational coefficients and roots at 0, 1, $\sqrt$ , and $1-(\sqrt(3))$ , then the degree of $\mathfrak(p)(\ensuremath(\mathbf(x)))$ is at least?
4. When Madison's dog chewed up her mathematics assignment, one particular equation was ripped apart.  I found a piece of the beginning of the equation and a piece at the end, but the middle was missing.  The beginning piece was $x^(5)-9x^(4)+$ and the ending piece was $+11=0$ .  Fortunately the teacher had promised that all of the roots would be integers.  How many times is $^(-1)$ a root? [Furman ????]
5. The following is a polynomial.  Find the sum of the squares of its coefficients. $\sqrt[3](x^(9)-3x^(8)+18x^(7)-28x^(6)+84x^(5)-42x^(4)+98x^(3)+72x^+15x+1)$ .  FURMAN
6. If a cubic polynomial $\operatorname(p)(\mathbf(x))$ has roots at -1, 2, and 3, and if $\mathfrak(p)(0)=1$ , then the remainder when $\mathfrak(p)(\ensuremath(\mathbf(x)))$ is divided by $\mathbf(X)-1$ is:
7. If 2 is a solution of $x^(3)+h x+10=0$ , then h equals:
8. The number of distinct real solutions of the equation $4x^(3)-8x^(2)+5x-1=0$ is:
9. What is the sum of the squares of the roots of $x^(4)-5x^(2)+6=0$
10. For how many integers $_\mathrm(N)$ is $N^(4)+6N<6N^(3)+N^(2)?$
11. How any times does the graph of $f(x)=x^(3)-x^(2)+2x+4$ cross the $\mathbf(X)$ axis?
12. Madison's dog chewed on her homework before she could finish it.  The fragment saved from the horrible canine's mouth reveal only the two terms of highest degree of the polynomial $\mathfrak(p)(\ensuremath\mathbf(x)))$

现在请给出你提取的全部文本，包括图片中的文字。
```

*图 24：**Gemini OCR 提示词**。*

```text
请把下面这段数学文本改写成一道答案可量化或可验证的题目，例如可以
出现在生物、物理或化学奥林匹克竞赛中的题目。
文本：{{text}}

只写出新的问题或任务，不要包含“下面是指令”之类的话。你可以从文本中
提取一道题，也可以根据文本另拟一道新题。让题目听起来像是人类会向语言模型提出的问题。
```

*图 25：**用于生成科学问题的提示词**。*

```text
请把下面这段数学文本改写成一道答案可量化或可验证的题目，例如可以
出现在生物、物理或化学奥林匹克竞赛中的题目。
文本：{{abstract}}

只写出新的问题或任务，不要包含“下面是指令”之类的话。你可以从文本中
提取一道题，也可以根据文本另拟一道新题。让题目听起来像是人类会向语言模型提出的问题。
```

*图 26：**用于生成科学问题的提示词**。*

#### R.2 问题过滤策略的相关信息

接下来，我们将更详细地介绍所用的问题过滤策略。

##### R.2.1 FastText 细节

下面补充介绍我们所用 FastText 过滤器的一些细节。

- 我们所用 FastText 过滤器的隐藏维度为 256。
- 我们将分类器训练 3 个 epoch。
- 我们使用的学习率为 0.1。
- 我们使用二元语法（bigram），即 n = 2。
- 我们使用的最小 n-gram 计数为 3。

##### R.2.2 代码过滤策略

下面给出我们代码过滤策略的更多细节。

- **基于难度的选择**：让 GPT-4o-mini 依据针对 ICPC 题目的评分标准，在 1 到 10 的范围内为问题评分，并选取被评为最难的题目。在让 GPT-4o-mini 协助进行问题过滤时，我们仅将温度设为 1.0。我们没有设置其他采样超参数。难度过滤所用的提示词见图 27。我们使用结构化解码从 GPT-4o-mini 中提取数值回答。对于 AskLLM 过滤，我们要求返回一个整数形式的数值回答，以及一个字符串形式的推理回答。
- **基于长度的选择（GPT-4.1-nano）**：使用 GPT-4.1-Nano 标注问题，并保留回答最长的问题。
- **AskLLM 选择**：让 GPT-4o-mini 在 1 到 100 的范围内打分，评估一个问题与一组优质问题有多相似、与一组劣质问题有多不同。在让 GPT-4o-mini 协助进行问题过滤时，我们仅将温度设为 1.0。我们没有设置其他采样超参数。AskLLM 过滤所用的提示词见图 28。我们使用结构化解码从 GPT-4o-mini 中提取数值回答。对于 AskLLM 过滤，我们要求返回一个整数形式的数值回答，以及一个字符串形式的推理回答。
- **基于长度的选择（GPT-4o-mini）**：使用 GPT-4o-mini 标注问题，并保留回答最长的问题。
- **FastText（正例：Codeforces；负例：CodeReview）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 CodeForces，负样本为来自 StackExchange Code Review 的问题。更多信息见第 R.2.1 节。
- **基于长度的选择（GPT-4.1-mini）**：让 GPT-4.1-mini 在 1 到 100 的范围内打分，评估一个问题与一组优质问题有多相似、与一组劣质问题有多不同。
- **随机选择**：随机选择问题。
- **FastText（正例：LeetCode；负例：SQL）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本来自 LeetCode，负样本为来自 bugdaryan/sql-create-context-instruction 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：Code Golf；负例：SQL）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本来自 StackExchange Code Golf，负样本为来自 bugdaryan/sql-create-context-instruction 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：全部；负例：SQL）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本来自 CodeForces、LeetCode、Code Golf 和 IOI，负样本为来自 bugdaryan/sql-create-context-instruction 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：IOI；负例：SQL）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本来自 IOI，负样本为来自 bugdaryan/sql-create-context-instruction 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：Codeforces；负例：全部）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 CodeForces，负样本为来自 StackExchange Code Review 和 bugdaryan/sql-create-context-instruction 的问题。更多信息见第 R.2.1 节。
- **FastText 选择（正例：Codeforces；负例：SQL）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 CodeForces，负样本为来自 bugdaryan/sql-create-context-instruction 的问题。更多信息见第 R.2.1 节。
- **基于嵌入的选择**：使用 OpenAI 的嵌入模型 text-embedding-3-large，对一组正样本和一组负样本进行嵌入，其中正样本为 CodeForces，负样本为 bugdaryan/sql-create-context-instruction。首先，对给定问题进行嵌入，并计算其与正样本的平均余弦相似度以及与负样本的平均余弦相似度，然后通过取二者之差生成最终得分。

```text
你会拿到一道编程题。你的任务是按照 ICPC 标准，给它评定 1-10 级的难度。
标准如下：
ICPC 题目的 10 级难度量表可以这样划分，其中 1 级代表最简单的题，10 级代表最难的题：
1 级：基础实现题，只需简单的输入/输出处理和直接的计算。通常用一个循环或基本的条件语句就能解决。例如对一组数求和，或找出数组中的最大值。
2 级：涉及数组、字符串等基本数据结构的题，需要线性查找或基础排序之类的简单算法。可能包含素数或基础几何之类的简单数学概念。
3 级：需要掌握标准算法的题，如二分查找、完整的排序算法或基本的图遍历（DFS/BFS）。可能包含状态转移清晰的简单动态规划题。
4 级：综合多个基础概念的题，需要细致的实现和适度的优化。包括中等难度的动态规划题和最短路之类的基本图算法。
5 级：需要扎实掌握线段树、树状数组或并查集等数据结构的题。可能包含最小生成树或网络流基础之类较复杂的图算法。
6 级：状态表示不明显的高级动态规划题；需要组合多种算法或数据结构的题。可能包含基础博弈论或基础数论概念。
7 级：需要高级算法知识的题，如树链剖分、后缀数组或高级几何算法。包括复杂的优化问题和更难的网络流应用。
8 级：需要深刻的数学洞察并结合复杂算法实现的题。可能包含高级数论、复杂的几何算法，或需要多个不明显观察的题。
9 级：需要广泛掌握高级算法和数学概念的题，往往需要多个关键洞察才能解出。可能包含后缀自动机之类的高级字符串算法，或复杂的数学优化。
10 级：最难的题，往往需要标准竞赛编程资料中没有的新方法或新洞察。这类题可能以不明显的方式组合多个高级概念，需要复杂的正确性证明，或需要高度优化的实现才能满足严格的时间限制。
这个量表大致对应从早期区域赛（1-4 级）到区域决赛（4-7 级）再到世界总决赛题目（7-10 级）的难度递进。
待标注的题目：{{question}}."
```

*图 27：**代码难度过滤的提示词**。这段文本是代码难度过滤所用的提示词。*

```text
我想请你判断下面这道题更像给出的正例，还是更像负例。下面是几道正例题目：

正例题目
1. A plane contains $40$ lines, no $2$ of which are parallel. Suppose that there are $3$ points where exactly $3$ lines intersect, $4$ points where exactly $4$ lines intersect, $5$ points where exactly $5$ lines intersect, $6$ points where exactly $6$ lines intersect, and no points where more than $6$ lines intersect. Find the number of points where exactly $2$ lines intersect.
2. A spin-half particle is in a linear superposition0.8|\uparrow\rangle+0.6|\downarrow\rangle of its spin-up and spin-down states. If |\uparrow\rangle and |\downarrow\rangle are the eigenstates of \sigma_{z} , then what is the expectation value up to one decimal place, of the operator 10\sigma_{z}+5\sigma_{x} ? Here, symbols have their usual meanings.
3. An established group of scientists are working on finding solution to NP hard problems. They claim Subset Sum as an NP-hard problem. The problem is to determine whether there exists a subset of a given set S whose sum is a given number K. You are a computer engineer and you claim to solve this problem given that all numbers in the set are non-negative. Given a set S of size N of non-negative integers, find whether there exists a subset whose sum is K. Input First line of input contains T, the number of test cases. T test cases follow. Each test case contains 2 lines. First line contains two integers N and K. Next line contains N space separated non-negative integers (each less than 100000). 0 < T < 1000 0 < N < 1000 0 < K < 1000 Output Output T lines, one for each test case. Every line should be either 0 or 1 depending on whether such a subset exists or not. Example Input: 2 5 10 3 4 6 1 9 3 2 1 3 4 Output: 1 0
4. Let $S$ be the set of positive integer divisors of $20^9.$ Three numbers are chosen independently and at random with replacement from the set $S$ and labeled $a_1,a_2,$ and $a_3$ in the order they are chosen. The probability that both $a_1$ divides $a_2$ and $a_2$ divides $a_3$ is $\tfrac{m}{n},$ where $m$ and $n$ are relatively prime positive integers. Find $m.$
5. What is the concentration of calcium ions in a solution containing 0.02 M stoichiometric Ca-EDTA complex (we assume that the pH is ideal, T = 25C). KCa-EDTA = 5x10\^10.

负例题目：
1. Solve 0 = 19*z - 17*z for z.
2. Simplify ((-2*(-2*sqrt(1210) - sqrt(1210) - sqrt(20)/sqrt(2)*-6))/((sqrt(1800)*2 + sqrt(1800) + sqrt(1800) + sqrt(1800))*-1)*3)**2.\n
3. Given a list of objects that have an `is_organized` method that returns a boolean value, write a Python function that takes the list and returns a new list of those objects for which `is_organized` returns True.
4. Can you provide a Python code snippet that demonstrates how to use a decorator to log the execution time of a function?
5. Is sodium hydroxide (NaOH) an acid or base?

下面是你要判断的题目：
{{question}}

返回一个 1 到 100 之间的分数，100 表示和正例完全一样，1 表示和负例完全一样。
```

*图 28：**AskLLM 过滤的提示词**。这段文本是 AskLLM 过滤所用的提示词。*

##### R.2.3 数学问题过滤

- **基于长度的选择（GPT-4.1-nano）**：使用 GPT-4.1-Nano 标注问题，并保留回答最长的问题。
- **AskLLM 选择**：让 GPT-4o-mini 在 1 到 100 的范围内打分，评估一个问题与一组优质问题有多相似、与一组劣质问题有多不同。在让 GPT-4o-mini 协助进行问题过滤时，我们仅将温度设为 1.0。我们没有设置其他采样超参数。AskLLM 过滤所用的提示词见图 28。我们使用结构化解码从 GPT-4o-mini 中提取数值回答。对于 AskLLM 过滤，我们要求返回一个整数形式的数值回答，以及一个字符串形式的推理回答。
- **随机选择**：随机选择问题。
- **基于嵌入的选择**：使用 OpenAI 的嵌入模型 text-embedding-3-large，对一组正样本和一组负样本进行嵌入，其中正样本为 AI-MO/NuminaMath-CoT 的“amc\_aime”和“olympiads”子集，负样本为 Lap1official/Math。首先，对给定问题进行嵌入，并计算其与正样本的平均余弦相似度以及与负样本的平均余弦相似度，然后通过取二者之差生成得分。
- **FastText（正例：S1.1；负例：Lap1official）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为来自 S1 的问题，负样本为来自 Lap1official/Math\_small\_corpus 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：Olympiad；负例：Lap1official）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为来自 brando/olympiad-bench-imo-math-boxed-825-v2-21-08-2024 的问题，负样本为来自 Lap1official/Math\_small\_corpus 的问题。更多信息见第 R.2.1 节。
- **基于难度的选择**：让 GPT-4o-mini 依据针对 AOPS 题目的评分标准，在 1 到 10 的范围内为问题评分，并选取被评为最难的题目。在让 GPT-4o-mini 协助进行问题过滤时，我们仅将温度设为 1.0。我们没有设置其他采样超参数。难度过滤所用的提示词见图 29。我们使用结构化解码从 GPT-4o-mini 中提取数值回答。对于 AskLLM 过滤，我们要求返回一个整数形式的数值回答，以及一个字符串形式的推理回答。
- **FastText（正例：OpenR1；负例：Lap1official）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 open-r1/OpenR1-Math-220K 中的问题，负样本为来自 Lap1official/Math\_small\_corpus 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：全部；负例：Lap1official）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 AI-MO/NuminaMath-CoT 的“amc\_aime”和“olympiads”子集、brando/olympiad-bench-imo-math-boxed-825-v2-21-08-2024、open-r1/OpenR1-Math-220K 以及 S1，负样本为来自 Lap1official/Math\_small\_corpus 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：Numina；负例：全部）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 AI-MO/NuminaMath-CoT 的“amc\_aime”和“olympiads”子集，负样本为来自 Lap1official/Math\_small\_corpus 和 facebook/natural\_reasoning 的问题。更多信息见第 R.2.1 节。
- **FastText（正例：Numina；负例：Natural Reasoning）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 AI-MO/NuminaMath-CoT 的“amc\_aime”和“olympiads”子集，负样本为来自 facebook/natural\_reasoning 的问题。更多信息见第 R.2.1 节。
- **基于长度的选择（GPT-4o-mini）**：使用 GPT-4o-mini 标注问题，并保留回答最长的问题。
- **基于长度的选择（GPT-4.1-mini）**：使用 GPT-4.1-mini 标注问题，并保留回答最长的问题。
- **FastText 选择（正例：Numina；负例：Lap1official）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为 AI-MO/NuminaMath-CoT 的“amc\_aime”和“olympiads”子集，负样本即来自 Lap1official/Math\_small\_corpus 的问题。更多信息见第 R.2.1 节。

```text
你会拿到一道数学题。你的任务是按照 AoPS 标准，给它评定 1-10 级的难度。 \
标准如下： \
All levels are estimated and refer to averages. The following is a rough standard based on the USA tier system AMC 8 - AMC 10 - AMC 12 - AIME - USAMO/USAJMO - IMO, \
representing Middle School - Junior High - High School - Challenging High School - Olympiad levels. Other contests can be interpolated against this. \
Notes: \
Multiple choice tests like AMC are rated as though they are free-response. Test-takers can use the answer choices as hints, and so correctly answer more AMC questions than Mathcounts or AIME problems of similar difficulty. \
Some Olympiads are taken in 2 sessions, with 2 similarly difficult sets of questions, numbered as one set. For these the first half of the test (questions 1-3) is similar difficulty to the second half (questions 4-6). \
Scale \
1: Problems strictly for beginners, on the easiest elementary school or middle school levels (MOEMS, MATHCOUNTS Chapter, AMC 8 1-20, AMC 10 1-10, AMC 12 1-5, and others that involve standard techniques introduced up to the middle school level), most traditional middle/high school word problems. \
2: For motivated beginners, harder questions from the previous categories (AMC 8 21-25, harder MATHCOUNTS States questions, AMC 10 11-20, AMC 12 5-15, AIME 1-3), traditional middle/high school word problems with extremely complex problem solving. \
3: Advanced Beginners problems that require more creative thinking (harder MATHCOUNTS National questions, AMC 10 21-25, AMC 12 15-20, AIME 4-6). \
4: Intermediate-level problems (AMC 12 21-25, AIME 7-9). \
5: More difficult AIME problems (10-12), simple proof-based Olympiad-style problems (early JBMO questions, easiest USAJMO 1/4). \
6: High-leveled AIME-styled questions (13-15). Introductory-leveled Olympiad-level questions (harder USAJMO 1/4 and easier USAJMO 2/5, easier USAMO and IMO 1/4). \
7: Tougher Olympiad-level questions, may require more technical knowledge (harder USAJMO 2/5 and most USAJMO 3/6, extremely hard USAMO and IMO 1/4, easy-medium USAMO and IMO 2/5). \
8: High-level Olympiad-level questions (medium-hard USAMO and IMO 2/5, easiest USAMO and IMO 3/6). \
9: Expert Olympiad-level questions (average USAMO and IMO 3/6). \
10: Historically hard problems, generally unsuitable for very hard competitions (such as the IMO) due to being exceedingly tedious, long, and difficult (e.g. very few students are capable of solving on a worldwide basis). \
Examples \
For reference, here are problems from each of the difficulty levels 1-10: \
<1: Jamie counted the number of edges of a cube, Jimmy counted the numbers of corners, and Judy counted the number of faces. They then added the three numbers. What was the resulting sum? (2003 AMC 8, Problem 1) \
1: How many integer values of $x$ satisfy $|x| < 3\pi$? (2021 Spring AMC 10B, Problem 1) \
2: A fair $6$-sided die is repeatedly rolled until an odd number appears. What is the probability that every even number appears at least once before the first occurrence of an odd number? (2021 Spring AMC 10B, Problem 18) \
3: Triangle $ABC$ with $AB=50$ and $AC=10$ has area $120$. Let $D$ be the midpoint of $\overline{AB}$, and let $E$ be the midpoint of $\overline{AC}$. The angle bisector of $\angle BAC$ intersects $\overline{DE}$ and $\overline{BC}$ at $F$ and $G$, respectively. What is the area of quadrilateral $FDBG$? (2018 AMC 10A, Problem 24) \
4: Define a sequence recursively by $x_0=5$ and\[x_{n+1}=\frac{x_n^2+5x_n+4}{x_n+6}\]for all nonnegative integers $n.$ Let $m$ be the least positive integer such that\[x_m\leq 4+\frac{1}{2^{20}}.\]In which of the following intervals does $m$ lie? \
$\textbf{(A) } [9,26] \qquad\textbf{(B) } [27,80] \qquad\textbf{(C) } [81,242]\qquad\textbf{(D) } [243,728] \qquad\textbf{(E) } [729,\infty)$ \
(2019 AMC 10B, Problem 24 and 2019 AMC 12B, Problem 22) \
5: Find all triples $(a, b, c)$ of real numbers such that the following system holds:\[a+b+c=\frac{1}{a}+\frac{1}{b}+\frac{1}{c},\]\[a^2+b^2+c^2=\frac{1}{a^2}+\frac{1}{b^2}+\frac{1}{c^2}.\](JBMO 2020/1) \
6: Let $\triangle ABC$ be an acute triangle with circumcircle $\omega,$ and let $H$ be the intersection of the altitudes of $\triangle ABC.$ Suppose the tangent to the circumcircle of $\triangle HBC$ at $H$ intersects $\omega$ at points $X$ and $Y$ with $HA=3,HX=2,$ and $HY=6.$ The area of $\triangle ABC$ can be written in the form $m\sqrt{n},$ where $m$ and $n$ are positive integers, and $n$ is not divisible by the square of any prime. Find $m+n.$ (2020 AIME I, Problem 15) \
7: We say that a finite set $\mathcal{S}$ in the plane is balanced if, for any two different points $A$, $B$ in $\mathcal{S}$, there is a point $C$ in $\mathcal{S}$ such that $AC=BC$. We say that $\mathcal{S}$ is centre-free if for any three points $A$, $B$, $C$ in $\mathcal{S}$, there is no point $P$ in $\mathcal{S}$ such that $PA=PB=PC$. \
Show that for all integers $n\geq 3$, there exists a balanced set consisting of $n$ points. \
Determine all integers $n\geq 3$ for which there exists a balanced centre-free set consisting of $n$ points. \
(IMO 2015/1) \
8: For each positive integer $n$, the Bank of Cape Town issues coins of denomination $\frac1n$. Given a finite collection of such coins (of not necessarily different denominations) with total value at most most $99+\frac{1}{2}$, prove that it is possible to split this collection into $100$ or fewer groups, such that each group has total value at most $1$. (IMO 2014/5) \
9: Let $k$ be a positive integer and let $S$ be a finite set of odd prime numbers. Prove that there is at most one way (up to rotation and reflection) to place the elements of $S$ around the circle such that the product of any two neighbors is of the form $x^2+x+k$ for some positive integer $x$. (IMO 2022/3) \
10: Prove that there exists a positive constant $c$ such that the following statement is true: Consider an integer $n > 1$, and a set $\mathcal S$ of $n$ points in the plane such that the distance between any two different points in $\mathcal S$ is at least 1. It follows that there is a line $\ell$ separating $\mathcal S$ such that the distance from any point of $\mathcal S$ to $\ell$ is at least $cn^{-1/3}$. \
(A line $\ell$ separates a set of points S if some segment joining two points in $\mathcal S$ crosses $\ell$.) (IMO 2020/6)
待标注的题目：{{question}}"
```

*图 29：**数学难度过滤的提示词**。这段文本是数学难度过滤所用的提示词。*

##### R.2.4 科学问题过滤

- **FastText（正例：ExpertQA；负例：Arxiv）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为来自 katielink/expertqa 的问题，负样本为来自 AdapterOcean/biology\_dataset\_standardized\_unified 的问题。更多信息见第 R.2.1 节。
- **基于长度的选择（GPT-4o-mini）**：使用 GPT-4o-mini 标注问题，并保留回答最长的问题。
- **基于长度的选择（GPT-4.1-nano）**：使用 GPT-4.1-Nano 标注问题，并保留回答最长的问题。
- **基于长度的选择（GPT-4.1-mini）**：使用 GPT-4.1-mini 标注问题，并保留回答最长的问题。
- **AskLLM 选择**：让 GPT-4o-mini 在 1 到 100 的范围内打分，评估一个问题与一组优质问题有多相似、与一组劣质问题有多不同。在让 GPT-4o-mini 协助进行问题过滤时，我们仅将温度设为 1.0。我们没有设置其他采样超参数。AskLLM 过滤所用的提示词见图 28。我们使用结构化解码从 GPT-4o-mini 中提取数值回答。对于 AskLLM 过滤，我们要求返回一个整数形式的数值回答，以及一个字符串形式的推理回答。
- **FastText（正例：SciQ；负例：Wikipedia + Arxiv）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为来自 allenai/sciq 的问题，负样本为来自 AdapterOcean/biology\_dataset\_standardized\_unified 的问题，以及按第 R.1.3 节所述方式从 millawell/wikipedia\_field\_of\_science 生成的问题。更多信息见第 R.2.1 节。
- **基于嵌入的选择**：使用 OpenAI 的嵌入模型 text-embedding-3-large，对一组正样本和一组负样本进行嵌入，其中正样本为来自 allenai/sciq 的问题，负样本为 AdapterOcean/biology\_dataset\_standardized\_unified。首先，对给定问题进行嵌入，并计算其与正样本的平均余弦相似度以及与负样本的平均余弦相似度，然后通过取二者之差生成一个得分。
- **FastText（正例：SCP、ExpertQA、SciQ；负例：Arxiv）**：使用 FastText 分类器对问题进行分类，训练该分类器所用的正样本为来自 allenai/sciq、EricLu/SCP-116K 和 katielink/expertqa 的问题，负样本为来自 AdapterOcean/biology\_dataset\_standardized\_unified 的问题，以及按第 R.1.3 节所述方式从 millawell/wikipedia\_field\_of\_science 生成的问题。更多信息见第 R.2.1 节。
- **随机选择**：随机选择问题。
- **基于难度的选择**：让 GPT-4o-mini 依据针对科学奥林匹克竞赛题目的评分标准，在 1 到 10 的范围内为问题评分，并选出被评为最难的题目。在让 GPT-4o-mini 协助进行问题过滤时，我们仅将温度设为 1.0。我们没有设置其他采样超参数。难度过滤所用的提示词见图 30。我们使用结构化解码从 GPT-4o-mini 中提取数值回答。对于 AskLLM 过滤，我们要求返回一个整数形式的数值回答，以及一个字符串形式的推理回答。

```text
你会拿到一道科学题。你的任务是按照国际科学奥林匹克竞赛的标准，给它评定 1-10 级的难度。 \
标准如下： \
国际科学奥林匹克竞赛题目的 10 级难度量表可以这样划分，其中 1 级代表最简单的题，10 级代表最难的题：
1 级：基础知识应用——直接回忆基本的科学事实和原理；只需基本公式的简单计算；直接应用单一的科学概念；题目通常 1-2 步就能解出；内容通常属于标准高中课程。例如识别简单的化合物、基础电路计算或对生物进行分类。
2 级：多步骤的基础应用——需要 2-3 个不同步骤才能解出的题；在单一领域内应用多个基础概念；从图表中做基本的数据解读；简单的实验技术和测量；内容通常出现在高中进阶课程中。例如化学计量计算、基础运动学题，或分析简单的生物过程。
3 级：标准概念的进阶应用——综合多个科学概念；包含多步计算的中等定量推理；需要分析性思维的实验数据解读；需要超越记忆的深入理解；是有挑战性的高中科学竞赛题的典型水平。例如结合热力学与动力学的题、多步骤的力学题，或生态关系分析。
4 级：国家级奥赛初期水平——需要特定科学领域专门知识的题；应用常规课程通常不涉及的进阶概念；中等水平的实验技术和对实验设计的理解；解题路径不明显、需要分析性思维；是国家科学奥赛早期轮次的典型水平。例如含多个变量的化学平衡题、含非理想元件的电路分析，或分子生物学机制。
5 级：国家级奥赛标准——综合多个科学领域概念的题；在非标准情境中创造性地应用标准原理；分析复杂的实验装置和数据；有多个需要洞察力的概念难点；是国家奥赛决赛的典型水平。例如复杂的有机合成路线、非理想热力学体系，或高级遗传学问题。
6 级：国家级高阶/国际级入门水平——需要超出标准课程的深刻概念理解的题；把理论知识与实际实验技术结合起来；有多种可行思路的创造性解题；把数学模型应用于复杂的科学现象；是国际奥赛集训营的典型水平。例如量子力学模型、复杂的生化途径，或生物系统的统计分析。
7 级：国际奥赛标准——达到 IChO、IPhO 或 IBO 理论考试水平的题；需要专门知识与创造性洞察相结合；对科学现象进行复杂的定量建模；跨学科地综合概念；有多个需要系统分析的概念层次。例如高级光谱解析、受多种力作用的复杂物理系统，或详细的生化机制分析。
8 级：国际奥赛高阶——需要兼具广度和深度的科学知识的题；以通常不会教授的新颖方式应用科学原理；精巧的实验设计与分析；有多条需要评估和取舍的解题路径；是有挑战性的国际奥赛题的典型水平。例如有难度的量子化学题、含多个变量的高级实验方案，或复杂的进化或生态模型。
9 级：国际奥赛精英水平——需要非凡科学洞察力和创造力的题；融合前沿科学知识；解题需要多个概念上的突破；连最有天赋的学生也会觉得有挑战；只出现在国际竞赛最难的题目中。例如物理原理的新颖应用、需要考虑立体化学的复杂多步合成，或系统生物学分析。
10 级：历史级难题——科学竞赛中难度传奇的题；需要超越标准方法论的创新思路；可能融合大学阶段的高级概念；全世界只有极少数参赛者能完整解出；常作为奥赛史上的特别难题被人记住。例如需要开创新方法的题，或在某一年难倒了几乎所有参赛者的题。

这个量表大致对应从校级科学竞赛（1-3 级）到国家选拔赛（4-5 级）再到国际奥赛题目（6-10 级）的难度递进。

分学科说明：
物理（IPhO）：1-3 级涵盖标准的高中物理内容（力学、电学、热力学）；4-6 级包括波动光学、基础量子物理和非理想系统等进阶主题；7-10 级纳入大学水平的内容，包括量子力学、统计物理和相对论。

化学（IChO）：1-3 级涵盖无机、有机和分析化学的基本概念；4-6 级包括复杂的反应机理、高级分析方法和物理化学；7-10 级纳入精密的实验方法、量子化学和前沿的化学概念。

生物（IBO）：1-3 级涵盖细胞、分子和生物个体层面的基础生物学；4-6 级包括高级细胞过程、遗传学、进化生物学和生态学；7-10 级纳入复杂的实验设计、高级生物化学、系统生物学和生物信息学。
待标注的题目：{{question}}."
```

*图 30：**科学难度过滤的提示词**。这段文本是科学难度过滤所用的提示词。*

#### R.3 去重与教师模型采样

执行去重的方法有多种。我们选择使用 Indel 相似度来衡量两个问题之间的相似性。该相似度指的是，要使一个样本与另一个样本相匹配，需要在其中插入或删除的字符数，并且是相对于样本长度来计算的。更准确地说，我们考虑一对字符串之间的归一化 Indel 相似度得分，它通过最长公共子序列（LCS）度量来计算：

```math
\text{indel}_{\text{sim}}=100\times\frac{\text{LCS}_{\text{length}}(s_{1},s_{2})}{\max(|s_{1}|,|s_{2}|)} \qquad (2)
```

#### R.4 问答过滤

下面我们讨论每种问答过滤方法的细节。

##### R.4.1 数学问答过滤

- **完整大规模数据集**：不经过滤，取全部 63,200 个回答构成一个数据集。这一设置没有控制计算量。
- **随机过滤**：随机过滤问答对。
- **最短答案选择**：对于任一给定问题，从其 16 个回答中选取最短的 8 个，为数据集构造 8 个问答对。
- **多数一致选择**：对于任一给定问题，将其全部回答提供给 GPT-4o-mini。让 GPT-4o-mini 返回与多数回答一致的那些回答的索引列表。仅使用每个回答的最后 1,000 个字符来获取最终答案。温度设为 1.0。提示词见图 31。
- **FastText 选择**：使用 FastText 过滤器对问答对进行分类。按以下格式构造查询字符串："Question: {question} \\nAnswer: {answer\_column}"。无论是训练还是使用 FastText 分类器，我们都采用这一格式。该分类器的正样本为 S1.1，其中包含来自 DeepSeek R1 的回答。该分类器的负样本来自用 GPT-4o-mini 标注的 mlfoundations-dev/stratos\_verified\_mix。更多信息见第 R.2.1 节。
- **最长答案选择**：对于任一给定问题，从其 16 个回答中选取最长的 8 个，为数据集构造 8 个问答对。
- **GPT 验证**：向 GPT-4o-mini 询问所给答案是否为所给问题的正确答案。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚（presence penalty）为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 32。
- **移除非英语答案**：向 GPT-4o-mini 询问所给答案是否只包含英语。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 34。
- **移除长段落**：向 GPT-4o-mini 询问所给答案是否不含长段落。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 35。

```text
我会给你 16 份数学题解答的最后几句话。
它们是同一道题的候选解答。

它们通常包含一道数学题的答案。请返回最终数值答案最常见的那些回答的索引。
只有最终的数值答案才算数。

问题：3 x 5 等于多少？

解答 0：
答案是 15。

解答 1：
15.0 是这道题的解。

解答 2：
答案是 14。

你应该返回：[0, 1]，因为它们都说答案是 15，只有一份回答说答案是 14。

下面是你的问题：
{{question}}

下面是候选解答：
{{list of all solutions}}

 现在告诉我是哪些解答。请记住，这些解答的索引从零开始。不要把数字 16 当作索引。
```

*图 31：**数学问答多数一致验证的提示词**。这段文本是数学问答多数一致验证所用的提示词。*

```text
给出的回答是下面这道题的正确解答吗？

问题：{{question}}
回答：{{answer}}
```

*图 32：**数学问答 GPT 验证的提示词**。这段文本是数学问答 GPT 验证所用的提示词。*

##### R.4.2 代码问答过滤

- **FastText 选择**：使用 FastText 过滤器对问答对进行分类。按以下格式构造查询字符串："Question: {question} \\nAnswer: {answer\_column}"。无论是训练还是使用 FastText 分类器，我们都采用这一格式。该分类器的正样本为 CodeForces，其中包含来自 DeepSeek R1 的回答。该分类器的负样本为用 GPT-4o-mini 标注的 CodeForces。更多信息见第 R.2.1 节。
- **完整大规模数据集**：不经过滤，取全部 63,200 个回答构成一个数据集。这一设置没有控制计算量。
- **最短答案选择**：对于任一给定问题，从其 16 个回答中选取最短的 8 个，为数据集构造 8 个问答对。
- **基于 Python 标签的选择**：过滤掉所有不带 python 标签的问题："“‘python"。
- **多数一致选择**：对于任一给定问题，将其全部回答提供给 GPT-4o-mini。让 GPT-4o-mini 返回与多数回答一致的那些回答的索引列表。温度设为 1.0。提示词见图 37。
- **最长答案选择**：对于任一给定问题，从其 16 个回答中选取最长的 8 个，为数据集构造 8 个问答对。
- **GPT 验证**：向 GPT-4o-mini 询问所给答案是否为所给问题的正确答案。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 33。
- **移除非英语答案**：向 GPT-4o-mini 询问所给答案是否只包含英语。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 34。
- **随机过滤**：随机过滤问答对。
- **移除长段落**：向 GPT-4o-mini 询问所给答案是否不含长段落。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 35。

##### R.4.3 科学问答过滤

- **FastText 选择**：使用 FastText 过滤器对问答对进行分类。按以下格式构造查询字符串："Question: {question} \\nAnswer: {answer\_column}"。无论是训练还是使用 FastText 分类器，我们都采用这一格式。该分类器的正样本为 S1.1，其中包含来自 DeepSeek R1 的回答。该分类器的负样本来自用 GPT-4o-mini 标注的 mlfoundations-dev/stratos\_verified\_mix。更多信息见第 R.2.1 节。
- **完整大规模数据集**：不经过滤，取全部 63,200 个回答构成一个数据集。这一设置没有控制计算量。
- **最长答案选择**：对于任一给定问题，从其 16 个回答中选取最长的 8 个，为数据集构造 8 个问答对。
- **移除非英语答案**：向 GPT-4o-mini 询问所给答案是否只包含英语。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 34。
- **随机过滤**：随机过滤问答对。
- **最短答案选择**：对于任一给定问题，从其 16 个回答中选取最短的 8 个，为数据集构造 8 个问答对。
- **移除长段落**：向 GPT-4o-mini 询问所给答案是否不含长段落。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 35。
- **多数一致选择**：对于任一给定问题，将其全部回答提供给 GPT-4o-mini。让 GPT-4o-mini 返回与多数回答一致的那些回答的索引列表。仅使用每个回答的最后 1,000 个字符来获取最终答案。温度设为 1.0。提示词见图 36。
- **GPT 验证**：向 GPT-4o-mini 询问所给答案是否为所给问题的正确答案。采样超参数如下：温度为 0.0，top\_p 为 1.0，存在惩罚为 1.0。我们使用结构化解码来获取一个布尔值形式的回答，以及一个字符串形式的推理。完整的提示词见图 32。

```text
给出的代码片段是下面这道题的正确解答吗？

问题：{{question}}
回答：{{answer}}
```

*图 33：**代码问答 GPT 验证的提示词**。这段文本是代码问答 GPT 验证所用的提示词。*

```text
给出的回答是否只使用了一种语言？

问题：{{question}}
回答：{{answer}}
```

*图 34：**英语验证的提示词**。这段文本是英语验证所用的提示词。*

```text
给出的回答中是否没有任何过长的段落？
段落是指用空行隔开的任意一块文本。
如果一个段落有 **>750 个词**，它就*过长*。

问题：{{question}}
回答：{{answer}}
```

*图 35：**长段落验证的提示词**。这段文本是长段落验证所用的提示词。*

```text
我会给你 16 份科学题解答的最后几句话。
它们是同一道题的候选解答。

它们通常包含一道科学题的答案。请返回答案最常见的那些回答的索引。


下面是你的问题：
{{question}}

下面是候选解答：
{{list of all solutions}}

现在告诉我是哪些解答。请记住，这些解答的索引从零开始。不要把数字 16 当作索引。
```

*图 36：**科学问答多数一致验证的提示词**。这段文本是科学多数一致验证所用的提示词。*

```text
我会给你 16 个 code_samples。
它们是同一道编程题的候选解答。

请从功能上比较所有代码样本，并返回一个索引列表，对应于
构成最常见的、功能等价的那组解答的样本。如果有多组
解答的规模相同，就随机选其中一组。同时请说明你的理由，
解释为什么你返回的这些索引对应的解答功能等价。下面是一个示例：

问题：实现 fizzbuzz。

解答 0：
def fizzbuzz1(n):
    for i in range(1, n + 1):
        output = ''

        if i % 3 == 0:
            output += 'Fizz'
        if i % 5 == 0:
            output += 'Buzz'

        print(output or i)

解答 1：
def fizzbuzz2(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print('FizzBuzz')
        elif i % 3 == 0:
            print('Fizz')
        elif i % 5 == 0:
            print('Buzz')
        else:
            print(i)

解答 2：
def fizzbuzz3(n):
    for i in range(1, n + 1):
        # 多处逻辑错误：
        if i % 3 == 0:  # 注意：简单的 if 语句不需要括号
            print('Fizz')
        elif i % 5 == 0:
            print('Buzz')
        elif i % 3 == 0 or i % 5 == 0:  # 逻辑顺序和运算符都错了
            print('FizzBuzz')
        else:
            print(i)

你应该返回：[0, 1]，因为它们功能等价，而第三份回答不同。

 下面是你的问题：
{{question}}

下面是候选解答：
{{list of all solutions}}
```

*图 37：**代码问答多数一致验证的提示词**。这段文本是代码问答多数一致验证所用的提示词。*

### 附录 S 流水线实验的扩展结果

由于篇幅所限，我们没有在正文中展示所有表格和所有数据策略。我们在此进一步展开，并给出完整结果。

#### S.1 问题来源

我们针对代码问题来源的消融实验结果见表 32。针对数学问题来源的消融实验结果见表 33。针对科学问题来源的消融实验结果见表 34。表现最好的数据集与表现最差的数据集之间差距很大。在代码数据领域，这一差距平均为 17.2 分

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 问题生成策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| StackExchange CodeGolf | **38.8 ± 0.4** | 25.3 ± 0.6 | **50.9 ± 1.1** | 40.7 ± 0.5 |
| nvidia/OpenCodeReasoning | **38.4 ± 0.3** | **27.5 ± 0.4** | 47.9 ± 0.7 | 40.7 ± 0.6 |
| KodCode/KodCode-V1 | 37.7 ± 0.3 | 23.9 ± 0.4 | **49.8 ± 0.7** | 40.4 ± 0.3 |
| cognitivecomputations/dolphin-coder | 37.1 ± 0.5 | 20.8 ± 0.4 | 49.2 ± 1.6 | **43.3 ± 0.7** |
| m-a-p/CodeFeedback… | 37.0 ± 0.4 | 18.9 ± 0.3 | **51.8 ± 1.1** | 41.8 ± 0.6 |
| Multilingual-Multimodal-NLP/McEval-… | 35.4 ± 0.3 | 16.2 ± 0.4 | 49.5 ± 0.7 | **42.9 ± 0.6** |
| OpenCoder-LLM/opc-sft-stage2 | 35.4 ± 0.4 | 16.7 ± 0.2 | **51.0 ± 1.1** | 39.8 ± 0.5 |
| ajibawa-2023/Code-290k-ShareGPT | 35.1 ± 0.4 | 18.5 ± 0.4 | 49.4 ± 1.0 | 38.7 ± 0.6 |
| christopher/rosetta-code | 35.0 ± 0.4 | 14.7 ± 0.3 | **49.6 ± 0.7** | **43.3 ± 1.0** |
| glaiveai/glaive-code-assistant-v3 | 35.0 ± 0.3 | 16.6 ± 0.3 | **50.2 ± 1.0** | 40.0 ± 0.3 |
| prithivMLmods/Coder-Stat | 34.2 ± 0.4 | 14.1 ± 0.7 | **49.7 ± 0.9** | 41.2 ± 0.7 |
| ise-uiuc/Magicoder-OSS-Instruct-75K | 33.9 ± 0.5 | 17.7 ± 0.4 | 47.4 ± 1.0 | 37.9 ± 1.2 |
| codeparrot/apps | 33.5 ± 0.4 | 15.6 ± 0.6 | **49.8 ± 0.9** | 35.8 ± 0.8 |
| StackExchange Codereview | 33.4 ± 0.4 | 13.5 ± 0.5 | 48.4 ± 0.9 | 40.7 ± 0.9 |
| nampdn-ai/tiny-codes | 32.8 ± 0.4 | 12.0 ± 0.5 | 48.0 ± 0.9 | 41.1 ± 0.5 |
| bigcode/commitpackft | 32.1 ± 0.5 | 12.2 ± 0.3 | 46.9 ± 0.9 | 39.6 ± 1.5 |
| deepmind/code\_contests | 31.8 ± 0.4 | 18.5 ± 0.5 | 45.1 ± 1.1 | 31.8 ± 0.5 |
| SenseLLM/ReflectionSeq-GPT | 31.5 ± 0.4 | 14.8 ± 0.4 | 45.6 ± 0.9 | 35.2 ± 1.0 |
| MatrixStudio/Codeforces-Python… | 31.4 ± 0.5 | 19.3 ± 0.4 | 39.3 ± 1.3 | 37.7 ± 1.1 |
| Magpie-Align/Magpie-Qwen2.5-… | 31.2 ± 0.5 | 12.3 ± 0.4 | 47.8 ± 1.3 | 34.6 ± 1.1 |
| bigcode/self-oss-instruct-sc2-… | 31.2 ± 0.4 | 13.7 ± 0.4 | 46.1 ± 0.9 | 35.0 ± 0.6 |
| PrimeIntellect/real-world-swe-problems | 30.5 ± 0.4 | 10.7 ± 0.2 | 45.7 ± 1.3 | 37.4 ± 0.7 |
| StackExchange | 30.3 ± 0.4 | 8.5 ± 0.4 | 47.5 ± 1.0 | 37.3 ± 0.3 |
| cfahlgren1/react-code-instructions | 28.5 ± 0.4 | 7.8 ± 0.3 | 45.5 ± 1.3 | 34.0 ± 0.5 |
| PrimeIntellect/stackexchange… | 27.6 ± 0.3 | 5.9 ± 0.2 | 46.8 ± 1.0 | 31.6 ± 0.5 |
| PrimeIntellect/synthetic… | 27.2 ± 0.3 | 2.2 ± 0.2 | 45.5 ± 0.7 | 37.2 ± 0.9 |
| bugdaryan/sql-create-… | 21.6 ± 0.6 | 7.0 ± 0.7 | 34.1 ± 1.4 | 24.7 ± 0.9 |

*表 32：**代码问题来源的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 问题生成策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| ai2-adapt-dev/openmath-2-math | **38.1 ± 0.3** | **12.4 ± 0.2** | **58.8 ± 1.0** | **45.6 ± 0.2** |
| AI-MO/NuminaMath-1.5 | 37.4 ± 0.5 | 11.4 ± 0.5 | **58.5 ± 1.0** | **45.0 ± 1.2** |
| openmathinstruct\_aime\* | 37.2 ± 0.5 | **12.5 ± 0.3** | **57.1 ± 0.9** | 44.3 ± 1.4 |
| GAIR/MathPile\* | 36.2 ± 0.5 | 11.5 ± 0.7 | 55.1 ± 0.9 | 44.6 ± 1.1 |
| 基于 Numina 的 MetaMath\* | 35.8 ± 0.6 | 10.9 ± 0.8 | 56.3 ± 1.4 | 42.5 ± 1.0 |
| math-ai/AutoMathText\* | 35.7 ± 0.4 | 8.7 ± 0.6 | 55.5 ± 0.8 | **46.6 ± 0.8** |
| nvidia/OpenMathInstruct-2 Aime | 35.4 ± 0.4 | 10.7 ± 0.4 | 55.8 ± 1.2 | 41.8 ± 0.4 |
| zwhe99/DeepMath-103K | 34.8 ± 0.6 | 7.2 ± 0.4 | 55.6 ± 1.9 | 44.8 ± 1.0 |
| ddrg/named\_math\_formulas\* | 33.9 ± 0.4 | 10.3 ± 0.5 | 53.9 ± 1.0 | 39.4 ± 0.4 |
| TIGER-Lab/MathInstruct | 33.8 ± 0.5 | **12.4 ± 0.6** | 50.6 ± 0.8 | 40.8 ± 1.1 |
| nvidia/OpenMathInstruct-2 | 33.5 ± 0.5 | 7.9 ± 0.5 | 55.2 ± 1.1 | 39.1 ± 1.0 |
| facebook/natural\_reasoning | 33.4 ± 0.4 | 7.6 ± 0.3 | 52.1 ± 1.0 | 43.9 ± 0.5 |
| SynthLabsAI/Big-Math… | 33.0 ± 0.3 | 9.4 ± 0.2 | 53.2 ± 1.0 | 38.1 ± 0.4 |
| TIGER-Lab/MATH-plus | 32.7 ± 0.4 | 8.8 ± 0.3 | 51.6 ± 0.9 | 40.3 ± 0.9 |
| Asap7772/hendrycks-math-… | 32.3 ± 0.4 | 8.9 ± 0.5 | 52.4 ± 1.1 | 37.4 ± 0.8 |
| ibivibiv/math\_instruct | 30.6 ± 0.4 | 8.2 ± 0.4 | 48.2 ± 1.0 | 37.6 ± 0.7 |
| ajibawa-2023/Maths-College | 30.1 ± 0.4 | 2.4 ± 0.2 | 51.6 ± 1.1 | 39.5 ± 0.7 |
| BAAI/InfinityMATH\* | 29.7 ± 0.3 | 7.4 ± 0.3 | 47.6 ± 1.0 | 36.5 ± 0.2 |
| MetaMath\* | 29.3 ± 0.4 | 6.1 ± 0.5 | 48.4 ± 1.2 | 35.3 ± 0.5 |
| allenai/math\_qa | 27.8 ± 0.4 | 4.9 ± 0.3 | 46.4 ± 0.8 | 34.1 ± 1.1 |
| deepmind/math\_dataset | 25.9 ± 0.4 | 5.1 ± 0.2 | 43.2 ± 1.2 | 31.1 ± 0.8 |
| Lap1official/Math\* | 24.4 ± 0.3 | 7.3 ± 0.3 | 38.6 ± 1.0 | 28.5 ± 0.3 |

*表 33：**数学问题来源的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 问题生成策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| StackExchange Physics | **34.3 ± 0.4** | **11.9 ± 0.5** | **50.9 ± 0.8** | 43.2 ± 0.7 |
| 有机化学 PDF 流水线 | **34.0 ± 0.3** | 8.4 ± 0.3 | **52.1 ± 0.7** | **45.3 ± 0.8** |
| mteb/cqadupstack-physics | 33.3 ± 0.4 | 7.4 ± 0.3 | **51.9 ± 1.1** | **44.1 ± 0.9** |
| camel-ai/physics | 30.9 ± 0.5 | 8.6 ± 0.2 | 48.0 ± 1.1 | 38.9 ± 1.2 |
| Josephgflowers/Par-Four-Fineweb… | 30.9 ± 0.4 | 8.2 ± 0.5 | 48.4 ± 1.0 | 38.8 ± 0.6 |
| mattany/wikipedia-biology | 29.3 ± 0.4 | 5.2 ± 0.2 | 47.3 ± 1.3 | 38.4 ± 0.7 |
| millawell/wikipedia\_field\_of\_science | 29.1 ± 0.4 | 4.8 ± 0.4 | 47.7 ± 1.0 | 37.5 ± 0.9 |
| zeroshot/arxiv-biology | 28.7 ± 0.4 | 5.5 ± 0.2 | 46.7 ± 0.9 | 36.4 ± 1.2 |
| camel-ai/chemistry | 27.8 ± 0.4 | 3.6 ± 0.3 | 46.4 ± 1.1 | 36.1 ± 0.7 |
| Sangeetha/Kaggle… | 27.5 ± 0.6 | 6.0 ± 0.6 | 43.8 ± 1.4 | 35.2 ± 1.0 |
| marcov/pubmed\_qa… | 25.6 ± 0.5 | 5.5 ± 0.2 | 41.8 ± 1.5 | 31.4 ± 0.5 |
| StackExchange Biology | 25.1 ± 0.4 | 4.0 ± 0.3 | 39.6 ± 1.1 | 34.8 ± 0.9 |
| camel-ai/biology | 25.0 ± 0.4 | 2.7 ± 0.2 | 44.1 ± 1.0 | 29.7 ± 1.0 |
| AdapterOcean/biology\_dataset… | 21.9 ± 0.4 | 3.1 ± 0.3 | 41.3 ± 1.1 | 21.1 ± 0.8 |

*表 34：**科学问题来源的完整消融实验**。*

#### S.2 混合问题生成策略

我们针对代码问题混合的消融实验结果见表 35。针对数学问题混合的消融实验结果见表 36。针对科学问题混合的消融实验结果见表 37。“混合越少越好”这一趋势在所有领域中都成立。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 混合策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 前 2 个代码来源 | **41.3 ± 0.4** | **27.3 ± 0.3** | **54.7 ± 0.9** | **42.1 ± 1.0** |
| 前 1 个代码来源 | 39.9 ± 0.6 | 23.1 ± 1.0 | **54.5 ± 0.8** | **43.1 ± 1.2** |
| 前 4 个代码来源 | 38.6 ± 0.4 | 24.2 ± 0.6 | 52.2 ± 0.8 | 39.8 ± 0.9 |
| 前 8 个代码来源 | 37.0 ± 0.4 | 21.8 ± 0.3 | 51.9 ± 1.2 | 37.7 ± 0.6 |
| 前 16 个代码来源 | 36.4 ± 0.4 | 20.8 ± 0.4 | 50.1 ± 0.9 | 39.1 ± 1.0 |

*表 35：**代码问题来源混合的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 混合策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 前 1 个数学来源 | **37.6 ± 0.5** | **12.1 ± 0.5** | **60.1 ± 1.5** | **41.9 ± 0.7** |
| 前 8 个数学来源 | 35.8 ± 0.5 | **12.6 ± 0.4** | 54.8 ± 0.9 | **42.3 ± 1.2** |
| 前 4 个数学来源 | 34.7 ± 0.3 | 9.0 ± 0.2 | 56.0 ± 0.9 | 41.4 ± 0.5 |
| 前 2 个数学来源 | 34.3 ± 0.3 | 6.9 ± 0.3 | 55.9 ± 0.9 | **43.0 ± 0.5** |
| 前 16 个数学来源 | 33.8 ± 0.3 | 11.2 ± 0.4 | 50.3 ± 0.8 | **43.1 ± 0.7** |

*表 36：**数学问题来源混合的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 混合策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 前 2 个科学来源 | **33.7 ± 0.4** | 9.5 ± 0.3 | **50.3 ± 0.9** | **44.8 ± 1.2** |
| 前 1 个科学来源 | **33.6 ± 0.5** | **12.0 ± 0.3** | **49.6 ± 0.9** | 42.0 ± 1.3 |
| 前 4 个科学来源 | 32.2 ± 0.4 | 8.1 ± 0.2 | **49.3 ± 1.3** | **42.5 ± 0.6** |
| 前 8 个科学来源 | 31.1 ± 0.4 | 6.4 ± 0.4 | **49.0 ± 1.1** | 41.4 ± 0.9 |
| 前 16 个科学来源 | 30.8 ± 0.3 | 6.7 ± 0.2 | 48.4 ± 1.0 | 40.3 ± 0.6 |

*表 37：**科学问题来源混合的完整消融实验**。*

#### S.3 问题过滤

我们针对代码问题过滤的消融实验结果见表 38。针对数学问题过滤的消融实验结果见表 39。针对科学问题过滤的消融实验结果见表 40。对于每个数据领域，我们都尝试了第 R.2 节中的每一种问题过滤策略。这些消融实验包含 FastText 正负样本的不同组合。它们还涵盖了基于长度的过滤所用的多种模型，例如 GPT-4o-mini、GPT-4.1-mini 和 GPT-4.1-nano。在科学和数学领域，使用 GPT-4.1 系列模型进行基于长度的过滤效果都很好。在每个数据领域中，大约一半的过滤策略优于随机过滤。在所有数据领域中，AskLLM 过滤和基于难度的过滤效果都相对较好。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 基于难度的选择 | **43.0 ± 0.5** | 27.7 ± 0.4 | **56.0 ± 1.3** | **46.4 ± 0.7** |
| 基于长度的选择（GPT-4.1-nano） | **42.2 ± 0.4** | 26.6 ± 0.5 | **55.4 ± 1.3** | **46.0 ± 0.2** |
| AskLLM 选择 | 41.6 ± 0.5 | **28.8 ± 0.5** | 52.1 ± 1.2 | **45.2 ± 0.8** |
| 基于长度的选择（GPT-4o-mini） | 40.8 ± 0.5 | 25.6 ± 0.5 | 53.1 ± 0.9 | **45.2 ± 1.1** |
| FastText（正例：Codeforces；负例：CodeReview） | 40.5 ± 0.3 | 26.3 ± 0.4 | **53.9 ± 0.9** | 41.8 ± 0.5 |
| 基于长度的选择（GPT-4.1-mini） | 40.5 ± 0.3 | 26.8 ± 0.3 | 51.3 ± 0.8 | 44.9 ± 0.8 |
| 随机选择 | 39.7 ± 0.5 | **28.6 ± 0.5** | 50.2 ± 1.3 | 40.5 ± 0.7 |
| FastText（正例：LeetCode；负例：SQL） | 39.6 ± 0.4 | 25.2 ± 0.5 | 52.8 ± 1.0 | 41.7 ± 0.5 |
| FastText（正例：Code Golf；负例：SQL） | 39.0 ± 0.5 | 23.9 ± 0.5 | 52.4 ± 1.3 | 41.5 ± 0.7 |
| FastText（正例：全部；负例：SQL） | 38.9 ± 0.5 | 26.3 ± 0.4 | 50.5 ± 1.0 | 40.7 ± 1.2 |
| FastText（正例：IOI；负例：SQL） | 38.5 ± 0.4 | 24.8 ± 0.4 | 50.2 ± 0.8 | 41.4 ± 0.7 |
| FastText（正例：Codeforces；负例：全部） | 38.5 ± 0.4 | 25.1 ± 0.4 | 50.9 ± 1.1 | 39.9 ± 0.8 |
| FastText（正例：Codeforces；负例：SQL） | 38.4 ± 0.4 | 25.0 ± 0.2 | 50.0 ± 1.3 | 41.1 ± 0.6 |
| 基于嵌入的选择 | 36.9 ± 0.6 | 16.2 ± 0.4 | **53.4 ± 1.2** | 43.1 ± 1.6 |

*表 38：**代码问题过滤的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 基于长度的选择（GPT-4.1-mini） | **41.9 ± 0.3** | **13.4 ± 0.3** | **66.0 ± 0.8** | **48.6 ± 0.4** |
| 基于长度的选择（GPT-4.1-nano） | 39.4 ± 0.3 | 11.0 ± 0.4 | **64.5 ± 0.7** | 44.3 ± 0.7 |
| AskLLM 选择 | 36.3 ± 0.4 | 9.5 ± 0.5 | 58.1 ± 1.1 | 43.8 ± 0.6 |
| FastText（正例：Numina；负例：Lap1official） | 35.6 ± 0.4 | 11.0 ± 0.2 | 54.9 ± 1.1 | 43.5 ± 0.8 |
| 基于难度的选择 | 35.5 ± 0.5 | 8.2 ± 0.3 | 59.3 ± 1.4 | 40.8 ± 1.1 |
| 基于嵌入的选择 | 35.4 ± 0.4 | 6.3 ± 0.3 | 57.0 ± 1.0 | 46.5 ± 0.9 |
| 随机选择 | 35.2 ± 0.5 | 8.1 ± 0.2 | 56.6 ± 1.3 | 43.8 ± 1.1 |
| FastText（正例：S1.1；负例：Lap1official） | 34.9 ± 0.4 | 10.8 ± 0.4 | 55.5 ± 1.1 | 40.5 ± 0.3 |
| FastText（正例：Olympiad；负例：Lap1official） | 34.9 ± 0.3 | 8.7 ± 0.3 | 56.2 ± 1.0 | 42.2 ± 0.4 |
| FastText（正例：OpenR1；负例：Lap1official） | 34.4 ± 0.4 | 8.7 ± 0.3 | 55.1 ± 1.2 | 41.7 ± 0.8 |
| FastText（正例：全部；负例：Lap1official） | 34.4 ± 0.4 | 9.8 ± 0.5 | 54.3 ± 1.0 | 41.4 ± 0.4 |
| FastText（正例：Numina；负例：全部） | 32.8 ± 0.4 | 7.8 ± 0.2 | 53.9 ± 1.2 | 38.5 ± 0.4 |
| FastText（正例：Numina；负例：Natural Reasoning） | 32.6 ± 0.6 | 6.8 ± 0.4 | 53.9 ± 1.2 | 39.4 ± 1.5 |
| 基于长度的选择（GPT-4o-mini） | 6.8 ± 0.3 | 2.3 ± 0.4 | 10.2 ± 0.9 | 8.4 ± 0.3 |

*表 39：**数学问题过滤的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 基于长度的选择（GPT-4.1-mini） | **35.9 ± 0.4** | 7.3 ± 0.5 | **54.4 ± 0.9** | **50.9 ± 0.9** |
| 基于长度的选择（GPT-4.1-nano） | **35.6 ± 0.3** | 7.7 ± 0.3 | **53.7 ± 0.7** | **50.2 ± 0.8** |
| AskLLM 选择 | **35.3 ± 0.3** | **11.1 ± 0.1** | 51.5 ± 0.8 | 47.2 ± 0.7 |
| FastText（正例：SciQ；负例：Wikipedia + Arxiv） | **35.1 ± 0.5** | 9.3 ± 0.3 | 51.8 ± 1.3 | 48.7 ± 1.1 |
| 基于嵌入的选择 | 34.9 ± 0.4 | 9.7 ± 0.4 | 51.2 ± 1.0 | 48.4 ± 1.0 |
| 基于长度的选择（GPT-4o-mini） | 34.9 ± 0.3 | **10.8 ± 0.3** | **52.9 ± 0.9** | 44.3 ± 0.6 |
| FastText（正例：SCP、SciQ、ExpertQA；负例：Arxiv） | 34.4 ± 0.6 | 9.5 ± 0.4 | 51.3 ± 1.1 | 46.4 ± 1.7 |
| 随机选择 | 33.8 ± 0.4 | 8.1 ± 0.4 | 52.1 ± 1.1 | 44.6 ± 0.6 |
| FastText（正例：SciQ；负例：Wikipedia + Arxiv） | 33.5 ± 0.3 | 8.2 ± 0.3 | 51.3 ± 1.0 | 44.6 ± 0.4 |
| 基于难度的选择 | 33.5 ± 0.4 | 7.7 ± 0.4 | 50.7 ± 0.9 | 46.4 ± 1.1 |
| FastText（正例：SciQ；负例：Wikipedia + Arxiv） | 33.4 ± 0.4 | 10.2 ± 0.6 | 50.7 ± 1.0 | 42.2 ± 0.5 |
| FastText（正例：ExpertQA；负例：Arxiv） | 31.5 ± 0.4 | **11.4 ± 0.3** | 45.9 ± 1.1 | 40.2 ± 0.8 |

*表 40：**科学问题过滤的完整消融实验**。*

#### S.4 去重与多次采样

我们针对代码去重与多次采样的消融实验结果见表 41。针对数学去重与多次采样的消融实验结果见表 42。针对科学去重与多次采样的消融实验结果见表 43。在所有数据领域中，精确去重或不去重都优于模糊去重。此外，多次采样的表现与每个问题只标注一次相当或持平。这里的主要例外是表 42，其中每个问题只标注 1 次的效果更好。不过，从实验结果来看，次优策略是精确去重加 16× 采样。16× 采样为 OpenThoughts3-1.2M 提供了一个进一步扩展数据规模的维度，因此我们在最终流水线中选择了这一标注策略。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 标注策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 精确去重 + 4× 采样 | **41.3 ± 0.5** | **28.6 ± 0.4** | **53.5 ± 1.2** | 42.1 ± 1.0 |
| 不去重 + 16× 采样 | **41.3 ± 0.4** | 25.9 ± 0.3 | **53.8 ± 1.2** | **45.8 ± 0.3** |
| 不去重 + 4× 采样 | **41.2 ± 0.4** | 27.3 ± 0.3 | **54.3 ± 1.2** | 42.2 ± 0.7 |
| 模糊去重 + 4× 采样 | **41.2 ± 0.4** | **28.1 ± 0.5** | 51.8 ± 1.1 | 45.0 ± 0.6 |
| 模糊去重 + 16× 采样 | **41.2 ± 0.4** | 24.8 ± 0.4 | **54.3 ± 1.0** | **46.1 ± 0.4** |
| 精确去重 + 16× 采样 | **40.6 ± 0.5** | 25.5 ± 0.4 | **53.5 ± 1.2** | 44.1 ± 1.1 |
| 不去重 + 1× 采样 | 39.8 ± 0.6 | 26.5 ± 0.4 | **53.0 ± 1.2** | 39.9 ± 1.5 |

*表 41：**代码去重与多次采样的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 标注策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 精确去重 + 1× 采样 | **41.7 ± 0.3** | **14.0 ± 0.3** | **66.0 ± 1.0** | 46.6 ± 0.2 |
| 精确去重 + 16× 采样 | 40.1 ± 0.4 | 11.0 ± 0.3 | 63.6 ± 1.3 | **48.7 ± 0.5** |
| 精确去重 + 4× 采样 | 39.2 ± 0.4 | 12.0 ± 0.3 | 62.6 ± 1.1 | 44.7 ± 0.5 |
| 模糊去重 + 4× 采样 | 38.8 ± 1.2 | 12.4 ± 0.5 | 60.6 ± 3.9 | 45.7 ± 0.9 |
| 不去重 + 1× 采样 | 38.3 ± 1.1 | 10.8 ± 0.3 | 59.8 ± 3.7 | 47.4 ± 1.0 |
| 不去重 + 4× 采样 | 37.7 ± 0.4 | 3.3 ± 0.3 | **64.6 ± 1.2** | **49.0 ± 0.6** |
| 模糊去重 + 1× 采样 | 37.4 ± 1.5 | 9.3 ± 1.7 | 60.6 ± 4.1 | 44.8 ± 2.0 |
| 不去重 + 16× 采样 | 36.5 ± 1.2 | **13.9 ± 0.4** | 55.4 ± 3.9 | 42.1 ± 1.1 |
| 模糊去重 + 16× 采样 | 36.0 ± 0.4 | 5.5 ± 0.2 | 61.1 ± 1.1 | 43.9 ± 0.9 |

*表 42：**数学去重与多次采样的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 标注策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 精确去重 + 16× 采样 | **36.2 ± 0.5** | 9.0 ± 0.4 | **54.5 ± 1.0** | 49.7 ± 1.2 |
| 模糊去重 + 16× 采样 | **36.1 ± 0.4** | **10.9 ± 0.2** | 52.9 ± 1.3 | 48.8 ± 0.5 |
| 精确去重 + 4× 采样 | **35.8 ± 0.5** | **10.6 ± 0.7** | 51.8 ± 1.0 | 49.6 ± 1.2 |
| 不去重 + 4× 采样 | **35.8 ± 0.4** | 10.0 ± 0.4 | **55.2 ± 0.8** | 45.4 ± 0.9 |
| 不去重 + 16× 采样 | **35.7 ± 0.4** | 7.6 ± 0.5 | **53.8 ± 1.0** | **50.9 ± 0.5** |
| 不去重 + 1× 采样 | **35.5 ± 0.3** | 9.3 ± 0.3 | **54.2 ± 1.1** | 46.9 ± 0.2 |
| 精确去重 + 1× 采样 | 35.0 ± 0.4 | 7.6 ± 0.4 | **54.0 ± 1.2** | 47.5 ± 0.5 |
| 模糊去重 + 4× 采样 | 34.9 ± 0.4 | 7.4 ± 0.5 | **55.0 ± 1.0** | 46.0 ± 0.7 |
| 模糊去重 + 1× 采样 | 34.2 ± 0.3 | 5.8 ± 0.4 | 52.5 ± 0.7 | 49.5 ± 0.4 |

*表 43：**科学去重与多次采样的完整消融实验**。*

#### S.5 问答过滤

我们针对代码问答过滤的消融实验结果见表 44。针对数学问答过滤的消融实验结果见表 45。针对科学问答过滤的消融实验结果见表 46。在所有数据领域中，完全不进行过滤的表现与最佳问答过滤策略相近或更优。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| FastText 选择 | **42.3 ± 0.5** | **27.2 ± 0.5** | **54.7 ± 1.4** | **46.5 ± 0.3** |
| 不过滤 | **42.2 ± 0.5** | **27.4 ± 0.6** | **54.5 ± 1.1** | **46.1 ± 0.9** |
| 最短答案选择 | **42.0 ± 0.5** | 26.5 ± 0.5 | **54.4 ± 1.1** | **46.9 ± 1.1** |
| 基于 Python 标签的选择 | **41.7 ± 0.5** | **27.8 ± 0.3** | **54.6 ± 1.0** | 43.4 ± 1.2 |
| 多数一致选择 | **41.3 ± 0.5** | 26.6 ± 0.2 | **53.6 ± 1.2** | **45.0 ± 1.0** |
| 最长答案选择 | 41.0 ± 0.4 | 26.9 ± 0.4 | **55.4 ± 1.2** | 40.5 ± 0.7 |
| GPT 验证 | 40.7 ± 0.4 | 25.5 ± 0.4 | **53.6 ± 0.8** | 44.2 ± 1.0 |
| 移除非英语答案 | 40.6 ± 0.4 | 26.2 ± 0.5 | **54.5 ± 1.1** | 41.6 ± 0.6 |
| 随机过滤 | 39.8 ± 0.4 | 25.1 ± 0.5 | 52.2 ± 1.1 | 43.0 ± 0.5 |
| 移除长段落 | 30.3 ± 0.5 | 19.6 ± 0.2 | 40.5 ± 1.5 | 31.3 ± 0.9 |

*表 44：**代码问答过滤的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 不过滤 | **41.9 ± 0.4** | **15.2 ± 0.5** | **65.6 ± 0.9** | 46.4 ± 0.7 |
| 随机过滤 | **41.6 ± 0.4** | **14.9 ± 0.4** | **64.8 ± 0.9** | 46.7 ± 0.5 |
| 最短答案选择 | **41.1 ± 0.4** | **14.8 ± 0.4** | 63.7 ± 1.1 | 46.7 ± 0.7 |
| 移除非英语答案 | **41.1 ± 0.5** | **14.2 ± 0.5** | 63.1 ± 1.0 | **48.6 ± 1.0** |
| 多数一致选择 | 41.0 ± 0.4 | **14.5 ± 0.5** | 62.3 ± 0.8 | **48.8 ± 0.8** |
| FastText 选择 | 40.7 ± 0.5 | 13.5 ± 0.2 | 62.8 ± 1.4 | **48.4 ± 0.8** |
| 最长答案选择 | 40.5 ± 0.5 | 12.9 ± 0.4 | **63.9 ± 1.4** | 46.7 ± 1.0 |
| GPT 验证 | 40.0 ± 0.5 | 13.1 ± 0.3 | 61.4 ± 1.1 | **48.3 ± 1.1** |
| 移除长段落 | 38.0 ± 0.4 | 5.7 ± 0.2 | **64.5 ± 0.9** | 46.8 ± 1.0 |

*表 45：**数学问答过滤的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 过滤策略 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| 不过滤 | **38.3 ± 0.4** | 10.6 ± 0.3 | **56.9 ± 0.9** | **51.9 ± 0.7** |
| 最长答案选择 | **37.5 ± 0.3** | 12.0 ± 0.2 | **55.4 ± 0.8** | 48.8 ± 0.7 |
| 移除非英语答案 | 37.4 ± 0.4 | **13.4 ± 0.4** | 54.5 ± 1.0 | 47.6 ± 0.9 |
| FastText 选择 | 36.8 ± 0.4 | 11.5 ± 0.4 | 54.7 ± 1.1 | 47.7 ± 0.5 |
| 随机过滤 | 36.5 ± 0.4 | 11.0 ± 0.4 | 53.9 ± 1.1 | 48.8 ± 0.7 |
| 最短答案选择 | 36.2 ± 0.5 | 11.4 ± 0.7 | 53.6 ± 1.2 | 47.5 ± 0.4 |
| 移除长段落 | 35.9 ± 0.5 | 11.4 ± 0.6 | 53.7 ± 1.0 | 45.7 ± 1.2 |
| 多数一致选择 | 35.7 ± 0.5 | 9.1 ± 0.5 | 54.6 ± 1.1 | 47.1 ± 0.9 |
| GPT 验证 | 35.6 ± 0.5 | 11.4 ± 0.5 | 52.6 ± 1.3 | 46.4 ± 1.0 |

*表 46：**科学问答过滤的完整消融实验**。*

#### S.6 教师模型实验

我们针对代码的教师模型消融实验结果见表 47。针对数学的教师模型消融实验结果见表 48。针对科学的教师模型消融实验结果见表 49。在所有数据领域中，QwQ-32B 都是最好的教师模型，且领先幅度具有统计显著性。

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 教师模型 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| Qwen/QwQ-32B | **44.2 ± 0.5** | **29.5 ± 0.3** | **58.7 ± 1.1** | **44.6 ± 1.0** |
| deepseek-ai/DeepSeek-R1 | 38.0 ± 1.5 | 19.2 ± 3.4 | 54.3 ± 1.6 | 41.8 ± 1.0 |
| microsoft/Phi-4-reasoning-plus | 29.0 ± 0.4 | 0.5 ± 0.1 | 52.1 ± 1.2 | 37.2 ± 0.6 |

*表 47：**代码领域教师模型的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 教师模型 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| Qwen/QwQ-32B | **44.2 ± 0.4** | 10.9 ± 0.4 | **71.6 ± 1.1** | **53.2 ± 0.4** |
| deepseek-ai/DeepSeek-R1 | 40.6 ± 0.3 | **13.3 ± 0.4** | 62.5 ± 0.9 | 48.5 ± 0.4 |
| microsoft/Phi-4-reasoning-plus | 30.6 ± 0.6 | 7.1 ± 0.4 | 49.0 ± 1.6 | 38.2 ± 0.9 |

*表 48：**数学领域教师模型的完整消融实验**。*

| SFT 数据集 | | 基准 | | |
| --- | --- | --- | --- | --- |
| 教师模型 | 平均 | 代码平均 | 数学平均 | 科学平均 |
| Qwen/QwQ-32B | **39.1 ± 0.4** | **10.1 ± 0.5** | **62.1 ± 1.2** | 48.0 ± 0.2 |
| deepseek-ai/DeepSeek-R1 | 35.9 ± 0.7 | 7.1 ± 1.6 | 55.9 ± 0.9 | **49.0 ± 0.4** |
| microsoft/Phi-4-reasoning-plus | 21.7 ± 0.4 | 4.8 ± 0.2 | 28.8 ± 1.3 | 36.4 ± 0.7 |

*表 49：**科学领域教师模型的完整消融实验**。*

[^1]: <https://www.bespokelabs.ai/blog/bespoke-stratos-the-unreasonable-effectiveness-of-reasoning-distillation>
[^2]: <https://www.openthoughts.ai/blog/launch>
[^3]: <https://www.openthoughts.ai/blog/thinkagain>
