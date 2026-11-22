# Inference

[中文](./README_zh.md) | English

[← Back to home](../../README.md)

- [Mooncake Transfer Engine Source Code Reading Glossary](./Mooncake-Transfer-Engine-Glossary_en.md) · 2026-11-20
  - The hardware, networking, RDMA verbs and TE-specific terms you need before reading the Transfer Engine source, each with a plain explanation and an example. The key point: TE's RDMA data path is one-sided WRITE/READ, the receiver's CPU never takes part, and "the data has arrived" has to come in a separate message. Includes the call chain of one RDMA WRITE from `submitTransfer` through `ibv_post_send` to the CQ completion.

- [Mooncake and SGLang: An Architecture Walkthrough Centered on KVCache](./Mooncake-SGLang-KVCache-Architecture_en.md) · 2026-11-13
  - The paper argues KVCache is worth reusing across machines: about 6 GB/s of load bandwidth suffices on an 8×A800 machine, but a cache that fits on one machine reaches less than half of the theoretical maximum hit rate (40%–66% in the paper) on most workloads, so a distributed pool is needed. SGLang uses Transfer Engine for PD transfer and Mooncake Store as the HiCache L3. Checked against the current code, the paper's Algorithm 1 has no open-source implementation: the routers pick instances by prefix match and load only, without estimating TTFT.

- [DeepSeek V4.1 Flash Inference Deployment Q&A: the official DeepInfer doc, with a full Chinese translation](./DeepSeek-V4.1-Flash-Inference-Deployment-QA_en.md) · 2026-10-20
  - DeepSeek's own production deployment details: a single cluster serves 155 trillion tokens per day; prefill runs on 8-GPU machines with the smallest EP that fits, decode on 64–128-GPU supernodes with Wide-EP, and the block KV cache lives on a dedicated 3FS cluster of about 100 PiB (3–7 day TTL). Also covers EPLB and DP load-balancing settings, SWA bounded replay hits and recomputation, and DSpark variable-length verification (+4–7% throughput at the production operating point).

- [Mooncake: Trading Storage for Computation (FAST 2025 Full Paper Translation)](./Mooncake-KVCache-Centric-Serving_en.md) · 2025-02-25
  - Combines prefill/decoding disaggregation with global KVCache reuse: effective request fractions improve by 59%–498% on real conversation traces; global caching reaches up to 2.36 times the local hit rate and saves up to 48% of prefill computation. Includes all figures, tables, algorithms, and references, distinguishing production statistics from replay experiments.

- [Flash-Decoding: Faster Long-Context Inference](./Flash-Decoding_en.md) · 2023-10-12
  - During inference the query length is just 1, so parallelizing over the batch doesn't fill the GPU; parallelize over the KV cache's sequence length instead, and long-sequence decoding gets up to 8x faster.
