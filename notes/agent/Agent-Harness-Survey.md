# Agent = Model + Harness：大模型 Harness 深度调研

中文 | [English](./Agent-Harness-Survey_en.md)

- **调研日期**: 2026-10-20
- **范围**: 大模型领域的 agent harness，包括定义与组成、主流产品、效果的正反证据、自动化 harness 优化、训练闭环和评测。资料主要覆盖 2025 年底至 2026 年 10 月的论文、厂商工程博客和开源项目。
- **依据**: 句末的上标数字是引用，对应文末的参考来源。标有（推断）、（归纳）或（估算）的内容，是根据所引资料作出的推断、归纳或估算。
- **时效**: GitHub 星数取自 2026-10-20 的仓库页面，只反映开发者关注度。产品状态变化很快，以官方页面为准。

## 结论先行

- **定义已经收敛**：harness 指模型之外的全部代码、配置和执行逻辑，包括系统提示、工具与 Skills/MCP、沙箱、编排、hooks 和上下文管理[^1]。它也叫 agent scaffolding，常写作 agent = model + harness[^2]。
- **产品已成规模**：按 GitHub 星数，开源 harness 中领先的是 OpenClaw（约 39.3 万）、Hermes Agent 和 DeepSeek Harness（各约 25.5 万）[^65][^62][^52]。其后是 OpenCode（约 21.8 万）和 Claw Code（约 19.5 万）[^64][^70]。（归纳）主要模型厂商几乎都推出了自家 harness，IDE 和工具厂商也把各自的 agent 做成了 CLI 和 SDK，详见第 3 节。
- **收益有条件**：约束紧、通用 harness 与模型的训练方式不匹配、或任务超出模型独立完成的能力时，换 harness 可以让分数翻几倍，例如 ARC-AGI-3 从 13.3% 升到 38.3%[^16]。条件宽松时，SWE-bench Verified 的 447 题上，最重和最轻的 harness 在 5 分以内等价；在 45 道难题上，换 harness 翻转的任务比例与同配置重跑相同，都是 13%[^19]。harness 稳定决定的是账单：同模型、同任务、同价目表，单任务成本最多相差 3 倍[^19]。
- **排行榜要打折读**：Terminal-Bench 2.0（TB2）上同为 Opus 4.6，Claude Code 得 58.0%，ForgeCode 得 81.8%[^13]。但据第三方追踪站汇总，榜首多为维护者未核验的自报结果，置信区间相互重叠，TB2 也因 89 题中 28 题有缺陷而被替换[^21]。仅资源配置一项就能让 TB2 分数相差 6 个百分点[^20]。
- **Harness 成了优化对象**：Meta-Harness、Self-Harness、VERSE 等把 harness 当作可搜索的代码[^13][^26][^27]。VERSE 的对照实验表明，没有执行验证时，优化器的自我进化不起作用[^27]。
- **Harness 进入了训练闭环**：LangChain 指出 Claude Code、Codex 等产品在后训练时就把 harness 放进了循环[^1]。新一代 RL 框架把交互循环交给部署时的 harness，带来重分词、样本合并、优势计算和 loss 归一化等新问题[^38]。交替优化 harness 与 policy 时，联合增益大于两者单独增益之和[^36]。

## 1. "Harness" 指什么

### 1.1 五种用法

| 用法 | 范围 | 代表 |
| --- | --- | --- |
| Agent harness（运行时，又称 scaffold） | 系统提示、工具/Skills/MCP、沙箱、编排、hooks、上下文管理 | Claude Code、Codex、OpenCode、Pi、Hermes Agent 等，见第 3 节[^1][^9] |
| 用户侧 outer harness | `AGENTS.md`、skills、自定义 linter、结构测试、pre-commit hook | Hashimoto、OpenAI、Böckeler[^3][^4][^6] |
| 评测 harness | 跑任务、记录轨迹、打分、汇总 | lm-eval、HAL、Harbor[^43][^18][^44] |
| 训练 harness / RL 环境 | rollout 循环、工具执行、奖励 | verl Agent Loop、Agent Lightning、Uni-Agent[^42][^38][^39] |
| 传统 test/fuzz harness | 驱动被测代码的程序 | OSS-Fuzz-gen 用 LLM 生成 fuzz harness[^54] |

Wikipedia 也把软件测试的 test harness、LLM 基准的评测 harness 和 RL 中包裹智能体的环境列为相关概念[^2]。Böckeler 区分了两层：coding agent 内置的那部分 harness（系统提示、检索机制、编排），以及用户在其上为自己的场景搭建的 outer harness[^6]。

**与 prompt/context engineering 的关系**：一种常见框架是，prompt engineering 优化单次交互，context engineering 管理模型某一时刻看到什么，harness engineering 设计整个运行环境并包含前两者[^2]。Böckeler 把用户侧 harness 视为 context engineering 的一种特定形式[^6]；LangChain 则说，今天的 harness 主要是交付上下文工程的载体[^1]。（推断）两种说法并不矛盾：context engineering 回答"给模型看什么"，harness engineering 还要回答"模型在什么环境里、按什么循环运行，由什么来验证"。

### 1.2 时间线

| 时间 | 事件 |
| --- | --- |
| 2023 | 英国 AI Security Institute 把 AI agent 描述为模型加 scaffolding[^2] |
| 2025-10 | HAL 发布标准化评测 harness，按模型 × scaffold × benchmark 三维分析[^18] |
| 2025-11-26 | Anthropic 发表《Effective harnesses for long-running agents》，称 Claude Agent SDK 为通用 agent harness[^7] |
| 2026-01-23 | OpenAI 发表《Unrolling the Codex agent loop》，把 Codex 的 agent 称为 harness[^48] |
| 2026-02-05 | Mitchell Hashimoto 提出 "Engineer the Harness"：agent 每犯一次错，就工程化地让它不再犯[^3] |
| 2026-02-11 | OpenAI 发表《Harness engineering》，介绍零手写代码、约百万行规模的内部产品[^4] |
| 2026-03-10 | LangChain 发表《The Anatomy of an Agent Harness》[^1] |
| 2026-03-30 | Meta-Harness 把 harness 当作端到端优化对象[^13] |
| 2026-03-31 | Claude Code 的 npm 包误带 source map，源码外泄[^107]；社区随即出现 Claw Code 等重写[^9] |
| 2026-04-02 | Böckeler 提出 guides/sensors 框架[^6] |
| 2026-05-19 | Google 宣布用 Antigravity CLI 接替 Gemini CLI[^86] |
| 2026-06 | Databricks 开源 meta-harness Omnigent[^9] |
| 2026-07 至 10 | 源码解剖[^9]、harness 化的 agentic RL[^38][^41]、自动 harness 优化[^27][^28]、反证研究[^19]集中出现 |
| 2026-08-13 | DeepSeek Harness 仓库建立[^71]；到 2026-10-20 星数约 25.5 万[^52] |

这个术语的归属有争议：有人归于 Hashimoto 二月的博文，也有人归于 LangChain 的 Vivek Trivedy[^2]。Böckeler 注意到 OpenAI 那篇文章全文只提到一次 "harness"，推测该词可能受 Hashimoto 启发[^5]。（推断）名词 harness 在 2025 年底的厂商文章里已经在用[^7]，2026 年初被命名的是这门学科[^9]。

## 2. 解剖：harness 由什么组成

- **七个子系统**：一项源码研究对比了 11 个生产级 harness（名单见 3.1 节），归纳出 agent loop、LLM 集成、记忆与上下文、工具与动作、安全与权限、扩展性、编排七个子系统，外加一个接口层[^9]。
- **六项运行时职责**：另一篇综述把 harness 分解为 observation、context、control、action、state、verification/governance 六项职责[^10]。
- **没人用通用框架**：语料扩大三倍、覆盖约 400 万行代码后，仍然没有一个 agent 运行时引入 LangChain、LangGraph、AutoGen 之类的通用 agent 框架，也没有一个用向量嵌入检索代码[^9]。它们靠 ripgrep、tree-sitter、glob 等确定性手段检索[^9]。
- **扩展标准**：`SKILL.md` 的采用率（11 个中有 9 个）已超过 MCP（8 个）[^9]。
- **从趋同到模仿**：一个季度内，Codex 原样采用了 Claude Code 的 hook 词汇，还提供了它的会话导入器；行为策略也从提示文本迁移到了配置[^9]。
- **复杂度不预测成绩**：这些系统的代码量相差三个数量级，但 loop 的复杂度并不能预测基准成绩[^9]。mini-SWE-agent 的极简线性循环与 OpenHands 的事件溯源引擎，成绩在同一区间[^9]。
- **厂商开放 harness**：OpenAI 开源了 Codex harness，并通过 app-server 协议让应用创建线程、启动轮次、接收事件、处理审批[^49]。Anthropic 的 Managed Agents 把 session（只追加的事件日志）、harness（调用模型并路由工具调用的循环）和 sandbox 虚拟化为三个可独立替换的接口，并自称 meta-harness[^11]。

### 2.1 有实证的设计模式

| 模式 | 针对的失败 | 做法 | 出处 |
| --- | --- | --- | --- |
| 进度外置 | 跨上下文窗口失忆；过早宣布完成 | 初始化 agent 写 feature list（JSON，200 多项，初始全部 failing）、进度文件和 git 提交；之后每轮只做一个 feature | [^7] |
| 地图式 `AGENTS.md` | 巨型指令文件挤占上下文、迅速过时 | 约 100 行的目录，docs/ 作为记录系统，linter 和 CI 校验文档新鲜度 | [^4] |
| 可执行约束 | 架构漂移 | 自定义 linter 和结构测试，错误信息里直接写修复指令 | [^4][^6] |
| 退出前验证 | 写完代码读一遍就停 | `PreCompletionChecklist` 中间件或 Ralph loop hook 拦截退出 | [^14][^1] |
| 死循环检测 | 同一方案小改 10 次以上 | 按文件统计编辑次数，超过 N 次注入"重新考虑方案" | [^14] |
| 时间预算与推理"三明治" | 超时 | 注入时间预算提醒；规划和验证用 xhigh 推理，实现用 high | [^14] |
| 上下文重置与 compaction | context anxiety | 结构化交接后开新窗口；模型行为改善后移除 | [^22][^11] |
| 生成与评审分离 | 自评过度乐观 | 独立 evaluator 用 Playwright 实际操作应用，低于阈值打回 | [^22] |
| 渐进披露与输出卸载 | 工具太多；大输出污染上下文 | Skills 启动时只加载 front-matter；超长工具输出保留首尾，全文写入文件 | [^1] |
| 垃圾回收 | agent 复制仓库里已有的坏模式 | 后台 agent 定期扫描偏差、开重构 PR | [^4] |
| 大脑与双手解耦 | 容器变成"宠物"；凭证泄露 | 沙箱作为工具 `execute(name, input) → string`；凭证不进沙箱 | [^11] |

## 3. 主流 harness 产品

源码研究认为，2026 年上半年 coding harness 完成了从工具到平台的转变[^9]。harness 变成了可导入的 SDK，框架厂商也开始发布自己的 harness[^9]。本节按出品方分组整理截至 2026-10-20 的主要产品。GitHub 星数只作关注度参考，不代表用户量或质量。

收录范围是可以直接使用的 harness，包括 coding agent 和个人助理型 agent。LangChain、AutoGen、CrewAI 这类框架不收录：论文的区分是，框架是开发者导入来构建 agent 的库，harness 是开发者在其中工作的运行时[^9]。应用生成平台和托管型通用 agent 产品也不在本节范围内。

### 3.1 源码研究覆盖的 11 个系统

这项研究按设计理念、成熟度和市场地位选样[^9]。样本包括四家主要模型厂商各自的旗舰 agent，另加七个开源项目[^9]。它只描述和比较实现方式，不做基准测试，也不排名[^9]。

| 系统 | 出品方 | 语言 / 代码规模 | 模型接入 | 执行隔离 | 论文概括的标志性设计[^9] | GitHub 星数 |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Code | Anthropic | TS / Large | 仅 Anthropic | 可选运行时 + worktree | 延迟加载工具；共享 prompt cache 的分叉；被其他系统模仿的参照 | 15.3 万[^68] |
| Codex | OpenAI | Rust / Very large | 仅 OpenAI | 原生沙箱（3 种 OS） | agent 维护的跨会话记忆；工具调用以 V8 执行的代码表达 | 13.0 万[^66] |
| Gemini CLI | Google | TS / Very large | 仅 Google | 原生沙箱（3 种 OS） | 把模型路由当作运行时调度；样本中唯一的 A2A server | 10.7 万[^67] |
| Mistral Vibe | Mistral | Python / Small | Mistral 优先，可接其他 | 可选 worktree | 中间件流水线式循环；通过 ACP 暴露回退功能 | 0.5 万[^112] |
| OpenHands | OpenHands（原 All-Hands-AI） | Python / Medium | 多家（LiteLLM） | Docker、Apptainer 或远程 | 资源加锁的并行工具；可把其他 harness 作为 ACP 后端 | 9.1 万[^73] |
| Aider | 社区（P. Gauthier），维护模式 | Python / Small | 多家（LiteLLM） | 无 | 13 种编辑格式；样本中唯一的排序式 repo map | 5.0 万[^76] |
| mini-SWE-agent | Princeton / Stanford | Python / Tiny | 多家（LiteLLM） | Docker 等 | 约 100 行实现全部七个子系统 | 0.9 万[^53] |
| Hermes Agent | Nous Research | Python / Very large | 多家（自有传输层） | 6 种可插拔执行后端 | 自我改进的 skill 循环；谱系式 compaction；verify-on-stop | 25.5 万[^62] |
| Pi | earendil-works（M. Zechner） | TS / Medium | 多家（35 家 provider） | 无（有意为之） | 一切皆扩展的内核；会话树式版本控制 | 11.7 万[^63] |
| OpenCode | Anomaly（原 SST） | TS / Large | 多家（Vercel AI SDK） | 无（靠权限策略） | client/server 架构；语法感知的命令授权 | 21.8 万[^64] |
| OpenClaw | 社区 | TS / Large | 多家 | 无 | 网关委派；每次回复前先跑记忆子 agent | 39.3 万[^65] |

- **代码规模**是论文的粗分档：Tiny 约 5,000 行，Small 2 万–4 万行，Medium 8 万–11 万行，Large 50 万行以上，Very large 60 万行以上（Codex 约 110 万行 Rust）[^9]。论文提醒，这些数字跨语言、跨统计口径不能直接比较[^9]。
- **Claude Code 的数据**来自 2026 年 3 月的源码快照[^9]。当月 Anthropic 发布的 npm 包 2.1.88 误带了 source map，泄露了近 2,000 个 TypeScript 文件、超过 51.2 万行代码[^107]。Claude Code 不是开源软件，仓库的 LICENSE 写明保留所有权利[^69]。
- **模型接入分三类**：Claude Code、Codex、Gemini CLI 只接自家模型[^9]；OpenHands、Aider、mini-SWE-agent 通过 LiteLLM 统一接入多家[^9]。Hermes、Pi、OpenCode 则集中维护各家 provider 的适配代码，论文认为它们证明了多 provider 架构也能拿到厂商原生的全部优化[^9]。

### 3.2 Hermes Agent、Pi、OpenCode 与 OpenClaw

这四个开源项目都在源码研究的样本中，代表四种不同的设计取向。DeepSeek Harness 的关注度与 Hermes Agent 相当，但它的仓库 2026-08-13 才建立[^71]，晚于该研究 2026 年 7 月的快照[^9]，放在 3.3 节。

#### Hermes Agent（Nous Research）：个人助理与编码合一

- 论文称它是增长最快的开源 harness，发布五个月内约 21.2 万星（2026-07-10 统计）[^9]。
- 它介于两类产品之间：像 OpenClaw 一样接入 Telegram、Discord、Slack 等消息渠道，又自带完整的原生编码工具集[^9]。
- **模型接入**：五种传输协议实现，背后是 29 个声明式 `ProviderProfile` 插件[^9]。
- **缓存**：每个会话按 stable、context、volatile 三层拼一次 prompt[^9]。前缀做逐位规范化（工具调用 JSON 排序后紧凑重序列化、时间戳只保留日期、记忆冻结为快照），本地 llama.cpp 和 vLLM 的 KV cache 也能跨轮命中[^9]。
- **上下文**：compaction 不改写对话记录，而是结束当前会话，再轮换到一个以 `parent_session_id` 相连的子会话[^9]。上下文管理和会话持久化因此合为一个机制，历史不会被销毁[^9]。
- **记忆**：`MEMORY.md` 限 2,200 字符、`USER.md` 限 1,375 字符，以冻结快照注入，会话中途写盘不会让 prompt cache 失效[^9]。agent 自己编写、修补和整理 skill，论文的 11 个系统里只有 Hermes 完整具备这一模式[^9]。
- **循环**：有 11 种枚举的结束原因，以及两道能否决过早最终回答的 stop-guard[^9]。其中 verify-on-stop 在本轮改了代码却没有新的验证证据时，把收尾回复改写成继续执行[^9]。
- **安全**：它是样本中最大的 Python 系统，却不带任何 OS 级隔离原语，隔离交给六种可插拔的执行后端[^9]。本地后端靠一个 3,200 行的审批模块，其中 12 条硬性底线规则在 `--yolo` 模式下依然生效[^9]。
- **编排**：默认是扁平委派[^9]。Kanban swarm 把规划、并行执行、验证和汇总放进独立的 `hermes -p <profile>` 子进程，通过 SQLite 看板协调[^9]。
- **版本**：论文分析的是 2026 年 7 月的 0.18.2 版[^9]。此后已有变化，例如主循环迭代上限的默认值从论文记录的 90 改成了 500[^9][^119]。

#### Pi（earendil-works / M. Zechner）：极简内核

- 论文把它看作"极简内核"这一反潮流的代表[^9]。它在 GitHub 上自述为 AI agent 工具包，包含统一 LLM API、agent loop、TUI 和 coding agent CLI[^63]。
- **循环**：约 790 行的函数式内核，没有规划器、反思步骤、轮数上限、卡死检测和成本熔断，模型不再调用工具时才停止[^9]。这些缺失都写进了文档，是有意的设计取舍[^9]。
- **提示**：整个系统提示由约 170 行的构建器生成，输出只有 30–40 行[^9]。几乎所有行为策略都留给用户的上下文文件和扩展[^9]。
- **扩展**：内核本身就是事件总线，约 33 种类型化事件覆盖从工具拦截到原始 provider I/O 的各个环节[^9]。核心没有 spawn 或 task 工具，子 agent 以扩展的形式提供，每次调用都起一个独立的 pi 进程[^9]。
- **会话**：会话是只追加的 JSONL 树，每条记录带 id 和 parentId，一个可移动的叶指针决定当前分支[^9]。`/tree`、`/fork`、`/clone` 把其他 harness 分开实现的检查点、回退和分支探索统一了起来[^9]。
- **安全**：它是样本中唯一把"不提供安全设施"写成设计原则的系统，文档认为进程内的不完整沙箱容易被误当成安全边界[^9]。
- **模型接入**：手写 9 种协议实现，内置 35 家 provider[^9]。使用 Claude Pro/Max 的 OAuth token 时，它会完整模仿 Claude Code 的身份来使用消费级订阅[^9]。
- **可嵌入**：`pi-agent-core` 可以作为库导入，也提供 RPC 模式[^9]。Omnigent 可以编排 Pi[^102]，Fireworks 的 RL 训练示例也支持 Pi[^40]。

#### OpenCode（Anomaly，原 SST）：client/server 架构

- 论文称它是 GitHub 上星数最多的专用 coding agent（2026-07-10 约 18.4 万）[^9]。
- **架构**：内嵌 HTTP server，发布 OpenAPI 规范和生成的 SDK；TUI、桌面、Web、IDE 插件和 CI action 都是它的客户端[^9]。约五分之三的非测试代码是这些客户端，而不是 harness 本体[^9]。
- **模型接入**：流式输出和工具分发交给 Vercel AI SDK 和 models.dev，它是样本中唯一一个底层 LLM 通路依赖第三方 SDK 的系统[^9]。它按模型 ID 子串从 9 套基础提示中选一套[^9]。
- **循环**：消息日志同时充当工作队列，因此进程重启后可以直接恢复[^9]。默认没有步数上限[^9]。连续三次完全相同的工具调用会触发 `doom_loop` 权限询问，由用户而不是 harness 判断是否出了问题[^9]。
- **安全**：它是除 Hermes 外第二大的、不带 OS 级隔离的系统，默认在项目内全部放行，与 Codex 正好相反[^9]。每条 bash 命令都先用 tree-sitter 解析再授权[^9]。
- **研究中的中立 harness**：Doc2Harness 统一用 OpenCode 构建 harness，理由是 Claude Code 和 Codex CLI 由模型厂商与自家模型一起开发，可能偏向自家模型[^32]。Harness2 用 OpenCode 和 Codex 作为冻结执行器的 harness[^30]，Fireworks 的 RL 示例支持 OpenCode、Pi 和 mini-SWE-agent 三种适配器[^40]。
- **实测**：在 SWE-bench Verified 的大题池上，OpenCode 最多落后 9 分，其中一个模型有一半差距出在被输出上限截断的运行上[^19]。

#### OpenClaw（社区）：多渠道个人助理网关

- GitHub 星数约 39.3 万[^65]，在本文列出的项目中最高。
- 它的 README 自称个人 AI 助理网关，不是 coding agent，覆盖 20 多个消息平台[^9]。它不带代码编辑工具，编码任务通过插件委派给 opencode、kimi-coding、github-copilot 等专用 agent[^9]。论文因此把它当作对照组，称它消费而不是实现编码能力[^9]。
- 每次回复前，Active Memory 插件会先运行一个专门的记忆子 agent[^9]。多 agent 通过 ACP 翻译层实现，子 agent 作为子进程拉起[^9]。
- 安全以网关的分域授权为主，区分 operator 和 node 两种连接角色[^9]。另有按 IP 或 token 限流、SSRF 策略、私信白名单和配对审批等机制[^9]。
- Agent Lightning 把 OpenClaw 和 Hermes 归为通用型 harness，与 coding harness 并列[^38]。社区还出现了一批轻量替代品，例如约 4,000 行 Python 的 nanobot、跑在容器里的 NanoClaw、能在 10 美元硬件上运行的 PicoClaw，以及用 Rust 重写并用 WASM 沙箱隔离的 IronClaw[^110]。

### 3.3 其他厂商与开源 harness

#### 模型厂商的自有 harness

论文观察到一波中国厂商的 harness（阿里的 Qwen Code、月之暗面的 Kimi CLI、字节的 Trae Agent），把开源权重模型的发布和自家 CLI 绑在一起[^9]。（归纳）到 2026 年下半年，多数主要模型厂商都有了自己的 harness。

| 产品 | 出品方 | 形态 / 许可 | 要点 |
| --- | --- | --- | --- |
| Claude Agent SDK、Claude Cowork | Anthropic | SDK；桌面与网页产品 | Anthropic 称 Claude Agent SDK 是通用 agent harness[^7]。Cowork 把 Claude Code 的 agent 能力用到编码以外的知识工作[^105]，据 Anthropic 工程师在 Hacker News 上的说明，它在 Linux VM 里运行 Claude Code 的 agent harness，并加了沙箱、网络控制和文件系统挂载[^106] |
| Antigravity CLI | Google | 闭源，Go[^9] | 2026-05-19 宣布接替 Gemini CLI，与 Antigravity 2.0 桌面应用共用架构[^86]。2026-06-18 起 Gemini CLI 停止服务免费、Google AI Pro 和 Ultra 用户，企业用户不受影响[^86]。Gemini CLI 仓库仍以 Apache 2.0 开放，继续为企业客户更新模型支持和修复[^86] |
| Grok Build | xAI（SpaceXAI） | Apache-2.0，Rust，2.7 万星[^77] | 全屏 TUI，可交互、可 headless，也能经 ACP 嵌入编辑器[^77]。论文 2026 年 7 月的版图表把它标为非开源[^9]，其 GitHub 仓库 2026-07-14 才建立[^72] |
| Muse Code | Meta | 终端与 CI | 为 Muse Spark 模型打造的 coding agent，首次运行就开启审批和 OS 沙箱[^78] |
| DeepSeek Harness | DeepSeek | MIT，25.5 万星[^52] | 开源 agent harness，采用一切皆插件的架构[^52]。仓库 2026-08-13 才建立[^71]，仍处于开发者预览阶段[^52] |
| Kimi Code CLI | 月之暗面 | MIT，0.8 万星[^79] | 默认接 Kimi 模型，也可配置其他兼容 provider[^79]；有桌面、CLI 和 IDE 插件三种形态[^80]。仓库 2026-05-22 建立[^120]，旧版 Python Kimi CLI 已于 2026-09-23 归档[^81] |
| Qwen Code | 阿里通义 | Apache-2.0，2.9 万星[^111] | 论文称它是 Gemini CLI 的分支，服务 Qwen 编码模型[^9] |
| Qoder、Qoder CLI | 阿里巴巴 | IDE、CLI、JetBrains 插件 | 2025-08-22 发布的 agentic 编程平台[^97]，覆盖桌面 IDE、CLI 和 JetBrains 插件[^98]，并提供 Qoder Agent SDK[^99] |
| ZCode | 智谱 Z.ai | Apache-2.0，0.8 万星[^83] | 自称 Z.ai 的 coding agent harness[^83]，官网称其为 GLM-5.3 的官方 harness[^82]。仓库 2026-09-20 建立[^121] |
| MiMo Code | 小米 | MIT，1.4 万星[^84] | 终端原生编码助手，带跨会话的持久记忆系统[^84]。项目口号是"模型与 agent 共同进化"[^84]，仓库 2026-06-10 建立[^122] |
| CodeBuddy Code | 腾讯 | CLI | CodeBuddy 产品线中面向专业工程师的 AI CLI 工具[^100]。腾讯称 CodeBuddy 基于混元代码模型，内部超过半数研发人员在用[^100] |
| Comate CLI | 百度 | CLI，npm 分发 | 终端 AI 编码助手，既有交互式 TUI，也可作为接入 CI 的 headless CLI[^101]。有 Agent、Plan、Goal 三种模式[^101] |
| Trae Agent | 字节跳动 | MIT，1.2 万星[^116] | 面向研究的 Python CLI agent[^9] |

#### IDE、工具厂商与创业公司

| 产品 | 出品方 | 要点 |
| --- | --- | --- |
| Cursor CLI、Cursor SDK | Anysphere（SpaceXAI） | Cursor CLI 在终端提供与 IDE 一致的 harness[^9]。Cursor SDK 让开发者用驱动 Cursor 的同一套 harness、运行时和模型构建 agent[^88]。SpaceX 在 2026 年 6 月宣布以 600 亿美元收购 Cursor[^9]；SpaceXAI 设有 Agent Harness 团队，负责 Cursor 各产品中 agent 的核心行为和能力[^89] |
| GitHub Copilot CLI | GitHub | 2026-02-25 对所有 Copilot 订阅用户正式发布[^87]。有 plan 模式和全自动的 autopilot 模式，会自动把任务委派给 Explore、Task、Code Review、Plan 等专门 agent[^87]；模型可选 Anthropic、OpenAI 和 Google 的[^87] |
| Devin CLI、Devin Desktop | Cognition | Devin CLI（2026-04-27）是本地 coding agent，可选任意前沿模型或自研的 SWE-1.6[^90]。Devin Desktop（2026-06-02）是 Windsurf 的下一代，任何兼容 ACP 的 agent 都能在其中与 Devin 并行运行[^91] |
| Kiro CLI | AWS | 论文称它由 Q Developer 演变而来，主打规格驱动开发[^9]；底层用 Claude 前沿模型[^92] |
| Junie | JetBrains | 可接任意模型的 coding agent[^93] |
| Droid | Factory | 2025 年 9 月以 58.75% 登顶 Terminal-Bench[^94]。Factory 认为，合适的 agent 框架带来的提升可以超过换模型[^94] |
| Amp | Sourcegraph | agent 可以在任何地方运行，关掉电脑后仍继续工作[^95] |
| Warp | Warp | 从终端演化来的 agentic 开发环境[^96] |
| pool | Poolside | 运行在终端，或接入任何兼容 ACP 的编辑器[^85]；以自家 Laguna 模型为后端，二进制按专有 EULA 分发[^110] |
| 其他 | Augment、Snowflake、Tabnine 等 | 社区清单还收录了 Augment 的 Auggie、Snowflake 的 Cortex Code CLI 和需要企业许可的 Tabnine CLI 等[^110] |

#### 开源社区项目

| 项目 | 维护方 | GitHub 星数 | 要点 |
| --- | --- | --- | --- |
| Claw Code | 社区 | 19.5 万[^70] | 自称是 2026 年 3 月 Claude Code 源码泄露后的净室重写（Python 和 Rust），几天内破 10 万星[^9]。论文认为这说明 harness 架构本身就能吸引社区关注，而不只靠模型[^9] |
| Cline | Cline Bot Inc. | 7.1 万[^74] | IDE 安装量超过 500 万，主打 plan/act 工作流，衍生出 Roo、Kilo 等分支[^9]。Roo Code 已于 2026-05-15 归档[^108]，Kilo Code 约 2.8 万星[^115] |
| goose | AAIF（原 Block） | 5.5 万[^75] | 原生支持 MCP，2026 年 4 月捐给 Agentic AI Foundation[^9]，现属 Linux Foundation 旗下的 AAIF[^75] |
| Deep Agents | LangChain | 3.0 万[^113] | 自称开箱即用的 agent harness[^113]。建在 LangGraph 上，带 todo 规划、有权限控制的虚拟文件系统、子 agent、`SKILL.md` 和 `AGENTS.md` 记忆[^9] |
| Crush | Charmbracelet | 2.9 万[^114] | Go 原生、能感知 LSP 的 TUI，源自早期 Go 版 opencode[^9] |
| ForgeCode | tailcallhq | 0.8 万[^109] | 支持 300 多种模型[^109]。TB2 排行榜上 Opus 4.6 配 ForgeCode 为 81.8%[^13]，但 Meta-Harness 作者没能用公开代码复现这一结果[^13] |
| Open Interpreter、Codewhale、Reasonix、Prime Agent | 社区与创业公司 | 2.2 万–6.9 万[^110] | Open Interpreter 常被当作在本机干活的 agent[^110]。Codewhale（原 deepseek-tui）支持 30 多家 provider 和本地 vLLM、SGLang、Ollama[^110]。Reasonix 是单个 Go 二进制，面向长时间无人值守运行[^110]。Prime Agent 用一个持久的 IPython kernel 作为模型唯一的工具[^110] |
| Browser Use | Browser Use | 11.9 万[^118] | 浏览器 agent 的开源 Python 库[^118]；其极简 harness 主张见第 8 节 |

研究和评测中常用的基线 harness 还有 Terminus 2，由 Terminal-Bench 团队开发，用作比较模型的中立测试台[^12]。

### 3.4 生态层：协议、meta-harness 与编排

- **ACP（Agent Client Protocol）**：论文称它是 Zed 和 Google 推动的、面向编辑器的 JSON-RPC 标准[^9]。官网列出了 43 个 agent（按该页计数），包括经适配器接入的 Claude Agent、Codex CLI 和 Pi[^104]。Gemini CLI、GitHub Copilot、Hermes Agent、Kimi CLI、Kiro CLI、OpenClaw、OpenCode、OpenHands、Qoder CLI、Qwen Code 等也在列[^104]。Devin Desktop 允许任何兼容 ACP 的 agent 与 Devin 并行运行[^91]。
- **Meta-harness**：Databricks 于 2026 年 6 月以 Apache 2.0 开源 Omnigent[^9]，GitHub 约 1.1 万星[^117]。它位于 Claude Code、Codex、Pi 等现有 agent 之上，让它们成为一个更大系统中可互操作的部件[^102]。注册表内置 23 个 harness 适配器，分 `sdk-in-process`、`cli-subprocess`、`acp-subprocess`、`native-tui`、`native-server` 五种接入模式[^9]。适配器声明的能力要通过一致性测试，论文的说法是"像测硬件一样测 harness"[^9]。论文认为它押注的是 harness 已成为商品化组件，持久价值在更上一层[^9]。
- **任务编排**：OpenAI 开源的 Symphony 把项目工作变成隔离的自动实现任务，让团队管理工作，而不是盯着 coding agent[^103]。它在采用了 harness engineering 的代码库里效果最好[^103]。社区的编排层还有 claude-flow（约 7.7 万星）、Oh My OpenAgent（约 7.0 万星，叠加在 OpenCode、Codex 和 Pi 之上）和 vibe-kanban（约 2.8 万星）[^110]。

### 3.5 格局观察

- **模型厂商纷纷自建 harness**：除 Anthropic、OpenAI 和 Google 外，xAI、Meta、Mistral、DeepSeek、月之暗面、阿里、智谱、小米、腾讯和百度都有了自家 harness（见 3.1 和 3.3 节）。但自家 harness 不等于更高分：受控实验里，厂商自家 harness 在自家模型上没有分数优势[^19]。
- **闭源化与并购**：Google 用闭源的 Antigravity CLI 接替 Apache 2.0 的 Gemini CLI[^9]；SpaceX 收购 xAI 之后，又宣布以 600 亿美元收购 Cursor[^9]。论文的结论是，harness 层已不再是空白地带，而是厂商收购、改名和设门槛的战略基础设施[^9]。
- **开源 harness 关注度更高**：（归纳）按星数，OpenClaw、Hermes Agent、DeepSeek Harness 和 OpenCode 都高于 Claude Code 和 Codex 的仓库（数据见 3.1 和 3.3 节），但星数反映的是开发者关注度，不是使用量。Claw Code 几天内破 10 万星，论文据此认为 harness 架构本身就能吸引社区关注[^9]。
- **从产品走向组件**：ACP 让同一个 agent 嵌入不同编辑器[^104]，Omnigent 把整套 harness 当作组件来编排[^102]，Agent Lightning 这类 RL 框架则直接接入现成的 harness 做训练（见 6.2 节）[^38]。（推断）竞争点正在从单个 harness 的功能，转向它能否被编辑器、meta-harness 和训练框架接入。

## 4. Harness 值多少：正反证据

| 证据 | 设置 | harness 变化 | 结果 | 可迁移性 |
| --- | --- | --- | --- | --- |
| TB2 排行（Meta-Harness 汇总） | 89 题 | 不同 harness | Opus 4.6：58.0%（Claude Code）至 81.8%（ForgeCode）；Haiku 4.5：13.9%（OpenHands）至 37.6%（Meta-Harness）[^13] | 多为自报；ForgeCode 无法用公开代码复现[^13][^21] |
| LangChain deepagents | gpt-5.2-codex，TB2 | 提示、中间件、推理预算 | 52.8% → 66.5%[^14] | 针对单一基准迭代 |
| Harness profiles | tau2-bench 难子集 | 按模型调整提示、工具和中间件 | GPT-5.3 Codex 33% → 53%；Opus 4.7 43% → 53%[^15] | 子集，作者自测 |
| ARC-AGI-3 | GPT-5.6 Sol | 保留推理；用 compaction 替代滚动截断 | 13.3% → 38.3%，输出 token 少 6 倍[^16] | 官方 harness 本身有缺陷 |
| Same Model, Different Harness | 20,480 token 窗口，169 题 | 随上下文填满截短旧工具输出，并对停滞作出反应 | F2PF 28% → 49%；完整解 43 → 72[^17] | 宽窗口下两组接近[^17] |
| Are Harnesses Worth the Cost? | 1 个 Java 服务，每个模型 10 次配对运行 | 行为 harness（契约、mock、测试） | GPT-6 Luna 3/10 → 10/10；GPT-6 Sol 都是 10/10，但成本约 7 倍[^24] | 样本小，单一任务 |
| What Does a Harness Buy? | SWE-bench Verified：447 题（2 个模型）与 45 道难题（5 个模型） | Claude Code、mini-SWE-agent、OpenCode | 447 题上 5 分内等价；45 道难题上换 harness 与重跑都翻转 13% 的任务；成本最多 3 倍[^19] | 单一基准；闭源模型只在 Claude Code 中运行[^19] |
| HAL | Online Mind2Web | SeeAct + GPT-5 Medium 对 Browser-Use + Claude Sonnet 4（模型也不同，不是同模型对照） | 成本 $171 对 $1,577（9 倍），准确率只差 2 个百分点；Claude 配 Browser-Use 更好，OpenAI 模型配 SeeAct 更好[^18] | 模型与 scaffold 存在交互 |
| 基础设施（非 harness） | TB2，同模型同 harness | 资源上限从 1 倍到不设限 | +6 个百分点[^20] | 混杂因素 |

**怎么调和**（推断）：大增益几乎都出现在三种条件下：约束紧，即小上下文窗口或有超时[^17][^14]；通用 harness 与模型的训练和部署方式不匹配，例如每步丢弃推理、滚动截断历史[^16]；任务超出模型独立稳定完成的范围[^24][^22]。条件宽松时（前沿模型、宽窗口、标准 SWE 任务），harness 主要改变 token 账单[^19]。这与 "What Does a Harness Buy?" 的结论一致：harness 买到的是更少的失败方式和一张账单，而不是更高的通过率[^19]。该文测到的每个 harness 效应，都是让模型丢掉本可解决的任务，例如输出截断后无法恢复、上下文满了没有 compaction[^19]。

**测量本身的噪声**：在 45 题上比较 harness，13 分的差距只有一半概率被测出；447 题能分辨约 5 分[^19]。作者建议在任何 harness 差距旁附上同一配置的重跑结果[^19]。（估算）若把 TB2 的 89 题看作任务总体的一个样本，通过率在 75% 附近时，单次运行的二项标准误约为 4.6 个百分点，大于榜首几家之间的差距。

## 5. 自动化：harness 成为可搜索的代码

| 工作 | 机构 | 优化什么 | 关键结果 |
| --- | --- | --- | --- |
| AutoHarness | Google DeepMind | 小模型自己写代码 harness，从动作校验一直到整个策略 | 145 个 TextArena 游戏的非法动作全部消除；代码策略在 16 个单人游戏上超过 Gemini-2.5-Pro 和 GPT-5.2-High[^25] |
| Meta-Harness | Stanford、MIT、KRAFTON | agentic proposer 通过文件系统读取所有历史候选的源码、分数和轨迹 | TB2：Opus 4.6 76.4%（手工最强的 Terminus-KIRA 为 74.7%），Haiku 4.5 37.6%[^13] |
| Self-Harness | 上海人工智能实验室 | 弱点挖掘 → 修改提案 → 回归验证，不依赖人类或更强的模型 | 9 个模型与基准组合的 held-in 和 held-out 全部提升，相对增益最高 132%[^26] |
| VERSE | MIT、Amazon | 同时进化优化器自身的工具和流程 | 最佳 harness 42.3%（最强基线 39.2%）；分布外任务 37.7%（基线 29.3%）[^27] |
| ActiveSaddler | Microsoft、POSTECH | 优化过程使用的训练场景课程 | GAIA2 +4.4、TB2 +7.5 个百分点[^29] |
| Harmony Harness | Google 等 | 多目标；通用机制与基准特定适配分开进化 | SecRepoBench 和 BaxBench 上增益均超过 10%[^28] |
| MoMHa | Adobe | 准确率、安全、token 三目标 | 真实基准 0.461，最强基线 DSPy 为 0.377[^31] |
| Harness2 | Google Cloud | 没有 ground-truth verifier 的开放世界任务 | WorkBuddy-Bench +11.5、JobBench +4.5、LAB +11.8[^30] |
| Doc2Harness | 中科院计算所等 | 基准：让模型按文档从零构建 harness | 19 个前沿模型中最强的 GPT-6 Astra 通过 53.05%，最弱 27.44%[^32] |

共性（推断）：

- **执行验证是前提**：VERSE 的对照实验中，没有基于执行的验证，优化器的自进化不提升性能；有了验证，它取得该实验的最好结果[^27]。
- **过拟合是头号风险**：LangChain 直言 agent 是"出了名的作弊者"，会让结构过拟合到看得见的评测上，所以要用 holdout 和人工审查兜底[^33]。Meta-Harness 在同一套 89 题上搜索和评测，只能靠人工检查和正则审计排查任务特定字符串的泄漏[^13]。
- **目标在变多**：MoMHa 的说法是，一个对不安全请求从不拒绝、或多耗一个数量级 token 的 harness，不算好 harness[^31]。
- **造 harness 本身就是长程任务**：Doc2Harness 的失败集中在横切功能如何拆分到各个模块[^32]。

## 6. 训练闭环：模型与 harness 共同演化

### 6.1 模型会适配到自己的 harness

- LangChain 指出，后训练时把 harness 放进循环会造成过拟合，例如 Codex 模型对 `apply_patch` 编辑逻辑的依赖[^1]。
- 但"模型最适合自家 harness"并不成立：TB2 上 Claude Code 在所有 Opus 4.6 提交中排最后[^15]。受控实验里，DeepSeek 自家 harness 在 DeepSeek-V4-Flash 上也没有分数优势[^19]。
- 训练与 harness 的匹配很关键：OpenAI 的模型带着保留的私有推理训练和部署，而 ARC-AGI-3 官方的通用 harness 每执行一步都丢弃私有推理[^16]。
- LangChain 因此推出按模型配置的 harness profiles，例如给 Codex 模型换成推荐的 `apply_patch` 工具[^15]。
- 研究层面，harness-aware 的后训练在分布内外都更好；在最简 harness 下后训练的模型，工具环境变化较大时会大幅掉点[^34]。Co-Harness 交替优化 harness 与权重，并把 harness 带来的改进蒸馏进参数[^35]。Self-HPO 让演化中的 policy 自己提出 harness 候选，把 Qwen3.5-35B-A3B 的平均解决率从 57.8% 提到 64.8%[^36]。Harness-1 反其道而行：把搜索簿记外置到 harness，让 RL 只优化语义决策[^37]。

### 6.2 harness-native RL 的新问题

范式变化：传统 agentic RL 由训练引擎掌握交互循环；在 harnessed agentic RL 中，循环归 harness 所有，训练引擎只看到一串 LLM 请求与响应[^38]。verl Uni-Agent、AReaL 2.0、slime v0.3.0 和 Polar 都采用了这种代理（proxy）方式[^38]。

| 问题 | 现象 | 现有做法 |
| --- | --- | --- |
| Token 保真 | 文本不变，重新分词后的 token ID 也可能不同于采样时[^38]；工具参数 JSON 可能被重新序列化，harness 还可能压缩或改写历史[^40] | Fireworks 的 TITO 记录精确的 prompt token、动作 token、logprob 和 loss mask[^40]；Uni-Agent 的 String-In-Token-Out 网关[^39] |
| 样本拆分 | Agent Lightning 的 coding agent 训练中，只有 36% 的 rollout 保持为单个样本，平均每个 rollout 产出 2.4 个样本[^38] | Uni-Agent 在上下文被裁剪或分叉时另起一条链[^39] |
| 优势计算 | verl Uni-Agent 和 Polar 在 rollout 级计算优势，slime 和 AReaL 在样本级计算[^38] | 需要显式选择 |
| Loss 归一化 | 样本级归一化让产出样本多的 rollout 权重更大，可能导致训练不稳定[^38] | — |
| Harness 敏感性 | 修复工具 bug、改变对无工具调用回复的处理，都会显著改变训练动态[^39] | 多 harness 混训[^39] |
| 奖励污染 | 环境崩溃和 reward hacking 污染结果信号[^41] | 沙箱编排加分阶段防御[^41] |

实证：Lego-RL 不改动原生 harness 的控制流，用 GSPO 训练 Qwen3.5-35B-A3B[^41]。在 SWE-bench Verified 上，OpenHands SDK 从 64.0% 升到 70.4%，Claude Code 从 62.4% 升到 68.2%，OpenCode 从 57.2% 升到 66.6%[^41]。rollout 端与训练端的概率相关性保持在 0.99 以上[^41]。

## 7. 评测 harness：分数测的是"模型 + harness + 基础设施"

- Anthropic 区分了评测 harness（端到端运行评测的基础设施）与 agent harness，并指出评测一个 agent 就是在评测 harness 与模型的组合[^8]。
- lm-eval 的维护者总结三年经验时，把模型对评测设置的敏感性列为主要的方法学问题之一[^43]。
- HAL 用标准化 harness 跑了 21,730 次 rollout，覆盖 9 个模型和 9 个基准[^18]。日志分析发现，agent 会去 HuggingFace 搜答案，还会在订票任务里误用信用卡[^18]。他们在投入大量评测费用之后，才发现某个 scaffold 存在数据泄漏[^18]。
- TB2 由 89 道终端任务组成[^12]。它的官方 harness Harbor 也能生成 RL rollout[^44]。（推断）评测 harness 与 RL 环境正在合并为同一套基础设施，评测 harness 的缺陷会直接变成训练 reward 的缺陷。
- Anthropic 发现，在 TB2 上仅资源配置一项，资源最多与最少的设置之间就差 6 个百分点[^20]。资源预算和时间限制不同的两个 agent，参加的并不是同一场考试[^20]。
- OpenAI 的总结是：评测很少孤立地测模型，它测的是 API 设置、harness 设计和提示的组合[^16]。

## 8. 争议与开放问题

- **薄 harness 还是厚 harness**：Browser Use 把整个浏览器 harness 压到约 600 行，主张连工具 helper 也删掉，让 agent 自己写需要的函数[^23]。mini-SWE-agent 的 README 称它用约 100 行代码在 SWE-bench Verified 上拿到 74% 以上[^53]。产品层面同样分化：按论文的粗分档，Pi 属于 Medium（8 万–11 万行），核心循环只有约 790 行，并把不做规划、不设轮数上限写成设计取舍[^9]；Hermes Agent 和 Codex 属于 Very large（60 万行以上）[^9]。另一边，Anthropic 认为模型变强后，harness 的设计空间不会缩小，只会移动[^22]。（推断）两边说的是不同层面：该变薄的是工具抽象层，需要保持厚的是验证、状态和安全层。
- **Harness 的假设会过期**：Anthropic 为 Sonnet 4.5 的 context anxiety 加了上下文重置，到 Opus 4.5 这个行为消失，重置成了累赘[^11][^22]。他们的做法是，每来一个新模型，就逐个移除组件，看哪些仍在起作用[^22]。
- **成本**：完整 harness 跑 6 小时花 $200，单 agent 跑 20 分钟花 $9，贵 20 倍以上；但单 agent 做出的游戏核心功能根本不能用[^22]。在 GPT-6 Sol 上，harness 的 token 用量约为 10.5 倍、成本约 7 倍，验收结果却没有变化[^24]。
- **行为正确性仍是短板**：Böckeler 认为当前过度依赖 AI 生成的测试，这还不够[^6]。她也指出，OpenAI 那篇文章缺少对功能和行为的验证[^5]。
- **如何评价 harness 本身**：Böckeler 呼吁建立类似代码覆盖率和变异测试的 harness 覆盖率与质量度量[^6]。
- **安全**：Managed Agents 的结构性做法是，凭证永远不能从运行生成代码的沙箱中访问[^11]。

## 参考来源

文中引用的资料如下，访问时间均为 2026-10-20。

[^1]: [LangChain — The Anatomy of an Agent Harness (Vivek Trivedy, 2026-03-10)](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)
[^2]: [Wikipedia — Agent harness](https://en.wikipedia.org/wiki/Agent_harness)
[^3]: [Mitchell Hashimoto — My AI Adoption Journey (2026-02-05)](https://mitchellh.com/writing/my-ai-adoption-journey)
[^4]: [OpenAI — Harness engineering: leveraging Codex in an agent-first world (2026-02-11; Wayback snapshot 2026-10-16)](https://web.archive.org/web/20261016135644/https://openai.com/index/harness-engineering)
[^5]: [Birgitta Böckeler — Harness Engineering: first thoughts (martinfowler.com)](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html)
[^6]: [Birgitta Böckeler — Harness engineering for coding agent users (martinfowler.com, 2026-04-02)](https://martinfowler.com/articles/harness-engineering.html)
[^7]: [Anthropic — Effective harnesses for long-running agents (2025-11-26)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
[^8]: [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
[^9]: [Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents — source-code study of 11 systems (arXiv 2609.00006v1)](https://arxiv.org/html/2609.00006)
[^10]: [From Question Answering to Task Completion: A Survey on Agent System and Harness Design (arXiv 2606.20683v1)](https://arxiv.org/html/2606.20683)
[^11]: [Anthropic — Scaling Managed Agents: Decoupling the brain from the hands (2026-04-08)](https://www.anthropic.com/engineering/managed-agents)
[^12]: [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in CLIs (arXiv 2601.11868v1)](https://arxiv.org/html/2601.11868)
[^13]: [Meta-Harness: End-to-End Optimization of Model Harnesses (arXiv 2603.28052v1)](https://arxiv.org/html/2603.28052)
[^14]: [LangChain — Improving Deep Agents with harness engineering (2026-02-17)](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
[^15]: [LangChain — Tuning Deep Agents to Work Well with Different Models (harness profiles)](https://www.langchain.com/blog/tuning-deep-agents-different-models)
[^16]: [OpenAI — How enabling two settings tripled our scores on ARC-AGI-3 (2026-07-29; Wayback snapshot 2026-10-02)](https://web.archive.org/web/20261002001010/https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores)
[^17]: [Same Model, Different Harness: Different Coding-Agent Results (arXiv 2608.26218v1)](https://arxiv.org/html/2608.26218)
[^18]: [Holistic Agent Leaderboard (HAL) (arXiv 2510.11977v1, ICLR 2026)](https://arxiv.org/html/2510.11977)
[^19]: [What Does a Harness Buy? Tokens, Mostly. (arXiv 2610.04433v1)](https://arxiv.org/html/2610.04433)
[^20]: [Anthropic — Quantifying infrastructure noise in agentic coding evals (2026-02-05)](https://www.anthropic.com/engineering/infrastructure-noise)
[^21]: [Can Agents Work? — Terminal-Bench 2.0 entry (third-party tracker)](https://canagentswork.com/benchmarks/terminal-bench-2)
[^22]: [Anthropic — Harness design for long-running application development (2026-03-24)](https://www.anthropic.com/engineering/harness-design-long-running-apps)
[^23]: [Browser Use — The Bitter Lesson of Agent Harnesses (2026-04-19)](https://browser-use.com/posts/bitter-lesson-agent-harnesses)
[^24]: [Naresh Jain — Are Harnesses Worth the Cost? (martinfowler.com, 2026-10-13)](https://martinfowler.com/articles/are-harnesses-worth-the-cost.html)
[^25]: [AutoHarness: improving LLM agents by automatically synthesizing a code harness (arXiv 2603.03329v1, DeepMind)](https://arxiv.org/html/2603.03329)
[^26]: [Self-Harness: Harnesses That Improve Themselves (arXiv 2606.09498v3)](https://arxiv.org/html/2606.09498)
[^27]: [VERSE: Verified Self-Evolving Optimizer for Agent Harnesses (arXiv 2610.02616v1)](https://arxiv.org/html/2610.02616)
[^28]: [Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses (arXiv 2610.15150v1)](https://arxiv.org/html/2610.15150)
[^29]: [ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization (arXiv 2610.00906v1)](https://arxiv.org/html/2610.00906)
[^30]: [Harness2: Recursive Agent Harnessing for an Open World (arXiv 2610.14224v1)](https://arxiv.org/html/2610.14224)
[^31]: [MoMHa: Multi-Objective Optimization of LLM Harnesses (arXiv 2609.30967v1)](https://arxiv.org/html/2609.30967)
[^32]: [Doc2Harness: Benchmarking LLMs on Long-Horizon Harness Engineering (arXiv 2610.20344v1)](https://arxiv.org/html/2610.20344)
[^33]: [LangChain — Better Harness: A Recipe for Harness Hill-Climbing with Evals](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals)
[^34]: [The Interplay of Harness Design and Post-Training in LLM Agents (arXiv 2606.25447v2)](https://arxiv.org/html/2606.25447)
[^35]: [Co-Harness: Co-Evolving Harnesses and Model Weights for LLM Agents (arXiv 2607.22688v1)](https://arxiv.org/html/2607.22688)
[^36]: [Self-Evolving Coding Agents via Harness-Policy Optimization (Self-HPO, arXiv 2610.22791v1)](https://arxiv.org/html/2610.22791)
[^37]: [Harness-1: RL for Search Agents with State-Externalizing Harnesses (arXiv 2606.02373v1)](https://arxiv.org/html/2606.02373)
[^38]: [Agent Lightning v1.0: Towards Harnessed Agentic RL (arXiv 2608.17528v1)](https://arxiv.org/html/2608.17528)
[^39]: [verl Blog — Uni-Agent: Train Long-Horizon Agents at Scale (2026-09-24)](https://verl-project.github.io/posts/2026-09-23-uni-agent-v0-1-0)
[^40]: [Fireworks Docs — Cookbook: Agentic Reinforcement Learning (TITO)](https://docs.fireworks.ai/fine-tuning/training-api/cookbook/agentic-rl)
[^41]: [Lego-RL: Harness-Native Reinforcement Learning for Coding Agents (arXiv 2608.17393v1)](https://arxiv.org/html/2608.17393)
[^42]: [verl docs — Agent Loop](https://raw.githubusercontent.com/volcengine/verl/main/docs/advance/agent_loop.rst)
[^43]: [Lessons from the Trenches on Reproducible Evaluation of Language Models (lm-eval, arXiv 2405.14782v3)](https://arxiv.org/html/2405.14782)
[^44]: [Harbor README (harbor-framework)](https://raw.githubusercontent.com/harbor-framework/harbor/main/README.md)
[^48]: [OpenAI — Unrolling the Codex agent loop (2026-01-23; Wayback snapshot 2026-02-10)](https://web.archive.org/web/20260210065637/https://openai.com/index/unrolling-the-codex-agent-loop)
[^49]: [OpenAI Developers — Codex as a platform: build on the open agent harness](https://developers.openai.com/blog/codex-as-a-platform.md)
[^52]: [DeepSeek Harness (GitHub)](https://github.com/deepseek-ai/deepseek-harness)
[^53]: [mini-SWE-agent (GitHub)](https://github.com/swe-agent/mini-swe-agent)
[^54]: [OSS-Fuzz blog — Introducing LLM-based harness synthesis for unfuzzed projects (2024-05-27)](https://blog.oss-fuzz.com/posts/introducing-llm-based-harness-synthesis-for-unfuzzed-projects)
[^62]: [Hermes Agent — GitHub NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
[^63]: [Pi — GitHub earendil-works/pi](https://github.com/earendil-works/pi)
[^64]: [OpenCode — GitHub anomalyco/opencode](https://github.com/anomalyco/opencode)
[^65]: [OpenClaw — GitHub openclaw/openclaw](https://github.com/openclaw/openclaw)
[^66]: [Codex — GitHub openai/codex](https://github.com/openai/codex)
[^67]: [Gemini CLI — GitHub google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
[^68]: [Claude Code — GitHub anthropics/claude-code](https://github.com/anthropics/claude-code)
[^69]: [Claude Code LICENSE.md (anthropics/claude-code)](https://raw.githubusercontent.com/anthropics/claude-code/main/LICENSE.md)
[^70]: [Claw Code — GitHub ultraworkers/claw-code](https://github.com/ultraworkers/claw-code)
[^71]: [GitHub API — deepseek-ai/deepseek-harness repository metadata](https://api.github.com/repos/deepseek-ai/deepseek-harness)
[^72]: [GitHub API — xai-org/grok-build repository metadata](https://api.github.com/repos/xai-org/grok-build)
[^73]: [OpenHands — GitHub OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)
[^74]: [Cline — GitHub cline/cline](https://github.com/cline/cline)
[^75]: [goose — GitHub aaif-goose/goose](https://github.com/aaif-goose/goose)
[^76]: [Aider — GitHub Aider-AI/aider](https://github.com/Aider-AI/aider)
[^77]: [Grok Build — GitHub xai-org/grok-build](https://github.com/xai-org/grok-build)
[^78]: [Meta Model API docs — Muse Code](https://dev.meta.ai/docs/muse-code)
[^79]: [Kimi Code CLI — GitHub MoonshotAI/kimi-code](https://github.com/MoonshotAI/kimi-code)
[^80]: [Kimi Code — kimi.com/code](https://www.kimi.com/code/en)
[^81]: [Kimi CLI (archived) — GitHub MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli)
[^82]: [ZCode — zcode.z.ai](https://zcode.z.ai/en)
[^83]: [ZCode — GitHub zai-org/ZCode](https://github.com/zai-org/ZCode)
[^84]: [MiMo Code — GitHub XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code)
[^85]: [pool — GitHub poolsideai/pool](https://github.com/poolsideai/pool)
[^86]: [Gemini CLI Discussion #27274 — Transitioning Gemini CLI to Antigravity CLI (2026-05-19)](https://github.com/google-gemini/gemini-cli/discussions/27274)
[^87]: [GitHub Changelog — GitHub Copilot CLI is now generally available (2026-02-25)](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available)
[^88]: [Cursor Help — How do I build an AI coding agent? (Cursor SDK)](https://cursor.com/help/getting-started/build-ai-coding-agent)
[^89]: [Cursor Careers — Software Engineer, Agent Harness (SpaceXAI)](https://cursor.com/careers/software-engineer-agent-harness)
[^90]: [Cognition — Devin CLI: Start Local, Hand Off to the Cloud (2026-04-27)](https://cognition.ai/blog/devin-for-terminal)
[^91]: [Cognition — Introducing Devin Desktop (2026-06-02)](https://cognition.ai/blog/introducing-devin-desktop)
[^92]: [Kiro CLI — kiro.dev/cli](https://kiro.dev/cli)
[^93]: [Junie by JetBrains](https://junie.jetbrains.com)
[^94]: [Factory — Droid: The #1 Software Development Agent on Terminal-Bench (2025-09-25)](https://factory.ai/news/terminal-bench)
[^95]: [Amp — ampcode.com](https://ampcode.com)
[^96]: [Warp — GitHub warpdotdev/warp](https://github.com/warpdotdev/warp)
[^97]: [科技日报 — 阿里发布新一代AI编程平台Qoder（2025-08-22）](https://www.stdaily.com/web/gdxw/2025-08/22/content_388981.html)
[^98]: [Alibaba Cloud Model Studio docs — Qoder](https://www.alibabacloud.com/help/en/model-studio/qoder-agent)
[^99]: [Qoder CLI — qoder.com/en/cli](https://qoder.com/en/cli)
[^100]: [Tencent Cloud — Tencent CodeBuddy](https://www.tencentcloud.com/products/acc)
[^101]: [百度智能云文档 — Comate CLI 快速入门（2026-07-09）](https://cloud.baidu.com/doc/COMATE/s/0mrcv8nsa)
[^102]: [Databricks — Introducing Omnigent: A Meta-Harness to Combine, Control and Share Your Agents](https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents)
[^103]: [OpenAI Symphony — GitHub openai/symphony](https://github.com/openai/symphony)
[^104]: [Agent Client Protocol — Agents](https://agentclientprotocol.com/overview/agents)
[^105]: [Claude Help Center — Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
[^106]: [Hacker News — Felix Rieseberg (Anthropic) on Claude Cowork's VM design](https://news.ycombinator.com/item?id=47220118)
[^107]: [Ars Technica — Entire Claude Code CLI source code leaks thanks to exposed map file (2026-03-31)](https://arstechnica.com/ai/2026/03/entire-claude-code-cli-source-code-leaks-thanks-to-exposed-map-file)
[^108]: [Roo Code (archived) — GitHub RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code)
[^109]: [ForgeCode — GitHub tailcallhq/forgecode](https://github.com/tailcallhq/forgecode)
[^110]: [bradAGI/awesome-cli-coding-agents — community-curated list of CLI coding agents and harnesses](https://github.com/bradagi/awesome-cli-coding-agents)
[^111]: [Qwen Code — GitHub QwenLM/qwen-code](https://github.com/QwenLM/qwen-code)
[^112]: [Mistral Vibe — GitHub mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe)
[^113]: [Deep Agents — GitHub langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)
[^114]: [Crush — GitHub charmbracelet/crush](https://github.com/charmbracelet/crush)
[^115]: [Kilo Code — GitHub Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode)
[^116]: [Trae Agent — GitHub bytedance/trae-agent](https://github.com/bytedance/trae-agent)
[^117]: [Omnigent — GitHub omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent)
[^118]: [Browser Use — GitHub browser-use/browser-use](https://github.com/browser-use/browser-use)
[^119]: [Hermes Agent source — `agent/iteration_budget.py` (main branch)](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/agent/iteration_budget.py)
[^120]: [GitHub API — MoonshotAI/kimi-code repository metadata](https://api.github.com/repos/MoonshotAI/kimi-code)
[^121]: [GitHub API — zai-org/ZCode repository metadata](https://api.github.com/repos/zai-org/ZCode)
[^122]: [GitHub API — XiaomiMiMo/MiMo-Code repository metadata](https://api.github.com/repos/XiaomiMiMo/MiMo-Code)
