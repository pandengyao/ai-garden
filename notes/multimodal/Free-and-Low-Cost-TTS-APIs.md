# 免费与低价语音合成（TTS）API 调研：额度、价格、声音复刻与接入

中文 | [English](./Free-and-Low-Cost-TTS-APIs_en.md)

- **调研日期**: 2026-10-21
- **范围**: 国内外有免费额度或价格较低的语音合成（TTS）API，包括声音复刻和音色设计，另附可以自己部署的开源模型。内容包括免费额度、价格、汉字的计费口径、套餐、限速、中文能力、数据政策，以及各平台的接口地址和接入方法。
- **依据**: 数据来自官方页面，包括文档、价格页、条款、公告、官方价格接口和代码仓库；少数没有官方来源的内容引用了第三方页面，正文已注明。句末的上标数字是引用，对应文末的参考来源。标“（推断）”的是根据所引资料作出的推断，标“（换算）”的是按官方单价或汇率算出来的，标“（实测）”的是 2026-10-21 在中国大陆网络下实际测试的结果。
- **换算方法**:
  - 各家对汉字的计数方法不同（见第二节），所以价格统一折算成“元/万汉字”：按纯中文文本、官方原价第一档计算（换算）。
  - 美元按 2026-10-20 欧洲央行参考汇率折算：1 欧元 = 1.1215 美元[^1]，1 欧元 = 7.4894 元[^1]，即 1 美元约合 6.68 元（换算）。
  - 按时长或音频 token 计费的，按每分钟约 260 个汉字估算，1 万汉字约合 38 分钟语音（实测：两个 Edge 中文音色朗读同一段 203 个汉字，分别用时 48.0 秒和 45.0 秒）。
  - 按调用次数计费的，按每次都用满字数上限计算；如果每次只合成一句短话，实际单价会高得多（推断）。
- **时效**: 价格、活动和免费额度变化很快，付费前请以官网为准。

## 一、要点

1. **长期免费的官方额度不多，而且各有门槛**：
   - Azure 的免费档 F0 每月 50 万字符[^2]，世纪互联运营的 Azure 中国也一样[^3]。Azure 把一个汉字算 2 个字符[^4]，所以约合每月 25 万汉字（换算）。
   - Google Cloud 每月免费 Standard/WaveNet 400 万字符、Chirp 3 HD 100 万字符[^5]，但必须先开通结算[^5]。
   - 讯飞在线语音合成每天免费 500 次[^6]；百炼的 Sambert 每个模型每月 3 万字符[^7]。
   - 海外小厂：Speechify API 每月 50 万字符，不用绑卡，标注可以商用[^8]；Unreal Speech 每月 25 万字符，免费档发布音频时要署名[^9][^10]。
2. **免费的模型**：
   - Gemini API 的 `gemini-3.8-flash-tts` 在免费层不收费[^11]，但免费层的数据会被用于改进产品[^11]，可用地区列表里也没有中国大陆和香港[^12]。
   - Fish Audio 的 `s2.1-pro-free` 单价为 0，限于合理使用，没有延迟保证[^13][^14]。
   - 小米 MiMo 的三个 TTS 模型限时免费[^15]，截止日期没写。
   - Edge 浏览器的在线朗读服务免费，开源库 edge-tts 调用的就是它[^16]。它不是微软对开发者提供的 API，没有价格、额度和 SLA（推断）。
   - 10 月微软改了令牌格式，旧版本大面积报 403[^17]。edge-tts 7.3.1 已改用新前缀[^18]，10-21 实测可以合成中文。
3. **国内大厂的新人赠送最多**：
   - 腾讯云基础/精品音色送 800 万字符，3 个月有效，每个账号一次[^19]。
   - 阿里云智能语音交互（NLS）开通后可以试用 3 个月[^20]，试用期语音合成不限调用量，但并发只有 2[^21]。
   - 百度短文本合成个人认证送 5 万次，永久有效[^22]；每 120 个 GBK 字节（约 60 个汉字）算 1 次[^23]。
   - 豆包语音合成 2.0 送 2 万字符，半年有效[^24]；百炼每个模型 1 万字符，90 天有效[^7][^25]。
4. **比价前先看一个汉字算几个字符**：
   - 百炼、MiniMax 国内站、Azure 把一个汉字算 2 个字符[^7][^26][^4]。
   - 豆包、腾讯、阶跃把一个汉字算 1 个字符[^27][^19][^28]。
   - 硅基流动和 Fish Audio 按 UTF-8 字节计费[^29][^13]，一个常用汉字占 3 个字节（推断）。
   - 多数海外厂商只写“按字符计费”，没说汉字怎么算。
5. **按量付费最便宜的（能合成中文）**：
   - 传统音色：华为云普通发音人的套餐包折合约 0.16–0.18 元/万汉字，百度短文本基础音库约 0.33 元/万汉字（换算）；腾讯精品音色 0.3 元/万字符[^19]。
   - 大模型音色：阶跃 `step-tts-mini` 0.9 元/万字符[^28]，腾讯大模型音色 1.2 元/万字符，用量大时更低[^19]。硅基流动的 CosyVoice2 和百炼的 `qwen3-tts-flash` 折合约 1.5–1.6 元/万汉字（换算）。
   - 海外托管的开源模型 Kokoro 最便宜：OpenRouter \$0.62/百万字符[^30]，DeepInfra \$0.99/百万字符[^31]。但 Kokoro 的中文音色质量评级只有 D[^32]。
6. **声音复刻**：
   - 百炼的 Qwen-Audio-TTS 和 CosyVoice 创建复刻音色免费，合成时按模型计费[^33]。
   - MiniMax 和阶跃每个音色 9.9 元[^26][^28]。
   - 智谱 6 元/次[^34]，百度 8.8 元/个[^35]。
   - 豆包按音色槽位收费，每个 138 元，量大降到 28 元[^27]。
7. **数据政策**：
   - 会使用用户数据的：Gemini 免费层[^11]；ElevenLabs 默认会用，可以关闭[^36]；Amazon Polly 可能用于改进服务，可以退出[^37]。
   - 写明不训练或不存储的：OpenAI API[^38]、Google Cloud TTS[^39]、Azure 预置音色[^40]。
   - 国内写明不用于训练的有百炼[^41]和豆包（豆包有例外条款）[^42]。
8. **正在下线的**：
   - OpenAI 的 `tts-1`、`tts-1-hd`、`gpt-4o-mini-tts` 已宣布弃用，2027-01-06 停服[^43]。
   - Hume 的 TTS API 2026-11-13 停止服务[^44]。
   - PlayHT 被 Meta 收购[^45]，据竞品 Inworld 的迁移指南，2025 年底已经关停[^46]。
9. **自己部署**：
   - 权重可以商用、中文能力强的有 CosyVoice 3[^47]、Qwen3-TTS[^48]、VoxCPM2[^49]，详见第七节。
   - F5-TTS[^50]、Spark-TTS[^51]、XTTS-v2[^52] 的权重不能商用。

## 二、计费口径：一个汉字算几个字符

同样 1 万个汉字，百炼按 2 万字符计费，豆包按 1 万字符计费，硅基流动按 3 万字节计费（换算）。

| 口径 | 平台 | 说明 |
| --- | --- | --- |
| 1 个汉字 = 2 个字符 | 阿里百炼 | 英文字母、数字、标点、空格各算 1 个；SSML 标签不计[^7] |
| 1 个汉字 = 2 个字符 | MiniMax 国内站 | 字母、标点、空格、回车各算 1 个[^26] |
| 1 个汉字 = 2 个字符 | Azure（全球和中国） | 除 `<speak>`、`<voice>` 以外的 SSML 标记都计费[^4] |
| 1 个汉字 = 2 个字符 | 阿里 NLS | 每 100 个字符算 1 次调用，单次最多 300 个字符[^20]；但接口说明页写一个汉字算 1 个字符[^53]，两页矛盾 |
| 1 个汉字 = 1 个字符 | 豆包语音 | 按字符数计费，与 UTF-8 字节数无关；SSML 标签照常计费[^27] |
| 1 个汉字 = 1 个字符 | 腾讯云 | 使用 SSML 不额外收费[^19][^54] |
| 1 个汉字 = 1 个字符 | 阶跃星辰 | 2 个英文字母或 2 个标点才算 1 个字符[^28] |
| 1 个汉字 = 1 个字符 | 百度（长文本、声音复刻） | [^55][^35] |
| 1 个汉字 = 1 个字符 | 讯飞（超拟人合成） | [^56] |
| 1 个汉字 = 1 个字符 | 华为云 | 普通发音人每 100 个字符算 1 次调用，精品发音人每 50 个字符算 1 次[^57] |
| 1 个汉字 = 1 个字符 | Google Cloud（Standard、WaveNet） | 多字节字符只算 1 个字符[^5]；SSML 标签计入（`<mark>` 除外）[^5] |
| 按字节 | 硅基流动、SiliconFlow 国际站 | 按输入文本的 UTF-8 字节数[^29][^58] |
| 按字节 | Fish Audio | 按百万 UTF-8 字节计价[^13] |
| 按字节 | 百度（短文本） | 每 120 个 GBK 字节算 1 次，约 60 个汉字[^23] |
| 按次，字数没写 | 讯飞在线合成、思必驰 | 官方页面没写一次对应多少字 |
| 没写 | OpenAI、Gemini、Amazon Polly、ElevenLabs、Cartesia、Inworld、xAI、Mistral 等 | 只写按字符或按 token 计费；Polly 写明 SSML 标签不计费[^59] |

## 三、免费额度

### 3.1 长期免费（按月或按天重置）

| 平台 | 免费内容 | 条件和限制 | 中文 |
| --- | --- | --- | --- |
| Azure AI Speech | F0 每月 50 万字符[^2] | 汉字算 2 个字符[^4]；F0 每 60 秒最多 20 次请求[^60] | 普通话、粤语、吴语、四川话等[^61] |
| Azure 中国（世纪互联） | F0 每月 50 万字符[^3] | 国内网络可以直连（实测）；开户条件本次没查 | 同上 |
| Google Cloud TTS | Standard/WaveNet 每月 400 万字符，Neural2 100 万字符[^5]；Chirp 3 HD 100 万字符[^5] | 必须开通结算[^5]；Standard 和 WaveNet 用同一个计费 SKU，免费额度可能是共用的（推断） | 普通话有约 30 个 Chirp3-HD 音色[^62]，粤语也有[^62] |
| Gemini API | `gemini-3.8-flash-tts`、`gemini-3.8-flash-lite-tts`、`gemini-2.5-flash-preview-tts` 免费层不收费[^11] | 免费层限速只有登录后才能看到[^63]；数据用于改进产品[^11]；可用地区没有中国大陆和香港[^12] | 支持中文和粤语[^64] |
| 讯飞在线合成 | 每天 500 次[^6] | 一次对应多少字没写 | 37 个语种、11 种方言[^65] |
| 百炼 Sambert | 每个模型每月 3 万字符[^7] | 只在北京地域 | — |
| Speechify API | 每月 50 万字符，用完暂停到下月[^8] | 不用绑卡；标注可以商用[^8] | 文档说 `simba-3.5` 支持中文且所有档位可用[^66]；定价页说自助档复刻只支持英语和另外 6 种语言[^8]，中文能否用没确认 |
| Unreal Speech | 每月 25 万字符，每月 1 日重置[^9][^10] | 免费档发布音频要署名并附链接[^10]；不支持声音复刻[^10] | 有普通话[^10] |
| ElevenLabs | 每月 1 万 credits[^67] | 不能商用，发布时要署名[^68] | 支持普通话[^69] |
| Cartesia | 每月 20K credits[^70]，约 27 分钟[^70] | 商用许可从 Pro 档起[^70] | 支持中文[^71] |
| Fish Audio | `s2.1-pro-free` 单价为 0[^13] | 限合理使用，额度没写[^14] | 中文属于一档语言[^72] |
| Cloudflare Workers AI | 每天 1 万 Neurons[^73] | 折合 MeloTTS 约 536 分钟/天（换算）；每天 00:00 UTC 重置[^73] | 托管版 MeloTTS 能否合成中文没核实，`lang` 参数默认是 `en`[^74] |
| NVIDIA build | 所有模型免费试用，不用绑卡[^75] | 只能试用，不能用于生产[^76]；可能被限流[^77] | `magpie-tts-multilingual` 支持普通话[^78] |
| Groq | 免费计划的 Orpheus 每天 100 次[^79] | — | 只支持英语和阿拉伯语[^80] |
| 小米 MiMo | 三个 TTS 模型限时免费[^15] | 每分钟 100 次[^81]；截止日期和之后的价格都没公布 | 有中文音色，可选方言风格[^82] |
| 魔搭 API-Inference | 免费给开发者体验[^83] | 是否包含 TTS 模型没核实 | — |
| Edge 朗读（edge-tts） | 免费，没有官方额度说明 | edge-tts 调用的是 Edge 的在线朗读服务[^16]，不是微软对开发者提供的 API（推断）；微软禁止自定义 SSML[^16]；10 月起旧版本报 403[^17] | Hermes 文档写有 322 个音色、74 种语言[^84] |

另外，IBM watsonx Text to Speech 每月免费 1 万字符[^85]，但语言列表里没有中文（推断）。

### 3.2 新人一次性赠送

国内：

| 平台 | 赠送内容 | 有效期和条件 |
| --- | --- | --- |
| 腾讯云 | 超自然大模型音色 2 万、大模型音色 10 万、基础/精品音色 800 万字符[^19] | 领取后 3 个月，每个账号一次，不含长文本和播客接口[^19]；开通前要完成实名和人脸认证[^86] |
| 腾讯云 | 一句话复刻 5 个音色和 1 万字符合成[^87] | 同上 |
| 阿里 NLS | 语音合成试用 3 个月[^20]，不限调用量，并发 2[^21] | 长文本合成、CosyVoice 流式合成不能试用[^20] |
| 百度智能云 | 短文本基础/精品音库个人 5 万次、企业 10 万次[^22]；长文本个人 5 万字符[^22] | 永久有效，每个认证主体只发一次[^22] |
| 百度智能云 | 大模型声音复刻：个人 10 次创建、5 万字符合成[^22] | 同上 |
| 讯飞 | 在线合成个人 1 万次、企业 2 万次，3 个月[^65] | 领取前要实名[^88]；同一产品只能领一次[^88] |
| 讯飞 | 超拟人合成个人 1 万字符[^89]；长文本 10 万字符，30 天[^90] | — |
| 讯飞 | 一句话复刻训练 5 次、合成 5 万字符，3 个月[^91] | 认证后领取 |
| 豆包语音 | 语音合成 2.0、声音复刻 2.0 各 2 万字符，半年[^24]；播客模型 100 万 token[^24] | 在控制台点“试用”领取[^24]；试用期可以用全部音色[^24] |
| 阿里百炼 | 多数 TTS 模型各 1 万字符[^7]；按 token 计费的模型各 100 万 token[^7] | 90 天[^25]；只在北京地域[^25]；不需要实名[^25] |
| 阿里百炼 | 声音复刻 `qwen-voice-enrollment` 1000 个音色[^7] | — |
| MiniMax、阶跃、智谱、硅基流动 | 官方文档没写赠送多少 | 阶跃提到有“免费套餐”，使用前要实名[^92] |

海外：

| 平台 | 赠送内容 | 说明 |
| --- | --- | --- |
| Google Cloud | 新客户 \$300，90 天[^93] | 可以用于 TTS |
| Azure | 免费账户 \$200，30 天[^94] | 注册要验证信用卡[^94]；不适用于 Azure 中国[^94] |
| AWS | 新客户最多 \$200 抵扣金，可用于 Polly[^95] | 免费计划 6 个月[^95] |
| Deepgram | \$200，不过期[^96] | Aura 不支持中文[^97] |
| Speechmatics | 前 100 万字符免费，另送 \$100[^98] | 只有 4 个英语音色[^99] |
| Rime | \$50[^100] | 不支持中文[^100] |
| Smallest.ai | \$10[^101] | 中文只在 v3.1 Pro[^102] |
| Inworld | 按量档含约 70 分钟 TTS[^103] | 中文属于一档语言[^104] |
| Murf | 定价页写注册送 \$10[^105]，API 文档写一次性 10 万字符[^106] | 两处矛盾 |
| Lemonfox | 首月免费[^107] | 支持中文[^108] |
| SiliconFlow 国际站 | \$1[^109] | — |
| Hume | \$20[^110] | TTS 2026-11-13 停止 |

### 3.3 包月套餐里的 TTS

- **阶跃 Step Plan**：
  - Mini 档每月 ¥49，含 400M Credit[^111]；1 元 = 100 万 Credit[^111]，语音按开放平台的价格折算扣减[^112]。按此算，¥49 相当于 400 元的开放平台用量（换算）。
  - Step Plan 只支持 `stepaudio-2.5-tts` 这一个 TTS 模型[^112]，按 5.8 元/万字符[^28] 算约可合成 69 万字，前提是额度全部用于 TTS（换算）。套餐自身的限速没查到。
- **MiniMax M Plan**：Go 档原价 ¥49/月起[^113]，三档都包括图像和音频模型[^114]。音频与文本共用额度，按按量价扣减[^115]，能合成多少字没公布。官方建议生产环境用按量付费[^115]。
- **小米 MiMo Token Plan**：TTS 限时免费，不消耗套餐额度[^116]。
- **海外订阅**：
  - MiniMax 国际站 Audio Subscription \$5/月起[^117]。
  - ElevenLabs Starter \$6/月，含 3 万 credits、商用许可和即时复刻[^67]。
  - Cartesia Pro \$5/月 100K credits，含商用许可和即时复刻[^70]；Fish Audio Plus \$15/月[^118]。

## 四、按量付费价格

### 4.1 国内（人民币）

“折合”一列是换算值，按纯中文、官方原价第一档计算。

| 平台 | 模型或音色 | 官方单价 | 折合元/万汉字 | 备注 |
| --- | --- | --- | --- | --- |
| 华为云 SIS | 普通发音人 | 套餐包 1 万次 18 元、100 万次 1600 元[^119] | 0.16–0.18 | 每 100 字符算 1 次[^57]；精品发音人每 50 字符算 1 次，折合翻倍 |
| 腾讯云 | 精品音色 | 0.3 元/万字符[^19] | 0.3 | 资源包低至 0.21[^19] |
| 百度智能云 | 短文本基础音库 | 2.0 元/千次[^120] | 0.33 | 每次约 60 个汉字[^23]；精品音库 4.0 元/千次[^120]，折合 0.67 |
| 阿里 NLS | 语音合成 | 3.50 元/千次[^121] | 0.7 | 每 100 字符算 1 次，汉字算 2 个字符[^20] |
| 阶跃星辰 | `step-tts-mini` | 0.9 元/万字符[^28] | 0.9 | 汉字算 1 个字符[^28] |
| 腾讯云 | 大模型音色 | 1.2 元/万字符，日用量大时降到 0.55[^19] | 1.2 | 资源包低至 0.4[^19] |
| 硅基流动 | CosyVoice2-0.5B、MOSS-TTSD | ¥0.05/千 UTF-8 字节[^122] | 1.5 | 一个汉字约 3 字节 |
| 阿里百炼 | `qwen3-tts-flash`、`cosyvoice-v3.5-flash` | 0.8 元/万字符[^7] | 1.6 | 汉字算 2 个字符[^7] |
| Azure 中国 | 神经网络语音 | ￥95.4/百万字符[^3] | 1.9 | 汉字算 2 个字符 |
| 阿里百炼 | `cosyvoice-v3-flash`、`qwen-audio-3.0-tts-flash` | 1 元/万字符[^7] | 2 | — |
| 智谱 | GLM-TTS | 2 元/万字符[^34] | 约 2 | 汉字怎么计数没写，按 1 个字符估算 |
| 云知声 | U2-TTS | 2 元/万字[^123] | 2 | — |
| 讯飞 | 超拟人合成 | 套餐 500 万字符 1000 元[^89] | 2 | 大套餐低至 1.2[^89] |
| 百度智能云 | 长文本基础音库 | 2 元/万字符[^120] | 2 | — |
| 阶跃星辰 | `stepaudio-3-tts`、`step-tts-2`、`stepaudio-2.5-tts` | 2.5、2.8、5.8 元/万字符[^28] | 2.5–5.8 | — |
| 豆包语音 | 语音合成 2.0 | 3 元/万字符[^27] | 3 | 资源包低至 2.1[^27] |
| 阿里百炼 | `cosyvoice-v3.5-plus`、`cosyvoice-v3-plus` | 1.5、2 元/万字符[^7] | 3–4 | — |
| MiniMax 国内站 | `speech-2.8-turbo` | 2 元/万字符[^26] | 4 | 汉字算 2 个字符[^26] |
| 腾讯云 | 超自然大模型音色 | 6.5 元/万字符[^19] | 6.5 | — |
| MiniMax 国内站 | `speech-2.8-hd` | 3.5 元/万字符[^26] | 7 | — |
| 讯飞 | 在线合成 | 50 万次 2000 元[^65] | — | 一次对应多少字没写 |

### 4.2 海外（美元）

海外厂商大多没写汉字怎么计数，“折合”一列按 1 个汉字算 1 个字符估算（换算）。

| 平台 | 模型 | 官方单价 | 折合元/万汉字 | 中文 | 备注 |
| --- | --- | --- | --- | --- | --- |
| OpenRouter | Kokoro 82M | \$0.62/百万字符[^30] | 0.04 | 有，但质量评级低[^32] | OpenAI 兼容[^124] |
| DeepInfra | Kokoro-82M | \$0.99/百万字符[^31] | 0.07 | 同上 | 必须绑卡或预付[^125] |
| DeepInfra | chatterbox-multilingual | \$1.00/百万字符[^31] | 0.07 | 支持[^31] | — |
| Lemonfox | — | \$2.50/百万字符[^108] | 0.17 | 支持[^108] | OpenAI 兼容[^108] |
| Google Cloud | Standard、WaveNet | \$4/百万字符[^5] | 0.27 | 支持 | 有免费额度 |
| Together AI | Kokoro | \$4/百万字符[^126] | 0.27 | — | 最低预付 \$15[^127] |
| Speechify | simba | 超出套餐后 \$10–6/百万字符[^8] | 0.4–0.67 | 有矛盾 | — |
| Unreal Speech | — | 超出套餐后 \$20–8/百万字符[^10] | 0.53–1.34 | 支持 | 底层是 Kokoro[^9] |
| Murf | Falcon 2.1 | \$10/百万字符[^128] | 0.67 | 没核实 | — |
| Mistral | Voxtral TTS 3 | \$13/百万字符[^129] | 0.87 | 说法矛盾[^130][^131] | — |
| xAI | — | \$15/百万字符[^132] | 1.0 | 支持[^133] | — |
| OpenAI | `tts-1` | \$15/百万字符[^134] | 1.0 | 支持，音色针对英语优化[^43] | 2027-01-06 停服 |
| Inworld | TTS-2 Flash / TTS-2 | \$15 / \$25 每百万字符[^103] | 1.0 / 1.67 | 支持 | 有 OpenAI 兼容接口[^135] |
| Amazon Polly | Neural | \$16/百万字符[^95] | 1.07 | 普通话只有 1 个女声[^136] | — |
| DeepInfra | Qwen3-TTS | \$20/百万字符[^31] | 1.34 | 支持[^31] | 3 秒样本可以克隆[^31] |
| SiliconFlow 国际站 | CosyVoice2 | \$7.15/百万 UTF-8 字节[^109] | 1.43 | 支持 | — |
| Azure | 神经语音 | \$15/百万字符[^137] | 2.0 | 支持 | 汉字算 2 个字符 |
| Google Cloud | Chirp 3 HD | \$30/百万字符[^5] | 2.0 | 支持 | — |
| Gemini API | `3.8-flash-lite-tts` / `3.8-flash-tts` | 音频输出 \$6 / \$9 每百万 token[^11] | 2.3 / 3.5 | 支持 | 每秒音频 25 个 token[^11]；2027 年起涨价一倍 |
| ElevenLabs | Flash / v3、v4 | \$0.04 / \$0.08 每千字符[^138] | 2.7 / 5.3 | 支持 | — |
| Cartesia | Sonic | 超出套餐后 \$38–65/百万 credits[^70] | 2.5–4.3 | 支持 | 1 credit = 1 字符[^70] |
| Fish Audio | `s2.1-pro` | \$15/百万 UTF-8 字节[^13] | 3.0 | 支持 | — |
| MiniMax 国际站 | turbo / hd | \$60 / \$100 每百万字符[^117] | 4.0 / 6.7 | 支持 | — |
| Deepgram | Aura-2 | \$0.030/千字符[^96] | — | 不支持[^97] | — |
| Groq | Orpheus | \$22/百万字符[^139] | — | 不支持[^80] | — |

其他托管开源模型的平台：

- fal.ai 的 Kokoro 是 \$0.02/千字符，有普通话专用端点和 8 个中文音色[^140]。IndexTTS 2.0 按秒计费，\$0.002/秒[^141]，折合约 31 元/万汉字（换算）。
- Replicate 按硬件秒数计费，T4 \$0.000225/秒[^142]；社区上传的 Kokoro 约 \$0.00042/次[^32]。
- Cloudflare 的 MeloTTS 是 \$0.0002/音频分钟[^73]。
- Hugging Face Inference Providers 的免费用户没有月度额度[^143]。接入的 TTS 模型只有 7 个（按接口返回统计），例如 Kokoro-82M[^144] 和 chatterbox[^144]。

## 五、声音复刻和音色设计

| 平台 | 复刻或设计的费用 | 合成单价 | 样本要求和限制 |
| --- | --- | --- | --- |
| 阿里百炼 | Qwen-Audio-TTS、CosyVoice 创建复刻音色免费[^33]；声音设计也免费[^145] | 按目标模型 | 推荐 10–20 秒，最长 60 秒[^33]；每个账号最多 1000 个[^33] |
| 阿里百炼 | Qwen-TTS 复刻 0.01 元/个，送 1000 个[^7] | — | — |
| MiniMax 国内站 | 快速复刻、音色设计各 9.9 元/个，首次合成时才收[^26] | 同普通合成 | 10 秒到 5 分钟[^146]；7 天内不用会被删除[^147] |
| MiniMax 国际站 | 复刻 \$1.5/个，设计 \$3/个[^117] | 同普通合成 | — |
| 阶跃星辰 | 9.9 元/个，复刻成功就收费[^28] | 同普通合成 | 5–10 秒[^148] |
| 智谱 | GLM-TTS-Clone 6 元/次[^34] | — | 约 3 秒[^149] |
| 百度智能云 | 8.8 元/个，预付最低 4 元/个[^35] | 7 元/万字符[^35] | — |
| 腾讯云 | 一句话复刻 39 元/个，大包 12 元/个[^87] | 8 元/万字符，量大降到 6.4[^87] | 5–15 秒[^150]；免费存储 3 个月，之后 0.03 元/个/天[^87] |
| 讯飞 | 一句话复刻标准版训练 5 元/次，量大降到 3 元[^91] | 2 元/万字符，量大降到 1.5[^91] | — |
| 云知声 | 10 元/个，首次合成时收[^123] | 2 元/万字 | — |
| 豆包语音 | 音色槽位 138 元/个，量大降到 28 元[^27] | 3 元/万字符[^27] | 最短 5 秒[^151]；试听音色 7 天内不正式调用会被删除[^27] |
| ElevenLabs | 即时复刻从 Starter（\$6/月）起[^67] | 同普通合成 | 少于 2 分钟的音频即可[^152] |
| Cartesia | 即时复刻从 Pro（\$5/月）起[^70] | 同普通合成 | 10 秒起[^153] |
| Inworld | 即时复刻所有用户都能用[^154] | 同普通合成 | 3 秒起 |
| Fish Audio | 音色设计 \$0.01/次[^13] | 同普通合成 | 至少 10 秒[^155] |
| Gemini API | 3.8 TTS 模型支持复刻和设计[^64] | 价格页没写额外费用 | 10–30 秒，另加一段授权录音[^156] |
| xAI | 控制台可以免费建 30 个[^157] | 同普通合成 | 只在美国可用（伊利诺伊州除外）[^157] |
| OpenAI | 录音复刻只对符合条件的客户开放[^158] | — | — |

## 六、中文和方言

- 方言多的国内平台：
  - 百炼 `qwen3-tts-flash` 的系统音色覆盖北京话、上海话、四川话、南京话、陕西话、闽南话、天津话、粤语[^159]。
  - 讯飞有 11 种方言[^65]；百度大模型音库有粤语、四川话等方言音色[^160]；豆包有 130 多款音色，覆盖多种方言口音[^151]。
- 海外：
  - Azure 除普通话外还有粤语、吴语、四川话[^61]；Google 普通话有约 30 个 Chirp3-HD 音色[^62]。
  - Amazon Polly 的普通话和粤语各只有 1 个女声[^136]。
  - 不支持中文的：Deepgram Aura[^97]、Hume[^44]、Rime[^100]。
  - Speechmatics[^99] 和 Groq[^80] 也不支持中文。

## 七、开源模型（自己部署）

| 模型 | 权重许可 | 能否商用 | 中文 | 说明 |
| --- | --- | --- | --- | --- |
| CosyVoice 3（阿里） | Apache-2.0[^47] | 可以 | 9 种语言、18 种以上方言[^161] | 双向流式，延迟约 150ms[^161] |
| Qwen3-TTS（阿里） | Apache-2.0[^48] | 可以 | 10 种语言，有方言音色[^162] | 3 秒克隆[^162]；延迟约 97ms[^162] |
| VoxCPM2（面壁智能） | Apache-2.0，写明可以免费商用[^49] | 可以 | 9 种方言[^49] | 约 8GB 显存[^49]；可用 vLLM-Omni 提供 OpenAI 兼容接口[^163] |
| MOSS-TTSD | Apache-2.0[^164] | 可以 | 支持 | 多人长对话，零样本克隆[^164]；8B 参数[^164] |
| FireRedTTS-2（小红书） | Apache-2.0[^165] | 可以 | 7 种语言含中文[^165] | 4 人 3 分钟对话[^166]；bf16 约 9GB 显存[^166] |
| SoulX-Podcast | Apache-2.0[^167] | 可以 | 四川话、河南话、粤语[^167] | 暂不支持流式[^168] |
| Step-Audio-TTS-3B（阶跃） | Apache-2.0[^169] | 可以 | 粤语、四川话等方言[^256] | 情感和风格控制[^169] |
| GPT-SoVITS | MIT[^170][^171] | 可以 | 中、英、日、韩、粤[^172] | 5 秒零样本，1 分钟数据微调[^172] |
| Ming-3.0-tts-0.5B（蚂蚁） | MIT[^173] | 可以 | 四川话、粤语[^173] | 100 多个中文音色[^173] |
| GLM-TTS（智谱） | 模型卡写 MIT[^174]，代码仓库写 Apache-2.0[^175] | 可以 | 以中文为主[^176] | 3–10 秒克隆[^176] |
| Kokoro-82M | Apache[^177] | 可以 | 普通话 8 个预置音色[^178] | 没有克隆功能（推断） |
| Chatterbox（Resemble） | MIT[^179] | 可以 | 多语言版含中文[^179] | 输出带隐形水印[^179] |
| Zonos（Zyphra） | Apache-2.0[^180] | 可以 | 支持[^181] | — |
| IndexTTS-2（B 站） | B 站自有许可，免版税[^182] | 月活超过 1 亿或年营收超过 10 亿元要另外申请[^182] | 支持 | 不能用来改进其他模型[^182] |
| Higgs Audio 2（Boson） | 社区许可[^183] | 年活跃用户超过 10 万要申请[^183] | — | — |
| Fish Speech | 社区许可[^184] | 年营收低于 50 万美元可以商用[^184]，但不能对外提供托管服务[^184] | 中文属于一档语言[^72] | S2-Pro 的权重是研究许可[^72] |
| F5-TTS | 代码 MIT，权重 CC-BY-NC[^50] | 不可以 | — | — |
| Spark-TTS | CC-BY-NC-SA[^51] | 不可以 | — | — |
| MaskGCT | CC-BY-NC[^185] | 不可以 | — | — |
| ChatTTS | 模型 CC BY-NC[^186] | 不可以 | — | — |
| XTTS-v2 | Coqui 公共模型许可，只能非商用[^52] | 不可以 | — | Coqui 公司已关闭（据 GitHub 社区讨论转引的创始人推文）[^187] |

其他：

- MegaTTS3 没有公开编码器参数，不能用任意音频克隆[^188]。
- 微软 VibeVoice 2025-09-05 移除了 TTS 代码[^189]。
- Piper 原仓库已归档[^190]，新仓库改为 GPL-3.0[^191]。
- 许可证写着 Apache 或 MIT，训练数据仍可能有授权问题，商用前要自己评估（推断）。

## 八、数据政策和商用条款

| 平台 | 是否用于训练 | 其他 |
| --- | --- | --- |
| OpenAI | 默认不用于训练[^38] | 滥用监控日志最多保存 30 天[^38]；必须告知用户听到的是 AI 声音[^43] |
| Google Cloud TTS | 不记录文本和音频[^39] | 生成的音频可以用于应用和媒体[^192] |
| Gemini API | 免费层会用于改进产品[^11]，人工审核员可能阅读输入输出[^193]；付费层不会 | — |
| Azure | 预置音色的输入和输出都不存日志[^40] | — |
| Amazon Polly | 可能用于改进服务[^37]，可以退出[^37] | — |
| ElevenLabs | 默认会用，可以关闭；企业客户默认不用[^36] | 免费档不能商用[^68]；付费档都含商用许可[^68] |
| xAI | 未经许可不训练，默认保存 30 天[^194] | — |
| Mistral | 可以单独关闭训练[^195] | — |
| Hume | 用户授予 Hume 永久许可，可以用录音改进服务[^196] | — |
| DeepInfra | 不训练，不存储（Google、Anthropic 模型除外）[^197] | — |
| NVIDIA 试用 | 会话结束后不存储内容[^76]，但会收集匿名指标用于改进[^76] | 不能用于生产[^76] |
| 阿里百炼 | 不用于训练[^41] | — |
| 豆包语音 | 不用于训练，有例外条款[^42] | 只许可在中国大陆使用[^42] |
| 腾讯云 | FAQ 说接口不保存数据[^54] | FAQ 说可以商用[^54] |
| 华为云 | 合成文本处理完立即释放[^198] | — |
| 讯飞 | 用户协议里没有训练条款（推断） | 超拟人合成可以加音频水印[^56] |
| 智谱 | — | 默认加显式和隐式水印[^199] |
| 阶跃星辰 | — | 音频归用户所有，建议标注由 AI 生成[^200] |

## 九、已下线、即将停服或不推荐

| 平台或模型 | 状态 |
| --- | --- |
| OpenAI `tts-1`、`tts-1-hd`、`gpt-4o-mini-tts` | 2026-10-01 宣布弃用，2027-01-06 停服[^201]；替代模型走 Realtime API，不支持 `/v1/audio/speech`[^43] |
| Hume TTS 和 EVI | 2026-11-13 停止，之后删除账户数据[^44] |
| PlayHT / PlayAI | 2025 年 7 月被 Meta 收购[^45]；2025-12-31 全部关停，账户和克隆音色被删除（来源是竞品 Inworld 的迁移指南）[^46] |
| Groq 的 PlayAI TTS | 2025-12-31 停用，由 Orpheus 替代[^202] |
| LMNT | 已关停[^203] |
| Resemble AI | 不再把 TTS 作为商业产品销售[^204] |
| Inworld `tts-1`、`tts-1-max` | 2026-06-15 停止服务[^205] |
| Fish Audio `s1` | 2026-12-31 退役[^206] |
| Rime Arcana | 2026-08-15 退役[^207] |
| Gemini `gemini-3.1-flash-tts-preview` | 已标为遗留模型[^208] |
| 豆包大模型语音合成 1.0 | 已列入历史模型价格[^27] |
| 百炼 Qwen3 的指令、复刻、设计模型 | `qwen3-tts-instruct-flash`、`qwen3-tts-vc`、`qwen3-tts-vd` 等详情页已跳转到通用页，可能已下线（推断） |
| Edge 朗读（edge-tts） | 10 月起旧版本报 403[^17]；7.3.1 换了新的令牌前缀[^18]，10-21 实测可用 |
| 微软 VibeVoice | 2025-09-05 移除 TTS 代码[^189] |
| Piper | 原仓库已归档[^190]，新仓库改为 GPL-3.0[^191] |

## 十、怎么接入

### 10.1 接口速查

| 平台 | API Key 页面 | 接口地址 | 鉴权 | OpenAI 兼容 |
| --- | --- | --- | --- | --- |
| 阿里百炼 | <https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key>[^209] | `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`[^210] | `DASHSCOPE_API_KEY`[^211] | 没找到 |
| 豆包语音 | <https://console.volcengine.com/speech/new/setting/apikeys>[^212] | `https://openspeech.bytedance.com/api/v3/tts/unidirectional`[^213] | `X-Api-Key` + `X-Api-Resource-Id`[^213] | 否 |
| 腾讯云 | <https://console.cloud.tencent.com/cam/capi>[^214] | `tts.tencentcloudapi.com`，Action=TextToVoice[^215] | TC3-HMAC-SHA256 签名[^216] | 否 |
| 百度智能云 | 控制台“应用列表”[^217] | `https://tsn.baidu.com/text2audio`[^23] | API Key + Secret Key 换 access_token[^217] | 否 |
| 讯飞 | 控制台服务页面[^218] | `wss://tts-api.xfyun.cn/v2/tts`[^218] | HMAC-SHA256 签名[^218] | 否 |
| 华为云 | — | `POST https://{endpoint}/v1/{project_id}/tts`[^57] | IAM Token[^57] | 否 |
| MiniMax 国内站 | 账户管理 > 接口密钥[^219] | `https://api.minimax.cn/v1/t2a_v2`[^220] | Bearer[^220] | 否 |
| 阶跃星辰 | <https://platform.stepfun.com/interface-key>[^221] | `https://api.stepfun.com/v1/audio/speech`[^222] | Bearer[^223] | 是，官方示例用 OpenAI SDK[^222] |
| 智谱 | <https://bigmodel.cn/usercenter/proj-mgmt/apikeys>[^224] | `https://open.bigmodel.cn/api/paas/v4/audio/speech`[^199] | Bearer[^199] | 路径相同，字段没核实 |
| 硅基流动 | API 密钥页面[^225] | `https://api.siliconflow.cn/v1/audio/speech`[^29] | Bearer[^226] | 是，官方示例用 OpenAI SDK[^29] |
| 小米 MiMo | — | `https://api.xiaomimimo.com/v1/chat/completions`[^227] | `api-key` 或 Bearer[^227] | 走 Chat Completions，不是 `/v1/audio/speech` |
| Azure 中国 | — | `https://chinaeast2.tts.speech.azure.cn/cognitiveservices/v1`[^228] | 资源密钥或 STS 令牌[^228] | 否 |
| Azure | — | `https://<region>.tts.speech.microsoft.com/cognitiveservices/v1`[^229] | `Ocp-Apim-Subscription-Key`[^229] | 否 |
| Google Cloud | — | `texttospeech.googleapis.com`[^230] | OAuth 令牌[^230] | 否 |
| Gemini API | <https://aistudio.google.com/api-keys>[^231] | `https://generativelanguage.googleapis.com/v1beta/interactions`[^64] | `x-goog-api-key`[^64] | 否 |
| OpenAI | — | `https://api.openai.com/v1/audio/speech`[^43] | Bearer[^43] | 原生 |
| ElevenLabs | — | `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`[^232] | `xi-api-key`[^233] | 否 |
| Cartesia | <https://play.cartesia.ai/keys>[^234] | `https://api.cartesia.ai`[^234] | Bearer[^234] | 否 |
| Fish Audio | — | `https://api.fish.audio/v1/tts`[^235] | Bearer | 否 |
| Mistral | — | `https://api.mistral.ai/v1/audio/speech`[^236] | Bearer | 路径相同，返回 base64 编码的音频[^236] |
| xAI | — | `https://api.x.ai/v1/tts`[^133] | Bearer | 否 |
| Inworld | — | `https://api.inworld.ai`[^135] | Basic | 有兼容接口[^135] |
| Lemonfox | — | `https://api.lemonfox.ai/v1/audio/speech`[^108] | Bearer | 是 |
| Speechify | — | `https://api.speechify.ai/v1/audio/speech`[^237] | Bearer | 路径相同，请求字段不同 |
| DeepInfra | — | `https://api.deepinfra.com/v1/audio/speech`[^238] | Bearer | 是 |
| OpenRouter | — | `https://openrouter.ai/api/v1/audio/speech`[^124] | Bearer | 是 |
| Together AI | — | `https://api.together.ai/v1/audio/speech`[^239] | Bearer | 是 |
| Groq | — | `https://api.groq.com/openai/v1/audio/speech`[^80] | Bearer | 是 |
| SiliconFlow 国际站 | — | `https://api.siliconflow.com/v1/audio/speech`[^240] | Bearer | 是 |
| NVIDIA build | — | `grpc.nvcf.nvidia.com:443`（Riva gRPC）[^241] | Bearer | 否 |
| Cloudflare | — | 原生 `ai/run` 接口[^242] | API Token | TTS 不兼容 |
| Pollinations（社区服务） | — | `https://gen.pollinations.ai/v1/audio/speech`[^243] | — | 是 |

### 10.2 注意事项

- **百炼**：各地域的 API Key、域名和模型列表互相独立，不能混用[^209]。`qwen3-tts-flash` 单次最多 600 个字符[^210]，不支持复刻、设计和指令控制[^159]。
- **豆包**：试用和开通都要在控制台手动操作[^24]；旧版控制台的 AppID + Access Token 鉴权会逐步下线[^244]。
- **腾讯云**：资源包用完会停服，不会自动转后付费[^19]；`TextToVoice` 单次最多 150 个汉字[^215]。
- **MiniMax**：同步接口单次少于 1 万字符[^220]；粤语音色要把 `language_boost` 设为 `Chinese,Yue`[^220]。
- **阶跃**：单次最多 1000 个字符[^222]。
- **硅基流动**：免费模型要实名后才能用[^245]，使用自定义音色也要实名[^29]；充值支持支付宝和微信[^246]。
- **智谱**：默认加水印[^199]；单次输入最多 1024[^199]。
- **Google Cloud**：单个请求最多 5000 字节[^192]，纯中文约 1666 个字（换算）。
- **Amazon Polly**：单次最多 3000 个计费字符[^59]。
- **Fish Audio、xAI、Mistral**：默认 DNS 下连不上，见第十一节。

## 十一、国内网络连通性测试（2026-10-21）

- **方法**：在国内网络下用 curl 直连各平台的 API 地址，不走代理，返回任何 HTTP 状态码都算连通。结果只代表测试时的这一个网络环境。
- **国内平台全部能连通**：百炼、阿里 NLS、豆包、腾讯、百度、讯飞、MiniMax、阶跃、智谱、硅基流动、魔搭、华为云、Azure 中国。
- **海外能直连的**：OpenAI、Google Cloud TTS、Gemini、Azure、Amazon Polly、Edge 朗读、ElevenLabs、Cartesia、Deepgram、Inworld、Hume、MiniMax 国际站、Unreal Speech、Smallest.ai、Speechify、Murf、Rime、DeepInfra、Replicate、fal.ai、Together、Groq、Hugging Face、NVIDIA、Cloudflare、SiliconFlow 国际站、Novita、Pollinations、Puter。
- **默认 DNS 下连不上的**：Fish Audio、xAI、Mistral。默认 DNS 返回的 IP 不对，连接超时；阿里公共 DNS 的 DNS over HTTPS 返回的 IP 也连不上。改用 Cloudflare 的 DNS over HTTPS 解析出的 IP 后，三个都能连上。LMNT 连接被重置，这个服务已经关停。
- **能连通不代表允许中国大陆用户使用**：
  - OpenAI 写明在支持列表以外的地区使用可能被封号[^247]，列表里没有中国大陆和香港（推断，按列表检索）。
  - Gemini API 的可用地区也没有中国大陆和香港[^12]。
  - 反过来，豆包语音只许可在中国大陆使用[^42]。

## 十二、待确认

1. 讯飞在线合成：一次对应多少字、并发多少；免费额度是“每天 500 次”还是“1 万次礼包”，或者两者都有。
2. 华为云：按需价格的单位、有没有免费额度、声音复刻的价格。
3. 汉字计数：智谱 GLM-TTS、MiniMax 国际站，以及 OpenAI、Gemini、Polly、ElevenLabs、Cartesia 等海外厂商都没写。
4. 免费额度的具体数字：Gemini 免费层的 TTS 限速、Fish Audio `s2.1-pro-free` 的合理使用上限、Mistral 免费档、NVIDIA 试用额度，以及 MiniMax、阶跃、智谱、硅基流动的新人赠送。
5. 小米 MiMo TTS 的免费截止日期和之后的价格。
6. 豆包试用要不要实名、试用期的并发；复刻音色的新客价 110.40 元只在搜索摘要里看到。
7. 百炼 Qwen3 的指令、复刻、设计模型是否已下线：官方公告是 JS 页面，没抓到正文。
8. Speechify 自助档能不能用中文模型 `simba-3.5`；Murf 的免费额度是每月还是一次性。
9. Azure 中国（世纪互联）的开户条件，个人能否注册。
10. 魔搭 API-Inference 是否包含 TTS 模型；Kimi、百度千帆、腾讯混元、扣子、百川是否提供 TTS API，本次没查。
11. 海外平台能不能用中国大陆的银行卡、支付宝或微信付款，各家都没写。

## 附录：在 Hermes Agent 中接入

本节按 Hermes v0.22.2 的文档和源码整理。除了标“实测”的，都没有用真实 key 调用过。

**内置 provider**：Hermes 内置 11 个 TTS provider，其中 Edge TTS 是默认的，免费，不需要 key[^84]。Gemini TTS 有免费层；NeuTTS、KittenTTS、Piper 在本地运行，免费[^84]。

**本地免费引擎的中文支持**：

- NeuTTS 的语言列表里没有中文[^248]。
- KittenTTS 0.8 的预置音色是 Bella、Jasper 等 8 个[^249]，没有中文音色（推断）。
- Piper 官方音色库有 `zh_CN` 音色，例如 `zh_CN-chaowen-medium`[^250]，按 voices.json 统计共 4 个。`tts.piper.voice` 可以直接填音色名，Hermes 会自动下载[^84]。

**Edge TTS 的 403**：

- Hermes v0.22.2 把 edge-tts 锁定在 7.2.7[^251]。7.2.7 的令牌版本前缀是 `1-`[^252]，而微软 10 月起强制使用新格式[^17]。10-21 实测 Hermes 自带的 7.2.7 返回 403。
- edge-tts 7.3.1 已改为 `2-` 前缀[^18]，实测可以合成中文。可以用 `uv tool install edge-tts` 单独安装新版，再按 command provider 接入[^84]：

```yaml
tts:
  provider: edge-new
  providers:
    edge-new:
      type: command
      command: "env -u PYTHONPATH -u PYTHONHOME edge-tts --voice {voice} --file {input_path} --write-media {output_path}"
      voice: zh-CN-XiaoxiaoNeural
      output_format: mp3
      timeout: 60
```

- 建议保留命令前的 `env -u PYTHONPATH -u PYTHONHOME`：如果子进程继承了指向 Hermes 虚拟环境的 `PYTHONPATH`，单独安装的 edge-tts 会加载 Hermes 自带的 7.2.7（实测），仍然报 403。
- `edge-tts` 要在 `PATH` 里，否则写绝对路径。

**OpenAI 兼容端点**：

- OpenAI provider 的 `base_url` 可以指向任何 OpenAI 兼容的 TTS 端点[^84]。key 依次读取 `tts.openai.api_key`、`VOICE_TOOLS_OPENAI_KEY`、`OPENAI_API_KEY`[^253]。
- 以硅基流动为例，模型和音色的写法来自官方示例[^29]：

```bash
# 在 ~/.hermes/.env 里加一行 VOICE_TOOLS_OPENAI_KEY=<硅基流动的 key>，然后：
hermes config set tts.provider openai
hermes config set tts.openai.base_url https://api.siliconflow.cn/v1
hermes config set tts.openai.model FunAudioLLM/CosyVoice2-0.5B
hermes config set tts.openai.voice FunAudioLLM/CosyVoice2-0.5B:alex
```

- 阶跃：`base_url` 设为 `https://api.stepfun.com/v1`[^222]，模型 `step-tts-mini`，音色 `cixingnansheng`[^222]。
- OpenRouter、Lemonfox、Together、Groq、SiliconFlow 国际站等也可以这样接，地址见 10.1 节；DeepInfra 有内置 provider[^84]。
- Hermes 的 OpenAI 语音识别也通过同一个函数读取 key[^254][^255]。如果语音识别也用 OpenAI provider，两者会共用 `VOICE_TOOLS_OPENAI_KEY`；这时可以把 TTS 的 key 写在 `tts.openai.api_key` 里，它的优先级最高[^253]，但会明文保存在 config.yaml 中。

**MiniMax**：内置 provider，`tts.minimax.region` 设为 `cn` 时走国内站 `api.minimaxi.com`，读取 `MINIMAX_CN_API_KEY`[^84]。MiniMax 国内文档现在的默认域名是 `api.minimax.cn`[^220]，两个域名 10-21 都能连通（实测）。文档中的默认模型是 `speech-02-hd`[^84]，单价 3.5 元/万字符[^26]；改成 `speech-2.8-turbo` 是 2 元/万字符[^26]。

**Gemini**：内置 provider，文档中的默认模型是 `gemini-2.5-flash-preview-tts`[^84]，这个模型在免费层不收费[^11]。可用地区不包括中国大陆和香港，见第十一节。

**豆包**：Hermes 文档给了一个用 command provider 接入豆包 seed-tts-2.0 的例子，用的是第三方 `doubao-speech` 包[^84]，鉴权是 AppID + Access Token[^84]。火山引擎说旧版控制台的这种鉴权会逐步下线[^244]。

**command provider 的密钥**：Hermes 会清掉子进程环境里的密钥，命令需要的变量要写进 `env_passthrough`[^84]。

**自己部署的开源模型**：VoxCPM2 可以用 vLLM-Omni 提供 OpenAI 兼容的 `/v1/audio/speech`[^163]，再把 OpenAI provider 的 `base_url` 指向这个服务；命令行工具可以按 command provider 接入[^84]。

## 参考来源

文中引用的页面如下，抓取时间为 2026-10-21。

[^1]: [Euro foreign exchange reference rates (ECB)](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml)
[^2]: [Azure Speech pricing | Microsoft Azure](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services)
[^3]: [Azure AI 服务价格详情 – Azure 云计算 (azure.cn)](https://www.azure.cn/pricing/details/cognitive-services)
[^4]: [Text to speech overview - Speech service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech)
[^5]: [Text-to-Speech pricing | Google Cloud](https://cloud.google.com/text-to-speech/pricing?hl=en)
[^6]: [在线语音合成服务说明 | 讯飞开放平台文档中心](https://www.xfyun.cn/doc/tts/online_tts/tts_description.html)
[^7]: [阿里云百炼模型价格-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/model-pricing)
[^8]: [Text-to-Speech API Pricing | SpeechifyAI](https://speechify.ai/pricing)
[^9]: [Text-to-Speech API Pricing - Unreal Speech](https://unrealspeech.com/pricing)
[^10]: [Unreal Speech: Cheapest Text-to-Speech API](https://unrealspeech.com)
[^11]: [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing.md.txt)
[^12]: [Available regions for Google AI Studio and Gemini API](https://ai.google.dev/gemini-api/docs/available-regions.md.txt)
[^13]: [Pricing & Rate Limits | Fish Audio Docs](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits.md)
[^14]: [Models Overview | Fish Audio Docs](https://docs.fish.audio/developer-guide/models-pricing/models-overview.md)
[^15]: [Xiaomi MiMo Pay-As-You-Go API 定价](https://mimo.mi.com/static/docs/price/pay-as-you-go.md)
[^16]: [rany2/edge-tts README](https://raw.githubusercontent.com/rany2/edge-tts/master/README.md)
[^17]: [GitHub API edge-tts issues](https://api.github.com/repos/rany2/edge-tts/issues?state=all&per_page=30)
[^18]: [edge-tts 7.3.1 wheel (PyPI) edge_tts/constants.py](https://files.pythonhosted.org/packages/35/86/3b97d755992777d5a9ca0e45a8ec96cc9858b2d6dd8f65f3f688d60e8709/edge_tts-7.3.1-py3-none-any.whl)
[^19]: [语音合成 计费概述（在线版）_腾讯云](https://cloud.tencent.com/document/product/1073/34112)
[^20]: [智能语音交互计费项、计费单元和计费方式-智能语音交互(ISI)-阿里云帮助中心](https://help.aliyun.com/zh/isi/getting-started/pricing)
[^21]: [非开发者如何快速使用智能语音交互产品-阿里云帮助中心](https://help.aliyun.com/zh/isi/getting-started/user-guide-for-non-developers)
[^22]: [免费测试资源 - 语音技术 百度智能云](https://cloud.baidu.com/doc/SPEECH/s/Wl9mh4doe)
[^23]: [短文本在线合成API - 语音技术 百度智能云](https://cloud.baidu.com/doc/SPEECH/s/mlbxh7xie)
[^24]: [计费概述--豆包语音-火山引擎](https://www.volcengine.com/docs/DoubaoVoice/BillingOverview-15?lang=zh)
[^25]: [新人免费额度获取及用完即停开关规则-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/new-free-quota)
[^26]: [MiniMax 开放平台 定价概览](https://platform.minimaxi.com/docs/pricing/overview.md)
[^27]: [豆包语音-计费说明-文档中心-火山引擎](https://docs.volcengine.com/docs/DoubaoVoice/Billinginstructions-21?lang=zh)
[^28]: [StepFun API 定价](https://platform.stepfun.com/docs/zh/guides/pricing/details.md)
[^29]: [硅基流动 语音合成使用指南](https://api-docs.siliconflow.cn/docs/userguide/capabilities/text-to-speech)
[^30]: [Best Text-to-Speech Models - OpenRouter](https://openrouter.ai/collections/text-to-speech-models)
[^31]: [Models | Machine Learning Inference | DeepInfra (text-to-speech)](https://deepinfra.com/models/text-to-speech)
[^32]: [jaaari/kokoro-82m – Replicate](https://replicate.com/jaaari/kokoro-82m)
[^33]: [声音复刻-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)
[^34]: [智谱 API 定价](https://docs.bigmodel.cn/cn/guide/start/pricing.md)
[^35]: [大模型声音复刻 - 语音技术 百度智能云](https://cloud.baidu.com/doc/SPEECH/s/vm9sbp4z9)
[^36]: [Is my data used to improve ElevenLabs' AI models? | ElevenLabs](https://elevenlabs.io/docs/help-center/legal/is-my-data-used-to-improve-eleven-labs-ai-models.md)
[^37]: [Amazon Polly FAQs](https://aws.amazon.com/polly/faqs)
[^38]: [Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data.md)
[^39]: [Data logging | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs/data-logging?hl=en)
[^40]: [Data, privacy, and security for text to speech | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security)
[^41]: [合规资质与隐私说明-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/privacy-notice)
[^42]: [生成式模型服务专用条款--豆包语音-火山引擎](https://docs.volcengine.com/docs/DoubaoVoice/Generativemodelservicespecificterms-1?lang=zh)
[^43]: [Text to speech | OpenAI API](https://developers.openai.com/api/docs/guides/text-to-speech.md)
[^44]: [Text-to-Speech (TTS) | Hume API Docs](https://dev.hume.ai/voice/docs/text-to-speech-tts/overview.md)
[^45]: [Meta acquires voice startup Play AI | TechCrunch](https://techcrunch.com/2025/07/13/meta-acquires-voice-startup-play-ai)
[^46]: [Migrate from PlayHT to Inworld Realtime TTS After Shutdown (third-party, competitor)](https://inworld.ai/resources/migrate-from-playht)
[^47]: [Fun-CosyVoice3-0.5B-2512 model card README](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512/raw/main/README.md)
[^48]: [Qwen3-TTS-12Hz-1.7B-Base model card README](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base/raw/main/README.md)
[^49]: [VoxCPM2 model card README](https://huggingface.co/openbmb/VoxCPM2/raw/main/README.md)
[^50]: [F5-TTS GitHub README](https://raw.githubusercontent.com/SWivid/F5-TTS/main/README.md)
[^51]: [Spark-TTS-0.5B model card README](https://huggingface.co/SparkAudio/Spark-TTS-0.5B/raw/main/README.md)
[^52]: [coqui/XTTS-v2 LICENSE.txt (CPML 1.0.0)](https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt)
[^53]: [阿里云语音合成接口说明-智能语音交互(ISI)-阿里云帮助中心](https://help.aliyun.com/zh/isi/developer-reference/overview-of-speech-synthesis)
[^54]: [语音合成 常见问题_腾讯云](https://cloud.tencent.com/document/product/1073/34090)
[^55]: [长文本在线合成API - 语音技术 百度智能云](https://cloud.baidu.com/doc/SPEECH/s/ulbxh8rbu)
[^56]: [超拟人语音合成API文档 | 讯飞开放平台文档中心](https://www.xfyun.cn/doc/spark/super%20smart-tts.html)
[^57]: [语音合成 - RunTts_语音合成接口_API参考_语音交互服务 SIS-华为云](https://support.huaweicloud.com/api-sis/sis_03_0111.html)
[^58]: [Text-to-speech - SiliconFlow docs (international)](https://docs.siliconflow.com/en/userguide/capabilities/text-to-speech.md)
[^59]: [Quotas in Amazon Polly - Developer Guide](https://docs.aws.amazon.com/polly/latest/dg/limits.html)
[^60]: [Speech service quotas and limits | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits)
[^61]: [Language and voice support for Azure Speech | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)
[^62]: [Supported voices and languages | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types?hl=en)
[^63]: [Rate limits | Gemini API](https://ai.google.dev/gemini-api/docs/rate-limits.md.txt)
[^64]: [Text-to-speech generation (TTS) | Gemini API](https://ai.google.dev/gemini-api/docs/speech-generation.md.txt)
[^65]: [在线语音合成_文字转语音-讯飞开放平台](https://www.xfyun.cn/services/online_tts)
[^66]: [Language Support | SpeechifyAI docs](https://docs.speechify.ai/build/guides/text-to-speech/language-support.md)
[^67]: [ElevenLabs Pricing](https://elevenlabs.io/pricing)
[^68]: [Can I publish the content I generate on the platform? | ElevenLabs](https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform.md)
[^69]: [ElevenLabs Models](https://elevenlabs.io/docs/overview/models.md)
[^70]: [Pricing: free plan, TTS, STT, and voice agents | Cartesia](https://www.cartesia.ai/pricing)
[^71]: [Sonic 3.6 | Cartesia Docs](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest.md)
[^72]: [fishaudio/s2-pro model card README](https://huggingface.co/fishaudio/s2-pro/raw/main/README.md)
[^73]: [Pricing · Cloudflare Workers AI docs](https://developers.cloudflare.com/workers-ai/platform/pricing/index.md)
[^74]: [melotts · Cloudflare Workers AI docs](https://developers.cloudflare.com/workers-ai/models/melotts/index.md)
[^75]: [NVIDIA API Catalog llms.txt (build.nvidia.com)](https://build.nvidia.com/llms.txt)
[^76]: [NVIDIA API Trial Terms of Service (PDF)](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)
[^77]: [magpie-tts-multilingual Model by NVIDIA | NVIDIA NIM](https://build.nvidia.com/nvidia/magpie-tts-multilingual)
[^78]: [magpie-tts-multilingual model card (.md) | build.nvidia.com](https://build.nvidia.com/nvidia/magpie-tts-multilingual.md)
[^79]: [Rate Limits - GroqDocs](https://console.groq.com/docs/rate-limits)
[^80]: [Text to Speech - GroqDocs](https://console.groq.com/docs/text-to-speech)
[^81]: [Xiaomi MiMo Rate Limit](https://mimo.mi.com/static/docs/api/guidance/rate-limit.md)
[^82]: [Xiaomi MiMo 语音合成（MiMo-V2.5-TTS）指南](https://mimo.mi.com/static/docs/quick-start/usage-guide/audio/speech-synthesis-v2.5.md)
[^83]: [魔搭 API-Inference使用限制（页面 meta 描述）](https://modelscope.cn/docs/model-service/API-Inference/limits)
[^84]: [Voice & TTS | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts)
[^85]: [IBM Text to Speech pricing](https://www.ibm.com/products/text-to-speech/pricing)
[^86]: [语音合成 一分钟接入服务端 API_腾讯云](https://cloud.tencent.com/document/product/1073/56640)
[^87]: [声音复刻 计费概述_腾讯云](https://cloud.tencent.com/document/product/1283/93105)
[^88]: [讯飞开放平台 免费套餐页（/free）](https://www.xfyun.cn/free)
[^89]: [超拟人语音合成_一键生成高拟真AI配音-讯飞开放平台](https://www.xfyun.cn/services/smart-tts)
[^90]: [长文本语音合成_语音合成-文字转语音-讯飞开放平台](https://www.xfyun.cn/services/online_tts_long)
[^91]: [一句话复刻_快速TTS 在线声音定制-讯飞开放平台](https://www.xfyun.cn/services/quick_tts)
[^92]: [StepFun 常见问题](https://platform.stepfun.com/docs/zh/faq/common-questions.md)
[^93]: [Free Trial and Free Tier | Google Cloud](https://docs.cloud.google.com/free/docs/free-cloud-features?hl=en)
[^94]: [创建 Azure 免费帐户或即付即用 | Microsoft Azure](https://azure.microsoft.com/zh-cn/pricing/purchase-options/azure-account)
[^95]: [Amazon Polly Pricing | AWS](https://aws.amazon.com/polly/pricing)
[^96]: [Deepgram Pricing](https://deepgram.com/pricing)
[^97]: [Voices and Languages | Deepgram Docs](https://developers.deepgram.com/docs/tts-models.md)
[^98]: [Speechmatics pricing](https://www.speechmatics.com/pricing)
[^99]: [Text to speech quickstart | Speechmatics docs](https://docs.speechmatics.com/text-to-speech/quickstart.md)
[^100]: [Rime AI Voice Pricing and Plans](https://rime.ai/pricing)
[^101]: [Smallest AI Pricing](https://smallest.ai/pricing)
[^102]: [Lightning v3.1 Pro model card](https://docs.smallest.ai/model-cards/text-to-speech/lightning-v-3-1-pro.md)
[^103]: [Pricing | Inworld AI](https://inworld.ai/pricing)
[^104]: [Language support | Inworld Docs](https://docs.inworld.ai/tts/capabilities/multilingual.md)
[^105]: [Murf pricing (API tab, JS bundle)](https://murf.ai/pricing?product=api)
[^106]: [FAQ | Murf API docs](https://murf.ai/api/docs/resources/faq.md)
[^107]: [Affordable Text-to-Speech API - Lemonfox.ai](https://www.lemonfox.ai/text-to-speech-api)
[^108]: [Text-to-Speech API - TTS | Lemonfox.ai](https://www.lemonfox.ai/apis/text-to-speech)
[^109]: [Pricing Plans - SiliconFlow | Transparent Pay-as-You-Go](https://www.siliconflow.com/pricing)
[^110]: [Billing | Hume API Docs](https://dev.hume.ai/voice/docs/resources/billing.md)
[^111]: [Step Plan 套餐与计费](https://platform.stepfun.com/docs/zh/step-plan/pricing.md)
[^112]: [Step Plan 语音模型接入](https://platform.stepfun.com/docs/zh/step-plan/integrations/audio-api.md)
[^113]: [MiniMax 文档全集 llms-full.txt](https://platform.minimaxi.com/docs/llms-full.txt)
[^114]: [MiniMax M Plan 概览](https://platform.minimaxi.com/docs/token-plan/intro.md)
[^115]: [MiniMax M Plan 常见问题](https://platform.minimaxi.com/docs/m-plan/faq.md)
[^116]: [Xiaomi MiMo Token Plan](https://mimo.mi.com/static/docs/price/token-plan.md)
[^117]: [MiniMax Pricing Overview (minimax.io)](https://platform.minimax.io/docs/pricing/overview.md)
[^118]: [Pricing & Plans - Fish Audio](https://fish.audio/plan)
[^119]: [华为云价格计算器 API（SIS 语音合成 SKU）](https://portal.huaweicloud.com/api/calculator/rest/cbc/portalcalculatornodeservice/v4/api/productInfo?urlPath=sis&tag=general.online.portal&region=cn-north-4&tab=calc&sign=common)
[^120]: [语音合成 - 语音技术 百度智能云](https://cloud.baidu.com/doc/SPEECH/s/Ql9misjot)
[^121]: [智能语音交互计费方式与收费标准-阿里云帮助中心](https://help.aliyun.com/zh/isi/getting-started/billing-10)
[^122]: [硅基流动 模型价格中心](https://siliconflow.cn/pricing)
[^123]: [模型价格 | 文档中心（云知声 Token Hub）](https://maas.unisound.com/docs/price/overview)
[^124]: [Text-to-Speech - OpenRouter docs](https://openrouter.ai/docs/guides/overview/multimodal/tts.md)
[^125]: [Simple Pricing | Machine Learning Infrastructure | DeepInfra](https://deepinfra.com/pricing)
[^126]: [Available models (serverless) - Together AI Docs](https://docs.together.ai/docs/serverless/models.md)
[^127]: [Credits - Together AI Docs](https://docs.together.ai/docs/billing.md)
[^128]: [Falcon 2.1 | Murf API docs](https://murf.ai/api/docs/text-to-speech-models/falcon-2-1.md)
[^129]: [Voxtral TTS 3 | Mistral Docs](https://docs.mistral.ai/models/voxtral-mini-tts-3-0.md)
[^130]: [Languages | Mistral Docs](https://docs.mistral.ai/studio/audio/specs-and-limits/languages.md)
[^131]: [Voices | Mistral Docs](https://docs.mistral.ai/studio/audio/text-to-speech/voices.md)
[^132]: [Pricing | SpaceXSI (xAI) Docs](https://docs.x.ai/developers/pricing.md)
[^133]: [Text to Speech | SpaceXSI (xAI) Docs](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech.md)
[^134]: [Pricing | OpenAI API (developers.openai.com/api/docs/pricing.md)](https://developers.openai.com/api/docs/pricing.md)
[^135]: [Inworld AI llms.txt](https://docs.inworld.ai/llms.txt)
[^136]: [Available voices - Amazon Polly](https://docs.aws.amazon.com/polly/latest/dg/available-voices.html)
[^137]: [Azure Retail Prices API (productName 'Azure Speech', eastus)](https://prices.azure.com/api/retail/prices?$filter=productName%20eq%20%27Azure%20Speech%27%20and%20armRegionName%20eq%20%27eastus%27)
[^138]: [ElevenAPI Pricing](https://elevenlabs.io/pricing/api)
[^139]: [Supported Models - GroqDocs](https://console.groq.com/docs/models)
[^140]: [Kokoro TTS (Mandarin Chinese) llms.txt | fal](https://fal.ai/models/fal-ai/kokoro/mandarin-chinese/llms.txt)
[^141]: [Pricing: Pay-Per-Use AI Model APIs and Serverless GPUs | fal](https://fal.ai/pricing)
[^142]: [Pricing – Replicate](https://replicate.com/pricing)
[^143]: [Pricing and Billing - Hugging Face Inference Providers docs](https://huggingface.co/docs/inference-providers/pricing.md)
[^144]: [Hugging Face Hub API — text-to-speech models with inference providers](https://huggingface.co/api/models?pipeline_tag=text-to-speech&inference_provider=all&limit=50&expand%5B%5D=inferenceProviderMapping)
[^145]: [声音设计-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)
[^146]: [MiniMax 音色快速复刻指南](https://platform.minimaxi.com/docs/guides/speech-voice-clone.md)
[^147]: [MiniMax llms.txt 文档索引](https://platform.minimaxi.com/docs/llms.txt)
[^148]: [StepFun 复刻音色 API](https://platform.stepfun.com/docs/zh/api-reference/audio/create-voice.md)
[^149]: [智谱 GLM-TTS-Clone 模型介绍](https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-tts-clone.md)
[^150]: [语音合成_语音定制_文本转语音服务 - 腾讯云](https://cloud.tencent.com/product/tts)
[^151]: [产品简介--豆包语音-火山引擎](https://www.volcengine.com/docs/DoubaoVoice/ProductOverview-9?lang=zh)
[^152]: [Voice cloning: how it works](https://elevenlabs.io/docs/eleven-api/concepts/voice-cloning.md)
[^153]: [Instant Voice Clone | Cartesia Docs](https://docs.cartesia.ai/build-with-cartesia/capability-guides/clone-voices.md)
[^154]: [Instant voice cloning | Inworld Docs](https://docs.inworld.ai/tts/instant-voice-cloning.md)
[^155]: [Voice Cloning Best Practices | Fish Audio Docs](https://docs.fish.audio/developer-guide/best-practices/voice-cloning.md)
[^156]: [Voice replication | Gemini API](https://ai.google.dev/gemini-api/docs/voice-replication.md.txt)
[^157]: [Custom Voices | SpaceXSI (xAI) Docs](https://docs.x.ai/developers/model-capabilities/audio/custom-voices.md)
[^158]: [Custom voices | OpenAI API](https://developers.openai.com/api/docs/guides/custom-voices.md)
[^159]: [语音合成-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/tts-model)
[^160]: [音色列表 - 语音技术 百度智能云](https://cloud.baidu.com/doc/SPEECH/s/Rluv3uq3d)
[^161]: [CosyVoice GitHub README](https://raw.githubusercontent.com/FunAudioLLM/CosyVoice/main/README.md)
[^162]: [Qwen3-TTS GitHub README](https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/README.md)
[^163]: [VoxCPM GitHub README](https://raw.githubusercontent.com/OpenBMB/VoxCPM/main/README.md)
[^164]: [MOSS-TTSD-v1.0 model card README](https://huggingface.co/OpenMOSS-Team/MOSS-TTSD-v1.0/raw/main/README.md)
[^165]: [FireRedTTS2 model card README](https://huggingface.co/FireRedTeam/FireRedTTS2/raw/main/README.md)
[^166]: [FireRedTTS2 GitHub README](https://raw.githubusercontent.com/FireRedTeam/FireRedTTS2/main/README.md)
[^167]: [SoulX-Podcast-1.7B model card README](https://huggingface.co/Soul-AILab/SoulX-Podcast-1.7B/raw/main/README.md)
[^168]: [SoulX-Podcast GitHub readme](https://raw.githubusercontent.com/Soul-AILab/SoulX-Podcast/main/readme.md)
[^169]: [Step-Audio-TTS-3B model card README](https://huggingface.co/stepfun-ai/Step-Audio-TTS-3B/raw/main/README.md)
[^170]: [GitHub API repos/RVC-Boss/GPT-SoVITS](https://api.github.com/repos/RVC-Boss/GPT-SoVITS)
[^171]: [lj1995/GPT-SoVITS model card README](https://huggingface.co/lj1995/GPT-SoVITS/raw/main/README.md)
[^172]: [GPT-SoVITS GitHub README](https://raw.githubusercontent.com/RVC-Boss/GPT-SoVITS/main/README.md)
[^173]: [inclusionAI/Ming-3.0-tts-0.5B model card README](https://huggingface.co/inclusionAI/Ming-3.0-tts-0.5B/raw/main/README.md)
[^174]: [zai-org/GLM-TTS model card README](https://huggingface.co/zai-org/GLM-TTS/raw/main/README.md)
[^175]: [GitHub API repos/zai-org/GLM-TTS](https://api.github.com/repos/zai-org/GLM-TTS)
[^176]: [zai-org/GLM-TTS GitHub README](https://raw.githubusercontent.com/zai-org/GLM-TTS/main/README.md)
[^177]: [hexgrad/Kokoro-82M model card README](https://huggingface.co/hexgrad/Kokoro-82M/raw/main/README.md)
[^178]: [hexgrad/Kokoro-82M VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/raw/main/VOICES.md)
[^179]: [ResembleAI/chatterbox model card README](https://huggingface.co/ResembleAI/chatterbox/raw/main/README.md)
[^180]: [HF API models/Zyphra/Zonos-v0.1-transformer](https://huggingface.co/api/models/Zyphra/Zonos-v0.1-transformer)
[^181]: [Zyphra/Zonos GitHub README](https://raw.githubusercontent.com/Zyphra/Zonos/main/README.md)
[^182]: [index-tts LICENSE (bilibili Model Use License Agreement)](https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE)
[^183]: [Higgs TTS 2 LICENSE](https://huggingface.co/bosonai/higgs-tts-2-3b-base/raw/main/LICENSE)
[^184]: [fish-speech LICENSE (Fish Audio Community License)](https://raw.githubusercontent.com/fishaudio/fish-speech/main/LICENSE)
[^185]: [amphion/MaskGCT model card README](https://huggingface.co/amphion/MaskGCT/raw/main/README.md)
[^186]: [2noise/ChatTTS GitHub README](https://raw.githubusercontent.com/2noise/ChatTTS/main/README.md)
[^187]: [coqui-ai/TTS Discussion #3489](https://github.com/coqui-ai/TTS/discussions/3489)
[^188]: [MegaTTS3 model card README](https://huggingface.co/ByteDance/MegaTTS3/raw/main/README.md)
[^189]: [microsoft/VibeVoice GitHub README](https://raw.githubusercontent.com/microsoft/VibeVoice/main/README.md)
[^190]: [GitHub API repos/rhasspy/piper](https://api.github.com/repos/rhasspy/piper)
[^191]: [GitHub API repos/OHF-Voice/piper1-gpl](https://api.github.com/repos/OHF-Voice/piper1-gpl)
[^192]: [Quotas & limits | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/quotas?hl=en)
[^193]: [Gemini API Additional Terms of Service](https://ai.google.dev/gemini-api/terms.md.txt)
[^194]: [Security FAQ | SpaceXSI (xAI) Docs](https://docs.x.ai/developers/faq/security.md)
[^195]: [Zero data retention | Mistral Docs](https://docs.mistral.ai/admin/monitor-comply/zero-data-retention.md)
[^196]: [Text-to-Speech API FAQ | Hume](https://dev.hume.ai/voice/docs/text-to-speech-tts/faq.md)
[^197]: [Data Privacy - DeepInfra docs](https://docs.deepinfra.com/account/data-privacy.md)
[^198]: [华为云语音交互服务（SIS）服务声明](https://www.huaweicloud.com/declaration/sis.html)
[^199]: [智谱 文本转语音 API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%9C%AC%E8%BD%AC%E8%AF%AD%E9%9F%B3.md)
[^200]: [StepFun 音频合成最佳实践](https://platform.stepfun.com/docs/zh/guides/developer/tts.md)
[^201]: [Deprecations | OpenAI API](https://developers.openai.com/api/docs/deprecations.md)
[^202]: [Model Deprecation - GroqDocs](https://console.groq.com/docs/deprecations)
[^203]: [LMNT has shut down](https://www.lmnt.com)
[^204]: [Product Notice | Resemble AI](https://www.resemble.ai/product-notice)
[^205]: [TTS models | Inworld Docs](https://docs.inworld.ai/tts/tts-models.md)
[^206]: [Model Deprecations | Fish Audio Docs](https://docs.fish.audio/developer-guide/models-pricing/deprecations.md)
[^207]: [Remove Arcana model IDs | Rime docs](https://docs.rime.ai/docs/migrate-arcana-to-coda.md)
[^208]: [Gemini 3.1 Flash TTS Preview | Gemini API](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview.md.txt)
[^209]: [获取与配置阿里云百炼 API Key-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/get-api-key)
[^210]: [非实时语音合成（Qwen-TTS）API参考-大模型服务平台百炼-阿里云](https://help.aliyun.com/zh/model-studio/qwen-tts-api)
[^211]: [非实时语音合成-大模型服务平台百炼(Model Studio)-阿里云帮助中心](https://help.aliyun.com/zh/model-studio/qwen-tts)
[^212]: [API Key使用--豆包语音-火山引擎](https://docs.volcengine.com/docs/DoubaoVoice/APIKeyUsage?lang=zh)
[^213]: [单向流式语音合成(HTTP)--豆包语音-火山引擎](https://docs.volcengine.com/docs/DoubaoVoice/unidirectional-streaming-text-to-speech-http?lang=zh)
[^214]: [语音合成 实时语音合成_腾讯云](https://cloud.tencent.com/document/api/1073/94308)
[^215]: [语音合成 基础语音合成_腾讯云](https://cloud.tencent.com/document/product/1073/37995)
[^216]: [语音合成 签名方法_腾讯云](https://cloud.tencent.com/document/api/1073/37991)
[^217]: [鉴权认证 - 语音技术 百度智能云](https://cloud.baidu.com/doc/SPEECH/s/Em8snejw1)
[^218]: [在线语音合成API文档 | 讯飞开放平台文档中心](https://www.xfyun.cn/doc/tts/online_tts/API.html)
[^219]: [MiniMax FAQ 接口相关](https://platform.minimaxi.com/docs/faq/about-apis.md)
[^220]: [MiniMax 同步语音合成 HTTP API](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http.md)
[^221]: [StepFun 快速开始](https://platform.stepfun.com/docs/zh/quickstart/overview.md)
[^222]: [StepFun 语音合成 API](https://platform.stepfun.com/docs/zh/api-reference/audio/create-audio.md)
[^223]: [StepFun 流式语音合成](https://platform.stepfun.com/docs/zh/api-reference/audio/ws-audio.md)
[^224]: [智谱 快速开始](https://docs.bigmodel.cn/cn/guide/start/quick-start.md)
[^225]: [硅基流动 快速上手](https://api-docs.siliconflow.cn/docs/userguide/quickstart)
[^226]: [SiliconFlow Create a Speech API](https://api-docs.siliconflow.cn/docs/api/audio-speech-post)
[^227]: [Xiaomi MiMo 语音合成 API（OpenAI 兼容）](https://mimo.mi.com/static/docs/api/audio/tts.md)
[^228]: [文本转语音 API 参考 (REST) - 语音服务 (docs.azure.cn)](https://docs.azure.cn/zh-cn/ai-services/speech-service/rest-text-to-speech)
[^229]: [Text to speech REST API | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech)
[^230]: [Gemini-TTS | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts?hl=en)
[^231]: [Billing | Gemini API](https://ai.google.dev/gemini-api/docs/billing.md.txt)
[^232]: [Create speech | ElevenLabs API reference](https://elevenlabs.io/docs/api-reference/text-to-speech/convert.md)
[^233]: [ElevenLabs API reference: Authentication](https://elevenlabs.io/docs/api-reference/authentication.md)
[^234]: [API Conventions | Cartesia Docs](https://docs.cartesia.ai/use-the-api/api-conventions.md)
[^235]: [Text to Speech | Fish Audio API reference](https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech.md)
[^236]: [Speech generation | Mistral Docs](https://docs.mistral.ai/studio/audio/text-to-speech/generate-speech.md)
[^237]: [Text-to-Speech API | SpeechifyAI docs](https://docs.speechify.ai/build/text-to-speech-api.md)
[^238]: [Openai Audio Speech - DeepInfra (OpenAPI)](https://docs.deepinfra.com/api-reference/audio/openai-audio-speech.md)
[^239]: [Generate speech - Together AI Docs](https://docs.together.ai/docs/text-to-speech.md)
[^240]: [Create speech - SiliconFlow API reference (international)](https://docs.siliconflow.com/en/api-reference/audio/create-speech.md)
[^241]: [nvidia/magpie_tts_multilingual_357m · Hugging Face (NVIDIA model card)](https://huggingface.co/nvidia/magpie_tts_multilingual_357m)
[^242]: [OpenAI compatible API endpoints · Cloudflare Workers AI docs](https://developers.cloudflare.com/workers-ai/configuration/open-ai-compatibility/index.md)
[^243]: [Pollinations API docs (enter.pollinations.ai llm.txt)](https://enter.pollinations.ai/api/docs/llm.txt)
[^244]: [旧版控制台鉴权参考--豆包语音-火山引擎](https://docs.volcengine.com/docs/6561/2534847?lang=zh)
[^245]: [硅基流动 Rate Limits](https://api-docs.siliconflow.cn/docs/userguide/faqs/rate-limit-and-upgradation)
[^246]: [硅基流动 财务相关](https://api-docs.siliconflow.cn/docs/userguide/faqs/misc_finance)
[^247]: [Supported countries and territories | OpenAI API](https://developers.openai.com/api/docs/supported-countries.md)
[^248]: [neuphonic/neutts GitHub README](https://raw.githubusercontent.com/neuphonic/neutts/main/README.md)
[^249]: [KittenML/kitten-tts-mini-0.8 model card README](https://huggingface.co/KittenML/kitten-tts-mini-0.8/raw/main/README.md)
[^250]: [rhasspy/piper-voices voices.json](https://huggingface.co/rhasspy/piper-voices/raw/main/voices.json)
[^251]: [hermes-agent v0.22.2 pyproject.toml](https://raw.githubusercontent.com/NousResearch/hermes-agent/v0.22.2/pyproject.toml)
[^252]: [edge-tts 7.2.7 wheel (PyPI) edge_tts/constants.py](https://files.pythonhosted.org/packages/bf/89/92ac6b154ab87d236c15e5e0c73cb99be58efb1ea3eb9318c266bf9a36bf/edge_tts-7.2.7-py3-none-any.whl)
[^253]: [hermes-agent v0.22.2 tools/tts_tool_openai.py](https://raw.githubusercontent.com/NousResearch/hermes-agent/v0.22.2/tools/tts_tool_openai.py)
[^254]: [hermes-agent v0.22.2 tools/transcription_cloud.py](https://raw.githubusercontent.com/NousResearch/hermes-agent/v0.22.2/tools/transcription_cloud.py)
[^255]: [hermes-agent v0.22.2 tools/tool_backend_helpers.py](https://raw.githubusercontent.com/NousResearch/hermes-agent/v0.22.2/tools/tool_backend_helpers.py)
[^256]: [Step-Audio GitHub README](https://raw.githubusercontent.com/stepfun-ai/Step-Audio/main/README.md)
