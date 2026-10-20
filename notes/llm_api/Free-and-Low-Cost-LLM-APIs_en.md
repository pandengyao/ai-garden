# Free and Low-Cost LLM APIs: Quotas, Prices, Plans and Access

[中文](./Free-and-Low-Cost-LLM-APIs.md) | English

- **Research date**: 2026-10-20 (prices and quotas captured 2026-10-19 to 10-20)
- **Scope**: LLM APIs, in China and abroad, that have a free quota or a low price. Covers free tiers, new-user credits, low-priced pay-as-you-go models, monthly plans, data policies, and each platform's website, API key page, endpoint and how to call it.
- **Basis**: data comes from official pages: docs, pricing pages, terms, announcements and official APIs. Superscript numbers at the end of a sentence are citations, matching the sources at the end. Content marked "(inferred)" or "(converted)" is inferred or converted from official data; content marked "(tested)" is the result of actual calls or connectivity tests on 2026-10-20.
- **Units**: RMB prices are in "yuan / million tokens", and the three numbers are, in order, "input (cache miss) / cache hit / output". USD prices use the same order.
- **Freshness**: prices, promotions and free-model lists change quickly; check the official site before paying.

## 1. Key Points

1. **Long-term free and usable right away**:
   - NVIDIA build: no card needed[^52], up to 40 requests per minute and 10,000 per day[^53], but for testing and evaluation only[^54].
   - Zhipu `glm-4.7-flash`: free input and output, 200K context[^1], supports tool calling[^14].
   - Kilo Gateway's `:free` models: 200 requests per hour per IP, callable without logging in[^56].
   - OpenRouter's `:free` models: 20 requests per minute; 50 per day while lifetime purchases are under 10 credits, 1,000 per day after that[^6].
2. **New-user credits mostly come as tokens**: Bailian gives about 1 million tokens per model, valid for 90 days[^8]; Tencent TokenHub 1 million tokens per language model, valid for 1 year[^32]; Volcano 500,000 tokens[^24]. Xiaomi gives ¥5[^17], Kimi a ¥15 voucher[^78].
3. **Cheapest pay-as-you-go**:
   - Bailian `qwen-flash` input starts at 0.15 yuan[^35]; `qwen3.7-flash` and Volcano `doubao-seed-2.0-mini` start at 0.2 yuan[^88][^26]. All three are tiered by the input length of a single request, and the longer the input, the higher the unit price.
   - Among models without tiers, StepFun `step-3.5-flash` (0.7 / 0.14 / 2.1)[^18], Zhipu `glm-5.3-flash` (0.8 / 0.23 / 2.8)[^1] and Xiaomi `mimo-v2.6-flash` (1 / 0.02 / 2)[^15] are among the cheapest.
4. **Cheapest monthly plans**: Chutes Base $3/month with 300 requests a day[^67]; OpenCode Go $10/month[^49]; Qianfan Token Plan Mini ¥9.9/month[^23]; Volcano Coding Plan Lite ¥9.9/month for the first two months[^29].
5. **Coding plans usually restrict how they're used**:
   - Bailian, Qianfan and Tencent's personal plans may only be used interactively inside tools, not for automation scripts or app backends[^37][^23][^33].
   - Volcano also explicitly bans scheduled tasks, and the personal edition licenses inputs and outputs to Volcano[^28].
   - Zhipu does not allow the plan to be used in self-built apps, bots and similar scenarios[^42].
6. **Data policies**: inputs to the NVIDIA trial[^54], Kilo's free models[^57] and Mistral's free tier[^70] may be used for training. Cloudflare[^116], Chutes[^118] and Ollama[^69] state that they don't train on or log your data.
7. **Retired or practically unusable**: GitHub Models[^64] and Baidu ERNIE Speed/Lite/Tiny[^21] have been shut down; Tencent hunyuan-lite[^34] and Bailian qwen-turbo[^36] have also been retired. The Gemini API's supported regions don't include mainland China or Hong Kong[^5].

## 2. Free Quotas

### 2.1 Long-term free

| Platform | What's free | Limits and conditions | Data |
| --- | --- | --- | --- |
| NVIDIA build | Free trial on all models, no card needed[^52]; 39 models on the free endpoints[^108], including DeepSeek V4.1 Flash, Kimi K2.6 and GLM-5.3[^55] | Up to 40 requests per minute and 10,000 per day[^53]; internal testing and evaluation only, not production[^54] | May be used to improve models[^54] |
| Zhipu | `glm-4.7-flash` free input and output, 200K context[^1] | No rate limit published | — |
| Kilo Gateway | `:free` models at zero cost, callable anonymously[^56]; 17 free models on 10-19 (counted from the API response)[^57] | 200 requests per hour per IP, 429 beyond that[^56] | All free models flagged as possibly used for training[^57] |
| OpenRouter | 16 `:free` models on 10-19 (counted from the API response), including Nemotron 3 Ultra with 1M context[^11] | 20 requests per minute; 50 per day while lifetime purchases are under 10 credits, 1,000 per day after that[^6] | Varies by model |
| OpenCode Zen | DeepSeek V4.1 Flash Free, GLM-5.3-Flash Free and others free for a limited time[^51] | Billing details and a top-up are required before you get an API key[^51]; free limits not published | Varies by model, see Section 6 |
| Nous Portal | Free tier can use the free models[^68] | When rate-limited, the whole service pauses[^75] | May be used for training unless Privacy Mode is on[^76] |
| ModelScope | API-Inference free for developers to try[^10] | Requires a linked, real-name-verified Alibaba Cloud account; in principle only a single concurrent request is guaranteed[^10] | — |
| iFlytek Spark | Spark Lite free with no usage cap[^90]; `spark-x2.5-4b` free for a limited time and `spark-x2.5-1.7b` free, both with 1M context[^91] | Spark Lite requires real-name verification and can be bound to only one app[^90]; input up to 8K[^72] | — |
| SiliconFlow | `XingChenAGI/Xing4.0-29B`, `tencent/Hunyuan-MT-7B` and other models free[^9] | Rate limits not verified | — |
| Mistral | Free mode, no card needed[^102] | Limits not public; check the dashboard after logging in[^71] | May be used for training by default; can be turned off[^70] |
| Cohere | Trial key free[^59] | 1,000 requests per month, 20 per minute[^59]; not for production or commercial use[^60] | Enterprise data commitments don't apply[^117] |
| Volcano Collaboration Rewards Program | After you authorize use of your inference data, an equal free resource pack is returned the next day, up to 5 million tokens per model per day[^27] | Only for models still in the program; the entry currently supports only Doubao-Seed-Evolving[^27] | Volcano may use the authorized data permanently[^27] |

### 2.2 New-user credits

| Platform | Credit | Conditions |
| --- | --- | --- |
| Alibaba Bailian | About 1 million tokens per model, valid for 90 days[^8] | Beijing region only; once used up, verified users switch to pay-as-you-go automatically[^8] |
| Tencent TokenHub | 1 million tokens per language model, valid for 1 year[^32] | Promotion runs to 2026-12-31; elsewhere the docs say "all models under one account share the quota", so the two statements conflict[^32] |
| Volcano Ark | 500,000 tokens in Safe Trial mode; the service pauses automatically when the quota is nearly used up[^24] | Only accounts that have never enabled a model service can turn it on, and once off it can't be turned back on[^24] |
| Baidu Qianfan | 1 million tokens per model for new users, valid for 3 months[^83] | Most models on the list have been retired[^21] |
| Xiaomi MiMo | ¥5 on first real-name verification, valid for 40 days[^17] | Mainland China users only[^17] |
| Kimi | ¥15 voucher after verification[^78] | Can't be used for Kimi K3[^78]; vouchers don't count toward the cumulative top-up that sets your rate-limit tier[^46] |
| Meituan LongCat | Console copy says 10 million tokens after real-name verification, plus a daily free quota[^74] | Not in the official docs |
| StepFun | Docs mention a "free plan"; real-name verification required before use[^19] | Amount not stated; an official notice says new claims of the Step Plan free trial will close[^77] |

## 3. Pay-As-You-Go: Low-Cost Models

### 3.1 RMB prices (yuan / million tokens)

| Model | Platform | Input / cache hit / output | Context | Tool calling |
| --- | --- | --- | --- | --- |
| `qwen-flash` | Alibaba Bailian | ≤128K: 0.15 / 0.03 / 1.5; 128K–256K: 0.6 / 0.12 / 6; 256K–1M: 1.2 / 0.24 / 12[^35] | 1M[^35] | Supported in the Beijing region[^35] |
| `qwen3.7-flash` | Alibaba Bailian | ≤32K: 0.2 / 0.04 / 0.8; 32K–256K: 0.6 / 0.12 / 2.4[^88] | 1M[^88] | Supported[^88] |
| `doubao-seed-2-0-mini-260428` | Volcano Ark | ≤32K: 0.2 / 0.04 / 2; 32K–128K: 0.4 / 0.08 / 4; 128K–256K: 0.8 / 0.16 / 8[^26] | 256K[^25] | Supported[^25] |
| `step-3.5-flash` | StepFun | 0.7 / 0.14 / 2.1[^18] | 256K[^18] | Supported[^18] |
| `doubao-seed-2-1-lite-260915` | Volcano Ark | 0.8 / 0.16 / 2.7[^26] | 1M[^25] | Supported[^25] |
| `glm-5.3-flash` | Zhipu; same price on Volcano[^26], Tencent[^86] and Qianfan[^84] | 0.8 / 0.23 / 2.8[^1] | 1M[^1] | Supported[^87] |
| `mimo-v2.6-flash` | Xiaomi; same price on Tencent[^86] | 1 / 0.02 / 2[^15] | 1M[^16] | Supported[^16] |
| `deepseek-flash` (V4.1 Flash) | DeepSeek; same price on Volcano[^26] and Tencent[^86] | Off-peak 1 / 0.02 / 4; peak 2 / 0.04 / 8[^3] | 1M[^3] | Supported[^3] |
| `deepseek-v4-flash` | Tencent TokenHub | 1 / 0.2 / 2[^86] | 1M[^87] | Supported[^87] |
| `MiniMax-M3.1-Flash` | MiniMax | 1 / 0.1 / 4[^97] | 1M[^98] | Supported[^98] |
| `hy3` | Tencent TokenHub | 1 / 0.25 / 4[^86] | 256K[^87] | Supported[^87] |
| `LongCat-2.5-Preview` | Meituan | 2 / 0.04 / 8, limited-time price[^73] | 1M[^94] | Agentic model[^94] |
| `kimi-k2.6` | Kimi | 6.5 / 1.1 / 27[^96] | 256K[^96] | Supports multi-step tool calling[^78] |

- Tiered models are priced by the input length of a single request: the longer the input, the higher the unit price for the whole request[^35][^26].
- DeepSeek's peak hours are 9:00–12:00 and 14:00–18:00 on weekdays, excluding public holidays[^3]. DeepSeek on Volcano and Tencent also has peak and off-peak prices[^26][^86]. Qianfan's peak hours are 8:00–22:00 every day[^84].
- Volcano's low-priority (Flex) mode charges about half price for input and output[^26], but requests may queue for up to 20 minutes[^123]. Volcano also charges 0.017 yuan per million tokens per hour for cache storage[^26].
- LongCat's current price is 40% of the list price (60% off); the list price is 5 / 0.1 / 20[^74].

### 3.2 USD prices (USD / million tokens)

| Model | Platform | Input / cache hit / output |
| --- | --- | --- |
| `deepseek-v4.1-flash` | Ollama Cloud | 0.30 / 0.006 / 1.20, half price off-peak[^69] |
| DeepSeek V4.1 Flash | OpenCode Go (deducted from the plan quota) | Peak 0.30 / 0.006 / 1.20, off-peak 0.15 / 0.003 / 0.60[^49] |
| `LongCat-2.5-Preview` | Meituan (international) | 0.30 / 0.006 / 1.20[^73] |
| `glm-5.3-flash` | Ollama Cloud | 0.15 / 0.03 / 0.50[^69] |
| `deepseek-ai/DeepSeek-V4-Flash-0731-TEE` | Chutes | 0.44 / — / 1.32[^67] |
| `@cf/zai-org/glm-4.7-flash` | Cloudflare | 0.0605 / — / 0.40[^115] |

## 4. Monthly and Subscription Plans

| Plan | Price | Quota | Main restrictions |
| --- | --- | --- | --- |
| Chutes | Base $3, Plus $10, Pro $20, all monthly[^67] | 300 / 2,000 / 5,000 requests per day[^67]; counted per request, not per token[^66] | No free tier; paid through Stripe, accepting crypto, cards and bank transfer[^66] |
| OpenCode Go | Go $10, Go Plus $40, both monthly[^49] | A separate monthly USD allowance per model, e.g. on Go, $80 for DeepSeek V4.1 Flash and $60 for GLM-5.3-Flash; at most 20% within 5 hours and 50% per week[^49] | Aimed at coding agents like OpenCode, with abusive traffic monitored; mainly for international users[^49] |
| Ollama Cloud | Pro $20, Max $100, both monthly[^69] | Include $60 and $300 of usage per month respectively[^69] | The Free tier allows only 1 concurrent request[^69] |
| StepFun Step Plan | Mini ¥49, Plus ¥99, Pro ¥199, Max ¥699, all monthly[^19] | 400M / 1,600M / 8,000M / 40,000M Credit per month, at 1 yuan = 1 million Credit; usage costs double during peak hours[^19] | Daily purchase slots are limited[^77] |
| Zhipu GLM Coding Plan | Lite ¥118, Pro ¥538, Max ¥1,078, all monthly[^41] | Points per 5 hours / per week: Lite 2,000 / 10,000, Pro 12,000 / 60,000, Max 28,000 / 140,000; off-peak usage costs only half[^39] | Only in officially listed tools[^42]; general agent tools rank below coding tools and may queue under heavy load[^40] |
| Bailian Coding Plan | Pro ¥39.9 for the first month, then ¥200 a month; Lite is discontinued[^37] | 6,000 model calls per 5 hours, 45,000 per week, 90,000 per month[^37] | Only inside coding tools; first-month discount slots refill daily at 9:30[^37] |
| Bailian Token Plan (personal) | From Lite at a limited-time ¥39/month (list price ¥60)[^38] | From 11,500 Credits per month[^38] | One per verified identity[^38] |
| Volcano Coding Plan | Lite ¥40/month, Pro ¥200/month; bought before 11-08, the first two months are 75% off, i.e. ¥9.9 and ¥49.9[^29] | Officially estimated with Doubao Seed 2.0 Lite: Lite about 18,000 requests per month, Pro 5x Lite[^31] | Can't be used for API calls[^30]; the personal edition licenses inputs and outputs to Volcano[^28] |
| Volcano Agent Plan | Small ¥40, Medium ¥200, Large ¥500, Max ¥1,000, all monthly[^133] | 20,000 / 100,000 / 250,000 / 500,000 AFP per month[^133] | Governed by the same terms as the Coding Plan[^28] |
| Qianfan Token Plan (personal) | Mini ¥9.9, Lite ¥40, Pro ¥200, Max ¥600, all monthly[^23]; new users get 50% off the first purchase[^101] | Token-based: 10 million / 42 million / 230 million / 700 million tokens per month, with input, output and cache all deducted at actual usage[^23] | No refunds or downgrades after purchase[^23] |
| Tencent Token Plan | General edition from Lite ¥39/month, Hunyuan edition from Lite ¥28/month[^33] | Lite 780 points per month, Hunyuan edition 560[^33] | No refunds[^33] |
| Kimi membership | Plus ¥99/month, Pro from ¥199/month; Go ¥49/month doesn't include Kimi Code[^43] | Kimi Code has a rolling 5-hour limit and a shared monthly quota pool, with no specific numbers published[^43] | Reselling accounts or API access for commercial purposes is prohibited[^45] |
| MiniMax M Plan | Go ¥49, Explore ¥119, Build ¥469, all monthly[^48] | Only relative multiples published (1x / 3x / 12x), with 5-hour and weekly windows[^47] | For production, MiniMax recommends pay-as-you-go[^47] |

Usage scope:

- **Interactive use inside tools only**: the Bailian[^37], Qianfan[^23] and Tencent[^33] plans all state this, and forbid use in automation scripts or app backends. Kimi Code is also limited to personal interactive use; batch calls from scripts go beyond normal use[^45].
- **Volcano**: the terms also explicitly ban programmatic calls such as scheduled tasks[^28].
- **Zhipu**: not allowed in self-built apps, bots, websites and similar scenarios[^42].
- **StepFun**: its official guide to connecting agent tools says you can have the agent run automated work such as scheduled tasks[^19].

## 5. Not Recommended or Retired

| Platform | Reason |
| --- | --- |
| GitHub Models | Fully shut down on 2026-07-30[^64] |
| Groq free tier | Taking gpt-oss-120b as an example: 30 requests per minute, 1,000 per day, 8K tokens per minute[^7]; long-context requests hit the limit easily (inferred) |
| Cerebras | No long-term free tier; a one-time $5 only after adding a card, expiring after 30 days[^62]; the free tier's context is only 64K[^63] |
| SambaNova | Free tier allows 20 requests and 200,000 tokens per model per day[^61]; official pages disagree on whether a card is required[^109] |
| Cloudflare Workers AI | 10,000 neurons per day; stronger models such as Kimi K2.6, GLM-5.3 and DeepSeek V4 require payment[^58]. At 5,500 neurons per million input tokens for glm-4.7-flash, 10,000 neurons is about 1.8 million input tokens (converted) |
| Google Gemini | Supported regions don't include mainland China or Hong Kong[^5]; free-tier data is used to improve products[^4] |
| Hugging Face | Free users no longer get credits[^65]; PRO at $9/month includes only $2 of credit[^113] |
| iFlytek Spark Lite | Input up to 8K and output up to 4K tokens; the docs list Function Call support only for 4.0Ultra and Max[^72] |
| Baidu ERNIE Speed / Lite / Tiny | Retired in 2026-06[^21] |
| Tencent hunyuan-lite | Retired on 2026-06-22[^34] |
| Bailian qwen-turbo | Retired on 2026-10-10[^36] |
| MiniMax M2.5 / M2.7 | Closed to new users from 10-19, retired on 11-18[^98] |

## 6. Data Policies

| Platform / tier | Is your data used for training? |
| --- | --- |
| NVIDIA trial | One clause says nothing is stored or used after the session ends; another says content is collected to improve models, so treat it as "may be"[^54] |
| Kilo free models | All flagged as possibly used for training[^57] |
| Mistral Free mode | May be, opted in by default; can be turned off[^70] |
| Gemini free tier | Used to improve products[^4] |
| Nous Portal | May be, unless Privacy Mode is on[^76] |
| Volcano Coding / Agent Plan (personal) | Inputs and outputs are licensed to Volcano for storage and use[^28] |
| Cohere trial | Enterprise data commitments don't apply; prompts and generations are kept for 30 days, and training use can be turned off in the dashboard[^117] |
| OpenCode Zen free models | Varies by model: the providers behind GLM-5.3-Flash Free and DeepSeek V4.1 Flash Free keep zero retention and don't train; Big Pickle may be used to improve the model during its free period[^51] |
| OpenCode Go | The zero-retention agreement with DeepSeek renews monthly and currently runs to 2026-10-31[^49] |
| Cloudflare Workers AI | Not used for training[^116] |
| Chutes | Requests and responses are not logged or stored[^118] |
| Ollama Cloud | No logging, no training[^69] |
| Cerebras | Inputs and outputs are not stored or used[^106]; the terms grant no right to train on them[^107] |

## 7. How to Use

### 7.1 General steps

1. Sign up. Most Chinese platforms require real-name verification, for example Tencent TokenHub[^85] and ModelScope[^10]. LongCat[^73] and StepFun[^19] also require it before you top up or pay.
2. Create an API key in the console; the key pages are listed in 7.2. Some platforms show the key only once, at creation, for example LongCat[^94].
3. Most of these platforms offer an OpenAI-compatible API, with endpoints listed in 7.2. Switching platforms usually means changing just three things, base_url, api_key and model, which is exactly what Volcano Ark's docs say[^82].

curl example (using NVIDIA):

```bash
export NVIDIA_API_KEY="nvapi-..."   # replace with your own key

curl https://integrate.api.nvidia.com/v1/chat/completions \
  -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-ai/deepseek-v4.1-flash", "messages": [{"role": "user", "content": "Hello"}]}'
```

Python example (run `pip install openai` first):

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",  # change this when switching platforms
    api_key=os.environ["NVIDIA_API_KEY"],            # and this
)
resp = client.chat.completions.create(
    model="deepseek-ai/deepseek-v4.1-flash",         # and the model ID
    messages=[{"role": "user", "content": "Hello"}],
)
print(resp.choices[0].message.content)
```

An example that needs no key: Kilo's free models returned normally in a 10-20 test (tested). Note that inputs to free models may be used for training[^57].

```bash
curl https://ai-gateway.kilo.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "nvidia/nemotron-3-ultra-550b-a55b:free", "messages": [{"role": "user", "content": "Reply with exactly: OK"}]}'
```

### 7.2 Endpoint quick reference

Platforms in China:

| Platform | Website | API key page | base_url (OpenAI-compatible) | Example model IDs |
| --- | --- | --- | --- | --- |
| Zhipu | <https://bigmodel.cn> | <https://bigmodel.cn/usercenter/proj-mgmt/apikeys>[^119] | `https://open.bigmodel.cn/api/paas/v4`[^119]; Coding Plan uses `https://open.bigmodel.cn/api/coding/paas/v4`[^40] | `glm-4.7-flash`[^14], `glm-5.3-flash`[^139] |
| DeepSeek | <https://platform.deepseek.com> | <https://platform.deepseek.com/api_keys>[^146] | `https://api.deepseek.com`[^3] | `deepseek-flash`, `deepseek-v4-pro`[^3] |
| Xiaomi MiMo | <https://platform.xiaomimimo.com> | <https://platform.xiaomimimo.com/#/console/api-keys>[^16] | `https://api.xiaomimimo.com/v1`[^16] | `mimo-v2.6-flash`[^15] |
| StepFun | <https://platform.stepfun.com> | <https://platform.stepfun.com/interface-key>[^120] | Pay-as-you-go: `https://api.stepfun.com/v1`[^18]; Step Plan: `https://api.stepfun.com/step_plan/v1`[^19] | `step-3.5-flash`[^18] |
| Alibaba Bailian | <https://bailian.console.aliyun.com> | <https://bailian.console.aliyun.com/cn-beijing/settings/api-key>[^121] | `https://dashscope.aliyuncs.com/compatible-mode/v1`[^122]; Coding Plan uses `https://coding.dashscope.aliyuncs.com/v1`[^37] | `qwen-flash`[^35], `qwen3.7-flash`[^88] |
| Volcano Ark | <https://www.volcengine.com/product/ark> | <https://ark.volcengine.com/region:cn-beijing/apiKey>[^123] | `https://ark.cn-beijing.volces.com/api/v3`[^82]; Coding Plan uses `…/api/coding/v3`[^30]; Agent Plan uses `…/api/plan/v3`[^124] | `doubao-seed-2-1-lite-260915`, `deepseek-v4-1-flash-261017`[^25] |
| Tencent TokenHub | <https://cloud.tencent.com/product/tokenhub> | The "API Key Management" page in the TokenHub console[^85] | `https://tokenhub.tencentmaas.com/v1`[^85]; Token Plan uses `https://api.lkeap.cloud.tencent.com/plan/v3`[^33] | `hy3`, `deepseek-v4.1-flash`[^87] |
| Baidu Qianfan | <https://cloud.baidu.com/product/qianfan.html> | Qianfan console: System Management → Create API Key[^137] | `https://qianfan.baidubce.com/v2`[^137]; Token Plan uses `https://qianfan.baidubce.com/v2/tokenplan/personal`[^23] | `deepseek-v4.1-flash`[^20] |
| Kimi | <https://platform.kimi.com> | <https://platform.kimi.com/console/api-keys>[^78] | `https://api.moonshot.cn/v1`[^78]; Kimi Code membership uses `https://api.kimi.com/coding/v1`[^44] | `kimi-k2.6`[^96] |
| MiniMax | <https://platform.minimaxi.com> | <https://platform.minimax.cn/user-center/basic-information/interface-key>[^98] | `https://api.minimax.cn/v1`[^98] | `MiniMax-M3.1-Flash`[^97]; M Plan uses `MiniMax-M3.1-Flash-Preview`[^100] |
| Meituan LongCat | <https://longcat.chat/platform> | Create one on the API Keys page after logging in[^94] | `https://api.longcat.chat/openai`[^94] | `LongCat-2.5-Preview`[^94] |
| iFlytek Spark | <https://xinghuo.xfyun.cn> | Console <https://console.xfyun.cn> | Spark Lite: `https://spark-api-open.xf-yun.com/v1/`[^72]; Xingchen MaaS: `https://maas-api.cn-huabei-1.xf-yun.com/v2`[^93] | `spark-x2.5-4b`[^92] |
| ModelScope | <https://modelscope.cn> | <https://modelscope.cn/my/myaccesstoken>[^125] | `https://api-inference.modelscope.cn/v1/`[^125] | `Qwen/Qwen3.5-35B-A3B`[^125] |
| SiliconFlow | <https://siliconflow.cn> | The "API Keys" page in the console[^126] | `https://api.siliconflow.cn/v1`[^126] | `XingChenAGI/Xing4.0-29B`[^9] |

Platforms outside China:

| Platform | Website | API key page | base_url (OpenAI-compatible) | Example model IDs |
| --- | --- | --- | --- | --- |
| NVIDIA build | <https://build.nvidia.com> | <https://build.nvidia.com/settings/api-keys>; keys start with `nvapi-`[^52][^12] | `https://integrate.api.nvidia.com/v1`[^52] | `deepseek-ai/deepseek-v4.1-flash`, `moonshotai/kimi-k2.6`[^55] |
| OpenRouter | <https://openrouter.ai> | <https://openrouter.ai/keys>[^138] | `https://openrouter.ai/api/v1`[^127] | `nvidia/nemotron-3-ultra-550b-a55b:free`[^11] |
| Kilo Gateway | <https://kilo.ai> | Generated with a Kilo account[^128]; exact page not verified | `https://ai-gateway.kilo.ai/api/v1`[^128] | `nvidia/nemotron-3-ultra-550b-a55b:free`[^57] |
| OpenCode | <https://opencode.ai> | <https://opencode.ai/auth>; billing details required first[^144] | Go: `https://opencode.ai/zen/go/v1`[^140][^75] | `deepseek-v4.1-flash`, `glm-5.3-flash`[^140] |
| Chutes | <https://chutes.ai> | Keys start with `cpk_`[^67]; page not verified | `https://llm.chutes.ai/v1`[^67] | `deepseek-ai/DeepSeek-V4-Flash-0731-TEE`[^67] |
| Ollama Cloud | <https://ollama.com> | <https://ollama.com/settings/keys>[^143] | `https://ollama.com/v1`[^142] | `deepseek-v4.1-flash`[^69] |
| Mistral | <https://console.mistral.ai> | <https://console.mistral.ai/api-keys>[^131] | `https://api.mistral.ai/v1`[^131] | `mistral-small-latest`[^102] |
| Cohere | <https://dashboard.cohere.com> | <https://dashboard.cohere.com/api-keys>[^59] | `https://api.cohere.ai/compatibility/v1`[^130] | `command-a-plus-05-2026`[^130] |
| Cloudflare | <https://dash.cloudflare.com> | Use an API token, and put your account_id in the URL[^129] | `https://api.cloudflare.com/client/v4/accounts/<account_id>/ai/v1`[^129] | `@cf/zai-org/glm-4.7-flash`[^58] |

### 7.3 Platform notes

#### Platforms in China

- **Zhipu**: a standard API key on `/api/paas/v4` is billed to your account balance and does not use your Coding Plan quota[^119]. To use the plan quota, you must go through `/api/coding/paas/v4`[^40].
- **DeepSeek**:
  - Use the model name `deepseek-flash`. The old name `deepseek-v4-flash` still works, and requests are served by V4.1 Flash[^3].
  - There is also an Anthropic-format endpoint, `https://api.deepseek.com/anthropic`[^3].
  - `deepseek-v4-pro` pricing: off-peak 4.5 / 0.15 / 13.5, peak 9 / 0.3 / 27[^3].
- **Xiaomi MiMo**:
  - China and international accounts use different base URLs, and keys don't carry over between them[^16].
  - Up to 100 requests per minute and 10 million TPM[^16].
  - `mimo-v2.6-pro` is priced at 3 / 0.025 / 6[^15]. The V2.5 series retires on 10-21[^15].
  - In China it accepts WeChat Pay, Alipay and Xiaomi Pay[^16].
  - There is also a Token Plan at `https://token-plan-cn.xiaomimimo.com/v1`[^16]; its price wasn't checked.
- **StepFun**: the pay-as-you-go API is rate-limited by cumulative cash top-up; under ¥100 you get 5 concurrent requests, 100 RPM and 500,000 TPM[^19]. The Step Plan isn't subject to these limits, and calls to the ordinary pay-as-you-go API don't draw on Step Plan quota[^19].
- **Alibaba Bailian**: the endpoint in the table above is for the Beijing region[^122], and the new-user credit is valid only in the Beijing region too[^8]. `qwen-flash` doesn't support Function Calling in the Singapore region[^35].
- **Volcano Ark**: enable the model on the activation management page before calling it[^123]. Model IDs include a version number[^25].
- **Tencent TokenHub**: real-name verification is required, and you must claim the free trial pack before creating an API key[^85].
- **Baidu Qianfan**: DeepSeek-V4.1-Flash is not in the support list of the Function calling docs[^22], so whether it can call tools needs testing.
- **Kimi**:
  - With zero cumulative top-up you get 1 concurrent request, 3 RPM and 1.5 million tokens a day; once cumulative top-ups reach ¥50, RPM rises to 100[^46].
  - Calling K3 requires a top-up of at least 10 yuan first[^78].
- **MiniMax**: use `api.minimax.cn` in China and `api.minimax.io` internationally[^98]. Free users get 20 RPM and 1 million TPM; paying users get 200 RPM[^98].
- **Meituan LongCat**:
  - The full chat endpoint is `https://api.longcat.chat/openai/v1/chat/completions`[^141].
  - Mainland users must complete real-name verification before topping up[^73].
  - In a 10-20 test, the default DNS couldn't resolve `api.longcat.chat`; switching to 223.5.5.5 or 8.8.8.8 resolved it (tested).
- **iFlytek Spark**: the old Spark API and Xingchen MaaS are two separate APIs. On Xingchen MaaS, each key gets 20 concurrent requests and 1 million TPM per model by default[^93].
- **ModelScope**: model IDs are ModelScope's Model-Id[^125]. You can also redeem Moli points for calls, at 0.5–2 points per call[^10].

#### Platforms outside China

- **NVIDIA build**:
  - Registrants must be of legal age where they live[^54]. The word "internal" in the terms restricts the purpose of use; it doesn't mean only NVIDIA employees may use it (inferred).
  - The terms ask you not to submit confidential or sensitive data[^54].
  - The model page states that `deepseek-v4.1-flash` supports up to 1 million tokens of context[^80]. GLM-5.3 was flagged on 10-19 as "deprecated in 9 days"[^108].
- **OpenRouter**: the daily cap on free models depends on your cumulative credit purchases[^6].
- **Kilo Gateway**:
  - Requests without an Authorization header can call free models anonymously; requests carrying an invalid key are rejected (tested).
  - Some free models require that you allow data collection[^56]. Buying credits carries an extra 5% fee[^56].
- **OpenCode**:
  - Paid through Stripe, accepting cards, Alipay and WeChat Pay, with an extra 4.6% + $0.31 fee[^50].
  - Beam Free is not available in mainland China, Hong Kong or Macau[^51].
  - DeepSeek's peak hours are UTC 01:00–04:00 and 06:00–10:00 on weekdays[^49], which is 9:00–12:00 and 14:00–18:00 Beijing time (converted).
  - In the official estimate table, the Go tier allows roughly 173,000 DeepSeek V4.1 Flash requests per month, or 32,000 GLM-5.3-Flash requests[^49]. The DeepSeek column assumes 410 input, 71,300 cached and 310 output tokens per request[^49].
- **Chutes**: no free tier; you must top up first[^66]. The docs don't say whether the daily request quota applies to every model.
- **Ollama Cloud**:
  - Off-peak means outside UTC 12:00–18:00 on weekdays, plus all day on weekends[^69]. In Beijing time, peak is 20:00 to 2:00 the next day on weekdays (converted).
  - The service is hosted mainly in the US[^69].
- **Mistral**: the API is served from EU data centers by default[^104].
- **Cohere**: production keys are requested through the Go to Production flow in the dashboard[^60].

## 8. Network Connectivity from China (2026-10-20)

- Method: from a network in China, curl each platform's API endpoint directly, with no proxy. The results reflect only this one network at test time.
- Reachable (returned 200, 401, 403, 405 or 429): NVIDIA, Zhipu, DeepSeek, Xiaomi, StepFun, Kimi, MiniMax, Bailian, Volcano, Tencent, Qianfan, SiliconFlow, ModelScope, OpenRouter, Kilo, OpenCode, Chutes, Ollama, Nous, Cohere, Mistral, Cloudflare, Gemini, Groq, Cerebras, SambaNova, Hugging Face.
- Unreachable: `api.longcat.chat`, because the default DNS failed to resolve it; it resolves with a public DNS.
- Reachable doesn't mean a platform permits users in mainland China. For example, Gemini's supported regions don't include mainland China or Hong Kong[^5], and OpenCode Go says it mainly serves international users[^49].

## 9. Still to Confirm

- NVIDIA: whether sign-up requires phone verification and whether +86 numbers pass; the context length each hosted endpoint actually allows.
- Zhipu: rate limits for `glm-4.7-flash`.
- Kilo, Chutes: which page generates the API key. For Chutes, whether the Base $3 tier can be bought on the web, whether the daily quota applies to all models, and whether Alipay is accepted.
- Kimi membership, MiniMax M Plan, the Bailian and Tencent Token Plans, Volcano Agent Plan: how their quotas convert into requests or tokens.
- Qianfan: whether `deepseek-v4.1-flash` supports tool calling.
- Tencent TokenHub: whether the new-user credit is "1 million per model" or "1 million shared across the account".
- LongCat: the current daily free quota; whether the DNS issue with `api.longcat.chat` is widespread.
- Mistral: Free mode's exact limits, and whether sign-up requires phone verification.
- The amount of StepFun's "free plan"; the price of Xiaomi MiMo's Token Plan.

## Appendix: Using These in Hermes Agent

This section covers only general setup, based on the Hermes v0.22.2 docs and testing.

Built-in providers: put the key in `.env`, then set the provider and model[^12]. Each profile has its own `.env`[^75].

```bash
# Add a line NVIDIA_API_KEY=nvapi-… to ~/.hermes/.env, then:
hermes config set model.provider nvidia
hermes config set model.default deepseek-ai/deepseek-v4.1-flash
hermes chat -q "Reply OK" --oneshot
```

| Platform | provider | `.env` variable | Notes |
| --- | --- | --- | --- |
| NVIDIA build | `nvidia` | `NVIDIA_API_KEY` | — |
| Zhipu | `zai` | `GLM_API_KEY` | Detects the China or international endpoint automatically[^12]; if you only use the free model, set `GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4` explicitly (inferred) |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` | — |
| Xiaomi MiMo | `xiaomi` | `XIAOMI_API_KEY` | — |
| StepFun Step Plan | `stepfun` | `STEPFUN_API_KEY` | Defaults to the international site; for a China account set `STEPFUN_BASE_URL=https://api.stepfun.com/step_plan/v1` (tested) |
| Alibaba Bailian | `alibaba-cn` | `DASHSCOPE_API_KEY` | Coding Plan uses `alibaba-coding-plan-cn`, Token Plan uses `alibaba-token-plan-cn`[^12] |
| Tencent TokenHub | `tencent-tokenhub` | `TOKENHUB_API_KEY` | Token Plan uses `tencent-tokenplan`[^12] |
| Kimi | `kimi-coding-cn` | `KIMI_CN_API_KEY` | A Kimi Code membership key uses `kimi-coding` and `KIMI_API_KEY` (tested) |
| MiniMax | `minimax-cn` | `MINIMAX_CN_API_KEY` | — |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | `hermes auth add openrouter` also works[^12] |
| Kilo Gateway | `kilocode` | `KILOCODE_API_KEY` | — |
| OpenCode Go / Zen | `opencode-go` / `opencode-zen` | `OPENCODE_GO_API_KEY` / `OPENCODE_ZEN_API_KEY` | — |
| Ollama Cloud | `ollama-cloud` | `OLLAMA_API_KEY` | — |
| Hugging Face | `huggingface` | `HF_TOKEN` | — |
| Nous Portal | `nous` | No key needed | Log in with OAuth in `hermes model`[^12] |

Provider names and variable names come from Hermes's provider registry; see the official docs[^12].

Platforms without a built-in provider (Volcano, Qianfan, LongCat, iFlytek, ModelScope, SiliconFlow, Chutes, Cohere, Mistral, Cloudflare) can be added as custom providers, with the key named by `key_env`[^12]. Chutes as an example (tested to work):

```bash
# Add a line CHUTES_API_KEY=cpk_… to .env, then:
hermes config set providers.chutes.name Chutes
hermes config set providers.chutes.base_url https://llm.chutes.ai/v1
hermes config set providers.chutes.key_env CHUTES_API_KEY
hermes config set providers.chutes.api_mode chat_completions
hermes config set model.provider chutes
hermes config set model.default deepseek-ai/DeepSeek-V4-Flash-0731-TEE
```

Notes:

- When switching from a custom endpoint to a built-in provider, the old `model.base_url` is not cleared automatically, and requests still go to the old address. Run `hermes config unset model.base_url` in that case (tested).
- Hermes requires a model context of at least 64K[^12], so 8K models such as iFlytek Spark Lite won't work.
- Plans whose official integration lists include Hermes Agent:
  - Zhipu GLM Coding Plan[^40]
  - Bailian Coding Plan[^37]
  - Qianfan Token Plan[^23]
  - Volcano Coding Plan[^30] and Agent Plan[^133]
  - MiniMax M Plan[^47]
  - Kimi Code[^44]
  - StepFun Step Plan[^19]
  - OpenCode Go[^49]

## References

The official pages cited in the text are listed below, captured 2026-10-19 to 10-20.

[^1]: [Zhipu API pricing](https://docs.bigmodel.cn/cn/guide/start/pricing.md)
[^3]: [DeepSeek models & pricing](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)
[^4]: [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
[^5]: [Gemini API available regions](https://ai.google.dev/gemini-api/docs/available-regions)
[^6]: [OpenRouter Limits](https://openrouter.ai/docs/api/reference/limits)
[^7]: [Groq rate limits](https://console.groq.com/docs/rate-limits)
[^8]: [Alibaba Cloud Bailian: new-user free quota](https://help.aliyun.com/zh/model-studio/new-free-quota)
[^9]: [SiliconFlow pricing](https://siliconflow.cn/pricing)
[^10]: [ModelScope API-Inference usage limits](https://resouces.modelscope.cn/document/docdata/2026-10-9_16-57-CN/dist/model-service/API-Inference/limits/limits_CN.md)
[^11]: [OpenRouter models API](https://openrouter.ai/api/v1/models)
[^12]: [Hermes docs: AI Providers](https://hermes-agent.nousresearch.com/docs/integrations/providers)
[^14]: [Zhipu GLM-4.7-Flash](https://docs.bigmodel.cn/cn/guide/models/free/glm-4.7-flash)
[^15]: [Xiaomi MiMo pay-as-you-go pricing](https://mimo.mi.com/docs/zh-CN/price/pay-as-you-go)
[^16]: [Xiaomi MiMo docs (llms-full)](https://mimo.mi.com/llms-full.txt)
[^17]: [Xiaomi MiMo new-user credit](https://mimo.mi.com/docs/zh-CN/quick-start/promotions/new%20user)
[^18]: [StepFun step-3.5-flash](https://platform.stepfun.com/docs/zh/guides/models/step-3.5-flash.md)
[^19]: [StepFun docs (llms-full)](https://platform.stepfun.com/docs/llms-full.txt)
[^20]: [Qianfan model list](https://cloud.baidu.com/doc/qianfan/s/rmh4stp0j)
[^21]: [Qianfan model retirement log](https://cloud.baidu.com/doc/qianfan/s/zmh4stou3)
[^22]: [Qianfan Function calling](https://cloud.baidu.com/doc/qianfan-docs/s/xm95lyys5)
[^23]: [Qianfan Token Plan (personal)](https://cloud.baidu.com/doc/qianfan/s/Dmrabu8b6)
[^24]: [Volcano Ark Safe Trial mode](https://www.volcengine.com/docs/82379/1465347)
[^25]: [Volcano Ark model list](https://www.volcengine.com/docs/82379/1330310)
[^26]: [Volcano Ark model pricing](https://www.volcengine.com/docs/82379/1544106)
[^27]: [Volcano Ark Collaboration Rewards Program](https://www.volcengine.com/docs/82379/1391869)
[^28]: [Volcano Ark terms for subscription plans](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=subscription-package-service-terms-conditions&type=online)
[^29]: [Volcano Ark Coding Plan 75%-off promotion](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=coding-plan-personal-universal-promotion&type=online)
[^30]: [Volcano Ark Coding Plan overview](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=coding-plan-personal-plan-overview&type=online)
[^31]: [Volcano Ark Coding Plan FAQ](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=coding-plan-personal-faq&type=online)
[^32]: [Tencent Cloud TokenHub new-user free trial](https://cloud.tencent.com/document/product/1823/130053)
[^33]: [Tencent Cloud Token Plan](https://cloud.tencent.com/document/product/1823/130060)
[^34]: [Tencent Hunyuan legacy model retirement notice](https://cloud.tencent.com/document/product/1729/131925)
[^35]: [Bailian qwen-flash](https://help.aliyun.com/zh/model-studio/qwen-flash)
[^36]: [Bailian notice on retiring legacy models](https://www.aliyun.com/notice/118420)
[^37]: [Bailian Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan)
[^38]: [Bailian Token Plan (personal)](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview)
[^39]: [Zhipu GLM Coding Plan overview](https://docs.bigmodel.cn/cn/coding-plan/overview.md)
[^40]: [Zhipu Coding Plan supported tools](https://docs.bigmodel.cn/cn/coding-plan/tool/others.md)
[^41]: [Zhipu Coding Plan pricing config (frontend JS)](https://static.bigmodel.cn/wd-paas-front/js/3323.218d86c4.js)
[^42]: [Zhipu subscription agreement](https://docs.bigmodel.cn/cn/terms/subscription-agreement.md)
[^43]: [Kimi membership pricing](https://www.kimi.com/help/membership/membership-pricing)
[^44]: [Kimi Code with Hermes](https://www.kimi.com/code/docs/third-party-tools/hermes.html)
[^45]: [Kimi Code community guidelines](https://www.kimi.com/code/docs/kimi-code/community-guidelines.html)
[^46]: [Kimi Open Platform rate limits](https://platform.kimi.com/docs/pricing/limits.md)
[^47]: [MiniMax M Plan FAQ](https://platform.minimaxi.com/docs/m-plan/faq.md)
[^48]: [MiniMax M Plan first-month promotion](https://platform.minimaxi.com/docs/m-plan/monthly-offer.md)
[^49]: [OpenCode Go](https://opencode.ai/docs/go)
[^50]: [OpenCode Console Billing](https://opencode.ai/v2/docs/console/billing)
[^51]: [OpenCode Console Models](https://opencode.ai/docs/zen)
[^52]: [NVIDIA build llms.txt](https://build.nvidia.com/llms.txt)
[^53]: [NVIDIA NIM rate limits](https://build.nvidia.com/nim/rate-limits)
[^54]: [NVIDIA API Trial ToS](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)
[^55]: [NVIDIA /v1/models (live)](https://integrate.api.nvidia.com/v1/models)
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
[^70]: [Mistral on training with user data](https://help.mistral.ai/en/articles/347617-do-you-use-my-user-data-to-train-your-artificial-intelligence-models)
[^71]: [Mistral rate limits](https://help.mistral.ai/en/articles/698531-why-am-i-hitting-api-rate-limits-and-how-do-i-increase-them)
[^72]: [iFlytek Spark HTTP docs](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html)
[^73]: [LongCat pay-as-you-go](https://longcat.chat/platform/docs/zh/api-pay-as-you-go)
[^74]: [LongCat console copy (frontend JS)](https://s3.meituan.net/static-prod01/com.sankuai.friday.longcat.platform/js/34441.8742e9b5846947edbb0b.js)
[^75]: [Hermes docs (llms-full)](https://hermes-agent.nousresearch.com/docs/llms-full.txt)
[^76]: [Nous Portal Privacy](https://portal.nousresearch.com/privacy)
[^77]: [StepFun Step Plan page notice (frontend JS)](https://platform.stepfun.com/_next/static/chunks/55412-ba99317b8b8b5cc4.js)
[^78]: [Moonshot AI Kimi Open Platform | ¥15 new-user voucher, model capabilities and endpoints](https://platform.kimi.com/docs/llms-full.txt)
[^80]: [NVIDIA build: DeepSeek-V4.1-Flash model page](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash)
[^82]: [Volcano Ark (Doubao) | OpenAI-compatible access](https://www.volcengine.com/docs/82379/1330626)
[^83]: [Baidu Qianfan (Wenxin ERNIE) | "New-user free quota" page](https://cloud.baidu.com/doc/qianfan/s/Imi2rpirg)
[^84]: [Baidu Qianfan (Wenxin ERNIE) | Prices of the cheapest available models (model service billing)](https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya)
[^85]: [Tencent Cloud TokenHub | Real-name requirement and the OpenAI-compatible base_url](https://cloud.tencent.com/document/product/1823/130058)
[^86]: [Tencent Cloud TokenHub | Prices of the cheapest agent-capable models](https://cloud.tencent.com/document/product/1823/130055)
[^87]: [Tencent Cloud TokenHub | Context and Function Calling (model list)](https://cloud.tencent.com/document/product/1823/130051)
[^88]: [Alibaba Cloud Bailian (Tongyi Qianwen) | qwen3.7-flash pricing, context, tool calling, rate limits](https://help.aliyun.com/zh/model-studio/qwen3-7-flash)
[^90]: [iFlytek Spark (iFlytek Open Platform) | Spark Lite free-use conditions (console copy)](https://console.xfyun.cn/2.b633f2bbfd0933b44d9d.bundle.js)
[^91]: [iFlytek Spark (iFlytek Open Platform) | Spark X2.5 free small models and flagship pricing (Spark API product page)](https://xhspdup.xfyun.cn/static/js/2737.d6f2bd9e.chunk.js)
[^92]: [iFlytek Spark (iFlytek Open Platform) | Spark X2.5 model capabilities (Xingchen MaaS)](https://www.xfyun.cn/doc/spark/Spark-X2.5%E6%A8%A1%E5%9E%8B%E4%BB%8B%E7%BB%8D.html)
[^93]: [iFlytek Spark (iFlytek Open Platform) | Xingchen MaaS endpoints and default rate limits](https://www.xfyun.cn/doc/spark/%E4%BA%A7%E5%93%81%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.html)
[^94]: [Meituan LongCat API platform | Endpoints, context and rate limits](https://longcat.chat/platform/docs/zh)
[^96]: [Moonshot AI Kimi Open Platform | Model pricing (cheapest: kimi-k2.6)](https://platform.kimi.com/docs/pricing/chat.md)
[^97]: [MiniMax Open Platform | Language model pricing (cheapest: M3.1-Flash)](https://platform.minimax.cn/docs/pricing/overview.md)
[^98]: [MiniMax Open Platform | Free-user rate limits, endpoints, model capabilities and M Plan](https://platform.minimax.cn/docs/llms-full.txt)
[^100]: [MiniMax (M Plan, formerly Coding Plan / Token Plan) | General access parameters (Base URL)](https://platform.minimaxi.com/docs/m-plan/other-tools.md)
[^101]: [Baidu Qianfan Token Plan (personal) | Product page: 50% off the first purchase / 40% off renewals](https://cloud.baidu.com/product/codingplan.html)
[^102]: [Mistral (Mistral AI Studio, formerly La Plateforme) | Free mode (the free tier in current docs, formerly the Experiment tier)](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key.md)
[^104]: [Mistral (Mistral AI Studio, formerly La Plateforme) | Model context and function calling](https://docs.mistral.ai/resources/known-limitations.md)
[^106]: [Cerebras Inference | Data and privacy](https://www.cerebras.ai/policies)
[^107]: [Cerebras Inference | Terms of use: training and export controls](https://cdn.sanity.io/files/e4qjo92p/production/b749958186be1ea10320eef749d9c49e2459293c.pdf)
[^108]: [NVIDIA NIM / build.nvidia.com | Free models (Free Endpoint)](https://build.nvidia.com/models)
[^109]: [SambaNova Cloud (SambaCloud) | Whether a card is required (official pages disagree)](https://cloud.sambanova.ai/plans)
[^113]: [Hugging Face Inference Providers | PRO subscription price](https://huggingface.co/subscribe/pro)
[^115]: [Cloudflare Workers AI | GLM-4.7-Flash (usable on the free quota, supports tool calling)](https://developers.cloudflare.com/workers-ai/models/glm-4.7-flash/index.md)
[^116]: [Cloudflare Workers AI | Data policy](https://developers.cloudflare.com/workers-ai/platform/data-usage/index.md)
[^117]: [Cohere | Data policy (trial users are outside the enterprise commitments)](https://cohere.com/enterprise-data-commitments)
[^118]: [Chutes | Data policy](https://chutes.ai/privacy)
[^119]: [Zhipu API key management](https://docs.bigmodel.cn/cn/coding-plan/notice/api-key-management.md)
[^120]: [StepFun quick start](https://platform.stepfun.com/docs/zh/quickstart/overview.md)
[^121]: [Bailian Base URL and API Key](https://docs.bailian.console.aliyun.com/zh/model-studio/base-url.md)
[^122]: [Bailian Base URL](https://help.aliyun.com/zh/model-studio/base-url)
[^123]: [Volcano Ark low-priority (Flex) mode](https://www.volcengine.com/docs/82379/2665244)
[^124]: [Volcano Ark Agent Plan with Hermes](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=agent-plan-personal-hermes-agent&type=online)
[^125]: [ModelScope API-Inference introduction](https://resouces.modelscope.cn/document/docdata/2026-10-9_16-57-CN/dist/model-service/API-Inference/intro/intro_CN.md)
[^126]: [SiliconFlow quick start](https://docs.siliconflow.cn/cn/userguide/quickstart)
[^127]: [OpenRouter Quickstart](https://openrouter.ai/docs/quickstart.md)
[^128]: [Kilo Gateway authentication](https://kilo.ai/docs/gateway/authentication)
[^129]: [Cloudflare Workers AI OpenAI compatibility](https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/index.md)
[^130]: [Cohere Compatibility API](https://docs.cohere.com/docs/compatibility-api.md)
[^131]: [Mistral: your first API request](https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request.md)
[^133]: [Volcano Ark Agent Plan (personal)](https://www.volcengine.com/api/doc/getDocDetail?LibraryCode=ark&DocumentCode=agent-plan-personal-plan-overview&type=online)
[^137]: [Qianfan OpenAI-compatible API](https://cloud.baidu.com/doc/qianfan/s/Hmh4suq26)
[^138]: [OpenRouter API Authentication](https://openrouter.ai/docs/api/reference/authentication.md)
[^139]: [Zhipu Coding Plan: switching to the latest model](https://docs.bigmodel.cn/cn/coding-plan/latest-model.md)
[^140]: [OpenCode Go /models (live)](https://opencode.ai/zen/go/v1/models)
[^141]: [LongCat OpenAI Chat Completion API](https://longcat.chat/platform/docs/zh/api/chat)
[^142]: [Ollama API authentication](https://docs.ollama.com/api/authentication.md)
[^143]: [Ollama Cloud](https://docs.ollama.com/cloud.md)
[^144]: [OpenCode Providers](https://opencode.ai/docs/providers)
[^146]: [DeepSeek API docs: your first call](https://api-docs.deepseek.com/zh-cn)
