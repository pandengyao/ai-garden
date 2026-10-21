# DeepSeek V4.1 Flash 推理部署 Q&A

中文 | [English](./DeepSeek-V4.1-Flash-Inference-Deployment-QA_en.md)

- **原文链接**: [DeepSeek V4.1 Flash Inference Deployment Q&A](https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md)
- **发布日期**: 2026-10-20
- **译注**: 中文版是原文在提交 [`774ce24`](https://github.com/deepseek-ai/DeepInfer/blob/774ce244b87cc0eb8d4b94ab9f5de2ab22049f01/doc/inference_deployment_qa.md) 时的非官方全文翻译，图片和表格与原文一致，术语参照了 DeepSeek 此前在同一仓库发布的[中文 PDF 版](https://github.com/deepseek-ai/DeepInfer/blob/8b16149741a4935e1dec8cea27853f273b374c5b/doc/DeepSeek%20V4.1%20Flash%20%E6%8E%A8%E7%90%86%E9%83%A8%E7%BD%B2%20Q%26A.pdf)。英文版即原文，只改了图片路径、列表缩进和一处脚本链接。原文以 [Apache License 2.0](https://github.com/deepseek-ai/DeepInfer/blob/main/LICENSE) 发布，两个版本沿用同一许可。

大模型的能力边界由模型本身划定，而如何让这些能力以合理的成本服务海量用户，则是**推理框架**要解决的核心问题。

面对大规模的 AI 调用需求，推理框架已经从单机服务程序演变为跨集群协同的复杂系统。算子、通信、调度与缓存管理相互影响，共同决定端到端性能。对于大规模在线服务，性能优化需要落实到具体的部署条件中：使用什么芯片、如何组织硬件、如何分配计算，以及如何复用已有的计算结果。

DeepSeek V4.1 Flash 推理系统从设计之初，就确立了三个目标：

1. **兼容多种厂商的计算芯片**：支持在不同硬件平台上部署，并充分发挥各平台的性能。

2. **基于常见硬件组织 Prefill 和 Decode**：用常见的 8 卡机器做 Prefill，用常见的 64–128 卡超节点做 Decode，围绕两个阶段的负载特征设计计算、通信与调度。

3. **支持将 KVCache 保留 72 小时以上**：为上下文复用提供更长的时间窗口，在缓存命中时减少重复的 Prefill 计算，并将长时间保留缓存所需的容量与管理开销纳入系统设计。

围绕这些目标，我们持续优化计算、通信、调度与存储，在满足延迟要求的前提下提高系统的有效吞吐，用更少的算力与能源支撑更多请求，让智能服务以更低的价格触达更多用户。

此前，我们已开源 [TileLang 以及一系列推理算子库](https://mp.weixin.qq.com/s/X41mKH4Ds-VXUAnK6M8Eww)。**今天，我们正式开源大规模云服务推理框架 [DeepInfer](https://github.com/deepseek-ai/DeepInfer)。** 基于这一框架，我们实现了 DeepSeek V4.1 Flash 的高吞吐、低延迟大规模推理服务。目前单一集群的服务吞吐是每天 155 万亿 tokens，整体收入是每卡每小时 38 美元（按谷价）。

DeepInfer 集成了高性能算子和深度优化的推理引擎，支持分布式推理、投机解码、SWA Bounded Replay、结构化输出等能力，可在英伟达与华为昇腾平台上运行。同时，我们还开源了生产级 Token 编解码组件 [**deepseek-recipe**](https://github.com/deepseek-ai/deepseek-recipe)，它能在主流大模型 API 协议与模型 Token 序列之间高效、准确地编解码，处理逻辑与 DeepSeek 官方 API 完整对齐，确保第三方部署获得与官方一致的 API 体验。未来，DeepSeek 新模型的推理代码及后续的性能优化也将在 DeepInfer 中持续开源。

推理系统中的 KVCache 管理与负载均衡组件因与内部基础设施耦合较深，相关代码目前尚未完整开源。已发布的[知乎博客](https://zhuanlan.zhihu.com/p/2095560295930508953)从上述设计目标出发，介绍了 DeepSeek V4.1 Flash 推理系统的整体架构与关键实现，其中包括这两个组件的设计。**本 Q&A 以该博客为基础，并将持续更新，解答更多细节问题，帮助开发者与企业组织提升 DeepSeek V4.1 Flash 的推理部署效率。**

## 推理系统概览

**DeepSeek V4.1 Flash 推理系统的优化目标是：更大的吞吐，更低的延迟。**

为了同时实现这两个目标，我们采用：

- **（超）节点内 MoE 部分专家并行（EP）**：增大 batch size，提高 GPU 矩阵乘法效率，从而提高吞吐。

- **Vision Encoder / Prefill / Decode 分离部署**：解耦各阶段的资源分配，从而独立控制并分别优化 TTFT 和 TBT。

与 [DeepSeek-V3 / R1 推理系统](https://zhuanlan.zhihu.com/p/27181462601)一样，Attention 部分使用数据并行（#DP = #EP）。不同的 DP / EP 副本之间需要负载均衡，为此我们开发了 **Prefill Load Balancer、Decode Load Balancer、Vision Encoder Load Balancer 和 Expert-Parallel Load Balancer**。为了节省重复 Prefill 的成本，我们开发了 **KVCache Storage**。

请求进出推理系统时，都需要在 API 协议与 token 序列之间转换。**DeepSeek Recipe** 能高效、准确地完成这一编解码：它按 special token 分段并行编码，在防止 special token 注入的同时，降低长文本 tokenize 的时延。

参考架构图：

![DeepSeek V4.1 Flash 推理系统架构](./img/DeepSeek-V4.1-Flash-Inference-Deployment-QA-architecture.png)

- 推理系统的整体形态？

  - E/P/D 分离架构 + 独立的存储节点。

- 并行策略？

  - Prefill：EP2–8 / DP2–8；在显存足够的情况下用尽可能小的 EP/DP。

  - Decode：EP64–128 / DP64–128（Wide-EP）；在显卡可用的情况下用尽可能大的 EP/DP。

  - VE：一般单卡部署一个实例即可，建议用便宜的卡。

  - 暂未使用 TP 和 CP。

- Decode 开 Wide-EP 的收益？

  - Wide-EP 显著减少了 per-step MoE 专家部分的访存量，在较好的 EPLB 配合下能有效提升 TPS。下图是 EP8 vs. EP64 的 benchmark 数据（离线测试脚本，配置如图所示）。

![EP8 vs. EP64 Decode 吞吐](./img/DeepSeek-V4.1-Flash-Inference-Deployment-QA-wide-ep-decode.png)

- 多模态怎么部署？

  - EPD 分离部署，Vision Encoder 用单卡部署。

- 最小部署单元要多大？

  - 1P + 1D 就能部署。实践中 P 和 D 所需的卡数比例基本是 1:1。由于 D 的推荐配置是 EP64 以上，效率高的最小部署单元是 64 卡 Prefill + 64 卡 Decode。

## 集群 & 存储

- 可以跨机房部署吗？

  - 由于 V4.1 Flash 大幅压缩了 KVCache，P、D 跨机房部署在技术上可行（会损失一些可靠性，比如跨机房的光纤容易被施工挖断）。大约每 8 张卡需要配备 400 Gbps 的互联带宽。在实践中，DeepSeek 的推理节点部署在不同但相邻的机房。

- 存储服务器的标准配置？

  - 推荐每台 KVCache 存储服务器配 20 × 30.73 TB SSD，单台至少提供 40 GB/s 读、5 GB/s 写吞吐，总存储空间能保留 24 小时的数据。再根据实际的推理规模，增加存储服务器的数量。

- 存储集群和线上卡的配比？

  - 实践中按逻辑大小计算，约为每卡 14.4 TB，实际所需的物理容量比这更大。

- 3FS 分布式文件系统有哪些特点？

  - 面对节点宕机和网络抖动，需要兼顾高可用与高性能。

  - 数据以纠删码（10+2 Erasure Coding）存放在 3FS 上，每个 EC 组可容忍两个节点同时故障。

  - 读取时同时向组内全部 11 台 Storage 节点发起请求，任意 10 个响应即可解码返回。

  - GC Worker 组件负责回收过期缓存：每个 Storage 节点部署一个实例，按 LRU 策略周期性淘汰最久未访问的 KVCache，将磁盘占用控制在水位线以下。

## 专家并行负载均衡

- Prefill 的 EPLB 策略？

  - 实现方法：每卡在自己负责的专家之外多备若干冗余专家，用来放热门专家的副本；统计最近 N 步各专家的负载，每 M 步根据统计结果重新把专家分配到卡上，其中专家权重经 NVLink `symm_mem` 在组内 shuffle。

  - Prefill 的设置：每卡 4 个冗余专家起步（向上填充至总专家数为 `ep_size` 的倍数），统计窗 100 步，每 1,000 步重排一次。实测 `moe_lb`（最慢 rank / 均值）= 1.074（EP4DP4）/ 1.045（EP2DP2）。

- Decode 的 EPLB 策略？

  - 实现方法同 Prefill。设置：每卡 1 个冗余专家起步（向上填充至总专家数为 `ep_size` 的倍数），例如 EP64 取整后每卡共 7 个专家（不含共享专家）；统计窗 1,000 步，每 10,000 步重排一次。实测 `moe_lb` = 1.090。

## 数据并行负载均衡

- Prefill Load Balancer 的实现？

  - 分桶（tiers）：按 context 总长把请求分为 4 个 tiers：<16K / 16–64K / 64–256K / ≥256K。每档分到的引擎台数，按该档上一轮的 compute-quota 需求占比动态重分，且每档有各自的单批 compute-quota 上限。

  - DP 组间：引擎按目前剩余的 compute quota 拉取请求。由于任何引擎都能命中任何前缀，不做前缀亲和路由。

  - DP 组内：一批请求交给一个 engine，每到达一个请求，就分给当前 quota 负载最低的 DP rank。

  - 单卡内：请求 FIFO 出队，chunk size 不固定，而是由预算反解。Prefill 每一步定一个时间预算（`compute_quota_limit`，单位为纳秒），用一个拟合的二次代价模型 `cost(q, c)` 预测这一步要花多久（`q` = 序列 token 数，`c` = 这条序列已经算完的前缀长度）。调度器对 `q` 反解这个二次方程，取“在 32,768 的 token 预算之内、又正好把剩余时间预算吃满”的最大 `q`。预算本身还会被 DP 组内的 all-reduce MIN 进一步减少。

- Decode Load Balancer 的实现？

  - Decode Load Balancer 对所有 Decode 实例的所有卡进行统一路由，原则是同时均衡两个维度：请求数（决定每步的批大小）和 KVCache 总长度（决定注意力部分的代价）。它启发式地把短请求发给并发较小但 KVCache 总长偏大的卡，把长请求发给 KVCache 总长较小的卡，具体可参考 DualPath 的组内调度算法。

- Vision Encoder Load Balancer 的实现？

  - 图片以单台机器为单位路由：Prefill 机器随机选中一台每卡部署一个 Vision Encoder 的机器；在这台机器上，图片交给当前处理图片 patch 数最少的卡（patch 数由宽高直接算出：`(width/patch_size) × (height/patch_size)`），由它生成 embedding。

- 做了负载均衡后，整体提升有多少？

  - 可以与离线 benchmark 对比：我们大概能达到完全均衡的离线 benchmark 的 80%。

## KVCache 存储

| 内容 | 介质 | 副本 | 管理方 |
| :--- | :--- | :--- | :--- |
| 运行中的 Block KVCache + State KVCache | 推理卡显存 | — | Prefill / Decode 实例 |
| SWA KVCache | 本机内存 | 单副本，3FS 上没有 | Prefill / Decode 实例；跨机命中通过 400G VLAN 拉取 |
| 分页 Block KVCache | 独立的 3FS 存储集群 | 应用层无副本，依靠 3FS 自身的冗余 | kvcache-store |

### Block KVCache

- 存储介质？

  - 如上表所示，Block KVCache（Main KV + Indexer K）存放在独立的 3FS 存储集群上，而不是本机内存。相比多级存储系统，独立的存储集群让每台 Prefill 机器都能命中任何前缀，避免前缀亲和与负载均衡路由策略冲突；它还让存储节点与计算节点的自动扩缩容解耦，使 KVCache 不受计算节点故障的影响（计算节点的故障率比存储节点高一个数量级以上）。

- Prefill 有没有用 paged KV cache？

  - 有，Prefill 侧同样使用 paged KV cache。

- Decode 阶段有没有开 KV offload？

  - 没开。Decode 阶段的瓶颈不在 cache 容量，因此也没用 Hi-Sparse。不过 Decode 阶段产生的 KVCache 仍会落盘，以提升缓存命中率。

- 过期与 TTL？

  - kvcache-store 侧没有任何过期逻辑，回收完全由 3FS 自己的 GC 完成。3FS 分布式文件系统为 KVCache 提供约 100 PiB 的 SSD 存储，agent 流量的 TTL（Time-To-Live）为 3 天，chatbot 流量为 7 天。chatbot 流量的长尾命中严重得多：少量 KVCache 会被读取极多次，一旦丢失，对整体命中率的损失明显更大。根据经验，3 天左右的 TTL 会让 chatbot 流量的 KVCache 命中率下降 0.5%–1%。

- Cache 相关的开销如何通过 overlap 掩盖？

  - **匹配**由 Entrypoint 在本机 CHECK 角色的 kvcache-store 上完成，做的是只查元数据的哈希链前缀匹配；但命中长度必须在路由前算出，所以无法掩盖。**取 KV** 在独立进程里异步进行，把 KVCache 从 3FS 搬进宿主机共享内存。**换入**（从共享内存到 HBM）在 engine 进程内的一个线程里进行，目标是让逐层 H2D（Host-to-Device）传输与前向计算重叠。由于 CUDA copy engine 对 KVCache Block 的细粒度拷贝性能不佳，换入使用 GDR 实现：用 RDMA 网卡就能打满 PCIe 带宽，而且不占用 SM。

### SWA KVCache

- 存储方式？

  - SWA KVCache 不进分页 KV block，而是放在 state cache 里，每个序列占一个定长 slot（`StateBlock`）。每个 slot 按“是否需要 store”切成两段：`[stored region: SWA] [dropped region: YOCO consumer SWA]`。stored region 是需要跨请求持久化的 SWA 窗口；dropped region 包含 YOCO consumer SWA 层（其恢复依赖 Prefill 重算）和 C2 压缩的边界累加器 `ca_state` / `ica_state`（压缩窗口边界天然对齐在 store 粒度 128 token 的整数倍上，没有跨边界的依赖）。对 V4.1 来说，store 的是前 20 层。

  - SWA KVCache 只在 128 token 整数倍的位置上存储。Prefill 阶段结束后存储：存储位置取序列末尾留出一个 token 后向下对齐到 128 的位置；不足一个完整的 128 token 单元，则本轮不存储。chunked prefill 中途不存储，只有最后一个 chunk 才存储。Decode 阶段在显存中另开一块副本区，请求每跨过一个 128 token 边界，就把它当前的窗口在显存内拷入副本区。请求结束时，从副本区中最近一次完成的拷贝存储，附着点向下对齐到 128 边界。拷贝位置最多越过边界 5 个 token，由 slot 的 ring buffer 比窗口多出的 6 个位置吸收。

- store 的内容与介质？

  - 落进 store 的只有 `state_size_to_disk` = 20 层 × 134 token × 528 B = 1,415,040 B/序列。528 B/token 是 MXFP8 的 SWA KV 格式。SWA KVCache 不进持久化缓存，而是留在产生它的那台机器的内存里；由一个逻辑上统一、实际按 key 分散存放在各台 Entrypoint 机器上的内存目录记录它在哪台机器，命中时如果本机没有，就从远端机器取回。

- Prefill → Decode 如何传输？

  - SWA KVCache 和 Block KVCache 走同一套 P→D 传输链路。

- 是否支持跨机命中？

  - 跨机命中依靠 Entrypoint 的内存目录，配合 400G VLAN 回拉。

### KVCache 命中与重算

- 重算方式？

  - SWA Bounded Replay 只重算最近 128 个 token，并把注意力窗口截断在重算段内：从位置 s 起回放，位置 i 的 query 只和 max(s, i−127) 到 i 区间内的 key 计算，重算得到近似的 SWA KVCache。重算代价由此降为与上下文长度和层数无关的常数。该机制用在两处：

  - Encoder SWA Bounded Replay：前缀缓存的命中长度从此只取决于 Block KVCache。SWA KVCache 缺失时，重算命中前缀的最后 128 个 token，与未命中的后缀一起前向；重算段只重建 SWA KVCache，Block KVCache 原样复用，既不重算也不覆写。

  - Decoder SWA Bounded Replay：Prefill 计算只发生在 encoder 层。在 CED 架构下，decoder 层的 Block KVCache 由 encoder 末层的 hidden state 投影得到，只有 decoder SWA KVCache 需要逐层计算；若要精确重建，需要让最后 2,560 个 token 跑过 20 个 decoder 层。改为每次 Prefill 在 decoder 层只重算 prompt 末尾的 128 个 token，结果仅供 Decode 使用、不进前缀缓存，总 Prefill 计算量因此近乎减半。

- 命中策略？

  - 原则是：命中长度由 Block KVCache 决定，最后一个 block 是否需要重算由 SWA KVCache 决定；若 SWA KVCache 未命中，就退一块重算。具体来说，根据 YOCO 截断要求，长度为 L 的输入，最大命中长度至多为 L − 134（128 token 的窗口 + 6 token 的投机回退）。在这个上限下，先查询 Block KVCache，得到命中长度 L1（block size 128 token 的整数倍），再查询 SWA KVCache。如果在 L1 − 128 到 L1 的范围内存在 SWA KVCache，命中长度就是 L1，否则为 L1 − 128，其中 128 是重算窗口。

## 扩缩容 & 容错

- 扩缩容的实现？

  - Prefill 根据未命中 token 数确定所需的机器数，Decode 根据在跑的请求数调整；调整有限速，也有上下界。

  - 针对大 EP 部署中长尾请求造成资源浪费的问题，Decode 引擎（CE）收到下线通知后进入宽限期（1 min），届时仍未完成的请求连同其 KVCache 一次性全部转发给其他 CE 继续 Decode。

- 冗余配额是什么样的？

  - 部署时保留冗余配额来吸收流量波动带来的冲击，形式有两种：一是池子里留有尚未被占用的 ready 机器作为扩容库存；二是在线实例永远多于算出来的需求，具体来说，配额占用率高于 0.8 时禁止缩容。

- 重启需要多长时间？

  - 重启在分钟量级。容错靠的是 PE（Prefill 引擎）/ CE 的配额冗余加上请求级重新路由，而不是缩短单个引擎的重启时间。

- EP failover 策略？

  - 在大 EP 部署下，一个实例的全部卡构成单一通信域，任意一张卡故障都会导致整个实例不可用。重启时，为了让该实例其余健康的卡继续服务，平台按当前所有健康的卡重新确定 EP 大小，实例以实际拿到的卡数作为 EP 规模。

## 低精度计算

- FP4 用在哪些地方？

  - Main KV：per-16，e4m3，类似 NVFP4，但没有 global scale。

  - Indexer KV：per-32，ue8m0，MXFP4。

  - MoE 路由专家权重：per-32，ue8m0，MXFP4。

## 算子实现

- 用了哪些 kernel（kernel backend）？

  - 可以用 DeepInfer 仓库中的 [`examples/benchmark.py`](https://github.com/deepseek-ai/DeepInfer/blob/main/examples/benchmark.py) 脚本 profile 得到对应的 trace，其中包含 kernel 的使用信息。

- 什么时候用 Mega MoE？

  - Mega MoE 是 scale-up 域内的通用方案：无论 EP 大小、batch 大小如何，Mega MoE 都显著快于 unfused MoE。

- DeepGEMM / FlashMLA 等 kernel 库内部有没有更优的版本？

  - 大体是统一的，indexer 和 mega 系列有些差异。FlashMLA 少了一个手工修改 SASS 的优化，decoding 算子因此慢 5%–10%。

  - 端到端性能接近，最多相差 5%。

## 投机解码

- 实现方法？

  - 在推理系统层面，DSpark 采用变长验证。由于不同请求、不同位置的 draft token 接受概率不同，固定长度验证会把验证算力浪费在低概率 token 上。DSpark 用 Confidence Head 预测每个 draft token 的接受率，调度时把验证算力分配给边际收益最高的 token。线上部署时，draft model 一次生成 5 个 token；根据 profile 得到的硬件吞吐曲线，以及每个请求、每个 draft token 的接受率，把各 draft token 按预期接受率排序，选出有效吞吐最大的前缀子集进行验证。

- 相比 fixed-5，动态长度验证能带来多少吞吐收益？

  - 动态长度验证把每步验证的 draft token 数砍掉约 30%（5.00 → 3.2–4.4），同时平均接受长度基本不变（3.29 vs. 3.20）。根据 EP64/DP64 的 benchmark 数据计算，在生产运行点（每 rank 约 60 条并发序列）折合吞吐 +4–7%。

| 并发（seqs/rank） | fixed-5 平均验证长度 | 动态长度平均验证长度 | fixed-5 接受长度 | 动态长度接受长度 | fixed-5 估算吞吐（tok/s/rank） | 动态长度估算吞吐（tok/s/rank） | 动态长度相对 fixed-5 的收益 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 5 | 4.44 | 3.32 | 3.24 | 4891 | 4816 | −1.5% |
| 32 | 5 | 3.65 | 3.25 | 3.17 | 8964 | 9111 | +1.6% |
| 48 | 5 | 3.94 | 3.3 | 3.26 | 12032 | 12467 | +3.6% |
| 60 | 5 | 3.58 | 3.3 | 3.21 | 13730 | 14466 | +5.4% |
| 72 | 5 | 3.24 | 3.29 | 3.12 | 14962 | 15961 | +6.7% |
| 96 | 5 | 3.24 | 3.3 | 3.15 | 16817 | 18660 | +11.0% |

- Draft Model 内部有没有更优的版本？

  - 内部版本新一些，但性能差别不大。

- 与异步调度如何配合？

  - `schedule(N+1)` 执行时，第 N 步的 confidence 尚未回传，因此 CPU 调度时只确定总预算；每个请求的长度在 GPU 上由一个 TileLang kernel 重新计算（累乘、全局排序取 top-k，并融合 remap scatter），结果写回 pinned buffer。

## 异步调度（Zero-Overhead Batch Scheduler）

- 优化目标？

  - Decode 第 N 步的流程是 `schedule(N) → forward(N) → sample(N) → post-process(N)`，其中 schedule 和 post-process 是纯 CPU 逻辑，并且在 `post-process(N)` 之前需要一次 GPU-CPU 同步来拿到 `sample(N)` 的结果。这就导致在 `post-process(N)` 和 `schedule(N+1)` 期间 GPU 处于空闲状态。异步调度的目标就是消除这段空闲。

- 实现方法？

  - 参考已有实现（SGLang、NanoFlow），通过 GPU 与 CPU 之间的异步调度让流水线重叠：GPU 执行 `forward(N) → sample(N)` 的同时，CPU 执行 `schedule(N+1) → launch_forward(N+1) → post-process(N−1) → launch_sample(N+1)`，GPU 全程没有空闲。

## 结构化输出

- 结构化输出是什么？

  - 结构化输出（Structured Output，SO）用于约束模型输出严格符合指定格式（JSON schema、正则表达式、EBNF 等）。

- 工作流程？

  - 编译与推理解耦：SO 编译异步进行，请求在进入 engine 之前取回编译结果。

  - 编译阶段（在独立的 SO 机器上）：将格式约束编译为语法自动机。

  - 运行时：每步 decode 时推进自动机，确定合法 token 集合，生成 mask 并作用于采样逻辑，强制输出符合目标结构。

## DeepSeek Recipe

- API 多协议适配怎么做？

  - DeepSeek Recipe 把 Chat Completions API、Responses API 和 Messages API 的请求转成同一种对话格式，共用一套模型模板和编码逻辑，按模型版本生成 prompt 和 token 序列。

  - 模型输出经解析后形成正文、思考内容和工具调用等事件，再转换为各协议的流式响应。请求转换、prompt 编码和输出解析都用 Rust 实现，以保证处理效率，同时提供 Python 绑定，方便使用。

- Tokenizer 处理与加速怎么做？

  - 输入编码：构建 prompt 时记录显式插入的 special token 及其位置，编码时将它们直接映射为对应的 token ID，普通文本则按基础词表编码。用户输入、工具返回或工具调用参数中出现的 `<｜User｜>`、`<｜image｜>` 等字符串，会被编码为相应的普通 token 序列，防止通过文本注入控制 token 来影响模型行为。

  - 输出解析：处理响应 token 流时，我们根据 token ID 识别思考结束标记 `</think>` 和 DSML 标签中的 `｜DSML｜` special token。模型用普通 token 拼出的相同文本会被正确保留为字面内容，不会因此获得触发思考结束或工具调用的能力。

  - 分段加速：构建 prompt 时，special token 的位置和边界就已经确定。根据 BPE tokenizer 的工作原理，special token 之间的各段普通文本可以独立编码。因此，我们跳过在普通文本中匹配和切分 special token 的步骤，并行编码各段文本，再按原顺序拼接结果。这样能降低超长上下文请求的分词耗时，改善请求延迟。

- 流式输出解析怎么做？

  - 推理后端按 token 粒度返回 chunk，所以一个 UTF-8 字符、一个 DSML 标签或一个工具参数都可能被拆到多个 chunk 中。流式解析需要一套状态机，既保留尚未完成的处理进度，又及时返回已经确定的内容，以降低响应时延。

  - 跨 chunk 解析：解码遇到不完整的 UTF-8 字符时，先缓冲相关 token，待后续 token 补齐后再交给解析器。解析器按思考、正文和工具参数等阶段维护状态，并用增量 KMP 匹配分隔标记。如果一个 chunk 在某个标记中途结束，就保留匹配进度，在下一个 chunk 到达时继续识别；已确定的内容随解析进度输出，无需反复扫描之前的文本。

  - 工具参数转换：工具名一解析完就可以返回，之后直接根据 DSML 参数边界生成 JSON 片段。字符串值逐段做 JSON 转义，数组、对象等非字符串值按原始 JSON 文本输出，无需构造完整的参数对象，也不用反复解析和序列化。即使参数很长，也能边生成边逐段返回，缩短首个参数片段的等待时间。
