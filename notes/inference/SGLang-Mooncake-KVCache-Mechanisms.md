# SGLang 和 Mooncake 的 KV Cache 机制：存储层级、数据流转、淘汰、传输与调度

中文 | [English](./SGLang-Mooncake-KVCache-Mechanisms_en.md)

- **整理日期**: 2026-11-28
- **范围**: SGLang HiCache（L1 GPU、L2 Host、L3 外部存储）和 Mooncake Store 的 KV cache 存储层级、容量估算、前缀树、L3 的 key 与共享、数据流转、淘汰、传输方式、计算与传输重叠、PD 分离、请求调度与负载均衡、部署调优、监控和大规模部署，以及所需的硬件和网络基础。
- **代码版本**: [sgl-project/sglang](https://github.com/sgl-project/sglang/tree/0d311f2508d8cbdb1d5f9b804a1f39310264f5d1) main 分支 `0d311f2508`（2026-11-28，含 sgl-router），[kvcache-ai/Mooncake](https://github.com/kvcache-ai/Mooncake/tree/ab2595576a0b6469bea1fb7e12476937eb949dc5) main 分支 `ab259557`（2026-11-28）。
- **依据**: 阅读上述两个提交中的代码、SGLang 和 Mooncake 文档，以及 3FS 的 README，没有实际运行验证。

Transfer Engine 和 PD 分离的细节另见 [Mooncake Transfer Engine 学习笔记](./Mooncake-Transfer-Engine-Notes.md) 和 [SGLang PD 分离学习笔记](./SGLang-PD-Disaggregation-Mooncake-Notes.md)。

## 1. 存储层级总览

SGLang 自己有 3 层（L1 GPU、L2 Host、L3 外部存储），Mooncake 是 L3 的一种后端，它内部又分内存池和盘两级。两者合起来，端到端共 4 级：

1. GPU 显存
2. 本机 Host DRAM（CPU 内存）
3. Mooncake 分布式内存池（默认也是 DRAM，也可配置成显存）
4. Mooncake 盘层（SSD / 磁盘 / 分布式文件系统）

SGLang 里没有 L4 的概念：L3 一次只能选一个后端，常说的"第 4 级"是 Mooncake 内部的盘层，从 SGLang 角度看仍属于 L3。

实际用到几级取决于配置。SGLang 需要开启分层缓存（`--enable-hierarchical-cache`）并选 mooncake 作为存储后端；Mooncake 需要开启 offload 或配置盘副本，第 4 级才会生效。如果 L3 改用 3FS，就只有 3 级（GPU → L2 → 3FS）。

一条 KV 的典型路径：在 GPU 上算出 → 备份到本机 L2（默认写策略下立即备份）→ 写到 Mooncake 内存池 →（开启 offload 时）落到 SSD。别的实例遇到相同前缀时，从 Mooncake 读到它自己的 L2，再拷到 GPU。

## 2. 网络与硬件基础

后面讲传输方式时会用到很多硬件和协议术语，这里先按"数据在哪些设备之间、经过什么线路、由谁来搬"解释清楚。

### 一台 GPU 服务器内部长什么样

```text
GPU0 ══ GPU1 ══ … ══ GPU7        ← GPU 之间：NVLink（机内高速直连）
 │  每张 GPU 自带 HBM 显存（L1）
 │  PCIe
PCIe Switch ──── 网卡 NIC ────→ 机房网络（交换机）────→ 其他服务器
 │  PCIe
CPU ──── DRAM 内存（L2）
 │  PCIe
NVMe SSD（本地盘）
```

- 一台典型的 8 卡服务器：8 张 GPU，CPU 和内存，多块网卡（常见 1 张 GPU 配 1 张网卡），若干块 NVMe SSD。
- GPU、网卡、SSD 都通过 **PCIe** 接到 CPU 上，很多机器中间还有 **PCIe Switch**（PCIe 交换芯片），把几张 GPU 和一张网卡挂在同一个 Switch 下。
- GPU 之间另有 **NVLink** 直连，不走 PCIe。
- 跨机器只能通过网卡走网络（跨机 NVLink 的新机型除外）。

### 各条线路的速度量级

数字随硬件代际变化很大，这里只给量级，方便比较：

- GPU 显存（HBM）：每张卡约 2～8 TB/s。
- NVLink：每张 H100 与其他卡之间合计约 900 GB/s（双向）。
- PCIe 5.0 x16：单向约 64 GB/s；PCIe 4.0 x16 约 32 GB/s。GPU 和 Host 内存之间的拷贝就受这个限制。
- 网卡：常见 200 Gbps 或 400 Gbps。注意网卡用 **bit**（b）计，存储和内存用 **Byte**（B）计，1 Byte = 8 bit，所以 400 Gbps ≈ 50 GB/s。8 张 400G 网卡合计约 400 GB/s。
- 单块 NVMe SSD：读约 7～14 GB/s，延迟几十到上百微秒。
- 延迟量级：显存访问纳秒级；PCIe 和 RDMA 一次传输几微秒；TCP 几十微秒；SSD 读几十到上百微秒。

所以 KV cache 越往下层，容量越大、越便宜，但带宽越低、延迟越高。

### 机内互联：PCIe、NVLink、CXL

- **PCIe**：服务器里连接 CPU 和各种设备（GPU、网卡、SSD）的标准总线。"x16"表示 16 条通道，"4.0 / 5.0"是代际，每代带宽翻倍。KV 在 GPU 显存和 Host 内存之间搬（L1 ↔ L2）走的就是 PCIe。
- **PCIe Switch**：PCIe 的交换芯片。挂在同一个 Switch 下的 GPU 和网卡互相传数据时，可以只经过 Switch、不绕到 CPU，路径更短、更快。这就是 Mooncake 要"按拓扑选网卡"的原因：给某张 GPU 或某块内存选离它最近的那张网卡。
- **NUMA**：多路 CPU 服务器里，每颗 CPU 有自己就近的内存，访问另一颗 CPU 下的内存要跨一次 CPU 间互联，会慢一些。分配 Host 内存时尽量和网卡、GPU 在同一个 NUMA 节点上。
- **NVLink / NVSwitch**：NVIDIA 的 GPU 之间专用互联，带宽是 PCIe 的数倍（H100 约为 PCIe 5.0 x16 的 7 倍）。通常只在一台机器内部。**MNNVL**（Multi-Node NVLink，如 GB200 NVL72 机柜）把 NVLink 扩展到多台机器，Mooncake 的 `nvlink` 协议就是用这个。
- **CXL**：基于 PCIe 物理接口的新互联标准，可以接内存扩展卡，甚至让多台机器共享一个内存池。Mooncake 的 `cxl` 协议和分配策略就是给这种内存用的。

### 谁来搬数据：CPU、SM、DMA

同样是"把一块数据从 A 拷到 B"，执行者不同，效果差很多：

- **CPU memcpy**：由 CPU 核执行读写指令完成拷贝。最通用，但占 CPU，而且速度受 CPU 内存带宽限制。文档里说"多一次 memcpy"，就是指多了一次这样的拷贝。
- **GPU SM 拷贝**：GPU 上启动一个拷贝 kernel，用 GPU 的计算单元（SM）去读写。SGLang 的 `kernel` io-backend 就是这种。灵活，能一次搬很多分散的小块，但会占用本来给模型计算用的 SM。
- **DMA（直接内存访问）**：设备里有专门的搬运电路（GPU 的拷贝引擎、网卡、SSD 控制器都有），CPU 或 GPU 只需下达"从地址 X 搬 N 字节到地址 Y"的指令，搬运本身不占计算资源。SGLang 的 `direct` io-backend、RDMA、NVMe 读写本质上都是 DMA。

### 内存相关术语

- **Pinned memory（页锁定内存）**：操作系统平时可以把内存页换到磁盘或挪位置，设备 DMA 时如果页被挪走就会出错。把内存"钉住"后，物理地址固定，GPU 和网卡才能直接 DMA。代价是这部分内存不能被系统回收。SGLang 的 L2 默认就是 pinned 的。
- **内存注册（memory registration）**：RDMA、SPDK 等要求先把一块内存"登记"给网卡或驱动：钉住内存，并把虚拟地址到物理地址的映射告诉设备，之后设备才能直接读写。注册比较慢，所以 SGLang（默认的内嵌 Mooncake client 模式下）启动时一次性把整块 L2 注册给 Mooncake，后面反复使用。有的环境对能注册的总量有上限（如阿里云 eRDMA）。
- **大页（hugepage）**：普通内存页 4 KB，大页 2 MB 或 1 GB。页越大，地址翻译表越小，设备访问越快、注册也更省事。SPDK 要求用大页内存，Mooncake 也可以开大页。
- **页缓存（page cache）**：Linux 读写文件时默认先经过内核里的一块缓存。好处是重复读快；坏处是多一次拷贝、占内存。**O_DIRECT** 是打开文件时的一个选项，绕过页缓存直接读写磁盘，但要求读写的地址和长度按块对齐。
- **用户态 / 内核态**：普通程序跑在用户态；读写文件、收发网络包要通过系统调用进入内核态，由内核完成。每次切换和内核里的拷贝都有开销。"绕过内核"（kernel bypass）的技术，如 RDMA、SPDK、3FS 的 USRBIO，就是让用户程序直接和硬件打交道，省掉这些开销。

### 跨机网络：TCP 和 RDMA

**TCP**：最常见的网络通信方式，程序通过 socket 收发数据。发送一段数据的过程：

1. 程序调用 `send`，数据从程序内存拷到内核的 socket 缓冲区。
2. 内核协议栈把数据切包、加包头，交给网卡发出去。
3. 对端网卡收到后交给对端内核，内核再拷到对端程序的内存。

两端 CPU 都要参与，至少多两次拷贝，延迟几十微秒，单连接很难跑满 200G/400G 网卡。好处是任何网络都能用，不需要特殊硬件。

**RDMA（Remote Direct Memory Access，远程直接内存访问）**：网卡直接读写另一台机器上已注册的内存。

1. 双方先把内存注册给各自的网卡，交换"内存地址 + 访问密钥（rkey）"。
2. 发起方告诉本机网卡"把我这块内存写到对方的地址 Y"（RDMA write）或"把对方地址 Y 的数据读到我这里"（RDMA read）。
3. 两张网卡之间直接完成传输，数据直接落到目标内存。

全程不经过两端的内核，**对端 CPU 完全不参与**，没有额外拷贝，延迟几微秒，能跑满网卡带宽。这种只需一方发起的操作叫**单边操作**；**双边操作**（send/recv）则要求对端程序事先准备好接收缓冲区，类似 TCP 的收发，但仍然绕过内核。Mooncake 的 `rdma` 协议用单边操作；`rdma_twosided` 的数据传输同样是单边操作，只是另加一条双边（send/recv）的控制通道来传通知。

**RDMA 的几种实现**：RDMA 是一种能力，需要网卡和网络支持，有几种实现：

- **InfiniBand（IB）**：专门为高性能计算设计的网络，有自己的网卡和交换机，天然支持 RDMA，延迟最低。
- **RoCE（RDMA over Converged Ethernet）**：在普通以太网上跑 RDMA，网卡要支持 RoCE，交换机要配置成不丢包（PFC/ECN 等流控），否则性能下降很快。国内数据中心常用。
- **云厂商的 RDMA**：AWS 的 **EFA**、阿里云的 **eRDMA** 等。EFA 虽然也有 ibverbs 驱动，但只支持 SRD/UD 传输、不支持常规的 RC 连接，一般通过 **libfabric** 使用，所以 Mooncake 有单独的 `efa` 协议。
- **ibverbs**：Linux 上 RDMA 的标准编程接口，IB 和 RoCE 都用它。**libfabric** 是另一套更通用的高性能网络编程接口，EFA 等用它。

**RDMA 网卡常见术语**：RNIC 或 HCA 都是指支持 RDMA 的网卡；Mellanox / NVIDIA ConnectX 系列是最常见的型号。

**GPUDirect RDMA**：普通 RDMA 读写的是 Host 内存。GPUDirect RDMA 让网卡**直接读写 GPU 显存**，跨机传 KV 时不用先拷到 Host 内存。条件是：网卡和驱动支持（需要 `nvidia-peermem` 内核模块，或较新的 dmabuf 机制），而且 GPU 和网卡最好在同一个 PCIe Switch 下，否则数据要绕经 CPU，性能下降。SGLang 的 L3 直连模式要真正不经 Host 内存，就依赖这个。

### 机内进程间：共享内存和 CUDA IPC

- **共享内存（shm）**：同一台机器上的两个进程映射同一块物理内存，一方写了另一方直接能读，传输就是一次 memcpy。Mooncake 的 `shm` 协议、3FS USRBIO 与应用之间的数据交换都用到它。
- **CUDA IPC**：同一台机器上的不同进程共享 GPU 显存。一个进程导出显存句柄，另一个进程打开后直接访问，数据经 NVLink 或 PCIe 传输。Mooncake 的 `nvlink_intra` 用它。

### 存储接口：NVMe、I/O 方式、文件系统

- **NVMe**：SSD 的接口协议，SSD 直接插在 PCIe 上，比老的 SATA 接口快一个数量级。"NVMe SSD"就是现在服务器上常见的高速固态盘。
- **POSIX 读写**（`read` / `write` / `pread` / `pwrite`，以及一次处理多段内存的 `preadv` / `pwritev`）：Linux 标准的文件读写系统调用。每次调用要进内核，默认经过页缓存，调用期间程序等待完成（同步）。
- **io_uring**：Linux 较新的异步 I/O 接口。程序把一批读写请求放进与内核共享的队列，内核处理完再放回结果队列，程序不用为每个请求都做一次系统调用、也不用干等，适合大量小 I/O。还能预先注册缓冲区，减少每次 I/O 的准备开销。
- **libaio / POSIX AIO**：更早的异步 I/O 接口，作用类似 io_uring，限制更多。
- **SPDK**：Intel 开源的用户态存储驱动。它把 NVMe 盘从内核"拿走"，由用户程序直接驱动，完全绕过内核和页缓存，延迟最低、吞吐最高。代价是这块盘不能再被普通文件系统使用，而且要用大页内存。
- **NVMe KV**：一些 SSD 支持直接按 key-value 存取（盘内部自己管理 key 到位置的映射），不需要文件系统。Mooncake 的 `nvme_kv` 后端用它。
- **NVMe-oF（NVMe over Fabrics）**：通过网络访问另一台机器上的 NVMe 盘，用起来像本地盘。底下的网络可以是 RDMA 或 TCP。Mooncake 的 `NOF_SSD` 副本类型就是这样把远端 SSD 当作存储层。
- **GPUDirect Storage（GDS）/ cuFile**：让 SSD 直接 DMA 到 GPU 显存，不经过 Host 内存。cuFile 是 NVIDIA 提供的编程接口。Mooncake 的 `nvmeof` 传输协议和 NIXL 的 GDS 插件都基于它。
- **分布式文件系统**：把很多台机器的盘组织成一个统一的文件系统，所有机器看到同样的目录和文件，如 3FS、CephFS、NFS 等。Mooncake 的 `DFS` 和 `DISK` 副本、SGLang 的 3FS 后端都在这一层。
- **FUSE**：一种让文件系统跑在用户态的机制。应用照常读写文件，内核把请求转给用户态的文件系统程序处理。兼容性好，但每次读写多绕一圈，性能一般。3FS 的 FUSE 挂载就是这种。
- **对象存储（S3 / OSS）**：通过 HTTP 接口按"桶 + 对象名"存取整块数据，容量几乎无限、便宜，但延迟高（毫秒级）。Mooncake 通过 offload 路径支持它作为最底层，记为 `LOCAL_DISK` 副本。

### 其他硬件和接口名词

- **NPU / 昇腾（Ascend）**：华为的 AI 加速卡，相当于 GPU 的角色。Mooncake 的 `ascend` 协议、SGLang 的 `kernel_ascend` io-backend 是给它用的。
- **ROCm / HIP**：AMD GPU 的软件栈，HIP 相当于 AMD 版的 CUDA。Mooncake 的 `hip` 协议是给 AMD GPU 用的。
- **UVA（统一虚拟地址）**：CUDA 让 GPU 和 CPU 共用一套虚拟地址空间，GPU kernel 可以直接用指针访问 pinned 的 Host 内存，数据经 PCIe 传输。SGLang 的 `kernel` io-backend 就靠这个让 GPU 直接读写 L2。
- **ZMQ（ZeroMQ）**：一个消息队列库，用来在进程之间发消息。SGLang 用它向路由器发布 KV 事件和负载信息，与 KV 数据本身的传输无关。

## 3. 各层存储组件

### SGLang HiCache 三层

SGLang 的分层缓存叫 HiCache：

- **L1 GPU 显存**：模型推理时直接读写的 KV cache，容量最小、速度最快。
- **L2 Host DRAM**：本机 CPU 内存，存放从 GPU 备份下来的 KV，需要时再拷回 GPU（H2D/D2H）。
- **L3 外部存储**：跨机共享或持久化的 KV 存储，以前缀 hash 为 key、KV 数据为 value。所有后端实现同一个接口 `HiCacheStorage`，部署时用 `--hicache-storage-backend` 选一种。可选后端包括 mooncake、hf3fs、file / fast_file（本地文件）、nixl、aibrix、eic、simm、mori、shm、tensorcast、seaweedfs 等。LMCache 不走这个接口，它以替换整个前缀缓存的方式接入。

### Mooncake Store 的存储介质

Mooncake Store 是分布式 KV 存储，每个对象可以有多种副本。副本类型决定数据放在哪种介质上：

- **MEMORY**：分布式内存池，由各节点注册出来的 DRAM（或显存）组成，读写最快。
- **DISK**：共享文件存储上的磁盘副本。这是旧的方式，由 master 的 `--root_fs_dir` 开启，官方建议不要和 `--enable_offload` 同时用。
- **LOCAL_DISK**：客户端本机 SSD（也可以是 NVMe KV、OSS / S3 等对象存储）。开启 offload（默认关闭）后，数据写进内存的同时异步复制一份到本地盘（开 `offload_on_evict` 时改为淘汰时才写）；再开启 `--promotion_on_hit`（默认关闭）后，被反复读到的数据才会提升回内存（门槛见第 7 节）。
- **NOF_SSD**：通过 NVMe-oF 远程访问的 SSD（实验性质）。
- **DFS**：分布式文件系统，按文件页偏移存放。文件系统适配器只有两种：3FS（设置 `MOONCAKE_DFS_FS_ADAPTER=hf3fs`，编译时 `-DUSE_3FS=ON`，走 3FS 原生 USRBIO 接口）和 posix；另外 `kvcs-lowlevel` 后端也能存 DFS 副本。OSS、S3 不走 DFS，走的是上面 LOCAL_DISK 的 offload 路径。整个 DFS 方式目前仍是开发中、实验性质，不建议生产使用。

所以 Mooncake 内部是两级：第一级是内存池；第二级是盘，上面后四种介质任选。3FS 也可以挂载成普通目录，通过 DFS 的 posix 适配器或旧的 `DISK` 方式使用。

### Mooncake 内存池与 SGLang L2 的区别

**介质**：默认部署下两者都是 CPU DRAM，但细节不同：

- L2 是 pinned（页锁定）内存。SGLang 默认 `pin_memory=True`，这样 GPU 能直接 DMA 读写，H2D/D2H 更快。
- Mooncake 内存池默认也是 Host DRAM，具体怎么分配取决于协议和配置：`rdma` 协议下网卡分布在多个 NUMA 节点时按 NUMA 分段分配；开了大页（hugepage）就用大页；否则 `rdma` / `efa` 协议默认用透明大页（THP）方式映射内存（`efa` 按 NUMA 交错分配）；其他情况才退回普通的对齐分配（`aligned_alloc`）。它也可以不是 DRAM：Mooncake 编译时开 `USE_VRAM_SEGMENT`，走通用分配路径时会改用 GPU 显存（`cudaMalloc`）；用 Ascend、sunrise_link、UB 等协议时，用的是对应设备或互联的内存。

区别主要在归属和访问范围：

- **归属**：L2 是 SGLang 进程自己申请的内存，用作本机 GPU 显存的溢出区。Mooncake 内存池由集群里各节点各贡献一段内存（大小由 `global_segment_size` 配置），由 Mooncake master 统一管理元数据，拼成一个全局池。
- **共享范围**：L2 只服务本实例，其他机器看不到。Mooncake 池全集群共享，一个实例写进去的 KV 前缀，其他实例也能读到并复用。
- **速度与容量**：L2 只经过本机 PCIe，延迟最低，但容量受单机内存限制。Mooncake 池容量是所有节点贡献量之和，通常远大于单机，但访问远端数据要走网络，比 L2 慢。
- **生命周期**：L2 随 SGLang 进程退出而释放。Mooncake 池里的数据在 master 和 store 节点存活期间都保留，SGLang 实例重启后仍能命中。但如果数据所在的那段内存是由 SGLang 进程自己贡献的，进程退出后这部分数据就丢了。

**部署注意**：SGLang **默认就会**给 Mooncake 池贡献内存：`global_segment_size` 默认 4 GB（按 4 GiB 解析），在一个 DP 组的 attention TP × PP 个 rank 之间平分（开 DP attention 时每个 DP 组各贡献一份），所以不单独起 store 服务也能用；设为 0 则只当客户端、不贡献内存。此时这台机器的内存要同时容纳 L2 和贡献出去的那一段，规划内存时两者都要算上。

### 3FS 是什么

3FS（Fire-Flyer File System）是 DeepSeek 开源的分布式文件系统，专为 AI 训练和推理设计，底层用 NVMe SSD + RDMA 网络。用途包括训练数据加载、checkpoint 和推理 KV cache。在 KV cache 场景下，它的定位是比 DRAM 便宜得多、容量大得多、吞吐仍然很高的共享存储。

#### 组成

- **Cluster manager**：管理集群成员和节点状态，多副本部署保证高可用。
- **Metadata service**：负责文件、目录等元数据，本身无状态，元数据存在事务型 KV 数据库 FoundationDB 里，可水平扩展。
- **Storage service**：每个存储节点管理本机多块 SSD，存放文件数据块。副本之间用 CRAQ（链式复制）保证强一致，读请求可以分摊到链上各副本。
- **Client**：有两种接入方式。FUSE 挂载成普通目录，兼容性好，但要经过内核，性能一般；USRBIO 是用户态 I/O 接口，应用把数据放在与 3FS 共享的内存里，直接提交读写请求，绕过内核，延迟和吞吐都好得多。高性能场景（包括 KV cache）都用 USRBIO。

**公开的性能数据**（来自 3FS 官方 README）：180 个存储节点（每节点 2×200Gbps IB、16 块 14TiB NVMe）的集群，聚合读吞吐约 6.6 TiB/s；KV cache 场景下，所有客户端（每节点 1×400Gbps 网卡）的读吞吐峰值约 40 GiB/s。

**和 Mooncake 内存池的取舍**：3FS 数据落在 SSD 上，容量大、成本低、进程或节点重启后数据还在；Mooncake 内存池在 DRAM 上，延迟更低，但容量受集群内存总量限制。

### 3FS 的接入方式

- **直接作为 SGLang 的 L3**：启动参数 `--hicache-storage-backend hf3fs`，L2 直接读写 3FS，不经过 Mooncake，没有分布式内存池那一级。
  - **数据**：KV 页写进 3FS 上的文件，通过 USRBIO 客户端读写，每个方向比零拷贝多一次内存拷贝。每个 rank 在文件里按固定大小的页分配空间；MLA 模型下各 rank 共用同一个文件，只由一个 rank 写入。
  - **元数据**：3FS 只负责存文件，"哪个前缀 hash 对应文件里哪一页"这张索引表由 SGLang 自己维护。单机部署用本地元数据（进程内），多机要共享 KV 时，需要单独起一个全局元数据服务（`mini_3fs_metadata_server.py`），各实例都去查这个服务。MLA 模型只支持全局元数据服务模式。
  - **部署前提**：要先部署好 3FS 集群（官方文档用 k8s 的 3fs-operator），SGLang 所在机器要装 USRBIO 客户端（`hf3fs-py-usrbio`）。

- **作为 Mooncake 的盘层**：用 `DFS` 副本类型（hf3fs 适配器，实验性质），或挂载成目录后用 posix 适配器 / 旧的 `DISK` 副本。这时 3FS 在 Mooncake 内存池之下，是端到端的第 4 级。

## 4. 容量估算与省显存手段

### 每个 token 的 KV 占多少字节

- **普通注意力（MHA / GQA）**：每层存 K 和 V 两份，每份大小 = KV 头数 × 头维度。所以每 token 字节数 = 2 × 层数 × KV 头数 × 头维度 × 每个数的字节数（bf16 为 2，fp8 为 1）。
- **开 TP 时**：KV 头按注意力部分的 TP（开 DP attention 时是 attention TP 大小）切分，每个 rank 只存"KV 头数 / TP"个头；TP 比 KV 头数还大时按 1 个头算，也就是多个 rank 存同样的头。（严格的公式是"头数 × (K 维度 + V 维度)"，K、V 维度相同时就是上面的 2 倍。）
- **MLA（DeepSeek 系列）**：每层只存一个压缩后的向量，维度 = kv_lora_rank + qk_rope_head_dim（DeepSeek-V3 是 512 + 64 = 576），不分 K/V，也**不按 TP 切分**：每个 TP rank 都存完整的一份。（开 DCP 时会按 DCP 切分；DeepSeek-V3.2 等 DSA 模型每 token 还要加上 indexer 的一份开销。）
- **投机解码**：draft 模型的 KV 有自己的池，但和目标模型共用分配器和 `req_to_token` 表（同样的槽位编号），容量估算时每 token 字节数要按 draft 层数相应增加。

**例子**（按上面公式算）：

- Llama-3-70B（80 层，8 个 KV 头，头维度 128）：
  - bf16、TP1：2 × 80 × 8 × 128 × 2 = 327,680 字节 ≈ 320 KB/token。10 GiB 约放 3.3 万 token。
  - bf16、TP8：每个 rank 只有 1 个头，40 KB/token。每张卡 10 GiB 约放 26 万 token。8 张卡存的是同一批 token 的不同头，所以整机也是 26 万 token。
  - fp8、TP8：20 KB/token，每张卡 10 GiB 约 52 万 token。

- DeepSeek-V3（61 层，MLA 576 维）：
  - bf16：576 × 61 × 2 = 70,272 字节 ≈ 68.6 KB/token，10 GiB 约 15 万 token；fp8 减半，约 30 万 token。
  - 不管 TP 多大，每张卡都要存这么多。TP8 时一台机器的 8 张卡存的是 8 份完全相同的 KV。

### 各级池的大小怎么定

- **L1（GPU）**：`--mem-fraction-static` 表示"模型权重 + KV 池"占显存的比例。默认自动算：总显存减去预留部分。预留 = 512 MB + 激活（约 1.5 MB × max(分块 prefill 大小, 2048)）+ 按 TP × PP 增加的一部分 + CUDA graph 预留；大于 60 GB 的卡至少预留 10 GiB，DeepEP 的通信缓冲另加。80 GB 卡上通常在 0.85 左右或更低（0.87 是预留刚好 10 GiB 时的上限）。启动时先加载权重，再测剩余显存，剩下的按比例全部给 KV 池，可放 token 数 ≈ KV 池字节数 / 每 token 字节数。`--max-total-tokens` 只能在此基础上再往下限制。
- **L2（Host 内存）**：**每个 TP rank 各有一份**。
  - `--hicache-ratio`：Host 池能放的 token 数是 GPU 池的几倍。不设置时：普通模式取 2.0，`buffer_only` 模式取 1.2，PD 分离的 decode 实例：回退备份方式为 `host_pool` 且没开 HiCache 时取 0.2（至少能放下一个最长请求），否则取 2.0。
  - `--hicache-size`：直接指定每个 rank 的 Host 池大小（GB），设了就覆盖 ratio。
  - 两者都不设时，还会按机器可用内存自动收缩：整机先留 10 GiB，剩下的按本机 rank 数平分，再乘 `--hicache-host-memory-fraction`（默认 0.8）。
  - MLA 模型的 L2 默认也是每个 rank 存完整一份，没有去重。

- **L3（Mooncake 内存池）**：`global_segment_size` 是**每个 SGLang 实例**（开 DP attention 时是每个 DP 组）贡献的总量，在它的各个 attention TP × PP rank 之间平分（SGLang 的 Mooncake README 里写成"每个 TP rank 贡献 1/global_segment_size"，是笔误）。
  - MLA 模型：每页在 L3 只存一份，只有 TP rank 0 负责写。
  - MHA 模型：每个 rank 各写自己那部分头，合起来才是一页完整的 KV。

### 举例：一台机器各级能放多少

DeepSeek-V3、bf16、TP8 单机（8 张 80 GB 卡），假设每张卡给 KV 20 GB（这里的 GB 按 10^9 字节算）：

- L1：每张卡约 28 万 token。8 张卡存的是同一批 token，整机也是 28 万 token。
- L2：ratio 2.0 时每个 rank 约 40 GB Host 内存，8 个 rank 共占 320 GB，但因为每个 rank 都存完整一份，整机只能放约 57 万 token。
- L3：每页只存一份，Mooncake 内存池每 100 GB 约放 142 万 token。

这个例子说明：MLA 模型在 TP 下 L1、L2 都有 TP 倍的重复，L3 没有重复，所以 L3 的"每 GB 能放的 token 数"是 L2 的 TP 倍。MHA 模型在 TP 不超过 KV 头数时按头切分、不重复；TP 大于 KV 头数时，L1、L2 同样会有"TP / KV 头数"倍的重复。

### 省显存手段

- **KV 量化**（`--kv-cache-dtype`）：
  - 默认 `auto`：跟随模型精度；checkpoint 声明了 FP8 KV 时用 fp8，部分模型（如 DeepSeek-V4，以及 SM100 以上的 DeepSeek DSA 模型）也会自动用 fp8。
  - `fp8_e4m3` / `fp8_e5m2`：字节数减半。每个张量用 checkpoint 里给的一个缩放系数，没给时为 1.0。
  - `nvfp4` 等 4 bit 格式：再减半，另加少量缩放系数；需要 CUDA 12.8 和 PyTorch 2.8 以上，有精度风险。
  - L2、L3 存的是和 GPU 上相同的格式，压缩效果一路带到下面各层。

- **MLA**：模型结构上把 KV 压成一个低维向量，比同规模的 MHA 小很多，但 TP 下每个 rank 都要存完整一份（见上面的例子）。
- **滑动窗口注意力（SWA）**：这类层只需要最近一个窗口内的 KV。GPU 上 SWA 层和全注意力层各用一个池，窗口外的 SWA 数据在前缀树上标记为空、释放掉；两种层在 L2 也各有自己的 Host 池。
- **Mamba 等线性注意力**：每个请求只有一份固定大小的状态，不随序列长度增长。它在 GPU 上预先划出固定的一块，在 L2 也有自己的 Host 池，以请求为单位存放。
- **页大小**（`--page-size`）：KV 按页管理，CUDA 上默认 1 token 一页，部分后端默认 64 或 128。前缀匹配、L2/L3 传输都按整页进行，不足一页的尾巴不会被缓存。页越大，L3 对象越大、传输次数越少，但前缀复用的粒度越粗。生产上用 Mooncake 时常配 64。

## 5. 前缀树（Radix Tree）

前缀树记录"哪些 token 前缀已经算过 KV、KV 放在哪"，L1 和 L2 都由它管理。新请求进来时沿树往下匹配，匹配上的前缀直接复用 KV，不用重算。

**结构**：每条边是一段连续的 token（不是单个 token），节点表示"从根走到这里的整段前缀"。相同的开头只存一份，在分叉处拆成多个子节点。

例子：三个请求依次进来（每个方括号代表一段 token）：

- 请求 1：`[系统提示词] [问题A]`
- 请求 2：`[系统提示词] [问题B]`
- 请求 3：`[系统提示词] [问题A] [追问]`

```text
root
└── [系统提示词]                  ← 三个请求共享，只存一份 KV
    ├── [问题A]                   ← 请求 1、3 共享
    │   └── [追问]                ← 只属于请求 3
    └── [问题B]                   ← 只属于请求 2
```

插入请求 2 时，原来的边 `[系统提示词][问题A]` 在分叉点被拆成 `[系统提示词]` 和 `[问题A]` 两个节点，再挂上新分支 `[问题B]`。

### 节点上存什么

- **key**：这条边对应的 token 序列。
- **children**：子节点表。key 是子边开头第一页（`page_size` 个 token）的内容，再加上请求的命名空间（`extra_key`、`cache_salt`）。插入和匹配前，token 序列会先截断到整页长度，匹配长度也按页向下取整，所以不足一页的尾巴不会被缓存。
- **GPU 位置**（`value`）：这段 token 的 KV 在 GPU 池里的槽位下标。为空表示已从 GPU 淘汰。
- **Host 位置**（`host_value`）：这段 KV 在 L2 Host 池里的槽位下标。为空表示没有 Host 副本。
- **引用计数**（按组件分别存放）：`lock_ref` 记录正在使用 GPU 上这段 KV 的请求数，大于 0 时不能从 GPU 淘汰；`host_lock_ref` 在写 L3 等操作进行中时加上，大于 0 时不能释放 Host 副本。
- **淘汰用的统计**：`last_access_time`（LRU 用）、`hit_count`（LFU 和 write_through_selective 用）、请求优先级等。
- **hash_value**：每页的前缀 hash，就是 L3 存储里的 key。

#### 一个节点的三种状态

- 只在 GPU：刚算完、还没备份到 Host。
- GPU 和 Host 都有：已备份，GPU 淘汰时只释放显存。
- 只在 Host：GPU 已淘汰，再命中时要从 L2 加载回 GPU。

以全注意力 KV（Full 组件）为准，GPU 和 Host 上都没有 KV、没有子节点且没有加锁的节点会从树里删除，并向上逐级清理。L3 里数据的位置不记在树上，靠 `hash_value` 去存储后端查（节点上只有一个"已存到外部"的标记）。

**为什么只淘汰叶子**：子节点的前缀包含父节点，子节点在用时父节点一定也在用。所以淘汰总是从叶子开始：

- GPU 淘汰的是"GPU 层面的叶子"，即子节点都已不在 GPU 上的节点。它被淘汰后可能以"只在 Host"的状态留在树里，它的父节点随后成为新的候选。
- Host 淘汰的是真正没有子节点的节点，淘汰后从树里删除，父节点可能变成新的叶子。

**混合模型**：当前 SGLang 的实现（Unified Radix Cache）一个节点可以同时挂多种组件：全注意力 KV（Full）、滑动窗口 KV（SWA）、Mamba 等线性注意力的状态。每种组件各有自己的 GPU/Host 位置和引用计数。SWA、Mamba 这些辅助组件可以单独释放；但节点是否保留、什么时候从 Host 淘汰，都以 Full 组件为准，Host 淘汰时会一次清掉节点上所有组件。

## 6. L3 的 key、跨实例共享与一致性

### 每页的 hash 怎么算

L3 里每一页 KV 的 key 来自前缀树节点上的 `hash_value`，计算方式：

- 用 SHA-256，**链式计算**：第 1 页的 hash = SHA256(第 1 页的 token id)；第 N 页的 hash = SHA256(第 N−1 页的 hash + 第 N 页的 token id)。所以一页的 hash 代表"从开头到这一页为止的整段前缀"，前面任何一个 token 不同，后面所有页的 hash 都不同。
- **命名空间**：如果请求带了 `extra_key` 或 `cache_salt`，先用它们算一个种子，作为链的起点。不同种子的请求即使 token 完全一样，hash 也不同，互相不会命中。
  - LoRA：请求使用的 LoRA 适配器 id 会自动拼到 `extra_key` 后面，所以不同 LoRA 的 KV 互不共享（它们的 KV 本来就不同）。
  - 多租户隔离：可以给不同租户设不同的 `cache_salt`。

- **多模态**：图片、音频等在 token 序列里会被替换成一串由内容 hash 生成的特殊 token id（远大于文本 token id，不会和文本冲突）。同一张图片得到同样的 id，所以带图片的前缀也能命中缓存。
- **没有算进 hash 的**：模型、权重版本、KV 数据类型、TP 大小。页大小只影响在哪里切页。其中模型名和 KV 数据类型会另外写进 key 的前缀（见下）；权重版本和 TP 大小在 key 里都没有。

### 发给 Mooncake 的 key 长什么样

默认的 key 方案（`rank-suffix`）：

- 前缀：可选的后端标签 + 服务的模型名 + 存储格式标签（如有）+ `dtype_{KV 数据类型}`。只有开了 DCP（decode 上下文并行）时才会再加 `tp{N}_dcp{M}_page{P}_pp{Q}_cp{R}` 这样的配置信息。
- MHA 模型：`{前缀}_{hash}_{TP rank}_k` 和 `..._v` 两个对象（PP > 1 时 TP rank 后再加 `_{PP rank}`），每个 rank 写自己那部分头。
- MLA 模型：`{前缀}_{hash}__k` 一个对象（PP > 1 时中间是 `_{PP rank}_`），没有 TP rank，所以所有 TP rank 共用。
- draft 模型、SWA 层等额外的池在 rank 后缀之后、`_k` / `_v` 之前加池名，如 `_{TP rank}_draft_k`；MLA 类的额外池是 `_{PP rank}_{池名}`。

还有一种可选的统一方案（`--hicache-storage-key-scheme unified`）：在 key 里加入一段摘要，摘要由模型名、KV 数据类型、页大小、KV 头总数、头分组方式、层分组方式、存储布局、是否各 rank 复制等算出，key 里再带上与拓扑无关的层号和头组号。配置不同的实例 key 就不同，只会不命中，不会读错；而头分组相同时，TP 大小不同的实例可以共用同一批 key。

### 哪些实例之间能共享 L3 里的 KV

- **同一模型、同样配置的多个实例**：可以共享，这是 L3 的主要用途。需要用同一个 Mooncake 集群、同一个 `tenant_id`、同样的模型名。
- **MLA 模型、TP 不同**：可以共享（key 里没有 TP rank）。PP 大小不同则不能（key 后缀不同，只会不命中）。
- **MHA 模型、TP 不同**：默认方案下**不安全**。key 里有 TP rank 但没有 TP 大小，TP2 的 rank 0 和 TP4 的 rank 0 会用同一个 key，但存的头不一样。先写的那份留下（之后的写入发现 key 已存在就跳过）；TP4 去读 TP2 写的更大的对象时，Mooncake 报缓冲区太小、当作未命中；TP2 去读 TP4 写的更小的对象时，SGLang 会把这次部分读当作成功，从而用上错误的 KV。要混用不同 TP，有两种办法：默认方案下在 extra-config 里给所有实例设置相同的 `tp_lcm_size`（需要 `page_head` 布局），每个 rank 按更细的粒度拆成多个对象写；或者改用统一方案，并让所有实例设置相同的头分组（`--hicache-storage-head-partition`）。
- **页大小不同**：hash 的切页位置不同，只会不命中。
- **KV 数据类型不同**（如 bf16 和 fp8 混用）：两种方案的 key 前缀里都有 KV 数据类型（fp8 的 e4m3 和 e5m2 也会区分），只会不命中，不会读错。
- **模型名相同但权重不同**（比如更新了权重）：两种方案的 key 都一样，**会读到旧权重算出的 KV**。

结论：要正确，共享同一个 L3 的实例必须保持模型权重一致，MHA 模型还要 TP 一致（或按上面的办法配置）；要命中率高，页大小、KV 数据类型、PP 也要一致。需要混部时用统一 key 方案，或者用不同的 `tenant_id` 把它们隔开。

### 失效与一致性

- **SGLang 不会自动删除 L3 里的数据**，L3 的容量由后端自己淘汰。所以模型或权重更新后，旧 KV 会一直留在 L3 里，直到被挤掉。安全的做法是换一个模型名或 `tenant_id`，或者调用 `POST /hicache/storage-backend/clear` 清空 L3（Mooncake 后端调用 `remove_all`，会清掉整个 Mooncake 集群里的数据，不只是本实例写的），或者重启 Mooncake 集群。
- **`/flush_cache` 接口**：只在实例空闲时执行（没有运行中和排队中的请求；实例处于暂停状态时不看排队请求），清空 GPU 上的前缀树和 KV 池，同时清空 Host（L2）内存池和进行中的预取、备份状态。L3 里的数据不会被删除。
- **权重版本追踪**（`--enable-prefill-weight-versions`）：给 GPU 上每个 KV 槽位记录"它是用哪个权重版本算出来的"，请求 prefill 完成后把各段 KV 对应的权重版本返回给调用方。这是给强化学习等在线更新权重的场景用的，用来知道一个请求的 KV 混用了哪些版本。它只记录，不会让旧 KV 失效。它和 HiCache 互斥（开了 `--enable-hierarchical-cache` 就不能用），因为从 L2/L3 恢复的 KV 没有版本信息。

### 读失败时怎么办

- **L3 预取失败或没读完**：预取按批进行，遇到失败的那一批后不再继续读（但仍给每一批发确认消息，保持各 rank 同步）。已经读到的部分照常使用，剩下的部分重新计算。这对正确性没有影响，只是少命中了一些。
- **Mooncake 节点在读的过程中挂掉**：那一部分读取失败，按上面的方式退回重算。由于默认只有一个副本，这部分数据在 L3 里就丢了。
- **直连模式下加载失败**：按层加载时，前向计算不会中途报错，但这批请求在前向结束后会被中止（返回错误），而不是用错误的 KV 继续生成；整段预取时失败的部分改为重算。
- **L2 → L3 写失败**：从失败的那一批起不再继续写，已经在 L2 的数据不受影响，只是 L3 没有这份备份。

## 7. 数据流转：什么时候搬、按什么策略搬

### SGLang：L1、L2、L3 之间

#### 总览

- L1 → L2：按写策略备份，异步 GPU 拷贝。
- L2 → L3：L1 → L2 备份完成后立即异步写入。
- L3 → L2：请求到来时预取。
- L2 → L1：前缀命中 Host 副本时加载回 GPU，按层与计算重叠。
- HiCache 模式下数据总是先落到 L2，没有 L3 直接到 GPU 的路径（直连模式除外）。

**L1 → L2：写策略**。由 `--hicache-write-policy` 决定什么时候把 GPU 上的 KV 备份到 Host：

- **write_through**（默认）：节点第一次命中就备份，实际上新插入时就会备份。
- **write_through_selective**：节点被命中 2 次才备份，只备份被复用过的前缀，节省 Host 空间和 PCIe 带宽。阈值写死，不可配置。
- **write_back**：平时不备份，只在 L1 淘汰这个节点时才拷到 Host。

拷贝在专用的 D2H CUDA stream 上异步执行，并等待前向计算的 stream，保证不会读到还在写的 KV。拷贝完成后节点被标记为"已备份"。

#### L2 → L3：写入存储

- **时机**：L1 → L2 备份一完成，就把这些节点提交给 L3，不再另设命中阈值。
- **执行**：后台线程 `hicache-backup` 负责，每批 128 页调用后端的 `batch_set_v1`（零拷贝路径；旧路径是 `batch_set`）。只有部分 rank 负责写，避免多个 TP rank 重复写同一份数据。
- **保护**：写 L3 期间给 Host 页加锁，这些页在写完前不会被 L2 淘汰。
- **去重**：SGLang 写之前不先查 L3 是否已有这份数据，去重由后端在 `batch_set` 里自己处理。

#### L3 → L2：预取

- **触发**：请求进来后，如果本地 L1、L2 只匹配了前缀的一部分，就对剩下的部分发起 L3 预取。剩余部分少于 `prefetch_threshold`（默认 256 token）时不预取。正在预取的 token 总量超过上限时也会跳过。
- **流程**：先由 `hicache-prefetch` 线程用 `batch_exists` 按 128 页一批查 L3 能命中多少，遇到第一个未命中就停。各 rank 取命中数的最小值，保证结果一致。然后分配 Host 空间，由 `hicache-prefetch-io` 线程用 `batch_get` 读到 L2。
- **何时结束**：由 `--hicache-storage-prefetch-policy` 决定请求等多久。
  - `best_effort`：不等，调度时已经到了多少就用多少。
  - `wait_complete`：一直等到预取完成。
  - `timeout`（默认）：最多等 `1 秒 + 每 1024 token 0.25 秒`，超时后用已到的部分，没到的部分重新计算。（这是当前代码的默认值；SGLang 官方 hicache_design 文档里写的 2 秒 / 0.1 秒 / 上限 30 秒与代码不符。）

#### L2 → L1：加载回 GPU

- **触发**：调度请求时，如果命中的前缀只在 Host 上有副本，就把它加载回 GPU。少于 10 个 token 时不加载，直接重算更划算。GPU 空间不够时也不加载。
- **执行**：在专用的 H2D stream 上异步拷贝，按层与本 batch 的前向计算重叠。

### Mooncake 内存池的写入和读取

- **写入（Put）**：client 先向 master 申请空间（PutStart），master 选好目标节点的内存段后返回地址。client 再通过 Transfer Engine 把数据直接写到这些地址，最后通知 master 写完（PutEnd）。数据不经过 master。默认 1 个副本。
- **读取（Get）**：master 返回所有可读副本，client 按"本机内存 → 本机 NoF SSD → 远端内存 → 远端 NoF SSD → 本地 SSD 副本 → DFS → DISK"的顺序选一个读。每次读取会给对象续一个租约（lease，默认 10 秒），租约期内不会被淘汰，避免读到一半被删。

### Mooncake 内存池 ↔ 本地 SSD

需要开启 `enable_offload`（默认关闭）。

- **写到 SSD（offload）**：
  - 默认在 PutEnd 时就排队 offload，即写入内存的同时安排写一份到 SSD，内存满了被淘汰时数据还在 SSD 上。
  - 开 `offload_on_evict` 后，改为内存淘汰时才 offload，SSD 只存被挤出去的冷数据。
  - offload 写到持有这份内存副本的那台机器的本地 SSD，不是写入方的 SSD。
  - 执行方是那台机器上的 client：每次心跳（默认 10 秒）从 master 拉一批任务，从内存读出、写入 SSD，再通知 master 登记 LOCAL_DISK 副本。每个本地盘段最多积压 5 万个任务（`offloading_queue_limit`），每轮最多处理一半。

- **读回内存（promotion）**：需要再开 `promotion_on_hit`（默认关闭）。读取时如果只有 SSD 副本，并且这个 key 的访问次数达到门槛（默认 2 次），而内存使用率低于淘汰水位线，就排队把它提升回内存。由持有 SSD 副本的 client 在心跳时执行，默认每次心跳只处理 1 个。

## 8. 淘汰

### SGLang L1、L2、L3

- **策略**：L1 和 L2 都用 `--radix-eviction-policy`，默认 `lru`（最久未访问的先淘汰）。可选的还有 `lfu`（命中次数少的先淘汰）、`priority`（低优先级请求的前缀先淘汰）、`slru`（命中 2 次以上的进入保护区，较晚淘汰）、`tlru`、`joint_lru`、`state_cost` 等。
- **时机**：都是按需淘汰，分配空间不够时才淘汰，没有后台定时清理。只淘汰叶子节点，并且没有正在运行的请求引用它。
- **L1 淘汰后节点去哪**：
  - 已有 Host 副本：只释放 GPU 显存，节点留在树里变成"只在 Host 上"，之后命中可以从 L2 加载回来。
  - write_back 策略：先拷到 Host 再释放 GPU；Host 也满了就直接丢弃。
  - write_through 下还没来得及备份的节点：直接丢弃，下次只能重算或从 L3 取。

- **L2 淘汰**：只淘汰已不在 GPU 上、没有被加锁（包括正在写 L3）的 Host 叶子节点。淘汰后节点从树里删除。数据如果已写进 L3，之后还能从 L3 预取回来。
- **L3 淘汰**：SGLang 从不删除 L3 的数据，容量管理交给后端：本地文件后端用 LRU 删文件；Mooncake 内存池由 master 按内存水位淘汰，本地 SSD 由各 client 按磁盘水位淘汰，细节如下；3FS 等其他后端由各自的服务端处理。

### Mooncake 内存池

- **触发**：master 每 10 ms 检查一次，内存使用率超过 `eviction_high_watermark_ratio`（默认 0.9），或者有写入因为空间不够失败，就触发淘汰。
- **数量**：每轮淘汰约 `eviction_ratio`（默认 5%）的对象。如果用量超出水位线较多，就再多淘汰超出的部分。
- **顺序**：近似 LRU，按租约到期时间排序，越早到期（越久没被读）的越先淘汰。
- **跳过规则**：
  - hard pin 的对象永不淘汰。
  - 租约未到期的跳过。
  - soft pin 的对象（默认保留 30 分钟）只在普通对象不够淘汰时才淘汰。
  - 正在被引用的副本（如正在 offload 到 SSD）暂不释放。

- **去向**：默认直接丢弃。开启 `offload_on_evict` 后，先把数据转存到 SSD 再释放内存。
- **多租户**：开启多租户时，某个租户用量超过自己配额的 90% 就单独淘汰它的数据。

### Mooncake 本地 SSD

client 在心跳时检查，SSD 使用量超过 90% 就淘汰到 80%；写入时空间不够也会立即淘汰。默认的 bucket 存储后端按写入先后顺序（FIFO），以 bucket 为单位淘汰最旧的数据。淘汰后通知 master 删除对应的 SSD 副本记录。默认 SSD 容量上限 2 TB、1000 万个 key。

## 9. 传输方式：数据走什么线路、由谁来搬

下面用 L1 = GPU 显存、L2 = 本机 Host DRAM、L3 = Mooncake 内存池（或其他 L3 后端）、L4 = Mooncake 盘层。

### 每一跳的物理路径

- L1 ↔ L2：同一台机器内，GPU 显存 ↔ PCIe ↔ Host 内存。
- L2 ↔ L3：通常跨机器，本机 Host 内存 ↔ 本机网卡 ↔ 网络交换机 ↔ 对端网卡 ↔ 对端内存池。如果内存池那一段恰好在本机，就不出机器。
- L3 ↔ L4：内存池 ↔ 本机 NVMe SSD 是同机内的 PCIe；访问远端 SSD（NVMe-oF）或分布式文件系统（3FS 等）则要走网络。

### L1 ↔ L2：PCIe

走本机 PCIe，由 `--hicache-io-backend` 决定谁来搬数据：

- `kernel`**（默认）**：GPU 上跑一个拷贝 kernel，由 GPU 计算单元（SM）直接读写 Host 内存。Host 内存是 pinned 的，GPU 可以通过映射地址直接访问。好处是分散的页一次 kernel 就能搬完；代价是占用一部分 SM。
- `direct`：用 GPU 的拷贝引擎（DMA，`cudaMemcpyAsync`）。`layer_first` 布局下先把地址连续的页合并成段，每段一次拷贝；`page_first_direct` 布局在 CUDA 12.8 以上（驱动也要 12.8 以上）用批量拷贝接口，否则逐页拷贝。不占 SM，但要先把页索引拷回 CPU；DMA 还可能排在前向计算的小拷贝前面，拖慢前向。
- `kernel_ascend`：昇腾 NPU 专用。

`--hicache-mem-layout` 决定 KV 在 Host 上怎么摆，也限定了能用哪种 io-backend。常用的是下面三种（另有 `page_first_kv_split`、`layer_first_kv_split`、`page_head`，以及统一 key 方案强制使用的 `page_unified`）：

- `layer_first`：每一层的 KV 连续存放，适合按层加载回 GPU。kernel、direct 都能用。
- `page_first`（默认）：同一页所有层的 KV 放在一起，接近 L3 里的一个对象，写 L3 时更连续。只能用 kernel。
- `page_first_direct`：每页每层连续，适合 DMA 整页拷贝。用 direct。
- 选 Mooncake（或 `npu_memcache`）作 L3 时不支持 `layer_first`，会自动改成 page_first 系列（开 DCP 时例外）。

### L2 ↔ L3：取决于 L3 后端

- **Mooncake**：走 Mooncake Transfer Engine。L2 整块注册给 Mooncake，读写直接用 L2 里的地址。协议由配置里的 `protocol` 或环境变量 `MOONCAKE_PROTOCOL` 决定，SGLang 里两者都没配置时**默认是 `rdma`**（单边 RDMA 读写、零拷贝）。只有直接用 Mooncake 自带的 Python 配置或独立部署的 `mooncake_client` 时，默认才是 `tcp`。`tcp` 下走 socket，经过内核缓冲区。
- **3FS（hf3fs）**：走 3FS 的 USRBIO 用户态接口。写时先把 L2 的页 memcpy 到与 3FS 共享的内存区再提交 I/O，读时反过来，每个方向多一次内存拷贝。共享内存区到 3FS 存储节点的传输由 3FS 客户端库完成。
- **本地文件（file）**：普通 POSIX 文件读写，经过内核页缓存。读时直接读进 L2 的页；写时先写临时文件再原子改名。
- **NIXL**：NIXL agent 加存储插件，自动按 3FS、POSIX、GDS_MT、GDS 的顺序选一个可用的文件插件，也支持 S3 对象存储。`page_first` 系列布局时 L2 整块注册、零拷贝；其他布局要经过一块中转缓冲区。

### 零拷贝

零拷贝的一般含义：数据从源内存直接送到目标内存，中间不经过任何临时缓冲区，也不需要 CPU 逐字节搬运。

用 RDMA 协议时，L2 到 Mooncake 是零拷贝：SGLang 启动时把整块 L2 内存注册给 Mooncake（RDMA 下就是注册给网卡），读写时只传 L2 里的地址和长度（`batch_put_from` / `batch_get_into`），网卡直接从 L2 读数据发到远端，或把远端数据直接写进 L2，中间不用先拷到一块临时缓冲区。

- **代价**：注册的内存会被锁定。有的环境（如 eRDMA）对可注册总量有上限，L2 加上 `global_segment_size` 超限就会注册失败。
- **TCP**：没有 RDMA，数据要经过内核 socket 缓冲区，所以不是严格意义的零拷贝。

### Mooncake 内部与盘层

- **client ↔ 远端内存池**：走 Transfer Engine。`rdma` 协议下写入是单边 RDMA write，读取是单边 RDMA read，远端机器的 CPU 不参与。同一进程内的副本只有在 TCP 模式或设置了 `MC_STORE_MEMCPY` 时才直接 memcpy；RDMA 模式下写本机的段也会经网卡回环。
- **内存池 → 本地 SSD（offload）**：持有内存副本的 client 直接拿本机内存地址写盘，不经过 Transfer Engine。用 `pwritev` 或 io_uring（部分后端可开 O_DIRECT 绕过页缓存）；`nvme_kv` 后端直接发 NVMe KV 命令。
- **从其他节点的本地 SSD 读**：请求方先发 RPC，持有方把数据从 SSD 读进自己的一块中转内存（已注册给 Transfer Engine），请求方再用 Transfer Engine（RDMA 下是 RDMA read）拉走。路径是 SSD → 持有方内存 → 网络 → 请求方内存。
- **本地 SSD → 内存池（promotion）**：持有方把数据读进中转内存，再用 Transfer Engine 写进新分配的内存副本。
- **NOF_SSD**：用 SPDK 的 NVMe-oF 客户端直接对用户缓冲区发 NVMe 读写，不经过 Transfer Engine，没有中转拷贝。要求缓冲区是大页内存并注册给 SPDK。NVMe-oF 底下走 RDMA 还是 TCP 由目标端配置决定。
- **DISK（共享文件系统）**：写入时先把数据拷进一块内存，再由后台 2 个线程写文件；读取时直接读进用户缓冲区。用 POSIX 或 io_uring。
- **DFS**：不经过 Transfer Engine，直接调文件系统或对象存储。`posix` 适配器用 `preadv` / `pwritev` 直接读写用户缓冲区（经过页缓存）；`hf3fs` 适配器每块多一次 memcpy 到 3FS 共享内存区；另有 `kvcs-lowlevel` 后端。OSS / S3 走 HTTP（libcurl），但属于 offload 路径，不是 DFS。

### Transfer Engine 支持的协议

Transfer Engine 是 Mooncake 的数据传输层，对上提供统一的"把这块内存读/写到那块内存"接口，对下按配置的协议选具体的传输方式：

- `rdma`：用 RDMA 网卡（InfiniBand 或 RoCE），通过 ibverbs 做单边读写，对端 CPU 不参与。大请求切成 64 KB 的分片发送；按机器拓扑给每块内存选离它最近的网卡。支持 GPUDirect RDMA，显存可以直接注册给网卡（dmabuf 或 nvidia-peermem），网卡直接读写显存。生产环境跨机传 KV 基本都用它。
- `rdma_twosided`：RDMA 的双边模式（send/recv），对端要先准备好接收缓冲区。和 `rdma` 不能同时开。
- `tcp`：普通 socket，任何网络都能用，但要经过两端内核、CPU 参与拷贝，带宽和延迟都差很多。显存里的数据要先拷到 Host 内存再发。SGLang 里默认用的是 `rdma`；Mooncake 自带的 Python 配置和独立的 `mooncake_client` 没配置协议时默认是 `tcp`，生产上要确认改成了 `rdma`。
- `nvlink`：跨机 NVLink（MNNVL，如 GB200 NVL72 机柜），用 CUDA 的跨机显存共享句柄，GPU 之间直接传。
- `nvlink_intra`：同一台机器内的 GPU 之间，用 CUDA IPC 共享显存，经 NVLink 传输。
- `shm`：同一台机器内的进程之间，用共享内存，一次 memcpy。
- `efa`：AWS 云上的 RDMA 网卡 EFA，通过 libfabric 接口读写。
- `cxi`：HPE Slingshot 网络的网卡，也通过 libfabric。
- `nvmeof`：通过 cuFile（GPUDirect Storage）读写 NVMe 盘，可以让 SSD 直接 DMA 到显存。
- 其他：`cxl`（CXL 内存）、`hip`（AMD GPU）、`ascend`（华为昇腾 NPU）、`nccl`、`barex`、`ub`、`ubshmem`、`hylink`、`maca`、`musa`、`flagcx`、`sunrise_link` 等，对应特定厂商的硬件或通信库，本文未细查。

### 绕过 L2：L3 ↔ GPU 直连

除了 HiCache 的 L1 → L2 → L3 链路，SGLang 还有一种直连模式：`--enable-unified-cache-external-linker`，后端选 mooncake。

- 把 GPU 上的 KV 池直接注册给 Mooncake，读写都在 GPU 显存和 Mooncake 之间进行，没有 L2。
- 和 HiCache 互斥，不能同时开 `--enable-hierarchical-cache` 或 `--hicache-storage-backend`，也不能关掉前缀缓存；不支持流水线并行（PP > 1）。后端可选 `mooncake`（默认）、`mori`、`dynamic`。
- 是否真正不经过 Host 内存，取决于 Transfer Engine 用的协议：`rdma` 且网卡支持 GPUDirect RDMA 时，网卡直接读写显存；`tcp` 时仍要在 Host 上中转。

## 10. 计算与传输的重叠

### 为什么要重叠、靠什么实现

KV 在各级之间搬运要花时间。如果每次都等搬完再计算，GPU 就会空等。"重叠"就是让搬运和计算同时进行，用计算时间把搬运时间藏起来。实现手段主要有三种：

- **CUDA stream（流）**：GPU 上的任务队列。同一个 stream 里的任务按顺序执行，不同 stream 之间可以并行。把拷贝放在单独的 stream 上，就能和前向计算的 stream 同时跑。
- **CUDA event（事件）**：stream 里的一个标记点。一个 stream 可以"等另一个 stream 走到某个 event"再继续，这种等待发生在 GPU 上，CPU 不用停下来。
- **后台线程**：CPU 上单独的线程负责 L3 读写、网络传输，主线程继续调度和下发计算。

### 各段传输的重叠情况

每一项先说哪些事同时进行，再说必须停下来等的地方。

- **L1 → L2 备份**：在专用的 D2H stream 上进行，和后续的前向计算同时跑。
  - 不重叠的地方：每次提交拷贝前，D2H stream 要先等前向 stream 上已经排好的计算做完，因为这些计算可能还在写要备份的 KV。等待发生在 GPU 上，CPU 不停。
  - write_back 策略下，淘汰时要把数据先拷到 Host，CPU 会同步等待拷贝完成，而拷贝又要先等正在跑的前向结束。所以 write_back 下的淘汰会打断重叠。

- **L2 → L1 加载**：按层流水，同一个 batch 内重叠。H2D stream 按层拷贝，每拷完一层记一个 event；前向计算到第 N 层时，GPU 只等第 N 层的 event。效果是"GPU 在算第 1～N 层时，第 N+1 层以后的 KV 还在从 Host 往上拷"。
  - 不重叠的地方：加载开始前，H2D stream 要先等上一个 batch 的前向做完（要写入的显存位置可能刚被回收，上一个 batch 还在用）。所以加载只和本 batch 的前向重叠，不和上一个 batch 重叠。
  - 用 CUDA graph 执行、而 graph 里带不了这些 event 时，会在执行前等所有层加载完，这次就没有按层重叠。
  - 投机解码的 draft 模型要等最后一层加载完才开始，也没有按层重叠。
  - io-backend 的影响：`kernel` 用 GPU 的 SM 拷贝，会和计算抢 SM；`direct` 用拷贝引擎，不抢 SM，但可能卡住前向计算自己的小拷贝，可以设 `SGLANG_ENABLE_MLP_SYNC_METADATA_FILL=1` 缓解。

- **L3 → L2 预取**：请求一到达、还没进等待队列就发起预取，由后台线程查询和读取。预取和"请求自己排队等调度"的时间重叠，也和其他 batch 的 GPU 计算、CPU 调度重叠，不占 GPU stream。
  - 不重叠的地方：轮到这个请求准入时如果预取还没完成，就按 `--hicache-storage-prefetch-policy` 决定：`wait_complete` 继续等（请求本轮不调度），`timeout` 等到超时为止，`best_effort` 不等、用已到的部分。

- **L2 → L3 写入**：后台线程 `hicache-backup` 负责，和所有计算、调度并行。唯一的先后约束是：某页必须先完成 L1 → L2 拷贝，才能开始往 L3 写。
- **Mooncake 内部（内存池 ↔ SSD）**：offload 由持有数据的 client 在心跳时（默认 10 秒一次）后台执行，promotion 在心跳或预取时执行，都与推理异步，推理侧不等它们。
- **调度与计算重叠（overlap scheduler，默认开启）**：GPU 在跑第 N 个 batch 时，CPU 已经在准备第 N+1 个 batch，包括前缀匹配、提交 L1 → L2 备份、提交 L2 → L1 加载、检查各种传输是否完成。这些检查只查询完成状态、不阻塞，所以正常情况下不打断重叠。
- **L3 ↔ GPU 直连模式**：
  - 加载：按层分组（默认 8 层一组）并行拉取，一组到位就让前向算这一组，和计算按层重叠。这里的等待发生在 CPU 上：数据没到时，下发计算的线程停住，已经下发的前面几层继续在 GPU 上跑。加载跟不上时，GPU 会空等。
  - 写出：前向结束后由后台线程把新算的 KV 写到 Mooncake，和后续计算并行。
  - 不重叠的地方：下一个 batch 的加载要等当前 batch 的前向做完才开始写显存，只有准备 key 的工作能提前做。

- **PD 分离的 KV 传输**：
  - prefill 侧：一个请求（或一个分块）的 prefill 算完后才把整份 KV 发给 decode，不是边算边按层发。发送由后台线程完成，和 prefill 实例的下一批计算重叠。`SGLANG_DISAGG_PREFILL_EARLY_SEND_CACHED_PREFIX` 默认开启（设为 0 可关闭）：已经在显存里命中的前缀先发出去，和剩余部分的计算重叠。
  - decode 侧：等待接收 KV 的请求放在单独的队列里，调度器只做非阻塞查询，其他请求照常 decode。

- **分块 prefill**：PD 模式下每算完一个分块就发一次 KV，所以长请求的前面几块可以和后面几块的计算重叠。

### 小结

L2 → L3 写入、L3 → L2 预取、Mooncake 内部的 SSD 读写都在后台进行，和计算基本完全重叠。L2 → L1 加载（以及直连模式的加载）按层和本 batch 的计算重叠，但要等上一个 batch 结束才能开始。L1 → L2 备份和后续计算重叠，但 write_back 策略下的淘汰会让 CPU 同步等待。PD 的 KV 发送粒度是整个请求或分块，不是按层。

## 11. PD 分离的 KV 传输

### PD 分离是什么

一个请求的推理分两个阶段：**prefill**（一次性算完整个输入，产出全部输入 token 的 KV 和第一个输出 token）和 **decode**（每次生成一个 token）。prefill 主要受算力限制，decode 主要受显存带宽限制，放在同一组 GPU 上会互相干扰。PD 分离就是让 prefill 和 decode 跑在不同的实例上，prefill 实例算完后把 KV 传给 decode 实例继续生成。

### 一个请求的流程（以 Mooncake 后端为例）

1. 路由器给请求选一个 prefill 实例和一个 decode 实例，把同一份 bootstrap 信息（prefill 地址、bootstrap 端口、一个"房间号"）同时发给两边。
2. decode 实例连上 prefill 的 bootstrap 服务（默认端口 8998），拿到 prefill 的并行配置，并在第一次连接时把自己 KV 池的显存地址注册给 prefill。
3. decode 先在自己的 KV 池里给这个请求**预分配好槽位**，把槽位编号等信息发给 prefill。
4. prefill 正常计算。每算完一个分块（或整个请求），由后台线程通过 Transfer Engine 把这部分 KV **直接写进 decode 预留好的显存**（RDMA 单边写，decode 的 CPU 不参与）。数据按层组织，但发送发生在这一块的计算完成之后。
5. 最后一块写完后，prefill 再写一份附带数据（如第一个输出 token），并通知 decode 传输完成。
6. decode 实例的调度器只做非阻塞查询，发现传输完成后把请求放进 decode batch。

传输后端由 `--disaggregation-transfer-backend` 选择，默认 `mooncake`，还有 `nixl`、`ascend`、`mori`、`mooncake_tcp`（强制走 TCP）等。模式由 `--disaggregation-mode prefill/decode` 指定。

### prefill 和 decode 的 TP 不同时

- **MHA / GQA**：支持。prefill 的每个 rank 把自己持有的头写到 decode 对应 rank 的对应头位置；decode 的 TP 更大时，几个 decode rank 共用一个头（GQA 的头复制）。这条路径按 token 一个个发，传输次数多，可能拉高首 token 延迟；可以开 `SGLANG_DISAGG_STAGING_BUFFER`（仅 mooncake / nixl 后端）先在中转缓冲区拼好再发。
- **MLA**：每个 rank 都有完整的 KV，不需要切分，直接整份发送。
- Mamba 等状态类模型在 TP 不同时按状态切片传输；不支持的组合（如开 unified memory、KV 分片、DFLASH）在 decode 向 prefill 注册时被拒绝，不是在启动时。

### 和 HiCache 的配合

- **prefill 侧**：可以正常开 HiCache 和 L3，命中的前缀不用重算，直接从 L2/L3 加载后一起发给 decode。官方最佳实践给了两种 PD 配法：只在 prefill 侧开 HiCache；或者 prefill 侧开 HiCache、decode 侧开异步写出（多轮对话时 prefill 能复用 decode 写出的 KV）。
- **decode 侧**：开了 decode 侧前缀缓存（`--disaggregation-decode-enable-radix-cache`，默认关闭）或 decode HiCache 时，decode 也会查本地缓存和 L2/L3。如果它自己能找到一部分前缀，就只让 prefill 传剩下的部分。
- **decode 侧写出**：`--disaggregation-decode-enable-offload-kvcache`（默认关闭）开启后，decode 生成的新 KV 也会写到 L3，供后续多轮对话复用。只能在 decode 侧开，必须同时配置 `--hicache-storage-backend`，并且不能和 `--disaggregation-decode-retraction-backup host_pool` 同时用。

### 超时设置

- `SGLANG_DISAGGREGATION_BOOTSTRAP_TIMEOUT`：bootstrap 握手超时，默认 300 秒。
- `SGLANG_DISAGGREGATION_WAITING_TIMEOUT`：等待 KV 传输完成的超时，默认 300 秒。
- `SGLANG_DISAGGREGATION_HEARTBEAT_INTERVAL` / `..._MAX_FAILURE`：decode 向 prefill 发心跳（prefill 不检测 decode），间隔 5 秒（最小 2 秒），连续失败 2 次判定 prefill 失联。

## 12. 特殊场景：投机解码、多模态、稀疏注意力

### 投机解码

投机解码用一个小的 draft 模型先猜几个 token，再让大模型一次验证。

- draft 模型的 KV 通常有自己的池，但和目标模型共用分配器和槽位编号，分配、释放一次完成。只有开 `--enable-unified-memory`、目标模型是 SWA/Mamba 混合模型、并用 EAGLE 或 DFLASH 时，draft 的层才直接放进目标模型的池里（fused 方式）。
- 被拒绝的猜测 token 对应的槽位在验证后释放。
- 每 token 字节数会按 draft 层数增加，容量估算时要算进去。
- 备份到 L2/L3 时有三种方式：fused 方式下 draft 层本来就在目标模型的页里；packed 方式把 draft 层打包进目标模型的 Host 页；sidecar 方式才作为单独的池（`DRAFT`）写进 Mooncake。

### 多模态

- **前缀匹配**：图片、音频在 token 序列里被替换成由内容 hash 生成的特殊 token id，同一张图片得到同样的 id，所以"同一张图 + 同样的文字"可以命中前缀缓存。
- **编码器输出缓存**：图片经过视觉编码器得到的 embedding 也可以缓存。SGLang 有一个 embedding 缓存，按内容 hash 存放，Host 上有自己的页式内存池（LRU 淘汰），后端可以是 Mooncake（`MooncakeEmbeddingStore`），这样多个实例遇到同一张图片时不用重新跑编码器。开启参数是 `--enable-mm-global-cache`（默认关闭）和 `--mm-global-cache-backend mooncake`，目前只在 encoder 分离部署的 encoder 服务里生效。
- **路由**：sgl-router 的 `--cache-media-affinity-ttl-ms` 会记住带图片的对话发到了哪个实例，后续轮次优先发回去。

### 稀疏注意力（HiSparse）

- 思路：完整的 KV 放在 Host 内存，每一步只把注意力真正需要的那部分 token（由模型的稀疏选择机制选出）拷到 GPU 上的一块缓冲区里计算。这样 GPU 只需要一小块显存，就能支持很长的上下文。
- 开启：`--enable-hisparse`，只支持特定模型（DeepSeek V3.2、GLM-5 等带 DSA 稀疏注意力的模型，以及 DeepSeek V4、MiniMax M3），而且要求关闭前缀缓存（`--disable-radix-cache`），所以不能和 HiCache 的多级缓存同时使用。
- 它和 HiCache 都用到 Host 内存，但目的不同：HiCache 用 Host 内存缓存"以后可能复用的前缀"；HiSparse 用 Host 内存存放"当前请求放不进 GPU 的那部分 KV"。

## 13. 请求调度、准入与负载均衡

调度分两层：

- **实例内调度**：单个 SGLang 实例的 scheduler 决定等待队列里哪些请求先进 batch。
- **跨实例负载均衡**：多个实例前面的路由器（sgl-router）决定请求发给哪个实例。

SGLang 两层都有，而且都会看 KV cache 命中。准入（请求能不能放进来）也分两层：实例内按 KV 显存余量决定能否进 batch；集群级由 sgl-router 按实例负载决定往哪发、是否直接拒绝。Mooncake 不做请求调度，只提供全局前缀索引（Conductor）、存储侧的租户配额和 KV 数据存放位置的均衡。

### SGLang 实例内调度

**调度策略**（`--schedule-policy`，默认 `fcfs`）分两类：

- 不看缓存：`fcfs`（先到先服务）、`lof`（输出最长的先跑）、`random` 等。
- 看缓存：`lpm`（最长前缀匹配优先）、`dfs-weight`、`hrrn`、`shortest-prefill-first` 等。
- 关闭前缀缓存时，`lpm`、`dfs-weight`、`hrrn` 退化为 `fcfs`；`uniboost` 照常工作；`shortest-prefill-first` 会直接报错。

**lpm 怎么用前缀树**：对等待队列里的每个请求去前缀树匹配，按命中长度从长到短排序。命中多的先跑，需要新算的 token 少，而且它依赖的前缀节点刚被访问过，不容易被淘汰。命中长度包括 Host 上的命中。

**队列太长时**：每个请求都要查一次前缀树，开销随队列长度增长。等待队列超过 128 个请求时，`lpm` 和 `hrrn` 默认退回 `fcfs`。当前 SGLang 对 `lpm` 加了"有界 LPM"：判断值得时，只对队首 64 个请求按前缀命中排序，其余部分保持 FCFS。开启 HiCache、SWA、Mamba、session 前缀缓存，或缓存类型不是普通前缀树时，这个功能不启用，仍然退回 FCFS。

**批内前缀共享**：如果等待队列里多个请求有相同的、尚未缓存的开头（≥32 token），只让其中一个先跑，其他的往后排。第一个算完后前缀就进树了，后面的直接命中。

#### 准入时怎么算 KV 显存

- 新请求只按需要新算的部分计费：输入长度减去已命中前缀，再加上预计的输出长度（最多按 4096 估算）。已命中的前缀不重复计费，并且在挑选期间加锁，防止被当成可淘汰空间。
- 还要给正在 decode 的请求预留后续生成所需的空间：剩余输出长度 × `new_token_ratio`。这个比例初始为 `min(0.7 × --schedule-conservativeness, 1.0)`（conservativeness 默认 1.0），没有发生回退时分 600 步线性降到初始值的 14%。调大 conservativeness 更保守，回退少但 batch 小。
- 长输入按 `--chunked-prefill-size` 分块 prefill，同一时间只有一个请求在分块。

#### 和 HiCache 的配合

- 请求的 L3 预取还没完成时，scheduler 跳过它，先调度后面的请求，下一轮再看。
- 命中前缀在 Host 上时，准入阶段先为加载回 GPU 预留显存。预留成功就在同一个 batch 里异步加载；预留失败请求就等待。加载要么全部成功，要么不加载、改为重算。

**显存不够时回退（retract）**：decode 过程中 KV 显存耗尽时，按 `--retraction-policy`（默认 `length`：输出短、输入长的先退）把部分请求退回等待队列，释放它们的 KV，直到剩余请求放得下。至少保留一个请求，连最后一个都放不下时也会中止它；没有主机备份时被回退的请求会以 503 / 500 中止（见 [SGLang PD 分离学习笔记](./SGLang-PD-Disaggregation-Mooncake-Notes.md) 附录二 Q4）。回退后按"已生成 token + 预留步数"占总 `max_new_tokens` 的比例重新估算 `new_token_ratio`，之后的准入更保守。

### 跨实例负载均衡：sgl-router 的路由策略

**路由策略**（`--policy`，默认 `round_robin`；`--chat-routing reorg` 模式下默认 `power_of_two`）：

- 只看负载：`round_robin`、`random`、`power_of_two`（随机挑 2 个，选 prefill 压力小的）、`load_based`（按"排队数 + 运行数"打分）。
- 看缓存：`cache_aware`（缓存亲和，下面详述）、`fused_score`（前缀命中占比和负载加权求和，默认两项都参与）、`score_policy`（同样的融合打分，再加一层 prefill 准入；`power_of_two`、`cache_aware` 也用这层准入）。
- 其他：`sticky`（按请求头里的 key 固定发到同一实例）、`session_aware`。
- 还能叠加过滤器：`prefix_cache` 去掉命中占比太低的实例，`overloaded` 去掉在途请求过多的实例。

**路由器怎么知道每个实例缓存了什么**：当前的 sgl-router 不再像早期版本那样在路由器里用请求文本模拟一棵"近似前缀树"。它订阅每个 SGLang 实例发出的 KV 事件（实例需开启 `--kv-events-config`）：实例的前缀树每存入或删除一个 block，就通过 ZMQ 发一条 `BlockStored` / `BlockRemoved`。路由器据此维护一张按 block hash 索引的表，所以知道的是实例实际的缓存状态。路由器的模型里分 GPU、Host、本地盘、外部存储四层，但 SGLang 目前只发 GPU 和 Host 两层的事件，所以路由器不知道 block 是否在 L3。（这张表实际是一棵按 block hash 链组织的前缀树。）（可选的 `--cache-pending-prefix-ttl-ms` 会在事件确认前先把刚派出去的前缀记到对应实例上。）另一种来源是查询外部的 KV 索引服务。负载信息（排队请求数、排队中待算 token 数、KV 使用率、预计 prefill 排队时间）通过另一个 ZMQ 通道上报（SGLang 实例侧参数 `--load-publish-endpoint`，需同时开 `--kv-events-config`）。

#### cache_aware 的选择过程

1. 算出每个实例能命中多少 token。命中少于 1024 token 的实例不算候选，这是"值不值得追缓存"的门槛。候选数为健康 prefill 实例数的 5%（向上取整），并限制在 8 到 32 个之间、不超过实例总数，按命中多少排序。
2. 过滤：排队请求超过上限的实例去掉（需配置 `--worker-queue-limit`），KV 空间放不下这个请求的、运行请求数加 1 会超过 `max_running_requests` 的也去掉。
3. 排序：比较每个候选还需要新算多少 token。差距超过 1024 token 时，新算得少的胜出。差距不大时比负载：如果命中最多的实例排队待算的 token 比备选多 1024 以上且多出 50%，就改选备选。这一步防止热门前缀把一个实例压垮。
4. 没有任何候选时，退回 power-of-two 按负载选。

#### PD 分离时

- prefill 实例由 `--policy` 选，用 `cache_aware` 时就是按 KV 命中选。
- decode 实例由 `--decode-policy` 选（默认 `power_of_two`），只看排队数、运行数和 KV 使用率，不看前缀命中。原因是 decode 实例的 KV 由 prefill 实例传过来，不依赖它本地的缓存。
- 路由器给两边下发同一份 bootstrap 信息（prefill 地址、端口和一个房间号），两边据此建立 KV 传输连接。
- prefill 池和 decode 池分别通过 k8s 标签发现（匹配的是 Service 上的标签，路由器监听 EndpointSlice）；开 `--pd-version-group-label` 时同一版本的 prefill 只配同一版本的 decode。没有 prefill/decode 比例的自动调节，两个池各有多少实例由部署决定。

### sgl-router 的流量划分：分桶、SLO、会话亲和

除了按缓存命中和负载选实例，sgl-router 还能按请求特征把流量划给不同的实例组：

- **按请求长度和 SLO 分桶**：`--bucket-config` 把实例分成多个桶，每个桶声明能处理的输入长度范围、最大上下文，以及预估的 TTFT 和吞吐。请求先按长度筛出放得下的桶，再按 SLO 排序依次尝试，一个桶满了就试下一个。
  - 请求可以通过请求头 `x-sgl-ttft-slo-ms` / `x-sgl-tps-slo` 带上自己的延迟目标。bucket-config 里可以分别为 TTFT 和 TPS 设置 `slo_first` 或 `best_effort`（默认 `disabled`）。对带 SLO 请求头的请求，`slo_first` 先试能满足目标的桶；`best_effort` 先试不承诺满足该目标的桶，把达标的桶留在后面。不带 SLO 请求头的请求只按桶的 rank 排序。
  - 桶能否满足 SLO 是按配置里写的静态预估值判断的，路由器不实时测量延迟，也没有 TPOT 目标。

- **DP 感知**：`--dp-aware` 时路由器还会选实例内部的 DP rank（默认选在途请求最少的）。
- **会话亲和**：`session_aware` 和 `sticky` 把同一会话固定发到同一实例，提高多轮对话的缓存命中；`balanced` 模式（需 `--chat-routing reorg`）在备选实例负载明显更低时允许换实例：负载差距超过 2 倍，同时绝对差超过门槛（按 prefill token 比较时为 1024）。

### 集群级请求准入

**sgl-router 没有的**：全局限流（令牌桶、最大并发数）、路由器侧排队、按租户或 API key 的配额、请求优先级。一个路由器只服务一个模型，多个模型要各起一套。

**sgl-router 有的**：基于实例负载的准入，所有阈值默认不开启。

- 默认路由模式下：`--worker-queue-limit`（实例排队请求数达到上限就不再往它派）、`--bucket-config` 中每个桶的 `max_pending_prefill_tokens`（实例排队中待算 token 的上限）、`--filter overloaded`（路由器侧在途请求数上限）。
- `--chat-routing reorg` 模式下更全：`--max-inflight-requests`、`--max-kv-usage`（KV 使用率上限）、`--max-running-usage`、`--max-waiting-requests`、`--max-pending-prefill-tokens`。
- 这些检查只读实例上报的负载，不预占容量；负载数据缺失或过期时默认放行。
- 所有候选实例都不满足时，直接返回 503，不在路由器排队。
- 超时与重试：请求默认超时 300 秒；默认不重试（`--retry-max-attempts 1`），开启后换一个没试过的实例重试，且只在还没给客户端返回任何内容时才重试；客户端断开时路由器通知实例中止请求。

#### Mooncake Store 侧

- **多租户配额**：开 `--enable_multi_tenants` 后，每个租户有独立的 key 空间和内存配额（YAML 文件或 etcd 配置，可通过管理 API 在线修改）。写入超出配额直接拒绝（`TENANT_QUOTA_EXCEEDED`），不会为它腾空间，由调用方重试；另有后台淘汰线程按租户水位清理。总配额超过集群容量时按比例缩小，节点下线后也会重新按比例计算。要共享 KV 的实例必须用同一个 `tenant_id`。
- **内存池满**：写入直接失败（`NO_AVAILABLE_HANDLE`），同时触发后台淘汰，不阻塞等待。
- **队列背压**：SSD offload 队列（每个本地盘段默认 5 万）满了时 master 改为强制淘汰；promotion 队列（全局默认 5 万）满了就拒绝新任务。
- 没有对 put/get 的限流。

### Mooncake Conductor：全局前缀索引

Mooncake 没有请求调度器，只有 Conductor 这个"全局前缀索引"，只回答"哪个实例缓存了多少"，不做路由决策。

- **作用**：订阅各推理实例（SGLang、vLLM）和 Mooncake Store master 发出的 KV 事件，维护一张全局表："每个 block 在哪些实例上，在哪一层"。层分为 GPU、本机 CPU、共享 CPU（Mooncake 内存池）、磁盘。
- **查询**：路由器把请求的 token 发给 Conductor，Conductor 对每个实例沿前缀 hash 链往下查，返回每个实例在每一层能命中多少 token。
- **不做的事**：不跟踪负载、不打分、不选实例、不转发请求，这些都留给调用它的路由器。当前的 sgl-router 也没有接入 Conductor，用的是自己订阅的 KV 事件。Mooncake 自带的 PD 示例代理用的是轮询。
- **默认**：HTTP 端口 13333，RPC 端口 13334，每个上下文最多记录 20 万个 block，超出后淘汰最旧的到 90%。编译时需要 `-DWITH_CONDUCTOR=ON`。

Mooncake 论文（FAST'25）里描述的 Conductor 会综合缓存命中、排队时间和 KV 传输开销来估算 TTFT 选 prefill 实例，还会复制热点 KV、过载时提前拒绝请求。这些在开源代码里都没有实现，只实现了其中的前缀命中查询。

### Mooncake 数据放置的负载均衡

这里均衡的是 KV 数据的存放位置，不是请求：

- **写入选位置**：`allocation_strategy` 默认随机选内存段，并优先选写入方本机的段；也可选 `free_ratio_first`（优先空闲比例高的段，内存更均衡）、`local_first`（优先本机），此外还有 `cxl`、`ssd_free_ratio_first`。同一对象的多个副本放在不同段上。
- **读取选副本**：优先本机，其次是与网卡拓扑匹配的远端副本。这是按就近选，不按负载选。
- **热点复制**：`dynamic_replication_mode` 可设为 `off`（默认）、`observe`、`enforce`。按设计，`enforce` 下 10 秒窗口内访问超过 0.8 QPS 的对象会增加内存副本，最多 2 个，用来分散热点读压力。
- 不会迁移已有数据做再平衡。

## 14. 部署示例与调优

### 最小部署：SGLang + Mooncake 作 L3

第 1 步：启动 Mooncake master（自带元数据服务）：

```bash
mooncake_master --enable_http_metadata_server=true --http_metadata_server_port=8080 \
  --eviction_high_watermark_ratio=0.95
```

master 的 RPC 端口默认 50051，监控端口默认 9003。跨机器访问元数据服务时（Mooncake 0.3.14 及以上），元数据服务、所有 SGLang 进程和 store 服务要设置相同的 `MC_METADATA_HTTP_TOKEN`；可信网络里也可以用 `MC_METADATA_HTTP_ALLOW_INSECURE=1`。注意这个 token 检查只在独立的 Python 元数据服务（`mooncake.http_metadata_server`）里有，`mooncake_master` 内置的元数据服务（上面第 1 步）没有。

第 2 步：（可选）单独起存储服务贡献内存。不起的话，由 SGLang 进程自己贡献内存（`global_segment_size` 默认 4 GB）：

```bash
python -m mooncake.mooncake_store_service --config=store.json --port=8081
```

`store.json` 示例：`{"local_hostname":"<本机IP>","metadata_server":"http://<master IP>:8080/metadata","master_server_address":"<master IP>:50051","protocol":"rdma","device_name":"","global_segment_size":"4gb","local_buffer_size":0}`

第 3 步：启动 SGLang：

```bash
python -m sglang.launch_server --model-path <模型路径> --tp 8 --page-size 64 \
  --enable-hierarchical-cache --hicache-ratio 2 \
  --hicache-mem-layout page_first_direct --hicache-io-backend direct \
  --hicache-write-policy write_through --hicache-storage-prefetch-policy timeout \
  --hicache-storage-backend mooncake \
  --hicache-storage-backend-extra-config '{"master_server_address":"<master IP>:50051","local_hostname":"<本机IP>","metadata_server":"http://<master IP>:8080/metadata","global_segment_size":"100gb","protocol":"rdma","device_name":""}'
```

也可以用环境变量代替 extra-config：`MOONCAKE_MASTER`、`MOONCAKE_TE_META_DATA_SERVER`（元数据服务地址）、`MOONCAKE_PROTOCOL`、`MOONCAKE_DEVICE`、`MOONCAKE_GLOBAL_SEGMENT_SIZE`、`MOONCAKE_LOCAL_HOSTNAME`、`MOONCAKE_TENANT_ID`。优先级：extra-config（其中包含 `master_server_address` 或 `client_server_address` 时才生效）> 配置文件（`SGLANG_HICACHE_MOONCAKE_CONFIG_PATH`）> 环境变量。例外：`local_hostname` 以环境变量 `MOONCAKE_LOCAL_HOSTNAME` 为准，其次是 `LOCAL_HOSTNAME`。

第 4 步：开 SSD offload 时在 extra-config 里加 `"enable_ssd_offload": true`，并设环境变量 `MOONCAKE_OFFLOAD_FILE_STORAGE_PATH`（SSD 目录，由 Mooncake 直接读取），master 侧开 `--enable_offload`。注意：用 extra-config 配置时 SGLang 不读 `MOONCAKE_ENABLE_SSD_OFFLOAD` 这个环境变量，只取它的默认值（关闭）。

PD 分离部署时，官方最佳实践给了两种配法：只在 prefill 实例上开 HiCache；或者再在 decode 实例上开异步写出（`--disaggregation-decode-enable-offload-kvcache`）。

### 调优要点

- **协议用 `rdma`**：SGLang 内嵌 Mooncake 时 `MOONCAKE_PROTOCOL` 默认就是 `rdma`；但独立部署的 `mooncake_client` 和 Mooncake 自带的 Python 配置默认是 `tcp`，要显式配置。`device_name` 留空会自动发现网卡，也可以写成 `"mlx5_0,mlx5_1"`（用 `ibv_devices` 查看）。
- **布局和 io-backend 成对配置**：`page_first` 配 `kernel`，`page_first_direct` 配 `direct`。Mooncake 后端的常规路径不支持 `layer_first`。用 `direct` 时建议设 `SGLANG_ENABLE_MLP_SYNC_METADATA_FILL=1`。
- **L2 要比 L1 大**：L2 太小时，从 L3 预取回来的数据没地方放，监控里 `storage_prefetch_unfulfilled_tokens_total{reason="host_capacity"}` 会上涨。大显存卡跑小模型时，L2 默认 2 倍可能占太多内存，要调小 `--hicache-ratio` 或直接用 `--hicache-size`。
- **预取策略**：生产推荐 `timeout`。
- **master 淘汰水位**：文档示例用 0.95；分配失败多时（内存碎片导致还没满就分配不了）调低。
- **大页内存**：设 `MC_STORE_USE_HUGEPAGE=1`、`MC_STORE_HUGEPAGE_SIZE=2MB` 并预先用 `sysctl -w vm.nr_hugepages=...` 分配好；开了就必须够用，不会回退到普通页。Mooncake 仓库有脚本 `scripts/check_hicache_hugepage_requirements.py` 估算需要多少。
- **容器里运行**：加 `--ipc=host --ulimit memlock=-1` 和足够大的 `--shm-size`；RDMA 注册内存可能需要 root 权限。
- **注册内存上限**：eRDMA 等环境对能注册给网卡的内存总量有上限。L2 整块和 `global_segment_size` 都要注册，超限时调小其中之一。

## 15. 效果与适用场景

### 公开的测试结果

Mooncake 仓库有一份 SGLang HiCache 的测试（只有图表，没有给出具体数字）：

- **负载**：多轮对话，每一轮的输入都包含前面所有轮次的输入和输出。
- **对比四种配置**：只用 GPU；GPU + L2；GPU + L2 + Mooncake；以及提前把 Mooncake 填满的情况。指标是首 token 延迟（TTFT）、输入 token 吞吐和每轮的缓存命中率。
- **环境**：一组是 3 台各 2 张 A10、2 × 100 Gbps eRDMA 的机器，跑 Qwen3-14B TP2；另一组是 1 台 8 张 H800 的机器，跑 Qwen3-235B TP8。
- **结论**：
  - prefill 性能：提前填满的 Mooncake > GPU + L2 + Mooncake > GPU + L2 > 只用 GPU。
  - 前 1～3 轮大家的命中率一样，GPU + L2 反而比加了 Mooncake 稍快，因为不需要远程读取。这是多一层带来的开销。
  - 对话越来越长、KV 超出 L2 后，L2 命中率下降、TTFT 上升；加了 Mooncake 的配置命中率保持较高，TTFT 增长缓慢。
  - 收益来自 L3 的集群级容量，以及实例之间共享 KV。

另有一份 PD 分离的测试：KV 传输峰值带宽约 164 GB/s（线速的 82%），32K token 的请求里 KV 传输只占 TTFT 的 2.4%。

### 什么场景收益大

- **多轮对话、Agent**：每轮都带着之前的全部上下文，前缀重复率高，而且总量很快超过单机 GPU 和 L2。
- **长系统提示词、长文档问答、RAG**：很多请求共享同一段长前缀（同一份提示词或同一批文档）。
- **多个实例共享热门前缀**：一个实例算过的 KV 写进 L3，其他实例直接读取。
- **实例重启或扩容后**：新实例可以直接从 L3 读到已有的 KV，不用从零开始预热。

### 什么场景收益小或有额外开销

- **请求之间几乎没有共享前缀**（每个请求都是全新的短输入）：缓存基本不命中，备份到 L2/L3 只是额外开销。可以考虑 `write_through_selective`，只备份被复用过的前缀。
- **工作集不大、L2 就能放下**：加 L3 只会多一次远程读取，比 L2 稍慢。
- **网络慢（没有 RDMA，只能走 TCP）**：从 L3 读回来可能比重新计算还慢，尤其是小模型。
- **很短的命中前缀**：少于预取门槛（默认 256 token）不会去 L3 取，少于 10 个 token 也不会从 L2 加载，直接重算。

## 16. 监控与排查

### SGLang 侧（启动时加 `--enable-metrics`，Prometheus 格式）

- **命中情况**：
  - `sglang:cache_hit_rate`：前缀缓存总命中率。
  - `sglang:cached_tokens_total{cache_source}`：按来源分的命中 token 数，`device` / `host` / `storage` 分别对应 L1 / L2 / L3（`total` 只在没有分来源数据时作为兜底出现，不是三者之和）。看各级各贡献了多少命中，主要看它。

- **L2 使用量**：`sglang:hicache_host_used_tokens` / `sglang:hicache_host_total_tokens`。
- **L3 读写**：
  - `sglang:prefetched_tokens_total`（从 L3 读回的 token 数）、`sglang:backuped_tokens_total`（写到 L3 的 token 数）。
  - `sglang:prefetch_bandwidth` / `sglang:backup_bandwidth`：每次读写的带宽分布。
  - `sglang:storage_prefetch_hit_tokens_total`：L3 查询时报告能命中的 token 数。

- **命中了但没用上**：`sglang:storage_prefetch_unfulfilled_tokens_total{reason}`，原因共 12 种，常见的有：
  - `host_capacity`：L2 没空间放，说明 L2 太小。
  - `deadline`：预取超时，没读完就开始算了，说明 L3 读太慢或超时设得太短。
  - `below_threshold`：命中长度不到预取门槛。

- **失败**：`sglang:hicache_storage_backup_failed_tokens_total`（写 L3 失败）、`sglang:hicache_backup_dropped_tokens_total`（buffer 模式下备份被准入控制丢弃或源数据已失效）。
- SGLang 自带的 Grafana 面板只有命中率一项，HiCache 相关指标需要自己加面板。

### Mooncake 侧

- **master**：端口 9003，`/metrics` 是 Prometheus 格式，`/metrics/summary` 是可读摘要，另有 `/health`、`/ha_status`。常看：
  - 容量：`master_allocated_bytes` / `master_total_capacity_bytes`（内存池用了多少）。
  - key 数量和在线 client 数：`master_key_count`、`master_active_clients`。
  - 淘汰：`master_evicted_key_count`、`master_evicted_size_bytes`；分配失败次数也在摘要里。

- **client**：默认不开监控接口，需要单独开启（如 store 服务设 `MOONCAKE_ENABLE_CLIENT_HTTP_SERVER=true`）。可看到与 master 的心跳状态、读写延迟等。SGLang 进程内嵌的 Mooncake client 怎么开监控，没有找到文档，SGLang 代码里也没有开启它的地方。
- **现成面板**：Mooncake 仓库的 `monitoring/` 目录有 docker-compose，一条命令起 Prometheus（9090）和 Grafana（3000），自带 master 和核心指标的面板。

### 常见问题的排查思路

- **L3 命中率低**：先看 `cached_tokens_total{cache_source="storage"}` 是否有值；再确认共享的实例模型名、TP、页大小、KV 数据类型、`tenant_id` 是否一致（key 不同就不会命中）；再看 master 的淘汰量是否很大（容量不够）。
- **TTFT 没有改善**：看 `unfulfilled{reason="deadline"}` 是否很多（L3 读太慢），确认实际协议是 `rdma`，没有被环境变量或独立 `mooncake_client`（默认 `tcp`）改成 `tcp`。
- **写入失败多**：看 master 的分配失败次数和使用率，必要时加内存或调低淘汰水位。

## 17. 大规模集群部署

### 能否部署到大集群

能，但两部分的成熟度不同：

- **SGLang 推理侧**：有多机部署方案。单个模型实例可以跨机做 TP/EP（如 Llama 405B 跨 2 机 TP16，DeepSeek 大规模 EP），多个实例组成 PD 分离集群。文档里给了 k8s 上用 LWS（LeaderWorkerSet）和 RBG（RoleBasedGroup）部署 DeepSeek PD 的例子。96 张 H100 跑 DeepSeek、128 张 H200 跑 Kimi K2 这类规模只在外部博客里有，仓库文档里没有完整配置。
- **Mooncake Store**：数据在 client 之间直接传，master 只管元数据，数据面能横向扩展。但仓库里没有写明支持多少节点。公开的 benchmark 大多是 2 到 3 台机器，最大的一份是 vLLM 集成文档里提到的 60 张 GPU。元数据由单个 master 管理，不分片；Transfer Engine 的元数据服务，小规模可以用 P2P 握手，大规模或长期运行建议用 etcd 或 Redis。

### 扩缩容与高可用

#### SGLang 推理实例

- **扩容**：有两种方式。一是 k8s 服务发现（`--service-discovery`，按 Service 标签选择，PD 模式分别用 `--prefill-selector` / `--decode-selector`），新 Pod 就绪后路由器自动接入，并从它的 `/model_info`（退回 `/server_info`）读出模型和 PD 信息。二是 HTTP 管理接口 `POST /workers`、`PUT /workers/{id}`、`DELETE /workers/{id}`（2026-11-21 加入，需配置 `--worker-management-api-key`，修改时带 `If-Match` 版本号）。只用 `--worker-urls` 静态配置、又不开管理接口时，实例列表在启动时就固定了。
- **缩容**：Pod 被移除时，路由器立即不再给它派新请求，并清掉它的 KV 缓存状态；已经发出的请求继续跑完。路由器不主动排空实例，优雅退出靠 k8s 先把 Pod 标成未就绪，以及实例自己的退出处理。
- **故障**：没有主动健康探测，用熔断器：连续失败 3 次就熔断，30 秒后放一个请求试探。实例返回 503 / 429 / 500 算作中性结果，不计入失败。
- **路由器自身**：路由器无状态，可以多副本部署在负载均衡后面，每个副本独立订阅实例的 KV 事件和负载信息。新副本可以从已运行的副本拷贝一份 KV 状态再上线（peer bootstrap），避免冷启动时缓存命中判断不准。session 绑定保存在各副本内存里，多副本时前面的负载均衡要按 session 头做粘性。

#### Mooncake Store

- **扩容**：起一个新 client 挂载它的内存段即可，master 自动纳入分配。
- **缩容/故障**：client 每秒向 master 发心跳。超过 10 秒（`client_active_ttl_sec`）没有心跳，master 先把它标为疑似失联；再过 20 秒（`client_suspicion_ttl_sec`）仍未恢复，才判为下线，然后卸载它的内存段，并删除这些段上的副本。默认从断联到卸载约 30 秒。数据只在其他节点还有副本时才保留，系统不会自动补副本。有"优雅卸载"接口（等待一段宽限期再卸载），但不会把数据迁到其他节点。对 KV cache 来说，丢数据只意味着下次要重算，不影响正确性。
- **master 高可用**：默认单 master，是单点。开 `--enable_ha` 后用 etcd（或 k8s lease、实验性的 Redis）选主，备 master 通过操作日志（OpLog，需 `--enable_oplog=true`）和快照（需 `--enable_oplog_snapshot`）保持同步（两项默认都关闭；只有 etcd 后端做完整的主备复制，k8s lease 只做选主），主挂了由备接管，client 收到提示后重新挂载内存段。etcd 后端的主节点租约 `ha_leader_lease_ttl_sec` 默认 5 秒，切换总时长没有文档说明。
- **k8s**：只提供了普通 Deployment/Service 示例（1 个 master + 3 个 store），以及与 RBG、llm-d 集成的文档，没有 Helm chart 或 Operator。

### 总结与缺口

- 可以上大集群：推理侧有 k8s（LWS/RBG）方案和多机 TP/EP/PD，KV 存储侧数据面可扩展。
- 扩缩容：推理实例靠 k8s 服务发现或路由器的管理接口接入/摘除；Mooncake 节点可以随时加入，下线时数据直接丢弃，不迁移、不补副本。
- 准入和调度：有基于负载的准入、按长度/SLO 分桶、PD 分池，但没有全局限流、租户级请求配额、优先级排队，也没有根据实时延迟调整路由的闭环。Mooncake 论文里的集群级调度（按 TTFT 预估选实例、热点复制、过载提前拒绝）在开源代码里都没有实现。
- 单点和规模风险：Mooncake 默认单 master、元数据不分片，需要开 HA；仓库内没有大规模压测数据。

## 18. 与其他方案的对比

### LMCache

LMCache 是一个独立的 KV cache 服务，最早主要和 vLLM 配合使用，自己管理 CPU 内存、本地盘、远程存储等多级存储。

- **在 SGLang 里的用法**：`--enable-lmcache`。SGLang 保留自己的前缀树作为索引，把 L2 以下的存储全部交给一个独立的 LMCache 进程管理，KV 从 LMCache 直接加载到 GPU。
- **和 HiCache 互斥**：不能同时开 `--enable-hierarchical-cache`。可以理解为：要么用 SGLang 自己的 HiCache（L2 + 一个 L3 后端，比如 Mooncake），要么把多级存储整体外包给 LMCache。

### vLLM + Mooncake

Mooncake 也能接 vLLM，走的是 vLLM 的 KV connector 接口，有两种：

- `MooncakeConnector`：只做 PD 分离时 prefill → decode 的 KV 传输（RDMA）。
- `MooncakeStoreConnector`：把 Mooncake Store 当成多个 vLLM 实例共享的分布式 KV 池，按 block hash 做前缀共享，支持卸载到 CPU / 磁盘。

### 怎么理解它们的关系

- **Mooncake** 在两个引擎里都是"传输层 + 共享存储层"，放在引擎自己的缓存管理下面。在 SGLang 里是 HiCache 的一个 L3 后端；在 vLLM 里是一个 KV connector。
- **SGLang HiCache** 负责 GPU、Host 两级和前缀树索引，L3 可以换后端（Mooncake、3FS、本地文件、NIXL 等）。
- **LMCache** 是一整套外部缓存服务，在 SGLang 里替代 HiCache 的 L2 及以下部分。
- 前缀索引方式不同：SGLang 用前缀树（radix tree），vLLM 用按固定大小 block 的 hash 表。效果上都能做前缀复用，SGLang 的前缀树更适合分叉多的场景（如多轮对话、Agent 的多分支）。

## 19. 关键参数默认值

- **SGLang 容量与格式**：`--mem-fraction-static` 自动计算（80 GB 卡上通常在 0.85 左右或更低）、`--kv-cache-dtype auto`、`--page-size`（CUDA 上默认 1，不少模型和后端会自动改成 64 或 128）、`--hicache-host-memory-fraction 0.8`、`--hicache-storage-key-scheme rank-suffix`。
- **SGLang PD 分离**：`--disaggregation-transfer-backend mooncake`、`--disaggregation-bootstrap-port 8998`、bootstrap 和等待传输超时各 300 秒。
- **SGLang**：`--hicache-write-policy write_through`、`--hicache-storage-prefetch-policy timeout`、`--radix-eviction-policy lru`、`--hicache-ratio`（Host 池相对 GPU 池的大小；不设置时普通模式取 2.0、`buffer_only` 模式取 1.2、只做回退备份的 decode 实例取 0.2，并可能按 `--hicache-host-memory-fraction` 下调）、`--hicache-io-backend kernel`、`--hicache-mem-layout page_first`、`--schedule-policy fcfs`、`--schedule-conservativeness 1.0`、`--retraction-policy length`。
- **sgl-router**：`--policy round_robin`（`--chat-routing reorg` 时为 `power_of_two`）、`--decode-policy power_of_two`、`--request-timeout-secs 300`、`--retry-max-attempts 1`（不重试）、熔断 `--cb-threshold 3` / `--cb-cool-down-secs 30`。
- **Mooncake**：SGLang 里 `MOONCAKE_PROTOCOL` 默认 `rdma`、`MOONCAKE_GLOBAL_SEGMENT_SIZE` 默认 4 GB、`MOONCAKE_TE_META_DATA_SERVER` 默认 `P2PHANDSHAKE`（独立的 `mooncake_client` 默认协议是 `tcp`）；master 参数 `eviction_high_watermark_ratio 0.9`、`eviction_ratio 0.05`、`default_kv_lease_ttl 10000 ms`、`default_kv_soft_pin_ttl 30 分钟`、`enable_offload false`、`offload_on_evict false`、`promotion_on_hit false`、`allocation_strategy random`、`dynamic_replication_mode off`、`enable_ha false`、`client_active_ttl_sec 10`、`client_suspicion_ttl_sec 20`。

## 20. 代码位置

- SGLang（`sglang/python/sglang/srt/` 下）：
  - 存储分层：`mem_cache/`，L3 接口 `mem_cache/hicache_storage.py`，Mooncake 后端 `mem_cache/storage/mooncake_store/`，3FS 后端 `mem_cache/storage/hf3fs/`。
  - 前缀树：`mem_cache/unified_cache/unified_tree_core.py`（`UnifiedTreeNode`）、`mem_cache/unified_cache/components/base.py`（`ComponentData`）。
  - 传输与淘汰：`managers/cache_controller.py`、`mem_cache/unified_radix_cache.py`、`mem_cache/evict_policy.py`。
  - L1 ↔ L2 拷贝：`mem_cache/l2_transfer.py`、`mem_cache/pool_host/`，拷贝 kernel 在 `sglang/python/sglang/kernels/aot/csrc/kvcacheio/transfer.cu`；io-backend 与布局的自动调整在 `arg_groups/hicache_hook.py`。
  - L3 直连：`mem_cache/storage/mooncake_store/mooncake_direct_linker.py`。
  - 计算与传输重叠：按层加载的计数器在 `managers/cache_controller.py`（`LayerDoneCounter`）、`mem_cache/unified_cache/unified_cache_linker.py`（`LayerWiseLoadCounter`）；stream 栅栏设置在 `managers/scheduler.py`；PD 的 KV 发送在 `disaggregation/prefill.py`、`disaggregation/mooncake/conn.py`。
  - 调度：`managers/scheduler.py`、`managers/schedule_policy.py`；KV 事件发布：`mem_cache/events.py`、`disaggregation/kv_events.py`。
  - 参数定义：`arg_groups/fields/memory.py`、`arg_groups/fields/schedule.py`。

- SGLang 其他（`sglang/python/sglang/srt/` 下）：
  - 容量计算：`model_executor/pool_configurator.py`、`mem_cache/kv_cache_configurator.py`、`mem_cache/hicache_auto_size.py`；KV 数据类型：`mem_cache/kv_cache_dtype.py`。
  - L3 key：`mem_cache/utils.py`（hash 种子）、`mem_cache/cpp_utils/hash_binding.cpp`（SHA-256 链式 hash）、`mem_cache/hicache_key_scheme.py`（统一 key 方案）、`mem_cache/storage/mooncake_store/mooncake_store.py`（key 拼接）。
  - 一致性：`mem_cache/kv_weight_version_tracker.py`、`managers/scheduler.py`（`flush_cache`）。
  - PD 分离：`disaggregation/`（`prefill.py`、`decode.py`、`mooncake/conn.py`、`decode_hicache_mixin.py`），参数在 `arg_groups/fields/disagg.py`，超时在 `environ.py`。
  - 特殊场景：`mem_cache/unified_draft_pool.py`（draft KV）、`managers/req_types.py`（多模态 pad 值）、`mem_cache/embedding_cache_controller.py`（embedding 缓存）、`mem_cache/hisparse_memory_pool.py`、`mem_cache/storage/lmcache/`。
  - 监控指标：`observability/metrics_collector.py`。

- sgl-router：`sglang/sgl-router/src/policies/`（`cache_aware.rs`、`admission.rs`），服务发现 `src/discovery/k8s.rs`，分桶 `src/buckets_reorg.rs`，参数 `src/config/cli.rs`；k8s 部署文档 `sglang/docs/docs/references/multi_node_deployment/`。
- Mooncake（`Mooncake/` 下）：
  - 副本类型：`mooncake-store/include/allocator.h`；内存池分配：`mooncake-store/src/common/client_buffer_allocation.cpp`。
  - 淘汰：`mooncake-store/src/master_service.cpp`、`mooncake-store/src/eviction/`；SSD offload：`mooncake-store/src/file_storage.cpp`；参数定义：`mooncake-store/src/master.cpp`。
  - 传输：Transfer Engine 协议在 `mooncake-transfer-engine/src/multi_transport.cpp`、`mooncake-transfer-engine/src/transport/`；Store 读写路径选择在 `mooncake-store/src/transfer_task.cpp`；盘层 I/O 在 `mooncake-store/src/storage_backend.cpp`、`mooncake-store/src/storage/distributed/`；NoF SSD 在 `mooncake-store/src/nof/`。
  - 部署、调优、测试与监控文档：`docs/source/deployment/integrations/sglang/`、`docs/source/performance/sglang/`、`docs/source/getting_started/observability.md`、`monitoring/`；SGLang 侧最佳实践 `sglang/docs/docs/advanced_features/hicache_best_practices.mdx`。
  - Conductor：`mooncake-conductor/`，设计文档 `docs/source/design/conductor/conductor-architecture-design.md`。
  - 节点下线与 HA：`mooncake-store/src/master_service.cpp`（`ProcessClientOffboardingJob`、`GracefulUnmountSegment`）；多租户：`mooncake-store/src/tenant/`、`docs/source/deployment/multi-tenancy.md`；k8s 部署：`docs/source/deployment/kubernetes-deployment-guide/`。
