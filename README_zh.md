# 🌱 ai-garden

中文 | [English](./README.md)

> 我的 AI 数字花园：对 AI 的调研、阅读与思考，都慢慢记录在这里。

笔记按主题分目录，每个主题有一个索引页，列出全部笔记和结论摘要。每篇笔记先写中文，再配一份逐行对应的英文版，开头注明来源和日期。

## 主题

| 主题 | 内容 |
| --- | --- |
| [智能体](./notes/agent/README_zh.md) | Agent harness 调研 · MCP 入门 |
| [蒸馏](./notes/distillation/README_zh.md) | on-policy 蒸馏（OPD）与 on-policy 自蒸馏（OPSD）：季度论文调研、博客与论文全文翻译、单篇论文通俗解读 |
| [基础概念](./notes/fundamentals/README_zh.md) | 位置编码图解 · 熵、交叉熵与 KL 散度 |
| [推理优化](./notes/inference/README_zh.md) | Mooncake 与 KVCache 复用 · DeepSeek V4.1 Flash 线上部署 · Flash-Decoding |
| [模型 API](./notes/llm_api/README_zh.md) | 免费与低价大模型 API 的额度、价格与接入 |
| [多模态](./notes/multimodal/README_zh.md) | 免费与低价 TTS 和文生图 · Gemini 3 Pro Image |
| [缩放规律](./notes/scaling_laws/README_zh.md) | Kaplan、Chinchilla，以及微调与蒸馏的缩放规律 |
| [自我改进](./notes/self_improvement/README_zh.md) | 递归自我改进（RSI）文献综述与近期论文追踪 |
| [训练数据](./notes/training_data/README_zh.md) | 思维链数据合成综述 · OpenThoughts 数据配方 · 智能体轨迹精炼 · MMAT-1M |

## 最近更新

日期为收录日期。

- 2026-11-20 · 推理优化：[Mooncake Transfer Engine 源码阅读术语手册](./notes/inference/Mooncake-Transfer-Engine-Glossary.md)
- 2026-11-13 · 推理优化：[Mooncake 与 SGLang：围绕 KVCache 的架构梳理](./notes/inference/Mooncake-SGLang-KVCache-Architecture.md) · [Mooncake：以更多存储换取更少计算（FAST 2025 论文全文翻译）](./notes/inference/Mooncake-KVCache-Centric-Serving.md)
- 2026-11-09 · 缩放规律：[Kaplan：语言模型缩放定律](./notes/scaling_laws/Kaplan-Scaling-Laws-for-Neural-Language-Models.md) · [Chinchilla：同样算力如何分配模型与数据](./notes/scaling_laws/Chinchilla-Compute-Optimal-Training.md) · [微调缩放规律：数据、模型与方法](./notes/scaling_laws/LLM-Finetuning-Scaling-Laws.md) · [蒸馏缩放规律：教师、学生与计算预算](./notes/scaling_laws/Distillation-Scaling-Laws.md)；训练数据：[OpenThoughts：推理数据配方与规模效应](./notes/training_data/OpenThoughts-Reasoning-Data-Scaling.md)

## License

笔记内容采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，仓库内代码采用 [MIT](./LICENSE)。引用的原文版权归原作者所有。
