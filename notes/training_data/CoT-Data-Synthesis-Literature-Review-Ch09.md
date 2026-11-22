# 训练数据中的思维链合成：方法、证据与开放问题 · 第 9 节

中文 | [English](./CoT-Data-Synthesis-Literature-Review-Ch09_en.md)

- **调研日期**: 2026-10-22（证据截止：arXiv 首版日期不晚于 2026-10-22）
- **导航**: [主页面](./CoT-Data-Synthesis-Literature-Review.md)（摘要、第 1–3 节、第 11–13 节与附录） · 上一节：[第 8 节](./CoT-Data-Synthesis-Literature-Review-Ch08.md) · 下一节：[第 10 节](./CoT-Data-Synthesis-Literature-Review-Ch10.md)
- **依据**: 句末的上标数字是引用，对应文末参考来源中的精读文献；每条引用都有从该文献全文逐字摘录、并经脚本与全文核对的原文。标有（本文判断）、（本文推断）或（本文统计）的内容，是本文的综合分析或统计，不是来源原话。

## 9 智能体轨迹的合成

智能体轨迹在思维链之外还包含动作与环境观测，动作可以是工具调用、代码执行或网页操作（本文判断）。合成这类数据要同时回答四个问题：任务从哪里来，环境如何搭建，轨迹由谁生成，成功由什么判据认定（本文判断）。本节按场景梳理 2023 年以来的代表性管线，再讨论智能体数据的配方与蒸馏，最后单列成功过滤的分歧（本文判断）。题目来源、生成、验证与选择的一般方法见第 5—8 节，风险见第 10 节，本节只讨论它们在多轮交互中的特殊形态（本文判断）。表 9-1 汇总了本节涉及的主要管线（本文统计，各行依据见所标文献）。

表 9-1 代表性智能体数据管线对比（各行依据见所标文献）

| 系统 | 任务来源 | 环境 | 轨迹生成者 | 成功判据 | 规模 | 代表结果 |
| --- | --- | --- | --- | --- | --- | --- |
| ToolLLM[^185] | ChatGPT 依 3,451 个 RapidAPI 工具编写指令 | 真实 API 调用 | ChatGPT + DFSDT 搜索 | 仅保留判定通过的路径 | 126,486 对 | ToolLLaMA-7B 通过率 66.7，ChatGPT-DFSDT 为 64.8 |
| AgentTuning[^186] | 六类环境训练集与派生指令 | ALFWorld、WebShop 等 | GPT-4（ReAct） | 环境奖励 r = 1（Mind2Web 放宽） | 35,341 条指令保留 1,866 条 | AgentLM-70B held-out 1.40，GPT-3.5 为 1.49 |
| FireAct[^187] | HotpotQA 训练题 | Google 搜索 | GPT-4（ReAct/CoT/Reflexion） | 保留成功轨迹 | 默认 500 条 | Llama-2-7B EM 14.8→26.2 |
| ToRA[^189] | GSM8k、MATH 训练集 | 程序执行 | GPT-4；CodeLLaMA-34B 修正 | 答案正确且无工具错误 | 16k→69k 条 | ToRA-Code-34B MATH 50.8%，GPT-4 CoT 为 42.5% |
| ReTool[^190] | Open-Thoughts 等数学数据 | 代码沙箱 | 改写文本 CoT 冷启动 + PPO | 答案校验，奖励 ±1 | 未报告 | Qwen2.5-32B-Instruct AIME2024 67.0%，文本 RL 为 40.0% |
| APIGen[^192] | 3,673 个可执行 API + 种子问答 | 真实执行 | DeepSeek-V2-Chat 等开源模型 | 格式、执行、语义三级检查 | 约 60,000 条 | xLAM-7B BFCL 85.65（第 6 名） |
| ToolACE[^191] | 26,507 个合成 API | LLM 模拟用户、助手与工具 | 未注明具体模型 | 规则与模型双层检查，不执行 | 25,000 条（对照） | BFCL 58.19，xLAM 40.51 |
| APIGen-MT[^193] | τ-bench API 与策略生成的蓝图 | τ-bench + 模拟用户 | gpt-4o；DeepSeek V3 | 终态与输出匹配（r = 1） | 5K 条 | xLAM-2-70b τ-bench 56.2%，GPT-4o 为 52.9% |
| TOUCAN[^199] | 495 个 MCP 服务器上的合成任务 | 真实 MCP 执行 | GPT-OSS-120B、Kimi-K2、Qwen3-32B | 规则检查 + LLM 评审 | 1,527,259 条（SFT 用 119.3K） | Qwen2.5-32B BFCL-V3 61.73%→70.45% |
| ASTRA[^14] | 1,585 个 MCP 服务器的工具链任务 | 真实 MCP + 模拟器（20% 失败注入） | Qwen-Agent 框架（论文默认 LLM 为 GLM-4.6-FP8，未单列轨迹模型） | 七维自动评分；RL 用沙箱校验 | 54,885 条 SFT | Qwen3-32B BFCL-MT 47.88→64.25 |
| MidTool[^40] | 文档与真实 API/MCP 技能 | 以合成为主，另混入 AWM 环境 rollout | GPT-5、GPT-5.1、GPT-5.2 | 模式与顺序校验，重试后丢弃 | 20.3B token，轨迹 0.42M 条 | Qwen3-4B/8B-Base 在三个基准上优于仅 SFT 基线 |
| SWE-Gym[^194] | 11 个仓库的真实 issue | 可执行仓库 + 单元测试 | OpenHands + gpt-4o、claude-3.5-sonnet | 单元测试判定成功 | 2,438 个任务，491 条轨迹 | Qwen2.5-Coder-32B Verified 20.6% |
| R2E-Gym[^196] | 提交 + 生成测试 + 反向翻译描述 | 可执行仓库 | Sonnet-3.5-v2 | 测试通过 | 4,578 个任务，3,321 条轨迹 | 32B Verified 34.4%，Best@26 为 51.0 |
| SWE-smith[^195] | 128 个仓库中注入的缺陷 | 可执行仓库 | SWE-agent + Claude 3.7 Sonnet | 测试通过，每任务至多 3 条 | 50,137 个任务，5,016 条轨迹 | SWE-agent-LM-32B Verified 40.2% |
| AgentTrek[^198] | RedPajama 中的网页教程 | BrowserGym 真实网站 | GPT-4o 视觉语言智能体 | GPT-4o 评估器 | SFT 用 6,000 条文本轨迹 | Qwen2.5-32B WebArena 22.40，GPT-4o 为 13.10 |
| WebSailor[^197] | 知识图随机游走 + 信息模糊化 | Google 搜索 + 网页访问 | 开源推理模型动作 + 重建短思考 | 答案正确、≤32k token、>5 次调用 | 2k 余条冷启动 | 72B BrowseComp-en 12.0 |
| OpenResearcher[^202] | 约 6K 道 MiroVerse 问答 | 离线 15M 文档 + search/open/find | GPT-OSS-120B | 格式过滤，SFT 前按答案筛选 | 97K+ 条，SFT 约 55K | Nemotron-3-Nano-30B-A3B BrowseComp-Plus 54.8%（+34.0） |
| QUEST[^29] | 热点关键词→评分树→问题 | Google 搜索、网页访问、Python 等 | Tongyi DeepResearch | 生成的 Python 评分脚本 | 过滤后客观题 5,934 道；训练共用 8K 道任务 | Quest-35B GAIA 80.8%，GPT-5 为 76.4% |
| FORT-Searcher[^33] | 长尾实体 + 多源证据 + 数值模糊 | 真实检索接口 | DeepSeek-V4-Pro-0813 | 成功轨迹（任务经对抗求解改写） | 40K 条 | 三种规模学生 BrowseComp +5.3–18.9 点（不启用上下文管理） |
| OpenThoughts-Agent[^34] | 95 种策略中的前 4 个来源 | Daytona 沙箱 + terminus-2 | GLM-4.7-AWQ | 去掉少于 5 轮的轨迹 | 100K 条 | Qwen3-32B 七基准平均 44.8% |

### 9.1 从 ReAct 轨迹到智能体指令微调语料

ToolLLM 的工具来自 RapidAPI Hub，过滤后保留 3,451 个工具，共 16,464 个 RESTful API，覆盖 49 个类别[^185]。指令与解题路径都由 ChatGPT 生成[^185]。即便 GPT-4 也常找不到有效路径，作者因此用深度优先决策树搜索（DFSDT）代替单路径 ReAct，只保留通过的路径，共得到 126,486 个（指令，路径）对[^185]。以 ChatGPT 标注时，DFSDT 的平均通过率为 63.8，ReACT 为 35.3[^185]。以此微调的 ToolLLaMA（LLaMA-2 7B）在 DFSDT 推理下平均通过率为 66.7，教师 ChatGPT-DFSDT 为 64.8[^185]。这组对比除检索器变体外都直接给定标准 API 集合（oracle 检索器）[^185]。评测采用基于 ChatGPT 的 ToolEval，其通过率判定与人工标注的一致率为 87.1%[^185]。按其判定规则，穷尽调用仍得不到有用信息而放弃，也记为通过[^185]。

AgentTuning 把对象扩展到六类交互环境：有训练集的任务直接取训练集指令，操作系统与数据库任务用 Self-Instruct 和任务派生构造指令[^186]。GPT-4 作为智能体与环境交互，除 Mind2Web 放宽阈值外，只保留最终奖励 r = 1 的轨迹[^186]。35,341 条指令最终只留下 1,866 条轨迹，保留率 5.29%，Mind2Web 仅为 0.52%[^186]。派生任务的轨迹缺少思考，由 GPT-4 补写[^186]。在 7B 规模上，未过滤轨迹的 held-in/held-out 得分为 1.34/0.47，过滤后为 1.96/0.65[^186]。只用智能体数据时，AgentLM-7B 的 held-out 仅 0.09，与 ShareGPT 按 η = 0.2 混合后为 0.67[^186]。AgentLM-70B 的 held-out 得分为 1.40，GPT-3.5 为 1.49[^186]。但在 7B 与 13B 上，混合训练的 held-out 提升与只用通用数据几乎相同[^186]。10-gram 检查显示 WebShop 污染率达 47.18%，作者归因于任务中的价格约束，总体结论是未见泄漏[^186]。

FireAct 让 GPT-4 借助 Google 搜索，以 ReAct、CoT 与 Reflexion 解答 HotpotQA 训练题，成功轨迹统一转成 ReAct 格式[^187]。用 500 条成功轨迹微调后，Llama-2-7B 的 EM 从少样本提示的 14.8 升至 26.2，GPT-3.5 从 31.4 升至 39.2[^187]。结论只来自一种任务和一种工具[^187]。

Agent-FLAN 以 AgentInstruct 与 ToolBench 为基础数据，主要工作是重组已有语料[^188]。其诊断是，现有语料把格式遵循与推理纠缠在一起，偏离预训练分布，并会引入幻觉[^188]。作者把 ReAct 模板改写为多轮对话，ToolBench 部分只保留含 FinalAnswer 的样本，全集共 24,703 条[^188]。gpt-3.5-turbo 在不提供工具时回答的 761 条查询被用作负样本，用来教模型判断何时不该调用工具[^188]。相同数据量下，Llama2-7B 的综合得分为 41.7，重新实现的 AgentTuning 为 38.2[^188]。负样本使 ReAct 格式幻觉率从 15.6 降至 9.9，但所用的 Agent-H 是作者自建的基准[^188]。

这几项工作确立了此后多数管线沿用的流程：更强的模型在环境中执行任务，按结果保留成功轨迹，再对学生做监督微调（本文判断，依据见[^185][^186][^187]）。其中的思维链多为每步一句的 ReAct 思考，并常由另一个模型补写或改写（本文判断，依据见[^186][^188]）。held-in 评测取自训练环境的同分布划分，其分数不宜直接当作泛化能力（本文判断，依据见[^186]）。

### 9.2 数学与代码中的工具集成推理

ToRA 的轨迹由推理文本、程序与执行输出交替构成[^189]。GPT-4 在 GSM8k 与 MATH 训练集上生成至多 3 轮交互的轨迹，只保留答案正确且无工具错误者[^189]。最终为 98.2% 的 GSM8k 题和 83.1% 的 MATH 题得到轨迹，共 16k 条[^189]。第二阶段称为输出空间塑形：模仿学习后的模型每题采样 64 条轨迹[^189]。错误轨迹多在中途才出错，作者截取其前缀，由在 ToRA-Corpus 上训练的 CodeLLaMA-34B 教师补全[^189]。合并后共 69k 条训练标注[^189]。ToRA-Code-34B 在 MATH 上达到 50.8%，GPT-4 CoT 为 42.5%[^189]。输出空间塑形使 GSM8k 与 MATH 平均分别提升 3.4 与 4.0 个百分点[^189]。去掉推理文本后，ToRA-Code-7B 的 MATH 得分从 44.6 降至 36.8[^189]。

ReTool 同样使用文本与代码交错的轨迹，但训练重心转向强化学习（本文判断，依据见[^189][^190]）。冷启动数据取自 Open-Thoughts 等数学数据，经人工专家与 DeepSeek-R1 筛选[^190]。作者把其中的手工计算替换为代码及其解释器输出，并剔除答案不符的样本[^190]。随后用 PPO 训练，策略与代码沙箱多轮交互，答案等价得 1 分，否则得 −1 分[^190]。以 Qwen2.5-32B-Instruct 为骨干，ReTool 训练 400 步后 AIME2024 为 67.0%，先做文本冷启动再做文本强化学习超过 1000 步只有 40.0%[^190]。只做代码冷启动、不做强化学习为 40.9%[^190]。外部基线分数引自文献，冷启动集与强化学习题集的规模均未报告（本文判断，依据见[^190]）。

两项工作处理难题的方式不同（本文判断）。ToRA 用教师补全学生错误轨迹的后半段，把失败样本转成有效监督[^189]。ReTool 让模型在执行反馈下自行探索，学习信号来自结果奖励[^190]。只按结果过滤会使数据集中在教师已能解出的题上，难题要靠修正或强化学习进入训练（本文推断，依据见[^189][^190]）。

### 9.3 函数调用与多轮工具数据

APIGen 从 ToolBench 的 RapidAPI 工具池中清洗出可执行 API，加上 Python 函数共 3,673 个[^192]。每条数据依次经过格式检查、真实执行与语义检查，通过者回流种子池[^192]。不同生成器的通过率差异很大，DeepSeek-Coder-33B 为 34.42%，DeepSeek-V2-Chat 为 84.15%[^192]。作者公开了约 60,000 条数据[^192]。用 APIGen 数据训练的 xLAM-7B 在 2024 年 6 月 15 日的 BFCL 榜单上以 85.65 排第 6，GPT-4o-2024-05-13 以 82.94 排第 11[^192]。把执行与语义检查剔除的数据加回训练后，BFCL 成绩下降，小模型降幅更大[^192]。APIGen 只实现了单轮调用[^192]。

ToolACE 的工具本身也是合成的，前沿模型驱动的智能体从预训练语料的 API 文档中演化出 390 个领域的 26,507 个 API[^191]。对话由用户、助手、工具三个 LLM 智能体模拟生成，待训练模型以自身损失评估样本复杂度[^191]。验证分规则层与模型层，无需实际执行[^191]。在同为 25,000 条样本、同一 LLaMA-3.1-8B-Instruct 底座的对照中，BFCL 总分为 ToolACE 58.19、xLAM 40.51、ToolLLM 24.90[^191]。双层验证的数据量更小，却优于只做规则检查和不做验证的数据[^191]。作者也指出，按复杂度采样可能让模型停留在舒适区[^191]。

APIGen-MT 把函数调用扩展到多轮人机交互，任务取自 τ-bench 零售与航空领域的 15 个读 API、13 个写 API 及业务策略[^193]。LLM 先生成带标准动作的任务蓝图并经评审委员会审核，再由模拟用户与 gpt-4o 智能体对话生成轨迹[^193]。只保留最终环境状态与输出都和蓝图一致的轨迹，每个任务最多尝试 3 次[^193]。在 τ-bench 上，xLAM-2-70b-fc-r 的 pass@1 为 56.2%，GPT-4o 为 52.9%[^193]。训练同时混入了其他函数调用与智能体数据，任务又取自评测基准本身的 API 与策略，正文未见去污染检查（本文判断，依据见[^193]）。

TOUCAN 从约 2,800 个 MCP 服务器中筛出 495 个可远程访问、无需凭证者，由五个开源 LLM 生成任务[^199]。GPT-OSS-120B、Kimi-K2、Qwen3-32B 在两种智能体框架下真实调用工具生成轨迹，再经规则检查与 LLM 评审[^199]。全集为 1,527,259 条轨迹，SFT 只用 119.3K 条高质量子集[^199]。Qwen2.5-32B-Instruct 微调后，BFCL-V3 总分从 61.73% 升至 70.45%[^199]。扩展消融显示，Qwen2.5-14B 只加核心单轮数据时 τ-bench 零售从 44.46% 降至 36.95%，加入全部扩展与多轮数据后为 48.48%[^199]。

ASTRA 从 1,585 个 MCP 服务器的 19,036 份工具文档出发，以随机游走采样工具链，再由 LLM 合成任务[^14]。已部署的服务器真实调用，只有文档的服务器由有状态模拟器返回结果，并以 20% 的概率注入失败[^14]。轨迹由七维自动评分取均值评估，全程无人工标注，最终得到 54,885 条多轮 SFT 样本[^14]。强化学习环境由问答分解后编译为沙箱代码，执行结果包含目标答案才算有效[^14]。奖励按子任务完成度与调用效率的 F1 计算，只优化召回会使轮数暴涨直至训练崩溃[^14]。Qwen3-32B 的 BFCL-MT 总分经 SFT 从 47.88 升至 52.13，再经强化学习升至 64.25[^14]。

MidTool 把智能体轨迹前移到中期训练[^40]。其 20.3B token 的语料中，原生智能体轨迹为 1.8B token、0.42M 条[^40]。原生轨迹分支由 GPT-5、GPT-5.1、GPT-5.2 生成，按轮次顺序、模式对齐、必需参数与返回一致性校验，不合格者带反馈重试后丢弃[^40]。这部分还混入了 AWM 合成环境中的 rollout 与过滤后的 Nemotron Agentic 轨迹[^40]。Qwen3-4B-Base 与 Qwen3-8B-Base 经中期训练再做 SFT，在 BFCL、τ²-Bench 与 MCP-Universe 上都优于只做 SFT 的基线[^40]。

模拟执行与真实执行的取舍尚无定论（本文判断）。ToolACE 不经执行，仍在 BFCL 等量对照中领先[^191]。APIGen 与 TOUCAN 坚持真实执行[^192][^199]。按 MidTool 的说明，BFCL 尤其适合单独考查工具选择、参数构造与幻觉，τ²-Bench 则考查多步执行与恢复[^40]。由此推断，模拟返回足以教会调用格式与工具选择，多轮环境基准则更依赖多轮且有真实观测的交互数据（本文推断，依据见[^40][^191]）。TOUCAN 中只加单轮数据会拉低 τ-bench 零售分数，与这一推断相容（本文推断，依据见[^199]）。

### 9.4 软件工程环境与轨迹

软件工程场景的瓶颈主要在可执行环境（本文判断，依据见[^194][^195]）。SWE-Gym 从 358 个仓库提取 64,689 个原始任务，验证后只留下 11 个仓库的 2,438 个任务[^194]。这一步约需 200 小时人工标注与 10,000 CPU 核时，所选仓库与 SWE-Bench 不重合[^194]。OpenHands 智能体经拒绝采样得到 491 条成功轨迹，未解决的有 5,557 条[^194]。以此微调 Qwen2.5-Coder-32B，SWE-Bench Verified 解决率提高 13.6 个百分点至 20.6%[^194]。性能在 491 条时仍未饱和，作者认为瓶颈在采样预算[^194]。在线自我改进有限，32B 模型从 19.0% 升至 19.7% 后不再提升[^194]。

R2E-Gym 从提交中筛选代码变更，用已有或生成的 Fail→Pass 测试作判据，并以测试为条件反向翻译出问题描述[^196]。8.1K 个任务去掉与 SWE-Bench 仓库重叠者后剩 4,578 个，Sonnet-3.5-v2 在其上产出 3,321 条成功轨迹[^196]。32B 学生在 Verified 上 pass@1 为 34.4%，用 SWE-Gym 数据为 20.6%[^196]。受控消融中，带思考训练为 34.4，不带思考为 30.4[^196]。各用 400 条轨迹时，合成描述为 27.8，真实 issue 为 28.0[^196]。混合验证器使 Best@26 达到 51.0[^196]。无执行验证器若去掉轨迹、只看最终补丁，Best@26 从 42.8% 降至 37.6%[^196]。

SWE-smith 向可运行的仓库注入缺陷，只保留让原本通过的测试失败的补丁，再由 LM 撰写 issue[^195]。作者在 128 个仓库上构造了 50,137 个任务，花费约 1360 美元[^195]。专家智能体在 17,906 次尝试中解决 6,457 次，解决率 36%[^195]。反复解出的容易任务会损害学生，因此每个任务最多保留 3 条，最终由 Claude 3.7 Sonnet 生成的训练轨迹为 5,016 条[^195]。SWE-agent-LM-32B 在 Verified 上单次 pass@1 为 40.2%[^195]。在双方都报告的 500 条轨迹规模下（专家改用 Claude 3.5 Sonnet），32B 模型为 28.2%，相对 SWE-Gym 与 R2E-Gym 的差异为 +8.2% 与 +0.7%[^195]。R2E-Gym 的 51% 来自每个实例尝试 26 次，不可直接比较[^195]。在 issue 中给出 Fail-to-Pass 测试会使学生跳过复现步骤，性能反而下降[^195]。

两项消融都表明，模型生成的问题描述与真实 issue 训练效果相当[^195][^196]。SWE-Gym 约 200 小时人工得到 2,438 个任务，SWE-smith 约 1360 美元得到 50,137 个任务[^194][^195]。教师解决率普遍偏低，只留成功轨迹会使训练集偏向教师能解的任务，SWE-smith 对重复解出任务设限，说明这种偏向会伤害学生（本文推断，依据见[^194][^195]）。同属软件工程场景的 Hindsight Hint Distillation 在第 6 节讨论。

### 9.5 网页与深度研究任务的合成及抗捷径设计

AgentTrek 从 RedPajama 中挖掘网页操作教程作为任务说明[^198]。GPT-4o 视觉语言智能体在 BrowserGym 中按教程于真实网站回放，GPT-4o 评估器判定轨迹是否正确，准确率为 84.0%[^198]。回放成功率为 39.9%，每 1,000 条有效轨迹约花费 550.75 美元[^198]。在 400 个任务的对照中，按教程执行的成功率为 52%，只给高层目标时为 15.78%[^198]。微调后的 Qwen2.5-32B-Instruct 在 WebArena 上为 22.40，GPT-4o 为 13.10[^198]。在 Multimodal-Mind2Web 上，数据比例从 20% 增至 100% 时，跨域步骤成功率由 39.5% 升至 45.0%，人工标注的 Mind2Web 训练数据为 47.7%[^198]。

WebSailor 的 SailorFog-QA 从 Wikidata 模糊实体出发，在真实网站上随机游走建图，采样子图生成问答，并刻意模糊日期、名称与数量[^197]。开源推理模型生成轨迹后，作者丢弃其冗长的原生思考，只保留成功的动作与观测，再由另一模型以短思维链风格重建每步思考[^197]。保留条件为答案正确、不超过 32k token、调用多于 5 次，冷启动集只有 2k 余条，随后做 DUPO 强化学习[^197]。o4-mini 在 SailorFog-QA 上的 pass@1 为 47.3，在 WebDancer 训练集上为 90.2[^197]。WebSailor-72B 在 BrowseComp-en 上为 12.0[^197]。作者承认部分问题答案不唯一，强化学习只跑了 50 步[^197]。思考重建没有与原生思考的对照消融（本文判断，依据见[^197]）。

OpenResearcher 把搜索环境搬到离线：约 6K 道 MiroVerse 问答先用问题与答案拼接的查询在线检索一次，得到 10K 篇金标文档，再并入 15M 篇 FineWeb 文档[^202]。看不到答案的 GPT-OSS-120B 用 search、open、find 三个原语求解[^202]。轻量过滤后得到 97K+ 条轨迹，按答案正确拒绝采样后约 55K 条用于 SFT[^202]。Nemotron-3-Nano-30B-A3B 微调后在 BrowseComp-Plus 上为 54.8%，比基座高 34.0 个百分点[^202]。去掉金标文档后，下游成绩从 54.81% 降至 6.35%[^202]。合成共发起 5.76M 次搜索，按商业 API 估算需 5,760 至 28,800 美元[^202]。

QUEST 先构造评分标准，再由标准导出问题：智能体以热点关键词为种子浏览网页，把可验证约束组织成评分树，GPT-5 再为每题生成 Python 评测脚本[^29]。严格过滤使客观题从 17,000 道降至 5,934 道[^29]。对 50 道题的人工审查发现 2 个脚本无法执行，6 个存在评分错误，其中一类只核对答案字面[^29]。Tongyi DeepResearch 每题展开 5 次，达标轨迹进入 SFT，全部失败的 864 道客观题留给强化学习[^29]。以 Qwen3.5-35B-A3B 为底座、共用 8K 道任务训练的 Quest-35B 在 GAIA 上为 80.8%，GPT-5 为 76.4%[^29]。

FORT-Searcher 指出，结构复杂的任务在真实检索下仍可能有廉价路径，例如线索选择性过强、多条线索共享同一证据、可直接搜索或可由先验给出[^33]。对应的控制包括长尾实体、多源证据、派生事实与数值模糊化[^33]。草稿交由求解智能体实际求解，检索代价低于阈值者被改写，改写解决了 70% 的易走捷径草稿[^33]。在 3000 道题的累积消融中，逐项移除控制后求解准确率从 64.2 升至 92.0[^33]。同等训练设置下，完整配置数据训练出的学生 BrowseComp 为 61.9，两种代表性消融配置分别降至 58.1 与 54.9[^33]。把开源数据的平均检索代价从 30.0 提到 100.0，BrowseComp 从 55.7 升至 60.7，检索代价相同的 FORT 数据为 63.9[^33]。人工审查 150 道题，答案正确率不低于 94%[^33]。DeepSeek-V4-Pro-0813 生成的 40K 条成功轨迹只做 SFT，不启用上下文管理时，在三种规模的学生上使 BrowseComp 提升 5.3 至 18.9 个百分点[^33]。

深度研究数据的重点正在从把题做难转向堵住捷径（本文判断，依据见[^33][^197]）。只有 FORT 用匹配检索代价的对照证明了训练价值不只来自更长的搜索（本文判断，依据见[^33]）。OpenResearcher 的金标文档消融说明，环境覆盖不足时难度设计无从生效（本文推断，依据见[^202]）。

### 9.6 智能体数据的配方与蒸馏

OpenThoughts-Agent 把 OpenThoughts 的消融方法用于多轮智能体数据[^34]。每组消融由 GLM-4.7-AWQ 在 Daytona 沙箱中生成 10,000 条轨迹，对 Qwen3-8B 做 SFT，共 100 多组受控实验[^34]。任务来源是最重要的因素之一，95 种生成策略之间 SWE-Bench Verified-100 最多相差 30 个百分点[^34]。混合前 4 个来源优于只用第一名，对任务描述的各种增强干预则都没有超过保持原样[^34]。基准表现最强的 GPT-5.3-Codex 作教师时，Terminal-Bench 2.0 成绩比 GLM-4.7-AWQ 低约 5%[^34]。去掉少于 5 轮的轨迹收益最大，在约 145M token 的等量预算下仍比随机子集平均高 3.5 个百分点[^34]。最终 100K 条数据训练的 Qwen3-32B 在七个智能体基准上平均 44.8%，比 Nemotron-Terminal-32B 高 3.9 个百分点[^34]。

数据规模的收益并不一致（本文判断）。Agent-FLAN 只用 25% 的数据就获得了大部分增益[^188]。SWE-Gym 在 491 条轨迹时仍未饱和[^194]。OpenThoughts-Agent 对同一批任务追加采样，性能在 31.6K 到 100K 之间进入平台期，改写扩充 Tezos 的 997 个基础问题后则继续上升[^34]。作者据此认为瓶颈在任务描述的多样性[^34]。短格式调用数据很快饱和，长程任务的增长更多来自覆盖更多不同任务（本文推断，依据见[^34][^188][^194]）。

Agent Distillation 在同一教师、同一批题目下比较思维链蒸馏与智能体蒸馏[^200]。智能体框架为 CodeAct，动作以代码表达并接收执行反馈[^200]。教师 Qwen2.5-32B-Instruct 在 1000 道 HotPotQA 与 2000 道 MATH 上每题采样一条，去掉错误后约 2,000 条[^200]。教师作为智能体时在训练集 MATH 难题上为 58.4，不如 CoT 提示的 71.1[^200]。把 CoT 的第一步推理作为智能体首个思考的前缀后，该值回升到 67.1[^200]。在 8 个基准的平均分上，7B 学生做 CoT 蒸馏为 33.54，做智能体蒸馏为 39.85，加上前缀与测试时自洽动作生成为 42.68[^200]。但 3B 与 7B 智能体在 MATH500 上仍落后于 CoT 蒸馏[^200]。

π-Distill 面对的约束是，前沿模型在多轮环境中通常只暴露动作而隐藏推理[^201]。作者从 DeepSeek-chat-v3.1 采集成功轨迹，把动作转成特权信息，供与学生共享权重的教师使用[^201]。在 Qwen3-8B 上，π-Distill（α = 1）在 Travel Planner 上为 44.1%，带 CoT 的 SFT 加强化学习为 32.3%[^201]。在 τ-Bench 零售上两者为 29.7% 与 29.1%，可见推理的教师 DeepSeek V3.1 为 51.3%[^201]。实验模型不超过 8B，Travel Planner 原有的评分奖励曾被模型钻空子而需修改[^201]。

另有两项工作把合成对象扩展到求解轨迹之外（本文判断）。Unfolding Papers 让教师模型为 1.8M 篇论文反向重建写作请求、规划与各节写作前的思考，正文保持原文，得到约 60B token 的继续预训练语料[^41]。其写作提升超过用同批论文原文继续预训练，但重建的思考是否符合作者真实思路无从验证[^41]。Recursive Harness Self-Improvement 让合成框架本身迭代，只有在成本受控时生成更难且有效的任务才采纳修改，验证器保持冻结[^53]。经 14 轮演化，三个领域的平均求解器准确率从 100.0% 降至 54.8%[^53]。作者指出，要分离框架演化本身的下游贡献，还需在固定框架与演化框架的数据上做等 token 训练对照[^53]。

### 9.7 成功过滤之争：只留正确轨迹是否必要

按结果过滤是本节多数管线的默认步骤，但文献对其必要性给出了相反的证据（本文判断，依据见[^186][^194][^202]）。支持过滤的证据来自短交互与函数调用场景（本文判断）。AgentTuning 在 7B 上过滤后 held-in/held-out 为 1.96/0.65，未过滤为 1.34/0.47[^186]。APIGen 把被剔除的数据加回训练后 BFCL 成绩下降[^192]。ToolACE 的双层验证数据优于只做规则检查和不验证的数据[^191]。

相反的证据来自长程搜索（本文判断）。OpenResearcher 固定学生、训练配方与评测协议，只改变 SFT 轨迹子集，只用正确轨迹为 54.81%，只用错误轨迹为 55.06%，全部轨迹为 54.46%[^202]。作者认为失败轨迹同样示范了搜索结构、工具顺序、证据检查与停止行为，并提醒不要过度解读三者的排序[^202]。OpenThoughts-Agent 所列的轨迹过滤是超时、子代理与轮数等启发式规则，笔者未在正文中检索到按任务成败筛选的步骤（本文判断，依据见[^34]）。APIGen-MT 也承认，被丢弃的失败轨迹可能含有对比信号[^193]。

至少四个变量可以解释这一分歧（本文推断）。其一是失败的含义不同：APIGen 剔除的是格式错误、执行失败或语义不符的调用[^192]。OpenResearcher 的轻量过滤已去掉超长、格式错误与未得出结论的轨迹[^202]。若其错误轨迹取自过滤后的池子，它们就是格式完整、只在最终答案上出错的长程搜索（本文推断，依据见[^202]）。其二是轨迹长度：OpenResearcher 的失败轨迹平均调用工具 71.7 次，成功轨迹为 38.4 次[^202]。OpenThoughts-Agent 在等 token 预算下仍发现多轮轨迹有增益[^34]。长程任务中，过程携带的监督可能多于最终答案的对错（本文推断，依据见[^34][^202]）。其三是环境覆盖与判据可靠性：去掉金标文档使 OpenResearcher 的下游成绩从 54.81% 降至 6.35%，远大于正确性过滤造成的不到 0.6 个百分点（本文判断，依据见[^202]）。作者也指出，语料缺证据时，失败无法区分是策略不佳还是证据缺失[^202]。判据本身由模型给出时，只留正确轨迹同样含噪（本文判断）。ToolLLM 评测所用的 ToolEval 就把穷尽调用后放弃判为通过[^185]。其四是学生容量与样本量：AgentTuning 的过滤对照在 7B 上进行，过滤后的 AgentInstruct 只有 1,866 条轨迹[^186]。APIGen 中未经验证的数据对小模型伤害更大[^192]。OpenResearcher 的学生是 Nemotron-3-Nano-30B-A3B[^202]。按 56.7% 的教师成功率推算，若未做下采样，三组训练集的规模应各不相同，论文未说明是否做了等量处理（本文推断，依据见[^202]）。

据此，短程、结构化且判据可执行的场景宜坚持结果过滤（本文判断，依据见[^186][^191][^192]）。长程搜索中可以保留格式完整的失败轨迹，预算更应投向环境覆盖和轨迹长度（本文判断，依据见[^34][^202]）。

### 9.8 小结（本文判断）

- 主流范式是过滤式行为克隆，即由更强的模型在环境中执行任务、按结果保留轨迹、再对学生做 SFT，轨迹中的思维链多为每步短思考，并常由另一个模型补写或重建（依据见[^186][^194][^197]）。
- 数据瓶颈已从轨迹转向任务与环境：任务来源之间的差异可达 30 个百分点，模型生成的问题描述与真实 issue 效果相当，SWE-smith 以约 1360 美元构造了 50,137 个任务（依据见[^34][^195][^196]）。
- 成功判据覆盖从模型评审到执行测试、程序化评分的谱系，各类判据都有已记录的失效方式，包括放弃也算通过、无执行验证器依赖风格特征、评分脚本只核对字面答案（依据见[^29][^185][^196]）。
- 深度研究任务的合成以抗捷径为核心约束，训练价值要用匹配检索代价的对照来证明，环境覆盖是难度设计生效的前提（依据见[^33][^202]）。
- 是否只留正确轨迹取决于失败的含义、轨迹长度、环境覆盖与学生容量，短程结构化任务应过滤，长程搜索可保留格式完整的失败轨迹（依据见[^186][^192][^202]）。
- 开放问题包括：SFT 之上的强化学习证据仍少，训练任务与评测基准同源的污染缺少检查，原生思考、重建思考与只给动作三种监督形式缺少同条件对照（依据见[^14][^193][^201]）。

## 参考来源

[^185]: [Qin et al. — ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs (arXiv 2307.16789, 2023-07)](https://arxiv.org/abs/2307.16789)
[^186]: [Zeng et al. — AgentTuning: Enabling Generalized Agent Abilities for LLMs (arXiv 2310.12823, 2023-10)](https://arxiv.org/abs/2310.12823)
[^187]: [Chen et al. — FireAct: Toward Language Agent Fine-tuning (arXiv 2310.05915, 2023-10)](https://arxiv.org/abs/2310.05915)
[^189]: [Gou et al. — ToRA: A Tool-Integrated Reasoning Agent for Mathematical Problem Solving (arXiv 2309.17452, 2023-09)](https://arxiv.org/abs/2309.17452)
[^190]: [Feng et al. — ReTool: Reinforcement Learning for Strategic Tool Use in LLMs (arXiv 2504.11536, 2025-04)](https://arxiv.org/abs/2504.11536)
[^192]: [Liu et al. — APIGen: Automated Pipeline for Generating Verifiable and Diverse Function-Calling Datasets (arXiv 2406.18518, 2024-06)](https://arxiv.org/abs/2406.18518)
[^191]: [Liu et al. — ToolACE: Winning the Points of LLM Function Calling (arXiv 2409.00920, 2024-09)](https://arxiv.org/abs/2409.00920)
[^193]: [Prabhakar et al. — APIGen-MT: Agentic Pipeline for Multi-Turn Data Generation via Simulated Agent-Human Interplay (arXiv 2504.03601, 2025-04)](https://arxiv.org/abs/2504.03601)
[^199]: [Xu et al. — TOUCAN: Synthesizing 1.5M Tool-Agentic Data from Real-World MCP Environments (arXiv 2510.01179, 2025-10)](https://arxiv.org/abs/2510.01179)
[^14]: [Tian et al. — ASTRA: Automated Synthesis of agentic Trajectories and Reinforcement Arenas (arXiv 2601.21558, 2026-01)](https://arxiv.org/abs/2601.21558v2)
[^40]: [Jiang et al. — MidTool: Mid-training Data Synthesis for Agentic Tool Use (arXiv 2608.20314, 2026-08)](https://arxiv.org/abs/2608.20314v1)
[^194]: [Pan et al. — Training Software Engineering Agents and Verifiers with SWE-Gym (arXiv 2412.21139, 2024-12)](https://arxiv.org/abs/2412.21139)
[^196]: [Jain et al. — R2E-Gym: Procedural Environments and Hybrid Verifiers for Scaling Open-Weights SWE Agents (arXiv 2504.07164, 2025-04)](https://arxiv.org/abs/2504.07164)
[^195]: [Yang et al. — SWE-smith: Scaling Data for Software Engineering Agents (arXiv 2504.21798, 2025-04)](https://arxiv.org/abs/2504.21798)
[^198]: [Xu et al. — AgentTrek: Agent Trajectory Synthesis via Guiding Replay with Web Tutorials (arXiv 2412.09605, 2024-12)](https://arxiv.org/abs/2412.09605)
[^197]: [Li et al. — WebSailor: Navigating Super-human Reasoning for Web Agent (arXiv 2507.02592, 2025-07)](https://arxiv.org/abs/2507.02592)
[^202]: [Li et al. — OpenResearcher: A Fully Open Pipeline for Long-Horizon Deep Research Trajectory Synthesis (arXiv 2603.20278, 2026-03)](https://arxiv.org/abs/2603.20278)
[^29]: [Xie et al. — QUEST: Training Frontier Deep Research Agents with Fully Synthetic Tasks (arXiv 2605.24218, 2026-05)](https://arxiv.org/abs/2605.24218v1)
[^33]: [Deng et al. — FORT-Searcher: Synthesizing Shortcut-Resistant Search Tasks for Training Deep Search Agents (arXiv 2606.12087, 2026-06)](https://arxiv.org/abs/2606.12087v2)
[^34]: [Raoof et al. — OpenThoughts-Agent: Data Recipes for Agentic Models (arXiv 2606.24855, 2026-06)](https://arxiv.org/abs/2606.24855v1)
[^188]: [Chen et al. — Agent-FLAN: Designing Data and Methods of Effective Agent Tuning for Large Language Models (arXiv 2403.12881, 2024-03)](https://arxiv.org/abs/2403.12881)
[^200]: [Kang et al. — Distilling LLM Agent into Small Models with Retrieval and Code Tools (arXiv 2505.17612, 2025-05)](https://arxiv.org/abs/2505.17612)
[^201]: [Penaloza et al. — Privileged Information Distillation for Language Models (arXiv 2602.04942, 2026-02)](https://arxiv.org/abs/2602.04942)
[^41]: [Xu et al. — Unfolding Scientific Papers into Multi-Turn Generation Trajectories for Continued Pre-Training (arXiv 2608.25826, 2026-08)](https://arxiv.org/abs/2608.25826v2)
[^53]: [Zhang et al. — Recursive Harness Self-Improvement for Frontier Reasoning Data Synthesis (arXiv 2610.03548, 2026-10)](https://arxiv.org/abs/2610.03548v1)
