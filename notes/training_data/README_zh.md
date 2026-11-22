# 训练数据

中文 | [English](./README.md)

[← 返回首页](../../README_zh.md)

- [训练数据中的思维链合成：方法、证据与开放问题（文献综述）](./CoT-Data-Synthesis-Literature-Review.md) · 2026-10-22
  - 系统检索 13,589 篇候选、纳入 1,527 篇、精读 237 份来源后的结论：用于 SFT 与蒸馏的推理数据，重心已从“多找题”转向“每题多采样、再按学生挑选”，2026 年又快速转向 on-policy 蒸馏（摘要提及它的纳入文献从 2025 年下半年的 2 篇增至 2026 年上半年的 79 篇）；代码与智能体数据的瓶颈在任务与环境的多样性。“教师越强越好”“答案正确的轨迹更好”“数据越多越好”“验证一定有益”四条直觉都有受控实验给出的反例，成立与否取决于学生规模、师生分布距离与训练预算。以答案为条件的生成、长度惩罚与递归自训练，会以答案正确率察觉不到的方式损害数据。
  - 分节页面：[第 4 节](./CoT-Data-Synthesis-Literature-Review-Ch04.md) · [第 5 节](./CoT-Data-Synthesis-Literature-Review-Ch05.md) · [第 6 节](./CoT-Data-Synthesis-Literature-Review-Ch06.md) · [第 7 节](./CoT-Data-Synthesis-Literature-Review-Ch07.md) · [第 8 节](./CoT-Data-Synthesis-Literature-Review-Ch08.md) · [第 9 节](./CoT-Data-Synthesis-Literature-Review-Ch09.md) · [第 10 节](./CoT-Data-Synthesis-Literature-Review-Ch10.md)

- [面向高效多轮智能体微调的依赖感知轨迹精炼（论文全文翻译）](./Dependency-Aware-Trajectory-Refinement.md) · 2026-09-16
  - 把多轮智能体轨迹看成轮次级依赖 DAG，再在图上做确定性的编辑：L1 剪掉出度为 0 的死胡同轮次，L2 合并父节点和子节点都相同的兄弟轮次，L3 只要求父节点相同并迭代合并，L2a/L3a 再让 LLM 把合并后的 `<think>` 改写成一段连贯的推理。用 6196 条轨迹对 Qwen3-VL-30B-A3B-Thinking 做 SFT，在四个多模态 QA 基准上，L1 平均准确率 50.04%，比 Vanilla SFT 高 1.7 个百分点；L2a 与 Vanilla SFT 准确率相当，推理 token 却从 20.9K 降到 11.0K。L3 打破了推理时每回合一次工具调用的格式，卡死率是 L2 的 2–3 倍；让 LLM 直接删除轮次的 Critical-Path 基线反而比 Vanilla SFT 掉点。

- [MMAT-1M：百万级多模态 Agent 微调数据集](./MMAT-1M-Multimodal-Agent-Tuning.md) · 2025-07-29
  - 用 GPT-4o 给 5 个公开视觉问答数据集补上推理过程、工具调用（图片描述、OCR、检测、搜索）和反思，得到 902,965 条多轮对话（RR），另有一份压成单轮的版本（ORR）。用它 LoRA 微调 1 个 epoch 后，InternVL2.5-8B 的 8 项基准平均分从 60.7 涨到 63.4，Dyn-VQA 从 35.2 涨到 44.0；不微调、只靠提示词套用这种格式反而掉分。实测数据还发现：ORR 比 RR 少 16% 的样本，通用反思只指出“作弊”、不重新推理，不少样本的图片描述里已经写着答案；原图的下载地址已失效，图片要到各个原始数据集里找。

- [OpenThoughts：推理模型的数据配方（论文全文翻译）](./OpenThoughts-Data-Recipes-for-Reasoning-Models.md) · 2025-06-04
  - 用 1,000 多次受控实验逐步优化推理 SFT 数据流水线，得到 OpenThoughts3-1.2M；用它训练的 OpenThinker3-7B 在 AIME 2025、LiveCodeBench 06/24-01/25 和 GPQA Diamond 上分别达到 53%、51% 和 54%。主要发现：让教师模型给每个问题采样多个答案，能把数据扩大 16 倍以上；基准分数更低的 QwQ-32B 反而是比 DeepSeek-R1 更好的教师；答案验证与过滤没有带来明显收益；只用一两个高质量问题来源，好过追求来源多样；按 LLM 标注的难度或回答长度筛选问题，效果好于 fastText、embedding 这类预训练数据过滤方法。

- [OpenThoughts：推理数据配方与规模效应](./OpenThoughts-Reasoning-Data-Scaling.md) · 2025-06-04
  - 逐步讲解选题、来源混合、问题筛选、多答案采样、答案过滤与教师选择，结合最终模型评测和规模曲线，说明推理数据配方的收益及饱和、成本和去污染边界。
