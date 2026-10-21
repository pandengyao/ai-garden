# Free and Low-Cost Text-to-Speech (TTS) APIs: Quotas, Prices, Voice Cloning and Integration

[中文](./Free-and-Low-Cost-TTS-APIs.md) | English

- **Research date**: 2026-10-21
- **Scope**: text-to-speech (TTS) APIs in China and abroad that have a free quota or a low price, including voice cloning and voice design, plus open-weight models you can deploy yourself. Covers free quotas, prices, how Chinese characters are billed, plans, rate limits, Chinese-language support, data policies, and each platform's API endpoint and how to integrate it.
- **Basis**: data comes from official pages: docs, pricing pages, terms, announcements, official price APIs and code repositories; the few items with no official source cite third-party pages, and the text says so. Superscript numbers at the end of a sentence are citations, matching the references at the end. Content marked "(inferred)" is inferred from the cited sources, "(converted)" is calculated from official unit prices or exchange rates, and "(tested)" is the result of an actual test on 2026-10-21 on a network in mainland China.
- **Conversion method**:
  - Vendors count Chinese characters differently (see Section 2), so prices are normalized to "yuan per 10,000 Chinese characters": pure Chinese text at the official list price of the first tier (converted).
  - USD is converted at the European Central Bank reference rates of 2026-10-20: 1 euro = 1.1215 US dollars[^1] and 1 euro = 7.4894 yuan[^1], so 1 US dollar is about 6.68 yuan (converted).
  - For prices billed by duration or by audio tokens, speech is estimated at about 260 Chinese characters per minute, so 10,000 Chinese characters take about 38 minutes (tested: two Edge Chinese voices read the same 203 Chinese characters in 48.0 and 45.0 seconds).
  - Prices billed per call assume every call uses the full character limit; if each call synthesizes only a short sentence, the real unit price is much higher (inferred).
- **Freshness**: prices, promotions and free quotas change quickly; check the official site before paying.

## 1. Key Findings

1. **Long-term official free quotas are few, and each comes with conditions**:
   - Azure's free F0 tier gives 500,000 characters a month[^2], and Azure China, operated by 21Vianet, gives the same[^3]. Azure counts one Chinese character as 2 characters[^4], so that is about 250,000 Chinese characters a month (converted).
   - Google Cloud gives 4 million Standard/WaveNet characters and 1 million Chirp 3 HD characters free each month[^5], but billing must be enabled first[^5].
   - iFlytek's online speech synthesis is free for 500 calls a day[^6]; Bailian's Sambert gives 30,000 characters per model per month[^7].
   - Smaller overseas vendors: the Speechify API gives 500,000 characters a month with no card required and is marked for commercial use[^8]; Unreal Speech gives 250,000 characters a month, and audio published on its free tier must credit it[^9][^10].
2. **Free models**:
   - The Gemini API's `gemini-3.8-flash-tts` costs nothing on the free tier[^11], but free-tier data is used to improve products[^11], and the list of available regions excludes mainland China and Hong Kong[^12].
   - Fish Audio's `s2.1-pro-free` has a unit price of 0, under fair-use limits and with no latency guarantee[^13][^14].
   - Xiaomi MiMo's three TTS models are free for a limited time[^15], with no end date given.
   - The Edge browser's online read-aloud service is free, and it is what the open-source library edge-tts calls[^16]. It is not an API Microsoft offers to developers, and it has no price, quota or SLA (inferred).
   - In October Microsoft changed the token format, and older versions widely return 403[^17]. edge-tts 7.3.1 has switched to the new prefix[^18], and a test on 10-21 synthesized Chinese successfully.
3. **Big Chinese clouds give new users the most**:
   - Tencent Cloud gives 8 million characters for its basic/premium voices, valid for 3 months, once per account[^19].
   - Alibaba Cloud Intelligent Speech Interaction (NLS) has a 3-month trial after activation[^20]; during the trial, speech synthesis has no call limit, but concurrency is only 2[^21].
   - Baidu's short-text synthesis gives 50,000 calls to a verified individual, valid forever[^22]; every 120 GBK bytes (about 60 Chinese characters) count as 1 call[^23].
   - Doubao speech synthesis 2.0 gives 20,000 characters, valid for half a year[^24]; Bailian gives 10,000 characters per model, valid for 90 days[^7][^25].
4. **Before comparing prices, check how many characters one Chinese character counts as**:
   - Bailian, MiniMax's China site and Azure count one Chinese character as 2 characters[^7][^26][^4].
   - Doubao, Tencent and StepFun count one Chinese character as 1 character[^27][^19][^28].
   - SiliconFlow and Fish Audio bill by UTF-8 bytes[^29][^13], and a common Chinese character takes 3 bytes (inferred).
   - Most overseas vendors only say they bill "per character" and don't say how Chinese characters count.
5. **The cheapest pay-as-you-go options (that can synthesize Chinese)**:
   - Traditional voices: Huawei Cloud's standard voices work out to about 0.16–0.18 yuan per 10,000 Chinese characters in prepaid packs, and Baidu's short-text basic voices to about 0.33 yuan (converted); Tencent's premium voices cost 0.3 yuan per 10,000 characters[^19].
   - Large-model voices: StepFun `step-tts-mini` costs 0.9 yuan per 10,000 characters[^28], and Tencent's large-model voices 1.2 yuan per 10,000 characters, less at high volume[^19]. SiliconFlow's CosyVoice2 and Bailian's `qwen3-tts-flash` work out to about 1.5–1.6 yuan per 10,000 Chinese characters (converted).
   - The cheapest are overseas-hosted copies of the open model Kokoro: OpenRouter \$0.62 per million characters[^30], DeepInfra \$0.99 per million characters[^31]. But Kokoro's Chinese voices are rated only D for quality[^32].
6. **Voice cloning**:
   - Creating a cloned voice is free for Bailian's Qwen-Audio-TTS and CosyVoice; synthesis is billed at the model's price[^33].
   - MiniMax and StepFun charge 9.9 yuan per voice[^26][^28].
   - Zhipu charges 6 yuan per clone[^34], and Baidu 8.8 yuan per voice[^35].
   - Doubao charges per voice slot: 138 yuan each, dropping to 28 yuan at volume[^27].
7. **Data policies**:
   - Those that use customer data: the Gemini free tier[^11]; ElevenLabs by default, with an opt-out[^36]; Amazon Polly may use it to improve the service, with an opt-out[^37].
   - Those that state they don't train on it or don't store it: the OpenAI API[^38], Google Cloud TTS[^39] and Azure prebuilt voices[^40].
   - In China, Bailian[^41] and Doubao (with exceptions)[^42] state that data is not used for training.
8. **Being shut down**:
   - OpenAI's `tts-1`, `tts-1-hd` and `gpt-4o-mini-tts` are deprecated and shut down on 2027-01-06[^43].
   - Hume's TTS API stops on 2026-11-13[^44].
   - Meta acquired PlayHT[^45], which, according to a migration guide from the competitor Inworld, shut down at the end of 2025[^46].
9. **Self-hosting**:
   - Models whose weights allow commercial use and that are strong in Chinese include CosyVoice 3[^47], Qwen3-TTS[^48] and VoxCPM2[^49]; see Section 7.
   - The weights of F5-TTS[^50], Spark-TTS[^51] and XTTS-v2[^52] don't allow commercial use.

## 2. Billing Units: How Many Characters One Chinese Character Counts As

For the same 10,000 Chinese characters, Bailian bills 20,000 characters, Doubao bills 10,000 characters, and SiliconFlow bills 30,000 bytes (converted).

| Unit | Platform | Notes |
| --- | --- | --- |
| 1 Chinese character = 2 characters | Alibaba Bailian | English letters, digits, punctuation and spaces count as 1 each; SSML tags are not counted[^7] |
| 1 Chinese character = 2 characters | MiniMax China site | Letters, punctuation, spaces and line breaks count as 1 each[^26] |
| 1 Chinese character = 2 characters | Azure (global and China) | All SSML markup except `<speak>` and `<voice>` is billed[^4] |
| 1 Chinese character = 2 characters | Alibaba NLS | Every 100 characters count as 1 call, up to 300 characters per request[^20]; but the API description page says one Chinese character counts as 1 character[^53], so the two pages contradict each other |
| 1 Chinese character = 1 character | Doubao Speech | Billed by character count, regardless of UTF-8 byte count; SSML tags are billed as normal characters[^27] |
| 1 Chinese character = 1 character | Tencent Cloud | Using SSML costs nothing extra[^19][^54] |
| 1 Chinese character = 1 character | StepFun | It takes 2 English letters or 2 punctuation marks to make 1 character[^28] |
| 1 Chinese character = 1 character | Baidu (long text, voice cloning) | [^55][^35] |
| 1 Chinese character = 1 character | iFlytek (Super Smart TTS) | [^56] |
| 1 Chinese character = 1 character | Huawei Cloud | Standard voices count every 100 characters as 1 call, premium voices every 50 characters as 1 call[^57] |
| 1 Chinese character = 1 character | Google Cloud (Standard, WaveNet) | A multibyte character counts as only 1 character[^5]; SSML tags count (except `<mark>`)[^5] |
| By bytes | SiliconFlow (China and international sites) | By the UTF-8 byte count of the input text[^29][^58] |
| By bytes | Fish Audio | Priced per million UTF-8 bytes[^13] |
| By bytes | Baidu (short text) | Every 120 GBK bytes count as 1 call, about 60 Chinese characters[^23] |
| Per call, length not stated | iFlytek online synthesis, AISpeech | The official pages don't say how many characters one call covers |
| Not stated | OpenAI, Gemini, Amazon Polly, ElevenLabs, Cartesia, Inworld, xAI, Mistral and others | They only say they bill per character or per token; Polly states that SSML tags are not billed[^59] |

## 3. Free Quotas

### 3.1 Long-Term Free (Reset Monthly or Daily)

| Platform | What's free | Conditions and limits | Chinese |
| --- | --- | --- | --- |
| Azure AI Speech | F0 gives 500,000 characters a month[^2] | A Chinese character counts as 2 characters[^4]; F0 allows at most 20 requests per 60 seconds[^60] | Mandarin, Cantonese, Wu, Sichuanese and more[^61] |
| Azure China (21Vianet) | F0 gives 500,000 characters a month[^3] | Reachable directly from networks in China (tested); account-opening requirements were not checked this time | Same as above |
| Google Cloud TTS | Standard/WaveNet 4 million characters a month, Neural2 1 million[^5]; Chirp 3 HD 1 million[^5] | Billing must be enabled[^5]; Standard and WaveNet share one billing SKU, so the free quota may be shared (inferred) | Mandarin has about 30 Chirp3-HD voices[^62], and Cantonese has them too[^62] |
| Gemini API | `gemini-3.8-flash-tts`, `gemini-3.8-flash-lite-tts` and `gemini-2.5-flash-preview-tts` cost nothing on the free tier[^11] | Free-tier rate limits are visible only after logging in[^63]; data is used to improve products[^11]; available regions exclude mainland China and Hong Kong[^12] | Supports Chinese and Cantonese[^64] |
| iFlytek online synthesis | 500 calls a day[^6] | How many characters one call covers is not stated | 37 languages, 11 dialects[^65] |
| Bailian Sambert | 30,000 characters per model per month[^7] | Beijing region only | — |
| Speechify API | 500,000 characters a month; when used up, it pauses until next month[^8] | No card required; marked for commercial use[^8] | The docs say `simba-3.5` supports Chinese and is available on every plan[^66]; the pricing page says self-serve cloning covers only English and 6 other languages[^8], so whether Chinese works is unconfirmed |
| Unreal Speech | 250,000 characters a month, reset on the 1st of every month[^9][^10] | Audio published on the free tier must credit it with a link[^10]; no voice cloning[^10] | Has Mandarin[^10] |
| ElevenLabs | 10,000 credits a month[^67] | No commercial use; published content must credit it[^68] | Supports Mandarin[^69] |
| Cartesia | 20K credits a month[^70], about 27 minutes[^70] | Commercial license starts at the Pro tier[^70] | Supports Chinese[^71] |
| Fish Audio | `s2.1-pro-free` has a unit price of 0[^13] | Fair-use limits apply; the amount is not stated[^14] | Chinese is a tier-1 language[^72] |
| Cloudflare Workers AI | 10,000 Neurons a day[^73] | About 536 minutes of MeloTTS a day (converted); resets daily at 00:00 UTC[^73] | Whether the hosted MeloTTS can synthesize Chinese was not verified; the `lang` parameter defaults to `en`[^74] |
| NVIDIA build | Free trial of every model, no card required[^75] | Trial use only, not for production[^76]; may be rate-limited[^77] | `magpie-tts-multilingual` supports Mandarin[^78] |
| Groq | 100 Orpheus requests a day on the free plan[^79] | — | English and Arabic only[^80] |
| Xiaomi MiMo | Three TTS models free for a limited time[^15] | 100 requests per minute[^81]; neither the end date nor the price afterwards is published | Has Chinese voices and optional dialect styles[^82] |
| ModelScope API-Inference | Free for developers to try[^83] | Whether TTS models are included was not verified | — |
| Edge read-aloud (edge-tts) | Free, with no official quota statement | edge-tts calls Edge's online read-aloud service[^16], which is not an API Microsoft offers to developers (inferred); Microsoft forbids custom SSML[^16]; older versions return 403 since October[^17] | The Hermes docs list 322 voices in 74 languages[^84] |

In addition, IBM watsonx Text to Speech gives 10,000 characters free a month[^85], but its language list has no Chinese (inferred).

### 3.2 One-Time Credits for New Users

In China:

| Platform | Credit | Validity and conditions |
| --- | --- | --- |
| Tencent Cloud | 20,000 characters for super-natural large-model voices, 100,000 for large-model voices, 8 million for basic/premium voices[^19] | 3 months after claiming, once per account, not for the long-text or podcast APIs[^19]; real-name and face verification required before activation[^86] |
| Tencent Cloud | One-sentence cloning: 5 voices and 10,000 characters of synthesis[^87] | Same as above |
| Alibaba NLS | 3-month speech synthesis trial[^20], unlimited calls, concurrency 2[^21] | Long-text synthesis and CosyVoice streaming synthesis have no trial[^20] |
| Baidu AI Cloud | Short-text basic/premium voices: 50,000 calls for individuals, 100,000 for businesses[^22]; long text: 50,000 characters for individuals[^22] | Valid forever, issued once per verified entity[^22] |
| Baidu AI Cloud | Large-model voice cloning: 10 creations and 50,000 characters of synthesis for individuals[^22] | Same as above |
| iFlytek | Online synthesis: 10,000 calls for individuals, 20,000 for businesses, 3 months[^65] | Real-name verification before claiming[^88]; each product can be claimed only once[^88] |
| iFlytek | Super Smart TTS: 10,000 characters for individuals[^89]; long text: 100,000 characters, 30 days[^90] | — |
| iFlytek | One-sentence cloning: 5 trainings and 50,000 characters of synthesis, 3 months[^91] | Claimed after verification |
| Doubao Speech | Speech synthesis 2.0 and voice cloning 2.0: 20,000 characters each, half a year[^24]; podcast model: 1 million tokens[^24] | Claim it by clicking "Trial" in the console[^24]; all voices can be used during the trial[^24] |
| Alibaba Bailian | 10,000 characters for most TTS models[^7]; 1 million tokens for each token-billed model[^7] | 90 days[^25]; Beijing region only[^25]; no real-name verification needed[^25] |
| Alibaba Bailian | Voice cloning `qwen-voice-enrollment`: 1,000 voices[^7] | — |
| MiniMax, StepFun, Zhipu, SiliconFlow | The official docs don't say how much they give | StepFun mentions a "free plan" that requires real-name verification[^92] |

Abroad:

| Platform | Credit | Notes |
| --- | --- | --- |
| Google Cloud | \$300 for new customers, 90 days[^93] | Can be used for TTS |
| Azure | \$200 for a free account, 30 days[^94] | Sign-up requires credit card verification[^94]; not valid for Azure China[^94] |
| AWS | Up to \$200 in credits for new customers, usable for Polly[^95] | The free plan lasts 6 months[^95] |
| Deepgram | \$200, no expiry[^96] | Aura doesn't support Chinese[^97] |
| Speechmatics | First 1 million characters free, plus \$100[^98] | Only 4 English voices[^99] |
| Rime | \$50[^100] | No Chinese[^100] |
| Smallest.ai | \$10[^101] | Chinese only in v3.1 Pro[^102] |
| Inworld | The on-demand tier includes about 70 minutes of TTS[^103] | Chinese is a tier-1 language[^104] |
| Murf | The pricing page says \$10 on sign-up[^105]; the API docs say a one-time 100,000 characters[^106] | The two contradict each other |
| Lemonfox | First month free[^107] | Supports Chinese[^108] |
| SiliconFlow international | \$1[^109] | — |
| Hume | \$20[^110] | TTS stops on 2026-11-13 |

### 3.3 TTS in Monthly Plans

- **StepFun Step Plan**:
  - The Mini tier costs ¥49 a month and includes 400M Credit[^111]; 1 yuan = 1 million Credit[^111], and speech is deducted at the open platform's prices[^112]. On that basis, ¥49 is worth 400 yuan of open-platform usage (converted).
  - Step Plan supports only one TTS model, `stepaudio-2.5-tts`[^112]; at 5.8 yuan per 10,000 characters[^28] it can synthesize about 690,000 characters, assuming the whole quota goes to TTS (converted). The plan's own rate limits were not found.
- **MiniMax M Plan**: the Go tier starts at a list price of ¥49 a month[^113], and all three tiers include image and audio models[^114]. Audio shares the quota with text and is deducted at pay-as-you-go prices[^115]; how many characters that covers is not published. The vendor recommends pay-as-you-go for production[^115].
- **Xiaomi MiMo Token Plan**: TTS is free for a limited time and doesn't consume plan credits[^116].
- **Overseas subscriptions**:
  - MiniMax international Audio Subscription from \$5 a month[^117].
  - ElevenLabs Starter: \$6 a month, with 30,000 credits, a commercial license and instant cloning[^67].
  - Cartesia Pro: \$5 a month for 100K credits, with a commercial license and instant cloning[^70]; Fish Audio Plus: \$15 a month[^118].

## 4. Pay-As-You-Go Prices

### 4.1 China (RMB)

The "equivalent" column is a converted value: pure Chinese text at the official list price of the first tier.

| Platform | Model or voice | Official unit price | Equivalent, yuan per 10,000 Chinese characters | Notes |
| --- | --- | --- | --- | --- |
| Huawei Cloud SIS | Standard voices | Packs: 10,000 calls for 18 yuan, 1 million calls for 1,600 yuan[^119] | 0.16–0.18 | Every 100 characters count as 1 call[^57]; premium voices count every 50 characters as 1 call, which doubles the equivalent |
| Tencent Cloud | Premium voices | 0.3 yuan per 10,000 characters[^19] | 0.3 | Prepaid packs as low as 0.21[^19] |
| Baidu AI Cloud | Short-text basic voices | 2.0 yuan per thousand calls[^120] | 0.33 | About 60 Chinese characters per call[^23]; premium voices 4.0 yuan per thousand calls[^120], equivalent to 0.67 |
| Alibaba NLS | Speech synthesis | 3.50 yuan per thousand calls[^121] | 0.7 | Every 100 characters count as 1 call, and a Chinese character counts as 2[^20] |
| StepFun | `step-tts-mini` | 0.9 yuan per 10,000 characters[^28] | 0.9 | A Chinese character counts as 1 character[^28] |
| Tencent Cloud | Large-model voices | 1.2 yuan per 10,000 characters, down to 0.55 at high daily volume[^19] | 1.2 | Prepaid packs as low as 0.4[^19] |
| SiliconFlow | CosyVoice2-0.5B, MOSS-TTSD | ¥0.05 per thousand UTF-8 bytes[^122] | 1.5 | About 3 bytes per Chinese character |
| Alibaba Bailian | `qwen3-tts-flash`, `cosyvoice-v3.5-flash` | 0.8 yuan per 10,000 characters[^7] | 1.6 | A Chinese character counts as 2 characters[^7] |
| Azure China | Neural voices | ¥95.4 per million characters[^3] | 1.9 | A Chinese character counts as 2 characters |
| Alibaba Bailian | `cosyvoice-v3-flash`, `qwen-audio-3.0-tts-flash` | 1 yuan per 10,000 characters[^7] | 2 | — |
| Zhipu | GLM-TTS | 2 yuan per 10,000 characters[^34] | About 2 | How Chinese characters count is not stated; estimated at 1 character each |
| Unisound | U2-TTS | 2 yuan per 10,000 characters[^123] | 2 | — |
| iFlytek | Super Smart TTS | A pack of 5 million characters for 1,000 yuan[^89] | 2 | Larger packs as low as 1.2[^89] |
| Baidu AI Cloud | Long-text basic voices | 2 yuan per 10,000 characters[^120] | 2 | — |
| StepFun | `stepaudio-3-tts`, `step-tts-2`, `stepaudio-2.5-tts` | 2.5, 2.8 and 5.8 yuan per 10,000 characters[^28] | 2.5–5.8 | — |
| Doubao Speech | Speech synthesis 2.0 | 3 yuan per 10,000 characters[^27] | 3 | Prepaid packs as low as 2.1[^27] |
| Alibaba Bailian | `cosyvoice-v3.5-plus`, `cosyvoice-v3-plus` | 1.5 and 2 yuan per 10,000 characters[^7] | 3–4 | — |
| MiniMax China site | `speech-2.8-turbo` | 2 yuan per 10,000 characters[^26] | 4 | A Chinese character counts as 2 characters[^26] |
| Tencent Cloud | Super-natural large-model voices | 6.5 yuan per 10,000 characters[^19] | 6.5 | — |
| MiniMax China site | `speech-2.8-hd` | 3.5 yuan per 10,000 characters[^26] | 7 | — |
| iFlytek | Online synthesis | 500,000 calls for 2,000 yuan[^65] | — | How many characters one call covers is not stated |

### 4.2 Abroad (USD)

Most overseas vendors don't say how Chinese characters count, so the "equivalent" column assumes 1 Chinese character = 1 character (converted).

| Platform | Model | Official unit price | Equivalent, yuan per 10,000 Chinese characters | Chinese | Notes |
| --- | --- | --- | --- | --- | --- |
| OpenRouter | Kokoro 82M | \$0.62 per million characters[^30] | 0.04 | Yes, but rated low for quality[^32] | OpenAI-compatible[^124] |
| DeepInfra | Kokoro-82M | \$0.99 per million characters[^31] | 0.07 | Same as above | A card or prepayment is required[^125] |
| DeepInfra | chatterbox-multilingual | \$1.00 per million characters[^31] | 0.07 | Supported[^31] | — |
| Lemonfox | — | \$2.50 per million characters[^108] | 0.17 | Supported[^108] | OpenAI-compatible[^108] |
| Google Cloud | Standard, WaveNet | \$4 per million characters[^5] | 0.27 | Supported | Has a free quota |
| Together AI | Kokoro | \$4 per million characters[^126] | 0.27 | — | Minimum prepayment \$15[^127] |
| Speechify | simba | \$10–6 per million characters beyond the plan[^8] | 0.4–0.67 | Contradictory | — |
| Unreal Speech | — | \$20–8 per million characters beyond the plan[^10] | 0.53–1.34 | Supported | Built on Kokoro[^9] |
| Murf | Falcon 2.1 | \$10 per million characters[^128] | 0.67 | Not verified | — |
| Mistral | Voxtral TTS 3 | \$13 per million characters[^129] | 0.87 | Sources contradict each other[^130][^131] | — |
| xAI | — | \$15 per million characters[^132] | 1.0 | Supported[^133] | — |
| OpenAI | `tts-1` | \$15 per million characters[^134] | 1.0 | Supported; voices are optimized for English[^43] | Shuts down on 2027-01-06 |
| Inworld | TTS-2 Flash / TTS-2 | \$15 / \$25 per million characters[^103] | 1.0 / 1.67 | Supported | Has an OpenAI-compatible endpoint[^135] |
| Amazon Polly | Neural | \$16 per million characters[^95] | 1.07 | Mandarin has only 1 female voice[^136] | — |
| DeepInfra | Qwen3-TTS | \$20 per million characters[^31] | 1.34 | Supported[^31] | Can clone from a 3-second sample[^31] |
| SiliconFlow international | CosyVoice2 | \$7.15 per million UTF-8 bytes[^109] | 1.43 | Supported | — |
| Azure | Neural voices | \$15 per million characters[^137] | 2.0 | Supported | A Chinese character counts as 2 characters |
| Google Cloud | Chirp 3 HD | \$30 per million characters[^5] | 2.0 | Supported | — |
| Gemini API | `3.8-flash-lite-tts` / `3.8-flash-tts` | Audio output \$6 / \$9 per million tokens[^11] | 2.3 / 3.5 | Supported | 25 tokens per second of audio[^11]; prices double from 2027 |
| ElevenLabs | Flash / v3, v4 | \$0.04 / \$0.08 per thousand characters[^138] | 2.7 / 5.3 | Supported | — |
| Cartesia | Sonic | \$38–65 per million credits beyond the plan[^70] | 2.5–4.3 | Supported | 1 credit = 1 character[^70] |
| Fish Audio | `s2.1-pro` | \$15 per million UTF-8 bytes[^13] | 3.0 | Supported | — |
| MiniMax international | turbo / hd | \$60 / \$100 per million characters[^117] | 4.0 / 6.7 | Supported | — |
| Deepgram | Aura-2 | \$0.030 per thousand characters[^96] | — | Not supported[^97] | — |
| Groq | Orpheus | \$22 per million characters[^139] | — | Not supported[^80] | — |

Other platforms that host open models:

- fal.ai's Kokoro costs \$0.02 per thousand characters and has a Mandarin-only endpoint with 8 Chinese voices[^140]. IndexTTS 2.0 is billed by the second at \$0.002 per second[^141], about 31 yuan per 10,000 Chinese characters (converted).
- Replicate bills by hardware-seconds, T4 at \$0.000225 per second[^142]; the community-uploaded Kokoro costs about \$0.00042 per run[^32].
- Cloudflare's MeloTTS costs \$0.0002 per audio minute[^73].
- Hugging Face Inference Providers gives free users no monthly credit[^143]. Only 7 TTS models are connected (counted from the API response), such as Kokoro-82M[^144] and chatterbox[^144].

## 5. Voice Cloning and Voice Design

| Platform | Cloning or design fee | Synthesis price | Sample requirements and limits |
| --- | --- | --- | --- |
| Alibaba Bailian | Creating a cloned voice is free for Qwen-Audio-TTS and CosyVoice[^33]; voice design is free too[^145] | At the target model's price | 10–20 seconds recommended, 60 seconds at most[^33]; up to 1,000 voices per account[^33] |
| Alibaba Bailian | Qwen-TTS cloning 0.01 yuan per voice, with 1,000 voices free[^7] | — | — |
| MiniMax China site | Rapid cloning and voice design 9.9 yuan per voice each, charged only at the first synthesis[^26] | Same as regular synthesis | 10 seconds to 5 minutes[^146]; deleted if not used within 7 days[^147] |
| MiniMax international | Cloning \$1.5 per voice, design \$3 per voice[^117] | Same as regular synthesis | — |
| StepFun | 9.9 yuan per voice, charged once the clone succeeds[^28] | Same as regular synthesis | 5–10 seconds[^148] |
| Zhipu | GLM-TTS-Clone 6 yuan per clone[^34] | — | About 3 seconds[^149] |
| Baidu AI Cloud | 8.8 yuan per voice, as low as 4 yuan prepaid[^35] | 7 yuan per 10,000 characters[^35] | — |
| Tencent Cloud | One-sentence cloning 39 yuan per voice, 12 yuan in large packs[^87] | 8 yuan per 10,000 characters, down to 6.4 at volume[^87] | 5–15 seconds[^150]; free storage for 3 months, then 0.03 yuan per voice per day[^87] |
| iFlytek | One-sentence cloning (standard) training 5 yuan per run, down to 3 yuan at volume[^91] | 2 yuan per 10,000 characters, down to 1.5 at volume[^91] | — |
| Unisound | 10 yuan per voice, charged at the first synthesis[^123] | 2 yuan per 10,000 characters | — |
| Doubao Speech | Voice slots 138 yuan each, down to 28 yuan at volume[^27] | 3 yuan per 10,000 characters[^27] | 5 seconds at minimum[^151]; a preview voice not formally used within 7 days is deleted[^27] |
| ElevenLabs | Instant cloning from Starter (\$6 a month)[^67] | Same as regular synthesis | Less than 2 minutes of audio is enough[^152] |
| Cartesia | Instant cloning from Pro (\$5 a month)[^70] | Same as regular synthesis | From 10 seconds[^153] |
| Inworld | Instant cloning is available to all users[^154] | Same as regular synthesis | From 3 seconds |
| Fish Audio | Voice design \$0.01 per request[^13] | Same as regular synthesis | At least 10 seconds[^155] |
| Gemini API | The 3.8 TTS models support cloning and design[^64] | The pricing page lists no extra fee | 10–30 seconds, plus a consent recording[^156] |
| xAI | Up to 30 can be created free in the console[^157] | Same as regular synthesis | Only available in the US (except Illinois)[^157] |
| OpenAI | Cloning from recordings is open only to eligible customers[^158] | — | — |

## 6. Chinese and Dialects

- Chinese platforms with many dialects:
  - The system voices of Bailian's `qwen3-tts-flash` cover the Beijing, Shanghai, Sichuan, Nanjing, Shaanxi, Minnan and Tianjin dialects and Cantonese[^159].
  - iFlytek has 11 dialects[^65]; Baidu's large-model voices include Cantonese, Sichuanese and other dialect voices[^160]; Doubao has more than 130 voices covering many dialects and accents[^151].
- Abroad:
  - Besides Mandarin, Azure has Cantonese, Wu and Sichuanese[^61]; Google has about 30 Chirp3-HD voices for Mandarin[^62].
  - Amazon Polly has only 1 female voice each for Mandarin and Cantonese[^136].
  - Not supporting Chinese: Deepgram Aura[^97], Hume[^44] and Rime[^100].
  - Speechmatics[^99] and Groq[^80] don't support Chinese either.

## 7. Open-Weight Models (Self-Hosted)

| Model | Weights license | Commercial use | Chinese | Notes |
| --- | --- | --- | --- | --- |
| CosyVoice 3 (Alibaba) | Apache-2.0[^47] | Yes | 9 languages, 18+ dialects[^161] | Bidirectional streaming, about 150ms latency[^161] |
| Qwen3-TTS (Alibaba) | Apache-2.0[^48] | Yes | 10 languages, with dialect voices[^162] | 3-second cloning[^162]; about 97ms latency[^162] |
| VoxCPM2 (ModelBest) | Apache-2.0, explicitly free for commercial use[^49] | Yes | 9 dialects[^49] | About 8GB of VRAM[^49]; vLLM-Omni can serve an OpenAI-compatible endpoint[^163] |
| MOSS-TTSD | Apache-2.0[^164] | Yes | Supported | Long multi-speaker dialogue, zero-shot cloning[^164]; 8B parameters[^164] |
| FireRedTTS-2 (Xiaohongshu) | Apache-2.0[^165] | Yes | 7 languages including Chinese[^165] | 4-speaker, 3-minute dialogues[^166]; about 9GB of VRAM in bf16[^166] |
| SoulX-Podcast | Apache-2.0[^167] | Yes | Sichuanese, Henanese, Cantonese[^167] | No streaming yet[^168] |
| Step-Audio-TTS-3B (StepFun) | Apache-2.0[^169] | Yes | Cantonese, Sichuanese and other dialects[^256] | Emotion and style control[^169] |
| GPT-SoVITS | MIT[^170][^171] | Yes | Chinese, English, Japanese, Korean, Cantonese[^172] | 5-second zero-shot, fine-tuning on 1 minute of data[^172] |
| Ming-3.0-tts-0.5B (Ant Group) | MIT[^173] | Yes | Sichuanese, Cantonese[^173] | More than 100 Chinese voices[^173] |
| GLM-TTS (Zhipu) | The model card says MIT[^174], the code repo says Apache-2.0[^175] | Yes | Mainly Chinese[^176] | 3–10-second cloning[^176] |
| Kokoro-82M | Apache[^177] | Yes | 8 preset Mandarin voices[^178] | No cloning feature (inferred) |
| Chatterbox (Resemble) | MIT[^179] | Yes | The multilingual version includes Chinese[^179] | Output carries an invisible watermark[^179] |
| Zonos (Zyphra) | Apache-2.0[^180] | Yes | Supported[^181] | — |
| IndexTTS-2 (Bilibili) | Bilibili's own license, royalty-free[^182] | A separate license is needed above 100 million monthly active users or 1 billion yuan in annual revenue[^182] | Supported | May not be used to improve other models[^182] |
| Higgs Audio 2 (Boson) | Community license[^183] | Above 100,000 annual active users you must apply[^183] | — | — |
| Fish Speech | Community license[^184] | Commercial use allowed under \$500,000 in annual revenue[^184], but not for hosted services offered to others[^184] | Chinese is a tier-1 language[^72] | The S2-Pro weights are under a research license[^72] |
| F5-TTS | Code MIT, weights CC-BY-NC[^50] | No | — | — |
| Spark-TTS | CC-BY-NC-SA[^51] | No | — | — |
| MaskGCT | CC-BY-NC[^185] | No | — | — |
| ChatTTS | Model CC BY-NC[^186] | No | — | — |
| XTTS-v2 | Coqui Public Model License, non-commercial only[^52] | No | — | Coqui has shut down (per a founder's tweet quoted in a GitHub community discussion)[^187] |

Other notes:

- MegaTTS3 has not released its encoder parameters, so it can't clone from arbitrary audio[^188].
- Microsoft removed the VibeVoice TTS code on 2025-09-05[^189].
- The original Piper repository is archived[^190], and the new repository is GPL-3.0[^191].
- Even when the license says Apache or MIT, the training data may still carry licensing problems; assess this yourself before commercial use (inferred).

## 8. Data Policies and Commercial Terms

| Platform | Used for training? | Other |
| --- | --- | --- |
| OpenAI | Not used for training by default[^38] | Abuse-monitoring logs are kept for up to 30 days[^38]; users must be told that the voice they hear is AI-generated[^43] |
| Google Cloud TTS | Text and audio are not logged[^39] | Generated audio can be used in applications and media[^192] |
| Gemini API | The free tier is used to improve products[^11], and human reviewers may read inputs and outputs[^193]; the paid tier is not | — |
| Azure | Neither input nor output of prebuilt voices is logged[^40] | — |
| Amazon Polly | May be used to improve the service[^37], with an opt-out[^37] | — |
| ElevenLabs | Used by default, with an opt-out; not used for enterprise customers by default[^36] | The free tier can't be used commercially[^68]; all paid tiers include a commercial license[^68] |
| xAI | Not used for training without permission; kept for 30 days by default[^194] | — |
| Mistral | Training can be turned off separately[^195] | — |
| Hume | Users grant Hume a perpetual license to use recordings to improve the service[^196] | — |
| DeepInfra | No training, no storage (except Google and Anthropic models)[^197] | — |
| NVIDIA trial | Content is not stored after the session ends[^76], but anonymous metrics are collected for improvement[^76] | Not for production[^76] |
| Alibaba Bailian | Not used for training[^41] | — |
| Doubao Speech | Not used for training, with exceptions[^42] | Licensed for use only in mainland China[^42] |
| Tencent Cloud | The FAQ says the API doesn't store data[^54] | The FAQ says commercial use is allowed[^54] |
| Huawei Cloud | Synthesis text is released right after processing[^198] | — |
| iFlytek | The user agreement has no training clause (inferred) | Super Smart TTS can add audio watermarks[^56] |
| Zhipu | — | Adds visible and invisible watermarks by default[^199] |
| StepFun | — | Audio belongs to the user, and labeling it as AI-generated is recommended[^200] |

## 9. Retired, Shutting Down or Not Recommended

| Platform or model | Status |
| --- | --- |
| OpenAI `tts-1`, `tts-1-hd`, `gpt-4o-mini-tts` | Deprecated on 2026-10-01, shut down on 2027-01-06[^201]; the replacement model runs on the Realtime API and doesn't support `/v1/audio/speech`[^43] |
| Hume TTS and EVI | Stop on 2026-11-13, after which account data is deleted[^44] |
| PlayHT / PlayAI | Acquired by Meta in July 2025[^45]; fully shut down on 2025-12-31, with accounts and cloned voices deleted (source: a migration guide from the competitor Inworld)[^46] |
| Groq's PlayAI TTS | Retired on 2025-12-31 and replaced by Orpheus[^202] |
| LMNT | Shut down[^203] |
| Resemble AI | No longer sells TTS as a commercial product[^204] |
| Inworld `tts-1`, `tts-1-max` | Service ended on 2026-06-15[^205] |
| Fish Audio `s1` | Retires on 2026-12-31[^206] |
| Rime Arcana | Retired on 2026-08-15[^207] |
| Gemini `gemini-3.1-flash-tts-preview` | Marked as a legacy model[^208] |
| Doubao large-model speech synthesis 1.0 | Moved to the legacy-model price list[^27] |
| Bailian's Qwen3 instruct, cloning and design models | The detail pages of `qwen3-tts-instruct-flash`, `qwen3-tts-vc`, `qwen3-tts-vd` and others now redirect to a generic page, so they may be retired (inferred) |
| Edge read-aloud (edge-tts) | Older versions return 403 since October[^17]; 7.3.1 switched to the new token prefix[^18] and worked in a test on 10-21 |
| Microsoft VibeVoice | TTS code removed on 2025-09-05[^189] |
| Piper | The original repository is archived[^190], and the new repository is GPL-3.0[^191] |

## 10. How to Integrate

### 10.1 Endpoint Quick Reference

| Platform | API key page | Endpoint | Auth | OpenAI-compatible |
| --- | --- | --- | --- | --- |
| Alibaba Bailian | <https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key>[^209] | `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`[^210] | `DASHSCOPE_API_KEY`[^211] | Not found |
| Doubao Speech | <https://console.volcengine.com/speech/new/setting/apikeys>[^212] | `https://openspeech.bytedance.com/api/v3/tts/unidirectional`[^213] | `X-Api-Key` + `X-Api-Resource-Id`[^213] | No |
| Tencent Cloud | <https://console.cloud.tencent.com/cam/capi>[^214] | `tts.tencentcloudapi.com`, Action=TextToVoice[^215] | TC3-HMAC-SHA256 signature[^216] | No |
| Baidu AI Cloud | "Application list" in the console[^217] | `https://tsn.baidu.com/text2audio`[^23] | Exchange an API Key + Secret Key for an access_token[^217] | No |
| iFlytek | The service page in the console[^218] | `wss://tts-api.xfyun.cn/v2/tts`[^218] | HMAC-SHA256 signature[^218] | No |
| Huawei Cloud | — | `POST https://{endpoint}/v1/{project_id}/tts`[^57] | IAM Token[^57] | No |
| MiniMax China site | Account Management > API Keys[^219] | `https://api.minimax.cn/v1/t2a_v2`[^220] | Bearer[^220] | No |
| StepFun | <https://platform.stepfun.com/interface-key>[^221] | `https://api.stepfun.com/v1/audio/speech`[^222] | Bearer[^223] | Yes; the official example uses the OpenAI SDK[^222] |
| Zhipu | <https://bigmodel.cn/usercenter/proj-mgmt/apikeys>[^224] | `https://open.bigmodel.cn/api/paas/v4/audio/speech`[^199] | Bearer[^199] | Same path; fields not verified |
| SiliconFlow | API keys page[^225] | `https://api.siliconflow.cn/v1/audio/speech`[^29] | Bearer[^226] | Yes; the official example uses the OpenAI SDK[^29] |
| Xiaomi MiMo | — | `https://api.xiaomimimo.com/v1/chat/completions`[^227] | `api-key` or Bearer[^227] | Uses Chat Completions, not `/v1/audio/speech` |
| Azure China | — | `https://chinaeast2.tts.speech.azure.cn/cognitiveservices/v1`[^228] | Resource key or STS token[^228] | No |
| Azure | — | `https://<region>.tts.speech.microsoft.com/cognitiveservices/v1`[^229] | `Ocp-Apim-Subscription-Key`[^229] | No |
| Google Cloud | — | `texttospeech.googleapis.com`[^230] | OAuth token[^230] | No |
| Gemini API | <https://aistudio.google.com/api-keys>[^231] | `https://generativelanguage.googleapis.com/v1beta/interactions`[^64] | `x-goog-api-key`[^64] | No |
| OpenAI | — | `https://api.openai.com/v1/audio/speech`[^43] | Bearer[^43] | Native |
| ElevenLabs | — | `https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`[^232] | `xi-api-key`[^233] | No |
| Cartesia | <https://play.cartesia.ai/keys>[^234] | `https://api.cartesia.ai`[^234] | Bearer[^234] | No |
| Fish Audio | — | `https://api.fish.audio/v1/tts`[^235] | Bearer | No |
| Mistral | — | `https://api.mistral.ai/v1/audio/speech`[^236] | Bearer | Same path; returns base64-encoded audio[^236] |
| xAI | — | `https://api.x.ai/v1/tts`[^133] | Bearer | No |
| Inworld | — | `https://api.inworld.ai`[^135] | Basic | Has a compatible endpoint[^135] |
| Lemonfox | — | `https://api.lemonfox.ai/v1/audio/speech`[^108] | Bearer | Yes |
| Speechify | — | `https://api.speechify.ai/v1/audio/speech`[^237] | Bearer | Same path, different request fields |
| DeepInfra | — | `https://api.deepinfra.com/v1/audio/speech`[^238] | Bearer | Yes |
| OpenRouter | — | `https://openrouter.ai/api/v1/audio/speech`[^124] | Bearer | Yes |
| Together AI | — | `https://api.together.ai/v1/audio/speech`[^239] | Bearer | Yes |
| Groq | — | `https://api.groq.com/openai/v1/audio/speech`[^80] | Bearer | Yes |
| SiliconFlow international | — | `https://api.siliconflow.com/v1/audio/speech`[^240] | Bearer | Yes |
| NVIDIA build | — | `grpc.nvcf.nvidia.com:443` (Riva gRPC)[^241] | Bearer | No |
| Cloudflare | — | Native `ai/run` endpoint[^242] | API Token | Not compatible for TTS |
| Pollinations (community service) | — | `https://gen.pollinations.ai/v1/audio/speech`[^243] | — | Yes |

### 10.2 Notes

- **Bailian**: API keys, domains and model lists are separate for each region and can't be mixed[^209]. `qwen3-tts-flash` takes at most 600 characters per request[^210] and doesn't support cloning, design or instruction control[^159].
- **Doubao**: the trial and the activation are both done by hand in the console[^24]; the old console's AppID + Access Token authentication is being phased out[^244].
- **Tencent Cloud**: when a prepaid pack runs out, the service stops instead of switching to post-paid billing[^19]; `TextToVoice` takes at most 150 Chinese characters per request[^215].
- **MiniMax**: the synchronous API takes fewer than 10,000 characters per request[^220]; Cantonese voices need `language_boost` set to `Chinese,Yue`[^220].
- **StepFun**: at most 1,000 characters per request[^222].
- **SiliconFlow**: free models require real-name verification[^245], and so do custom voices[^29]; top-ups accept Alipay and WeChat Pay[^246].
- **Zhipu**: watermarks are added by default[^199]; a single input is limited to a length of 1024[^199].
- **Google Cloud**: a single request is at most 5,000 bytes[^192], about 1,666 characters of pure Chinese (converted).
- **Amazon Polly**: at most 3,000 billed characters per request[^59].
- **Fish Audio, xAI, Mistral**: unreachable with the default DNS; see Section 11.

## 11. Connectivity Test from Networks in China (2026-10-21)

- **Method**: on a network in China, curl connected directly to each platform's API address without a proxy; any HTTP status code counts as reachable. The results reflect only this one network at the time of the test.
- **All Chinese platforms are reachable**: Bailian, Alibaba NLS, Doubao, Tencent, Baidu, iFlytek, MiniMax, StepFun, Zhipu, SiliconFlow, ModelScope, Huawei Cloud and Azure China.
- **Reachable directly abroad**: OpenAI, Google Cloud TTS, Gemini, Azure, Amazon Polly, Edge read-aloud, ElevenLabs, Cartesia, Deepgram, Inworld, Hume, MiniMax international, Unreal Speech, Smallest.ai, Speechify, Murf, Rime, DeepInfra, Replicate, fal.ai, Together, Groq, Hugging Face, NVIDIA, Cloudflare, SiliconFlow international, Novita, Pollinations and Puter.
- **Unreachable with the default DNS**: Fish Audio, xAI and Mistral. The default DNS returns wrong IPs and the connection times out; the IPs returned by Alibaba's public DNS over HTTPS don't connect either. With the IPs resolved through Cloudflare's DNS over HTTPS, all three connect. LMNT's connection is reset, and that service has shut down.
- **Reachable doesn't mean users in mainland China are allowed**:
  - OpenAI states that use outside its list of supported regions may get the account blocked[^247], and the list includes neither mainland China nor Hong Kong (inferred, from searching the list).
  - The Gemini API's available regions don't include mainland China or Hong Kong either[^12].
  - Conversely, Doubao Speech is licensed for use only in mainland China[^42].

## 12. Open Questions

1. iFlytek online synthesis: how many characters one call covers and the concurrency; whether the free quota is "500 calls a day", "a 10,000-call pack", or both.
2. Huawei Cloud: the unit of the on-demand price, whether there is a free quota, and the voice-cloning price.
3. Counting Chinese characters: not stated by Zhipu GLM-TTS, MiniMax international, or overseas vendors such as OpenAI, Gemini, Polly, ElevenLabs and Cartesia.
4. Exact free-quota numbers: Gemini's free-tier TTS rate limits, the fair-use cap of Fish Audio `s2.1-pro-free`, Mistral's free tier, NVIDIA's trial credits, and the new-user credits of MiniMax, StepFun, Zhipu and SiliconFlow.
5. When Xiaomi MiMo's free TTS period ends, and the price afterwards.
6. Whether the Doubao trial requires real-name verification, and its concurrency during the trial; the new-customer price of 110.40 yuan for a cloned voice was seen only in a search snippet.
7. Whether Bailian's Qwen3 instruct, cloning and design models have been retired: the official notices are JavaScript pages, and their text could not be fetched.
8. Whether Speechify's self-serve plans can use the Chinese-capable model `simba-3.5`; whether Murf's free credit is monthly or one-time.
9. The account-opening requirements of Azure China (21Vianet), and whether individuals can sign up.
10. Whether ModelScope API-Inference includes TTS models; whether Kimi, Baidu Qianfan, Tencent Hunyuan, Coze and Baichuan offer TTS APIs was not checked this time.
11. Whether overseas platforms accept bank cards issued in mainland China, Alipay or WeChat Pay; none of them say.

## Appendix: Integrating with Hermes Agent

This section is based on the docs and source code of Hermes v0.22.2. Except where marked "tested", nothing was called with a real key.

**Built-in providers**: Hermes has 11 built-in TTS providers; Edge TTS is the default, free, and needs no key[^84]. Gemini TTS has a free tier, and NeuTTS, KittenTTS and Piper run locally for free[^84].

**Chinese support in the free local engines**:

- NeuTTS's language list has no Chinese[^248].
- KittenTTS 0.8 ships 8 preset voices such as Bella and Jasper[^249], none of them Chinese (inferred).
- The official Piper voice library has `zh_CN` voices, such as `zh_CN-chaowen-medium`[^250]; voices.json lists 4 of them. `tts.piper.voice` accepts a voice name directly, and Hermes downloads it automatically[^84].

**Edge TTS 403**:

- Hermes v0.22.2 pins edge-tts at 7.2.7[^251]. The token version prefix in 7.2.7 is `1-`[^252], while Microsoft has required the new format since October[^17]. In a test on 10-21, the 7.2.7 bundled with Hermes returned 403.
- edge-tts 7.3.1 has switched to the `2-` prefix[^18] and synthesized Chinese in a test. You can install the new version separately with `uv tool install edge-tts` and wire it in as a command provider[^84] as follows:

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

- Keep the `env -u PYTHONPATH -u PYTHONHOME` prefix: if the child process inherits a `PYTHONPATH` that points into Hermes's virtual environment, the separately installed edge-tts loads the 7.2.7 bundled with Hermes (tested) and still gets 403.
- `edge-tts` must be on `PATH`; otherwise use its absolute path.

**OpenAI-compatible endpoints**:

- The OpenAI provider's `base_url` can point at any OpenAI-compatible TTS endpoint[^84]. The key is read from `tts.openai.api_key`, `VOICE_TOOLS_OPENAI_KEY` and `OPENAI_API_KEY`, in that order[^253].
- Taking SiliconFlow as an example (the model and voice names come from its official example[^29]):

```bash
# Add a line VOICE_TOOLS_OPENAI_KEY=<your SiliconFlow key> to ~/.hermes/.env, then:
hermes config set tts.provider openai
hermes config set tts.openai.base_url https://api.siliconflow.cn/v1
hermes config set tts.openai.model FunAudioLLM/CosyVoice2-0.5B
hermes config set tts.openai.voice FunAudioLLM/CosyVoice2-0.5B:alex
```

- StepFun: set `base_url` to `https://api.stepfun.com/v1`[^222], with the model `step-tts-mini` and the voice `cixingnansheng`[^222].
- OpenRouter, Lemonfox, Together, Groq, SiliconFlow international and others can be wired in the same way, with the addresses in Section 10.1; DeepInfra has a built-in provider[^84].
- Hermes's OpenAI speech recognition reads its key through the same function[^254][^255]. If speech recognition also uses the OpenAI provider, the two share `VOICE_TOOLS_OPENAI_KEY`; in that case you can put the TTS key in `tts.openai.api_key`, which has the highest priority[^253], but it is then stored in plain text in config.yaml.

**MiniMax**: a built-in provider; with `tts.minimax.region` set to `cn` it uses the China site `api.minimaxi.com` and reads `MINIMAX_CN_API_KEY`[^84]. MiniMax's China docs now use `api.minimax.cn` as the default domain[^220], and both domains were reachable on 10-21 (tested). The default model in the docs is `speech-02-hd`[^84], at 3.5 yuan per 10,000 characters[^26]; switching to `speech-2.8-turbo` costs 2 yuan per 10,000 characters[^26].

**Gemini**: a built-in provider; the default model in the docs is `gemini-2.5-flash-preview-tts`[^84], which costs nothing on the free tier[^11]. The available regions don't include mainland China or Hong Kong; see Section 11.

**Doubao**: the Hermes docs give an example of wiring Doubao seed-tts-2.0 in as a command provider, using the third-party `doubao-speech` package[^84], with AppID + Access Token authentication[^84]. Volcengine says this old-console authentication is being phased out[^244].

**Secrets in command providers**: Hermes scrubs secrets from the child process environment, so any variable the command needs must be listed in `env_passthrough`[^84].

**Self-hosted open models**: VoxCPM2 can serve an OpenAI-compatible `/v1/audio/speech` through vLLM-Omni[^163]; then point the OpenAI provider's `base_url` at that service. Command-line tools can be wired in as a command provider[^84].

## References

The pages cited in the text are listed below, captured on 2026-10-21.

[^1]: [Euro foreign exchange reference rates (ECB)](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml)
[^2]: [Azure Speech pricing | Microsoft Azure](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services)
[^3]: [Azure AI services pricing details – Azure (azure.cn)](https://www.azure.cn/pricing/details/cognitive-services)
[^4]: [Text to speech overview - Speech service | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech)
[^5]: [Text-to-Speech pricing | Google Cloud](https://cloud.google.com/text-to-speech/pricing?hl=en)
[^6]: [Online speech synthesis service description | iFlytek Open Platform docs](https://www.xfyun.cn/doc/tts/online_tts/tts_description.html)
[^7]: [Alibaba Cloud Bailian model pricing - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/model-pricing)
[^8]: [Text-to-Speech API Pricing | SpeechifyAI](https://speechify.ai/pricing)
[^9]: [Text-to-Speech API Pricing - Unreal Speech](https://unrealspeech.com/pricing)
[^10]: [Unreal Speech: Cheapest Text-to-Speech API](https://unrealspeech.com)
[^11]: [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing.md.txt)
[^12]: [Available regions for Google AI Studio and Gemini API](https://ai.google.dev/gemini-api/docs/available-regions.md.txt)
[^13]: [Pricing & Rate Limits | Fish Audio Docs](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits.md)
[^14]: [Models Overview | Fish Audio Docs](https://docs.fish.audio/developer-guide/models-pricing/models-overview.md)
[^15]: [Xiaomi MiMo pay-as-you-go API pricing](https://mimo.mi.com/static/docs/price/pay-as-you-go.md)
[^16]: [rany2/edge-tts README](https://raw.githubusercontent.com/rany2/edge-tts/master/README.md)
[^17]: [GitHub API edge-tts issues](https://api.github.com/repos/rany2/edge-tts/issues?state=all&per_page=30)
[^18]: [edge-tts 7.3.1 wheel (PyPI) edge_tts/constants.py](https://files.pythonhosted.org/packages/35/86/3b97d755992777d5a9ca0e45a8ec96cc9858b2d6dd8f65f3f688d60e8709/edge_tts-7.3.1-py3-none-any.whl)
[^19]: [Speech synthesis billing overview (online edition) - Tencent Cloud](https://cloud.tencent.com/document/product/1073/34112)
[^20]: [Intelligent Speech Interaction billable items, billing units and billing methods - Alibaba Cloud Help Center](https://help.aliyun.com/zh/isi/getting-started/pricing)
[^21]: [How non-developers can quickly use Intelligent Speech Interaction - Alibaba Cloud Help Center](https://help.aliyun.com/zh/isi/getting-started/user-guide-for-non-developers)
[^22]: [Free test resources - Speech Technology - Baidu AI Cloud](https://cloud.baidu.com/doc/SPEECH/s/Wl9mh4doe)
[^23]: [Short-text online synthesis API - Speech Technology - Baidu AI Cloud](https://cloud.baidu.com/doc/SPEECH/s/mlbxh7xie)
[^24]: [Billing overview - Doubao Speech - Volcengine](https://www.volcengine.com/docs/DoubaoVoice/BillingOverview-15?lang=zh)
[^25]: [New-user free quota and the stop-when-exhausted switch - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/new-free-quota)
[^26]: [MiniMax Open Platform pricing overview](https://platform.minimaxi.com/docs/pricing/overview.md)
[^27]: [Doubao Speech billing instructions - Volcengine docs](https://docs.volcengine.com/docs/DoubaoVoice/Billinginstructions-21?lang=zh)
[^28]: [StepFun API pricing](https://platform.stepfun.com/docs/zh/guides/pricing/details.md)
[^29]: [SiliconFlow text-to-speech user guide](https://api-docs.siliconflow.cn/docs/userguide/capabilities/text-to-speech)
[^30]: [Best Text-to-Speech Models - OpenRouter](https://openrouter.ai/collections/text-to-speech-models)
[^31]: [Models | Machine Learning Inference | DeepInfra (text-to-speech)](https://deepinfra.com/models/text-to-speech)
[^32]: [jaaari/kokoro-82m – Replicate](https://replicate.com/jaaari/kokoro-82m)
[^33]: [Voice cloning - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)
[^34]: [Zhipu API pricing](https://docs.bigmodel.cn/cn/guide/start/pricing.md)
[^35]: [Large-model voice cloning - Speech Technology - Baidu AI Cloud](https://cloud.baidu.com/doc/SPEECH/s/vm9sbp4z9)
[^36]: [Is my data used to improve ElevenLabs' AI models? | ElevenLabs](https://elevenlabs.io/docs/help-center/legal/is-my-data-used-to-improve-eleven-labs-ai-models.md)
[^37]: [Amazon Polly FAQs](https://aws.amazon.com/polly/faqs)
[^38]: [Data controls in the OpenAI platform](https://developers.openai.com/api/docs/guides/your-data.md)
[^39]: [Data logging | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs/data-logging?hl=en)
[^40]: [Data, privacy, and security for text to speech | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security)
[^41]: [Compliance and privacy notice - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/privacy-notice)
[^42]: [Generative model service specific terms - Doubao Speech - Volcengine](https://docs.volcengine.com/docs/DoubaoVoice/Generativemodelservicespecificterms-1?lang=zh)
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
[^53]: [Alibaba Cloud speech synthesis API overview - Intelligent Speech Interaction - Alibaba Cloud Help Center](https://help.aliyun.com/zh/isi/developer-reference/overview-of-speech-synthesis)
[^54]: [Speech synthesis FAQ - Tencent Cloud](https://cloud.tencent.com/document/product/1073/34090)
[^55]: [Long-text online synthesis API - Speech Technology - Baidu AI Cloud](https://cloud.baidu.com/doc/SPEECH/s/ulbxh8rbu)
[^56]: [Super Smart TTS API docs | iFlytek Open Platform docs](https://www.xfyun.cn/doc/spark/super%20smart-tts.html)
[^57]: [Speech synthesis - RunTts API - API reference - Speech Interaction Service (SIS) - Huawei Cloud](https://support.huaweicloud.com/api-sis/sis_03_0111.html)
[^58]: [Text-to-speech - SiliconFlow docs (international)](https://docs.siliconflow.com/en/userguide/capabilities/text-to-speech.md)
[^59]: [Quotas in Amazon Polly - Developer Guide](https://docs.aws.amazon.com/polly/latest/dg/limits.html)
[^60]: [Speech service quotas and limits | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-services-quotas-and-limits)
[^61]: [Language and voice support for Azure Speech | Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)
[^62]: [Supported voices and languages | Cloud Text-to-Speech](https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types?hl=en)
[^63]: [Rate limits | Gemini API](https://ai.google.dev/gemini-api/docs/rate-limits.md.txt)
[^64]: [Text-to-speech generation (TTS) | Gemini API](https://ai.google.dev/gemini-api/docs/speech-generation.md.txt)
[^65]: [Online speech synthesis (text to speech) - iFlytek Open Platform](https://www.xfyun.cn/services/online_tts)
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
[^82]: [Xiaomi MiMo speech synthesis (MiMo-V2.5-TTS) guide](https://mimo.mi.com/static/docs/quick-start/usage-guide/audio/speech-synthesis-v2.5.md)
[^83]: [ModelScope API-Inference usage limits (page meta description)](https://modelscope.cn/docs/model-service/API-Inference/limits)
[^84]: [Voice & TTS | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/tts)
[^85]: [IBM Text to Speech pricing](https://www.ibm.com/products/text-to-speech/pricing)
[^86]: [Speech synthesis: one-minute server-side API quickstart - Tencent Cloud](https://cloud.tencent.com/document/product/1073/56640)
[^87]: [Voice cloning billing overview - Tencent Cloud](https://cloud.tencent.com/document/product/1283/93105)
[^88]: [iFlytek Open Platform free packages page (/free)](https://www.xfyun.cn/free)
[^89]: [Super Smart TTS: highly realistic AI voiceovers - iFlytek Open Platform](https://www.xfyun.cn/services/smart-tts)
[^90]: [Long-text speech synthesis (text to speech) - iFlytek Open Platform](https://www.xfyun.cn/services/online_tts_long)
[^91]: [One-sentence cloning: quick custom TTS voices online - iFlytek Open Platform](https://www.xfyun.cn/services/quick_tts)
[^92]: [StepFun FAQ](https://platform.stepfun.com/docs/zh/faq/common-questions.md)
[^93]: [Free Trial and Free Tier | Google Cloud](https://docs.cloud.google.com/free/docs/free-cloud-features?hl=en)
[^94]: [Create an Azure free account or pay as you go | Microsoft Azure](https://azure.microsoft.com/zh-cn/pricing/purchase-options/azure-account)
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
[^111]: [Step Plan plans and billing](https://platform.stepfun.com/docs/zh/step-plan/pricing.md)
[^112]: [Step Plan speech model integration](https://platform.stepfun.com/docs/zh/step-plan/integrations/audio-api.md)
[^113]: [MiniMax full docs llms-full.txt](https://platform.minimaxi.com/docs/llms-full.txt)
[^114]: [MiniMax M Plan overview](https://platform.minimaxi.com/docs/token-plan/intro.md)
[^115]: [MiniMax M Plan FAQ](https://platform.minimaxi.com/docs/m-plan/faq.md)
[^116]: [Xiaomi MiMo Token Plan](https://mimo.mi.com/static/docs/price/token-plan.md)
[^117]: [MiniMax Pricing Overview (minimax.io)](https://platform.minimax.io/docs/pricing/overview.md)
[^118]: [Pricing & Plans - Fish Audio](https://fish.audio/plan)
[^119]: [Huawei Cloud price calculator API (SIS speech synthesis SKUs)](https://portal.huaweicloud.com/api/calculator/rest/cbc/portalcalculatornodeservice/v4/api/productInfo?urlPath=sis&tag=general.online.portal&region=cn-north-4&tab=calc&sign=common)
[^120]: [Speech synthesis - Speech Technology - Baidu AI Cloud](https://cloud.baidu.com/doc/SPEECH/s/Ql9misjot)
[^121]: [Intelligent Speech Interaction billing methods and rates - Alibaba Cloud Help Center](https://help.aliyun.com/zh/isi/getting-started/billing-10)
[^122]: [SiliconFlow model pricing](https://siliconflow.cn/pricing)
[^123]: [Model pricing | Docs (Unisound Token Hub)](https://maas.unisound.com/docs/price/overview)
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
[^145]: [Voice design - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)
[^146]: [MiniMax rapid voice cloning guide](https://platform.minimaxi.com/docs/guides/speech-voice-clone.md)
[^147]: [MiniMax llms.txt docs index](https://platform.minimaxi.com/docs/llms.txt)
[^148]: [StepFun voice cloning API](https://platform.stepfun.com/docs/zh/api-reference/audio/create-voice.md)
[^149]: [Zhipu GLM-TTS-Clone model introduction](https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-tts-clone.md)
[^150]: [Speech synthesis, custom voices and text-to-speech service - Tencent Cloud](https://cloud.tencent.com/product/tts)
[^151]: [Product overview - Doubao Speech - Volcengine](https://www.volcengine.com/docs/DoubaoVoice/ProductOverview-9?lang=zh)
[^152]: [Voice cloning: how it works](https://elevenlabs.io/docs/eleven-api/concepts/voice-cloning.md)
[^153]: [Instant Voice Clone | Cartesia Docs](https://docs.cartesia.ai/build-with-cartesia/capability-guides/clone-voices.md)
[^154]: [Instant voice cloning | Inworld Docs](https://docs.inworld.ai/tts/instant-voice-cloning.md)
[^155]: [Voice Cloning Best Practices | Fish Audio Docs](https://docs.fish.audio/developer-guide/best-practices/voice-cloning.md)
[^156]: [Voice replication | Gemini API](https://ai.google.dev/gemini-api/docs/voice-replication.md.txt)
[^157]: [Custom Voices | SpaceXSI (xAI) Docs](https://docs.x.ai/developers/model-capabilities/audio/custom-voices.md)
[^158]: [Custom voices | OpenAI API](https://developers.openai.com/api/docs/guides/custom-voices.md)
[^159]: [Speech synthesis - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/tts-model)
[^160]: [Voice list - Speech Technology - Baidu AI Cloud](https://cloud.baidu.com/doc/SPEECH/s/Rluv3uq3d)
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
[^198]: [Huawei Cloud Speech Interaction Service (SIS) service statement](https://www.huaweicloud.com/declaration/sis.html)
[^199]: [Zhipu text-to-speech API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%9C%AC%E8%BD%AC%E8%AF%AD%E9%9F%B3.md)
[^200]: [StepFun audio synthesis best practices](https://platform.stepfun.com/docs/zh/guides/developer/tts.md)
[^201]: [Deprecations | OpenAI API](https://developers.openai.com/api/docs/deprecations.md)
[^202]: [Model Deprecation - GroqDocs](https://console.groq.com/docs/deprecations)
[^203]: [LMNT has shut down](https://www.lmnt.com)
[^204]: [Product Notice | Resemble AI](https://www.resemble.ai/product-notice)
[^205]: [TTS models | Inworld Docs](https://docs.inworld.ai/tts/tts-models.md)
[^206]: [Model Deprecations | Fish Audio Docs](https://docs.fish.audio/developer-guide/models-pricing/deprecations.md)
[^207]: [Remove Arcana model IDs | Rime docs](https://docs.rime.ai/docs/migrate-arcana-to-coda.md)
[^208]: [Gemini 3.1 Flash TTS Preview | Gemini API](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview.md.txt)
[^209]: [Get and configure an Alibaba Cloud Bailian API key - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/get-api-key)
[^210]: [Non-realtime speech synthesis (Qwen-TTS) API reference - Bailian - Alibaba Cloud](https://help.aliyun.com/zh/model-studio/qwen-tts-api)
[^211]: [Non-realtime speech synthesis - Model Studio - Alibaba Cloud Help Center](https://help.aliyun.com/zh/model-studio/qwen-tts)
[^212]: [Using API keys - Doubao Speech - Volcengine](https://docs.volcengine.com/docs/DoubaoVoice/APIKeyUsage?lang=zh)
[^213]: [Unidirectional streaming speech synthesis (HTTP) - Doubao Speech - Volcengine](https://docs.volcengine.com/docs/DoubaoVoice/unidirectional-streaming-text-to-speech-http?lang=zh)
[^214]: [Speech synthesis: realtime speech synthesis - Tencent Cloud](https://cloud.tencent.com/document/api/1073/94308)
[^215]: [Speech synthesis: basic speech synthesis - Tencent Cloud](https://cloud.tencent.com/document/product/1073/37995)
[^216]: [Speech synthesis: signature methods - Tencent Cloud](https://cloud.tencent.com/document/api/1073/37991)
[^217]: [Authentication - Speech Technology - Baidu AI Cloud](https://cloud.baidu.com/doc/SPEECH/s/Em8snejw1)
[^218]: [Online speech synthesis API docs | iFlytek Open Platform docs](https://www.xfyun.cn/doc/tts/online_tts/API.html)
[^219]: [MiniMax FAQ: APIs](https://platform.minimaxi.com/docs/faq/about-apis.md)
[^220]: [MiniMax synchronous speech synthesis HTTP API](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http.md)
[^221]: [StepFun quickstart](https://platform.stepfun.com/docs/zh/quickstart/overview.md)
[^222]: [StepFun speech synthesis API](https://platform.stepfun.com/docs/zh/api-reference/audio/create-audio.md)
[^223]: [StepFun streaming speech synthesis](https://platform.stepfun.com/docs/zh/api-reference/audio/ws-audio.md)
[^224]: [Zhipu quickstart](https://docs.bigmodel.cn/cn/guide/start/quick-start.md)
[^225]: [SiliconFlow quickstart](https://api-docs.siliconflow.cn/docs/userguide/quickstart)
[^226]: [SiliconFlow Create a Speech API](https://api-docs.siliconflow.cn/docs/api/audio-speech-post)
[^227]: [Xiaomi MiMo speech synthesis API (OpenAI-compatible)](https://mimo.mi.com/static/docs/api/audio/tts.md)
[^228]: [Text-to-speech API reference (REST) - Speech service (docs.azure.cn)](https://docs.azure.cn/zh-cn/ai-services/speech-service/rest-text-to-speech)
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
[^244]: [Old-console authentication reference - Doubao Speech - Volcengine](https://docs.volcengine.com/docs/6561/2534847?lang=zh)
[^245]: [SiliconFlow rate limits](https://api-docs.siliconflow.cn/docs/userguide/faqs/rate-limit-and-upgradation)
[^246]: [SiliconFlow finance FAQ](https://api-docs.siliconflow.cn/docs/userguide/faqs/misc_finance)
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
