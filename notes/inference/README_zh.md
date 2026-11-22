# 推理优化

中文 | [English](./README.md)

[← 返回首页](../../README_zh.md)

- [Mooncake Transfer Engine 源码阅读术语手册](./Mooncake-Transfer-Engine-Glossary.md) · 2026-11-20
  - 读 Transfer Engine 源码前要懂的硬件、网络、RDMA verbs 和 TE 自身术语，每个配通俗解释和例子。关键一点：TE 的 RDMA 数据面是单边 WRITE/READ，接收端 CPU 全程不参与，“数据到了”要靠另一条消息通知。附一次 RDMA WRITE 从 `submitTransfer` 经 `ibv_post_send` 到 CQ 完成的调用链。

- [Mooncake 与 SGLang：围绕 KVCache 的架构梳理](./Mooncake-SGLang-KVCache-Architecture.md) · 2026-11-13
  - 论文论证 KVCache 值得跨机复用：8×A800 机器加载带宽约 6 GB/s 即可，但单机放得下的缓存在多数负载下拿不到理论最高命中率（论文中为 40%～66%）的一半，需要分布式池。SGLang 用 Transfer Engine 做 PD 传输、用 Mooncake Store 做 HiCache L3。对照当前代码，论文的 Algorithm 1 没有开源实现：路由器只按前缀匹配和负载选实例，不估算 TTFT。

- [DeepSeek V4.1 Flash 推理部署 Q&A：DeepInfer 官方文档全文翻译](./DeepSeek-V4.1-Flash-Inference-Deployment-QA.md) · 2026-10-20
  - DeepSeek 官方的线上部署细节：单集群每天 155 万亿 tokens；Prefill 用 8 卡机器、尽量小的 EP，Decode 用 64–128 卡超节点做 Wide-EP，Block KVCache 存在约 100 PiB 的独立 3FS 集群上（TTL 3–7 天）。另含 EPLB 与 DP 负载均衡参数、SWA Bounded Replay 的命中与重算、DSpark 变长验证（生产点吞吐 +4–7%）。

- [Mooncake：以更多存储换取更少计算（FAST 2025 论文全文翻译）](./Mooncake-KVCache-Centric-Serving.md) · 2025-02-25
  - 将预填充／解码分离与全局 KVCache 复用结合：真实对话轨迹中，满足 SLO 的有效请求比例提高 59%–498%；全局缓存命中率最高为本地缓存的 2.36 倍，预填充计算时间最多减少 48%。含全部图表、算法和参考文献，区分生产统计与回放实验。

- [Flash-Decoding: 长上下文推理加速](./Flash-Decoding.md) · 2023-10-12
  - 推理时 Query Length 只有 1，Batch 维度并行不起来；那就去并行 KV Cache 的序列长度维度，长序列解码最高快 8 倍。
