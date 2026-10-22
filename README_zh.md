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

### 训练 (Training)

- [面向高效多轮智能体微调的依赖感知轨迹精炼（论文全文翻译）](./notes/training/Dependency-Aware-Trajectory-Refinement.md) · 2026-09-16
  - 把多轮智能体轨迹看成轮次级依赖 DAG，再在图上做确定性的编辑：L1 剪掉出度为 0 的死胡同轮次，L2 合并父节点和子节点都相同的兄弟轮次，L3 只要求父节点相同并迭代合并，L2a/L3a 再让 LLM 把合并后的 `<think>` 改写成一段连贯的推理。用 6196 条轨迹对 Qwen3-VL-30B-A3B-Thinking 做 SFT，在四个多模态 QA 基准上，L1 平均准确率 50.04%，比 Vanilla SFT 高 1.7 个百分点；L2a 与 Vanilla SFT 准确率相当，推理 token 却从 20.9K 降到 11.0K。L3 打破了推理时每回合一次工具调用的格式，卡死率是 L2 的 2–3 倍；让 LLM 直接删除轮次的 Critical-Path 基线反而比 Vanilla SFT 掉点。

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
