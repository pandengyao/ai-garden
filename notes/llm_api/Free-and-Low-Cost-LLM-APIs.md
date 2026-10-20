# 免费与低价大模型 API 调研：额度、价格、套餐与接入

- **成熟度**: 🌿 生长中
- **类型**: 原创调研
- **调研日期**: 2026-10-20（价格和额度抓取于 2026-10-19 至 10-20）
- **作者**: Pandeng Yao（资料由 Hermes Agent 辅助收集和核对）
- **范围**: 国内外有免费额度或价格较低的大模型 API。内容包括免费档、新人赠送、按量付费的低价模型、包月套餐、数据政策，以及各平台的官网、API Key 入口、接口地址和调用方法。
- **依据**: 数据来自官方页面，包括文档、价格页、条款、公告和官方接口。句末的上标数字是引用，对应文末的参考来源。标“（推断）”“（换算）”的内容是根据官方数据推断或换算的；标“（实测）”的内容是 2026-10-20 实际调用或连通测试的结果。
- **单位**: 人民币价格单位是“元 / 百万 tokens”，三个数依次是“输入（未命中缓存）/ 缓存命中 / 输出”。美元价格的顺序相同。
- **时效**: 价格、活动和免费名单变化很快，付费前请以官网为准。

## 一、要点

1. **长期免费、能直接用的**：
   - NVIDIA build：不用绑卡[^52]，每分钟最多 40 次、每天 1 万次[^53]，但只能用于测试和评估[^54]。
   - 智谱 `glm-4.7-flash`：输入和输出都免费，上下文 200K[^1]，支持工具调用[^14]。
   - Kilo Gateway 的 `:free` 模型：每个 IP 每小时 200 次，不登录也能调用[^56]。
   - OpenRouter 的 `:free` 模型：每分钟 20 次。累计购买不满 10 credits 时每天 50 次，满了以后每天 1,000 次[^6]。
2. **新人赠送大多按 token 给**：百炼每个模型约 100 万 tokens，有效期 90 天[^8]；腾讯 TokenHub 每个语言模型 100 万 tokens，有效期 1 年[^32]；火山 50 万 tokens[^24]。小米送 ¥5[^17]，Kimi 送 ¥15 代金券[^78]。
3. **按量付费最便宜的**：
   - 百炼 `qwen-flash` 的输入价 0.15 元起[^35]，`qwen3.7-flash` 和火山 `doubao-seed-2.0-mini` 是 0.2 元起[^88][^26]。这三个都按单次请求的输入长度分档，输入越长单价越高。
   - 不分档的模型里，阶跃 `step-3.5-flash`（0.7 / 0.14 / 2.1）[^18]、智谱 `glm-5.3-flash`（0.8 / 0.23 / 2.8）[^1]、小米 `mimo-v2.6-flash`（1 / 0.02 / 2）[^15] 价格较低。
4. **包月最便宜的**：Chutes Base $3/月，每天 300 次请求[^67]；OpenCode Go $10/月[^49]；千帆 Token Plan Mini ¥9.9/月[^23]；火山 Coding Plan Lite 前两个月 ¥9.9/月[^29]。
5. **编程套餐一般限制用途**：
   - 百炼、千帆、腾讯的个人套餐只能在工具里交互式使用，不能用于自动化脚本或应用后端[^37][^23][^33]。
   - 火山还明确禁止定时任务，个人版的输入和输出授权火山使用[^28]。
   - 智谱不允许把套餐用在自建应用、机器人等场景[^42]。
6. **数据政策**：NVIDIA 试用[^54]、Kilo 免费模型[^57]和 Mistral 免费档[^70]的输入可能被用于训练。Cloudflare[^116]、Chutes[^118]、Ollama[^69] 写明不训练或不记录。
7. **已下线或基本用不了的**：GitHub Models[^64] 和百度 ERNIE Speed/Lite/Tiny[^21] 已经下线；腾讯 hunyuan-lite[^34] 和百炼 qwen-turbo[^36] 也已下线。Gemini API 的可用地区不包括中国大陆和香港[^5]。

## 二、免费额度

### 2.1 长期免费

| 平台 | 免费内容 | 限额和条件 | 数据 |
| --- | --- | --- | --- |
| NVIDIA build | 所有模型都有免费试用，不用绑卡[^52]；免费端点共 39 个模型[^108]，包括 DeepSeek V4.1 Flash、Kimi K2.6、GLM-5.3 等[^55] | 每分钟最多 40 次、每天 1 万次[^53]；只能用于内部测试和评估，不能用于生产[^54] | 可能被用于改进模型[^54] |
| 智谱 | `glm-4.7-flash` 输入输出免费，200K 上下文[^1] | 官方没写限速 | — |
| Kilo Gateway | `:free` 模型零成本，匿名用户也能调[^56]；10-19 共有 17 个免费模型（按接口返回统计）[^57] | 每个 IP 每小时 200 次，超限返回 429[^56] | 免费模型都标注可能用于训练[^57] |
| OpenRouter | 10-19 共有 16 个 `:free` 模型（按接口返回统计），包括 1M 上下文的 Nemotron 3 Ultra[^11] | 每分钟 20 次；累计购买不满 10 credits 时每天 50 次，满了以后每天 1,000 次[^6] | 因模型而异 |
| OpenCode Zen | DeepSeek V4.1 Flash Free、GLM-5.3-Flash Free 等模型限时免费[^51] | 拿 API key 前要先填账单信息并充值[^51]；免费限额未公布 | 因模型而异，见第六节 |
| Nous Portal | Free 档可以用免费模型[^68] | 被限流时整个服务都会暂停[^75] | 不开 Privacy Mode 时可能用于训练[^76] |
| 魔搭 ModelScope | API-Inference 免费提供给开发者体验[^10] | 要绑定阿里云账号并实名，原则上只保证单并发[^10] | — |
| 讯飞星火 | Spark Lite 免费不限量[^90]；`spark-x2.5-4b` 限时免费，`spark-x2.5-1.7b` 免费，两者都是 1M 上下文[^91] | Spark Lite 要实名，并且只能绑定一个应用[^90]；输入最多 8K[^72] | — |
| 硅基流动 | `XingChenAGI/Xing4.0-29B`、`tencent/Hunyuan-MT-7B` 等模型免费[^9] | 限速没核实 | — |
| Mistral | Free mode，不用绑卡[^102] | 限额不公开，要登录后台查看[^71] | 默认可能用于训练，可以关闭[^70] |
| Cohere | Trial key 免费[^59] | 每月 1,000 次，每分钟 20 次[^59]；不能用于生产或商业用途[^60] | 不适用企业数据承诺[^117] |
| 火山 协作奖励计划 | 授权使用推理数据后，次日返还等量的免费资源包，每个模型每天最多 500 万 tokens[^27] | 只适用于仍在计划内的模型，目前入口只支持 Doubao-Seed-Evolving[^27] | 授权的数据火山可以永久使用[^27] |

### 2.2 新人赠送

| 平台 | 赠送内容 | 条件 |
| --- | --- | --- |
| 阿里百炼 | 每个模型约 100 万 tokens，有效期 90 天[^8] | 只限北京地域；已认证用户用完后自动转为按量付费[^8] |
| 腾讯 TokenHub | 每个语言模型 100 万 tokens，有效期 1 年[^32] | 活动到 2026-12-31；文档另一处写“同一账号下的所有模型共享额度”，两种说法有冲突[^32] |
| 火山方舟 | 安心体验模式 50 万 tokens，额度快用完时服务自动暂停[^24] | 只有从没开通过模型服务的账号能开启，关闭后不能再开[^24] |
| 百度千帆 | 新用户每个模型 100 万 tokens，有效期 3 个月[^83] | 名单里的模型大多已经退役[^21] |
| 小米 MiMo | 首次实名认证送 ¥5，有效期 40 天[^17] | 只限中国大陆用户[^17] |
| Kimi | 认证后送 ¥15 代金券[^78] | 不能用于 Kimi K3[^78]；代金券不计入限速档位的累计充值[^46] |
| 美团 LongCat | 控制台文案写实名后送 1,000 万 tokens，另有每日免费额度[^74] | 正式文档没写 |
| 阶跃星辰 | 文档提到有“免费套餐”，使用前要实名[^19] | 额度没写；官方通知将关闭 Step Plan 免费体验的新增领取[^77] |

## 三、按量付费：低价模型

### 3.1 人民币价格（元 / 百万 tokens）

| 模型 | 平台 | 输入 / 缓存命中 / 输出 | 上下文 | 工具调用 |
| --- | --- | --- | --- | --- |
| `qwen-flash` | 阿里百炼 | ≤128K：0.15 / 0.03 / 1.5；128K–256K：0.6 / 0.12 / 6；256K–1M：1.2 / 0.24 / 12[^35] | 1M[^35] | 北京地域支持[^35] |
| `qwen3.7-flash` | 阿里百炼 | ≤32K：0.2 / 0.04 / 0.8；32K–256K：0.6 / 0.12 / 2.4[^88] | 1M[^88] | 支持[^88] |
| `doubao-seed-2-0-mini-260428` | 火山方舟 | ≤32K：0.2 / 0.04 / 2；32K–128K：0.4 / 0.08 / 4；128K–256K：0.8 / 0.16 / 8[^26] | 256K[^25] | 支持[^25] |
| `step-3.5-flash` | 阶跃星辰 | 0.7 / 0.14 / 2.1[^18] | 256K[^18] | 支持[^18] |
| `doubao-seed-2-1-lite-260915` | 火山方舟 | 0.8 / 0.16 / 2.7[^26] | 1M[^25] | 支持[^25] |
| `glm-5.3-flash` | 智谱；火山[^26]、腾讯[^86]、千帆[^84] 同价 | 0.8 / 0.23 / 2.8[^1] | 1M[^1] | 支持[^87] |
| `mimo-v2.6-flash` | 小米；腾讯同价[^86] | 1 / 0.02 / 2[^15] | 1M[^16] | 支持[^16] |
| `deepseek-flash`（V4.1 Flash） | DeepSeek；火山[^26]、腾讯[^86] 同价 | 空闲 1 / 0.02 / 4；高峰 2 / 0.04 / 8[^3] | 1M[^3] | 支持[^3] |
| `deepseek-v4-flash` | 腾讯 TokenHub | 1 / 0.2 / 2[^86] | 1M[^87] | 支持[^87] |
| `MiniMax-M3.1-Flash` | MiniMax | 1 / 0.1 / 4[^97] | 1M[^98] | 支持[^98] |
| `hy3` | 腾讯 TokenHub | 1 / 0.25 / 4[^86] | 256K[^87] | 支持[^87] |
| `LongCat-2.5-Preview` | 美团 | 2 / 0.04 / 8，限时价[^73] | 1M[^94] | Agentic 模型[^94] |
| `kimi-k2.6` | Kimi | 6.5 / 1.1 / 27[^96] | 256K[^96] | 支持多步工具调用[^78] |

- 分档计价的模型按单次请求的输入长度定档，输入越长，整次请求的单价越高[^35][^26]。
- DeepSeek 的高峰时段是工作日 9:00–12:00 和 14:00–18:00，不含法定节假日[^3]。火山和腾讯的 DeepSeek 也分峰谷[^26][^86]。千帆的高峰时段是每天 8:00–22:00[^84]。
- 火山的低优（Flex）模式输入和输出约为半价[^26]，但请求最多会排队 20 分钟[^123]。火山还对缓存存储另收 0.017 元/百万 tokens/小时[^26]。
- LongCat 现在的价格是原价的 4 折，原价是 5 / 0.1 / 20[^74]。

### 3.2 美元价格（美元 / 百万 tokens）

| 模型 | 平台 | 输入 / 缓存命中 / 输出 |
| --- | --- | --- |
| `deepseek-v4.1-flash` | Ollama Cloud | 0.30 / 0.006 / 1.20，非高峰半价[^69] |
| DeepSeek V4.1 Flash | OpenCode Go（从套餐额度扣） | 高峰 0.30 / 0.006 / 1.20，非高峰 0.15 / 0.003 / 0.60[^49] |
| `LongCat-2.5-Preview` | 美团（海外） | 0.30 / 0.006 / 1.20[^73] |
| `glm-5.3-flash` | Ollama Cloud | 0.15 / 0.03 / 0.50[^69] |
| `deepseek-ai/DeepSeek-V4-Flash-0731-TEE` | Chutes | 0.44 / — / 1.32[^67] |
| `@cf/zai-org/glm-4.7-flash` | Cloudflare | 0.0605 / — / 0.40[^115] |

## 四、包月和订阅套餐

| 套餐 | 价格 | 额度 | 主要限制 |
| --- | --- | --- | --- |
| Chutes | Base $3、Plus $10、Pro $20，均为每月[^67] | 每天 300 / 2,000 / 5,000 次请求[^67]；按请求次数计，不按 token[^66] | 没有免费档；经 Stripe 付款，支持加密货币、银行卡和银行转账[^66] |
| OpenCode Go | Go $10、Go Plus $40，均为每月[^49] | 每个模型单独设月度美元额度，例如 Go 档 DeepSeek V4.1 Flash $80、GLM-5.3-Flash $60；5 小时内最多用掉 20%，每周最多 50%[^49] | 面向 OpenCode 这类编程 agent，会监控滥用流量；服务主要面向国际用户[^49] |
| Ollama Cloud | Pro $20、Max $100，均为每月[^69] | 每月分别含 $60、$300 用量[^69] | Free 档只有 1 个并发[^69] |
| 阶跃 Step Plan | Mini ¥49、Plus ¥99、Pro ¥199、Max ¥699，均为每月[^19] | 每月 400M / 1,600M / 8,000M / 40,000M Credit，1 元 = 100 万 Credit；高峰时段消耗翻倍[^19] | 购买名额每天限量[^77] |
| 智谱 GLM Coding Plan | Lite ¥118、Pro ¥538、Max ¥1,078，均为每月[^41] | 每 5 小时 / 每周的积分：Lite 2,000 / 10,000，Pro 12,000 / 60,000，Max 28,000 / 140,000；非高峰时段只扣一半[^39] | 只能在官方列出的工具里使用[^42]；通用 Agent 工具的优先级低于编程工具，高负载时可能排队[^40] |
| 百炼 Coding Plan | Pro 首月 ¥39.9，之后每月 ¥200；Lite 已停售[^37] | 每 5 小时 6,000 次，每周 4.5 万次，每月 9 万次模型调用[^37] | 只能在编程工具里使用；首月优惠名额每天 9:30 补充[^37] |
| 百炼 Token Plan 个人版 | Lite 限时 ¥39/月（原价 ¥60）起[^38] | 每月 11,500 Credits 起[^38] | 同一实名主体限购一份[^38] |
| 火山 Coding Plan | Lite ¥40/月、Pro ¥200/月；11-08 前购买，前两个月打 2.5 折，即 ¥9.9 和 ¥49.9[^29] | 官方按 Doubao Seed 2.0 Lite 估算：Lite 每月约 1.8 万次请求，Pro 是 Lite 的 5 倍[^31] | 不能用于 API 调用[^30]；个人版的输入和输出授权火山使用[^28] |
| 火山 Agent Plan | Small ¥40、Medium ¥200、Large ¥500、Max ¥1,000，均为每月[^133] | 每月 2 万 / 10 万 / 25 万 / 50 万 AFP[^133] | 和 Coding Plan 适用同一份条款[^28] |
| 千帆 Token Plan 个人版 | Mini ¥9.9、Lite ¥40、Pro ¥200、Max ¥600，均为每月[^23]；新用户首购五折[^101] | Token 制每月 1,000 万 / 4,200 万 / 2.3 亿 / 7 亿 tokens，输入、输出、缓存都按实际数量扣[^23] | 购买后不退费、不能降配[^23] |
| 腾讯 Token Plan | 通用版 Lite ¥39/月起，混元版 Lite ¥28/月起[^33] | Lite 每月 780 积分，混元版 560 积分[^33] | 不支持退款[^33] |
| Kimi 会员 | Plus ¥99/月、Pro ¥199/月起；Go ¥49/月不含 Kimi Code[^43] | Kimi Code 有滚动 5 小时限额和月度共享额度池，没公布具体数值[^43] | 不得以商业目的转售账号或 API 访问权限[^45] |
| MiniMax M Plan | Go ¥49、Explore ¥119、Build ¥469，均为每月[^48] | 只公布了相对倍数（1 / 3 / 12 倍），有 5 小时窗口和周窗口[^47] | 生产环境官方建议用按量付费[^47] |

使用范围：

- **只能在工具里交互式使用**：百炼[^37]、千帆[^23]、腾讯[^33] 的套餐都写明了这一点，并禁止用于自动化脚本或应用后端。Kimi Code 也只限个人交互式使用，脚本批量调用超出正常使用范围[^45]。
- **火山**：条款还明确禁止定时任务等程序化调用[^28]。
- **智谱**：不允许用在自建应用、机器人、网站等场景[^42]。
- **阶跃**：官方的 Agent 工具接入文档写到，可以让 agent 执行定时任务等自动化工作[^19]。

## 五、不推荐或已下线

| 平台 | 原因 |
| --- | --- |
| GitHub Models | 2026-07-30 已全面下线[^64] |
| Groq 免费档 | 以 gpt-oss-120b 为例，每分钟 30 次、每天 1,000 次、每分钟 8K tokens[^7]，长上下文请求很容易超限（推断） |
| Cerebras | 没有长期免费档；绑卡后才给一次性 $5，30 天后过期[^62]；免费档上下文只有 64K[^63] |
| SambaNova | 免费档每个模型每天 20 次请求、20 万 tokens[^61]；是否需要绑卡，官方页面说法不一致[^109] |
| Cloudflare Workers AI | 每天 1 万 neurons；Kimi K2.6、GLM-5.3、DeepSeek V4 等较强的模型要付费才能用[^58]。按 glm-4.7-flash 每百万输入消耗 5,500 neurons 算，1 万 neurons 约合 180 万输入 tokens（换算） |
| Google Gemini | 可用地区不包括中国大陆和香港[^5]；免费档的数据用于改进产品[^4] |
| Hugging Face | 免费用户不再赠送额度[^65]；PRO $9/月只含 $2 额度[^113] |
| 讯飞 Spark Lite | 输入最多 8K、输出最多 4K tokens；文档只写了 4.0Ultra 和 Max 支持 Function Call[^72] |
| 百度 ERNIE Speed / Lite / Tiny | 2026-06 已退役[^21] |
| 腾讯 hunyuan-lite | 2026-06-22 下线[^34] |
| 百炼 qwen-turbo | 2026-10-10 下线[^36] |
| MiniMax M2.5 / M2.7 | 10-19 起不再向新用户开放，11-18 下线[^98] |

## 六、数据政策

| 平台 / 档位 | 数据会不会被用于训练 |
| --- | --- |
| NVIDIA 试用 | 条款一处写会话结束后不存储、不使用，另一处写会收集内容来改进模型，应按“可能会”对待[^54] |
| Kilo 免费模型 | 全部标注可能用于训练[^57] |
| Mistral Free mode | 可能会，默认参与，可以关闭[^70] |
| Gemini 免费档 | 用于改进产品[^4] |
| Nous Portal | 不开 Privacy Mode 时可能会[^76] |
| 火山 Coding / Agent Plan 个人版 | 输入和输出授权火山存储和使用[^28] |
| Cohere trial | 不适用企业数据承诺；prompt 和生成内容保留 30 天，可以在后台关闭训练用途[^117] |
| OpenCode Zen 免费模型 | 因模型而异：GLM-5.3-Flash Free、DeepSeek V4.1 Flash Free 的供应商零留存、不训练；Big Pickle 在免费期内可能用于改进模型[^51] |
| OpenCode Go | DeepSeek 的零留存协议按月续签，目前有效到 2026-10-31[^49] |
| Cloudflare Workers AI | 不用于训练[^116] |
| Chutes | 不记录、不存储请求和响应[^118] |
| Ollama Cloud | 不记录、不训练[^69] |
| Cerebras | 不存储、不利用输入和输出[^106]；条款不授权用于训练[^107] |

## 七、怎么使用

### 7.1 通用步骤

1. 注册账号。国内平台大多要求实名认证，例如腾讯 TokenHub[^85] 和魔搭[^10]。LongCat[^73] 和阶跃[^19] 在充值或付费前也要实名。
2. 在控制台创建 API Key，入口见 7.2。有些平台的 key 只在创建时显示一次，例如 LongCat[^94]。
3. 这些平台大多提供 OpenAI 兼容接口，地址见 7.2。换平台时一般只需要改 base_url、api_key 和 model 三项，火山方舟的文档就是这样写的[^82]。

curl 示例（以 NVIDIA 为例）：

```bash
export NVIDIA_API_KEY="nvapi-..."   # 换成自己的 key

curl https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-ai/deepseek-v4.1-flash", "messages": [{"role": "user", "content": "你好"}]}'
```

Python 示例（先 `pip install openai`）：

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",  # 换平台时改这里
    api_key=os.environ["NVIDIA_API_KEY"],            # 和这里
)
resp = client.chat.completions.create(
    model="deepseek-ai/deepseek-v4.1-flash",         # 以及模型 ID
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

不需要 key 的例子：Kilo 的免费模型，10-20 实测能正常返回（实测）。注意，免费模型的输入可能被用于训练[^57]。

```bash
curl https://ai-gateway.kilo.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "nvidia/nemotron-3-ultra-550b-a55b:free", "messages": [{"role": "user", "content": "Reply with exactly: OK"}]}'
```

### 7.2 各平台接口速查

国内平台：

| 平台 | 官网 | API Key 入口 | base_url（OpenAI 兼容） | 模型 ID 示例 |
| --- | --- | --- | --- | --- |
| 智谱 | <https://bigmodel.cn> | <https://bigmodel.cn/usercenter/proj-mgmt/apikeys>[^119] | `https://open.bigmodel.cn/api/paas/v4`[^119]；Coding Plan 用 `https://open.bigmodel.cn/api/coding/paas/v4`[^40] | `glm-4.7-flash`[^14]、`glm-5.3-flash`[^139] |
| DeepSeek | <https://platform.deepseek.com> | <https://platform.deepseek.com/api_keys>[^146] | `https://api.deepseek.com`[^3] | `deepseek-flash`、`deepseek-v4-pro`[^3] |
| 小米 MiMo | <https://platform.xiaomimimo.com> | <https://platform.xiaomimimo.com/#/console/api-keys>[^16] | `https://api.xiaomimimo.com/v1`[^16] | `mimo-v2.6-flash`[^15] |
| 阶跃星辰 | <https://platform.stepfun.com> | <https://platform.stepfun.com/interface-key>[^120] | 按量：`https://api.stepfun.com/v1`[^18]；Step Plan：`https://api.stepfun.com/step_plan/v1`[^19] | `step-3.5-flash`[^18] |
| 阿里百炼 | <https://bailian.console.aliyun.com> | <https://bailian.console.aliyun.com/cn-beijing/settings/api-key>[^121] | `https://dashscope.aliyuncs.com/compatible-mode/v1`[^122]；Coding Plan 用 `https://coding.dashscope.aliyuncs.com/v1`[^37] | `qwen-flash`[^35]、`qwen3.7-flash`[^88] |
| 火山方舟 | <https://www.volcengine.com/product/ark> | <https://ark.volcengine.com/region:cn-beijing/apiKey>[^123] | `https://ark.cn-beijing.volces.com/api/v3`[^82]；Coding Plan 用 `…/api/coding/v3`[^30]；Agent Plan 用 `…/api/plan/v3`[^124] | `doubao-seed-2-1-lite-260915`、`deepseek-v4-1-flash-261017`[^25] |
| 腾讯 TokenHub | <https://cloud.tencent.com/product/tokenhub> | TokenHub 控制台的“API Key 管理”页[^85] | `https://tokenhub.tencentmaas.com/v1`[^85]；Token Plan 用 `https://api.lkeap.cloud.tencent.com/plan/v3`[^33] | `hy3`、`deepseek-v4.1-flash`[^87] |
| 百度千帆 | <https://cloud.baidu.com/product/qianfan.html> | 千帆控制台：系统管理 → 创建 API Key[^137] | `https://qianfan.baidubce.com/v2`[^137]；Token Plan 用 `https://qianfan.baidubce.com/v2/tokenplan/personal`[^23] | `deepseek-v4.1-flash`[^20] |
| Kimi | <https://platform.kimi.com> | <https://platform.kimi.com/console/api-keys>[^78] | `https://api.moonshot.cn/v1`[^78]；Kimi Code 会员用 `https://api.kimi.com/coding/v1`[^44] | `kimi-k2.6`[^96] |
| MiniMax | <https://platform.minimaxi.com> | <https://platform.minimax.cn/user-center/basic-information/interface-key>[^98] | `https://api.minimax.cn/v1`[^98] | `MiniMax-M3.1-Flash`[^97]；M Plan 用 `MiniMax-M3.1-Flash-Preview`[^100] |
| 美团 LongCat | <https://longcat.chat/platform> | 登录后在 API Keys 页创建[^94] | `https://api.longcat.chat/openai`[^94] | `LongCat-2.5-Preview`[^94] |
| 讯飞星火 | <https://xinghuo.xfyun.cn> | 控制台 <https://console.xfyun.cn> | Spark Lite：`https://spark-api-open.xf-yun.com/v1/`[^72]；星辰 MaaS：`https://maas-api.cn-huabei-1.xf-yun.com/v2`[^93] | `spark-x2.5-4b`[^92] |
| 魔搭 | <https://modelscope.cn> | <https://modelscope.cn/my/myaccesstoken>[^125] | `https://api-inference.modelscope.cn/v1/`[^125] | `Qwen/Qwen3.5-35B-A3B`[^125] |
| 硅基流动 | <https://siliconflow.cn> | 控制台的“API 密钥”页[^126] | `https://api.siliconflow.cn/v1`[^126] | `XingChenAGI/Xing4.0-29B`[^9] |

海外平台：

| 平台 | 官网 | API Key 入口 | base_url（OpenAI 兼容） | 模型 ID 示例 |
| --- | --- | --- | --- | --- |
| NVIDIA build | <https://build.nvidia.com> | <https://build.nvidia.com/settings/api-keys>，key 以 `nvapi-` 开头[^52][^12] | `https://integrate.api.nvidia.com/v1`[^52] | `deepseek-ai/deepseek-v4.1-flash`、`moonshotai/kimi-k2.6`[^55] |
| OpenRouter | <https://openrouter.ai> | <https://openrouter.ai/keys>[^138] | `https://openrouter.ai/api/v1`[^127] | `nvidia/nemotron-3-ultra-550b-a55b:free`[^11] |
| Kilo Gateway | <https://kilo.ai> | 用 Kilo 账号生成[^128]，具体页面没核实 | `https://ai-gateway.kilo.ai/api/v1`[^128] | `nvidia/nemotron-3-ultra-550b-a55b:free`[^57] |
| OpenCode | <https://opencode.ai> | <https://opencode.ai/auth>，要先填账单信息[^144] | Go：`https://opencode.ai/zen/go/v1`[^140][^75] | `deepseek-v4.1-flash`、`glm-5.3-flash`[^140] |
| Chutes | <https://chutes.ai> | key 以 `cpk_` 开头[^67]，入口没核实 | `https://llm.chutes.ai/v1`[^67] | `deepseek-ai/DeepSeek-V4-Flash-0731-TEE`[^67] |
| Ollama Cloud | <https://ollama.com> | <https://ollama.com/settings/keys>[^143] | `https://ollama.com/v1`[^142] | `deepseek-v4.1-flash`[^69] |
| Mistral | <https://console.mistral.ai> | <https://console.mistral.ai/api-keys>[^131] | `https://api.mistral.ai/v1`[^131] | `mistral-small-latest`[^102] |
| Cohere | <https://dashboard.cohere.com> | <https://dashboard.cohere.com/api-keys>[^59] | `https://api.cohere.ai/compatibility/v1`[^130] | `command-a-plus-05-2026`[^130] |
| Cloudflare | <https://dash.cloudflare.com> | 用 API token，并在地址里填 account_id[^129] | `https://api.cloudflare.com/client/v4/accounts/<account_id>/ai/v1`[^129] | `@cf/zai-org/glm-4.7-flash`[^58] |

### 7.3 各平台注意事项

#### 国内平台

- **智谱**：用标准 API Key 调 `/api/paas/v4` 扣的是账户余额，不消耗 Coding Plan 额度[^119]。要用套餐额度，必须走 `/api/coding/paas/v4`[^40]。
- **DeepSeek**：
  - 模型名用 `deepseek-flash`。旧名 `deepseek-v4-flash` 还能调用，请求会交给 V4.1 Flash 处理[^3]。
  - 另有 Anthropic 格式的地址 `https://api.deepseek.com/anthropic`[^3]。
  - `deepseek-v4-pro` 的价格：空闲 4.5 / 0.15 / 13.5，高峰 9 / 0.3 / 27[^3]。
- **小米 MiMo**：
  - 国内账号和海外账号的 Base URL、key 不互通[^16]。
  - 每分钟最多 100 次请求、TPM 1,000 万[^16]。
  - `mimo-v2.6-pro` 的价格是 3 / 0.025 / 6[^15]。V2.5 系列 10-21 下线[^15]。
  - 国内支持微信、支付宝和小米支付[^16]。
  - 另有 Token Plan，地址是 `https://token-plan-cn.xiaomimimo.com/v1`[^16]，价格没查。
- **阶跃星辰**：按量 API 按累计现金充值分档限速，不足 ¥100 时并发 5、RPM 100、TPM 50 万[^19]。Step Plan 不受这套限速约束，用普通按量 API 也不会扣 Step Plan 额度[^19]。
- **阿里百炼**：上表的地址是北京地域[^122]，新人额度也只在北京地域有效[^8]。`qwen-flash` 在新加坡地域不支持 Function Calling[^35]。
- **火山方舟**：调用前要先在开通管理页开通模型[^123]。模型 ID 带版本号[^25]。
- **腾讯 TokenHub**：使用前要实名，并先领取免费体验包，再创建 API Key[^85]。
- **百度千帆**：Function calling 文档的支持列表里没有 DeepSeek-V4.1-Flash[^22]，能不能调工具要实测。
- **Kimi**：
  - 累计充值为 0 时，并发 1、RPM 3、每天 150 万 tokens；累计充值满 ¥50 后 RPM 升到 100[^46]。
  - 调用 K3 要先充值至少 10 元[^78]。
- **MiniMax**：国内用 `api.minimax.cn`，国际用 `api.minimax.io`[^98]。免费用户 RPM 20、TPM 100 万，充值用户 RPM 200[^98]。
- **美团 LongCat**：
  - 对话接口的完整地址是 `https://api.longcat.chat/openai/v1/chat/completions`[^141]。
  - 大陆用户充值前要实名[^73]。
  - 10-20 测试时，默认 DNS 解析不了 `api.longcat.chat`，改用 223.5.5.5 或 8.8.8.8 可以解析（实测）。
- **讯飞星火**：旧版星火 API 和星辰 MaaS 是两套接口。星辰 MaaS 每个 Key 的每个模型默认并发 20、TPM 100 万[^93]。
- **魔搭**：模型 ID 用魔搭的 Model-Id[^125]。也可以用魔粒兑换调用次数，每次 0.5–2 魔粒[^10]。

#### 海外平台

- **NVIDIA build**：
  - 注册者要达到当地法定成年年龄[^54]。条款里的“internal”限制的是用途，不是只有 NVIDIA 员工能用（推断）。
  - 条款要求不要提交机密信息或敏感数据[^54]。
  - 模型页写明 `deepseek-v4.1-flash` 支持最多 100 万 tokens 上下文[^80]。GLM-5.3 在 10-19 被标注“9 天后弃用”[^108]。
- **OpenRouter**：免费模型的每日上限取决于累计购买的 credits[^6]。
- **Kilo Gateway**：
  - 请求里不带 Authorization 头可以匿名调用免费模型；带了无效 key 会被拒绝（实测）。
  - 部分免费模型要求允许数据收集[^56]。购买 credits 另收 5% 手续费[^56]。
- **OpenCode**：
  - 经 Stripe 付款，支持银行卡、支付宝和微信，另收 4.6% + $0.31 手续费[^50]。
  - Beam Free 不对中国大陆和港澳开放[^51]。
  - DeepSeek 的高峰时段是工作日 UTC 01:00–04:00 和 06:00–10:00[^49]，对应北京时间 9:00–12:00 和 14:00–18:00（换算）。
  - 官方估算表里，Go 档每月约可发 DeepSeek V4.1 Flash 17.3 万次请求，或 GLM-5.3-Flash 3.2 万次请求[^49]。DeepSeek 一栏按每次请求 410 输入、71,300 缓存、310 输出 token 估算[^49]。
- **Chutes**：没有免费档，要先充值[^66]。官方没写每日请求额度是否适用于所有模型。
- **Ollama Cloud**：
  - 非高峰时段指工作日 UTC 12:00–18:00 以外的时间和周末全天[^69]。换成北京时间，高峰是工作日 20:00 到次日 2:00（换算）。
  - 服务主要托管在美国[^69]。
- **Mistral**：API 默认由欧盟机房提供服务[^104]。
- **Cohere**：生产 key 要在后台走 Go to Production 流程申请[^60]。

## 八、国内网络连通性测试（2026-10-20）

- 测试方法：在国内网络下用 curl 直连各平台的 API 地址，不走代理。结果只代表测试时的这一个网络环境。
- 能连通（返回 200、401、403、405 或 429）的平台：NVIDIA、智谱、DeepSeek、小米、阶跃、Kimi、MiniMax、百炼、火山、腾讯、千帆、硅基流动、魔搭、OpenRouter、Kilo、OpenCode、Chutes、Ollama、Nous、Cohere、Mistral、Cloudflare、Gemini、Groq、Cerebras、SambaNova、Hugging Face。
- 连不通的：`api.longcat.chat`，原因是默认 DNS 解析失败，换公共 DNS 后可以解析。
- 能连通不代表平台允许中国大陆用户使用。例如 Gemini 的可用地区不包括中国大陆和香港[^5]，OpenCode Go 写明主要面向国际用户[^49]。

## 九、待确认

- NVIDIA：注册时是否要手机验证、+86 号码能否通过；各托管端点实际允许的上下文长度。
- 智谱：`glm-4.7-flash` 的限速。
- Kilo、Chutes：API key 在哪个页面生成。Chutes 的 Base $3 档能否在网页上购买、每日额度是否适用于所有模型、能否用支付宝付款。
- Kimi 会员、MiniMax M Plan、百炼和腾讯的 Token Plan、火山 Agent Plan：额度换算成请求次数或 tokens 是多少。
- 千帆：`deepseek-v4.1-flash` 是否支持工具调用。
- 腾讯 TokenHub：新人额度是“每个模型 100 万”还是“账号内共享 100 万”。
- LongCat：当前每日免费额度是多少；`api.longcat.chat` 的 DNS 问题是否普遍存在。
- Mistral：Free mode 的具体限额，以及注册是否需要手机验证。
- 阶跃“免费套餐”的额度；小米 MiMo Token Plan 的价格。

## 附录：在 Hermes Agent 中接入

本节只列通用接入方法，按 Hermes v0.22.2 的文档和实测整理。

内置 provider：把 key 写进 `.env`，再设置 provider 和模型即可[^12]。每个 profile 有自己的 `.env`[^75]。

```bash
# 在 ~/.hermes/.env 里加一行 NVIDIA_API_KEY=nvapi-…，然后：
hermes config set model.provider nvidia
hermes config set model.default deepseek-ai/deepseek-v4.1-flash
hermes chat -q "回复 OK" --oneshot
```

| 平台 | provider | `.env` 变量 | 备注 |
| --- | --- | --- | --- |
| NVIDIA build | `nvidia` | `NVIDIA_API_KEY` | — |
| 智谱 | `zai` | `GLM_API_KEY` | 会自动探测国内外地址[^12]；只用免费模型时，建议显式设 `GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4`（推断） |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` | — |
| 小米 MiMo | `xiaomi` | `XIAOMI_API_KEY` | — |
| 阶跃 Step Plan | `stepfun` | `STEPFUN_API_KEY` | 默认是国际站；国内账号设 `STEPFUN_BASE_URL=https://api.stepfun.com/step_plan/v1`（实测） |
| 阿里百炼 | `alibaba-cn` | `DASHSCOPE_API_KEY` | Coding Plan 用 `alibaba-coding-plan-cn`，Token Plan 用 `alibaba-token-plan-cn`[^12] |
| 腾讯 TokenHub | `tencent-tokenhub` | `TOKENHUB_API_KEY` | Token Plan 用 `tencent-tokenplan`[^12] |
| Kimi | `kimi-coding-cn` | `KIMI_CN_API_KEY` | Kimi Code 会员 key 用 `kimi-coding` 和 `KIMI_API_KEY`（实测） |
| MiniMax | `minimax-cn` | `MINIMAX_CN_API_KEY` | — |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | 也可以用 `hermes auth add openrouter`[^12] |
| Kilo Gateway | `kilocode` | `KILOCODE_API_KEY` | — |
| OpenCode Go / Zen | `opencode-go` / `opencode-zen` | `OPENCODE_GO_API_KEY` / `OPENCODE_ZEN_API_KEY` | — |
| Ollama Cloud | `ollama-cloud` | `OLLAMA_API_KEY` | — |
| Hugging Face | `huggingface` | `HF_TOKEN` | — |
| Nous Portal | `nous` | 不用 key | 在 `hermes model` 里用 OAuth 登录[^12] |

provider 名称和变量名来自 Hermes 的 provider 注册表，官方文档的说明见[^12]。

没有内置 provider 的平台（火山、千帆、LongCat、讯飞、魔搭、硅基流动、Chutes、Cohere、Mistral、Cloudflare）可以按自定义 provider 接入，key 用 `key_env` 指定[^12]。以 Chutes 为例（实测可用）：

```bash
# 在 .env 里加一行 CHUTES_API_KEY=cpk_…，然后：
hermes config set providers.chutes.name Chutes
hermes config set providers.chutes.base_url https://llm.chutes.ai/v1
hermes config set providers.chutes.key_env CHUTES_API_KEY
hermes config set providers.chutes.api_mode chat_completions
hermes config set model.provider chutes
hermes config set model.default deepseek-ai/DeepSeek-V4-Flash-0731-TEE
```

注意事项：

- 从一个自定义地址切到内置 provider 时，旧的 `model.base_url` 不会自动清除，请求仍会发到旧地址。这时要执行 `hermes config unset model.base_url`（实测）。
- Hermes 要求模型上下文至少 64K[^12]，所以讯飞 Spark Lite 这类 8K 的模型用不了。
- 官方接入名单里有 Hermes Agent 的套餐：
  - 智谱 GLM Coding Plan[^40]
  - 百炼 Coding Plan[^37]
  - 千帆 Token Plan[^23]
  - 火山 Coding Plan[^30] 和 Agent Plan[^133]
  - MiniMax M Plan[^47]
  - Kimi Code[^44]
  - 阶跃 Step Plan[^19]
  - OpenCode Go[^49]

## 参考来源

文中引用的官方页面如下，抓取时间为 2026-10-19 至 10-20。

[^1]: [智谱 API 定价](https://docs.bigmodel.cn/cn/guide/start/pricing.md)
[^3]: [DeepSeek 模型 & 价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)
[^4]: [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
[^5]: [Gemini API available regions](https://ai.google.dev/gemini-api/docs/available-regions)
[^6]: [OpenRouter Limits](https://openrouter.ai/docs/api/reference/limits)
[^7]: [Groq rate limits](https://console.groq.com/docs/rate-limits)
[^8]: [阿里云百炼 新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)
[^9]: [硅基流动 价格](https://siliconflow.cn/pricing)
[^10]: [魔搭 API-Inference 使用限制](https://resouces.modelscope.cn/document/docdata/2026-10-9_16-57-CN/dist/model-service/API-Inference/limits/limits_CN.md)
[^11]: [OpenRouter models API](https://openrouter.ai/api/v1/models)
[^12]: [Hermes docs: AI Providers](https://hermes-agent.nousresearch.com/docs/integrations/providers)
[^14]: [智谱 GLM-4.7-Flash](https://docs.bigmodel.cn/cn/guide/models/free/glm-4.7-flash)
[^15]: [小米 MiMo 按量计费](https://mimo.mi.com/docs/zh-CN/price/pay-as-you-go)
[^16]: [小米 MiMo 文档（llms-full）](https://mimo.mi.com/llms-full.txt)
[^17]: [小米 MiMo 新客赠金](https://mimo.mi.com/docs/zh-CN/quick-start/promotions/new%20user)
[^18]: [阶跃 step-3.5-flash](https://platform.stepfun.com/docs/zh/guides/models/step-3.5-flash.md)
[^19]: [阶跃星辰文档（llms-full）](https://platform.stepfun.com/docs/llms-full.txt)
[^20]: [千帆 模型列表](https://cloud.baidu.com/doc/qianfan/s/rmh4stp0j)
[^21]: [千帆 模型退役记录](https://cloud.baidu.com/doc/qianfan/s/zmh4stou3)
[^22]: [千帆 Function calling](https://cloud.baidu.com/doc/qianfan-docs/s/xm95lyys5)
[^23]: [千帆 Token Plan 个人版](https://cloud.baidu.com/doc/qianfan/s/Dmrabu8b6)
[^24]: [火山方舟 安心体验模式](https://www.volcengine.com/docs/82379/1465347)
[^25]: [火山方舟 模型列表](https://www.volcengine.com/docs/82379/1330310)
[^26]: [火山方舟 模型价格](https://www.volcengine.com/docs/82379/1544106)
[^27]: [火山方舟 协作奖励计划](https://www.volcengine.com/docs/82379/1391869)
[^28]: [火山方舟 订阅套餐专用条款](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=subscription-package-service-terms-conditions&type=online)
[^29]: [火山方舟 Coding Plan 2.5 折活动](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=coding-plan-personal-universal-promotion&type=online)
[^30]: [火山方舟 Coding Plan 概览](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=coding-plan-personal-plan-overview&type=online)
[^31]: [火山方舟 Coding Plan FAQ](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=coding-plan-personal-faq&type=online)
[^32]: [腾讯云 TokenHub 新人免费体验](https://cloud.tencent.com/document/product/1823/130053)
[^33]: [腾讯云 Token Plan](https://cloud.tencent.com/document/product/1823/130060)
[^34]: [腾讯混元 旧模型下线公告](https://cloud.tencent.com/document/product/1729/131925)
[^35]: [百炼 qwen-flash](https://help.aliyun.com/zh/model-studio/qwen-flash)
[^36]: [百炼 老旧模型下线通知](https://www.aliyun.com/notice/118420)
[^37]: [百炼 Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan)
[^38]: [百炼 Token Plan 个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)
[^39]: [智谱 GLM Coding Plan 概览](https://docs.bigmodel.cn/cn/coding-plan/overview.md)
[^40]: [智谱 Coding Plan 适用工具](https://docs.bigmodel.cn/cn/coding-plan/tool/others.md)
[^41]: [智谱 Coding Plan 价格配置（前端 JS）](https://static.bigmodel.cn/wd-paas-front/js/3323.218d86c4.js)
[^42]: [智谱 订阅协议](https://docs.bigmodel.cn/cn/terms/subscription-agreement.md)
[^43]: [Kimi 会员价格](https://www.kimi.com/help/membership/membership-pricing)
[^44]: [Kimi Code 接入 Hermes](https://www.kimi.com/code/docs/third-party-tools/hermes.html)
[^45]: [Kimi Code 社区倡议](https://www.kimi.com/code/docs/kimi-code/community-guidelines.html)
[^46]: [Kimi 开放平台限速](https://platform.kimi.com/docs/pricing/limits.md)
[^47]: [MiniMax M Plan FAQ](https://platform.minimaxi.com/docs/m-plan/faq.md)
[^48]: [MiniMax M Plan 首月活动](https://platform.minimaxi.com/docs/m-plan/monthly-offer.md)
[^49]: [OpenCode Go](https://opencode.ai/docs/go)
[^50]: [OpenCode Console Billing](https://opencode.ai/v2/docs/console/billing)
[^51]: [OpenCode Console Models](https://opencode.ai/docs/zen)
[^52]: [NVIDIA build llms.txt](https://build.nvidia.com/llms.txt)
[^53]: [NVIDIA NIM rate limits](https://build.nvidia.com/nim/rate-limits)
[^54]: [NVIDIA API Trial ToS](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)
[^55]: [NVIDIA /v1/models（实时）](https://integrate.api.nvidia.com/v1/models)
[^56]: [Kilo Gateway usage & billing](https://kilo.ai/docs/gateway/usage-and-billing)
[^57]: [Kilo /models](https://ai-gateway.kilo.ai/api/v1/models)
[^58]: [Cloudflare Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/index.md)
[^59]: [Cohere rate limits](https://docs.cohere.com/docs/rate-limits.md)
[^60]: [Cohere pricing](https://cohere.com/pricing)
[^61]: [SambaNova rate limits](https://docs.sambanova.ai/docs/en/models/rate-limits.md)
[^62]: [Cerebras rate limits](https://inference-docs.cerebras.ai/support/rate-limits.md)
[^63]: [Cerebras qwen-3.8-27b](https://inference-docs.cerebras.ai/models/qwen-3.8-27b.md)
[^64]: [GitHub Models](https://docs.github.com/api/article/body?pathname=/en/github-models/use-github-models/prototyping-with-ai-models)
[^65]: [HF Inference Providers pricing](https://huggingface.co/docs/inference-providers/pricing.md)
[^66]: [Chutes pricing](https://chutes.ai/pricing)
[^67]: [Chutes llms.txt](https://chutes.ai/llms.txt)
[^68]: [Nous Portal](https://portal.nousresearch.com)
[^69]: [Ollama pricing](https://ollama.com/pricing)
[^70]: [Mistral 数据训练说明](https://help.mistral.ai/en/articles/347617-do-you-use-my-user-data-to-train-your-artificial-intelligence-models)
[^71]: [Mistral rate limits](https://help.mistral.ai/en/articles/698531-why-am-i-hitting-api-rate-limits-and-how-do-i-increase-them)
[^72]: [讯飞星火 HTTP 文档](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html)
[^73]: [LongCat 按量付费](https://longcat.chat/platform/docs/zh/api-pay-as-you-go)
[^74]: [LongCat 控制台文案（前端 JS）](https://s3.meituan.net/static-prod01/com.sankuai.friday.longcat.platform/js/34441.8742e9b5846947edbb0b.js)
[^75]: [Hermes docs (llms-full)](https://hermes-agent.nousresearch.com/docs/llms-full.txt)
[^76]: [Nous Portal Privacy](https://portal.nousresearch.com/privacy)
[^77]: [阶跃 Step Plan 页面通知（前端 JS）](https://platform.stepfun.com/_next/static/chunks/55412-ba99317b8b8b5cc4.js)
[^78]: [月之暗面 Kimi 开放平台｜新用户 15 元代金券、模型能力与接入地址](https://platform.kimi.com/docs/llms-full.txt)
[^80]: [NVIDIA build: DeepSeek-V4.1-Flash 模型页](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash)
[^82]: [火山方舟（豆包）｜OpenAI 兼容接入](https://www.volcengine.com/docs/82379/1330626)
[^83]: [百度千帆（文心 ERNIE）｜“新用户免费额度”页面内容](https://cloud.baidu.com/doc/qianfan/s/Imi2rpirg)
[^84]: [百度千帆（文心 ERNIE）｜最便宜可用模型价格（模型服务计费）](https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya)
[^85]: [腾讯云 TokenHub｜实名要求与 OpenAI 兼容 base_url](https://cloud.tencent.com/document/product/1823/130058)
[^86]: [腾讯云 TokenHub｜最便宜的 agent 可用模型价格](https://cloud.tencent.com/document/product/1823/130055)
[^87]: [腾讯云 TokenHub｜上下文与 Function Calling（模型列表）](https://cloud.tencent.com/document/product/1823/130051)
[^88]: [阿里云百炼（通义千问）｜qwen3.7-flash 价格、上下文、工具调用、限流](https://help.aliyun.com/zh/model-studio/qwen3-7-flash)
[^90]: [讯飞星火（讯飞开放平台）｜Spark Lite 免费条件（控制台文案）](https://console.xfyun.cn/2.b633f2bbfd0933b44d9d.bundle.js)
[^91]: [讯飞星火（讯飞开放平台）｜Spark X2.5 系列免费小模型与旗舰价格（星火API产品页）](https://xhspdup.xfyun.cn/static/js/2737.d6f2bd9e.chunk.js)
[^92]: [讯飞星火（讯飞开放平台）｜Spark X2.5 系列模型能力（星辰 MaaS）](https://www.xfyun.cn/doc/spark/Spark-X2.5%E6%A8%A1%E5%9E%8B%E4%BB%8B%E7%BB%8D.html)
[^93]: [讯飞星火（讯飞开放平台）｜星辰 MaaS 接入地址与默认限速](https://www.xfyun.cn/doc/spark/%E4%BA%A7%E5%93%81%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.html)
[^94]: [美团 LongCat API 开放平台｜接入地址、上下文与限流说明](https://longcat.chat/platform/docs/zh)
[^96]: [月之暗面 Kimi 开放平台｜模型价格（最便宜 kimi-k2.6）](https://platform.kimi.com/docs/pricing/chat.md)
[^97]: [MiniMax 开放平台｜语言模型价格（最便宜 M3.1-Flash）](https://platform.minimax.cn/docs/pricing/overview.md)
[^98]: [MiniMax 开放平台｜免费用户限速、接入地址、模型能力与 M Plan](https://platform.minimax.cn/docs/llms-full.txt)
[^100]: [MiniMax（M Plan，原 Coding Plan / Token Plan）｜通用接入参数（Base URL）](https://platform.minimaxi.com/docs/m-plan/other-tools.md)
[^101]: [百度千帆 Token Plan 个人版｜产品页首购五折 / 续费 6 折](https://cloud.baidu.com/product/codingplan.html)
[^102]: [Mistral（Mistral AI Studio，原 La Plateforme）｜Free mode（现行文档里的免费档，对应原 Experiment 档）](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key.md)
[^104]: [Mistral（Mistral AI Studio，原 La Plateforme）｜模型上下文与 function calling](https://docs.mistral.ai/resources/known-limitations.md)
[^106]: [Cerebras Inference｜数据与隐私](https://www.cerebras.ai/policies)
[^107]: [Cerebras Inference｜使用条款：训练与出口管制](https://cdn.sanity.io/files/e4qjo92p/production/b749958186be1ea10320eef749d9c49e2459293c.pdf)
[^108]: [NVIDIA NIM / build.nvidia.com｜免费模型（Free Endpoint）](https://build.nvidia.com/models)
[^109]: [SambaNova Cloud (SambaCloud)｜是否需要绑卡（官方页面说法矛盾）](https://cloud.sambanova.ai/plans)
[^113]: [Hugging Face Inference Providers｜PRO 订阅价格](https://huggingface.co/subscribe/pro)
[^115]: [Cloudflare Workers AI｜GLM-4.7-Flash（免费额度可用、支持工具调用）](https://developers.cloudflare.com/workers-ai/models/glm-4.7-flash/index.md)
[^116]: [Cloudflare Workers AI｜数据政策](https://developers.cloudflare.com/workers-ai/platform/data-usage/index.md)
[^117]: [Cohere｜数据政策（trial 用户不在企业承诺范围内）](https://cohere.com/enterprise-data-commitments)
[^118]: [Chutes｜数据政策](https://chutes.ai/privacy)
[^119]: [智谱 API Key 管理说明](https://docs.bigmodel.cn/cn/coding-plan/notice/api-key-management.md)
[^120]: [阶跃 快速开始](https://platform.stepfun.com/docs/zh/quickstart/overview.md)
[^121]: [百炼 Base URL 与 API Key](https://docs.bailian.console.aliyun.com/zh/model-studio/base-url.md)
[^122]: [百炼 Base URL](https://help.aliyun.com/zh/model-studio/base-url)
[^123]: [火山方舟 低优（Flex）](https://www.volcengine.com/docs/82379/2665244)
[^124]: [火山方舟 Agent Plan 接入 Hermes](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=agent-plan-personal-hermes-agent&type=online)
[^125]: [魔搭 API-Inference 介绍](https://resouces.modelscope.cn/document/docdata/2026-10-9_16-57-CN/dist/model-service/API-Inference/intro/intro_CN.md)
[^126]: [硅基流动 快速上手](https://docs.siliconflow.cn/cn/userguide/quickstart)
[^127]: [OpenRouter Quickstart](https://openrouter.ai/docs/quickstart.md)
[^128]: [Kilo Gateway 认证](https://kilo.ai/docs/gateway/authentication)
[^129]: [Cloudflare Workers AI OpenAI 兼容](https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/index.md)
[^130]: [Cohere Compatibility API](https://docs.cohere.com/docs/compatibility-api.md)
[^131]: [Mistral 第一个 API 请求](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request.md)
[^133]: [火山方舟 Agent Plan 个人版](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=agent-plan-personal-plan-overview&type=online)
[^137]: [千帆 OpenAI 兼容接口说明](https://cloud.baidu.com/doc/qianfan/s/Hmh4suq26)
[^138]: [OpenRouter API Authentication](https://openrouter.ai/docs/api/reference/authentication.md)
[^139]: [智谱 Coding Plan 切换最新模型](https://docs.bigmodel.cn/cn/coding-plan/latest-model.md)
[^140]: [OpenCode Go /models（实时）](https://opencode.ai/zen/go/v1/models)
[^141]: [LongCat OpenAI Chat Completion API](https://longcat.chat/platform/docs/zh/api/chat)
[^142]: [Ollama API authentication](https://docs.ollama.com/api/authentication.md)
[^143]: [Ollama Cloud](https://docs.ollama.com/cloud.md)
[^144]: [OpenCode Providers](https://opencode.ai/docs/providers)
[^146]: [DeepSeek API 文档：首次调用](https://api-docs.deepseek.com/zh-cn)
