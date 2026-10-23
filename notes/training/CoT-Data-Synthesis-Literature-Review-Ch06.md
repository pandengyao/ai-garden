# 训练数据中的思维链合成：方法、证据与开放问题 · 第 6 节

中文 | [English](./CoT-Data-Synthesis-Literature-Review-Ch06_en.md)

- **调研日期**: 2026-10-22（证据截止：arXiv 首版日期不晚于 2026-10-22）
- **导航**: [主页面](./CoT-Data-Synthesis-Literature-Review.md)（摘要、第 1–3 节、第 11–13 节与附录） · 上一节：[第 5 节](./CoT-Data-Synthesis-Literature-Review-Ch05.md) · 下一节：[第 7 节](./CoT-Data-Synthesis-Literature-Review-Ch07.md)
- **依据**: 句末的上标数字是引用，对应文末参考来源中的精读文献；每条引用都有从该文献全文逐字摘录、并经脚本与全文核对的原文。标有（本文判断）、（本文推断）或（本文统计）的内容，是本文的综合分析或统计，不是来源原话。

## 6 轨迹生成：教师、自我与搜索

第 5 节讨论训练题从哪里来，本节讨论推理轨迹由谁来写（本文判断）。按监督信号的来源，现有做法可分为五类：更强教师离线写好轨迹，模型自身采样后按答案筛选，树搜索或进化算法在采样之上改进轨迹，强化学习在自身 rollout 中混入教师轨迹，以及 on-policy 蒸馏让学生自己生成、由教师逐词元评分（本文判断）。本节围绕三个问题展开：哪种信号在受控对照下更有效，教师是否越强越好，生成代价与数据效率如何权衡（本文判断）。保留判据见第 7 节，选择与配比见第 8 节，智能体轨迹见第 9 节（本文判断）。表 6-1 把这五类细分为八种做法，汇总其信号来源、保留内容、代价与代表数字（本文统计，各行依据见所标文献）。

表 6-1 推理轨迹生成范式对比

| 范式 | 信号来源 | 保留内容 | 主要代价 | 典型师生 | 代表数字 |
| --- | --- | --- | --- | --- | --- |
| 离线教师蒸馏 | 更强教师写轨迹，按答案与规则过滤[^80] | 答对的教师轨迹[^80] | 离线生成一次，同一份 800k 数据用于多个基座[^80] | DeepSeek-R1→Qwen2.5-32B[^80] | AIME 2024 pass@1：蒸馏 72.6，同基座纯 RL 47.0[^80] |
| 自我生成与拒绝采样 | 自身采样，按答案对错过滤[^151] | RAFT 只留答对样本[^151] | 每轮 1024 题各采 4 个回复[^151] | Qwen2.5-Math-7B-base 自训练[^151] | 三项数学均值：RAFT 52.3，GRPO 56.3[^151] |
| 答案条件生成 | 以标准答案为条件反推 CoT[^52] | 前向一致的 CoT[^52] | 需另训逆向模型[^52] | Qwen3-0.6B 自蒸馏[^52] | Countdown 难题 pass@1：0.08→0.19[^52] |
| 树搜索 | 搜索加价值模型与最终答案[^137] | 正确路径训策略，正负路径训价值头[^137] | 节点扩展与价值评估开销大[^135] | DeepSeekMath-Base-7B 自训练[^137] | MATH：33.2→53.6[^137] |
| 进化式多教师 | 多教师候选池加 LLM 适应度[^8] | 重组与变异后的轨迹[^8] | 多教师反复采样与评估[^8] | 多个教师→Qwen3-8B 等学生[^8] | BioProBench 可用轨迹比例：多教师 0.536，CoT-Evo 0.729[^8] |
| RL 中混入教师轨迹 | 每题 1 条教师轨迹加 7 条自身 rollout[^140] | 教师轨迹经 Math-Verify 过滤，组内按优势计算[^140] | GPU 时间为 SFT+RL 的 59%[^140] | DeepSeek-R1→Qwen2.5-Math-7B[^140] | 六项竞赛均值 50.1，比 on-policy RL 高 4.6[^140] |
| On-policy 蒸馏 | 教师在学生前缀上的逐词元分布[^139] | 学生自生成序列[^139]，无需正确性验证器[^56] | GSM8K 上学生采样开销为固定数据的 1.8 至 2.2 倍[^139] | Qwen3-30B-A3B→Qwen3-4B[^142] | 四项数学均值：SFT 35.1，OPD 42.6，ExOPD 45.3[^142] |
| 特权自蒸馏 | 同一模型看到标准解答后给出逐词元分布[^141] | 学生 rollout，不做正确性验证[^141] | 每题 1 条 1024 token 的 rollout[^141] | Qwen3 系列自蒸馏[^141][^145] | Qwen3-1.7B 学生关思考训练：37.1→43.4[^141]；开思考训练：0.372→0.308[^145] |

### 6.1 离线教师蒸馏与教师选择

**谱系与机制。** 离线教师蒸馏由教师为每道题写出轨迹，过滤后供学生做监督微调（本文判断）。Distilling Step-by-Step 把大模型生成的理由作为多任务框架中的附加监督[^73]。其 770M T5 只用某基准 80% 的数据就超过少样本提示的 540B PaLM，同一 T5 做标准微调用满 100% 数据仍难以追平[^73]。Orca 让 13B 学生学习 GPT-4 的解释轨迹与逐步思考过程，并以 ChatGPT 作教师助手[^67]。它先在 FLAN-5M 的 ChatGPT 回复上训练，再在 FLAN-1M 的 GPT-4 回复上训练[^67]。作者设置中间教师的理由是容量差：13B 学生远小于 GPT-4，能力差距较小的中间教师可改善模仿学习[^67]。

长思维链阶段的离线蒸馏可以 DeepSeek-R1 为例（本文判断）。其推理数据来自第一阶段强化学习检查点的拒绝采样，每题采多条回复、只保留正确者，并滤掉语言混杂、长段落与代码块的思维链[^80]。最终得到约 600k 条推理样本与约 200k 条非推理样本，这 800k 条数据用于对 Qwen2.5 与 Llama 系列基座微调 2–3 个 epoch[^80]。在 AIME 2024 上，DeepSeek-R1-Distill-Qwen-32B 的 pass@1 为 72.6，同一基座直接做超过 10K 步强化学习的 Qwen2.5-32B-Zero 只有 47.0，与 QwQ-32B-Preview 的 50.0 相当[^80]。作者据此认为，小模型做大规模强化学习代价巨大，还可能不及蒸馏[^80]。Qwen3 对 Qwen3-0.6B 至 14B 的稠密模型和 Qwen3-30B-A3B 采用两段式强到弱蒸馏[^70]。第一段合并教师在 /think 与 /no_think 两种模式下的输出做离策略回复蒸馏，第二段由学生生成序列，再把其 logits 与 Qwen3-32B 或 Qwen3-235B-A22B 对齐[^70]。从同一个离策略蒸馏后的 8B 检查点出发、只用数学与代码题时，on-policy 蒸馏把 AIME24 从 55.0 提到 74.4，耗时 1,800 GPU 小时，强化学习只到 67.6，耗时 17,920 GPU 小时[^70]。

**证据：更强的教师未必更好。** RevisitCapacityGap 指出既有容量差研究的协议缺陷，包括没有与蒸馏前的学生比较，以及跨教师过滤只保留所有教师都做对的题，剥夺了强教师独有的正确数据[^22]。在五个数学基准上，以 Qwen2.5-3B-Instruct 与 Qwen2.5-72B-Instruct 等为教师时，多数配置下蒸馏后的学生反而不如蒸馏前[^22]。改用 Qwen2.5-14B-Instruct 与 Qwen2.5-72B-Instruct 作小、大教师，在 15 个 BBH 任务上按实际协议重评，11 个蒸馏有效任务中有 8 个出现容量差效应[^22]。以 Qwen2.5-32B-Instruct 与 QwQ-32B-Preview 作短、长教师时，10 个任务中只有 2 个出现[^22]。跨教师过滤使大教师的数据从 1,928 条减到 1,684 条（−12.7%），小教师只从 1,769 条减到 1,684 条（−4.8%），四种学生规模上的平均准确率分别下降 3.61 与 1.78[^22]。作者据此认为，强教师的优势主要来自更多可用数据，而非更高的 CoT 质量[^22]。

TeacherGRPO 把相反的现象称为 Gap Curse：教师越复杂，其分布越偏离容量有限的学生能近似的范围[^49]。以 Qwen2.5-3B-Instruct 为教师、Qwen2.5-0.5B-Instruct 为学生，在 Date Understanding 上用 KD 把教师向学生对齐 40 步，学生准确率从 30.2% 升到 38.5%[^49]。继续对齐到第 80 步时，教师从 59.2% 跌到 43.8%，学生也跌到 29.0%[^49]。改用以反向 KL 为奖励的 GRPO 对齐，教师在第 80 步仍为 58.5%[^49]。完整的 TeacherGRPO 在 Qwen 与 Gemma 两族上比原始蒸馏方法平均高 7.4 与 3.6 个点[^49]。Strong Teacher Not Needed 在预训练阶段做 logit 级蒸馏，学生为训练 50B token 的 1.7B 模型[^30]。教师均训练 300B token 时，教师越小学生越好，1.7B、3.8B 与 8.0B 教师分别带来 +4.3%、+3.5% 与 +2.8% 的下游提升[^30]。8.0B 教师在 30B token 时收益最高（+4.3%），训练到 300B token 后降到 +2.8%[^30]。Knowledge Distillation During Mid-Training 以 OLMo-2 1B 为学生、1B 至 13B Instruct 为教师，发现前向 KL 蒸馏在中训练阶段减慢事实回忆的习得，而推理仍在改善[^44]。其中 7B 教师一般优于 13B 教师[^44]。按教师预测熵路由、只在教师自信的词元上蒸馏后，7B 教师下的推理宏平均从 NTP 的 26.1% 升到 44.7%，事实回忆为 29.3%，NTP 为 30.3%[^44]。on-policy 蒸馏中也有同类证据：Ask to Distill（A2D）的代码实验以 Qwen3-4B 为学生，4B 教师下的教师差距恢复率为 82.9%，更强的 30B-A3B 教师只有 32.8%[^56]。同一学生用更强教师得到的蒸馏后平均分反而更低[^56]。

**局限与争议。** 这些结论未必矛盾，它们改变的是不同的变量（本文推断）。RevisitCapacityGap 的结论针对候选教师性能差距大的情形，Strong Teacher Not Needed 改变的是教师的参数量与训练 token 数，TeacherGRPO 针对的是小模型间的推理蒸馏（本文推断，依据见[^22][^30][^49]）。RevisitCapacityGap 也承认，候选教师性能接近时容量差的作用可能更大[^22]。教师选择至少取决于候选教师之间的差距、师生容量比与训练阶段（本文判断，依据见[^22][^44][^56]）。RevisitCapacityGap 的实际协议只覆盖 BBH 且多为单次运行，TeacherGRPO 把 7B→1.5B 及更大的师生对留作后续工作[^22][^49]。

### 6.2 自我生成与拒绝采样

**谱系与机制。** 自我生成让待训练模型自己写轨迹，再用最终答案或测试筛选（本文判断）。STaR 让模型按少量示例为大量题目生成理由，答错时在给出正确答案的条件下重写理由，只在最终答对的理由上微调并迭代[^82]。ReST-EM 把同类循环建立在期望最大化框架上：生成样本，按二值反馈过滤，在保留样本上微调，重复数轮[^81]。TRICE 把 CoT 视为隐变量，用 MCMC-EM 从以正确答案为条件的理由后验中采样[^90]。与 STaR 相比，它更少忽略难题，并能利用错误理由[^90]。Inverse Reasoning Models 沿这两条思路训练一个以答案为条件生成 CoT 的逆向模型，用于拒绝采样没有信号的难题[^52]。这一循环在长思维链阶段仍是主流配方的一环（本文判断）。DeepSeek-R1 的约 600k 条推理样本即来自对自身第一阶段 RL 检查点的拒绝采样[^80]。

**证据。** 以 GPT-J 为基座，带重写的 STaR 在 CommonsenseQA 上达到 72.5%，与大 30 倍的微调模型的 73.0% 相当[^82]。在 GSM8K 上，不带重写的 STaR 只用 25.0% 的训练数据就超过了各基线[^82]。ReST-EM 在 PaLM 2 上的 MATH 与 APPS 收益随模型规模增大，并显著超过只用人工数据微调[^81]。TRICE 以 PaLM 2-M 做提示微调，并把它与拒绝采样每次迭代的代价对齐[^90]。在 27 个 BBH 任务的自举初始化下，STaR、拒绝采样与 TRICE 的贪心准确率依次为 62.0、64.6 与 72.8[^90]。在 GSM8K 上，拒绝采样为 77.9，高于自举初始化的 TRICE（74.7），与非自举初始化的 TRICE（77.7）相当，STaR 为 53.5[^90]。作者总体表述为 TRICE 优于拒绝采样，GSM8K 的数字并不支持这一点（本文判断，依据见[^90]）。Xiong 等以 Numina-Math 约 860k 道题为题库，每轮 1024 题、每题 4 个回复，比较拒绝采样与强化学习[^151]。Qwen2.5-Math-7B-base 在 Math500、Minerva 与 OlympiadBench 上的均值为：基座 23.6，只学正样本的 RAFT 52.3，PPO 52.5，RAFT++ 56.1，GRPO 56.3[^151]。消融显示，GRPO 的主要优势来自丢弃全错的题，而非奖励归一化[^151]。逆向模型在 GRPO 已饱和的 Qwen3-0.6B 上做一轮离线蒸馏，使 Countdown 难题的 pass@1 从 0.08 升到 0.19[^52]。在模型从未解出的 17% 新题上，GRPO 的每组 rollout 全错、梯度恒为零，逆向模型却为其中 30% 产出了前向一致的 CoT[^52]。

**局限与争议。** ReST-EM 迭代超过少数几轮后收益递减，作者归因于在少量训练题上过拟合[^81]。只学正样本会使策略熵下降更快，RAFT++ 随后停滞并被 GRPO 反超，作者认为负样本有助于维持探索[^151]。该比较的评测为 4096 token 上限下的 avg@16[^151]。长思维链场景下这一结论是否成立尚无证据（本文判断）。逆向模型只用 NLL 训练时会忽略给定答案，需加对比损失[^52]。作者也承认，逆向模型若只复述答案，同样能通过前向一致性检查[^52]。GSM8K 上它相对拒绝采样的难题 pass@32 增益至多 0.03，高混合比例下 pass@1 还低于拒绝采样与初始模型[^52]。不依赖标准答案的自我验证路线（如 Self-Verified Distillation）见第 7 节（本文判断）。Apriel-Reasoner 在 15B 的 Apriel-Base 上只用公开数据做五个领域的强化学习后训练，16K 输出预算下推理轨迹缩短 30–50%[^20]。但其基座经过含显式推理轨迹的继续预训练与指令微调，作者也把与 DeepSeek-R1-Distill 等蒸馏基线的同基座对照留作后续工作[^20]。它因此不能作为不用教师轨迹的路线优于蒸馏的证据（本文判断）。

### 6.3 搜索与进化生成的轨迹

**谱系与机制。** TS-LLM 把树搜索当作策略改进算子：搜索得到更好的轨迹，再把它们蒸馏回策略，同时训练价值函数[^135]。它用学习的价值函数代替提示 LLM 打分，可处理深度 64 的搜索树[^135]。后续工作改变的主要是从树中保留什么（本文判断）。AlphaMath 只用 GSM8K 与 MATH 的 15k 个问答对，由 DeepSeekMath-Base-7B 结合 Python 解释器与价值头做 MCTS[^137]。每轮每题建 10 棵树，正例每轮 57k 至 59k 条，策略只学正确路径，价值头同时学正负路径[^137]。MCTS-DPO 把同一深度上 Q 值最高与最低的候选步骤配成 DPO 偏好对[^138]。ReST-MCTS\* 用标准答案推断每一步的过程奖励，既作 PRM 训练目标，也作筛选自训练轨迹的依据[^136]。rStar-Math 在 747k 道题上做四轮自进化，每轮每题 16 次 MCTS rollout（首轮限为 8 次），只保留 Python 代码执行成功的节点[^78]。它取答对轨迹中平均 Q 值最高的两条作为 SFT 数据[^78]。O1 Replication Journey 则把搜索树中的错误步骤连同回溯与反思编进长思维链[^91]。CoT-Evo 不在单个模型的采样空间上搜索，而是对 Qwen3-32B-think、DeepSeek-R1 等多个教师的轨迹做新颖度驱动的选择、重组与变异[^8]。其适应度考察答案正确性、连贯性与知识运用[^8]。MIMIC 让语言模型表述推理、由确定性代码执行保证计算，自然语言 CoT 锚定在插桩程序的执行轨迹上[^46]。

**证据。** 在 GSM8K 上，TS-LLM 的 LLaMA2-7B 策略经一轮更新，贪心准确率从 41.4 升到 47.9，拒绝采样基线 RFT-50 与 RFT-100 为 47.0 与 47.5[^135]。AlphaMath 三轮后，贪心解码的 MATH 从 33.2 升到 53.6，仍低于用 776k 条 GPT-4 与人工数据训练的 DeepSeekMath-Instruct 的 57.4[^137]。配合步级束搜索可达 66.3[^137]，超出部分来自推理时搜索（本文判断）。MCTS-DPO 以在 Arithmo（约 540K 道数学与代码题）上 SFT 的 Mistral-7B 为起点，GSM8K 从 75.9 升到 81.8，MATH 从 28.9 升到 34.7[^138]。LLaMA-3-8B-Instruct 经两轮 ReST-MCTS\* 后，MATH、GPQA-Diamond 与 CEval-Hard 的均值从 24.78 升到 29.02，ReST-EM 与 Self-Rewarding 为 26.83 与 27.73[^136]。rStar-Math 的 Qwen2.5-Math-7B 策略模型在 MATH 上的 pass@1 从 58.8 经四轮升到 78.4，高于引导模型的 75.3[^78]。以分别在 Abel 与 PRM800K 上微调的 deepseek-math-7b-base 为基座，用从推理树构造的 327 条长轨迹训练，MATH500 比同一棵树导出的 327 条 shortcut 轨迹高 8.4% 与 8.0%[^91]。CoT-Evo 在 BioProBench 上相对单教师与多教师蒸馏的相对增益为 12.6% 与 8.4%，在 ChemCoTBench 上为 27.0% 与 19.3%[^8]。它也优于每个教师各采 21 条再择优的 Best-of-K，后者的候选数与 CoT-Evo 单题最多产生的轨迹数相同[^8]。在 Qwen3-8B 的题面格式对比中，原始 Codeforces 题面使模型在 38.7% 的情况下转而写代码，MIMIC 的叙事融合题面降到 0.7%，准确率从 23.8% 升到 42.2%[^46]。受控消融中，同以 Qwen3-4B 做 SFT 且测试用例相同，改用原始 Codeforces 题训练比用 MIMIC 数据时通用推理低 16.5 分、数学低 21.6 分[^46]。

**局限与争议。** 搜索方法普遍依赖标准答案（本文判断，依据见[^136][^137][^138]）。MCTS-DPO 引入答案引导后训练信号的准确率从 81.2% 升到 97.9%，去掉后 MATH 为 32.2，与离线变体的 31.9 相近[^138]。ReST-MCTS\* 的增益也有限：LLaMA-3-8B-Instruct 未经训练的少样本提示已达 28.99，Mistral-7B 的 MATH 从第一轮的 31.06 降到第二轮的 24.40[^136]。rStar-Math 称不依赖更强模型的蒸馏，但第一轮用 236B 的 DeepSeek-Coder-V2-Instruct 跑 MCTS 收集 SFT 数据[^78]。其 90.0% 的头条数字还叠加了 64 条测试时搜索轨迹[^78]。只看训练数据的贡献时，应以策略模型的 78.4 为准（本文判断，依据见[^78]）。按代价对齐的证据也不一致（本文判断）。ReST-MCTS\* 报告在相同搜索预算下优于 Best-of-N 与 Tree-of-Thought[^136]。TS-LLM 自己按 token 数对齐的比较却显示，GSM8K 上带 ORM 投票的 CoT-SC 以 500 个 token 得到 52.3，MCTS-α 以 561 个 token 得到 51.9[^135]。在其余四个任务上多数树搜索变体仍占优，作者也承认节点扩展与价值评估的开销使其难以扩展[^135]。最可能的解释变量是任务所需的搜索深度（本文推断）。作者在单路径比较中指出，MCTS-α 与 MCTS-Rollout 在 GSM8K、Game24 与 ProntoQA 等浅层搜索任务上只取得相当的精度，在 RLHF 与国际象棋残局等深层搜索任务上则占优[^135]。TS-LLM 只做了一轮更新，RFT 基线每题采 10 条、取前 5 条，多轮迭代下二者的差距如何变化尚无证据（本文判断，依据见[^135]）。CoT-Evo 的适应度由 LLM 打分，作者承认可能带有偏差[^8]。本节训练实验的学生均不超过 8B（本文统计）。已报告的迭代轮数也少，TS-LLM 一轮，ReST-MCTS\* 两轮，AlphaMath 三轮[^135][^136][^137]。rStar-Math 为四轮[^78]。

### 6.4 强化学习中的离策略引导

**谱系与机制。** LUFFY 认为纯 on-policy 的 RLVR 只能从自身输出中学习，无法获得超出初始能力的推理[^140]。它把教师轨迹放进 rollout 组，每题 1 条 DeepSeek-R1 轨迹加 7 条自身 rollout，自身失败时模仿教师，成功时继续探索[^140]。训练题取自 OpenR1-Math-220k 的 94k 道题，滤去超过 8192 token 或被 Math-Verify 判错的轨迹后剩 45k 道[^140]。为避免熵塌缩与表面模仿，它用正则化重要性采样放大低概率关键动作的学习信号[^140]。Hindsight Hint Distillation（HHD）面向约 100 轮交互的 SWE-bench 任务，只需没有 CoT 的问答对[^24]。它从模型自己的失败 rollout 中提炼一句提示，只在开头注入，整条轨迹仍由模型自己生成[^24]。自身 rollout 与带提示 rollout 中的成功轨迹再汇总起来做 SFT[^24]。

**证据。** 以 Qwen2.5-Math-7B 为学生，LUFFY 在六个竞赛基准上的均值为 50.1，比此前 RLVR 方法高 6.4，比同设置的 on-policy RL 高 4.6[^140]。与先 SFT 再 RL 相比，它在分布内高 1.9、分布外高 16.1，GPU 时间只用 59%（77×8 对 130×8 小时）[^140]。在难题子集上，LLaMA-3.1-8B 的 on-policy RL 训练奖励塌到零，LUFFY 仍稳定提升[^140]。以 Qwen2.5-72B-base 为骨干时，SWE-bench Verified 的 pass@1 依次为：拒绝采样微调 44.0，专家中途接管的 Agent-RLVR-Plan 45.6，逐步专家拒绝采样的 Dense Expert Judge 45.8，HHD 51.2[^24]。把同一提示改在轨迹中途注入的 HHD-M 只有 47.2[^24]。各基线中提供引导的专家为 DeepSeek-V3，它在该基准上弱于 rollout 模型，作者认为这削弱了知识蒸馏带来的混淆[^24]。

**局限与争议。** HHD 作者认为，专家接管迫使模型在自己的前缀上预测专家续写，违背自回归一致性[^24]。离策略基线的 rollout 成功率略高，产出的数据却更难学[^24]。LUFFY 也观察到，直接在教师轨迹上 SFT 会导致表面、僵化的模仿并损害分布外表现[^140]。两项工作对离策略轨迹的态度看似相反，差别在于使用方式：LUFFY 经重要性采样修正后在策略梯度中使用教师轨迹，HHD 的基线把混合来源的轨迹直接用于 SFT（本文推断，依据见[^24][^140]）。此外，LUFFY 的教师强于学生，HHD 的专家弱于学生，交互轮数也从单轮变为约百轮（本文推断，依据见[^24][^140]）。LUFFY 作者说明，实验主要针对 7B 及以下的模型与有标准答案的数学题，每题只用一条教师轨迹[^140]。

### 6.5 On-policy 蒸馏

**谱系与机制。** On-policy 蒸馏（OPD）让学生在自己采样的前缀上接受教师的逐词元监督，训练数据不再是固定的轨迹集合（本文判断）。记学生为 $`\pi_\theta`$、教师为 $`\pi_T`$、教师额外可见的特权上下文为 $`c`$，其目标可写为（本文判断）：

```math
\mathcal{L}(\theta)=\mathbb{E}_{x\sim\mathcal{Q},\;y\sim\pi_\theta(\cdot\mid x)}\Big[\textstyle\sum_{t} D\big(\pi_T(\cdot\mid x,c,y_{<t})\,\big\|\,\pi_\theta(\cdot\mid x,y_{<t})\big)\Big]
```

其中 $`D`$ 可取前向 KL、反向 KL 或 JSD[^141]。$`c=\varnothing`$ 对应普通 OPD，$`c`$ 为最终答案或标准解答时即特权上下文 OPD[^145]。GKD 指出，自回归模型的常规蒸馏存在训练序列与学生推理时生成序列的分布错配，并让学生在自生成序列上接受教师反馈[^139]。G-OPD 与 Rethinking OPD 均把 GKD 作为 OPD 的先行工作引用[^142][^144]。G-OPD 证明 OPD 是奖励项与 KL 项权重恒等的稠密 KL 约束强化学习的特例，奖励缩放因子大于 1 时称为 ExOPD，实验中固定为 1.25[^142]。W2S-OPD 去掉教师至少与学生同等强的前提，用两个比学生小的模型的 logit 差作为能力方向，加到学生自身的基座上构成代理教师[^38]。OPSD 让同一模型兼任师生，教师在提示中看到标准解答，学生只看到题目[^141]。

**证据。** 以 T5-XL 为教师、T5-small/base/large 为学生，on-policy GKD 在摘要、翻译与算术推理上的提升分别是基线 KD 提升的 2.1、1.7 与 1.9 倍[^139]。GSM8K 上只用学生自生成 CoT 的效果好于固定 CoT 数据集或二者混合[^139]。以 Qwen3-30B-A3B-Instruct-2507 为教师（数学均值 59.7），Qwen3-4B-Non-Thinking 的四项数学均值为：基座 15.4，教师轨迹 SFT 35.1，OPD 42.6，ExOPD 45.3[^142]。以非思考模式的 Qwen3-8B 为学生、Qwen3-4B 的 RL 版本与原始版本为正负对，数学均值为 SFT 45.7、OPD 46.5、W2S-OPD 51.8，后者超过 48.8 的 4B-RL 领域教师[^38]。代码均值上 OPD 为 58.7，低于 SFT 的 59.7[^38]。W2S-OPD 需前向三个冻结模型，每步训练时间只比 OPD 多 20%（1043 秒对 868 秒）[^38]。OPCD 把 OPD 用于上下文蒸馏，Qwen3-8B 内化自身轨迹中提炼的经验后，数学准确率为基座 75.0、上下文内 77.6、离策略上下文蒸馏 78.5、OPCD 79.7[^150]。

**失效模式与修正。** Revisiting On-Policy Distillation 一文归纳了按采样词元计算的 OPD 的三类失效：词元级监督失衡，学生前缀漂移后教师引导不可靠，分词器与特殊词元不匹配[^143]。他们改在教师 top-K 支撑集上做截断反向 KL[^143]。以 Qwen2.5-7B-Instruct 为学生、OpenThinker3-7B 为教师，五项数学均值从学生的 28.2 经采样词元 OPD 升到 36.4，局部支撑匹配为 41.7，教师为 56.0[^143]。Rethinking OPD（Li 等）提出 OPD 成功的两个条件：师生思维模式相容，教师具备学生未见过的新能力[^144]。成功的 OPD 表现为学生访问状态上的逐步对齐，共享词元集中了 97%–99% 的概率质量[^144]。把 JustRL-1.5B 反向蒸馏到其 RL 前检查点会抹去全部 RL 收益，换成更大的 R1-Distill-7B 作教师也回落到同一水平[^144]。先用教师的 200K 条回复做 SFT 冷启动、再做 OPD，明显优于纯 OPD[^144]。稠密信号随深度衰减，教师续写学生前缀的准确率优势从 1K 前缀的 +0.37 降到 16K 前缀的 +0.02[^144]。Armandpour 等的免训练诊断显示，在 BoolQ 上蒸馏梯度与理想梯度的平均余弦只有 +0.027（Qwen3-0.6B）与 +0.026（Qwen3-1.7B）[^149]。对齐在错误 rollout 上显著更高，最优教师随学生容量而变[^149]。G-OPD 发现奖励权重增到 1.5 时学生会利用隐式奖励而失稳[^142]。W2S-OPD 观察到，在 IFBench 上普通 OPD 使学生低于其初始化，作者认为学生吸收了小专家的局限[^38]。OPCD 中持续更新的自教师会发散，作者归因于以不断变化的模型作教师带来的高方差[^150]。Sokoban 上自蒸馏为 18.8，冻结的师生配置为 53.9[^150]。OPCD 的检查点按最高测试准确率选取，报告值可能偏乐观（本文推断，依据见[^150]）。

**特权自蒸馏的矛盾。** OPSD 以 OpenThoughts 数学子集中至多 30K 个题目与解答对训练 Qwen3 的后训练版本（作者称指令微调版），教师固定为初始策略，学生关闭思考而教师开启[^141]。Qwen3-1.7B 在 AIME24、AIME25 与 HMMT25 上的 Avg@12 均值从 37.1 升到 43.4，SFT 为 35.8，GRPO 为 37.7[^141]。OPSD 每题只采 1 条 1024 token 的 rollout，100 步内收敛，GRPO 每题需 8 条 16k token 的 rollout[^141]。Kaur 等在思维模型上得到相反结果，五个 Qwen3 与 OLMo 思维模型的 avg@16 全部下降，相对降幅最高 17%[^145]。在 Qwen3-1.7B 思维模型上，以 Qwen3-8B 为教师的普通 OPD 从 0.372 升到 0.392，给教师加金标示范后降到 0.350[^145]。作者据此认为问题出在教师侧的特权上下文，而非 OPD 本身[^145]。损失集中在长预算，32k–38k token 时 OPSD 模型持平或不如基座，回复明显变短[^145]。Kim 等在 DeepSeek-R1-Distill-Qwen-7B 上发现，GRPO 使 AIME24 从 54.7 升到 56.0，以完整解答为条件的 SDPO 却下降约 40%[^146]。以完整解答为条件生成时，得分从 0.30 升到 0.98，平均长度却从 13,054 token 降到 1,873 token，认知标记从 182.5 个降到 8.8 个[^146]。表 6-2 并列三项研究的条件（本文统计，各行依据见所标文献）。

表 6-2 特权上下文自蒸馏的三项研究条件对照

| 研究 | 学生 | 训练时思考模式 | 特权上下文 | 训练设置 | 评测 | 结果 |
| --- | --- | --- | --- | --- | --- | --- |
| OPSD[^141] | Qwen3-1.7B/4B/8B[^141] | 学生关、教师开[^141] | 标准解答[^141] | 1024 token rollout，前向 KL 全词表蒸馏，LoRA，100 步内每 20 步取最佳[^141] | Avg@12，上限 38k[^141] | Qwen3-1.7B：37.1→43.4[^141] |
| Kaur 等[^145] | Qwen3-1.7B/4B/8B、Qwen3-4B-Think-2507、OLMo-7B-Think[^145] | 训练 rollout 开启思考；对照组关闭[^145] | 完整解答[^145] | rollout 上限 4,096 token，JSD，一个 epoch[^145] | avg@16，上限 38,912[^145] | Qwen3-1.7B：0.372→0.308；关思考训练的 Qwen3-4B：0.591→0.590[^145] |
| Kim 等[^146] | Qwen3-8B、DeepSeek-R1-Distill-Qwen-7B 等[^146] | 师生同开或同关[^146] | 完整解答或去掉 think 部分[^146] | 回复上限 20,480 token，JSD，全参数微调[^146] | AIME24、AMC23[^146] | DeepSeek-R1-Distill-Qwen-7B 的 AIME24 约降 40%；复现 OPSD 混合配置时先升后降[^146] |

两项研究的 Qwen3-1.7B 起点几乎相同（37.1 与 0.372），评测都开启思考、生成上限都是 38,912 token，很可能是同一检查点（本文推断，依据见[^141][^145]）。分歧最可能由训练时被监督的 rollout 是否为思考模式解释（本文推断，依据见[^141][^145][^146]）。OPSD 让学生关闭思考生成 rollout，教师开启思考[^141]。Kim 等认为这种混合配置更接近常规的师生蒸馏[^146]。Kaur 等也指出，此前的自蒸馏证据多来自指令微调模型、短生成预算或关闭思考的 rollout[^145]。Kaur 等固定 Qwen3-4B 时，非思考 rollout 训练保持性能（0.591→0.590），思考 rollout 训练则降到 0.532[^145]。关闭思考只保住了性能，并未复现 OPSD 在 Qwen3-4B 上从 61.2 到 63.6 的增益（本文判断，依据见[^141][^145]）。思考模式也不是唯一变量，关闭思考的 Qwen3-8B 在 SDPO 下 AIME24 仍从 0.25 降到 0.23[^146]。散度与检查点选择可能是第二组变量（本文推断）。OPSD 的散度消融以前向 KL 最好，作者此后的实验都采用前向 KL[^141]。同一消融里 JSD 第 50 步只有 36.9，基线为 36.7[^141]。Kaur 等与 Kim 等用的都是 JSD[^145][^146]。Kim 等复现混合配置时，早期性能上升，随后持续下降[^146]。OPSD 报告的则是 100 步内每 20 步评测的最佳检查点[^141]。特权信息的多少与任务覆盖面是另外两个调节变量（本文推断）。只给最终答案作特权上下文时损害较轻，给完整解答时更重[^145]。SDPO 此前奏效的化学数据只来自六种主要题型[^146]。Countdown 训练设置下，OPSD 对指令模型的帮助也比对思维模型更稳定[^145]。Qwen3-4B-Instruct-2507 的四项均值从 0.527 升到 0.559，Qwen3-4B-Think-2507 则从 0.776 降到 0.765[^145]。OPSD 的增益目前只见于学生关闭思考、短训练的设置，监督思考 rollout 时尚无正面证据（本文判断，依据见[^141][^145][^146]）。

**数据效率。** OPD 对题目数量的需求很低（本文判断）。Rethinking OPD II（Fu 等）以 R1-Distill-1.5B 为学生、JustRL-1.5B 为教师，只用一道题训练，第 300 步时 MATH-500、AIME25 与 AMC23 的均值为 68.5，全量 OPD 为 69.8，恢复全量增益的 87%[^147]。单题的状态覆盖率已达 71.5%，16 道语义不同的题达到 98.9% 并与全量训练持平，从未解出的难题同样有效[^147]。作者认为输入只需启动学生的推理，数据设计的重点由此从收集题目转向选择教师[^147]。Hou 等以同一对师生为对象，从 DAPO-Math-17K 中抽 1,000 道题作候选池，六项基准均值上，基座为 42.4，教师为 55.9，8 道难题为 53.6，接近全量 17K 题的 53.7，随机 8 道为 52.1[^148]。师生训练准确率均为零的题仍能提升验证准确率[^148]。作者把难题的收益归因于其诱导的更长 CoT，而非高词元熵[^148]。A2D 进一步用 GRPO 训练出题器，奖励由冻结师生对的分歧与教师在学生 top-K 候选上的概率质量计算，无需参考答案[^56]。在 Qwen3-1.7B、R1-Distill-1.5B 与 R1-Distill-7B 三个学生上，合成题的六项数学均值为 46.2、51.6 与 64.5，用真实题库的普通 OPD 为 43.0、50.5 与 62.9[^56]。作者也说明，其 token 统计未计入出题与打分的上游成本[^56]。

难题是否有信号取决于信号由谁提供（本文推断）。在学生乃至教师从未答对的题上，OPD 仍能提升验证准确率[^147][^148]。这类信号来自教师在学生前缀上的分布，不依赖答对（本文推断）。依赖结果奖励的 on-policy RL 在难题上奖励塌到零[^140]，拒绝采样对从未解出的题也没有信号[^52]。OPSD 作者承认，题目超出模型理解范围时，看得到标准解的自教师也无法提供有效监督[^141]。rollout 长度的结论需按区间理解（本文推断）。Hou 等在 7,168 token 的生成上限内观察到更长 CoT 有益[^148]，Li 等发现最大长度取 10K 与 15K 时持平或下降，并出现后期崩溃[^144]，OPSD 发现 4096 与 1024 相比没有一致改善[^141]。

### 6.6 小结（本文判断）

- 离线教师蒸馏是小模型获得长思维链能力的高性价比途径，同基座蒸馏明显优于纯强化学习，后接 on-policy 蒸馏能以约十分之一的 GPU 时间超过强化学习，依据见[^70][^80]。
- 更强的教师未必更好：候选教师差距大时强者占优，优势多来自可用数据量，教师过大、过度训练或与学生模式不相容时增益下降甚至反转，依据见[^22][^30][^144]。
- 本节的自我生成与搜索方法大多依赖标准答案筛选，只学正样本简单有效但会压缩探索，搜索在按 token 对齐的浅层任务上优势有限，依据见[^135][^138][^151]。
- 离策略教师轨迹的效果取决于用法，在强化学习组内经重要性采样使用有益，朴素 SFT 或中途接管会导致模仿与记忆，依据见[^24][^140]。
- On-policy 蒸馏把数据从轨迹集合变为题目加教师，极少题目即可恢复大部分增益，风险在于长前缀信号衰减、师生不匹配与教师缺乏新知识，依据见[^144][^147][^148]。
- 特权自蒸馏的正面证据局限于学生关闭思考的混合配置与短训练，监督思考 rollout 时思维模型在长预算数学推理上普遍退化，依据见[^141][^145][^146]。

## 参考来源

[^80]: [DeepSeek-AI — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (arXiv 2501.12948, 2025-01)](https://arxiv.org/abs/2501.12948v2)
[^151]: [Xiong et al. — A Minimalist Approach to LLM Reasoning: from Rejection Sampling to Reinforce (arXiv 2504.11343, 2025-04)](https://arxiv.org/abs/2504.11343)
[^52]: [Korman — Inverse Reasoning Models for Efficient Post-Training and Verification from Answer-Only Data (arXiv 2610.18878, 2026-10)](https://arxiv.org/abs/2610.18878v1)
[^137]: [Chen et al. — AlphaMath Almost Zero: Process Supervision without Process (arXiv 2405.03553, 2024-05)](https://arxiv.org/abs/2405.03553)
[^135]: [Feng et al. — Alphazero-like Tree-Search can Guide Large Language Model Decoding and Training (arXiv 2309.17179, 2023-09)](https://arxiv.org/abs/2309.17179)
[^8]: [Feng et al. — CoT-Evo: Evolutionary Distillation of Chain-of-Thought for Scientific Reasoning (arXiv 2510.13166, 2025-10)](https://arxiv.org/abs/2510.13166v2)
[^140]: [Yan et al. — Learning to Reason under Off-Policy Guidance (arXiv 2504.14945, 2025-04)](https://arxiv.org/abs/2504.14945)
[^139]: [Agarwal et al. — On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes (arXiv 2306.13649, 2023-06)](https://arxiv.org/abs/2306.13649)
[^56]: [Sun et al. — Ask to Distill: Learning to Synthesize Data for On-Policy Distillation (arXiv 2610.27450, 2026-10)](https://arxiv.org/abs/2610.27450v1)
[^142]: [Yang et al. — Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation (arXiv 2602.12125, 2026-02)](https://arxiv.org/abs/2602.12125)
[^141]: [Zhao et al. — Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models (arXiv 2601.18734, 2026-01)](https://arxiv.org/abs/2601.18734)
[^145]: [Kaur et al. — Rethinking On-Policy Self-Distillation for Thinking Models (arXiv 2607.05184, 2026-07)](https://arxiv.org/abs/2607.05184)
[^73]: [Hsieh et al. — Distilling Step-by-Step! Outperforming Larger Language Models with Less Training Data and Smaller Model Sizes (arXiv 2305.02301, 2023-05)](https://arxiv.org/abs/2305.02301v2)
[^67]: [Mukherjee et al. — Orca: Progressive Learning from Complex Explanation Traces of GPT-4 (arXiv 2306.02707, 2023-06)](https://arxiv.org/abs/2306.02707v1)
[^70]: [Yang et al. — Qwen3 Technical Report (arXiv 2505.09388, 2025-05)](https://arxiv.org/abs/2505.09388v1)
[^22]: [Kajitsuka et al. — Revisiting the Capacity Gap in Chain-of-Thought Distillation from a Practical Perspective (arXiv 2604.08880, 2026-04)](https://arxiv.org/abs/2604.08880v2)
[^49]: [Lei et al. — TeacherGRPO: Closing the Capacity Gap in Reasoning Distillation via Teacher Alignment (arXiv 2609.33426, 2026-09)](https://arxiv.org/abs/2609.33426v1)
[^30]: [Lu & Liu — Strong Teacher Not Needed? On Distillation in LLM Pretraining (arXiv 2605.23857, 2026-05)](https://arxiv.org/abs/2605.23857v1)
[^44]: [He et al. — Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall (arXiv 2609.01532, 2026-09)](https://arxiv.org/abs/2609.01532v2)
[^82]: [Zelikman et al. — STaR: Bootstrapping Reasoning With Reasoning (arXiv 2203.14465, 2022-03)](https://arxiv.org/abs/2203.14465v2)
[^81]: [Singh et al. — Beyond Human Data: Scaling Self-Training for Problem-Solving with Language Models (arXiv 2312.06585, 2023-12)](https://arxiv.org/abs/2312.06585v4)
[^90]: [Du Phan et al. — Training Chain-of-Thought via Latent-Variable Inference (arXiv 2312.02179, 2023-11)](https://arxiv.org/abs/2312.02179v1)
[^20]: [Pardinas et al. — Apriel-Reasoner: RL Post-Training for General-Purpose and Efficient Reasoning (arXiv 2604.02007, 2026-04)](https://arxiv.org/abs/2604.02007v3)
[^138]: [Xie et al. — Monte Carlo Tree Search Boosts Reasoning via Iterative Preference Learning (arXiv 2405.00451, 2024-05)](https://arxiv.org/abs/2405.00451)
[^136]: [Zhang et al. — ReST-MCTS\*: LLM Self-Training via Process Reward Guided Tree Search (arXiv 2406.03816, 2024-06)](https://arxiv.org/abs/2406.03816)
[^78]: [Guan et al. — rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking (arXiv 2501.04519, 2025-01)](https://arxiv.org/abs/2501.04519v1)
[^91]: [Qin et al. — O1 Replication Journey: A Strategic Progress Report -- Part 1 (arXiv 2410.18982, 2024-10)](https://arxiv.org/abs/2410.18982v1)
[^46]: [Zhang et al. — The Imitation Game: When LLMs Learn to Reason Like Programs via Code-Centric Reasoning Data Synthesis (arXiv 2609.16076, 2026-09)](https://arxiv.org/abs/2609.16076v1)
[^24]: [Wang et al. — Hindsight Hint Distillation: Scaffolded Reasoning for SWE Agents from CoT-free Answers (arXiv 2605.11556, 2026-05)](https://arxiv.org/abs/2605.11556v1)
[^144]: [Li et al. — Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe (arXiv 2604.13016, 2026-04)](https://arxiv.org/abs/2604.13016)
[^38]: [Yu et al. — Weak-to-Strong On-Policy Distillation (arXiv 2607.26246, 2026-07)](https://arxiv.org/abs/2607.26246v2)
[^150]: [Ye et al. — On-Policy Context Distillation for Language Models (arXiv 2602.12275, 2026-02)](https://arxiv.org/abs/2602.12275)
[^143]: [Fu et al. — Revisiting On-Policy Distillation: Empirical Failure Modes and Simple Fixes (arXiv 2603.25562, 2026-03)](https://arxiv.org/abs/2603.25562)
[^149]: [Armandpour et al. — Unmasking On-Policy Distillation: Where It Helps, Where It Hurts, and Why (arXiv 2605.10889, 2026-05)](https://arxiv.org/abs/2605.10889)
[^146]: [Kim et al. — Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? (arXiv 2603.24472, 2026-03)](https://arxiv.org/abs/2603.24472)
[^147]: [Fu et al. — Rethinking On-Policy Distillation of Large Language Models II: One Training Example (arXiv 2609.04172, 2026-09)](https://arxiv.org/abs/2609.04172)
[^148]: [Hou et al. — What Matters in On-Policy Distillation? A Perspective on Data Efficiency and Data Selection (arXiv 2609.05198, 2026-09)](https://arxiv.org/abs/2609.05198)
