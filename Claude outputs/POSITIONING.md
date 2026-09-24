---
title: "Where AI Music Generation Stands, and Where the Openings Are"
subtitle: "A research-positioning one-pager, drawn from the Maestro survey of 463 works (1957–2026)"
author: "Henry Tan · Maestro"
date: "2026-09-07"
bibliography: references.bib
description: "What AI music generation has solved, what it is still arguing about, and three thesis-shaped projects that fit a 6–12 month timeline."
canonical: "https://htansetiawan.github.io/maestro/survey/positioning.html"
---

# 1. The state of the field in one paragraph

Generation is no longer the bottleneck. Text-to-audio song generation works at consumer quality, commercially and in the open [@suno2026; @udio2025; @google2025lyria2; @gong2026acestep15; @ning2025diffrhythm]. Symbolic infilling under hard constraints — mask a region, regenerate it, keep everything else fixed — is mature and available under permissive licences [@thickstun2024anticipatory; @pasquier2025midigpt; @malandro2024composersassistant2; @ens2020mmm]. What remains unsolved is everything around the act of generation: how a musician states what they want, and how the machine reports what it did. The field optimised the *compile* step and left *annotate* and *review* almost untouched.

# 2. Solved enough to build on

**Audio synthesis and full-song generation.** Prompt to finished master, with vocals, in seconds; open weights run on consumer GPUs [@gong2026acestep15; @yuan2025yue; @liu2025songgen; @evans2024stableaudioopen].

**Transcription and separation.** Piano audio to MIDI is reliable [@hawthorne2018onsets; @hawthorne2019maestro]; instrument-agnostic note transcription ships as a plugin [@bittner2022basicpitch]; stem separation is a commodity feature.

**Symbolic infrastructure.** Notation rendering [@pugin2014verovio; @osmd2026], tokenisation [@fradet2021miditok; @liao2024symusic], score–performance alignment [@cancinochacon2022partitura] and corpus analysis [@cuthbert2010music21] are all adopt-not-build.

**Constrained regeneration.** The primitive the composer's loop needs. Coconet framed it in 2017 as modelling how composers "write music in a nonlinear fashion, scribbling motifs here and there" [@huang2017coconet]; nine years on it works at bar × track granularity with ten-odd named controls [@malandro2024composersassistant2; @pasquier2025midigpt], and one deployment reports musicians accepting roughly 23% of 318,000 span-level suggestions inside a notation editor [@donahue2024hookpadaria].

# 3. Working, imperfect — where the effort currently goes

**Long-form structure.** Deep generators still differ measurably from human music in repetition and hierarchy [@dai2022missing; @dai2024interconnections]. The remedies make form an explicit, editable input [@dai2021controllable; @wang2024wholesong].

**Controllability of audio models.** Chord-, melody- and curve-conditioning exist but stay research-grade [@tal2024jasco; @lin2023cocomulla; @wu2024musiccontrolnet; @tsai2025musecontrollite]; no commercial full-song system accepts MIDI or chords as a *generation* condition. Inference-time optimisation is the most general mechanism for imposing a musical feature on a frozen model [@novack2024ditto].

**Real-time interaction.** Latency crossed into usability — roughly 200 ms control latency on a laptop with open weights [@lyria2025livemusic] — and RL-tuned accompaniment now anticipates rather than merely reacts [@wu2024realchords; @scarlatos2025realjam; @wu2026gapt]. A 2024 Aalto thesis reaches the same anticipation behaviour with a much cheaper trick: pad away part of the chord sequence so the model learns to generate melody while harmony lags [@wang2024realtimesymbolic].

**Expressive rendering.** Score to expressive MIDI is a separable, controllable stage [@jeong2019virtuosonet; @wu2022mididdsp; @borovik2023scoreperformer].

**Machine music analysis.** Roman-numeral analysis reaches about 51% full-label accuracy (AugmentedNet) to 62% (RNBert), with key at 82–83% [@napoleslopez2021augmentednet; @sailor2024rnbert] — good enough to *propose* a label for correction, not to trust silently.

# 4. Contested, no consensus

**Evaluation.** Distributional audio metrics correlate weakly with human preference [@chung2025kad; @grotschla2025benchmarking; @huang2025aligning], and almost no generation paper evaluates a composer's workflow at all. The one substantial producer study reports "creative misalignment" and demands for control [@ronchini2025ttmuserstudy]; co-creative systems over-measure user experience and under-measure the creativity of the collaboration [@karimi2018evaluating].

**Provenance and law.** Being settled in court, not in papers: memorisation held to be reproduction in Munich [@lgmunich2025gemaopenai; @lgmunich2026gemasuno], human authorship required for protection in the United States [@usco2025part2; @thaler2025perlmutter], and the label settlements producing licensed, walled-garden models [@umg2025udio; @wmg2025suno].

**Whether language models can reason about music.** Every benchmark says not reliably [@li2024ziqieval; @weck2024muchomusic; @wei2024musictheory; @kumar2026howfar]. The emerging architecture is an LLM as orchestrator around deterministic analysers, not as the analyser.

# 5. Genuinely open — the thin nodes

Four taxonomy nodes are nearly empty, and they are the ones a composer inhabits.

**Annotations as machine instructions (S2.4 — 4 of 463 works, none about music).** All the parts exist and have never been assembled: typed, musical-time-anchored annotation records [@giraud2018dezrann; @pugin2014verovio]; free-form ink and audio placed on and between staves [@cavez2025euterpen]; a grammar that parses "language plus a sketch on the artifact" into typed references with per-modality resolvers, demonstrated for video [@tilekbay2024expressedit]; selection-then-instruction as an interaction [@masson2024directgpt]; musician-readable structural feedback to an agent [@xu2026libretto].

**The machine explaining itself (S4.4 — 2 works).** A survey of 92 co-creative systems found the AI-to-human direction essentially undesigned [@rezwana2023cofi]. The exceptions are few and instructive: a critic that says *where* to change before *how* [@ramoneda2024refinpaint], committed-versus-tentative display of an agent's plan [@scarlatos2025realjam], explain-and-debug affordances [@louie2020cococo].

**Symbolic editing and proofreading (S4.2 — 2 works)** and **musical version control (S4.5 — 5 works, none with branch/merge)** [@foscarin2019diff; @flat2026history; @suh2024luminate].

**Notation-native generation.** No verified system emits MusicXML or MEI directly [@xu2025metascore; @qu2024mupt; @wang2025notagen], and the notation incumbents ship nothing generative [@steinberg2025dorico6; @avid2026sibelius; @musegroup2025musescore46] — DeepBach's 2017 MuseScore plugin remains nearly the only research deployment on a notation surface [@hadjeres2017deepbach].

Two findings make this the right place to work rather than merely an empty one. Steering interfaces move a composer's control, ownership and self-efficacy even with the model held fixed, and interface and model gains are complementary [@louie2020cococo; @louie2022expressive]; and a single slider is not control — MMM-C scored acceptable usability while its users' desire for more control averaged 9.5 out of 10 [@tchemeube2023mmmc]. Practitioners, asked directly, want to pull material rather than be pushed it, and reject automatic completion while accepting transformation of their own material [@deruty2022sonycsl; @newman2023perceptions; @krol2025ownership; @huang2020aisongcontest].

# 6. Three projects that fit 6–12 months

**A. The build log — best risk/reward.** Wrap a frozen, permissively-licensed infiller [@thickstun2024anticipatory] — it runs in a browser [@zhou2024midinfinite] — with the missing return channel: per region, which constraints bound, which were relaxed and why, where the model was least confident, what it would offer instead. Then measure whether the explanation changes trust, ownership and *suggestion acceptance rate*. No model training. Instruments already exist [@cherry2014csi]. Directly addresses S4.4, the thinnest load-bearing node. CHI- or ISMIR-shaped.

**B. Annotation-following: a benchmark, then a system.** No benchmark exists for "did the model honour the composer's marks?" Build the task suite, compliance metrics and baselines across existing infillers, then a compiler for *one* annotation type — region plus natural-language instruction on a lead sheet. Nearest precedents: rejection sampling of LLM proposals against a music prior [@kim2025amuse], zero-shot symbolic editing evaluated as unit tests [@zhang2025groove]. Higher ceiling than A; the benchmark alone stands as a contribution if the system slips.

**C. The notation round-trip.** Lossless textual IR ↔ MusicXML/MEI, so generation can happen in notation at all. Lower risk, lower ceiling — a resource paper, and a prerequisite for A and B. Best treated as a component.

**Avoid at this timescale:** symbolically-conditioned audio rendering (compute-heavy, crowded), licence-clean corpus assembly (legal legwork, though the clean sets are real [@long2024pdmx; @gotham2022openscore]), version control (needs a user base before it can be studied).

**The failure mode that kills all three:** building a demo and running out of time before the evaluation. Fix the study design in month one.

# 7. Local advantage

Krzysztof Gajos is at Harvard SEAS and co-authored ChordRipple — Anna Huang's first music paper — with her at Harvard in 2016 [@huang2016chordripple]. His group's work is exactly the human-AI interaction research that projects A and B require. Huang is now at MIT [@mit2026mtcshowcase], one stop away, and Donahue's lab at CMU is the other centre of gravity for this line [@gclef2026lab; @kim2026decomposer]. For the interaction-flavoured version of this work, the advising is unusually well placed.

# References
