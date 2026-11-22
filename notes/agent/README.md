# Agents

[中文](./README_zh.md) | English

[← Back to home](../../README.md)

- [Agent = Model + Harness: An In-Depth Survey of LLM Harnesses](./Agent-Harness-Survey_en.md) · 2026-10-20
  - A harness is the whole runtime outside the model: system prompt, tools, sandbox, orchestration and context management. When constraints are tight or a generic harness doesn't match how the model was trained, swapping the harness can multiply scores; when conditions are relaxed, it mainly decides the cost. Includes a landscape of major products such as Hermes Agent, Pi, OpenCode and OpenClaw, plus progress on automated harness optimization and harness-native RL.

- [MCP (Model Context Protocol): A Primer](./MCP-Model-Context-Protocol_en.md) · 2026-10-20
  - A "universal port" for AI: a tool vendor builds one server to the standard, and every MCP-capable AI can use it. Includes a complete to-do server example and the renaming pitfall between SDK versions.
