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

- [MCP (Model Context Protocol): A Primer](./notes/agent/MCP-Model-Context-Protocol_en.md) · 2026-10-20
  - A "universal port" for AI: a tool vendor builds one server to the standard, and every MCP-capable AI can use it. Includes a complete to-do server example and the renaming pitfall between SDK versions.

### Inference

- [Flash-Decoding: Faster Long-Context Inference](./notes/inference/Flash-Decoding_en.md) · 2023-10-12
  - During inference the query length is just 1, so parallelizing over the batch doesn't fill the GPU; parallelize over the KV cache's sequence length instead, and long-sequence decoding gets up to 8x faster.

### LLM APIs

- [Free and Low-Cost LLM APIs: Quotas, Prices, Plans and Access](./notes/llm_api/Free-and-Low-Cost-LLM-APIs_en.md) · 2026-10-20
  - The main long-term free options are NVIDIA build, Zhipu's glm-4.7-flash, and the free models on Kilo and OpenRouter; the cheapest Chinese pay-as-you-go tier costs 0.15–1 yuan per million input tokens, and most monthly coding plans only allow interactive use inside tools. Includes the website, key page, base_url and a call example for 23 platforms.

### Multimodal

- [Gemini 3 Pro Image Preview: The ChatGPT Moment for Image Generation](./notes/multimodal/Gemini-3-Pro-Image-Preview_en.md) · 2025-11-20
  - Image models are shifting from "drawing pretty pictures" to "explaining information clearly"; native multimodality lets understanding carry over into generation.

## How this garden is tended

- Each note opens with its source link and date, so it can be traced back.
- Retold in my own words, not copied from the source; only the figures that carry the argument are kept.
- Notes are all Markdown, written in Chinese first, each with an English version (`_en.md`); images live in each section's `img/` folder.
- Content grows here slowly, with no rush to call a note finished.

## License

Note content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and code in this repo under [MIT](./LICENSE). Copyright of the cited originals stays with their authors.
