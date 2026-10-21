# 免费与低价文生图调研：网页 App、API、本地软件与合规

中文 | [English](./Free-and-Low-Cost-Text-to-Image_en.md)

- **调研日期**: 2026-10-21（价格和额度抓取于 2026-10-20 至 10-21）
- **范围**: 国内外免费或低价的文生图服务，包括网页和 App 的免费额度与会员档位、免费 API 和调用示例、新用户赠送、按张计费的付费 API、开源本地软件、Draw Things 云端免费版、开源模型的许可证，以及在国内上线要满足的标识和备案要求。
- **依据**: 数据来自官方页面，包括价格页、文档、条款、公告、官方接口和开源仓库；官方没公布的，用媒体、评测或用户反馈补充，并标“（第三方）”。句末的上标数字是引用，对应文末的参考来源。标“（实测）”的是 2026-10-20 至 10-21 实际操作、调用或连通测试的结果；标“（换算）”的是按官方单价或汇率算出来的；标“（推断）”的是根据所引资料作出的推断。
- **实测环境**: 中国大陆网络。表格里的“直连”指不走代理：✓ 能连；✗ 连不上，一般要走代理；403 是连得上但被网站拒绝。
- **单位**: 价格是官方原价，不含限时折扣。美元按 1 USD ≈ 6.69 元换算（2026-10-21 汇率）[^1]。
- **时效**: 免费额度、会员权益和价格变化很快，付费前请以官网为准。

## 先看这里：按需求选

| 需求 | 先试这些 | 说明 |
| --- | --- | --- |
| 不写代码，国内免费出图 | 通义万相网页版[^2]、即梦[^3]、豆包[^4]、腾讯元宝[^5]、文心助手[^6] | 都能直连；元宝明确说暂无收费计划，其余的每天免费几次大多没公布 |
| 想免费用开源大模型（Qwen-Image、Z-Image 等） | 魔搭 AIGC 专区[^7][^8]、LiblibAI[^9] | 每天登录送魔粒 / 积分 |
| Mac / iPhone 用户 | Draw Things 云端免费版[^10][^11] | 本机跑不动的大模型放到官方服务器上跑，见第 10 节 |
| 免费 API，国内厂商 | 智谱 CogView-3-Flash[^12]、硅基流动 Kolors[^13]、魔搭 API-Inference[^14]、商汤 SenseNova U1.5 Lite（公测期）[^15] | 都能直连，见第 4 节 |
| 免费 API，海外但国内能直连 | Cloudflare Workers AI[^16]、Agnes AI（限时 \$0）[^17]、Pollinations 旧接口（实测） | Cloudflare 每天约 173 张 FLUX.1 schnell（换算） |
| 国内最便宜的付费 API | MiniMax image-01 0.025 元[^18]、智谱 CogView-4 Batch 0.03 元[^19]、通义万相 wanx2.0-t2i-turbo 0.04 元[^20]、百度 musesteamer-air-image 0.05 元[^21] | 都是每张的价格 |
| 画质和价格兼顾（国内） | 豆包 Seedream 5.0 flash 0.12 元[^22] | 官方说能力和 5.0 pro 完全一致，只是更快更便宜[^23] |
| 海外最便宜的付费 API | Prodia FLUX.2 Klein 4B \$0.0005[^24]、Runware FLUX.2 [klein] 4B \$0.0006[^25] | 约 0.003–0.004 元/张（换算） |
| 要商用、想自己部署 | Z-Image-Turbo、FLUX.2 [klein] 4B、ERNIE-Image、Qwen-Image-2512，都是 Apache 2.0[^26] | 见第 11 节 |
| 在国内给公众提供生图功能 | 调用已备案模型的 API，到属地网信办登记，图上加 AI 标识[^27][^28] | 见第 12 节 |

## 1. 品牌 ↔ API 模型对照

App 里的品牌名和 API 文档里的模型名常常对不上，按品牌查这张表。

| 品牌 | 厂商 | API 模型 ID | 在哪调用 |
| --- | --- | --- | --- |
| 通义万相 | 阿里 | wan2.6-t2i、wan2.5-t2i-preview、wan2.2-t2i-flash / plus、wanx2.1-t2i-turbo / plus、wanx2.0-t2i-turbo、wanx-v1；生成与编辑 wan2.7-image / pro、wan2.6-image[^20] | 阿里云百炼；Together 也有 Wan 2.6 Image[^29] |
| 千问（App 生图） | 阿里 | qwen-image-3.0 / pro、qwen-image-2.1-pro / turbo、qwen-image-2.0 / pro[^20] | 百炼；硅基流动[^30]、千帆[^21]、优云智算[^31]、Runware[^32]、Together[^29]也有 Qwen-Image |
| Z-Image（开源） | 阿里通义实验室 | z-image-turbo[^20] | 百炼、硅基流动[^33]、fal[^34]、Runware[^35]、WaveSpeed[^36]、Pollinations[^37] |
| 豆包 / 即梦 | 字节跳动 | doubao-seedream-5-0-pro / flash / lite、4-5、4-0[^22]；即梦 API 文生图 3.0 / 3.1、图片生成 4.0 / 4.6[^38] | 火山方舟、火山引擎；七牛[^39]、TokenHub[^40]、优云智算[^31]、OpenRouter[^41]也转售 |
| 可灵 | 快手 | Kling Image 2.1、3.0、3.0-omni、O1[^42] | 可灵开放平台（国际版另有美元价[^43]）；百炼[^20]、TokenHub、七牛也转售 |
| 可图 Kolors（开源） | 快手 | Kwai-Kolors/Kolors[^44] | 硅基流动限免[^13] |
| 混元（元宝里的生图） | 腾讯 | Hy-Image-3.5-preview、Hy-Image-3.0[^40] | 腾讯云 TokenHub（元宝已接入混元图像 3.5[^45]） |
| 蒸汽机 | 百度 | musesteamer-air-image[^21]、qianfan-image（文档标"内部使用"）[^46] | 百度千帆；文心助手生图用的模型没公布 |
| 文心 ERNIE-Image（开源） | 百度 | ERNIE-Image、ERNIE-Image-Turbo | Apache 2.0，可本地跑[^26]；硅基流动已下线[^13] |
| 智谱 | 智谱 | CogView-3-Flash（免费）、CogView-4、GLM-Image[^19] | 智谱开放平台；国际站 Z.ai[^47] |
| 海螺 | MiniMax | image-01、image-01-live[^18] | MiniMax 开放平台（国际站[^48]） |
| 商汤 | 商汤 | sensenova-u1.5-lite、sensenova-u1.5-fast[^49] | SenseNova 平台 |
| Vidu | 生数科技 | vidu/viduq2-fast_reference2image 等（参考生图）[^20]；Vidu-Image-q2（文生图）[^40] | 百炼、TokenHub |
| Nano Banana（Gemini 生图） | Google | gemini-nano-banana-2.1、gemini-3.1-flash-image（Nano Banana 2）、gemini-3.1-flash-lite-image（Nano Banana 2 Lite）[^50] | Gemini API；七牛也上架了 gemini-2.5-flash-image[^51] |
| GPT Image | OpenAI | gpt-image-2.5-flare、gpt-image-2，旧的 GPT Image 1 / 1.5 / 1 Mini[^52] | OpenAI API |
| Grok Imagine | xAI | grok-imagine-image、grok-imagine-image-2.0[^53][^54] | xAI API |
| MAI-Image | 微软 | MAI-Image-2.6、MAI-Image-2.6-Flash[^55]；Bing 改图用 MAI-Image-2.5-Flash[^56] | Microsoft Foundry（要有绑了有效付款方式的 Azure 订阅[^57]） |
| FLUX | Black Forest Labs | FLUX 3 Image、FLUX 3 Klein、FLUX.2 [klein] 4B / 9B[^58]、FLUX.2 [pro] / [flex] / [max] 等[^59] | BFL API；Runware、fal、Prodia、Cloudflare 等托管 |

## 2. 国内免费网页 / App

下面这些国内网站直连都能通（实测）。

### 2.1 通义万相网页版

- **入口**：tongyi.aliyun.com/wan/，定价页在 /wan/pricing。
- **会员档位**[^2]：

| 档位 | 价格 | 灵感值 | 同时提交 | 其他权益 |
| --- | --- | --- | --- | --- |
| 免费 | ￥0 | 每日签到获赠（数量没写） | 1 个图片任务、1 个视频任务 | 6 个文生图风格模板 |
| 标准会员 | 标价 ￥72/月；连续包年 5 折，等价 ￥36/月；连续包月标 6.5 折 | 300/月，"最多加速生成1200张图片或60个视频" | 3 个图片、3 个视频任务 | 去品牌水印、1080p 视频、10–30 秒视频、全部风格模板 |
| 高级会员 | 标价 ￥288/月；连续包年等价 ￥145/月 | 1200/月，最多加速 4800 张图或 240 个视频 | 5 个图片、8 个视频任务 | 同标准会员 |

- 灵感值的用途是"加速图片与视频生成"[^2]。免费档列了"同时提交1个图片任务"，所以不花灵感值也能出图，只是不加速（推断）。按 300 灵感值加速 1200 张算，每张约 0.25 灵感值（换算）。
- "图片、视频去品牌水印"只列在会员权益里[^2]，所以免费档出的图应该带品牌水印（推断）。
- 会员自动续费，可以随时取消，但一经支付不退款[^2]。
- 会员只能在 tongyi.aliyun.com/wan 网页上用，API 要另外买[^2]。API 见 6.1 节。

### 2.2 千问 App / 网页

- **入口**：qianwen.com 和千问 App。
- **生图免费吗**：2025-12 新浪科技实测，千问生图"直接拉满免费不限次"，用的是"特供满血版 Qwen-Image 2511"[^60]。现在每天给多少，官方没公布，也没找到更新的报道。
- **2026-08 开始收费的部分**[^61]：
  - 办公助理专业会员：高级 19 元/月（年付 200 元）、精英 49 元/月、旗舰 128 元/月；
  - 视频生成每天 10 个免费额度，超出按包买：26 元 10 个、116 元 50 个、228 元 100 个。
- **App Store 内购**[^62]：创作会员 7 天 ¥10；创作积分 200 个 ¥20、500 个 ¥50；"千问创作-标准会员"连续包月 ¥58，另有一档 ¥48。

### 2.3 即梦 AI

- **入口**：jimeng.jianying.com 和即梦 App。
- **免费积分**：每天登录送，到期清零[^3]。
- 送多少一直在变，下面是第三方汇总的用户反馈[^3]：
  - 8 月上旬每天随机 66–100；
  - 之后陆续有人反映每天只给 20、30；
  - 到 9 月降到 10–30；
  - 客服的说法是"这些是惊喜积分，随机的"。
- **会员**：基础会员每月 725 积分，渠道口径最多约 2900 张图或 72 个视频，折合每张图约 0.25 积分（第三方，未经官方核实）[^63]。基础会员的价格，有网友 8 月开通时付了 41 元[^63]。
- 视频很贵：Seedance 2.5 每秒约 26–29 积分（第三方）[^63]。只出图的话，会员积分比较宽裕。
- 即梦的 API 在火山引擎单独计费，见 6.3 节。

### 2.4 豆包

- **入口**：doubao.com 和豆包 App。
- 生图模型是 Seedream 5.0，支持文生图和图生图[^4]。
- 免费版能用 AI 生图、视频，"不过有额度限制"，次数没公布[^4]。
- 2026-06 推出了付费套餐[^64]：
  - 标准套餐连续包月 68 元，学生认证后 38 元，额度是免费版的 5 倍以上；
  - 加强套餐 200 元、高级套餐 500 元，额度分别是标准套餐的 4 倍和 10 倍。

### 2.5 腾讯元宝

- **入口**：yuanbao.tencent.com 和元宝 App。
- 腾讯回应媒体："元宝目前完全免费使用，暂无收费计划"[^5]。
- 生图用的是混元图像 3.5，Hy Image 3.5 preview 在元宝里灰度测试了约两个月[^45]。
- 普通用户可以在元宝里免费用人像编辑、智能 P 图、旅游规划图、知识信息图；企业和开发者通过腾讯云 API 调用[^45]。API 见 6.5 节。

### 2.6 文心助手（原文心一言）

- **入口**：wenxin.baidu.com。旧的文心一格 yige.baidu.com 现在也跳到这里（实测）。
- 百度把文心一言 Web 端、文心、文心助手合并成文心助手，价格策略"继续免费"[^6]。
- 首页有"图片生成"入口[^65]。
- 文心一言 2025-02-13 起已全面免费，2026-06-25 起官网提问入口升级[^66]。
- 生图用的是哪个模型、每天能生几次，官方没写。

### 2.7 可灵 AI（国内版）

- **入口**：klingai.com、app.klingai.com。
- **会员档位**[^67]（黄金、铂金、钻石的新客都有 7 天 3 折试用）：

| 档位 | 7 天试用 | 试用之后 | 灵感值 / 月 | 100 灵感值折合 |
| --- | --- | --- | --- | --- |
| 黄金 | ¥5.99 | 首月 46 元，之后 58 元/月 | 660 | ¥6.97 |
| 铂金 | ¥11.99 | 首月 186 元，之后 234 元/月 | 3,000 | ¥6.20 |
| 钻石 | ¥17.99 | 首月 466 元，之后 586 元/月 | 8,000 | ¥5.83 |
| 黑金 | 无试用；首月 ¥916（首购 7 折） | 之后 1,149 元/月 | 26,000 | ¥3.52 |

- 各档会员都有：每日送会员灵感值、不限并发、专享快速通道、1080p/4K 视频、作品去品牌水印、生成内容可商用[^67]。
- **免费用户**：会员页没写每天送多少。第三方 8 月的说法是非会员每天登录送 66 灵感值，而且服务条款写明免费档产出不可商用[^68]。
- 单独买灵感值是 1 元 10 个，不退款（第三方）[^69]。
- 出一张图扣多少灵感值，没找到官方数字。

### 2.8 智谱清言

- **入口**：chatglm.cn。没注册过的手机号登录时会自动注册[^70]。
- 每天首次打开领积分。双节期间（9-25 至 10-07）积分翻 10 倍：普通用户 2000、VIP 4000、SVIP 8000，24 小时过期[^70]。按这个推算，平日约 200 / 400 / 800（换算）。
- 10-08 至 10-31 还有返还活动：双节花掉的积分 100% 返还，领取后 30 天有效[^70]。
- 生一张图扣多少积分没公布。

### 2.9 LiblibAI（哩布哩布）

- **入口**：liblib.art，社区模型站，能选社区模型和 LoRA。
- 免费用户登录每天送 20 积分，云端存储 3GB[^9]。
- 入门版 ¥429/年，每月 700 积分，最多约 2800 张图或 87 个视频[^9]。订阅积分每 31 天重置[^9]。
- 按"700 积分最多约 2800 张"的口径，每天 20 积分最多约 80 张（换算）。换大模型或高分辨率会少很多。

### 2.10 魔搭 AIGC 专区

- **入口**：modelscope.cn/aigc，阿里的开源模型社区。能在线用 Qwen Image 2512、Z Image、Qwen Edit 2511 等开源模型[^8]。
- **魔粒怎么拿**：
  - 10-20 构建的官方文档写的是：每天登录送 200 魔粒，绑定阿里云账号再加 50[^7]。
  - 官方 8 月的文章写的是绑定后每天 150[^8]。两处不一致，以较新的文档为准。
  - 每天提交作品最多再拿 200，点赞评论最多 50[^8]。
  - 短期魔粒 24 小时有效，长期魔粒 90 天[^7]。
  - 用魔粒之前要完善个人信息，包括验证过的个人邮箱[^7]。
- **怎么扣**：生图每张 1–2 魔粒，视频每个 8–28 魔粒，LoRA 训练按数据量和模型动态计算[^8]。每天 250 魔粒约够 125–250 张图（换算）。
- 魔粒和 API-Inference 共用[^7]。API 见 4.3 节。

### 2.11 海螺 AI

- **入口**：hailuoai.com，MiniMax 旗下。
- 国内版每天自动发 100 贝壳，不累计，生成失败不退（第三方）[^71]。贝壳主要按视频规格扣，图片每张扣多少没公布。
- 3 月有过活动：3 月 4 日前开通标准档以上年卡的，一年内用 Seedream 5.0 Lite、全能图片 pro、悠船 V7 等模型生图不扣积分[^72]。

### 2.12 其他国内平台（免费额度大多没公布）

| 产品 | 已知信息 |
| --- | --- |
| 讯飞星火 | 对话框里输入"画一张…"就能生成[^73]；第三方称注册后每天 100 次免费、每次最多 4 张，付费 29 元/月 1000 次、99 元/月 5000 次[^74] |
| 美图 WHEE | 新用户送 20 美豆，单张约 2 美豆；会员连续包月 52 元、包季 142 元、包年 462 元，每月 1800 美豆（第三方）[^75]；会员赠送的美豆当月有效，过期作废[^76] |
| 吐司 Tusi | 免费版每天 100 算力，排队任务 1 个，每次最多 2 张（第三方，2025 年资料）[^77]；App 连续包月 24.8 元[^78] |
| 纳米 AI（360） | "一句话生成图片"；内购 100 纳米 ¥10，连续包月 VIP ¥49[^79] |
| 堆友（阿里） | 有"经典生图"功能[^80]，免费额度没公布 |
| 商汤秒画 | 用的是 Artist v1.0 Alpha 模型[^81]；第三方称官网首页写着"AI作画，免费"[^82] |
| 天工 AI | App 能做 PPT、文档、表格、图片和视频；内购 Basic 连续包月 ¥45[^83] |
| 夸克 | App 搜索框上方有"图像生成"入口[^84] |
| 美图设计室 | 偏电商和海报设计；VIP 连续包月 ¥30[^85] |
| WPS 灵犀 | 侧边栏有"AI 文生图"[^86] |

### 2.13 已停服

- **星流 AI**：2026-10-10 24:00 停止运营[^87]。官方短信建议迁移到 Lovart；每个账号只能迁移一次，原平台停服后内容彻底删除、不能恢复[^88]。
- **快手可图网页版**：2024-08-23 已关闭[^89]。Kolors 模型现在还能在硅基流动免费调用[^13]。

## 3. 海外免费网页 / App

| 产品 | 免费额度 | 限制 / 商用 | 付费起价 | 直连 |
| --- | --- | --- | --- | --- |
| Bing Image Creator | 每天 15 次快速生成，用完转标准速度，24 小时最多 200 个提示词[^56] | 要个人微软账户，工作/学校的 Entra ID 账户不能用；改图一律用 MAI-Image-2.5-Flash[^56] | 免费 | ✗（跳到 cn.bing.com 后 404） |
| Microsoft Designer | 每月初发一批积分，每次用 AI 扣 1 个，免费账户给多少没写[^90] | 每张图都自动 boost[^90] | — | ✓ |
| ChatGPT 免费版 | "Limited image creation"[^91] | 生图和文字聊天分开限额[^92] | — | 403 |
| Gemini App | 不订阅是"Standard limits"，每 5 小时刷新，另有周上限[^93] | 生成图片视频更耗额度[^93]；不订阅只能下载 1K，订阅 2K[^94] | — | ✗ |
| Google AI Studio | 在可用地区免费用[^95] | 可用地区不含中国大陆和香港[^96]；同样的模型走 API 没有免费层[^50] | — | ✗ |
| Meta AI | 宣称免费[^97]，一次出多张[^98] | — | — | ✗ |
| Grok Imagine | 免费账号 0 张，2026-03-19 起取消免费档（第三方）[^99][^100] | 最低档 SuperGrok Lite 只是"试用"生图生视频[^101] | — | ✓ |
| Leonardo.Ai | 每天 150 Fast Tokens[^102] | 正从订阅制转向按量付费[^103] | — | ✗ |
| Ideogram | 每周 30 credits，用完等下周或者买[^104] | 私密生成和高质量导出要 Plus[^104] | Plus \$20/月（年付 \$15/月），每月 2400 credits[^104] | ✗（走代理 403） |
| Adobe Firefly | 免费版每天有少量次数，数字没写[^105] | 自家模型的输出可商用[^105] | Standard \$9.99/月 2000 积分；付费档标准生图不限量[^105] | ✗（显示"访问被拒"） |
| Dreamina（即梦国际版） | 每天 120 credits，图片视频共用[^106] | 另一个官方页写限"eligible U.S. web accounts"[^107] | — | ✓ |
| Kling AI 国际版 | 活动期间的每日登录积分只发给订阅用户，当天 24:00 清零[^108] | \$1 = 66 credits[^108] | — | ✓ |
| NightCafe | 每天补 5 credits，不管余额多少都发[^109] | 注册不用绑卡[^110] | — | ✗ |
| SeaArt | 每天 130 Stamina，每日刷新[^111][^112] | 约够 21 张、可同时跑 2 个任务（第三方）[^113] | — | ✗ |
| Tensor.Art | 每天 50 credits，标准图 0.36 credits/张，约 138 张（第三方）[^114] | 免费版作品只存 7 天[^114] | Pro \$9.90/月，每天 300 credits[^114] | ✗ |
| Civitai | 新用户 100 Blue Buzz，生成器里每天可领一次[^115] | 2025-05 起不能直接刷信用卡买[^115] | — | ✗ |
| PixAI（动漫向） | 每天 10,000 免费 credits，不用绑卡[^116] | — | — | ✗ |
| Perchance | 免注册、没有每日上限、不加水印（第三方，2026-04）[^117] | 没有付费档[^117] | — | ✗ |
| Raphael AI | 基础模式免注册、不限次；登录后有每日积分和 2K 模型[^118] | 基础模型约 8 秒一张，一次最多 4 张[^118] | — | ✗ |
| Craiyon | 次数有限；只用文字生图不扣积分[^119] | 任何账户都可商用，免费用户要署名[^119] | — | ✗ |
| Freepik（文档已改名 Magnific） | 每天最多 20 次（自家模型）[^120] | 仅限个人用途，要署名[^120] | — | 403 |
| Recraft | 每天能上传 3 张参考图，每次出 2 张[^121] | 免费版作品归 Recraft、公开展示、不可商用[^122] | — | ✓ |
| Playground | Playground v3 每 3 小时 5 次；GPT Image 2 / Seedream / Nano Banana 合计每月 3 次[^123] | 每天只能下载 2 个设计[^123] | — | 403 |
| Mistral Le Chat | 免费档含基础生图和改图[^124] | 付费档生图额度"最多是免费的 40 倍"[^124] | — | ✗ |
| OpenArt | 只有一次性 40 个试用 credits，4 个并行，作品私密[^125] | — | Essential \$14/月[^125] | ✗ |
| Midjourney | 套餐页没有免费档[^126] | 隐身模式只有 Pro、Mega 档有[^126] | Basic \$10/月，年付 8 折[^126] | 403 |
| Hugging Face Spaces（ZeroGPU） | 任何人都能免费用 ZeroGPU Space[^127] | 每天 GPU 配额：不登录 2 分钟、免费账号 5 分钟、PRO 40 分钟[^127] | PRO \$9/月[^128] | ✗ |
| Google Flow（原 ImageFX） | 免费层每月有积分上限（第三方）[^129] | 付费档生图上限更高[^130] | — | ✗ |
| Draw Things 云端 | 见第 10 节 | — | Draw Things+ \$8.99/月[^10] | ✓（慢） |

## 4. 免费 API（含调用示例）

API key 一律设成环境变量，不要写进代码。下面的示例照官方文档整理；不带 key 调用时，智谱、硅基流动、魔搭、商汤、Cloudflare 这 5 个端点都返回 401（10-21 实测），说明地址可达，但带真 key 出图没有测过。Pollinations 的示例不需要 key，实测能出图。

### 4.1 智谱 CogView-3-Flash（国内，直连 ✓）

- 官方定为免费图像生成模型[^12][^19]。
- 支持 1024x1024、768x1344、864x1152、1344x768、1152x864、1440x720、720x1440 等分辨率[^12]。
- 端点是 open.bigmodel.cn/api/paas/v4/images/generations[^131]，模型名 cogview-3-flash[^12]。
- 限速和用户权益等级挂钩[^132]，每天最多多少张没公布。
- 第三方实测：图右下角带深色圆角的"AI生成"标[^133]。
- 优点是国内厂商、免费、能直连；缺点是画质一般（个人看法）。

```bash
curl https://open.bigmodel.cn/api/paas/v4/images/generations \
  -H "Authorization: Bearer $ZHIPU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "cogview-3-flash", "prompt": "一只坐在窗台上的橘猫", "size": "1024x1024"}'
```

### 4.2 硅基流动 Kolors（国内，直连 ✓）

- Kolors 标"限免"[^13]。
- 图像模型限速：每分钟 2 张（IPM 2）、每天 400 张（IPD 400）[^134]；免费模型的限速是固定值，不随等级提升[^134]。
- 要实名认证后才能领奖励、用部分功能[^135]。
- **水印**：API 默认加显式的"AI 生成"水印，隐式水印始终加[^44]。传 `X-Enable-Watermark: 0` 可以关显式水印，但开发者依法要在最终图上自己加[^44]。更新日志里也写了"水印默认添加"[^136]。

```bash
curl https://api.siliconflow.cn/v1/images/generations \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "Kwai-Kolors/Kolors", "prompt": "an island near sea, lighthouse, boats", "image_size": "1024x1024", "num_inference_steps": 20, "guidance_scale": 7.5}'
```

### 4.3 魔搭 API-Inference（国内，直连 ✓）

- **门槛**：魔搭账号必须先绑定阿里云账号[^14]。
- **额度**：按魔粒扣，轻量模型 0.5、主流模型 1、旗舰模型 2 魔粒/次[^14]。魔粒每天登录送 200、绑阿里云再加 50[^7]，按此每天约 125–500 次（换算）。
- **定位**：官方说是给开发者的免费便捷调用方式，有商业化需求建议用商业平台的 API[^14]；不要用于要高并发、要 SLA 的线上任务[^14]。
- **调用方式**：异步。先 POST v1/images/generations 并带请求头 `X-ModelScope-Async-Mode: true`，再轮询 v1/tasks/{task_id}[^137]。
- 最多叠加 6 个 LoRA[^137]。
- 尺寸范围：SD 系列 64–2048，FLUX 64–1024，Qwen-Image 64–1664，Z-Image-Turbo 512–2048[^137]。

```python
import os, time, requests

base = "https://api-inference.modelscope.cn/"
h = {"Authorization": f"Bearer {os.environ['MODELSCOPE_TOKEN']}", "Content-Type": "application/json"}
r = requests.post(base + "v1/images/generations",
                  headers={**h, "X-ModelScope-Async-Mode": "true"},
                  json={"model": "Qwen/Qwen-Image", "prompt": "A golden cat"})
task_id = r.json()["task_id"]
while True:
    d = requests.get(base + f"v1/tasks/{task_id}",
                     headers={**h, "X-ModelScope-Task-Type": "image_generation"}).json()
    if d["task_status"] in ("SUCCEED", "FAILED"):
        print(d.get("output_images"))
        break
    time.sleep(5)
```

### 4.4 商汤 SenseNova U1.5 Lite（国内，公测期，直连 ✓）

- 公测期每 5 小时 1,500 次请求，"完全免费"[^15]。
- 要在 SenseNova 平台注册并完成账号认证[^15]。
- 平台文档的说法是按积分池算：每 5 小时 60,000 积分、每 7 天 600,000 积分[^49]。Flash-Lite 模型先扣专用积分池[^49]。
- 端点 token.sensenova.cn/v1/images/generations，模型名 sensenova-u1.5-lite，尺寸支持 2K/4K 常量[^15]。
- 公测什么时候结束、正式价多少，都没公布。

```bash
curl https://token.sensenova.cn/v1/images/generations \
  -H "Authorization: Bearer $SENSENOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sensenova-u1.5-lite", "prompt": "A baby sea otter floating on a calm sea", "n": 1}'
```

### 4.5 Cloudflare Workers AI（海外，直连 ✓）

- 免费计划每天 10,000 Neurons[^16]，每天 00:00 UTC 重置[^16]，也就是北京时间早上 8 点。
- 每张消耗（按官方单价换算）：
  - FLUX.1 schnell：每个 512² 块 4.80 Neurons，每步 9.60[^16]。1024²、4 步是 57.6 Neurons，每天约 173 张。
  - FLUX.2 [klein] 4B：每个输出 512² 块 26.05 Neurons[^16]。1024² 是 104.2，每天约 96 张。
  - FLUX.2 [klein] 9B：首个百万像素 \$0.015[^16]，约合 1,364 Neurons，每天只够约 7 张。
- 超出部分付费计划按 \$0.011 / 1,000 Neurons 收[^16]。

```bash
curl https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/black-forest-labs/flux-1-schnell \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{"prompt": "cyberpunk cat"}'
```

接口写法来自官方模型页[^138]。

### 4.6 Pollinations（海外，开源，直连 ✓）

- 项目开源[^139]。
- **10-21 实测**：
  - 旧接口 image.pollinations.ai/prompt/提示词，不带 key：连续请求返回 402，"Free limit reached: 1 image every 45 seconds per IP"。
  - 等 50 秒再请求，返回 768×768 的 JPEG，用时 7.9 秒，响应头显示用的模型是 sana。
  - 新接口 gen.pollinations.ai/image/提示词，不带 key：新提示词返回 401，要求 API key；之前用过的提示词能返回图，但那是缓存。
- **官方定价**：1 pollen = \$1[^140]；Z-Image Turbo 每张 0.004 pollen，FLUX.2 Klein 4B 每张 0.005 pollen，每个用户 60 RPM[^37]。
- 旧的直接扣费方式限每 IP 每小时 1 pollen[^141]。
- 做 GitHub 任务、试模型、做应用可以领免费 pollen[^140]。
- 第三方实测：图上带 pollinations.ai 的 logo，nologo=true 参数没能去掉[^133]。

```bash
curl -o out.jpg "https://image.pollinations.ai/prompt/a%20small%20lighthouse%20at%20dusk"
```

### 4.7 AI Horde（海外，开源，志愿者算力）

- 任何人都能免费用，可以匿名，kudos 不过期[^142]。第三方网站、游戏和应用能通过 REST API 接入[^142]。
- 匿名用户 0 kudos，注册用户至少 25；kudos 越多排得越前，匿名和 0 kudos 的请求先到先得[^143]。
- 10-21 上午查询实时状态：图像 worker 11 个，排队 701 个请求（实测）。
- 直连时通时断：10-21 第一次直连超时、走代理能通，第二次直连能通（实测）。
- 请求在志愿者的电脑上跑，敏感内容别发（建议）。

### 4.8 其他免费 / 限时免费的

| 服务 | 怎么免费 | 注意 | 直连 |
| --- | --- | --- | --- |
| Agnes AI | agnes-image-2.0-flash、2.1-flash、2.5-flash 现价 \$0（2.0-flash 原价 1K 每千张 \$10）[^17] | 限时优惠，结束时间看平台公告[^17]；第三方实测图上不带水印，免费限速 09-23 减半[^133] | ✓ |
| Puter.js | "用户付费"模式：开发者成本 \$0，每个用户有免费月度额度[^144]，用完由用户自己付[^145] | 适合纯前端网页应用（个人看法） | ✓ |
| Pixazo | 免费层不收费，但开通要绑信用卡[^146] | Flux Schnell、SDXL 最高 1024²，SD 1.5 最高 512²[^146] | ✓ |

## 5. 新用户一次性额度

### 5.1 国内

#### 阿里云百炼

- 规则[^147]：
  - 每个模型单独给，同一模型的不同快照也各算各的，互不共享；
  - 不用实名就能领和用，用完要按量付费时才需要实名；
  - 主账号和 RAM 子账号共享；
  - 只抵扣实时推理；
  - 同一实名主体重新注册，不能再领。
- 有效期 90 天，从开通、模型发布或申请通过算起（取较晚的）；只有华北 2（北京）有免费额度[^20]。
- 文生图相关模型的免费张数[^20]：

| 模型 | 免费张数 | 原价（元/张） |
| --- | --- | --- |
| wanx2.0-t2i-turbo | 500 | 0.04 |
| wanx2.1-t2i-turbo | 500 | 0.14 |
| wanx2.1-t2i-plus | 500 | 0.20 |
| wanx-v1 | 500 | 0.16 |
| wan2.2-t2i-flash | 100 | 0.14 |
| wan2.2-t2i-plus | 100 | 0.20 |
| wan2.5-t2i-preview、wan2.6-t2i | 各 50 | 0.20 |
| wan2.7-image | 50 | 0.20 |
| wan2.7-image-pro | 50 | 0.50 |
| z-image-turbo | 100 | 0.10 |
| qwen-image-2.0 | 100 | 0.20 |
| qwen-image-2.0-pro（每个快照另算） | 100 | 0.50 |
| qwen-image-2.1-pro、qwen-image-2.1-turbo | 各 10 | 0.25、0.10 |
| qwen-image-3.0、qwen-image-3.0-pro | 输入输出合计 10 | 见 6.1 节 |

- 上表合计约 2,720 张，按原价约值 442 元（换算，不含 qwen-image-3.0 和快照）。
- 百炼上转售的可灵、Vidu 没有免费额度[^20]。

#### 火山方舟

- 注册就送"一定额度"的免费推理次数[^148]，只抵扣按 token 后付费的在线推理[^148]。
- 用完调用会直接失败；要继续用得实名认证，再手动开通模型服务[^148]。
- 文档没列 Seedream 送几张。第三方汇总：Seedream 4.0 送 200 张[^149]，5.0-lite 送 50 张[^150]。

#### 其他

- **火山引擎即梦 API**：免费状态有 200 次体验额度，并发 1[^38]。
- **腾讯云 TokenHub**：新人包里语言模型各 100 万 tokens、1 年有效，另有视频、3D 的积分，但没有图片生成[^151]。旧混元平台首次开通生图各送 50 次，但已停止新购[^152]。
- **百度千帆**：新用户额度只抵扣预置模型的在线推理 tokens[^153]，清单里是 ERNIE-4.5-Turbo-128K、DeepSeek-R1 等各 100 万 tokens、3 个月[^153]，没有图像模型。
- **硅基流动**：实名认证领一张 16 元通用代金券，全平台通用[^135]。推荐官计划邀请一人双方再各得 16 元，人数不设上限，活动到 2026-12-31[^135]。16 元约够 160 张 Z-Image-Turbo 或 53 张 Qwen-Image（换算）。
- **优云智算**：每个生图模型免费 5 张，2025-06-30 起开始收费[^31]。

### 5.2 海外

| 平台 | 送什么 | 能出多少（换算） |
| --- | --- | --- |
| Stability AI | 25 credits，1 credit = \$0.01；Stable Image Core 每张 3 credits[^154] | 约 8 张 Core |
| Runware | 用企业邮箱注册送 \$2[^155] | 约 3,300 张 FLUX.2 [klein] 4B |
| WaveSpeedAI | 新账号送 \$1，不用绑卡；支持微信、支付宝付款[^36] | 200 张 Z-Image Turbo[^36] |
| Novita | 注册页写送 \$100 Sandbox credits，90 天有效[^156] | 能不能用于生图 API 未核实 |
| fal | 赠送额度和优惠券有效期 1 周到 1 年不等[^157] | 送多少没写 |
| Replicate | "Try for Free"集合里的模型（比如 google/imagen-4）可以免费跑有限次[^158]；其他要先预充值[^159] | — |
| Together AI | 没有免费试用，首充至少 \$15[^160] | — |
| DeepInfra | FLUX-1-schnell 标了"no-free-anon"，不支持匿名免费[^161] | — |
| ModelsLab | 只有付费档，最低 \$21/月 3,250 次调用[^162] | — |

## 6. 国内付费 API（逐平台）

下面的国内 API 主机直连都能通（实测）。

### 6.1 阿里云百炼（通义万相 / 千问 / Z-Image）

| 模型 | 用途 | 单价（元/张） |
| --- | --- | --- |
| wanx2.0-t2i-turbo | 文生图 | 0.04 |
| wan2.2-t2i-flash、wanx2.1-t2i-turbo | 文生图 | 0.14 |
| wanx-v1 | 文生图 | 0.16 |
| wan2.6-t2i、wan2.5-t2i-preview、wan2.2-t2i-plus、wanx2.1-t2i-plus | 文生图 | 0.20 |
| wan2.7-image、wan2.6-image | 生成与编辑 | 0.20 |
| wan2.7-image-pro | 生成与编辑 | 0.50 |
| wan2.5-i2i-preview / wanx2.1-imageedit | 图像编辑 | 0.20 / 0.14 |
| wanx-sketch-to-image-lite | 涂鸦作画 | 0.06（免费 500 张） |
| wanx-poster-generation-v1 | 创意海报 | 目前只供免费体验，额度用完不能调用 |
| qwen-image-2.1-turbo / qwen-image-2.1-pro | 文生图 | 0.10 / 0.25 |
| qwen-image-3.0 | 文生图 | 1K、2K 都是 0.18；输入图 0.02 元/张 |
| qwen-image-3.0-pro | 文生图 | 1K 0.25、2K 0.5；输入图 0.02 元/张 |
| qwen-image-2.0 / qwen-image-2.0-pro | 文生图与编辑 | 0.2 / 0.5 |
| z-image-turbo | 文生图 | 0.1；开启提示词改写 0.2 |
| kling/kling-v3-image-generation | 可灵转售 | 0.2 |
| kling/kling-v3-omni-image-generation | 可灵转售 | 1K、2K 0.2，4K 0.4 |
| vidu/viduq2-fast_reference2image、vidu/vidu-image_reference2image | Vidu 参考生图 | 0.28125、0.625 |

- 上表价格都来自百炼的模型价格页[^20]，是华北 2（北京）的价。新加坡地域更贵，比如 z-image-turbo 是 0.110089 元/张[^20]。
- **怎么调用**：
  - HTTP 只支持异步，必须带请求头 `X-DashScope-Async: enable`[^163]。
  - 先 POST `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis` 拿 task_id，再 GET `/api/v1/tasks/{task_id}` 取结果[^163]。
  - 官方建议从老域名 dashscope.aliyuncs.com 迁到业务空间专属域名[^163]。

### 6.2 火山方舟（豆包 Seedream）

| 模型 | 单价（元/张） | 备注 |
| --- | --- | --- |
| doubao-seedream-5-0-flash | 0.12 | 输入图免费 |
| doubao-seedream-4-0 | 0.20 | 输入图免费 |
| doubao-seedream-5-0-lite | 0.22 | 输入图免费 |
| doubao-seedream-4-5 | 0.25 | 输入图免费 |
| doubao-seedream-5-0-pro | ≤261 万像素（1.5K 及以下）0.30；更大 0.60；图层拆分 0.15 / 0.30 | 输入图首张免费，第 2 张起 0.02 |

- 价格来自方舟模型价格页[^22]。组图按实际生成的张数计费；因为审核等原因没输出的图不收费[^22]。
- 5.0 flash（doubao-seedream-5-0-flash-260915）的能力和 5.0 pro 完全一致，生图更快、价格更低[^23]。
- **怎么调用**：POST `https://ark.cn-beijing.volces.com/api/v3/images/generations`[^164]。
- **水印**：`watermark` 参数默认 true，会在图右下角加"AI 生成"字样[^164]。
- **同款转售**：七牛的 5.0 flash 0.12 元（1.5K 以上也是 0.12），5.0 pro 0.3 / 0.6 元[^39]；TokenHub 的 Seedream-Image-v5.0-lite 0.22 元[^40]；优云智算的 4.5 是 0.25 元[^31]。

### 6.3 火山引擎·即梦 API

| 能力 | 计费方式 | 单价（元） |
| --- | --- | --- |
| 文生图 3.0 / 3.1、图生图 3.0 智能参考、AI 营销商品图 3.0 | 按调用次数（每次 1 张） | 0.2 |
| 图片生成 4.0 系列（含素材提取） | 按生成张数（一次可能出多张） | 0.22 |
| 交互编辑 inpainting | 按次 | 0.2 |
| 智能超清 | 按次 | 0.4 |

- 以上价格来自即梦 API 计费说明[^38]。
- **资源包**[^38]：
  - 3.0 系列 10 万次 18,000 元（0.18 元/次）；50 万次 8 万元（页面写作"8,0000"），约 0.16 元/次（换算）；
  - 1 年有效，可以叠加，支持 7 天无理由退订；
  - 资源包用完不会停服，改按次扣费。
- **并发**：免费状态 1；付费 1 或 2，部分能力可以加购并发[^38]。
- 文生图 2.1 正在下线[^38]。图片生成 4.6 在文档目录里有，但计费表里没有单价。

### 6.4 可灵开放平台（Kling）

- 图片 API 1 积分 = 0.025 元（原价）；视频 API 1 积分 = 1 元[^42]。

| 模型 | 能力 | 分辨率 | 积分 / 张 | 折合 |
| --- | --- | --- | --- | --- |
| Kling Image 2.1 | 文生图 | 1K、2K | 4 | 0.1 元 |
| Kling Image 2.1 | 图生图 | 1K、2K | 8 | 0.2 元 |
| Kling Image 3.0 | 文生图、图生图 | 1K、2K | 8 | 0.2 元 |
| Kling Image 3.0-omni | 文生图、图生图 | 1K、2K / 4K | 8 / 16 | 0.2 / 0.4 元 |
| Kling Image O1 | 文生图、图生图 | 1K、2K | 8 | 0.2 元 |

- 上表来自可灵开放平台定价页[^42]。
- **资源包**[^42]：
  - 套餐一 ¥2,500 / 10 万积分；套餐二 ¥7,500 / 30 万积分；套餐三 ¥13,500 / 60 万积分（直降 10%，0.0225 元/积分）；
  - 有效期 180 天，过期剩余积分不延期；并发 9；暂不支持 Kling 4.0。
- 套餐一约够 2.5 万张 Kling Image 2.1 文生图（换算）。
- 国际版 kling-v2-1 文生图 4 积分，\$0.014/张[^43]。
- **转售**：七牛的 Kling v2.1 文生图 0.1 元、图生图 0.2 元、多图生图 0.4 元，Omni 生图 0.2 元、4K 0.4 元[^39]；TokenHub 的 Kling-Image-v3 0.2 元[^40]。

### 6.5 腾讯云 TokenHub（混元等）

- 统一按 10 元 / 百万 tokens 计价，每张按固定 token 数折算[^40]：

| 模型 | 每张 token | 折合（元/张） |
| --- | --- | --- |
| Hy-Image-3.5-preview | 1K、2K 15,000；4K 20,000 | 0.15；0.2 |
| Hy-Image-3.0 | 20,000 | 0.2 |
| WAND-Vega-Image-1.0-Lite | 13,500 | 0.135 |
| WAND-Vega-Image-1.0-Flash | 45,000 | 0.45 |
| Seedream-Image-v5.0-lite | 22,000 | 0.22 |
| Seedream-Image-v5.0-pro（≤261 万像素） | 30,000 | 0.3（换算） |
| Kling-Image-v3 | 20,000 | 0.2 |
| Vidu-Image-q2 | 18,750 | 0.1875 |

- 旧版按张计费的 HY 图片模型从 2026-09-15 起下线[^40]。旧混元平台的混元生图 0.5 元/张、文生图轻量版 0.099 元/张起，现已停止新购[^152]。

### 6.6 百度千帆

- musesteamer-air-image（蒸汽机）0.05 元/张，1024×1024[^21]。
- 千帆也转售千问：qwen-image 0.25 元/张、qwen-image-edit 0.3 元/张[^21]。
- qianfan-image 按积分计价，1 积分 0.025 元：o1-base 文生图 8 积分（0.2 元），v3o 4K 16 积分（0.4 元）[^46]。但文档目录标着"内部使用"[^46]，所以首选 musesteamer-air-image。

### 6.7 智谱开放平台

- CogView-3-Flash 免费；CogView-4 每次 0.06 元，Batch 0.03 元；GLM-Image 每次 0.1 元，不支持 Batch[^19]。
- 国际站 Z.ai：CogView-4 \$0.01，GLM-Image \$0.015[^47]。

### 6.8 MiniMax（海螺）

- image-01 / image-01-live 每张 0.025 元[^18]，是国内最便宜的；国际站 \$0.0035[^48]。
- 端点 api.minimax.cn/v1/image_generation[^165]；参数里有 aspect_ratio、n、prompt_optimizer[^165]。

### 6.9 硅基流动

- Kolors 限免[^13]。
- Z-Image-Turbo 0.1 元/张，Z-Image 0.3 元/张[^33]。
- Qwen-Image（200 亿参数[^166]）0.3 元/张[^30]。
- ERNIE-Image-Turbo 上线时 0.11 元/张[^167]，现已下线[^13]。

### 6.10 七牛云

- 端点 api.qnaigc.com/v1，文生图接口 /images/generations，返回 Base64[^51]。
- 价格：Seedream 5.0 flash 0.12 元；5.0 pro ≤1.5K 0.3 元、更大 0.6 元，输入图首张免费，限流每分钟 500 张[^39]。Kling v2.1 文生图 0.1 元[^39]。
- 模型列表里还有 gemini-2.5-flash-image（Nano Banana）[^51]，国内直连就能调；七牛的价格没查到，优云智算也有这个模型（见 6.11）。

### 6.11 优云智算（Compshare）

- 端点 api.modelverse.cn/v1，兼容 OpenAI 协议[^168]。
- 按张计费[^31]：flux.1-dev 0.10 元；Qwen-Image 0.25 元；doubao-seedream-4.5 0.25 元；Qwen-Image-Edit 0.3 元；flux-kontext-pro 0.35 元；flux-kontext-max 0.70 元。
- 按 token 计费[^31]：gpt-image-1 输入 35 元、输出 280 元 / 百万 tokens；gemini-2.5-flash-image 输入 2.2 元、输出 219 元 / 百万 tokens。

### 6.12 其他国内渠道

- **302.AI**：Z-Image-Turbo \$0.05/次[^169]，约合 0.33 元，是硅基流动同款的 3.3 倍（换算）。充值余额永久有效[^170]。它的 API 直连和走代理都连不上（实测）。
- **模力方舟（Gitee AI）**：有 24 个文生图模型、51 个接口[^171]，已部署的模型能在线免费体验[^172]；单价未核实。
- **无问芯穹 GenStudio**：支持 Seedream 等闭源模型，只对成功出图的请求收费[^173]；单价没查到。

## 7. 海外付费 API

| 平台 | 模型与每张价格（美元） | 计费细节 | 直连 |
| --- | --- | --- | --- |
| Prodia | FLUX.2 Klein 4B：≤1MP \$0.0005、≤2MP \$0.0027、≤3MP \$0.0040、>3MP \$0.0059；FLUX.2 [dev] 1MP \$0.012；SDXL ≤25 步 \$0.0020、26–50 步 \$0.0025[^24] | SDXL 边长 512–1536 都同价[^24] | ✓ |
| Runware | FLUX.2 [klein] 4B \$0.0006[^25]；klein 9B \$0.00169[^174]；FLUX.1 schnell 1024² \$0.0013、512² \$0.0006[^175]；SDXL 1024² 20 步 \$0.0013[^176] | 部分模型公布的是实测记录，不是费率[^177] | ✓ |
| Runware（续） | Z-Image-Turbo 1024² \$0.0032、2048² \$0.0141[^35]；Qwen-Image 1024² \$0.0058[^32] | 模型页写的示例价更低：Z-Image-Turbo \$0.0013[^178]（等于 schema 里 512² 的价），Qwen-Image \$0.0032[^179]；按 1024² 估以 schema 为准 | ✓ |
| Cloudflare Workers AI | FLUX.1 schnell 约 \$0.00063；FLUX.2 [klein] 4B 约 \$0.00115（按官方单价换算）[^16] | 每天前 10,000 Neurons 免费[^16] | ✓ |
| DeepInfra | FLUX-1-schnell 每个 image unit 0.05 美分，默认 1024²[^161] | 1 unit 是否等于一张 1024² 图未核实 | ✓ |
| Together AI | Juggernaut Lightning Flux \$0.0017 起；SD XL \$0.0019 起；Qwen Image \$0.0058 起；Wan 2.6 Image \$0.03 起[^29] | 首充至少 \$15[^160] | ✓ |
| fal | FLUX.1 schnell \$0.003/MP[^180]；Z-Image Turbo \$0.005/MP[^34]；FLUX.2 [klein] 4B \$0.005/MP[^181] | 1024² 算 1MP[^182]，不足 1MP 向上取整[^180]；Z-Image 开提示词扩写每次加 \$0.0025[^34] | ✓ |
| Replicate | flux-schnell 每千张 \$3[^183] | schnell 是 Apache 2.0，可商用[^184]；要先预充值[^159] | ✓ |
| Novita | FLUX.1 schnell：\$0.003 ×（宽×高×步数）/（1024×1024×4）[^185] | 1024²、4 步正好 \$0.003（换算） | ✓ |
| Segmind | Flux Schnell、SDXL 约 \$0.008；Pruna P Image \$0.005（Segmind 官方博客，2026-04）[^186] | 每分钟 60–1000 次请求，按档位[^187] | ✓ |
| WaveSpeedAI | Z-Image Turbo \$0.005[^36] | 支持微信、支付宝[^36] | ✓ |
| MiniMax 国际站 | image-01 \$0.0035[^48] | — | ✓ |
| Recraft | V4.1 Flash \$0.007；V4.1 栅格 \$0.035、矢量 \$0.08、Pro 2K \$0.21、Pro 矢量 \$0.30；V4 \$0.04[^188] | 买的单位不过期[^188] | ✓ |
| BFL（FLUX 官方） | FLUX 3 Klein：768² \$0.008、1K \$0.009、1.5K \$0.011、2K \$0.014、4K \$0.036[^58] | 被拒、失败和被审核拦下的不收费[^189] | ✓ |
| BFL（续） | FLUX 3 Image：768² \$0.041、1K \$0.048、1.5K \$0.07、2K \$0.10、4K \$0.607[^189]；FLUX.2 [klein] 4B 起 \$0.014、9B 起 \$0.015[^58] | FLUX.2 [pro] 起 \$0.03/MP、[flex] \$0.05/MP、[max] 起 \$0.07/MP，分辨率向上取整到整 MP[^59] | ✓ |
| Stability AI | 1 credit = \$0.01：SDXL 1.0 起 0.9、SD 3.5 Flash 2.5、Stable Image Core 3、SD 3.5 Medium 3.5、SD 3.5 Large Turbo 4、SD 3.5 Large 6.5、Stable Image Ultra 8 credits[^154] | — | ✓ |
| Z.ai（智谱国际站） | CogView-4 \$0.01；GLM-Image \$0.015[^47] | — | ✓ |
| Runway | muse_image 1 credit；gen4_image_turbo 2 credits；gen4_image 720p 5、1080p 8 credits；1 credit = \$0.01[^190] | — | ✓ |
| Kling 国际版 | kling-v2-1 文生图 \$0.014[^43] | — | ✓ |
| OpenRouter | Seedream 5.0 Flash 起 \$0.018；Seedream 4.5 \$0.04，不论尺寸[^41] | 出图模型没有免费的（10-21 实测） | ✓ |
| xAI | grok-imagine-image 1K、2K 都是 \$0.02，输入图 \$0.002[^53]；grok-imagine-image-2.0 1K Low 起 \$0.04[^54] | — | ✗（走代理返回 421） |
| Krea | Krea 2 Medium \$0.030、Large \$0.060；加风格参考或情绪板更贵[^191] | — | ✗（走代理也超时） |
| Luma | Uni-1.1（2K）\$0.0404；Uni-1.1 Max \$0.10[^192]；旧的 Photon 每张 2MP \$0.015、Photon Flash \$0.004[^193] | 主要针对英文优化[^192] | ✗ |
| Ideogram | 官方价格页列了 Ideogram 4.5 / 4.0 / 3.0 和 P-Image[^194]，单价是动态加载的，没抓到 | 第三方：P-Image \$0.003 至 \$0.03[^195]；AA 榜单列的 Ideogram 4.0 Instant 每千张 \$7.5、Fast \$10.5、标准 \$60[^196] | 时通时断 |
| OpenAI | gpt-image-2（1024²）low \$0.006、medium \$0.053、high \$0.211；GPT Image 1 Mini low \$0.005[^52] | gpt-image-2.5-flare 按 token：图像输出 \$30/百万，Batch \$15[^197]；官方示例一张图 196 个输出 token，约 \$0.00588[^52] | ✗（代理返回 421） |
| Google Gemini | Nano Banana 2.1：1K \$0.0336、2K \$0.0504、4K \$0.113，Batch 半价；Nano Banana 2：1K \$0.067；Nano Banana 2 Lite：1K \$0.0336[^50] | Nano Banana Pro 1K/2K \$0.134、4K \$0.24；初代 Nano Banana \$0.039[^198]；这些图像模型都没有免费层[^50] | ✗ |
| Google Vertex AI | Imagen 4 Fast \$0.02、Imagen 4 \$0.04、Imagen 4 Ultra \$0.06[^199] | Gemini API 里的 Imagen 已经关停[^200] | ✗ |
| Microsoft Foundry | MAI-Image-2.6-Flash 图像输出 \$19/百万 tokens；MAI-Image-2.6 \$38/百万[^55] | 每张图多少 token 没公布；要有绑定有效付款方式的 Azure 订阅[^57] | — |

- Gemini API 的可用地区不含中国大陆和香港[^96]。
- Midjourney 没有正式 API。官方只说在调研企业 API[^201]；10-10 宣布了小范围的 MCP 测试，用量、价格、开始时间都没公布（第三方）[^202]。
- 微软 2.5 代的价格：MAI-Image-2.5-Flash 图像输出 \$19.50/百万 tokens[^203]。

## 8. 按 1000 张算成本（换算）

按第 6、7 节的官方单价乘 1000；美元按 6.69 折算[^1]，不含跨境支付手续费。默认 1024² 左右、出 1 张。

| 排名 | 模型（平台） | 1000 张 | 折合人民币 |
| --- | --- | --- | --- |
| 1 | FLUX.2 Klein 4B（Prodia）[^24] | \$0.50 | ≈ 3.3 元 |
| 2 | FLUX.2 [klein] 4B（Runware）[^25] | \$0.60 | ≈ 4.0 元 |
| 3 | FLUX.1 schnell（Cloudflare，超出免费部分）[^16] | \$0.63 | ≈ 4.2 元 |
| 4 | FLUX.2 [klein] 4B（Cloudflare）[^16] | \$1.15 | ≈ 7.7 元 |
| 5 | FLUX.1 schnell（Runware）[^175] | \$1.30 | ≈ 8.7 元 |
| 6 | FLUX.2 [klein] 9B（Runware）[^174] | \$1.69 | ≈ 11.3 元 |
| 7 | FLUX.1 schnell（fal、Replicate、Novita）[^180][^183][^185] | \$3.00 | ≈ 20.1 元 |
| 8 | Z-Image-Turbo（Runware）[^35] | \$3.20 | ≈ 21.4 元 |
| 9 | image-01（MiniMax 国际站）[^48] | \$3.50 | ≈ 23.4 元 |
| 10 | image-01（MiniMax 国内）[^18] | — | 25 元 |
| 11 | CogView-4 Batch（智谱）[^19] | — | 30 元 |
| 12 | Z-Image Turbo（fal、WaveSpeed）[^34][^36] | \$5.00 | ≈ 33.5 元 |
| 13 | wanx2.0-t2i-turbo（百炼）[^20] | — | 40 元 |
| 14 | gpt-image-2 low（OpenAI）[^52] | \$6.00 | ≈ 40.1 元 |
| 15 | Recraft V4.1 Flash[^188] | \$7.00 | ≈ 46.8 元 |
| 16 | musesteamer-air-image（千帆）[^21] | — | 50 元 |
| 17 | CogView-4（智谱）[^19] | — | 60 元 |
| 18 | FLUX 3 Klein 1K（BFL）[^58] | \$9.00 | ≈ 60.2 元 |
| 19 | Kling 2.1 国际版[^43] | \$14.00 | ≈ 93.7 元 |
| 20 | Z-Image-Turbo（百炼、硅基流动）、Kling Image 2.1、qwen-image-2.1-turbo[^20][^33][^42] | — | 100 元 |
| 21 | Nano Banana 2.1 Batch[^50] | \$16.80 | ≈ 112.4 元 |
| 22 | Seedream 5.0 flash（方舟、七牛）[^22][^39] | — | 120 元 |
| 23 | Seedream 5.0 Flash（OpenRouter）[^41] | \$18.00 | ≈ 120.4 元 |
| 24 | grok-imagine-image（xAI）[^53] | \$20.00 | ≈ 133.8 元 |
| 25 | Hy-Image-3.5-preview（TokenHub）[^40] | — | 150 元 |
| 26 | 即梦 API 3.0（10 万次资源包）[^38] | — | 180 元 |
| 27 | wan2.6-t2i（百炼）[^20] | — | 200 元 |
| 28 | Nano Banana 2.1[^50] | \$33.60 | ≈ 224.8 元 |
| 29 | Luma Uni-1.1（2K）[^192] | \$40.40 | ≈ 270.3 元 |
| 30 | Seedream 5.0 pro（≤1.5K）[^22] | — | 300 元 |
| 31 | FLUX 3 Image 1K（BFL）[^189] | \$48.00 | ≈ 321.2 元 |
| 32 | Z-Image-Turbo（302.AI）[^169] | \$50.00 | ≈ 334.6 元 |
| 33 | gpt-image-2 medium（OpenAI）[^52] | \$53.00 | ≈ 354.6 元 |

- 便宜不等于好。第三方的开放权重榜（Artificial Analysis，按两两盲选投票算 Elo）[^196]：FLUX.2 [klein] 4B 837 分，Z-Image Turbo 936 分，Qwen-Image-2.1 1042 分，FLUX.1 [schnell] 只有 740 分[^196]。
- 同一个模型在不同平台能差十几倍，比如 Z-Image-Turbo 从 Runware 的约 0.02 元到 302.AI 的约 0.33 元（换算）。

## 9. 本地免费软件

### 9.1 还在维护的

星数、最新版本和最后提交时间是 10-21 用 GitHub API 查的（实测）。

| 软件 | 许可证 | ★ | 最新版本 | 特点 |
| --- | --- | --- | --- | --- |
| ComfyUI | GPL-3.0 | 140,730 | v0.42.1（10-19） | 节点式工作流；支持所有系统和 NVIDIA、AMD、Intel、Apple 芯片、昇腾[^204]；有桌面版、便携版和官方付费云[^204]；能通过 API 接进生产流程[^204] |
| SwarmUI | MIT | 4,691 | 0.9.8-Beta（02-06），代码 10-20 仍在更新 | 能自动安装 ComfyUI 当后端[^205]；Mac 只支持 M 系列芯片[^205] |
| Forge Neo | AGPL-3.0 | 1,834 | 2.30.1（10-19） | sd-webui-forge-classic 的 neo 分支[^206]；原版 Forge 2025 年中以后没提交、也没加 FLUX.2，Neo 是维护中的后继，保留单页界面[^207]；去掉了 SD3 支持[^207] |
| InvokeAI | Apache-2.0 | 28,791 | v6.14.2（09-27） | 面向专业用户和爱好者的创作引擎[^208]，带画布和工作流；社区版有 Windows、Mac、Linux 安装包[^209] |
| SD.Next | Apache-2.0 | 7,357 | 没发正式版，最后提交 10-19 | 能生成和编辑图片、视频[^210]；支持 NVIDIA、AMD、Intel、Apple 芯片和 CPU[^210] |
| Krita AI Diffusion | GPL-3.0 | 10,750 | v1.53.0（08-22），最后提交 10-03 | 绘画软件 Krita 的插件；本地跑建议 6 GB 以上显存的 NVIDIA 显卡[^211]；Apple 芯片要 macOS 14+[^211] |
| Mochi Diffusion | GPL-3.0 | 7,971 | v6.2（09-30） | 原生 Mac 应用，跑 SD 和 FLUX.2 Klein[^212]；用 Core ML，能走神经网络引擎，很省内存，但每个模型的出图尺寸在转换时就固定了[^212] |
| mflux | MIT | 2,524 | v0.23.0（10-16） | 把多个主流模型逐行移植到 Apple 的 MLX[^213]；命令行，比如 mflux-generate-z-image-turbo[^213] |
| stable-diffusion.cpp | MIT | 7,743 | master-982（10-20） | 纯 C/C++ 实现[^214]；10-16 首日支持 FLUX.3 Image Klein，09-20 支持 Qwen-Image-2.1[^214] |
| Draw Things | GPL-3.0（推理引擎） | 594 | v26.1014.0（10-15） | Mac / iPhone 应用，推理引擎开源，也能自己搭 gRPC 服务端[^215]；云端见第 10 节 |

### 9.2 已停更或只修 bug，不建议新装

- **AUTOMATIC1111 WebUI**：基于 Gradio 的老牌界面[^216]。最新版 v1.10.1 发布于 2025-02，默认分支最后一次提交在 2024-07（实测）。
- **原版 Forge**[^217]：最后一次提交在 2025-06-26（实测），后继是 Forge Neo[^207]。
- **Fooocus**：官方状态是"只修 bug 的有限长期支持"，而且只支持 SDXL[^218]。
- **DiffusionBee**[^219]：最新版 2.5.3 停在 2024-08-14，最后一次提交在 2023-12-28（实测）。

### 9.3 8 GB 内存的 Mac 怎么选

- 第三方测试，SD 1.5 出 512²：M1 8GB 要 20–30 秒，M2 Pro 16GB 要 8–15 秒[^220]。
- 同一测试里，8GB 的 Mac 跑 SDXL"太慢"，跑 Flux Schnell"装不下"[^220]。
- Draw Things 按需加载权重，内存占用最多能省一半，所以它能在 8GB 上跑 SD 1.5，ComfyUI 不行[^220]。同一个模型 ComfyUI 在 Mac 上慢约 3 倍，安装要花一小时[^220]。
- Draw Things 的 Z-Image Turbo 6-bit 版全部加载进内存只占约 4 GiB[^221]。官方建议内存小的设备打开"Optimize for Faster Loading"[^222]。
- vdf.ai 的推荐里，Mac 最低一档是 16–24 GB，用 Z-Image-Turbo 或 FLUX.2 [klein] 4B 的 8-bit 版[^26]，没有给 8GB Mac 的推荐。
- 建议：8 GB 内存的 M2 本地用 Draw Things 跑 SD 1.5 或 Z-Image Turbo 6-bit，更大的模型放到 Draw Things 云端跑。

## 10. Draw Things 云端免费版

### 10.1 怎么开

1. 「机器设置」→「显示云端和共享相关功能」，默认是开的[^11]（Wiki 里叫 Cloud Compute & Sharing；中文界面标签为实测）。
2. 点左下角的「服务器协助」图标，在「云计算」里选免费版，按钮叫「登录免费版」[^11]。
   - 登录后回到「服务器协助」列表，把勾从本机改到「免费版」，生成就跑在官方的 NVIDIA 服务器上[^11]。
   - 别点「返回本地」：它会切回"仅本地"并退出登录（实测）。
3. 登录：Wiki 写的是用 Apple 账号登录[^11]，5 月的版本加了"Sign in with Google"[^223]。官网直装版（26.1013.0）的签名权限里没有 Apple 登录要的 `com.apple.developer.applesignin`（实测），所以直装版建议用 Google 登录（推断）。
4. 模型下拉框下面会显示这次任务要多少算力单元[^11]。

### 10.2 免费档和付费档

| 项目 | 免费档（Community） | Draw Things+ |
| --- | --- | --- |
| 价格 | 免费[^10] | \$8.99/月[^10] |
| 单次任务上限 | 15,000 算力单元[^11] | 40,000，优先排队[^11] |
| 模型 | 只能用官方和社区模型[^11] | 还能用本地 LoRA[^11]、上传自定义 LoRA[^10] |
| 单个任务时长（Wiki 写法） | 约 2 分钟[^11] | 约 5 分钟[^11] |
| API | 每月 20 次请求[^224] | 每月 200 次[^224] |

- 超出上限的任务会被取消，调低设置再试[^11]。
- 开源代码里免费档的默认上限是 10,000，注释写"约 120 秒"[^225]。开发者也说过，免费档大约相当于 2 分钟 GPU 时间[^226]。
- "实验时段"（Lab Hours）会把免费上限提到 30,000，但 Wiki 备注说自从支持 LTX 模型后就没再见过[^226]。
- 每天能用几次，官方没公布。

### 10.3 免费档出一张图要多少单元

用官方开源的 draw-things-cli（26.1014.0）离线估算（实测），参数用官方推荐的步数和 CFG，每次 1 张。✅ 1 万以内；⚠️ 1 万到 1.5 万，看实际上限；❌ 超过 1.5 万，免费档跑不了（1.5 万到 3 万的理论上实验时段能跑，但实验时段已经很久没出现）。

| 模型 | 步数 / CFG | 512² | 1024² | 1536² | 2048² |
| --- | --- | --- | --- | --- | --- |
| FLUX.2 [klein] 4B | 4 / 1 | ✅ 104 | ✅ 359 | ✅ 919 | ✅ 1,988 |
| FLUX.2 [klein] 9B | 4 / 1 | ✅ 233 | ✅ 778 | ✅ 1,918 | ✅ 3,999 |
| FLUX.1 schnell | 4 / 4.5 | ✅ 182 | ✅ 718 | ✅ 1,919 | ✅ 4,248 |
| Z-Image Turbo | 8 / 1 | ✅ 373 | ✅ 1,282 | ✅ 3,229 | ✅ 6,865 |
| Qwen-Image-2.1 Turbo | 8 / 1 | ✅ 331 | ✅ 1,404 | ✅ 3,655 | ✅ 7,776 |
| ERNIE-Image Turbo | 8 / 1 | ✅ 527 | ✅ 1,754 | ✅ 4,319 | ✅ 9,000 |
| SDXL | 16 / 5 | ✅ 318 | ✅ 1,389 | ✅ 3,576 | ✅ 7,482 |
| SD 1.5 | 20 / 7 | ✅ 209 | ✅ 1,233 | ✅ 4,275 | ⚠️ 11,337 |
| Krea 2 Turbo | 8 / 1 | ✅ 663 | ✅ 2,451 | ✅ 6,036 | ⚠️ 12,328 |
| Qwen-Image-2.1 | 40 / 1 | ✅ 1,577 | ✅ 6,945 | ❌ 18,200 | ❌ 38,804 |
| Z-Image（Base） | 30 / 4 | ✅ 2,786 | ✅ 9,601 | ❌ 24,206 | ❌ 51,470 |
| Qwen-Image-2512 | 30 / 4 | ✅ 3,485 | ⚠️ 12,124 | ❌ 31,392 | ❌ 68,593 |
| FLUX.2 [dev] | 28 / 4.5 | ✅ 6,296 | ❌ 20,375 | ❌ 48,081 | ❌ 95,778 |
| Ideogram 4 | 48 / 7 | ✅ 6,891 | ❌ 22,990 | ❌ 56,380 | ❌ 116,901 |

**省额度的规律**（实测）：

- 消耗和步数基本成正比；边长翻倍（像素变 4 倍），消耗变成约 5 倍。
- 多数模型 CFG 大于 1 时消耗翻倍，比如 Z-Image Turbo 从 1,282 变成 2,564。
- 选不压缩的 Exact 版和选 6-bit 版，消耗一样。
- 大模型用官方的 4 步加速 LoRA：Qwen-Image-2512 + Lightning 出 1024² 只要 809、2048² 要 4,573；FLUX.2 [dev] + Turbo 出 1024² 要 2,911。
- Wiki 也建议免费档出大图时用 Schnell 这类加速模型[^11]。

### 10.4 隐私和画质

- 数据走 TLS 加密传输；服务端开源，但没有远程证明，不能保证不被偷看[^11]。
- 官方说云端请求只在内存里处理，数据不能被存下或事后查看[^227]；服务器跑的是官方公开发布的 Docker 镜像[^227]。
- Wiki 的建议是要最高隐私就本地跑，云端不存图但隐私不能完全保证[^11]。
- 画质：同模型同参数，云端和本地基本一样。不同硬件的浮点误差会让结果略有差别，官方把这视为可接受的数值误差[^228]。

## 11. 开源模型：许可证、显存、排名

### 11.1 模型一览

许可证和显存数据来自 vdf.ai 的整理[^26]，Elo 来自 Artificial Analysis 开放权重榜[^196]（以 FLUX.2 [dev] = 1000 为基准[^196]）。

| 模型（厂商） | 发布 | 参数 | 许可证 | 显存 / 权重大小 | Elo |
| --- | --- | --- | --- | --- | --- |
| Z-Image-Turbo（阿里通义） | 2025-11 | 6B | Apache 2.0 | 16 GB 消费级显卡可跑 | 936 |
| FLUX.2 [klein] 4B（BFL） | 2026-01 | 4B | Apache 2.0 | 约 13 GB；RTX 3090 / 4070 起 | 837 |
| ERNIE-Image / Turbo（百度） | 2026-04 | 8B | Apache 2.0 | 24 GB 消费级显卡 | 907 / 914 |
| Qwen-Image-2512（阿里千问） | 2025-12 | 20B | Apache 2.0 | BF16 40.86 GB，FP8 20.43 GB | — |
| LongCat-Image（美团） | 2025-12 | 6B | Apache 2.0 | 开 CPU 卸载约 17 GB | 856 |
| HiDream-O1-Image（HiDream.ai） | 2026-05 | 8B | MIT | BF16 16.37 GB，FP8 8.07 GB | 975 |
| GLM-Image（智谱） | 2026-01 | 9B 自回归 + 7B 解码器 | MIT | 开 CPU 卸载约 23 GB | 885 |
| Qwen-Image-2.1 / Turbo（阿里千问） | 2026-09 / 10 | 7B + 8B 文本编码器 | Qwen 研究许可，**不可商用** | 14.23 GB + 17.53 GB 编码器 | 1042 |
| FLUX.2 [klein] 9B（BFL） | 2026-01 | 9B | FLUX 非商用许可 | FP8 9.43 GB | 929 |
| FLUX.2 [dev]（BFL） | 2025-11 | 32B | FLUX 非商用许可 | FP8 35.46 GB | 1000 |
| Krea 2（Krea） | 2026-06 | 12B | Krea 2 社区许可 | BF16 26.28 GB，FP8 13.14 GB | — |
| Ideogram 4（Ideogram） | 2026-06 | 9.3B | Ideogram 4 非商用许可 | 两个 9.29 GB 的 FP8 主模型 + 8.78 GB 编码器 | 1002 |
| SD 3.5 Large / Medium（Stability） | 2024-10 | 8.1B / 2.5B | Stability AI 社区许可 | Medium 9.9 GB（不含文本编码器） | — |
| HunyuanImage-3.0（腾讯） | 2025-09 | 80B MoE，激活 13B | 腾讯混元社区许可 | 至少 3 张 80 GB 显卡 | 932 |

- **FLUX 3 Image Klein**：BFL 10 月放出的开放权重，stable-diffusion.cpp 10-16 首日支持[^214]。5.6B 参数，单张消费级显卡能跑[^189]，最低 8 GB 显存的 RTX[^229]。许可证是 FLUX Kommunity License，年收入 500 万美元以下的个人和公司可以免费商用[^229]。
- BFL 自己的文档也写明 klein 4B 是 Apache 2.0，9B 是 FLUX 非商用许可[^230]。
- 榜上靠前的还有 Fibo 2.0（1039 分，API 每千张 \$32）和 Ming-Image-0.1-Design（999 分）[^196]。Ming-Image 是 6B、MIT 许可，但官方是在 80 GiB 显存的单卡上验证的[^26]。Fibo 2.0 在 Hugging Face 上标的许可证是"other"（实测）。

### 11.2 许可证要注意的

- 许可证跟着模型走，在哪个平台跑都一样。各平台用户协议对生成图能否商用另有规定，未逐一核实。
- SD 3.5 Medium、Krea 2 有收入门槛：年收入 100 万美元以下才能用[^26]。HunyuanImage-3.0 不适用于欧盟、英国和韩国[^26]。
- 大部分模型还要单独的文本编码器和 VAE[^26]。比如 Z-Image 和 klein 4B 用的 Qwen3 4B 编码器，BF16 就有 8.04 GB[^26]。

### 11.3 按显卡选（vdf.ai 的推荐）

| 硬件 | 可商用 | 非商用或有收入上限 |
| --- | --- | --- |
| 8 GB 显卡 | FLUX.2 [klein] 4B（FP8）；SDXL | 无推荐 |
| 12 GB | Z-Image-Turbo（INT8）；FLUX.2 [klein] 4B | SD 3.5 Medium（年收入 100 万美元以下） |
| 16 GB | Z-Image-Turbo；FLUX.2 [klein] 4B | Qwen-Image-2.1 / Turbo（INT8）；Krea 2（FP8，年收入 100 万美元以下） |
| 24 GB | ERNIE-Image；HiDream-O1-Image；GLM-Image；LongCat-Image | Qwen-Image-2.1（BF16）；Ideogram 4；FLUX.2 [klein] 9B |
| 32–48 GB | Qwen-Image-2512（FP8 32 GB 起，BF16 48 GB 起） | FLUX.2 [dev]（FP8，48 GB 卡） |
| 多卡服务器 | Qwen-Image-2512（BF16） | HunyuanImage-3.0（欧盟、英国、韩国以外） |
| Mac 16–24 GB | Z-Image-Turbo 或 FLUX.2 [klein] 4B（8-bit） | 无推荐 |
| Mac 48 GB 以上 | Qwen-Image-2512（96 GB 起） | Qwen-Image-2.1；Krea 2 |

上表整理自 vdf.ai[^26]。

## 12. 合规：标识、备案、水印

### 12.1 《人工智能生成合成内容标识办法》

- 2025-09-01 起施行[^28]。
- **两种标识**[^28]：
  - 显式标识：在内容或界面里用文字、声音、图形等方式呈现，用户能明显感知到；
  - 隐式标识：用技术手段加在文件数据里，用户不容易感知到。
- **图片怎么加**：在图片的适当位置加显著的提示标识[^28]；提供下载、复制、导出功能时，文件里要带显式标识[^28]。
- **元数据**：要在文件元数据里加隐式标识，内容包括生成合成属性、服务提供者名称或编码、内容编号等[^28]；鼓励再加数字水印[^28]。
- 任何组织和个人不得恶意删除、篡改、伪造、隐匿这些标识[^28]。所以平台加在图上的"AI 生成"角标，拿去当素材时不能随意去掉。

### 12.2 备案和登记

- 通过 API 调用已备案模型的生成式 AI 应用，由地方网信办登记[^27]。
- 截至 2026-04-30，累计 868 款生成式 AI 服务完成备案，530 款应用或功能完成登记[^27]。
- 已上线的应用要在显著位置或产品详情页公示用了哪个已备案或登记的服务[^27]，注明模型名称、备案号或上线编号[^27]。
- Pollinations、AI Horde、Cloudflare 这些境外服务应该没有国内备案（推断），面向国内公众上线时不适合直接用。

### 12.3 各家 API 的水印默认值

| 平台 | 默认 | 能不能关 |
| --- | --- | --- |
| 火山方舟 Seedream | `watermark` 默认 true，右下角加"AI 生成"[^164] | 可设为 false |
| 硅基流动 | 默认加显式水印，隐式水印始终加[^44] | 可关显式水印，但开发者要自己补加[^44] |
| 智谱 CogView-3-Flash | 右下角"AI生成"（第三方实测）[^133] | 没查到 |
| Pollinations | 带 pollinations.ai 的 logo（第三方实测）[^133] | nologo=true 没能去掉[^133] |
| 通义万相、可灵网页版 | 免费档应该带品牌水印（推断） | 去品牌水印是会员权益[^2][^67] |

## 13. 已停服 / 已失效

别按旧教程去找这些：

| 项目 | 状态 |
| --- | --- |
| 星流 AI | 2026-10-10 停止运营[^87]，可迁移到 Lovart[^88] |
| 快手可图网页版 | 2024-08-23 关闭[^89] |
| 阶跃星辰生图 API | 2026-10-10 下线，国内和海外同时停[^231] |
| Amazon Nova Canvas | 2026-09-30 停服[^232] |
| Gemini API 里的 Imagen | 已关停[^200]，Vertex AI 上还有 Imagen 4[^199] |
| Google ImageFX | 2026-04-30 关闭，并入 Flow[^129] |
| TokenHub 旧版按张计费的 HY 图片模型 | 2026-09-15 起下线[^40]；旧混元平台停止新购[^152] |
| 硅基流动 ERNIE-Image-Turbo | 已下线[^13] |
| 即梦 API 文生图 2.1 | 下线中[^38] |
| Together 免费 FLUX.1 schnell | 已不在 Serverless API 上[^233] |
| Hugging Face 免费推理额度 | 免费账户不再送，官方文档的修改 2026-10-07 合并[^234]；现在只有 PRO（\$9/月）含 \$2 额度[^128][^235] |
| GitHub Models | 2026-07-30 完全退役[^236] |
| 魔搭 API-Inference "每天 2000 次" | 现行文档里已经没有，改成按魔粒扣[^14] |
| Grok Imagine 免费档 | 2026-03-19 起取消（第三方）[^100] |
| OpenRouter 免费出图模型 | 没有：10-21 调它的模型列表接口，63 个出图模型都没有 `:free` 版本，单价都不是 0（实测） |
| Pollinations 新接口免 key 出图 | 已不行，要 API key（10-21 实测） |

## 14. 待确认

- 火山方舟每个 Seedream 模型送几张（只在控制台显示）。
- 千问、豆包、可灵、即梦 App 每天能免费生几张图（官方都没公布）。
- 可灵每张图扣多少灵感值、智谱清言每张扣多少积分、魔搭每个模型具体扣几个魔粒（官方只说 1–2）。
- Ideogram 官方 API 的单价（页面动态加载，没抓到；第 7 节给了第三方数字）、Leonardo 的 API 单价。
- 模力方舟、无问芯穹、七牛 Nano Banana 的单价。
- 天工、夸克、WPS 灵犀、美图设计室、堆友每天免费几次。
- Draw Things 免费档每天能用几次。
- 商汤 SenseNova 公测什么时候结束、正式价多少。
- 微软 MAI-Image 每张图折合多少钱（每张的 token 数没公布）。

## 附录：国内网络连通性实测

测试时间是 10-20 晚和 10-21 上午，在中国大陆网络下用 curl 先直连；直连不通的，再走代理试一次。结果只代表测试时的这一个网络环境。

| 类别 | 直连能通 | 直连不通，走代理能通 | 都不通 / 被拒 |
| --- | --- | --- | --- |
| 国内网页 | 第 2 节所有平台 | — | — |
| 国内 API | 百炼、火山方舟、即梦 API、智谱、硅基流动、魔搭、MiniMax、商汤、七牛、优云智算、可灵、千帆、腾讯云、模力方舟 | — | — |
| 海外 API | Cloudflare、OpenRouter、Runware、fal、Replicate、Together、DeepInfra、Novita、WaveSpeed、Stability、Segmind、Prodia、Recraft、BFL、Z.ai、MiniMax 国际站、Runway、可灵国际版、Pollinations、Agnes、Puter、Pixazo | Luma、Ideogram（时通时断）、AI Horde（时通时断）、Gemini API、Vertex AI、Hugging Face（含 router） | Krea、302.AI；OpenAI、xAI 走代理返回 421 |
| 海外网页 | Microsoft Designer、Grok、Recraft、Dreamina、Lovart | Gemini、Google AI Studio、Google Labs、Copilot、SeaArt、Civitai、PixAI、Hugging Face | 直连返回 403：ChatGPT、Playground、Freepik、Midjourney 官网；走代理也 403：Meta AI、Ideogram 网页；都不通：NightCafe、Perchance、Raphael、Tensor.Art、Craiyon、Krea、Mage、Leonardo、Mistral |

## 参考来源

文中引用的页面如下，抓取时间为 2026-10-20 至 10-21。

[^1]: [ExchangeRate-API 开放汇率（2026-10-21 00:02 UTC 更新）](https://open.er-api.com/v6/latest/USD)
[^2]: [通义万相：会员订阅（定价页）](https://tongyi.aliyun.com/wan/pricing)
[^3]: [什么值得买：即梦每日赠送积分缩水时间线（第三方）](https://post.smzdm.com/p/ad793rex)
[^4]: [网易号·秋叶PPT：豆包正式收费了！但这6个功能免费无限次用](https://www.163.com/dy/article/L08MTNQL05169CIL.html)
[^5]: [北京商报：从请客到收费的千问（2026-08）](https://xinwen.bjd.com.cn/content/s6a7b472ae4b0e45f3fd5edcb.html)
[^6]: [钛媒体：文心升级、豆包收费](https://www.tmtpost.com/8041957.html)
[^7]: [魔搭：魔粒激励体系说明（官方文档源文件，2026-10-20 构建）](https://resouces.modelscope.cn/document/docdata/2026-10-20_18-23-CN/dist/magicube/intro/intro_CN.md)
[^8]: [魔搭：平台免费资源清单（官方文章，2026-08）](https://www.modelscope.cn/learn/1409)
[^9]: [LiblibAI 会员中心](https://www.liblib.art/viphome)
[^10]: [Draw Things Pricing](https://drawthings.ai/pricing)
[^11]: [Draw Things Wiki: Cloud Compute](https://wiki.drawthings.ai/wiki/Cloud_Compute)
[^12]: [智谱开放文档：CogView-3-Flash](https://docs.bigmodel.cn/cn/guide/models/free/cogview-3-flash)
[^13]: [硅基流动：模型广场（Kolors）](https://cloud.siliconflow.cn/open/models?target=Kwai-Kolors%2FKolors)
[^14]: [魔搭：API-Inference 使用限制（官方文档源文件，2026-10-20 构建）](https://resouces.modelscope.cn/document/docdata/2026-10-20_18-23-CN/dist/model-service/API-Inference/limits/limits_CN.md)
[^15]: [SenseTime：SenseNova U1.5 Lite 上线 Token Plan 公测（2026-09-11）](https://sensetime.com/en/news/sensenova-u1-5-lite-token-plan-20260911-1741)
[^16]: [Cloudflare Workers AI: Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing)
[^17]: [Agnes AI Wiki: Model Pricing](https://wiki.agnes-ai.com/en/docs/pricing)
[^18]: [MiniMax 开放平台：定价概览](https://platform.minimax.cn/docs/pricing/overview)
[^19]: [智谱开放平台：API 定价](https://docs.bigmodel.cn/cn/guide/start/pricing)
[^20]: [阿里云百炼：模型调用价格（图像生成）](https://help.aliyun.com/zh/model-studio/model-pricing)
[^21]: [百度千帆：模型服务计费](https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya)
[^22]: [火山方舟：模型价格](https://ark.volcengine.com/region:cn-beijing/docs/model-pricing.md)
[^23]: [火山方舟：模型发布公告](https://ark.volcengine.com/region:cn-beijing/docs/model-release-announcement)
[^24]: [Prodia Docs: Pricing](https://docs.prodia.com/reference/pricing)
[^25]: [Runware: FLUX.2 [klein] 4B](https://runware.ai/models/bfl-flux-2-klein-4b)
[^26]: [vdf.ai：开源生图模型许可证汇总（2026-10-14）](https://vdf.ai/blog/best-local-image-generation-models)
[^27]: [网信办：生成式人工智能服务已备案信息公告](https://www.cac.gov.cn/2026-05/13/c_1780413225190669.htm)
[^28]: [网信办等：《人工智能生成合成内容标识办法》](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)
[^29]: [Together AI Docs: Available models](https://docs.together.ai/docs/serverless/models)
[^30]: [硅基流动：模型价格](https://www.siliconflow.cn/pricing)
[^31]: [优云智算：模型 API 计费说明](https://compshare.cn/docs/modelverse/price)
[^32]: [Runware: Qwen-Image schema](https://runware.ai/docs/models/alibaba-qwen-image/schema.json)
[^33]: [硅基流动：上线阿里 Z-Image](https://www.siliconflow.cn/news/zab9zcwcqa2qe4gi5iy7z2pf)
[^34]: [fal: Z-Image Turbo](https://fal.ai/models/fal-ai/z-image/turbo)
[^35]: [Runware API: Z-Image-Turbo schema.json](https://runware.ai/docs/models/alibaba-z-image-turbo/schema.json)
[^36]: [WaveSpeedAI: Pricing](https://wavespeed.ai/pricing)
[^37]: [Pollinations：图像模型列表（API JSON）](https://gen.pollinations.ai/image/models)
[^38]: [火山引擎：即梦AI-图像生成计费说明](https://docs.volcengine.com/docs/JimengAI/JimengAI-imagegenerationbillinginstructions)
[^39]: [七牛云：AI 大模型广场](https://www.qiniu.com/ai/models)
[^40]: [腾讯云 TokenHub：模型价格](https://cloud.tencent.com/document/product/1823/130055)
[^41]: [OpenRouter: Image models](https://openrouter.ai/collections/image-models)
[^42]: [可灵 AI 开放平台：API 价格](https://klingai.com/dev/pricing)
[^43]: [Kling AI API Pricing（国际版，图片）](https://klingai.com/global/dev/model/image)
[^44]: [硅基流动 API 参考：创建图片生成请求](https://api-docs.siliconflow.cn/docs/api/images-generations-post)
[^45]: [新浪财经：腾讯混元发布混元图像 3.5 预览版（2026-09-22）](https://finance.sina.com.cn/stock/t/2026-09-22/doc-inistrnx1775920.shtml)
[^46]: [百度千帆：图像生成模型价格](https://cloud.baidu.com/doc/qianfan-multimodal/s/mmmt5xhbv)
[^47]: [Z.ai: Pricing](https://docs.z.ai/guides/overview/pricing)
[^48]: [MiniMax API Docs: Pricing Overview](https://platform.minimax.io/docs/pricing/overview)
[^49]: [SenseNova AI API docs](https://platform.sensenova.ai/docs)
[^50]: [Gemini Developer API: Pricing（markdown 版）](https://ai.google.dev/gemini-api/docs/pricing.md.txt)
[^51]: [七牛云：文生图 API](https://developer.qiniu.com/aitokenapi/13166/text-to-image-api)
[^52]: [OpenAI API: Image generation](https://developers.openai.com/api/docs/guides/image-generation)
[^53]: [xAI Docs: Grok Imagine Image](https://docs.x.ai/developers/models/grok-imagine-image)
[^54]: [xAI Docs: grok-imagine-image-2.0](https://docs.x.ai/developers/models/grok-imagine-image-2.0)
[^55]: [Microsoft Tech Community: MAI-Image-2.6](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/mai-image-2-6-and-mai-image-2-6-flash-quality-and-speed-at-production-scale/4550970)
[^56]: [Bing Image Creator FAQ](http://www.bing.com/images/create/ai-image-generator/faq)
[^57]: [Microsoft Learn: Use MAI-Image models in Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-mai-image?tabs=python)
[^58]: [Black Forest Labs API: Pricing](https://docs.bfl.ai/quick_start/pricing)
[^59]: [BFL Help: What are the costs associated with using your models](https://help.bfl.ai/articles/7986977817-what-are-the-costs-associated-with-using-your-models)
[^60]: [新浪科技：实测千问 App 生图、生视频（2025-12-02）](https://finance.sina.com.cn/tech/roll/2025-12-02/doc-infzmppc0200858.shtml)
[^61]: [DoNews：千问推出收费版本（2026-08-11）](https://www.donews.com/news/detail/1/6665859.html)
[^62]: [App Store：千问 - 阿里AI助手（内购列表）](https://apps.apple.com/cn/app/%E5%8D%83%E9%97%AE-%E9%98%BF%E9%87%8Cai%E5%8A%A9%E6%89%8B/id6466733523)
[^63]: [什么值得买：即梦每日免费积分被曝缩水（第三方）](https://post.smzdm.com/p/a5rgd6pk)
[^64]: [21经济网：豆包专业版发布（2026-06-24）](https://www.21jingji.com/article/20260624/herald/c579e97b948a6d0fd1588bffad3c94ee.html)
[^65]: [百度文心助手首页](https://wenxin.baidu.com)
[^66]: [IT之家：文心一言官网入口升级（2026-06）](https://www.ithome.com/0/968/360.htm)
[^67]: [可灵 AI：会员计划（国内版）](https://app.klingai.com/cn/membership/membership-plan)
[^68]: [白嫖计：可灵 AI 免费额度（核实于 2026-08-06，第三方）](https://baipiaoji.com/tools/kling)
[^69]: [BigoLab：可灵 AI 使用指南（第三方）](https://bigolab.com/guides/2290-kling-ai-how-to)
[^70]: [智谱清言：双节活动公告](https://chatglm.cn/apps)
[^71]: [三文阁：实测海螺 AI（第三方，2026-06）](https://www.sanwenge.com/post/1133.html)
[^72]: [海螺AI 官方微博（2026-02-26）](https://www.sina.cn/news/detail/5270573464683042.html)
[^73]: [讯飞星火文档：AI绘画](https://xinghuo.xfyun.cn/doc/spark-guide/AI%E7%BB%98%E7%94%BB.html)
[^74]: [提效路：讯飞星火 AI 绘画评测（第三方）](https://www.tixiaolu.com/v2/posts/v2-b63f275f.html)
[^75]: [AI工具集：WHEE（第三方，未标日期）](https://ai-bot.cn/sites/2976.html)
[^76]: [美图 WHEE 会员服务协议](https://www.whee.com/agreement/vip-service.html)
[^77]: [AI工具集：吐司 TusiArt（第三方，2025 年资料）](https://ai-bot.cn/tusiart)
[^78]: [吐司 Tusi.cn - App Store（订阅说明）](https://apps.apple.com/cn/app/%E5%90%90%E5%8F%B8tusi-cn-ai%E6%A8%A1%E5%9E%8Bart%E5%9C%A8%E7%BA%BF%E7%94%9F%E5%9B%BE%E7%BB%98%E7%94%BBcomfy/id6458545837)
[^79]: [App Store：纳米AI（360）](https://apps.apple.com/cn/app/%E7%BA%B3%E7%B1%B3ai-%E4%BD%A0%E7%9A%84%E4%B8%93%E5%B1%9E%E8%B6%85%E7%BA%A7%E6%99%BA%E8%83%BD%E4%BD%93/id6737763506)
[^80]: [堆友 AI 反应堆](https://d.design/ai/video)
[^81]: [商汤秒画 SenseMirage 官网](https://miaohua.sensetime.com)
[^82]: [三文阁：商汤秒画评测（第三方）](https://www.sanwenge.com/post/1154.html)
[^83]: [天工 App - App Store](https://apps.apple.com/cn/app/%E5%A4%A9%E5%B7%A5/id6447616432)
[^84]: [太平洋电脑网：夸克 AI 生图教程](https://www.pconline.com.cn/ai/1933/19333212.html)
[^85]: [美图设计室 - App Store（内购列表）](https://apps.apple.com/cn/app/%E7%BE%8E%E5%9B%BE%E8%AE%BE%E8%AE%A1%E5%AE%A4-%E8%AE%A9%E5%95%86%E4%B8%9A%E8%AE%BE%E8%AE%A1-%E5%A5%BD%E7%9C%8B%E5%8F%88%E8%A7%81%E6%95%88/id875654777)
[^86]: [WPS AI 办公（灵犀）](https://x.wps.cn/lingxi)
[^87]: [星流 AI 官网（停运公告）](https://www.xingliu.art)
[^88]: [搜狐：星流停止运营、迁移至 Lovart（转述官方公告）](https://www.sohu.com/a/1076951619_121124728)
[^89]: [快手可图官网（关停公告）](https://kolors.kuaishou.com)
[^90]: [Microsoft Designer（FAQ）](https://www.microsoft.com/en-us/microsoft-365/microsoft-designer)
[^91]: [ChatGPT Pricing](https://chatgpt.com/pricing)
[^92]: [OpenAI Help: ChatGPT Free Tier FAQ](https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq)
[^93]: [Gemini Apps Help：用量限制](https://support.google.com/gemini/answer/16275805?co=GENIE.Platform%3DDesktop&hl=en)
[^94]: [Gemini Apps Help：生成和编辑图片](https://support.google.com/gemini/answer/14286560?co=GENIE.Platform%3DDesktop&hl=en-JM)
[^95]: [Gemini API Pricing（网页版）](https://ai.google.dev/gemini-api/docs/pricing)
[^96]: [Gemini API: Available regions](https://ai.google.dev/gemini-api/docs/available-regions)
[^97]: [Meta AI：AI image generator](https://www.meta.ai/ai-image-generator)
[^98]: [Meta Help: Imagine with Meta AI](https://www.meta.com/help/artificial-intelligence/1337455336906126)
[^99]: [Goongen：Is Grok Imagine Still Free in 2026?（第三方）](https://goongen.ai/blog/is-grok-imagine-free)
[^100]: [Sloane：Grok Imagine free vs premium 2026（第三方）](https://www.sloane.world/guides/grok-imagine-free-vs-premium-2026)
[^101]: [Grok Plans](https://grok.com/plans)
[^102]: [Leonardo.Ai Pricing](https://www.leonardo.ai/pricing)
[^103]: [Leonardo.Ai Docs: Pricing and Plans FAQ](https://docs.leonardo.ai/docs/pricing-and-plans-faq.md)
[^104]: [Ideogram Docs: Plans and Credits](https://docs.ideogram.ai/plans-and-billing/available-plans.md)
[^105]: [Adobe Firefly: Plans](https://www.adobe.com/products/firefly/plans.html)
[^106]: [Dreamina: Free Credits FAQ](https://dreamina.capcut.com/ai-video/free-image-to-video-generator-credits-faq)
[^107]: [Dreamina: Best free AI generation tools 2026](https://dreamina.capcut.com/ai-video/best-free-ai-generation-tools-2026)
[^108]: [Kling AI: Credits Policy](https://kling.ai/docs/point-policy)
[^109]: [NightCafe Help: Free credits questions](https://help.nightcafe.studio/portal/en/kb/articles/free-credits-questions)
[^110]: [NightCafe Creator](https://creator.nightcafe.studio)
[^111]: [SeaArt: Daily Rewards](https://www.seaart.ai/post)
[^112]: [SeaArt Docs: Pricing and Credits](https://docs.seaart.ai/guide-1/getting-started/pricing-and-credits)
[^113]: [Creamify: SeaArt Review（第三方）](https://www.creamify.ai/blog/seaart-review)
[^114]: [Scrutool：TensorArt AI Review 2026（第三方）](https://www.scrutool.com/review/tensorart-ai)
[^115]: [Civitai Education: Guide to Buzz](https://education.civitai.com/civitais-guide-to-on-site-currency-buzz-%E2%9A%A1)
[^116]: [PixAI: Sign Up](https://pixai.art/en/sign-up)
[^117]: [Knowara：Perchance AI Review 2026（第三方）](https://knowara.com/ai-tools/image/perchance-ai-review)
[^118]: [Raphael AI 官网](https://raphael.app)
[^119]: [Craiyon Pricing](https://www.craiyon.com/en/pricing)
[^120]: [Magnific（原 Freepik AI）Docs: Plans and pricing](https://www.magnific.com/ai/docs/plans-and-pricing)
[^121]: [Recraft Docs: Free plan](https://www.recraft.ai/docs/plans-and-billing/free-plan)
[^122]: [Recraft: Pricing and plans](https://www.recraft.ai/pricing)
[^123]: [Playground Help: Free plan limits](https://help.playgroundai.com/en/articles/11434147-what-are-the-limits-on-the-free-plan)
[^124]: [Mistral AI: Pricing](https://mistral.ai/pricing)
[^125]: [OpenArt Pricing（legacy 页）](https://openart.ai/legacy/pricing)
[^126]: [Midjourney Docs: Comparing Midjourney Plans](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans)
[^127]: [Hugging Face Docs: Spaces ZeroGPU（源文件）](https://github.com/huggingface/hub-docs/blob/main/docs/hub/spaces-zerogpu.md)
[^128]: [Hugging Face: Pricing](https://huggingface.co/pricing)
[^129]: [vmake.ai：ImageFX Review（第三方）](https://vmake.ai/blog/imagefx-ai-image-generator-review)
[^130]: [Google Flow: About](https://labs.google/flow/about)
[^131]: [智谱开放平台 API 参考：图像生成](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90)
[^132]: [智谱开放平台：速率限制](https://docs.bigmodel.cn/cn/api/rate-limit)
[^133]: [hermes-plugin-free-image-gen（第三方实测）](https://github.com/ulysis6/hermes-plugin-free-image-gen)
[^134]: [硅基流动文档：Rate Limits](https://docs.siliconflow.cn/docs/userguide/faqs/rate-limit-and-upgradation)
[^135]: [硅基流动：推荐官计划](https://www.siliconflow.cn/developer-talk/od7wj9rr23p95uhihmhrombp)
[^136]: [硅基流动：产品更新日志](https://docs.siliconflow.cn/docs/release-notes/overview)
[^137]: [魔搭：API-Inference 介绍（官方文档源文件，2026-10-20 构建）](https://resouces.modelscope.cn/document/docdata/2026-10-20_18-23-CN/dist/model-service/API-Inference/intro/intro_CN.md)
[^138]: [Cloudflare Workers AI: flux-1-schnell 模型页](https://developers.cloudflare.com/workers-ai/models/flux-1-schnell)
[^139]: [Pollinations (GitHub)](https://github.com/pollinations/pollinations)
[^140]: [Pollinations.ai 官网](https://pollinations.ai)
[^141]: [Pollinations API 文档](https://enter.pollinations.ai/api/docs)
[^142]: [AI Horde (GitHub)](https://github.com/Haidra-Org/AI-Horde)
[^143]: [AI Horde 文档：kudos](https://github.com/Haidra-Org/haidra-assets/blob/main/docs/kudos.md)
[^144]: [Puter.js Docs: User-Pays Model](https://docs.puter.com/user-pays-model)
[^145]: [Puter: Free, Unlimited Image Generation API](https://developer.puter.com/tutorials/free-unlimited-image-generation-api)
[^146]: [Pixazo: Free AI APIs](https://www.pixazo.ai/api/free)
[^147]: [阿里云百炼：新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)
[^148]: [火山方舟：免费推理额度](https://ark.volcengine.com/region:cn-beijing/docs/free-inference-quota)
[^149]: [第三方汇总：Doubao-Seedream-4.0 免费额度](https://buguoshixc.github.io/ai-deals-aggregator/deal/7f8c32f6a327)
[^150]: [第三方汇总：Doubao-Seedream-5.0-lite 免费额度](https://buguoshixc.github.io/ai-deals-aggregator/deal/d6aaee8c7379)
[^151]: [腾讯云 TokenHub：免费体验额度](https://cloud.tencent.com/document/product/1823/130053)
[^152]: [腾讯混元（旧平台）：混元生图计费概述](https://cloud.tencent.com/document/product/1729/105925)
[^153]: [百度千帆：新用户免费额度](https://cloud.baidu.com/doc/qianfan/s/Imi2rpirg)
[^154]: [Stability AI Platform: Pricing](https://platform.stability.ai/pricing)
[^155]: [Runware: Pricing](https://runware.ai/pricing)
[^156]: [Novita AI 注册页](https://novita.ai/zh/user/register)
[^157]: [fal Docs: Model APIs FAQ](https://fal.ai/docs/documentation/model-apis/faq)
[^158]: [Replicate: Try for free](https://replicate.com/collections/try-for-free)
[^159]: [Replicate Docs: Prepaid credit](https://replicate.com/docs/topics/billing/prepaid-credit)
[^160]: [Together AI Docs: Credits](https://docs.together.ai/docs/billing-credits)
[^161]: [DeepInfra: FLUX-1-schnell 模型元数据](https://api.deepinfra.com/models/black-forest-labs/FLUX-1-schnell)
[^162]: [ModelsLab Pricing](https://modelslab.com/pricing.md)
[^163]: [阿里云百炼：通义万相文生图 V2 API 参考](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
[^164]: [火山方舟：图片生成 API](https://ark.volcengine.com/region:cn-beijing/docs/image-generation-api)
[^165]: [MiniMax 开放平台：文生图 API](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i)
[^166]: [硅基流动模型广场：Qwen-Image](https://cloud.siliconflow.cn/open/models?target=Qwen%2FQwen-Image)
[^167]: [硅基流动：上线 ERNIE-Image-Turbo](https://www.siliconflow.cn/news/t9hvfusja8yijr3k61gz7c6r)
[^168]: [优云智算：模型 API 快速开始](https://www.compshare.cn/docs/modelverse/models/quick-start)
[^169]: [302.AI：Z-Image-Turbo](https://302.ai/product/detail/z-image-turbo)
[^170]: [302.AI 帮助中心：API 价格](https://help.302.ai/docs/API-jia-ge-dY9X)
[^171]: [模力方舟文档：文生图](https://ai.gitee.com/docs/products/apis/images-vision/text2image)
[^172]: [模力方舟：Serverless API](https://ai.gitee.com/docs/products/apis)
[^173]: [无问芯穹 GenStudio：图片生成 API](https://docs.infini-ai.com/gen-studio/api/multimodal/image-generation.html)
[^174]: [Runware: FLUX.2 [klein] 9B](https://runware.ai/models/bfl-flux-2-klein-9b)
[^175]: [Runware API: FLUX.1 [schnell] schema.json](https://runware.ai/docs/models/bfl-flux-1-schnell/schema.json)
[^176]: [Runware: SDXL schema](https://runware.ai/docs/models/stabilityai-stable-diffusion-xl-v1-0-vae-fix/schema.json)
[^177]: [Runware Docs: Pricing](https://runware.ai/docs/platform/pricing)
[^178]: [Runware: Z-Image-Turbo 模型页](https://runware.ai/models/z-image-turbo)
[^179]: [Runware: Qwen-Image 模型页](https://runware.ai/models/alibaba-qwen-image)
[^180]: [fal: FLUX.1 [schnell]](https://fal.ai/models/fal-ai/flux/schnell)
[^181]: [fal: FLUX.2 [klein] 4B](https://fal.ai/models/fal-ai/flux-2/klein/4b/llms.txt)
[^182]: [fal: Pricing](https://fal.ai/pricing)
[^183]: [Replicate: Pricing](https://replicate.com/pricing)
[^184]: [Replicate: black-forest-labs/flux-schnell](https://replicate.com/black-forest-labs/flux-schnell)
[^185]: [Novita AI Docs: FLUX.1 [schnell]](https://novita.ai/docs/api-reference/model-apis-flux-1-schnell)
[^186]: [Segmind Blog: The Cheapest AI Image Generation API（2026-04）](https://blog.segmind.com/the-cheapest-ai-image-generation-api-for-developers-in-2026)
[^187]: [Segmind Pricing](https://www.segmind.com/pricing)
[^188]: [Recraft API: Pricing](https://www.recraft.ai/docs/api-reference/pricing)
[^189]: [Black Forest Labs: Pricing](https://bfl.ai/pricing)
[^190]: [Runway API: Pricing & Costs](https://docs.dev.runwayml.com/guides/pricing)
[^191]: [Krea Docs: Krea 2 API](https://www.krea.ai/docs/developers/krea-2/overview)
[^192]: [Luma AI: API（Uni-1.1）](https://lumalabs.ai/api)
[^193]: [Luma Photon（2024）](https://lumalabs.ai/photon)
[^194]: [Ideogram: API Pricing](https://about.ideogram.ai/api-pricing)
[^195]: [UsagePricing：Ideogram P-Image 上线（2026-08-04）](https://usagepricing.com/blueprint/activity/ideogram-2026-08-04-p-image-price-floor)
[^196]: [Artificial Analysis：文生图开放权重排行榜（第三方）](https://artificialanalysis.ai/image/leaderboard/text-to-image/open-weights?tab=table)
[^197]: [OpenAI Docs: gpt-image-2.5-flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare.md)
[^198]: [Gemini API 价格（中文页）](https://ai.google.dev/gemini-api/docs/pricing?hl=zh-cn)
[^199]: [Google Cloud: Generative AI pricing（Vertex）](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)
[^200]: [Gemini API: Imagen](https://ai.google.dev/gemini-api/docs/imagen)
[^201]: [Midjourney: Enterprise API survey](https://www.midjourney.com/updates/enterprise-api-survey)
[^202]: [TL Dev Tech：Midjourney 开放 MCP 小范围测试（第三方）](https://www.tldevtech.com/midjourney-finally-lets-agents-in-on-its-terms)
[^203]: [Microsoft AI: Introducing MAI-Image-2.5](https://microsoft.ai/news/introducing-mai-image-2-5)
[^204]: [ComfyUI (GitHub)](https://github.com/Comfy-Org/ComfyUI)
[^205]: [SwarmUI (GitHub)](https://github.com/mcmonkeyprojects/SwarmUI)
[^206]: [Forge Neo — sd-webui-forge-classic neo 分支 (GitHub)](https://github.com/Haoming02/sd-webui-forge-classic)
[^207]: [Pinggy: Best Open-Source AI Image Models to Self-Host in 2026（第三方）](https://pinggy.io/blog/best_free_open_source_ai_image_generators_to_self_host)
[^208]: [InvokeAI (GitHub)](https://github.com/invoke-ai/InvokeAI)
[^209]: [Invoke — About](https://invoke.ai/about)
[^210]: [SD.Next (GitHub)](https://github.com/vladmandic/sdnext)
[^211]: [Krita AI Diffusion (GitHub)](https://github.com/Acly/krita-ai-diffusion)
[^212]: [Mochi Diffusion (GitHub)](https://github.com/MochiDiffusion/MochiDiffusion)
[^213]: [mflux (GitHub)](https://github.com/mflux-community/mflux)
[^214]: [stable-diffusion.cpp (GitHub)](https://github.com/leejet/stable-diffusion.cpp)
[^215]: [draw-things-community (GitHub)](https://github.com/drawthingsai/draw-things-community)
[^216]: [AUTOMATIC1111 stable-diffusion-webui (GitHub)](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
[^217]: [原版 Forge (GitHub)](https://github.com/lllyasviel/stable-diffusion-webui-forge)
[^218]: [Fooocus (GitHub)](https://github.com/lllyasviel/Fooocus)
[^219]: [DiffusionBee (GitHub)](https://github.com/divamgupta/diffusionbee-stable-diffusion-ui)
[^220]: [InsiderLLM: Stable Diffusion on Mac — MLX and Draw Things（第三方）](https://insiderllm.com/guides/stable-diffusion-mac-mlx)
[^221]: [Draw Things: Quantify Z-Image Turbo Efficiency](https://releases.drawthings.ai/p/quantify-z-image-turbo-efficiency)
[^222]: [Draw Things Wiki: How Powerful Is My Device](https://wiki.drawthings.ai/wiki/How_Powerful_Is_My_Device)
[^223]: [Draw Things Downloads / 更新日志](https://drawthings.ai/downloads)
[^224]: [Draw Things Cloud Compute API 控制台](https://api.drawthings.ai/dashboard)
[^225]: [Draw Things 开源代码：ComputeUnits.swift（免费版默认上限）](https://github.com/drawthingsai/draw-things-community/blob/main/Libraries/ModelZoo/Sources/ComputeUnits.swift)
[^226]: [Draw Things Wiki: Glossary（Lab Hours）](https://wiki.drawthings.ai/wiki/Glossary)
[^227]: [Draw Things: Privacy Pass and Draw Things+ Cloud Compute](https://releases.drawthings.ai/p/privacy-pass-and-draw-things-cloud)
[^228]: [Draw Things: Harvest Season（2026-10-15）](https://releases.drawthings.ai/p/harvest-season-new-hardware-new-inference)
[^229]: [BFL Blog: FLUX 3 Image Klein（开放权重）](https://bfl.ai/blog/flux-3-image-klein)
[^230]: [Black Forest Labs Docs: FLUX.2 Overview](https://docs.bfl.ai/flux_2)
[^231]: [阶跃星辰：图像模型下线公告](https://platform.stepfun.com/docs/zh/announcements/image-model-retirement)
[^232]: [Amazon Bedrock: Nova Canvas model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-canvas.html)
[^233]: [Together AI: FLUX.1 [schnell] Free（已不在 Serverless API）](https://www.together.ai/models/flux-1-schnell)
[^234]: [huggingface/hub-docs PR #2865：免费用户不再含每月额度（2026-10-07 合并）](https://github.com/huggingface/hub-docs/pull/2865)
[^235]: [Hugging Face: Inference Providers Pricing](https://huggingface.co/docs/inference-providers/en/pricing)
[^236]: [GitHub Docs: GitHub Models](https://docs.github.com/en/github-models)
