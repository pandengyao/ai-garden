# on-policy 蒸馏（OPD）论文调研：2026 年 8–10 月的新论文与 GitHub 论文合集

中文 | [English](./On-Policy-Distillation-Literature-Review_en.md)

- **调研日期**: 2026-11-02（证据截止：arXiv 编号到 2610 为止，最晚一篇提交于 2026-10-30）
- **范围**: 2026 年 8–10 月在 arXiv 首次提交的 on-policy 蒸馏（OPD）论文，以及 GitHub 上整理 OPD 论文的合集仓库。候选 704 篇，逐篇读摘要分类后，满足 OPD 定义的核心论文 540 篇，相关工作 136 篇。
- **结构**: 本页是综述正文；全部 676 篇论文的一句话总结和关键结果在[论文清单](./On-Policy-Distillation-Literature-Review-Papers.md)。
- **依据**: 分类只依据摘要和 comments，没有读全文。文中写到的每篇论文的数字都已对照该论文的 arXiv 摘要核对；篇数统计来自本文对候选论文的分类。

## 结论

1. **方向很热，而且还在加速**。在 704 篇候选里，核心 OPD 论文（满足第 1 节的 C1+C2）有 540 篇：8 月 128 篇，9 月 200 篇，10 月 212 篇。另有 136 篇相关工作，其中 35 篇是用了 OPD 的工业技术报告。
2. **本季度最大的主题是"OPD 到底在起什么作用"，而且多数答案和直觉相反**。数据量方面，1 条 query、4 条 prompt 或 8 条 prompt 就能接近全量数据的效果。监督密度方面，只在 0.05%～1% 的 token 上施加教师监督，效果就能追平全 token。信号来源方面，有一篇论文把教师信号换成固定的负优势，效果相当。知识迁移方面，反向 KL 的 OPD 传的是技能，不是事实。采样方式方面，多数师生对用初始学生离线采样的数据反而更好。合并方面，在受控对比中，多教师 OPD 并不比 SFT 合并更准，训练 GPU 时却是 SFT 的 14.8～23.1 倍。详见第 2 节。
3. **同模型自蒸馏（OPSD）是论文最多的分支，也是受质疑最多的分支**。同一模型拿到参考答案等特权信息后当教师，这一类核心论文有 236 篇，占 44%。同时有十余篇分析论文发现：正确的参考答案并不稳定地带来增益，换成别的题的解也一样有效；OPSD 只在很窄的兼容区间内有效；在多轮智能体任务上，它甚至不如纯 GRPO。详见第 3 节。
4. **OPD 和 RL 的关系基本清楚了**。先做 OPD 再做 RL，效果优于两者联合训练。即使 OPD 当时没有提高准确率，RL 之前做 OPD 也能抬高 RL 的最终上限。联合训练的不稳定来自两种信号的梯度幅度相差悬殊。详见第 5 节。
5. **多教师 OPD（MOPD）已经是工业界合并专家模型的常用做法**，NVIDIA Nemotron 3.5、小米 MiMo-V2.6、AMD Instella-MoE、Motif 3、商汤 SenseNova-U1.5 等技术报告都在用。学术界的新论文集中在三类问题：各领域信号尺度不均、token 预算分配错配、教师路由。另一方面，也有论文证明同一 basin 内的 MOPD 在二阶近似下就是 Fisher 合并，还有论文给出完全不用训练的闭式解。详见第 4 节。
6. **GitHub 上有三个大而活跃的合集**：chrisliu298、thinkwee、nick7nlp。但它们对近三个月论文的覆盖重叠很小，而且都还没收 10 月中下旬的论文。本次评为重要度 3 的 75 篇核心论文里，有 23 篇不在任何合集中。详见第 8 节。

## 1 范围与方法

**判定标准**沿用 thinkwee/AwesomeOPD 的定义。一篇论文要算 OPD，必须同时满足两条：

- C1：训练时由学生从自己当前的策略采样轨迹；
- C2：教师对这些学生轨迹给出监督，形式可以是逐 token 的 logits / log-prob / KL、序列级奖励、判别器打分或口头反馈。

OPSD 是 OPD 的特例：教师和学生是同一个模型，但教师额外拿到特权上下文（参考答案、反馈、提示、更长的上下文等）。

**候选池（704 篇）** 由两部分组成：

- arXiv 全文检索 6 组关键词：`"on-policy distillation"`、`"on-policy self-distillation"`、`"self-distillation" AND "on-policy"`、`"OPD" AND distillation`、`"on-policy" AND "distill"`、`"self-distillation" AND privileged`。取 2608 以后的结果。
- 8 个 GitHub 合集里 2608 以后的条目。其中 41 篇关键词检索搜不到，是靠合集补进来的。

11 月 2 日又重跑了一遍检索，补进 10 月 30 日的 2 篇。被关键词过滤掉的 296 篇也用关键词复查过，没有发现 OPD 论文。

**分类**：逐篇阅读摘要和 comments，标注相关性（核心 / 相关 / 无关）、方法方向、领域、教师类型、重要度（1–3）和一句话总结。完整结果见[论文清单](./On-Policy-Distillation-Literature-Review-Papers.md)。

**局限**：

- 分类只依据摘要。小米 MiMo-V2.6 技术报告的摘要没提 OPD，但 thinkwee 和 kissshhot 两个合集都根据正文把它收为 MOPD 实践，本文据此改判为相关工作。
- 两篇已撤稿的论文保留在清单里，但本文不引用：2608.04408（v2/v3 撤回，comments 栏写着 "false information"）和 2609.38777（模板错误，作者计划重投）。
- 重要度是主观判断。

## 2 机制分析：OPD 到底在做什么

本季度共有 71 篇论文以分析或理论为主要贡献，另有 48 篇带分析标签。其中最集中的是对常见假设的证伪和修正。

### 2.1 数据：需要的 prompt 极少

| 论文 | 发现 |
| --- | --- |
| [2609.04172](https://arxiv.org/abs/2609.04172) Rethinking OPD II: One Training Example | 只用 1 条 query 就能回收全量数据 OPD 的大部分收益。按语义簇度量，单条 query 在第 300 步已覆盖全量数据状态空间的 71.5%；换成 16 条语义不同的 query，覆盖率达到 98.9%，效果追平全量。作者的解释是：OPD 的数据量远远过剩，真正受限的是算法吸收的速度。本仓库有这篇论文的[全文翻译](./One-Shot-On-Policy-Distillation.md) |
| [2609.14193](https://arxiv.org/abs/2609.14193) Data-Free OPD | 8 条真实 prompt 的效果约等于 17k 道题；完全不用种子样例、只用 64 条自生成的问题，就能匹配全量 OPD。多教师设定下，1k 条生成问题约等于 7k 条真实后训练样本 |
| [2609.37377](https://arxiv.org/abs/2609.37377) Beyond Prompt Count | 4 条 DAPO prompt 的数学分数就能追平 3840 条 DeepMath prompt。不过 prompt 有没有用取决于具体的教师，只换教师就可能让数学 prompt 和代码 prompt 的相对效果对调。定向挑选 prompt 也不比均匀随机采样稳定地更好 |
| [2608.16647](https://arxiv.org/abs/2608.16647) Every Coin Has Two Sides | 训练题的难度几乎不影响结果，连教师自己都解不出的题也有用。OPD 传递的是推理行为，不是具体答案。迁移的强弱取决于师生是否同源：同源时可以跨语言、跨领域接近教师，不同源时主要只拟合训练分布 |

### 2.2 监督密度：极少数 token 就够

- [2609.04565](https://arxiv.org/abs/2609.04565) Extremely Sparse Supervision：每条推理轨迹只监督 1～2 个 token（约占全部 token 的 0.05%），多数情况下就能追平甚至超过全 token 训练。这个结论在 9 组师生配置上成立。
- [2609.24432](https://arxiv.org/abs/2609.24432) 1% of Tokens Can Be Enough：从梯度估计噪声的角度挑选 token，用的指标是信噪比式的信息效率比（IER）。在 0.1%～1% 的 token 预算下，就能匹配或超过不做 token 选择的全量 OPD。
- [2609.33791](https://arxiv.org/abs/2609.33791) Do We Really Need KL Divergence?：OPD 不一定要用 KL。只给每个 token 打 ±1，即教师概率比学生高就给 +1、低就给 −1，就能复现反向 KL OPD 的训练模式。真正起决定作用的，是少数师生分歧大的 token 是否朝着教师的方向更新。
- 反面提醒：[2609.22109](https://arxiv.org/abs/2609.22109) 指出，比较 token 选择器时如果共用同一个学习率，选择器与学习率会纠缠在一起。在 LoRA + GSM8K 的设置下，稠密与稀疏监督的差距在学习率 1e-4 时是 10.1 个百分点，在 5e-5 时只有 5.1 个百分点；选择器之间的 6 组两两显著性结论里，有 2 组会在相邻学习率之间翻转。

### 2.3 信号来源：教师到底贡献了什么

- [2608.31046](https://arxiv.org/abs/2608.31046) Does OPD Really Distill?：教师监督的噪声相当大，而且教师越大噪声越多，学生却对这些噪声不敏感。OPD 的收益主要来自压低学生的低概率 token。用一个固定的负优势替代教师给出的优势，效果相当。据此提出的免监督方法 OPSA，在 AIME24 上的 Avg@32 比基座高 35.41 点，比 OPD 高 16.77 点。
- [2610.03185](https://arxiv.org/abs/2610.03185) Gains and Collapse：从 RL 视角看，教师相当于一个隐式奖励模型。OPD 能让正确回答更容易被采样到，但不会扩展学生的能力边界；隐式奖励和质量错位时，就会放大冗长、重复的回答，相当于奖励劫持。
- [2610.03529](https://arxiv.org/abs/2610.03529) Divergence controls entropy：证明前向 KL 会把学生熵抬到教师之上，反向 KL 会压低熵。所以 OPD 学生熵低，原因是逐 token 的反向 KL，而不是 on-policy 采样本身。
- [2610.09639](https://arxiv.org/abs/2610.09639) OPD Teaches New Skills but Not New Knowledge：在受控的合成任务上，反向 KL 的 OPD 能稳定迁移组合技能，但几乎不迁移事实知识；换成前向 KL，事实迁移就能恢复。
- [2610.39020](https://arxiv.org/abs/2610.39020) Distilling the Shape of Uncertainty：OPD 不仅教学生考虑哪些候选 token，还教它在哪些位置让推理路径保持开放。作者用逐 token 的熵序列来刻画后者，干预实验证明它对 OPD 的增益有因果作用。蒸馏前测出的熵形状相关度（ESC）能为两个学生都选出最佳教师。
- [2609.35210](https://arxiv.org/abs/2609.35210) 用稀疏 crosscoder 做的机制可解释性分析：OPD 既不创造新特征，也不搬运教师的特征。学生常用特征中，超过 98% 的发放率变化在 20% 以内。
- [2610.13205](https://arxiv.org/abs/2610.13205)：更强的专家不一定是更好的教师。由任务训练（RL / SFT）引起的策略差异可以稳定迁移，单纯由规模带来的差异几乎不迁移。

### 2.4 on-policy 采样是否必要

- [2610.11291](https://arxiv.org/abs/2610.11291) When Do We Need OPD?：用初始学生离线采样一次的 Semi-OPD，在 17 组师生对（1.5B～235B）里有 14 组优于 OPD，准确率最多高 13.6%，训练最多快 11.4 倍。只有当师生的输出 token 重叠率很高时，OPD 才真的划算。原因是：对错位的师生对来说，学生轨迹越往后越偏离教师，蒸馏信号随之变弱。
- [2609.35259](https://arxiv.org/abs/2609.35259) On-Policy or Off-Policy?：在受控实验里分别改变 rollout 策略、KL 方向和学习率。结果是 rollout 策略并不起核心作用：前向 KL 对 rollout 策略很稳健，只有反向 KL 才偏好学生自采样；学习率决定遗忘程度和更新的稀疏度。
- [2610.33740](https://arxiv.org/abs/2610.33740)：从分布匹配的角度给出理论解释：模型离目标分布近时 OPD 占优，离得远时反而吃亏。
- [2610.30844](https://arxiv.org/abs/2610.30844)：反向 KL 蒸馏的样本复杂度。在线设置下如果只能观测采样动作的概率，可能需要多得多的数据；离线设置下，两种反馈方式所需的数据量同阶。

### 2.5 失败模式

| 现象 | 论文 | 要点 |
| --- | --- | --- |
| 长度膨胀 | [2609.20511](https://arxiv.org/abs/2609.20511) When EOS Tokens Disagree | 基座学生和后训练教师把停止概率放在不同的 EOS token 上。OPD 会压制学生偏好的终止 token，却没有把教师偏好的那个转移过去。只对齐解码时的停止集合不够，要把功能等价的 EOS token 视为同一个语义上的停止动作 |
| 小模型学不会"何时停止" | [2609.37326](https://arxiv.org/abs/2609.37326) Solving Without Stopping | 解题能力能传过去，但思考模式下"何时结束推理"传不过去：教师几乎只在学生本来就会停的地方发出停止信号。另外，学生单次作答的上限不超过它训练前多次尝试能达到的水平 |
| 在学生做错的题上失效 | [2610.18011](https://arxiv.org/abs/2610.18011) Correcting or Continuing? | 只在学生当前做错的题上训练时，8 种配置全部下降（双边符号检验 p=0.0078），训练 KL 却还在下降；不集中在失败题上时，同一套流程能提升 4.6 个百分点 |
| 学习信号提前消失 | [2610.11247](https://arxiv.org/abs/2610.11247) | 训练 200 步后，大教师 OPD 的损失只降了 25.1%，self-RL 教师则降了 96.2%。学生表示几乎不变（各层线性 CKA 都高于 0.98） |
| 退化一致性 | [2608.09836](https://arxiv.org/abs/2608.09836) Mismatch Matters | 学生靠重复循环就能和教师达到接近完美的 token 一致性。作者改为处理两类失配：学生多生成了教师认为不该出现的 token，以及教师偏好的 token 学生却很少采到 |
| 多样性丢失 | [2608.29846](https://arxiv.org/abs/2608.29846) IDA-OPD、[2608.11829](https://arxiv.org/abs/2608.11829) | 采样 token 版 OPD 会出现 pass@1 上涨而 pass@k 停滞的情况；小采样预算下提升，大预算下 pass@K 反而可能下降。后者提出 TAS@K，可以在训练前挑选教师 |
| 收益依赖流水线顺序 | [2609.31900](https://arxiv.org/abs/2609.31900) | OPD 的效果取决于师生兼容性，而不只是教师规模。先用 RLVR 把学生练强，再从同一个教师蒸馏，结果会退步；反过来，用 RLVR 适配教师、再给学生做 SFT 预热，平均准确率能从 29.2% 升到 43.8% |
| 预热阶段 | [2608.06802](https://arxiv.org/abs/2608.06802) Simple-OPD | 预热主要传的是与教师兼容的思维模式：用错误的教师 rollout 做预热，效果和用正确的差不多；用 LoRA 训练到接近饱和，效果优于全参 SFT |

### 2.6 规模规律

[2609.32722](https://arxiv.org/abs/2609.32722) Scaling Properties of Same-Family OPD：训练早期，准确率随反向 KL 的平方根近似线性上升。所有弱到强的配对里，学生的峰值都超过了教师。在分数相同的前提下，小教师迁移得更好，所以教师分数本身并不能代表它的监督价值。作者还拟合出峰值随师生参数量变化的幂律。

## 3 同模型自蒸馏（OPSD）：数量最多，争议最大

### 3.1 质疑特权信息的分析

| 论文 | 结论 |
| --- | --- |
| [2608.18271](https://arxiv.org/abs/2608.18271) Rethinking PI in OPSD | 正确参考答案的收益不稳定；在几个数学基准上，换成别的题的解反而更好 |
| [2608.09228](https://arxiv.org/abs/2608.09228) OP²SD | 把参考解换成另一道题的题目和解，其余设置不变，效果仍和 OPSD 相当。说明起作用的主要是参考解改变了教师所处的上下文，而不是答案本身 |
| [2609.20612](https://arxiv.org/abs/2609.20612) What Does PI Add? | 无参考蒸馏已经能解释 Qwen3-1.7B 的大部分提升；把直接作答的 rollout 换成长思考 rollout 后，收益变成了损失 |
| [2608.04794](https://arxiv.org/abs/2608.04794) Privileged, but Biased | 在难任务上，逐 token 损失持续下降，验证准确率却不升反降。原因是教师的目标被拉向那一条特定的参考轨迹 |
| [2608.09263](https://arxiv.org/abs/2608.09263) | 特权似然回答的问题是"上下文变丰富后预测会怎么变"，而不是"换一个 token 后期望结果会怎么变"。在 AIME 2025 上，这个分数区分对错 rollout 的能力接近随机（AUC 0.505） |
| [2609.39118](https://arxiv.org/abs/2609.39118) Diagnosing OPSD | 在 0.6B～8B 模型上，OPSD 只在很窄的兼容区间内有效；超出这个区间，就会出现无效的长度增长、稳定退化甚至行为崩溃 |
| [2610.18613](https://arxiv.org/abs/2610.18613) Does self-distillation improve reasoning? | 复核 SDPO 和 OPSD 在代码、科学、工具、数学上的表现：收益大多可以用过拟合或已有推理行为的迁移来解释，自蒸馏梯度和策略梯度的方向也只是弱对齐 |
| [2610.13744](https://arxiv.org/abs/2610.13744)（NeurIPS 2026 FLLMPT workshop oral） | 只打分的特权教师既不能定位错误，也不会压低错误 token。让教师先写一段批评、再据此打分，信号才能定位并纠正错误 |
| [2609.29051](https://arxiv.org/abs/2609.29051) From Self-Distillation to Self-Practice | 在多轮智能体上，OPSD 教出来的学生会表现得好像自己拥有从未见过的特权信息，效果低于纯 RL，最坏时低于未训练的基座。改法是把特权指令放进采样阶段，损失函数仍用原版 GRPO；在 AppWorld 和 SWE-bench Verified 上相对 GRPO 提升 7%～58% |
| [2608.25936](https://arxiv.org/abs/2608.25936) One Symptom, Three Levers | 一篇综述：把"坍缩"看成一个症状，由三个杠杆决定——信号加在哪些 token 上、教师能看到什么、引导强度随时间怎么衰减 |

相关工作 [2610.05872](https://arxiv.org/abs/2610.05872) 在持续学习场景里，用 off-policy 的权重嫁接方法赢过了 OPSD。

### 3.2 改进方向：改教师看到的内容

- **少给一点**：[2609.25623](https://arxiv.org/abs/2609.25623) 发现，只给"策略名称""方法无关的框架"这类中间抽象，比给完整参考解高 1.4～1.6 点，而提示的 token 数少一个数量级。[2609.32201](https://arxiv.org/abs/2609.32201) 把逐题标准答案换成针对学生常见错误写的几句通用指令，8 组实验里有 7 组的分布外准确率高 4～17 点。
- **换成软特权**：[2608.02948](https://arxiv.org/abs/2608.02948) 用评分量表（rubric）作为特权信息，把 OPSD 扩展到开放式生成，效果优于把 rubric 当奖励的 RL。
- **完全不要特权**：[2608.06296](https://arxiv.org/abs/2608.06296) U-OPSD 用多数投票得到伪解，Qwen3 4B 和 8B 比基座分别提升 8.5% 和 10.7%。[2608.27448](https://arxiv.org/abs/2608.27448) TTPO 做无标签的测试时训练：与投票一致的 rollout 走 OPSD，不一致的用分组 RL 惩罚，效果追平有标签的 OPSD。[2610.22080](https://arxiv.org/abs/2610.22080) SRD 从未经验证的同伴解里提取监督，Qwen3-8B 在 AIME24～26 上的 avg@12 从 21.39 升到 54.44。[2610.38681](https://arxiv.org/abs/2610.38681) WISD 用量化或剪枝造一个更弱的自身副本来做对比，Qwen3.5-4B 在 HMMT 2025 上从 57.7% 升到 70.5%。
- **削弱学生而不是增强教师**：[2608.14144](https://arxiv.org/abs/2608.14144) 在视觉任务里让教师看原图、学生看强增强后的视图，恢复了特权方法 96% 的收益。
- **让教师适应学生**：[2610.10447](https://arxiv.org/abs/2610.10447) JOLT 推导出特权教师的蒸馏更新是学生奖励梯度正倍数的充要条件，并据此联合训练教师角色和学生角色。[2608.01735](https://arxiv.org/abs/2608.01735) DAPD 针对"特权幻觉"（学生学会依赖推理时并不存在的特权信息）做双向锚定。

## 4 多教师 OPD（MOPD）与能力合并

MOPD 的做法是：先用 RL 训出若干领域专家，再让一个学生在自己的轨迹上接受各领域专家的逐 token 监督。

**工业实践**：在 35 篇使用了 OPD 的技术报告里，有 21 篇用 OPD 合并多个专家，而且这一步通常排在后训练的最后。代表有：

- [2610.38095](https://arxiv.org/abs/2610.38095) NVIDIA Nemotron 3.5 Super：专门训练教师后再做 MOPD；在 SWE-bench Pro 上达到 51.78%，激活参数只有 Nemotron 3 Ultra 的约 1/4.6，成绩却超过了它。
- [2610.11959](https://arxiv.org/abs/2610.11959) 小米 MiMo-V2.6：MOPD2，即多前缀多教师 OPD（据 thinkwee 与 kissshhot 两个合集对正文的摘录）。
- [2608.09119](https://arxiv.org/abs/2608.09119) Motif 3：6 个用 RL 训练的专家教师，加 1 个用 SFT 训练的软件工程教师。
- [2609.00791](https://arxiv.org/abs/2609.00791) AMD Instella-MoE。
- [2609.11929](https://arxiv.org/abs/2609.11929) 商汤 SenseNova-U1.5：统一多模态模型。
- [2609.23377](https://arxiv.org/abs/2609.23377) 阿里巴巴的 SWE 智能体：在 SWE-bench Pro V2 上达到 86.19%。

完整列表见[论文清单](./On-Policy-Distillation-Literature-Review-Papers.md)的"技术报告"一节。

**已知问题与修复**：

| 问题 | 论文 | 做法与结果 |
| --- | --- | --- |
| 各领域信号尺度不均 | [2609.35347](https://arxiv.org/abs/2609.35347) DN-MOPD | 指令遵循的反馈比数学分散好几倍，主导了更新方向。按实测离散度给每个领域归一化后，6 个基准、3 种规模上都优于 MOPD |
| token 预算错配 | [2608.19098](https://arxiv.org/abs/2608.19098) Open-MOPD | 标准 MOPD 只拿到 35.6% 的提升空间，原因不是梯度冲突，而是 token 预算分配错误。修正后提升到 83.4%，完整训练配方已开源 |
| 领域调度 | [2608.24987](https://arxiv.org/abs/2608.24987) D³-MOPD | 复用训练中已有的反向 KL 信号，在线调整各领域的采样比例。师生差距闭合 97%（原版 63%），rollout 步数约减少 3 倍 |
| 教师路由 | [2609.30837](https://arxiv.org/abs/2609.30837) MOPD-Router、[2610.13521](https://arxiv.org/abs/2610.13521) | 按 token 在整个教师池里选教师，或让非路由教师充当跨域评审 |
| 传什么 | [2610.10460](https://arxiv.org/abs/2610.10460) Δ-MOPD、[2609.14708](https://arxiv.org/abs/2609.14708) | 不传教师的最终策略，只传教师相对其后训练前模型的偏移 |
| 任务干扰 | [2609.34605](https://arxiv.org/abs/2609.34605) PMOPD | 各任务的参数更新会集中到各自的低维子空间，把干扰受保护子空间的梯度投影掉 |

**对 MOPD 必要性的质疑**：

- [2610.04272](https://arxiv.org/abs/2610.04272)：在同基座的受控实验里，SFT、软标签、教师前缀混合、MOPD 四种方法的准确率几乎相同，但 MOPD 的训练 GPU 时是 SFT 的 14.8～23.1 倍。用拒绝采样数据训练 SFT 基线后，已发表论文里的 on-policy 增益大幅缩水。
- [2610.26525](https://arxiv.org/abs/2610.26525)：同一 basin 内，MOPD 的目标在二阶近似下就是 Fisher 合并。只做第一步的闭式合并，效果就能匹配或超过完整的多教师蒸馏。
- [2610.22236](https://arxiv.org/abs/2610.22236) Training-Free OPD：各专家共享基座时，蒸馏有逐层的最小二乘闭式解，只需要几百条 rollout 的前向传播。
- [2609.39405](https://arxiv.org/abs/2609.39405)：OPD 产生的任务向量与 RL 任务向量合并后可以超过两者；跨任务合并时，8 组对比里有 7 组优于 RL 任务向量的合并。

## 5 OPD 与 RL 的组合

- **先后顺序**：[2609.04108](https://arxiv.org/abs/2609.04108) Sequential Beats Joint 发现，先 OPD 后 RL 稳定优于纯 OPD、纯 RLVR 和各种联合方案。解释是 OPD 扩大学生对教师所支持解法的覆盖，RL 再在这个范围内收紧；两者联合训练会互相干扰。什么时候切换到 RL，以 OPD 的验证分数为准。
- **OPD 作为 RL 的前置**：[2609.28145](https://arxiv.org/abs/2609.28145) RL Starts before RL 发现，用 OPD 初始化的学生，最终 RL 表现超过直接 RL 和 SFT+RL；即使 OPD 当时几乎没有提高准确率，这个优势也存在。反向 KL 在 RL 之前更好，RL 之后被前向 KL 反超；两种目标下，学生 rollout 都优于教师 rollout。
- **联合训练为什么不稳**：[2609.34849](https://arxiv.org/abs/2609.34849) 用 NTK 分析发现，奖励梯度可能比蒸馏梯度大好几个数量级，同一个 token 上还可能出现方向冲突；两者的梯度范数比超过某个经验阈值后，简单混合可能导致训练持续崩溃。
- **融合做法**：[2608.24696](https://arxiv.org/abs/2608.24696) OPDVR 按轨迹是否正确，用 ReLU 给隐式奖励加门控，把 OPD 变成一种 RLVR 方法。[2609.32674](https://arxiv.org/abs/2609.32674) 发现成功轨迹上学生自己的动作更有益，失败轨迹上换成教师动作更有益，于是在成功轨迹上做强化、在失败轨迹上做蒸馏。[2610.40576](https://arxiv.org/abs/2610.40576) PIVOT 把教师纠正插进学生 rollout，并对这些片段施加 KL；在困难逻辑游戏上，avg@8 从最佳基线的 19.5% 升到 35.6%。[2609.08798](https://arxiv.org/abs/2609.08798) OPRD 只用弱教师的偏移方向去放大验证器梯度，学生可以超过教师。

## 6 目标函数、教师侧与 rollout 侧改进

这三类方法论文共有 200 篇（按第一个标签计），这里只列出摘要里报告了较大提升的几篇。

- **token 加权**：[2609.38025](https://arxiv.org/abs/2609.38025) Dr. OPD 把每个 token 的权重当作双层优化变量，权重有闭式更新。在强到弱设置下，数学平均分比原版 OPD 高 9.7 点，较小的学生能反超较大的教师。
- **教师续写**：[2608.16333](https://arxiv.org/abs/2608.16333) 让教师从学生轨迹的中间状态续写出完整的修复路径；在 ALFWorld 上比原版 OPD 高 13.4 点。[2609.22254](https://arxiv.org/abs/2609.22254) AC-OPD 自适应地选择教师续写的长度。[2610.27467](https://arxiv.org/abs/2610.27467) 对学生失败的尝试做最小编辑，得到正确目标；用不针对学生的标准解替换后，保持度从 0.916 降到 0.744。
- **rollout 提案**：[2610.36477](https://arxiv.org/abs/2610.36477) MPOPD 用学生和教师的几何混合分布来生成 rollout。在 16 个基准上一致优于 OPD，数学平均准确率高 6.91，生成长度减少 41%。[2610.07874](https://arxiv.org/abs/2610.07874) 在 rollout 里混入一个更弱的负策略，让学生得到显式的负向信号。
- **分支**：[2610.13481](https://arxiv.org/abs/2610.13481) BranchOPD 在学生不确定或师生分歧大的决策点，从共享前缀重新采样出分支。数学 avg@16 比原版 OPD 高 18.55 点，ALFWorld 高 13.8 点。
- **省算力**：[2610.21337](https://arxiv.org/abs/2610.21337) STOPD 随机截断 rollout，再用逆概率加权保持期望梯度不变；生成 token 减少 25%～48%，训练快 1.3～2.2 倍。[2609.35505](https://arxiv.org/abs/2609.35505) LSPD 的完全 off-policy 变体只用前 25% 的 rollout 批次就能媲美 OPD。
- **把整个分布蒸进去**：[2610.06804](https://arxiv.org/abs/2610.06804) OPPD 把序列级幂分布的锐化效果蒸进单次生成。MATH500 提升 23.0 点，比同预算的 GRPO 高 3.8～5.4 点，接在 GRPO 之后还能再加 9.3 点。

## 7 应用领域

核心论文的领域分布：通用 LLM 271、智能体 99、多模态理解 63、生成 29、其他应用 26、安全与隐私 18、具身 13、扩散语言模型 10、量化与剪枝 10、投机解码 1。

**智能体（99 篇）**。多轮交互里，一个错误动作会改变之后遇到的所有状态，问题和单轮推理不同。

- [2609.40285](https://arxiv.org/abs/2609.40285) PivotOPD（NVIDIA）：超过一半的失败轨迹里有一个早期的关键错误，而且通常还能挽回。在这一步用反向 KL 教正确动作，在随后几轮用前向 KL 教恢复动作；ALFWorld +5.5%，SWE-Bench Verified +3.2%。
- [2610.25034](https://arxiv.org/abs/2610.25034) 发现"蒸馏过冲"：学生先超过教师，随后又回落。SPOD 屏蔽掉与学生成功选择冲突的教师监督后，最高能超过教师 20.0 点。
- [2610.28586](https://arxiv.org/abs/2610.28586)：问题不只是误差累积，而是教师逐 token 打分太"近视"。先修复教师打分器再做 OPD，12 个组合全部胜出，平均高 12.8 个成功点。
- [2610.31918](https://arxiv.org/abs/2610.31918)：把 on-policy 拆成"交互历史"和"当前动作前缀"两层。学生的历史配上教师的动作前缀，信号最强；两层都跟随学生，反而最差。
- [2610.19820](https://arxiv.org/abs/2610.19820) ActionOPD：在语义动作的粒度上蒸馏黑盒教师，不要求师生同族或同词表。
- [2610.08077](https://arxiv.org/abs/2610.08077)：把事后的经验蒸成行动前的预判。在 2B 模型、98% 的组全部失败的情况下，RLVR 只有 0% 的成功率，加上这种蒸馏后达到 60.6%。

**多模态与生成**。[2610.20989](https://arxiv.org/abs/2610.20989) 在 VLM 上发现，只有当教师在学生轨迹上保持可靠时，OPD 才有效：ChartQA 上用 10% 的数据就接近全量 SFT，Geometry3K 上却落后 7.9 点，主要因为回答没有完成。扩散和 flow 模型方面，跨模型族的 [2608.03316](https://arxiv.org/abs/2608.03316) Any-OPD 在冻结的视觉表征空间里对齐教师和学生；[2608.24646](https://arxiv.org/abs/2608.24646) 在 20 组设置里有 19 组最优，训练 GPU 时比 DiffusionNFT 少 40%～63%。

**架构迁移与压缩**：

- [2609.31947](https://arxiv.org/abs/2609.31947) 注意力线性化：只用 3B 训练 token，大海捞针检索就恢复到 100%。
- [2609.26708](https://arxiv.org/abs/2609.26708) 3 比特以下量化：MATH-500 的保持率从 35% 升到 70%。
- 自回归模型蒸到扩散语言模型：[2609.35362](https://arxiv.org/abs/2609.35362) d-OPD、[2610.17397](https://arxiv.org/abs/2610.17397) JustOPD。
- 跨 tokenizer：[2610.08448](https://arxiv.org/abs/2610.08448) 发现严格 1:1 对齐的位置已经覆盖了大部分 token；[2609.10154](https://arxiv.org/abs/2609.10154) 发现跨模型族 OPD 即使对齐了 tokenizer 仍然失效，提出只迁移"族内似然偏移"。

**安全与隐私**：

- [2609.33136](https://arxiv.org/abs/2609.33136)：第一个针对 OPD 的成员推断攻击，平均 AUROC 0.875。
- [2610.07654](https://arxiv.org/abs/2610.07654)：带后门的安全教师会通过 OPD 把后门传给学生。3% 的投毒率就能让攻击成功率最高达到 70%；常用的 top-k KL 会加快后门的传递。
- [2608.21500](https://arxiv.org/abs/2608.21500) SecOPD：面对 SOTA 自适应提示注入攻击 PISmith，攻击成功率为 9.0%，此前最优的防御 Meta-SecAlign 为 94.0%。

**投机解码**：只有 1 篇核心论文，[2610.37778](https://arxiv.org/abs/2610.37778) Multi-Draft OPD，面向并行扩散草稿器。之前的 Draft-OPD（2605.29343）不在本次的时间窗口内。

## 8 GitHub 上的 OPD 论文合集

以下数据是 2026-11-02 用 GitHub API 查到的。"近三个月条目"指 README 中 arXiv 编号为 2608～2610 的论文数（按编号去重）。

### 8.1 主要合集

| 仓库 | Stars | 创建 | 最近提交 | 规模 | 近三个月条目（2608/2609/2610） | 特点 |
| --- | --- | --- | --- | --- | --- | --- |
| [chrisliu298/awesome-on-policy-distillation](https://github.com/chrisliu298/awesome-on-policy-distillation) | 903 | 2026-03-22 | 2026-10-06 | 徽章写 800 条，README 中有 748 个 arXiv 编号 | 299（112/154/33） | 覆盖面最广。分核心论文、相关工作、领域扩展（智能体、多模态、语音、扩散与 flow、具身、投机解码）、技术报告、框架几块，另有按教师类型和按目标的两张分类表、Start Here 阅读路径和博客教程汇总。每条一句英文说明。CC0 许可 |
| [thinkwee/AwesomeOPD](https://github.com/thinkwee/AwesomeOPD) | 882 | 2026-04-27 | 2026-10-18 | 12 个分区，徽章合计约 490 条，README 中有 462 个 arXiv 编号 | 127（90/29/8） | 收录标准写得最明确：C1 学生自采样加 C2 教师监督学生样本，不满足的写进每节的 Strictness notes，被拒的论文和理由也记在更新日志里。每条带 Stars、日期、机构，并有折叠的技术细节表（损失与散度、数据、教师访问方式、粒度）。按月扫描，更新日志会总结当月的主线。有 Curator's Picks 入门阅读顺序 |
| [nick7nlp/Awesome-LLM-On-Policy-Distillation](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation) | 592 | 2026-04-05 | 2026-10-13 | 362 条，其中 134 条有代码 | 127（43/45/39） | OPD 综述（arXiv 2604.00626）的配套阅读列表，按研究问题组织，每篇一段摘要。配套检索站 [OPDHub](https://nick7nlp.github.io/OPDHub/)；`resources/` 下有方法对比、损失分类、关键公式、代码索引、评测指南和机器可读的 `catalog.json`。三个大合集里，10 月的条目它最多 |
| [Jingchensun/Awesome-Multimodal-OPD](https://github.com/Jingchensun/Awesome-Multimodal-OPD) | 38 | 2026-06-18 | 2026-11-01 | 158 条（图像 57、视频 15、音频 16、生成 45、具身 25），61 条有代码 | 69（34/35/0） | 只收多模态 OPD 和 OPSD。按 GitHub stars 排序，有中英文交互阅读页，`papers.json` 里每篇有四点摘要，并标注是否严格属于 OPD。近 30 天提交最勤（30 次） |
| [DjangoJungle/Awesome_MOPD](https://github.com/DjangoJungle/Awesome_MOPD) | 16 | 2026-08-04 | 2026-10-22 | 69 条 | 38（8/19/11） | 专收多教师 OPD（MOPD），分基础、方法、分析、应用，另列使用 MOPD 的技术报告 |
| [HJSang/awesome-OPSD](https://github.com/HJSang/awesome-OPSD) | 0 | 2026-10-06 | 2026-10-07 | 60 条，31 条有代码 | 25（10/13/2） | 专收 OPSD，每条有方法注释，附 `data/papers.json` 和 `papers.bib` |
| [kissshhot/Awesome-OPD](https://github.com/kissshhot/Awesome-OPD) | 26 | 2026-07-31 | 2026-10-10 | 114 条 | 37（6/19/12） | 每条有中英文摘要，`docs/SOURCE_AUDIT.md` 记录逐条核对时用的论文版本 |
| [hhlxm/Awesome_OPD](https://github.com/hhlxm/Awesome_OPD) | 0 | 2026-10-25 | 2026-11-01 | 34 条 | 13（3/7/3） | 每篇有较长的英文 TL;DR，按通用 OPD、智能体 OPD、高效 OPD、Latent OPD、OPSD 分组，并存档了 PDF |

### 8.2 已停更或只部分相关的合集

| 仓库 | 说明 |
| --- | --- |
| [Jianglin954/awesome-on-policy-distillation](https://github.com/Jianglin954/awesome-on-policy-distillation) | 113 条，最后提交 2026-04-13 |
| [AnhaoZhao-LLMer/On_Policy_Distillation_Paper_List](https://github.com/AnhaoZhao-LLMer/On_Policy_Distillation_Paper_List) | 176 个 arXiv 编号，最后提交 2026-06-08 |
| [china10s/awesome-opd](https://github.com/china10s/awesome-opd) | 122 条，最后提交 2026-05-15 |
| [miracle-techlink/opd-papers](https://github.com/miracle-techlink/opd-papers) | 多模态 OPD，34 条，最后提交 2026-05-15 |
| [zsxm1998/awesome-perception-aware-rlvr](https://github.com/zsxm1998/awesome-perception-aware-rlvr) | 36 stars，VLM 上感知相关的 RLVR 和 OPD 的复现与评测，含 24 篇近三个月的论文 |
| [yingyingxia666/awesome-agentic](https://github.com/yingyingxia666/awesome-agentic) | 中文的 LLM RL 大合集（910 篇以上），OPD 是其中一个方向，最后提交 2026-09-11 |
| [MAC-AutoML/Awesome-Self-Distillation](https://github.com/MAC-AutoML/Awesome-Self-Distillation)、[ahmedheakl/Awesome-Self-Distillation](https://github.com/ahmedheakl/Awesome-Self-Distillation) | 广义自蒸馏，没有 2608 之后的条目 |
| [Tebmer/Awesome-Knowledge-Distillation-of-LLMs](https://github.com/Tebmer/Awesome-Knowledge-Distillation-of-LLMs) | 1318 stars，是 2024 年一篇 LLM 知识蒸馏综述的配套列表，不专门针对 OPD |

### 8.3 合集之间的覆盖关系

| 合集 | 近三个月条目 | 只有它收录 |
| --- | --- | --- |
| chrisliu298 | 299 | 131 |
| thinkwee | 127 | 8 |
| nick7nlp | 127 | 25 |
| Jingchensun（多模态） | 69 | 20 |
| DjangoJungle（MOPD） | 38 | 9 |
| kissshhot | 37 | 1 |
| HJSang（OPSD） | 25 | 3 |
| hhlxm | 13 | 2 |

- 两两重合：chrisliu298 与 thinkwee 共有 97 篇，chrisliu298 与 nick7nlp 共有 78 篇，thinkwee 与 nick7nlp 共有 47 篇，三者都收的只有 42 篇。
- 8 个合集的并集是 409 篇。其中 368 篇本次 arXiv 关键词检索也能搜到；另外 41 篇搜不到（摘要里没有 "on-policy distillation" 之类的字眼，例如 EviSD、Woodpecker Distillation、MiMo-V2.6 技术报告），是从合集补进候选池的。
- 本次 540 篇核心论文里，有 186 篇不在任何合集中。第 2～7 节引用的 10 月下旬论文大多属于这一类，例如 2610.22236、2610.25034、2610.28586、2610.36477、2610.38681、2610.39020；2610.26525 只有 DjangoJungle 收录。

### 8.4 怎么用

- 入门：先读 thinkwee 的 Curator's Picks 和 chrisliu298 的 Start Here，再读 nick7nlp 的 `resources/reading-order.md`。
- 查某篇论文的技术细节（损失、教师访问方式、粒度）：看 thinkwee 的折叠表。
- 找全某个方向：用 chrisliu298 的对应小节，加上专题合集（多模态看 Jingchensun，多教师看 DjangoJungle，OPSD 看 HJSang）。
- 按关键词检索、筛选：用 nick7nlp 的 OPDHub，或 Jingchensun 的交互阅读页。
- 机器可读的数据：nick7nlp 的 `resources/catalog.json`，Jingchensun 的 `papers.json`，HJSang 的 `data/papers.json` 和 `papers.bib`。
- 三个大合集都还没收 10 月中下旬的论文，最新的论文要靠 arXiv 检索补齐。

## 9 入门阅读顺序

本季度的论文大多以下面这些为基线，先读：

1. Thinking Machines 的博客 [On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/)（2025-10）
2. GKD（2306.13649）和 MiniLLM（2306.08543）
3. Rethinking OPD（2604.13016）：本仓库有[全文翻译](./Rethinking-On-Policy-Distillation.md)
4. OPSD（2601.18734）
5. OPD 综述 A Survey of On-Policy Distillation for Large Language Models（2604.00626）

再读本季度的论文，按下面的顺序：

1. 先了解边界：2609.04172（1 条 query 就够）→ 2610.11291（何时需要 on-policy）→ 2610.09639（学技能，不学知识）→ 2608.31046（真的在蒸馏吗）
2. 再了解失败模式：2609.20511（EOS 失配）→ 2610.18011（在学生做错的题上失效）→ 2609.31900（流水线顺序）
3. 做 OPSD 的话：2608.18271 → 2609.20612 → 2609.29051 → 2610.13744
4. 做 MOPD 的话：2608.19098 → 2609.35347 → 2610.04272 → 2610.26525
5. 做 OPD 和 RL 组合的话：2609.04108 → 2609.28145
6. 做智能体的话：2609.40285 → 2610.25034 → 2610.28586 → 2610.31918
