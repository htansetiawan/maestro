# 09 — Anatomy verification: architecture facts for the bidirectional music ↔ sheet-music report

Verified 2026-10-04 against primary sources (arXiv abstract/HTML or ar5iv, official blogs, GitHub READMEs, HF model cards). ~49 lookups. Anything not read directly from a primary source is marked **UNVERIFIED**. Format per item: Source URL · Confirmed facts · Unverified/inferred · Relevance.

---

## A. Closed commercial systems (public statements only)

### Suno (v3 → v6; Bark lineage)
- **Source URLs**: https://github.com/suno-ai/bark · https://suno.com/release-notes · https://suno.com/blog/suno-studio · https://www.latent.space/p/suno (Shulman interview, 2024-03-14) · MBW on v4.5+ (2025-07-18)
- **Confirmed facts**
  - **Bark** (Suno AI, released 2023-04-20, MIT licence): README states it "follows a GPT style architecture similar to AudioLM and Vall-E and a quantized Audio representation from EnCodec"; "fully generative text-to-audio model", no phoneme stage. README does not spell out the three stages on the landing page, but the repo's model code exposes `text` (semantic), `coarse` and `fine` models over EnCodec codes — i.e. semantic → coarse (first EnCodec codebooks) → fine (remaining codebooks). (Stage names confirmed from repo structure; the exact codebook split 2 coarse / 6 fine is **inferred from code, not README prose**.)
  - **Shulman interview (Latent Space, 2024-03-14)**: Suno "prefer transformers"; "you have some abstract notion of a token and you train a model to predict the probability over all of the next token. So it's a language model"; discrete audio tokenisation "similar to how it's done in the open source stuff"; explicitly declines to give model size (175B "would be technologically difficult" because of tokens/sec latency); Bark code borrowed from nanoGPT.
  - **Release-notes feature timeline**: audio uploads/inputs (2024-06-12 Pro/Premier, 2024-06-28 all); Stems (2024-07-23); **Covers** (2024-09-12); Crop (2024-09-24); **Replace Section** (2024-10-10); Personas (2024-10-31); **Extend** (listed 2025-02-06 iOS; present on web since v3 era); **Add Vocals / Add Instrumentals / Inspire** shipped with v4.5+ on 2025-07-18 (MBW quoting Suno); **Suno Studio** launched 2025-09-25 ("generative audio workstation", Premier only; stem generation, multitrack timeline, "Export stems as both audio and MIDI files"); Studio 2.0 (2026-08-13) with "Import, record and edit MIDI directly on the timeline", wavetable synth, sidechain/convolution reverb; "Advanced Split" stem separation (2026-06-11); Voices (2026-03-26). Model versions: v3 alpha 2024-02-22 → v3.5 2024-05-24 → v4 2024-11-19 → v4.5 2025-05-01 → v5 2025-09-23 → v5.5 2026-03-26 → v6 / v6-wild / v6-mini 2026-09-09.
- **Unverified / NOT public**: model size, parameter count, training-data composition, tokenizer/codec used by the production models (whether still EnCodec-based), whether v5/v6 are still pure autoregressive LMs or hybrid LM+diffusion. Release notes contain **no** architecture statements. Everything about the current model beyond "transformer LM over discrete audio tokens" (2024 statement) is inference.
- **Relevance**: the only public architectural anchor for Suno is Bark-style hierarchical token LM (2023) + the 2024 "it's a language model" statement; all audio-input features (Covers, Add Vocals/Instrumentals, Replace Section, Studio stems/MIDI) are confirmed and dated.

### Google Lyria / Lyria RealTime / Magenta RealTime 1 & 2
- **Source URLs**: https://arxiv.org/abs/2508.04651 (+ HTML) "Live Music Models" · https://magenta.withgoogle.com/magenta-realtime (2025-06-20) · https://huggingface.co/google/magenta-realtime-2 · https://deepmind.google/models/lyria/
- **Confirmed facts**
  - Paper: *Live Music Models*, Caillon, McWilliams, Tarakajian, Simon, Manco, Engel, … (Lyria Team, 26 authors), arXiv 2508.04651 (v1 2025-08-06, v3 2025-11-05), NeurIPS 2025 Creative AI track (per HF card). Introduces "live music models" producing "a continuous stream of music in real-time with synchronized user control"; two models: Magenta RealTime (open weights) and Lyria RealTime (API).
  - **SpectroStream**: "full-band (48 kHz) multichannel neural audio codec based on residual vector quantization", 25 Hz token frame rate, up to d_c = 64 RVQ levels with codebook size 1024; live generation uses first 16 RVQ levels (~4 kbps).
  - **MusicCoCa**: contrastive captioner with two towers (12-layer ViT audio tower, 12-layer Transformer text tower) into a shared 768-d space; style embedding quantised to 12 discrete tokens (codebook 1024).
  - **Magenta RT v1 transformer**: encoder-decoder — "encoder receives the concatenation of the acoustic history and style tokens"; decoder is two connected Transformer modules (temporal + depth, RQ-Transformer-style). Sizes in paper: **Base 220M, Large 770M**. Blog rounds this to "800 million parameter autoregressive transformer". Chunk C = 2 s; context H = 5 previous chunks = 10 s of history; RTF 1.8 on H100, 1.6 on free Colab TPU. Training: ~190,000 h "primarily instrumental stock music", 1.86M steps on TPU-v6e. Code Apache-2.0; weights "permissive" (CC-BY 4.0 per MRT2 card).
  - **Magenta RealTime 2** (HF card): components SpectroStream (stereo 48 kHz, 25 Hz) + MusicCoCa (768-d) + **decoder-only** Transformer LLM "with frame-wise autoregression and windowed attention"; **Base 2.4B** (20 layers, 25-frame window) and **Small 230M** (12 layers, 41-frame window); ~20 s effective receptive field; adds MIDI input conditioning; code Apache-2.0, weights CC-BY 4.0; "forthcoming dedicated paper", cite Live Music Models meanwhile.
  - Lyria product page lists Lyria 3.5 (tracks up to 3 min), Lyria, Lyria RealTime, Magenta RealTime; all outputs SynthID-watermarked. **No architecture statements** for Lyria 2 / 3 / 3.5.
- **Unverified / inferred**: that Lyria RealTime shares the Magenta RT architecture at larger scale (the paper presents both together, but Lyria RT parameter count and data are not disclosed); Lyria 2/3 architecture entirely undisclosed. Note the v1 ↔ v2 shift encoder-decoder → decoder-only is stated by the v2 card, not by a paper.
- **Relevance**: the cleanest public example of a codec-token LM with chunked streaming + a joint text/audio embedding for conditioning; MRT2's MIDI input is a symbolic-conditioning precedent.

---

## B. Open "Suno-like" song models

### YuE
- **Source URLs**: https://arxiv.org/abs/2503.08638 (+ HTML) · https://github.com/multimodal-art-projection/YuE
- **Confirmed facts**: *YuE: Scaling Open Foundation Models for Long-Form Music Generation*, Yuan, Lin, Guo, Zhang, Pan, … (M-A-P), arXiv 2503.08638 (v1 2025-03-11, v2 2025-09-15). Two-stage: **Stage-1** LLaMA2-based LM (released weights 7B, e.g. `YuE-s1-7B-anneal-en-cot`) over text tokens (LLaMA 32K BPE) + **semantic tokens = X-Codec codebook-0**; **Stage-2** 1B LM (8K context) predicting residual acoustic codebooks 1–7 from codebook-0, trained on 6 s single-track segments. **Track-decoupled next-token prediction** ("dual-token"): interleaves vocal and accompaniment tokens (v1, a1, v2, a2, …). **Structural progressive conditioning** (the "CoT" mode): songs segmented into ~14 labelled sections; segment label + lyrics + audio interleaved in ≤30 s contexts. ICL mode: 20–40 s reference audio prepended only during annealing (~10B tokens). Codec: **X-Codec**, 16 kHz (upsampled to 44.1 kHz after), 50 Hz, 12 RVQ layers (8 used) × 1024, HuBERT-semantic fusion; codec trained on 200k h. Licence: README states weights "released under the Apache License, Version 2.0".
- **Unverified / inferred**: exact total training-token count ("trillions" per abstract, no exact figure extracted); whether Stage-1 is exactly 7.0B vs rounded.
- **Relevance**: the open reference for "lyrics → full song" via a semantic/acoustic split; its codebook-0-as-semantic-layer is the natural place to insert a symbolic (score) bottleneck.

### ACE-Step 1.0 and 1.5
- **Source URLs**: https://arxiv.org/abs/2506.00045 · https://github.com/ace-step/ACE-Step · https://arxiv.org/abs/2602.00744 · https://github.com/ace-step/ACE-Step-1.5
- **Confirmed facts**
  - **1.0**: *ACE-Step: A Step Towards Music Generation Foundation Model*, Gong, Zhao, Wang, Xu, Guo, … (ACE Studio + StepFun), arXiv 2506.00045 (2025-05-28). "Integrating diffusion-based generation with Sana's Deep Compression AutoEncoder (DCAE) and a lightweight linear transformer"; **REPA** semantic alignment "leverages MERT and m-hubert to align semantic representations" during training; flow-matching; 4 min of music in ~20 s on A100, "15× faster than LLM-based baselines". Released weights `ACE-Step-v1-3.5B` (**3.5B**). Features: variations, **repainting**, **lyric editing** (flow-edit), extend, remix, Lyric2Vocal / RapMachine LoRAs, Singing2Accompaniment, ControlNet-LoRA stems. **Licence: Apache-2.0** (README), **not MIT**.
  - **1.5**: *ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation*, Gong, Song, Zhao, Wang, Xu, …, arXiv 2602.00744 (2026-01-31, rev 2026-02-06). **LM planner + DiT**: LM "transforms simple user queries into comprehensive song blueprints" with CoT; LM sizes **0.6B / 1.7B / 4B** (`acestep-5Hz-lm-*`); DiT **2B** (base/SFT/turbo) and **XL 4B**; turbo = 8 steps vs 50; VAE latent; 10 s–10 min outputs; <2 s/song on A100; "intrinsic reinforcement learning". Features: **Cover Generation**, **Repaint & Edit**, Vocal2BGM, track separation / multi-track, audio understanding (BPM, key, time signature, caption), LRC timestamp generation, 50+ languages. **Licence: MIT** (README).
- **Unverified / inferred**: whether the 1.0 "linear transformer" is formally a DiT (paper calls it a lightweight linear transformer in a diffusion framework; "DiT" is the 1.5 paper's term); DCAE latent frame rate; exact 1.5 VAE specs.
- **Relevance**: the open latent-diffusion counterpart to YuE; 1.5's LM planner is the closest open analogue to a "plan (symbolic/structure) → render (audio)" split.

### DiffRhythm
- **Source URLs**: https://arxiv.org/abs/2503.01183 (+ HTML) · https://github.com/ASLP-lab/DiffRhythm · https://huggingface.co/ASLP-lab/DiffRhythm-full
- **Confirmed facts**: *DiffRhythm: Blazingly Fast and Embarrassingly Simple End-to-End Full-Length Song Generation with Latent Diffusion*, Ning, Chen, Jiang, Hao, Ma, … (ASLP, NWPU), arXiv 2503.01183 (2025-03-03). VAE: 44.1 kHz stereo, fully-convolutional backbone "adapted from Stable Audio 2", multi-resolution STFT + adversarial loss, trained lossy(MP3)→lossless; DiT = "stacks of LLaMA decoder layers", conditional flow matching; conditioning = style prompt (via LSTM), timestep, phoneme tokens with **sentence-level lyrics alignment** (G2P + timestamps). Up to **4 m 45 s (285 s)** in ~10 s. Variants: base (1 m 35 s), full (4 m 45 s), v1.2 base/full, separate VAE. **Licence: Apache-2.0** (README + HF).
- **Unverified**: **parameter count** — not stated in abstract, HTML extract, README or HF card (the "1.1B" figure circulating in secondary sources is UNVERIFIED). Venue (ACL 2025?) UNVERIFIED.
- **Relevance**: simplest full-song latent-diffusion baseline; shows lyrics-timing alignment can be done at sentence level without a semantic-token stage.

### MusicGen
- **Source URLs**: https://arxiv.org/abs/2306.05284 (+ HTML)
- **Confirmed facts**: *Simple and Controllable Music Generation*, Copet, Kreuk, Gat, Remez, Kant, … (Meta), NeurIPS 2023. Single-stage transformer LM over EnCodec tokens: 32 kHz, 4 RVQ codebooks × 2048, 50 Hz (stride 640) → 30 s = 1,500 AR steps. Codebook interleaving patterns compared: parallel, flattening, **delay**, VALL-E-style partial; flattening scores best but is costliest; delay is the deployed trade-off. Sizes **300M / 1.5B / 3.3B** ("subjective quality stop improving at 1.5B"). Text via T5; **melody conditioning via chromagram** quantised to the dominant time-frequency bin per step (unsupervised). Training 20k h licensed (10k internal + ShutterStock + Pond5).
- **Unverified**: none material.
- **Relevance**: canonical single-stage codec-LM; chromagram melody conditioning is the weakest form of "symbolic" control and the baseline JASCO/Coco-Mulla improve on.

---

## C. The lenses — foundations

### Jukebox
- **Source URLs**: https://arxiv.org/abs/2005.00341 · https://openai.com/index/jukebox/
- **Confirmed facts**: *Jukebox: A Generative Model for Music*, Dhariwal, Jun, Payne, Kim, Radford, Sutskever (OpenAI, 2020). Multi-scale VQ-VAE with three levels at **8×, 32×, 128×** compression (= hop 8/32/128), **codebook 2048** per level, 44.1 kHz; autoregressive **sparse (factorised-attention) transformers**; **top-level prior 5B params, 72 layers**, context 8192 codes ≈ 24 s; lyrics conditioning via encoder-decoder attention on unaligned lyrics (alignment learnt); 1.2M songs (600k English) with LyricWiki metadata; ~9 h to render 1 min of audio.
- **Unverified**: none material.
- **Relevance**: origin of the "hierarchical discrete codes + LM prior" recipe later refined by Bark/MusicLM/YuE.

### SoundStream and EnCodec
- **Source URLs**: https://arxiv.org/abs/2107.03312 (+ ar5iv) · https://arxiv.org/abs/2210.13438 (+ ar5iv)
- **Confirmed facts**
  - **SoundStream**: Zeghidour, Luebs, Omran, Skoglund, Tagliasacchi (Google), arXiv 2107.03312 (2021-07). Fully-convolutional encoder/decoder + **residual vector quantizer**; 24 kHz, total stride 320 → **75 Hz**; codebook 1024 (10 bits) per quantizer; e.g. N_q = 8 at 6 kbps; **3–18 kbps** from one model via **quantizer dropout** (n_q sampled uniformly in [1, N_q] per example). Published in IEEE/ACM TASLP 30 (2022) — journal venue is **UNVERIFIED from the fetched pages** (arXiv page did not state it).
  - **EnCodec**: *High Fidelity Neural Audio Compression*, Défossez, Copet, Synnaeve, Adi (Meta), arXiv 2210.13438 (2022-10-24). Streaming encoder-decoder + RVQ; **24 kHz mono model at 75 Hz (stride 320)**: 1.5 kbps = 2 codebooks, 3 = 4, 6 = 8, 12 = 16, 24 kbps = 32, each 1024 entries (10 bits); **48 kHz stereo model at 150 Hz**, 3–24 kbps, up to 16 codebooks; optional 5-layer Transformer LM for entropy coding (~40% further compression); multi-scale STFT discriminator; loss balancer. TMLR 2023 venue **UNVERIFIED from fetched pages**.
- **Relevance**: the RVQ token streams every codec-LM in this report consumes; frame rate × codebooks defines the sequence length a symbolic layer must align to.

### ViT · AST · MERT · MuQ (universal features)
- **Source URLs**: https://arxiv.org/abs/2010.11929 (+ ar5iv) · https://arxiv.org/abs/2104.01778 (+ ar5iv) · https://arxiv.org/abs/2306.00107 · https://arxiv.org/abs/2501.01108
- **Confirmed facts**
  - **ViT**: *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*, Dosovitskiy, Beyer, Kolesnikov, Weissenborn, Zhai, … (Google), ICLR 2021. Fixed **16×16 patches**, flattened + linear projection; **learnable [class] token** prepended (BERT-style); learnable 1D position embeddings (2D-aware gave no gain); ViT-B/L/H = 86M/307M/632M; pre-training ImageNet-21k (14M) and JFT-300M (303M).
  - **AST**: *AST: Audio Spectrogram Transformer*, Gong, Chung, Glass (MIT), Interspeech 2021. Input 128-bin log-Mel fbank (25 ms window, 10 ms hop); **16×16 patches with overlap 6 (stride 10) in time and frequency**; linear projection to 768; [CLS] token; 12 layers/12 heads/768 (ViT-B); **ImageNet-pretrained DeiT init** with RGB patch-embedding channels averaged and positional embeddings cut/bilinearly interpolated; AudioSet mAP 0.485, ESC-50 95.6%, Speech Commands V2 98.1%.
  - **MERT**: *MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training*, Li, Yuan, Zhang, Ma, Chen, … , ICLR 2024. Masked-LM pre-training with an **acoustic teacher (RVQ-VAE, EnCodec)** and a **musical teacher (CQT)** as pseudo-labels; **95M and 330M**; 14 MIR tasks. (160k h training figure not in abstract — UNVERIFIED from fetched page.)
  - **MuQ**: *MuQ: Self-Supervised Music Representation Learning with Mel Residual Vector Quantization*, Zhu, Zhou, Chen, Yu, Ma, … (Tencent/SJTU), arXiv 2501.01108 (2025-01). Predicts tokens from **Mel-RVQ** (residual linear projection on Mel); strong with 0.9k h, better at 160k+ h with iterative training; **MuQ-MuLan** contrastive music-text model, SOTA zero-shot tagging on MagnaTagATune. Parameter count (~300M) and MARBLE results **UNVERIFIED** from abstract; licence of weights UNVERIFIED (abstract page shows CC BY-NC-SA 4.0 but that may be the paper licence).
- **Relevance**: ViT/AST justify "spectrogram patches as tokens"; MERT (used by ACE-Step REPA and CLaMP 3) and MuQ (used by the 2026 audio-to-score system) are the de-facto frozen audio features in the audio→score pipeline.

### VQ-VAE
- **Source URLs**: https://arxiv.org/abs/1711.00937 (+ ar5iv)
- **Confirmed facts**: *Neural Discrete Representation Learning*, van den Oord, Vinyals, Kavukcuoglu (DeepMind), NIPS 2017. Codebook of K embeddings; **nearest-neighbour lookup** q(z=k|x)=1 for k = argmin_j ||z_e(x) − e_j||; **straight-through** gradient (copy decoder-input gradient to encoder output); loss = reconstruction + ||sg[z_e] − e||² (codebook) + **β||z_e − sg[e]||² (commitment, β = 0.25)**; learned autoregressive prior (PixelCNN images / WaveNet audio); avoids posterior collapse; speech experiments discover phoneme-like units.
- **Relevance**: the primitive every codec and Genie's tokenizer/LAM build on.

### Genie, Genie 2, Genie 3
- **Source URLs**: https://arxiv.org/abs/2402.15391 (+ HTML) · https://proceedings.mlr.press/v235/bruce24a.html · https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/ · https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/
- **Confirmed facts**
  - **Genie**: *Genie: Generative Interactive Environments*, Bruce, Dennis, Edwards, Parker-Holder, Shi, … (Google DeepMind), ICML 2024, PMLR 235:4603–4623, arXiv 2402.15391 (2024-02-23). Three components: (1) **video tokenizer — ST-ViViT** (spatiotemporal), VQ-VAE, 200M params, patch size 4, codebook 1024 × 32-d; (2) **latent action model (LAM)** — unsupervised, VQ codebook of **8 latent actions** (32-d), operates on pixels; (3) **dynamics model — MaskGIT**, 10.1B; total **10.7B** (abstract: "11B"). Data: 30,000 h curated 2D-platformer gameplay filtered from 55M 16-s clips (abstract: "unlabelled Internet videos"; the "200k hours" figure is the pre-filter pool in the paper's data section — **not confirmed in fetched text**); 160×90 @ 10 FPS, 16-frame sequences; 25 MaskGIT steps per frame; 942B tokens. Prompted from text, images, sketches; "foundation world model".
  - **Genie 2** (blog, 2024-12-04): "autoregressive latent diffusion model"; autoencoder → latent frames → "large transformer dynamics model, trained with a causal mask similar to that used by large language models"; sampled autoregressively frame-by-frame given actions; classifier-free guidance for action controllability; consistent worlds "up to a minute, with the majority of examples shown lasting 10–20 s"; keyboard/mouse control. No sizes.
  - **Genie 3** (blog, 2025-08-05): real-time **24 fps, 720p**, consistency for "several minutes", "promptable world events"; consistency described as an emergent capability; frame-by-frame generation; limited research preview. **No architecture disclosed.**
- **Unverified**: ICML oral/best-paper status (not on PMLR page); exact 200k-hour pool figure; Genie 2/3 parameter counts.
- **Relevance**: the LAM (an unsupervised discrete "action" bottleneck between frames) is the structural analogue of a learned symbolic bottleneck between audio and score — i.e. the Genie lens for SMN-VAE.

---

## D. Symbolic latent / cross-modal alignment — SMN-VAE prior art

### MusicVAE
- **Source URL**: https://arxiv.org/abs/1803.05428
- **Confirmed facts**: *A Hierarchical Latent Vector Model for Learning Long-Term Structure in Music*, Roberts, Engel, Raffel, Hawthorne, Eck (Google Brain/Magenta), ICML 2018. Bidirectional-LSTM encoder; **hierarchical decoder: conductor RNN emits one embedding per bar/subsequence, independent decoder RNNs decode each**; mitigates posterior collapse; **2-bar and 16-bar** models; latent interpolation and attribute vectors; **trio** model (melody, bass, drums). Code public.
- **Relevance**: the canonical symbolic-latent VAE; its conductor hierarchy is what SMN-VAE would extend to multi-staff notation.

### PianoTree VAE
- **Source URLs**: https://arxiv.org/abs/2008.07118 (+ ar5iv)
- **Confirmed facts**: *PianoTree VAE: Structured Representation Learning for Polyphonic Music*, Wang, Zhang, Zhang, Zhang, Wang, Xia (NYU Shanghai), ISMIR 2020. Tree latent: **score → simu_note (simultaneous notes) → note (pitch, duration)**; bottom-up bi-GRU encoders at each level (note emb 128, simu_note 512, score 1024); isotropic Gaussian latent **z ∈ R^512**; top-down uni-GRU decoders; duration as 5-bit binary; segment = **32 steps = 8 beats at 16th-note resolution (2 bars of 4/4)**; β-VAE; evaluated by reconstruction F1, latent visualisation, interpolation and downstream generation.
- **Unverified**: author list taken from ar5iv header — first author Ziyu Wang confirmed, full list per paper: Ziyu Wang, Yiyi Zhang, Yixiao Zhang, Junyan Jiang, Ruihan Yang, Junbo Zhao, Gus Xia. (Treat full list as **lightly verified**.)
- **Relevance**: the only widely cited VAE whose latent is explicitly *polyphonic-structure-aware*; a direct precedent for a score-structured latent.

### CLaMP → CLaMP 2 → CLaMP 3
- **Source URLs**: https://arxiv.org/abs/2304.11029 · https://github.com/sanderwood/clamp2 (arXiv 2410.13267) · https://arxiv.org/abs/2502.10362 (+ HTML) · https://github.com/sanderwood/clamp3
- **Confirmed facts**
  - **CLaMP** (Wu, Yu, Tan, Sun; ISMIR 2023): contrastive text ↔ **ABC notation**; **1.4M** music-text pairs; **bar patching** cuts sequence length to <10%; WikiMusicText (1,010 ABC lead sheets); zero-shot classification and semantic search comparable/superior to fine-tuned baselines on score-oriented datasets.
  - **CLaMP 2** (Wu, Wang, Yuan, Guo, Tan, … Sun; NAACL 2025; arXiv 2410.13267; MIT): **101 languages** (XLM-R base text tower); symbolic music as **ABC and MIDI (via MIDI Text Format, MTF)** through the **M3** patch-based multimodal symbolic encoder (patch 64, seq 512); LLM-refined multilingual descriptions; 1.5M ABC-MIDI-text triplets.
  - **CLaMP 3** (*CLaMP 3: Universal Music Information Retrieval Across Unaligned Modalities and Unseen Languages*, Wu, Guo, Yuan, Jiang, Doh, … ; **ACL 2025** per README; arXiv 2502.10362; **MIT**): one contrastive space over **sheet music (interleaved ABC, 512 bars; MusicXML converted)**, **performance signals (MIDI → MTF, 512 messages)**, **audio (frozen MERT-v1-95M, one embedding per 5-s clip averaged over all layers/time)**, and **multilingual text (XLM-R-base; 27 training languages, 100 at inference)**. All encoders 12 layers × 768. Trained on **M4-RAG (2.31M pairs, 27 languages, 194 countries)**; benchmark **WikiMT-X (1,000 sheet/audio/text triplets)**. Retrieval MRR: text→symbolic WikiMT 0.4498 (CLaMP 2: 0.3438); text→audio SDD 0.1985 (TTMR++ 0.1437); **emergent cross-modal** sheet→audio 0.0578, performance→audio 0.0397 (never trained on paired sheet–audio). Two released variants: SAAS (audio-oriented) and C2 (symbolic). Released code, weights, 1.56M audio-text pairs, WikiMT-X.
- **Unverified**: total parameter count (sum of three 12×768 towers ≈ 3 × ~100M is **inferred**, not stated).
- **Relevance**: CLaMP 3 is the direct prior art for a shared sheet-music ↔ audio embedding, and its low sheet→audio MRR quantifies the gap a generative bidirectional model must close.

### Polyffusion and Whole-Song cascaded diffusion
- **Source URLs**: https://arxiv.org/abs/2307.10304 · https://arxiv.org/abs/2405.09901
- **Confirmed facts**
  - **Polyffusion** (*Polyffusion: A Diffusion Model for Polyphonic Score Generation with Internal and External Controls*, Min, Jiang, Xia, Zhao; ISMIR 2023; arXiv 2307.10304): diffusion over **image-like piano rolls** (2D UNet); **internal control = inpainting/masking** (melody given accompaniment, accompaniment given melody, segment infill); **external control = cross-attention** on chord / texture conditions from pretrained disentangled encoders; outperforms Transformer and sampling baselines.
  - **Whole-Song** (*Whole-Song Hierarchical Generation of Symbolic Music Using Cascaded Diffusion Models*, Wang, Min, Xia; ICLR 2024): cascaded diffusion where "each level of hierarchy focuses on the semantics and context dependency at a certain music scope" — high levels: whole-song form, phrases, cadences; low levels: notes, chords, accompaniment; produces verse-chorus structure; controllable via phrase harmony, rhythm, texture.
- **Unverified**: the exact four-level naming (form → reduced lead sheet → lead sheet → accompaniment) and 8-bar Polyffusion window were not in the fetched abstracts (consistent with the papers but **UNVERIFIED here**). Polyffusion author list beyond first author taken from existing bib.
- **Relevance**: the symbolic-side generative models an audio↔score system would pair with; Whole-Song's hierarchy is the symbolic analogue of Jukebox's multi-scale codes.

---

## E. Music → sheet music pipeline

### MT3 and Onsets & Frames — output is note events, not notation
- **Source URLs**: https://arxiv.org/abs/2111.03017 (+ ar5iv) · https://arxiv.org/abs/1710.11153
- **Confirmed facts**
  - **MT3** (*MT3: Multi-Task Multitrack Music Transcription*, Gardner, Simon, Manilow, Hawthorne, Engel; ICLR 2022): T5 encoder-decoder (~60M), log-Mel input; output vocabulary = **MIDI-like events**: instrument (128), note (128), on/off (2), absolute time (205), drum (128), end-tie-section, EOS — "the output is a sequence of symbolic tokens representing the notes being played". Datasets MAESTRO, Slakh2100, Cerberus4, GuitarSet, MusicNet, URMP. **No notation elements (meter, key, voices, spelling) are produced.**
  - **Onsets and Frames** (*Onsets and Frames: Dual-Objective Piano Transcription*, Hawthorne, Elsen, Song, Roberts, Simon, …; ISMIR 2018, arXiv 2017-10): CNN + BiLSTM onset head and frame head (onset gates frame activations) + velocity head → note events (onset/offset/velocity) i.e. MIDI; >100% relative note-F1-with-offsets gain on MAPS.
- **Relevance**: confirms AMT ≠ notation; both stop at performance MIDI.

### Audio → score: what notation requires, and papers that output scores
- **Confirmed requirements** (synthesised from the score-transcription papers below, each of which models them explicitly): beat & downbeat tracking / tempo, **time signature**, **key signature**, **rhythm quantisation** of onsets/durations to note values, **voice / hand / staff separation**, enharmonic **pitch spelling**, plus notational details (clefs, ties, stem direction, ornaments). None are produced by MT3/O&F.
- **Papers**
  1. **PM2S** — *Performance MIDI-to-Score Conversion by Neural Beat Tracking*, Liu, Kong, Morfi, Benetos; ISMIR 2022 (archives.ismir.net/ismir2022/paper/000047.pdf; code https://github.com/cheriell/PM2S, MIT). Input performance MIDI; neural beat/downbeat tracking drives quantisation; also time-signature, key-signature and hand-part modules (per paper; README lists beat tracking only — sub-task list **lightly verified**). Output: quantised score-MIDI (`generated_score.mid`); MusicXML export **UNVERIFIED**. Note: the "Foscarin PM2S" attribution in the brief is **incorrect** — authors are Liu/Kong/Morfi/Benetos (QMUL/Turing).
  2. **Beyer & Dai 2024** — *End-to-end Piano Performance-MIDI to Score Conversion with Transformers*, ISMIR 2024, arXiv 2410.00210; seq2seq transformer with compound tokens (3.5× shorter sequences); predicts note values, rhythm, **staff assignment**, and notational details (trills, stem direction); MUSTER metrics; code MIDI2ScoreTransformer. Output format (MusicXML vs **kern) **UNVERIFIED** from abstract.
  3. **Zeng, He & Wang 2024** — *End-to-End Real-World Polyphonic Piano Audio-to-Score Transcription with Hierarchical Decoding*, IJCAI 2024 (dl.acm.org/doi/10.24963/ijcai.2024/862), arXiv 2405.13527. **Audio → \*\*kern score** directly; hierarchical decoder: bar-level decoder (5 bars) predicts **time and key signatures**, two note-level decoders for **upper/lower staff**; pre-train on MuseSyn + HumSyn via expressive-performance rendering, fine-tune on ASAP human recordings; WER 55.1% overall on ASAP.
  4. **Cummins et al. 2026** — *Audio-to-Score Transcription using Pre-trained Features, Data Augmentation, and the New SheetSage-A2S Dataset*, Cummins, Huang, D'Hooge, Mo, Ju, …; ACM MM '26; arXiv 2608.06165 (2026-08-06). **Audio → \*\*kern**, frozen **MuQ** features + augmentation; new **SheetSage-A2S** (61 h, 9,468 clips, 6,066 pop songs); SER 4.98% on Quartets (prior 15.3%), 20.92% on SheetSage-A2S. Code/data/model public.
  5. **Jung et al. 2025** — *Unified Cross-modal Translation of Score Images, Symbolic Music, and Performance Audio*, Jung, Kim, Lee, Cho, So, Bukey, Donahue, Jeong; arXiv 2505.12863 (bib lists IEEE/ACM TASLP; HTML says under review — venue **UNVERIFIED**). One Transformer encoder-decoder per direction (Image→Audio, Audio→Image); all modalities tokenised: RQVAE for score images (16×, 4 codebooks), DAC for audio (4 codebooks), **Linearized MusicXML** for notation, MIDI-like tokens (10 ms); tasks OMR, AMT, MIDI→audio, image→audio, audio→image, score rendering; YTSV dataset (1,341 h, 433,920 image-audio pairs). OMR SER 13.67% on BPSD (vs 24.58% baseline); MIDI→audio onset F1 39.37% with multitask. **Note: its audio→symbolic path outputs MIDI-like tokens, not MusicXML** (notation output comes from the image/OMR path).
  6. **Sheet Sage** (Donahue, Thickstun, Liang; ISMIR 2022; existing bib) — audio → **lead sheet** (melody + chords) via Jukebox features; Hooktheory dataset.
- **Relevance**: audio→MusicXML today is a two-hop pipeline (AMT → MIDI-to-score) or a direct **kern seq2seq confined to piano; no open system produces full multi-instrument MusicXML from audio.

### Sheet music → audio: symbolic conditioning
- **Source URLs**: https://arxiv.org/abs/2406.10970 (+ HTML, audiocraft JASCO.md) · https://arxiv.org/abs/2310.17162 (+ HTML) · https://arxiv.org/abs/2311.07069 (+ ar5iv) · https://arxiv.org/abs/2112.09312
- **Confirmed facts**
  - **JASCO** (*Joint Audio and Symbolic Conditioning for Temporally Controlled Text-to-Music Generation*, Tal, Ziv, Gat, Kreuk, Adi; Meta/HUJI; arXiv 2406.10970, 2024): flow matching over **continuous EnCodec latent (32 kHz, 128-d, 50 Hz)**; 330M-param transformer in paper (24 layers/16 heads/1024); released **400M and 1B** variants (chords+drums; chords+drums+melody), 10-s outputs. Controls: **chords** (Chordino labels → 16-d embedding, symbolic), **melody** (deep-salience binary 53-note matrix G2–B7, from audio), **drums** (Demucs stem → EnCodec → temporal blurring), full-mix audio; multi-source CFG. Weights licence not stated in fetched pages (**UNVERIFIED**; audiocraft code MIT).
  - **Coco-Mulla** (*Content-based Controls for Music Large Language Modeling*, Lin, Xia, Jiang, Zhang; ISMIR 2024; arXiv 2310.17162): PEFT on **MusicGen 3.3B** (frozen EnCodec/T5); joint embedding of **symbolic chords (root/bass/chroma multi-hot)**, **piano roll (projected to 12-d)** and **drum track (EnCodec codes)**; LLaMA-Adapter-style condition prefix in last L layers; <4% params tuned; 299 songs (17.12 h) with MIR pseudo-labels.
  - **Music ControlNet** (*Music ControlNet: Multiple Time-varying Controls for Music Generation*, Wu, Donahue, Watanabe, Bryan; Adobe/CMU; arXiv 2311.07069, 2023): ControlNet adapter (cloned encoder + zero convs) on a **41M-param mel-spectrogram diffusion** model + vocoder; controls **melody (chroma), dynamics (RMS), rhythm (beat/downbeat)**, Uni-ControlNet-style partial masking; ~1,800 h; "49% more faithful" melody than MusicGen with "35× fewer parameters". Existing bib lists IEEE/ACM TASLP as venue; not confirmed from fetched pages (**UNVERIFIED**). Note controls are *time-varying signals* extracted from audio, not score tokens.
  - **MIDI-DDSP** (*MIDI-DDSP: Detailed Control of Musical Performance via Hierarchical Modeling*, Wu, Manilow, Deng, Swavely, Kastner, …; ICLR 2022): hierarchy **notes → performance expression (timbre, vibrato, dynamics, articulation) → DDSP synthesis parameters**; renders MIDI to realistic monophonic instrument audio with intervention at any level. (URMP dataset not in abstract — **UNVERIFIED** here.)
- **Relevance**: "symbolic" conditioning in current audio models means chord labels, chroma/salience matrices or piano rolls — never full notation (meter, voices, dynamics markings). MIDI-DDSP is the only one that takes true note events and respects performance structure, but is monophonic.

---

## Cross-cutting corrections for the report
1. **ACE-Step 1.0 is Apache-2.0, not MIT**; ACE-Step 1.5 is MIT.
2. **Magenta RT v1 is 220M/770M in the paper** (blog says 800M); **MRT2 is 230M/2.4B** and decoder-only (v1 encoder-decoder).
3. **Genie** total is 10.7B (abstract "11B"); LAM codebook = 8; data 30k h curated (not 200k h trained).
4. **PM2S authors are Liu, Kong, Morfi, Benetos**, not Foscarin.
5. **DiffRhythm parameter count is not published** in primary sources.
6. **Jung et al. 2025** audio→symbolic path emits MIDI-like tokens, not notation; notation (Linearized MusicXML) comes from OMR.
7. CLaMP 3 emergent sheet→audio retrieval MRR is only 0.0578 — useful as a hardness number.
