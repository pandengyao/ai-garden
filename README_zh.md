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

- [Flash-Decoding: 长上下文推理加速](./notes/inference/Flash-Decoding.md) · 2023-10-12
  - 推理时 Query Length 只有 1，Batch 维度并行不起来；那就去并行 KV Cache 的序列长度维度，长序列解码最高快 8 倍。

### 模型 API (LLM APIs)

- [免费与低价大模型 API 调研：额度、价格、套餐与接入](./notes/llm_api/Free-and-Low-Cost-LLM-APIs.md) · 2026-10-20
  - 长期免费能用的主要是 NVIDIA build、智谱 glm-4.7-flash，以及 Kilo 和 OpenRouter 的免费模型；国内按量最便宜的一档每百万输入 0.15–1 元，编程包月套餐大多只许在工具里交互使用。附 23 家平台的官网、Key 入口、base_url 和调用示例。

### 多模态 (Multimodal)

- [Gemini 3 Pro Image Preview: 图片生成的 ChatGPT 时刻](./notes/multimodal/Gemini-3-Pro-Image-Preview.md) · 2025-11-20
  - 生图模型从“画得好看”转向“把信息讲清楚”，原生多模态让理解能力正向迁移到生成上。

## 这座花园怎么打理

- 每篇笔记开头记来源链接和日期，方便回溯。
- 用自己的话复述，不搬运原文；图表只留撑得起论点的那几张。
- 笔记统一用 Markdown，先写中文，每篇配一份英文版（`_en.md`）；图片放在各分区的 `img/` 下。
- 内容只在这里慢慢生长，不追求写完就定稿。

## License

笔记内容采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，仓库内代码采用 [MIT](./LICENSE)。引用的原文版权归原作者所有。
