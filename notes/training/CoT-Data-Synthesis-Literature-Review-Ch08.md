# 训练数据中的思维链合成：方法、证据与开放问题 · 第 8 节

中文 | [English](./CoT-Data-Synthesis-Literature-Review-Ch08_en.md)

- **调研日期**: 2026-10-22（证据截止：arXiv 首版日期不晚于 2026-10-22）
- **导航**: [主页面](./CoT-Data-Synthesis-Literature-Review.md)（摘要、第 1–3 节、第 11–13 节与附录） · 上一节：[第 7 节](./CoT-Data-Synthesis-Literature-Review-Ch07.md) · 下一节：[第 9 节](./CoT-Data-Synthesis-Literature-Review-Ch09.md)
- **依据**: 句末的上标数字是引用，对应文末参考来源中的精读文献；每条引用都有从该文献全文逐字摘录、并经脚本与全文核对的原文。标有（本文判断）、（本文推断）或（本文统计）的内容，是本文的综合分析或统计，不是来源原话。

## 8 选择、规模与长度

通过验证的候选轨迹通常多于训练所需，同一道题也常有多条正确轨迹（本文判断）。本节讨论验证之后的决定：留多少、按什么信号留、题数与每题采样数如何配置、轨迹多长，以及这些决定如何随学生变化（本文判断）。保留判据见验证一章，智能体轨迹的筛选见智能体轨迹一章（本文判断）。贯穿本节的问题是：“少而精胜过全量”一类结论有多少来自选择信号本身，多少来自未控制的训练预算、轨迹长度与学生规模（本文判断）。

### 8.1 少量精选与扩量

“少而精”有两个源头（本文判断）。其一是指令微调中的影响估计：LESS 在约 270K 条混合指令数据上，用低秩梯度特征与目标任务少样本的相似度挑选数据[^164]，并报告 5% 的子集常常优于全量训练[^164]。其二是 2025 年初的长 CoT 精选（本文判断）。LIMO 只用 800 条样本微调 Qwen2.5-32B-Instruct[^72]，并提出假说：当领域知识已在预训练中充分编码时，少量经过设计的示范即可诱发复杂推理[^72]。s1 从 16 个来源收集 59,029 道题[^86]，再按质量、难度与多样性三条准则过滤到 1,000 条[^86]。此后的工作把精选做成排序器或课程：Select2Reason 结合难度奖励模型与轨迹长度排序[^173]，Light-R1 按通过率逐级缩小题集[^174]，Phi-4-reasoning 专选处在 Phi-4 能力边缘的“可教”题目[^175]。

LIMO 在 AIME24 上达到 63.3%，在 MATH500 上达到 95.6%，此前的微调模型分别为 6.5% 与 59.2%[^72]。其样本效率实验按推理链质量分给 2,125 道候选题排序，取靠前的子集训练[^72]。前 400 条就把 AIME24 从 16.5 提到 57.5[^72]；超过 800 条后收益递减，LIMO-800 到 LIMO-1k2 在 AIME24 上只多 0.9[^72]。s1 以 Qwen2.5-32B-Instruct 为底座，在思考上限约 30,000 token 的消融中，随机、只按多样性、只取最长轨迹的三个 1K 子集在 AIME24 上分别为 36.7、26.7 和 33.3，s1K 为 50.0[^86]。用全部 59K 条训练得到 53.3，与 s1K 之差的 95% 自助置信区间为 -13.3% 至 20.0%[^86]，训练成本却是 394 对 7 个 H100 GPU 小时[^86]。

LESS 的结论随底座而变[^164]。在 Mistral-7B 上，LESS 的 5% 子集在 MMLU、TydiQA、BBH 上为 61.8、60.3、56.0，全量为 60.4、57.7、53.0[^164]。在 Llama-2-7B 上，它只在 TydiQA 上超过全量（56.2 对 54.0），在 MMLU 与 BBH 上低于全量（50.2 对 51.6，41.5 对 43.2）[^164]。Select2Reason 以 Qwen2.5-Math-7B-Instruct 为学生，从 OpenR1-Math-220k 约 196k 条正确样本中选 10%[^173]。该子集在 MATH 上 Pass@1 为 0.914，高于全量的 0.894，在 AIME24 上为 0.433，低于全量的 0.465[^173]。

Light-R1 先按 DeepScaleR-1.5B-Preview 的通过率筛出约 76k 道题交给 DeepSeek-R1 生成，再保留 DeepSeek-R1 采样既非全对也非全错的约 3k 道难题[^174]。Qwen2.5-32B-Instruct 的 AIME24 经两个 SFT 阶段与 DPO 从 16.6 依次升到 69.0、73.0、75.8，模型合并后为 76.6[^174]。同一批 3k 道题还把 DeepSeek-R1-Distill 的 32B 模型在 AIME24 上从 72.6 提到 78.1[^174]。Phi-4-reasoning 用 o3-mini 生成示范，SFT 数据超过 1.4M 条、8.3B 个 token[^175]。其 14B 模型在 AIME 25 上为 63.1，再经短期结果奖励 RL 后为 78.0，DeepSeek-R1-Distill-70B 为 51.5[^175]。该报告也提示，两次各取 5 次平均的 AIME 评测最多可差 5 至 10 个百分点[^175]。

强化学习的提示选择把“少”推到了极端（本文判断）。Qwen2.5-Math-1.5B 只用一个样本做 RLVR，MATH500 从 36.0% 升到 73.6%，与 1,209 条 DSR-sub 的 73.6% 持平[^172]。但在按各自最优检查点报告的对照表中，只奖励格式的基线在 MATH500 上已达 65.6，DSR-sub 为 75.2[^172]。作者也说明 1-shot RLVR 并不节省 RL 计算[^172]。

扩量一侧也有稳定的证据（本文判断）。RFT 发现 SFT 准确率随监督数据量呈对数线性增长[^165]。Demystifying Long CoT 在 Llama-3.1-8B 上用 QwQ-32B-Preview 蒸馏的长 CoT 做 SFT，MATH-500 超过 70% 且到 3.5B token 仍未饱和，而用 Qwen2.5-Math-72B-Instruct 蒸馏的短 CoT 收敛在 55% 以下[^83]。Qwen2.5-32B-Instruct 学 DeepSeek-R1 数据时持续随数据量受益，约 16k 条即把平均成绩提高 15.2%[^169]。

分歧最可能来自三个未控制的变量（本文推断）。第一是优化步数。LESS 对所有子集都训练 4 个 epoch，作者称给小子集加 epoch 并无收益[^164]；Select2Reason 对任何规模的子集都训练 3 个 epoch[^173]。按此设置，10% 子集只得到全量约十分之一的梯度步数（本文推断，依据见[^173]）。而在固定更新预算下，Olmo3-7B 在 400 条长 CoT 样本上训练 128 个 epoch，在 AIME'24/25 与 GPQA 上比在 51,200 条上训练 1 个 epoch 高 12 至 26 个百分点[^18]。第二是底座知识。同一份 LIMO 数据用于 Qwen1.5-32B-Chat 时 AIME2024 只有 9.2%，用于 Qwen2.5-32B-Instruct 时为 63.3%[^72]。第三是评测难度。Select2Reason 的子集在 MATH 上胜出而在 AIME24 上落后[^173]；影响函数剪枝一文中，各方法在 AIME24 上的成绩都可忽略[^7]。OpenThoughts 与 ZGCM-1 在扩量与剪枝上的相反结论，也宜放在这三个变量下比较（本文判断）。

### 8.2 选择信号及其混淆

在答案正确性过滤之上，最常见的第二道信号是相对于某个模型的难度，Light-R1 的两级通过率筛选即属此类（本文判断，依据见[^174]）。Phi-4-reasoning 在没有标准答案时以强模型的多数答案为代理，用较弱模型与之一致的比例估计难度[^175]。在强化学习的提示选择上，这类信号收敛到“既非全对也非全错”的区间（本文判断，依据见[^174][^178]）。Light-R1 只保留通过率在 0.25 到 0.625 之间的 RL 提示[^174]。在线难度过滤以经 1.1K 条 SFT 冷启动的 Qwen2.5-3B 为策略，平衡区间 (0.3, 0.7) 的五项基准均值为 30.1，不过滤的 GRPO 为 26.3，只截一侧的偏斜过滤为 24.9 至 25.9[^178]。其理论依据是期望策略改进以任务成功率的方差为下界[^178]。通过率为零也不等于难，Light-R1 人工检查发现这类题中一半以上的答案无法验证或本身有误[^174]。1-shot RLVR 按历史训练准确率的方差排序，但中低方差的样本单独使用也能提升 MATH500[^172]。

基于似然的选择（自然度选择）计算模型赋予每条样本的平均对数概率，保留概率高者，假定它们更贴合模型的固有偏好[^21]。The Signal is in the Steps 指出，整条轨迹的平均对数概率（GALP）在短的单教师回答上有效，在长轨迹、多教师的场景中失效[^6]。在 817 道 LIMO 题与 DeepSeek-R1、Qwen3-32B、QwQ-32B 三个教师上，Qwen3-32B 的轨迹在 7B 与 32B 学生下 GALP 都最高，训练效果却最差[^6]。该文提出 LALP，把轨迹切成步骤，每步只在小的局部窗口内打分，再对步骤取平均[^6]。两种打分可写成如下形式（本文判断，记号依据[^21]）：

```math
s_{\mathrm{G}}(r)=\frac{1}{|r|}\sum_{t}\log p_\theta(y_t\mid y_{<t},q),\qquad
s_{\mathrm{L}}(r)=\frac{1}{|\mathcal{S}|}\sum_{j}\frac{1}{|s_j|}\sum_{l}\log p_\theta\big(s_{j,l}\mid s_{j,<l},\,s_{j-k:j-1},\,q\big)
```

其中 $`\mathcal{S}`$ 为步骤集合，$`k`$ 为窗口步数（本文判断）。在每题从三教师池中选一条的设置下，Qwen2.5-32B-Instruct 用 LALP 选出的数据训练后均值为 0.726，GALP 为 0.632，随机为 0.651[^6]；作者认为全局似然在此是系统性错排而非噪声[^6]。

似然类信号还受步长混淆[^21]。On the Step Length Confounding 把 Just 等人的 Local LP 列为当前最好的自然度方法[^21]，该方法即 LALP[^21][^6]。它发现这类选择系统性地偏好推理步更长的样本[^21]。机制是每步首 token 的概率偏低，步越长，它在平均中被摊得越薄，平均对数概率随之虚高[^21]；总响应长度的影响则弱得多[^21]。在 LIMO-v2 的 800 道题上，每题由四个模型各生成 5 条、共 20 条，几种自然度方法选出的样本步长都明显偏长[^21]。在 LIMO-v2 与 AceReason-1.1-SFT 上训练四个不同规模的模型，丢弃首 token 概率与用因果去偏回归消除首 token 混淆两种变体，平均准确率比 Local LP 高 6.28% 与 9.08%[^21]。偏置的后果是选择器过度集中于单一数据源[^21]。

梯度类方法以“对目标的影响”为信号（本文判断）。LESS 发现未归一化的梯度内积偏向梯度范数更大的短序列，因此改用余弦相似度[^164]。影响函数剪枝在 LIMO 上以 Llama3-8B-Instruct 打分并训练，保留 90% 时 GSM8k 为 0.8113，随机保留 90% 为 0.7839，不剪枝为 0.7722[^7]。但该文以 MATH500 为验证集挑选检查点[^7]，所选子集用于 Qwen2.5-Math-7B-Instruct 时没有策略稳定胜过基线[^7]。GRACE 在步级上衡量与答案方向梯度的对齐及与前文轨迹的一致性；以 Qwen3-VL-2B 在多模态数学 CoT 上选 20% 子集时，去掉答案对齐项后相对均值从 108.8 降到 97.5[^26]。DeGMatch 给出了更强的诊断：长推理轨迹的候选梯度被少数群体级方向主导，前 50 个主成分解释了 86.7% 至 89.4% 的中心化梯度方差[^55]。它先以群体均值中心化梯度并去掉主成分，再做目标匹配[^55]。只用前 50 个主成分排序时，五类目标识别准确率为 56%，去掉均值与这些主成分后为 71%[^55]。以 Qwen2.5-Math-7B 的派生模型为学生、从 OpenR1-Math-220k 的 93K 条轨迹中各选 10K 条时，八项数学基准均值随机为 55.03，按长度选为 58.73，LESS 为 56.98，DeGMatch 为 60.73[^55]。该文还发现 LESS、RDS+、GIST、TAROT 等目标感知方法在推理场景下不能稳定胜过长度基线[^55]。在面向 AIME 的 3K 子集上，它与总 token 数相近（36.1M 对 35.3M）的长度分层随机子集相比，均值为 34.83 对 33.70[^55]。

不依赖梯度的信号成本更低（本文判断）。HES 只对熵最高的 0.5% token 的熵求和[^28]。以 Qwen3-8B-Base 在 Mixture-of-Thoughts 上做 SFT，数学域前 20% 的 HES 子集均值为 31.34，全量为 31.83，同比例按长度选为 29.05，随机为 23.86[^28]。在各长度分组内，高 HES 子集都胜过低 HES 子集[^28]。TEMP 只看推理轨迹前 100 个 token 在扰动检查点上的损失来判断难度[^35]。从 M23k 选 1k 条时，它在 Qwen2.5-7B-Instruct 与 Llama-3.1-8B-Instruct 上比次优基线最多高 1.1% 与 1.7%[^35]。TEMP 也指出，损失、嵌入与梯度类指标主要被轨迹长度、冗长度与风格差异主导[^35]。

RSR 以学生下平均 token 秩与平均负对数似然之比衡量轨迹，取比值最小者[^13]。它在 5 个学生与 11 个教师上与训练后成绩的平均 Spearman 相关为 0.86，以平均 token 长度为指标时只有 0.53[^13]。每题从 11 个教师的 33 条候选中选 1 条、共 5k 题时，Qwen-3-14B 的四项均值为 78.6，随机为 70.2，取最长为 71.4[^13]。但在 DeGMatch 从 93K 条中选 10K 条的设置中，RSR 选出的子集只有 34.9M token，均值 51.24，低于随机的 55.03[^55]。两者的差别最可能在于选择发生在题内还是跨题（本文推断，依据见[^13][^55]）。RSR 作者也承认，跨题选择会引入额外混淆[^13]。MI-Distillation 只改变排序准则做了对照：在同一候选池与同一正确性过滤下，Qwen2.5-3B-Instruct 上 SeqLSS 均值为 47.14，PPL 为 44.90，随机为 43.95，反向排序为 42.10[^43]。

多样性信号的评价对象正从 SFT 本身转向后续 RL（本文判断）。DiverseSFTTraces 用规则化的“路径指纹”刻画步骤事件序列，聚类后做最远点选择[^48]。与同预算的“相似”选择相比，OLMo3-7B 经相同 RL 后，在 SFT 未见过的环境上 pass@8 高 16.9 分[^48]。路径多样的检查点平均准确率略低，但成败混合的提示占 54.7%，相似选择为 46.9%[^48]；在二值结果奖励下，全对或全错的 rollout 组组内优势为零[^48]。合成文本的聚类多样性与预训练和 SFT 表现正相关，但这一证据只来自 350M 与 1.4B 模型[^179]，且不涉及推理轨迹（本文判断）。

这些信号的共同问题是长度（本文判断，依据见[^21][^35][^55]）。显式控制长度的有 LESS 的梯度归一化[^164]、HES 的长度分组检验[^28] 与 DeGMatch 的 token 匹配对照[^55]；Select2Reason 的排序器本身含长度项[^173]。选择的跨模型稳定性也不足：用 Llama 选出的子集训练 Qwen 时没有策略稳定胜出[^7]，S2L 在 Llama3.1 上排第二，在 Qwen2.5 上只略好于随机[^35]。选择本身的成本相差几个数量级（本文判断）。步长去偏的回归拟合通常几秒即可完成[^21]，路径指纹选择在 Nemotron-Cascade 2 上只需一个 CPU 节点约三小时[^48]。RSR 对 5,000 条轨迹的打分在单张 H200 上不到 1 小时[^13]，DeGMatch 为数学候选池计算梯度约需 58.3 个 GPU 小时[^55]。表 8-1 汇总了主要方法（本文统计）。

表 8-1 推理数据选择方法对比

| 方法 | 选择信号 | 子集规模 | 预算控制 | 结果（条件） | 主要局限 |
| --- | --- | --- | --- | --- | --- |
| LESS[^164] | 低秩梯度与目标少样本的余弦相似度 | 约 270K 条指令中选 5% | 各子集均训 4 个 epoch | Mistral-7B：MMLU 61.8，全量 60.4；Llama-2-7B：MMLU 50.2，全量 51.6 | 需先预热微调 |
| Select2Reason[^173] | 难度奖励模型与轨迹长度加权排序 | 约 196k 条中选 10% | 任何规模均训 3 个 epoch | Qwen2.5-Math-7B-Instruct：MATH 0.914，全量 0.894；AIME24 0.433，全量 0.465 | 排序器含长度项 |
| 影响函数剪枝[^7] | 对微调后答案对错的影响 | LIMO 保留 90% | 按 MATH500 选检查点 | Llama3-8B-Instruct：GSM8k 0.8113，随机 0.7839 | 跨模型族不迁移；单次运行 |
| LALP[^6] | 步级局部对数概率 | 817 题，每题从三教师中选 1 条 | 题数固定 | Qwen2.5-32B-Instruct：0.726，GALP 0.632，随机 0.651 | 看不到长程错误 |
| Aslec[^21] | 去除步首 token 偏置的对数概率 | 每题 20 条中选 5 条 | 题数固定 | 平均比 Local LP 高 6.28% 与 9.08% | 可能存在更深的混淆 |
| RSR[^13][^55] | 平均 token 秩与平均负对数似然之比 | 每题 33 条中选 1 条，共 5k 题 | 题数固定 | Qwen-3-14B：78.6，随机 70.2；跨题选 10K 时 51.24，随机 55.03 | 跨题选择引入额外混淆 |
| SeqLSS[^43] | 学生可学区域内的信息占比 | 7,500 道 MATH 题，每题选 1 条 | 同一候选池与正确性过滤 | Qwen2.5-3B-Instruct：47.14，随机 43.95 | 以数学为主；看不到步骤正确性 |
| HES[^28] | 熵最高 0.5% token 的熵之和 | 前 20% | 子集训练 FLOPs 少 80% | Qwen3-8B-Base 数学：31.34，全量 31.83，长度 29.05 | 依赖稀疏的分叉点 |
| TEMP[^35] | 前 100 个 token 在扰动检查点上的损失 | 从 M23k 选 1k 条 | 各方法同为 1k 条 | 比次优基线最多高 1.1%（Qwen2.5）与 1.7%（Llama3.1） | 需要合理的微调方向估计 |
| GRACE[^26] | 步级梯度对齐与轨迹一致性 | 20% 与 5% | 按比例与全量比较 | Qwen3-VL-2B-Instruct：全量的 108.8% 与 100.2% | 多模态；部分收益来自少遗忘 |
| DeGMatch[^55] | 去群体结构的梯度目标匹配 | 93K 条中选 10K | token 匹配与长度分层随机对照 | 60.73，长度 58.73，全量参考 58.80 | 全量对比未对齐预算；约 58.3 GPU 小时 |
| 路径多样性[^48] | 规则路径指纹与最远点选择 | 同池多样子集对相似子集 | 同预算与训练配方 | OLMo3-7B：留出环境 pass@8 高 16.9；单模型候选池在 10 个数学基准上高 3.39 至 6.17 | 未测量训练种子间方差 |

### 8.3 规模的维度

规模至少有三个维度：题目数、每题轨迹数与训练轮数（本文判断）。RFT 较早系统考察了前两者的关系（本文判断）。它在 GSM8K 的 7,473 道训练题上让 SFT 模型自采样，每题最多 100 条，只保留答案正确且经 Python 复核计算的路径，再按方程列表去重[^165]。LLaMA-7B 的 maj1@1 从 SFT 的 35.9 升到 41.7，33B 模型则无收益（SFT 54.6，RFT 54.5）[^165]。汇集多个模型的拒绝采样结果后，LLaMA-7B 达到 49.3[^165]。收益随不同推理路径的数量而非样本数增长[^165]。更强的生成器多样性反而更低：LLaMA-33B-SFT 平均每题生成 88.7 条正确路径，只有 6.5% 的路径为其独有[^165]。

同一团队随后用这批数据研究配比（本文判断，依据见[^165][^166]）。Dong 等人从 GSM8K RFT、Code Alpaca 与 ShareGPT 中按 1 到 1/256 的比例取子集，分别训练或混合训练[^166]，其中 GSM8K RFT 出自 Yuan 等人的 RFT 一文[^166]。数学与代码能力随数据量持续提升，通用能力在约 1k 条后进入平台[^166]。混合在低资源时互相促进，在数据充足时产生冲突，组成数据的绝对量比比例更重要[^166]。相对混合顺序训练，其双阶段混合微调使 LLaMA-7B 的 GSM8K 从 32.6 升到 41.92，33B 从 44.24 升到 56.36[^166]。

题数与每题采样数之间的权衡，两类证据并不一致（本文判断）。RFT 发现，翻倍每题采样数的收益不如翻倍训练题，因为新路径不带来新题[^165]。BehavioralEssence 则在固定轨迹总数下比较，500 道题各采 128 条与 16K 道题各采 4 条的平均结果几乎相同[^54]。最可能的解释变量是轨迹形态（本文推断）。RFT 的对象是 GSM8K，同一题的不同推理路径数量存在上限[^165]；BehavioralEssence 研究长 CoT 蒸馏，并认为其传递的主要是可复用的推理行为[^54]。

DataRepetition 把训练轮数作为第三个维度[^18]。在 51200 次更新的固定预算下，Olmo3-7B 在 1600 条样本上训练 32 个 epoch，基准均值为 39%，在 51200 条上训练 1 个 epoch 只有 17%[^18]。收益在 32 至 64 个 epoch 附近饱和，训练 token 准确率达到完全记忆可作为停止信号[^18]。单 epoch 模型只有 24% 的生成能正常结束，32 epoch 模型接近 89%[^18]。随着 epoch 增加，验证损失明显上升[^18]，基准成绩却仍在提高，因此验证损失不宜作为长 CoT SFT 的早停依据（本文推断，依据见[^18]）。教师强弱决定扩量是否有益，用 Qwen3-0.6B 作教师时平均成绩随样本增多而下降[^18]。

扩量也有跨领域代价（本文判断）。Light-R1 从第二阶段起 GPQA 下降，作者归因于大量数学训练削弱泛化[^174]。影响函数一文也发现数学 SFT 会损害 GPQA，剪得更多反而损害更小[^7]。中训练阶段的串行扩量也会先升、后平、再降[^51]。

这一方向的证据仍有缺口（本文判断）。RFT 没有拟合缩放律，因为许多数字是估计值且各模型设置未对齐[^165]。DataRepetition 没有找到因果机制，最优数据集大小仍无法事先确定[^18]。在本节文献中，尚无工作在同一受控框架下联合比较题目数、每题采样数与训练轮数（本文判断）。

### 8.4 轨迹中什么在起作用

一组受控研究表明，学生学到的主要是轨迹的结构与行为，而非逐步内容（本文判断，依据见[^169][^170][^54]）。Li 等人以 Qwen2.5-32B-Instruct 为学生，17k 条长 CoT 即在 AIME 2024 上达到 56.7%（+40.0%）[^169]。在以 4,618 条正确的 QwQ-32B-Preview 轨迹为对照的扰动实验中，只用答案错误的样本训练，平均成绩为 63.1%，只比全对低 3.2%[^169]。70% 的数字被篡改时仍有 62%，全部数字被篡改则跌到 2.7%[^169]。打乱 67% 样本的推理步骤，AIME 2024 下降 13.3%[^169]。删除步骤会同时缩短长度，插入步骤则基本保持原长度[^169]。Valmeekam 等人用 A\* 搜索生成可形式化验证的迷宫轨迹，从头训练 0.5B 的 Qwen 模型，每个模型用 500K 条样本[^170]。在 Wilson 迷宫上训练并测试时，规划准确率在只训解答时为 10.0，用正确轨迹为 79.9，用跨题随机交换的轨迹为 83.3[^170]。在开卷问答 CoTemp QA 上，DeepSeek-R1 轨迹在四个学生中的三个上训练效果最好，却被受试者评为最难理解[^182]。

答案错误的轨迹同样可用（本文判断，依据见[^12][^54]）。Shape of Thought 用 Gemma-2-27B-IT 为每题各取一条答案正确与一条答案错误的轨迹[^12]。在 GSM8K 上，Gemma-2-2B 以人工 CoT 训练的最高准确率为 0.29，错误轨迹与正确轨迹分别再高 0.11 与 0.09[^12]。合成轨迹的初始训练损失为 0.55 至 0.59，人工轨迹为 0.86，作者据此认为分布接近程度可能比正确性更重要[^12]。BehavioralEssence 用 Qwen3-4B 为 3,000 道 DAPO-Math-17K 题各生成 16 条轨迹，得到 22,222 条正确与 25,778 条错误轨迹[^54]。只用错误轨迹训练，在数学集上保留了正确轨迹 97.7% 的绝对准确率[^54]；以 Qwen3-4B 为学生时，两种模型表示的线性 CKA 达 0.998[^54]。DataRepetition 中负例甚至略好，AIME'24 上为 40.0% 对 37.3%[^18]。Cognitive Behaviors 发现，在 Countdown 上做相同的 RL，Qwen-2.5-3B 约达 60%，Llama-3.2-3B 为 30%[^87]。用含验证、回溯等行为的合成轨迹预热 Llama 后，其 RL 表现追上 Qwen[^87]，预热轨迹答案错误时也是如此[^87]。空思维链与等长占位符两种对照都只与 Llama 底座相当，约 30% 至 35%[^87]。

回溯行为也并非总有益[^183]。Qin 等人在 CountDown 上用 DFS 生成带回溯的搜索轨迹，DFS 只解出 57% 的题[^183]。以从头训练的 17M 与 38M 模型、在相同推理算力下比较，回溯轨迹训练的模型在 CountDown 上不如直接解答加并行采样，在 Sudoku 上则更好[^183]。模型会照搬轨迹中的搜索过程，包括先犯错再纠正，表现也受轨迹生成器的质量所限[^183]。经 GRPO 后，回溯模型在 4096 token 预算下解出近 70%，超过 DFS 教师的 57%[^183]。

反方证据来自对生成过程的干预（本文判断）。Lee 等人固定生成器、题集与正确性过滤，只改变生成时是否给出标准答案并要求推向该答案[^184]。Qwen3-8B 在 935 道题上自蒸馏后，MATH-500 从答案盲的 95.1 降到 78.9，AIME 2024–2025 从 71.7 降到 44.4[^184]。把答案盲轨迹截到与泄露轨迹等长后仍得 95.0，说明损失来自内容而非长度[^184]。在答案过早出现的子集上，只切掉首次陈述答案的那一行（约占轨迹的 1.4%），就收回 29.8 分差距中的 24.6 分[^184]。只在失败题上泄露答案的 STaR 式补救仍损失 4.0 分[^184]。这一损失在 MMLU 与 GPQA-Diamond 等多选基准上不出现[^184]。

两类证据最可能由“扰动是否改变了生成过程”来调和（本文推断，依据见[^169][^184]）。篡改数字、答案错误与跨题交换都保留了向前推导或搜索的形式，打乱步骤与以答案为条件的合理化则破坏了它（本文推断，依据见[^169][^170][^184]）。任务类型是第二个变量：在要求精确运算序列的 Countdown 上，正确轨迹的增益明显大于错误轨迹，绝对增益最高达 20%[^12]，而以答案为条件的损失在多选题上消失（本文推断，依据见[^12][^184]）。BehavioralEssence 也把结论限定在局部事实错误，不包括推理整体崩坏[^54]。此外，Chen 等人的教师 CoT 是在提示中给出标准答案并要求与之一致的条件下生成的[^171]。按答案条件化研究的结果，其教师与粒度比较可能带有这一混淆（本文推断，依据见[^171][^184]）。

### 8.5 长度与压缩

Wu 等人在 MATH Level 5 上让 Qwen2.5-Instruct 系列每题生成 60 个长度各异的解[^167]。准确率随 CoT 步数先升后降，最优步数随题目难度增加、随模型能力下降[^167]。最优长度从 1.5B 模型的 14 步降到 72B 模型的 4 步，72B 模型最优长度与最长 CoT 的准确率差距可达 40%[^167]。在只含加法的合成算术上，用最优长度 CoT 训练的 6 层 GPT-2 胜过用随机长度训练的 9 层模型[^167]。作者也承认，真实问题的最优长度难以估计[^167]。

长 CoT 是否有益取决于学生规模（本文判断，依据见[^71][^43]）。Small Models Struggle 在 MATH 的 7,500 道题上，用 QwQ-32B-Preview 生成长 CoT，用 Qwen2.5-32B-Instruct 生成短 CoT[^71]。Qwen2.5-0.5B、1.5B、3B 用长 CoT 的平均成绩为 14.8、27.0、40.3，低于短 CoT 的 19.5、34.2、43.4[^71]。7B、14B、32B 则反过来，32B 为 73.0 对 59.3[^71]。MI-Distillation 也报告长 CoT 对小模型学生常不如短 CoT[^43]，其梯度分析显示长 CoT 引起更大的梯度幅度与更集中的更新方向，且学生越大越明显[^43]。PropsOfSupervision 保持题目与答案不变，只改写推理部分[^25]。约为 Detailed 变体两倍长的 Lengthy 变体使 PLLuM-8B 出现灾难性遗忘，却让 Bielik-11B 在 MoT-PL-eval 与 LightR1 上分别提高 12.3% 与 15.0%[^25]。

压缩数据的构造有三条路线（本文判断）。CoT-Valve 在参数空间中找到可缩放的方向来控制生成长度，为同一道题构造由长到短的多条解[^168]。QwQ-32B-Preview 在 GSM8K 上的链长从 741 降到 225 token，准确率从 95.07% 变为 94.92%[^168]。LLaMA-3.2-1B 学 QwQ 的长链得到 52.69（759.3 token），学 CoT-Valve 压缩后的链得到 55.50（267.0 token）[^168]。但“中等偏短最好”只见于小模型与简单数据集[^168]。第二条路线是自训练：Munkhbat 等人让学生自己做 best-of-N 采样（可辅以简洁示例作少样本条件），每题只保留最短的正确路径[^176]。在 GSM8K 与 MATH 上，组合方法使五个模型族的输出 token 平均减少 30%，平均准确率保持不变[^176]。按题而非全局选最短，是为了保留需要长推理的难题[^176]。直接用外部简洁数据会损失准确率，五个模型在 GSM8K 上用人工 CoT 微调的平均值只有 65.73，零样本基线为 78.06[^176]。第三条路线是剪枝与改写：Lyu 等人分别考察粒度、改写程度与压缩预算[^177]。在 Qwen2.5-7B-Instruct 的短 CoT 设置中，MATH 基线为 75.3，按 token 级 NLL 剪枝（比例 0.7）后跌到 15.8，按步级熵剪枝（同一比例）仍为 74.8[^177]。保持结构的摘要在 0.5 比例下为 76.8，语义融合为 71.7[^177]。长 CoT 学生在简洁监督下仍保留冗长习惯，训练时的压缩率只是部署成本的乐观下界[^177]。ZippingThought 主要在合成算术任务上发现，粒度越粗的压缩 CoT 需要越多 SFT 数据，也比显式 CoT 更受益于数据扩充[^31]。数据有限时，重复训练改善 Composed CoT，却损害 Implicit CoT[^31]。SFT 无法把推理拆得比训练数据的压缩粒度更细，RLVR 则可以[^31]。

长度也是选择中的混淆变量（本文判断）。按长度选择是强基线：Select2Reason 中最长轨迹子集稳定胜过中等与最短子集[^173]。DeGMatch 中按长度选的 10K 条均值为 58.73，高于随机的 55.03，但用了 142.3M token，随机只有 60.3M[^55]。s1 中只取最长轨迹的 1K 子集提高了 GPQA，总体仍不如 s1K[^86]。单纯增加长度并不带来收益：把 Level 1 粒度的链填充到 Level 5 的长度后，Gemma 2B 在 GSM8K 上为 46.62，原链为 47.61，真正的 Level 5 为 52.92[^171]。

“长更好”与“短更好”的分歧主要由两个变量解释（本文推断）。一是学生容量相对于题目难度：最优长度随难度上升、随能力下降，CoT-Valve 的“短更好”在复杂数据集上消失（本文推断，依据见[^167][^168][^71]）。二是长度选择的粒度：全局取最长很可能同时选中了难题，按题取最短则保住了难题（本文推断，依据见[^173][^176]）。

### 8.6 师生适配

在固定题集上比较教师时，强教师可以明显胜出[^180]。Tian 等人在同一批 1.89M 条查询上分别用 AM-Thinking-v1、Qwen3-235B-A22B 与 DeepSeek-R1 蒸馏，每条回答都重采到验证分不低于 0.9[^180]。以 Qwen2.5-32B 基座为学生，三者的 AIME2024 为 84.3、79.4、70.9，AIME2025 为 72.2、62.2、52.8[^180]。胜出的数据并非最长：平均 token 数 Qwen3 为 4196.7，DeepSeek-R1 为 3784.8，AM 为 3757.3，AM 的平均困惑度最低（2.5）[^180]。但该研究对各教师使用不同的困惑度阈值，只训练了一个学生[^180]，AM-Thinking-v1 又出自与作者重叠的团队[^180]。

小模型学生的情形不同（本文判断）。Chen 等人在 4 个教师、7 个学生上发现，更强的教师并不总能教出更好的学生，但更强的学生更能从更强的教师中受益[^171]。Small Models Struggle 称之为小模型可学习性差距，提出混合长短 CoT 或大小教师回答的 Mix Distillation[^71]。Qwen2.5-3B-Instruct 用 Mix-Long 比直接学长 CoT 在 MATH 与 AMC 上高 8 分以上，用 Mix-Large 比只学大教师 CoT 在 MATH、AIME、AMC 上高 7 分以上[^71]。PerSyn 把这一思路细化到每道题，并以上述方法为 Mix 基线[^181]。它用学生对数似然衡量可学性、奖励模型衡量质量，训练路由器为每道题指派教师[^181]。Qwen2.5-3B 在 IFEval、TruthfulQA、LiveBench、GSM8K、MATH、SVAMP 六项上的均值，从单一最强教师的 55.38 升到 58.09，Mix 为 55.39[^181]；Qwen2.5-0.5B 从 28.51 升到 34.13[^181]。超过 95% 的题被路由给较小的教师[^181]，全部使用长 CoT 的最强教师基线则会让学生陷入不终止的重复推理[^181]。

教师选择也可以借助学生侧信号低成本完成（本文判断）。LALP 只需 200 道题就能复现完整 817 题上的教师排序，即 QwQ 优于 DeepSeek-R1、再优于 Qwen3，GALP 给出相反顺序[^6]。RSR 每个教师只抽 200 条轨迹即可选教师[^13]，其按题混合选择在 5 个学生中的 4 个上超过任何单一教师的最好成绩[^13]。

“强教师是否更好”最可能由学生相对教师的规模解释（本文推断，依据见[^171][^180][^181]）。Tian 等人的学生是 32B 基座，PerSyn 的主要学生在 0.5B 到 3B 之间，Small Models Struggle 中长 CoT 的劣势只出现在不超过 3B 的学生上（本文推断，依据见[^180][^181][^71]）。前述过滤阈值未对齐与教师同源的问题，也削弱了 Tian 等人结论的因果解释（本文判断，依据见[^180]）。

### 8.7 小结（本文判断）

- 少量精选的收益真实存在，但常见的“子集胜过全量”比较没有对齐优化步数（依据见[^164][^173][^55]）。在固定更新预算下，Olmo3-7B 重复训练少量数据就能高出 12 至 26 个百分点，底座的预训练知识也决定精选能否奏效（依据见[^18][^72]）。
- 选择信号普遍受长度混淆，形式包括步长、总长度与梯度中的群体级结构，没有长度对照的选择结论应视为弱证据（依据见[^21][^35][^55]）。
- 当错误多为局部事实错误时，答案正确性对轨迹价值的影响小于结构与行为（依据见[^169][^54][^87]）。以答案为条件的生成则会以正确性过滤察觉不到的方式损害数据（依据见[^184]）。
- 最优长度随学生能力与题目难度变化，小模型学生更适合短链或长短混合（依据见[^167][^71][^168]）。压缩数据需要更多样本，训练时的压缩率也不等于推理时的节省（依据见[^31][^177]）。
- 教师选择应以学生为条件：强教师在 32B 学生上占优，不超过 3B 的学生更适合较小或按题路由的教师，学生侧的低成本信号已能完成教师排序（依据见[^180][^181][^6]）。

## 参考来源

[^164]: [Xia et al. — LESS: Selecting Influential Data for Targeted Instruction Tuning (arXiv 2402.04333, 2024-02)](https://arxiv.org/abs/2402.04333)
[^72]: [Ye et al. — LIMO: Less is More for Reasoning (arXiv 2502.03387, 2025-02)](https://arxiv.org/abs/2502.03387v3)
[^86]: [Muennighoff et al. — s1: Simple test-time scaling (arXiv 2501.19393, 2025-01)](https://arxiv.org/abs/2501.19393v3)
[^173]: [Yang et al. — Select2Reason: Efficient Instruction-Tuning Data Selection for Long-CoT Reasoning (arXiv 2505.17266, 2025-05)](https://arxiv.org/abs/2505.17266)
[^174]: [Wen et al. — Light-R1: Curriculum SFT, DPO and RL for Long COT from Scratch and Beyond (arXiv 2503.10460, 2025-03)](https://arxiv.org/abs/2503.10460)
[^175]: [Abdin et al. — Phi-4-reasoning Technical Report (arXiv 2504.21318, 2025-04)](https://arxiv.org/abs/2504.21318)
[^172]: [Wang et al. — Reinforcement Learning for Reasoning in Large Language Models with One Training Example (arXiv 2504.20571, 2025-04)](https://arxiv.org/abs/2504.20571)
[^165]: [Yuan et al. — Scaling Relationship on Learning Mathematical Reasoning with Large Language Models (arXiv 2308.01825, 2023-08)](https://arxiv.org/abs/2308.01825)
[^83]: [Yeo et al. — Demystifying Long Chain-of-Thought Reasoning in LLMs (arXiv 2502.03373, 2025-02)](https://arxiv.org/abs/2502.03373v1)
[^169]: [Li et al. — LLMs Can Easily Learn to Reason from Demonstrations Structure, not content, is what matters! (arXiv 2502.07374, 2025-02)](https://arxiv.org/abs/2502.07374)
[^18]: [Kopiczko et al. — Data Repetition Beats Data Scaling in Long-CoT Supervised Fine-Tuning (arXiv 2602.11149, 2026-02)](https://arxiv.org/abs/2602.11149v2)
[^7]: [Humane et al. — Influence Functions for Efficient Data Selection in Reasoning (arXiv 2510.06108, 2025-10)](https://arxiv.org/abs/2510.06108v2)
[^178]: [Bae et al. — Online Difficulty Filtering for Reasoning Oriented Reinforcement Learning (arXiv 2504.03380, 2025-04)](https://arxiv.org/abs/2504.03380)
[^21]: [Wang et al. — On the Step Length Confounding in LLM Reasoning Data Selection (arXiv 2604.06834, 2026-04)](https://arxiv.org/abs/2604.06834v1)
[^6]: [Just et al. — The Signal is in the Steps: Local Scoring for Reasoning Data Selection (arXiv 2510.03988, 2025-10)](https://arxiv.org/abs/2510.03988v2)
[^26]: [Li et al. — GRACE: Gradient-aligned Reasoning Data Curation for Efficient Post-training (arXiv 2605.13130, 2026-05)](https://arxiv.org/abs/2605.13130v1)
[^55]: [Lee et al. — DeGMatch: Target-Aware Reasoning Data Selection via Deconfounded Gradient Matching (arXiv 2610.24963, 2026-10)](https://arxiv.org/abs/2610.24963v1)
[^28]: [Li et al. — Unified Data Selection for LLM Reasoning (arXiv 2605.22389, 2026-05)](https://arxiv.org/abs/2605.22389v1)
[^35]: [Jin et al. — Reasoning Quality Emerges Early: Data Curation for Reasoning Models (arXiv 2606.26797, 2026-06)](https://arxiv.org/abs/2606.26797v1)
[^13]: [Yang et al. — Which Reasoning Trajectories Teach Students to Reason Better? A Simple Metric of Informative Alignment (arXiv 2601.14249, 2026-01)](https://arxiv.org/abs/2601.14249v5)
[^43]: [Lan et al. — MI-Distillation: Selecting from Model-Interpolated Instruct-Reasoning Data Spectrum for Chain-of-Thought Distillation (arXiv 2608.29623, 2026-08)](https://arxiv.org/abs/2608.29623v1)
[^48]: [Zhang et al. — Selecting Diverse SFT Traces Improves Post-RL Generalization (arXiv 2609.33780, 2026-09)](https://arxiv.org/abs/2609.33780v1)
[^179]: [Chen et al. — On the Diversity of Synthetic Data and its Impact on Training Large Language Models (arXiv 2410.15226, 2024-10)](https://arxiv.org/abs/2410.15226)
[^166]: [Dong et al. — How Abilities in Large Language Models are Affected by Supervised Fine-tuning Data Composition (arXiv 2310.05492, 2023-10)](https://arxiv.org/abs/2310.05492)
[^54]: [Yu et al. — Facts Don't Speak Louder than Words: The Behavioral Essence of Long-CoT Distillation (arXiv 2610.17607, 2026-10)](https://arxiv.org/abs/2610.17607v1)
[^51]: [Huang et al. — Trajectory Soup: Pushing the Compute-Scaling Frontier of LLM Mid-training via Diverse Trajectories (arXiv 2609.37169, 2026-09)](https://arxiv.org/abs/2609.37169v1)
[^170]: [Valmeekam et al. — Beyond Semantics: The Unreasonable Effectiveness of Reasonless Intermediate Tokens (arXiv 2505.13775, 2025-05)](https://arxiv.org/abs/2505.13775)
[^182]: [Bhambri et al. — Do Cognitively Interpretable Reasoning Traces Improve LLM Performance? (arXiv 2508.16695, 2025-08)](https://arxiv.org/abs/2508.16695)
[^12]: [Chandra et al. — Shape of Thought: When Distribution Matters More than Correctness in Reasoning Tasks (arXiv 2512.22255, 2025-12)](https://arxiv.org/abs/2512.22255v2)
[^87]: [Gandhi et al. — Cognitive Behaviors that Enable Self-Improving Reasoners, or, Four Habits of Highly Effective STaRs (arXiv 2503.01307, 2025-03)](https://arxiv.org/abs/2503.01307v2)
[^183]: [Qin et al. — To Backtrack or Not to Backtrack: When Sequential Search Limits Model Reasoning (arXiv 2504.07052, 2025-04)](https://arxiv.org/abs/2504.07052)
[^184]: [Lee et al. — Answer-Conditioned Chains of Thought Degrade Verifiable-Reasoning Distillation in Large Language Models (arXiv 2607.14552, 2026-07)](https://arxiv.org/abs/2607.14552)
[^171]: [Chen et al. — Unveiling the Key Factors for Distilling Chain-of-Thought Reasoning (arXiv 2502.18001, 2025-02)](https://arxiv.org/abs/2502.18001)
[^167]: [Wu et al. — When More is Less: Understanding Chain-of-Thought Length in LLMs (arXiv 2502.07266, 2025-02)](https://arxiv.org/abs/2502.07266)
[^71]: [Li et al. — Small Models Struggle to Learn from Strong Reasoners (arXiv 2502.12143, 2025-02)](https://arxiv.org/abs/2502.12143v3)
[^25]: [Langner et al. — What properties of reasoning supervision are associated with improved downstream model quality? (arXiv 2605.13290, 2026-05)](https://arxiv.org/abs/2605.13290v1)
[^168]: [Ma et al. — CoT-Valve: Length-Compressible Chain-of-Thought Tuning (arXiv 2502.09601, 2025-02)](https://arxiv.org/abs/2502.09601)
[^176]: [Munkhbat et al. — Self-Training Elicits Concise Reasoning in Large Language Models (arXiv 2502.20122, 2025-02)](https://arxiv.org/abs/2502.20122)
[^177]: [Lyu et al. — When Compression Helps and When It Hurts: Condition-Aware Analysis of Chain-of-Thought Distillation (arXiv 2606.21704, 2026-06)](https://arxiv.org/abs/2606.21704)
[^31]: [Matsutani et al. — Zipping the Thought: When and How Compressed Reasoning Data Works in LLM Post-Training (arXiv 2605.28008, 2026-05)](https://arxiv.org/abs/2605.28008v2)
[^180]: [Tian et al. — Not All Correct Answers Are Equal: Why Your Distillation Source Matters (arXiv 2505.14464, 2025-05)](https://arxiv.org/abs/2505.14464)
[^181]: [Zhang et al. — Find Your Optimal Teacher: Personalized Data Synthesis via Router-Guided Multi-Teacher Distillation (arXiv 2510.10925, 2025-10)](https://arxiv.org/abs/2510.10925)
