# Researchers in AI music and musical interaction

A working directory for Music Kitchen, checked October 17, 2026. The industry groups below identify the work these researchers contributed to, not their current employer. The final column explains why I want to follow their work.

## AudioCraft and MusicGen contributors

| Researcher | Selected work | Relevance to Music Kitchen |
|---|---|---|
| Alexandre Défossez | Co-author of [EnCodec](https://arxiv.org/abs/2210.13438) and [MusicGen](https://arxiv.org/abs/2306.05284). | Audio compression and generation through discrete representations. |
| Jade Copet | First author of [Simple and Controllable Music Generation](https://arxiv.org/abs/2306.05284); EnCodec co-author. | Codebook interleaving, text conditioning and melody conditioning. |
| Yossi Adi | Co-author of [EnCodec](https://arxiv.org/abs/2210.13438), MusicGen and AudioGen. | The relationship between audio representations and controllability. |
| Felix Kreuk | First author of [AudioGen](https://arxiv.org/abs/2209.15352); MusicGen co-author. | Text-guided audio generation and conditional modeling. |

[AudioCraft code](https://github.com/facebookresearch/audiocraft) · [EnCodec code](https://github.com/facebookresearch/encodec)

## Jukebox and MuseNet contributors

| Researcher | Selected work | Relevance to Music Kitchen |
|---|---|---|
| Prafulla Dhariwal | First author of [Jukebox](https://arxiv.org/abs/2005.00341). | Hierarchical audio compression and autoregressive song generation. |
| Alec Radford | [Jukebox](https://arxiv.org/abs/2005.00341) co-author. | Learning representations for generative audio models. |
| Ilya Sutskever | [Jukebox](https://arxiv.org/abs/2005.00341) co-author. | Historical work on large generative models for music. |
| Christine Payne, also known as Christine McLeavey | Creator of [MuseNet](https://openai.com/index/musenet/) and Jukebox co-author; [OpenAI profile](https://forum.openai.com/public/videos/music-is-math-an-interdisciplinary-exploration-of-sound-science-and-creativity-2025). | Connects symbolic music generation with later raw-audio generation. |

## MIT faculty

| Researcher | Role and work | Relevance to Music Kitchen |
|---|---|---|
| Cheng-Zhi Anna Huang | MIT Music and EECS faculty; [Music Transformer, Coconet and human–AI songwriting](https://czhuang.github.io/). | Long-range musical structure, editable generation and co-creation. |
| Eran Egozy | [Professor of the Practice of Music](https://music.mit.edu/people/faculty/); [Interactive Music Systems](https://news.mit.edu/2016/passion-for-music-and-interactive-technology-eran-egozy-0504). | Interfaces that let people participate in music without mastering notation first. |
| Joseph A. Paradiso | [Professor of Media Arts and Sciences; Responsive Environments](https://www.media.mit.edu/people/joep/overview/). | Musical interfaces and live interaction; [the Jordan Rudess jam_bot collaboration](https://news.mit.edu/2024/model-virtuosity-jordan-rudess-jam-bot-1119) is a relevant example. |
| Tod Machover | [Professor of Music and Media; Opera of the Future](https://www.media.mit.edu/people/tod/overview/). | Hyperinstruments, Hyperscore and composition interfaces that expand human expression. |

Egozy, Paradiso and Machover are included for musical interaction and creative systems as well as AI-related work; their relevance extends beyond training music generators.

## Other academic and research contributors

| Researcher | Affiliation or research context | Relevance to Music Kitchen |
|---|---|---|
| Chris Donahue | [Carnegie Mellon University](https://chrisdonahue.com/). | Controllable music generation, Piano Genie and interactive systems for musicians and non-musicians. |
| Hao-Wen (Herman) Dong | [University of Michigan, Performing Arts Technology](https://smtd.umich.edu/profiles/hao-wen-dong/). | Music AI and music technology; symbolic representation and generation. |
| Xu Tan | Co-author in Microsoft Research Asia's [AI Music / Muzic work](https://www.microsoft.com/en-us/research/project/ai-music/), including PopMAG and DeepSinger. | Accompaniment generation and singing synthesis. |
| Tie-Yan Liu | Co-author in Microsoft's [AI Music work](https://www.microsoft.com/en-us/research/project/ai-music/), including PopMAG and DeepSinger. | Symbolic generation and the connection between composition and voice synthesis. |
| Meinard Müller | [International Audio Laboratories Erlangen / FAU](https://www.audiolabs-erlangen.de/fau/professor/mueller). | Music representations, audio–score synchronization and methods for measuring musical fidelity. |

## Reading this week

- **Meinard Müller.** *Fundamentals of Music Processing: Audio, Analysis, Algorithms, Applications.* Springer, **2015, first edition**. Reading **Chapter 1, Music Representations**, pp. 1–37: sheet music, symbolic representations and audio. [Publisher](https://link.springer.com/book/10.1007/978-3-319-21945-5) · [Companion notebooks](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C0/C0.html).
- **Jade Copet et al.** *Simple and Controllable Music Generation* (**MusicGen**, NeurIPS 2023). Focus: how melody conditioning differs from exact note control. [Paper](https://arxiv.org/abs/2306.05284).
- **Alexandre Défossez, Jade Copet, Gabriel Synnaeve and Yossi Adi.** *High Fidelity Neural Audio Compression* (**EnCodec**, 2022 preprint). Focus: what the compressed audio representation retains, and why codec tokens are not readable notation. [Paper](https://arxiv.org/abs/2210.13438).
