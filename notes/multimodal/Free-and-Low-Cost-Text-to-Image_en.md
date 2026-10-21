# Free and Low-Cost Text-to-Image: Web Apps, APIs, Local Software and Compliance

[中文](./Free-and-Low-Cost-Text-to-Image.md) | English

- **Research date**: 2026-10-21 (prices and quotas captured 2026-10-20 to 10-21)
- **Scope**: free or low-cost text-to-image services in China and abroad: free quotas and membership tiers of websites and apps, free APIs with call examples, new-user credits, pay-per-image APIs, open-source local software, the Draw Things cloud free tier, licenses of open models, and the labeling and filing rules for launching in China.
- **Basis**: data comes from official pages: pricing pages, docs, terms, announcements, official APIs and open-source repositories; where the vendor publishes nothing, media reports, reviews or user reports fill the gap and are marked "(third party)". Superscript numbers at the end of a sentence are citations, matching the references at the end. Content marked "(tested)" is the result of hands-on use, actual calls or connectivity tests on 2026-10-20 to 10-21; "(converted)" is calculated from official unit prices or exchange rates; "(inferred)" is inferred from the cited sources.
- **Test environment**: a network in mainland China. "Direct" in the tables means without a proxy: ✓ connects; ✗ does not connect, usually needs a proxy; 403 means it connects but the site refuses.
- **Units**: prices are official list prices, without limited-time discounts. USD is converted at 1 USD ≈ 6.69 yuan (2026-10-21 rate)[^1].
- **Freshness**: free quotas, membership benefits and prices change quickly; check the official site before paying.

## Start Here: Pick by Need

| Need | Try these first | Notes |
| --- | --- | --- |
| No coding, free image generation in China | Tongyi Wanxiang (Wan) web version[^2], Jimeng AI[^3], Doubao[^4], Tencent Yuanbao[^5], Wenxin Assistant[^6] | All reachable via direct connection; Yuanbao has explicitly said it has no plans to charge for now, and most of the others don't publish how many free uses they give per day |
| Use large open-source models for free (Qwen-Image, Z-Image, etc.) | ModelScope AIGC zone[^7][^8], LiblibAI[^9] | Moli points / credits for logging in each day |
| Mac / iPhone users | Draw Things Cloud free tier[^10][^11] | Runs large models your device can't handle on the official servers; see section 10 |
| Free APIs from Chinese vendors | Zhipu CogView-3-Flash[^12], SiliconFlow Kolors[^13], ModelScope API-Inference[^14], SenseTime SenseNova U1.5 Lite (during public beta)[^15] | All reachable via direct connection; see section 4 |
| Free APIs outside China but reachable directly from China | Cloudflare Workers AI[^16], Agnes AI (\$0 for a limited time)[^17], Pollinations legacy API (tested) | Cloudflare: about 173 FLUX.1 schnell images per day (converted) |
| Cheapest paid APIs in China | MiniMax image-01 0.025 yuan[^18], Zhipu CogView-4 Batch 0.03 yuan[^19], Tongyi Wanxiang wanx2.0-t2i-turbo 0.04 yuan[^20], Baidu musesteamer-air-image 0.05 yuan[^21] | All prices are per image |
| Balancing quality and price (China) | Doubao Seedream 5.0 flash 0.12 yuan[^22] | The vendor says its capabilities are exactly the same as 5.0 pro, just faster and cheaper[^23] |
| Cheapest paid APIs outside China | Prodia FLUX.2 Klein 4B \$0.0005[^24], Runware FLUX.2 [klein] 4B \$0.0006[^25] | About 0.003–0.004 yuan per image (converted) |
| Commercial use and self-hosting | Z-Image-Turbo, FLUX.2 [klein] 4B, ERNIE-Image, Qwen-Image-2512, all Apache 2.0[^26] | See section 11 |
| Offering image generation to the public in China | Call the API of a model that has completed filing, register with the local office of the Cyberspace Administration of China (CAC), and add AI labels to the images[^27][^28] | See section 12 |

## 1. Brand ↔ API Model Mapping

Brand names in apps often don't match the model names in API docs; use this table to look them up by brand.

| Brand | Vendor | API model ID | Where to call it |
| --- | --- | --- | --- |
| Tongyi Wanxiang (Wan) | Alibaba | wan2.6-t2i, wan2.5-t2i-preview, wan2.2-t2i-flash / plus, wanx2.1-t2i-turbo / plus, wanx2.0-t2i-turbo, wanx-v1; for generation and editing: wan2.7-image / pro, wan2.6-image[^20] | Alibaba Cloud Bailian; Together also has Wan 2.6 Image[^29] |
| Qwen (image generation in the app) | Alibaba | qwen-image-3.0 / pro, qwen-image-2.1-pro / turbo, qwen-image-2.0 / pro[^20] | Bailian; SiliconFlow[^30], Qianfan[^21], Compshare[^31], Runware[^32] and Together[^29] also offer Qwen-Image |
| Z-Image (open source) | Alibaba Tongyi Lab | z-image-turbo[^20] | Bailian, SiliconFlow[^33], fal[^34], Runware[^35], WaveSpeed[^36], Pollinations[^37] |
| Doubao / Jimeng AI | ByteDance | doubao-seedream-5-0-pro / flash / lite, 4-5, 4-0[^22]; Jimeng AI API: Text-to-Image 3.0 / 3.1, Image Generation 4.0 / 4.6[^38] | Volcano Ark, Volcano Engine; Qiniu[^39], TokenHub[^40], Compshare[^31] and OpenRouter[^41] also resell it |
| Kling | Kuaishou | Kling Image 2.1, 3.0, 3.0-omni, O1[^42] | Kling Open Platform (the international version has separate USD prices[^43]); Bailian[^20], TokenHub and Qiniu also resell it |
| Kolors (open source) | Kuaishou | Kwai-Kolors/Kolors[^44] | SiliconFlow, free for a limited time[^13] |
| Hunyuan (image generation in Yuanbao) | Tencent | Hy-Image-3.5-preview, Hy-Image-3.0[^40] | Tencent Cloud TokenHub (Yuanbao has integrated Hunyuan Image 3.5[^45]) |
| MuseSteamer | Baidu | musesteamer-air-image[^21], qianfan-image (the docs mark it "internal use")[^46] | Baidu Qianfan; the model Wenxin Assistant uses for image generation has not been disclosed |
| Wenxin ERNIE-Image (open source) | Baidu | ERNIE-Image, ERNIE-Image-Turbo | Apache 2.0, can run locally[^26]; SiliconFlow has taken it offline[^13] |
| Zhipu | Zhipu | CogView-3-Flash (free), CogView-4, GLM-Image[^19] | Zhipu Open Platform; international site Z.ai[^47] |
| Hailuo | MiniMax | image-01, image-01-live[^18] | MiniMax Open Platform (international site[^48]) |
| SenseTime | SenseTime | sensenova-u1.5-lite, sensenova-u1.5-fast[^49] | SenseNova platform |
| Vidu | ShengShu | vidu/viduq2-fast_reference2image and others (reference-to-image)[^20]; Vidu-Image-q2 (text-to-image)[^40] | Bailian, TokenHub |
| Nano Banana (Gemini image generation) | Google | gemini-nano-banana-2.1, gemini-3.1-flash-image (Nano Banana 2), gemini-3.1-flash-lite-image (Nano Banana 2 Lite)[^50] | Gemini API; Qiniu also lists gemini-2.5-flash-image[^51] |
| GPT Image | OpenAI | gpt-image-2.5-flare, gpt-image-2, and the older GPT Image 1 / 1.5 / 1 Mini[^52] | OpenAI API |
| Grok Imagine | xAI | grok-imagine-image, grok-imagine-image-2.0[^53][^54] | xAI API |
| MAI-Image | Microsoft | MAI-Image-2.6, MAI-Image-2.6-Flash[^55]; Bing image editing uses MAI-Image-2.5-Flash[^56] | Microsoft Foundry (requires an Azure subscription with a valid payment method attached[^57]) |
| FLUX | Black Forest Labs | FLUX 3 Image, FLUX 3 Klein, FLUX.2 [klein] 4B / 9B[^58], FLUX.2 [pro] / [flex] / [max] and others[^59] | BFL API; hosted by Runware, fal, Prodia, Cloudflare and others |

## 2. Free Websites and Apps in China

All of the Chinese sites below are reachable via direct connection (tested).

### 2.1 Tongyi Wanxiang Web Version

- **Access**: tongyi.aliyun.com/wan/; the pricing page is at /wan/pricing.
- **Membership tiers[^2]**:

| Tier | Price | Inspiration points | Concurrent submissions | Other benefits |
| --- | --- | --- | --- | --- |
| Free | ¥0 | Given for daily check-ins (amount not stated) | 1 image task, 1 video task | 6 text-to-image style templates |
| Standard membership | List price ¥72/month; auto-renewing annual plan at 50% off, equivalent to ¥36/month; auto-renewing monthly plan listed at 35% off | 300/month, "accelerated generation of up to 1,200 images or 60 videos" | 3 image and 3 video tasks | Brand watermark removal, 1080p video, 10–30 second videos, all style templates |
| Premium membership | List price ¥288/month; auto-renewing annual plan equivalent to ¥145/month | 1,200/month, accelerated generation of up to 4,800 images or 240 videos | 5 image and 8 video tasks | Same as standard membership |

- Inspiration points are used to "speed up image and video generation"[^2]. The free tier lists "1 image task submitted at a time", so you can still generate images without spending inspiration points, just without acceleration (inferred). Taking 300 inspiration points for 1,200 accelerated images, that is about 0.25 inspiration points per image (converted).
- "Brand watermark removal for images and videos" is listed only among the membership benefits[^2], so images made on the free tier should carry the brand watermark (inferred).
- Memberships renew automatically and can be canceled at any time, but payments are non-refundable[^2].
- Membership can only be used on the tongyi.aliyun.com/wan website; the API has to be bought separately[^2]. For the API, see section 6.1.

### 2.2 Qwen App and Website

- **Access**: qianwen.com and the Qwen app.
- **Is image generation free**: in Sina Tech's hands-on test in 2025-12, Qwen's image generation was "maxed out: free, with no limit on uses", using a "specially supplied full-power Qwen-Image 2511"[^60]. How much is given per day now has not been officially published, and no newer reports were found.
- **What became paid in 2026-08[^61]**:
  - Office Assistant Pro membership: Advanced 19 yuan/month (200 yuan paid annually), Elite 49 yuan/month, Flagship 128 yuan/month;
  - Video generation has 10 free uses per day; beyond that you buy packs: 26 yuan for 10, 116 yuan for 50, 228 yuan for 100.
- **App Store in-app purchases[^62]**: Creation membership 7 days ¥10; Creation credits 200 for ¥20, 500 for ¥50; "Qwen Creation - Standard Membership" auto-renewing monthly plan ¥58, plus another tier at ¥48.

### 2.3 Jimeng AI

- **Access**: jimeng.jianying.com and the Jimeng AI app.
- **Free credits**: given for logging in each day, and cleared when they expire[^3].
- The amount given keeps changing; the user feedback below was compiled by a third party[^3].
  - In early August, a random 66–100 per day;
  - After that, users began reporting only 20 or 30 per day;
  - By September it had dropped to 10–30;
  - Customer service said "these are surprise credits, and they're random".
- **Membership**: basic membership gives 725 credits a month, which by sales-channel figures covers up to about 2,900 images or 72 videos, or about 0.25 credits per image (third party, not officially confirmed)[^63]. As for the basic membership price, one user paid 41 yuan when signing up in August[^63].
- Video is expensive: Seedance 2.5 costs about 26–29 credits per second (third party)[^63]. If you only generate images, membership credits are fairly ample.
- The Jimeng AI API is billed separately on Volcano Engine; see section 6.3.

### 2.4 Doubao

- **Access**: doubao.com and the Doubao app.
- The image model is Seedream 5.0, which supports text-to-image and image-to-image[^4].
- The free version can generate AI images and videos, "but with quota limits"; the number of uses has not been published[^4].
- Paid plans launched in 2026-06[^64].
  - Standard plan: 68 yuan on an auto-renewing monthly plan, 38 yuan with student verification, with more than 5 times the free version's quota;
  - Enhanced plan 200 yuan and Premium plan 500 yuan, with 4 times and 10 times the Standard plan's quota respectively.

### 2.5 Tencent Yuanbao

- **Access**: yuanbao.tencent.com and the Yuanbao app.
- Tencent told the media: "Yuanbao is currently completely free to use, and there are no plans to charge for now"[^5].
- Image generation uses Hunyuan Image 3.5; Hy Image 3.5 preview had been in staged-rollout testing in Yuanbao for about two months[^45].
- Regular users can use portrait editing, smart photo retouching, travel-planning images and knowledge infographics in Yuanbao for free; businesses and developers call it through the Tencent Cloud API[^45]. For the API, see section 6.5.

### 2.6 Wenxin Assistant (Formerly ERNIE Bot)

- **Access**: wenxin.baidu.com. The old Wenxin Yige site, yige.baidu.com, now redirects here too (tested).
- Baidu merged the ERNIE Bot web version, Wenxin (ERNIE) and Wenxin Assistant into Wenxin Assistant, and the pricing policy is to "stay free"[^6].
- The home page has an "Image generation" entry[^65].
- ERNIE Bot has been completely free since 2025-02-13, and the official website's entry for asking questions was upgraded as of 2026-06-25[^66].
- There is no official word on which model generates the images or how many generations you get per day.

### 2.7 Kling AI (China Version)

- **Access**: klingai.com, app.klingai.com.
- **Membership tiers**[^67] (new customers on Gold, Platinum and Diamond all get a 7-day trial at 70% off):

| Tier | 7-day trial | After the trial | Inspiration points / month | Price per 100 inspiration points |
| --- | --- | --- | --- | --- |
| Gold | ¥5.99 | 46 yuan for the first month, then 58 yuan/month | 660 | ¥6.97 |
| Platinum | ¥11.99 | 186 yuan for the first month, then 234 yuan/month | 3,000 | ¥6.20 |
| Diamond | ¥17.99 | 466 yuan for the first month, then 586 yuan/month | 8,000 | ¥5.83 |
| Black Gold | No trial; ¥916 for the first month (30% off the first purchase) | Then 1,149 yuan/month | 26,000 | ¥3.52 |

- Every membership tier includes: daily member inspiration points, unlimited concurrency, an exclusive fast lane, 1080p/4K video, brand watermark removal from works, and commercial use of generated content[^67].
- **Free users**: the membership page does not say how many points are given per day. A third-party source from August says non-members get 66 inspiration points a day for logging in, and that the terms of service state free-tier output cannot be used commercially[^68].
- Inspiration points bought separately cost 1 yuan per 10 and are non-refundable (third party)[^69].
- No official figure was found for how many inspiration points one image costs.

### 2.8 Zhipu Qingyan

- **Access**: chatglm.cn. Logging in with a phone number that has never been registered signs it up automatically[^70].
- You collect credits the first time you open it each day. During the Mid-Autumn and National Day holidays (9-25 to 10-07), credits are multiplied by 10: 2,000 for regular users, 4,000 for VIP, 8,000 for SVIP, expiring after 24 hours[^70]. Working back from this, a normal day gives about 200 / 400 / 800 (converted).
- From 10-08 to 10-31 there is also a rebate campaign: credits spent during the holidays are 100% returned, valid for 30 days after you claim them[^70].
- How many credits one image costs has not been published.

### 2.9 LiblibAI (Libulibu)

- **Access**: liblib.art, a community model site where you can pick community models and LoRAs.
- Free users get 20 credits a day for logging in, plus 3GB of cloud storage[^9].
- The entry-level plan is ¥429/year with 700 credits a month, enough for up to about 2,800 images or 87 videos[^9]. Subscription credits reset every 31 days[^9].
- Going by "700 credits for up to about 2,800 images", 20 credits a day is up to about 80 images (converted). Switching to a large model or a high resolution gives far fewer.

### 2.10 ModelScope AIGC Zone

- **Access**: modelscope.cn/aigc, Alibaba's open-source model community. You can use open-source models such as Qwen Image 2512, Z Image and Qwen Edit 2511 online[^8].
- **How to get Moli points**:
  - The official docs built on 10-20 say: 200 Moli points for logging in each day, plus another 50 for linking an Alibaba Cloud account[^7].
  - An official article from August says 150 a day after linking[^8]. The two disagree; go by the newer docs.
  - Each day, submitting works earns up to 200 more, and liking and commenting up to 50[^8].
  - Short-term Moli points are valid for 24 hours, long-term Moli points for 90 days[^7].
  - Before using Moli points you must complete your personal information, including a verified personal email address[^7].
- **How they are deducted**: 1–2 Moli points per image, 8–28 Moli points per video, and LoRA training is calculated dynamically from data volume and model[^8]. 250 Moli points a day is enough for about 125–250 images (converted).
- Moli points are shared with API-Inference[^7]. For the API, see section 4.3.

### 2.11 Hailuo AI

- **Access**: hailuoai.com, owned by MiniMax.
- The China version automatically grants 100 shells a day; they do not carry over, and failed generations are not refunded (third party)[^71]. Shells are deducted mainly by video specs; how many an image costs has not been published.
- There was a promotion in March: anyone who bought an annual plan at Standard tier or above before March 4 could generate images for a year with models such as Seedream 5.0 Lite, Quanneng Tupian pro and Youchuan V7 without spending credits[^72].

### 2.12 Other Chinese Platforms (Free Quotas Mostly Unpublished)

| Product | What is known |
| --- | --- |
| iFlytek Spark | Type "draw a picture of…" in the chat box to generate an image[^73]; a third party says that after signing up you get 100 free uses a day, up to 4 images each, and that paid plans are 29 yuan/month for 1,000 uses and 99 yuan/month for 5,000 uses[^74] |
| Meitu WHEE | New users get 20 Meidou, about 2 Meidou per image; membership is 52 yuan on an auto-renewing monthly plan, 142 yuan for a quarterly plan and 462 yuan for an annual plan, with 1,800 Meidou a month (third party)[^75]; Meidou granted with a membership are valid for that month and void once expired[^76] |
| Tusi | The free version gives 100 compute points a day, 1 queued task and up to 2 images per run (third party, 2025 data)[^77]; the app's auto-renewing monthly plan is 24.8 yuan[^78] |
| Nano AI (360) | "Generate images from a single sentence"; in-app purchases: 100 Nano credits for ¥10, VIP auto-renewing monthly plan ¥49[^79] |
| Duiyou (Alibaba) | Has a "Classic image generation" feature[^80]; the free quota has not been published |
| SenseTime SenseMirage | Uses the Artist v1.0 Alpha model[^81]; a third party says the official home page reads "AI painting, free"[^82] |
| Tiangong AI (Skywork) | The app can make slide decks (PPT), documents, spreadsheets, images and videos; in-app purchase: Basic auto-renewing monthly plan ¥45[^83] |
| Quark | The app has an "Image generation" entry above the search box[^84] |
| Meitu Design Studio | Geared toward e-commerce and poster design; VIP auto-renewing monthly plan ¥30[^85] |
| WPS Lingxi | The sidebar has "AI text-to-image"[^86] |

### 2.13 Discontinued

- **Xingliu AI**: ceased operations at 24:00 on 2026-10-10[^87]. An official text message recommends migrating to Lovart; each account can be migrated only once, and once the original platform shuts down, its content is permanently deleted and cannot be recovered[^88].
- **Kuaishou Kolors web version**: closed on 2024-08-23[^89]. The Kolors model can still be called for free on SiliconFlow[^13].

## 3. Free Websites and Apps Outside China

| Product | Free quota | Limits / commercial use | Paid plans from | Direct |
| --- | --- | --- | --- | --- |
| Bing Image Creator | 15 fast generations a day, then standard speed once they are used up; at most 200 prompts per 24 hours[^56] | Requires a personal Microsoft account; work/school Entra ID accounts cannot be used; image edits always use MAI-Image-2.5-Flash[^56] | Free | ✗ (redirects to cn.bing.com, then 404) |
| Microsoft Designer | A batch of credits is issued at the start of each month, and each AI use costs 1; how many free accounts get is not stated[^90] | Every image is boosted automatically[^90] | — | ✓ |
| ChatGPT Free | "Limited image creation"[^91] | Image generation and text chat have separate limits[^92] | — | 403 |
| Gemini App | Without a subscription you get "Standard limits", which refresh every 5 hours, plus a weekly cap[^93] | Generating images and videos uses up more of the quota[^93]; without a subscription you can only download at 1K, subscribers get 2K[^94] | — | ✗ |
| Google AI Studio | Free to use in available regions[^95] | Available regions exclude mainland China and Hong Kong[^96]; the same models have no free tier through the API[^50] | — | ✗ |
| Meta AI | Advertised as free[^97]; generates several images at a time[^98] | — | — | ✗ |
| Grok Imagine | 0 images for free accounts; the free tier was cancelled as of 2026-03-19 (third party)[^99][^100] | The lowest tier, SuperGrok Lite, only gets a "trial" of image and video generation[^101] | — | ✓ |
| Leonardo.Ai | 150 Fast Tokens a day[^102] | Moving from subscriptions to pay-as-you-go[^103] | — | ✗ |
| Ideogram | 30 credits a week; once they are used up, wait for the next week or buy more[^104] | Private generation and high-quality export require Plus[^104] | Plus \$20/month (\$15/month billed annually), 2,400 credits a month[^104] | ✗ (403 via a proxy) |
| Adobe Firefly | The free version gets a small number of generations a day; the number is not stated[^105] | Output from Adobe's own models can be used commercially[^105] | Standard \$9.99/month for 2,000 credits; paid tiers get unlimited standard image generation[^105] | ✗ (shows "Access denied") |
| Dreamina (international version of Jimeng AI) | 120 credits a day, shared between images and videos[^106] | Another official page says it is limited to "eligible U.S. web accounts"[^107] | — | ✓ |
| Kling AI international version | During promotions, daily login credits go only to subscribers and are cleared at 24:00 that day[^108] | \$1 = 66 credits[^108] | — | ✓ |
| NightCafe | Tops up 5 credits a day, given regardless of your balance[^109] | No card needed to sign up[^110] | — | ✗ |
| SeaArt | 130 Stamina a day, refreshed daily[^111][^112] | Enough for about 21 images, with 2 tasks running at the same time (third party)[^113] | — | ✗ |
| Tensor.Art | 50 credits a day; a standard image costs 0.36 credits, so about 138 images (third party)[^114] | Free-version works are stored for only 7 days[^114] | Pro \$9.90/month, 300 credits a day[^114] | ✗ |
| Civitai | 100 Blue Buzz for new users; you can claim once a day in the generator[^115] | Since 2025-05 you can no longer buy it directly with a credit card[^115] | — | ✗ |
| PixAI (anime-focused) | 10,000 free credits a day, no card required[^116] | — | — | ✗ |
| Perchance | No sign-up, no daily cap, no watermark (third party, 2026-04)[^117] | No paid tier[^117] | — | ✗ |
| Raphael AI | Basic mode needs no sign-up and has no usage limit; logging in gives daily credits and a 2K model[^118] | The basic model takes about 8 seconds per image, up to 4 images at a time[^118] | — | ✗ |
| Craiyon | Limited uses; text-only image generation does not cost credits[^119] | Commercial use allowed on any account; free users must give attribution[^119] | — | ✗ |
| Freepik (renamed Magnific in its docs) | Up to 20 uses a day (in-house models)[^120] | Personal use only; attribution required[^120] | — | 403 |
| Recraft | You can upload 3 reference images a day; each generation produces 2 images[^121] | Free-version works belong to Recraft, are shown publicly and cannot be used commercially[^122] | — | ✓ |
| Playground | Playground v3: 5 uses every 3 hours; GPT Image 2 / Seedream / Nano Banana: 3 uses a month combined[^123] | Only 2 designs can be downloaded per day[^123] | — | 403 |
| Mistral Le Chat | The free tier includes basic image generation and editing[^124] | The paid tier's image-generation quota is "up to 40 times the free one"[^124] | — | ✗ |
| OpenArt | Only 40 one-time trial credits, 4 parallel jobs, works kept private[^125] | — | Essential \$14/month[^125] | ✗ |
| Midjourney | The plans page lists no free tier[^126] | Stealth mode is available only on the Pro and Mega tiers[^126] | Basic \$10/month, 20% off billed annually[^126] | 403 |
| Hugging Face Spaces (ZeroGPU) | Anyone can use ZeroGPU Spaces for free[^127] | Daily GPU quota: 2 minutes without logging in, 5 minutes for free accounts, 40 minutes for PRO[^127] | PRO \$9/month[^128] | ✗ |
| Google Flow (formerly ImageFX) | The free tier has a monthly credit cap (third party)[^129] | Paid tiers have higher image-generation caps[^130] | — | ✗ |
| Draw Things Cloud | See section 10 | — | Draw Things+ \$8.99/month[^10] | ✓ (slow) |

## 4. Free APIs (with Call Examples)

Always set API keys as environment variables; never write them into code. The examples below are based on the official docs. Called without a key, all 5 endpoints (Zhipu, SiliconFlow, ModelScope, SenseTime and Cloudflare) return 401 (tested 10-21), which shows the addresses are reachable, but generating images with a real key has not been tested. The Pollinations example needs no key and produced an image in testing.

### 4.1 Zhipu CogView-3-Flash (In China, Direct Connection ✓)

- Officially designated as a free image generation model[^12][^19].
- Supports resolutions such as 1024x1024, 768x1344, 864x1152, 1344x768, 1152x864, 1440x720 and 720x1440[^12].
- The endpoint is open.bigmodel.cn/api/paas/v4/images/generations[^131] and the model name is cogview-3-flash[^12].
- Rate limits are tied to the user's benefit level[^132]; the maximum number of images per day has not been published.
- Third-party test: images carry a dark rounded-corner "AI-generated" label in the bottom-right corner[^133].
- Pros: a Chinese vendor, free, and reachable by direct connection; cons: average image quality (opinion).

```bash
curl https://open.bigmodel.cn/api/paas/v4/images/generations \
  -H "Authorization: Bearer $ZHIPU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "cogview-3-flash", "prompt": "an orange cat sitting on a windowsill", "size": "1024x1024"}'
```

### 4.2 SiliconFlow Kolors (In China, Direct Connection ✓)

- Kolors is labeled "free for a limited time"[^13].
- Image model rate limits: 2 images per minute (IPM 2) and 400 images per day (IPD 400)[^134]; limits for free models are fixed and do not rise with your tier[^134].
- Real-name verification is required before you can claim rewards or use some features[^135].
- **Watermark**: by default the API adds a visible "AI-generated" watermark, and an invisible watermark is always added[^44]. Passing `X-Enable-Watermark: 0` turns off the visible watermark, but by law developers must then add one to the final image themselves[^44]. The changelog also says "watermarks are added by default"[^136].

```bash
curl https://api.siliconflow.cn/v1/images/generations \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "Kwai-Kolors/Kolors", "prompt": "an island near sea, lighthouse, boats", "image_size": "1024x1024", "num_inference_steps": 20, "guidance_scale": 7.5}'
```

### 4.3 ModelScope API-Inference (In China, Direct Connection ✓)

- **Prerequisite**: the ModelScope account must first be linked to an Alibaba Cloud account[^14].
- **Quota**: deducted in Moli points, at 0.5 per call for lightweight models, 1 for mainstream models and 2 for flagship models[^14]. Logging in each day gives 200 Moli points, and linking Alibaba Cloud adds another 50[^7], which works out to about 125–500 calls per day (converted).
- **Intended use**: officially it is a free, convenient way for developers to call models, and those with commercial needs are advised to use a commercial platform's API[^14]; do not use it for production tasks that need high concurrency or an SLA[^14].
- **How to call**: asynchronous. First POST v1/images/generations with the request header `X-ModelScope-Async-Mode: true`, then poll v1/tasks/{task_id}[^137].
- Up to 6 LoRAs can be stacked[^137].
- Size ranges: SD series 64–2048, FLUX 64–1024, Qwen-Image 64–1664, Z-Image-Turbo 512–2048[^137].

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

### 4.4 SenseTime SenseNova U1.5 Lite (In China, Public Beta, Direct Connection ✓)

- During the public beta: 1,500 requests every 5 hours, "completely free"[^15].
- You must register on the SenseNova platform and complete account verification[^15].
- The platform docs describe it in terms of credit pools: 60,000 credits every 5 hours and 600,000 credits every 7 days[^49]. Flash-Lite models draw on a dedicated credit pool first[^49].
- Endpoint token.sensenova.cn/v1/images/generations, model name sensenova-u1.5-lite; sizes accept the 2K/4K constants[^15].
- Neither the end date of the public beta nor the regular price has been announced.

```bash
curl https://token.sensenova.cn/v1/images/generations \
  -H "Authorization: Bearer $SENSENOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sensenova-u1.5-lite", "prompt": "A baby sea otter floating on a calm sea", "n": 1}'
```

### 4.5 Cloudflare Workers AI (Outside China, Direct Connection ✓)

- The free plan includes 10,000 Neurons per day[^16], reset every day at 00:00 UTC[^16], which is 8 a.m. Beijing time.
- Cost per image (converted from official unit prices):
  - FLUX.1 schnell: 4.80 Neurons per 512² tile and 9.60 per step[^16]. At 1024² with 4 steps that is 57.6 Neurons, about 173 images per day.
  - FLUX.2 [klein] 4B: 26.05 Neurons per output 512² tile[^16]. 1024² comes to 104.2, about 96 images per day.
  - FLUX.2 [klein] 9B: \$0.015 for the first megapixel[^16], about 1,364 Neurons, enough for only about 7 images per day.
- Beyond that, the paid plan charges \$0.011 / 1,000 Neurons[^16].

```bash
curl https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/black-forest-labs/flux-1-schnell \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{"prompt": "cyberpunk cat"}'
```

The call format comes from the official model page[^138].

### 4.6 Pollinations (Outside China, Open Source, Direct Connection ✓)

- The project is open source[^139].
- **Tested 10-21**:
  - Old endpoint image.pollinations.ai/prompt/{prompt}, without a key: back-to-back requests returned 402, "Free limit reached: 1 image every 45 seconds per IP".
  - After waiting 50 seconds and requesting again, it returned a 768×768 JPEG in 7.9 seconds; the response headers showed the model used was sana.
  - New endpoint gen.pollinations.ai/image/{prompt}, without a key: a new prompt returned 401, asking for an API key; prompts used before did return images, but those were cached.
- **Official pricing**: 1 pollen = \$1[^140]; Z-Image Turbo costs 0.004 pollen per image and FLUX.2 Klein 4B 0.005 pollen per image, with 60 RPM per user[^37].
- The old direct-billing method is limited to 1 pollen per IP per hour[^141].
- You can earn free pollen by doing GitHub tasks, trying models or building apps[^140].
- Third-party test: images carry the pollinations.ai logo, and the nologo=true parameter did not remove it[^133].

```bash
curl -o out.jpg "https://image.pollinations.ai/prompt/a%20small%20lighthouse%20at%20dusk"
```

### 4.7 AI Horde (Outside China, Open Source, Volunteer Compute)

- Anyone can use it for free, even anonymously, and kudos do not expire[^142]. Third-party websites, games and apps can connect to it through the REST API[^142].
- Anonymous users have 0 kudos and registered users at least 25; the more kudos, the further forward in the queue, and requests from anonymous users and those with 0 kudos are first come, first served[^143].
- Live status checked on the morning of 10-21: 11 image workers and 701 requests in the queue (tested).
- Direct connection is intermittent: on 10-21 the first direct attempt timed out but going via a proxy worked, and the second direct attempt worked (tested).
- Requests run on volunteers' computers, so do not send sensitive content (suggestion).

### 4.8 Other Free and Limited-Time Free Services

| Service | How it is free | Caveats | Direct |
| --- | --- | --- | --- |
| Agnes AI | agnes-image-2.0-flash, 2.1-flash and 2.5-flash currently cost \$0 (2.0-flash list price at 1K: \$10 per thousand images)[^17] | Limited-time offer; check the platform's announcements for the end date[^17]; a third-party test found no watermark on images, and the free rate limit was halved on 09-23[^133] | ✓ |
| Puter.js | "User pays" model: \$0 cost to the developer; each user gets a free monthly allowance[^144] and pays for themselves once it is used up[^145] | Suits pure front-end web apps (opinion) | ✓ |
| Pixazo | The free tier costs nothing, but activating it requires linking a credit card[^146] | Flux Schnell and SDXL up to 1024², SD 1.5 up to 512²[^146] | ✓ |

## 5. One-Time Credits for New Users

### 5.1 In China

#### Alibaba Cloud Bailian

- The rules[^147] are:
  - Granted separately for each model; different snapshots of the same model are also counted separately and not shared;
  - Can be claimed and used without real-name verification, which is needed only when you switch to pay-as-you-go after using it up;
  - Shared between the main account and RAM sub-accounts;
  - Covers real-time inference only;
  - Re-registering under the same real-name-verified identity does not let you claim it again.
- Valid for 90 days, counted from activation, model release or application approval (whichever is later); only the China North 2 (Beijing) region has free quota[^20].
- Free image counts for the text-to-image models[^20] are listed below:

| Model | Free images | List price (yuan per image) |
| --- | --- | --- |
| wanx2.0-t2i-turbo | 500 | 0.04 |
| wanx2.1-t2i-turbo | 500 | 0.14 |
| wanx2.1-t2i-plus | 500 | 0.20 |
| wanx-v1 | 500 | 0.16 |
| wan2.2-t2i-flash | 100 | 0.14 |
| wan2.2-t2i-plus | 100 | 0.20 |
| wan2.5-t2i-preview, wan2.6-t2i | 50 each | 0.20 |
| wan2.7-image | 50 | 0.20 |
| wan2.7-image-pro | 50 | 0.50 |
| z-image-turbo | 100 | 0.10 |
| qwen-image-2.0 | 100 | 0.20 |
| qwen-image-2.0-pro (each snapshot counted separately) | 100 | 0.50 |
| qwen-image-2.1-pro, qwen-image-2.1-turbo | 10 each | 0.25, 0.10 |
| qwen-image-3.0, qwen-image-3.0-pro | 10 total, input and output combined | See section 6.1 |

- The table above adds up to about 2,720 images, worth about 442 yuan at list prices (converted, excluding qwen-image-3.0 and snapshots).
- Kling and Vidu, resold on Bailian, have no free quota[^20].

#### Volcano Ark

- Signing up gives "a certain amount" of free inference calls[^148], which only cover online inference billed postpaid per token[^148].
- Once it is used up, calls fail outright; to keep using it you must complete real-name verification and then manually activate the model service[^148].
- The docs do not list how many free Seedream images you get. Third-party roundups: Seedream 4.0 comes with 200 images[^149] and 5.0-lite with 50 images[^150].

#### Others

- **Volcano Engine Jimeng AI API**: in free status it has a trial quota of 200 calls, with a concurrency of 1[^38].
- **Tencent Cloud TokenHub**: the new-user pack gives 1 million tokens for each language model, valid for 1 year, plus credits for video and 3D, but nothing for image generation[^151]. The old Hunyuan platform gave 50 calls for each image generation service on first activation, but new purchases have been stopped[^152].
- **Baidu Qianfan**: the new-user quota only covers online inference tokens for preset models[^153]; the list has ERNIE-4.5-Turbo-128K, DeepSeek-R1 and others at 1 million tokens each, valid for 3 months[^153], and no image models.
- **SiliconFlow**: real-name verification earns a 16-yuan general voucher usable across the whole platform[^135]. Under the referral program, each person you invite earns both of you another 16 yuan, with no cap on the number of invitees; the program runs until 2026-12-31[^135]. 16 yuan buys about 160 Z-Image-Turbo images or 53 Qwen-Image images (converted).
- **Compshare**: 5 free images per image generation model; charging started on 2025-06-30[^31].

### 5.2 Outside China

| Platform | What you get | How many images (converted) |
| --- | --- | --- |
| Stability AI | 25 credits, 1 credit = \$0.01; Stable Image Core costs 3 credits per image[^154] | About 8 Core images |
| Runware | \$2 for signing up with a business email[^155] | About 3,300 FLUX.2 [klein] 4B images |
| WaveSpeedAI | \$1 for new accounts, no card required; WeChat Pay and Alipay accepted[^36] | 200 Z-Image Turbo images[^36] |
| Novita | The sign-up page says \$100 in Sandbox credits, valid for 90 days[^156] | Not verified whether they work for the image generation API |
| fal | Free credits and coupons are valid for anywhere from 1 week to 1 year[^157] | Amount not stated |
| Replicate | Models in the "Try for Free" collection (e.g. google/imagen-4) can be run for free a limited number of times[^158]; everything else needs prepaid credit first[^159] | — |
| Together AI | No free trial; the first top-up must be at least \$15[^160] | — |
| DeepInfra | FLUX-1-schnell is tagged "no-free-anon", so anonymous free use is not supported[^161] | — |
| ModelsLab | Paid plans only; the cheapest is \$21/month for 3,250 calls[^162] | — |

## 6. Paid APIs in China (Platform by Platform)

All of the Chinese API hosts below are reachable via direct connection (tested).

### 6.1 Alibaba Cloud Bailian (Tongyi Wanxiang / Qwen / Z-Image)

| Model | Use | Price (yuan per image) |
| --- | --- | --- |
| wanx2.0-t2i-turbo | Text-to-image | 0.04 |
| wan2.2-t2i-flash, wanx2.1-t2i-turbo | Text-to-image | 0.14 |
| wanx-v1 | Text-to-image | 0.16 |
| wan2.6-t2i, wan2.5-t2i-preview, wan2.2-t2i-plus, wanx2.1-t2i-plus | Text-to-image | 0.20 |
| wan2.7-image, wan2.6-image | Generation and editing | 0.20 |
| wan2.7-image-pro | Generation and editing | 0.50 |
| wan2.5-i2i-preview / wanx2.1-imageedit | Image editing | 0.20 / 0.14 |
| wanx-sketch-to-image-lite | Sketch to image | 0.06 (500 images free) |
| wanx-poster-generation-v1 | Creative posters | Free trial only for now; cannot be called once the free quota is used up |
| qwen-image-2.1-turbo / qwen-image-2.1-pro | Text-to-image | 0.10 / 0.25 |
| qwen-image-3.0 | Text-to-image | 0.18 for both 1K and 2K; input images 0.02 yuan each |
| qwen-image-3.0-pro | Text-to-image | 1K 0.25, 2K 0.5; input images 0.02 yuan each |
| qwen-image-2.0 / qwen-image-2.0-pro | Text-to-image and editing | 0.2 / 0.5 |
| z-image-turbo | Text-to-image | 0.1; 0.2 with prompt rewriting enabled |
| kling/kling-v3-image-generation | Resold Kling | 0.2 |
| kling/kling-v3-omni-image-generation | Resold Kling | 1K, 2K 0.2; 4K 0.4 |
| vidu/viduq2-fast_reference2image, vidu/vidu-image_reference2image | Vidu reference-to-image | 0.28125, 0.625 |

- All prices above come from Bailian's model pricing page[^20] and are the prices for the China North 2 (Beijing) region. The Singapore region costs more; for example, z-image-turbo is 0.110089 yuan per image there[^20].
- **How to call it**:
  - HTTP supports async calls only, and requests must carry the header `X-DashScope-Async: enable`[^163].
  - First POST to `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis` to get a task_id, then GET `/api/v1/tasks/{task_id}` to fetch the result[^163].
  - The official docs recommend moving from the old domain dashscope.aliyuncs.com to the workspace's dedicated domain[^163].

### 6.2 Volcano Ark (Doubao Seedream)

| Model | Price (yuan per image) | Notes |
| --- | --- | --- |
| doubao-seedream-5-0-flash | 0.12 | Input images free |
| doubao-seedream-4-0 | 0.20 | Input images free |
| doubao-seedream-5-0-lite | 0.22 | Input images free |
| doubao-seedream-4-5 | 0.25 | Input images free |
| doubao-seedream-5-0-pro | ≤2.61 million pixels (1.5K and below) 0.30; larger 0.60; layer splitting 0.15 / 0.30 | First input image free, 0.02 each from the 2nd on |

- Prices come from Ark's model pricing page[^22]. Image sets are billed by the number of images actually generated; images not output because of moderation or other reasons are not charged[^22].
- 5.0 flash (doubao-seedream-5-0-flash-260915) has exactly the same capabilities as 5.0 pro, but generates faster and costs less[^23].
- **How to call it**: POST `https://ark.cn-beijing.volces.com/api/v3/images/generations`[^164].
- **Watermark**: the `watermark` parameter defaults to true, which adds the words "AI-generated" to the bottom-right corner of the image[^164].
- **Same models via resellers**: Qiniu sells 5.0 flash at 0.12 yuan (still 0.12 above 1.5K) and 5.0 pro at 0.3 / 0.6 yuan[^39]; TokenHub sells Seedream-Image-v5.0-lite at 0.22 yuan[^40]; Compshare sells 4.5 at 0.25 yuan[^31].

### 6.3 Volcano Engine Jimeng AI API

| Capability | Billing | Price (yuan) |
| --- | --- | --- |
| Text-to-image 3.0 / 3.1, image-to-image 3.0 smart reference, AI marketing product images 3.0 | Per call (1 image per call) | 0.2 |
| Image generation 4.0 series (including asset extraction) | Per image generated (one call may return several) | 0.22 |
| Interactive editing (inpainting) | Per call | 0.2 |
| Smart super-resolution | Per call | 0.4 |

- These prices come from the Jimeng AI API billing notes[^38].
- **Resource packages:**[^38]
  - 3.0 series: 100,000 calls for 18,000 yuan (0.18 yuan per call); 500,000 calls for 80,000 yuan (the page writes it as "8,0000"), about 0.16 yuan per call (converted);
  - Valid for 1 year, stackable, with no-questions-asked cancellation within 7 days;
  - When a package runs out, service does not stop; usage is billed per call instead.
- **Concurrency**: 1 in free status; 1 or 2 when paid, and extra concurrency can be bought for some capabilities[^38].
- Text-to-image 2.1 is being taken offline[^38]. Image generation 4.6 is listed in the docs table of contents, but the billing table has no price for it.

### 6.4 Kling Open Platform

- Image API: 1 credit = 0.025 yuan (list price); video API: 1 credit = 1 yuan[^42].

| Model | Capability | Resolution | Credits / image | Equivalent |
| --- | --- | --- | --- | --- |
| Kling Image 2.1 | Text-to-image | 1K, 2K | 4 | 0.1 yuan |
| Kling Image 2.1 | Image-to-image | 1K, 2K | 8 | 0.2 yuan |
| Kling Image 3.0 | Text-to-image, image-to-image | 1K, 2K | 8 | 0.2 yuan |
| Kling Image 3.0-omni | Text-to-image, image-to-image | 1K, 2K / 4K | 8 / 16 | 0.2 / 0.4 yuan |
| Kling Image O1 | Text-to-image, image-to-image | 1K, 2K | 8 | 0.2 yuan |

- The table above comes from the Kling Open Platform pricing page[^42].
- **Resource packages:**[^42]
  - Package one: ¥2,500 / 100,000 credits; package two: ¥7,500 / 300,000 credits; package three: ¥13,500 / 600,000 credits (a flat 10% off, 0.0225 yuan per credit);
  - Valid for 180 days, and credits left at expiry are not extended; concurrency 9; Kling 4.0 is not supported yet.
- Package one is enough for about 25,000 images with Kling Image 2.1 text-to-image (converted).
- International version: kling-v2-1 text-to-image costs 4 credits, \$0.014 per image[^43].
- **Resellers**: Qiniu charges 0.1 yuan for Kling v2.1 text-to-image, 0.2 yuan for image-to-image, 0.4 yuan for multi-image-to-image, 0.2 yuan for Omni image generation and 0.4 yuan for 4K[^39]; TokenHub charges 0.2 yuan for Kling-Image-v3[^40].

### 6.5 Tencent Cloud TokenHub (Hunyuan and Others)

- Everything is priced at a flat 10 yuan per million tokens, and each image is billed as a fixed number of tokens:[^40]

| Model | Tokens per image | Equivalent (yuan per image) |
| --- | --- | --- |
| Hy-Image-3.5-preview | 1K, 2K 15,000; 4K 20,000 | 0.15; 0.2 |
| Hy-Image-3.0 | 20,000 | 0.2 |
| WAND-Vega-Image-1.0-Lite | 13,500 | 0.135 |
| WAND-Vega-Image-1.0-Flash | 45,000 | 0.45 |
| Seedream-Image-v5.0-lite | 22,000 | 0.22 |
| Seedream-Image-v5.0-pro (≤2.61 million pixels) | 30,000 | 0.3 (converted) |
| Kling-Image-v3 | 20,000 | 0.2 |
| Vidu-Image-q2 | 18,750 | 0.1875 |

- The old per-image-billed HY image models were taken offline as of 2026-09-15[^40]. On the old Hunyuan platform, Hunyuan image generation cost 0.5 yuan per image and the lite text-to-image version from 0.099 yuan per image; new purchases are no longer accepted[^152].

### 6.6 Baidu Qianfan

- musesteamer-air-image (MuseSteamer): 0.05 yuan per image, 1024×1024[^21].
- Qianfan also resells Qwen: qwen-image 0.25 yuan per image, qwen-image-edit 0.3 yuan per image[^21].
- qianfan-image is priced in credits, 1 credit = 0.025 yuan: o1-base text-to-image 8 credits (0.2 yuan), v3o 4K 16 credits (0.4 yuan)[^46]. But the docs table of contents marks it "internal use"[^46], so musesteamer-air-image is the first choice.

### 6.7 Zhipu Open Platform

- CogView-3-Flash is free; CogView-4 costs 0.06 yuan per call, 0.03 yuan with Batch; GLM-Image costs 0.1 yuan per call and does not support Batch[^19].
- International site Z.ai: CogView-4 \$0.01, GLM-Image \$0.015[^47].

### 6.8 MiniMax (Hailuo)

- image-01 / image-01-live: 0.025 yuan per image[^18], the cheapest in China; \$0.0035 on the international site[^48].
- Endpoint: api.minimax.cn/v1/image_generation[^165]; parameters include aspect_ratio, n and prompt_optimizer[^165].

### 6.9 SiliconFlow

- Kolors is free for a limited time[^13].
- Z-Image-Turbo 0.1 yuan per image, Z-Image 0.3 yuan per image[^33].
- Qwen-Image (20 billion parameters[^166]): 0.3 yuan per image[^30].
- ERNIE-Image-Turbo cost 0.11 yuan per image at launch[^167] and has since been taken offline[^13].

### 6.10 Qiniu Cloud

- Endpoint: api.qnaigc.com/v1; the text-to-image API is /images/generations, which returns Base64[^51].
- Prices: Seedream 5.0 flash 0.12 yuan; 5.0 pro 0.3 yuan at ≤1.5K and 0.6 yuan above that, first input image free, rate limit 500 images per minute[^39]. Kling v2.1 text-to-image 0.1 yuan[^39].
- The model list also includes gemini-2.5-flash-image (Nano Banana)[^51], which can be called from China via direct connection; Qiniu's price for it could not be found, and Compshare also offers this model (see 6.11).

### 6.11 Compshare

- Endpoint: api.modelverse.cn/v1; compatible with the OpenAI protocol[^168].
- Per-image prices[^31] are as follows: flux.1-dev 0.10 yuan; Qwen-Image 0.25 yuan; doubao-seedream-4.5 0.25 yuan; Qwen-Image-Edit 0.3 yuan; flux-kontext-pro 0.35 yuan; flux-kontext-max 0.70 yuan.
- Per-token prices[^31] are as follows: gpt-image-1 input 35 yuan, output 280 yuan per million tokens; gemini-2.5-flash-image input 2.2 yuan, output 219 yuan per million tokens.

### 6.12 Other Channels in China

- **302.AI**: Z-Image-Turbo \$0.05 per call[^169], about 0.33 yuan, 3.3 times SiliconFlow's price for the same model (converted). Top-up balances never expire[^170]. Its API could not be reached either directly or via a proxy (tested).
- **Moark (Gitee AI)**: offers 24 text-to-image models and 51 APIs[^171], and deployed models can be tried online for free[^172]; unit prices not verified.
- **Infinigence AI GenStudio**: supports closed-source models such as Seedream and charges only for requests that successfully produce an image[^173]; unit prices could not be found.

## 7. Paid APIs Outside China

| Platform | Models and price per image (USD) | Billing details | Direct |
| --- | --- | --- | --- |
| Prodia | FLUX.2 Klein 4B: ≤1MP \$0.0005, ≤2MP \$0.0027, ≤3MP \$0.0040, >3MP \$0.0059; FLUX.2 [dev] 1MP \$0.012; SDXL ≤25 steps \$0.0020, 26–50 steps \$0.0025[^24] | SDXL costs the same for any side length in the 512–1536 range[^24] | ✓ |
| Runware | FLUX.2 [klein] 4B \$0.0006[^25]; klein 9B \$0.00169[^174]; FLUX.1 schnell 1024² \$0.0013, 512² \$0.0006[^175]; SDXL 1024² 20 steps \$0.0013[^176] | For some models, the published figures are records from actual runs, not rates[^177] | ✓ |
| Runware (cont.) | Z-Image-Turbo 1024² \$0.0032, 2048² \$0.0141[^35]; Qwen-Image 1024² \$0.0058[^32] | The model pages list lower example prices: Z-Image-Turbo \$0.0013[^178] (equal to the 512² price in the schema), Qwen-Image \$0.0032[^179]; for 1024² estimates, go by the schema | ✓ |
| Cloudflare Workers AI | FLUX.1 schnell about \$0.00063; FLUX.2 [klein] 4B about \$0.00115 (converted from official unit prices)[^16] | The first 10,000 Neurons each day are free[^16] | ✓ |
| DeepInfra | FLUX-1-schnell 0.05 US cents per image unit, 1024² by default[^161] | Not verified whether 1 unit equals one 1024² image | ✓ |
| Together AI | Juggernaut Lightning Flux from \$0.0017; SD XL from \$0.0019; Qwen Image from \$0.0058; Wan 2.6 Image from \$0.03[^29] | The first top-up must be at least \$15[^160] | ✓ |
| fal | FLUX.1 schnell \$0.003/MP[^180]; Z-Image Turbo \$0.005/MP[^34]; FLUX.2 [klein] 4B \$0.005/MP[^181] | 1024² counts as 1MP[^182], and anything under 1MP is rounded up[^180]; turning on prompt expansion for Z-Image adds \$0.0025 per call[^34] | ✓ |
| Replicate | flux-schnell \$3 per thousand images[^183] | schnell is licensed under Apache 2.0, so commercial use is allowed[^184]; you must prepay credit first[^159] | ✓ |
| Novita | FLUX.1 schnell: \$0.003 × (width × height × steps) / (1024 × 1024 × 4)[^185] | Exactly \$0.003 at 1024² and 4 steps (converted) | ✓ |
| Segmind | Flux Schnell and SDXL about \$0.008; Pruna P Image \$0.005 (Segmind's official blog, 2026-04)[^186] | 60–1000 requests per minute, depending on tier[^187] | ✓ |
| WaveSpeedAI | Z-Image Turbo \$0.005[^36] | Supports WeChat Pay and Alipay[^36] | ✓ |
| MiniMax international site | image-01 \$0.0035[^48] | — | ✓ |
| Recraft | V4.1 Flash \$0.007; V4.1 raster \$0.035, vector \$0.08, Pro 2K \$0.21, Pro vector \$0.30; V4 \$0.04[^188] | Purchased units do not expire[^188] | ✓ |
| BFL (official FLUX provider) | FLUX 3 Klein: 768² \$0.008, 1K \$0.009, 1.5K \$0.011, 2K \$0.014, 4K \$0.036[^58] | Rejected, failed and moderation-blocked requests are not charged[^189] | ✓ |
| BFL (cont.) | FLUX 3 Image: 768² \$0.041, 1K \$0.048, 1.5K \$0.07, 2K \$0.10, 4K \$0.607[^189]; FLUX.2 [klein] 4B from \$0.014, 9B from \$0.015[^58] | FLUX.2 [pro] from \$0.03/MP, [flex] \$0.05/MP, [max] from \$0.07/MP; resolution is rounded up to a whole MP[^59] | ✓ |
| Stability AI | 1 credit = \$0.01: SDXL 1.0 from 0.9, SD 3.5 Flash 2.5, Stable Image Core 3, SD 3.5 Medium 3.5, SD 3.5 Large Turbo 4, SD 3.5 Large 6.5, Stable Image Ultra 8 credits[^154] | — | ✓ |
| Z.ai (Zhipu's international site) | CogView-4 \$0.01; GLM-Image \$0.015[^47] | — | ✓ |
| Runway | muse_image 1 credit; gen4_image_turbo 2 credits; gen4_image 720p 5, 1080p 8 credits; 1 credit = \$0.01[^190] | — | ✓ |
| Kling international version | kling-v2-1 text-to-image \$0.014[^43] | — | ✓ |
| OpenRouter | Seedream 5.0 Flash from \$0.018; Seedream 4.5 \$0.04 regardless of size[^41] | No image-generation models are free (tested 10-21) | ✓ |
| xAI | grok-imagine-image \$0.02 at both 1K and 2K, input images \$0.002[^53]; grok-imagine-image-2.0 1K Low from \$0.04[^54] | — | ✗ (returns 421 via a proxy) |
| Krea | Krea 2 Medium \$0.030, Large \$0.060; adding a style reference or mood board costs more[^191] | — | ✗ (times out via a proxy too) |
| Luma | Uni-1.1 (2K) \$0.0404; Uni-1.1 Max \$0.10[^192]; the older Photon \$0.015 per 2MP image, Photon Flash \$0.004[^193] | Optimized mainly for English[^192] | ✗ |
| Ideogram | The official pricing page lists Ideogram 4.5 / 4.0 / 3.0 and P-Image[^194]; the unit prices load dynamically and were not captured | Third party: P-Image \$0.003 to \$0.03[^195]; the AA leaderboard lists Ideogram 4.0 Instant at \$7.5 per thousand images, Fast \$10.5, standard \$60[^196] | Intermittent |
| OpenAI | gpt-image-2 (1024²) low \$0.006, medium \$0.053, high \$0.211; GPT Image 1 Mini low \$0.005[^52] | gpt-image-2.5-flare is billed per token: image output \$30 per million, Batch \$15[^197]; in the official example one image uses 196 output tokens, about \$0.00588[^52] | ✗ (proxy returns 421) |
| Google Gemini | Nano Banana 2.1: 1K \$0.0336, 2K \$0.0504, 4K \$0.113, half price with Batch; Nano Banana 2: 1K \$0.067; Nano Banana 2 Lite: 1K \$0.0336[^50] | Nano Banana Pro 1K/2K \$0.134, 4K \$0.24; the original Nano Banana \$0.039[^198]; none of these image models has a free tier[^50] | ✗ |
| Google Vertex AI | Imagen 4 Fast \$0.02, Imagen 4 \$0.04, Imagen 4 Ultra \$0.06[^199] | Imagen in the Gemini API has been shut down[^200] | ✗ |
| Microsoft Foundry | MAI-Image-2.6-Flash image output \$19 per million tokens; MAI-Image-2.6 \$38 per million[^55] | Tokens per image not published; requires an Azure subscription linked to a valid payment method[^57] | — |

- The Gemini API's available regions do not include mainland China or Hong Kong[^96].
- Midjourney has no official API. The company has only said it is researching an enterprise API[^201]; on 10-10 it announced a small-scale MCP test, with usage, pricing and start date all unpublished (third party)[^202].
- Pricing for Microsoft's 2.5 generation: MAI-Image-2.5-Flash image output \$19.50 per million tokens[^203].

## 8. Cost per 1,000 Images (Converted)

Official unit prices from sections 6 and 7, multiplied by 1,000; USD converted to yuan at 6.69[^1], excluding cross-border payment fees. Assumes roughly 1024² and 1 image per request.

| Rank | Model (platform) | 1,000 images | Yuan equivalent |
| --- | --- | --- | --- |
| 1 | FLUX.2 Klein 4B (Prodia)[^24] | \$0.50 | ≈ 3.3 yuan |
| 2 | FLUX.2 [klein] 4B (Runware)[^25] | \$0.60 | ≈ 4.0 yuan |
| 3 | FLUX.1 schnell (Cloudflare, beyond the free allowance)[^16] | \$0.63 | ≈ 4.2 yuan |
| 4 | FLUX.2 [klein] 4B (Cloudflare)[^16] | \$1.15 | ≈ 7.7 yuan |
| 5 | FLUX.1 schnell (Runware)[^175] | \$1.30 | ≈ 8.7 yuan |
| 6 | FLUX.2 [klein] 9B (Runware)[^174] | \$1.69 | ≈ 11.3 yuan |
| 7 | FLUX.1 schnell (fal, Replicate, Novita)[^180][^183][^185] | \$3.00 | ≈ 20.1 yuan |
| 8 | Z-Image-Turbo (Runware)[^35] | \$3.20 | ≈ 21.4 yuan |
| 9 | image-01 (MiniMax international site)[^48] | \$3.50 | ≈ 23.4 yuan |
| 10 | image-01 (MiniMax China)[^18] | — | 25 yuan |
| 11 | CogView-4 Batch (Zhipu)[^19] | — | 30 yuan |
| 12 | Z-Image Turbo (fal, WaveSpeed)[^34][^36] | \$5.00 | ≈ 33.5 yuan |
| 13 | wanx2.0-t2i-turbo (Bailian)[^20] | — | 40 yuan |
| 14 | gpt-image-2 low (OpenAI)[^52] | \$6.00 | ≈ 40.1 yuan |
| 15 | Recraft V4.1 Flash[^188] | \$7.00 | ≈ 46.8 yuan |
| 16 | musesteamer-air-image (Qianfan)[^21] | — | 50 yuan |
| 17 | CogView-4 (Zhipu)[^19] | — | 60 yuan |
| 18 | FLUX 3 Klein 1K (BFL)[^58] | \$9.00 | ≈ 60.2 yuan |
| 19 | Kling 2.1 international version[^43] | \$14.00 | ≈ 93.7 yuan |
| 20 | Z-Image-Turbo (Bailian, SiliconFlow), Kling Image 2.1, qwen-image-2.1-turbo[^20][^33][^42] | — | 100 yuan |
| 21 | Nano Banana 2.1 Batch[^50] | \$16.80 | ≈ 112.4 yuan |
| 22 | Seedream 5.0 flash (Volcano Ark, Qiniu)[^22][^39] | — | 120 yuan |
| 23 | Seedream 5.0 Flash (OpenRouter)[^41] | \$18.00 | ≈ 120.4 yuan |
| 24 | grok-imagine-image (xAI)[^53] | \$20.00 | ≈ 133.8 yuan |
| 25 | Hy-Image-3.5-preview (TokenHub)[^40] | — | 150 yuan |
| 26 | Jimeng AI API 3.0 (100,000-call resource package)[^38] | — | 180 yuan |
| 27 | wan2.6-t2i (Bailian)[^20] | — | 200 yuan |
| 28 | Nano Banana 2.1[^50] | \$33.60 | ≈ 224.8 yuan |
| 29 | Luma Uni-1.1 (2K)[^192] | \$40.40 | ≈ 270.3 yuan |
| 30 | Seedream 5.0 pro (≤1.5K)[^22] | — | 300 yuan |
| 31 | FLUX 3 Image 1K (BFL)[^189] | \$48.00 | ≈ 321.2 yuan |
| 32 | Z-Image-Turbo (302.AI)[^169] | \$50.00 | ≈ 334.6 yuan |
| 33 | gpt-image-2 medium (OpenAI)[^52] | \$53.00 | ≈ 354.6 yuan |

- Cheap does not mean good. On a third-party open-weights leaderboard (Artificial Analysis, Elo calculated from pairwise blind votes)[^196], FLUX.2 [klein] 4B scores 837, Z-Image Turbo 936 and Qwen-Image-2.1 1042, while FLUX.1 [schnell] gets only 740[^196].
- The same model can differ in price more than tenfold across platforms; for example, Z-Image-Turbo ranges from about 0.02 yuan on Runware to about 0.33 yuan on 302.AI (converted).

## 9. Free Local Software

### 9.1 Still Maintained

Star counts, latest versions and last-commit dates were checked with the GitHub API on 10-21 (tested).

| Software | License | ★ | Latest version | Features |
| --- | --- | --- | --- | --- |
| ComfyUI | GPL-3.0 | 140,730 | v0.42.1 (10-19) | Node-based workflows; supports all operating systems and NVIDIA, AMD, Intel, Apple silicon and Ascend[^204]; has a desktop version, a portable version and an official paid cloud[^204]; can be plugged into production pipelines through its API[^204] |
| SwarmUI | MIT | 4,691 | 0.9.8-Beta (02-06), code still being updated as of 10-20 | Can install ComfyUI automatically as its backend[^205]; on Mac, only M-series chips are supported[^205] |
| Forge Neo | AGPL-3.0 | 1,834 | 2.30.1 (10-19) | The neo branch of sd-webui-forge-classic[^206]; the original Forge has had no commits since mid-2025 and has not added FLUX.2, while Neo is the maintained successor and keeps the single-page interface[^207]; SD3 support was dropped[^207] |
| InvokeAI | Apache-2.0 | 28,791 | v6.14.2 (09-27) | A creative engine for professionals and enthusiasts[^208], with a canvas and workflows; the Community Edition has installers for Windows, Mac and Linux[^209] |
| SD.Next | Apache-2.0 | 7,357 | No formal release; last commit 10-19 | Generates and edits images and videos[^210]; supports NVIDIA, AMD, Intel, Apple silicon and CPU[^210] |
| Krita AI Diffusion | GPL-3.0 | 10,750 | v1.53.0 (08-22), last commit 10-03 | A plugin for the painting app Krita; for running locally, an NVIDIA GPU with 6 GB or more of VRAM is recommended[^211]; Apple silicon needs macOS 14+[^211] |
| Mochi Diffusion | GPL-3.0 | 7,971 | v6.2 (09-30) | Native Mac app that runs SD and FLUX.2 Klein[^212]; uses Core ML, can run on the Neural Engine and is very memory-efficient, but each model's output size is fixed when the model is converted[^212] |
| mflux | MIT | 2,524 | v0.23.0 (10-16) | Line-by-line ports of several mainstream models to Apple's MLX[^213]; runs from the command line, e.g. mflux-generate-z-image-turbo[^213] |
| stable-diffusion.cpp | MIT | 7,743 | master-982 (10-20) | Pure C/C++ implementation[^214]; day-one support for FLUX.3 Image Klein on 10-16, support for Qwen-Image-2.1 on 09-20[^214] |
| Draw Things | GPL-3.0 (inference engine) | 594 | v26.1014.0 (10-15) | Mac / iPhone app; the inference engine is open source, and you can also set up your own gRPC server[^215]; for the cloud, see section 10 |

### 9.2 No Longer Updated or Bug-Fix Only: Not Recommended for New Installs

- **AUTOMATIC1111 WebUI**: the long-established Gradio-based interface[^216]. The latest release, v1.10.1, came out in 2025-02; the last commit on the default branch was in 2024-07 (tested).
- **Original Forge[^217]**: last commit on 2025-06-26 (tested); its successor is Forge Neo[^207].
- **Fooocus**: its official status is "limited long-term support with bug fixes only", and it supports only SDXL[^218].
- **DiffusionBee[^219]**: the latest release is still 2.5.3, from 2024-08-14, and the last commit was on 2023-12-28 (tested).

### 9.3 What to Choose on a Mac with 8 GB of Memory

- In a third-party test of SD 1.5 at 512²: an M1 with 8GB takes 20–30 seconds; an M2 Pro with 16GB takes 8–15 seconds[^220].
- In the same test, an 8GB Mac was "too slow" with SDXL and "could not fit" Flux Schnell[^220].
- Draw Things loads weights on demand, which can cut memory use by up to half, so it can run SD 1.5 on 8GB while ComfyUI cannot[^220]. With the same model, ComfyUI is about 3 times slower on a Mac, and installing it takes an hour[^220].
- In Draw Things, the 6-bit version of Z-Image Turbo takes only about 4 GiB when fully loaded into memory[^221]. The official advice is to turn on "Optimize for Faster Loading" on devices with little memory[^222].
- In vdf.ai's recommendations, the lowest Mac tier is 16–24 GB, using the 8-bit versions of Z-Image-Turbo or FLUX.2 [klein] 4B[^26]; there is no recommendation for 8GB Macs.
- Suggestion: on an M2 with 8 GB of memory, run SD 1.5 or Z-Image Turbo 6-bit locally in Draw Things, and run larger models on the Draw Things cloud.

## 10. Draw Things Cloud Free Tier

### 10.1 How to Turn It On

1. "Machine Settings" → "Show Cloud & Sharing Features", which is on by default[^11] (the Wiki calls it Cloud Compute & Sharing; the Chinese UI labels were verified in testing).
2. Click the "Server Offload" icon at the bottom left and choose the free tier ("Community") under "Cloud Compute"; the button is called "Sign in to Community"[^11].
   - After signing in, go back to the "Server Offload" list and move the check mark from this machine to "Community"; generation then runs on the official NVIDIA servers[^11].
   - Don't click "Back to Local": it switches back to "Local only" and signs you out (tested).
3. Signing in: the Wiki says to sign in with an Apple account[^11], and the May release added "Sign in with Google"[^223]. The code-signing entitlements of the direct-download version from the official website (26.1013.0) do not include `com.apple.developer.applesignin`, which Sign in with Apple requires (tested), so on the direct-download version, signing in with Google is advisable (inferred).
4. Below the model drop-down, the app shows how many compute units the current job needs[^11].

### 10.2 Free and Paid Tiers

| Item | Free tier (Community) | Draw Things+ |
| --- | --- | --- |
| Price | Free[^10] | \$8.99/month[^10] |
| Limit per job | 15,000 compute units[^11] | 40,000, priority queuing[^11] |
| Models | Official and community models only[^11] | Can also use local LoRAs[^11] and upload custom LoRAs[^10] |
| Time per job (as the Wiki puts it) | About 2 minutes[^11] | About 5 minutes[^11] |
| API | 20 requests per month[^224] | 200 per month[^224] |

- Jobs over the limit are canceled; lower the settings and try again[^11].
- In the open-source code, the free tier's default limit is 10,000, with a comment saying "about 120 seconds"[^225]. The developer has also said the free tier is roughly equivalent to 2 minutes of GPU time[^226].
- "Lab Hours" raise the free limit to 30,000, but a Wiki note says they have not been seen since support for LTX models was added[^226].
- How many times per day the free tier can be used has not been officially published.

### 10.3 How Many Units One Image Costs on the Free Tier

Units were estimated offline (tested) with the official open-source draw-things-cli (26.1014.0), using the officially recommended steps and CFG, 1 image per job. ✅ up to 10,000; ⚠️ 10,000 to 15,000, depends on the actual limit; ❌ over 15,000, the free tier cannot run it (jobs between 15,000 and 30,000 could in theory run during Lab Hours, but there have been no Lab Hours for a long time).

| Model | Steps / CFG | 512² | 1024² | 1536² | 2048² |
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
| Z-Image (Base) | 30 / 4 | ✅ 2,786 | ✅ 9,601 | ❌ 24,206 | ❌ 51,470 |
| Qwen-Image-2512 | 30 / 4 | ✅ 3,485 | ⚠️ 12,124 | ❌ 31,392 | ❌ 68,593 |
| FLUX.2 [dev] | 28 / 4.5 | ✅ 6,296 | ❌ 20,375 | ❌ 48,081 | ❌ 95,778 |
| Ideogram 4 | 48 / 7 | ✅ 6,891 | ❌ 22,990 | ❌ 56,380 | ❌ 116,901 |

**Patterns for saving quota** (tested):

- Cost is roughly proportional to the number of steps; doubling the side length (4 times the pixels) makes the cost about 5 times as high.
- For most models, a CFG above 1 doubles the cost; for example, Z-Image Turbo goes from 1,282 to 2,564.
- Choosing the uncompressed Exact version or the 6-bit version makes no difference to the cost.
- For large models, use the official 4-step acceleration LoRAs: Qwen-Image-2512 + Lightning needs only 809 for 1024² and 4,573 for 2048²; FLUX.2 [dev] + Turbo needs 2,911 for 1024².
- The Wiki also recommends accelerated models such as Schnell for large images on the free tier[^11].

### 10.4 Privacy and Image Quality

- Data is encrypted in transit with TLS; the server code is open source, but there is no remote attestation, so there is no guarantee against snooping[^11].
- Draw Things says cloud requests are processed only in memory, and the data cannot be stored or viewed afterwards[^227]; the servers run the official, publicly released Docker image[^227].
- The Wiki's advice: for maximum privacy, run locally; the cloud does not store images, but privacy cannot be fully guaranteed[^11].
- Image quality: with the same model and parameters, cloud and local results are essentially the same. Floating-point error on different hardware can make results differ slightly; Draw Things regards this as acceptable numerical error[^228].

## 11. Open Models: Licenses, VRAM, Rankings

### 11.1 Model Overview

License and VRAM data come from vdf.ai's compilation[^26]; Elo scores come from the Artificial Analysis open-weights leaderboard[^196] (with FLUX.2 [dev] = 1000 as the baseline[^196]).

| Model (vendor) | Released | Parameters | License | VRAM / weight size | Elo |
| --- | --- | --- | --- | --- | --- |
| Z-Image-Turbo (Alibaba Tongyi) | 2025-11 | 6B | Apache 2.0 | Runs on a 16 GB consumer GPU | 936 |
| FLUX.2 [klein] 4B (BFL) | 2026-01 | 4B | Apache 2.0 | About 13 GB; RTX 3090 / 4070 and up | 837 |
| ERNIE-Image / Turbo (Baidu) | 2026-04 | 8B | Apache 2.0 | 24 GB consumer GPU | 907 / 914 |
| Qwen-Image-2512 (Alibaba Qwen) | 2025-12 | 20B | Apache 2.0 | BF16 40.86 GB, FP8 20.43 GB | — |
| LongCat-Image (Meituan) | 2025-12 | 6B | Apache 2.0 | About 17 GB with CPU offload | 856 |
| HiDream-O1-Image (HiDream.ai) | 2026-05 | 8B | MIT | BF16 16.37 GB, FP8 8.07 GB | 975 |
| GLM-Image (Zhipu) | 2026-01 | 9B autoregressive + 7B decoder | MIT | About 23 GB with CPU offload | 885 |
| Qwen-Image-2.1 / Turbo (Alibaba Qwen) | 2026-09 / 10 | 7B + 8B text encoder | Qwen Research License, **no commercial use** | 14.23 GB + 17.53 GB encoder | 1042 |
| FLUX.2 [klein] 9B (BFL) | 2026-01 | 9B | FLUX Non-Commercial License | FP8 9.43 GB | 929 |
| FLUX.2 [dev] (BFL) | 2025-11 | 32B | FLUX Non-Commercial License | FP8 35.46 GB | 1000 |
| Krea 2 (Krea) | 2026-06 | 12B | Krea 2 Community License | BF16 26.28 GB, FP8 13.14 GB | — |
| Ideogram 4 (Ideogram) | 2026-06 | 9.3B | Ideogram 4 Non-Commercial License | Two 9.29 GB FP8 main models + 8.78 GB encoder | 1002 |
| SD 3.5 Large / Medium (Stability) | 2024-10 | 8.1B / 2.5B | Stability AI Community License | Medium 9.9 GB (excluding text encoders) | — |
| HunyuanImage-3.0 (Tencent) | 2025-09 | 80B MoE, 13B active | Tencent Hunyuan Community License | At least 3 GPUs with 80 GB of VRAM each | 932 |

- **FLUX 3 Image Klein**: open weights released by BFL in October, with day-one support in stable-diffusion.cpp on 10-16[^214]. It has 5.6B parameters and runs on a single consumer GPU[^189]; the minimum is an RTX card with 8 GB of VRAM[^229]. The license is the FLUX Kommunity License: individuals and companies with annual revenue under USD 5 million can use it commercially for free[^229].
- BFL's own documentation also states that klein 4B is licensed under Apache 2.0 and 9B under the FLUX Non-Commercial License[^230].
- Also near the top of the leaderboard are Fibo 2.0 (1039 points, API \$32 per thousand images) and Ming-Image-0.1-Design (999 points)[^196]. Ming-Image is 6B and MIT-licensed, but it was officially validated on a single GPU with 80 GiB of VRAM[^26]. On Hugging Face, Fibo 2.0's license is listed as "other" (tested).

### 11.2 License Caveats

- The license goes with the model: it is the same whichever platform you run it on. Each platform's user agreement has its own rules on whether generated images may be used commercially; these have not been verified one by one.
- SD 3.5 Medium and Krea 2 have a revenue threshold: you can only use them if your annual revenue is under USD 1 million[^26]. HunyuanImage-3.0's license does not apply in the EU, the UK or South Korea[^26].
- Most models also need a separate text encoder and VAE[^26]. For example, the Qwen3 4B encoder used by Z-Image and klein 4B is already 8.04 GB in BF16[^26].

### 11.3 Picking by GPU (vdf.ai's Recommendations)

| Hardware | Commercial use allowed | Non-commercial or revenue-capped |
| --- | --- | --- |
| 8 GB GPU | FLUX.2 [klein] 4B (FP8); SDXL | No recommendation |
| 12 GB | Z-Image-Turbo (INT8); FLUX.2 [klein] 4B | SD 3.5 Medium (annual revenue under USD 1 million) |
| 16 GB | Z-Image-Turbo; FLUX.2 [klein] 4B | Qwen-Image-2.1 / Turbo (INT8); Krea 2 (FP8, annual revenue under USD 1 million) |
| 24 GB | ERNIE-Image; HiDream-O1-Image; GLM-Image; LongCat-Image | Qwen-Image-2.1 (BF16); Ideogram 4; FLUX.2 [klein] 9B |
| 32–48 GB | Qwen-Image-2512 (FP8 from 32 GB, BF16 from 48 GB) | FLUX.2 [dev] (FP8, 48 GB card) |
| Multi-GPU server | Qwen-Image-2512 (BF16) | HunyuanImage-3.0 (outside the EU, the UK and South Korea) |
| Mac 16–24 GB | Z-Image-Turbo or FLUX.2 [klein] 4B (8-bit) | No recommendation |
| Mac 48 GB or more | Qwen-Image-2512 (from 96 GB) | Qwen-Image-2.1; Krea 2 |

The table above is compiled from vdf.ai[^26].

## 12. Compliance: Labeling, Filing, Watermarks

### 12.1 *Measures for Labeling AI-Generated Synthetic Content*

- In effect since 2025-09-01[^28].
- **Two kinds of labels:**[^28]
  - Explicit labels: presented in the content or the interface through text, sound, graphics or similar means, so users can clearly perceive them;
  - Implicit labels: added to the file data by technical means, so users do not easily perceive them.
- **How to label images**: add a prominent notice label at a suitable place on the image[^28]; when download, copy or export functions are offered, the file must carry an explicit label[^28].
- **Metadata**: implicit labels must be added to the file metadata, including the generated/synthetic attribute, the service provider's name or code, the content ID and so on[^28]; adding a digital watermark as well is encouraged[^28].
- No organization or individual may maliciously delete, tamper with, forge or conceal these labels[^28]. So the "AI-generated" corner badge that a platform adds to an image cannot be removed at will when you use the image as source material.

### 12.2 Filing and Registration

- Generative AI apps that call a filed model through an API are registered with the local CAC office[^27].
- As of 2026-04-30, a total of 868 generative AI services had completed filing and 530 apps or features had completed registration[^27].
- Apps that are already live must publicly state, in a prominent place or on the product details page, which filed or registered service they use[^27], giving the model name and the filing number or launch number[^27].
- Services based outside China, such as Pollinations, AI Horde and Cloudflare, probably have no filing in China (inferred), so they are not suitable for direct use when launching to the public in China.

### 12.3 Watermark Defaults per API

| Platform | Default | Can it be turned off |
| --- | --- | --- |
| Volcano Ark Seedream | `watermark` defaults to true and adds "AI-generated" in the bottom-right corner[^164] | Can be set to false |
| SiliconFlow | Adds a visible watermark by default; the invisible watermark is always added[^44] | The visible watermark can be turned off, but developers must then add one themselves[^44] |
| Zhipu CogView-3-Flash | "AI-generated" in the bottom-right corner (third-party test)[^133] | No information found |
| Pollinations | Carries the pollinations.ai logo (third-party test)[^133] | nologo=true did not remove it[^133] |
| Tongyi Wanxiang (Wan) and Kling web versions | The free tier probably carries a brand watermark (inferred) | Removing the brand watermark is a membership benefit[^2][^67] |

## 13. Discontinued or No Longer Valid

Don't go looking for these by following old tutorials:

| Item | Status |
| --- | --- |
| Xingliu AI | Ceased operations on 2026-10-10[^87]; users can migrate to Lovart[^88] |
| Kuaishou Kolors web version | Closed on 2024-08-23[^89] |
| StepFun image generation API | Taken offline on 2026-10-10, in China and internationally at the same time[^231] |
| Amazon Nova Canvas | Discontinued on 2026-09-30[^232] |
| Imagen in the Gemini API | Shut down[^200]; Imagen 4 is still available on Vertex AI[^199] |
| Google ImageFX | Closed on 2026-04-30 and merged into Flow[^129] |
| TokenHub's old per-image-billed HY image models | Taken offline as of 2026-09-15[^40]; the old Hunyuan platform no longer accepts new purchases[^152] |
| SiliconFlow ERNIE-Image-Turbo | Taken offline[^13] |
| Jimeng AI API text-to-image 2.1 | Being taken offline[^38] |
| Together's free FLUX.1 schnell | No longer on the Serverless API[^233] |
| Hugging Face free inference credits | No longer given to free accounts; the change to the official docs was merged on 2026-10-07[^234]; now only PRO (\$9/month) includes \$2 of credits[^128][^235] |
| GitHub Models | Fully retired on 2026-07-30[^236] |
| ModelScope API-Inference "2,000 calls per day" | No longer in the current docs; now charged in Moli points[^14] |
| Grok Imagine free tier | Cancelled as of 2026-03-19 (third party)[^100] |
| OpenRouter free image models | None: when its model list endpoint was called on 10-21, none of the 63 image models had a `:free` version and none had a unit price of 0 (tested) |
| Keyless image generation on the new Pollinations endpoint | No longer works; an API key is required (tested 10-21) |

## 14. Still to Confirm

- How many free images Volcano Ark gives for each Seedream model (only shown in the console).
- How many images per day can be generated for free in the Qwen, Doubao, Kling and Jimeng AI apps (none of them has officially published this).
- How many inspiration points Kling deducts per image, how many credits Zhipu Qingyan deducts per image, and exactly how many Moli points each ModelScope model costs (officially only given as 1–2).
- The unit price of Ideogram's official API (the page loads dynamically and could not be scraped; section 7 gives third-party figures), and Leonardo's API unit price.
- Unit prices on Moark and Infinigence AI, and for Nano Banana on Qiniu.
- How many free uses per day Tiangong (Skywork), Quark, WPS Lingxi, Meitu Design Studio and Duiyou give.
- How many times per day the Draw Things free tier can be used.
- When the SenseTime SenseNova public beta ends, and what the regular price will be.
- How much Microsoft MAI-Image works out to per image (the number of tokens per image has not been published).

## Appendix: Network Connectivity Tests from China

Tests were run on the evening of 10-20 and the morning of 10-21 with curl from a mainland China network, first over a direct connection; anything that failed over the direct connection was tried once more via a proxy. The results only reflect this one network environment at the time of testing.

| Category | Direct connection works | Direct fails, works via a proxy | Both fail / refused |
| --- | --- | --- | --- |
| Websites in China | All platforms in section 2 | — | — |
| APIs in China | Bailian, Volcano Ark, Jimeng AI API, Zhipu, SiliconFlow, ModelScope, MiniMax, SenseTime, Qiniu, Compshare, Kling, Qianfan, Tencent Cloud, Moark | — | — |
| APIs outside China | Cloudflare, OpenRouter, Runware, fal, Replicate, Together, DeepInfra, Novita, WaveSpeed, Stability, Segmind, Prodia, Recraft, BFL, Z.ai, MiniMax international site, Runway, Kling international version, Pollinations, Agnes, Puter, Pixazo | Luma, Ideogram (intermittent), AI Horde (intermittent), Gemini API, Vertex AI, Hugging Face (including the router) | Krea, 302.AI; OpenAI and xAI return 421 via a proxy |
| Websites outside China | Microsoft Designer, Grok, Recraft, Dreamina, Lovart | Gemini, Google AI Studio, Google Labs, Copilot, SeaArt, Civitai, PixAI, Hugging Face | 403 over a direct connection: ChatGPT, Playground, Freepik, the Midjourney website; 403 via a proxy as well: Meta AI, the Ideogram website; both fail: NightCafe, Perchance, Raphael, Tensor.Art, Craiyon, Krea, Mage, Leonardo, Mistral |

## References

The pages cited in the text are listed below, captured 2026-10-20 to 10-21.

[^1]: [ExchangeRate-API open access exchange rates (updated 2026-10-21 00:02 UTC)](https://open.er-api.com/v6/latest/USD)
[^2]: [Tongyi Wanxiang: membership subscriptions (pricing page)](https://tongyi.aliyun.com/wan/pricing)
[^3]: [SMZDM: timeline of cuts to Jimeng AI's daily bonus credits (third party)](https://post.smzdm.com/p/ad793rex)
[^4]: [NetEase account · Qiuye PPT: Doubao has officially started charging! But these 6 features are free with unlimited use](https://www.163.com/dy/article/L08MTNQL05169CIL.html)
[^5]: [Beijing Business Today: Qwen, from treating users to charging them (2026-08)](https://xinwen.bjd.com.cn/content/s6a7b472ae4b0e45f3fd5edcb.html)
[^6]: [TMTPost: Wenxin upgrades, Doubao starts charging](https://www.tmtpost.com/8041957.html)
[^7]: [ModelScope: the Moli points incentive system explained (official docs source file, built 2026-10-20)](https://resouces.modelscope.cn/document/docdata/2026-10-20_18-23-CN/dist/magicube/intro/intro_CN.md)
[^8]: [ModelScope: list of free resources on the platform (official article, 2026-08)](https://www.modelscope.cn/learn/1409)
[^9]: [LiblibAI membership center](https://www.liblib.art/viphome)
[^10]: [Draw Things Pricing](https://drawthings.ai/pricing)
[^11]: [Draw Things Wiki: Cloud Compute](https://wiki.drawthings.ai/wiki/Cloud_Compute)
[^12]: [Zhipu Open Platform docs: CogView-3-Flash](https://docs.bigmodel.cn/cn/guide/models/free/cogview-3-flash)
[^13]: [SiliconFlow: model marketplace (Kolors)](https://cloud.siliconflow.cn/open/models?target=Kwai-Kolors%2FKolors)
[^14]: [ModelScope: API-Inference usage limits (official docs source file, built 2026-10-20)](https://resouces.modelscope.cn/document/docdata/2026-10-20_18-23-CN/dist/model-service/API-Inference/limits/limits_CN.md)
[^15]: [SenseTime: SenseNova U1.5 Lite goes live in the Token Plan public beta (2026-09-11)](https://sensetime.com/en/news/sensenova-u1-5-lite-token-plan-20260911-1741)
[^16]: [Cloudflare Workers AI: Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing)
[^17]: [Agnes AI Wiki: Model Pricing](https://wiki.agnes-ai.com/en/docs/pricing)
[^18]: [MiniMax Open Platform: pricing overview](https://platform.minimax.cn/docs/pricing/overview)
[^19]: [Zhipu Open Platform: API pricing](https://docs.bigmodel.cn/cn/guide/start/pricing)
[^20]: [Alibaba Cloud Bailian: model call pricing (image generation)](https://help.aliyun.com/zh/model-studio/model-pricing)
[^21]: [Baidu Qianfan: model service billing](https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya)
[^22]: [Volcano Ark: model pricing](https://ark.volcengine.com/region:cn-beijing/docs/model-pricing.md)
[^23]: [Volcano Ark: model release announcements](https://ark.volcengine.com/region:cn-beijing/docs/model-release-announcement)
[^24]: [Prodia Docs: Pricing](https://docs.prodia.com/reference/pricing)
[^25]: [Runware: FLUX.2 [klein] 4B](https://runware.ai/models/bfl-flux-2-klein-4b)
[^26]: [vdf.ai: roundup of open-source image model licenses (2026-10-14)](https://vdf.ai/blog/best-local-image-generation-models)
[^27]: [CAC: announcement of generative AI services that have completed filing](https://www.cac.gov.cn/2026-05/13/c_1780413225190669.htm)
[^28]: [CAC et al.: *Measures for Labeling AI-Generated Synthetic Content*](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)
[^29]: [Together AI Docs: Available models](https://docs.together.ai/docs/serverless/models)
[^30]: [SiliconFlow: model pricing](https://www.siliconflow.cn/pricing)
[^31]: [Compshare: model API billing details](https://compshare.cn/docs/modelverse/price)
[^32]: [Runware: Qwen-Image schema](https://runware.ai/docs/models/alibaba-qwen-image/schema.json)
[^33]: [SiliconFlow: Alibaba's Z-Image now live](https://www.siliconflow.cn/news/zab9zcwcqa2qe4gi5iy7z2pf)
[^34]: [fal: Z-Image Turbo](https://fal.ai/models/fal-ai/z-image/turbo)
[^35]: [Runware API: Z-Image-Turbo schema.json](https://runware.ai/docs/models/alibaba-z-image-turbo/schema.json)
[^36]: [WaveSpeedAI: Pricing](https://wavespeed.ai/pricing)
[^37]: [Pollinations: image model list (API JSON)](https://gen.pollinations.ai/image/models)
[^38]: [Volcano Engine: Jimeng AI - image generation billing details](https://docs.volcengine.com/docs/JimengAI/JimengAI-imagegenerationbillinginstructions)
[^39]: [Qiniu Cloud: AI large model marketplace](https://www.qiniu.com/ai/models)
[^40]: [Tencent Cloud TokenHub: model pricing](https://cloud.tencent.com/document/product/1823/130055)
[^41]: [OpenRouter: Image models](https://openrouter.ai/collections/image-models)
[^42]: [Kling AI Open Platform: API pricing](https://klingai.com/dev/pricing)
[^43]: [Kling AI API Pricing (international version, images)](https://klingai.com/global/dev/model/image)
[^44]: [SiliconFlow API reference: create image generation request](https://api-docs.siliconflow.cn/docs/api/images-generations-post)
[^45]: [Sina Finance: Tencent Hunyuan releases Hunyuan Image 3.5 preview (2026-09-22)](https://finance.sina.com.cn/stock/t/2026-09-22/doc-inistrnx1775920.shtml)
[^46]: [Baidu Qianfan: image generation model pricing](https://cloud.baidu.com/doc/qianfan-multimodal/s/mmmt5xhbv)
[^47]: [Z.ai: Pricing](https://docs.z.ai/guides/overview/pricing)
[^48]: [MiniMax API Docs: Pricing Overview](https://platform.minimax.io/docs/pricing/overview)
[^49]: [SenseNova AI API docs](https://platform.sensenova.ai/docs)
[^50]: [Gemini Developer API: Pricing (markdown version)](https://ai.google.dev/gemini-api/docs/pricing.md.txt)
[^51]: [Qiniu Cloud: text-to-image API](https://developer.qiniu.com/aitokenapi/13166/text-to-image-api)
[^52]: [OpenAI API: Image generation](https://developers.openai.com/api/docs/guides/image-generation)
[^53]: [xAI Docs: Grok Imagine Image](https://docs.x.ai/developers/models/grok-imagine-image)
[^54]: [xAI Docs: grok-imagine-image-2.0](https://docs.x.ai/developers/models/grok-imagine-image-2.0)
[^55]: [Microsoft Tech Community: MAI-Image-2.6](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/mai-image-2-6-and-mai-image-2-6-flash-quality-and-speed-at-production-scale/4550970)
[^56]: [Bing Image Creator FAQ](http://www.bing.com/images/create/ai-image-generator/faq)
[^57]: [Microsoft Learn: Use MAI-Image models in Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-mai-image?tabs=python)
[^58]: [Black Forest Labs API: Pricing](https://docs.bfl.ai/quick_start/pricing)
[^59]: [BFL Help: What are the costs associated with using your models](https://help.bfl.ai/articles/7986977817-what-are-the-costs-associated-with-using-your-models)
[^60]: [Sina Tech: hands-on test of image and video generation in the Qwen app (2025-12-02)](https://finance.sina.com.cn/tech/roll/2025-12-02/doc-infzmppc0200858.shtml)
[^61]: [DoNews: Qwen launches a paid version (2026-08-11)](https://www.donews.com/news/detail/1/6665859.html)
[^62]: [App Store: Qwen - Alibaba AI assistant (in-app purchases list)](https://apps.apple.com/cn/app/%E5%8D%83%E9%97%AE-%E9%98%BF%E9%87%8Cai%E5%8A%A9%E6%89%8B/id6466733523)
[^63]: [SMZDM: Jimeng AI's daily free credits reportedly cut (third party)](https://post.smzdm.com/p/a5rgd6pk)
[^64]: [21jingji.com: Doubao Professional edition launched (2026-06-24)](https://www.21jingji.com/article/20260624/herald/c579e97b948a6d0fd1588bffad3c94ee.html)
[^65]: [Baidu Wenxin Assistant home page](https://wenxin.baidu.com)
[^66]: [IT Home: ERNIE Bot's official website entry upgraded (2026-06)](https://www.ithome.com/0/968/360.htm)
[^67]: [Kling AI: membership plans (China version)](https://app.klingai.com/cn/membership/membership-plan)
[^68]: [Baipiaoji: Kling AI free quota (verified 2026-08-06, third party)](https://baipiaoji.com/tools/kling)
[^69]: [BigoLab: Kling AI user guide (third party)](https://bigolab.com/guides/2290-kling-ai-how-to)
[^70]: [Zhipu Qingyan: Mid-Autumn and National Day holiday event announcement](https://chatglm.cn/apps)
[^71]: [Sanwenge: hands-on test of Hailuo AI (third party, 2026-06)](https://www.sanwenge.com/post/1133.html)
[^72]: [Hailuo AI official Weibo (2026-02-26)](https://www.sina.cn/news/detail/5270573464683042.html)
[^73]: [iFlytek Spark docs: AI painting](https://xinghuo.xfyun.cn/doc/spark-guide/AI%E7%BB%98%E7%94%BB.html)
[^74]: [Tixiaolu: iFlytek Spark AI painting review (third party)](https://www.tixiaolu.com/v2/posts/v2-b63f275f.html)
[^75]: [AI Toolset: WHEE (third party, undated)](https://ai-bot.cn/sites/2976.html)
[^76]: [Meitu WHEE membership service agreement](https://www.whee.com/agreement/vip-service.html)
[^77]: [AI Toolset: TusiArt (third party, 2025 data)](https://ai-bot.cn/tusiart)
[^78]: [Tusi.cn - App Store (subscription details)](https://apps.apple.com/cn/app/%E5%90%90%E5%8F%B8tusi-cn-ai%E6%A8%A1%E5%9E%8Bart%E5%9C%A8%E7%BA%BF%E7%94%9F%E5%9B%BE%E7%BB%98%E7%94%BBcomfy/id6458545837)
[^79]: [App Store: Nano AI (360)](https://apps.apple.com/cn/app/%E7%BA%B3%E7%B1%B3ai-%E4%BD%A0%E7%9A%84%E4%B8%93%E5%B1%9E%E8%B6%85%E7%BA%A7%E6%99%BA%E8%83%BD%E4%BD%93/id6737763506)
[^80]: [Duiyou AI Reactor](https://d.design/ai/video)
[^81]: [SenseTime SenseMirage official website](https://miaohua.sensetime.com)
[^82]: [Sanwenge: SenseTime SenseMirage review (third party)](https://www.sanwenge.com/post/1154.html)
[^83]: [Tiangong app - App Store](https://apps.apple.com/cn/app/%E5%A4%A9%E5%B7%A5/id6447616432)
[^84]: [PConline: Quark AI image generation tutorial](https://www.pconline.com.cn/ai/1933/19333212.html)
[^85]: [Meitu Design Studio - App Store (in-app purchases list)](https://apps.apple.com/cn/app/%E7%BE%8E%E5%9B%BE%E8%AE%BE%E8%AE%A1%E5%AE%A4-%E8%AE%A9%E5%95%86%E4%B8%9A%E8%AE%BE%E8%AE%A1-%E5%A5%BD%E7%9C%8B%E5%8F%88%E8%A7%81%E6%95%88/id875654777)
[^86]: [WPS AI Office (Lingxi)](https://x.wps.cn/lingxi)
[^87]: [Xingliu AI official website (end-of-service notice)](https://www.xingliu.art)
[^88]: [Sohu: Xingliu shuts down, migration to Lovart (relaying the official announcement)](https://www.sohu.com/a/1076951619_121124728)
[^89]: [Kuaishou Kolors official website (shutdown notice)](https://kolors.kuaishou.com)
[^90]: [Microsoft Designer (FAQ)](https://www.microsoft.com/en-us/microsoft-365/microsoft-designer)
[^91]: [ChatGPT Pricing](https://chatgpt.com/pricing)
[^92]: [OpenAI Help: ChatGPT Free Tier FAQ](https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq)
[^93]: [Gemini Apps Help: usage limits](https://support.google.com/gemini/answer/16275805?co=GENIE.Platform%3DDesktop&hl=en)
[^94]: [Gemini Apps Help: generate and edit images](https://support.google.com/gemini/answer/14286560?co=GENIE.Platform%3DDesktop&hl=en-JM)
[^95]: [Gemini API Pricing (web version)](https://ai.google.dev/gemini-api/docs/pricing)
[^96]: [Gemini API: Available regions](https://ai.google.dev/gemini-api/docs/available-regions)
[^97]: [Meta AI: AI image generator](https://www.meta.ai/ai-image-generator)
[^98]: [Meta Help: Imagine with Meta AI](https://www.meta.com/help/artificial-intelligence/1337455336906126)
[^99]: [Goongen: Is Grok Imagine Still Free in 2026? (third party)](https://goongen.ai/blog/is-grok-imagine-free)
[^100]: [Sloane: Grok Imagine free vs premium 2026 (third party)](https://www.sloane.world/guides/grok-imagine-free-vs-premium-2026)
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
[^113]: [Creamify: SeaArt Review (third party)](https://www.creamify.ai/blog/seaart-review)
[^114]: [Scrutool: TensorArt AI Review 2026 (third party)](https://www.scrutool.com/review/tensorart-ai)
[^115]: [Civitai Education: Guide to Buzz](https://education.civitai.com/civitais-guide-to-on-site-currency-buzz-%E2%9A%A1)
[^116]: [PixAI: Sign Up](https://pixai.art/en/sign-up)
[^117]: [Knowara: Perchance AI Review 2026 (third party)](https://knowara.com/ai-tools/image/perchance-ai-review)
[^118]: [Raphael AI official website](https://raphael.app)
[^119]: [Craiyon Pricing](https://www.craiyon.com/en/pricing)
[^120]: [Magnific (formerly Freepik AI) Docs: Plans and pricing](https://www.magnific.com/ai/docs/plans-and-pricing)
[^121]: [Recraft Docs: Free plan](https://www.recraft.ai/docs/plans-and-billing/free-plan)
[^122]: [Recraft: Pricing and plans](https://www.recraft.ai/pricing)
[^123]: [Playground Help: Free plan limits](https://help.playgroundai.com/en/articles/11434147-what-are-the-limits-on-the-free-plan)
[^124]: [Mistral AI: Pricing](https://mistral.ai/pricing)
[^125]: [OpenArt Pricing (legacy page)](https://openart.ai/legacy/pricing)
[^126]: [Midjourney Docs: Comparing Midjourney Plans](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans)
[^127]: [Hugging Face Docs: Spaces ZeroGPU (source file)](https://github.com/huggingface/hub-docs/blob/main/docs/hub/spaces-zerogpu.md)
[^128]: [Hugging Face: Pricing](https://huggingface.co/pricing)
[^129]: [vmake.ai: ImageFX Review (third party)](https://vmake.ai/blog/imagefx-ai-image-generator-review)
[^130]: [Google Flow: About](https://labs.google/flow/about)
[^131]: [Zhipu Open Platform API reference: Image generation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%9B%BE%E5%83%8F%E7%94%9F%E6%88%90)
[^132]: [Zhipu Open Platform: Rate limits](https://docs.bigmodel.cn/cn/api/rate-limit)
[^133]: [hermes-plugin-free-image-gen (third-party test)](https://github.com/ulysis6/hermes-plugin-free-image-gen)
[^134]: [SiliconFlow Docs: Rate Limits](https://docs.siliconflow.cn/docs/userguide/faqs/rate-limit-and-upgradation)
[^135]: [SiliconFlow: Referral program](https://www.siliconflow.cn/developer-talk/od7wj9rr23p95uhihmhrombp)
[^136]: [SiliconFlow: Product changelog](https://docs.siliconflow.cn/docs/release-notes/overview)
[^137]: [ModelScope: API-Inference introduction (official doc source file, built 2026-10-20)](https://resouces.modelscope.cn/document/docdata/2026-10-20_18-23-CN/dist/model-service/API-Inference/intro/intro_CN.md)
[^138]: [Cloudflare Workers AI: flux-1-schnell model page](https://developers.cloudflare.com/workers-ai/models/flux-1-schnell)
[^139]: [Pollinations (GitHub)](https://github.com/pollinations/pollinations)
[^140]: [Pollinations.ai official website](https://pollinations.ai)
[^141]: [Pollinations API docs](https://enter.pollinations.ai/api/docs)
[^142]: [AI Horde (GitHub)](https://github.com/Haidra-Org/AI-Horde)
[^143]: [AI Horde Docs: kudos](https://github.com/Haidra-Org/haidra-assets/blob/main/docs/kudos.md)
[^144]: [Puter.js Docs: User-Pays Model](https://docs.puter.com/user-pays-model)
[^145]: [Puter: Free, Unlimited Image Generation API](https://developer.puter.com/tutorials/free-unlimited-image-generation-api)
[^146]: [Pixazo: Free AI APIs](https://www.pixazo.ai/api/free)
[^147]: [Alibaba Cloud Bailian: Free quota for new users](https://help.aliyun.com/zh/model-studio/new-free-quota)
[^148]: [Volcano Ark: Free inference quota](https://ark.volcengine.com/region:cn-beijing/docs/free-inference-quota)
[^149]: [Third-party roundup: Doubao-Seedream-4.0 free quota](https://buguoshixc.github.io/ai-deals-aggregator/deal/7f8c32f6a327)
[^150]: [Third-party roundup: Doubao-Seedream-5.0-lite free quota](https://buguoshixc.github.io/ai-deals-aggregator/deal/d6aaee8c7379)
[^151]: [Tencent Cloud TokenHub: Free trial quota](https://cloud.tencent.com/document/product/1823/130053)
[^152]: [Tencent Hunyuan (old platform): Hunyuan image generation billing overview](https://cloud.tencent.com/document/product/1729/105925)
[^153]: [Baidu Qianfan: Free quota for new users](https://cloud.baidu.com/doc/qianfan/s/Imi2rpirg)
[^154]: [Stability AI Platform: Pricing](https://platform.stability.ai/pricing)
[^155]: [Runware: Pricing](https://runware.ai/pricing)
[^156]: [Novita AI sign-up page](https://novita.ai/zh/user/register)
[^157]: [fal Docs: Model APIs FAQ](https://fal.ai/docs/documentation/model-apis/faq)
[^158]: [Replicate: Try for free](https://replicate.com/collections/try-for-free)
[^159]: [Replicate Docs: Prepaid credit](https://replicate.com/docs/topics/billing/prepaid-credit)
[^160]: [Together AI Docs: Credits](https://docs.together.ai/docs/billing-credits)
[^161]: [DeepInfra: FLUX-1-schnell model metadata](https://api.deepinfra.com/models/black-forest-labs/FLUX-1-schnell)
[^162]: [ModelsLab Pricing](https://modelslab.com/pricing.md)
[^163]: [Alibaba Cloud Bailian: Tongyi Wanxiang (Wan) text-to-image V2 API reference](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
[^164]: [Volcano Ark: Image generation API](https://ark.volcengine.com/region:cn-beijing/docs/image-generation-api)
[^165]: [MiniMax Open Platform: Text-to-image API](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i)
[^166]: [SiliconFlow model catalog: Qwen-Image](https://cloud.siliconflow.cn/open/models?target=Qwen%2FQwen-Image)
[^167]: [SiliconFlow: ERNIE-Image-Turbo now available](https://www.siliconflow.cn/news/t9hvfusja8yijr3k61gz7c6r)
[^168]: [Compshare: Model API quick start](https://www.compshare.cn/docs/modelverse/models/quick-start)
[^169]: [302.AI: Z-Image-Turbo](https://302.ai/product/detail/z-image-turbo)
[^170]: [302.AI Help Center: API pricing](https://help.302.ai/docs/API-jia-ge-dY9X)
[^171]: [Moark Docs: Text-to-image](https://ai.gitee.com/docs/products/apis/images-vision/text2image)
[^172]: [Moark: Serverless API](https://ai.gitee.com/docs/products/apis)
[^173]: [Infinigence AI GenStudio: Image generation API](https://docs.infini-ai.com/gen-studio/api/multimodal/image-generation.html)
[^174]: [Runware: FLUX.2 [klein] 9B](https://runware.ai/models/bfl-flux-2-klein-9b)
[^175]: [Runware API: FLUX.1 [schnell] schema.json](https://runware.ai/docs/models/bfl-flux-1-schnell/schema.json)
[^176]: [Runware: SDXL schema](https://runware.ai/docs/models/stabilityai-stable-diffusion-xl-v1-0-vae-fix/schema.json)
[^177]: [Runware Docs: Pricing](https://runware.ai/docs/platform/pricing)
[^178]: [Runware: Z-Image-Turbo model page](https://runware.ai/models/z-image-turbo)
[^179]: [Runware: Qwen-Image model page](https://runware.ai/models/alibaba-qwen-image)
[^180]: [fal: FLUX.1 [schnell]](https://fal.ai/models/fal-ai/flux/schnell)
[^181]: [fal: FLUX.2 [klein] 4B](https://fal.ai/models/fal-ai/flux-2/klein/4b/llms.txt)
[^182]: [fal: Pricing](https://fal.ai/pricing)
[^183]: [Replicate: Pricing](https://replicate.com/pricing)
[^184]: [Replicate: black-forest-labs/flux-schnell](https://replicate.com/black-forest-labs/flux-schnell)
[^185]: [Novita AI Docs: FLUX.1 [schnell]](https://novita.ai/docs/api-reference/model-apis-flux-1-schnell)
[^186]: [Segmind Blog: The Cheapest AI Image Generation API (2026-04)](https://blog.segmind.com/the-cheapest-ai-image-generation-api-for-developers-in-2026)
[^187]: [Segmind Pricing](https://www.segmind.com/pricing)
[^188]: [Recraft API: Pricing](https://www.recraft.ai/docs/api-reference/pricing)
[^189]: [Black Forest Labs: Pricing](https://bfl.ai/pricing)
[^190]: [Runway API: Pricing & Costs](https://docs.dev.runwayml.com/guides/pricing)
[^191]: [Krea Docs: Krea 2 API](https://www.krea.ai/docs/developers/krea-2/overview)
[^192]: [Luma AI: API (Uni-1.1)](https://lumalabs.ai/api)
[^193]: [Luma Photon (2024)](https://lumalabs.ai/photon)
[^194]: [Ideogram: API Pricing](https://about.ideogram.ai/api-pricing)
[^195]: [UsagePricing: Ideogram P-Image launches (2026-08-04)](https://usagepricing.com/blueprint/activity/ideogram-2026-08-04-p-image-price-floor)
[^196]: [Artificial Analysis: Text-to-image open-weights leaderboard (third party)](https://artificialanalysis.ai/image/leaderboard/text-to-image/open-weights?tab=table)
[^197]: [OpenAI Docs: gpt-image-2.5-flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare.md)
[^198]: [Gemini API pricing (Chinese page)](https://ai.google.dev/gemini-api/docs/pricing?hl=zh-cn)
[^199]: [Google Cloud: Generative AI pricing (Vertex)](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)
[^200]: [Gemini API: Imagen](https://ai.google.dev/gemini-api/docs/imagen)
[^201]: [Midjourney: Enterprise API survey](https://www.midjourney.com/updates/enterprise-api-survey)
[^202]: [TL Dev Tech: Midjourney opens a small-scale MCP test (third party)](https://www.tldevtech.com/midjourney-finally-lets-agents-in-on-its-terms)
[^203]: [Microsoft AI: Introducing MAI-Image-2.5](https://microsoft.ai/news/introducing-mai-image-2-5)
[^204]: [ComfyUI (GitHub)](https://github.com/Comfy-Org/ComfyUI)
[^205]: [SwarmUI (GitHub)](https://github.com/mcmonkeyprojects/SwarmUI)
[^206]: [Forge Neo — sd-webui-forge-classic neo branch (GitHub)](https://github.com/Haoming02/sd-webui-forge-classic)
[^207]: [Pinggy: Best Open-Source AI Image Models to Self-Host in 2026 (third party)](https://pinggy.io/blog/best_free_open_source_ai_image_generators_to_self_host)
[^208]: [InvokeAI (GitHub)](https://github.com/invoke-ai/InvokeAI)
[^209]: [Invoke — About](https://invoke.ai/about)
[^210]: [SD.Next (GitHub)](https://github.com/vladmandic/sdnext)
[^211]: [Krita AI Diffusion (GitHub)](https://github.com/Acly/krita-ai-diffusion)
[^212]: [Mochi Diffusion (GitHub)](https://github.com/MochiDiffusion/MochiDiffusion)
[^213]: [mflux (GitHub)](https://github.com/mflux-community/mflux)
[^214]: [stable-diffusion.cpp (GitHub)](https://github.com/leejet/stable-diffusion.cpp)
[^215]: [draw-things-community (GitHub)](https://github.com/drawthingsai/draw-things-community)
[^216]: [AUTOMATIC1111 stable-diffusion-webui (GitHub)](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
[^217]: [Original Forge (GitHub)](https://github.com/lllyasviel/stable-diffusion-webui-forge)
[^218]: [Fooocus (GitHub)](https://github.com/lllyasviel/Fooocus)
[^219]: [DiffusionBee (GitHub)](https://github.com/divamgupta/diffusionbee-stable-diffusion-ui)
[^220]: [InsiderLLM: Stable Diffusion on Mac — MLX and Draw Things (third party)](https://insiderllm.com/guides/stable-diffusion-mac-mlx)
[^221]: [Draw Things: Quantify Z-Image Turbo Efficiency](https://releases.drawthings.ai/p/quantify-z-image-turbo-efficiency)
[^222]: [Draw Things Wiki: How Powerful Is My Device](https://wiki.drawthings.ai/wiki/How_Powerful_Is_My_Device)
[^223]: [Draw Things Downloads / Changelog](https://drawthings.ai/downloads)
[^224]: [Draw Things Cloud Compute API console](https://api.drawthings.ai/dashboard)
[^225]: [Draw Things open-source code: ComputeUnits.swift (default free-tier limits)](https://github.com/drawthingsai/draw-things-community/blob/main/Libraries/ModelZoo/Sources/ComputeUnits.swift)
[^226]: [Draw Things Wiki: Glossary (Lab Hours)](https://wiki.drawthings.ai/wiki/Glossary)
[^227]: [Draw Things: Privacy Pass and Draw Things+ Cloud Compute](https://releases.drawthings.ai/p/privacy-pass-and-draw-things-cloud)
[^228]: [Draw Things: Harvest Season (2026-10-15)](https://releases.drawthings.ai/p/harvest-season-new-hardware-new-inference)
[^229]: [BFL Blog: FLUX 3 Image Klein (open weights)](https://bfl.ai/blog/flux-3-image-klein)
[^230]: [Black Forest Labs Docs: FLUX.2 Overview](https://docs.bfl.ai/flux_2)
[^231]: [StepFun: Image model retirement notice](https://platform.stepfun.com/docs/zh/announcements/image-model-retirement)
[^232]: [Amazon Bedrock: Nova Canvas model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-canvas.html)
[^233]: [Together AI: FLUX.1 [schnell] Free (no longer on the Serverless API)](https://www.together.ai/models/flux-1-schnell)
[^234]: [huggingface/hub-docs PR #2865: Free users no longer get monthly credits (merged 2026-10-07)](https://github.com/huggingface/hub-docs/pull/2865)
[^235]: [Hugging Face: Inference Providers Pricing](https://huggingface.co/docs/inference-providers/en/pricing)
[^236]: [GitHub Docs: GitHub Models](https://docs.github.com/en/github-models)
