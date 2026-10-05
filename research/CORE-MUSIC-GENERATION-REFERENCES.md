# How AI Music Generation Works — Core References

A curated starting bibliography for a book about music generation, with particular attention to controllable representations and the path between audio, performance, and written scores.

**50 references: 48 papers and 2 official project write-ups.** Checkboxes are for your reading progress; **★** marks the 15-paper first pass. Years refer to the first preprint or project release, so they can differ from conference publication years. Primary links checked on 2026-10-05.

## Suggested first pass

1. **Representations:** VQ-VAE → EnCodec → MERT.
2. **Generation:** DDPM → Latent Diffusion → Flow Matching → Jukebox → MusicGen.
3. **Song generation and control:** ACE-Step → ACE-Step 1.5 → JASCO.
4. **Your score ↔ audio direction:** REMI → MT3 → PM2S → DDSP.

Read the other foundations as needed. Then compare YuE, SongGen, and DiffRhythm to understand competing ways of generating vocals and accompaniment.

## 1. Generative modeling foundations

- [ ] **P01 · VAE** — Kingma & Welling (2013). [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114). Learn the ELBO, reparameterization, reconstruction–regularization tradeoff, and what a continuous latent variable model actually learns.

- [ ] **P02 · Transformer** — Vaswani et al. (2017). [Attention Is All You Need](https://arxiv.org/abs/1706.03762). The attention architecture underlying symbolic music models, audio token language models, and diffusion transformers.

- [ ] **P03 · WaveNet** — van den Oord et al. (2016). [WaveNet: A Generative Model for Raw Audio](https://arxiv.org/abs/1609.03499). Understand sample-level autoregression and why later systems move generation into compressed representations.

- [ ] **★ P04 · DDPM** — Ho, Jain & Abbeel (2020). [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239). The forward noise process, denoising objective, and iterative sampling foundation for diffusion-based audio generation.

- [ ] **P05 · Classifier-free guidance** — Ho & Salimans (2022). [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598). How conditional and unconditional predictions steer sampling; useful for understanding prompt adherence and guidance tradeoffs.

- [ ] **★ P06 · Latent Diffusion** — Rombach et al. (2021). [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752). Image-domain foundation for separating an autoencoder from a generator operating in its compressed latent space.

- [ ] **★ P07 · Flow Matching** — Lipman et al. (2022). [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747). Learn vector-field training, probability paths, and ODE sampling before studying modern flow-based music generators.

- [ ] **P08 · DiT** — Peebles & Xie (2022). [Scalable Diffusion Models with Transformers](https://arxiv.org/abs/2212.09748). The image-domain diffusion transformer foundation; focus on latent tokens, timestep conditioning, and adaptive normalization.

## 2. Audio compression, discrete tokens, and continuous latents

- [ ] **★ P09 · VQ-VAE** — van den Oord, Vinyals & Kavukcuoglu (2017). [Neural Discrete Representation Learning](https://arxiv.org/abs/1711.00937). The essential starting point for learned codebooks, commitment loss, discrete bottlenecks, and separately trained generative priors.

- [ ] **P10 · VQ-VAE-2** — Razavi, van den Oord & Vinyals (2019). [Generating Diverse High-Fidelity Images with VQ-VAE-2](https://arxiv.org/abs/1906.00446). Hierarchical discrete representations and priors; useful background for Jukebox's multiscale design.

- [ ] **P11 · SoundStream** — Zeghidour et al. (2021). [SoundStream: An End-to-End Neural Audio Codec](https://arxiv.org/abs/2107.03312). Residual vector quantization, adversarial reconstruction, and variable-rate neural audio compression.

- [ ] **★ P12 · EnCodec** — Défossez et al. (2022). [High Fidelity Neural Audio Compression](https://arxiv.org/abs/2210.13438). Understand audio codebooks, bitrate, reconstruction losses, and the codec interface used by MusicGen.

- [ ] **P13 · DAC / RVQGAN** — Kumar et al. (2023). [High-Fidelity Audio Compression with Improved RVQGAN](https://arxiv.org/abs/2306.06546). A strong codec reference for quantization design, codebook utilization, and perceptual reconstruction quality.

- [ ] **P14 · FSQ** — Mentzer et al. (2023). [Finite Scalar Quantization: VQ-VAE Made Simple](https://arxiv.org/abs/2309.15505). Discretize bounded scalar dimensions instead of learning a vector codebook; relevant to understanding alternative token bottlenecks, including ACE-Step 1.5.

- [ ] **P15 · DC-AE / DCAE** — Chen et al. (2024). [Deep Compression Autoencoder for Efficient High-Resolution Diffusion Models](https://arxiv.org/abs/2410.10733). An image-domain compression paper that informs the adapted DCAE in original ACE-Step. Study compression versus reconstruction; check audio implementations separately.

- [ ] **P16 · X-Codec** — Ye et al. (2024). [Codec Does Matter: Exploring the Semantic Shortcoming of Codec for Audio Language Model](https://arxiv.org/abs/2408.17175). Why acoustic reconstruction alone can produce weak tokens for language modeling, and how semantic features improve the codec; relevant to YuE.

## 3. Understanding and aligning audio representations

- [ ] **P17 · HuBERT** — Hsu et al. (2021). [HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units](https://arxiv.org/abs/2106.07447). Cluster-derived targets and masked prediction underpin a major family of speech representation models.

- [ ] **P18 · mHuBERT** — Boito et al. (2024). [mHuBERT-147: A Compact Multilingual HuBERT Model](https://arxiv.org/abs/2406.06371). A concrete multilingual speech-model reference. Useful for vocal-content features; distinguish the mHuBERT family from the exact checkpoint used by a music system.

- [ ] **★ P19 · MERT** — Li et al. (2023). [MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training](https://arxiv.org/abs/2306.00107). Music-specific self-supervised representations using acoustic and musical teacher targets; important for probing what musical information a representation preserves.

- [ ] **P20 · LAION-CLAP** — Wu et al. (2022). [Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation](https://arxiv.org/abs/2211.06687). Audio–text contrastive alignment used for retrieval, conditioning, and semantic evaluation; a global similarity embedding does not encode an exact score.

- [ ] **P21 · REPA** — Yu et al. (2024). [Representation Alignment for Generation: Training Diffusion Transformers Is Easier Than You Think](https://arxiv.org/abs/2410.06940). Align generator features with pretrained representations. Read this image-domain foundation alongside ACE-Step's adaptation to audio teachers.

## 4. From audio modeling to music and complete songs

- [ ] **★ P22 · Jukebox** — Dhariwal et al. (2020). [Jukebox: A Generative Model for Music](https://arxiv.org/abs/2005.00341). Hierarchical VQ-VAE compression plus autoregressive priors for music with singing; a landmark in lyrics-conditioned audio generation. [Official code](https://github.com/openai/jukebox).

- [ ] **P23 · AudioLM** — Borsos et al. (2022). [AudioLM: a Language Modeling Approach to Audio Generation](https://arxiv.org/abs/2209.03143). Separates semantic and acoustic token modeling; essential background for hierarchical audio language models.

- [ ] **P24 · MusicLM** — Agostinelli et al. (2023). [MusicLM: Generating Music From Text](https://arxiv.org/abs/2301.11325). Hierarchical text-conditioned music generation, including melody conditioning; compare semantic planning with acoustic detail generation.

- [ ] **★ P25 · MusicGen** — Copet et al. (2023). [Simple and Controllable Music Generation](https://arxiv.org/abs/2306.05284). A single-stage autoregressive model over EnCodec tokens with codebook delay patterns and melody conditioning.

- [ ] **P26 · AudioLDM** — Liu et al. (2023). [AudioLDM: Text-to-Audio Generation with Latent Diffusion Models](https://arxiv.org/abs/2301.12503). Connects contrastive audio–text embeddings, a latent audio autoencoder, and diffusion; foundational beyond music-specific models.

- [ ] **P27 · Riffusion — original prototype** — Forsgren & Martiros (2022). [Official repository](https://github.com/riffusion/riffusion-hobby) · [Original model card](https://huggingface.co/riffusion/riffusion-model-v1). **Project/code reference, not a formal paper:** Stable Diffusion adapted to spectrogram images, followed by audio reconstruction. Useful for understanding representation choices and their limitations.

- [ ] **P28 · Stable Audio — timing conditioning** — Evans et al. (2024). [Fast Timing-Conditioned Latent Audio Diffusion](https://arxiv.org/abs/2402.04825). Duration and timing conditioning for latent audio diffusion; the original Stable Audio architecture reference.

- [ ] **P29 · Stable Audio 2.0 — long-form generation** — Evans et al. (2024). [Long-form music generation with latent diffusion](https://arxiv.org/abs/2404.10301). A fully convolutional audio autoencoder and diffusion transformer for longer, high-fidelity music generation.

- [ ] **P30 · Stable Audio Open** — Evans et al. (2024). [Stable Audio Open](https://arxiv.org/abs/2407.14358). An openly released text-to-audio system; read for the relationship between training data, autoencoding, text conditioning, and diffusion.

- [ ] **P31 · YuE** — Yuan et al. (2025). [YuE: Scaling Open Foundation Models for Long-Form Music Generation](https://arxiv.org/abs/2503.08638). Lyrics-to-song generation with track-decoupled token prediction and progressive conditioning; compare vocal/accompaniment coordination with latent diffusion. [Official code](https://github.com/multimodal-art-projection/YuE).

- [ ] **P32 · SongGen** — Liu et al. (2025). [SongGen: A Single Stage Auto-regressive Transformer for Text-to-Song Generation](https://arxiv.org/abs/2502.13128). Mixed and dual-track token generation from descriptions and lyrics, with optional reference voice conditioning. [Official code](https://github.com/LiuZH-19/SongGen).

- [ ] **P33 · DiffRhythm** — Ning et al. (2025). [DiffRhythm: Blazingly Fast and Embarrassingly Simple End-to-End Full-Length Song Generation with Latent Diffusion](https://arxiv.org/abs/2503.01183). Joint vocal/accompaniment generation through latent flow matching with lyrics and style conditioning; inspect how lyric timing enters the model. [Official code](https://github.com/ASLP-lab/DiffRhythm).

- [ ] **★ P34 · ACE-Step — original model** — Gong et al. (2025). [ACE-Step: A Step Towards Music Generation Foundation Model](https://arxiv.org/abs/2506.00045). Connect DCAE compression, diffusion/flow generation, lyric conditioning, and representation alignment with music and speech teachers. [Official code](https://github.com/ace-step/ACE-Step).

- [ ] **★ P35 · ACE-Step 1.5** — Gong et al. (2026). [ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation](https://arxiv.org/abs/2602.00744). Study the language-model planning stage, semantic tokens, and acoustic diffusion renderer. Compare the paper with the selected checkpoint and inference path. [Official code](https://github.com/ace-step/ACE-Step-1.5).

## 5. Adaptation and precise musical control

- [ ] **P36 · LoRA** — Hu et al. (2021). [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). Low-rank weight updates for economical adaptation; useful background for music-model fine-tuning, separate from per-note conditioning.

- [ ] **P37 · ControlNet** — Zhang, Rao & Agrawala (2023). [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543). The image-domain foundation for adding structured conditions to pretrained diffusion models.

- [ ] **P38 · Music ControlNet** — Wu et al. (2023). [Music ControlNet: Multiple Time-varying Controls for Music Generation](https://arxiv.org/abs/2311.07069). Melody, dynamics, and rhythm controls over time, including partially specified controls; directly relevant to your melody-following problem.

- [ ] **★ P39 · JASCO** — Tal et al. (2024). [Joint Audio and Symbolic Conditioning for Temporally Controlled Text-to-Music Generation](https://arxiv.org/abs/2406.10970). A bridge between symbolic conditions and audio generation, combining text with temporally aligned chord, melody, and drum controls.

## 6. Symbolic composition, transcription, and score ↔ audio bridges

- [ ] **P40 · MusicVAE** — Roberts et al. (2018). [A Hierarchical Latent Vector Model for Learning Long-Term Structure in Music](https://arxiv.org/abs/1803.05428). A foundational symbolic latent-space model for interpolation and long-range musical structure.

- [ ] **P41 · Music Transformer** — Huang et al. (2018). [Music Transformer](https://arxiv.org/abs/1809.04281). Relative attention for expressive symbolic music with longer-range repetition and structure.

- [ ] **★ P42 · REMI / Pop Music Transformer** — Huang & Yang (2020). [Pop Music Transformer: Beat-based Modeling and Generation of Expressive Pop Piano Compositions](https://arxiv.org/abs/2002.00212). Beat- and bar-aware event representations; a key reference for designing a musically meaningful intermediate representation.

- [ ] **P43 · MuseNet** — Payne (2019). [Official MuseNet write-up](https://openai.com/index/musenet/). **Project write-up, not a formal paper:** multi-instrument MIDI token prediction with style and instrumentation conditioning. Study its event encoding alongside REMI.

- [ ] **P44 · Anticipatory Music Transformer** — Thickstun et al. (2023). [Anticipatory Music Transformer](https://arxiv.org/abs/2306.08620). Asynchronous symbolic controls, infilling, and accompaniment generation; useful for preserving specified events while generating surrounding music.

- [ ] **P45 · Onsets and Frames** — Hawthorne et al. (2017). [Onsets and Frames: Dual-Objective Piano Transcription](https://arxiv.org/abs/1710.11153). Audio-to-note estimation with explicit onset and frame objectives; understand transcription before attempting audio-to-score systems.

- [ ] **★ P46 · MT3** — Gardner et al. (2021). [MT3: Multi-Task Multitrack Music Transcription](https://arxiv.org/abs/2111.03017). Sequence-to-sequence transcription from audio into instrument-labeled note events across multiple datasets.

- [ ] **★ P47 · PM2S** — Liu, Kong, Morfi & Benetos (2022). [Performance MIDI-to-Score Conversion by Neural Beat Tracking](https://archives.ismir.net/ismir2022/paper/000047.pdf). The next bridge after transcription: rhythmic quantization and score-related predictions from performed note events. [Official code](https://github.com/cheriell/PM2S).

- [ ] **★ P48 · DDSP** — Engel et al. (2020). [DDSP: Differentiable Digital Signal Processing](https://arxiv.org/abs/2001.04643). Differentiable synthesis with explicit pitch, loudness, and signal-processing structure; a foundational example of interpretable controls combined with learned components.

- [ ] **P49 · CLaMP 3** — Wu et al. (2025). [CLaMP 3: Universal Music Information Retrieval Across Unaligned Modalities and Unseen Languages](https://arxiv.org/abs/2502.10362). Align sheet music, performance MIDI, audio, and text for retrieval. Relevant to a shared musical interface; contrastive alignment alone does not provide score↔audio conversion.

## 7. Evaluation

- [ ] **P50 · Fréchet Audio Distance** — Kilgour et al. (2018). [Fréchet Audio Distance: A Metric for Evaluating Music Enhancement Algorithms](https://arxiv.org/abs/1812.08466). The origin of a widely used distributional audio metric. Pair it with listening tests and separate checks of notes, timing, lyrics, and control adherence.

## How to curate this into a book

For each reference, keep a short note: **representation → training objective → conditioning → inference → evidence → unresolved question**. Record which information is explicit, which is compressed into learned features, and which can actually be edited.

For your compiler-oriented research, a useful working decomposition is:

```text
score / notation → structured musical events → expressive performance → audio renderer
audio → estimated performance events → rhythm / meter / voice interpretation → score
```

This is a research organizing framework, not a claim that the cited systems implement a complete reversible pipeline. Transcription, score interpretation, and rendering have different objectives; acoustic codec tokens, semantic embeddings, and symbolic note events also carry different information.

Read ACE-Step 1.0 and 1.5 as separate architectures. Likewise, mHuBERT is a speech representation family, MERT is music-oriented, and DC-AE, DiT, LoRA, and ControlNet originated outside music. Those distinctions help trace which ideas were transferred and what the music-specific adaptations actually contribute.
