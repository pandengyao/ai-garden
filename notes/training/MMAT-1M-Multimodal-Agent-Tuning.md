# MMAT-1M: A Large Reasoning Dataset for Multimodal Agent Tuning

中文 | [English](./MMAT-1M-Multimodal-Agent-Tuning_en.md)

- **原文链接**: [MMAT-1M: A Large Reasoning Dataset for Multimodal Agent Tuning](https://arxiv.org/abs/2507.21924)
- **论文**: [arXiv:2507.21924](https://arxiv.org/abs/2507.21924) · [ICCV 2025 会议版](https://openaccess.thecvf.com/content/ICCV2025/html/Gao_MMAT-1M_A_Large_Reasoning_Dataset_for_Multimodal_Agent_Tuning_ICCV_2025_paper.html)
- **发布日期**: 2025-07-29
- **官方资料**: [GitHub 仓库](https://github.com/VIS-MPU-Agent/MMAT-1M) · [Hugging Face 数据集](https://huggingface.co/datasets/VIS-MPU-Agent/MMAT-1M)
- **实测环境**: macOS，Python 3.12.13，`datasets` 5.1.0；数据为 Hugging Face 上的 `b5bf713` 版本（2025-08-04），2026-10-22 访问

## 核心要点

这是百度团队发表在 ICCV 2025 的数据集论文。核心是一套用 GPT-4o 批量生成多模态 agent 轨迹的数据引擎：给现成的视觉问答补上推理过程、工具调用和反思，再用这些数据微调开源多模态模型，让小模型也学会边推理边调用工具。

### 1. 为什么需要它？(Motivation)

让模型学会分步推理和调用工具，大致有两条路。一条是用提示词驱动大模型（HuggingGPT、ReAct 一类），效果取决于模型理解指令的能力，而且每次都要调用大模型，成本高。另一条是 agent tuning：用专门构造的轨迹数据做微调，让小模型也有接近闭源大模型的规划、推理和工具调用能力；纯文本方向已有 AgentTuning、FireAct 等工作。

多模态方向的 agent tuning 数据还很少，规模也小：LLaVA-Plus 把 LLaVA-158K 改写成 117K 条工具调用数据，T3-Agent 的 MM-Traj 有 20K 条带工具轨迹的任务。论文认为现有数据有三个毛病：

- **分布单一**，对各类基准的提升有限；
- **没有反思机制**，视觉工具出错时模型容易被带偏；
- **推理和工具调用方式不灵活**，不好落地。

MMAT-1M 想用一个百万级、任务多样、带反思、同时提供单轮和多轮格式的数据集补上这块。

### 2. 它是怎么做的？(Data Engine)

![MMAT-1M 的数据引擎](./img/MMAT-1M-Multimodal-Agent-Tuning-data-engine.png)

*论文图 2：数据引擎分 Foundation、Rationale、Reflection、Integration 四个阶段，产出 RR 和 ORR 两种格式。图中的例子是求一周每天行驶里程的平均数。*

1. **打底**（Foundation）：从公开数据集里取图片和问答对。为了统一回答风格，短答案的样本会在问题末尾加一句格式要求，答案本身不改。同时准备好 5 个外部工具：
   - Image Caption：仿照 CCoT，先让 GPT-4o 针对问题生成场景图（与回答相关的物体、属性和关系），再根据场景图写图片描述；
   - OVD（开放词表目标检测）：用 Grounding DINO 检测场景图里提到的物体；
   - OCR：用 PaddleOCR 识别图中文字；
   - Face Detection：用 deepface 定位人脸；
   - RAG：由 GPT-4o 写搜索词，调用 Google API 取回最相关的 top-k 条结果。
2. **推理轨迹**（Rationale）：GPT-4o 分多轮推理。每一轮先写思考，再决定调用哪些工具（可以不调、调一个或多个）、要不要搜索；工具结果作为下一轮的用户消息返回，直到它发出结束信号，最后再单独问一次答案。生成时 GPT-4o 是知道标准答案的，提示词要求它“靠推理逼近标准答案，但不能直接用标准答案”。
3. **反思**（Reflection）：作者发现这样生成的轨迹有两类问题。一是跳步，数学题尤其明显，关键计算被省掉；二是“推理作弊”，推理过程其实推不出答案，GPT-4o 却因为知道答案而硬凑上去。对应有两个提示词：数学反思让 GPT-4o 检查倒数第二步到最后一步之间有没有省掉计算过程，有就补上；通用反思让它判断推理是否作弊并说明理由。查出问题的样本会在轨迹里插入一段反思。
4. **整合**（Integration，可选）：多轮的 RR 格式要等工具一轮轮返回，不适合对延迟敏感的场景。作者受 LUMOS 启发，把它压成单轮的 ORR：除 RAG 外，所有工具的结果都预先放进输入，用特殊标记包起来，输出只有一段思考和一个答案。代价是推理时不能再动态调用工具，也拿不到搜索结果。

最后，作者用 Doubao-1.5-Vision-Pro-32K 按连贯性、相关性、准确性、完整性和图文结合五个维度给全部样本打 0.0–1.0 分，称 89% 以上属于高质量推理。论文没给“高质量”的分数线，也没说剩下的样本有没有剔除。

### 3. 数据集长什么样？(Dataset)

| 来源 | 对话数 | 主要内容 |
| --- | --- | --- |
| Visual CoT | 434,265 | 文档、图表、细粒度理解、通用 VQA、关系推理 |
| The Cauldron | 215,680 | 表格问答、场景文字、界面截图、图表描述、几何与图形推理等 10 个子集 |
| InfoSeek | 131,400 | 要靠外部知识才能回答的视觉信息检索问答 |
| LLaVA-CoT | 98,561 | 通用 VQA、科学、数学、文档理解 |
| TabMWP | 23,059 | 结合表格的数学应用题 |
| 合计 | 902,965 | 共 1,090,263 个问答对 |

论文表 1 里的其他统计：

- 原始数据里 93.7% 的对话只有一轮问答（846,389 条），2 轮的有 28,646 条，3 轮及以上的有 27,930 条；
- 按问答对算，推理 3 步的占 70.0%，4 步的占 20.3%，5 步及以上的占 9.0%，2 步的占 0.7%；
- 工具调用次数：Image Caption 620,644，OCR 471,866，RAG 205,682，OVD 156,237，Face Detection 20,077；
- 反思：通用反思 46,508 次，数学反思 11,139 次，合计 57,647 次。

和同类数据（LLaVA-Plus-v1 117K、Visual CoT 438K、LLaVA-CoT 100K、MM-Traj 20K）相比，MMAT-1M 规模最大，也是其中唯一同时带工具调用、联网搜索、CoT 和反思，并且同时提供单轮和多轮格式的。

每条数据只有 `messages`（对话）和 `images`（图片相对路径）两个字段，图片本身不在数据集里。RR 是多轮格式：系统提示说明了推理流程和每一轮的标签格式，但没有列出有哪些工具，模型只能从训练数据里学到工具名（`image_caption`、`ocr`、`object_detection`、`face_detection`）。助手每一轮写 `<THOUGHT>`，按需带上 `<OPERATOR>`（工具名）和 `<RAG>`（搜索词），最后用 `<SIGNAL>` 表示下一步：`continue` 是继续，`reflection` 是进入反思，`end` 是结束推理。工具结果以用户消息返回；推理结束后，用户要求“总结并回答最初的问题”，助手只输出答案。下面是验证集里的一条 DocVQA 样本（有删节）：

```text
system     You are an advanced multimodal reasoner. ...（RR 系统提示，说明推理流程和标签格式，这里省略）
user       <image>what is the department mentioned in the slip ?
           Short answer required. Please start your reasoning.
assistant  <THOUGHT>To identify the department mentioned in the slip, I should extract the text from the image.</THOUGHT>
           <OPERATOR>ocr</OPERATOR>
           <SIGNAL>continue</SIGNAL>
user       Here are ocr results from the previous step:
           - ocr information: U.S.DEPARTMENT CF AGRICULTURE DATE Hapr REFERENCE SLIP ...
           Please continue your reasoning.
assistant  <THOUGHT>The OCR results show that the department mentioned in the slip is 'U.S. DEPARTMENT OF AGRICULTURE'.</THOUGHT>
           <SIGNAL>end</SIGNAL>
user       Based on the above information, please summarize and give the answer to the initial question: ...
assistant  U.S. Department of agriculture
```

ORR 是单轮格式：工具结果预先写进输入，用 `<|begin_api_invoke|>`、`<|begin_result_of_api|>` 等标记包起来，助手一次输出 `<THOUGHT>` 和 `<ANSWER>`。下面是验证集里的一条 WTQ 表格问答样本（有删节）：

```text
system     ... Respond in the format like this:
           <THOUGHT>your reasoning</THOUGHT>
           <ANSWER>The answer is: your answer</ANSWER>
user       <image>Was it dallas or ottawa that won the game on december 9, 1993?
           Use the following operators to help answer the question:
           <|begin_api_invoke|>image_caption<|end_api_invoke|>
           <|begin_result_of_api|>
           The image is a table listing hockey game results from 1993-1994, ... on December 9, 1993, Dallas won against Ottawa with a score of 6-1 ...
           <|end_result_of_api|>
           <|begin_api_invoke|>ocr<|end_api_invoke|>
           <|begin_result_of_api|>
           ['Date', 'Winning Team', 'Score', 'Losing Team', ...]
           <|end_result_of_api|>
assistant  <THOUGHT>... According to the OCR results, on December 9, 1993, the game was between Dallas and Ottawa. The winning team recorded was Dallas with a score of 6, while Ottawa had a score of 1.</THOUGHT>
           <ANSWER>The answer is: Dallas.</ANSWER>
```

论文里的 OVD 工具在 ORR 里叫 `label_bbox`，在 RR 里叫 `object_detection`，两边的结果格式也不一样。论文是用两种格式分别训练模型的；如果想混在一起训练，最好先统一工具名和结果格式。

### 4. 怎么训练、效果如何？(Training and Results)

训练用 ms-swift 做 LoRA 微调，只训 1 个 epoch，学习率 4e-5，batch size 1，最大长度 16384，BF16，DeepSpeed ZeRO-2；论文没给 LoRA 的秩、GPU 数量和训练时长。五个模型（Llama-3.2-11B-Vision-Instruct、MiniCPM-V-2.6、InternVL2.5-2B/4B/8B）各用 ORR 和 RR 分别训一份。

评测用 VLMEvalKit 跑 8 个基准：MMStar、MMMU、MathVista、MathVision（这两个数学基准用 testmini）、AI2D、OCRBench、RealWorldQA、HallusionBench；另用 Dyn-VQA 考检索增强和多跳推理，指标是 F1-Recall。评测时的搜索用 Google，每次最多取 3 条。

8 个基准的平均分（OCRBench 满分 1000，折算成 100 分制后参与平均）：

| 模型 | Baseline | ORR | RR |
| --- | --- | --- | --- |
| Llama-3.2-11B-Vision-Instruct | 52.2 | 54.6 | 55.3 |
| MiniCPM-V-2.6 | 58.0 | 58.8 | 59.9 |
| InternVL2.5-2B | 52.7 | 54.4 | 54.7 |
| InternVL2.5-4B | 58.4 | 59.5 | 60.6 |
| InternVL2.5-8B | 60.7 | 62.4 | 63.4 |

作为参考，GPT-4o 是 65.6。

- 五个模型的平均分都涨了，而且每个模型都是 RR 高于 ORR。
- 涨得最多的是 RealWorldQA 和 HallusionBench：按论文表 3 算，RR 在五个模型上平均分别涨 5.8 和 4.6 分。
- OCRBench 是 RR 最弱的一项：五个模型里有三个低于基线，而 ORR 在五个模型上都比 RR 高。论文的解释是，RR 虽然有一定的纠错能力，OCR 认错的字还是会拖累最终结果；ORR 借助图片描述，能缓解 OCR 的错误。
- 和 GPT-4o 比，InternVL2.5-8B-RR 在 MMStar（65.3 对 65.1）、MathVista（64.8 对 60.0）和 OCRBench（839 对 806）上更高，在 AI2D（84.2 对 84.9）和 HallusionBench（55.8 对 56.2）上接近；不过 MathVista 和 OCRBench 两项，8B 的基线（64.5、819）本来就高于 GPT-4o。MMMU（57.3 对 70.7）和 MathVision（21.7 对 30.4）的差距仍然很大。

检索增强基准 Dyn-VQA 的结果如下（Query 指模型检索时实际用的输入，Golden Query 是针对最后一步检索优化过的提示）：

| 模型 | Query 基线 | Query RR | Golden Query 基线 | Golden Query RR |
| --- | --- | --- | --- | --- |
| Llama-3.2-11B-Vision-Instruct | 29.4 | 38.0 | 34.6 | 45.1 |
| MiniCPM-V-2.6 | 32.7 | 35.9 | 39.2 | 44.4 |
| InternVL2.5-2B | 19.3 | 30.9 | 26.0 | 38.8 |
| InternVL2.5-4B | 23.3 | 35.4 | 31.1 | 42.1 |
| InternVL2.5-8B | 27.0 | 36.8 | 35.2 | 44.0 |

RR 让五个模型的 Query 分数提高了 3.2–12.1 分，但最高的 38.0 仍明显低于 GPT-4o 的 52.0（Golden Query 为 61.5）和 OmniSearch（GPT-4V）的 50.0。

消融实验的数值和表 3 里的 InternVL2.5-8B 基本对得上（论文没点名用的哪个模型）。这里的平均分是 9 项（8 个基准加 Dyn-VQA）的平均，Dyn-VQA 一栏对应上表的 Golden Query：

| 设置 | 工具 | 搜索 | 9 项平均 | Dyn-VQA |
| --- | --- | --- | --- | --- |
| Baseline | ✗ | ✗ | 57.9 | 35.2 |
| RR 格式，不微调，只靠提示词 | ✓ | ✓ | 55.0 | 31.5 |
| RR，只有搜索 | ✗ | ✓ | 57.3 | 43.4 |
| RR，只有工具 | ✓ | ✗ | 59.8 | 35.4 |
| ORR | ✓ | ✗ | 59.6 | 36.6 |
| R（有推理轨迹，没有反思） | ✓ | ✓ | 60.2 | 42.9 |
| RR | ✓ | ✓ | 61.3 | 44.0 |

- 不微调，直接让基线模型按 RR 格式调用工具，平均分反而从 57.9 掉到 55.0，说明这套调用方式要靠微调才学得会。
- 反思带来 1.1 分（60.2 → 61.3）。
- 搜索主要提升 Dyn-VQA（35.4 → 44.0）；只给搜索、不给工具时，9 项平均（57.3）还低于基线。

![ORR 与 RR 的效果和推理耗时](./img/MMAT-1M-Multimodal-Agent-Tuning-latency.png)

*论文图 3：InternVL2.5 三个尺寸下，Baseline、ORR、RR 的 8 项平均分（纵轴）和推理耗时（横轴）。*

图上没有标数值。按坐标网格把各个标记点的像素位置换算成数值，耗时大约如下（换算出的纵坐标和表 3 的平均分相差不到 0.1，说明读数可靠）：

| 模型 | Baseline | ORR | RR |
| --- | --- | --- | --- |
| InternVL2.5-2B | 2.6 秒 | 3.2 秒 | 3.3 秒 |
| InternVL2.5-4B | 4.2 秒 | 5.4 秒 | 6.1 秒 |
| InternVL2.5-8B | 5.9 秒 | 8.0 秒 | 8.2 秒 |

ORR 和 RR 比基线多花 0.6–2.3 秒，也就是多出约 23%–45% 的时间。ORR 比 RR 快得不多：2B 和 8B 上只差 0.1–0.2 秒，4B 上差 0.7 秒。实验部分自己也只说 RR 的开销比 ORR“略高”，和数据引擎一节“ORR 显著提高推理速度”的说法不太一致。论文也没说明耗时是怎么计的，比如是否包含调用外部工具的时间。

最后是一个定性实验。MMAT-1M 里没有名人识别工具，所以遇到“图中这个人从哪所大学获得荣誉艺术博士学位”这类问题，微调后的 InternVL2.5-8B 只能先做人脸检测，再拿“这个人”去搜索，结果答错。作者在提示词里加一句“还可以调用人脸识别工具”，模型就会调用这个训练时没见过的工具，拿到人名后再去搜索，最终答对。论文据此认为，微调后的模型对新工具有一定的零样本调用能力，但效果不如训练过的工具。论文只给了这一个例子。

### 5. 怎么用？(Usage)

- **文件**：Hugging Face 上有 4 个 JSONL：训练集 ORR 1.69 GB、RR 3.02 GB，验证集 ORR 17 MB、RR 30 MB。直接对整个仓库 `load_dataset` 时，训练 split 会把两个训练文件拼在一起：共 1,642,687 行，前 748,751 行是 ORR，后 893,936 行是 RR；验证 split 有 16,592 行（ORR 7,563、RR 9,029）。
- **只要一种格式时按文件加载**（已实测）：

```python
from datasets import load_dataset

# 只加载 RR 格式的验证集（30 MB）；data_files 指定单个文件时，split 名固定是 "train"
rr = load_dataset("VIS-MPU-Agent/MMAT-1M", data_files="dataset_qa_rr_val_all_RR_sys.jsonl", split="train")
print(len(rr), rr[0]["images"])  # 9029 ['../datasets/llava-cot/geoqa+/images/9767.png']
```

- **图片要自己凑**：数据卡片给的 17 个图片分包放在 S3 上，2026-10-22 访问时返回 `NoSuchBucket`。项目方 2025-12-24 在 [GitHub issue #1](https://github.com/VIS-MPU-Agent/MMAT-1M/issues/1) 里回复，原来的存储桶已不可用，目前只提供标注 JSON，图片要按标注里的路径（如 `../datasets/viscot_dataset/docvqa/...`）到各个原始公开数据集里找。
- **许可证是混合的**：Visual CoT、LLaVA-CoT、InfoSeek 部分是 Apache 2.0；The Cauldron 各子集的许可不一样，由它派生的提示词是 CC BY 4.0；TabMWP 部分是 CC BY-NC-SA 4.0，只能非商用。商用前要逐个来源核对。

## 实测记录

以下统计是 2026-10-22 在上面那个版本的数据上算的：验证集下载到本地逐条统计，训练集通过 Hugging Face 的 datasets-server 接口按行读取。

- **训练 split 里两种格式各多少条**：按行号二分查找系统提示词变化的位置，再随机抽 16 行核对，结果是第 0–748,750 行为 ORR，第 748,751–1,642,686 行为 RR。加上验证集，RR 共 902,965 条，正好等于论文里的对话数；ORR 共 756,314 条，比 RR 少 16%，而正文只说两种格式都用 MMAT-1M（1,090,263 个问答对）训练，没提 ORR 更少。从来源看，ORR 里 InfoSeek 的占比明显更低，而 InfoSeek 最依赖搜索（它的 RR 验证样本里 68% 发起过搜索）：验证集里 InfoSeek 在 ORR 中占 5.9%、在 RR 中占 14.8%；训练集两种格式各随机抽 10 段、每段 50 条，是 5.2% 对 15.4%。
- **验证集和论文表 1 对得上**：表 1 的“推理步数”对应每个问答对里助手的发言轮数（含最后给答案的那一轮），RR 验证集是 2 步 0.7%、3 步 69.9%、4 步 20.2%、5 步及以上 9.1%，论文是 0.7%、70.0%、20.3%、9.0%。按每 100 个问答对的调用次数算，验证集是图片描述 56.7 次、OCR 44.0 次、目标检测 13.5 次、人脸检测 2.0 次、搜索 19.5 次、反思 5.6 次；用表 1 的总数除以 1,090,263 个问答对，分别是 56.9、43.3、14.3、1.8、18.9 和 5.3。
- **多数轨迹很短**：RR 验证集 9,029 条对话里，65.4% 是“调用一轮工具 → 结束推理 → 回答”，表 1 里占七成的“3 步”样本大多是这种。
- **ORR 的输入**：验证集 7,563 条全都预置了 `image_caption` 的结果，69.4% 还带 `label_bbox`，57.2% 带 OCR，30.9% 带人脸检测结果。
- **反思片段**：RR 验证集里共有 593 处 `<SIGNAL>reflection</SIGNAL>`。触发反思的那句话只有 13 种固定说法，比如“Hold on, I need to double-check. The reasoning might be a bit off and could have some sneaky shortcuts.”，都是“推理可能有漏洞”这类套话。随后的反思内容里，483 处（81%）是通用反思，说明上一段推理为什么算“作弊”；其余基本是数学反思，补上省掉的推导。两者约 8:2，和表 1 的比例一致。论文说通用反思会让推理“意识到作弊并加以纠正”，但通用反思的提示词（论文图 7）只要求 GPT-4o 写出作弊的理由，数据里也是这样：这 483 处反思都是指出作弊后就以 `<SIGNAL>end</SIGNAL>` 结束，不再调用工具或重新推理，下一轮照样给出最终答案。
- **图片描述里常常已经有答案**：Image Caption 是 GPT-4o 看着问题生成的（场景图提示词里带着问题）。比如 RR 验证集里有一道 InfoSeek 题问图中植物以什么命名，图片描述写的是“图中是一朵鲜艳的鸢尾花（iris），以希腊女神 Iris 命名”，答案正是 Iris；上面那条 ORR 样本也一样，图片描述里已经写着 Dallas 赢了 Ottawa。在单轮问答的 ORR 验证样本里，去掉是非题的答案、选项字母、少于 4 个字符的答案和问题里已经出现过的答案后还剩 5,057 条，其中 36.5% 的答案原文（忽略大小写和常见标点）直接出现在 `image_caption` 的结果里；在单轮问答且调用过 `image_caption` 的 RR 验证样本里，按同样口径算是 19.4%。实验部分没有交代评测时图片描述、OCR、检测这些工具由什么模型提供，读和 GPT-4o 的对比时要考虑这一点。
- **复算论文表格**：表 3 的平均分是 8 个基准的平均（OCRBench 先除以 10），表 5 是 9 项（多了 Dyn-VQA）的平均，两张表的平均分都能复算出来。对不上的有两处：InternVL2.5-8B 基线的 MathVista，表 3 写 64.5，表 5 写 65.1；正文说 InternVL2.5 系列在 Dyn-VQA 上的相对涨幅在 31.9% 到 60.1% 之间，按表 4 两栏的数字算是 25.0% 到 60.1%。摘要里的“2.7%”和“8.8%”是绝对分差，不是相对涨幅：前者是 8 项平均分 60.7 → 63.4，后者是 Dyn-VQA 的 Golden Query 一栏 35.2 → 44.0；按 Query 一栏算是 27.0 → 36.8。
