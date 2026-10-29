# 重新思考大语言模型的 on-policy 蒸馏：现象、机制与配方

中文 | [English](./Rethinking-On-Policy-Distillation_en.md)

- **原文链接**: [Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe](https://arxiv.org/abs/2604.13016v2)
- **论文**: [arXiv:2604.13016](https://arxiv.org/abs/2604.13016)
- **官方资料**: [thunlp/OPD](https://github.com/thunlp/OPD)（论文给出的代码地址，现重定向到 Thinking-Space/Rethinking-OPD）
- **发布日期**: 2026-04-14
- **译注**: “主要结论”是为本笔记写的摘要，不属于原文，数字均取自论文；“全文翻译”是 arXiv v2 版的非官方全文中译，含正文、附录、全部图表和参考文献。原文以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可发布，本译文沿用同一许可，格式上的改动列在“全文翻译”一节的开头。英文版的“主要结论”译自中文摘要，其余是原文转成的 Markdown。

## 主要结论

- **问题**：on-policy 蒸馏（OPD）已经成为大语言模型后训练的核心技术，Qwen3、MiMo、GLM-5 的后训练流水线都在用它，Thinking Machines Lab 也以远低于强化学习的算力复现了 Qwen3 的 OPD 配方。但它的训练动力学几乎没有被系统研究过，实践中还很脆弱：论文观察到一个醒目的失败模式——更强的教师可能完全无法提升学生，而一个更弱、初始对齐程度更低的教师却能成功。
- **成功的两个条件**：(i) *思维模式一致性*——学生和教师的思维模式要相容（例如 top-$`k`$ 词元分布的重叠率更高）；即便教师的基准分数更高，模式不匹配带来的低初始重叠也无法在训练中完全弥补。(ii) *更高的分数 ≠ 新知识*——即便思维模式一致、分数更高，教师也必须提供学生在训练中尚未见过的新能力；当两个模型用同样的数据和配方训练时，它们会在各自规模上收敛到相似的分布，教师几乎没有可传递的信号。
- **后训练过的教师才带来增益**：在 DeepSeek 和 Qwen 两个家族中，来自同一流水线的教师收益有限，而经过额外强化学习的教师收益大得多。差距回收率 $`(\mathrm{Acc}_{\text{after OPD}} - \mathrm{Acc}_{\text{before OPD}}) / (\mathrm{Acc}_{\text{teacher}} - \mathrm{Acc}_{\text{before OPD}})`$ 分别是 Skywork-OR1-Math-7B 的 16.9% 对 R1-Distill-7B 的 5.3%，以及 Qwen3-4B-Non-Thinking-RL-Math 的 58.6% 对 Qwen3-4B 的 15.6%——而后训练过的教师初始重叠率反而更低（71.5% 对 74.7%，70.3% 对 75.7%）。
- **反向蒸馏：OPD 学的是思维模式，不是分数**：把 JustRL-1.5B（由 R1-Distill-1.5B 经强化学习得到）当作学生，向它自己强化学习之前的检查点 R1-Distill-1.5B 蒸馏，会让它几乎精确地退回强化学习之前的水平，强化学习获得的收益全部被抹掉；换成规模更大、基准分数还略高的 R1-Distill-7B 作教师，训练轨迹几乎无法区分，学生退回到同样的水平。由于 OPD 最小化的是学生生成轨迹上的反向 KL，这说明两个教师在学生访问到的状态上诱导出了几乎相同的局部目标分布，与规模差异无关。
- **词元层面的机制：高概率词元上的渐进对齐**：成功的 OPD 有一致的特征——重叠率从约 72% 稳步升到 91% 以上，重叠词元优势向 0 靠拢，熵差收窄，最终学生回收了与教师差距的 80% 以上；失败的运行则三项指标从一开始就停滞。重叠词元在整个训练过程中都占双方 97%–99% 的概率质量，所以重叠率上升反映的是概率上占主导的词元在对齐，而不只是集合层面的巧合。
- **只优化重叠词元就够了**：把蒸馏损失限制在学生与教师 top-$`k`$ 集合的交集上（Overlap Top-$`k`$），在三个基准上都能恢复标准 Student Top-$`k`$ OPD 的几乎全部收益，而限制在对称差上的 Non-Overlap Top-$`k`$ 则明显更差。重叠优化还是自我强化的：一个词元一旦进入共享的高概率区域并被教师偏好，反向 KL 更新就会把更多质量集中到它上面，逐步把竞争的非重叠词元挤出学生的 top-$`k`$ 集合。
- **配方一：off-policy 冷启动**：先用教师生成的 rollout 对学生做监督微调，再进入 OPD。用 Qwen3-4B（非思考模式）在 OpenThoughts3-1.2M 数学子集的 200K 条提示词上离线生成回答，过滤后微调 Qwen3-1.7B-Base，再用去重后剩下的约 30K 条提示词做 OPD；相比直接从基座模型开始的纯 OPD，验证性能自始至终更好，初始重叠率更高且轨迹平滑稳定，熵差也小得多。这说明冷启动抬高的不只是早期优化效率，还有后续 OPD 的性能上限。
- **配方二：与教师对齐的提示词**：仅仅把提示词模板换成教师后训练时用的格式，三个基准上的验证性能就都提高，重叠率起点更高、收敛位置也更高，学生回收的教师性能比例从约 80% 升到约 85%。在内容层面，用教师强化学习训练集里的提示词（DAPO-Math-17K）比只是同领域的提示词（去重后的 DeepMath）效果更好，虽然重叠率反而更低，但学生在重叠词元上的累积概率质量高得多——对齐集中在更少但共享得更强的词元上。代价是学生熵显著下降，所以实践中应当与教师后训练数据之外的提示词混合，以保住策略熵和探索能力。
- **密集奖励的代价：可靠性随轨迹深度下降**：最大响应长度存在甜点区——0.5K 和 1K 提供的监督词元太少，3K 和 7K 最好，10K 和 15K 则持平或下降并在后期崩溃（重叠率骤降，伴随学生熵和梯度范数的尖峰）。崩溃从后往前传播：在 15K 设置下，高熵先出现在响应末尾，再逐步向更早的词元蔓延，教师熵也呈现同样的后缀到前缀趋势。让教师从学生生成的前缀继续写下去，其准确率优势从 1K 前缀的 +0.37 单调降到 16K 前缀的 +0.02。
- **全局有信息，不等于局部可利用**：在失败的配置里，奖励信号本身并不更差——两个教师给正确 rollout 的序列平均奖励都高于错误 rollout，AUROC 相当（JustRL-1.5B 为 0.73，R1-Distill-7B 为 0.75）。但失败运行的重叠词元优势幅度更大、梯度范数却持续更小。作者由此提出一个**未经验证的假设**：7B 教师的逐词元优势在序列内各位置之间各向异性，聚合成梯度更新时相互抵消，于是逐词元奖励很大、有效梯度却很小。验证它需要分析逐词元梯度的方向结构，论文留给了未来工作。
- **支撑集大小不关键，但 Top-1 不行**：$`k \in \{1, 4, 16, 64\}`$ 的 Top-$`k`$ OPD 与只用一个采样词元的 sampled-token OPD 在三个基准的平均分上相当，唯一明显更差的是 Top-1，它的重叠率增长不稳定并伴随熵和梯度范数的尖峰；$`k`$ 超过 4 之后收益可以忽略，计算开销却在增加。原因不在于用的词元太少，而在于 Top-1 总是选 argmax，把奖励集中到单一模式上，策略的微小变化就会改变排名第一的词元，产生无法在训练中被平均掉的不稳定信号。
- **局限**：全部实验都在数学推理上，代码和开放式任务是否遵循同样的条件与机制仍是开放问题；“新知识”这个条件隐含地依赖预训练语料的差异，但跨家族蒸馏会把数据差异与分词器、架构差异混在一起，受控的预训练消融又过于昂贵；轨迹长度的上限也让作者质疑 OPD 能否干净地扩展到长程推理和多轮智能体场景。

## 全文翻译

**格式改动**：原文的各级标题都降了一级，放在本节之下；图片取自 arXiv 源文件中的矢量图，渲染为 PNG，图 4 由原文并排的两张子图拼接而成；标题页的作者脚注（同等贡献、项目负责人、通讯作者）合并成一行；引言中的“本文概览”方框改为引用块，各节开头的 Takeaways 方框也改为引用块；提示词方框改为文本代码块，框的标题放在上方的说明里；表格中的多行表头改为普通 Markdown 表格；交叉引用改为纯文本，节号引用保留原文的 §n 写法；公式按原文编号，写在行末。中文版把提示词方框里的文字也译成了中文，模板变量 `{Question}` 和 `\boxed{}` 保持原样。参考文献，以及模型、数据集和基准名称保留英文。

Yaxuan Li$`^{*1,2}`$, Yuxin Zuo$`^{*\dagger 1}`$, Bingxiang He$`^{*\dagger 1}`$, Jinqian Zhang$`^{1}`$, Chaojun Xiao$`^{\ddagger 1}`$, Cheng Qian$`^{3}`$, Tianyu Yu$`^{1}`$, Huan-ang Gao$`^{1}`$, Wenkai Yang$`^{4}`$, Zhiyuan Liu$`^{\ddagger 1}`$, Ning Ding$`^{\ddagger 1}`$

$`^{1}`$Tsinghua University, $`^{2}`$ShanghaiTech University, $`^{3}`$University of Illinois Urbana-Champaign, $`^{4}`$Renmin University of China

\* 表示同等贡献，† 表示项目负责人，‡ 表示通讯作者。代码：<https://github.com/thunlp/OPD>。

![图 1](./img/Rethinking-On-Policy-Distillation-fig01.png)

*图 1：本文概览。JustRL-1.5B 由 DeepSeek-Distill-1.5B（DS-1.5B）经强化学习得到，Skywork-OR1-Math-7B（SW-7B）由 DeepSeek-Distill-7B（DS-7B）经强化学习得到。*

### 摘要

on-policy 蒸馏（OPD）已成为大语言模型后训练中的一项核心技术，但其训练动力学仍然缺乏理解。本文对 OPD 的动力学与机制进行了系统研究。我们首先识别出决定 OPD 成败的两个条件：(i) 学生与教师应当具有相容的思维模式；(ii) 即便思维模式一致、分数更高，教师也必须提供学生在训练期间未曾见过的、真正新的能力。我们通过弱到强的反向蒸馏验证了这些发现，表明同一家族的 1.5B 和 7B 教师从学生的视角看在分布上是难以区分的。深入到词元层面的机制，我们表明成功的 OPD 的特征是：在学生访问到的状态上，高概率词元逐步对齐，一个小的共享词元集合集中了大部分概率质量（97%–99%）。我们进一步提出两种可以挽救失败 OPD 的实用策略：off-policy 冷启动与教师对齐的提示词选择。最后，我们表明 OPD 那看似免费的密集词元级奖励是有代价的，这让人怀疑 OPD 能否扩展到长程蒸馏。

### 1 引言

on-policy 蒸馏（OPD）已迅速成为大语言模型（LLM）后训练的一项核心技术。近期的industry实践，包括 Qwen3 [Yang et al., 2025]、MiMo [Xiao et al., 2026] 和 GLM-5 [Zeng et al., 2026]，都在其后训练流水线中采用了 OPD 并报告了显著增益，使其成为传统监督微调（SFT）和结果奖励强化学习（RL）之外一个有竞争力的补充。Thinking Machines Lab [Lu and Lab, 2025] 以 RL 算力成本的一小部分复现了 Qwen3 的 OPD 配方，独立确认了 on-policy 的密集监督在实践中是一种高效的替代方案。

off-policy 蒸馏在固定的、由教师生成的序列上训练学生，因而受到曝光偏差 [Bengio et al., 2015] 的困扰；与之不同，OPD 让学生生成自己的 rollout，并利用教师的逐词元对数概率作为密集奖励信号，在学生实际访问到的状态上精炼其行为。最近，这一框架被扩展到自蒸馏设定：单个模型在获得特权信息的条件下充当自己的教师，表明该框架能够驱动持续的自我改进 [Hübotter et al., 2026, Shenfeld et al., 2026, Zhao et al., 2026b]。

然而，尽管取得了这些成功，OPD 在实践中仍然难以理解且脆弱。我们观察到一个醒目的失败模式：一个更强的教师可能完全无法提升学生，而一个更弱的教师却能从更低的初始对齐出发取得成功。但很少有研究探讨教师的词元级信号为何能把学生分布推向期望的方向，以及它在什么条件下会失效。

> **本文概览**
>
> - **现象（§3）**——*OPD 何时成功、何时失败？* 区分有效 OPD 的两个经验规律：思维模式一致性；更高的分数 ≠ 新知识。
> - **机制（§4）**——*OPD 为什么在词元层面有效？* 高概率词元上的渐进对齐支配着 OPD：重叠词元稳步增长；只靠重叠词元就足够。
> - **配方（§5）**——*如何挽救失败的 OPD？* 两种策略可以弥合思维模式的差距：off-policy 冷启动；与教师对齐的提示词。

我们对 OPD 的训练动力学进行了系统研究，从经验条件出发，经由词元级机制，最终给出实用配方。

**现象（§3）。** 我们考察区分有效与无效 OPD 的经验规律，并识别出两个支配因素。*(i) 思维模式一致性*：学生与教师应当具有一致的思维模式（例如 top-$`k`$ 词元分布中更高的重叠率）。即便教师取得了更高的基准分数，模式不匹配也会造成低初始重叠，而训练无法将其完全弥补。*(ii) 更高的分数 ≠ 新知识*：即便思维模式一致且基准分数更高，教师也应当提供学生尚未获得的知识。当两个模型用相同的数据和配方训练时，它们会在各自的规模上收敛到相似的分布，使教师几乎没有可传递的信号。只有当教师携带了学生此前未曾见过的知识时，OPD 才能带来实质性增益。我们通过反向蒸馏实验验证了这两个条件，这些实验进一步揭示：OPD 从根本上学习的是思维模式，而不只是从模式一致性中获益，而且训练动力学可以与基准分数完全脱钩。

**机制（§4）。** 随后我们基于这些条件考察词元级机制。在我们研究的所有设定中，有效的 OPD 都表现出一个一致的特征：在学生访问到的状态上，学生与教师的分布逐步变得更加相似。高概率词元越来越重合（重叠率从 72% 升到 91%），两个分布之间的熵差收窄，共享的 top-$`k`$ 词元集中了 97%–99% 的合计概率质量。相比之下，失败的运行从一开始就表现出重叠停滞和持续的熵不匹配。我们进一步表明，仅把监督限制在重叠词元上就能达到完整 top-$`k`$ 的性能，这确认了重叠集合是 OPD 梯度信号的主要所在。

**配方（§5）。** 在现象学分析的指引下，我们提出两种互补的策略，它们能在原本会失败的配置中挽救 OPD：*(i) off-policy 冷启动*，即在 OPD 之前先在教师生成的 rollout 上做一个预热 SFT 阶段，通过抬高初始重叠率来弥合思维模式的差距；*(ii) 与教师对齐的提示词选择*，即使用取自教师后训练数据的提示词来强化高概率词元上的对齐，但代价是学生熵大幅降低，因而有必要与分布外的提示词混合使用。在这两种情形下，被挽救的运行都表现出与天然成功的运行相同的动态特征（见 §4）：重叠率稳步上升、词元级优势改善、熵差收窄。

最后，我们考察 OPD 密集监督的代价（§6）。我们表明奖励质量会随轨迹深度系统性地退化，而且不稳定性起源于靠后的词元，然后沿轨迹向前传播。令人惊讶的是，即便是失败的教师也能提供在全局上与 rollout 正确性相关的奖励，这说明失败不是信号质量的问题，而是局部优化几何的问题。更大的教师可能在学生策略附近诱导出一个局部平坦的奖励曲面，使得词元级梯度即便在全局信号富含信息时也难以奏效。这些发现揭示了监督密度与监督可靠性之间的根本张力，也指出了当前 OPD 在长程推理和智能体场景中的局限。

### 2 预备知识

#### 2.1 记号

设 $`x = (x_1, \ldots, x_n)`$ 表示一个输入提示词，$`y = (y_1, \ldots, y_m)`$ 表示一个回答。我们用 $`y_{<t} \triangleq (y_1, \ldots, y_{t-1})`$ 表示直到第 $`t`$ 步的前缀。我们考虑两个 LLM：学生 $`\pi_\theta`$ 和教师 $`\pi_T`$，各自在词表 $`\mathcal{V}`$ 上定义一个下一词元分布 $`\pi(\cdot \mid x, y_{<t})`$。我们用 $`y \sim \pi_\theta(\cdot \mid x)`$ 表示从学生自回归采样得到的一个回答。$`\mathcal{D} = \{(x^{(i)}, y^{(i)})\}_{i=1}^N`$ 表示一个固定的提示词–回答对数据集，其中的输出由教师生成，$`\mathcal{D}_x \triangleq \{x^{(i)}\}_{i=1}^N`$ 表示对应的提示词集合。知识蒸馏（KD）通过最小化两个分布之间的散度，把知识从 $`\pi_T`$ 传递给 $`\pi_\theta`$。一个标准的选择是 Kullback-Leibler（KL）散度，对于 $`\mathcal{V}`$ 上的两个分布 $`P`$ 和 $`Q`$ 定义为 $`D_{\mathrm{KL}}(P \| Q) = \sum_{v \in \mathcal{V}} P(v) \log \frac{P(v)}{Q(v)}`$。

#### 2.2 on-policy 蒸馏

on-policy 蒸馏（OPD）在从当前学生 $`\pi_\theta`$ 采样得到的轨迹上计算监督信号。给定提示词 $`x \sim \mathcal{D}_x`$，学生采样出一个回答 $`\hat{y} = (\hat{y}_1, \ldots, \hat{y}_{T}) \sim \pi_\theta(\cdot \mid x)`$，其中 $`T \triangleq |\hat{y}|`$ 表示 rollout 长度。随后，两个模型都在学生生成的前缀 $`\hat{y}_{<t}`$ 上被评估，在每一步 $`t`$ 得到两个下一词元分布：对 $`v \in \mathcal{V}`$，$`p_t(v) \triangleq \pi_\theta(v \mid x, \hat{y}_{<t})`$ 和 $`q_t(v) \triangleq \pi_T(v \mid x, \hat{y}_{<t})`$。

一个标准的形式化是在学生生成的轨迹上最小化序列级反向 KL：

```math
\mathcal{L}_{\mathrm{OPD}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_x} \Bigl[ D_{\mathrm{KL}}\bigl(\pi_\theta(\cdot \mid x)\;\|\;\pi_T(\cdot \mid x)\bigr) \Bigr] \qquad (1)
```

利用自回归分解，这个序列级目标允许一个精确的词元级分解：

```math
\mathcal{L}_{\mathrm{OPD}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_x,\; \hat{y} \sim \pi_\theta(\cdot \mid x)} \left[ \sum_{t=1}^{T} D_{\mathrm{KL}}(p_t \| q_t) \right] \qquad (2)
```

在实践中，不同实现计算这个精确的逐词元反向 KL 的方式各不相同：全词表 OPD 直接优化式 (2)，采样词元 OPD 对每个词元级 KL 项使用一个无偏的蒙特卡洛估计量，top-$`k`$ OPD 则用一个基于子集的近似替代全词表 KL。下面我们描述这三种常见的监督粒度。

**采样词元 OPD。** 最轻量的变体只评估学生采样到的那个词元，这也是此前 on-policy 蒸馏工作中最常见的实现 [Lu and Lab, 2025, Xiao et al., 2026, Yang et al., 2026b]。给定 $`\hat{y}_t \sim p_t`$，逐词元损失为 $`\ell_t^{\mathrm{sample}} \triangleq \log p_t(\hat{y}_t) - \log q_t(\hat{y}_t)`$，聚合为：

```math
\mathcal{L}_{\mathrm{OPD}}^{\mathrm{sample}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_x,\; \hat{y} \sim \pi_\theta(\cdot \mid x)} \left[\sum_{t=1}^{T} \ell_t^{\mathrm{sample}}\right] \qquad (3)
```

由于 $`\mathbb{E}_{\hat{y}_t \sim p_t}[\ell_t^{\mathrm{sample}}] = D_{\mathrm{KL}}(p_t \| q_t)`$，每个 $`\ell_t^{\mathrm{sample}}`$ 都是词元级反向 KL 的一个无偏单样本估计量。

**全词表 OPD。** 在另一个极端，可以在每个前缀上对整个词表计算散度：

```math
\mathcal{L}_{\mathrm{OPD}}^{\mathrm{full}}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_x,\; \hat{y} \sim \pi_\theta(\cdot \mid x)} \left[\sum_{t=1}^{T} D_{\mathrm{KL}}(p_t \| q_t)\right] \qquad (4)
```

与采样词元 OPD 相比，这会产生更密集的梯度，代价是对批大小 $`B`$、序列长度 $`T`$ 和词表大小 $`M = |\mathcal{V}|`$ 需要 $`O(BTM)`$ 的显存。

**Top-$`k`$ OPD。** Top-$`k`$ OPD 通过把散度计算限制在子集 $`S_t \subseteq \mathcal{V}`$ 上，在采样词元 OPD 与全词表 OPD 之间提供了一种折中设计。这里我们关注学生 top-$`k`$ 变体，它选取学生赋予最高概率的 $`k`$ 个词元，即 $`S_t = \operatorname{TopK}(p_t, k)`$。定义 $`S_t`$ 上重新归一化的学生与教师分布为：

```math
\bar{p}_t^{(S_t)}(v) = \frac{p_t(v)\,\mathbf{1}[v \in S_t]}{\sum_{u \in S_t} p_t(u)}, \qquad \bar{q}_t^{(S_t)}(v) = \frac{q_t(v)\,\mathbf{1}[v \in S_t]}{\sum_{u \in S_t} q_t(u)}
```

随后通过最小化子集 KL 散度 $`D_{\mathrm{KL}}\bigl(\bar{p}_t^{(S_t)} \| \bar{q}_t^{(S_t)}\bigr)`$ 来执行蒸馏，得到轨迹级目标：

```math
\mathcal{L}_{\mathrm{OPD}}^{\mathrm{top}\text{-}k}(\theta) = \mathbb{E}_{x \sim \mathcal{D}_x,\; \hat{y} \sim \pi_\theta(\cdot \mid x)} \left[ \sum_{t=1}^{T} D_{\mathrm{KL}}\!\bigl(\bar{p}_t^{(S_t)} \,\|\, \bar{q}_t^{(S_t)}\bigr) \right] \qquad (5)
```

这一形式丢弃了 $`S_t`$ 之外的质量，因此仍然是对全词表反向 KL 的一个近似，但它大幅降低了教师查询成本，同时在学生的高概率区域上保留了多词元监督。

#### 2.3 动态指标

我们把学生和教师在第 $`t`$ 步的 top-$`k`$ 集合分别定义为 $`S_t^{(p)} = \operatorname{TopK}(p_t, k)`$ 和 $`S_t^{(q)} = \operatorname{TopK}(q_t, k)`$。以下指标将在后续实验中贯穿 OPD 训练全过程进行监控。

**重叠率。** 该指标量化学生与教师候选空间之间的对齐程度。它被定义为同时出现在学生和教师 top-$`k`$ 集合中的词元所占的平均比例：

```math
\mathcal{M}_{\text{overlap}} \triangleq \mathbb{E}_{t} \left[ \frac{|S_t^{(p)} \cap S_t^{(q)}|}{k} \right] \qquad (6)
```

低重叠率表明学生的概率质量集中在与教师不相交的一组词元上，意味着显著的策略偏离或“模式失配”。反之，接近 $`1.0`$ 的比率意味着学生已经成功定位到教师的支撑区域。

**重叠词元优势。** 为了衡量重叠词元内部的分布一致程度，我们定义 $`A_t(v) \triangleq \bar{p}_t(v)(\log \bar{q}_t(v) - \log \bar{p}_t(v))`$，其中 $`\bar{p}_t, \bar{q}_t`$ 是在 $`S_t^{(p)} \cap S_t^{(q)}`$ 上重新归一化的学生与教师分布。该指标对这一量取平均：

```math
\mathcal{M}_{\text{adv}} \triangleq \mathbb{E}_{t}\!\left[ \frac{1}{|S_t^{(p)} \cap S_t^{(q)}|} \sum_{v \in S_t^{(p)} \cap S_t^{(q)}} A_t(v) \right] \qquad (7)
```

接近零的值表示高质量的对齐：学生以恰当的置信度把质量放在教师偏好的词元上。反之，较大的负值表示在交集内部，学生相对教师过于自信（$`p_t`$ 高而 $`q_t`$ 较低）。

**熵与熵差。** 为了监控策略的分布性质，我们在学生的 rollout 上追踪学生熵 $`H(p_t)`$ 和教师熵 $`H(q_t)`$，并定义熵差为：

```math
\Delta H_t = \left| H(q_t) - H(p_t) \right| \qquad (8)
```

$`\Delta H_t`$ 是模式对齐的一个状态相关指标。较大的差距意味着学生与教师在同样被访问到的状态上，在置信度和多样性方面存在显著失配；而它收敛到零则表明学生已经在其生成的轨迹上匹配了教师的不确定性特征。

### 3 on-policy 蒸馏的现象学

在考察 OPD 的词元级机制之前，我们先问一个更宽泛的问题：什么条件支配着 OPD 的有效性？一个自然的假设是，更强的教师应当总是带来更好的蒸馏结果，但我们观察到了这一假设失效的配置。我们在受控设定下比较 OPD 运行，并识别出共同支配结果的两个条件。

> **要点**
>
> - **思维模式一致性。** 学生与教师应当共享相容的思维模式。即便教师取得更高的基准分数，较大的失配也会削弱词元级的蒸馏信号（§3.1）。
> - **更高的分数 ≠ 新知识。** 教师应当提供学生在训练期间未曾见过的知识。即便思维模式一致、分数更高，教师也可能提供不了真正新的知识，使 OPD 失去驱动信号（§3.2）。

#### 3.1 思维模式一致性

![图 2](./img/Rethinking-On-Policy-Distillation-fig02.png)

*图 2：从两个思维模式不同的教师向同一个学生（Qwen3-1.7B-Base）做 OPD。GRPO 教师取得了更强的性能（左）和更高的初始重叠率（右），说明思维模式的相容性支配着 OPD 的有效性。*

我们首先研究 OPD 是否需要学生与教师之间具有相容的思维模式。更强的教师并不保证更好的蒸馏：推理模式上的较大失配会削弱蒸馏信号，不管教师在基准上有多大优势。

**设置。** 我们以 Qwen3-1.7B-Base [Yang et al., 2025] 为学生，比较两个教师：Qwen3-4B（非思考模式）[Yang et al., 2025] 和 Qwen3-4B-Base-GRPO，后者是用 GRPO [Shao et al., 2024] 对 Qwen3-4B-Base [Yang et al., 2025] 做 zero-RL 得到的（详细训练设置见附录 A.1）。由于学生也是一个基座模型，我们预期它的思维模式更接近经 GRPO 训练的教师。我们用 DAPO-Math-17K 数据集 [Yu et al., 2025] 做两个 OPD 实验，仅在教师模型的选择上有所不同。除非另有说明，所有实验都使用附录 A.2 中描述的默认超参数，并在 AIME 2024 [Li et al., 2024]、AIME 2025 [Balunović et al., 2025] 和 AMC 2023 [Li et al., 2024] 上评估。遵循标准做法，我们对每道题以温度 0.7、top-$`p`$ 0.95 采样 16 个解，验证时的最大响应长度为 31,744 个词元。我们报告 16 个样本的平均准确率（avg@16）作为主要评估指标。

![图 3](./img/Rethinking-On-Policy-Distillation-fig03.png)

*图 3：两个教师（Qwen3-4B 非思考模式 vs. Qwen3-4B-Base-GRPO）在 AIME 2024、AIME 2025 和 AMC 2023 上的验证性能。*

**结果。** 如图 2 所示，尽管两个教师的性能大体相当（见图 3），从 Qwen3-4B-Base-GRPO 蒸馏始终优于从 Qwen3-4B（非思考模式）蒸馏。尽管在基准上表现更弱，GRPO 教师却表现出更高的初始重叠率，说明它的思维模式与学生更为接近。虽然两条重叠率曲线在训练后期趋于收敛，性能差距却持续存在，说明早期阶段的思维模式失配造成了一种蒸馏收益的损失，而这种损失在训练后期无法弥补。我们在附录 A.3 中逐个基准报告验证准确率，同样的总体趋势在所有数据集上都成立。

#### 3.2 新知识，而不只是规模

思维模式一致性本身并不能解释我们的所有观察。即便教师分数更高、且与学生共享一致的思维模式，OPD 仍可能失败。

**设置。** 我们构建两组跨模型家族的受控对比。在 DeepSeek 家族中，我们以 DeepSeek-R1-Distill-Qwen-1.5B（R1-Distill-1.5B）[Guo et al., 2025] 为学生，比较两个教师：DeepSeek-R1-Distill-Qwen-7B（R1-Distill-7B）[Guo et al., 2025] 和 Skywork-OR1-Math-7B [He et al., 2025b]，后者是对 R1-Distill-7B 做 RL 后训练得到的。在 Qwen 家族中，我们以 Qwen3-1.7B（非思考模式）[Yang et al., 2025] 为学生，比较两个教师：Qwen3-4B（非思考模式）和 Qwen3-4B-Non-Thinking-RL-Math [Yang et al., 2026b]，后者是在 DeepMath [He et al., 2025c] 的一个 57K 子集上对 Qwen3-4B（非思考模式）做 RL 得到的。在两种设定中，关键对比都在于：一个来自同一训练流水线的教师，与一个通过进一步 RL 获得了额外能力的教师。所有运行都使用与之前相同的数据集和训练配方。

![图 4](./img/Rethinking-On-Policy-Distillation-fig04.png)

*图 4：在两个模型家族上，比较教师有无额外 RL 后训练时的 OPD 性能。**左：**DeepSeek 家族。**右：**Qwen 家族。经后训练的教师带来了显著更强的增益和更高的师生*差距回收率*。*

**结果。** 如图 4 所示，两个家族都表现出一致的模式。**来自同一流水线的教师**带来的提升有限，而**经后训练的教师**在所有基准上都产生了显著更强的增益。重要的是，经后训练的教师不仅取得了更高的绝对性能，还回收了师生差距中大得多的一部分，这由*差距回收率* $`(\mathrm{Acc}_{\text{after OPD}} - \mathrm{Acc}_{\text{before OPD}}) / (\mathrm{Acc}_{\text{teacher}} - \mathrm{Acc}_{\text{before OPD}})`$ 衡量。这说明这些教师通过 RL 获得的额外能力更容易通过 OPD 传递。由于经后训练的教师源自相同的基座检查点，它们的思维模式仍然大体对齐，这一点也在重叠率动态中得到观察。因此，提升来自教师通过 RL 获得的新能力。

#### 3.3 通过反向蒸馏进行验证

我们设计了一个反向蒸馏实验，作为同时验证两个条件、并揭示 OPD 本质更深层洞见的对比。

**设置。** JustRL-DeepSeek-1.5B（JustRL-1.5B）[He et al., 2025a] 是通过对 R1-Distill-1.5B 做 RL 得到的。我们现在把方向反过来，以 JustRL-1.5B 为学生，从 R1-Distill-1.5B（它自己 RL 之前的检查点）蒸馏。我们还用 R1-Distill-7B 作为教师来做对比。注意 R1-Distill-7B 的基准分数略高于 JustRL-1.5B，而 R1-Distill-1.5B 则明显更弱。

![图 5](./img/Rethinking-On-Policy-Distillation-fig05.png)

*图 5：以 JustRL-1.5B 为学生、两个同家族教师（R1-Distill-1.5B 和 R1-Distill-7B）做反向蒸馏。尽管 R1-Distill-7B 的分数高于 JustRL-1.5B，两次运行都让学生退回到大致相同的水平，表明 OPD 的训练动力学由思维模式而非基准性能支配。*

**结果。** 图 5 揭示了两个醒目的现象。第一，把 JustRL-1.5B 向它自己 RL 之前的检查点 R1-Distill-1.5B 蒸馏，会让学生几乎精确地退回到它 RL 之前的性能，抹去了通过 RL 获得的所有增益。第二，当我们把教师换成 R1-Distill-7B——一个来自同一家族、规模大得多、分数甚至略高的模型——训练轨迹几乎无法区分：尽管在基准上胜过 JustRL-1.5B，R1-Distill-7B 把学生驱动到了与更弱的 1.5B 教师相同的退化水平。由于 OPD 在学生生成的轨迹上最小化反向 KL 散度，这种收敛意味着两个教师在学生访问到的状态上诱导出了几乎相同的局部目标分布，尽管它们的规模不同。

这些结果得出若干结论：

- **思维模式至关重要，而且 OPD 从根本上学习的是思维模式。** 从 R1-Distill-1.5B 向 JustRL-1.5B 蒸馏会让 JustRL-1.5B 退回到它 RL 之前的性能。这表明 OPD 主动获取了教师的思维模式，并覆盖了学生自己的思维模式。这正是思维模式一致性为何重要的原因：如果差距太大，学生可能无法有效学习。
- **基准性能不能预测 OPD 的结果。** R1-Distill-7B 的分数高于 JustRL-1.5B，但蒸馏没有带来任何提升，反而导致退化。这表明 OPD 的训练动力学可以完全独立于教师的基准性能，甚至可能朝相反方向移动。
- **更高的分数不意味着对 OPD 而言有新知识。** R1-Distill-7B 和 R1-Distill-1.5B 属于同一模型家族，仅在规模上不同。两个模型对学生产生的效果无法区分，这已经确认了：(i) 更高的分数（R1-Distill-7B）可能只是反映了对同一数据不同程度的拟合，而非真正新颖的能力。要让 OPD 产生增益，教师应当拥有学生在训练期间尚未见过的知识；以及 (ii) 尽管规模不同，R1-Distill-7B 和 1.5B 表现出相同的思维模式。

反向蒸馏实验与 §3.1、§3.2 中的正向对比共同巩固了这两个条件。思维模式一致性与更高的初始重叠和更强的 OPD 结果相关联，而新知识（例如来自进一步的后训练）能在重叠已经很高时带来更大的可传递增益。

### 4 on-policy 蒸馏的机制

§3 识别出支配 OPD 有效性的两个条件：思维模式一致性，以及超出同一模型家族的新知识。我们现在考察这些条件在训练中借以显现的词元级机制。通过比较成功与失败的 OPD 运行，我们表明有效的蒸馏是由高概率词元上的渐进对齐驱动的。

> **要点**
>
> - **渐进对齐。** 在学生访问到的状态上，学生与教师高概率 top-$`k`$ 词元之间的重叠在整个训练过程中稳步增加；失败的运行从一开始就表现出重叠停滞。
> - **重叠充分性。** 优化的几乎全部效果都集中在共享的 top-$`k`$ 词元上；只优化这些重叠词元就足以匹配标准 OPD，而非重叠词元贡献甚微。

#### 4.1 高概率词元的渐进对齐

我们在相同设定下比较同一个学生从两个不同教师蒸馏的动力学，一个带来明显提升，另一个毫无提升。我们发现成功的 OPD 本质上是由学习学生与教师之间共享的高概率词元驱动的。

**设置。** 我们选择 R1-Distill-1.5B 为学生，比较两个教师：JustRL-1.5B 和 R1-Distill-7B。两个教师的数学性能相当，后者略强。我们使用与之前相同的 DAPO-Math-17K 数据集和训练设置，并在 OPD 过程中监控三个动态指标。

![图 6](./img/Rethinking-On-Policy-Distillation-fig06.png)

*图 6：同一个学生（R1-Distill-1.5B）与两个教师的成功 vs. 失败 OPD。**上：**三个基准上的 avg@16 准确率。虚线表示教师性能。**下：**训练过程中的三个动态。成功的蒸馏（JustRL-1.5B）表现出上升的重叠率和收窄的熵差，而这些趋势在失败的运行（R1-Distill-7B）中不存在。*

**结果。** 图 6 显示了截然不同的结果。从 JustRL-1.5B 蒸馏带来了持续的增益，最终学生回收了与教师差距的 $`80\%`$ 以上，而从 R1-Distill-7B 蒸馏尽管教师整体更强，却未能带来任何提升。训练动力学（图 6，下）揭示了背后的分化。**在成功的运行中，重叠率稳步上升，重叠词元优势朝零改善，熵差收窄，表明学生逐步定位到教师的高概率区域、在该区域内校准其质量、并匹配教师的局部置信度。在失败的运行中，三个指标全部停滞。**

有两点值得强调。第一，重叠词元在整个训练过程中对两个模型都占据 $`97\%`$-$`99\%`$ 的总概率质量（见附录 B.1），所以上升的重叠反映的是在概率上占主导的词元上的对齐，而不只是集合层面的巧合。第二，重叠词元优势的改善表明，OPD 的主要优化信号在于重新加权重叠区域内部的概率，而不在于该区域之外的词元。

我们还在附录 B.2 中报告了辅助优化指标（策略损失、梯度范数和极端优势词元的概率差），它们显示出一致的次级模式：成功的运行表现出损失下降和持续的梯度幅度，而失败的运行表现出微弱的梯度和持续的概率差异。我们在附录 B.3 中进一步验证这些发现能推广到不同的模型对，那里以 R1-Distill-7B 为学生、在相同设定下搭配两个不同的教师。

#### 4.2 只优化共享词元就足够

上述分析表明高概率词元对齐与 OPD 的成功相关。我们进一步考察这种相关是否是因果的：重叠区域是否不仅是对齐涌现的地方，也是驱动优化的区域。我们设计了一个有针对性的消融，把 top-$`k`$ 支撑集分解为其重叠和非重叠两部分，分别单独训练。

**设置。** 使用 §4.1 中成功的 OPD 设定（JustRL-1.5B $`\to`$ R1-Distill-1.5B），我们比较三个仅在蒸馏损失覆盖哪些词元上有所不同的变体：(i) **Student Top-$`k`$**，在完整的学生 top-$`k`$ 支撑集 $`S_t^{(p)}`$ 上优化；(ii) **Overlap Top-$`k`$**，把优化限制在学生与教师 top-$`k`$ 集合的交集 $`S_t^{(p)} \cap S_t^{(q)}`$ 上；(iii) **Non-Overlap Top-$`k`$**，把优化限制在它们的对称差 $`S_t^{(p)} \triangle S_t^{(q)}`$ 上。我们把默认的 $`k`$ 设为 $`16`$。

![图 7](./img/Rethinking-On-Policy-Distillation-fig07.png)

*图 7：Top-$`k`$ OPD 中优化支撑集的消融。Overlap Top-$`k`$ 匹配 Student Top-$`k`$，而 Non-Overlap Top-$`k`$ 则明显更弱。*

**结果。** 如图 7 所示，只优化重叠区域就足以在全部三个基准上恢复标准 Student Top-$`k`$ OPD 的几乎全部收益，而 Non-Overlap Top-$`k`$ 始终更弱。这说明 OPD 的主要增益来自共享高概率区域上的梯度，而非来自非重叠词元。这也解释了为什么 Student Top-$`k`$ 和 Overlap Top-$`k`$ 的表现如此相似：学生专属支撑集中额外的那些词元携带的概率质量非常少。与此一致，Student Top-$`k`$ 和 Overlap Top-$`k`$ 的重叠词元优势曲线几乎无法区分，而 Non-Overlap Top-$`k`$ 的幅度小得多，表明其在重叠词元上的有效梯度弱得多。

**重叠优化是自我强化的。** Student Top-$`k`$ 和 Overlap Top-$`k`$ 都把重叠率从约 $`72\%`$ 稳步抬升到 $`91\%`$ 以上，而 Non-Overlap Top-$`k`$ 则先下降、随后只部分恢复（图 7，左下）。这揭示了一种自我强化的动态：一旦一个词元进入共享的高概率区域并被教师偏好，反向 KL 更新就会把更多质量集中到它上面，逐步把竞争的非重叠词元挤出学生的 top-$`k`$ 集合。于是重叠区域不是尽管优化而增长，而是因为优化而增长，形成一个在整个训练中维持对齐的良性循环。

总体而言，这些结果支持 OPD 的一个统一机制：它的主要效果是在学生访问到的状态上，逐步精炼学生在教师支持的高概率词元上的分布。这种对齐既是成功 OPD 的特征，也是它的操作所在：只优化重叠词元就足够，而非重叠词元贡献甚微。当 §3 识别出的条件满足时，这种自我强化的动态驱动稳步提升；当条件不满足时，重叠停滞，训练无法推进。

### 5 实用配方

在 §3 中，我们识别出 OPD 成功的两个条件。拥有新知识是教师的一种内在属性，而教师与学生之间的思维模式差距则可以通过训练设计来缩小。在本节中，我们提出两种互补的策略，它们通过改善重叠动态，在原本会失败的配置中挽救 OPD。

> **要点**
>
> - **off-policy 冷启动（§5.1）。** 在 OPD 之前先在教师生成的 rollout 上微调学生，弥合初始的思维模式差距，从而从一开始就带来更高的重叠和始终更强的最终性能。
> - **与教师对齐的提示词（§5.2）。** 使用取自教师后训练数据的提示词能锐化高概率词元上的对齐，不过这类提示词应当与分布外的提示词混合，以防止熵坍缩。

#### 5.1 以教师 rollout 做 off-policy 蒸馏作为冷启动

当学生与教师的思维模式差异很大时，纯 OPD 可能无效，因为从学生的初始策略出发，教师的词元级监督很难被学生利用。为缓解这种失配，我们考虑一个两阶段框架：首先通过在教师生成的 rollout 上做监督微调（SFT）来做 off-policy 蒸馏，让学生更接近教师的思维模式，然后再继续用标准 OPD 训练。

![图 8](./img/Rethinking-On-Policy-Distillation-fig08.png)

*图 8：OPD 之前做 off-policy 冷启动的效果，固定教师为 Qwen3-4B（非思考模式）。两条曲线分别对应从 Qwen3-1.7B-SFT 和 Qwen3-1.7B-Base 做的 OPD。*

**设置。** 我们以 Qwen3-1.7B-Base 为学生、Qwen3-4B（非思考模式）为教师来研究这一设定。我们使用 OpenThoughts3-1.2M [Guha et al., 2025] 的数学领域子集作为 SFT 的提示词来源。教师在该数据集的一个子集上生成 200K 条回答，我们用这些教师 rollout 对学生做 SFT 作为冷启动，得到 Qwen3-1.7B-SFT。随后我们从这个 SFT 初始化继续用 OPD 训练，使用 OpenThoughts 中剩余的提示词（对 SFT 提示词子集去重后约 30K 条）。作为对照，我们与一个纯 OPD 基线比较：它直接从 Qwen3-1.7B-Base 开始，使用相同的教师和 OPD 提示词集合，但在 OPD 之前不做任何冷启动蒸馏。详细的离线 rollout 和 SFT 配置见附录 C.1。

**结果。** 如图 8 所示，两阶段方法大幅优于纯 OPD。从 Qwen3-1.7B-SFT 开始，始终比直接从 Qwen3-1.7B-Base 开始带来更好的验证性能。而且性能差距在整个训练中持续存在，表明 off-policy 冷启动不仅改善了早期优化，还提升了后续 OPD 的最终性能上限。

重叠动态支持同样的结论。SFT 初始化的学生从一个高得多的重叠率开始，并保持平滑、稳定的轨迹，而基座初始化的学生起点更低，在逐步恢复之前表现出明显的不稳定。SFT 初始化的学生熵差也小得多，表明它从一开始就更贴近教师的置信度特征。这些观察确认了 off-policy 蒸馏降低了初始的模式失配，使得教师的词元级监督一旦 OPD 开始就能被立即利用。关于重叠质量动态的更详细分析见附录 C.2。

#### 5.2 利用教师后训练的提示词

上一节通过 SFT 把学生拉近教师来缩小思维模式差距。另一种改善对齐的方式来自数据侧。由于教师的策略是由后训练期间见过的提示词塑造的，我们发现在 OPD 期间使用与教师对齐的提示词能带来更有效的监督。

![图 9](./img/Rethinking-On-Policy-Distillation-fig09.png)

*图 9：提示词模板对齐的效果。与教师对齐的模板在整个训练中带来更高的准确率和重叠增长。*

![图 10](./img/Rethinking-On-Policy-Distillation-fig10.png)

*图 10：提示词内容对齐的效果。与教师对齐的提示词内容带来更强的性能，共享词元上的质量集中度更高，熵也明显更低。*

**设置。** 我们在两个粒度上做实验：提示词*模板*是否匹配重要，以及提示词*内容*是否匹配重要。

**提示词模板。** 教师是 JustRL-1.5B，学生是 R1-Distill-1.5B。提示词集合为 DAPO-Math-17K，仅提示词模板不同。*原始*模板是此前所有实验（除非另有说明）使用的标准 DAPO 格式，而*与教师对齐*的模板匹配 JustRL 后训练时使用的格式：

*原始 DAPO 模板。*

```text
请一步一步解答下面的数学题。你的回答的最后一行应为 Answer: $Answer（不含引号）的形式，其中 $Answer 是该题的答案。{Question} 记得把你的答案单独放在最后一行，写在 “Answer:” 之后。
```

*与教师对齐的模板。*

```text
{Question} 请一步一步推理，并把你的最终答案放在 \boxed{} 中。
```

因此，两次运行包含相同的数学题，但在把任务呈现给模型的方式上不同。这一设计隔离出与教师的提示词模板对齐的效果，同时保持底层题目内容不变。

**提示词内容。** 教师是 §3.1 介绍的 Qwen3-4B-Base-GRPO，学生是 Qwen3-1.7B-Base。我们比较两个规模相当的提示词集合：DAPO-Math-17K（与教师的 RL 训练数据集对齐）和一个对 DAPO-Math-17K 去重后的 DeepMath 子集（见附录 C.3）。这一设计检验 OPD 是否能从与教师后训练数据相同的提示词中获益，而不只是从同领域的提示词中获益。

**结果。** 图 9 的提示词模板设定表明，仅仅切换到与教师对齐的模板，就在全部三个基准上改善了验证性能。重叠动态支持这一结果：与教师对齐的模板那次运行从更高的重叠率开始，并收敛到更高的水平，这表明即便是提示词模板上的微小改变，也能通过让学生生成的状态与教师更兼容，而对 OPD 产生实质影响。附录 C.4 中逐个基准的分解显示了相同的趋势。

图 10 的提示词内容设定显示出类似的下游优势，但带有一个微妙之处：与教师对齐的提示词在整个训练中产生了更低的重叠率。然而，学生在重叠词元上的累积概率质量却高得多，表明学生把质量集中在更少但共享得更强的词元上。因此，即便重叠集合更小，在高概率词元上的有效对齐反而更强。

**与此同时，我们观察到使用与教师对齐的提示词会导致训练期间学生熵显著降低。** 这表明只在教师后训练期间见过的提示词上做 OPD 未必总是理想的，因为它可能过度降低策略熵。在实践中，一个更稳健的策略可能是把与教师对齐的提示词和教师后训练数据之外的提示词混合，以保住策略熵，维持学生探索的能力。

总体而言，这些结果表明 OPD 不仅受益于一个合适的教师，还受益于一个良好匹配的提示词集合。更接近教师后训练数据的提示词能改善下游性能，并锐化在最重要的共享词元上的对齐，但使用时要谨慎，以免过度抑制学生熵。

### 6 讨论

OPD 的吸引力在于它的密集监督：每个词元都从教师那里得到一个奖励信号，这与 RL 中使用的稀疏的结果级奖励形成对比。然而，这种更高的监督密度是有代价的。上面各节都隐含地依赖于教师的词元级奖励在学生访问到的状态上是可靠的，但我们已经看到这一假设可能失效。在本节中，我们考察奖励信号本身，检视它的性质和局限。

![图 11](./img/Rethinking-On-Policy-Distillation-fig11.png)

*图 11：(a) 不同响应长度下三个基准上的验证准确率。(b) 不同学生前缀截断长度下，教师续写带来的准确率增益。*

![图 12](./img/Rethinking-On-Policy-Distillation-fig12.png)

*图 12：OPD 在不同最大响应长度下的训练动力学。*

#### 6.1 奖励质量随轨迹深度下降

我们首先考察教师的奖励质量如何随响应长度变化。

**响应长度存在一个甜点区。** 位置 $`t`$ 上的监督依赖于教师在学生生成的前缀 $`y_{<t}`$ 下的条件分布 $`\pi_{T}(y_t \mid x, y_{<t})`$，而这个前缀可能偏离教师自己自然会产生的轨迹。我们在六种最大响应长度下，用 JustRL-1.5B 训练 R1-Distill-1.5B 共 200 步。如图 11(a) 所示，非常短的响应（0.5K 和 1K）提供的被监督词元太少，不利于样本高效学习，而中等长度（3K 和 7K）产生最强的结果。超出这一范围（10K 和 15K），性能持平或下降。图 12 中的训练动力学确认，中等长度产生平滑的重叠增长，而 10K 和 15K 表现出后期崩溃，重叠率骤降，并伴随学生熵和梯度范数的尖峰。

**不稳定性起源于靠后的词元。** 这种崩溃从哪里开始？在 15K 设定下，把学生熵作为输出位置的函数、跨训练步来分析，揭示出一个清晰的从后到前的模式：如图 13 所示，高熵首先出现在响应的末尾，然后随着训练推进逐步向更早的词元传播。教师熵表现出类似的后缀到前缀趋势（见附录 D.1），这与教师在靠后的位置遇到越来越不熟悉的前缀、从而产生更嘈杂的奖励、进而破坏学生稳定性的说法一致。

![图 13](./img/Rethinking-On-Policy-Distillation-fig13.png)

*图 13：在最大响应长度 15K 的 OPD 训练中，跨解码位置的平均学生熵，测量自第 180 步到第 250 步的学生生成轨迹。*

**教师续写随前缀深度退化。** 我们进一步通过测试教师能否在从学生生成的前缀出发时仍改进学生的续写来探究这一点。我们从 DAPO-Math-17K 采样 2K 条提示词，生成完整的学生 rollout，并选出超过 16K 词元的那些。随后我们在多个位置截断每条 rollout，让教师从得到的前缀继续写。图 11(b) 显示，教师的准确率优势单调下降，从 1K 前缀处的 +0.37 降到 16K 前缀处的仅 +0.02。

综合来看，这些结果揭示了 OPD 词元级监督中的一个根本权衡。密集奖励在中等长度的推理轨迹上有效，但其可靠性随深度退化，因为学生前缀越来越偏离教师熟悉的状态。这表明 OPD 可能无法干净地扩展到更长程的设定，例如加长的思维链或智能体式的多轮交互。

![图 14](./img/Rethinking-On-Policy-Distillation-fig14.png)

*图 14：正确与错误学生 rollout 的序列平均奖励分布。两个教师都给正确的 rollout 更高的奖励，AUROC 相当（0.73 和 0.75）。*

#### 6.2 全局有信息的奖励不保证局部可利用

上一小节表明奖励质量随轨迹深度退化。一个自然的后续问题是：在失败的 OPD 配置中，奖励信号是否从根本上就缺乏信息，还是失败的根源在别处。

**设置。** 我们回到 §4.1 的受控对比，以 R1-Distill-1.5B 为学生，两个教师为 JustRL-1.5B（成功的 OPD）和 R1-Distill-7B（失败的 OPD）。对每条学生 rollout $`y`$，我们在采样词元 OPD 下计算序列平均奖励 $`\bar{r}(y) = \frac{1}{T}\sum_{t=1}^{T} [\log \pi_{T}(y_t \mid x, y_{<t}) - \log \pi_\theta(y_t \mid x, y_{<t})]`$，并比较正确与错误 rollout 之间 $`\bar{r}(y)`$ 的分布。

**两种设定下全局奖励结构都得到保留。** 图 14 显示，对两个教师而言，正确的 rollout 始终比错误的 rollout 获得更高的序列平均奖励，AUROC 相当（JustRL-1.5B 为 0.73，R1-Distill-7B 为 0.75）。失败的 7B 教师并没有产生更弱的全局信号，它与 rollout 正确性的相关程度不相上下。

**关于局部优化几何的一个假设。** 如果两种情形下奖励在全局上都有信息，为什么 OPD 会在 7B 教师下失败？§4.1 的训练动力学给出了一条线索。如图 6 所示，当 R1-Distill-7B 充当教师时，重叠词元优势在训练后期的幅度比 JustRL 设定更大，但梯度范数却持续更小（见附录 B.2）。一个可能的解释是：7B 教师的逐词元优势虽然单个很大，却在每个序列内部各位置之间各向异性。当这些异质信号被聚合成一次梯度更新时，它们部分相互抵消，于是尽管逐词元奖励很大，有效梯度却很小。相比之下，JustRL-1.5B 与学生共享相容的思维模式，可能把它的优势集中在一个更连贯的词元子集上。由此产生的梯度虽然由更小的逐词元信号组成，却指向一个一致的方向，反向 KL 能通过其寻模行为将其放大。

我们尚未直接验证这个各向异性假设，验证它需要分析逐词元梯度的方向结构，我们把这留给未来工作。尽管如此，高逐词元优势与低梯度范数的共现是有启发性的，它指向一个重要区别：全局有信息的奖励并不保证局部可利用。理解 OPD 奖励曲面的几何，以及开发能利用各向异性奖励结构的目标函数，仍是一个开放问题。

#### 6.3 采样词元奖励已经足够

关于 OPD 奖励的一个自然问题是：每个位置需要多少个词元才能计算出有用的梯度？Top-$`k`$ OPD 在每个位置把奖励聚合到 $`k`$ 个最高概率的词元上，人们可能会预期更大的支撑集总是带来更好或更稳定的学习。我们通过改变 $`k`$ 并与更简单的采样词元 OPD（在每个位置只使用从学生分布中抽取的一个词元）比较来研究这一点。

![图 15](./img/Rethinking-On-Policy-Distillation-fig15.png)

*图 15：Top-$`k`$ OPD 中支撑集大小 $`k`$ 的效果。所有数值都以 avg@16 报告。*

**设置。** 我们以 R1-Distill-1.5B 为学生、JustRL-1.5B 为教师，比较 $`k\in\{1, 4, 16, 64\}`$ 的 Top-$`k`$ OPD 与采样词元 OPD，其他所有超参数保持固定。

![图 16](./img/Rethinking-On-Policy-Distillation-fig16.png)

*图 16：Top-$`k`$ OPD 在不同支撑集大小 $`k`$ 下的训练动力学。*

**结果。** 图 15 显示，采样词元 OPD 在三个基准的平均上取得了与各 Top-$`k`$ 设定相当的性能。唯一明显更差的配置是 Top-1，它始终表现不佳。把 $`k`$ 扩大到 4 以上带来的额外收益可忽略，却导致更大的计算开销。图 16 显示了训练动力学，揭示出差异产生在何处。Top-1 表现出不稳定的重叠增长，伴随熵和梯度范数的剧烈尖峰。Top-4 稳定得多，但仍有一个后期的下陷。Top-16 和 Top-64 自始至终保持平滑。

总体而言，这些结果表明，只要避开退化的 Top-1 设定，支撑集大小对 OPD 可能并非一个关键的设计选择。采样词元 OPD 尽管每个位置只用一个词元却效果良好，原因在于它在每一步按学生自己的分布比例抽取一个不同的词元，从而在整个训练中对高概率区域提供了无偏覆盖。相比之下，Top-1 总是选择 argmax 词元，从而把奖励集中到单一模式上。策略的微小变化就可能改变占据排名第一的词元，产生一个无法在训练中被平均掉的不稳定奖励信号。因此 Top-1 的失败不在于用的词元太少，而在于使用了一个有偏的、集中于单一模式的选择规则。

### 7 相关工作

**知识蒸馏。** 知识蒸馏（KD）[Hinton et al., 2015] 通过在教师的软输出分布上训练一个学生网络，把知识从一个大模型传递给一个较小的模型。对于自回归序列模型，[Kim and Rush, 2016] 把它扩展到序列级蒸馏，在教师生成的输出上训练学生，确立了占主导地位的 off-policy 蒸馏基线 [Sanh et al., 2019, Jiao et al., 2020, Wang et al., 2020]。与此并行，监督微调（SFT）被直接用于提升各种下游任务的性能 [Chung et al., 2024, Sanh et al., 2021, Wei et al., 2021]。所有 off-policy 方法共有的一个根本局限是训练-推理分布失配。学生在教师生成的或参考序列上被优化，但在推理时必须从它自己的分布中生成，这是曝光偏差 [Bengio et al., 2015] 的一个实例，会在长序列生成中累积误差。这种失配促使人们把蒸馏转移到学生自己的 on-policy 分布上，这正是 on-policy 蒸馏的核心思想。

**on-policy 蒸馏。** MiniLLM [Gu et al., 2023] 首次在反向 KL 目标下、通过策略梯度优化，为 LLM 形式化了 on-policy 蒸馏（OPD），论证反向 KL 的寻模行为能防止学生把概率质量铺洒到教师认为不太可能的区域。GKD [Agarwal et al., 2024] 引入了一个统一框架，在 on-policy 与 off-policy 数据之间、跨多种散度进行插值，相比其他 KD 基线取得了一致的增益。[Yang et al., 2026b] 随后在理论上把 OPD 形式化为密集 KL 约束 RL 的一个特例，表明教师的逐词元对数比构成一个隐式奖励，并且把这个奖励放大到超出其标准权重可以把学生推过教师的性能边界。此后 OPD 被 industry 的后训练流水线采用 [Yang et al., 2025, Lu and Lab, 2025, Zeng et al., 2026, Xiao et al., 2026, Ko et al., 2026, Jin et al., 2026, Jang et al., 2026, Fu et al., 2026, Yang et al., 2026b]，并扩展到可规模化的自蒸馏 [Hübotter et al., 2026, Zhao et al., 2026b, He et al., 2026, Shenfeld et al., 2026, Ye et al., 2026b, Sang et al., 2026, Kim et al., 2026, Ye et al., 2026a, Yang et al., 2026a, Li et al., 2026, Zhao et al., 2026a, Ding, 2026]，其中单个模型以诸如标准答案或执行反馈之类的特权信息为条件，充当自己的教师。尽管这一研究体量不断增长，现有研究聚焦于展示 OPD 的前景（如密集奖励和缓解曝光偏差），跨越各种目标、任务和师生配对，却没有系统地分析 OPD 何时或为何失败。

**容量差距与可蒸馏性。** 知识蒸馏中一个反复出现的观察是，巨大的师生容量差距会削弱甚至反转蒸馏的收益。[Cho and Hariharan, 2019] 证明，当教师的能力强出许多时，蒸馏会损害学生性能，而 [Mirzadeh et al., 2020] 提出用一个中等大小的教师助理来弥合差距。[Busbridge et al., 2025] 通过蒸馏缩放定律给出了定量处理，表明学生损失作为教师质量、学生规模和数据量的函数遵循幂律，并识别出一个 U 形的容量区间，在该区间中教师过强会降低蒸馏效率。对于 LLM 推理，[Li et al., 2025] 记录了一个“可学习性差距”，表明在来自强推理教师的长思维链轨迹上训练小模型，始终不如更简单的方法，说明教师输出的推理复杂度必须与学生容量相匹配。这些发现呼吁对蒸馏的普适性保持谨慎。然而，现有分析大多集中在 off-policy 知识蒸馏上。特别是，OPD 中的容量差距和可蒸馏性问题仍未被充分探索。

### 8 结论与未来工作

本工作对 OPD 进行了系统分析，把它的成功分解为两个支配条件：思维模式一致性，以及存在超出学生在训练期间所见的、真正新的知识。当这些条件不满足时，off-policy 冷启动和与教师对齐的提示词选择提供了有效的补救。我们还揭示了一个由长轨迹上奖励退化所施加的实际上限。

**未来工作** 在我们发现的基础上，我们指出几个未来的研究方向：

- **超越数学推理：** 本工作的全部实验都在数学基准上进行。同样的条件和词元级机制是否支配着其他领域（如代码和开放式设定）中的 OPD，仍是一个重要的开放问题。
- **预训练的影响：** “新知识”这一条件隐含地依赖于预训练语料的差异，但隔离这一因素颇具挑战。当前的研究主要依赖跨家族蒸馏（例如 Qwen → LLaMA），这会把数据差异与分词器失配和架构差异混在一起，而受控的预训练消融又昂贵到难以承受。因此，测量预训练数据对 OPD 的影响仍是一个开放问题。
- **自蒸馏动力学：** 近期工作越来越多地采用自蒸馏，即单个模型在获得特权信息的条件下充当自己的教师。把这些洞见扩展到自蒸馏范式——那里思维模式一致性有保证，但知识的新颖性来自特权访问而非一个独立的教师——是一个自然的下一步。
- **长程与智能体设定：** §6 揭示的轨迹长度上限促使人们考虑混合方法：在短片段上结合密集的词元级监督，在更长的时程上结合稀疏的结果级奖励，以及在训练中逐步延长被监督时程的课程策略。

### 参考文献

- Rishabh Agarwal, Nino Vieillard, Yongchao Zhou, Piotr Stanczyk, Sabela Ramos Garea, Matthieu Geist, and Olivier Bachem. On-policy distillation of language models: Learning from self-generated mistakes. In *The Twelfth International Conference on Learning Representations*, 2024.
- Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola Jovanović, and Martin Vechev. Matharena: Evaluating llms on uncontaminated math competitions. *arXiv preprint arXiv:2505.23281*, 2025.
- Samy Bengio, Oriol Vinyals, Navdeep Jaitly, and Noam Shazeer. Scheduled sampling for sequence prediction with recurrent neural networks. *Advances in Neural Information Processing Systems*, 28, 2015.
- Dan Busbridge, Amitis Shidani, Floris Weers, Jason Ramapuram, Etai Littwin, and Russ Webb. Distillation scaling laws. *arXiv preprint arXiv:2502.08606*, 2025.
- Jang Hyun Cho and Bharath Hariharan. On the efficacy of knowledge distillation. In *Proceedings of the IEEE/CVF International Conference on Computer Vision*, pages 4794--4802, 2019.
- Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, et al. Scaling instruction-finetuned language models. *Journal of Machine Learning Research*, 25(70):1--53, 2024. URL <http://jmlr.org/papers/v25/23-0870.html>.
- Ken Ding. Hdpo: Hybrid distillation policy optimization via privileged self-distillation. *arXiv preprint arXiv:2603.23871*, 2026.
- Yuqian Fu, Haohuan Huang, Kaiwen Jiang, Yuanheng Zhu, and Dongbin Zhao. Revisiting on-policy distillation: Empirical failure modes and simple fixes. *arXiv preprint arXiv:2603.25562*, 2026.
- Yuxian Gu, Li Dong, Furu Wei, and Minlie Huang. Minillm: Knowledge distillation of large language models. *arXiv preprint arXiv:2306.08543*, 2023.
- Etash Guha, Ryan Marten, Sedrick Keh, Negin Raoof, Georgios Smyrnis, Hritik Bansal, Marianna Nezhurina, Jean Mercat, Trung Vu, Zayne Sprague, et al. Openthoughts: Data recipes for reasoning models. *arXiv preprint arXiv:2506.04178*, 2025.
- Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. *Nature*, 645(8081):633--638, 2025.
- Bingxiang He, Zekai Qu, Zeyuan Liu, Yinghao Chen, Yuxin Zuo, Cheng Qian, Kaiyan Zhang, Weize Chen, Chaojun Xiao, Ganqu Cui, et al. Justrl: Scaling a 1.5b llm with a simple rl recipe. *arXiv preprint arXiv:2512.16649*, 2025a.
- Bingxiang He, Yuxin Zuo, Zeyuan Liu, Shangziqi Zhao, Zixuan Fu, Junlin Yang, Cheng Qian, Kaiyan Zhang, Yuchen Fan, Ganqu Cui, et al. How far can unsupervised rlvr scale llm training? *arXiv preprint arXiv:2603.08660*, 2026.
- Jujie He, Jiacai Liu, Chris Yuhao Liu, Rui Yan, Chaojie Wang, Peng Cheng, Xiaoyu Zhang, Fuxiang Zhang, Jiacheng Xu, Wei Shen, et al. Skywork open reasoner 1 technical report. *arXiv preprint arXiv:2505.22312*, 2025b.
- Zhiwei He, Tian Liang, Jiahao Xu, Qiuzhi Liu, Xingyu Chen, Yue Wang, Linfeng Song, Dian Yu, Zhenwen Liang, Wenxuan Wang, et al. Deepmath-103k: A large-scale, challenging, decontaminated, and verifiable mathematical dataset for advancing reasoning. *arXiv preprint arXiv:2504.11456*, 2025c.
- Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network. *arXiv preprint arXiv:1503.02531*, 2015.
- Jonas Hübotter, Frederike Lübeck, Lejs Behric, Anton Baumann, Marco Bagatella, Daniel Marta, Ido Hakimi, Idan Shenfeld, Thomas Kleine Buening, Carlos Guestrin, et al. Reinforcement learning via self-distillation. *arXiv preprint arXiv:2601.20802*, 2026.
- Ijun Jang, Jewon Yeom, Juan Yeo, Hyunggu Lim, and Taesup Kim. Stable on-policy distillation through adaptive target reformulation. *arXiv preprint arXiv:2601.07155*, 2026.
- Xiaoqi Jiao, Yichun Yin, Lifeng Shang, Xin Jiang, Xiao Chen, Linlin Li, Fang Wang, and Qun Liu. Tinybert: Distilling bert for natural language understanding. In *Findings of the Association for Computational Linguistics: EMNLP 2020*, pages 4163--4174, 2020.
- Woogyeol Jin, Taywon Min, Yongjin Yang, Swanand Ravindra Kadhe, Yi Zhou, Dennis Wei, Nathalie Baracaldo, and Kimin Lee. Entropy-aware on-policy distillation of language models. *arXiv preprint arXiv:2603.07079*, 2026.
- Jeonghye Kim, Xufang Luo, Minbeom Kim, Sangmook Lee, Dohyung Kim, Jiwon Jeon, Dongsheng Li, and Yuqing Yang. Why does self-distillation (sometimes) degrade the reasoning capability of llms? *arXiv preprint arXiv:2603.24472*, 2026.
- Yoon Kim and Alexander M Rush. Sequence-level knowledge distillation. In *Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing*, pages 1317--1327, 2016.
- Jongwoo Ko, Sara Abdali, Young Jin Kim, Tianyi Chen, and Pashmina Cameron. Scaling reasoning efficiently via relaxed on-policy distillation. *arXiv preprint arXiv:2603.11137*, 2026.
- Gengsheng Li, Tianyu Yang, Junfeng Fang, Mingyang Song, Mao Zheng, Haiyun Guo, Dan Zhang, Jinqiao Wang, and Tat-Seng Chua. Unifying group-relative and self-distillation policy optimization via sample routing. *arXiv preprint arXiv:2604.02288*, 2026.
- Jia Li, Edward Beeching, Lewis Tunstall, Ben Lipkin, Roman Soletskyi, Shengyi Huang, Kashif Rasul, Longhui Yu, Albert Q Jiang, Ziju Shen, et al. Numinamath: The largest public dataset in ai4maths with 860k pairs of competition math problems and solutions. *Hugging Face repository*, 13:9, 2024.
- Yuetai Li, Xiang Yue, Zhangchen Xu, Fengqing Jiang, Luyao Niu, Bill Yuchen Lin, Bhaskar Ramasubramanian, and Radha Poovendran. Small models struggle to learn from strong reasoners. In *Findings of the Association for Computational Linguistics: ACL 2025*, pages 25366--25394, 2025.
- Kevin Lu and Thinking Machines Lab. On-policy distillation. *Thinking Machines Lab: Connectionism*, 2025. doi: 10.64434/tml.20251026. <https://thinkingmachines.ai/blog/on-policy-distillation>.
- Seyed Iman Mirzadeh, Mehrdad Farajtabar, Ang Li, Nir Levine, Akihiro Matsukawa, and Hassan Ghasemzadeh. Improved knowledge distillation via teacher assistant. In *Proceedings of the AAAI Conference on Artificial Intelligence*, volume 34, pages 5191--5198, 2020.
- Nils Reimers and Iryna Gurevych. Sentence-bert: Sentence embeddings using siamese bert-networks. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing*, 2019. URL <http://arxiv.org/abs/1908.10084>.
- Hejian Sang, Yuanda Xu, Zhengze Zhou, Ran He, Zhipeng Wang, and Jiachen Sun. Crisp: Compressed reasoning via iterative self-policy distillation, 2026. URL <https://arxiv.org/abs/2603.05433>.
- Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter. *arXiv preprint arXiv:1910.01108*, 2019.
- Victor Sanh, Albert Webson, Colin Raffel, Stephen Bach, Lintang Sutawika, Zaid Alyafeai, Antoine Chaffin, Arnaud Stiegler, Arun Raja, Manan Dey, et al. Multitask prompted training enables zero-shot task generalization. In *International Conference on Learning Representations*, 2021.
- Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. *arXiv preprint arXiv:2402.03300*, 2024.
- Idan Shenfeld, Mehul Damani, Jonas Hübotter, and Pulkit Agrawal. Self-distillation enables continual learning. *arXiv preprint arXiv:2601.19897*, 2026.
- Wenhui Wang, Furu Wei, Li Dong, Hangbo Bao, Nan Yang, and Ming Zhou. Minilm: Deep self-attention distillation for task-agnostic compression of pre-trained transformers. *Advances in Neural Information Processing Systems*, 33:5776--5788, 2020.
- Jason Wei, Maarten Bosma, Vincent Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M Dai, and Quoc V Le. Finetuned language models are zero-shot learners. In *International Conference on Learning Representations*, 2021.
- Bangjun Xiao, Bingquan Xia, Bo Yang, Bofei Gao, Bowen Shen, Chen Zhang, Chenhong He, Chiheng Lou, Fuli Luo, Gang Wang, et al. Mimo-v2-flash technical report. *arXiv preprint arXiv:2601.02780*, 2026.
- An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. *arXiv preprint arXiv:2505.09388*, 2025.
- Chenxu Yang, Chuanyu Qin, Qingyi Si, Minghui Chen, Naibin Gu, Dingyu Yao, Zheng Lin, Weiping Wang, Jiaqi Wang, and Nan Duan. Self-distilled rlvr. *arXiv preprint arXiv:2604.03128*, 2026a.
- Wenkai Yang, Weijie Liu, Ruobing Xie, Kai Yang, Saiyong Yang, and Yankai Lin. Learning beyond teacher: Generalized on-policy distillation with reward extrapolation. *arXiv preprint arXiv:2602.12125*, 2026b.
- Tianzhu Ye, Li Dong, Qingxiu Dong, Xun Wu, Shaohan Huang, and Furu Wei. Online experiential learning for language models. *arXiv preprint arXiv:2603.16856*, 2026a.
- Tianzhu Ye, Li Dong, Xun Wu, Shaohan Huang, and Furu Wei. On-policy context distillation for language models. *arXiv preprint arXiv:2602.12275*, 2026b.
- Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan, Gaohong Liu, Lingjun Liu, et al. Dapo: An open-source llm reinforcement learning system at scale. *arXiv preprint arXiv:2503.14476*, 2025.
- Aohan Zeng, Xin Lv, Zhenyu Hou, Zhengxiao Du, Qinkai Zheng, Bin Chen, Da Yin, Chendi Ge, Chengxing Xie, Cunxiang Wang, et al. Glm-5: from vibe coding to agentic engineering. *arXiv preprint arXiv:2602.15763*, 2026.
- Guoliang Zhao, Ruobing Xie, An Wang, Shuaipeng Li, Huaibing Xie, and Xingwu Sun. Self-distillation for multi-token prediction, 2026a. URL <https://arxiv.org/abs/2603.23911>.
- Siyan Zhao, Zhihui Xie, Mengchen Liu, Jing Huang, Guan Pang, Feiyu Chen, and Aditya Grover. Self-distilled reasoner: On-policy self-distillation for large language models. *arXiv preprint arXiv:2601.18734*, 2026b.
- Yaowei Zheng, Richong Zhang, Junhao Zhang, Yanhan Ye, Zheyan Luo, Zhangchi Feng, and Yongqiang Ma. Llamafactory: Unified efficient fine-tuning of 100+ language models. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations)*, Bangkok, Thailand, 2024. URL <http://arxiv.org/abs/2403.13372>.

### 附录 A 第 3 节相关细节

#### A.1 GRPO 训练细节

**基座模型。** 我们从 Qwen3-4B-Base 初始化 GRPO 训练。

**训练数据集。** 我们使用处理后的 DAPO-Math-17K 数据集做 GRPO 训练。具体而言，每道题都用以下指令增强：

*GRPO 数据集模板。*

```text
{Question} 请一步一步推理，并把你的最终答案放在 \boxed{} 中。
```

**训练与评估设置。** 我们用 GRPO 训练教师模型。训练期间，我们对每条提示词采样 $`n=8`$ 个回答。最大提示词长度和最大响应长度分别设为 1,024 和 7,168 个词元。训练在 8 张 A800 80G GPU 上进行一个 epoch，学习率为 $`1\times10^{-6}`$。我们把学生采样温度和教师温度都设为 1.0，使用 1.0 的重复惩罚，禁用 KL 正则化，并采用 `token-mean` 损失聚合。主要超参数汇总于表 1。

*表 1：Qwen3-4B-Base-GRPO 的 GRPO 训练超参数。*

| 超参数 | 取值 |
| --- | --- |
| Base model | Qwen3-4B-Base |
| RL algorithm | GRPO |
| Training epochs | 1 |
| Train batch size | 64 |
| Micro batch size | 64 |
| Rollout $`n`$ | 8 |
| Maximum prompt length | 1,024 |
| Maximum response length | 7,168 |
| Validation max response length | 31,744 |
| Learning rate | $`1 \times 10^{-6}`$ |
| Temperature | 1.0 |
| Top-$`p`$ | 1.0 |
| KL regularization | 0.0 |
| Loss aggregation | `token-mean` |
| KL Coefficient | 0.0 |

#### A.2 实验设置

除非另有说明，所有实验都使用表 2 中列出的默认 OPD 超参数。

*表 2：OPD 的默认超参数。*

| 项目 | 取值 |
| --- | --- |
| Training temperature | 1.0 |
| Global batch size | 64 |
| Mini batch size | 64 |
| Rollout number | 4 |
| LogProb top-$`K`$ | 16 |
| Top-$`K`$ strategy | Student Top-$`K`$ |
| Top-$`p`$ | 1.0 |
| Max prompt length | 1024 |
| Max response length | 7168 |
| Learning rate | 1e-6 |
| Epoch | 1 |
| KL Coefficient | 0.0 |

#### A.3 思维模式相容性的逐基准分解

为进一步拆解图 2 中的平均结果，图 17 给出了逐基准的分解。从 Qwen3-4B-Base-GRPO 蒸馏的优势在各数据集上大体一致，而不是由单一基准驱动。这一差距在 AMC 2023 和 AIME 2024 上更明显，在 AIME 2025 上更小但总体仍然存在。这一逐基准视角支持了如下解读：更好的早期思维模式相容性带来更好的下游蒸馏性能，而早期失配造成的损失在训练后期无法完全弥补。

![图 17](./img/Rethinking-On-Policy-Distillation-fig17.png)

*图 17：图 2 所示平均验证准确率的逐基准分解。我们分别报告 AIME 2024、AIME 2025 和 AMC 2023 上的结果。从 Qwen3-4B-Base-GRPO 蒸馏在三个基准上始终匹配或优于从 Qwen3-4B（非思考模式）蒸馏。*

### 附录 B 第 4 节相关细节

#### B.1 词元重叠质量的补充分析

为量化每个模型赋予重叠 top-$`k`$ 区域多少概率质量，我们定义：

```math
\mathcal{M}_{\text{overlap-mass}}^{(p)} = \mathbb{E}_{t}\left[ \sum_{v \in S_t^{(p)} \cap S_t^{(q)}} p_t(v) \right] \qquad (9)
```

以及

```math
\mathcal{M}_{\text{overlap-mass}}^{(q)} = \mathbb{E}_{t}\left[ \sum_{v \in S_t^{(p)} \cap S_t^{(q)}} q_t(v) \right] \qquad (10)
```

它们分别衡量学生和教师赋予其 top-$`k`$ 集合中共享词元的总概率质量所占的比例。在我们的实验中，重叠词元在整个训练过程中对两个模型都占据 $`97\%`$--$`99\%`$ 的总概率质量，如图 18 所示。

![图 18](./img/Rethinking-On-Policy-Distillation-fig18.png)

*图 18：训练期间赋予重叠词元的概率质量。对学生和教师分布而言，重叠词元始终占据约 97%--99% 的总概率质量，表明重叠不仅在集合层面增加，也在概率分布上占主导。*

#### B.2 辅助优化动力学

为补充 §4.1 的分析，我们为同一组对比设定报告若干额外的优化诊断量。在本附录中，我们固定学生为 R1-Distill-1.5B，并在相同的 Student Top-$`k`$ OPD 训练配方下比较两个教师：JustRL-1.5B（成功的运行）和 R1-Distill-7B（在其他条件匹配时失败的运行）。这些诊断量并非作为主要证据，而是提供一个关于成功与失败 OPD 之间优化信号差异的互补视角。

![图 19](./img/Rethinking-On-Policy-Distillation-fig19.png)

*图 19：§4.1 对比 OPD 设定的辅助优化诊断量，以 R1-Distill-1.5B 为学生，比较 JustRL-1.5B 与 R1-Distill-7B 作教师。**左：**训练过程中按批平均的 OPD 训练损失（*PG Loss*）。**中：**训练过程中的梯度范数。**右：**在绝对优势最大的词元上测得的概率差 $`p_t(v)-q_t(v)`$。成功的运行表现出优化损失的大幅下降、持续的梯度幅度，以及极端词元概率失配的稳步减小。相比之下，失败的运行一开始就带有并维持着弱得多的梯度，其极端词元概率差异在整个训练中始终明显更大。*

**诊断量。** 我们监控三个额外的量。第一个是按批平均的 OPD 训练损失，在图 19 中记作 *PG Loss*。第二个是梯度范数，衡量到达学生的更新信号的整体幅度。第三个是绝对优势最大的词元上的概率差 $`p_t(v)-q_t(v)`$，它追踪学生能否在携带最强优化信号的词元上减小它与教师最显著的局部分歧。这些指标合在一起有助于区分成功与失败的 OPD：在前者中，学生收到可用的信号并逐步减小失配；在后者中，信号太弱或对齐太差，不足以驱动实质性改进。

**结果。** 图 19 中的趋势与 §4.1 的主要结论一致。第一，用 JustRL-1.5B 的成功运行在优化过程中表现出训练损失的明显下降。从一个大得多的初始失配出发，损失在训练的大部分时间里稳步下降，之后才在一个低值处趋平。相比之下，用 R1-Distill-7B 的失败运行从一个小得多的损失开始，此后只有适度变化。这一模式说明失败运行中更小的损失并不意味着更好的优化，而是反映了一个从一开始就由教师诱导的弱训练信号，它始终太小，不足以驱动实质性的策略改进。

第二，梯度范数在两次运行之间表现出更加清晰的分离。在成功的运行中，梯度范数初始很大，并在训练的很长一段时间内保持可观，表明学生持续收到有意义的纠正信号。在失败的运行中，梯度范数始终小得多，随时间只有有限的变化。因此，即便在相同的算法和训练预算下进行优化，用 R1-Distill-7B 训练的学生所经历的更新信号也弱得多。这一观察与如下发现一致：失败与高概率词元上的糟糕对齐相关联——当学生没有有意义地进入教师支持的区域时，由此产生的梯度就始终很弱。

第三，右图显示成功的运行稳步减小了绝对优势最大的词元上的概率差异，而失败的运行在整个训练中始终维持着明显更大的差距。换言之，当 OPD 成功时，学生逐步纠正了在教师诱导的优势信号下最重要的局部错误；当 OPD 失败时，这些高优势分歧持续存在而未被解决。这再次与如下解读一致：OPD 的决定性信号在于一小组高概率、高优势的词元，而失败发生在学生无法有效利用该信号之时。

综合来看，这些辅助动力学强化了 §4.1 中发展出的解读。成功的 OPD 的特征不仅是高概率词元上重叠的增加，还有一个学生收到足够幅度梯度、从而减小最重要局部分布失配的训练状态。相比之下，失败的 OPD 伴随着弱梯度、有限的损失下降，以及在优势信号最强的词元上持续的分歧。尽管这些诊断量是支持性而非核心的，它们提供了一个优化层面的视角，与“OPD 有用的学习信号集中在学生访问状态上的高概率词元、而当该信号太弱或太失配以至无法驱动有效更新时训练就退化”这一结论完全一致。

#### B.3 高概率词元对齐的跨模型验证

我们进一步测试 §4.1 中的现象是否能推广到另一个模型对。这里我们把学生模型固定为 R1-Distill-7B，选择 Skywork-OR1-Math-7B 和 DeepSeek-R1-Distill-Qwen-14B（R1-Distill-14B）作为教师，使用与 §4.1 相同的训练和评估设置。

![图 20](./img/Rethinking-On-Policy-Distillation-fig20.png)

*图 20：固定学生（R1-Distill-7B）与两个教师的跨模型验证。**上：**AIME 2024、AIME 2025 和 AMC 2023 上的 avg@16 准确率。**下：**训练过程中的重叠率、重叠词元优势和绝对熵差。成功的运行再次伴随着高概率词元对齐的增加，而停滞的运行则没有。*

**结果。** 图 20 显示出与图 6 相同的模式。以 Skywork-OR1-Math-7B 为教师时，蒸馏改善了学生性能，并伴随着稳步增加的重叠率、趋近于零的重叠词元优势和小的熵差。相反，以 R1-Distill-14B 为教师时，训练几乎没有改善，对齐指标始终糟糕或不稳定。这为“成功的 OPD 始终与学生访问状态上高概率词元对齐的涌现同时出现”提供了额外证据。

### 附录 C 第 5 节相关细节

#### C.1 冷启动蒸馏细节

**离线教师 rollout。** 为构建冷启动 SFT 数据，我们从 OpenThoughts3-1.2M [Guha et al., 2025] 的数学子集采样 200K 条数学提示词，并用 Qwen3-4B（非思考模式）为每条提示词生成一个离线回答。对每条提示词，我们使用以下模板：

*教师 rollout 模板。*

```text
{Question} 请一步一步推理，并把你的最终答案放在 \boxed{} 中。
```

我们以温度 $`0.7`$、top-$`p=0.95`$、top-$`k=-1`$ 和最大生成长度 12,288 个词元进行解码。生成之后，我们过滤掉不完整的回答（例如未正常结束的截断输出）和退化的重复回答。剩余的提示词-回答对被用作训练学生的监督蒸馏语料。

**学生 SFT。** 从 Qwen3-1.7B-Base 出发，我们使用 LLaMA-Factory 框架 [Zheng et al., 2024] 在过滤后的 200K 条教师生成样本上做全参数 SFT，得到 Qwen3-1.7B-SFT。详细超参数汇总于表 3。

*表 3：从 Qwen3-4B（非思考模式）到 Qwen3-1.7B-Base 的冷启动蒸馏的 SFT 超参数。*

| 超参数 | 取值 |
| --- | --- |
| Student model | Qwen3-1.7B-Base |
| Training objective | Full-parameter SFT |
| Template | `qwen3` |
| Training epochs | 1 |
| Sequence length | 14,336 |
| Per-device batch size | 8 |
| Gradient accumulation steps | 1 |
| Learning rate | $`1 \times 10^{-5}`$ |
| LR scheduler | Cosine |
| Warmup ratio | 0.05 |
| Precision | BF16 |

#### C.2 重叠质量的补充分析

为更好地理解为什么基座初始化的学生有时能表现出相当甚至略好的重叠词元优势，却仍整体表现不佳，我们进一步从学生和教师两侧考察重叠集合覆盖的概率质量。如图 21 所示，SFT 初始化的学生在整个训练过程中把学生重叠质量和教师重叠质量都维持在始终很高的水平。这表明重叠词元覆盖了学生和教师分布的大部分高概率区域，意味着从 OPD 一开始就有一个强而稳定的对齐。相比之下，基座初始化的学生表现出明显更低且更不稳定的重叠质量，尤其是在训练早期。

这一分析有助于解释为什么单看重叠词元优势有时会产生误导。由于它只在重叠词元上取平均，即便重叠集合本身漏掉了大量高概率的教师词元，它看上去也可能相对有利。重叠质量补充了这一视角，揭示共享的支撑集是否真的覆盖了两个分布最重要的部分。从这个角度看，SFT 冷启动带来了学生与教师之间实质上更好、更稳定的匹配。

![图 21](./img/Rethinking-On-Policy-Distillation-fig21.png)

*图 21：SFT 初始化和基座初始化学生在训练期间的学生重叠质量与教师重叠质量。*

#### C.3 DeepMath 子集的去重细节

对于跨规模设定，我们构建一个对 DAPO-Math-17K 去重后的 DeepMath 子集，以便比较与教师 RL 后训练数据对齐的提示词和仅仅同领域的提示词。

我们的去重分两个阶段进行：精确匹配去重和语义去重。

**题目抽取。** 对 DAPO-Math-17K 和 DeepMath，我们抽取题目内容并移除提示词中的指令后缀，使去重仅基于题目文本进行。

**阶段 1：精确匹配去重。** 我们把所有抽取出的 DAPO-Math-17K 题目收入一个集合，并移除任何其抽取题目与某道 DAPO 题目精确匹配的 DeepMath 样本。

**阶段 2：语义去重。** 为进一步移除近似重复的提示词，我们使用句向量模型 all-mpnet-base-v2 [Reimers and Gurevych, 2019] 对 DAPO-Math-17K 和 DeepMath 的题目编码。我们对嵌入做 L2 归一化，并在 DAPO 嵌入上构建一个 FAISS 内积索引，使内积对应余弦相似度。对每道 DeepMath 题目，我们在 DAPO-Math-17K 中检索其 top-1 最近邻。如果到最近 DAPO 题目的余弦相似度至少为 $`0.6`$，我们就把该 DeepMath 样本标记为语义重复并移除。

**最终保留的子集。** 我们移除任何被精确匹配或语义去重标记的 DeepMath 样本。得到的子集是同领域的，但对 DAPO-Math-17K 去重，从而能在与教师后训练数据重叠的提示词和仅仅同领域的提示词之间进行受控比较。

![图 22](./img/Rethinking-On-Policy-Distillation-fig22.png)

*图 22：图 9 所示平均验证准确率的逐基准分解。使用与教师对齐的模板在三个基准上始终匹配或优于原始 DAPO 模板。*

#### C.4 提示词模板对齐的逐基准分解

为进一步拆解图 9 中的平均结果，图 22 给出了逐基准的分解。与教师对齐的模板在各数据集上带来大体一致的提升，在两个 AIME 集上增益更大，在 AMC 2023 上效果更小但仍为正。它还让学生回收了更大比例的教师性能，从约 80% 升到约 85%。结合 §5.2 中的重叠率结果，这表明提示词模板对齐通过让学生生成的状态与教师更兼容来改善 OPD。

### 附录 D 第 6 节相关细节

#### D.1 按输出位置划分的教师熵

为补充 §6.1 中的学生熵分析，我们还把教师熵作为输出位置的函数，在 15$`K`$ 最大响应长度设定下跨训练步可视化（见图 23）。与学生类似，教师熵首先在靠后的解码位置增加，然后随训练逐步向更早的词元传播。

![图 23](./img/Rethinking-On-Policy-Distillation-fig23.png)

*图 23：在最大响应长度 15K 的 OPD 训练中，跨解码位置的平均教师熵，测量自第 180 步到第 250 步的学生生成轨迹。升高的熵首先出现在后缀，并随训练逐步向更早的输出位置传播。*
