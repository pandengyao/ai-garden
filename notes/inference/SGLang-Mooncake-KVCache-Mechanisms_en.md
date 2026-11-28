# KV Cache Mechanisms in SGLang and Mooncake: Storage Tiers, Data Movement, Eviction, Transfer and Scheduling

[中文](./SGLang-Mooncake-KVCache-Mechanisms.md) | English

- **Compiled**: 2026-11-28
- **Scope**: The KV cache storage tiers of SGLang HiCache (L1 GPU, L2 Host, L3 external storage) and Mooncake Store: capacity estimates, the radix tree, L3 keys and sharing, data movement, eviction, transfer methods, overlap of compute and transfer, PD disaggregation, request scheduling and load balancing, deployment tuning, monitoring and large-scale deployment, plus the hardware and network basics they rely on.
- **Code versions**: [sgl-project/sglang](https://github.com/sgl-project/sglang/tree/0d311f2508d8cbdb1d5f9b804a1f39310264f5d1) main branch `0d311f2508` (2026-11-28, including sgl-router), [kvcache-ai/Mooncake](https://github.com/kvcache-ai/Mooncake/tree/ab2595576a0b6469bea1fb7e12476937eb949dc5) main branch `ab259557` (2026-11-28).
- **Basis**: Reading the code at the two commits above, the SGLang and Mooncake docs, and the 3FS README; nothing was verified by actually running it.

For details of Transfer Engine and PD disaggregation, see the [Mooncake Transfer Engine Study Notes](./Mooncake-Transfer-Engine-Notes_en.md) and the [SGLang PD Disaggregation Study Notes](./SGLang-PD-Disaggregation-Mooncake-Notes_en.md).

## 1. Overview of the Storage Tiers

SGLang has 3 tiers of its own (L1 GPU, L2 Host, L3 external storage). Mooncake is one of the L3 backends, and inside it splits again into a memory pool and a disk tier. Together that makes 4 levels end to end:

1. GPU memory
2. Local Host DRAM (CPU memory)
3. Mooncake distributed memory pool (DRAM by default, can also be configured as GPU memory)
4. Mooncake disk tier (SSD / disk / distributed file system)

SGLang has no concept of L4: L3 can use only one backend at a time, and what people call "level 4" is Mooncake's internal disk tier, which from SGLang's point of view still belongs to L3.

How many levels are actually used depends on the configuration. SGLang needs hierarchical caching turned on (`--enable-hierarchical-cache`) with mooncake chosen as the storage backend; Mooncake needs offload turned on or disk replicas configured before level 4 takes effect. If L3 uses 3FS instead, there are only 3 levels (GPU → L2 → 3FS).

The typical path of one piece of KV: computed on the GPU → backed up to local L2 (immediately, under the default write policy) → written to the Mooncake memory pool → (with offload on) landed on SSD. When another instance meets the same prefix, it reads from Mooncake into its own L2, then copies to the GPU.

## 2. Network and Hardware Basics

The transfer sections later use many hardware and protocol terms. This section first explains them in terms of "which devices the data moves between, over which links, and who moves it".

### What the Inside of a GPU Server Looks Like

```text
GPU0 ══ GPU1 ══ … ══ GPU7        ← between GPUs: NVLink (high-speed in-machine link)
 │  each GPU has its own HBM memory (L1)
 │  PCIe
PCIe Switch ──── NIC ────→ data center network (switches) ────→ other servers
 │  PCIe
CPU ──── DRAM memory (L2)
 │  PCIe
NVMe SSD (local disk)
```

- A typical 8-GPU server: 8 GPUs, CPUs and memory, several NICs (commonly 1 GPU paired with 1 NIC), and a few NVMe SSDs.
- GPUs, NICs and SSDs all connect to the CPU over **PCIe**. Many machines also have a **PCIe Switch** (a PCIe switching chip) in between, which hangs several GPUs and one NIC under the same Switch.
- GPUs are also directly connected by **NVLink**, which does not go over PCIe.
- Across machines, the only way is through the NIC over the network (except for new models with cross-machine NVLink).

### Speed Ranges of Each Link

The numbers vary a lot between hardware generations; only orders of magnitude are given here, for comparison:

- GPU memory (HBM): about 2~8 TB/s per GPU.
- NVLink: about 900 GB/s total (bidirectional) between each H100 and the other GPUs.
- PCIe 5.0 x16: about 64 GB/s one way; PCIe 4.0 x16 about 32 GB/s. Copies between the GPU and Host memory are limited by this.
- NIC: commonly 200 Gbps or 400 Gbps. Note that NICs are measured in **bits** (b) while storage and memory are measured in **Bytes** (B); 1 Byte = 8 bit, so 400 Gbps ≈ 50 GB/s. 8 NICs at 400G total about 400 GB/s.
- One NVMe SSD: reads at about 7~14 GB/s, with latency of tens to over a hundred microseconds.
- Latency ranges: GPU memory access in nanoseconds; one PCIe or RDMA transfer a few microseconds; TCP tens of microseconds; an SSD read tens to over a hundred microseconds.

So the lower a KV cache tier is, the larger and cheaper it is, but the lower its bandwidth and the higher its latency.

### In-Machine Interconnects: PCIe, NVLink, CXL

- **PCIe**: The standard bus in a server that connects the CPU and devices (GPU, NIC, SSD). "x16" means 16 lanes, and "4.0 / 5.0" is the generation; each generation doubles the bandwidth. Moving KV between GPU memory and Host memory (L1 ↔ L2) goes over PCIe.
- **PCIe Switch**: A PCIe switching chip. When a GPU and a NIC under the same Switch exchange data, the data can pass only through the Switch without detouring to the CPU, so the path is shorter and faster. This is why Mooncake "picks NICs by topology": for each GPU or block of memory it picks the NIC closest to it.
- **NUMA**: In a multi-socket server, each CPU has its own nearby memory, and accessing memory under the other CPU crosses an inter-CPU link and is somewhat slower. When allocating Host memory, try to keep it on the same NUMA node as the NIC and GPU.
- **NVLink / NVSwitch**: NVIDIA's dedicated interconnect between GPUs, with several times the bandwidth of PCIe (H100 has about 7 times PCIe 5.0 x16). It is usually only inside one machine. **MNNVL** (Multi-Node NVLink, as in the GB200 NVL72 rack) extends NVLink across machines, and Mooncake's `nvlink` protocol uses it.
- **CXL**: A new interconnect standard on the PCIe physical interface. It can attach memory expansion cards and even let several machines share one memory pool. Mooncake's `cxl` protocol and allocation strategy are for this kind of memory.

### Who Moves the Data: CPU, SM, DMA

For the same "copy a block of data from A to B", the result differs a lot depending on who does it:

- **CPU memcpy**: A CPU core runs read and write instructions to do the copy. It is the most general, but it uses the CPU, and its speed is limited by CPU memory bandwidth. When the docs say "one more memcpy", they mean one more copy of this kind.
- **GPU SM copy**: A copy kernel is launched on the GPU and the GPU's compute units (SMs) do the reads and writes. SGLang's `kernel` io-backend is this kind. It is flexible and can move many scattered small blocks at once, but it uses SMs that would otherwise run the model.
- **DMA (direct memory access)**: Devices have dedicated copy circuits (the GPU's copy engines, NICs and SSD controllers all have them). The CPU or GPU only issues the command "move N bytes from address X to address Y", and the copy itself uses no compute resources. SGLang's `direct` io-backend, RDMA and NVMe reads and writes are all DMA underneath.

### Memory Terms

- **Pinned memory (page-locked memory)**: The OS normally can swap memory pages to disk or move them, and if a page moves during a device DMA, things break. Once memory is "pinned", its physical address is fixed, and only then can the GPU and NIC DMA to it directly. The cost is that the system cannot reclaim this memory. SGLang's L2 is pinned by default.
- **Memory registration**: RDMA, SPDK and others require a block of memory to be "registered" with the NIC or driver first: the memory is pinned and the virtual-to-physical address mapping is given to the device, after which the device can read and write it directly. Registration is slow, so SGLang (in the default embedded Mooncake client mode) registers the whole L2 with Mooncake once at startup and reuses it afterwards. Some environments cap the total amount that can be registered (such as Alibaba Cloud eRDMA).
- **Hugepage**: Normal memory pages are 4 KB; hugepages are 2 MB or 1 GB. The larger the page, the smaller the address translation tables, so device access is faster and registration is easier. SPDK requires hugepage memory, and Mooncake can also turn hugepages on.
- **Page cache**: By default, Linux file reads and writes go through a cache in the kernel first. Repeated reads are fast; the downside is one more copy and the memory it takes. **O_DIRECT** is an option when opening a file that bypasses the page cache and reads and writes the disk directly, but it requires the addresses and lengths to be block-aligned.
- **User space / kernel space**: Normal programs run in user space; reading files and sending or receiving network packets go through system calls into kernel space, where the kernel does the work. Each switch and each copy inside the kernel has a cost. "Kernel bypass" technologies, such as RDMA, SPDK and 3FS's USRBIO, let user programs talk to the hardware directly and save these costs.

### Cross-Machine Networking: TCP and RDMA

**TCP**: The most common way to communicate over a network; programs send and receive data through sockets. Sending a piece of data goes like this:

1. The program calls `send`, and the data is copied from program memory into the kernel's socket buffer.
2. The kernel protocol stack splits the data into packets, adds headers and hands them to the NIC to send.
3. The peer NIC receives them and hands them to the peer kernel, which copies them into the peer program's memory.

The CPUs on both ends are involved, there are at least two extra copies, latency is tens of microseconds, and a single connection can hardly saturate a 200G/400G NIC. The upside is that it works on any network and needs no special hardware.

**RDMA (Remote Direct Memory Access)**: The NIC reads and writes registered memory on another machine directly.

1. Both sides first register memory with their own NIC and exchange "memory address + access key (rkey)".
2. The initiator tells its local NIC "write this block of my memory to the peer's address Y" (RDMA write) or "read the data at the peer's address Y into here" (RDMA read).
3. The two NICs complete the transfer between themselves, and the data lands directly in the target memory.

The whole process bypasses the kernels on both ends, **the peer CPU is not involved at all**, there are no extra copies, latency is a few microseconds, and it can saturate the NIC bandwidth. Operations started by one side alone like this are called **one-sided operations**; **two-sided operations** (send/recv) require the peer program to prepare a receive buffer in advance, similar to TCP send and receive, but still bypass the kernel. Mooncake's `rdma` protocol uses one-sided operations; `rdma_twosided` also moves data with one-sided operations, and only adds a two-sided (send/recv) control channel to carry notifications.

**Implementations of RDMA**: RDMA is a capability that needs NIC and network support, and there are several implementations:

- **InfiniBand (IB)**: A network designed for high-performance computing, with its own NICs and switches. It supports RDMA natively and has the lowest latency.
- **RoCE (RDMA over Converged Ethernet)**: RDMA over ordinary Ethernet. The NIC must support RoCE, and the switches must be configured to be lossless (PFC/ECN and other flow control), or performance drops quickly. Common in data centers in China.
- **Cloud vendors' RDMA**: AWS **EFA**, Alibaba Cloud **eRDMA** and others. EFA does have an ibverbs driver, but it supports only SRD/UD transport, not regular RC connections, and is usually used through **libfabric**, so Mooncake has a separate `efa` protocol.
- **ibverbs**: The standard RDMA programming interface on Linux, used by both IB and RoCE. **libfabric** is another, more general high-performance network programming interface, used by EFA and others.

**Common RDMA NIC terms**: RNIC and HCA both mean a NIC that supports RDMA; the Mellanox / NVIDIA ConnectX series is the most common model.

**GPUDirect RDMA**: Ordinary RDMA reads and writes Host memory. GPUDirect RDMA lets the NIC **read and write GPU memory directly**, so cross-machine KV transfer does not need to copy to Host memory first. The conditions: the NIC and driver support it (the `nvidia-peermem` kernel module, or the newer dmabuf mechanism, is needed), and the GPU and NIC are ideally under the same PCIe Switch; otherwise the data has to detour through the CPU and performance drops. SGLang's L3 direct mode relies on this to truly avoid Host memory.

### Between Processes in a Machine: Shared Memory and CUDA IPC

- **Shared memory (shm)**: Two processes on the same machine map the same physical memory; what one writes, the other can read directly, and a transfer is one memcpy. Mooncake's `shm` protocol and the data exchange between 3FS USRBIO and the application both use it.
- **CUDA IPC**: Different processes on the same machine share GPU memory. One process exports a memory handle, and another opens it and accesses it directly; the data moves over NVLink or PCIe. Mooncake's `nvlink_intra` uses it.

### Storage Interfaces: NVMe, I/O Methods, File Systems

- **NVMe**: The interface protocol for SSDs. The SSD plugs directly into PCIe and is an order of magnitude faster than the old SATA interface. "NVMe SSD" is the high-speed solid-state disk common in servers today.
- **POSIX reads and writes** (`read` / `write` / `pread` / `pwrite`, and `preadv` / `pwritev`, which handle several memory segments at once): The standard Linux file read and write system calls. Each call enters the kernel, goes through the page cache by default, and the program waits during the call for it to finish (synchronous).
- **io_uring**: A newer asynchronous I/O interface in Linux. The program puts a batch of read and write requests into a queue shared with the kernel, and the kernel puts the results into a completion queue when done. The program does not need a system call for each request, nor does it wait idly, which suits large numbers of small I/Os. Buffers can also be registered in advance to cut the setup cost of each I/O.
- **libaio / POSIX AIO**: Older asynchronous I/O interfaces with a similar role to io_uring and more limits.
- **SPDK**: Intel's open-source user-space storage driver. It "takes" the NVMe disk away from the kernel and lets the user program drive it directly, bypassing the kernel and page cache completely, for the lowest latency and highest throughput. The cost is that the disk can no longer be used by an ordinary file system, and hugepage memory is required.
- **NVMe KV**: Some SSDs support key-value access directly (the disk manages the key-to-location mapping itself), with no file system needed. Mooncake's `nvme_kv` backend uses it.
- **NVMe-oF (NVMe over Fabrics)**: Accesses an NVMe disk on another machine over the network, used as if it were a local disk. The network underneath can be RDMA or TCP. Mooncake's `NOF_SSD` replica type uses remote SSDs as a storage tier this way.
- **GPUDirect Storage (GDS) / cuFile**: Lets the SSD DMA directly into GPU memory without going through Host memory. cuFile is the programming interface NVIDIA provides. Mooncake's `nvmeof` transport protocol and NIXL's GDS plugin are both based on it.
- **Distributed file system**: Organizes the disks of many machines into one unified file system, where all machines see the same directories and files, such as 3FS, CephFS and NFS. Mooncake's `DFS` and `DISK` replicas and SGLang's 3FS backend all sit at this layer.
- **FUSE**: A mechanism that lets a file system run in user space. Applications read and write files as usual, and the kernel forwards the requests to the user-space file system program. Compatibility is good, but every read and write takes an extra round trip, so performance is average. The FUSE mount of 3FS is this kind.
- **Object storage (S3 / OSS)**: Stores and fetches whole blocks of data through an HTTP interface by "bucket + object name". Capacity is nearly unlimited and cheap, but latency is high (milliseconds). Mooncake supports it as the lowest tier through the offload path, recorded as a `LOCAL_DISK` replica.

### Other Hardware and Interface Terms

- **NPU / Ascend**: Huawei's AI accelerator card, which plays the role of a GPU. Mooncake's `ascend` protocol and SGLang's `kernel_ascend` io-backend are for it.
- **ROCm / HIP**: The software stack for AMD GPUs; HIP is the AMD counterpart of CUDA. Mooncake's `hip` protocol is for AMD GPUs.
- **UVA (Unified Virtual Addressing)**: CUDA lets the GPU and CPU share one virtual address space, so a GPU kernel can access pinned Host memory directly through a pointer, with the data moving over PCIe. SGLang's `kernel` io-backend relies on this to let the GPU read and write L2 directly.
- **ZMQ (ZeroMQ)**: A message queue library for sending messages between processes. SGLang uses it to publish KV events and load information to the router; it has nothing to do with moving the KV data itself.

## 3. Storage Components at Each Tier

### The Three Tiers of SGLang HiCache

SGLang's hierarchical cache is called HiCache:

- **L1 GPU memory**: The KV cache that model inference reads and writes directly; the smallest and fastest.
- **L2 Host DRAM**: Local CPU memory that holds KV backed up from the GPU and copies it back to the GPU when needed (H2D/D2H).
- **L3 external storage**: KV storage shared across machines or persisted, with the prefix hash as the key and the KV data as the value. All backends implement the same `HiCacheStorage` interface, and one is chosen at deployment with `--hicache-storage-backend`. The available backends include mooncake, hf3fs, file / fast_file (local files), nixl, aibrix, eic, simm, mori, shm, tensorcast, seaweedfs and others. LMCache does not use this interface; it plugs in by replacing the whole prefix cache.

### Storage Media of Mooncake Store

Mooncake Store is a distributed KV store, and each object can have several kinds of replicas. The replica type decides which medium the data sits on:

- **MEMORY**: The distributed memory pool, made of DRAM (or GPU memory) registered by each node; the fastest to read and write.
- **DISK**: A disk replica on shared file storage. This is the old way, turned on by the master's `--root_fs_dir`, and the official advice is not to use it together with `--enable_offload`.
- **LOCAL_DISK**: The client's local SSD (it can also be NVMe KV, or object storage such as OSS / S3). With offload on (off by default), a copy is replicated asynchronously to the local disk at the same time the data is written into memory (with `offload_on_evict` on, it is written only on eviction instead); with `--promotion_on_hit` also on (off by default), only data that is read repeatedly is promoted back to memory (the threshold is in Section 7).
- **NOF_SSD**: SSD accessed remotely over NVMe-oF (experimental).
- **DFS**: A distributed file system, stored by file page offset. There are only two file system adapters: 3FS (set `MOONCAKE_DFS_FS_ADAPTER=hf3fs`, build with `-DUSE_3FS=ON`, uses the native 3FS USRBIO interface) and posix; the `kvcs-lowlevel` backend can also store DFS replicas. OSS and S3 do not use DFS; they use the LOCAL_DISK offload path above. The whole DFS approach is still under development and experimental, and not recommended for production.

So Mooncake has two levels inside: the first is the memory pool; the second is disk, using any of the last four media above. 3FS can also be mounted as an ordinary directory and used through the DFS posix adapter or the old `DISK` way.

### How the Mooncake Memory Pool Differs From SGLang L2

**Medium**: In a default deployment both are CPU DRAM, but the details differ:

- L2 is pinned (page-locked) memory. SGLang defaults to `pin_memory=True` so the GPU can DMA to it directly and H2D/D2H is faster.
- The Mooncake memory pool is also Host DRAM by default, and how it is allocated depends on the protocol and configuration: under the `rdma` protocol, when NICs are spread across several NUMA nodes, it is allocated in per-NUMA segments; with hugepages on, it uses hugepages; otherwise the `rdma` / `efa` protocols map memory with transparent hugepages (THP) by default (`efa` interleaves across NUMA); only in other cases does it fall back to plain aligned allocation (`aligned_alloc`). It does not have to be DRAM either: when Mooncake is built with `USE_VRAM_SEGMENT`, the general allocation path uses GPU memory instead (`cudaMalloc`); with protocols such as Ascend, sunrise_link and UB, it uses the memory of the corresponding device or interconnect.

The main differences are ownership and access scope:

- **Ownership**: L2 is memory the SGLang process allocates itself, used as the overflow area of local GPU memory. The Mooncake memory pool is made of a segment of memory contributed by each node in the cluster (size set by `global_segment_size`), with metadata managed centrally by the Mooncake master, joined into one global pool.
- **Sharing scope**: L2 serves only this instance and other machines cannot see it. The Mooncake pool is shared by the whole cluster; a KV prefix written by one instance can be read and reused by other instances.
- **Speed and capacity**: L2 only goes over local PCIe and has the lowest latency, but its capacity is limited by one machine's memory. The Mooncake pool's capacity is the sum of all nodes' contributions, usually far larger than one machine, but accessing remote data goes over the network and is slower than L2.
- **Lifetime**: L2 is freed when the SGLang process exits. Data in the Mooncake pool is kept as long as the master and store nodes are alive, and can still be hit after an SGLang instance restarts. But if the memory holding the data was contributed by the SGLang process itself, that data is lost when the process exits.

**Deployment note**: SGLang **contributes memory to the Mooncake pool by default**: `global_segment_size` defaults to 4 GB (parsed as 4 GiB), split evenly among the attention TP × PP ranks of one DP group (with DP attention on, each DP group contributes its own share), so it works without starting a separate store service; setting it to 0 makes it a client only that contributes no memory. In that case this machine's memory has to hold both L2 and the contributed segment, and memory planning must count both.

### What 3FS Is

3FS (Fire-Flyer File System) is a distributed file system open-sourced by DeepSeek, designed for AI training and inference, built on NVMe SSDs and an RDMA network. Its uses include loading training data, checkpoints and inference KV cache. In the KV cache case, it is positioned as shared storage that is much cheaper than DRAM, much larger, and still has high throughput.

#### Components

- **Cluster manager**: Manages cluster membership and node state, deployed with multiple replicas for high availability.
- **Metadata service**: Handles metadata such as files and directories. It is stateless itself; metadata is stored in the transactional KV database FoundationDB, and it scales horizontally.
- **Storage service**: Each storage node manages several local SSDs and stores file data chunks. Replicas use CRAQ (chain replication) for strong consistency, and reads can be spread over the replicas on the chain.
- **Client**: There are two ways to connect. A FUSE mount as an ordinary directory has good compatibility but goes through the kernel, so performance is average; USRBIO is a user-space I/O interface where the application puts data in memory shared with 3FS and submits read and write requests directly, bypassing the kernel, with much better latency and throughput. High-performance cases (including KV cache) all use USRBIO.

**Published performance numbers** (from the official 3FS README): a cluster of 180 storage nodes (each with 2×200Gbps IB and 16 14TiB NVMe disks) reached an aggregate read throughput of about 6.6 TiB/s; in the KV cache case, the peak read throughput of all clients (each node with 1×400Gbps NIC) was about 40 GiB/s.

**Trade-off against the Mooncake memory pool**: 3FS data lands on SSD, with large capacity, low cost, and data that survives process or node restarts; the Mooncake memory pool is in DRAM, with lower latency, but its capacity is limited by the total memory of the cluster.

### Ways to Use 3FS

- **Directly as SGLang's L3**: With the launch flag `--hicache-storage-backend hf3fs`, L2 reads and writes 3FS directly, without Mooncake and without the distributed memory pool level.
  - **Data**: KV pages are written into files on 3FS and read and written through the USRBIO client, with one more memory copy per direction than zero-copy. Each rank allocates space in the file in fixed-size pages; with MLA models all ranks share the same file and only one rank writes.
  - **Metadata**: 3FS only stores files; the index of "which prefix hash maps to which page in the file" is maintained by SGLang itself. A single-machine deployment uses local metadata (in-process); when several machines need to share KV, a separate global metadata service (`mini_3fs_metadata_server.py`) must be started, and every instance queries it. MLA models support only the global metadata service mode.
  - **Prerequisites**: A 3FS cluster must be deployed first (the official docs use the k8s 3fs-operator), and the machines running SGLang must have the USRBIO client (`hf3fs-py-usrbio`) installed.

- **As Mooncake's disk tier**: Use the `DFS` replica type (hf3fs adapter, experimental), or mount it as a directory and use the posix adapter / the old `DISK` replica. 3FS then sits below the Mooncake memory pool, as level 4 end to end.

## 4. Capacity Estimates and Ways to Save GPU Memory

### How Many Bytes the KV of One Token Takes

- **Standard attention (MHA / GQA)**: Each layer stores two copies, K and V, and each copy's size = number of KV heads × head dimension. So bytes per token = 2 × number of layers × number of KV heads × head dimension × bytes per number (2 for bf16, 1 for fp8).
- **With TP**: KV heads are split by the TP of the attention part (the attention TP size when DP attention is on), and each rank stores only "number of KV heads / TP" heads; when TP is larger than the number of KV heads, it counts as 1 head, meaning several ranks store the same head. (The strict formula is "number of heads × (K dimension + V dimension)"; when K and V have the same dimension, it is the 2× above.)
- **MLA (DeepSeek series)**: Each layer stores only one compressed vector, with dimension = kv_lora_rank + qk_rope_head_dim (512 + 64 = 576 for DeepSeek-V3). It is not split into K/V and is **not split by TP**: every TP rank stores a full copy. (With DCP on, it is split by DCP; DSA models such as DeepSeek-V3.2 also add one indexer overhead per token.)
- **Speculative decoding**: The draft model's KV has its own pool, but shares the allocator and the `req_to_token` table (the same slot numbers) with the target model, so the bytes per token in capacity estimates must grow by the draft model's layers.

**Examples** (computed with the formulas above):

- Llama-3-70B (80 layers, 8 KV heads, head dimension 128):
  - bf16, TP1: 2 × 80 × 8 × 128 × 2 = 327,680 bytes ≈ 320 KB/token. 10 GiB holds about 33 thousand tokens.
  - bf16, TP8: each rank has only 1 head, 40 KB/token. 10 GiB per GPU holds about 260 thousand tokens. The 8 GPUs store different heads of the same batch of tokens, so the whole machine also holds 260 thousand tokens.
  - fp8, TP8: 20 KB/token, about 520 thousand tokens per 10 GiB per GPU.

- DeepSeek-V3 (61 layers, MLA 576 dimensions):
  - bf16: 576 × 61 × 2 = 70,272 bytes ≈ 68.6 KB/token, about 150 thousand tokens per 10 GiB; fp8 halves it, about 300 thousand tokens.
  - However large TP is, every GPU has to store this much. With TP8, the 8 GPUs of a machine store 8 identical copies of the KV.

### How the Size of Each Pool Is Set

- **L1 (GPU)**: `--mem-fraction-static` is the fraction of GPU memory taken by "model weights + KV pool". By default it is computed automatically: total GPU memory minus a reserve. Reserve = 512 MB + activations (about 1.5 MB × max(chunked prefill size, 2048)) + a part that grows with TP × PP + the CUDA graph reserve; GPUs larger than 60 GB reserve at least 10 GiB, and the DeepEP communication buffer is added on top. On an 80 GB GPU it is usually around 0.85 or lower (0.87 is the upper bound when the reserve is exactly 10 GiB). At startup the weights are loaded first, the remaining GPU memory is measured, and everything left is given to the KV pool by that fraction; tokens it can hold ≈ KV pool bytes / bytes per token. `--max-total-tokens` can only lower the limit further from there.
- **L2 (Host memory)**: **Each TP rank has its own copy**.
  - `--hicache-ratio`: How many times the GPU pool's token count the Host pool can hold. When not set: 2.0 in normal mode, 1.2 in `buffer_only` mode, and for a decode instance in PD disaggregation: 0.2 when the retraction backup method is `host_pool` and HiCache is off (enough for at least one longest request), otherwise 2.0.
  - `--hicache-size`: Directly sets the Host pool size per rank (GB); when set, it overrides the ratio.
  - When neither is set, it also shrinks automatically based on the machine's available memory: 10 GiB is first kept for the whole machine, the rest is split evenly among the local ranks, then multiplied by `--hicache-host-memory-fraction` (default 0.8).
  - For MLA models, L2 also stores a full copy per rank by default, with no deduplication.

- **L3 (Mooncake memory pool)**: `global_segment_size` is the total contributed by **each SGLang instance** (each DP group when DP attention is on), split evenly among its attention TP × PP ranks (SGLang's Mooncake README says "each TP rank contributes 1/global_segment_size", which is a typo).
  - MLA models: each page is stored only once in L3, and only TP rank 0 writes.
  - MHA models: each rank writes its own share of the heads, and together they make one full page of KV.

### Example: How Much Each Tier of One Machine Holds

DeepSeek-V3, bf16, TP8 on a single machine (8 80 GB GPUs), assuming 20 GB per GPU for KV (GB here means 10^9 bytes):

- L1: about 280 thousand tokens per GPU. The 8 GPUs store the same batch of tokens, so the whole machine also holds 280 thousand tokens.
- L2: with ratio 2.0, each rank uses about 40 GB of Host memory, 320 GB for the 8 ranks, but because each rank stores a full copy, the whole machine holds only about 570 thousand tokens.
- L3: each page is stored once, so every 100 GB of the Mooncake memory pool holds about 1.42 million tokens.

This example shows that MLA models under TP have TP-fold duplication in both L1 and L2 but none in L3, so L3's "tokens per GB" is TP times that of L2. MHA models split by head without duplication when TP does not exceed the number of KV heads; when TP is larger than the number of KV heads, L1 and L2 also have "TP / number of KV heads"-fold duplication.

### Ways to Save GPU Memory

- **KV quantization** (`--kv-cache-dtype`):
  - The default `auto`: follows the model's precision; uses fp8 when the checkpoint declares FP8 KV, and some models (such as DeepSeek-V4, and DeepSeek DSA models on SM100 and above) also use fp8 automatically.
  - `fp8_e4m3` / `fp8_e5m2`: halve the bytes. Each tensor uses one scale factor given in the checkpoint, or 1.0 when none is given.
  - 4-bit formats such as `nvfp4`: halve again, plus a small number of scale factors; they need CUDA 12.8 and PyTorch 2.8 or later, and carry accuracy risk.
  - L2 and L3 store the same format as on the GPU, so the compression carries all the way down the tiers.

- **MLA**: The model structure compresses KV into one low-dimensional vector, much smaller than MHA of the same scale, but under TP every rank stores a full copy (see the example above).
- **Sliding window attention (SWA)**: These layers only need the KV within the most recent window. On the GPU, SWA layers and full attention layers each use their own pool, and SWA data outside the window is marked empty in the radix tree and freed; the two kinds of layers also have their own Host pools in L2.
- **Linear attention such as Mamba**: Each request has only one fixed-size state that does not grow with sequence length. It takes a fixed block reserved in advance on the GPU, also has its own Host pool in L2, and is stored per request.
- **Page size** (`--page-size`): KV is managed in pages; on CUDA the default is 1 token per page, and some backends default to 64 or 128. Prefix matching and L2/L3 transfers all work in whole pages, and a tail shorter than one page is not cached. Larger pages make L3 objects larger and transfers fewer, but make prefix reuse coarser. 64 is common in production with Mooncake.

## 5. The Radix Tree

The radix tree records "which token prefixes already have KV computed, and where the KV is"; it manages both L1 and L2. When a new request comes in, it matches down the tree, and the matched prefix reuses KV directly without recomputing.

**Structure**: Each edge is a run of consecutive tokens (not a single token), and a node stands for "the whole prefix from the root to here". A shared beginning is stored only once and is split into several children at the fork.

Example: three requests come in one after another (each pair of brackets stands for a run of tokens):

- Request 1: `[system prompt] [question A]`
- Request 2: `[system prompt] [question B]`
- Request 3: `[system prompt] [question A] [follow-up]`

```text
root
└── [system prompt]               ← shared by all three requests, KV stored once
    ├── [question A]              ← shared by requests 1 and 3
    │   └── [follow-up]           ← belongs only to request 3
    └── [question B]              ← belongs only to request 2
```

When request 2 is inserted, the original edge `[system prompt][question A]` is split at the fork into two nodes, `[system prompt]` and `[question A]`, and the new branch `[question B]` is attached.

### What a Node Stores

- **key**: The token sequence of this edge.
- **children**: The child table. The key is the content of the first page (`page_size` tokens) of the child edge, plus the request's namespace (`extra_key`, `cache_salt`). Before insertion and matching, the token sequence is first truncated to a whole number of pages, and the match length is also rounded down to pages, so a tail shorter than one page is not cached.
- **GPU location** (`value`): The slot indices of this run's KV in the GPU pool. Empty means it has been evicted from the GPU.
- **Host location** (`host_value`): The slot indices of this run's KV in the L2 Host pool. Empty means there is no Host copy.
- **Reference counts** (stored per component): `lock_ref` counts the requests using this KV on the GPU, and while it is above 0 the KV cannot be evicted from the GPU; `host_lock_ref` is raised while operations such as writing to L3 are in progress, and while it is above 0 the Host copy cannot be freed.
- **Statistics for eviction**: `last_access_time` (for LRU), `hit_count` (for LFU and write_through_selective), request priority and so on.
- **hash_value**: The prefix hash of each page, which is the key in L3 storage.

#### The Three States of a Node

- Only on the GPU: just computed, not yet backed up to the Host.
- On both the GPU and the Host: backed up; GPU eviction only frees GPU memory.
- Only on the Host: evicted from the GPU; a later hit has to load it back to the GPU from L2.

Going by the full attention KV (the Full component), a node with no KV on either the GPU or the Host, no children and no locks is deleted from the tree, and cleanup continues up level by level. Where data sits in L3 is not recorded in the tree; it is looked up in the storage backend by `hash_value` (the node only has a "stored externally" flag).

**Why only leaves are evicted**: A child's prefix contains its parent's, so when a child is in use, its parent must be in use too. So eviction always starts from the leaves:

- GPU eviction removes "leaves at the GPU level", meaning nodes whose children are all no longer on the GPU. After eviction it may stay in the tree in the "only on the Host" state, and its parent then becomes a new candidate.
- Host eviction removes nodes that truly have no children; after eviction they are deleted from the tree, and the parent may become a new leaf.

**Hybrid models**: In the current SGLang implementation (Unified Radix Cache), one node can carry several components at once: full attention KV (Full), sliding window KV (SWA), and the state of linear attention such as Mamba. Each component has its own GPU/Host locations and reference counts. Auxiliary components such as SWA and Mamba can be freed on their own; but whether a node is kept and when it is evicted from the Host both go by the Full component, and Host eviction clears all components on the node at once.

## 6. L3 Keys, Sharing Across Instances, and Consistency

### How the Hash of Each Page Is Computed

The key of each KV page in L3 comes from `hash_value` on the radix tree node, computed like this:

- SHA-256, **chained**: the hash of page 1 = SHA256(token ids of page 1); the hash of page N = SHA256(hash of page N−1 + token ids of page N). So a page's hash stands for "the whole prefix from the start up to this page"; if any earlier token differs, all later pages' hashes differ.
- **Namespace**: If the request carries `extra_key` or `cache_salt`, a seed is first computed from them and used as the start of the chain. Requests with different seeds have different hashes even if their tokens are identical, so they never hit each other.
  - LoRA: The id of the LoRA adapter the request uses is automatically appended to `extra_key`, so KV of different LoRAs is not shared (their KV differs anyway).
  - Multi-tenant isolation: Different tenants can be given different `cache_salt` values.

- **Multimodal**: Images, audio and so on are replaced in the token sequence with a run of special token ids generated from a content hash (far larger than text token ids, so they do not collide with text). The same image gets the same ids, so prefixes with images can hit the cache too.
- **Not in the hash**: the model, the weight version, the KV data type, the TP size. Page size only affects where pages are cut. Of these, the model name and KV data type are written separately into the key prefix (see below); the weight version and TP size are not in the key at all.

### What the Keys Sent to Mooncake Look Like

The default key scheme (`rank-suffix`):

- Prefix: an optional backend tag + the served model name + a storage format tag (if any) + `dtype_{KV data type}`. Only with DCP (decode context parallelism) on is configuration information like `tp{N}_dcp{M}_page{P}_pp{Q}_cp{R}` added.
- MHA models: two objects, `{prefix}_{hash}_{TP rank}_k` and `..._v` (with PP > 1, `_{PP rank}` is added after the TP rank); each rank writes its own share of the heads.
- MLA models: one object, `{prefix}_{hash}__k` (with PP > 1 the middle is `_{PP rank}_`), with no TP rank, so all TP ranks share it.
- Extra pools such as the draft model and SWA layers add the pool name after the rank suffix and before `_k` / `_v`, such as `_{TP rank}_draft_k`; the extra pools of MLA types use `_{PP rank}_{pool name}`.

There is also an optional unified scheme (`--hicache-storage-key-scheme unified`): it adds a digest to the key, computed from the model name, KV data type, page size, total number of KV heads, head grouping, layer grouping, storage layout, whether each rank keeps a replica and so on, and the key also carries topology-independent layer and head group numbers. Instances with different configurations get different keys, so they only miss and never read wrong data; and when the head grouping is the same, instances with different TP sizes can share the same keys.

### Which Instances Can Share KV in L3

- **Several instances of the same model with the same configuration**: They can share; this is the main use of L3. They need the same Mooncake cluster, the same `tenant_id` and the same model name.
- **MLA models with different TP**: They can share (there is no TP rank in the key). Different PP sizes cannot (the key suffixes differ, so they only miss).
- **MHA models with different TP**: **Not safe** under the default scheme. The key has the TP rank but not the TP size, so rank 0 of TP2 and rank 0 of TP4 use the same key while storing different heads. The copy written first stays (later writes find the key already exists and skip); when TP4 reads the larger object written by TP2, Mooncake reports the buffer is too small and it counts as a miss; when TP2 reads the smaller object written by TP4, SGLang treats this partial read as a success and ends up using wrong KV. To mix different TP, there are two ways: under the default scheme, set the same `tp_lcm_size` in extra-config for all instances (requires the `page_head` layout), so each rank splits its data into several objects at a finer grain; or switch to the unified scheme and give all instances the same head grouping (`--hicache-storage-head-partition`).
- **Different page sizes**: The hash cuts pages at different places, so they only miss.
- **Different KV data types** (such as mixing bf16 and fp8): The key prefixes of both schemes include the KV data type (fp8's e4m3 and e5m2 are also told apart), so they only miss and never read wrong data.
- **Same model name but different weights** (for example after a weight update): The keys of both schemes are the same, so **KV computed from the old weights will be read**.

Conclusion: to be correct, instances sharing one L3 must keep the same model weights, and MHA models must also keep the same TP (or be configured as above); for a high hit rate, page size, KV data type and PP should match too. When they have to be mixed, use the unified key scheme, or separate them with different `tenant_id` values.

### Invalidation and Consistency

- **SGLang does not delete data in L3 automatically**; L3 capacity is evicted by the backend itself. So after a model or weight update, the old KV stays in L3 until it is pushed out. The safe ways are to change the model name or `tenant_id`, to call `POST /hicache/storage-backend/clear` to empty L3 (the Mooncake backend calls `remove_all`, which clears data in the whole Mooncake cluster, not just what this instance wrote), or to restart the Mooncake cluster.
- **The `/flush_cache` endpoint**: Runs only when the instance is idle (no running or queued requests; when the instance is paused, queued requests are ignored). It clears the radix tree and KV pool on the GPU, and also clears the Host (L2) memory pool and the state of in-flight prefetches and backups. Data in L3 is not deleted.
- **Weight version tracking** (`--enable-prefill-weight-versions`): Records for each KV slot on the GPU "which weight version computed it", and after a request's prefill finishes, returns to the caller the weight versions of each run of KV. This is for scenarios such as reinforcement learning that update weights online, to know which versions a request's KV mixes. It only records; it does not invalidate old KV. It is mutually exclusive with HiCache (it cannot be used with `--enable-hierarchical-cache` on), because KV restored from L2/L3 has no version information.

### What Happens When a Read Fails

- **L3 prefetch fails or does not finish**: Prefetch runs in batches; after a failed batch it stops reading further (but still sends an acknowledgment for every batch to keep the ranks in sync). The part already read is used as usual, and the rest is recomputed. This has no effect on correctness; it just hits a little less.
- **A Mooncake node goes down during a read**: That part of the read fails and falls back to recomputing as above. Since there is only one replica by default, that data is lost from L3.
- **Load fails in direct mode**: With layer-wise loading, the forward pass does not fail midway, but the requests in this batch are aborted after the forward pass (returning an error) instead of continuing to generate with wrong KV; with whole-run prefetch, the failed part is recomputed instead.
- **L2 → L3 write fails**: From the failed batch on, no more writes are made; data already in L2 is not affected, and L3 just lacks this backup.

## 7. Data Movement: When Data Moves and by What Policy

### SGLang: Between L1, L2 and L3

#### Overview

- L1 → L2: backed up by the write policy, as an asynchronous GPU copy.
- L2 → L3: written asynchronously right after the L1 → L2 backup finishes.
- L3 → L2: prefetched when a request arrives.
- L2 → L1: loaded back to the GPU when a prefix hits a Host copy, overlapped with compute layer by layer.
- In HiCache mode data always lands in L2 first; there is no path from L3 straight to the GPU (except in direct mode).

**L1 → L2: write policy**. `--hicache-write-policy` decides when KV on the GPU is backed up to the Host:

- **write_through** (default): backs up on a node's first hit; in practice it backs up as soon as the node is inserted.
- **write_through_selective**: backs up a node only after it is hit 2 times, so only reused prefixes are backed up, saving Host space and PCIe bandwidth. The threshold is hard-coded and not configurable.
- **write_back**: does not back up normally, and copies to the Host only when L1 evicts the node.

The copy runs asynchronously on a dedicated D2H CUDA stream and waits on the forward compute stream, so it never reads KV that is still being written. After the copy finishes, the node is marked "backed up".

#### L2 → L3: Writing to Storage

- **When**: As soon as the L1 → L2 backup finishes, these nodes are submitted to L3, with no extra hit threshold.
- **How**: The background thread `hicache-backup` handles it, calling the backend's `batch_set_v1` in batches of 128 pages (the zero-copy path; the old path is `batch_set`). Only some ranks write, so that several TP ranks do not write the same data twice.
- **Protection**: Host pages are locked while being written to L3, so they are not evicted from L2 before the write finishes.
- **Deduplication**: SGLang does not check whether L3 already has the data before writing; the backend handles deduplication itself in `batch_set`.

#### L3 → L2: Prefetch

- **Trigger**: When a request comes in, if the local L1 and L2 matched only part of the prefix, an L3 prefetch is started for the rest. If the rest is shorter than `prefetch_threshold` (default 256 tokens), no prefetch is made. It is also skipped when the total tokens being prefetched exceed a limit.
- **Flow**: First the `hicache-prefetch` thread uses `batch_exists` in batches of 128 pages to check how much L3 can hit, stopping at the first miss. The ranks take the minimum hit count so the result is consistent. Then Host space is allocated, and the `hicache-prefetch-io` thread reads into L2 with `batch_get`.
- **When it ends**: `--hicache-storage-prefetch-policy` decides how long the request waits.
  - `best_effort`: does not wait; whatever has arrived at scheduling time is used.
  - `wait_complete`: waits until the prefetch finishes.
  - `timeout` (default): waits at most `1 second + 0.25 seconds per 1024 tokens`; after the timeout, the part that arrived is used and the rest is recomputed. (These are the defaults in the current code; the 2 seconds / 0.1 seconds / 30-second cap in SGLang's official hicache_design doc does not match the code.)

#### L2 → L1: Loading Back to the GPU

- **Trigger**: When scheduling a request, if the matched prefix has a copy only on the Host, it is loaded back to the GPU. Below 10 tokens it is not loaded, since recomputing is cheaper. It is also not loaded when GPU space is short.
- **How**: Copied asynchronously on a dedicated H2D stream, overlapped layer by layer with this batch's forward pass.

### Writing to and Reading From the Mooncake Memory Pool

- **Write (Put)**: The client first asks the master for space (PutStart), and the master picks memory segments on target nodes and returns the addresses. The client then writes the data directly to those addresses through Transfer Engine, and finally tells the master the write is done (PutEnd). Data does not pass through the master. 1 replica by default.
- **Read (Get)**: The master returns all readable replicas, and the client picks one to read in the order "local memory → local NoF SSD → remote memory → remote NoF SSD → local SSD replica → DFS → DISK". Each read renews a lease on the object (default 10 seconds), and the object is not evicted during the lease, so it is not deleted halfway through a read.

### Mooncake Memory Pool ↔ Local SSD

Requires `enable_offload` to be on (off by default).

- **Writing to SSD (offload)**:
  - By default offload is queued at PutEnd, meaning a copy to SSD is scheduled at the same time as the write into memory, so the data is still on SSD when memory fills up and evicts it.
  - With `offload_on_evict` on, offload happens only on memory eviction instead, and the SSD holds only the cold data pushed out.
  - Offload writes to the local SSD of the machine holding this memory replica, not to the writer's SSD.
  - The client on that machine does the work: at each heartbeat (default 10 seconds) it pulls a batch of tasks from the master, reads from memory, writes to SSD, then tells the master to register the LOCAL_DISK replica. Each local disk segment can have at most 50 thousand pending tasks (`offloading_queue_limit`), and at most half are handled per round.

- **Reading back into memory (promotion)**: Requires `promotion_on_hit` to be on as well (off by default). On a read, if there is only an SSD replica, this key's access count has reached the threshold (default 2), and memory usage is below the eviction watermark, it is queued for promotion back into memory. The client holding the SSD replica does it at heartbeat time, handling only 1 per heartbeat by default.

## 8. Eviction

### SGLang L1, L2, L3

- **Policy**: L1 and L2 both use `--radix-eviction-policy`, default `lru` (least recently accessed first). Other options include `lfu` (fewest hits first), `priority` (prefixes of low-priority requests first), `slru` (nodes hit 2 or more times enter a protected segment and are evicted later), `tlru`, `joint_lru`, `state_cost` and others.
- **When**: Both evict on demand, only when allocation runs short, with no periodic background cleanup. Only leaf nodes are evicted, and only those no running request references.
- **Where a node goes after L1 eviction**:
  - Already has a Host copy: only GPU memory is freed; the node stays in the tree as "only on the Host", and a later hit can load it back from L2.
  - write_back policy: copied to the Host first, then GPU memory is freed; if the Host is also full, it is dropped.
  - A node not yet backed up under write_through: dropped directly; next time it can only be recomputed or fetched from L3.

- **L2 eviction**: Evicts only Host leaf nodes that are no longer on the GPU and are not locked (including being written to L3). After eviction the node is deleted from the tree. If the data was already written to L3, it can still be prefetched back from L3 later.
- **L3 eviction**: SGLang never deletes L3 data and leaves capacity management to the backend: the local file backend deletes files by LRU; the Mooncake memory pool is evicted by the master by memory watermark, and local SSD by each client by disk watermark, as detailed below; other backends such as 3FS are handled by their own servers.

### Mooncake Memory Pool

- **Trigger**: The master checks every 10 ms, and starts eviction when memory usage exceeds `eviction_high_watermark_ratio` (default 0.9) or a write fails for lack of space.
- **Amount**: Each round evicts about `eviction_ratio` (default 5%) of the objects. If usage is well over the watermark, the excess is evicted on top.
- **Order**: Approximate LRU, sorted by lease expiry time; the earlier the lease expired (the longer since the last read), the earlier it is evicted.
- **Skip rules**:
  - Hard-pinned objects are never evicted.
  - Objects whose lease has not expired are skipped.
  - Soft-pinned objects (kept 30 minutes by default) are evicted only when there are not enough ordinary objects to evict.
  - Replicas that are referenced (such as being offloaded to SSD) are not freed for now.

- **Where it goes**: Dropped directly by default. With `offload_on_evict` on, the data is first moved to SSD, then the memory is freed.
- **Multi-tenancy**: With multi-tenancy on, a tenant whose usage exceeds 90% of its own quota has its data evicted separately.

### Mooncake Local SSD

The client checks at heartbeat time: when SSD usage exceeds 90%, it evicts down to 80%; a write that runs short of space also evicts immediately. The default bucket storage backend evicts the oldest data per bucket in write order (FIFO). After eviction it tells the master to delete the corresponding SSD replica records. The default SSD capacity limit is 2 TB and 10 million keys.

## 9. Transfer Methods: Which Links the Data Takes and Who Moves It

Below, L1 = GPU memory, L2 = local Host DRAM, L3 = the Mooncake memory pool (or another L3 backend), L4 = the Mooncake disk tier.

### The Physical Path of Each Hop

- L1 ↔ L2: inside one machine, GPU memory ↔ PCIe ↔ Host memory.
- L2 ↔ L3: usually across machines, local Host memory ↔ local NIC ↔ network switch ↔ peer NIC ↔ peer memory pool. If the memory pool segment happens to be on this machine, it does not leave the machine.
- L3 ↔ L4: memory pool ↔ local NVMe SSD is PCIe inside the machine; accessing remote SSD (NVMe-oF) or a distributed file system (3FS and so on) goes over the network.

### L1 ↔ L2: PCIe

Goes over local PCIe, and `--hicache-io-backend` decides who moves the data:

- `kernel` **(default)**: A copy kernel runs on the GPU, and the GPU's compute units (SMs) read and write Host memory directly. Host memory is pinned, so the GPU can access it directly through mapped addresses. The upside is that scattered pages are moved by one kernel; the cost is that it uses some SMs.
- `direct`: Uses the GPU's copy engines (DMA, `cudaMemcpyAsync`). In the `layer_first` layout, pages with contiguous addresses are first merged into segments, one copy per segment; the `page_first_direct` layout uses the batched copy API on CUDA 12.8 and above (the driver must also be 12.8 or above), otherwise copies page by page. It uses no SMs, but the page indices must first be copied back to the CPU; DMA may also queue ahead of the forward pass's small copies and slow the forward pass.
- `kernel_ascend`: For Ascend NPUs only.

`--hicache-mem-layout` decides how KV is laid out on the Host, and also limits which io-backend can be used. The three common ones are below (there are also `page_first_kv_split`, `layer_first_kv_split`, `page_head`, and `page_unified`, which the unified key scheme forces):

- `layer_first`: Each layer's KV is stored contiguously, suited to loading back to the GPU layer by layer. Both kernel and direct work.
- `page_first` (default): All layers' KV of one page sit together, close to one object in L3, so writes to L3 are more contiguous. Only kernel works.
- `page_first_direct`: Each layer of each page is contiguous, suited to whole-page DMA copies. Uses direct.
- When Mooncake (or `npu_memcache`) is the L3, `layer_first` is not supported and is changed automatically to the page_first family (except with DCP on).

### L2 ↔ L3: Depends on the L3 Backend

- **Mooncake**: Goes through Mooncake Transfer Engine. The whole L2 is registered with Mooncake, and reads and writes use addresses in L2 directly. The protocol is set by `protocol` in the config or the environment variable `MOONCAKE_PROTOCOL`; in SGLang, when neither is set, **the default is `rdma`** (one-sided RDMA reads and writes, zero-copy). Only when Mooncake's own Python config or a separately deployed `mooncake_client` is used directly is the default `tcp`. Under `tcp` it goes over sockets, through kernel buffers.
- **3FS (hf3fs)**: Goes through 3FS's USRBIO user-space interface. On writes, L2 pages are first memcpy'd into the memory region shared with 3FS and then the I/O is submitted; reads go the other way, so each direction has one extra memory copy. The 3FS client library moves data from the shared memory region to the 3FS storage nodes.
- **Local files (file)**: Ordinary POSIX file reads and writes, through the kernel page cache. Reads go directly into L2 pages; writes first go to a temporary file, then are renamed atomically.
- **NIXL**: A NIXL agent plus a storage plugin; it automatically picks an available file plugin in the order 3FS, POSIX, GDS_MT, GDS, and also supports S3 object storage. With the `page_first` family of layouts, the whole L2 is registered and it is zero-copy; other layouts go through a staging buffer.

### Zero-Copy

The general meaning of zero-copy: data goes straight from the source memory to the target memory, without passing through any temporary buffer, and without the CPU moving it byte by byte.

With the RDMA protocol, L2 to Mooncake is zero-copy: at startup SGLang registers the whole L2 memory with Mooncake (under RDMA that means registering it with the NIC), and reads and writes pass only addresses and lengths in L2 (`batch_put_from` / `batch_get_into`). The NIC reads data straight from L2 and sends it to the remote side, or writes remote data straight into L2, without first copying to a temporary buffer.

- **Cost**: Registered memory is locked. Some environments (such as eRDMA) cap the total that can be registered, and registration fails if L2 plus `global_segment_size` exceeds it.
- **TCP**: Without RDMA, data has to pass through kernel socket buffers, so it is not zero-copy in the strict sense.

### Inside Mooncake and the Disk Tier

- **client ↔ remote memory pool**: Goes through Transfer Engine. Under the `rdma` protocol, writes are one-sided RDMA writes and reads are one-sided RDMA reads, and the remote machine's CPU is not involved. Replicas in the same process are memcpy'd directly only in TCP mode or when `MC_STORE_MEMCPY` is set; in RDMA mode, writes to a local segment also loop back through the NIC.
- **Memory pool → local SSD (offload)**: The client holding the memory replica writes to disk straight from the local memory address, without Transfer Engine. It uses `pwritev` or io_uring (some backends can turn on O_DIRECT to bypass the page cache); the `nvme_kv` backend sends NVMe KV commands directly.
- **Reading from another node's local SSD**: The requester first sends an RPC; the holder reads the data from SSD into a staging buffer of its own (registered with Transfer Engine), and the requester then pulls it with Transfer Engine (an RDMA read under RDMA). The path is SSD → holder's memory → network → requester's memory.
- **Local SSD → memory pool (promotion)**: The holder reads the data into a staging buffer, then writes it into the newly allocated memory replica with Transfer Engine.
- **NOF_SSD**: Uses SPDK's NVMe-oF client to issue NVMe reads and writes directly on the user buffer, without Transfer Engine and without a staging copy. The buffer must be hugepage memory registered with SPDK. Whether NVMe-oF runs over RDMA or TCP underneath is decided by the target's configuration.
- **DISK (shared file system)**: On writes, the data is first copied into a block of memory, then 2 background threads write the files; reads go directly into the user buffer. Uses POSIX or io_uring.
- **DFS**: Does not go through Transfer Engine, and calls the file system or object storage directly. The `posix` adapter reads and writes the user buffer directly with `preadv` / `pwritev` (through the page cache); the `hf3fs` adapter does one extra memcpy per block into the 3FS shared memory region; there is also the `kvcs-lowlevel` backend. OSS / S3 use HTTP (libcurl), but belong to the offload path, not DFS.

### Protocols Supported by Transfer Engine

Transfer Engine is Mooncake's data transfer layer. Upward it offers one interface, "read/write this block of memory to that block of memory"; downward it picks the concrete transfer method by the configured protocol:

- `rdma`: Uses RDMA NICs (InfiniBand or RoCE), doing one-sided reads and writes through ibverbs, without the peer CPU. Large requests are cut into 64 KB slices; for each block of memory, it picks the closest NIC by machine topology. It supports GPUDirect RDMA: GPU memory can be registered with the NIC directly (dmabuf or nvidia-peermem), and the NIC reads and writes GPU memory directly. Cross-machine KV transfer in production almost always uses it.
- `rdma_twosided`: The two-sided mode of RDMA (send/recv), where the peer must prepare receive buffers first. It cannot be on at the same time as `rdma`.
- `tcp`: Ordinary sockets. It works on any network, but goes through the kernels on both ends with the CPU doing copies, so bandwidth and latency are much worse. Data in GPU memory must first be copied to Host memory before sending. SGLang uses `rdma` by default; Mooncake's own Python config and the standalone `mooncake_client` default to `tcp` when no protocol is configured, so in production confirm it has been changed to `rdma`.
- `nvlink`: Cross-machine NVLink (MNNVL, as in the GB200 NVL72 rack), using CUDA's cross-machine memory sharing handles; GPUs transfer directly to each other.
- `nvlink_intra`: Between GPUs inside one machine, sharing GPU memory with CUDA IPC and transferring over NVLink.
- `shm`: Between processes inside one machine, using shared memory, one memcpy.
- `efa`: The RDMA NIC EFA on AWS, read and written through the libfabric interface.
- `cxi`: The NIC of the HPE Slingshot network, also through libfabric.
- `nvmeof`: Reads and writes NVMe disks through cuFile (GPUDirect Storage), and can let the SSD DMA directly into GPU memory.
- Others: `cxl` (CXL memory), `hip` (AMD GPU), `ascend` (Huawei Ascend NPU), `nccl`, `barex`, `ub`, `ubshmem`, `hylink`, `maca`, `musa`, `flagcx`, `sunrise_link` and more, for specific vendors' hardware or communication libraries; this note did not look into them in detail.

### Bypassing L2: Direct L3 ↔ GPU

Besides HiCache's L1 → L2 → L3 chain, SGLang has a direct mode: `--enable-unified-cache-external-linker`, with mooncake as the backend.

- The KV pool on the GPU is registered with Mooncake directly, and reads and writes go between GPU memory and Mooncake, with no L2.
- It is mutually exclusive with HiCache: it cannot be used with `--enable-hierarchical-cache` or `--hicache-storage-backend`, nor with prefix caching turned off; pipeline parallelism (PP > 1) is not supported. The backend can be `mooncake` (default), `mori` or `dynamic`.
- Whether it truly avoids Host memory depends on the protocol Transfer Engine uses: with `rdma` and a NIC that supports GPUDirect RDMA, the NIC reads and writes GPU memory directly; with `tcp`, data is still staged on the Host.

## 10. Overlapping Compute and Transfer

### Why Overlap, and What Makes It Possible

Moving KV between tiers takes time. If compute always waited for the move to finish, the GPU would sit idle. "Overlap" means running the move and the compute at the same time, hiding the transfer time behind compute time. There are three main tools:

- **CUDA stream**: A task queue on the GPU. Tasks in the same stream run in order, and different streams can run in parallel. Putting copies on a separate stream lets them run alongside the forward compute stream.
- **CUDA event**: A marker in a stream. One stream can "wait until another stream reaches some event" before continuing; this wait happens on the GPU, and the CPU does not have to stop.
- **Background threads**: Separate threads on the CPU handle L3 reads and writes and network transfer, while the main thread keeps scheduling and launching compute.

### How Each Transfer Overlaps

Each item first says what runs at the same time, then where things must stop and wait.

- **L1 → L2 backup**: Runs on a dedicated D2H stream, alongside the following forward passes.
  - Where it does not overlap: before each copy is submitted, the D2H stream first waits for the compute already queued on the forward stream to finish, because it may still be writing the KV to back up. The wait happens on the GPU; the CPU does not stop.
  - Under the write_back policy, eviction must copy the data to the Host first, and the CPU waits synchronously for the copy, which in turn waits for the running forward pass to end. So eviction under write_back breaks the overlap.

- **L2 → L1 load**: Pipelined by layer, overlapped within the same batch. The H2D stream copies layer by layer and records an event after each layer; when the forward pass reaches layer N, the GPU waits only for layer N's event. The effect is "while the GPU computes layers 1~N, the KV from layer N+1 on is still being copied up from the Host".
  - Where it does not overlap: before the load starts, the H2D stream first waits for the previous batch's forward pass to finish (the GPU memory to be written may have just been reclaimed and still be in use by the previous batch). So the load overlaps only with this batch's forward pass, not the previous batch's.
  - When running with a CUDA graph that cannot carry these events, it waits for all layers to load before running, and there is no layer-wise overlap that time.
  - The draft model of speculative decoding starts only after the last layer has loaded, so it has no layer-wise overlap either.
  - Effect of the io-backend: `kernel` copies with the GPU's SMs and competes with compute for SMs; `direct` uses copy engines and does not compete for SMs, but may block the forward pass's own small copies, which `SGLANG_ENABLE_MLP_SYNC_METADATA_FILL=1` can ease.

- **L3 → L2 prefetch**: Started as soon as the request arrives, before it enters the waiting queue, with background threads doing the query and the read. Prefetch overlaps with the time "the request itself waits in the queue to be scheduled", and also with other batches' GPU compute and CPU scheduling, without using a GPU stream.
  - Where it does not overlap: if the prefetch has not finished when the request's turn for admission comes, `--hicache-storage-prefetch-policy` decides: `wait_complete` keeps waiting (the request is not scheduled this round), `timeout` waits until the timeout, `best_effort` does not wait and uses what has arrived.

- **L2 → L3 write**: The background thread `hicache-backup` handles it, in parallel with all compute and scheduling. The only ordering constraint: a page must finish its L1 → L2 copy before its write to L3 can start.
- **Inside Mooncake (memory pool ↔ SSD)**: Offload is run in the background by the client holding the data at heartbeat time (once every 10 seconds by default), and promotion runs at heartbeat or prefetch time; both are asynchronous to inference, and the inference side does not wait for them.
- **Overlapping scheduling and compute (overlap scheduler, on by default)**: While the GPU runs batch N, the CPU is already preparing batch N+1, including prefix matching, submitting L1 → L2 backups, submitting L2 → L1 loads, and checking whether the various transfers have finished. These checks only query completion status and do not block, so normally they do not break the overlap.
- **Direct L3 ↔ GPU mode**:
  - Load: fetched in parallel in layer groups (8 layers per group by default); as soon as a group arrives, the forward pass computes that group, overlapping with compute by layer. The wait here happens on the CPU: when data has not arrived, the thread launching compute stops, while the earlier layers already launched keep running on the GPU. When loading cannot keep up, the GPU sits idle.
  - Write-out: after the forward pass, a background thread writes the newly computed KV to Mooncake, in parallel with later compute.
  - Where it does not overlap: the next batch's load waits for the current batch's forward pass to finish before writing GPU memory; only the work of preparing keys can be done ahead.

- **KV transfer in PD disaggregation**:
  - Prefill side: only after a request's (or a chunk's) prefill is computed is the whole KV sent to decode; it is not sent layer by layer during compute. A background thread does the sending, overlapping with the prefill instance's next batch of compute. `SGLANG_DISAGG_PREFILL_EARLY_SEND_CACHED_PREFIX` is on by default (set to 0 to turn it off): the prefix already hit in GPU memory is sent first, overlapping with the compute of the rest.
  - Decode side: requests waiting to receive KV are kept in a separate queue, the scheduler only does non-blocking queries, and other requests decode as usual.

- **Chunked prefill**: In PD mode, KV is sent once after each chunk is computed, so the first chunks of a long request can overlap with the compute of the later chunks.

### Summary

L2 → L3 writes, L3 → L2 prefetch, and SSD reads and writes inside Mooncake all run in the background and overlap with compute almost completely. L2 → L1 loads (and loads in direct mode) overlap by layer with this batch's compute, but must wait for the previous batch to finish before starting. L1 → L2 backups overlap with later compute, but eviction under the write_back policy makes the CPU wait synchronously. PD's KV is sent at the grain of a whole request or chunk, not by layer.

## 11. KV Transfer in PD Disaggregation

### What PD Disaggregation Is

Inference for a request has two phases: **prefill** (computes the whole input at once, producing the KV of all input tokens and the first output token) and **decode** (generates one token at a time). Prefill is mainly compute-bound and decode is mainly memory-bandwidth-bound, so putting them on the same GPUs makes them interfere with each other. PD disaggregation runs prefill and decode on different instances; after the prefill instance finishes, it sends the KV to the decode instance, which continues generating.

### The Flow of One Request (Using the Mooncake Backend as the Example)

1. The router picks a prefill instance and a decode instance for the request, and sends the same bootstrap information (prefill address, bootstrap port, and a "room number") to both sides.
2. The decode instance connects to the prefill's bootstrap service (default port 8998), gets the prefill's parallel configuration, and on the first connection registers the GPU memory addresses of its own KV pool with the prefill.
3. Decode first **preallocates slots** in its own KV pool for this request and sends the slot numbers and related information to prefill.
4. Prefill computes as normal. Each time a chunk (or the whole request) is computed, a background thread **writes this part of the KV directly into the GPU memory decode reserved** through Transfer Engine (a one-sided RDMA write, without the decode CPU). The data is organized by layer, but it is sent after this chunk's compute is done.
5. After the last chunk is written, prefill writes one more piece of auxiliary data (such as the first output token) and tells decode the transfer is complete.
6. The decode instance's scheduler only does non-blocking queries; when it sees the transfer is complete, it puts the request into a decode batch.

The transfer backend is chosen by `--disaggregation-transfer-backend`, default `mooncake`; there are also `nixl`, `ascend`, `mori`, `mooncake_tcp` (forces TCP) and others. The mode is set with `--disaggregation-mode prefill/decode`.

### When Prefill and Decode Have Different TP

- **MHA / GQA**: Supported. Each prefill rank writes the heads it holds to the matching head positions on the matching decode rank; when decode's TP is larger, several decode ranks share one head (GQA head replication). This path sends token by token with many transfers, which may raise time to first token; `SGLANG_DISAGG_STAGING_BUFFER` (mooncake / nixl backends only) can be turned on to assemble the data in a staging buffer before sending.
- **MLA**: Every rank has the full KV, so no splitting is needed and the whole copy is sent directly.
- State models such as Mamba transfer state slices when TP differs; unsupported combinations (such as unified memory, KV sharding or DFLASH on) are rejected when decode registers with prefill, not at startup.

### Working With HiCache

- **Prefill side**: HiCache and L3 can be turned on as normal; a hit prefix is not recomputed, but loaded from L2/L3 and sent to decode along with the rest. The official best practices give two PD setups: HiCache on the prefill side only; or HiCache on the prefill side plus asynchronous write-out on the decode side (in multi-turn dialogue, prefill can then reuse the KV that decode wrote out).
- **Decode side**: With decode-side prefix caching (`--disaggregation-decode-enable-radix-cache`, off by default) or decode HiCache on, decode also checks its local cache and L2/L3. If it can find part of the prefix itself, it asks prefill to send only the rest.
- **Decode-side write-out**: With `--disaggregation-decode-enable-offload-kvcache` (off by default) on, new KV generated by decode is also written to L3 for later turns of a multi-turn dialogue to reuse. It can only be turned on on the decode side, requires `--hicache-storage-backend` to be configured too, and cannot be used with `--disaggregation-decode-retraction-backup host_pool`.

### Timeout Settings

- `SGLANG_DISAGGREGATION_BOOTSTRAP_TIMEOUT`: bootstrap handshake timeout, default 300 seconds.
- `SGLANG_DISAGGREGATION_WAITING_TIMEOUT`: timeout for waiting for the KV transfer to finish, default 300 seconds.
- `SGLANG_DISAGGREGATION_HEARTBEAT_INTERVAL` / `..._MAX_FAILURE`: decode sends heartbeats to prefill (prefill does not check decode), every 5 seconds (minimum 2 seconds), and 2 consecutive failures mean prefill is considered lost.

## 12. Special Cases: Speculative Decoding, Multimodal, Sparse Attention

### Speculative Decoding

Speculative decoding uses a small draft model to guess a few tokens first, then lets the large model verify them in one pass.

- The draft model's KV usually has its own pool, but shares the allocator and slot numbers with the target model, so allocation and freeing happen in one step. Only with `--enable-unified-memory` on, a target model that is an SWA/Mamba hybrid, and EAGLE or DFLASH in use, are the draft layers placed directly in the target model's pool (the fused way).
- The slots of rejected guessed tokens are freed after verification.
- Bytes per token grow by the draft model's layers, which must be counted in capacity estimates.
- There are three ways to back up to L2/L3: in the fused way, the draft layers are already in the target model's pages; the packed way packs the draft layers into the target model's Host pages; only the sidecar way writes them to Mooncake as a separate pool (`DRAFT`).

### Multimodal

- **Prefix matching**: Images and audio are replaced in the token sequence with special token ids generated from a content hash; the same image gets the same ids, so "the same image + the same text" can hit the prefix cache.
- **Encoder output cache**: The embeddings an image gets from the vision encoder can also be cached. SGLang has an embedding cache stored by content hash, with its own paged memory pool on the Host (LRU eviction), and the backend can be Mooncake (`MooncakeEmbeddingStore`), so several instances meeting the same image do not have to rerun the encoder. It is turned on with `--enable-mm-global-cache` (off by default) and `--mm-global-cache-backend mooncake`, and currently takes effect only in the encoder service of an encoder-disaggregated deployment.
- **Routing**: sgl-router's `--cache-media-affinity-ttl-ms` remembers which instance a conversation with images was sent to, and later turns prefer to go back there.

### Sparse Attention (HiSparse)

- Idea: The full KV is kept in Host memory, and at each step only the tokens attention actually needs (picked by the model's sparse selection mechanism) are copied to a buffer on the GPU for compute. That way the GPU needs only a small piece of memory to support very long contexts.
- How to turn it on: `--enable-hisparse`. It supports only specific models (models with DSA sparse attention such as DeepSeek V3.2 and GLM-5, plus DeepSeek V4 and MiniMax M3), and requires prefix caching to be off (`--disable-radix-cache`), so it cannot be used together with HiCache's multi-tier cache.
- It and HiCache both use Host memory, but for different purposes: HiCache uses Host memory to cache "prefixes that may be reused later"; HiSparse uses Host memory to hold "the part of the current request's KV that does not fit on the GPU".

## 13. Request Scheduling, Admission and Load Balancing

Scheduling has two layers:

- **Scheduling within an instance**: The scheduler of one SGLang instance decides which requests in the waiting queue go into a batch first.
- **Load balancing across instances**: The router in front of several instances (sgl-router) decides which instance a request goes to.

SGLang has both layers, and both look at KV cache hits. Admission (whether a request can come in) also has two layers: within an instance, whether it can enter a batch depends on the free KV memory; at the cluster level, sgl-router decides where to send it and whether to reject it outright based on instance load. Mooncake does no request scheduling; it only provides a global prefix index (Conductor), storage-side tenant quotas, and balancing of where KV data is stored.

### Scheduling Within an SGLang Instance

**Scheduling policies** (`--schedule-policy`, default `fcfs`) fall into two kinds:

- Cache-unaware: `fcfs` (first come, first served), `lof` (longest output first), `random` and others.
- Cache-aware: `lpm` (longest prefix match first), `dfs-weight`, `hrrn`, `shortest-prefill-first` and others.
- With prefix caching off, `lpm`, `dfs-weight` and `hrrn` fall back to `fcfs`; `uniboost` works as usual; `shortest-prefill-first` raises an error.

**How lpm uses the radix tree**: Each request in the waiting queue is matched against the radix tree and sorted by hit length from long to short. Requests with more hits run first; they need fewer new tokens computed, and the prefix nodes they depend on were just accessed, so they are less likely to be evicted. The hit length includes hits on the Host.

**When the queue is too long**: Each request needs one radix tree lookup, and the cost grows with queue length. When the waiting queue exceeds 128 requests, `lpm` and `hrrn` fall back to `fcfs` by default. Current SGLang adds "bounded LPM" to `lpm`: when it judges it worthwhile, it sorts only the first 64 requests of the queue by prefix hit and keeps FCFS for the rest. This feature is not enabled when HiCache, SWA, Mamba or session prefix caching is on, or when the cache type is not an ordinary radix tree; it still falls back to FCFS.

**Prefix sharing within a batch**: If several requests in the waiting queue share the same not-yet-cached beginning (≥32 tokens), only one of them runs first and the others are pushed back. After the first one is computed, the prefix is in the tree, and the later ones hit it directly.

#### How KV Memory Is Counted at Admission

- A new request is charged only for the part that needs computing: input length minus the hit prefix, plus the expected output length (estimated at most 4096). The hit prefix is not charged again, and it is locked during selection so it is not counted as evictable space.
- Space must also be reserved for the rest of the generation of requests already decoding: remaining output length × `new_token_ratio`. This ratio starts at `min(0.7 × --schedule-conservativeness, 1.0)` (conservativeness defaults to 1.0), and when no retraction happens it drops linearly over 600 steps to 14% of the initial value. Raising conservativeness is more conservative: fewer retractions, but smaller batches.
- Long inputs are prefilled in chunks by `--chunked-prefill-size`, with only one request being chunked at a time.

#### Working With HiCache

- When a request's L3 prefetch has not finished, the scheduler skips it and schedules the requests behind it first, checking again next round.
- When the hit prefix is on the Host, GPU memory for loading it back is reserved first at admission. If the reservation succeeds, it is loaded asynchronously in the same batch; if it fails, the request waits. The load either fully succeeds or does not happen and is replaced by recomputing.

**Retraction when GPU memory runs out**: When KV memory runs out during decode, some requests are sent back to the waiting queue according to `--retraction-policy` (default `length`: short outputs with long inputs go first), freeing their KV until the remaining requests fit. At least one request is kept, and if even the last one does not fit, it is aborted too; without a Host backup, retracted requests are aborted with 503 / 500 (see Appendix 2 Q4 of the [SGLang PD Disaggregation Study Notes](./SGLang-PD-Disaggregation-Mooncake-Notes_en.md)). After retraction, `new_token_ratio` is re-estimated as the share of "generated tokens + reserved steps" in the total `max_new_tokens`, and later admission becomes more conservative.

### Load Balancing Across Instances: sgl-router's Routing Policies

**Routing policies** (`--policy`, default `round_robin`; default `power_of_two` in `--chat-routing reorg` mode):

- Load only: `round_robin`, `random`, `power_of_two` (picks 2 at random and chooses the one with less prefill pressure), `load_based` (scores by "queued + running").
- Cache-aware: `cache_aware` (cache affinity, detailed below), `fused_score` (a weighted sum of prefix hit share and load, with both terms on by default), `score_policy` (the same fused score, plus a layer of prefill admission; `power_of_two` and `cache_aware` also use this admission layer).
- Others: `sticky` (pins to the same instance by a key in the request header), `session_aware`.
- Filters can be stacked on top: `prefix_cache` removes instances whose hit share is too low, and `overloaded` removes instances with too many in-flight requests.

**How the router knows what each instance has cached**: The current sgl-router no longer simulates an "approximate radix tree" in the router from request text, as early versions did. It subscribes to the KV events each SGLang instance emits (the instance must turn on `--kv-events-config`): each time the instance's radix tree stores or removes a block, it sends a `BlockStored` / `BlockRemoved` over ZMQ. From these the router maintains a table indexed by block hash, so what it knows is the instance's actual cache state. The router's model has four tiers, GPU, Host, local disk and external storage, but SGLang currently emits events only for the GPU and Host tiers, so the router does not know whether a block is in L3. (This table is actually a radix tree organized by block hash chains.) (The optional `--cache-pending-prefix-ttl-ms` records a just-dispatched prefix on the corresponding instance before the event confirms it.) Another source is querying an external KV index service. Load information (queued requests, queued tokens waiting to be computed, KV usage, estimated prefill queue time) is reported over another ZMQ channel (instance-side flag `--load-publish-endpoint` on SGLang, which also requires `--kv-events-config`).

#### How cache_aware Chooses

1. Compute how many tokens each instance can hit. Instances with fewer than 1024 hit tokens are not candidates; this is the threshold for "whether chasing the cache is worth it". The number of candidates is 5% of the healthy prefill instances (rounded up), limited to between 8 and 32 and to no more than the total number of instances, sorted by hits.
2. Filter: remove instances whose queued requests exceed the limit (requires `--worker-queue-limit`), and also those whose KV space cannot hold this request or whose running requests plus 1 would exceed `max_running_requests`.
3. Rank: compare how many new tokens each candidate still has to compute. When the gap exceeds 1024 tokens, the one that computes less wins. When the gap is small, compare load: if the instance with the most hits has 1024 or more queued tokens to compute than the alternative and 50% more, switch to the alternative. This step keeps a hot prefix from overwhelming one instance.
4. When there are no candidates at all, fall back to power-of-two selection by load.

#### With PD Disaggregation

- The prefill instance is chosen by `--policy`; with `cache_aware`, it is chosen by KV hits.
- The decode instance is chosen by `--decode-policy` (default `power_of_two`), which looks only at queued count, running count and KV usage, not prefix hits. The reason is that a decode instance's KV is sent by the prefill instance and does not depend on its local cache.
- The router sends the same bootstrap information (prefill address, port and a room number) to both sides, and they use it to set up the KV transfer connection.
- The prefill pool and decode pool are each discovered through k8s labels (matching the labels on the Service, with the router watching EndpointSlice); with `--pd-version-group-label` on, prefill of a version is paired only with decode of the same version. There is no automatic adjustment of the prefill/decode ratio; how many instances each pool has is decided by the deployment.

### sgl-router Traffic Splitting: Buckets, SLO, Session Affinity

Besides choosing instances by cache hits and load, sgl-router can also split traffic into different instance groups by request features:

- **Buckets by request length and SLO**: `--bucket-config` splits instances into several buckets, each declaring the input length range it can handle, its maximum context, and its estimated TTFT and throughput. A request first filters the buckets that can fit it by length, then tries them in SLO order; when one bucket is full it tries the next.
  - A request can carry its own latency target in the request headers `x-sgl-ttft-slo-ms` / `x-sgl-tps-slo`. In bucket-config, `slo_first` or `best_effort` can be set separately for TTFT and TPS (default `disabled`). For requests with an SLO header, `slo_first` tries the buckets that can meet the target first; `best_effort` first tries the buckets that do not promise to meet the target, leaving the compliant buckets for later. Requests without an SLO header are sorted only by the bucket's rank.
  - Whether a bucket can meet the SLO is judged by the static estimates written in the config; the router does not measure latency in real time, and there is no TPOT target.

- **DP awareness**: With `--dp-aware`, the router also picks the DP rank inside the instance (by default the one with the fewest in-flight requests).
- **Session affinity**: `session_aware` and `sticky` pin the same session to the same instance, raising cache hits in multi-turn dialogue; `balanced` mode (requires `--chat-routing reorg`) allows switching instances when the alternative's load is clearly lower: the load gap is more than 2×, and the absolute gap exceeds a threshold (1024 when comparing by prefill tokens).

### Cluster-Level Request Admission

**What sgl-router does not have**: global rate limiting (token bucket, maximum concurrency), router-side queuing, quotas per tenant or API key, request priority. One router serves only one model; several models each need their own setup.

**What sgl-router has**: admission based on instance load, with all thresholds off by default.

- In the default routing mode: `--worker-queue-limit` (stops dispatching to an instance once its queued requests reach the limit), `max_pending_prefill_tokens` for each bucket in `--bucket-config` (the limit on an instance's queued tokens waiting to be computed), `--filter overloaded` (a router-side limit on in-flight requests).
- `--chat-routing reorg` mode has more: `--max-inflight-requests`, `--max-kv-usage` (KV usage limit), `--max-running-usage`, `--max-waiting-requests`, `--max-pending-prefill-tokens`.
- These checks only read the load the instances report and do not reserve capacity; when load data is missing or stale, requests are let through by default.
- When no candidate instance qualifies, it returns 503 directly, without queuing at the router.
- Timeouts and retries: the request timeout defaults to 300 seconds; no retry by default (`--retry-max-attempts 1`). When enabled, it retries on an instance not yet tried, and only if nothing has been returned to the client yet; when the client disconnects, the router tells the instance to abort the request.

#### On the Mooncake Store Side

- **Multi-tenant quotas**: With `--enable_multi_tenants` on, each tenant has its own key space and memory quota (configured by a YAML file or etcd, and changeable online through the admin API). A write over quota is rejected directly (`TENANT_QUOTA_EXCEEDED`) without freeing space for it, and the caller retries; a separate background eviction thread also cleans up by tenant watermark. When the total quota exceeds cluster capacity, quotas are scaled down proportionally, and they are recomputed proportionally after a node goes offline too. Instances that share KV must use the same `tenant_id`.
- **Memory pool full**: The write fails directly (`NO_AVAILABLE_HANDLE`) and background eviction is triggered at the same time, without blocking to wait.
- **Queue backpressure**: When the SSD offload queue (50 thousand per local disk segment by default) is full, the master switches to forced eviction; when the promotion queue (50 thousand globally by default) is full, new tasks are rejected.
- There is no rate limiting of put/get.

### Mooncake Conductor: A Global Prefix Index

Mooncake has no request scheduler, only Conductor, a "global prefix index" that answers only "which instance has cached how much" and makes no routing decisions.

- **Role**: Subscribes to KV events from each inference instance (SGLang, vLLM) and the Mooncake Store master, and maintains a global table of "which instances each block is on, and in which tier". The tiers are GPU, local CPU, shared CPU (the Mooncake memory pool) and disk.
- **Query**: The router sends the request's tokens to Conductor, and Conductor walks down the prefix hash chain for each instance, returning how many tokens each instance can hit in each tier.
- **What it does not do**: It does not track load, score, choose instances or forward requests; all of that is left to the router calling it. The current sgl-router does not use Conductor either; it uses the KV events it subscribes to itself. Mooncake's own PD example proxy uses round-robin.
- **Defaults**: HTTP port 13333, RPC port 13334, at most 200 thousand blocks recorded per context, and beyond that the oldest are evicted down to 90%. It must be built with `-DWITH_CONDUCTOR=ON`.

The Conductor described in the Mooncake paper (FAST'25) combines cache hits, queue time and KV transfer cost to estimate TTFT and choose a prefill instance, and also replicates hot KV and rejects requests early under overload. None of this is implemented in the open-source code; only the prefix hit query part is.

### Load Balancing of Mooncake Data Placement

What is balanced here is where KV data is stored, not requests:

- **Choosing a location on write**: `allocation_strategy` by default picks memory segments at random, preferring segments on the writer's own machine; it can also be `free_ratio_first` (prefers segments with a high free ratio, for more even memory), `local_first` (prefers the local machine), and there are also `cxl` and `ssd_free_ratio_first`. Several replicas of the same object go on different segments.
- **Choosing a replica on read**: The local machine first, then remote replicas that match the NIC topology. This picks by proximity, not by load.
- **Hot-spot replication**: `dynamic_replication_mode` can be `off` (default), `observe` or `enforce`. By design, under `enforce`, an object accessed at more than 0.8 QPS in a 10-second window gets more memory replicas, up to 2, to spread hot read load.
- Existing data is not migrated for rebalancing.

## 14. Deployment Example and Tuning

### Minimal Deployment: SGLang + Mooncake as L3

Step 1: Start the Mooncake master (with its built-in metadata service):

```bash
mooncake_master --enable_http_metadata_server=true --http_metadata_server_port=8080 \
  --eviction_high_watermark_ratio=0.95
```

The master's RPC port defaults to 50051 and its monitoring port to 9003. When the metadata service is accessed across machines (Mooncake 0.3.14 and later), the metadata service, all SGLang processes and the store services must set the same `MC_METADATA_HTTP_TOKEN`; on a trusted network `MC_METADATA_HTTP_ALLOW_INSECURE=1` can be used instead. Note that this token check exists only in the standalone Python metadata service (`mooncake.http_metadata_server`), not in the metadata service built into `mooncake_master` (Step 1 above).

Step 2: (Optional) Start a separate store service to contribute memory. Without it, the SGLang processes contribute memory themselves (`global_segment_size` defaults to 4 GB):

```bash
python -m mooncake.mooncake_store_service --config=store.json --port=8081
```

`store.json` example: `{"local_hostname":"<local IP>","metadata_server":"http://<master IP>:8080/metadata","master_server_address":"<master IP>:50051","protocol":"rdma","device_name":"","global_segment_size":"4gb","local_buffer_size":0}`

Step 3: Start SGLang:

```bash
python -m sglang.launch_server --model-path <model path> --tp 8 --page-size 64 \
  --enable-hierarchical-cache --hicache-ratio 2 \
  --hicache-mem-layout page_first_direct --hicache-io-backend direct \
  --hicache-write-policy write_through --hicache-storage-prefetch-policy timeout \
  --hicache-storage-backend mooncake \
  --hicache-storage-backend-extra-config '{"master_server_address":"<master IP>:50051","local_hostname":"<local IP>","metadata_server":"http://<master IP>:8080/metadata","global_segment_size":"100gb","protocol":"rdma","device_name":""}'
```

Environment variables can be used instead of extra-config: `MOONCAKE_MASTER`, `MOONCAKE_TE_META_DATA_SERVER` (metadata service address), `MOONCAKE_PROTOCOL`, `MOONCAKE_DEVICE`, `MOONCAKE_GLOBAL_SEGMENT_SIZE`, `MOONCAKE_LOCAL_HOSTNAME`, `MOONCAKE_TENANT_ID`. Priority: extra-config (takes effect only when it contains `master_server_address` or `client_server_address`) > config file (`SGLANG_HICACHE_MOONCAKE_CONFIG_PATH`) > environment variables. Exception: `local_hostname` follows the environment variable `MOONCAKE_LOCAL_HOSTNAME` first, then `LOCAL_HOSTNAME`.

Step 4: To turn on SSD offload, add `"enable_ssd_offload": true` to extra-config, set the environment variable `MOONCAKE_OFFLOAD_FILE_STORAGE_PATH` (the SSD directory, read by Mooncake directly), and turn on `--enable_offload` on the master side. Note: when configuring through extra-config, SGLang does not read the environment variable `MOONCAKE_ENABLE_SSD_OFFLOAD` and only takes its default (off).

For a PD disaggregated deployment, the official best practices give two setups: HiCache on the prefill instances only; or additionally asynchronous write-out on the decode instances (`--disaggregation-decode-enable-offload-kvcache`).

### Tuning Points

- **Use the `rdma` protocol**: When SGLang embeds Mooncake, `MOONCAKE_PROTOCOL` already defaults to `rdma`; but a separately deployed `mooncake_client` and Mooncake's own Python config default to `tcp` and must be configured explicitly. Leaving `device_name` empty discovers NICs automatically; it can also be written as `"mlx5_0,mlx5_1"` (check with `ibv_devices`).
- **Configure layout and io-backend in pairs**: `page_first` goes with `kernel`, and `page_first_direct` with `direct`. The regular path of the Mooncake backend does not support `layer_first`. When using `direct`, setting `SGLANG_ENABLE_MLP_SYNC_METADATA_FILL=1` is recommended.
- **L2 should be larger than L1**: When L2 is too small, data prefetched from L3 has nowhere to go, and `storage_prefetch_unfulfilled_tokens_total{reason="host_capacity"}` rises in monitoring. When a small model runs on a large-memory GPU, the default 2× L2 may take too much memory; lower `--hicache-ratio` or use `--hicache-size` directly.
- **Prefetch policy**: `timeout` is recommended for production.
- **Master eviction watermark**: The doc example uses 0.95; lower it when allocation failures are frequent (memory fragmentation makes allocation fail before memory is full).
- **Hugepage memory**: Set `MC_STORE_USE_HUGEPAGE=1` and `MC_STORE_HUGEPAGE_SIZE=2MB`, and allocate them in advance with `sysctl -w vm.nr_hugepages=...`; once turned on, there must be enough, since it does not fall back to normal pages. The Mooncake repository has a script, `scripts/check_hicache_hugepage_requirements.py`, that estimates how many are needed.
- **Running in containers**: Add `--ipc=host --ulimit memlock=-1` and a large enough `--shm-size`; registering memory for RDMA may need root privileges.
- **Registered memory limit**: Environments such as eRDMA cap the total memory that can be registered with the NIC. Both the whole L2 and `global_segment_size` must be registered; when over the limit, lower one of them.

## 15. Results and Where It Fits

### Published Test Results

The Mooncake repository has a test of SGLang HiCache (charts only, with no exact numbers given):

- **Workload**: Multi-turn dialogue, where each turn's input contains the inputs and outputs of all previous turns.
- **Four configurations compared**: GPU only; GPU + L2; GPU + L2 + Mooncake; and Mooncake filled in advance. The metrics are time to first token (TTFT), input token throughput and the cache hit rate of each turn.
- **Environment**: One setup is 3 machines, each with 2 A10s and 2 × 100 Gbps eRDMA, running Qwen3-14B TP2; the other is 1 machine with 8 H800s running Qwen3-235B TP8.
- **Conclusions**:
  - Prefill performance: Mooncake filled in advance > GPU + L2 + Mooncake > GPU + L2 > GPU only.
  - In turns 1~3 all have the same hit rate, and GPU + L2 is actually slightly faster than with Mooncake, because no remote read is needed. This is the overhead of the extra tier.
  - As the dialogue grows and KV exceeds L2, the L2 hit rate falls and TTFT rises; the configurations with Mooncake keep a higher hit rate and TTFT grows slowly.
  - The gain comes from L3's cluster-level capacity and from sharing KV between instances.

There is also a PD disaggregation test: peak KV transfer bandwidth was about 164 GB/s (82% of line rate), and for a 32K-token request, KV transfer took only 2.4% of TTFT.

### Where the Gain Is Large

- **Multi-turn dialogue, agents**: Each turn carries all the earlier context, the prefix repetition rate is high, and the total soon exceeds one machine's GPU and L2.
- **Long system prompts, long-document QA, RAG**: Many requests share the same long prefix (the same prompt or the same set of documents).
- **Several instances sharing hot prefixes**: KV computed by one instance is written to L3, and other instances read it directly.
- **After an instance restarts or scales out**: A new instance can read existing KV straight from L3 instead of warming up from zero.

### Where the Gain Is Small or There Is Extra Overhead

- **Requests share almost no prefixes** (every request is a brand-new short input): The cache basically never hits, and backing up to L2/L3 is pure overhead. `write_through_selective` can be considered, to back up only reused prefixes.
- **The working set is small and fits in L2**: Adding L3 only adds a remote read, slightly slower than L2.
- **Slow network (no RDMA, TCP only)**: Reading back from L3 may be slower than recomputing, especially for small models.
- **Very short hit prefixes**: Below the prefetch threshold (default 256 tokens) nothing is fetched from L3, and below 10 tokens nothing is loaded from L2; it is recomputed directly.

## 16. Monitoring and Troubleshooting

### On the SGLang Side (Add `--enable-metrics` at Launch, Prometheus Format)

- **Hits**:
  - `sglang:cache_hit_rate`: total prefix cache hit rate.
  - `sglang:cached_tokens_total{cache_source}`: hit tokens by source, with `device` / `host` / `storage` for L1 / L2 / L3 (`total` appears only as a fallback when there is no per-source data, and is not the sum of the three). This is the main one to watch to see how many hits each tier contributes.

- **L2 usage**: `sglang:hicache_host_used_tokens` / `sglang:hicache_host_total_tokens`.
- **L3 reads and writes**:
  - `sglang:prefetched_tokens_total` (tokens read back from L3), `sglang:backuped_tokens_total` (tokens written to L3).
  - `sglang:prefetch_bandwidth` / `sglang:backup_bandwidth`: the bandwidth distribution of each read and write.
  - `sglang:storage_prefetch_hit_tokens_total`: the tokens an L3 query reports it can hit.

- **Hit but not used**: `sglang:storage_prefetch_unfulfilled_tokens_total{reason}`, with 12 reasons in total; common ones are:
  - `host_capacity`: no room in L2, meaning L2 is too small.
  - `deadline`: the prefetch timed out and compute started before the read finished, meaning L3 reads are too slow or the timeout is too short.
  - `below_threshold`: the hit length is below the prefetch threshold.

- **Failures**: `sglang:hicache_storage_backup_failed_tokens_total` (failed writes to L3), `sglang:hicache_backup_dropped_tokens_total` (in buffer mode, backups dropped by admission control or whose source data has become invalid).
- SGLang's own Grafana dashboard has only the hit rate; panels for the HiCache metrics have to be added yourself.

### On the Mooncake Side

- **master**: Port 9003; `/metrics` is Prometheus format, `/metrics/summary` is a readable summary, and there are also `/health` and `/ha_status`. Commonly watched:
  - Capacity: `master_allocated_bytes` / `master_total_capacity_bytes` (how much of the memory pool is used).
  - Key count and online clients: `master_key_count`, `master_active_clients`.
  - Eviction: `master_evicted_key_count`, `master_evicted_size_bytes`; the allocation failure count is also in the summary.

- **client**: The monitoring endpoint is off by default and must be turned on separately (for example, set `MOONCAKE_ENABLE_CLIENT_HTTP_SERVER=true` for the store service). It shows the heartbeat status with the master, read and write latency and so on. No documentation was found on how to turn on monitoring for the Mooncake client embedded in the SGLang process, and the SGLang code has no place that turns it on.
- **Ready-made dashboards**: The `monitoring/` directory of the Mooncake repository has a docker-compose setup that starts Prometheus (9090) and Grafana (3000) with one command, with dashboards for the master and core metrics included.

### How to Troubleshoot Common Problems

- **Low L3 hit rate**: First check whether `cached_tokens_total{cache_source="storage"}` has values; then confirm that the sharing instances have the same model name, TP, page size, KV data type and `tenant_id` (different keys never hit); then check whether the master's eviction volume is large (not enough capacity).
- **TTFT does not improve**: Check whether `unfulfilled{reason="deadline"}` is high (L3 reads too slow), and confirm the actual protocol is `rdma` and has not been changed to `tcp` by environment variables or a standalone `mooncake_client` (default `tcp`).
- **Many write failures**: Check the master's allocation failure count and usage, and add memory or lower the eviction watermark if needed.

## 17. Large-Cluster Deployment

### Can It Be Deployed on a Large Cluster

Yes, but the two parts differ in maturity:

- **SGLang inference side**: There are multi-machine deployment setups. One model instance can do TP/EP across machines (such as Llama 405B on TP16 across 2 machines, or large-scale EP for DeepSeek), and several instances form a PD disaggregated cluster. The docs give examples of deploying DeepSeek PD on k8s with LWS (LeaderWorkerSet) and RBG (RoleBasedGroup). Scales like 96 H100s running DeepSeek or 128 H200s running Kimi K2 appear only in external blogs; the repository docs have no complete configuration for them.
- **Mooncake Store**: Data moves directly between clients and the master handles only metadata, so the data plane scales horizontally. But the repository does not state how many nodes are supported. Most published benchmarks use 2 to 3 machines, and the largest is the 60 GPUs mentioned in the vLLM integration docs. Metadata is managed by a single master, not sharded; for Transfer Engine's metadata service, P2P handshake works at small scale, and etcd or Redis is recommended at large scale or for long-running setups.

### Scaling and High Availability

#### SGLang Inference Instances

- **Scaling out**: There are two ways. One is k8s service discovery (`--service-discovery`, selecting by Service labels; PD mode uses `--prefill-selector` / `--decode-selector` separately): once a new Pod is ready, the router adds it automatically and reads the model and PD information from its `/model_info` (falling back to `/server_info`). The other is the HTTP admin API `POST /workers`, `PUT /workers/{id}`, `DELETE /workers/{id}` (added 2026-11-21; requires `--worker-management-api-key`, and changes carry an `If-Match` version). With only a static `--worker-urls` configuration and the admin API off, the instance list is fixed at startup.
- **Scaling in**: When a Pod is removed, the router immediately stops sending it new requests and clears its KV cache state; requests already sent run to completion. The router does not actively drain instances; graceful exit relies on k8s first marking the Pod not ready, and on the instance's own exit handling.
- **Failures**: There is no active health probing; a circuit breaker is used instead: 3 consecutive failures open the circuit, and after 30 seconds one request is let through as a probe. Instances returning 503 / 429 / 500 count as a neutral result, not as failures.
- **The router itself**: The router is stateless and can be deployed as several replicas behind a load balancer, each replica subscribing independently to the instances' KV events and load information. A new replica can copy the KV state from a running replica before going online (peer bootstrap), to avoid inaccurate cache hit judgments on a cold start. Session bindings are kept in each replica's memory, so with several replicas the load balancer in front must be sticky by the session header.

#### Mooncake Store

- **Scaling out**: Start a new client that mounts its memory segment, and the master includes it in allocation automatically.
- **Scaling in/failures**: Clients send heartbeats to the master every second. With no heartbeat for over 10 seconds (`client_active_ttl_sec`), the master first marks it as suspected lost; if it has not recovered after another 20 seconds (`client_suspicion_ttl_sec`), it is judged offline, its memory segments are unmounted, and the replicas on those segments are deleted. By default it takes about 30 seconds from disconnect to unmount. Data is kept only if other nodes still have replicas, and the system does not add replicas automatically. There is a "graceful unmount" API (waits for a grace period before unmounting), but it does not migrate data to other nodes. For KV cache, lost data only means recomputing next time; it does not affect correctness.
- **Master high availability**: A single master by default, which is a single point of failure. With `--enable_ha` on, etcd (or k8s lease, or the experimental Redis) is used for leader election, and the standby master stays in sync through the operation log (OpLog, requires `--enable_oplog=true`) and snapshots (requires `--enable_oplog_snapshot`) (both are off by default; only the etcd backend does full primary-standby replication, and k8s lease does only leader election). When the primary goes down the standby takes over, and clients remount their memory segments after being notified. With the etcd backend, the leader lease `ha_leader_lease_ttl_sec` defaults to 5 seconds; the total failover time is not documented.
- **k8s**: Only plain Deployment/Service examples (1 master + 3 stores) and docs on integrating with RBG and llm-d are provided; there is no Helm chart or Operator.

### Summary and Gaps

- It can go on large clusters: the inference side has k8s (LWS/RBG) setups and multi-machine TP/EP/PD, and the data plane of KV storage scales.
- Scaling: inference instances join and leave through k8s service discovery or the router's admin API; Mooncake nodes can join at any time, and when they go offline their data is simply dropped, with no migration and no added replicas.
- Admission and scheduling: there is load-based admission, bucketing by length/SLO, and separate PD pools, but no global rate limiting, no per-tenant request quotas, no priority queuing, and no closed loop that adjusts routing by real-time latency. The cluster-level scheduling in the Mooncake paper (choosing instances by estimated TTFT, hot-spot replication, early rejection under overload) is not implemented in the open-source code.
- Single-point and scale risks: Mooncake has a single master by default with unsharded metadata, so HA needs to be turned on; the repository has no large-scale load test data.

## 18. Comparison With Other Approaches

### LMCache

LMCache is a standalone KV cache service, originally used mainly with vLLM, that manages several storage tiers itself, such as CPU memory, local disk and remote storage.

- **Use in SGLang**: `--enable-lmcache`. SGLang keeps its own radix tree as the index and hands all storage below L2 to a separate LMCache process, with KV loaded from LMCache straight to the GPU.
- **Mutually exclusive with HiCache**: It cannot be used with `--enable-hierarchical-cache`. One way to see it: either use SGLang's own HiCache (L2 + one L3 backend, such as Mooncake), or outsource the whole multi-tier storage to LMCache.

### vLLM + Mooncake

Mooncake can also work with vLLM, through vLLM's KV connector interface, in two forms:

- `MooncakeConnector`: Only does the prefill → decode KV transfer in PD disaggregation (RDMA).
- `MooncakeStoreConnector`: Uses Mooncake Store as a distributed KV pool shared by several vLLM instances, sharing prefixes by block hash, with support for offloading to CPU / disk.

### How to Think About Their Relationship

- **Mooncake** is the "transfer layer + shared storage layer" in both engines, sitting below the engine's own cache management. In SGLang it is one L3 backend of HiCache; in vLLM it is a KV connector.
- **SGLang HiCache** handles the GPU and Host tiers and the radix tree index, and L3 can switch backends (Mooncake, 3FS, local files, NIXL and so on).
- **LMCache** is a complete external cache service that replaces HiCache's L2 and everything below it in SGLang.
- The prefix indexes differ: SGLang uses a radix tree, and vLLM uses a hash table over fixed-size blocks. Both can reuse prefixes; SGLang's radix tree suits cases with many branches better (such as multi-turn dialogue and agents with multiple branches).

## 19. Default Values of Key Parameters

- **SGLang capacity and format**: `--mem-fraction-static` computed automatically (usually around 0.85 or lower on an 80 GB GPU), `--kv-cache-dtype auto`, `--page-size` (default 1 on CUDA; many models and backends change it automatically to 64 or 128), `--hicache-host-memory-fraction 0.8`, `--hicache-storage-key-scheme rank-suffix`.
- **SGLang PD disaggregation**: `--disaggregation-transfer-backend mooncake`, `--disaggregation-bootstrap-port 8998`, bootstrap and transfer-wait timeouts of 300 seconds each.
- **SGLang**: `--hicache-write-policy write_through`, `--hicache-storage-prefetch-policy timeout`, `--radix-eviction-policy lru`, `--hicache-ratio` (Host pool size relative to the GPU pool; when not set, 2.0 in normal mode, 1.2 in `buffer_only` mode, 0.2 for decode instances that only do retraction backup, and possibly lowered by `--hicache-host-memory-fraction`), `--hicache-io-backend kernel`, `--hicache-mem-layout page_first`, `--schedule-policy fcfs`, `--schedule-conservativeness 1.0`, `--retraction-policy length`.
- **sgl-router**: `--policy round_robin` (`power_of_two` with `--chat-routing reorg`), `--decode-policy power_of_two`, `--request-timeout-secs 300`, `--retry-max-attempts 1` (no retry), circuit breaker `--cb-threshold 3` / `--cb-cool-down-secs 30`.
- **Mooncake**: in SGLang, `MOONCAKE_PROTOCOL` defaults to `rdma`, `MOONCAKE_GLOBAL_SEGMENT_SIZE` to 4 GB, and `MOONCAKE_TE_META_DATA_SERVER` to `P2PHANDSHAKE` (the standalone `mooncake_client` defaults to the `tcp` protocol); master parameters `eviction_high_watermark_ratio 0.9`, `eviction_ratio 0.05`, `default_kv_lease_ttl 10000 ms`, `default_kv_soft_pin_ttl 30 minutes`, `enable_offload false`, `offload_on_evict false`, `promotion_on_hit false`, `allocation_strategy random`, `dynamic_replication_mode off`, `enable_ha false`, `client_active_ttl_sec 10`, `client_suspicion_ttl_sec 20`.

## 20. Code Locations

- SGLang (under `sglang/python/sglang/srt/`):
  - Storage tiers: `mem_cache/`; L3 interface `mem_cache/hicache_storage.py`, Mooncake backend `mem_cache/storage/mooncake_store/`, 3FS backend `mem_cache/storage/hf3fs/`.
  - Radix tree: `mem_cache/unified_cache/unified_tree_core.py` (`UnifiedTreeNode`), `mem_cache/unified_cache/components/base.py` (`ComponentData`).
  - Transfer and eviction: `managers/cache_controller.py`, `mem_cache/unified_radix_cache.py`, `mem_cache/evict_policy.py`.
  - L1 ↔ L2 copies: `mem_cache/l2_transfer.py`, `mem_cache/pool_host/`; the copy kernel is in `sglang/python/sglang/kernels/aot/csrc/kvcacheio/transfer.cu`; automatic adjustment of io-backend and layout is in `arg_groups/hicache_hook.py`.
  - L3 direct mode: `mem_cache/storage/mooncake_store/mooncake_direct_linker.py`.
  - Overlapping compute and transfer: the layer-wise load counters are in `managers/cache_controller.py` (`LayerDoneCounter`) and `mem_cache/unified_cache/unified_cache_linker.py` (`LayerWiseLoadCounter`); the stream fences are set in `managers/scheduler.py`; PD KV sending is in `disaggregation/prefill.py` and `disaggregation/mooncake/conn.py`.
  - Scheduling: `managers/scheduler.py`, `managers/schedule_policy.py`; KV event publishing: `mem_cache/events.py`, `disaggregation/kv_events.py`.
  - Parameter definitions: `arg_groups/fields/memory.py`, `arg_groups/fields/schedule.py`.

- SGLang, other (under `sglang/python/sglang/srt/`):
  - Capacity calculation: `model_executor/pool_configurator.py`, `mem_cache/kv_cache_configurator.py`, `mem_cache/hicache_auto_size.py`; KV data types: `mem_cache/kv_cache_dtype.py`.
  - L3 keys: `mem_cache/utils.py` (hash seed), `mem_cache/cpp_utils/hash_binding.cpp` (chained SHA-256 hash), `mem_cache/hicache_key_scheme.py` (unified key scheme), `mem_cache/storage/mooncake_store/mooncake_store.py` (key assembly).
  - Consistency: `mem_cache/kv_weight_version_tracker.py`, `managers/scheduler.py` (`flush_cache`).
  - PD disaggregation: `disaggregation/` (`prefill.py`, `decode.py`, `mooncake/conn.py`, `decode_hicache_mixin.py`); parameters in `arg_groups/fields/disagg.py`, timeouts in `environ.py`.
  - Special cases: `mem_cache/unified_draft_pool.py` (draft KV), `managers/req_types.py` (multimodal pad values), `mem_cache/embedding_cache_controller.py` (embedding cache), `mem_cache/hisparse_memory_pool.py`, `mem_cache/storage/lmcache/`.
  - Monitoring metrics: `observability/metrics_collector.py`.

- sgl-router: `sglang/sgl-router/src/policies/` (`cache_aware.rs`, `admission.rs`), service discovery `src/discovery/k8s.rs`, buckets `src/buckets_reorg.rs`, parameters `src/config/cli.rs`; k8s deployment docs `sglang/docs/docs/references/multi_node_deployment/`.
- Mooncake (under `Mooncake/`):
  - Replica types: `mooncake-store/include/allocator.h`; memory pool allocation: `mooncake-store/src/common/client_buffer_allocation.cpp`.
  - Eviction: `mooncake-store/src/master_service.cpp`, `mooncake-store/src/eviction/`; SSD offload: `mooncake-store/src/file_storage.cpp`; parameter definitions: `mooncake-store/src/master.cpp`.
  - Transfer: Transfer Engine protocols in `mooncake-transfer-engine/src/multi_transport.cpp` and `mooncake-transfer-engine/src/transport/`; Store read/write path selection in `mooncake-store/src/transfer_task.cpp`; disk-tier I/O in `mooncake-store/src/storage_backend.cpp` and `mooncake-store/src/storage/distributed/`; NoF SSD in `mooncake-store/src/nof/`.
  - Deployment, tuning, test and monitoring docs: `docs/source/deployment/integrations/sglang/`, `docs/source/performance/sglang/`, `docs/source/getting_started/observability.md`, `monitoring/`; SGLang-side best practices `sglang/docs/docs/advanced_features/hicache_best_practices.mdx`.
  - Conductor: `mooncake-conductor/`, design doc `docs/source/design/conductor/conductor-architecture-design.md`.
  - Node offlining and HA: `mooncake-store/src/master_service.cpp` (`ProcessClientOffboardingJob`, `GracefulUnmountSegment`); multi-tenancy: `mooncake-store/src/tenant/`, `docs/source/deployment/multi-tenancy.md`; k8s deployment: `docs/source/deployment/kubernetes-deployment-guide/`.
