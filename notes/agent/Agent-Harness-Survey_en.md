# Agent = Model + Harness: An In-Depth Survey of LLM Harnesses

[中文](./Agent-Harness-Survey.md) | English

- **Research date**: 2026-10-20
- **Scope**: agent harnesses in the LLM field, covering definition and anatomy, the main products, evidence for and against their effect, automated harness optimization, the training loop and evaluation. Sources mainly cover papers, vendor engineering blogs and open-source projects from late 2025 to October 2026.
- **Basis**: superscript numbers at the end of a sentence are citations, matching the references at the end. Content marked (inferred), (synthesis) or (estimate) is inferred, synthesized or estimated from the cited sources.
- **Freshness**: GitHub star counts were read from the repository pages on 2026-10-20 and only reflect developer attention. Products change quickly; check the official pages.

## Bottom Line

- **The definition has converged**: a harness is all the code, configuration and execution logic outside the model, including the system prompt, tools and Skills/MCP, sandbox, orchestration, hooks and context management[^1]. It is also called agent scaffolding, and is often written as agent = model + harness[^2].
- **Products have reached scale**: by GitHub stars, the leading open-source harnesses are OpenClaw (about 393K), Hermes Agent and DeepSeek Harness (about 255K each)[^65][^62][^52]. They are followed by OpenCode (about 218K) and Claw Code (about 195K)[^64][^70]. (synthesis) Nearly every major model vendor has launched its own harness, and IDE and tool vendors have turned their agents into CLIs and SDKs; see Section 3.
- **Gains are conditional**: when constraints are tight, when a generic harness doesn't match how the model was trained, or when the task exceeds what the model can complete on its own, swapping the harness can multiply scores, as on ARC-AGI-3, from 13.3% to 38.3%[^16]. When conditions are relaxed, the heaviest and lightest harnesses are equivalent within 5 points on the 447 tasks of SWE-bench Verified; on 45 hard tasks, swapping the harness flips the same share of tasks as rerunning the same configuration, 13% in both cases[^19]. What the harness reliably determines is the bill: with the same model, the same tasks and the same price list, cost per task differs by up to 3x[^19].
- **Read leaderboards with a discount**: on Terminal-Bench 2.0 (TB2), with Opus 4.6 in both cases, Claude Code scores 58.0% and ForgeCode 81.8%[^13]. But according to a third-party tracker, the top entries are mostly unverified self-reports by maintainers with overlapping confidence intervals, and TB2 was replaced after 28 of its 89 tasks were found defective[^21]. Resource configuration alone can move TB2 scores by 6 percentage points[^20].
- **The harness has become an optimization target**: Meta-Harness, Self-Harness, VERSE and others treat the harness as searchable code[^13][^26][^27]. VERSE's controlled experiment shows that without execution-based verification, the optimizer's self-evolution doesn't help[^27].
- **The harness has entered the training loop**: LangChain notes that products like Claude Code and Codex are post-trained with the harness in the loop[^1]. A new generation of RL frameworks hands the interaction loop to the harness used in deployment, which raises new issues around retokenization, sample merging, advantage computation and loss normalization[^38]. When the harness and the policy are optimized in alternation, the joint gain exceeds the sum of the two separate gains[^36].

## 1. What "Harness" Means

### 1.1 Five Senses of the Word

| Sense | Scope | Examples |
| --- | --- | --- |
| Agent harness (runtime, also called scaffold) | System prompt, tools/Skills/MCP, sandbox, orchestration, hooks, context management | Claude Code, Codex, OpenCode, Pi, Hermes Agent and others; see Section 3[^1][^9] |
| User-side outer harness | `AGENTS.md`, skills, custom linters, structural tests, pre-commit hooks | Hashimoto, OpenAI, Böckeler[^3][^4][^6] |
| Evaluation harness | Runs tasks, records trajectories, grades, aggregates | lm-eval, HAL, Harbor[^43][^18][^44] |
| Training harness / RL environment | Rollout loop, tool execution, reward | verl Agent Loop, Agent Lightning, Uni-Agent[^42][^38][^39] |
| Classic test/fuzz harness | The program that drives the code under test | OSS-Fuzz-gen uses an LLM to generate fuzz harnesses[^54] |

Wikipedia also lists the test harness of software testing, the evaluation harness of LLM benchmarking and the environment that wraps an agent in RL as related notions[^2]. Böckeler separates two layers: the harness built into a coding agent (system prompt, retrieval mechanisms, orchestration), and the outer harness that users build on top of it for their own setting[^6].

**Relation to prompt/context engineering**: one common framing is that prompt engineering optimizes a single interaction, context engineering manages what the model sees at a given moment, and harness engineering designs the whole operating environment and contains the other two[^2]. Böckeler sees the user-side harness as a specific form of context engineering[^6]; LangChain says today's harnesses are largely delivery mechanisms for context engineering[^1]. (inferred) The two views don't conflict: context engineering answers "what does the model see", while harness engineering also answers "in what environment and loop does the model run, and what verifies it".

### 1.2 Timeline

| Date | Event |
| --- | --- |
| 2023 | The UK AI Security Institute described an AI agent as a model plus scaffolding[^2] |
| 2025-10 | HAL releases a standardized evaluation harness and analyzes along three dimensions: model × scaffold × benchmark[^18] |
| 2025-11-26 | Anthropic publishes "Effective harnesses for long-running agents", calling the Claude Agent SDK a general-purpose agent harness[^7] |
| 2026-01-23 | OpenAI publishes "Unrolling the Codex agent loop", calling Codex's agent a harness[^48] |
| 2026-02-05 | Mitchell Hashimoto proposes "Engineer the Harness": every time an agent makes a mistake, engineer a fix so it never makes that mistake again[^3] |
| 2026-02-11 | OpenAI publishes "Harness engineering", describing an internal product of about a million lines with zero hand-written code[^4] |
| 2026-03-10 | LangChain publishes "The Anatomy of an Agent Harness"[^1] |
| 2026-03-30 | Meta-Harness treats the harness as an end-to-end optimization target[^13] |
| 2026-03-31 | Claude Code's npm package accidentally ships a source map and its source leaks[^107]; community rewrites such as Claw Code follow[^9] |
| 2026-04-02 | Böckeler proposes the guides/sensors framework[^6] |
| 2026-05-19 | Google announces Antigravity CLI as the successor to Gemini CLI[^86] |
| 2026-06 | Databricks open-sources the meta-harness Omnigent[^9] |
| 2026-07 to 10 | Source-code anatomy[^9], harness-based agentic RL[^38][^41], automated harness optimization[^27][^28] and counter-evidence studies[^19] cluster in this period |
| 2026-08-13 | The DeepSeek Harness repository is created[^71]; by 2026-10-20 it has about 255K stars[^52] |

The attribution of the term is disputed: some credit Hashimoto's February blog post, others LangChain's Vivek Trivedy[^2]. Böckeler notes that the OpenAI article mentions "harness" only once, and guesses the word may have been inspired by Hashimoto[^5]. (inferred) The noun harness was already in use in vendor articles in late 2025[^7]; what got named in early 2026 was the discipline[^9].

## 2. Anatomy: What a Harness Is Made Of

- **Seven subsystems**: a source-code study compared 11 production harnesses (listed in Section 3.1) and identified seven subsystems: the agent loop, LLM integration, memory and context, tools and actions, safety and permissions, extensibility and orchestration, plus an interface layer[^9].
- **Six runtime responsibilities**: another survey breaks a harness into six responsibilities: observation, context, control, action, state, and verification/governance[^10].
- **Nobody uses a general-purpose framework**: even after the corpus tripled to about 4 million lines of code, no agent runtime imports a general-purpose agent framework such as LangChain, LangGraph or AutoGen, and none retrieves code with vector embeddings[^9]. They retrieve with deterministic tools such as ripgrep, tree-sitter and glob[^9].
- **Extension standards**: `SKILL.md` adoption (9 of the 11) has overtaken MCP (8)[^9].
- **From convergence to imitation**: within one quarter, Codex adopted Claude Code's hook vocabulary verbatim and shipped an importer for its sessions; behavioral policy also migrated from prompt text into configuration[^9].
- **Complexity doesn't predict scores**: the systems' code sizes span three orders of magnitude, but loop complexity doesn't predict benchmark scores[^9]. mini-SWE-agent's minimal linear loop and OpenHands's event-sourced engine score in the same range[^9].
- **Vendors open up their harnesses**: OpenAI open-sourced the Codex harness and, through the app-server protocol, lets applications create threads, start turns, receive events and handle approvals[^49]. Anthropic's Managed Agents virtualizes the session (an append-only event log), the harness (the loop that calls the model and routes tool calls) and the sandbox into three independently replaceable interfaces, and calls itself a meta-harness[^11].

### 2.1 Design Patterns with Evidence

| Pattern | Failure it targets | How | Source |
| --- | --- | --- | --- |
| Externalized progress | Amnesia across context windows; declaring completion too early | An initializer agent writes a feature list (JSON, 200+ items, all initially failing), a progress file and git commits; each session then works on one feature | [^7] |
| Map-style `AGENTS.md` | Huge instruction files crowd out context and go stale fast | A table of contents of about 100 lines, with docs/ as the system of record and linters and CI checking that docs stay fresh | [^4] |
| Executable constraints | Architectural drift | Custom linters and structural tests whose error messages contain the fix instructions | [^4][^6] |
| Verify before exit | Writing code, reading it once and stopping | A `PreCompletionChecklist` middleware or a Ralph loop hook intercepts the exit | [^14][^1] |
| Loop detection | Making small edits to the same approach 10+ times | Count edits per file and inject "reconsider your approach" after N edits | [^14] |
| Time budget and reasoning "sandwich" | Timeouts | Inject time-budget reminders; use xhigh reasoning for planning and verification, high for implementation | [^14] |
| Context resets and compaction | Context anxiety | Start a fresh window after a structured handoff; remove once model behavior improves | [^22][^11] |
| Separate generation from evaluation | Overly optimistic self-assessment | An independent evaluator drives the app with Playwright and sends work back below a threshold | [^22] |
| Progressive disclosure and output offloading | Too many tools; large outputs pollute context | Skills load only their front-matter at startup; long tool outputs keep the head and tail, with the full text written to a file | [^1] |
| Garbage collection | Agents copy bad patterns already in the repo | Background agents periodically scan for drift and open refactoring PRs | [^4] |
| Decoupling the brain from the hands | Containers become "pets"; credential leaks | The sandbox is a tool, `execute(name, input) → string`; credentials never enter the sandbox | [^11] |

## 3. Major Harness Products

The source-code study argues that in the first half of 2026 coding harnesses completed the shift from tools to platforms[^9]. Harnesses became importable SDKs, and framework vendors began shipping harnesses of their own[^9]. This section groups the main products as of 2026-10-20 by who makes them. GitHub stars are only a reference for attention, not for user numbers or quality.

The scope is harnesses you can use directly, including coding agents and personal-assistant agents. Frameworks such as LangChain, AutoGen and CrewAI are not included: in the paper's distinction, a framework is a library developers import to build agents, while a harness is the runtime developers work inside[^9]. App-generation platforms and hosted general-purpose agent products are also out of scope for this section.

### 3.1 The 11 Systems Covered by the Source-Code Study

The study selected its sample by design philosophy, maturity and market position[^9]. The sample includes the flagship agent of each of four major model vendors, plus seven open-source projects[^9]. It only describes and compares implementations; it does not benchmark or rank them[^9].

| System | Maker | Language / code size | Model access | Execution isolation | Signature design, as the paper summarizes it[^9] | GitHub stars |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Code | Anthropic | TS / Large | Anthropic only | Optional runtime + worktree | Deferred tool loading; forks that share the prompt cache; the reference other systems imitate | 153K[^68] |
| Codex | OpenAI | Rust / Very large | OpenAI only | Native sandbox (3 OSes) | Cross-session memory maintained by the agent; tool calls expressed as code executed in V8 | 130K[^66] |
| Gemini CLI | Google | TS / Very large | Google only | Native sandbox (3 OSes) | Model routing treated as runtime scheduling; the only A2A server in the sample | 107K[^67] |
| Mistral Vibe | Mistral | Python / Small | Mistral first, others possible | Optional worktree | A middleware-pipeline loop; rollback exposed over ACP | 5K[^112] |
| OpenHands | OpenHands (formerly All-Hands-AI) | Python / Medium | Multiple (LiteLLM) | Docker, Apptainer or remote | Parallel tools with resource locks; can use other harnesses as ACP backends | 91K[^73] |
| Aider | Community (P. Gauthier), maintenance mode | Python / Small | Multiple (LiteLLM) | None | 13 edit formats; the only ranked repo map in the sample | 50K[^76] |
| mini-SWE-agent | Princeton / Stanford | Python / Tiny | Multiple (LiteLLM) | Docker and others | All seven subsystems in about 100 lines | 9K[^53] |
| Hermes Agent | Nous Research | Python / Very large | Multiple (own transport layer) | 6 pluggable execution backends | A self-improving skill loop; lineage-based compaction; verify-on-stop | 255K[^62] |
| Pi | earendil-works (M. Zechner) | TS / Medium | Multiple (35 providers) | None (by design) | An everything-is-an-extension kernel; session-tree version control | 117K[^63] |
| OpenCode | Anomaly (formerly SST) | TS / Large | Multiple (Vercel AI SDK) | None (relies on permission policy) | Client/server architecture; syntax-aware command authorization | 218K[^64] |
| OpenClaw | Community | TS / Large | Multiple | None | Gateway delegation; a memory sub-agent runs before every reply | 393K[^65] |

- **Code size** uses the paper's coarse bands: Tiny is about 5,000 lines, Small 20K–40K lines, Medium 80K–110K lines, Large 500K+ lines and Very large 600K+ lines (Codex is about 1.1 million lines of Rust)[^9]. The paper cautions that these numbers can't be compared directly across languages and counting methods[^9].
- **Claude Code's data** comes from a March 2026 source snapshot[^9]. That month, npm package 2.1.88 published by Anthropic accidentally included a source map, leaking nearly 2,000 TypeScript files and more than 512,000 lines of code[^107]. Claude Code is not open-source software: the repository's LICENSE states that all rights are reserved[^69].
- **Model access falls into three kinds**: Claude Code, Codex and Gemini CLI connect only to their own vendor's models[^9]; OpenHands, Aider and mini-SWE-agent reach multiple vendors through LiteLLM[^9]. Hermes, Pi and OpenCode instead maintain provider-specific adapter code centrally, and the paper argues that they show a multi-provider architecture can still get all of a vendor's native optimizations[^9].

### 3.2 Hermes Agent, Pi, OpenCode and OpenClaw

These four open-source projects are all in the source-code study's sample and represent four different design directions. DeepSeek Harness draws about as much attention as Hermes Agent, but its repository was only created on 2026-08-13[^71], after the study's July 2026 snapshot[^9], so it is covered in Section 3.3.

#### Hermes Agent (Nous Research): Personal Assistant and Coding in One

- The paper calls it the fastest-growing open-source harness, with about 212K stars within five months of release (counted on 2026-07-10)[^9].
- It sits between two kinds of product: like OpenClaw it connects to messaging channels such as Telegram, Discord and Slack, yet it also ships a full native coding toolset[^9].
- **Model access**: five transport protocol implementations, backed by 29 declarative `ProviderProfile` plugins[^9].
- **Caching**: each session assembles its prompt once, in three layers: stable, context and volatile[^9]. The prefix is normalized byte for byte (tool-call JSON is sorted and compactly re-serialized, timestamps keep only the date, memory is frozen into a snapshot), so the KV cache of local llama.cpp and vLLM also hits across turns[^9].
- **Context**: compaction doesn't rewrite the transcript; it ends the current session and rotates to a child session linked by `parent_session_id`[^9]. Context management and session persistence thus become one mechanism, and history is never destroyed[^9].
- **Memory**: `MEMORY.md` is capped at 2,200 characters and `USER.md` at 1,375, both injected as frozen snapshots, so writes to disk mid-session don't invalidate the prompt cache[^9]. The agent writes, patches and curates its own skills, and among the paper's 11 systems only Hermes has this pattern in full[^9].
- **Loop**: there are 11 enumerated exit reasons, plus two stop-guards that can veto a premature final answer[^9]. One of them, verify-on-stop, rewrites the closing reply into a continuation when the turn changed code but produced no new verification evidence[^9].
- **Safety**: it is the largest Python system in the sample, yet it carries no OS-level isolation primitives and leaves isolation to six pluggable execution backends[^9]. The local backend relies on a 3,200-line approval module, whose 12 hard floor rules still apply in `--yolo` mode[^9].
- **Orchestration**: delegation is flat by default[^9]. Kanban swarm puts planning, parallel execution, verification and aggregation into separate `hermes -p <profile>` subprocesses, coordinated through a SQLite board[^9].
- **Version**: the paper analyzed version 0.18.2 from July 2026[^9]. Things have changed since; for example, the default main-loop iteration cap went from the 90 the paper records to 500[^9][^119].

#### Pi (earendil-works / M. Zechner): A Minimal Kernel

- The paper treats it as the representative of the "minimal kernel" counter-trend[^9]. On GitHub it describes itself as an AI agent toolkit, including a unified LLM API, an agent loop, a TUI and a coding agent CLI[^63].
- **Loop**: a functional kernel of about 790 lines, with no planner, reflection step, turn limit, stall detection or cost circuit breaker; it stops only when the model stops calling tools[^9]. These absences are all documented as deliberate design trade-offs[^9].
- **Prompt**: the entire system prompt is generated by a builder of about 170 lines, and its output is only 30–40 lines[^9]. Nearly all behavioral policy is left to the user's context files and extensions[^9].
- **Extensions**: the kernel itself is an event bus, with about 33 typed events covering everything from tool interception to raw provider I/O[^9]. The core has no spawn or task tool; sub-agents come as an extension, and each call starts a separate pi process[^9].
- **Sessions**: a session is an append-only JSONL tree in which every entry has an id and a parentId, and a movable leaf pointer determines the current branch[^9]. `/tree`, `/fork` and `/clone` unify the checkpoints, rewinds and branch exploration that other harnesses implement separately[^9].
- **Safety**: it is the only system in the sample that makes "no safety features" a design principle; its docs argue that an incomplete in-process sandbox is easily mistaken for a security boundary[^9].
- **Model access**: 9 hand-written protocol implementations and 35 built-in providers[^9]. With a Claude Pro/Max OAuth token, it fully impersonates Claude Code's identity to use the consumer subscription[^9].
- **Embeddable**: `pi-agent-core` can be imported as a library and also offers an RPC mode[^9]. Omnigent can orchestrate Pi[^102], and Fireworks's RL training example supports Pi too[^40].

#### OpenCode (Anomaly, formerly SST): A Client/Server Architecture

- The paper calls it the most-starred dedicated coding agent on GitHub (about 184K on 2026-07-10)[^9].
- **Architecture**: an embedded HTTP server that publishes an OpenAPI spec and generated SDKs; the TUI, desktop, web, IDE plugins and CI action are all its clients[^9]. About three-fifths of the non-test code is these clients rather than the harness itself[^9].
- **Model access**: streaming and tool dispatch are handed to the Vercel AI SDK and models.dev, making it the only system in the sample whose underlying LLM path depends on a third-party SDK[^9]. It picks one of 9 base prompts by model-ID substring[^9].
- **Loop**: the message log doubles as the work queue, so it can resume directly after a process restart[^9]. There is no step limit by default[^9]. Three identical tool calls in a row trigger a `doom_loop` permission prompt, so the user, not the harness, judges whether something has gone wrong[^9].
- **Safety**: after Hermes, it is the second-largest system without OS-level isolation, and by default it allows everything inside the project, the exact opposite of Codex[^9]. Every bash command is parsed with tree-sitter before it is authorized[^9].
- **A neutral harness in research**: Doc2Harness builds all its harnesses with OpenCode, on the grounds that Claude Code and Codex CLI are developed by model vendors together with their own models and may favor them[^32]. Harness2 uses OpenCode and Codex as the harnesses for its frozen executor[^30], and Fireworks's RL example supports three adapters: OpenCode, Pi and mini-SWE-agent[^40].
- **Measured**: on the large SWE-bench Verified task pool, OpenCode trails by up to 9 points, and for one model half of the gap comes from runs cut off by the output limit[^19].

#### OpenClaw (Community): A Multi-Channel Personal Assistant Gateway

- It has about 393K GitHub stars[^65], the most of any project listed in this survey.
- Its README calls it a personal AI assistant gateway, not a coding agent, covering more than 20 messaging platforms[^9]. It has no code-editing tools and delegates coding tasks through plugins to specialized agents such as opencode, kimi-coding and github-copilot[^9]. The paper therefore uses it as a control, saying it consumes rather than implements coding capability[^9].
- Before every reply, the Active Memory plugin first runs a dedicated memory sub-agent[^9]. Multi-agent work goes through an ACP translation layer, with sub-agents spawned as subprocesses[^9].
- Safety rests mainly on the gateway's scoped authorization, which distinguishes two connection roles, operator and node[^9]. Other mechanisms include rate limiting per IP or token, an SSRF policy, a DM allowlist and pairing approval[^9].
- Agent Lightning classes OpenClaw and Hermes as general-purpose harnesses, alongside coding harnesses[^38]. The community has also produced a wave of lightweight alternatives, such as nanobot in about 4,000 lines of Python, NanoClaw running in containers, PicoClaw that runs on $10 hardware, and IronClaw, rewritten in Rust and isolated with a WASM sandbox[^110].

### 3.3 Other Vendor and Open-Source Harnesses

#### Model Vendors' Own Harnesses

The paper observes a wave of harnesses from Chinese vendors (Alibaba's Qwen Code, Moonshot AI's Kimi CLI, ByteDance's Trae Agent) that tie the release of open-weight models to the vendor's own CLI[^9]. (synthesis) By the second half of 2026, most major model vendors had a harness of their own.

| Product | Maker | Form / license | Key points |
| --- | --- | --- | --- |
| Claude Agent SDK, Claude Cowork | Anthropic | SDK; desktop and web product | Anthropic calls the Claude Agent SDK a general-purpose agent harness[^7]. Cowork brings Claude Code's agent capabilities to knowledge work beyond coding[^105]; according to an Anthropic engineer on Hacker News, it runs Claude Code's agent harness inside a Linux VM, with added sandboxing, network controls and file system mounts[^106] |
| Antigravity CLI | Google | Closed source, Go[^9] | Announced on 2026-05-19 as the successor to Gemini CLI, sharing its architecture with the Antigravity 2.0 desktop app[^86]. From 2026-06-18, Gemini CLI stopped serving free, Google AI Pro and Ultra users; enterprise users are not affected[^86]. The Gemini CLI repository remains open under Apache 2.0 and keeps getting model support updates and fixes for enterprise customers[^86] |
| Grok Build | xAI (SpaceXAI) | Apache-2.0, Rust, 27K stars[^77] | A full-screen TUI that runs interactively or headless and can also be embedded in editors via ACP[^77]. The paper's July 2026 landscape table marks it as not open source[^9]; its GitHub repository was only created on 2026-07-14[^72] |
| Muse Code | Meta | Terminal and CI | A coding agent built for the Muse Spark model, with approvals and an OS sandbox turned on from the first run[^78] |
| DeepSeek Harness | DeepSeek | MIT, 255K stars[^52] | An open-source agent harness with an everything-is-a-plugin architecture[^52]. The repository was only created on 2026-08-13[^71] and is still in developer preview[^52] |
| Kimi Code CLI | Moonshot AI | MIT, 8K stars[^79] | Uses Kimi models by default and can be configured for other compatible providers[^79]; comes in three forms: desktop, CLI and IDE plugin[^80]. The repository was created on 2026-05-22[^120], and the older Python Kimi CLI was archived on 2026-09-23[^81] |
| Qwen Code | Alibaba Tongyi | Apache-2.0, 29K stars[^111] | The paper calls it a fork of Gemini CLI that serves Qwen's coding models[^9] |
| Qoder, Qoder CLI | Alibaba | IDE, CLI, JetBrains plugin | An agentic coding platform launched on 2025-08-22[^97], spanning a desktop IDE, a CLI and a JetBrains plugin[^98], and offering the Qoder Agent SDK[^99] |
| ZCode | Zhipu Z.ai | Apache-2.0, 8K stars[^83] | Describes itself as Z.ai's coding agent harness[^83], and the website calls it the official harness for GLM-5.3[^82]. The repository was created on 2026-09-20[^121] |
| MiMo Code | Xiaomi | MIT, 14K stars[^84] | A terminal-native coding assistant with a persistent memory system that carries across sessions[^84]. The project's tagline is "Where Models and Agents Co-Evolve"[^84], and the repository was created on 2026-06-10[^122] |
| CodeBuddy Code | Tencent | CLI | The AI CLI tool for professional engineers in the CodeBuddy product line[^100]. Tencent says CodeBuddy is built on the Hunyuan code model and is used by more than half of its internal developers[^100] |
| Comate CLI | Baidu | CLI, distributed via npm | A terminal AI coding assistant with both an interactive TUI and a headless CLI that plugs into CI[^101]. It has three modes: Agent, Plan and Goal[^101] |
| Trae Agent | ByteDance | MIT, 12K stars[^116] | A research-oriented Python CLI agent[^9] |

#### IDE Vendors, Tool Vendors and Startups

| Product | Maker | Key points |
| --- | --- | --- |
| Cursor CLI, Cursor SDK | Anysphere (SpaceXAI) | Cursor CLI provides the same harness in the terminal as in the IDE[^9]. Cursor SDK lets developers build agents with the same harness, runtime and models that power Cursor[^88]. In June 2026 SpaceX announced it would acquire Cursor for $60 billion[^9]; SpaceXAI has an Agent Harness team responsible for the core behavior and capabilities of the agents across Cursor's products[^89] |
| GitHub Copilot CLI | GitHub | Generally available to all Copilot subscribers on 2026-02-25[^87]. It has a plan mode and a fully autonomous autopilot mode, and automatically delegates tasks to specialized agents such as Explore, Task, Code Review and Plan[^87]; models can be chosen from Anthropic, OpenAI and Google[^87] |
| Devin CLI, Devin Desktop | Cognition | Devin CLI (2026-04-27) is a local coding agent that can use any frontier model or Cognition's own SWE-1.6[^90]. Devin Desktop (2026-06-02) is the next generation of Windsurf, in which any ACP-compatible agent can run alongside Devin[^91] |
| Kiro CLI | AWS | The paper says it evolved from Q Developer and focuses on spec-driven development[^9]; it runs on Claude frontier models[^92] |
| Junie | JetBrains | A coding agent that works with any model[^93] |
| Droid | Factory | Topped Terminal-Bench with 58.75% in September 2025[^94]. Factory argues that the right agent framework can bring larger gains than switching models[^94] |
| Amp | Sourcegraph | Agents can run anywhere and keep working after you shut down your computer[^95] |
| Warp | Warp | An agentic development environment that evolved from a terminal[^96] |
| pool | Poolside | Runs in the terminal or in any ACP-compatible editor[^85]; backed by Poolside's own Laguna models, with binaries distributed under a proprietary EULA[^110] |
| Others | Augment, Snowflake, Tabnine and more | The community list also includes Augment's Auggie, Snowflake's Cortex Code CLI and Tabnine CLI, which needs an enterprise license, among others[^110] |

#### Open-Source Community Projects

| Project | Maintainer | GitHub stars | Key points |
| --- | --- | --- | --- |
| Claw Code | Community | 195K[^70] | Describes itself as a clean-room rewrite (Python and Rust) made after the March 2026 Claude Code source leak, and passed 100K stars within days[^9]. The paper takes this as a sign that harness architecture can attract community attention on its own, not just through the model[^9] |
| Cline | Cline Bot Inc. | 71K[^74] | More than 5 million IDE installs, built around a plan/act workflow, and the source of forks such as Roo and Kilo[^9]. Roo Code was archived on 2026-05-15[^108], and Kilo Code has about 28K stars[^115] |
| goose | AAIF (formerly Block) | 55K[^75] | Supports MCP natively; donated to the Agentic AI Foundation in April 2026[^9] and now part of AAIF under the Linux Foundation[^75] |
| Deep Agents | LangChain | 30K[^113] | Describes itself as a batteries-included agent harness[^113]. Built on LangGraph, with todo planning, a permission-controlled virtual file system, sub-agents, and `SKILL.md` and `AGENTS.md` memory[^9] |
| Crush | Charmbracelet | 29K[^114] | A Go-native, LSP-aware TUI that descends from the early Go version of opencode[^9] |
| ForgeCode | tailcallhq | 8K[^109] | Supports more than 300 models[^109]. On the TB2 leaderboard, Opus 4.6 with ForgeCode scores 81.8%[^13], but the Meta-Harness authors could not reproduce this result with the public code[^13] |
| Open Interpreter, Codewhale, Reasonix, Prime Agent | Community and startups | 22K–69K[^110] | Open Interpreter is often used as an agent that gets work done on your own machine[^110]. Codewhale (formerly deepseek-tui) supports 30+ providers and local vLLM, SGLang and Ollama[^110]. Reasonix is a single Go binary built for long unattended runs[^110]. Prime Agent uses one persistent IPython kernel as the model's only tool[^110] |
| Browser Use | Browser Use | 119K[^118] | An open-source Python library for browser agents[^118]; for its minimal-harness position, see Section 8 |

Another baseline harness common in research and evaluation is Terminus 2, developed by the Terminal-Bench team as a neutral test bed for comparing models[^12].

### 3.4 The Ecosystem Layer: Protocols, Meta-Harnesses and Orchestration

- **ACP (Agent Client Protocol)**: the paper calls it an editor-facing JSON-RPC standard driven by Zed and Google[^9]. The official site lists 43 agents (counted from that page), including Claude Agent, Codex CLI and Pi, which connect through adapters[^104]. Gemini CLI, GitHub Copilot, Hermes Agent, Kimi CLI, Kiro CLI, OpenClaw, OpenCode, OpenHands, Qoder CLI, Qwen Code and others are also listed[^104]. Devin Desktop lets any ACP-compatible agent run alongside Devin[^91].
- **Meta-harness**: Databricks open-sourced Omnigent under Apache 2.0 in June 2026[^9]; it has about 11K GitHub stars[^117]. It sits on top of existing agents such as Claude Code, Codex and Pi, making them interoperable parts of a larger system[^102]. Its registry ships 23 harness adapters in five integration modes: `sdk-in-process`, `cli-subprocess`, `acp-subprocess`, `native-tui` and `native-server`[^9]. The capabilities an adapter declares must pass conformance tests, which the paper describes as "testing harnesses the way you test hardware"[^9]. The paper reads it as a bet that the harness has become a commodity component, with lasting value one layer up[^9].
- **Task orchestration**: Symphony, open-sourced by OpenAI, turns project work into isolated, autonomous implementation runs, so teams manage work instead of supervising coding agents[^103]. It works best in codebases that have adopted harness engineering[^103]. Community orchestration layers also include claude-flow (about 77K stars), Oh My OpenAgent (about 70K stars, layered on OpenCode, Codex and Pi) and vibe-kanban (about 28K stars)[^110].

### 3.5 Observations on the Landscape

- **Model vendors are building their own harnesses**: beyond Anthropic, OpenAI and Google, xAI, Meta, Mistral, DeepSeek, Moonshot AI, Alibaba, Zhipu, Xiaomi, Tencent and Baidu all have their own harness (see Sections 3.1 and 3.3). But an in-house harness doesn't mean a higher score: in a controlled experiment, vendors' own harnesses showed no score advantage on their own models[^19].
- **Closing up and consolidation**: Google replaced the Apache 2.0 Gemini CLI with the closed-source Antigravity CLI[^9]; after acquiring xAI, SpaceX announced it would acquire Cursor for $60 billion[^9]. The paper concludes that the harness layer is no longer open territory but strategic infrastructure that vendors acquire, rebrand and gate[^9].
- **Open-source harnesses draw more attention**: (synthesis) by stars, OpenClaw, Hermes Agent, DeepSeek Harness and OpenCode all rank above the Claude Code and Codex repositories (data in Sections 3.1 and 3.3), but stars reflect developer attention, not usage. Claw Code passed 100K stars within days, which the paper takes as evidence that harness architecture can attract community attention on its own[^9].
- **From products to components**: ACP lets the same agent embed in different editors[^104], Omnigent orchestrates whole harnesses as components[^102], and RL frameworks such as Agent Lightning plug existing harnesses straight into training (see Section 6.2)[^38]. (inferred) Competition is shifting from the features of a single harness to whether it can be plugged into editors, meta-harnesses and training frameworks.

## 4. What a Harness Is Worth: Evidence For and Against

| Evidence | Setup | Harness change | Result | Transferability |
| --- | --- | --- | --- | --- |
| TB2 leaderboard (compiled by Meta-Harness) | 89 tasks | Different harnesses | Opus 4.6: 58.0% (Claude Code) to 81.8% (ForgeCode); Haiku 4.5: 13.9% (OpenHands) to 37.6% (Meta-Harness)[^13] | Mostly self-reported; ForgeCode can't be reproduced with its public code[^13][^21] |
| LangChain deepagents | gpt-5.2-codex, TB2 | Prompts, middleware, reasoning budget | 52.8% → 66.5%[^14] | Iterated against a single benchmark |
| Harness profiles | Hard subset of tau2-bench | Prompts, tools and middleware tuned per model | GPT-5.3 Codex 33% → 53%; Opus 4.7 43% → 53%[^15] | A subset, tested by the authors themselves |
| ARC-AGI-3 | GPT-5.6 Sol | Keep reasoning; replace rolling truncation with compaction | 13.3% → 38.3%, with 6x fewer output tokens[^16] | The official harness itself is flawed |
| Same Model, Different Harness | 20,480-token window, 169 tasks | Shorten old tool outputs as the context fills, and react to stalls | F2PF 28% → 49%; full solves 43 → 72[^17] | The two groups are close with a wide window[^17] |
| Are Harnesses Worth the Cost? | 1 Java service, 10 paired runs per model | Behavioral harness (contracts, mocks, tests) | GPT-6 Luna 3/10 → 10/10; GPT-6 Sol 10/10 in both cases, but at about 7x the cost[^24] | Small sample, a single task |
| What Does a Harness Buy? | SWE-bench Verified: 447 tasks (2 models) and 45 hard tasks (5 models) | Claude Code, mini-SWE-agent, OpenCode | Equivalent within 5 points on the 447 tasks; on the 45 hard tasks, swapping the harness and rerunning both flip 13% of tasks; cost differs by up to 3x[^19] | A single benchmark; closed models ran only in Claude Code[^19] |
| HAL | Online Mind2Web | SeeAct + GPT-5 Medium vs. Browser-Use + Claude Sonnet 4 (the models differ too, so this is not a same-model comparison) | Cost $171 vs. $1,577 (9x), with accuracy only 2 percentage points apart; Claude does better with Browser-Use, OpenAI models do better with SeeAct[^18] | The model and the scaffold interact |
| Infrastructure (not the harness) | TB2, same model and same harness | Resource limits from 1x to uncapped | +6 percentage points[^20] | A confounding factor |

**How to reconcile them** (inferred): the large gains almost all appear under three conditions: tight constraints, meaning a small context window or a timeout[^17][^14]; a generic harness that doesn't match how the model was trained and deployed, such as dropping reasoning at every step or truncating history on a rolling basis[^16]; and tasks beyond what the model can complete reliably on its own[^24][^22]. When conditions are relaxed (frontier models, wide windows, standard SWE tasks), the harness mainly changes the token bill[^19]. This matches the conclusion of "What Does a Harness Buy?": what a harness buys is fewer ways to fail and a bill, not a higher pass rate[^19]. Every harness effect that paper measured made the model lose tasks it could have solved, for example failing to recover after output truncation, or having no compaction when the context filled up[^19].

**Noise in the measurement itself**: when comparing harnesses on 45 tasks, a 13-point gap is detected only half the time; 447 tasks can resolve about 5 points[^19]. The authors recommend reporting a rerun of the same configuration next to any harness gap[^19]. (estimate) If TB2's 89 tasks are treated as a sample of a task population, then at a pass rate around 75% the binomial standard error of a single run is about 4.6 percentage points, larger than the gaps between the top few entries.

## 5. Automation: The Harness Becomes Searchable Code

| Work | Institution | What it optimizes | Key results |
| --- | --- | --- | --- |
| AutoHarness | Google DeepMind | A small model writes its own code harness, from action validation all the way to the entire policy | Illegal moves eliminated in all 145 TextArena games; the code policy beats Gemini-2.5-Pro and GPT-5.2-High on 16 single-player games[^25] |
| Meta-Harness | Stanford, MIT, KRAFTON | An agentic proposer reads the source code, scores and trajectories of all past candidates through the file system | TB2: Opus 4.6 at 76.4% (the strongest hand-built harness, Terminus-KIRA, is at 74.7%), Haiku 4.5 at 37.6%[^13] |
| Self-Harness | Shanghai AI Laboratory | Weakness mining → change proposals → regression verification, without relying on humans or stronger models | Held-in and held-out scores improve for all 9 model and benchmark combinations, with relative gains of up to 132%[^26] |
| VERSE | MIT, Amazon | Co-evolves the optimizer's own tools and workflow | Best harness at 42.3% (strongest baseline 39.2%); out-of-distribution tasks at 37.7% (baseline 29.3%)[^27] |
| ActiveSaddler | Microsoft, POSTECH | The curriculum of training scenarios used during optimization | GAIA2 +4.4 and TB2 +7.5 percentage points[^29] |
| Harmony Harness | Google and others | Multiple objectives; general mechanisms and benchmark-specific adaptations evolve separately | Gains above 10% on both SecRepoBench and BaxBench[^28] |
| MoMHa | Adobe | Three objectives: accuracy, safety and tokens | 0.461 on real benchmarks, vs. 0.377 for the strongest baseline, DSPy[^31] |
| Harness2 | Google Cloud | Open-world tasks with no ground-truth verifier | WorkBuddy-Bench +11.5, JobBench +4.5, LAB +11.8[^30] |
| Doc2Harness | ICT (Chinese Academy of Sciences) and others | Benchmark: models build a harness from scratch following documentation | Of 19 frontier models, the strongest, GPT-6 Astra, passes 53.05% and the weakest 27.44%[^32] |

Common threads (inferred):

- **Execution-based verification is a prerequisite**: in VERSE's controlled experiment, without execution-based verification the optimizer's self-evolution doesn't improve performance; with verification, it achieves the best result in that experiment[^27].
- **Overfitting is the top risk**: LangChain says bluntly that agents are "famous cheaters" that will overfit their structure to make the evals they can see pass, so holdout sets and human review are needed as a backstop[^33]. Meta-Harness searches and evaluates on the same 89 tasks, and can only rely on manual inspection and regex audits to rule out leakage of task-specific strings[^13].
- **Objectives are multiplying**: as MoMHa puts it, a harness that never refuses unsafe requests, or that spends an order of magnitude more tokens, is not a good harness[^31].
- **Building a harness is itself a long-horizon task**: Doc2Harness's failures concentrate on how cross-cutting features get split across modules[^32].

## 6. The Training Loop: Models and Harnesses Co-Evolve

### 6.1 Models Adapt to Their Own Harness

- LangChain notes that putting the harness in the loop during post-training causes overfitting, such as Codex models' reliance on the `apply_patch` editing logic[^1].
- But "a model works best in its own vendor's harness" doesn't hold: on TB2, Claude Code ranks last among all Opus 4.6 submissions[^15]. In a controlled experiment, DeepSeek's own harness showed no score advantage on DeepSeek-V4-Flash either[^19].
- The match between training and harness matters: OpenAI's models are trained and deployed with their private reasoning preserved, while the official generic harness of ARC-AGI-3 discards the private reasoning after every step[^16].
- LangChain therefore introduced per-model harness profiles, for example swapping in the recommended `apply_patch` tool for Codex models[^15].
- On the research side, harness-aware post-training does better both in and out of distribution; models post-trained under a minimal harness drop sharply when the tool environment changes substantially[^34]. Co-Harness alternates between optimizing the harness and the weights, and distills the harness's improvements into the parameters[^35]. Self-HPO has the evolving policy propose harness candidates itself, raising the average resolve rate of Qwen3.5-35B-A3B from 57.8% to 64.8%[^36]. Harness-1 goes the other way: it moves search bookkeeping out into the harness, so that RL only optimizes semantic decisions[^37].

### 6.2 New Problems in Harness-Native RL

The paradigm shift: in traditional agentic RL the training engine owns the interaction loop; in harnessed agentic RL, the loop belongs to the harness, and the training engine sees only a stream of LLM requests and responses[^38]. verl Uni-Agent, AReaL 2.0, slime v0.3.0 and Polar all take this proxy approach[^38].

| Problem | Symptom | Current approach |
| --- | --- | --- |
| Token fidelity | Even when the text is unchanged, retokenized token IDs can differ from those at sampling time[^38]; tool-argument JSON may be re-serialized, and the harness may also compress or rewrite history[^40] | Fireworks's TITO records the exact prompt tokens, action tokens, logprobs and loss mask[^40]; Uni-Agent's String-In-Token-Out gateway[^39] |
| Sample splitting | In Agent Lightning's coding-agent training, only 36% of rollouts stay a single sample, and each rollout yields 2.4 samples on average[^38] | Uni-Agent starts a new chain when the context is trimmed or forked[^39] |
| Advantage computation | verl Uni-Agent and Polar compute advantages at the rollout level, slime and AReaL at the sample level[^38] | Requires an explicit choice |
| Loss normalization | Sample-level normalization gives more weight to rollouts that yield more samples, which can destabilize training[^38] | — |
| Harness sensitivity | Fixing a tool bug, or changing how replies without tool calls are handled, significantly changes training dynamics[^39] | Mixed training across multiple harnesses[^39] |
| Reward contamination | Environment crashes and reward hacking contaminate the outcome signal[^41] | Sandbox orchestration plus staged defenses[^41] |

Evidence: Lego-RL trains Qwen3.5-35B-A3B with GSPO without changing the native harnesses' control flow[^41]. On SWE-bench Verified, the OpenHands SDK rises from 64.0% to 70.4%, Claude Code from 62.4% to 68.2%, and OpenCode from 57.2% to 66.6%[^41]. The probability correlation between the rollout side and the training side stays above 0.99[^41].

## 7. Evaluation Harnesses: Scores Measure "Model + Harness + Infrastructure"

- Anthropic distinguishes the evaluation harness (the infrastructure that runs evals end to end) from the agent harness, and notes that evaluating an agent means evaluating the combination of harness and model[^8].
- Summing up three years of experience, the lm-eval maintainers list the sensitivity of models to evaluation setup as one of the main methodological problems[^43].
- HAL ran 21,730 rollouts with a standardized harness, covering 9 models and 9 benchmarks[^18]. Log analysis found agents searching HuggingFace for answers and misusing credit cards in booking tasks[^18]. Only after spending heavily on evaluation did they discover that one scaffold had data leakage[^18].
- TB2 consists of 89 terminal tasks[^12]. Its official harness, Harbor, can also generate RL rollouts[^44]. (inferred) Evaluation harnesses and RL environments are merging into the same infrastructure, so flaws in an evaluation harness turn directly into flaws in training rewards.
- Anthropic found that on TB2, resource configuration alone separates the most- and least-resourced setups by 6 percentage points[^20]. Two agents with different resource budgets and time limits are not taking the same exam[^20].
- OpenAI's summary: evals rarely measure a model in isolation; they measure the combination of API settings, harness design and prompts[^16].

## 8. Debates and Open Questions

- **Thin harness or thick harness**: Browser Use compressed its entire browser harness to about 600 lines and argues for deleting even the tool helpers, letting the agent write the functions it needs[^23]. mini-SWE-agent's README says it reaches more than 74% on SWE-bench Verified with about 100 lines of code[^53]. Products are split the same way: in the paper's coarse bands, Pi is Medium (80K–110K lines), with a core loop of only about 790 lines and no planning or turn limit, documented as design trade-offs[^9]; Hermes Agent and Codex are Very large (600K+ lines)[^9]. On the other side, Anthropic argues that as models get stronger the harness design space doesn't shrink, it moves[^22]. (inferred) The two sides are talking about different layers: the tool-abstraction layer should get thinner, while the verification, state and safety layers need to stay thick.
- **A harness's assumptions expire**: Anthropic added context resets for Sonnet 4.5's context anxiety; by Opus 4.5 the behavior was gone and the resets had become dead weight[^11][^22]. Their practice is to remove components one at a time with each new model and see which ones still matter[^22].
- **Cost**: the full harness ran for 6 hours at $200, versus 20 minutes and $9 for a single agent, more than 20x the cost; but the core features of the game the single agent built simply didn't work[^22]. On GPT-6 Sol, the harness used about 10.5x the tokens at about 7x the cost, yet the acceptance result didn't change[^24].
- **Behavioral correctness is still a weak spot**: Böckeler argues that today's heavy reliance on AI-generated tests is not enough[^6]. She also points out that the OpenAI article lacks verification of functionality and behavior[^5].
- **How to evaluate the harness itself**: Böckeler calls for harness coverage and quality metrics, analogous to code coverage and mutation testing[^6].
- **Safety**: Managed Agents' structural approach is that credentials can never be reached from the sandbox where generated code runs[^11].

## References

The sources cited above are listed below; all were accessed on 2026-10-20.

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
[^97]: [Science and Technology Daily — Alibaba launches Qoder, a new-generation AI coding platform (2025-08-22)](https://www.stdaily.com/web/gdxw/2025-08/22/content_388981.html)
[^98]: [Alibaba Cloud Model Studio docs — Qoder](https://www.alibabacloud.com/help/en/model-studio/qoder-agent)
[^99]: [Qoder CLI — qoder.com/en/cli](https://qoder.com/en/cli)
[^100]: [Tencent Cloud — Tencent CodeBuddy](https://www.tencentcloud.com/products/acc)
[^101]: [Baidu AI Cloud docs — Comate CLI Quick Start (2026-07-09)](https://cloud.baidu.com/doc/COMATE/s/0mrcv8nsa)
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
