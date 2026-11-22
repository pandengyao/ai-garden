# 训练数据中的思维链合成：方法、证据与开放问题 · 第 4 节

中文 | [English](./CoT-Data-Synthesis-Literature-Review-Ch04_en.md)

- **调研日期**: 2026-10-22（证据截止：arXiv 首版日期不晚于 2026-10-22）
- **导航**: [主页面](./CoT-Data-Synthesis-Literature-Review.md)（摘要、第 1–3 节、第 11–13 节与附录） · 上一节：[第 3 节（主页面）](./CoT-Data-Synthesis-Literature-Review.md) · 下一节：[第 5 节](./CoT-Data-Synthesis-Literature-Review-Ch05.md)
- **依据**: 句末的上标数字是引用，对应文末参考来源中的精读文献；每条引用都有从该文献全文逐字摘录、并经脚本与全文核对的原文。标有（本文判断）、（本文推断）或（本文统计）的内容，是本文的综合分析或统计，不是来源原话。

## 4 发展脉络：从理由蒸馏到长思维链

2025 年长思维链（long CoT）蒸馏兴起之前，用模型生成的推理轨迹训练模型的基本做法已在 2022 年 10 月至 2024 年 7 月间成形（本文判断）。本节按首版时间梳理这一时期的 22 篇代表工作（本文统计），关注三个设计变量：轨迹由谁生成，靠什么判据保留，答错的轨迹丢弃还是利用（本文判断）。本节为后续按流水线阶段展开的各节提供时间坐标（本文判断）。STaR、Orca 等奠基工作由后续各节讨论（本文判断）。表 4-1 按首版时间列出各工作的数据构造要素（本文统计）。

表 4-1 推理轨迹数据构造的代表工作（按 arXiv 首版排序；“未描述”指原文未报告该步骤）

| 文献 | 首版 | 生成方式 | 保留判据 | 数据规模 | 教师→学生 | 代表结果（条件） |
| --- | --- | --- | --- | --- | --- | --- |
| Li 等[^96] | 2022-10 | 7 个人工示例，贪心解码；RP 以金标答案为条件 | COTE：教师答对才保留；CROP 以 RP 补缺 | 每例 1 条 | GPT-3（175B）→T5 | CSQA：T5 多任务（3B）82.47，GPT-3 直接提示 80.59 |
| LMSI[^100] | 2022-10 | 每题 32 条路径（T=0.7），4 种格式增广 | 多数投票，不用标签 | 至多 128 倍训练集 | PaLM-540B 自训练；数据再用于 8B/62B | GSM8K 自洽解码 74.4%→82.1%；PaLM-8B 5.0→33.4 |
| Socratic CoT[^94] | 2022-12 | 生成 CoT，或子问题与解答 | 末步答案正确，否则重采（至多 3 次） | 每题 1 条 | GPT-3 175B→GPT-2（问题分解器＋子问题求解器） | GSM8K，GPT-2 Large（774M）：人工步骤 14.10，GPT-3 CoT 12.85，以人工解答提示生成子问题 21.08 |
| Magister 等[^92] | 2022-12 | 8 例提示，提示中给出目标答案 | 删去答案错误的 CoT | GSM8K 6725 题留 5337 条（PaLM） | PaLM 540B、GPT-3 175B→T5 XXL（11B）等 | GSM8K，T5 XXL：8.11%→21.99%（PaLM）/18.42%（GPT-3） |
| Fine-tune-CoT[^93] | 2022-12 | 零样本 CoT，每题 D 条 | 最终答案正确 | D=64（MultiArith、SVAMP）或 8 | text-davinci-002（175B）→GPT-3 ada/babbage/curie 等（小 25～2500 倍） | 6.7B 学生 MultiArith：33.33，多样推理 53.33，零样本 CoT 5.00 |
| Fu 等[^95] | 2023-01 | 每题 40 条 | 保留答对的解；按教师 top-5 词元概率做分布匹配 | GSM8K 7K 题→130K 条 | code-davinci-002（≥175B）→FlanT5（≤11B） | FlanT5-XXL：GSM8K 16.1→27.1，BBH CoT 41.8→0.0 |
| RAFT[^102] | 2023-04 | 当前策略每提示 K 条 | 奖励模型取 best-of-K | HH-RLHF 82147 条提示 | LLaMA-7B-SFT 自训练 | 平均奖励：RAFT（K=32）2.294，PPO 2.077 |
| SCOTT[^98] | 2023-05 | 以金标答案为条件做对比解码；为错误答案生成反事实理由 | 未描述拒绝过滤，一致性由解码保证 | CSQA 等 4 个数据集的训练集 | GPT-neox 20B→T5-3B | 4 个数据集上理由更一致，学生更忠实且准确率相当 |
| CoT Collection[^109] | 2023-05 | 每组 6～8 个手写示例，以金标标签为条件 | 须含答案词；剔除超长、重复、含代码者 | 1,060 个任务，1.84M 条 | Codex→Flan-T5 3B/11B | BBH 零样本平均 +4.34%（3B）、+2.60%（11B） |
| phi-1[^112] | 2023-06 | GPT-3.5 写教科书（约束主题与受众）和习题（约束函数名） | 网页代码用 GPT-4 标注训练的分类器过滤；合成数据未描述正确性检查 | 教科书不足 1B、习题约 180M、网页约 6B 词元 | GPT-3.5→phi-1（1.3B） | HumanEval 50.6%，MBPP 55.5% |
| SCoTD[^97] | 2023-06 | 温度 1.0，每例 30 条 | 监督设定丢弃标签错误者（40.4%/45.0%/34.2%）；少样本设定不过滤 | 每例 30 条 | code-davinci-002→OPT（125M～1.3B） | 监督设定，OPT-1.3B，QuaRel：仅标签 59.0，SCoTD 83.8，教师 83.3 |
| ReST[^101] | 2023-08 | 当前策略在 Grow 步采样 | 奖励模型（Metric X）打分，阈值逐轮提高；保留原始数据 | IWSLT 2014 上 16M～32M 条不同样本 | 机器翻译模型自训练 | IWSLT 2014 平均奖励：BC 70.9，ReST（G=2，I=3）83.1，在线 PPO 71.6 |
| LEMA[^106] | 2023-10 | GPT-4 生成 CoT，并纠正多个 LLM 的错误路径 | CoT 与纠错均按最终答案过滤 | GSM8K：增广 CoT 24,948 条，纠错 12,523 对 | GPT-4→LLaMA-2 等（默认 QLoRA） | LLaMA-2-70B GSM8K 83.5%，仅 CoT 81.4% |
| Orca 2[^99] | 2023-11 | GPT-4 按任务采用指定解题策略；训练时擦除系统提示 | 未描述答案正确性过滤；生成时有内容过滤 | 约 817K 条（另继承 Orca 1 的 5M＋1M 条） | GPT-4→LLaMA-2 7B/13B | 零样本推理：Orca-2-13B 比同基座 LLaMA-2-Chat-13B 相对提升 47.54% |
| Turning Dust into Gold[^107] | 2023-12 | 每题 8 条 | 按答案分正负，双 LoRA 分别吸收（NAT） | MATH 训练集，每题 8 条 | gpt-3.5-turbo、gpt-4→LLaMA-7b | MATH 平均（GPT-3.5 Turbo 教师）：正样本蒸馏 5.29，正负混合 3.03，NAT 6.81 |
| ReFT[^104] | 2024-01 | SFT 预热 1～2 轮后在线 PPO 采样 | 无硬过滤，奖励由标准答案给出 | 与 SFT 相同的训练题 | CodeLLAMA-7B、Galactica-6.7B 自训练 | CodeLLAMA-7B GSM8K（N-CoT）：SFT 43.59，离线自训练 45.10，ReFT 53.30 |
| Orca-Math[^110] | 2024-02 | GPT4-Turbo 解题；智能体扩写新题 120,445 道、加难新题 37,157 道 | 新题未描述正确性检查；学生样本按是否与教师答案一致标正负 | 200K 题 | GPT4-Turbo→Mistral-7B | GSM8K pass@1：SFT 81.50%，迭代偏好学习后 86.81% |
| Havrilla 等[^113] | 2024-03 | EI 每题 96 条（T=1.0）；另比较 PPO 与回报条件强化学习 | 去掉错误与重复解；另试稠密奖励与 ORM | 不经 SFT 时 EI 与 PPO 也只需约 60,000 次 rollout 收敛 | Llama-2 7B/13B 自训练 | GSM8K（SFT 初始化）maj@1：SFT 0.41/0.48，EI 0.48/0.53，稀疏奖励 PPO 0.44/0.51（7B/13B） |
| Quiet-STaR[^103] | 2024-03 | 每个词元后并行生成思考 | 无硬过滤；REINFORCE 奖励提高后续文本似然的思考 | OpenWebMath、C4 网络文本 | Mistral 7B 自训练 | OpenWebMath 训练后零样本 GSM8K 5.9%→10.9%，CommonsenseQA 36.3%→47.2% |
| Iterative RPO[^105] | 2024-04 | 每题 30 条；胜者集合并入人工解，以免为空 | 答对为胜、答错为负，构成偏好对 | GSM8K 约 7.5k 题，每轮 55～60k 对，共 4 轮 | Llama-2-70B-chat 自训练（DPO+NLL） | GSM8K 55.6%→81.6%；同数据金标 SFT 63.5%，STaR 一轮 65.2% |
| Setlur 等[^111] | 2024-06 | GPT-4 与 Gemini 1.5 Pro 以 5:1 出题并解题；学生自采正负样本 | 最终答案与合成答案字符串匹配；负样本按步骤优势构造 | 合成题集规模递增；部分实验固定 8k/16k 题 | GPT-4、Gemini 1.5 Pro→DeepSeek-Math-7B、Llama2-7B | 相对合成正样本 SFT，自采正样本使有效数据量约 2 倍，按步骤负样本约 8 倍 |
| System 2 蒸馏[^108] | 2024-07 | 模型自身运行 RaR、S2A、BSM、CoT | 多数投票或输入扰动下一致，否则丢弃 | GSM8k 7461 对（仅答案） | Llama-2-70B-chat 自蒸馏 | 末字母拼接 30.0%→98.0%；GSM8k 蒸馏 CoT 7.13%（System 2 CoT 52.77%，k=1） |

### 4.1 教师理由蒸馏的确立（2022 年 10 月至 2023 年 6 月）

教师理由蒸馏的起点，是把自训练中的答案拒绝采样搬到外部教师上（本文判断）。Li 等让 GPT-3（text-davinci-002）依据 7 个人工示例贪心生成解释，仅在 GPT-3 答对时采用，称为 COTE[^96]。作者把 STaR 列为与其最接近的工作[^96]。合理化提示（RP）则在给定金标答案的条件下生成解释，CROP 在 COTE 被拒时改用 RP 补缺[^96]。2022 年 12 月，三篇工作几乎同时把这一流程用于多步推理[^92][^93][^94]。Magister 等以 PaLM 540B 和 GPT-3 175B 为教师，在 8 例提示中给出目标答案，删去答案错误的 CoT 后微调 T5[^92]。Fine-tune-CoT 用 text-davinci-002 的零样本 CoT 生成理由，只保留最终答案正确者，并可为每题采样多条理由[^93]。Socratic CoT 让 GPT-3 175B 生成子问题及其解答，分别蒸馏成问题分解器和子问题求解器[^94]。Fu 等随后用 code-davinci-002 为 GSM8K 的 7K 道训练题各采样 40 条解，保留答对者后得到 130K 条样本[^95]。2023 年的 SCoTD 与 SCOTT 分别在每例理由数和理由与答案的一致性上继续推进（本文判断）。SCoTD 以温度 1.0 为每例采样 30 条理由，学生为 125M～1.3B 的 OPT[^97]。SCOTT 让 GPT-neox 20B 在给定金标答案时做对比解码，并为错误答案生成反事实理由，用于训练 T5-3B 学生[^98]。

这一阶段的学生均不超过 11B（本文判断）。T5 XXL 在 GSM8K 上的准确率由 8.11% 升至 21.99%（PaLM 540B 教师）或 18.42%（GPT-3 175B 教师）[^92]。GPT-3 6.7B 学生在 MultiArith 上达到 33%，同尺寸模型的零样本 CoT 只有 5%[^93]。为每题采样多条理由后，该学生在 MultiArith 和 SVAMP 上又分别提升约 26% 和 17%[^93]。监督设定下，OPT-1.3B 在 QuaRel 上由仅用标签的 59.0 升至 83.8，与教师贪心解码的 83.3 相当[^97]。按多样性、教师似然、开放性或随机抽样把每例压到 5 条的预算对照，都追不上用满 30 条的模型[^97]。作者据此认为 CoT 的数量是关键驱动力，每例 50 条与 30 条效果相近[^97]。Fu 等专门化后的 FlanT5-XXL（11B）在 GSM8K 上由 16.1 升至 27.1[^95]。

教师 CoT 是否优于数据集自带的人工步骤，同期结论并不一致（本文判断）。Magister 等以 T5 XXL 为学生时，PaLM 教师 CoT 在 GSM8K 上得 21.99，高于人工步骤的 19.94，GPT-3 教师只有 18.42[^92]。在 StrategyQA 上，人工 CoT 以 71.98 高于 PaLM 的 67.15 与 GPT-3 的 63.77，作者归因于人工集样本最多，因为两个教师都会答错部分题目[^92]。Socratic CoT 在 GSM8K 上用 GPT-3 CoT 训练 GPT-2 Large（774M）得 12.85，低于人工步骤的 14.10[^94]。作者因此认为，有人工逐步解答时 LLM 生成的 CoT 并无优势[^94]。Fine-tune-CoT 在 Date Understanding 上的过滤消融显示，初始样本数相同时，按答案过滤比更严格的人工过滤高 5～11%[^93]。按过滤后样本数对齐时，人工核验样本反而高 5～8%，作者将其解读为样本质量与数量之间的权衡[^93]。最可能解释分歧的变量是教师相对任务的强弱和过滤后的样本量，而非理由出自人还是模型（本文推断，依据见[^92][^93][^94]）。

答案过滤并不保证理由正确，Date Understanding 上 27.6% 的答对教师样本含推理错误[^93]。SCOTT 的预研发现，100 条 GPT-3 理由中 42% 未提供输入之外的新信息，37% 不能支撑答案[^98]。用人工理由训练的学生在理由被扰动后，性能变化在 CSQA 上低至 1.1%，说明学生基本忽略理由[^98]。把目标答案放进提示后，PaLM 540B 在 GSM8K 上的 CoT 正确率由 59.98% 升至 79.37%[^92]。作者分析认为，提升主要来自修正了缺一步或错一步的 CoT[^92]。以答案为条件生成的理由可能是事后合理化（本文判断）。SCoTD 作者也承认，无法保证学生的输出确实由其理由推出[^97]。专门化还会损失通用能力，FlanT5-XXL 在 GSM8K 蒸馏数据上专门化后，BBH CoT 准确率由 41.8 降为 0.0[^95]。

### 4.2 自训练谱系：从多数投票到专家迭代（2022 年 10 月至 2024 年 3 月）

自训练路线让模型为自己生成轨迹（本文判断）。这条路线的早期代表 STaR 从少量示例出发推断理由，只学习最终答对的那部分[^103]。ReST 把 STaR 归入受专家迭代（Expert Iteration，EI）启发的方法，概括为采样理由、按答案正确性过滤、再微调的循环[^101]。2022 年 10 月的 LMSI 去掉了对标准答案的依赖[^100]。PaLM-540B 为每道无标签训练题采样 32 条路径，以多数投票确定答案[^100]。通向多数答案的路径全部保留，经 4 种格式增广后用于自我微调[^100]。2023 年的 RAFT 与 ReST 在对齐与机器翻译任务上采用同一模板[^101][^102]。RAFT 每轮从当前模型采样 K 条回复，用奖励模型保留最优者后做 SFT[^102]。ReST 把流程拆成离线的 Grow（策略采样扩充数据）与 Improve（奖励模型排序过滤，阈值逐步提高）两步[^101]。作者把 RAFT 视为每次 Grow 只做一次 Improve 的特例[^101]。2024 年，Quiet-STaR 把 STaR 推广到无标注的网络文本，让 Mistral 7B 在每个词元后生成思考[^103]。它用 REINFORCE 强化有助于预测后续文本的思考[^103]。ReFT 先做 1～2 轮 SFT 预热，再用在线 PPO 对同一批训练题采样大量推理路径，奖励由标准答案直接给出[^104]。Havrilla 等在相同任务和模型上比较 EI、PPO 与回报条件强化学习[^113]。

LMSI 不用任何标签，把 PaLM-540B 的 GSM8K 自洽解码准确率由 74.4% 提到 82.1%[^100]。同一批自产数据用于微调 PaLM-8B 后，其 GSM8K 准确率由 5.0 升至 33.4，超过未调优的 62B 模型[^100]。RAFT（K=32）以 LLaMA-7B-SFT 为起点，在 HH-RLHF 上的平均奖励为 2.294，PPO 为 2.077[^102]。ReST 在 IWSLT 2014 上经两次 Grow、三次 Improve 后平均奖励为 83.1，行为克隆为 70.9[^101]。训练数据量与一次 Grow 相当的在线 PPO 为 71.6[^101]。Quiet-STaR 在 OpenWebMath 上训练后，未经任务微调的零样本 GSM8K 由 5.9% 升至 10.9%，CommonsenseQA 由 36.3% 升至 47.2%[^103]。

在线强化学习是否优于拒绝采样式自训练，两项受控研究的结论相反（本文判断）。ReFT 以 CodeLLAMA-7B 在 GSM8K 自然语言 CoT 上得到 53.30，离线自训练为 45.10，SFT 为 43.59[^104]。Havrilla 等在 GSM8K 上从 SFT 初始化 Llama-2 时，EI 的 maj@1 为 0.48（7B）和 0.53（13B），稀疏奖励 PPO 为 0.44 和 0.51[^113]。他们的总体结论是各算法表现相近，EI 在多数情形下最好，样本复杂度与 PPO 相近[^113]。ReST 在机器翻译上也发现，同等数据量下多步 Improve 的奖励高于在线 PPO[^101]。两项推理研究的离线基线强度不同（本文判断）。ReFT 的离线自训练只从预热检查点采样，每题采 100 条，保留答对者后随机取 10 条[^104]。Havrilla 等的 EI 每题采 96 条，滤掉错误与重复解，并反复迭代至验证集饱和[^113]。ReFT 报告的优势可能部分来自离线基线偏弱，而非在线采样本身（本文推断，依据见[^104][^113]）。

自训练的过滤器同样会出错（本文判断）。LMSI 的多数答案不一定正确，作者的论证是错误答案通常只获得较少路径支持，引入的噪声有限[^100]。ReFT 在选项有限的 MathQA 上出现奖励投机，推理错误但碰对选项的 CoT 同样获得奖励[^104]。ReST 的奖励模型分数随 Grow 次数持续上升，人工评价却以一次 Grow 为最好[^101]。在 IWSLT 2014 上，在线 PPO 的验证集 BLEU 下降近 8 分，作者视为奖励投机的迹象[^101]。Havrilla 等发现强化学习没有让 pass@n 明显超过轻量 SFT，并据此认为模型几乎没有在预训练与 SFT 数据之外探索[^113]。

### 4.3 错误轨迹进入训练信号（2023 年 10 月至 2024 年 6 月）

Turning Dust into Gold 指出，以往蒸馏只从正样本迁移知识，丢弃答错的合成数据[^107]。2023 年下半年起，错误轨迹以纠错、负样本蒸馏和偏好对三种方式进入训练（本文判断）。LEMA 先收集多个 LLM 的错误推理路径，再由 GPT-4 指出出错步骤、解释原因并给出改正，只保留最终答案正确的纠错[^106]。Turning Dust into Gold 用 gpt-3.5-turbo 和 gpt-4 为 MATH 每题采 8 条回答，按答案分成正负两组，再用双 LoRA 结构分别吸收两侧知识（NAT）[^107]。Iterative RPO 回到自训练，Llama-2-70B-chat 每题采 30 条，以答对者为胜、答错者为负构成偏好对[^105]。训练目标是 DPO 加上对胜者的负对数似然（NLL）项，共迭代 4 轮[^105]。作者指出它与 STaR 的区别在于后者只做 SFT，而偏好优化能利用错误的推理链[^105]。Setlur 等区分了三类数据：GPT-4 与 Gemini 1.5 Pro 合成的题目与解答、学生自采的正确解（RFT），以及按步骤优势构造的负样本[^111]。

LEMA 数据让 LLaMA-2-70B 在 GSM8K 上达到 83.5%，只用 CoT 数据为 81.4%[^106]。在数据量与训练词元数相同的对照中，混合 CoT 与纠错数据仍在 5 个基座中的 4 个上占优，例外是 LLaMA-2-7B[^106]。以 GPT-3.5 Turbo 为教师、LLaMA-7b 为学生时，只用正样本蒸馏的 MATH 平均准确率为 5.29，NAT 为 6.81[^107]。分别用正、负样本训练的两个模型在 MATH 测试集上答对的题目几乎不重叠，交并比仅 0.074[^107]。Iterative RPO 在同一份 GSM8K 训练题上给出受控对照：零样本 55.6%，金标 SFT 63.5%，STaR 一轮 65.2%，Iterative RPO 第一轮 73.1%，四轮后 81.6%[^105]。Setlur 等发现，只用强模型生成的正样本做 SFT 时，错误率随合成数据量 $`D`$ 下降很慢，GSM8K 上约为 $`D^{-0.15}`$，MATH 上约为 $`D^{-0.05}`$ [^111]。其学生为 DeepSeek-Math-7B 与 Llama2-7B，自采正样本使有效数据量翻倍，按步骤构造的负样本带来的提升相当于把合成数据扩大 8 倍[^111]。

负样本以什么方式进入目标函数，比是否使用负样本更关键（本文推断，依据见[^105][^107][^111]）。把正负样本直接混合微调时，MATH 平均准确率降到 3.03，低于在原始训练样本上微调的 3.88，作者认为这会把不良行为引入模型[^107]。Setlur 等的标准 DPO 正负配对也没有超过 SFT 策略[^111]。在 GSM8K 上，去掉 NLL 项的标准 DPO 一轮后只有 61.8%，低于 Iterative RPO 的 73.1%[^105]。作者观察到，无 NLL 项时被选序列的对数概率在训练中下降，加入后则不降[^105]。偏好学习中有效的做法是按步骤分配信用或保留对胜者的 NLL 项（本文判断，依据见[^105][^111]）。自产正样本也有代价，Setlur 等发现只用自产正样本训练会放大虚假步骤，使性能随数据量持平甚至下降[^111]。这些方法仍以最终答案为准绳（本文判断）。Iterative RPO 需要标准答案，在四选一的 ARC 上碰对的 CoT 会给偏好对带来噪声[^105]。LEMA 的纠错数据在 QLoRA 下只能被吸收有限的量[^106]。

### 4.4 语料规模化与向长思维链过渡（2023 年 5 月至 2024 年 7 月）

另一条线把教师生成做成大规模语料（本文判断）。CoT Collection 用 Codex 以每组 6～8 个手写示例、在给定金标标签的条件下生成理由[^109]。它为只含 9 个 CoT 任务的 Flan Collection 补充了 1,060 个任务的 1.84M 条理由[^109]。phi-1 的对象是代码而非推理轨迹，但其“合成教科书与习题”的做法是后来推理数据合成的直接前身（本文判断）。GPT-3.5 在主题与受众约束下写出 Python 教科书，并在函数名约束下写出习题与解答[^112]。网页代码则由一个经 GPT-4 标注训练的分类器筛选[^112]。Orca 2 把重点从模仿转到解题策略，GPT-4 按任务被提示采用直接作答、逐步推理或先解释后作答等策略[^99]。训练学生时，这些系统提示被换成不含解题指引的通用提示[^99]。Orca-Math 进一步用智能体合成题目，Ask Me Anything 由每道种子题扩写多道新题，Suggester 与 Editor 逐轮加大难度，解答均由 GPT4-Turbo 生成[^110]。SFT 之后，学生每题采 4 个回答，由 GPT-4 判定是否与教师答案一致来标注正负，再做 KTO 或 DPO 迭代偏好学习[^110]。System 2 蒸馏走相反方向，Llama-2-70B-chat 先用 RaR、S2A、BSM 或 CoT 等多步方法作答，经多数投票或输入扰动下的一致性筛选[^108]。随后只把最终答案蒸馏回不输出中间步骤的同一模型[^108]。

CoT Collection 使 Flan-T5 的 BBH 零样本准确率平均提升 4.34%（3B）和 2.60%（11B）[^109]。其消融显示，覆盖 1,060 个任务的 10K 条样本优于只覆盖 9 个任务的 180K 条样本[^109]。phi-1（1.3B）在 HumanEval 和 MBPP 上的 pass@1 分别为 50.6% 和 55.5%[^112]。Orca-2-13B 在零样本推理基准上比同基座的 LLaMA-2-Chat-13B 相对提升 47.54%，并超过 LLaMA-2-Chat-70B[^99]。Orca-Math 的 Mistral-7B 只做 SFT 时 GSM8K pass@1 为 81.50%，迭代偏好学习后为 86.81%[^110]。正样本只保留教师解时，DPO 与 KTO 的结果都下降 2.27 个百分点[^110]。System 2 蒸馏把 Llama-2-70B-chat 在末字母拼接任务上的准确率由 30.0% 提到 98.0%，高于两步 RaR 本身的 44.5%[^108]。在 TriviaQA 有偏与无偏评测集上，蒸馏模型为 81.3% 与 78.6%，平均生成 56 个词元，S2A 本身为 76.0% 与 69.3%，需 147 个词元[^108]。

Orca 2 与 phi-1 未描述对教师输出的正确性检查，Orca-Math 也只对来自 DMath 的 6,216 道题描述了按标准答案的筛选（本文判断，依据见[^99][^110][^112]）。Orca 2 作者指出，把 GSM8K 等训练集的提示纳入训练，会使相应基准成为域内评测[^99]。Orca-Math 的偏好标签以教师答案为准，教师答错时无从纠正（本文判断，依据见[^110]）。phi-1 作者承认 GPT-3.5 生成的数据错误率高，且部分合成细节因专有原因未公开[^112]。CoT Collection 所用的 Codex 已停止服务，作者认为这对可复现性是严重隐患[^109]。System 2 蒸馏的失败案例划出了答案级压缩的边界（本文判断）。在 GSM8k 上把 CoT 蒸馏成只输出答案的模型后，单样本（k=1）准确率仅 7.13%，零样本 CoT 本身为 52.77%[^108]。其自监督目标由多数投票得到，共 7461 对，准确率只有 56.81%[^108]。作者认为数学题所需的推理与其他任务差异很大，该方法并非总能奏效[^108]。由于目标本身噪声很大，现有实验无法区分失败来自压缩推理还是目标错误（本文推断，依据见[^108]）。Quiet-STaR 的零样本收益随思考词元数增加而增大，这与后来长思维链以更多推理词元换取准确率的思路一致（本文判断，依据见[^103]）。其代价是每生成一个词元前都要先生成多个思考词元，且只在 7B 模型上验证过[^103]。后续各节讨论的长思维链数据工作（如 DeepSeek-R1、s1、LIMO）仍以“生成、筛选、再做 SFT”为骨架，变化主要在轨迹长度、题目难度与数据量（本文判断）。

### 4.5 小结（本文判断）

- 2022 至 2024 年确立的基本骨架是“采样多条轨迹、按最终答案或一致性过滤、再微调”，教师蒸馏与自训练共享这一骨架，区别在于由谁生成（依据见[^92][^100][^113]）。
- 每题采样数与任务覆盖面是早期证据最一致的正向杠杆，前者的收益会饱和，对未见任务的泛化而言后者更重要（依据见[^93][^97][^109]）。
- 答案过滤成本最低，却会放行推理错误的样本，并在选项有限的任务上引发奖励投机，过程级奖励因此被列为后续方向（依据见[^93][^104][^105]）。
- 错误轨迹需要与正样本区别对待才能提供额外信号，直接混入 SFT 会降低准确率，标准 DPO 配对也不优于 SFT（依据见[^105][^107][^111]）。改写为纠错样本、按步骤分配信用或在 DPO 中保留胜者 NLL 项则带来提升（依据见[^105][^106][^111]）。
- 在线强化学习与专家迭代孰优尚无定论，现有分歧很可能来自离线基线的采样策略、保留量与迭代轮数不同（依据见[^101][^104][^113]）。
- 证据强度不均，多数结果是相对基座或 SFT 的前后对比，独立改变教师、过滤与数据量的受控研究很少，且多项工作依赖已停用或不公开细节的闭源教师（依据见[^97][^109][^112]）。

## 参考来源

[^96]: [Li et al. — Explanations from Large Language Models Make Small Reasoners Better (arXiv 2210.06726, 2022-10)](https://arxiv.org/abs/2210.06726)
[^100]: [Huang et al. — Large Language Models Can Self-Improve (arXiv 2210.11610, 2022-10)](https://arxiv.org/abs/2210.11610)
[^94]: [Shridhar et al. — Distilling Reasoning Capabilities into Smaller Language Models (arXiv 2212.00193, 2022-12)](https://arxiv.org/abs/2212.00193)
[^92]: [Magister et al. — Teaching Small Language Models to Reason (arXiv 2212.08410, 2022-12)](https://arxiv.org/abs/2212.08410)
[^93]: [Ho et al. — Large Language Models Are Reasoning Teachers (arXiv 2212.10071, 2022-12)](https://arxiv.org/abs/2212.10071)
[^95]: [Fu et al. — Specializing Smaller Language Models towards Multi-Step Reasoning (arXiv 2301.12726, 2023-01)](https://arxiv.org/abs/2301.12726)
[^102]: [Dong et al. — RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment (arXiv 2304.06767, 2023-04)](https://arxiv.org/abs/2304.06767)
[^98]: [Wang et al. — SCOTT: Self-Consistent Chain-of-Thought Distillation (arXiv 2305.01879, 2023-05)](https://arxiv.org/abs/2305.01879)
[^109]: [Kim et al. — The CoT Collection: Improving Zero-shot and Few-shot Learning of Language Models via Chain-of-Thought Fine-Tuning (arXiv 2305.14045, 2023-05)](https://arxiv.org/abs/2305.14045)
[^112]: [Gunasekar et al. — Textbooks Are All You Need (arXiv 2306.11644, 2023-06)](https://arxiv.org/abs/2306.11644)
[^97]: [Li et al. — Symbolic Chain-of-Thought Distillation: Small Models Can Also "Think" Step-by-Step (arXiv 2306.14050, 2023-06)](https://arxiv.org/abs/2306.14050)
[^101]: [Gulcehre et al. — Reinforced Self-Training (ReST) for Language Modeling (arXiv 2308.08998, 2023-08)](https://arxiv.org/abs/2308.08998)
[^106]: [An et al. — Learning From Mistakes Makes LLM Better Reasoner (arXiv 2310.20689, 2023-10)](https://arxiv.org/abs/2310.20689)
[^99]: [Mitra et al. — Orca 2: Teaching Small Language Models How to Reason (arXiv 2311.11045, 2023-11)](https://arxiv.org/abs/2311.11045)
[^107]: [Li et al. — Turning Dust into Gold: Distilling Complex Reasoning Capabilities from LLMs by Leveraging Negative Data (arXiv 2312.12832, 2023-12)](https://arxiv.org/abs/2312.12832)
[^104]: [Luong et al. — ReFT: Reasoning with Reinforced Fine-Tuning (arXiv 2401.08967, 2024-01)](https://arxiv.org/abs/2401.08967)
[^110]: [Mitra et al. — Orca-Math: Unlocking the potential of SLMs in Grade School Math (arXiv 2402.14830, 2024-02)](https://arxiv.org/abs/2402.14830)
[^113]: [Havrilla et al. — Teaching Large Language Models to Reason with Reinforcement Learning (arXiv 2403.04642, 2024-03)](https://arxiv.org/abs/2403.04642)
[^103]: [Zelikman et al. — Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking (arXiv 2403.09629, 2024-03)](https://arxiv.org/abs/2403.09629)
[^105]: [Pang et al. — Iterative Reasoning Preference Optimization (arXiv 2404.19733, 2024-04)](https://arxiv.org/abs/2404.19733)
[^111]: [Setlur et al. — RL on Incorrect Synthetic Data Scales the Efficiency of LLM Math Reasoning by Eight-Fold (arXiv 2406.14532, 2024-06)](https://arxiv.org/abs/2406.14532)
[^108]: [Yu et al. — Distilling System 2 into System 1 (arXiv 2407.06023, 2024-07)](https://arxiv.org/abs/2407.06023)
