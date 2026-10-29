# 🌱 ai-garden

[中文](./README_zh.md) | English

> My AI digital garden: research, reading and thinking about AI, recorded here bit by bit.

This is not a bookmark list but a garden. Each note is a plant: articles I read get digested into my own words here, and ideas start as one-line seeds that grow with research and practice. Some become trees, some stop halfway, and they all stay, because the trace of thinking is worth keeping too.

## Getting around the garden

| Section | What's inside |
| --- | --- |
| [🌳 Notes](#-notes) | Articles, papers and reports I've read, digested into notes (Chinese originals, English versions alongside) |
| [🌱 Ideas](./ideas/) | My own thoughts and guesses, starting from a single line |
| [📰 News](./news/) | AI news logged by month, one line per item |

## 🌳 Notes

### Agents

- [Agent = Model + Harness: An In-Depth Survey of LLM Harnesses](./notes/agent/Agent-Harness-Survey_en.md) · 2026-10-20
  - A harness is the whole runtime outside the model: system prompt, tools, sandbox, orchestration and context management. When constraints are tight or a generic harness doesn't match how the model was trained, swapping the harness can multiply scores; when conditions are relaxed, it mainly decides the cost. Includes a landscape of major products such as Hermes Agent, Pi, OpenCode and OpenClaw, plus progress on automated harness optimization and harness-native RL.

- [MCP (Model Context Protocol): A Primer](./notes/agent/MCP-Model-Context-Protocol_en.md) · 2026-10-20
  - A "universal port" for AI: a tool vendor builds one server to the standard, and every MCP-capable AI can use it. Includes a complete to-do server example and the renaming pitfall between SDK versions.

### Inference

- [DeepSeek V4.1 Flash Inference Deployment Q&A: the official DeepInfer doc, with a full Chinese translation](./notes/inference/DeepSeek-V4.1-Flash-Inference-Deployment-QA_en.md) · 2026-10-20
  - DeepSeek's own production deployment details: a single cluster serves 155 trillion tokens per day; prefill runs on 8-GPU machines with the smallest EP that fits, decode on 64–128-GPU supernodes with Wide-EP, and the block KV cache lives on a dedicated 3FS cluster of about 100 PiB (3–7 day TTL). Also covers EPLB and DP load-balancing settings, SWA bounded replay hits and recomputation, and DSpark variable-length verification (+4–7% throughput at the production operating point).

- [Flash-Decoding: Faster Long-Context Inference](./notes/inference/Flash-Decoding_en.md) · 2023-10-12
  - During inference the query length is just 1, so parallelizing over the batch doesn't fill the GPU; parallelize over the KV cache's sequence length instead, and long-sequence decoding gets up to 8x faster.

### LLM APIs

- [Free and Low-Cost LLM APIs: Quotas, Prices, Plans and Access](./notes/llm_api/Free-and-Low-Cost-LLM-APIs_en.md) · 2026-10-20
  - The main long-term free options are NVIDIA build, Zhipu's glm-4.7-flash, and the free models on Kilo and OpenRouter; the cheapest Chinese pay-as-you-go tier costs 0.15–1 yuan per million input tokens, and most monthly coding plans only allow interactive use inside tools. Includes the website, key page, base_url and a call example for 23 platforms.

### Multimodal

- [Free and Low-Cost Text-to-Speech (TTS) APIs: Quotas, Prices, Voice Cloning and Integration](./notes/multimodal/Free-and-Low-Cost-TTS-APIs_en.md) · 2026-10-21
  - Before comparing prices, check how many characters one Chinese character counts as: Bailian, MiniMax and Azure count 2, Doubao, Tencent and StepFun count 1, and SiliconFlow and Fish Audio count UTF-8 bytes. Long-term free quotas include Azure's 500,000 characters a month, Google Cloud's 4 million characters a month and Speechify's 500,000 characters a month; the Gemini free tier costs nothing, but China is not among its available regions. Among pay-as-you-go options that can synthesize Chinese, the cheapest large-model voices cost about 0.9–1.6 yuan per 10,000 characters. Includes voice-cloning prices, open-weight models licensed for commercial use (CosyVoice 3, Qwen3-TTS, VoxCPM2), and how to integrate with Hermes Agent.

- [Free and Low-Cost Text-to-Image: Web Apps, APIs, Local Software and Compliance](./notes/multimodal/Free-and-Low-Cost-Text-to-Image_en.md) · 2026-10-21
  - Without writing code, Chinese websites such as Tongyi Wanxiang, Jimeng, Doubao, Yuanbao and Wenxin generate images for free; free APIs include Zhipu CogView-3-Flash, SiliconFlow Kolors, ModelScope, SenseTime's public beta and Cloudflare's daily quota; the cheapest paid API in China costs about 0.025 yuan per image (MiniMax), and abroad FLUX.2 Klein 4B costs about $0.0005 per image. Includes call examples for 6 free APIs, a compute-unit table for the Draw Things cloud free tier, open-model licenses, and the labeling and filing needed to launch in China.

- [Gemini 3 Pro Image Preview: The ChatGPT Moment for Image Generation](./notes/multimodal/Gemini-3-Pro-Image-Preview_en.md) · 2025-11-20
  - Image models are shifting from "drawing pretty pictures" to "explaining information clearly"; native multimodality lets understanding carry over into generation.

### Self-Improvement

- [Recursive Self-Improvement (RSI) in AI: A Literature Review](./notes/self_improvement/RSI-Literature-Review_en.md) · 2026-10-21
  - After a systematic search of 5,784 candidate papers and a full reading of 365, the review finds plenty of bounded self-improvement in all five strands (weights, context/memory/skills, harnesses, AI-designed components and automated research), but reliable evidence of recursive, compounding self-improvement in none. Multi-round gains shrink or saturate, and the outermost layer always keeps a fixed evaluation or selection step; of 90 studies that call themselves RSI, only 22% audit two or more reruns of the full loop. The signal source sets the ceiling: loops anchored in execution or formal verification are the most stable, self-judged loops reverse or collapse within a few rounds, and the evidence that risk accumulates across generations is firmer than the evidence that capability compounds.
  - Chapter pages: [4](./notes/self_improvement/RSI-Literature-Review-Ch04_en.md) · [5](./notes/self_improvement/RSI-Literature-Review-Ch05_en.md) · [6](./notes/self_improvement/RSI-Literature-Review-Ch06_en.md) · [7](./notes/self_improvement/RSI-Literature-Review-Ch07_en.md) · [8](./notes/self_improvement/RSI-Literature-Review-Ch08_en.md) · [9](./notes/self_improvement/RSI-Literature-Review-Ch09_en.md) · [10](./notes/self_improvement/RSI-Literature-Review-Ch10_en.md) · [11](./notes/self_improvement/RSI-Literature-Review-Ch11_en.md) · [12](./notes/self_improvement/RSI-Literature-Review-Ch12_en.md) · [13](./notes/self_improvement/RSI-Literature-Review-Ch13_en.md)

### Training

- [Chain-of-Thought Synthesis for Training Data: Methods, Evidence, and Open Problems (literature review)](./notes/training/CoT-Data-Synthesis-Literature-Review_en.md) · 2026-10-22
  - After a systematic search of 13,589 candidates, 1,527 inclusions and a full reading of 237 sources: for reasoning data used in SFT and distillation, the emphasis has shifted from "find more questions" to "sample many traces per question, then select for the student", and in 2026 it moved quickly toward on-policy distillation (included papers whose abstracts mention it rose from 2 in the second half of 2025 to 79 in the first half of 2026); for code and agentic data the bottleneck is the diversity of tasks and environments. Four intuitions, "stronger teachers are better", "answer-correct traces are better", "more data is better" and "verification always helps", each have counterexamples from controlled experiments; whether they hold depends on student scale, the teacher-student distribution gap and the training budget. Answer-conditioned generation, length penalties and recursive self-training can damage data in ways that answer accuracy does not reveal.
  - Section pages: [Section 4](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch04_en.md) · [Section 5](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch05_en.md) · [Section 6](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch06_en.md) · [Section 7](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch07_en.md) · [Section 8](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch08_en.md) · [Section 9](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch09_en.md) · [Section 10](./notes/training/CoT-Data-Synthesis-Literature-Review-Ch10_en.md)

- [Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning (full paper, with a Chinese translation)](./notes/training/Dependency-Aware-Trajectory-Refinement_en.md) · 2026-09-16
  - Treats each multi-turn agent trajectory as a round-level dependency DAG and edits it deterministically on the graph: L1 prunes out-degree-0 dead-end rounds, L2 merges sibling rounds that share both parents and children, L3 requires only shared parents and merges iteratively, and L2a/L3a have an LLM rewrite the merged `<think>` into one coherent passage. With SFT of Qwen3-VL-30B-A3B-Thinking on 6196 trajectories, L1 reaches 50.04% average accuracy across four multi-modal QA benchmarks, 1.7 pp above vanilla SFT; L2a matches vanilla SFT accuracy while cutting inference tokens from 20.9K to 11.0K. L3 breaks the one-tool-call-per-turn format used at inference and gets stuck 2–3× as often as L2; the Critical-Path baseline, which has an LLM delete rounds outright, falls below vanilla SFT.

- [Rethinking On-Policy Distillation of Large Language Models II: One Training Example (full paper, with a Chinese translation)](./notes/training/One-Shot-On-Policy-Distillation_en.md) · 2026-09-03
  - Pushes OPD's training data down to a single query: on mathematical reasoning, one-shot OPD reaches 68.5 at step 300 (69.8 for full-data OPD), recovering 87% of full-data OPD's gain, and it holds across three model families and four task domains, even on a hard query the student never solves during training. The explanation has two sides: on the data side OPD consumes states rather than queries, so one query already covers 71.5% of the full-data state space while 16 semantically diverse queries cover 98.9% and match full-data training, in multi-teacher OPD too; on the algorithm side the proportion of the remaining teacher–student gap that one update absorbs keeps falling, at the same pace on 1 query as on all 17k, so OPD is data-overfed but algorithm-starved. Even content-free templates and off-domain WildChat queries approach the real-query baseline.

- [Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe (full paper, with a Chinese translation)](./notes/training/Rethinking-On-Policy-Distillation_en.md) · 2026-04-14
  - A systematic study of what makes on-policy distillation (OPD) succeed or fail and its token-level mechanism. Success needs two things at once: compatible student-teacher thinking patterns, and a teacher that brings knowledge the student has not seen in training — reverse distillation shows same-family 1.5B and 7B teachers are distributionally indistinguishable to the student, and OPD learns thinking patterns rather than benchmark scores. Mechanistically, successful OPD progressively aligns the student's and teacher's high-probability top-k tokens (overlap ratio rising from ~72% to above 91%, carrying 97%–99% of both distributions' probability mass), and optimizing only the overlap tokens suffices. Two recipes recover failing OPD: off-policy cold start and teacher-aligned prompts. It also shows the cost of dense reward — reliability degrades with trajectory depth, failure stems from local optimization geometry rather than signal quality, and support size is not critical as long as Top-1 is avoided.

- [MMAT-1M: A Million-Scale Dataset for Multimodal Agent Tuning](./notes/training/MMAT-1M-Multimodal-Agent-Tuning_en.md) · 2025-07-29
  - GPT-4o adds reasoning, tool calls (image description, OCR, detection, search) and reflection to 5 public visual QA datasets, yielding 902,965 multi-turn dialogues (RR), plus a version compressed to one turn (ORR). After 1 epoch of LoRA fine-tuning on it, InternVL2.5-8B's 8-benchmark average rises from 60.7 to 63.4 and Dyn-VQA from 35.2 to 44.0; applying the format through prompting alone, without fine-tuning, lowers the score. Testing the data also shows that ORR has 16% fewer samples than RR, general reflection only points out "cheating" without re-reasoning, and in many samples the image description already contains the answer; the original image download link is dead, so images have to be found in each source dataset.

- [OpenThoughts: Data Recipes for Reasoning Models (full paper, with a Chinese translation)](./notes/training/OpenThoughts-Data-Recipes-for-Reasoning-Models_en.md) · 2025-06-04
  - Over 1,000 controlled experiments optimize a reasoning SFT data pipeline step by step, yielding OpenThoughts3-1.2M; the OpenThinker3-7B model trained on it reaches 53%, 51% and 54% on AIME 2025, LiveCodeBench 06/24-01/25 and GPQA Diamond. Main findings: having the teacher sample several answers per question grows the data by 16× or more; QwQ-32B, despite lower benchmark scores, is a better teacher than DeepSeek-R1; answer verification and filtering bring no clear gain; using one or two high-quality question sources beats chasing source diversity; and filtering questions by LLM-labeled difficulty or response length works better than pre-training data filters such as fastText and embeddings.

## How this garden is tended

- Each note opens with its source link and date, so it can be traced back.
- Notes are all Markdown, written in Chinese first, each with an English version (`_en.md`); images live in each section's `img/` folder.
- Content grows here slowly, with no rush to call a note finished.

## License

Note content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and code in this repo under [MIT](./LICENSE). Copyright of the cited originals stays with their authors.
