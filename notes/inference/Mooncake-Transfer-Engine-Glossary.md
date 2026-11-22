# Mooncake Transfer Engine 源码阅读术语手册

中文 | [English](./Mooncake-Transfer-Engine-Glossary_en.md)

- **整理日期**: 2026-11-20
- **范围**: 阅读 Mooncake Transfer Engine（`mooncake-transfer-engine/`）源码需要的硬件、网络、RDMA 和 TE 自身的术语，以及一次 RDMA WRITE 从提交到完成的调用链。
- **代码版本**: [kvcache-ai/Mooncake](https://github.com/kvcache-ai/Mooncake/tree/301261358eef0b13fa55645ccde4a988f1ca7505) main 分支 `30126135`（2026-11-20），[sgl-project/sglang](https://github.com/sgl-project/sglang/tree/94d3dbad27dcb10ca0e83ec5ccac3c87f6c1e0ca) main 分支 `94d3dbad27`（2026-11-13）。第 7、8 节的 `文件:行号` 都对应这两个提交。
- **依据**: 阅读上述两个提交中的代码和 Mooncake 文档，没有实际运行验证。

每个术语给一个通俗解释，多数配一个例子或类比。源码位置只放在第 7、8 节，路径中的 `TE/` 指 `Mooncake/mooncake-transfer-engine/`。

术语后的括号里依次写英文全称和中文译名，格式是 `缩写（英文全称，中文译名）`。一个术语里有多个缩写时，写成 `缩写 = 英文全称，中文译名`。产品名、库名没有通用中文译名，括号里给的是中文说明。MUSA、MACA、CXI、EID 这几个厂商私有缩写找不到可靠出处，没有展开。

## 0. 先看全局

### 0.1 一句话说清 TE 的 RDMA 路径

TE（Transfer Engine，传输引擎）的 RDMA（Remote Direct Memory Access，远程直接内存访问）数据面是**单边**（one-sided）的：发起方自己算好对端内存地址和 rkey，本地网卡把数据直接写进（或读出）对端内存，对端 CPU 不参与，也收不到任何通知。

所以“接收端”要做的事都在传输之前：注册内存、发布元数据、被动接受建连。传输结束后，要靠另外一条消息告诉它“数据到了”。

### 0.2 对象层次

```text
TransferEngine                     对外 API（TE/include/transfer_engine.h）
 └─ TransferEngineImpl             经典实现；设 MC_USE_TENT=1 时改走 TE/tent/
     ├─ TransferMetadata           段描述、握手、notify（元数据面）
     └─ MultiTransport             按对端 protocol 选后端
         ├─ RdmaTransport          RDMA 后端：注册内存、切 slice、选本地网卡
         │   └─ RdmaContext × 每块本地网卡     PD、MR、CQ、WorkerPool、EndpointStore
         │       ├─ WorkerPool               worker 线程：post send + poll CQ
         │       └─ RdmaEndPoint × 每块对端网卡  内含 num_qp_per_ep 个 RC QP
         ├─ TcpTransport
         └─ NvlinkTransport / ShmTransport / ...
```

### 0.3 建议阅读顺序

先读第 3 节（RDMA）和第 4 节（TE 自己的概念），再对照第 7 节的调用链读源码。第 1、2 节遇到不懂的词再查，第 5 节只在用到其他硬件时看。

---

## 1. 硬件与操作系统基础

| 术语 | 解释 |
| --- | --- |
| PCIe（Peripheral Component Interconnect Express，高速外设组件互连） | 服务器内部连接 CPU、GPU、网卡的总线，设备之间搬数据都走它。例：网卡读 GPU 显存时，数据经 PCIe 从 GPU 到网卡，再发到网络上。 |
| PCIe 距离 / PCIe 交换机（PCIe distance / PCIe switch） | 两个设备在 PCIe 树上隔了几跳。挂在同一个 PCIe 交换机下的 GPU 和网卡离得最近，互传最快。例：GPU0 和 mlx5_0 挂在同一个交换机下，GPU0 的数据就该优先走 mlx5_0。 |
| NUMA 节点（Non-Uniform Memory Access node，非一致性内存访问节点） | 多路服务器里每个 CPU 插槽带一组内存。CPU 访问自己那组快，访问另一组要跨插槽，慢。例：插在 node0 上的网卡读 node0 的内存，比读 node1 的快。 |
| DMA（Direct Memory Access，直接内存访问） | 设备自己读写内存，不用 CPU 一个字节一个字节地搬。类比：CPU 只负责下单，设备自己去仓库搬货。 |
| 虚拟地址 / 物理页（virtual address / physical page） | 程序看到的是虚拟地址，数据实际放在物理内存的页上（通常每页 4 KB），由操作系统维护两者的对应关系。设备不认识虚拟地址，所以要事先告诉它这段虚拟地址对应哪些物理页。 |
| 锁页内存（pinned memory / page-locked memory） | 被固定住、操作系统不会换出或挪动的内存。网卡按物理地址读写，页如果中途被挪走，网卡就会读写到错误的位置。例：把 1 GB 内存注册给网卡后，这 1 GB 在注销前一直留在原来的物理位置。 |
| IOVA（I/O Virtual Address，I/O 虚拟地址） | 设备那一侧使用的地址，和程序里的虚拟地址是两套编号，由硬件负责翻译。 |
| GPUDirect RDMA（GDR，GPU 直连 RDMA） | 网卡直接读写 GPU 显存，不经过主机内存中转。例：没有 GDR 时，KV Cache（Key-Value Cache，键值缓存）要先从显存拷到主机内存再发出；有了 GDR，网卡直接从显存读出来发。 |
| nvidia-peermem（NVIDIA peer memory，NVIDIA 对等内存模块） | 一个内核模块，让 RDMA 网卡驱动能注册 GPU 显存。没有它（也没有 dma-buf）时，网卡只能注册主机内存。 |
| dma-buf（DMA buffer sharing，DMA 缓冲区共享） | Linux 让不同设备驱动共享同一块缓冲区的机制。GPU 驱动把显存导出成一个 fd（file descriptor，文件描述符），网卡驱动拿这个 fd 去注册。它是 nvidia-peermem 之外的另一条路。 |
| BAR（Base Address Register，基址寄存器）/ BAR1 | GPU 在 PCIe 地址空间里开的一扇“窗口”，网卡通过这扇窗口访问显存。窗口大小有限，注册的显存太多可能把窗口占满。 |
| PCIe Relaxed Ordering（PCIe 宽松排序） | 允许 PCIe 上的写请求不按发出顺序完成。放松顺序要求后，部分平台写显存会更快。 |
| Data Direct（数据直连） | NVIDIA 部分网卡的功能：网卡在 GPU 所在的 PCIe 分支上多开一个 DMA 入口，读写显存时少绕路。 |
| CUDA IPC 句柄（CUDA = Compute Unified Device Architecture，统一计算设备架构；IPC = Inter-Process Communication，进程间通信） | 同一台机器上，一个进程把自己的一块显存做成“提货单”交给另一个进程，对方凭它直接访问这块显存。例：同机两个推理进程用它在 GPU 之间直接拷 KV。 |
| CUDA VMM（Virtual Memory Management，虚拟内存管理） | CUDA 的一组接口，把“申请物理显存”和“映射到虚拟地址”拆成两步。拆开以后，一块物理显存可以导出给其他进程，甚至其他节点去映射。 |
| fork 安全（fork safety，派生子进程时的安全问题） | 进程 fork 出子进程时，已注册给网卡的内存页可能被复制或改动，导致网卡读写错位。RDMA 库提供了专门的初始化函数来规避。 |

---

## 2. 网络基础

| 术语 | 解释 |
| --- | --- |
| Gb/s 与 GB/s（gigabits / gigabytes per second，吉比特每秒 / 吉字节每秒） | 网卡速率按比特算，程序里通常按字节算，1 字节 = 8 比特。例：400 Gb/s 的网卡最多约 50 GB/s。 |
| 延迟、带宽、在途数据（latency / bandwidth / in-flight data） | 要跑满带宽，路上同时要有足够多的数据，即 BDP（Bandwidth-Delay Product，带宽时延积）= 带宽 × RTT（Round-Trip Time，往返时延）。例：50 GB/s × 10 µs = 500 KB，所以 TE 要切片、开多个连接并行发。 |
| TCP（Transmission Control Protocol，传输控制协议）/ socket（套接字） | 操作系统提供的可靠字节流连接，数据要经过内核拷贝。TE 用它交换建连信息、传小消息；没有 RDMA 网卡时也用它传数据。 |
| RPC 端口（RPC = Remote Procedure Call，远程过程调用） | 进程对外开的一个 TCP 端口，别的进程连上来请求服务。在 TE 里，对端连这个端口来交换建连信息。 |
| epoll（event poll，事件轮询） | Linux 让一个线程同时盯住很多连接或设备的接口，哪个有动静就处理哪个。 |
| asio（Asynchronous I/O，异步 I/O 库） | C++ 的异步网络库：发起读写后不阻塞，数据到了再回调处理。TE 的 TCP 后端用它。 |
| etcd（分布式键值存储） | 专门存配置和元数据的分布式键值数据库：数据同时存在几台机器上，坏掉其中少数几台也能照常工作，所有人读到的都是同一份最新值。Kubernetes 就用它存整个集群的状态。名字来自 Unix 存配置的 `/etc` 目录加 d（distributed，分布式）。在 TE 里它可以当元数据后端。例：各进程初始化时都填 `etcd://10.0.0.1:2379`，把自己的段描述写进去，再按段名查别的进程。 |
| Redis / HTTP 元数据服务（Redis = Remote Dictionary Server，远程字典服务；HTTP = HyperText Transfer Protocol，超文本传输协议） | 和 etcd 作用一样的另外两种元数据后端：各进程把“我是谁、我的内存在哪”写进去，其他进程按名字查。Redis 是常用的内存键值数据库，HTTP 后端是一个按网址存取数据的简单 Web 服务。例：进程 A 以自己的名字为键写入信息，进程 B 按 A 的名字读出来。 |
| ZMQ（ZeroMQ，消息队列库） | 一个轻量的进程间消息库。例：SGLang 的 PD 分离（Prefill-Decode disaggregation，预填充与解码分离部署）里，P 传完 KV 后用 ZMQ 发一条“传完了”给 D。 |
| IB（InfiniBand，无限带宽技术） | 专为 RDMA 设计的一整套网络，网卡、交换机、线缆都是专用的，由子网管理器 SM（Subnet Manager）统一分配地址。 |
| RoCE（RDMA over Converged Ethernet，基于融合以太网的 RDMA）/ RoCEv2 | 在普通以太网上跑 RDMA。RoCEv2 把 RDMA 包装进 UDP（User Datagram Protocol，用户数据报协议）/IP（Internet Protocol，网际协议）包里，因此能像普通 IP 流量一样跨网段路由。数据中心多用 RoCEv2。 |
| LID（Local Identifier，本地标识符） | IB 网络里每个端口的 16 位短地址，由子网管理器分配，相当于子网内的门牌号。RoCE 不用 LID。 |
| GID（Global Identifier，全局标识符）/ GID 表 / GID index（GID 索引） | RDMA 端口的 128 位全局地址，RoCE 下就是网卡 IP 换一种写法。例：IP 10.0.0.1 的 GID 是 `::ffff:10.0.0.1`。一个端口的 GID 表里同一个 IP 常有好几行（RoCEv1、RoCEv2 各一行），GID index 选第几行，选错常常连不上。 |
| GRH（Global Route Header，全局路由头） | 数据包里装着 GID 的那段包头，跨子网路由要靠它。RoCE 的包都带 GRH。 |
| 端口（port） | 网卡上的物理接口。一块网卡有 1 个或 2 个口，编号从 1 开始。 |
| MTU（Maximum Transmission Unit，最大传输单元） | 一个网络包最多装多少数据，RDMA 最大是 4096 字节。例：MTU 为 4096 时，64 KB 的数据会被网卡拆成 16 个包。 |
| PKey（Partition Key，分区键） | IB 网络的“分组号”。只有分区相同的端口才能互相通信，用来隔离不同租户。 |
| SL / TC / DSCP（SL = Service Level，服务等级；TC = Traffic Class，流量类别；DSCP = Differentiated Services Code Point，区分服务码点） | 包上的优先级标记，交换机按它把包放进不同的队列。例：把 RDMA 流量标成某个 TC，交换机就把它放进不丢包的那条队列。 |
| PFC / ECN / DCQCN（PFC = Priority-based Flow Control，基于优先级的流量控制；ECN = Explicit Congestion Notification，显式拥塞通知；DCQCN = Data Center Quantized Congestion Notification，数据中心量化拥塞通知） | RoCE 防丢包、防拥塞的三件套。PFC：交换机队列快满时让上游暂停发送。ECN：交换机在拥塞时给包打标记。DCQCN：接收方看到标记后通知发送方，发送方降速。这些由网卡和交换机配置，程序里一般只体现为优先级设置。 |
| ECMP（Equal-Cost Multi-Path，等价多路径）与 UDP 源端口 | 两台机器之间有多条一样好的路径时，交换机按包头算哈希决定走哪条。RoCEv2 的 UDP 源端口参与哈希，给不同连接设不同的源端口，流量就能分散到不同路径上。 |
| Bonding（网卡绑定）/ LAG（Link Aggregation Group，链路聚合组） | 把网卡的两个物理口绑成一个逻辑口，带宽叠加，坏了一个口另一个还能用。 |
| Rail（轨道） | 多网卡集群的一种接法：每台机器的第 i 块网卡都接到同一组交换机上，这一组叫第 i 条 rail。例：所有机器的 mlx5_0 在 rail 0，mlx5_1 在 rail 1。TE 源码里说的 rail 指“本地某块网卡到对端某块网卡”这条路径。 |
| 多网卡（multi-NIC；NIC = Network Interface Card，网络接口卡） | 一台 GPU 服务器常配 4～8 块高速网卡，数据可以同时从多块网卡发出，带宽叠加。例：每块 400 Gb/s 网卡约 50 GB/s，8 块合计约 400 GB/s。 |

---

## 3. RDMA 与 verbs 编程（最重要）

RDMA 的编程接口叫 **verbs**（动词接口），库是 libibverbs（属于 rdma-core），函数前缀 `ibv_` 就是 InfiniBand Verbs 的缩写。NVIDIA（Mellanox）网卡另有扩展接口 `mlx5dv_`（mlx5 Direct Verbs，mlx5 直通动词接口）。

**例子**：进程 A 要把本地 1 MB 数据写进进程 B 的显存：

1. B 把这块显存注册成 MR，拿到 rkey，再把显存地址和 rkey 告诉 A。
2. A 把自己存数据的内存也注册成 MR，拿到 lkey。
3. A 和 B 各建一个 QP，交换 QP 编号后把两个 QP 配成一对。
4. A 往 QP 里放一个 WR（“把本地这 1 MB 写到 B 的这个地址，钥匙是这个 rkey”），然后按门铃通知网卡。
5. 网卡写完后往 CQ 里放一条完成记录，A 取出来，就知道写完了。B 的 CPU 全程不参与。

### 3.1 基本对象

| 术语 | 解释 |
| --- | --- |
| HCA / RNIC / 设备名（HCA = Host Channel Adapter，主机通道适配器；RNIC = RDMA-enabled NIC，支持 RDMA 的网卡） | 都指支持 RDMA 的网卡。IB 网络里叫 HCA，以太网里叫 RNIC。Linux 下名字形如 `mlx5_0`、`mlx5_1`。 |
| mlx5（Mellanox 网卡驱动名） | NVIDIA（原 Mellanox）RDMA 网卡在 Linux 上的驱动名，mlx 就是 Mellanox 的缩写。ConnectX-4 及之后的型号（ConnectX-5、6、7 等）都用这个驱动，更早的 ConnectX-3 用 mlx4，所以数字 5 和网卡型号无关。驱动按顺序给网卡起名 `mlx5_0`、`mlx5_1`……，`mlx5dv_` 开头的函数是这个驱动独有的扩展接口。例：装了 8 块 ConnectX-7 的机器，通常能看到 `mlx5_0` 到 `mlx5_7`。 |
| `ibv_context`（device context，设备上下文） | 程序“打开”一块网卡后拿到的句柄，之后在这块网卡上的操作都要带着它。类比：打开文件得到的文件句柄。 |
| PD（Protection Domain，保护域） | 一个分组容器。内存区域和连接必须在同一个 PD 里才能配合使用，防止连接访问不属于它的内存。 |
| MR（Memory Region，内存区域） | 告诉网卡“这段内存你可以读写”。注册时内核把页锁住，网卡记下地址对应关系，并返回两把钥匙 lkey 和 rkey。例：注册一块 1 GB 的显存后，网卡就能直接读写这 1 GB。 |
| lkey（local key，本地密钥）/ rkey（remote key，远程密钥） | 访问已注册内存的两把钥匙：本机网卡用 lkey，远端机器用 rkey，rkey 要事先交给对方。类比：rkey 像交给对方的门禁卡，没有它，对方的网卡进不了这块内存。同一块内存在每块网卡上各注册一次，每块网卡给的钥匙都不同。 |
| 访问权限（access flags） | 注册内存时声明允许做什么：本地写、远端读、远端写。例：只开本地写，远端就读写不了这块内存。 |
| QP（Queue Pair，队列对） | RDMA 里的“连接”，由一个发送队列 SQ（Send Queue）和一个接收队列 RQ（Receive Queue）组成。两台机器各出一个 QP 配成一对才能通信。类比：一条专线电话。 |
| RC / UD（RC = Reliable Connection，可靠连接；UD = Unreliable Datagram，不可靠数据报） | QP 的两种类型。RC 类似 TCP：一对一、保证送达、按顺序，丢包由网卡硬件重传。UD 类似 UDP：能发给任何人，但不保证送达。传 KV 这类大数据都用 RC。 |
| QPN（Queue Pair Number，队列对编号） | QP 的编号，建连时双方要交换。例：A 想连 B，就得知道 B 那边 QP 的编号。 |
| WR / WQE（WR = Work Request，工作请求；WQE = Work Queue Element，工作队列元素） | WR 是程序交给网卡的一张“工单”：做什么（读、写、发消息），用本地哪块内存，写到对端哪个地址，带哪把钥匙。驱动把它翻译成网卡能直接执行的 WQE，放进发送队列。 |
| SGE（Scatter/Gather Element，分散/聚集元素） | 工单里描述本地内存的一行：起始地址、长度、lkey。一张工单可以列好几行，网卡会把这几段内存拼起来发出去。 |
| post send（提交发送）/ doorbell（门铃） | post send 是把工单放进发送队列；放完后写一下网卡的寄存器通知它开工，这一下叫按门铃。函数马上返回，不等数据传完。 |
| wr_id（work request ID，工作请求标识） | 工单上的自定义编号，网卡做完后原样带回，程序靠它认出是哪张工单完成了。例：程序可以把记录这次传输的对象地址填进去。 |
| CQ / CQE / WC（CQ = Completion Queue，完成队列；CQE = Completion Queue Entry，完成队列条目；WC = Work Completion，工作完成记录） | 网卡每做完一张工单，就往 CQ 里放一条完成记录 CQE（程序读出来的结构叫 WC），写明成功还是失败。程序要自己去 CQ 里取（poll）。类比：快递的签收回执。 |
| signaled / unsignaled（要回执 / 不要回执） | 每张工单可以选择完成后要不要回执，少要回执能省开销。例：连发 16 张工单只让最后一张回执，看到它就知道前 15 张也做完了，因为 RC 按顺序完成。 |
| inline（内联） | 很小的数据直接写进工单里，网卡不用再去内存读一次。例：几十字节的控制消息适合内联发送。 |
| 队列深度（queue depth） | 一个队列最多同时挂多少张没做完的工单，挂满了就要等前面的完成。例：发送队列深度是 256，最多就有 256 张工单同时在途。 |
| 完成通道（completion channel） | CQ 有新回执时主动通知程序的机制，程序可以睡着等，不用一直去查。代价是唤醒有延迟，所以追求低延迟的程序常用忙轮询代替它。 |
| 异步事件（async event） | 网卡主动报告的状态变化，和具体哪张工单无关。例：网线被拔掉、端口恢复、网卡出现致命错误。 |

### 3.2 操作语义

| 术语 | 解释 |
| --- | --- |
| 单边（one-sided） | READ/WRITE 只需要发起方动手，对方 CPU 不参与，也不知道数据被读写了。类比：你有对方仓库的门禁卡，自己进去放货或取货，仓库管理员并不知情。 |
| 双边（two-sided） | SEND/RECV 需要双方配合：接收方先备好接收缓冲区（post recv），发送方的消息到达后，接收方会收到一条回执。类比：寄挂号信，对方要签收。 |
| RDMA WRITE（RDMA 写） | 把本机内存的数据直接写进远端内存。例：Prefill 节点把算好的 KV 直接写进 Decode 节点的显存。 |
| RDMA READ（RDMA 读） | 把远端内存的数据直接读到本机。例：从存储节点把一份缓存的 KV 拉到本机。 |
| max_rd_atomic / max_dest_rd_atomic（max outstanding RDMA Read & Atomic，最大在途读与原子操作数） | 一个连接上最多同时有几个 READ 在等对方回数据。READ 要等对端把数据送回来，这个数太小，READ 就跑不满带宽。 |
| RNR（Receiver Not Ready，接收端未就绪） | SEND 的消息到了，接收方却还没备好接收缓冲区，网卡会等一会儿再重发。只发生在双边操作里。 |

### 3.3 QP 状态机与建连

| 术语 | 解释 |
| --- | --- |
| RESET → INIT → RTR → RTS（RESET，复位；INIT = Initialized，已初始化；RTR = Ready To Receive，可接收；RTS = Ready To Send，可发送） | QP 从创建到能用要走四步：RESET 是刚创建；INIT 绑定网卡端口和访问权限；RTR 填上对端的地址和 QP 编号，从此能收；RTS 设好超时和重传次数，从此能发。类比：开通专线要先装好线路（INIT），再登记对方号码、可以接听（RTR），最后才能拨出（RTS）。 |
| ERR 状态（Error，错误状态） | 连接出错后进入的状态。进入 ERR 后，队列里没做完的工单全部作废，这个 QP 只能重建。 |
| 带外交换（OOB = Out-Of-Band，带外） | RDMA 连接建好之前还不能用 RDMA 通信，所以要先借另一条通道（通常是 TCP）交换 GID、QP 编号这些建连信息。类比：先打普通电话互报专线号码，再开通专线。TE 用自己的 TCP 握手做这件事，不用 rdma_cm（RDMA Connection Manager，RDMA 连接管理器）库。 |
| PSN（Packet Sequence Number，包序列号） | 每个包的序号，接收方靠它发现丢包和乱序。建连时双方约定起始序号。 |
| ah_attr（Address Handle attributes，地址句柄属性）/ AV（Address Vector，地址向量） | 建连时填写的“怎么找到对方”：对方的 GID、走本机哪个端口、用什么优先级。类比：快递单上的收件地址。 |
| timeout（超时）/ retry_cnt（retry count，重传次数） | 发出的包等多久没收到确认 ACK（Acknowledgement，确认）就重发，以及最多重发几次。例：超时约 67 ms、最多重发 7 次，全失败后连接进入 ERR。 |

### 3.4 常见完成错误码（看日志时用）

| 错误码 | 通常的原因 |
| --- | --- |
| `IBV_WC_SUCCESS`（成功） | 工单正常完成。 |
| `IBV_WC_RETRY_EXC_ERR`（Retry Exceeded Error，重传次数超限） | 重发次数用完还没收到确认。常见原因：对端机器或进程挂了、网络不通、GID 选错。 |
| `IBV_WC_REM_ACCESS_ERR`（Remote Access Error，远端访问错误） | 对端拒绝访问。常见原因：rkey 不对、地址超出对端注册的范围、对端已经注销了这块内存。 |
| `IBV_WC_LOC_PROT_ERR`（Local Protection Error，本地保护错误）/ `IBV_WC_LOC_LEN_ERR`（Local Length Error，本地长度错误） | 本地这边的问题：本地内存没注册、lkey 不对，或者长度越界。 |
| `IBV_WC_WR_FLUSH_ERR`（Work Request Flushed Error，工作请求被冲刷） | 连接已经坏了，排在后面的工单被批量作废。它是结果而不是原因，要往前找第一条不是 FLUSH 的错误。 |

---

## 4. Mooncake TE 自己的概念

### 4.1 对外 API

| 术语 | 解释 |
| --- | --- |
| TransferEngine（传输引擎） | 用户使用的入口。用法分四步：初始化、注册内存、打开对端、提交传输并查结果。 |
| 经典 TE 与 TENT（Transfer Engine NEXT，下一代传输引擎） | TE 现在有两套实现。默认用经典实现，设环境变量 `MC_USE_TENT=1` 才切到 TENT。读源码建议先读经典实现。 |
| Segment（段） | 一个进程对外公开的“可被远端读写的内存集合”，用一个全局唯一的名字标识，每个进程一个。例：Decode 进程的段名是 `10.0.0.2:15123`，里面包括它注册的所有 KV 显存。 |
| 段名（segment name） | 段的名字。P2PHANDSHAKE（peer-to-peer handshake，点对点握手）模式下就是 `IP:端口`，别人凭它就能找到你。 |
| SegmentID（段 ID）/ SegmentHandle（段句柄） | 打开一个对端段后，本进程给它的编号，之后提交传输用编号代替段名。例：打开 `10.0.0.2:15123` 得到编号 1；编号 0 永远指自己。 |
| Buffer（缓冲区） | 段里的一块已注册内存，每注册一次就多一个 buffer。例：一个进程注册了一块 KV 显存和一块主机内存，它的段里就有 2 个 buffer。 |
| location（内存位置） | 一块 buffer 在哪个设备上，用字符串表示。例：`cpu:0` 是 NUMA 节点 0 的内存，`cuda:3` 是 3 号 GPU 的显存，`*` 表示让 TE 自己探测。TE 按它挑离得最近的网卡。 |
| remote_accessible（允许远端访问） | 注册内存时选择是否允许别人读写。只用作发送源的内存可以不开放。 |
| TransferRequest（传输请求） | 一次传输的描述：读还是写、本地地址、对端段编号、对端地址、长度。例：“WRITE，本地地址 X，段 1，对端地址 Y，1 MB”表示把本地 X 处的 1 MB 写到段 1 的 Y 处。注意 Y 是对端进程里真实的虚拟地址。 |
| Batch（批次）/ BatchID（批次 ID）/ BatchDesc（batch descriptor，批次描述符） | 把多个请求打包，一起提交、一起查进度，BatchID 是这个包的编号。例：一层 KV 拆成 100 个请求，放进一个 batch 一次提交。 |
| TransferStatus（传输状态） | 查询结果：等待中、已完成、失败、超时等。只要有一片数据失败，整个请求就算失败。 |
| 提交与轮询（submit / poll） | 提交只是把任务交出去，函数马上返回；之后要反复查状态，直到完成。Python 接口里的“同步传输”就是提交后替你一直查到完成。 |
| 完成事件 fd（completion eventfd，完成事件文件描述符） | 轮询之外的另一种等法：传输完成时 TE 往一个 fd 里写一下，程序睡在这个 fd 上，被叫醒后再取结果，省掉反复查询的 CPU。 |
| Notify（通知） | TE 自带的小消息功能。单边写完成后，接收方并不知道数据到了，发送方可以再发一条通知告诉它。例：P 写完 KV 后，发一条“请求 42 已传完”给 D。 |

### 4.2 元数据与握手

| 术语 | 解释 |
| --- | --- |
| TransferMetadata（传输元数据） | TE 里负责“谁在哪、内存在哪、怎么连”的模块：发布自己的信息、查询对方的信息、建连握手、收发通知。 |
| SegmentDesc（segment descriptor，段描述符） | 一个段的“说明书”：段名、协议、有哪些网卡、有哪些 buffer、内存和网卡怎么对应。对端拿到这份说明书，才知道往哪写、带哪把钥匙。 |
| DeviceDesc（device descriptor，设备描述符） | 说明书里描述一块网卡的部分：网卡名、LID、GID。 |
| BufferDesc（buffer descriptor，缓冲区描述符） | 说明书里描述一块 buffer 的部分：位置、起始地址、长度，以及它在每块网卡上的 lkey 和 rkey。例：一块 buffer 注册到了 4 块网卡上，就有 4 个 rkey。 |
| 元数据后端（metadata backend）/ conn string（connection string，连接字符串） | 说明书存在哪。可以是 etcd、Redis、HTTP 这样的中心服务；也可以选 P2PHANDSHAKE，不设中心，谁需要就直接连到对方去要。例：SGLang PD 分离用的是 P2PHANDSHAKE。 |
| 发布（publish） | 注册内存后，把更新后的说明书放到元数据后端，让别人查得到。 |
| metacache（metadata cache，元数据缓存） | 把查到的对端说明书在本地缓存起来，不用每次传输都去查。对端新注册了内存时缓存会过期，要重新拉。 |
| 握手（handshake） | 建 RDMA 连接前，双方通过 TCP 交换网卡地址和 QP 编号，内容是 JSON（JavaScript Object Notation，JavaScript 对象表示法）。例：A 说“我的 QP 是 101、102”，B 回“我的是 201、202”，双方再把各自的 QP 推进到 RTS。 |
| 握手 daemon（handshake daemon，握手守护线程） | 每个 TE 进程后台开着的一个 TCP 服务，专门应答别人的建连、查说明书、发通知等请求。 |
| 主动方 / 被动方（active / passive） | 发起握手的是主动方，应答的是被动方。通常是要发数据的一方先发起。 |
| ready ack（ready acknowledgement，就绪确认） | 握手的最后一步：双方的 QP 都设好后，主动方再发一条确认，双方都确认之后才开始在这个连接上发数据。这样可以避免一方已经开始发、另一方的 QP 还没准备好。 |
| NIC path（网卡路径） | 用“段名@网卡名”唯一标识某个进程的某块网卡。例：`10.0.0.2:15123@mlx5_2`。 |

### 4.3 拓扑与选网卡

| 术语 | 解释 |
| --- | --- |
| Topology（topology matrix，拓扑矩阵） | 一张表：每种内存位置首选哪些网卡、其次可以用哪些网卡。例：`cuda:0` 首选 mlx5_0，备选 mlx5_1、mlx5_2。 |
| preferred_hca / avail_hca（preferred / available HCA，首选网卡 / 可用网卡） | 首选网卡是离这块内存最近的网卡：对 GPU 是 PCIe 距离最近的，对主机内存是同 NUMA 节点的。其余网卡都是可用网卡，首选的出问题时才用。 |
| 选网卡策略（NIC selection） | 先从首选网卡里随机挑一块；失败重试时按“先首选、后备选”的顺序依次换。例：GPU0 首选 mlx5_0，mlx5_0 出错后改用 mlx5_1。 |
| 本地网卡 / 对端网卡（local NIC / peer NIC） | 每片数据要选两块网卡：本机从哪块发，对端用哪块收。本地按源数据的位置挑，对端按目的内存的位置挑。例：从本机 GPU0 写到对端 GPU5，本地选 GPU0 旁边的网卡，对端选 GPU5 旁边的网卡。 |
| device_id（设备下标）/ buffer_id（缓冲区下标） | 网卡编号和 buffer 编号。“第几块 buffer 在第几块网卡上的钥匙”就靠这两个编号查表。 |

### 4.4 RDMA 后端内部对象

| 术语 | 解释 |
| --- | --- |
| Transport（传输后端） | 一种传输方式的实现。RDMA、TCP、NVLink 各有一个。 |
| MultiTransport（多传输后端管理器） | 总调度：看对端段用什么协议，就把请求交给对应的后端。例：对端是 `rdma` 段，就交给 RDMA 后端。 |
| protocol（协议） | 段用什么方式访问，例如 `rdma`、`tcp`、`nvlink_intra`。 |
| RdmaTransport（RDMA 传输后端） | 负责注册内存、把请求切片、为每片选本地网卡。 |
| RdmaContext（RDMA 上下文） | 一块本地网卡的“管家”，管着这块网卡上的所有资源：注册的内存、完成队列、连接、工作线程。有几块网卡就有几个 RdmaContext。 |
| RdmaEndPoint（RDMA endpoint，RDMA 端点） | 本机某块网卡到对端某块网卡的连接，里面通常有 2 个 QP 并行使用。例：本机 mlx5_0 到对端 mlx5_2 是一个 endpoint。 |
| EndpointStore（端点缓存） | 存放已建好的连接，按 NIC path 查找。连接太多时淘汰不常用的，默认淘汰算法叫 SIEVE（比 LRU（Least Recently Used，最近最少使用）更简单的一种算法，SIEVE 是名字不是缩写），也可以选 FIFO（First In, First Out，先进先出）。 |
| 懒建连（lazy connection setup） | 连接第一次用到时才建。所以和某个对端的第一次传输会多花一次握手的时间。 |
| WorkerPool（工作线程池）/ worker 线程（工作线程） | 每块网卡配几个后台线程，循环做两件事：把排队的数据片交给网卡，去完成队列取回执。 |
| TransferTask（传输任务） | 一个请求在 TE 内部的进度记录：切成了几片、完成几片、失败几片、传了多少字节。 |
| Slice（切片） | 请求被切成的小块，每块对应一张 RDMA 工单。例：1 MB 的请求按 64 KB 切成 16 片，分给多个连接和网卡并行发。 |
| slice_size（切片大小）/ fragment_limit（尾片合并阈值） | 最后剩下的一小截如果不太大，就和前一片合在一起发，避免出现很碎的尾片。例：切片 64 KB、阈值 16 KB 时，剩下的 70 KB 不再切成 64 KB + 6 KB，而是一次发 70 KB。 |
| markSuccess（标记成功）/ markFailed（标记失败） | 一片数据完成或失败时调用，更新任务的计数。所有片都结束后，任务的状态才确定。 |
| 重试 / 重新分派（retry / redispatch） | 某片失败后，TE 自己换一块网卡或换一条路径重发，有次数上限。它和网卡硬件的重发是两层：硬件重发应对偶尔丢包，TE 重试应对网卡或链路坏掉。 |
| rail 暂停 / context 暂停（rail pause / context pause，路径暂停 / 网卡暂停） | 某条网卡到网卡的路径短时间内连续出错，就先停用一段时间，期间改走别的路径。例：连续出错 5 次，就暂停这条路径 30 秒。整块本地网卡坏了，就停用整块网卡。 |
| auto GID（GID 自动选择） | 不手动指定 GID index 时，TE 自己从 GID 表里挑最可能连通的一行，连不通再换下一行。 |
| rdma_twosided（two-sided RDMA，双边 RDMA） | 另一种 RDMA 后端，用 SEND/RECV 传数据，带 credit（信用）流控：接收方先给发送方额度，发送方只能在额度内发。 |
| 自适应拥塞控制（adaptive congestion control） | 根据网络反馈自动调节同时在途的数据量：网络通畅就多发，开始拥塞就少发。默认不开启。 |

---

## 5. 其他 Transport（用到再查）

| protocol | 解释 |
| --- | --- |
| `tcp` | 走普通 TCP，任何网络都能用，但数据要经过内核拷贝，比 RDMA 慢得多。适合开发测试，或者没有 RDMA 网卡的环境。 |
| `shm`（shared memory，共享内存） | 同一台机器上的进程之间通过共享内存直接拷贝，不经过网卡。用到 POSIX（Portable Operating System Interface，可移植操作系统接口）共享内存和 mmap（memory map，内存映射）。 |
| `nvlink_intra`（intra-node NVLink，节点内 NVLink） | 同一台机器内的 GPU 之间通过 NVLink（NVIDIA 的 GPU 高速互连）直接拷贝显存，比走网卡快得多。 |
| `nvlink`（跨节点 NVLink） | MNNVL（Multi-Node NVLink，多节点 NVLink）：像 GB200 NVL72 这样，多台机器的 GPU 用 NVLink 连成一体，跨机也能直接拷显存。 |
| `nvmeof` | 直接读写 NVMe（Non-Volatile Memory Express，非易失性存储器高速接口）固态盘上的文件。NVMe-oF（NVMe over Fabrics，基于网络的 NVMe）指通过网络访问远端盘；GDS（GPUDirect Storage，GPU 直连存储）让盘和显存直接传，不经过主机内存。 |
| `cxl` | CXL（Compute Express Link，计算快速链路）内存：通过 CXL 接入的外接内存，可以被多台机器共享，读写方式和本地内存一样。 |
| `efa` | AWS 云上的 EFA（Elastic Fabric Adapter，弹性结构适配器）网卡。它不支持 RC，用自己的 SRD（Scalable Reliable Datagram，可扩展可靠数据报）协议，通过 libfabric（OFI = OpenFabrics Interfaces，开放网络结构接口）编程。 |
| `cxi` | HPE Slingshot 网络的网卡（芯片代号 Cassini），也通过 libfabric 编程。 |
| `hip` | AMD GPU 的同机传输，用 HIP（Heterogeneous-computing Interface for Portability，可移植异构计算接口）在 GPU 之间拷贝。相关名词：ROCm（AMD 的 GPU 软件栈），KFD（Kernel Fusion Driver，内核融合驱动，AMD GPU 的内核驱动）。 |
| `ascend` | 华为昇腾 NPU（Neural Processing Unit，神经网络处理器）的传输，基于 HCCL（Huawei Collective Communication Library，华为集合通信库）等接口。 |
| `ubshmem` / kunpeng | 华为鲲鹏的 UB（Unified Bus，统一总线）互连，编程接口叫 URMA（Unified Remote Memory Access，统一远程内存访问）。jetty 相当于 RDMA 的 QP，JFC（Jetty For Completion）相当于 CQ，EID 相当于 GID。 |
| `musa` / `maca` / `hylink` / sunrise_link | 分别是摩尔线程、沐曦、海光 DCU（Deep Computing Unit，深度计算单元）、Sunrise 各自的 GPU 互连。海光的工具包叫 DTK（DCU Toolkit，DCU 工具包），互连叫 HSL（Hygon Scale-up Link，海光纵向扩展互连）。 |
| `barex` | 官方文档称为 Bare-metal RDMA extension（裸金属 RDMA 扩展），基于 RDMA 网卡。 |
| `nccl` / `flagcx` | 借用 NCCL（NVIDIA Collective Communications Library，NVIDIA 集合通信库）或 FlagCX（FlagOS 的跨厂商通信库）的点对点收发来传数据。 |

---

## 6. 源码里常见的并发与工程写法

| 术语 | 解释 |
| --- | --- |
| 原子操作（`std::atomic`，atomic operation） | 不会被其他线程“插一半”的读写。例：两个线程同时给计数器加 1，用原子加法结果一定是 2，普通加法可能只加了 1。 |
| 内存序（memory_order） | 规定一个线程写的数据何时能被另一个线程看到。例：A 写完数据后用 release 写一个标志，B 用 acquire 读到这个标志，就一定能看到 A 写的数据。relaxed（宽松）不保证这一点，seq_cst（sequentially consistent，顺序一致）最严格。 |
| `__atomic_*` / `__sync_*` | GCC（GNU Compiler Collection，GNU 编译器套件）提供的原子操作函数，作用和 `std::atomic` 一样，可以直接用在普通变量上。 |
| `volatile`（易变限定符） | 告诉编译器每次都真的去内存读写这个变量，不要优化掉。它不保证线程安全，所以源码里都和原子函数一起用。 |
| 自旋锁 / 读写锁（RWSpinlock，read-write spinlock，读写自旋锁） | 自旋锁拿不到锁时原地空转，不去睡眠，适合锁只占很短时间的场景。读写锁允许多个读者同时进入，写者独占。例：查连接表的线程很多、改表的很少，就适合用读写锁。 |
| 缓存行 / 伪共享（cache line / false sharing） | CPU 缓存按 64 字节一块读写。两个线程各改各的变量，但两个变量恰好在同一块里，就会不停地让对方的缓存失效，程序变慢。例：把两个线程各自的计数器隔开 64 字节存放，就能避免。 |
| 线程局部对象池（thread_local object pool） | 每个线程自己留一批用过的对象，下次直接复用，省掉频繁的分配和释放。例：每秒要创建几十万个切片对象时，这样做很划算。 |
| 忙轮询（busy polling） | 线程不停地主动查“有没有完成”，不睡眠。延迟最低，代价是一直占着一个 CPU 核。 |
| 引用计数 / pin（reference count） | 记录“还有几个人在用这个对象”，计数归零前不许释放。例：回调还在读一个批次的数据时，别的线程不能把这个批次删掉。 |
| 条件编译（conditional compilation，`#ifdef`） | 编译时按开关决定包含哪段代码。例：没有 AMD GPU，就不编译 HIP 相关的代码。读源码时，先跳过和自己硬件无关的分支。 |
| 返回值风格（return convention） | 老接口返回整数，0 表示成功，负数是错误码；新接口返回一个 Status 对象，里面带错误类型和说明。 |

---

## 7. 把术语串起来：一次 RDMA WRITE 的调用链

以 SGLang PD 分离为例：Prefill（发送端）把 KV Cache 用 RDMA WRITE 写进 Decode（接收端）的显存。

### 7.1 准备阶段（两端都要做）

1. **初始化**：`TransferEngine::init(conn_string, local_server_name, ...)` 安装 RdmaTransport（`rdma_transport.cpp:350`）：为每块网卡建 RdmaContext（打开设备、建 PD 和 CQ、起 worker 线程），起握手 daemon，发现拓扑并发布本地段描述。
2. **注册内存**：`registerLocalMemory(addr, len, "cuda:0")` → `RdmaTransport::registerLocalMemory`（`rdma_transport.cpp:511`）→ 在每块网卡上 `ibv_reg_mr` 或 `ibv_reg_dmabuf_mr`（`rdma_context.cpp:893-901`）→ 把 `BufferDesc{addr, len, lkey[], rkey[]}` 加进本地段描述并发布（`rdma_transport.cpp:1088`）。
3. **交换地址**：上层把接收端 buffer 的虚拟地址告诉发送端（SGLang 通过 bootstrap 消息里的 `dst_kv_ptrs` 传递）。TE 本身不管这一步。

### 7.2 发送端

1. **打开对端段**：`openSegment("decode_ip:port")` 拿到对端 SegmentDesc（网卡 GID、各 buffer 的 rkey）和本地 SegmentID。
2. **提交**：`allocateBatchID` + `submitTransfer(batch, [{WRITE, src, sid, dst_addr, len}])`
   - `TransferEngine::submitTransfer`（`transfer_engine.cpp:987`）判断是否走 TENT；
   - → `TransferEngineImpl`（`transfer_engine_impl.h:143`）→ `MultiTransport::submitTransfer`（`multi_transport.cpp:572`），`selectTransport` 按 protocol 选中 RdmaTransport；
   - → `RdmaTransport::submitTransferTask`（`rdma_transport.cpp:1840`）：选本地网卡、切 slice、填 lkey、按网卡分组；
   - → `RdmaContext::submitPostSend`（`rdma_context.cpp:1822`）→ `WorkerPool::submitPostSend`（`worker_pool.cpp:790`）：选对端网卡，填 rkey 和 peer NIC path，放进 worker 队列。
3. **发出**：worker 线程 `performPostSend`（`worker_pool.cpp:1084`）按 NIC path 取 endpoint，没有就新建并握手（`setupConnectionsByActive`，`rdma_endpoint.cpp:666`；QP 经过 INIT → RTR → RTS，`:1569`）
   - → `RdmaEndPoint::submitPostSendLimited`（`rdma_endpoint.cpp:1329`）：每个 slice 填一个 `ibv_send_wr`（`wr_id` = slice 指针），分配到各个 QP，调用 `ibv_post_send`（`:1430`）。
4. **网卡干活**：本地网卡把数据从本地显存 DMA 出来发到网络上；对端网卡用 rkey 校验地址和权限，直接 DMA 写进对端显存，回 ACK。
5. **收完成**：本地 CQ 出现 CQE → `performPollCq`（`worker_pool.cpp:1438`）→ `slice->markSuccess()`（`:1531`）；失败则重试，重试用尽就 `markFailed`。
6. **查结果**：调用方 `getTransferStatus` / `getBatchTransferStatus` 看到 COMPLETED。

### 7.3 接收端

- **被动建连**：握手 daemon 收到 Connection 请求 → `RdmaTransport::onSetupRdmaConnections`（`rdma_transport.cpp:2278`）→ `setupConnectionsByPassive`（`rdma_endpoint.cpp:1029`），建好本端 QP 并回复自己的 QPN。
- **数据到达**：接收端 CPU 不参与，TE 也不会产生任何回调。
- **得知完成**：发送端看到 COMPLETED 后另发一条消息。SGLang 用 ZMQ 推送状态（`sglang/python/sglang/srt/disaggregation/common/conn.py:895`）；也可以用 TE 的 notify。

---

## 8. 常用环境变量速查

配置结构体在 `TE/include/config.h:52`（`GlobalConfig`），解析在 `TE/src/config.cpp`。

| 变量 | 默认值 | 作用 |
| --- | --- | --- |
| `MC_SLICE_SIZE` | 65536 | slice 大小（字节） |
| `MC_FRAGMENT_RATIO` | 4 | `fragment_limit = slice_size / ratio`，即默认 16 KB |
| `MC_NUM_QP_PER_EP` | 2 | 每个 endpoint 的 QP 数 |
| `MC_MAX_WR` | 256 | 每个 QP 的 SQ 深度 |
| `MC_MAX_CQE_PER_CTX` | 4096 | 每个 CQ 的容量 |
| `MC_WORKERS_PER_CTX` | 2 | 每块网卡的 worker 线程数 |
| `MC_MAX_SGE` / `MC_MAX_INLINE` | 4 / 64 | WR 的 SGE 上限 / inline 上限 |
| `MC_MTU` | 4096 | 路径 MTU（再与端口实际 MTU 取较小值） |
| `MC_GID_INDEX` | 自动 | GID 表下标 |
| `MC_IB_PORT` | 1 | 网卡端口号 |
| `MC_IB_TC` / `MC_IB_SL` | 不设 | 流量类别 / 服务等级 |
| `MC_RETRY_CNT` | 9 | slice 的软件层重试次数 |
| `MC_RDMA_SIGNAL_INTERVAL` | 1 | 每几个 WR 产生一个 CQE |
| `MC_RDMA_WORKER_IDLE_SPIN_US` | 100000 | worker 空闲后忙等多久再睡（微秒） |
| `MC_RDMA_RAIL_PAUSE_SECONDS` | 30 | 出错路径的暂停时长 |
| `MC_MAX_EP_PER_CTX` | 65536 | 每块网卡最多缓存的 endpoint 数 |
| `MC_ENDPOINT_STORE_TYPE` | SIEVE | endpoint 淘汰算法（SIEVE / FIFO） |
| `MC_MIN_RPC_PORT` / `MC_MAX_RPC_PORT` | 15000 / 17000 | 握手端口的随机范围 |
| `MC_DISABLE_METACACHE` | 不设 | 关闭远端段描述缓存 |
| `MC_USE_TENT` | 不设 | 改用 TENT 引擎 |
| `MC_LOG_LEVEL` | INFO | 日志级别 |
