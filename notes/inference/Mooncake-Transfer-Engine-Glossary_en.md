# Mooncake Transfer Engine Source Code Reading Glossary

[中文](./Mooncake-Transfer-Engine-Glossary.md) | English

- **Compiled**: 2026-11-20
- **Scope**: The hardware, networking, RDMA and Transfer Engine terms you need to read the Mooncake Transfer Engine (`mooncake-transfer-engine/`) source, plus the call chain of one RDMA WRITE from submission to completion.
- **Code versions**: [kvcache-ai/Mooncake](https://github.com/kvcache-ai/Mooncake/tree/301261358eef0b13fa55645ccde4a988f1ca7505) main branch `30126135` (2026-11-20), [sgl-project/sglang](https://github.com/sgl-project/sglang/tree/94d3dbad27dcb10ca0e83ec5ccac3c87f6c1e0ca) main branch `94d3dbad27` (2026-11-13). The file:line references in Sections 7 and 8 all refer to these two commits.
- **Basis**: Reading the code at those two commits and the Mooncake docs; not verified by running it.

Each term gets a plain-language explanation, most with an example or analogy. Source locations appear only in Sections 7 and 8, where `TE/` stands for `Mooncake/mooncake-transfer-engine/`.

Acronyms are followed by their full English name in parentheses (the Chinese version adds a Chinese translation). When one term contains several acronyms, each is written as acronym = full name. Product and library names have no standard translation, so the parentheses give a short description instead. MUSA, MACA, CXI and EID are vendor-specific acronyms with no reliable source for their expansions, so they are left unexpanded.

## 0. The Big Picture

### 0.1 The TE RDMA Path in One Sentence

The RDMA (Remote Direct Memory Access) data path of TE (Transfer Engine) is **one-sided**: the initiator works out the peer's memory address and rkey itself, and the local NIC writes data straight into (or reads it out of) the peer's memory, while the peer's CPU takes no part and receives no notification.

So everything the "receiver" does happens before the transfer: register memory, publish metadata, and accept connections passively. After the transfer, a separate message has to tell it that the data has arrived.

### 0.2 Object Hierarchy

```text
TransferEngine                     Public API (TE/include/transfer_engine.h)
 └─ TransferEngineImpl             Classic implementation; MC_USE_TENT=1 switches to TE/tent/
     ├─ TransferMetadata           Segment descriptors, handshake, notify (metadata plane)
     └─ MultiTransport             Picks a backend by the peer's protocol
         ├─ RdmaTransport          RDMA backend: registers memory, cuts slices, picks the local NIC
         │   └─ RdmaContext × one per local NIC     PD, MR, CQ, WorkerPool, EndpointStore
         │       ├─ WorkerPool               worker threads: post send + poll CQ
         │       └─ RdmaEndPoint × one per peer NIC  holds num_qp_per_ep RC QPs
         ├─ TcpTransport
         └─ NvlinkTransport / ShmTransport / ...
```

### 0.3 Suggested Reading Order

Read Section 3 (RDMA) and Section 4 (TE's own concepts) first, then read the source alongside the call chain in Section 7. Look up Sections 1 and 2 when you hit an unfamiliar term, and read Section 5 only when you work with other hardware.

---

## 1. Hardware and Operating System Basics

| Term | Explanation |
| --- | --- |
| DRAM (Dynamic Random Access Memory) | The server's main memory, the memory modules plugged into the motherboard, which the CPU reads and writes directly and which loses its data when powered off. "Host memory" in this glossary means DRAM. The GPU's own memory is VRAM (Video Random Access Memory); on data-center GPUs it is HBM (High Bandwidth Memory), much faster than DRAM but much smaller. Example: in TE, location `cpu:0` means DRAM on NUMA node 0, and `cuda:0` means the memory of GPU 0. |
| PCIe (Peripheral Component Interconnect Express) | The bus inside a server that connects the CPU, GPUs and NICs; devices move data to each other over it. Example: when a NIC reads GPU memory, the data travels over PCIe from the GPU to the NIC, then out onto the network. |
| PCIe distance / PCIe switch | How many hops apart two devices are in the PCIe tree. A GPU and a NIC under the same PCIe switch are closest and transfer fastest. Example: if GPU0 and mlx5_0 sit under the same switch, GPU0's data should go through mlx5_0 first. |
| NUMA node (Non-Uniform Memory Access node) | In a multi-socket server, each CPU socket has its own bank of memory. A CPU reaches its own bank quickly and the other bank slowly, across sockets. Example: a NIC attached to node0 reads node0's memory faster than node1's. |
| DMA (Direct Memory Access) | A device reads and writes memory by itself, without the CPU copying byte by byte. Analogy: the CPU only places the order, and the device fetches the goods from the warehouse itself. |
| Virtual address / physical page | Programs see virtual addresses, while data actually sits in pages of physical memory (usually 4 KB each), and the operating system keeps the mapping between them. Devices don't understand virtual addresses, so they must be told in advance which physical pages a virtual range maps to. |
| Pinned memory (page-locked memory) | Memory that is fixed in place: the operating system won't swap it out or move it. The NIC reads and writes by physical address, so if a page moved midway, the NIC would hit the wrong location. Example: after 1 GB of memory is registered with the NIC, that 1 GB stays at the same physical location until it is unregistered. |
| IOVA (I/O Virtual Address) | The address used on the device side, numbered separately from the program's virtual addresses and translated by hardware. |
| GPUDirect RDMA (GDR) | The NIC reads and writes GPU memory directly, without staging through host memory. Example: without GDR, the KV Cache (Key-Value Cache) must first be copied from GPU memory to host memory before sending; with GDR, the NIC reads it straight from GPU memory. |
| nvidia-peermem (NVIDIA peer memory) | A kernel module that lets the RDMA NIC driver register GPU memory. Without it (and without dma-buf), the NIC can only register host memory. |
| dma-buf (DMA buffer sharing) | The Linux mechanism that lets different device drivers share one buffer. The GPU driver exports GPU memory as an fd (file descriptor), and the NIC driver registers it using that fd. It is the alternative to nvidia-peermem. |
| BAR (Base Address Register) / BAR1 | A "window" the GPU opens in the PCIe address space, through which the NIC reaches GPU memory. The window is limited in size, and registering too much GPU memory can fill it up. |
| PCIe Relaxed Ordering | Lets write requests on PCIe complete out of the order they were issued. With the ordering requirement relaxed, writes to GPU memory get faster on some platforms. |
| Data Direct | A feature of some NVIDIA NICs: the NIC opens an extra DMA entry point on the PCIe branch where the GPU sits, so reads and writes of GPU memory take a shorter path. |
| CUDA IPC handle (CUDA = Compute Unified Device Architecture; IPC = Inter-Process Communication) | On the same machine, one process turns a piece of its GPU memory into a "claim ticket" and hands it to another process, which then uses it to access that GPU memory directly. Example: two inference processes on the same machine use it to copy KV directly between GPUs. |
| CUDA VMM (Virtual Memory Management) | A set of CUDA APIs that splits "allocate physical GPU memory" and "map it to a virtual address" into two steps. Once they are split, a piece of physical GPU memory can be exported for other processes, or even other nodes, to map. |
| Fork safety | When a process forks a child, memory pages registered with the NIC may be copied or changed, so the NIC reads and writes the wrong place. The RDMA library provides a dedicated initialization function to avoid this. |

---

## 2. Networking Basics

| Term | Explanation |
| --- | --- |
| Gb/s and GB/s (gigabits / gigabytes per second) | NIC speeds are counted in bits, while programs usually count in bytes, and 1 byte = 8 bits. Example: a 400 Gb/s NIC tops out at about 50 GB/s. |
| Latency, bandwidth, in-flight data | To fill the bandwidth, enough data must be on the wire at the same time, namely the BDP (Bandwidth-Delay Product) = bandwidth × RTT (Round-Trip Time). Example: 50 GB/s × 10 µs = 500 KB, which is why TE cuts transfers into slices and sends over several connections in parallel. |
| TCP (Transmission Control Protocol) / socket | A reliable byte-stream connection provided by the operating system, in which data passes through kernel copies. TE uses it to exchange connection setup information and send small messages; without RDMA NICs, it also carries the data. |
| RPC port (RPC = Remote Procedure Call) | A TCP port a process opens to the outside, which other processes connect to for service. In TE, the peer connects to this port to exchange connection setup information. |
| epoll (event poll) | The Linux interface that lets one thread watch many connections or devices at once and handle whichever one has activity. |
| asio (Asynchronous I/O) | A C++ asynchronous networking library: a read or write is issued without blocking, and a callback handles the data when it arrives. TE's TCP backend uses it. |
| etcd (distributed key-value store) | A distributed key-value database built for configuration and metadata: the data is stored on several machines at once, it keeps working when a minority of them fail, and every reader sees the same latest value. Kubernetes stores its whole cluster state in it. The name comes from the Unix `/etc` directory, where configuration lives, plus d (distributed). In TE it can serve as the metadata backend. Example: every process is initialized with `etcd://10.0.0.1:2379`, writes its own segment descriptor into it, and looks up other processes by segment name. |
| Redis / HTTP metadata services (Redis = Remote Dictionary Server; HTTP = HyperText Transfer Protocol) | Two other metadata backends that do the same job as etcd: each process writes "who I am and where my memory is" into one, and other processes look it up by name. Redis is a widely used in-memory key-value database, and the HTTP backend is a simple web service that stores and fetches data by URL. Example: process A writes its information under its own name as the key, and process B reads it by A's name. |
| ZMQ (ZeroMQ) | A lightweight inter-process messaging library. Example: in SGLang's PD disaggregation (Prefill-Decode disaggregation), P sends a "transfer done" message to D over ZMQ after transferring the KV. |
| IB (InfiniBand) | A complete network built for RDMA, with dedicated NICs, switches and cables, where a Subnet Manager (SM) assigns addresses centrally. |
| RoCE (RDMA over Converged Ethernet) / RoCEv2 | RDMA running over ordinary Ethernet. RoCEv2 wraps RDMA in UDP (User Datagram Protocol) / IP (Internet Protocol) packets, so it can be routed across subnets like ordinary IP traffic. Data centers mostly use RoCEv2. |
| LID (Local Identifier) | A 16-bit short address for each port on an IB network, assigned by the subnet manager, like a house number within the subnet. RoCE doesn't use LIDs. |
| GID (Global Identifier) / GID table / GID index | The 128-bit global address of an RDMA port; under RoCE it is just the NIC's IP written another way. Example: the GID for IP 10.0.0.1 is `::ffff:10.0.0.1`. A port's GID table often holds several rows for the same IP (one for RoCEv1, one for RoCEv2), and the GID index picks which row; the wrong row often means no connection. |
| GRH (Global Route Header) | The part of the packet header that carries the GID, which routing across subnets depends on. Every RoCE packet carries a GRH. |
| Port | A physical interface on the NIC. A NIC has 1 or 2 ports, numbered from 1. |
| MTU (Maximum Transmission Unit) | The most data one network packet can carry; for RDMA the maximum is 4096 bytes. Example: with an MTU of 4096, the NIC splits 64 KB of data into 16 packets. |
| PKey (Partition Key) | The "group number" of an IB network. Only ports in the same partition can talk to each other, which isolates tenants. |
| SL / TC / DSCP (SL = Service Level; TC = Traffic Class; DSCP = Differentiated Services Code Point) | Priority markings on a packet, which the switch uses to put it into different queues. Example: mark RDMA traffic with a particular TC, and the switch puts it into the lossless queue. |
| PFC / ECN / DCQCN (PFC = Priority-based Flow Control; ECN = Explicit Congestion Notification; DCQCN = Data Center Quantized Congestion Notification) | The three mechanisms RoCE relies on against packet loss and congestion. PFC: a switch tells upstream to pause when its queue is nearly full. ECN: a switch marks packets when congested. DCQCN: the receiver sees the mark and tells the sender, which slows down. These are configured on NICs and switches; in programs they usually show up only as priority settings. |
| ECMP (Equal-Cost Multi-Path) and the UDP source port | When there are several equally good paths between two machines, the switch hashes the packet header to choose one. RoCEv2's UDP source port goes into the hash, so giving different connections different source ports spreads the traffic over different paths. |
| Bonding / LAG (Link Aggregation Group) | Binds two physical ports of a NIC into one logical port: the bandwidth adds up, and if one port fails the other still works. |
| Rail | A way of wiring multi-NIC clusters: the i-th NIC of every machine connects to the same group of switches, called rail i. Example: every machine's mlx5_0 is on rail 0 and its mlx5_1 on rail 1. In the TE source, a rail means the path "a given local NIC to a given peer NIC". |
| Multi-NIC (NIC = Network Interface Card) | A GPU server often has 4 to 8 high-speed NICs, and data can go out of several at once, adding up their bandwidth. Example: each 400 Gb/s NIC is about 50 GB/s, so 8 of them total about 400 GB/s. |

---

## 3. RDMA and Verbs Programming (Most Important)

The RDMA programming interface is called **verbs**, its library is libibverbs (part of rdma-core), and the function prefix `ibv_` is short for InfiniBand Verbs. NVIDIA (Mellanox) NICs have an extension interface, `mlx5dv_` (mlx5 Direct Verbs).

**Example**: process A wants to write 1 MB of local data into process B's GPU memory:

1. B registers this GPU memory as an MR, gets an rkey, and tells A the memory address and the rkey.
2. A also registers the memory holding its data as an MR and gets an lkey.
3. A and B each create a QP, exchange QP numbers, and pair the two QPs.
4. A puts a WR into the QP ("write this local 1 MB to this address on B, and the key is this rkey"), then rings the doorbell to notify the NIC.
5. When the write finishes, the NIC puts a completion record into the CQ; A takes it out and knows the write is done. B's CPU takes no part at any point.

### 3.1 Basic Objects

| Term | Explanation |
| --- | --- |
| HCA / RNIC / device name (HCA = Host Channel Adapter; RNIC = RDMA-enabled NIC) | Both mean a NIC that supports RDMA. It is called an HCA on IB networks and an RNIC on Ethernet. On Linux the names look like `mlx5_0`, `mlx5_1`. |
| mlx5 (Mellanox NIC driver name) | The Linux driver name for NVIDIA (formerly Mellanox) RDMA NICs; mlx is short for Mellanox. ConnectX-4 and later models (ConnectX-5, 6, 7 and so on) all use this driver, while the older ConnectX-3 uses mlx4, so the digit 5 has nothing to do with the NIC model. The driver names the NICs in order, `mlx5_0`, `mlx5_1` and so on, and functions starting with `mlx5dv_` are this driver's own extension interface. Example: a machine with 8 ConnectX-7 NICs usually shows `mlx5_0` through `mlx5_7`. |
| `ibv_context` (device context) | The handle a program gets after "opening" a NIC, which every later operation on that NIC carries. Analogy: the file handle you get by opening a file. |
| PD (Protection Domain) | A grouping container. Memory regions and connections must be in the same PD to work together, which stops a connection from touching memory that isn't its own. |
| MR (Memory Region) | Tells the NIC "you may read and write this memory". Registration makes the kernel lock the pages and the NIC record the address mapping, and returns two keys, lkey and rkey. Example: after registering 1 GB of GPU memory, the NIC can read and write that 1 GB directly. |
| lkey (local key) / rkey (remote key) | The two keys for accessing registered memory: the local NIC uses the lkey, a remote machine uses the rkey, and the rkey must be handed to the other side in advance. Analogy: the rkey is like an access card given to the other side; without it, their NIC can't get into this memory. The same memory is registered once on each NIC, and each NIC hands out different keys. |
| Access flags | What registration declares as allowed: local write, remote read, remote write. Example: with only local write enabled, remote machines can neither read nor write this memory. |
| QP (Queue Pair) | The "connection" in RDMA, made of a Send Queue (SQ) and a Receive Queue (RQ). Two machines each contribute a QP and pair them before they can communicate. Analogy: a dedicated phone line. |
| RC / UD (RC = Reliable Connection; UD = Unreliable Datagram) | The two QP types. RC is like TCP: one-to-one, guaranteed delivery, in order, with lost packets retransmitted by the NIC hardware. UD is like UDP: it can send to anyone but doesn't guarantee delivery. Large data such as KV always goes over RC. |
| QPN (Queue Pair Number) | The QP's number, which both sides exchange during connection setup. Example: for A to connect to B, A must know the number of B's QP. |
| WR / WQE (WR = Work Request; WQE = Work Queue Element) | A WR is a "work order" the program hands to the NIC: what to do (read, write, send a message), which local memory to use, which peer address to write to, and which key to carry. The driver translates it into a WQE the NIC can execute directly and puts it into the send queue. |
| SGE (Scatter/Gather Element) | One line of the work order describing local memory: start address, length, lkey. A work order can list several lines, and the NIC stitches those pieces of memory together when sending. |
| Post send / doorbell | Post send puts the work order into the send queue; afterwards the program writes a NIC register to tell it to start, which is called ringing the doorbell. The function returns immediately, without waiting for the data to finish transferring. |
| wr_id (work request ID) | A custom number on the work order that the NIC returns unchanged when done, so the program can tell which work order completed. Example: the program can put in the address of the object that tracks this transfer. |
| CQ / CQE / WC (CQ = Completion Queue; CQE = Completion Queue Entry; WC = Work Completion) | Each time the NIC finishes a work order, it puts a completion record, a CQE, into the CQ (the structure the program reads is called a WC), saying whether it succeeded or failed. The program has to fetch (poll) it from the CQ itself. Analogy: a delivery receipt. |
| Signaled / unsignaled | Each work order can choose whether to produce a receipt when done, and fewer receipts save overhead. Example: send 16 work orders and let only the last one produce a receipt; seeing it means the first 15 are done too, because RC completes in order. |
| Inline | Very small data is written straight into the work order, so the NIC doesn't need to read memory again. Example: control messages of a few dozen bytes suit inline sending. |
| Queue depth | The most unfinished work orders a queue can hold at once; when it is full, new ones wait for earlier ones to finish. Example: with a send queue depth of 256, at most 256 work orders are in flight at once. |
| Completion channel | A mechanism by which the CQ notifies the program when a new receipt arrives, so the program can sleep instead of checking constantly. The cost is wake-up latency, so latency-sensitive programs often use busy polling instead. |
| Async event | A status change the NIC reports on its own, unrelated to any particular work order. Example: a cable unplugged, a port coming back, a fatal NIC error. |

### 3.2 Operation Semantics

| Term | Explanation |
| --- | --- |
| Initiator / target | In a transfer, the side that issues the read or write request is the initiator, and the side whose memory is read or written is the target, also called the peer. For both READ and WRITE, the initiator submits the work order, rings the doorbell and collects the receipt, while the target is only accessed. Example: when Prefill writes KV into Decode, Prefill is the initiator; when Decode reads KV from a storage node, Decode is the initiator. In the source, target (as in `target_id`, `target_offset`) means the target side, and the initiator is usually also the active side during connection setup. |
| One-sided | READ/WRITE needs only the initiator to act; the other side's CPU takes no part and doesn't even know its data was read or written. Analogy: you hold an access card to the other side's warehouse and go in to drop off or pick up goods yourself, without the warehouse keeper knowing. |
| Two-sided | SEND/RECV needs both sides to cooperate: the receiver first prepares a receive buffer (post recv), and when the sender's message arrives, the receiver gets a receipt. Analogy: registered mail, which the recipient has to sign for. |
| RDMA WRITE | Writes data from local memory directly into remote memory. Example: a Prefill node writes the KV it computed directly into a Decode node's GPU memory. |
| RDMA READ | Reads data from remote memory directly into local memory. Example: pulling a cached copy of KV from a storage node to this machine. |
| max_rd_atomic / max_dest_rd_atomic (max outstanding RDMA Read & Atomic) | How many READs can wait at once on one connection for the other side to return data. A READ has to wait for the peer to send the data back, so if this number is too small, READs can't fill the bandwidth. |
| RNR (Receiver Not Ready) | A SEND message arrives but the receiver hasn't prepared a receive buffer yet, so the NIC waits a while and resends. It only happens with two-sided operations. |

### 3.3 The QP State Machine and Connection Setup

| Term | Explanation |
| --- | --- |
| RESET → INIT → RTR → RTS (RESET; INIT = Initialized; RTR = Ready To Receive; RTS = Ready To Send) | A QP goes through four steps from creation to use: RESET is freshly created; INIT binds the NIC port and access flags; RTR fills in the peer's address and QP number, after which it can receive; RTS sets the timeout and retransmission count, after which it can send. Analogy: to open a dedicated line, you first install the line (INIT), then register the other party's number so you can answer (RTR), and only then can you dial out (RTS). |
| ERR state (Error) | The state a connection enters after an error. Once in ERR, all unfinished work orders in the queue are discarded, and the QP can only be rebuilt. |
| Out-of-band exchange (OOB = Out-Of-Band) | RDMA can't be used before the RDMA connection exists, so connection setup information such as GIDs and QP numbers must first go over another channel, usually TCP. Analogy: first make an ordinary phone call to tell each other the dedicated line numbers, then open the dedicated line. TE does this with its own TCP handshake rather than the rdma_cm (RDMA Connection Manager) library. |
| PSN (Packet Sequence Number) | The sequence number of each packet, which the receiver uses to detect loss and reordering. Both sides agree on the starting number during setup. |
| ah_attr (Address Handle attributes) / AV (Address Vector) | The "how to reach the other side" filled in during connection setup: the peer's GID, which local port to use, and what priority. Analogy: the recipient address on a shipping label. |
| timeout / retry_cnt (retry count) | How long a sent packet waits for an ACK (Acknowledgement) before being resent, and the maximum number of resends. Example: with a timeout of about 67 ms and at most 7 resends, the connection enters ERR when all of them fail. |

### 3.4 Common Completion Error Codes (for Reading Logs)

| Error code | Usual cause |
| --- | --- |
| `IBV_WC_SUCCESS` (success) | The work order completed normally. |
| `IBV_WC_RETRY_EXC_ERR` (Retry Exceeded Error) | Resends ran out without an acknowledgement. Common causes: the peer machine or process died, the network is down, or the wrong GID was chosen. |
| `IBV_WC_REM_ACCESS_ERR` (Remote Access Error) | The peer refused access. Common causes: a wrong rkey, an address outside the peer's registered range, or the peer has already unregistered that memory. |
| `IBV_WC_LOC_PROT_ERR` (Local Protection Error) / `IBV_WC_LOC_LEN_ERR` (Local Length Error) | A problem on the local side: local memory not registered, a wrong lkey, or a length out of bounds. |
| `IBV_WC_WR_FLUSH_ERR` (Work Request Flushed Error) | The connection has already broken, and the work orders queued behind are discarded in bulk. It is a result rather than the cause, so look further back for the first error that isn't a FLUSH. |

---

## 4. Mooncake TE's Own Concepts

### 4.1 Public API

| Term | Explanation |
| --- | --- |
| TransferEngine | The entry point users work with. Usage takes four steps: initialize, register memory, open the peer, then submit transfers and check the results. |
| Classic TE and TENT (Transfer Engine NEXT) | TE currently has two implementations. The classic one is the default, and setting the environment variable `MC_USE_TENT=1` switches to TENT. When reading the source, start with the classic implementation. |
| Segment | The "remotely readable and writable memory set" a process exposes, identified by a globally unique name, one per process. Example: the Decode process's segment is named `10.0.0.2:15123` and includes all the KV GPU memory it registered. |
| Segment name | The name of a segment. In P2PHANDSHAKE (peer-to-peer handshake) mode it is simply IP:port, which is how others find you. |
| SegmentID / SegmentHandle | The number this process gives a peer segment after opening it; later transfers use the number instead of the segment name. Example: opening `10.0.0.2:15123` gives number 1, and number 0 always means yourself. |
| Buffer | A piece of registered memory within a segment, and each registration adds one buffer. Example: if a process registers one block of KV GPU memory and one block of host memory, its segment has 2 buffers. |
| location | Which device a buffer is on, written as a string. Example: `cpu:0` is memory on NUMA node 0, `cuda:3` is GPU 3's memory, and `*` lets TE detect it. TE uses it to pick the nearest NIC. |
| remote_accessible | Whether registration allows others to read and write the memory. Memory used only as a send source can stay closed. |
| TransferRequest | The description of one transfer: read or write, local address, peer segment number, peer address, length. Example: "WRITE, local address X, segment 1, peer address Y, 1 MB" means writing the 1 MB at local X to Y in segment 1. Note that Y is a real virtual address in the peer process. |
| Batch / BatchID / BatchDesc (batch descriptor) | Several requests packed together, submitted and tracked together, and the BatchID is the pack's number. Example: one layer's KV split into 100 requests and submitted at once in one batch. |
| TransferStatus | The query result: waiting, completed, failed, timed out, and so on. If any slice of data fails, the whole request counts as failed. |
| Submit and poll | Submitting only hands the task over and returns immediately; afterwards you check the status repeatedly until it finishes. The "synchronous transfer" in the Python API is just a submit followed by checking for you until it completes. |
| Completion eventfd | Another way to wait besides polling: when a transfer completes, TE writes to an fd, and the program sleeps on that fd, then wakes up and fetches the result, saving the CPU spent on repeated queries. |
| Notify | TE's built-in small-message feature. After a one-sided write completes, the receiver doesn't know the data has arrived, so the sender can send a notification to tell it. Example: after P finishes writing the KV, it sends "request 42 is done" to D. |
| `transfer_engine_validator` (data validation tool) | A test program shipped with Mooncake that checks whether data was transferred correctly, rather than measuring speed. One machine runs in target mode and provides the memory, the other runs in initiator mode and repeatedly "writes over, clears the local buffer, reads back, and compares byte by byte", exiting with an error as soon as a single byte doesn't match. Bandwidth is measured by a different program, `transfer_engine_bench`, which only transfers and doesn't check the contents. Example: when testing failover after a network link goes down, the validator confirms that no data was corrupted during the switch. Separately, `DEFINE_validator` in the Mooncake Store source is something else: it checks whether startup flags are valid. |

### 4.2 Metadata and Handshake

| Term | Explanation |
| --- | --- |
| TransferMetadata | The TE module in charge of "who is where, where the memory is, how to connect": publishing its own information, querying the other side's, handshaking for connections, and sending and receiving notifications. |
| SegmentDesc (segment descriptor) | A segment's "manual": segment name, protocol, which NICs, which buffers, and how memory maps to NICs. Only with this manual does the peer know where to write and which key to carry. |
| DeviceDesc (device descriptor) | The part of the manual describing one NIC: NIC name, LID, GID. |
| BufferDesc (buffer descriptor) | The part of the manual describing one buffer: location, start address, length, plus its lkey and rkey on each NIC. Example: a buffer registered on 4 NICs has 4 rkeys. |
| Metadata backend / conn string (connection string) | Where the manuals are stored. It can be a central service such as etcd, Redis or HTTP; or you can choose P2PHANDSHAKE, with no center, where whoever needs a manual connects directly to the other side to ask for it. Example: SGLang PD disaggregation uses P2PHANDSHAKE. |
| P2PHANDSHAKE (peer-to-peer handshake mode) | A mode that needs no central metadata service, enabled by passing the string `P2PHANDSHAKE` as the metadata backend at initialization. The segment name is then IP:port, and the manual is not published anywhere but stays inside the process. Whoever wants to access you connects straight to your handshake daemon at the IP and port in your segment name, and the two sides exchange manuals on the spot. Analogy: instead of looking you up in a phone book, they dial the number on your business card and you exchange details during the call. The benefit is that no service such as etcd has to be deployed; the cost is that every process must keep a port open that the other side can reach. Example: SGLang PD disaggregation uses this mode; D's segment name looks like `10.0.0.2:15123`, and P connects to that address, gets D's manual, and starts writing KV. |
| Publish | After registering memory, put the updated manual into the metadata backend so others can find it. |
| metacache (metadata cache) | Caches the peers' manuals locally so they aren't fetched on every transfer. When a peer registers new memory the cache goes stale and has to be fetched again. |
| Handshake | Before an RDMA connection is set up, the two sides exchange NIC addresses and QP numbers over TCP, in JSON (JavaScript Object Notation). Example: A says "my QPs are 101 and 102", B replies "mine are 201 and 202", and then each side moves its own QPs to RTS. |
| Handshake daemon | A TCP service running in the background of every TE process, answering others' requests to connect, fetch the manual, send notifications, and so on. |
| Active / passive | The side that starts the handshake is active, and the side that answers is passive. Usually the side that wants to send data starts it. |
| ready ack (ready acknowledgement) | The last step of the handshake: once both sides have set up their QPs, the active side sends one more acknowledgement, and data starts flowing on the connection only after both sides confirm. This keeps one side from starting to send while the other side's QPs aren't ready. |
| NIC path | Uses "segment name@NIC name" to uniquely identify a given NIC of a given process. Example: `10.0.0.2:15123@mlx5_2`. |

### 4.3 Topology and NIC Selection

| Term | Explanation |
| --- | --- |
| Topology (topology matrix) | A table: for each memory location, which NICs are preferred and which can be used next. Example: `cuda:0` prefers mlx5_0, with mlx5_1 and mlx5_2 as fallbacks. |
| preferred_hca / avail_hca (preferred / available HCA) | Preferred NICs are the ones closest to the memory: for a GPU, the nearest by PCIe distance; for host memory, the ones on the same NUMA node. All other NICs are available NICs, used only when the preferred ones have problems. |
| NIC selection | First pick a preferred NIC at random; on retry after a failure, move through them in the order "preferred first, fallbacks after". Example: GPU0 prefers mlx5_0, and after mlx5_0 fails it switches to mlx5_1. |
| Local NIC / peer NIC | Each slice of data needs two NICs: the local one that sends and the peer one that receives. The local one is picked by where the source data is, and the peer one by where the destination memory is. Example: writing from local GPU0 to peer GPU5, the local side picks the NIC next to GPU0, and the peer side picks the NIC next to GPU5. |
| device_id / buffer_id | The NIC number and the buffer number. "Which buffer's key on which NIC" is looked up with these two numbers. |

### 4.4 Internal Objects of the RDMA Backend

| Term | Explanation |
| --- | --- |
| Transport | The implementation of one transport method. RDMA, TCP and NVLink each have one. |
| MultiTransport | The dispatcher: it looks at which protocol the peer segment uses and hands the request to the matching backend. Example: if the peer is an `rdma` segment, the request goes to the RDMA backend. |
| protocol | How a segment is accessed, for example `rdma`, `tcp`, `nvlink_intra`. |
| RdmaTransport | Registers memory, cuts requests into slices, and picks a local NIC for each slice. |
| RdmaContext | The "steward" of one local NIC, managing all of its resources: registered memory, completion queues, connections, worker threads. There is one RdmaContext per NIC. |
| RdmaEndPoint (RDMA endpoint) | The connection from a given local NIC to a given peer NIC, usually holding 2 QPs used in parallel. Example: local mlx5_0 to peer mlx5_2 is one endpoint. |
| EndpointStore | Stores established connections, looked up by NIC path. When there are too many, it evicts rarely used ones; the default eviction algorithm is called SIEVE (simpler than LRU (Least Recently Used); SIEVE is a name, not an acronym), and FIFO (First In, First Out) is also available. |
| Lazy connection setup | A connection is set up the first time it is used, so the first transfer to a given peer costs an extra handshake. |
| WorkerPool / worker threads | Each NIC has a few background threads looping over two jobs: handing queued data slices to the NIC, and fetching receipts from the completion queue. |
| TransferTask | The progress record of one request inside TE: how many slices it was cut into, how many completed, how many failed, and how many bytes were transferred. |
| Slice | A small piece a request is cut into, each matching one RDMA work order. Example: a 1 MB request is cut into 16 slices of 64 KB and spread over several connections and NICs in parallel. |
| slice_size / fragment_limit (tail merge threshold) | If the last remaining piece isn't too large, it is sent together with the previous slice, avoiding tiny tail slices. Example: with 64 KB slices and a 16 KB threshold, the remaining 70 KB is not cut into 64 KB + 6 KB but sent as one 70 KB slice. |
| markSuccess / markFailed | Called when a slice completes or fails, updating the task's counters. The task's status is settled only after all its slices have finished. |
| Retry / redispatch | After a slice fails, TE resends it on another NIC or another path, up to a limit. This is a separate layer from the NIC's hardware retransmission: hardware retransmission handles occasional packet loss, while TE's retry handles a broken NIC or link. |
| Rail pause / context pause | If the path from one NIC to another fails repeatedly in a short time, it is paused for a while and traffic goes over other paths meanwhile. Example: after 5 consecutive errors, the path is paused for 30 seconds. If a whole local NIC breaks, the whole NIC is taken out of use. |
| auto GID | When no GID index is specified, TE picks the row in the GID table most likely to connect, and moves to the next row if that one doesn't. |
| rdma_twosided (two-sided RDMA) | Another RDMA backend that moves data with SEND/RECV and uses credit-based flow control: the receiver first grants the sender a quota, and the sender can only send within it. |
| Adaptive congestion control | Automatically adjusts how much data is in flight based on network feedback: send more when the network is clear, and less when congestion starts. Off by default. |

---

## 5. Other Transports (Look Up When Needed)

| protocol | Explanation |
| --- | --- |
| `tcp` | Plain TCP: it works on any network, but data passes through kernel copies, so it is much slower than RDMA. Suited to development and testing, or environments without RDMA NICs. |
| `shm` (shared memory) | Processes on the same machine copy directly through shared memory, without going through a NIC. It uses POSIX (Portable Operating System Interface) shared memory and mmap (memory map). |
| `nvlink_intra` (intra-node NVLink) | GPUs in the same machine copy GPU memory directly over NVLink (NVIDIA's high-speed GPU interconnect), much faster than going through a NIC. |
| `nvlink` (cross-node NVLink) | MNNVL (Multi-Node NVLink): as in GB200 NVL72, the GPUs of several machines are joined by NVLink into one system, so GPU memory can be copied directly across machines too. |
| `nvmeof` | Reads and writes files on NVMe (Non-Volatile Memory Express) SSDs directly. NVMe-oF (NVMe over Fabrics) means accessing a remote drive over the network; GDS (GPUDirect Storage) lets the drive and GPU memory transfer directly, without going through host memory. |
| `cxl` | CXL (Compute Express Link) memory: external memory attached over CXL, which several machines can share and which is read and written just like local memory. |
| `efa` | The EFA (Elastic Fabric Adapter) NIC on AWS. It doesn't support RC; it uses its own SRD (Scalable Reliable Datagram) protocol and is programmed through libfabric (OFI = OpenFabrics Interfaces). |
| `cxi` | The NIC of HPE Slingshot networks (chip codename Cassini), also programmed through libfabric. |
| `hip` | Same-machine transfer for AMD GPUs, copying between GPUs with HIP (Heterogeneous-computing Interface for Portability). Related terms: ROCm (AMD's GPU software stack), KFD (Kernel Fusion Driver, the kernel driver for AMD GPUs). |
| `ascend` | Transfer for Huawei Ascend NPUs (Neural Processing Unit), built on interfaces such as HCCL (Huawei Collective Communication Library). |
| `ubshmem` / kunpeng | Huawei Kunpeng's UB (Unified Bus) interconnect, whose programming interface is URMA (Unified Remote Memory Access). A jetty corresponds to an RDMA QP, a JFC (Jetty For Completion) to a CQ, and an EID to a GID. |
| `musa` / `maca` / `hylink` / sunrise_link | The GPU interconnects of Moore Threads, MetaX, Hygon DCU (Deep Computing Unit) and Sunrise respectively. Hygon's toolkit is DTK (DCU Toolkit), and its interconnect is HSL (Hygon Scale-up Link). |
| `barex` | Described in the official docs as a Bare-metal RDMA extension, built on RDMA NICs. |
| `nccl` / `flagcx` | Moves data with the point-to-point send and receive of NCCL (NVIDIA Collective Communications Library) or FlagCX (FlagOS's cross-vendor communication library). |

---

## 6. Common Concurrency and Engineering Patterns in the Source

| Term | Explanation |
| --- | --- |
| Atomic operation (`std::atomic`) | A read or write that no other thread can "cut into halfway". Example: if two threads each add 1 to a counter at the same time, atomic addition always gives 2, while plain addition may add only 1. |
| Memory order (memory_order) | Rules for when data written by one thread becomes visible to another. Example: A writes data and then writes a flag with release; when B reads the flag with acquire, it is guaranteed to see the data A wrote. relaxed doesn't guarantee this, and seq_cst (sequentially consistent) is the strictest. |
| `__atomic_*` / `__sync_*` | Atomic operation functions provided by GCC (GNU Compiler Collection), doing the same job as `std::atomic` but usable directly on ordinary variables. |
| `volatile` | Tells the compiler to really read and write memory for this variable every time, without optimizing it away. It doesn't make anything thread-safe, so the source always uses it together with the atomic functions. |
| Spinlock / read-write lock (RWSpinlock, read-write spinlock) | A spinlock spins in place instead of sleeping when it can't get the lock, which suits locks held only very briefly. A read-write lock lets many readers in at once while a writer gets exclusive access. Example: when many threads look up the connection table and few modify it, a read-write lock fits. |
| Cache line / false sharing | The CPU cache reads and writes in 64-byte blocks. When two threads each modify their own variable but the two variables happen to share a block, they keep invalidating each other's cache and the program slows down. Example: storing each thread's counter 64 bytes apart avoids it. |
| Thread-local object pool (thread_local object pool) | Each thread keeps a batch of used objects to reuse next time, saving frequent allocation and freeing. Example: when hundreds of thousands of slice objects are created per second, this pays off. |
| Busy polling | A thread keeps actively checking "is it done yet" without sleeping. Latency is lowest, at the cost of permanently occupying one CPU core. |
| Reference count / pin | Records "how many users this object still has", and the object may not be freed until the count reaches zero. Example: while a callback is still reading a batch's data, other threads may not delete that batch. |
| Conditional compilation (`#ifdef`) | Decides at compile time, by switches, which code to include. Example: without an AMD GPU, the HIP-related code isn't compiled. When reading the source, skip the branches unrelated to your hardware first. |
| Return convention | Old interfaces return an integer, 0 for success and a negative error code otherwise; new interfaces return a Status object carrying the error type and message. |

---

## 7. Putting the Terms Together: The Call Chain of One RDMA WRITE

Take SGLang PD disaggregation as the example: Prefill (the sender) writes the KV Cache into the GPU memory of Decode (the receiver) with RDMA WRITE.

### 7.1 Preparation (Both Sides)

1. **Initialize**: `TransferEngine::init(conn_string, local_server_name, ...)` installs RdmaTransport (`rdma_transport.cpp:350`): it creates an RdmaContext for each NIC (opening the device, creating the PD and CQ, starting the worker threads), starts the handshake daemon, discovers the topology and publishes the local segment descriptor.
2. **Register memory**: `registerLocalMemory(addr, len, "cuda:0")` → `RdmaTransport::registerLocalMemory` (`rdma_transport.cpp:511`) → `ibv_reg_mr` or `ibv_reg_dmabuf_mr` on each NIC (`rdma_context.cpp:893-901`) → adds `BufferDesc{addr, len, lkey[], rkey[]}` to the local segment descriptor and publishes it (`rdma_transport.cpp:1088`).
3. **Exchange addresses**: the upper layer tells the sender the virtual addresses of the receiver's buffers (SGLang passes them as `dst_kv_ptrs` in its bootstrap message). TE itself doesn't handle this step.

### 7.2 Sender

1. **Open the peer segment**: `openSegment("decode_ip:port")` gets the peer's SegmentDesc (NIC GIDs, the rkey of each buffer) and a local SegmentID.
2. **Submit**: `allocateBatchID` + `submitTransfer(batch, [{WRITE, src, sid, dst_addr, len}])`
   - `TransferEngine::submitTransfer` (`transfer_engine.cpp:987`) decides whether to go through TENT;
   - → `TransferEngineImpl` (`transfer_engine_impl.h:143`) → `MultiTransport::submitTransfer` (`multi_transport.cpp:572`), where `selectTransport` picks RdmaTransport by protocol;
   - → `RdmaTransport::submitTransferTask` (`rdma_transport.cpp:1840`): picks the local NIC, cuts slices, fills in the lkey, and groups the slices by NIC;
   - → `RdmaContext::submitPostSend` (`rdma_context.cpp:1822`) → `WorkerPool::submitPostSend` (`worker_pool.cpp:790`): picks the peer NIC, fills in the rkey and peer NIC path, and puts the slices into the worker queues.
3. **Send**: the worker thread's `performPostSend` (`worker_pool.cpp:1084`) gets the endpoint by NIC path, creating it and handshaking if it doesn't exist yet (`setupConnectionsByActive`, `rdma_endpoint.cpp:666`; the QPs go through INIT → RTR → RTS, `:1569`)
   - → `RdmaEndPoint::submitPostSendLimited` (`rdma_endpoint.cpp:1329`): fills one `ibv_send_wr` per slice (`wr_id` = slice pointer), spreads them over the QPs, and calls `ibv_post_send` (`:1430`).
4. **The NICs do the work**: the local NIC DMAs the data out of local GPU memory onto the network; the peer NIC checks the address and permissions with the rkey, DMAs the data straight into the peer's GPU memory, and returns an ACK.
5. **Collect completions**: a CQE appears in the local CQ → `performPollCq` (`worker_pool.cpp:1438`) → `slice->markSuccess()` (`:1531`); on failure the slice is retried, and `markFailed` is called once retries run out.
6. **Check the result**: the caller sees COMPLETED from `getTransferStatus` / `getBatchTransferStatus`.

### 7.3 Receiver

- **Passive connection setup**: the handshake daemon receives a Connection request → `RdmaTransport::onSetupRdmaConnections` (`rdma_transport.cpp:2278`) → `setupConnectionsByPassive` (`rdma_endpoint.cpp:1029`), which sets up the local QPs and replies with their QPNs.
- **Data arrives**: the receiver's CPU takes no part, and TE raises no callback at all.
- **Learning of completion**: after the sender sees COMPLETED, it sends a separate message. SGLang pushes the status over ZMQ (`sglang/python/sglang/srt/disaggregation/common/conn.py:895`), and TE's notify can be used as well.

---

## 8. Common Environment Variables

The config struct is in `TE/include/config.h:52` (`GlobalConfig`), and it is parsed in `TE/src/config.cpp`.

| Variable | Default | Purpose |
| --- | --- | --- |
| `MC_SLICE_SIZE` | 65536 | Slice size (bytes) |
| `MC_FRAGMENT_RATIO` | 4 | `fragment_limit = slice_size / ratio`, 16 KB by default |
| `MC_NUM_QP_PER_EP` | 2 | QPs per endpoint |
| `MC_MAX_WR` | 256 | SQ depth per QP |
| `MC_MAX_CQE_PER_CTX` | 4096 | Capacity of each CQ |
| `MC_WORKERS_PER_CTX` | 2 | Worker threads per NIC |
| `MC_MAX_SGE` / `MC_MAX_INLINE` | 4 / 64 | SGE limit per WR / inline limit |
| `MC_MTU` | 4096 | Path MTU (then capped at the port's actual MTU) |
| `MC_GID_INDEX` | Auto | GID table index |
| `MC_IB_PORT` | 1 | NIC port number |
| `MC_IB_TC` / `MC_IB_SL` | Unset | Traffic class / service level |
| `MC_RETRY_CNT` | 9 | Software-level retries per slice |
| `MC_RDMA_SIGNAL_INTERVAL` | 1 | One CQE every this many WRs |
| `MC_RDMA_WORKER_IDLE_SPIN_US` | 100000 | How long an idle worker busy-waits before sleeping (microseconds) |
| `MC_RDMA_RAIL_PAUSE_SECONDS` | 30 | Pause duration for a failing path |
| `MC_MAX_EP_PER_CTX` | 65536 | Maximum cached endpoints per NIC |
| `MC_ENDPOINT_STORE_TYPE` | SIEVE | Endpoint eviction algorithm (SIEVE / FIFO) |
| `MC_MIN_RPC_PORT` / `MC_MAX_RPC_PORT` | 15000 / 17000 | Random range for the handshake port |
| `MC_DISABLE_METACACHE` | Unset | Disables the cache of peer segment descriptors |
| `MC_USE_TENT` | Unset | Switches to the TENT engine |
| `MC_LOG_LEVEL` | INFO | Log level |
