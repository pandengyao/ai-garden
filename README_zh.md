# 🌱 ai-garden

中文 | [English](./README.md)

> 我的 AI 数字花园：对 AI 的调研、阅读与思考，都慢慢记录在这里。

这不是一份收藏夹，而是一座花园。每篇笔记都是一株植物：读到的文章在这里被消化成自己的语言，想法从一句话的种子开始，随着调研和实践慢慢长大。有的会长成大树，有的停在半路——都留着，因为思考的痕迹本身也值得保留。

## 怎么逛这座花园

| 分区 | 里面是什么 |
| --- | --- |
| [🌳 笔记 notes](#-笔记-notes) | 读过的文章、论文、报告，消化后的中文笔记（附英文版） |
| [🌱 想法 ideas](./ideas/README_zh.md) | 自己的思考与猜想，从一句话开始 |
| [📰 速递 news](./news/README_zh.md) | 按月记录的 AI 动态，一句话一条 |

## 🌳 笔记 notes

### 智能体 (Agents)

- [Agent = Model + Harness：大模型 Harness 深度调研](./notes/agent/Agent-Harness-Survey.md) · 2026-10-20
  - harness 是模型之外的整套运行时：系统提示、工具、沙箱、编排与上下文管理。约束紧、或通用 harness 与模型的训练方式不匹配时，换 harness 能让分数翻几倍；条件宽松时，它主要决定的是成本。附 Hermes Agent、Pi、OpenCode、OpenClaw 等主流产品的版图，以及自动化 harness 优化与 harness-native RL 的进展。

- [MCP (Model Context Protocol) 入门整理](./notes/agent/MCP-Model-Context-Protocol.md) · 2026-10-20
  - 给 AI 装的「万能接口」：工具方按标准做一次服务器，所有支持 MCP 的 AI 都能用。含待办事项服务器完整示例与新旧 SDK 的改名坑。

### 推理优化 (Inference)

- [DeepSeek V4.1 Flash 推理部署 Q&A：DeepInfer 官方文档全文翻译](./notes/inference/DeepSeek-V4.1-Flash-Inference-Deployment-QA.md) · 2026-10-20
  - DeepSeek 官方的线上部署细节：单集群每天 155 万亿 tokens；Prefill 用 8 卡机器、尽量小的 EP，Decode 用 64–128 卡超节点做 Wide-EP，Block KVCache 存在约 100 PiB 的独立 3FS 集群上（TTL 3–7 天）。另含 EPLB 与 DP 负载均衡参数、SWA Bounded Replay 的命中与重算、DSpark 变长验证（生产点吞吐 +4–7%）。

- [Flash-Decoding: 长上下文推理加速](./notes/inference/Flash-Decoding.md) · 2023-10-12
  - 推理时 Query Length 只有 1，Batch 维度并行不起来；那就去并行 KV Cache 的序列长度维度，长序列解码最高快 8 倍。

### 模型 API (LLM APIs)

- [免费与低价大模型 API 调研：额度、价格、套餐与接入](./notes/llm_api/Free-and-Low-Cost-LLM-APIs.md) · 2026-10-20
  - 长期免费能用的主要是 NVIDIA build、智谱 glm-4.7-flash，以及 Kilo 和 OpenRouter 的免费模型；国内按量最便宜的一档每百万输入 0.15–1 元，编程包月套餐大多只许在工具里交互使用。附 23 家平台的官网、Key 入口、base_url 和调用示例。

### 多模态 (Multimodal)

- [免费与低价语音合成（TTS）API 调研：额度、价格、声音复刻与接入](./notes/multimodal/Free-and-Low-Cost-TTS-APIs.md) · 2026-10-21
  - 比价先看一个汉字算几个字符：百炼、MiniMax、Azure 算 2 个，豆包、腾讯、阶跃算 1 个，硅基流动和 Fish Audio 按 UTF-8 字节算。长期免费额度有 Azure 每月 50 万字符、Google Cloud 每月 400 万字符和 Speechify 每月 50 万字符，Gemini 免费层不收费但国内不在可用地区；能合成中文的按量付费，大模型音色最便宜的约 0.9–1.6 元/万字。附声音复刻价格、可商用的开源模型（CosyVoice 3、Qwen3-TTS、VoxCPM2）和 Hermes Agent 接入方法。

- [免费与低价文生图调研：网页 App、API、本地软件与合规](./notes/multimodal/Free-and-Low-Cost-Text-to-Image.md) · 2026-10-21
  - 不写代码，国内用通义万相、即梦、豆包、元宝、文心等网页就能免费出图；免费 API 有智谱 CogView-3-Flash、硅基流动 Kolors、魔搭、商汤公测和 Cloudflare 每日额度；付费 API 国内最低约 0.025 元/张（MiniMax），海外 FLUX.2 Klein 4B 约 $0.0005/张。附 6 个免费 API 的调用示例、Draw Things 云端免费档的算力单元表、开源模型许可证，以及在国内上线要做的标识和备案。

- [Gemini 3 Pro Image Preview: 图片生成的 ChatGPT 时刻](./notes/multimodal/Gemini-3-Pro-Image-Preview.md) · 2025-11-20
  - 生图模型从“画得好看”转向“把信息讲清楚”，原生多模态让理解能力正向迁移到生成上。

### 自我改进 (Self-Improvement)

- [RSI 论文追踪：2026 年 8–10 月新论文与 GitHub 论文合集横评](./notes/self_improvement/RSI-Recent-Papers-and-GitHub-Lists.md) · 2026-11-02
  - GitHub 上整理 RSI 论文的清单已有 30 多个，但收录量最大的五个两两重叠只有 0.02–0.15（Jaccard 系数），没有一个能单独覆盖这个方向：通用图谱看 lobehub/awesome-rsi，按维度检索看 Prism-Shadow/awesome-rsi，最新论文和逐条证据等级看 pinkbubblebubble/awesome-rsi，每周更新和机读数据看 KaiWU5/Awesome-AI4AI，中文每日追踪看 adongwanai/follow-rsi。10 月 15–30 日又有 497 篇候选论文、32 篇以 RSI 命名，但没有改变上一篇综述的结论：harness 自进化仍是方法论文最多的地方，增长最快的是审计、测量与安全研究，前沿智能体自主后训练有了可测量的平台，具身方向的两篇综述都认为还没有研究隔离出可归因于递归的增益。

- [AI 递归自我改进（RSI）文献综述](./notes/self_improvement/RSI-Literature-Review.md) · 2026-10-21
  - 系统检索 5,784 篇候选论文、精读 365 篇后的结论：权重、上下文/记忆/技能、脚手架、AI 设计组件和自动化研究五条线索都有大量有界自我改进，但没有一条有可靠的递归（复利）自我改进证据。多轮实验的增益逐轮递减或饱和，最外层始终保留一个固定的评估或选择环节；自称 RSI 的 90 篇研究中，只有 22% 审计过两次以上的完整闭环复跑。信号来源决定上限：以执行或形式验证为锚的回路最稳，自评回路几轮内就会反转或崩溃；风险随世代累积的证据，反而比能力复利的证据更扎实。
  - 分章页面：[第 4 章](./notes/self_improvement/RSI-Literature-Review-Ch04.md) · [第 5 章](./notes/self_improvement/RSI-Literature-Review-Ch05.md) · [第 6 章](./notes/self_improvement/RSI-Literature-Review-Ch06.md) · [第 7 章](./notes/self_improvement/RSI-Literature-Review-Ch07.md) · [第 8 章](./notes/self_improvement/RSI-Literature-Review-Ch08.md) · [第 9 章](./notes/self_improvement/RSI-Literature-Review-Ch09.md) · [第 10 章](./notes/self_improvement/RSI-Literature-Review-Ch10.md) · [第 11 章](./notes/self_improvement/RSI-Literature-Review-Ch11.md) · [第 12 章](./notes/self_improvement/RSI-Literature-Review-Ch12.md) · [第 13 章](./notes/self_improvement/RSI-Literature-Review-Ch13.md)

### 训练 (Training)

- [OPD 中的 Forward KL 与 Reverse KL：直觉、公式与常见误区](./notes/training/Forward-and-Reverse-KL-in-OPD.md) · 2026-11-06
  - Forward KL 按老师概率加权，防止漏掉老师认可的选择；Reverse KL 按学生概率加权，防止高估老师低概率的选择。用一个三 token 例子澄清两者的区别，并区分 KL 方向与 OPD 的轨迹来源。

- [on-policy 蒸馏（OPD）论文调研：2026 年 8–10 月的新论文与 GitHub 论文合集](./notes/training/On-Policy-Distillation-Literature-Review.md) · 2026-11-02
  - 2026 年 8–10 月 arXiv 上有 540 篇核心 OPD 论文（8 月 128 篇，10 月 212 篇），另有 35 篇工业技术报告用到 OPD。这一季的主线是追问 OPD 到底在起什么作用，多数结论和直觉相反：1～8 条 prompt 就能接近全量数据，只监督 0.05%～1% 的 token 就能追平全 token，反向 KL 的 OPD 传技能不传事实，17 组师生对里有 14 组用初始学生离线采样的数据反而更好。同模型自蒸馏（OPSD）论文最多，特权信息的作用也被十余篇分析论文质疑；先 OPD 后 RL 优于联合训练；多教师 OPD 已是工业界合并专家模型的常用做法，但在受控对比中并不比 SFT 合并更准。GitHub 上 chrisliu298、thinkwee、nick7nlp 三个大合集对近三个月论文只共同收录了 42 篇，而且都还没收 10 月中下旬的论文。
  - 配套页面：[论文清单（540 篇核心论文与 136 篇相关工作）](./notes/training/On-Policy-Distillation-Literature-Review-Papers.md)

- [训练数据中的思维链合成：方法、证据与开放问题（文献综述）](./notes/training/CoT-Data-Synthesis-Literature-Review.md) · 2026-10-22
  - 系统检索 13,589 篇候选、纳入 1,527 篇、精读 237 份来源后的结论：用于 SFT 与蒸馏的推理数据，重心已从“多找题”转向“每题多采样、再按学生挑选”，2026 年又快速转向 on-policy 蒸馏（摘要提及它的纳入文献从 2025 年下半年的 2 篇增至 2026 年上半年的 79 篇）；代码与智能体数据的瓶颈在任务与环境的多样性。“教师越强越好”“答案正确的轨迹更好”“数据越多越好”“验证一定有益”四条直觉都有受控实验给出的反例，成立与否取决于学生规模、师生分布距离与训练预算。以答案为条件的生成、长度惩罚与递归自训练，会以答案正确率察觉不到的方式损害数据。
  - 分节页面：[第 4 节](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch04.md) · [第 5 节](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch05.md) · [第 6 节](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch06.md) · [第 7 节](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch07.md) · [第 8 节](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch08.md) · [第 9 节](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch09.md) · [第 10 节](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch10.md)

- [面向在线学习的桥接自蒸馏（论文通俗解读）](./notes/training/BSD-Bridged-Self-Distillation.md) · 2026-10-19
  - BSD 只要求老师交一份文字解答，交给学生的冻结副本当参考，由它逐个 token 检查学生做错的答卷、调整扣分轻重，对错仍由判卷器决定，所以同分词器、不同分词器和闭源 API 三种老师共用一套训练流程。4 个 Qwen3 学生跟 3 种老师学的 12 组里，BSD 都超过未训练的学生，平均正确率提升 1.2～4.7 个百分点，11 组是蒸馏方法里的最高分或并列最高；直接模仿老师解答的 SFT 有 8 组反而变差。按 6 个检查点平均读图估计，BSD 对专门方法的领先只有约 0.3～1.3 分。

- [该蒸馏哪项技能？SGUID：为模型与技能的共同进化挑选精简技能库（论文通俗解读）](./notes/training/SGUID-Selecting-a-Compact-Skill-Bank.md) · 2026-10-08
  - 论文发现，把技能蒸馏进模型时，按语义相关检索到的技能大多没起作用：三个 Qwen3 模型上只有 6.4%～21.2% 的技能检索真正进入训练。据此提出的 SGUID 先带全部技能试训，按训练中是否一直给出有效信号只留几条，再从原模型重新训练；变强的模型再总结新技能、再挑、再学。在三套数学竞赛题上，只学 6 条技能，4 个模型中有 3 个追平或超过学全部 30～71 条的效果；第 2 轮再学 3 条后 4 个模型全部追平或超过，Qwen3-8B 的平均正确率从 62.9% 升到 66.3%。

- [面向高效多轮智能体微调的依赖感知轨迹精炼（论文全文翻译）](./notes/training/Dependency-Aware-Trajectory-Refinement.md) · 2026-09-16
  - 把多轮智能体轨迹看成轮次级依赖 DAG，再在图上做确定性的编辑：L1 剪掉出度为 0 的死胡同轮次，L2 合并父节点和子节点都相同的兄弟轮次，L3 只要求父节点相同并迭代合并，L2a/L3a 再让 LLM 把合并后的 `<think>` 改写成一段连贯的推理。用 6196 条轨迹对 Qwen3-VL-30B-A3B-Thinking 做 SFT，在四个多模态 QA 基准上，L1 平均准确率 50.04%，比 Vanilla SFT 高 1.7 个百分点；L2a 与 Vanilla SFT 准确率相当，推理 token 却从 20.9K 降到 11.0K。L3 打破了推理时每回合一次工具调用的格式，卡死率是 L2 的 2–3 倍；让 LLM 直接删除轮次的 Critical-Path 基线反而比 Vanilla SFT 掉点。

- [重新思考大语言模型的同策略蒸馏 II：一个训练样本（论文全文翻译）](./notes/training/One-Shot-On-Policy-Distillation.md) · 2026-09-03
  - 把 OPD 的训练数据压到一条查询：数学推理上 one-shot OPD 在第 300 步达到 68.5 分（全量数据 OPD 为 69.8），回收 87% 的全量数据收益，跨三个模型家族、四个任务领域都成立，连训练中从未解出的难题也一样有效。解释分两侧：数据侧，OPD 消耗的是状态而不是查询，一条查询就覆盖全量数据状态空间的 71.5%，16 条语义多样的查询覆盖 98.9% 并追平全量数据训练，多教师 OPD 同样如此；算法侧，一次更新吸收掉的剩余师生差距的比例持续下降，而且 1 条与全部 17k 条查询的下降速度相同，所以 OPD 数据过饱、算法饥饿。连不含任务内容的模板和域外 WildChat 查询，都能逼近真实查询的基线。

- [特权似然不自动等于价值：在线自蒸馏中 token 功劳分的三项检查（论文通俗解读）](./notes/training/Three-Checks-for-Token-Credit-in-OPSD.md) · 2026-08-10
  - 一项诊断研究：在线自蒸馏（OPSD）拿看过特权提示的模型给 token 打的分当功劳分，作者提出使用前该做的三项检查：分数能否分清对错、提示是否照着被打分的解答写、训练怎样用分数。gpt-oss-20b 做 AIME 2025 时，分数分辨对错的 AUC 只有 0.505，五种加 token 分的做法比只看对错的 GRPO（64.2%）低 30.4～40.0 个百分点；SDPO 训练 Qwen3-8B 做生物题时 AUC 为 0.813～0.924，正确率涨了 26.75 和 28.00 个百分点。

- [特权解答，还是上下文引起的老师行为？拆解在线自蒸馏（论文通俗解读）](./notes/training/OP2SD-Dissecting-On-Policy-Self-Distillation.md) · 2026-08-10
  - 在线自蒸馏（OPSD）让同一个模型当老师和学生，老师额外看本题的参考解答。这篇论文把老师看的本题解答换成另一道题和它的解答（OP²SD），其余不变，以拆开"老师知道本题答案"和"老师手边有一份解题范例"这两种作用。在 Qwen3 的 1.7B、4B、8B 和 AIME 2024、AIME 2025、HMMT 2025 上，9 组对比里 OP²SD 有 8 组得分最高，8B 上比 OPSD 高约 10 分，例如 AIME 2024 上原模型 28.47%、OPSD 45.00%、OP²SD 55.83%。范例用一道固定的题就够，改错一步也照样有效；"1+1=2" 会把模型教崩，物理题解答会让成绩低于原模型。作者认为提升主要来自一份像样的数学解题范例改变了老师的打分方式。

- [让监督匹配学生的学习能力：在线自蒸馏的统一框架（论文通俗解读）](./notes/training/USD-Unified-On-Policy-Self-Distillation.md) · 2026-08-08
  - 在线自蒸馏（OPSD）可以调两个旋钮：学生重点学哪些 token，给老师看多少参考解答。论文认为两者在争用学生同一份消化能力，提出 USD：把它们放进同一个带难度预算的优化问题，推出一个难度价格 λ，每个批次按平均难度高于还是低于预算同时调两个旋钮。在 Qwen3-1.7B、4B、8B 和三个数学竞赛测试集上，USD 比普通 OPSD 分别高 2.5、2.3、2.1 个百分点，只调一个旋钮的变体只高 0.4～1.8 个百分点；能力预算 ε 只有取 0.3 时 USD 才明显好于普通 OPSD。

- [有特权，但有偏见：看过答案的老师如何让自蒸馏失效（论文通俗解读）](./notes/training/PI-Bias-Privileged-but-Biased-Teachers.md) · 2026-08-05
  - 一项诊断研究：把自蒸馏（同一个模型看了参考答案后给只看题目的自己当老师，逐 token 纠正学生）原封不动搬到难的问答、数学、编程和多轮工具调用任务上，不加任何奖励。用 Qwen3-8B 训练时损失一路下降，成绩却不涨，多数还在下降：SDPO 配方下 think 模式的多轮工具调用平均掉 3.51 个百分点，OPSD 配方下 think 模式的数学平均掉 4.28 个百分点。原因是看过答案的老师只认那一份答案：数学上它对这份答案的 PI 偏差分数是 0.52，换成同一题的另一份正确答案只有 0.02 左右或更低；损失还有一半以上花在虚词、标点和犹豫词上，试错被罚，学生最后变得更"平"、更早收笔。

- [DAPD：双锚定策略蒸馏（论文通俗解读）](./notes/training/DAPD-Dual-Anchored-Policy-Distillation.md) · 2026-08-03
  - OPSD 让看着参考解答的自己当老师、教考试时看不到答案的自己，学生因此学会推不下去就硬报一个答案，论文称为特权幻觉。DAPD 保留 OPSD 原来的损失，加入"眼前放着完整解答"的中间角色 Self，搭出两条信息对等的对齐路径，并让参考解答和学生回答轮流当指导材料。在 Qwen3-4B 上，六项基准平均分比 OPSD 高 2.00 分；在 1.7B 到 32B 五个尺寸上，三个数学竞赛的平均正确率比 OPSD 高 1.94～2.78 分；训练后期硬报答案的次数，五个尺寸合计从 33 次降到 9 次，少 73%。

- [超越模仿：面向大模型推理的反思式在线自蒸馏（论文通俗解读）](./notes/training/ROSD-Reflective-On-Policy-Self-Distillation.md) · 2026-05-27
  - ROSD 改进在线自蒸馏：模型做错题后先对照同组一份做对的回答自己复盘，找出第一句错话并写改错要点；老师只看这段要点，不看整份答案，且只从第一句错话开始纠正，前面推对的部分不计入损失。在 Qwen3-4B、Qwen3-8B、Llama-3.2-3B-Instruct 上，五任务平均分都是第一（72.83、73.45、53.38），比增强版 GRPO 高 0.69～2.97 分（取训练中的最高分），没有 SDPO 那样的后期崩溃；跨领域测试明显好于 SDPO，但全部 10 组都不如 GRPO。

- [HINT-SD：面向长程智能体的定向事后自蒸馏（论文通俗解读）](./notes/training/HINT-SD-Targeted-Hindsight-Self-Distillation.md) · 2026-05-18
  - HINT-SD 让长程智能体在任务失败后自己复盘整条轨迹，挑出真正需要改的一到三步，给每步写一两句修改意见，然后只在这几步上让看过意见的自己逐 token 教没看意见的自己，默认不需要更强的老师模型。用 Qwen3-4B 训练后，它在 BFCL v3 和 AppWorld 上的平均成功率分别是 41.88% 和 18.46%，比各自最强的对照方法高 10.32 和 8.72 个百分点；和每步都请裁判打分的 OpenClaw-RL 相比，每个训练步的耗时从 84.76 秒降到 37.45 秒。

- [成功很少、反馈很多时，靠"反思增强的自蒸馏"来学（论文通俗解读）](./notes/training/RESD-Reflection-Enhanced-Self-Distillation.md) · 2026-05-12
  - 成功很少时，SDPO 的老师只剩原始报错，教不出什么。RESD 让模型做错后自己写错题分析，把经验攒进所有题共用的错题本，并存档做对的回答，都放进老师的提示里，逐 token 纠正学生。每题每步只生成 1 份回答，Manufactoria-Has 每题全对率从 SDPO 的不到 1% 提到 35.80%，两个物理模拟任务到 4.25%～7.25%，FiNER 比最好基线的 50.25% 高到 53.66%；前期比 GRPO 涨得快，后期不一定更好，每步耗时约为 SDPO 的 1.5～2 倍。

- [在线蒸馏的多面性：陷阱、成因与补救（论文通俗解读）](./notes/training/Many-Faces-of-On-Policy-Distillation.md) · 2026-05-11
  - 实证分析在线蒸馏（OPD）和在线自蒸馏（OPSD）何时管用、为何失败，原因有三：学生的半截答案带偏老师；不归一化的 Top-K 损失多出 "+1" 梯度偏差，训练会崩成一串 "maybe"；OPSD 只学到各题小抄的共同部分。Qwen3-14B 接着学生的半截答案做 GPQA-Diamond，准确率从 62.1% 掉到 46.0%；经 RL 调过的 1.7B 老师和 Qwen3-8B 成绩相近（0.82 对 0.83）却更好用。OPSD 对风格对齐和系统提示内化有效，在所测数学设置里没有提升。

- [重新思考大语言模型的 on-policy 蒸馏：现象、机制与配方（论文全文翻译）](./notes/training/Rethinking-On-Policy-Distillation.md) · 2026-04-14
  - 系统研究 on-policy 蒸馏（OPD）成败的条件与词元级机制。成功要同时满足两点：师生思维模式相容，且教师带来学生训练中没见过的新知识——反向蒸馏显示同家族 1.5B 与 7B 教师在学生看来分布上不可区分，OPD 学的是思维模式而非基准分数。机制上，成功的 OPD 让学生与教师的高概率 top-k 词元渐进对齐（重叠率从约 72% 升到 91% 以上，占双方 97%–99% 的概率质量），只优化重叠词元就够。给出两种补救失败 OPD 的配方：off-policy 冷启动、与教师对齐的提示词。并指出密集奖励的代价——可靠性随轨迹深度下降，失败源于局部优化几何而非信号质量，而支撑集大小只要避开 Top-1 就不关键。

- [自蒸馏 Zero：用自我修改把"对/错"奖励变成逐词的监督（论文通俗解读）](./notes/training/Self-Distillation-Zero.md) · 2026-04-13
  - SD-Zero 让模型分饰答题者和修改者，后者看过答案和对错再逐词重读，把对/错奖励变成逐词监督，无需更强的老师或标准解法。先用约 6000 条自己写的、最终答案正确的修改稿学会改答案，再把这本事蒸馏回答题。Qwen3-4B-Instruct 和 Olmo-3-7B-Instruct 在 8 个数学和编程测试集上平均正确率从 49.8% 提到 60.3%、从 41.1% 提到 51.5%；按论文的记账，生成次数相当时比 SFT、RFT、GRPO、SDFT 高 4.8～10.3 个百分点。

- [语言模型的特权信息蒸馏（论文通俗解读）](./notes/training/Pi-Distill-Privileged-Information-Distillation.md) · 2026-02-04
  - 想把大模型多步调工具的本事教给小模型，可不少大模型藏起思维链。论文把大模型成功的动作记录当"小抄"放进提示词，同一模型带小抄当老师、不带当学生一起训练（π-Distill），上线时学生不看小抄也能做好。Qwen3-8B 在 Travel Planner 上从 23.6% 升到 44.1%，接近 671B 的 DeepSeek-V3.1（45.0%），比用完整思维链的 SFT + RL（32.3%）高 11.8 个百分点；τ-Bench 零售从 3.35% 升到 31.1%，该对照 29.1%。

- [用自蒸馏做强化学习（论文通俗解读）](./notes/training/SDPO-Reinforcement-Learning-via-Self-Distillation.md) · 2026-01-28
  - SDPO 把环境返回的报错等文字反馈交给同一个模型，让它当老师逐词重读自己刚写的答案、指出哪个词写错了，再让模型朝老师的看法调整，不需要更强的外部模型，也不需要单独训练奖励模型。在 Qwen3-8B 上练 LiveCodeBench v6 编程题，准确率 48.8%，比 GRPO 的 41.2% 高 7.6 个百分点，只用约四分之一的生成量就达到 GRPO 的最终水平；在只给对错的科学问答和工具调用任务上，10 组对比赢了 GRPO 7 组，回答长度只有 GRPO 的约三分之一；短板是模型太弱时反而不如 GRPO。

- [自蒸馏让持续学习成为可能（论文通俗解读）](./notes/training/SDFT-Self-Distillation-Continual-Learning.md) · 2026-01-27
  - SDFT 让同一个模型分饰两角：老师在提示词里多看一份专家示范，学生只看题目、自己作答，老师对学生的回答逐个 token 给出概率分布，学生朝老师靠拢，所以只有示范、没有奖励函数，也能在自己写的回答上学习。在 Qwen2.5-7B-Instruct 上分别学科学问答、工具调用、医疗三项新技能，新任务准确率比 SFT 高 4.0～7.4 个百分点，六项旧能力的平均分只比原模型低 0.1～1.0 分，SFT 则低 5.3～12.1 分；学新知识时间接问题答对 98%，SFT 是 80%；连续学三项技能时能把学过的攒住。代价是训练耗时约为 SFT 的 4 倍，3B 这么小的模型上反而不如 SFT。

- [自蒸馏推理者：大语言模型的 On-Policy 自蒸馏（论文通俗解读）](./notes/training/On-Policy-Self-Distillation.md) · 2026-01-26
  - OPSD（on-policy 自蒸馏）让同一个模型分饰两角：老师多看一份参考解答，学生只看题目并自己作答，老师在每个位置给出下一个 token 的分布让学生靠拢，不用外部老师。Qwen3-1.7B 只训练 100 步、每题只采 1 条回答，三个竞赛数学测试集平均分从 37.1 提到 43.4；GRPO 训练 500 步只到 37.7，前 100 步生成的 token 约是 OPSD 的 8 倍。4B、8B 上 OPSD 只比 GRPO 高 0.9、0.8 分；SFT 在三个尺寸上平均分都下降。

- [MMAT-1M：百万级多模态 Agent 微调数据集](./notes/training/MMAT-1M-Multimodal-Agent-Tuning.md) · 2025-07-29
  - 用 GPT-4o 给 5 个公开视觉问答数据集补上推理过程、工具调用（图片描述、OCR、检测、搜索）和反思，得到 902,965 条多轮对话（RR），另有一份压成单轮的版本（ORR）。用它 LoRA 微调 1 个 epoch 后，InternVL2.5-8B 的 8 项基准平均分从 60.7 涨到 63.4，Dyn-VQA 从 35.2 涨到 44.0；不微调、只靠提示词套用这种格式反而掉分。实测数据还发现：ORR 比 RR 少 16% 的样本，通用反思只指出“作弊”、不重新推理，不少样本的图片描述里已经写着答案；原图的下载地址已失效，图片要到各个原始数据集里找。

- [OpenThoughts：推理模型的数据配方（论文全文翻译）](./notes/training/OpenThoughts-Data-Recipes-for-Reasoning-Models.md) · 2025-06-04
  - 用 1,000 多次受控实验逐步优化推理 SFT 数据流水线，得到 OpenThoughts3-1.2M；用它训练的 OpenThinker3-7B 在 AIME 2025、LiveCodeBench 06/24-01/25 和 GPQA Diamond 上分别达到 53%、51% 和 54%。主要发现：让教师模型给每个问题采样多个答案，能把数据扩大 16 倍以上；基准分数更低的 QwQ-32B 反而是比 DeepSeek-R1 更好的教师；答案验证与过滤没有带来明显收益；只用一两个高质量问题来源，好过追求来源多样；按 LLM 标注的难度或回答长度筛选问题，效果好于 fastText、embedding 这类预训练数据过滤方法。

## 这座花园怎么打理

- 每篇笔记开头记来源链接和日期，方便回溯。
- 笔记统一用 Markdown，先写中文，每篇配一份英文版（`_en.md`）；图片放在各分区的 `img/` 下。
- 内容只在这里慢慢生长，不追求写完就定稿。

## License

笔记内容采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，仓库内代码采用 [MIT](./LICENSE)。引用的原文版权归原作者所有。
