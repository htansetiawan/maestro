---
title: "A Taxonomy of the Human-Centered AI Music Co-Creation Space"
subtitle: "Organizing 463 works (1957–2026) around the composer's loop: Compose → Annotate → Compile → Edit"
author: "Henry Tan · Maestro"
date: "2026-09-07"
bibliography: references.bib
description: "Forty-nine nodes and ten coding dimensions for placing any music-AI system inside a composer's workflow — and for seeing exactly where the field is thin."
canonical: "https://htansetiawan.github.io/maestro/survey/taxonomy.html"
---

# 1. Purpose and organizing principle

This taxonomy organizes the literature and system landscape relevant to an open-source, **human-centered AI music studio for composers**. The studio's thesis is that the composer stays at the center and the AI acts as a *compiler, assembler and enabler*: the human composes material, annotates it (in notation, by scribbling, humming, or attaching example audio, images, video or text), the AI **compiles** a fuller realization under those constraints, and the human edits and re-annotates — iteratively, at the granularity of a bar, a part, or a gesture, never as a one-shot "prompt → finished song."

Most existing surveys of music AI are organized by *technique* (autoregressive vs. diffusion), *domain* (symbolic vs. audio) or *task* (generation, transcription, recommendation) [@ji2023survey; @le2025nlpsurvey; @ma2024foundation; @kader2025survey]. Those axes matter, but they do not tell a builder *where a given piece of work fits in a composer's workflow*. We therefore use two orthogonal views:

1. **The stage view (Part A).** Every work is assigned a primary node in a tree whose trunk is the composer's loop — **Compose (S1) → Annotate (S2) → Compile (S3) → Edit (S4)**, with **Play (S5)** for the real-time branch of the loop — plus three supporting layers: **Foundations (F)** that precede the loop (history and theories of co-creativity), **Substrate (B)** beneath it (representations, engines, toolkits, data), and **Context (C)** around it (products, law, ethics, economics). **Evidence & Evaluation (E)** is the meta-layer that tells us whether any of it works for composers.
2. **The dimension view (Part B).** Ten cross-cutting dimensions (domain, task framing, control granularity, input modalities, initiative, communication direction, editability of the intermediate representation, integration surface, evidence level, openness/provenance) code any work independently of its stage. These dimensions are where the studio's *design position* is stated precisely (Part C) and where the *gaps* become visible (Part D).

The corpus behind this taxonomy is the set of 463 annotated entries in `notes/01–08` (399 unique bibliographic records in `references.bib`), gathered in September 2026 from eight research clusters seeded by the founder (Music Transformer and Anna Huang's lineage; the CMU/G-CLef cluster including Amuse, ExpressEdit and REAL; Egozy and Machover at MIT; music21 and MIT 21M.383; Suno and ACE-Step; the CMU 2026 creativity study). Each entry carries a verification level (verified against a primary source / partial / unverified) that is preserved in the notes.

Vocabulary borrowed and reused. From Rowe's *Interactive Music Systems* [@rowe1993interactive]: *score-driven vs. performance-driven* input, *transformative / generative / sequenced* response, and the *instrument vs. player* paradigm. From Kantosalo & Toivonen [@kantosalo2016modes]: *alternating vs. task-divided* co-creativity. From Rezwana & Maher's COFI [@rezwana2023cofi]: the two *communication directions* (human→AI, AI→human). From Lubart [@lubart2005partners]: the computer as *nanny, pen-pal, coach, colleague*. From Shneiderman [@shneiderman2007cst; @shneiderman2020hcai]: *creativity support* and the *high-control / high-automation* quadrant of human-centered AI.

---

# 2. Part A — The stage view

Each node lists a definition, the questions it answers for the studio, and *representative* works (not exhaustive; the full auto-coded assignment of all 463 entries is in `taxonomy-map.md`).

## F. Foundations (before the loop)

**F1. Algorithmic composition lineage.** Rule-, Markov-, grammar- and recombination-based composition from the ILLIAC Suite onward; the first neural sequence models. *Why it matters:* it fixes the vocabulary of "constraint-satisfying generation" and shows that "compile from rules" predates deep learning by decades.
Representative: @hiller1959experimental; @xenakis1992formalized; @koenig1970project; @cope2001virtual; @mcintyre1994bachinabox; @eck2002blues; @boulangerlewandowski2012modeling; @sturm2016folkrnn; @nierhaus2009algorithmic.

**F2. Interactive music systems and accompaniment lineage.** Machines that listen and respond in real time: score following, computer accompaniment, improvising partners. *Why it matters:* Rowe's taxonomy is directly reusable for the studio's design space, and Dannenberg's 1984 accompaniment algorithm is the ancestor of every "AI plays with you" feature.
Representative: @dannenberg1984online; @vercoe1984syntheticperformer; @rowe1993interactive; @lewis2000toomanynotes; @biles1994genjam; @pachet2003continuator; @assayag2006omax; @dannenberg2014hcmp.

**F3. Commercial auto-accompaniment and notation lineage.** Band-in-a-Box, the Korg i3 and the arranger-keyboard "style" engine; notation editors and MIDI sequencers. *Why it matters:* "chords + style → arrangement" is the historical *compile*; its strengths (deterministic, editable, parameterized) and weakness (genericness) define what a learned, annotation-steerable descendant must improve on.
Representative: @pgmusic1990bandinabox; @pgmusic2026biab; @korg1993i3; @makemusic2024finale; @apple2024logicpro11.

**F4. Theories of co-creativity and creativity support.** Frameworks for describing and evaluating human–AI creative partnership.
Representative: @shneiderman2007cst; @shneiderman2020hcai; @cherry2014csi; @lubart2005partners; @deterding2017mici; @kantosalo2016modes; @rezwana2023cofi; @rezwana2022perceptions; @karimi2018evaluating; @guzdial2019friend; @davis2016drawingapprentice; @boden2004creativemind; @colton2008tripod; @jordanous2012standardised; @ritchie2007criteria; @fiebrink2018mlcreativetool; @wan2024secondmind.

**F5. Human-centered music-AI programmes and design spaces.** Articulated research agendas that share the studio's stance: Huang's "steerable, decomposable" line at Magenta and now MIT HAI-Res; Donahue's G-CLef at CMU; Sony CSL's practitioner-embedded approach; the Metacreation Lab; the 2026 design space for live music agents.
Representative: @huang2025creativityinteraction; @huang2020aisongcontest; @gclef2026lab; @kim2026designspace; @deruty2022sonycsl; @mit2026mtcshowcase; @egozy21m385.

## S1. Compose — getting musical ideas in

The composer's raw material enters through many channels. The recurring finding across this node is that **every successful "loose" modality lands in a symbolic, editable representation** (MIDI, lead sheet, notation); systems that go straight to audio offer no correction handle.

**S1.1 Performance capture and transcription.** MIDI keyboard input; audio→MIDI/score transcription; optical music recognition.
Representative: @hawthorne2018onsets; @gardner2022mt3; @bittner2022basicpitch; @donahue2022sheetsage; @hawthorne2019maestro; @riosvila2024smt; @jung2025unified; @bradshaw2025ariamidi.

**S1.2 Voice: humming and singing as input.** Query-by-humming → humming transcription → vocal→accompaniment → vocal imitation as a control signal.
Representative: @ghias1995qbh; @frank2020humtosearch; @liu2023humtrans; @gupta2024dynhumtrans; @doremir2014scorecloud; @vochlea2021dubler; @donahue2023singsong; @cartwright2015vocalsketch; @floresgarcia2025sketch2sound; @magenta2020tonetransfer.

**S1.3 Sketch, pen and scribble as input.** Drawn contours and pen-based notation, from UPIC and Hyperscore to sketch-conditioned melody models and pen-and-touch score writing.
Representative: @xenakis1992formalized; @farbood2004hyperscore; @coughlan2006interaction; @garcia2012paper; @hearn2015staffpad; @chen2020sketchnet; @namgyal2022mididraw; @liang2024drawlody; @benetatos2022drawlisten; @cavez2024challenges; @cavez2025euterpen; @igarashi1999teddy.

**S1.4 Image, video and text as inspiration or condition.** Cross-modal conditioning, including text→symbolic generation.
Representative: @kim2025amuse; @zhang2022vis2mus; @chowdhury2024melfusion; @rinaldi2024art2mus; @su2024v2meow; @kang2024video2music; @tian2025vidmuse; @li2024muvi; @liu2024mumullama; @lu2023musecoco; @bhandari2025text2midi; @wu2025midillm; @xu2025metascore.

**S1.5 Example audio and personal style as reference.** "Make it like this" steering by instance rather than by words.
Representative: @rouard2024musicgenstyle; @dinculescu2019midime; @frid2020example; @louie2020cococo; @neutone2024morpho; @zhouzheng2025midirwkv.

## S2. Annotate — expressing intent on the material

Annotation is the studio's central concept: a typed, musically-anchored mark (on a bar, staff, region or note) that the compiler must honor. The literature offers mature *encodings* and *analysis models*, a converging *control vocabulary*, and a striking **gap**: no system treats a composer's margin notes on notation as instructions to a generator.

**S2.1 Annotation encodings, standards and tools.** How analysts, editors and performers mark up scores and audio; machine-readable formats anchored to musical time.
Representative: @pugin2014verovio; @goebl2023meifriend; @w3c2021musicxml40; @walshaw2011abc; @huron1995humdrum; @giraud2018dezrann; @cannam2010sonicvisualiser; @gotham2019wheninrome; @neuwirth2018abc; @hentschel2021mozart; @newzik2026readers; @fu2026tactus; @egozy2018concertcue.

**S2.2 Machine-proposed annotations (analysis models).** Harmony, key, structure, phrase and schema analysis that can *propose* labels for the composer to accept or fix.
Representative: @napoleslopez2021augmentednet; @karystinaios2023chordgnn; @sailor2024rnbert; @chen2021attend; @nieto2016msaf; @kim2023allinone; @dai2022missing; @dai2024interconnections; @bock2016madmom; @nihahn2024schenker; @finkensiep2018skipgrams; @wei2024musictheory; @huang2005palestrinapal.

**S2.3 Control vocabularies as annotation schemas.** The attributes generation systems already accept — instrument, note density, polyphony, pitch range, chord per beat, section label, style, tempo, dynamics/rhythm curves — which are exactly what a composer would annotate.
Representative: @vonrutte2023figaro; @guo2022musiac; @malandro2024composersassistant2; @pasquier2025midigpt; @lu2023musecoco; @chen2024sympac; @wu2024musiccontrolnet; @tan2022melodyinfilling; @young2021compositionalsteering; @tan2020fadernets.

**S2.4 Multimodal annotation as instruction.** Natural language + sketch + selection turned into an edit or generation request; the template is video's ExpressEdit and vision's instruction editing. *This is the studio's white space in music.*
Representative: @tilekbay2024expressedit; @masson2024directgpt; @brooks2023instructpix2pix; @xu2026libretto; @zhang2025groove; @elkins2025dawzy; @thisgoober2026real.

**S2.5 Economics of human labelling.** Where one cheap, well-placed human annotation outperforms full automation.
Representative: @bukey2024justlabel.

## S3. Compile — assembling music from human material and annotations

The generative core. Two sub-trees: **symbolic** (S3.1–S3.7), where outputs are directly editable notation/MIDI, and **audio** (S3.8–S3.10), where the studio needs *rendering* and must understand the text-to-song paradigm it is inverting.

**S3.1 Symbolic representations and tokenizations.** MIDI-like events, REMI, Compound Word, Octuple, MMM's per-track bars, ABC text, piano-roll images; tokenizer libraries.
Representative: @huang2018musictransformer; @huang2020popmusictransformer; @hsiao2021compoundword; @zeng2021musicbert; @fradet2021miditok; @liao2024symusic; @dong2023mmt; @ens2020mmm; @yuan2024chatmusician; @qu2024mupt.

**S3.2 Infilling and constrained regeneration.** Mask-and-refill at note, bar, track or region granularity with everything else as a hard constraint — *the primitive that implements "edit → compile."*
Representative: @huang2017coconet; @hadjeres2017deepbach; @ippolito2018infilling; @pati2019inpaintnet; @ens2020mmm; @chang2021xlnet; @guo2022musiac; @thickstun2024anticipatory; @malandro2024composersassistant2; @pasquier2025midigpt; @zhouzheng2025midirwkv; @min2023polyffusion; @lv2023getmusic; @ramoneda2024refinpaint; @papadopoulos2016flowcomposer; @donahue2024hookpadaria.

**S3.3 Attribute-, text- and rule-conditioned symbolic generation.** Steering by descriptors, sliders, text, or training-free guidance.
Representative: @vonrutte2023figaro; @lu2023musecoco; @wu2023musemorphose; @tan2020fadernets; @huang2024scg; @petteno2025lcdiff; @bhandari2025text2midi; @lin2026diffsymbo; @xu2025metascore; @wu2025midillm; @roberts2018musicvae.

**S3.4 Structure-aware and hierarchical pipelines.** Form → phrase → lead sheet → accompaniment, each level editable; the strongest existing analogues of a "compiler with intermediate representations."
Representative: @huang2018musictransformer; @yu2022museformer; @dai2021controllable; @dai2022missing; @wang2024wholesong; @tan2022melodyinfilling; @chen2024sympac; @xu2026libretto; @dai2023personalised.

**S3.5 Harmonization, accompaniment and arrangement.** Lead sheet → piano texture → multi-track orchestration; chord-constrained harmonization; the commercial arranger engines.
Representative: @zhao2021accomontage; @zhao2023qa; @zhao2024structured; @kaliakatsospapakostas2025harmonization; @wu2024melodyt5; @jiang2025functionalignment; @huang2016chordripple; @pgmusic2026biab; @apple2024logicpro11; @wu2026stemphonic.

**S3.6 Music LLMs and music-as-code.** LLMs writing ABC/MIDI tokens/programs; multi-agent composition; decompiling MIDI to editable programs; the live-coding and computer-aided-composition lineage that makes "compile" literal.
Representative: @yuan2024chatmusician; @qu2024mupt; @wang2025notagen; @wu2024melodyt5; @kumar2026howfar; @deng2024composerx; @yu2023musicagent; @kim2026decomposer; @xu2026libretto; @nienhuys2003lilypond; @mclean2014tidal; @assayag1999openmusic; @wang2015chuck; @omar2019hazel; @cuthbert2010music21; @dannenberg1997nyquist.

**S3.7 Expressive performance rendering.** Score → expressive MIDI (timing, dynamics, articulation), with text/emotion controls; a separable, editable stage before synthesis.
Representative: @jeong2019virtuosonet; @borovik2023scoreperformer; @zhang2024dexter; @wu2022mididdsp; @cancinochacon2022partitura.

**S3.8 Audio rendering and symbolic-conditioned audio generation.** Audio models that accept chords, melody, MIDI or time-varying curves; neural synthesis from MIDI; real-time MIDI-steerable audio.
Representative: @tal2024jasco; @lin2023cocomulla; @wu2024musiccontrolnet; @tsai2025musecontrollite; @melechovsky2024mustango; @novack2024ditto; @hou2024melodycontrolnet; @wu2022mididdsp; @lyria2025livemusic; @zhu2024musichifi; @engel2020ddsp; @magenta2022ddspvst.

**S3.9 Text-to-music and full-song audio generation (the paradigm to invert).** Foundations, commercial systems, open-weights song models, and stem-level generation.
Representative: @dhariwal2020jukebox; @agostinelli2023musiclm; @huang2023noise2music; @copet2023musicgen; @liu2023audioldm; @evans2024longform; @evans2024stableaudioopen; @li2023jen1; @prajwal2024musicflow; @ziv2024magnet; @suno2026; @udio2025; @google2025lyria2; @elevenlabs2025music; @gong2025acestep; @gong2026acestep15; @yuan2025yue; @ning2025diffrhythm; @liu2025songgen; @heartmula2026; @parker2024stemgen; @mariani2024msdm; @rouard2025musicgenstem; @nistal2024diffariff; @forsgren2022riffusion.

**S3.10 Music-understanding models as compile-time critics.** Encoders and audio-LLMs that could check, caption or critique compiled output — currently not reliable enough to trust silently.
Representative: @li2024mert; @zhu2025muq; @wu2023clap; @liu2023mullama; @gardner2024llark; @deng2024musilingo; @tang2024salmonn; @chu2024qwen2audio; @zhao2024openmu; @weck2024muchomusic; @castellon2021codified.

## S4. Edit — revising and iterating

**S4.1 Editing paradigms (from HCI at large).** Direct manipulation, instruction-based editing, sketch interfaces, programming by demonstration, live/projectional programming.
Representative: @shneiderman1983direct; @masson2024directgpt; @brooks2023instructpix2pix; @tilekbay2024expressedit; @igarashi1999teddy; @cypher1993wwid; @omar2019hazel.

**S4.2 Symbolic editing, variation and proofreading.** Transform-what-I-wrote rather than generate-for-me; AI critics that mark *where* to edit.
Representative: @krol2025ownership; @wu2023musemorphose; @zhang2025groove; @ramoneda2024refinpaint; @malandro2024composersassistant2; @papadopoulos2016flowcomposer; @tan2020fadernets.

**S4.3 Audio editing and inpainting.** Text- and inversion-based editing, instruction editors, region repainting in products.
Representative: @zhang2024musicmagus; @manor2024zeta; @wang2023audit; @han2023instructme; @zhang2025instructmusicgen; @lelan2024melodyflow; @yang2025songeditor; @chu2025text2fx; @adobe2024musicgenaicontrol; @novack2025arc; @wang2026latentft.

**S4.4 AI→human feedback, explanation and plan preview.** The under-designed half of co-creation: systems that annotate *back*.
Representative: @ramoneda2024refinpaint; @louie2020cococo; @bryankinns2021xai; @rezwana2023cofi; @tilekbay2024expressedit; @scarlatos2025realjam.

**S4.5 History, versioning, alternatives and branching.** Side-by-side alternatives, workflow histories, design-space exploration trees, score diffs, notation-editor version history.
Representative: @terry2002sideviews; @grossman2010chronicle; @suh2024luminate; @foscarin2019diff; @flat2026history; @goebl2023meifriend.

## S5. Play — real-time co-performance

**S5.1 Score following and accompaniment.** Representative: @dannenberg1984online; @vercoe1984syntheticperformer; @dannenberg2014hcmp; @egozy2016harmonix.

**S5.2 Improvisation partners.** Representative: @lewis2000toomanynotes; @biles1994genjam; @pachet2003continuator; @assayag2006omax; @shepardson2022notochord; @blanchard2025jambot.

**S5.3 RL-tuned and live neural models.** Representative: @wu2024realchords; @scarlatos2025realjam; @wu2026gapt; @wu2026streaming; @lyria2025livemusic; @novack2026lmdm; @donahue2019pianogenie; @scurto2021coexplorer; @zhou2024midinfinite.

**S5.4 Design spaces, practice and play.** Representative: @kim2026designspace; @brade2026agentsinconcert; @rowe1993interactive; @egozy21m385; @egozy2005harmonix; @miller2009schizophonic; @harmonix2020fuser; @wang2024musicaware; @wang2025rise.

## E. Evidence and evaluation

**E1. Controlled studies of co-creative music systems.** Representative: @louie2020cococo; @louie2022expressive; @kim2025amuse; @tchemeube2023mmmc; @liang2024drawlody; @scarlatos2025realjam; @zhang2023loopcopilot; @krol2025ownership; @oros2026cmu; @frid2020example; @wang2026multiverse.

**E2. Field studies and practitioner perspectives.** Representative: @huang2020aisongcontest; @micchi2021ikeepcounting; @morris2024haisp; @deruty2022sonycsl; @newman2023perceptions; @ronchini2025ttmuserstudy; @fu2025novice; @sturm2019machinefolk; @cavez2024challenges; @ford2024reflection; @suh2021socialglue; @oros2026helpthathurts.

**E3. Deployed systems with usage data.** Representative: @donahue2024hookpadaria; @huang2019bachdoodle; @papadopoulos2016flowcomposer; @casini2025sunoudio.

**E4. Metrics for generated music.** Representative: @kilgour2019fad; @gui2024fad; @chung2025kad; @retkowski2024fmd; @yang2020evaluation; @huang2025aligning; @kim2025musicarena; @liu2025musiceval; @grotschla2025benchmarking; @zhang2025aesthetics; @huang2025audiomos; @batlleroca2024mira; @figueiredo2025echoes; @manco2023songdescriber.

**E5. Creativity and co-creativity evaluation frameworks.** Representative: @cherry2014csi; @karimi2018evaluating; @jordanous2012standardised; @ritchie2007criteria; @colton2008tripod; @boden2004creativemind; @kantosalo2016modes; @deezer2025ipsos.

**E6. Music-theory competence benchmarks for models.** Representative: @yuan2024chatmusician; @li2024ziqieval; @wei2024musictheory; @weck2024muchomusic; @kumar2026howfar.

## B. Substrate (beneath the loop)

**B1. Notation engines and editors.** @pugin2014verovio; @osmd2026; @vexflow2024; @alphatab2026; @abcjs2026; @lilypond2026; @musescore2026studio; @musegroup2025musescore46; @steinberg2025dorico6; @avid2026sibelius; @makemusic2024finale; @flat2026; @soundslice2026; @donahue2024hookpadaria.

**B2. Symbolic toolkits.** @cuthbert2010music21; @cuthbert2023ocw21m383; @liao2024symusic; @fradet2021miditok; @cancinochacon2022partitura; @dong2020muspy; @raffel2014prettymidi; @roberts2018magentajs.

**B3. Runtime and integration.** @w3c2026webmidi; @spessasynth2026; @clap2022; @clavia2023nordstage4; @ahuja2025abletonmcp; @roberts2019magentastudio; @metacreation2023mmm4live.

**B4. Datasets and corpora (with licences).** Symbolic: @raffel2016lakh; @long2024pdmx; @gotham2022openscore; @bradshaw2025ariamidi; @hawthorne2019maestro; @kong2020giantmidi; @zhang2022atepp; @wang2020pop909; @ens2021metamidi; @lev2024lamidi; @kantarelis2024chordonomicon; @huang2019bachdoodle; @melechovsky2024midicaps; @xu2025metascore; @xmader2021musescore. Analysis corpora: @gotham2019wheninrome; @hentschel2021mozart; @neuwirth2018abc. Audio, stems, captions, humming: @manilow2019slakh; @manco2023songdescriber; @liu2023humtrans; @cartwright2015vocalsketch.

**B5. Education and the pedagogy of music-as-computation.** @cuthbert2023ocw21m383; @egozy21m385; @horn2022tunepad; @freeman2019earsketch; @aaron2016sonicpi; @donahue2024hookpadaria; @yousician2026; @miller2009schizophonic.

## C. Context (around the loop)

**C1. Product landscape 2024–2026.** Audio text-to-song platforms; symbolic assistants inside DAWs; DAW-native features; notation incumbents; AI singers; LLM→DAW bridges. @suno2026; @udio2025; @google2025lyria2; @elevenlabs2025music; @kunlun2025mureka; @novack2025arc; @apple2024logicpro11; @ableton2024live12; @donahue2024hookpadaria; @scaler2025v3; @hexachords2022orb; @malandro2024composersassistant2; @pasquier2025midigpt; @ahuja2025abletonmcp; @suno2025wavtool; @dreamtonics2025synthv2; @neutone2024morpho; @moises2025aistudio; @splice2024create; @steinberg2025dorico6; @avid2026sibelius; @musegroup2025musescore46.

**C2. Law and policy.** @umg2024vsuno; @umg2025udio; @wmg2025suno; @lgmunich2025gemaopenai; @lgmunich2026gemasuno; @usco2025part2; @thaler2025perlmutter; @eu2024aiact; @tennessee2024elvis; @concord2023anthropic; @sturm2019openquestions.

**C3. Ethics, provenance and disclosure.** @newtonrex2024fairlytrained; @newtonrex2024statement; @spawning2022haveibeentrained; @herndon2021hollyplus; @spotify2025aipolicy; @deezer2026aistats; @epple2024watermarking; @batlleroca2024mira; @usdoj2024smith.

**C4. Economics and attitudes.** @goldmedia2024gemasacem; @cisac2024pmp; @apraamcos2024ai; @deezer2025ipsos; @newman2023perceptions.

---

# 3. Part B — The dimension view (coding scheme)

Any work — paper, model, product — can be coded on the ten dimensions below. The values are ordered where an order is meaningful.

| # | Dimension | Values | Why it matters for the studio |
|---|-----------|--------|-------------------------------|
| D1 | **Output domain** | symbolic (score/MIDI) · audio · hybrid/multi-level (score → performance → audio) | The studio is symbolic-first with audio rendering; hybrid, multi-level systems (MIDI-DDSP, whole-song cascades) are its closest architectural relatives. |
| D2 | **Task framing** | from-scratch generation · continuation · **infilling / constrained regeneration** · transformation / variation · analysis / annotation · response / accompaniment | Infilling and transformation are the framings that keep the human's material as hard constraints. |
| D3 | **Control granularity** (the human's handle) | global prompt or attributes → section / form → bar × track region → note / event → continuous curve or parameter · plus *by example* | The founder's loop demands region-, note- and curve-level handles; text-to-song sits at the "global prompt" end. |
| D4 | **Input modalities** | notation · MIDI performance · text · voice/hum · sketch/pen · image · video · audio example | The studio is deliberately multimodal; most systems accept one or two. |
| D5 | **Initiative and timing** (Rowe; Kantosalo; COFI) | human-initiated turn-taking · alternating · task-divided · simultaneous / real-time · AI-initiated (proactive) | The loop is human-initiated turn-taking; Play (S5) is simultaneous. |
| D6 | **Communication direction** (COFI) | human→AI only · **bidirectional** (AI explains, critiques, previews its plan) | Almost all systems are one-directional; the studio wants AI annotations *back*. |
| D7 | **Editability of the intermediate representation** | opaque audio · editable symbolic · programmatic / code · multi-level editable | Determines whether "edit" is possible at all; code IRs (Decomposer, Strudel, ABC) make "compile" literal. |
| D8 | **Integration surface** | research demo · web app · DAW plugin · notation-editor plugin · API/library · hardware instrument | Practitioners reject tool-switching; notation-editor integration is nearly absent in the literature. |
| D9 | **Evidence level** | none · offline metrics only · lab user study (report N) · longitudinal / field · deployed with telemetry | Most generation papers stop at offline metrics; the HCI line supplies the user evidence. |
| D10 | **Openness and provenance** | open weights + code · code only · closed product; weight licence; training-data provenance (public-domain / CC / licensed / scraped) | Governs what an open-source studio can ship and on what legal footing. |

---

# 4. Part C — Where the studio sits in this space

Stated in the coding scheme, the founder's studio is:

- **D1** hybrid, *symbolic-first*: notation/MIDI is the source of truth; audio is a rendering target (S3.7 → S3.8), never the primary artifact.
- **D2** infilling and transformation dominant (S3.2, S4.2); from-scratch generation is a minor mode used to seed ideas, not to finish songs.
- **D3** region-, note- and curve-level control, plus by-example steering; annotations (S2) are the control vocabulary.
- **D4** all eight modalities, each routed into a symbolic representation before compilation (the S1 finding).
- **D5** human-initiated turn-taking as the default, with a real-time Play mode (S5) built on the same material.
- **D6** bidirectional: the compiler explains what it did with each annotation and can annotate back (critique, alternatives, structure labels).
- **D7** multi-level editable, including a programmatic IR ("music as code") so that *compile* is a real, inspectable operation with intermediate representations (form → lead sheet → parts → performance → audio).
- **D8** notation-editor-native (integrating with, not replacing, MuseScore/Verovio-class engines), with DAW and hardware (Nord Stage via MIDI) bridges.
- **D9** designed for lab studies *and* deployment telemetry from day one (CSI, ownership/control items, acceptance rates of suggestions).
- **D10** open code and open weights where possible; training data restricted to public-domain / CC / consented material; provenance metadata emitted by design.

In Rowe's terms the studio is a *score-driven, transformative* system in the *instrument* paradigm, with optional *player*-paradigm agents in Play mode. In Lubart's terms the AI is a *colleague* at compile time and a *coach* when it annotates back — never the *author*.

---

# 5. Part D — Gaps the taxonomy makes visible

Each gap is a node or dimension where the literature is thin *and* the studio's design needs it. These are candidate research contributions.

1. **Annotations as prompts on notation (S2.4).** No fetched system treats a composer's typed, drawn, hummed or attached annotations on a score as machine-readable instructions to a generator. The nearest pieces are ExpressEdit for video [@tilekbay2024expressedit], DirectGPT's selection→prompt engineering [@masson2024directgpt], Libretto's structural feedback grammar [@xu2026libretto], EuterPen's non-AI free-form annotations on staves [@cavez2025euterpen] and Dezrann/MEI's typed, time-anchored labels [@giraud2018dezrann; @pugin2014verovio]. A *music annotation compiler* that combines them is white space.
2. **No verified system generates MusicXML/MEI natively (S3.1).** Generation lives in MIDI tokens, ABC or piano-roll; MetaScore converts MuseScore files *out* to REMI+ [@xu2025metascore]. A lossless bridge between an LLM-friendly textual IR and engraving-grade notation is both an engineering prerequisite and an open research problem.
3. **Notation-editor integration is nearly absent (S3.2 × D8).** DeepBach's 2017 MuseScore plugin [@hadjeres2017deepbach] and Hookpad Aria's lead-sheet copilot [@donahue2024hookpadaria] are the only notation-surface deployments found; the DAW side (Composer's Assistant, MIDI-GPT, Magenta Studio) is far richer. The notation incumbents (Dorico, Sibelius, MuseScore) ship no generative features as of 2026.
4. **Multimodal editing on scores (S4.1 × D4).** NL + sketch + audio-example editing exists for video, not for music; Draw and Listen! [@benetatos2022drawlisten] and Drawlody [@liang2024drawlody] handle sketch alone.
5. **AI→human communication is under-designed (S4.4 × D6).** COFI found almost no AI→human communication across 92 systems [@rezwana2023cofi]; RefinPaint's "where to modify" critic [@ramoneda2024refinpaint] and ReaLJam's committed-vs-tentative waterfall [@scarlatos2025realjam] are the early exceptions.
6. **Versioning with musical semantics (S4.5).** Score diffs exist [@foscarin2019diff] and Flat.io keeps per-edit history [@flat2026history], but branch/merge, variation trees over compiled outputs [@suh2024luminate] and provenance logs that could double as authorship evidence [@micchi2021ikeepcounting] are unexplored for music.
7. **Symbolic-conditioned audio rendering is thin (S3.8).** JASCO, Coco-Mulla, Music ControlNet, MuseControlLite and MIDI-DDSP are research-grade; no commercial full-song system accepts MIDI or chords as a *generation* condition (Suno Studio's 2026 MIDI editing is inside its DAW, not its generator) [@suno2026; @tal2024jasco].
8. **Humming transcription still needs a correction UI (S1.2).** Off-the-shelf transcribers reach single-digit note-F1 on HumTrans; purpose-built models reach ~0.67 [@liu2023humtrans; @gupta2024dynhumtrans]. Interactive disambiguation is a design requirement, not a nicety.
9. **Structure and repetition remain weak in deep generators (S3.4).** Dai & Dannenberg's analyses show striking differences from human pop [@dai2022missing]; explicit, editable structural skeletons [@dai2021controllable; @wang2024wholesong] are the remedy and fit the annotation layer.
10. **Evaluation of the *loop*, not the output (E).** Instruments exist (CSI, Karimi's framework, ownership/control items, paired listener tests) but longitudinal, in-practice studies are rare [@krol2025ownership; @deruty2022sonycsl]; distributional audio metrics correlate weakly with human preference [@chung2025kad; @grotschla2025benchmarking].
11. **LLMs are not yet music theorists (E6).** ZIQI-Eval, ABC-Eval, MusicTheoryBench and MuChoMusic all report weak reasoning [@li2024ziqieval; @yuan2024chatmusician; @weck2024muchomusic]; architectures should use LLMs as orchestrators around specialised symbolic models and analysers.
12. **Licence-clean training data for symbolic models (B4 × D10).** PDMX, OpenScore and Bach Doodle are clean; Aria-MIDI, Hooktheory and DCML are non-commercial; MuseScore scrapes are legally toxic; Lakh's CC-BY licence covers the collection, not the underlying songs [@long2024pdmx; @gotham2022openscore; @bradshaw2025ariamidi; @xmader2021musescore; @raffel2016lakh].

---

# 6. How to use this taxonomy

- **For the literature review:** `literature-review.md` follows Part A's order (F → S1 → S2 → S3 → S4 → S5 → E → B → C) and closes with Part D.
- **For the annotated bibliography:** the per-cluster notes in `notes/` are the long-form records; `taxonomy-map.md` assigns every entry a primary node (461 of 464 hand-coded by canonical BibKey; 3 auto-coded from tags). Node counts are themselves diagnostic: the thinnest nodes — S2.3 control vocabularies as annotation schemas (3 primary entries), S2.4 multimodal annotation as instruction (4), S2.5 (1), S4.2 symbolic editing and proofreading (2), S4.4 AI→human feedback (2), S5.1 score following (1), and S1.5 example-based steering and S5.2 improvisation partners (3 each) — coincide with the gaps in Part D, while S3.9 text-to-music (23), B4 datasets (21) and C1 products (21) are the crowded nodes.
- **For design work:** Part B is a checklist. Every feature proposal for the studio should state its D1–D10 values; every competitor or paper can be placed on the same grid.
- **For the research agenda:** Part D is the seed list of contributions; each gap names the nearest prior work to build on.

# References
