---
title: "Annotated Bibliography"
subtitle: "394 unique works, organized by taxonomy node"
author: "Henry Tan · Maestro"
date: "7 September 2026"
description: "394 works in AI music research, each with what it does, what evidence backs it, and how it was verified — organized by taxonomy node rather than alphabetically."
canonical: "https://htansetiawan.github.io/maestro/survey/annotated-bibliography.html"
---

Records merged from the eight research clusters in `notes/`. Each entry gives provenance, what the system does, its evidence, and why it matters for a composer-centered studio. **Verification** records how the entry was checked in September 2026: *verified* = a primary source was fetched; *partial* = secondary pages or search snippets only; *unverified* = recall, not re-confirmed. Treat figures in partial and unverified entries as indicative. Cluster numbers refer to the source notes files. Citation keys match `references.bib`.

## F1. Algorithmic composition lineage

### `sturm2016folkrnn` — folk-rnn — Music transcription modelling and composition using deep learning

*Bob L. Sturm, João Felipe Santos, Oded Ben-Tal, Iryna Korshunova; QMUL/Kingston; Conference on Computer Simulation of Musical Creativity (CSMC) 2016; arXiv 1604.08723.*

Links: https://arxiv.org/abs/1604.08723 ; code/data: https://github.com/IraKorshunova/folk-rnn ; web: https://folkrnn.org

Character-level LSTM trained on ~23,000 Irish/Celtic session tunes in ABC notation; generates complete tunes as text that renders directly to notation. Human control is via seeding (key, meter, opening notes) and temperature; no infilling. Evaluated at population level, individual-tune level, and for usefulness in composers' practice.

**Evidence.** Musicians adopted tunes into sessions; a series of follow-ups (Sturm & Ben-Tal 2017, "Machine folk" concerts) and the "Let's Have Another Gan Ainm" album.

**For the studio.** Established ABC-as-text as a viable symbolic representation for neural models — the lineage that leads to ChatMusician/MuPT/NotaGen — and showed early on that composers use such models as idea generators, not song machines.

<small>Tags: [symbolic-generation] [representation] [notation] [creativity-support] [history] · Verification: verified (arXiv abstract fetched) · Clusters 03, 08</small>

### `cope2001virtual` — EMI — Experiments in Musical Intelligence ("Emmy") and Emily Howell

*David Cope, UC Santa Cruz; started 1981; ICMC paper 1987; books *Computers and Musical Style* (1991), *Experiments in Musical Intelligence* (1996), *Virtual Music* (MIT Press 2001, ed. Cope with Hofstadter et al.); database deleted 2005; Emily Howell album 2009.*

Links: https://en.wikipedia.org/wiki/Experiments_in_Musical_Intelligence

Recombinant style modelling in ~20,000 lines of Lisp: segment a corpus of one composer, pattern-match "signatures", classify segments (SPEAC: statement/preparation/extension/antecedent/consequent), and recombine under grammar constraints into new works in that style (Bach chorales, Mozart, Chopin, opera). Emily Howell added interactive feedback so a *personal* style emerged.

**Evidence.** Hofstadter's touring "Chopin vs EMI" tests — audiences (incl. at University of Oregon, 1997, with Steve Larson) guessed at roughly chance. *Virtual Music* (2001) collects the Cope–Hofstadter debate on whether recombinant pastiche is creativity; Hofstadter found the results disturbing precisely because they succeeded.

**For the studio.** The canonical warning about *style pastiche* and authorship; also the origin of the "creativity vs perception of creativity" argument later formalised by Colton. Cope's deletion of the database anticipates today's memorisation/originality debates.

<small>Tags: [history] [symbolic-generation] [style-transfer] [ethics-legal] [evaluation] · Verification: verified (Wikipedia + recall for Virtual Music details) · Cluster 08</small>

### `eck2002blues` — EckLSTM — Finding temporal structure in music: blues improvisation with LSTM

*Douglas Eck & Jürgen Schmidhuber, IDSIA; IEEE Workshop on Neural Networks for Signal Processing 2002 (and IDSIA tech report IDSIA-07-02).*

Links: https://people.idsia.ch/~juergen/blues/

First LSTM music generation: learns 12-bar blues chord progressions and melodies (piano-roll, quantised) and generates coherent long-range structure where earlier RNNs drifted.

**Evidence.** Qualitative; demonstrated LSTM keeps global form.

**For the studio.** Origin of neural symbolic generation; the *structure* problem it addressed remains the central problem for "compiling" full forms.

<small>Tags: [history] [symbolic-generation] [structure] · Verification: partial · Cluster 08</small>

### `nierhaus2009algorithmic` — CompositionScholarship — Algorithmic composition & music-representation scholarship

*Gerhard Nierhaus, *Algorithmic Composition: Paradigms of Automated Music Generation*, Springer 2009 (DOI 10.1007/978-3-211-75540-2). Roger B. Dannenberg, "Music Representation Issues, Techniques, and Systems," Computer Music Journal 17(3), 1993. Thor Magnusson, *Sonic Writing: Technologies of Material, Symbolic and Signal Inscriptions*, Bloomsbury 2019; also "Algorithms as Scores: Coding Live Music," Leonardo Music Journal 21, 2011. Curtis Roads, *The Computer Music Tutorial*, MIT Press 1996 (2nd ed. 2023).*

Links: https://link.springer.com/book/10.1007/978-3-211-75540-2

Nierhaus surveys Markov models, generative grammars, transition networks, chaos/self-similarity, genetic algorithms, cellular automata, neural networks and AI as compositional paradigms. Dannenberg lays out the representation problem — hierarchy, time, multiple simultaneous views, performance vs. score — that any musical IR must solve. Magnusson theorises notation, instruments and code as three inscription technologies and argues code is a new kind of score.

**Evidence.** Standard references.

**For the studio.** Dannenberg's issues list is a checklist for the studio's internal representation; Magnusson's "code as score" supplies the conceptual bridge from *compile* metaphor to compositional practice; Nierhaus catalogues what a rule-based "compiler backend" can do without ML.

<small>Tags: [music-as-code] [representation] [history] · Verification: Nierhaus verified (fetched); Dannenberg, Magnusson, Roads partial (well-known, not fetched) · Cluster 06</small>

### `koenig1970project` — KoenigProject — Project 1 (1964) and Project 2 (1966)

*Gottfried Michael Koenig, Institute of Sonology, Utrecht; 1964 and 1966.*

Links: (no stable primary URL fetched)

Serial/aleatoric composition programs: Project 1 produces a structured table of parameters (pitch, duration, register, dynamics, entry delays) from selection principles the composer sets; Project 2 exposes far more composer-specified constraints and a "score" of parameter-selection strategies. Output is a symbolic parameter list the composer then transcribes into notation.

**Evidence.** Historical.

**For the studio.** Early example of the composer *programming the generator's constraints* rather than the notes — the "composition as program" metaphor the founder uses.

<small>Tags: [history] [symbolic-generation] [music-as-code] · Verification: unverified (recall; dates widely cited) · Cluster 08</small>

### `xenakis1992formalized` — UPIC — Unité Polyagogique Informatique du CEMAMu (Xenakis)

*Iannis Xenakis, CEMAMu, Paris; completed 1977; first work *Mycènes Alpha* (1978). Stochastic-music theory in *Formalized Music* (1971, rev. 1992).*

Links: https://en.wikipedia.org/wiki/UPIC

A digitising tablet + computer on which the composer *draws* waveforms, envelopes and "arcs" (x = time, y = pitch) that are rendered directly to sound; drawings can be stretched, transposed, inverted, algorithmically transformed. Successors: IanniX (open-source), UPISketch (2018, macOS/iOS).

**Evidence.** Historical; adopted by Estrada, Risset, Mâche among others.

**For the studio.** The earliest realisation of *sketch as score*: drawing is the primary input and is directly executable. Directly relevant to the "scribble/sketch on the notation" annotation channel.

<small>Tags: [history] [sketch] [multimodal-input] [representation] · Verification: verified · Cluster 08</small>

### `hiller1959experimental` — IlliacSuite — Illiac Suite (String Quartet No. 4) and *Experimental Music: Composition with an Electronic Computer*

*Lejaren Hiller & Leonard Isaacson, University of Illinois Urbana-Champaign; work composed 1956–57 on ILLIAC I; book McGraw-Hill 1959.*

Links: https://en.wikipedia.org/wiki/Illiac_Suite

Generally credited as the first score composed by a computer. Four "experiments": (1) generation of cantus firmi, (2) four-voice writing under strict counterpoint rules (generate-and-test), (3) rhythm, dynamics and playing instructions, (4) Markov-chain (stochastic) generation. Output was symbolic (notes for string quartet) and then human-engraved and performed.

**Evidence.** Historical; no user study. Established the *rule-based generate-and-test* and *Markov* paradigms.

**For the studio.** The two paradigms of experiment 2 (constraint rules) and experiment 4 (probabilistic style) are exactly the two modes a "compiler" needs: hard constraints from the composer's annotations plus soft stylistic priors.

<small>Tags: [history] [symbolic-generation] [notation] · Verification: verified · Cluster 08</small>

### `boulangerlewandowski2012modeling` — RNNRBM — Modeling temporal dependencies in high-dimensional sequences: polyphonic music

*Nicolas Boulanger-Lewandowski, Yoshua Bengio, Pascal Vincent, Université de Montréal; ICML 2012.*

Links: https://icml.cc/2012/papers/590.pdf

RNN-RBM for polyphonic piano-roll prediction; introduced the four benchmark datasets (JSB Chorales, MuseData, Nottingham, Piano-midi.de) used for a decade.

**Evidence.** Log-likelihood benchmarks on those datasets; also improved polyphonic transcription.

**For the studio.** Anchors the modern symbolic-generation benchmark lineage; the datasets are small, clean and licence-friendly (JSB chorales) — still useful for unit-testing a harmony engine.

<small>Tags: [history] [symbolic-generation] [dataset] · Verification: partial · Cluster 08</small>

### `mcintyre1994bachinabox` — BachInABox — "Bach in a Box" and *Bach by Design*

*R. A. McIntyre, "Bach in a Box: The Evolution of Four Part Baroque Harmony Using the Genetic Algorithm", IEEE Conf. on Evolutionary Computation 1994; David Cope, *Bach by Design* (Centaur CD, 1994) — first commercial recording of EMI output.*

Links: https://doi.org/10.1109/ICEC.1994.350040

GA harmonises a given melody into four-part Baroque style using a rule-based fitness function (McIntyre). Cope's CD was the public debut of computer-composed Bach-style pieces.

**Evidence.** Small-scale; historically cited as an early GA harmonisation.

**For the studio.** Harmonise-my-melody is a core "compile" task; early rule-fitness approaches are still a useful baseline/constraint layer.

<small>Tags: [history] [symbolic-generation] [theory-analysis] · Verification: unverified (recall) · Cluster 08</small>

## F2. Interactive systems & accompaniment lineage

### `vercoe1984syntheticperformer` — Vercoe — Barry Vercoe: Csound and the Synthetic Performer

*Barry Vercoe; MIT Experimental Music Studio (est. 1973 after PDP-11 acquisition; he joined MIT 1971) → founding member of MIT Media Lab (1985); MUSIC 11 (1973), Csound (1985–86; LGPL); "The Synthetic Performer in the Context of Live Performance," ICMC 1984 (demonstrated at IRCAM 1984)*

Links: https://csound.com/ ; https://en.wikipedia.org/wiki/Barry_Vercoe

Csound is a text-based sound-compiler language (orchestra + score files) still in wide use — the literal ancestor of "music as code that gets compiled." The Synthetic Performer was an early real-time score-following accompanist that listened to a live flautist and adjusted tempo/expression — the first "AI accompanist" in this lineage. Students include Miller Puckette (Max/Pd) and Paris Smaragdis (now MIT MTC faculty).

**Evidence.** Historical; Csound in continuous development for ~40 years.

**For the studio.** Grounds the founder's "compile" metaphor historically (Csound's *orc/sco* compile model) and shows the real-time-accompaniment thread (Vercoe 1984 → ReaLchords 2024) is 40 years old at MIT.

<small>Tags: [history] [music-as-code] [accompaniment] [real-time] [toolkit] · Verification: partial (Wikipedia fetched; ICMC citation and Csound license from recall) · Cluster 01</small>

### `pachet2003continuator` — Continuator — The Continuator (Pachet) and Flow Machines

*François Pachet, Sony CSL Paris; "The Continuator: Musical Interaction with Style", *Journal of New Music Research* 32(3), 2003 (ICMC 2002 earlier). Flow Machines (ERC project 2012–17): *Daddy's Car* (2016), SKYGGE *Hello World* album (2018).*

Links: https://www.francoispachet.fr/continuator/ ; https://doi.org/10.1076/jnmr.32.3.333.16861

Learns a variable-order Markov model (prefix trees) of a player's MIDI phrases *in real time* and continues each phrase in that style when the player stops; can be biased by external constraints. Flow Machines generalised this to *Markov constraints* (style + hard constraints such as meter, harmony, positional) and lead-sheet generation (FlowComposer), producing the first commercially released "AI-assisted" pop songs.

**Evidence.** Addessi & Pachet studies with children (reflexive interaction increased engagement); Flow Machines outputs were human-arranged/produced.

**For the studio.** *Markov constraints* are the pre-deep-learning version of "generate in my style subject to my annotations"; FlowComposer's lead-sheet-first workflow is a direct ancestor of the symbolic-first studio.

<small>Tags: [history] [real-time] [symbolic-generation] [controllability] [accompaniment] · Verification: partial (site fetched; JNMR citation from recall) · Cluster 08</small>

### `lewis2000toomanynotes` — Voyager — George Lewis's *Voyager*

*George E. Lewis (trombonist/composer), begun 1987 (Forth on Atari/Mac); "Too Many Notes: Computers, Complexity and Culture in *Voyager*", *Leonardo Music Journal* 10, 2000.*

Links: https://doi.org/10.1162/096112100570585

A "virtual improvising orchestra": listens (pitch-to-MIDI) to a human improviser and generates multiple independent voices with their own behaviours; may respond, ignore, or initiate. Explicitly *not* an instrument the human controls — a player-paradigm partner rooted in Afrological improvisation aesthetics.

**Evidence.** Decades of performances/recordings (Voyager, 1993 CD); conceptual essay.

**For the studio.** The antithesis of "compile": an AI with its own agency. Useful as the far pole of the control axis and as a source of ideas for "player" agents that the composer can invite in but not fully script.

<small>Tags: [history] [real-time] [mixed-initiative] [co-creation-framework] · Verification: partial · Cluster 08</small>

### `assayag2006omax` — OMax — OMax / Somax2 (IRCAM)

*Gérard Assayag, Georges Bloch, Marc Chemillier, Shlomo Dubnov et al., IRCAM; OMax from 2004–06 (Factor Oracle); Somax (Bonnasse-Gahot 2014) → Somax2 (Borg, Assayag, 2020s, Max/MSP).*

Links: https://forum.ircam.fr/projects/detail/somax-2/ ; https://forum.ircam.fr/projects/detail/omax/

"Stylistic reinjection": learns a Factor Oracle over the live audio/MIDI stream and improvises by navigating and recombining the performer's own material; Somax2 adds reactive listening (harmonic/melodic influence from what the human plays now) and multi-agent co-improvisation.

**Evidence.** Extensive concert practice (Bernard Lubat, Steve Lehman etc.); design papers at ICMC/NIME/CMJ.

**For the studio.** Shows how an AI can work exclusively from *the composer's own material* (no external corpus) — an ethically clean approach to style; also a model for "recombine my sketches".

<small>Tags: [history] [real-time] [mixed-initiative] [accompaniment] · Verification: partial · Cluster 08</small>

### `biles1994genjam` — GenJam — Genetic Jammer

*John A. "Al" Biles, Rochester Institute of Technology; "GenJam: A Genetic Algorithm for Generating Jazz Solos", ICMC 1994; later interactive versions (1998–2000s).*

Links: https://igm.rit.edu/~jabics/GenJam.html

Genetic algorithm evolves populations of measure- and phrase-level jazz licks over a chord progression; the human "mentor" gives real-time good/bad feedback as fitness (interactive GA); later versions trade fours with the human and use autonomous fitness.

**Evidence.** Long-running performance practice ("Virtual Quintet"); famous for exposing the *fitness bottleneck* of human-in-the-loop evaluation.

**For the studio.** Early formalisation of *annotation as fitness*: the human's thumbs-up/down on generated material steers the system — the primitive form of the studio's annotate→regenerate loop.

<small>Tags: [history] [accompaniment] [mixed-initiative] [annotation] · Verification: partial · Cluster 08</small>

### `rowe1993interactive` — RoweIMS — *Interactive Music Systems: Machine Listening and Composing*

*Robert Rowe, NYU; MIT Press, 1993 (now free online).*

Links: https://wp.nyu.edu/robert_rowe/text/interactive-music-systems-1993/chapter-1-interactive-music-systems/

Defines interactive music systems as sensing→processing→response, and classifies them on three dimensions: (1) **score-driven** (match input against a stored score/fragments; uses beat/meter) vs **performance-driven** (no stored score; uses perceptual measures like density, regularity); (2) response method **transformative** (vary existing input material), **generative** (rules produce complete output from elementary seeds), **sequenced** (play back prerecorded fragments); (3) **instrument paradigm** (extends a human performer's gesture → solo-like) vs **player paradigm** (an artificial musician with its own personality → duet-like). Also introduces the *Cypher* system.

**Evidence.** Conceptual; became the standard vocabulary in NIME/ICMC.

**For the studio.** Provides a ready-made axis set for the project's taxonomy. The founder's loop is score-driven + transformative, instrument paradigm, with the AI as "compiler"; accompaniment agents would be player-paradigm.

<small>Tags: [history] [co-creation-framework] [real-time] [accompaniment] · Verification: verified · Cluster 08</small>

### `dannenberg1984online` — Dannenberg1984 — An On-Line Algorithm for Real-Time Accompaniment

*Roger B. Dannenberg, CMU, "An On-Line Algorithm for Real-Time Accompaniment", ICMC 1984; Barry Vercoe, MIT Media Lab/IRCAM, "The Synthetic Performer in the Context of Live Performance", ICMC 1984 (with Puckette 1985 follow-up).*

Links: https://www.cs.cmu.edu/~rbd/bib.html (bibliography); PDF via https://www.cs.cmu.edu/~rbd/papers/

Score following: dynamic-programming alignment of a live monophonic performance to a stored score, driving synchronised accompaniment (Dannenberg); Vercoe's system tracked a flautist via pitch + fingering sensors and learned tempo tendencies across rehearsals. Later: polyphonic following (1985), stochastic vocal tracking (Grubb & Dannenberg 1997), *Music Score Alignment and Computer Accompaniment* (CACM 2006, with Raphael), Human-Computer Music Performance (2011–14).

**Evidence.** Engineering demonstrations; CACM 2006 is the standard review.

**For the studio.** Score-driven interaction is the studio's native mode; score following is the technology that would let the composer *hum or play* against the compiled score and have the AI stay aligned.

<small>Tags: [history] [accompaniment] [real-time] [transcription] · Verification: verified (author bibliography) · Clusters 02, 08</small>

### `machover1992hyperinstruments` — Hyperinstruments — Hyperinstruments / Opera of the Future (Tod Machover)

*Tod Machover, MIT Media Lab (Professor of Music and Media; group founded at the Lab's start, hyperinstruments from 1986); "Hyperinstruments: A Progress Report 1987–1991" (MIT Media Lab, 1992); Brain Opera 1996; Toy Symphony 2002–03; City Symphonies 2012–*

Links: https://www.media.mit.edu/groups/opera-of-the-future/overview/ ; https://en.wikipedia.org/wiki/Tod_Machover

Sensor-augmented instruments that let performer gesture shape sound beyond the acoustic instrument (Hypercello for Yo-Yo Ma, *Begin Again Again…* 1991; Hyperviolin), then "hyperinstruments for non-professionals" (Brain Opera) and composition tools for children (Hyperscore). Machover's stated goal: "making every human being into a musician." Huang (SM 2008) and Egozy (SM 1995) both came through the Media Lab in this orbit; Kimaya Lecamwasam (jam_bot co-author) is a current Opera of the Future PhD student collaborating with HAI-Res.

**Evidence.** Decades of premieres; no controlled studies.

**For the studio.** Establishes the MIT stance that technology should *expand* human expression (hyper-), not substitute for it — the institutional ancestor of Huang's "interaction, not imitation."

<small>Tags: [history] [expression-performance] [creativity-support] [real-time] · Verification: partial (Wikipedia fetched; report citation from recall) · Cluster 01</small>

## F3. Commercial auto-accompaniment & notation lineage

### `makemusic2024finale` — Finale sunset → Dorico / Sibelius — commercial notation landscape 2024–2026

*Finale (Coda/MakeMusic, 1988; **discontinued 26 Aug 2024**, support ended 26 Aug 2025); Encore (Passport Designs, 1990); Sibelius (Finn brothers, Acorn 1993 → Windows/Mac 1998; Avid since 2006); Dorico (Steinberg, 2016); MuseScore (2002, Muse Group). Sequencers: Cakewalk (Twelve Tone Systems, 1987 DOS), Cubase (Steinberg, Atari ST 1989), Logic (C-Lab Notator 1988 → Emagic Logic → Apple 2002).*

Links: https://www.makemusic.com/press-room/press-releases-2024/makemusic-sunsets-finale/ ; https://blog.dorico.com/2026/03/dorico-6-2-update-released/

MakeMusic ended Finale development and sales (no further updates to Finale, PrintMusic, Songwriter, Notepad), citing "millions of lines of code" and OS churn; support through 26 Aug 2025; partnered with Steinberg to offer Dorico Pro at $149 (list $579). Dorico 6.x continues rapid iteration (6.2: repeat-barline cautionaries, European tab styles, harmonics popover, >70 fixes; Pro/Elements/SE/iPad). Sibelius remains (Ultimate/Artist/First, cloud sharing) — not re-verified here.

**Evidence.** Verified by MakeMusic press release; Scoring Notes coverage.

**For the studio.** Shows the fragility of closed monoliths and the market gap (Finale users displaced); MusicXML export from Dorico/Sibelius is the interchange path; the studio should target MusicXML (and MEI) import robustly.

<small>Tags: [product] [notation] [history] · Verification: verified · Clusters 07, 08</small>

### `korg1993i3` — Arranger keyboards — Korg i3 (1993) and the "style" paradigm (Yamaha Genos, Korg Pa)

*Korg i3 "Interactive Music Workstation", 1993 (Japan); lineage i2/i4S/i5S → i30/iS series (1998) → Pa-series (2001–, Pa5X 2022); Yamaha PSR → Tyros → Genos (2017) / Genos2 (2023); Roland G-800/E-series; Korg reused the "i3" name in 2020*

Links: https://en.wikipedia.org/wiki/Korg_i3 ; https://www.korg.com/us/products/synthesizers/i3/ ; https://www.muzines.co.uk/articles/korg-i3/7651

The i3 established the "pro arranger" category: 48 styles × (4 variations, 2 fills, 2 intros/endings), chord recognition from the left hand driving multi-part accompaniment (drums, bass, 3–4 accompaniment parts), AI² synthesis (32 voices, 340 programs), 16-track GM sequencer plus a "Backing Sequencer" that records the style performance into an editable song. Modern arrangers (Genos2, Pa5X) add hundreds of styles, style-creator editors, chord-sequencer, audio styles, and MIDI implementations exposing style parts on fixed channels.

**Evidence.** Wikipedia/Music Technology Nov 1993 review; $2,500 launch price; "inspired Roland G-800 and Yamaha PSR variants."

**For the studio.** The founder's formative instrument is literally a rule-based "compile" engine: human chords + a parameterised style → arrangement, then editable in a sequencer. The studio can be framed as the learned, annotation-steered successor, keeping the arranger's virtues (instant, deterministic, editable) and fixing its genericness.

<small>Tags: [history] [accompaniment] [product] [real-time] · Verification: verified (Wikipedia); Genos/Pa details partial · Cluster 07</small>

### `pgmusic1990bandinabox` — BandInABox — Band-in-a-Box and the arranger-keyboard lineage

*PG Music (Peter Gannon), Victoria BC; first release 1990 (PC, Atari ST); Soloist 1997; RealDrums 2006; RealTracks + Audio Chord Wizard 2007; annual releases continue (BiaB 2026). Arranger keyboards: Korg i3 (1993, first Korg "interactive" workstation), Yamaha PSR series (1980s→), Korg Pa series (Pa80 2000 → Pa5X 2022).*

Links: https://en.wikipedia.org/wiki/Band-in-a-Box ; https://www.pgmusic.com

Type chords into a bar grid, pick key/tempo/style → the program generates a full band arrangement (originally MIDI styles; since 2007 "RealTracks" = recorded human phrases spliced to fit chords). Melodist/Soloist generate melodies/solos; Audio Chord Wizard transcribes chords from audio. Arranger keyboards do the same in hardware in real time from left-hand chords, with style/variation/fill/intro/ending buttons.

**Evidence.** 35 years of continuous commercial existence; huge hobbyist base.

**For the studio.** This *is* the "compile a lead sheet" paradigm in its commercial form (the founder grew up on a Korg i3). Its limits define the opportunity: no multimodal annotation, coarse style vocabularies, weak editability of generated parts, MIDI/audio not notation-first.

<small>Tags: [history] [product] [accompaniment] [symbolic-generation] · Verification: verified (BiaB) / partial (keyboards) · Cluster 08</small>

## F4. Theories of co-creativity & creativity support

### `kantosalo2016modes` — Kantosalo2016 — Modes for Creative Human-Computer Collaboration: Alternating and Task-Divided Co-Creativity

*Anna Kantosalo & Hannu Toivonen, University of Helsinki; ICCC 2016; extended in Kantosalo's 2019 PhD and "Human–computer co-creativity: designing, evaluating and modelling" work.*

Links: https://researchportal.helsinki.fi/en/publications/modes-for-creative-human-computer-collaboration-alternating-and-t/ ; PDF via computationalcreativity.net/iccc2016

Using Wiggins' creativity-as-search formalism, distinguishes *alternating co-creativity* (turn-taking on the same artefact) from *task-divided co-creativity* (human and computer own different sub-tasks, working in parallel), and analyses what the computational agent must be able to do in each.

**Evidence.** School studies (children writing poetry) with qualitative + questionnaire data.

**For the studio.** The compile loop is *both*: alternating at the notation level (compose → compile → edit) and task-divided at the arrangement level (human writes lead sheet, AI voices/orchestrates). Naming the mode per feature clarifies the interaction design.

<small>Tags: [co-creation-framework] [mixed-initiative] [evaluation] · Verification: verified (fetched Helsinki research-portal record) · Clusters 05, 08</small>

### `shneiderman2007cst` — CST2007 — Creativity Support Tools: Accelerating Discovery and Innovation

*Ben Shneiderman, University of Maryland; Communications of the ACM 50(12):20–32, 2007*

Links: https://doi.org/10.1145/1323688.1323689

Agenda-setting essay defining creativity support tools (CSTs) and principles for designing them: support exploratory search, enable collaboration, provide rich history-keeping (undo, versioning, replay), design with low thresholds/high ceilings/wide walls, and support many paths and many styles. Argues CST research needs new evaluation methods (long-term case studies rather than short lab tasks).

**Evidence.** Position/essay; synthesises the 2005 NSF workshop on CSTs.

**For the studio.** "Rich history-keeping" and "many paths/styles" are exactly the version-tree / annotation-history features a compile-loop needs; also legitimises longitudinal case-study evaluation of a composer's tool.

<small>Tags: [creativity-support] [co-creation-framework] [evaluation] · Verification: verified (Crossref metadata) · Cluster 05</small>

### `shneiderman2020hcai` — HCAI — Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy (and the 2022 book)

*Ben Shneiderman, University of Maryland; International Journal of Human–Computer Interaction 36(6):495–504, 2020; book *Human-Centered AI*, Oxford University Press, 2022*

Links: https://doi.org/10.1080/10447318.2020.1741118

Proposes a two-dimensional framework (human control × computer automation) replacing the one-dimensional "more automation = less control" view; argues for designs with *high* human control *and* high automation, with "supertools" and "active appliances" rather than autonomous agents; emphasises reliable, safe, trustworthy systems via audit trails, explainability and human oversight.

**Evidence.** Conceptual framework; the book expands it with design patterns and governance structures.

**For the studio.** Gives the founder's "human is the center; AI is the compiler" thesis a citable HCI grounding: high automation (compile arrangements) and high human control (notation editing, annotations) are not a trade-off.

<small>Tags: [co-creation-framework] [creativity-support] · Verification: verified (Crossref metadata) · Cluster 05</small>

### `le2025nlpsurvey` — LeSurvey — Natural Language Processing Methods for Symbolic Music Generation and Information Retrieval: a Survey

*Dinh-Viet-Toan Le, Louis Bigo, Mikaela Keller, Dorien Herremans (Univ. Lille / CNRS / SUTD); ACM Computing Surveys 2025 (arXiv Feb 2024)*

Links: https://arxiv.org/abs/2402.17467 ; https://dl.acm.org/doi/10.1145/3714457

Systematic survey organised along two axes — *representations* (time-slice vs event-based tokenization; elementary vs composite tokens) and *models* (RNNs, Transformers, pre-trained BERT/GPT variants) — covering both generation and MIR. Discusses data-scale disparity (billions of text tokens vs millions of music tokens), polyphony/simultaneity, and the epistemological limits of the music-as-language analogy. Note: the brief's title "A Survey on Deep Learning for Symbolic Music Generation and Information Retrieval" refers to this paper.

**Evidence.** Survey (no experiments); advocates lighter models, explainability, standard benchmarks.

**For the studio.** The best single map of tokenization choices and their trade-offs — the reference to consult when designing the studio's internal symbolic format.

<small>Tags: [representation] [symbolic-generation] [evaluation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `rezwana2022perceptions` — CreativePenpal — Understanding User Perceptions, Collaborative Experience and User Engagement in Different Human-AI Interaction Designs for Co-Creative Systems

*Jeba Rezwana, Mary Lou Maher; UNC Charlotte; ACM Creativity & Cognition 2022, pp. 38–48*

Links: https://doi.org/10.1145/3527927.3532789

Compares two versions of a co-creative sketching system ("Creative Penpal"): one where the AI only contributes sketches, and one where it also *communicates* (speech/text about its intentions and reactions).

**Evidence.** Between-subjects user study; the communicating version was perceived as more collaborative, engaging and partner-like, with higher perceived reliability, though some users found it intrusive.

**For the studio.** Direct evidence for adding AI→human commentary to the compile step (e.g., "I re-voiced the piano because your annotation asked for a Foster-style ballad").

<small>Tags: [HCI-study] [co-creation-framework] [mixed-initiative] · Verification: partial (Crossref metadata fetched; findings from recall) · Cluster 05</small>

### `rezwana2023cofi` — COFI — Designing Creative AI Partners with COFI: A Framework for Modeling Interaction in Human-AI Co-Creative Systems

*Jeba Rezwana, Mary Lou Maher; UNC Charlotte; ACM Transactions on Computer-Human Interaction 30(5), 2023 (arXiv 2022)*

Links: https://doi.org/10.1145/3519026 ; https://arxiv.org/abs/2204.07666

The Co-Creative Framework for Interaction design (COFI) decomposes co-creative interaction into *collaboration* dimensions (participation style: alternating/parallel; timing: spontaneous/planned; task distribution; contribution type; creative process) and *communication* dimensions (human→AI: direct manipulation, embodied, intentional; AI→human: task-related and non-task-related communication).

**Evidence.** Coded 92 existing co-creative systems; found the field concentrates on AI generative ability and almost entirely lacks AI→human communication (explanations, intentions, confidence), which the authors argue is what makes AI a *partner* rather than a tool.

**For the studio.** The best available vocabulary for specifying the studio's interaction design; suggests the compiler should *talk back* (annotate what it changed and why) — the mirror image of the composer's annotations.

<small>Tags: [co-creation-framework] [mixed-initiative] [evaluation] · Verification: verified (fetched arXiv abstract) · Cluster 05</small>

### `guzdial2019friend` — MoraiMaker — Friend, Collaborator, Student, Manager: How Design of an AI-Driven Game Level Editor Affects Creators

*Matthew Guzdial, Nicholas Liao, Jonathan Chen, Shao-Yu Chen, Shukan Shah, Vishwa Shah, Joshua Reno, Gillian Smith, Mark O. Riedl; Georgia Tech, WPI; CHI 2019*

Links: https://arxiv.org/abs/1901.06417 ; https://doi.org/10.1145/3290605.3300854 ; companion framework paper https://arxiv.org/abs/1903.09709

Morai Maker is a *turn-based* co-creative level editor for Super Mario-style games: the human edits, then the AI takes a turn adding content, and so on. Compares three AI agents (Markov chain, Bayes net, LSTM) and how designers frame the AI's role.

**Evidence.** Two mixed-methods studies, >100 participants total (91 in the controlled study). Designers split by preferred AI role — friend, collaborator, student or manager — and the AI changed how they designed; the same agent was rated helpful or annoying depending on the role a designer wanted.

**For the studio.** Strong evidence that role preference is *individual* and that turn-taking must be interruptible; the studio should let the composer set how much initiative the compiler takes.

<small>Tags: [mixed-initiative] [game] [HCI-study] [co-creation-framework] · Verification: verified (fetched arXiv abstract page) · Cluster 05</small>

### `davis2016drawingapprentice` — DrawingApprentice — Empirically Studying Participatory Sense-Making in Abstract Drawing with a Co-Creative Cognitive Agent

*Nicholas Davis, Chih-Pin Hsiao, Kunwar Yashraj Singh, Lisa Li, Brian Magerko; Georgia Tech; IUI 2016 (plus "Quantifying Collaboration with a Co-Creative Drawing Agent," ACM TiiS 2017)*

Links: https://doi.org/10.1145/2856767.2856795 ; https://doi.org/10.1145/3009981 ; http://mici.codingconduct.cc/drawing-apprentice/

Drawing Apprentice is a real-time co-creative drawing partner that responds to the user's strokes with its own, alternating on a shared canvas; the papers introduce *participatory sense-making* and the "creative sense-making" framework for analysing turn-by-turn co-creation, later formalised as Observable Creative Sense-Making (C&C 2023).

**Evidence.** IUI 2016 study compared the agent to a Wizard-of-Oz human; users often could not distinguish them, and enjoyment/collaboration ratings were comparable; TiiS 2017 quantifies collaboration behaviours.

**For the studio.** The canonical non-music example of *simultaneous* (rather than turn-taking) co-creation; its sense-making coding scheme is reusable for analysing composer–AI sessions.

<small>Tags: [co-creation-framework] [HCI-study] [real-time] [evaluation] · Verification: partial (venue/DOI from search results and ACM listing; PDF not fetched) · Cluster 05</small>

### `wan2024secondmind` — SecondMind — "It Felt Like Having a Second Mind": Investigating Human-AI Co-creativity in Prewriting with Large Language Models

*Qian Wan, Siying Hu, Yu Zhang, Piaohong Wang, Bo Wen, Zhicong Lu; City University of Hong Kong; PACM HCI 8 (CSCW1), 2024 (arXiv 2023)*

Links: https://arxiv.org/abs/2307.10811 ; https://doi.org/10.1145/3637361

Qualitative study of how people co-create with GPT-3 during prewriting (story and slogan tasks); proposes a three-stage iterative co-creativity model — Ideation (LLM-led), Illumination (human-led, LLM organises), Implementation (human-led, LLM enriches details) — with humans holding initiative except when blocked.

**Evidence.** N=15 creativity-major students, three sessions each (scenario ideation, think-aloud, interviews), constructivist grounded theory.

**For the studio.** A general-purpose model of *who leads when* in LLM co-creation that transfers to compose/annotate/compile; supports designing the compiler to take initiative mainly at ideation/blockage points.

<small>Tags: [HCI-study] [co-creation-framework] [LLM-agent] · Verification: verified (fetched arXiv abstract page) · Cluster 05</small>

### `fiebrink2018mlcreativetool` — MLasTool — The Machine Learning Algorithm as Creative Musical Tool (and Wekinator)

*Rebecca Fiebrink, Baptiste Caramiaux; Goldsmiths / IRCAM; chapter in *The Oxford Handbook of Algorithmic Music*, 2018 (arXiv 2016); Wekinator: Fiebrink, Trueman, Cook, "A Meta-Instrument for Interactive, On-the-Fly Machine Learning," NIME 2009*

Links: https://arxiv.org/abs/1611.00379 ; http://www.wekinator.org

Argues that ML algorithms should be understood as *interfaces* whose affordances intersect with musicians' goals — supervised learning by demonstration lets a musician teach an idiosyncratic mapping in minutes and then "break the rules." Wekinator operationalises this: record a few gesture→sound examples, train, play, correct, retrain (interactive machine learning).

**Evidence.** Years of workshops and studies with composers/performers (Fiebrink's PhD, 2011) showing fast iteration and example-based specification outperform parameter tweaking for non-programmers.

**For the studio.** The founding case for *example-based* steering ("here is a hummed phrase / an audio clip; make it like this") and for tight train–test–correct loops — the interactive-ML lineage the compile loop belongs to.

<small>Tags: [co-creation-framework] [expression-performance] [real-time] [HCI-study] · Verification: verified (fetched arXiv abstract) · Cluster 05</small>

### `deterding2017mici` — MICI — Mixed-Initiative Creative Interfaces

*Sebastian Deterding, Jonathan Hook, Rebecca Fiebrink, Marco Gillies, Jeremy Gow, Memo Akten, Gillian Smith, Antonios Liapis, Kate Compton; York, Goldsmiths, WPI, Malta, UCSC; CHI 2017 Extended Abstracts (workshop)*

Links: https://doi.org/10.1145/3027063.3027072 ; workshop proceedings https://ceur-ws.org/Vol-1907/

Defines mixed-initiative creative interfaces as systems where human and computer take turns constraining, suggesting and evaluating in a tight loop, sitting between human-driven creativity tools and autonomous computational creativity. Names open challenges: letting non-programmers express formal constraints, legibility of AI decisions, fatigue, evaluation of co-creativity, up-skilling vs de-skilling.

**Evidence.** Workshop proposal; the CEUR proceedings collect ~20 position papers.

**For the studio.** Annotations are precisely a way for non-programmers to "express constraints"; the paper's questions (legibility, fatigue, evaluation) are the studio's research questions.

<small>Tags: [mixed-initiative] [co-creation-framework] [creativity-support] · Verification: verified (fetched White Rose eprint PDF) · Cluster 05</small>

### `ji2023survey` — JiSurvey — A Survey on Deep Learning for Symbolic Music Generation: Representations, Algorithms, Evaluations, and Challenges

*Shulei Ji, Xinyu Yang, Jing Luo (Xi'an Jiaotong University); ACM Computing Surveys 2023 (updates the 2020 arXiv survey "A Comprehensive Survey on Deep Music Generation", arXiv 2011.06801)*

Links: https://dl.acm.org/doi/10.1145/3597493 ; https://arxiv.org/abs/2011.06801 (2020 version)

Taxonomy of symbolic generation by representation (piano-roll, event, text, graph), by algorithm (VAE, GAN, Transformer, diffusion, RL) and by task (melody, polyphony, accompaniment, arrangement, style transfer), with a section on evaluation metrics and open challenges (structure, controllability, interaction).

**Evidence.** Survey; catalogues metrics and datasets.

**For the studio.** Complementary to Le et al.; its task taxonomy (melody→harmony→arrangement→performance) is a useful scaffold for the studio's literature review.

<small>Tags: [symbolic-generation] [evaluation] [representation] · Verification: partial (ACM DL blocked; located via search; 2020 arXiv version known) · Cluster 03</small>

### `lubart2005partners` — Lubart2005 — How can computers be partners in the creative process: Classification and commentary on the Special Issue

*Todd Lubart; Université Paris Descartes; International Journal of Human-Computer Studies 63(4–5):365–369, 2005*

Links: https://doi.org/10.1016/j.ijhcs.2005.04.002 ; PDF: http://www.cs.tufts.edu/~jacob/250aui/creativity-hci.pdf

Classifies computers' roles in creative work as *nanny* (manages the process, time, breaks), *pen-pal* (mediates human collaboration), *coach* (teaches creativity techniques), and *colleague* (generates alternatives that the human evaluates and refines).

**Evidence.** Commentary on a special issue; no study.

**For the studio.** Still the most-cited vocabulary for "what role does the AI play"; the studio's compiler is a colleague for arrangement but could be a coach (theory hints) and nanny (session/version management) too.

<small>Tags: [co-creation-framework] [creativity-support] · Verification: verified (fetched PDF) · Cluster 05</small>

### `ma2024foundation` — FM4Music — Foundation Models for Music: A Survey

*Yinghao Ma, Anders Øland, Anton Ragni, et al. (40+ authors incl. Chris Donahue, Roger Dannenberg, Shuqi Dai, Shih-Lun Wu); QMUL-led. arXiv 2024.*

Links: https://github.com/nicolaus625/FM4Music ; PDF: https://gclef-cmu.org/static/pdfs/2024mafoundation.pdf

Broad survey of music foundation models (representations, pretraining, adaptation, evaluation, ethics), with both CMU generations as co-authors.

**For the studio.** Background reading; taxonomy source for the audio/representation side.

<small>Tags: [representation] [evaluation] [ethics-legal] · Verification: partial (lab page listing; arXiv id from recall) · Cluster 02</small>

## F5. Human-centered music-AI programmes & design spaces

### `cmu2025musictech` — CMU-Other — Other CMU music/creativity pointers (brief)

*CMU School of Music "Music & Technology" programme (BS/MS; faculty incl. Richard Randall, Jesse Stiles; historical thesis projects incl. Zeyu Jin's "Formal Semantics for Music Notation Control Flow" → Live Score Display); HCII (Lindlbauer, Forlizzi/Holstein) — music-specific work found only via Alexander Wang's papers with Donahue; Bhiksha Raj's group — no music-generation or music-editing system located in this pass (co-author with Dannenberg on "Artificial Creative Intelligence: Breaking the Imitation Barrier", ICCC 2020); Dannenberg's current project list (Spring 2025): O2, AMADS symbolic-music-analysis library, Arco, Accomplice (keyboard accompaniment), Soundcool web port, "Computer Music Archeology", "Music Patterns and Music Models".*

Links: https://www.cmu.edu/cfa/music/programs/music-technology/ ; https://www.cs.cmu.edu/~rbd/projects-spring2025.html

Institutional context; AMADS (analysis algorithms for key, contour, chord labelling) and Accomplice are the live Dannenberg-side codebases.

**For the studio.** Identifies which CMU groups actually do music (G-CLef, Dannenberg/Dai lineage, WAVLab for singing) and which the founder can skip.

<small>Tags: [history] [toolkit] [theory-analysis] · Verification: partial (pages fetched; Raj/HCII negative result from limited search) · Cluster 02</small>

### `huang2025creativityinteraction` — HuangPhilosophy — Anna Huang's articulated philosophy of human-AI co-creation (talks, bios, course)

*Cheng-Zhi Anna Huang; MIT (2024–2026): GenAI Summit 2025 (UCSD) talk "Creativity through Interaction"; MIT Spectrum Spring 2025; MIT News June 2026; course 21M.369 (Fall 2024) → 21M.386 "Algorithms and Interactions for Human-AI Music Making"*

Links: https://genaisummit2025.ucsd.edu/schedule/anna-huang ; https://betterworld.mit.edu/spectrum/issues/spring-2025/music-and-technology-intertwined ; https://news.mit.edu/2026/inaugural-mit-music-technology-research-showcase-celebrates-work-students-0629 ; https://musictech.mit.edu/21m369fa24/ ; https://czhuang.github.io/

Verbatim statements of position. GenAI Summit abstract: "How can we elicit creativity not through imitation but through interaction? … Coconet … supports a nonlinear compositional process through an iterative block-Gibbs like generative procedure, while MIDI-DDSP supports intuitive user control in performance synthesis through hierarchical modeling. … I'm interested in designing visualizations and interactions that can help musicians understand and steer system behavior, and algorithms that can learn from their feedback in more organic ways. I aim to build systems that musicians can shape, negotiate, and jam with in their creative practice." Spectrum: "I'm interested in thinking about creativity not through imitation, but as a collaborative process where creative ideas emerge through human-AI interaction"; "We also teach machines to listen, so that they can jam with other musicians and respond to what they're playing." MIT News 2026: "We work with these musicians, we go into the studio, and every week we try something. The technology grows with the creative process." Homepage: neural networks "as a lens onto music, and a mirror onto our own understanding of music"; goal of designing "interactive systems and visualizations" so artists can "understand and steer" AI. Course 21M.369/386 surveys generative modeling, learning from human feedback, RL/social RL, and "abstractions that empower human-AI collaboration."

**Evidence.** Primary pages fetched.

**For the studio.** These are quotable anchors for the studio's manifesto: interaction over imitation, steer + understand, nonlinear composition, co-design in the studio week by week.

<small>Tags: [co-creation-framework] [creativity-support] [history] · Verification: verified · Cluster 01</small>

### `gclef2026lab` — G-CLef — Generative Creativity Lab (G-CLef) @ CMU

*Chris Donahue (PI, Dannenberg Assistant Professor, CMU CSD; part-time Research Scientist, Google DeepMind Magenta). PhD students: Wayne Chi, Irmak Bukey, Yewon Kim, Nathan Pruyne (CSD), Alexander Wang (HCII). MS: Satvik Dixit (ECE), Lynn Ye (Music & Technology). Alumni: Shih-Lun Wu (now MIT PhD), Xun Zhou, Yichen Huang. Founded 2023 when Donahue joined CMU after a Stanford postdoc (Percy Liang) and UCSD PhD (Puckette, McAuley).*

Links: https://gclef-cmu.org/ ; https://gclef-cmu.org/research ; https://gclef-cmu.org/team ; https://chrisdonahue.com/publication/

Lab mission "empower and enrich human creativity and productivity with generative AI", centred on music with side-lines in code LLM evaluation (Copilot Arena, ICML 2025) and agents. Publications 2023–2026 (lab page): SingSong (arXiv 2023); Anticipatory Music Transformer (TMLR 2024); Music ControlNet (TASLP 2024); ReaLchords (ICML 2024); V2Meow (AAAI 2024); Foundation Models for Music survey (arXiv 2024); Towards Music-Aware Virtual Assistants (UIST 2024); Do Music Generation Models Encode Music Theory? (ISMIR 2024); Just Label the Repeats (ISMIR 2024); Hookpad Aria (ISMIR LBD 2024); MIDInfinite/local deployment (ISMIR LBD 2024); Amuse (CHI 2025, Best Paper); Copilot Arena (ICML 2025); Aligning Text-to-Music Evaluation with Human Preferences (ISMIR 2025); Music Arena (NeurIPS 2025 Creative AI track); Live Music Models / Magenta RealTime (arXiv 2025); RISE (ISMIR 2025); Unified Cross-modal Translation (TASLP 2025, with Sogang); A Design Space for Live Music Agents (CHI 2026); MultiVerse (UIST 2026); Decomposer (preprint 2026). Jan 2026 news: two ICASSP 2026 papers (FoleyBench, music captioning), EDIT-Bench (ICLR 2026 oral), Schmidt HAVI grant for a multimodal music-AI project co-led with Annie Hsieh.

**For the studio.** The single most aligned academic group: symbolic-first, deployed-with-real-musicians (Hookpad Aria), multimodal inspiration (Amuse), and now programs-as-representation (Decomposer). Natural collaboration / hiring pool; their public PDFs are all at gclef-cmu.org/static/pdfs/.

<small>Tags: [co-creation-framework] [symbolic-generation] [evaluation] [HCI-study] [history] · Verification: verified (fetched lab pages and chrisdonahue.com) · Cluster 02</small>

### `mit2026mtcshowcase` — MITMTC — MIT Music Technology and Computation Graduate Program & HAI-Res lab

*MIT Music & Theater Arts (SHASS) + School of Engineering + Schwarzman College of Computing; director Eran Egozy; faculty Anna Huang, Mark Rau, Paris Smaragdis, Grisha Coleman, Ian Hattwick; launched Fall 2024 (SM for MIT undergrads from Fall 2025; open admission from Fall 2026; MASc also offered); first showcase 13 May 2026, Linde Music Building*

Links: https://musictech.mit.edu/ ; https://musictech.mit.edu/mtcgp/ ; https://news.mit.edu/2026/inaugural-mit-music-technology-research-showcase-celebrates-work-students-0629 ; https://risingstars-eecs.mit.edu/speakers/anna-huang

New graduate program (SM/MASc; EECS PhD track via affiliated faculty) with dedicated labs in the Edward and Joyce Linde Music Building. Huang's **Human-AI Resonance (HAI-Res)** group at CSAIL "co-design[s] with musicians new algorithms and interactions for Human-AI partnerships." Showcase projects: Rachel Loh, "Visualizing the Internal State of Music Models for Live Human-AI Improvisation"; Nithya Shikarpur, live Hindustani voice + generative models + loops; Brade/Kim/Chen, "Whale, Cello (there?)" (cello vs real-time diffusion model trained on whale song); Zhixing Chen, generative music from dance circles; Claire Southard, EEG decoding of imagined music; Salcedo, neural cellular automata visuals. 10 students admitted for 2026–27 from 100+ applicants.

**Evidence.** Institutional reporting; first cohort of five.

**For the studio.** The nearest academic community to the studio's thesis (Boston/Cambridge), a pipeline of open real-time co-creation prototypes, and a venue for co-design partnerships and evaluation.

<small>Tags: [education] [co-creation-framework] [real-time] [history] · Verification: verified · Cluster 01</small>

### `kim2026designspace` — LiveAgentsDesignSpace — A Design Space for Live Music Agents

*Yewon Kim, Stephen Brade, Alexander Wang, David Zhou, Haven Kim, Bill Wang, Sung-Ju Lee, Hugo F. Flores García, Cheng-Zhi Anna Huang, Chris Donahue; CMU / MIT / UIUC / UCSD / KAIST / Northwestern; ACM CHI 2026 (arXiv 2602.05064)*

Links: https://arxiv.org/abs/2602.05064 ; https://doi.org/10.1145/3772318.3791291 ; https://live-music-agents.github.io

Systematic review of 184 live-music-agent systems (153 papers from HCI/AI/computer-music venues + 31 videos; 731 papers screened; 89.8% inter-annotator agreement) yielding a design space of 31 dimensions / 165 codes in four aspects: Usage Context (user role, agent role, topology…), Interaction (I/O modality, planning, temporal structure, control mode/scope, system initiative, agency framing tool/partner/hybrid), Technology (model class, learning, adaptation, latency emphasis, integration), Ecosystem (authorship, economic, cultural).

**Evidence.** Only ~5% of systems discuss ecosystem/policy; trend from reactive accompanists to proactive partners; control vs novelty and coherence vs diversity trade-offs.

**For the studio.** Ready-made taxonomy of interaction dimensions to reuse in the studio's own taxonomy (esp. the real-time/accompaniment corner); the database is a citation source.

<small>Tags: [co-creation-framework] [real-time] [evaluation] [mixed-initiative] · Verification: verified (arXiv HTML fetched) · Clusters 01, 02</small>

## S1.1. Compose: performance capture & transcription

### `riosvila2024smt` — SMT-OMR — Sheet Music Transformer (end-to-end polyphonic OMR), with oemer and Audiveris

*Antonio Ríos-Vila, Jorge Calvo-Zaragoza (U. Alicante), Thierry Paquet (U. Rouen); ICDAR 2024 (arXiv Feb 2024); SMT++ full-page (arXiv May 2024). oemer: BreezeWhite (MIT licence). Audiveris: Hervé Bitteur et al. (AGPL-3.0, v5.5+).*

Links: https://arxiv.org/abs/2402.07596 ; https://github.com/antoniorv6/SMT ; https://github.com/BreezeWhite/oemer ; https://github.com/Audiveris/audiveris

SMT: image-to-sequence Transformer that transcribes *polyphonic* (pianoform, quartet) score images directly to Humdrum **kern, chosen for its simple, parseable vocabulary. oemer: UNet segmentation + SVM classifiers → MusicXML from phone photos. Audiveris: classical pipeline with an interactive **OMR editor** to correct errors before MusicXML 4.0 export.

**Evidence.** SMT on GrandStaff (53,882 images) and new Quartets set (38,051): SMT_NexT cut Character Error Rate by 91.8% and Line Error Rate by 89.1% vs baselines.

**For the studio.** OMR is how a composer's *paper* or handwritten sketch (photographed) enters the symbolic model; **kern as the OMR target aligns with the LLM-friendly text IR idea; Audiveris's correction-first UI is the right workflow for imperfect recognition.

<small>Tags: [transcription] [notation] [sketch] [toolkit] · Verification: verified (fetched primary sources) · Cluster 06</small>

### `donahue2022sheetsage` — SheetSage — Melody Transcription via Generative Pre-training

*Chris Donahue, John Thickstun, Percy Liang; Stanford; ISMIR 2022 ("Melody transcription via generative pre-training")*

Links: https://arxiv.org/abs/2212.01884 ; code+dataset: https://github.com/chrisdonahue/sheetsage ; examples: https://chrisdonahue.com/sheetsage

Uses Jukebox's pretrained audio representations as features for a melody transcriber; a new 50-hour crowd-sourced melody dataset over broad-genre music. Sheet Sage composes melody transcription with beat tracking, key and chord estimation to output a *lead sheet* (melody + chords) from arbitrary audio. Input: audio file/URL; output: LilyPond/MusicXML-style lead sheet. No interactive correction inside the tool.

**Evidence.** Jukebox features improved melody-transcription F1 substantially over spectrogram baselines (paper). TheoryTab overall >50k analyses powers Hookpad Aria (see above).

**For the studio.** Directly matches the studio's symbolic-first, lead-sheet-centric representation: "insert example audio → get a lead sheet you can edit." Also demonstrates the value of generative-model features for transcription.

<small>Tags: [transcription] [notation] [symbolic-generation] [multimodal-input] · Verification: verified (arXiv page) · Clusters 02, 06, 07</small>

### `hawthorne2018onsets` — OnsetsFrames — Onsets and Frames: Dual-Objective Piano Transcription

*Curtis Hawthorne, Erich Elsen, Jialin Song, Adam Roberts, Ian Simon, Colin Raffel, Jesse Engel, Sageev Oore, Douglas Eck; Google Brain (Magenta); ISMIR 2018 (arXiv Oct 2017)*

Links: https://arxiv.org/abs/1710.11153 ; https://magenta.withgoogle.com/onsets-frames

CNN+BiLSTM that jointly predicts note onsets and frame-wise pitch activity; onset predictions gate frame predictions so notes cannot start without a detected attack. Also predicts velocity. Input: piano audio; output: MIDI notes with onsets/offsets/velocity. No user control; correction happens downstream in a DAW/notation editor.

**Evidence.** >100% relative improvement in note-with-offset F1 over prior state of the art on MAPS.

**For the studio.** The architectural template (onset + frame heads) underlies Basic Pitch and many hum transcribers; the studio's "play or sing it in" path inherits its failure modes (offsets, repeated notes).

<small>Tags: [transcription] [audio-generation] [toolkit] · Verification: verified (fetched primary source) · Cluster 06</small>

### `jung2025unified` — UnifiedScoreTranslation — Unified Cross-modal Translation of Score Images, Symbolic Music, and Performance Audio

*Jongmin Jung, Dongmin Kim, Sihun Lee, Seola Cho, Hyungjoon So, Irmak Bukey, Chris Donahue, Dasaem Jeong; Sogang University + CMU. arXiv May 2025; IEEE/ACM TASLP (Dec 2025 per Donahue's news).*

Links: https://arxiv.org/abs/2505.12863

One encoder–decoder Transformer with unified tokenisation of score images, MusicXML, MIDI and audio, trained multitask on the new **YouTube Score Video (YTSV)** dataset (>1,300 h of aligned score-image/audio, ~10× prior datasets).

**Evidence.** OMR symbol error rate 24.58% → 13.67% (SOTA); first score-image-conditioned audio generation.

**For the studio.** Cross-modal bridge among the studio's core representations (scanned/handwritten score ↔ symbolic ↔ audio) — including a path from a *photographed sketch of notation* to symbolic.

<small>Tags: [representation] [transcription] [notation] [audio-generation] [dataset] [multimodal-input] · Verification: verified (arXiv HTML) · Cluster 02</small>

### `gardner2022mt3` — MT3 — MT3: Multi-Task Multitrack Music Transcription

*Josh Gardner, Ian Simon, Ethan Manilow, Curtis Hawthorne, Jesse Engel; Google Magenta / U. Washington; ICLR 2022 (arXiv Nov 2021)*

Links: https://arxiv.org/abs/2111.03017 ; code: https://github.com/magenta/mt3

A T5-style encoder-decoder Transformer that maps spectrogram frames to a MIDI-like token vocabulary with instrument program tokens, trained jointly on several AMT datasets (MAESTRO, Slakh, Cerberus4, GuitarSet, MusicNet, URMP). Input: mixed polyphonic audio; output: multi-instrument note events. Human control: none at inference; errors corrected after the fact in MIDI.

**Evidence.** Unified training substantially improves low-resource instruments (e.g., guitar) while matching piano SOTA; established a multi-task AMT benchmark suite.

**For the studio.** The reference approach for "drop in an example recording and get a multitrack MIDI sketch" — the studio's *example-audio-as-annotation* path. Token-based output is also LLM-compatible.

<small>Tags: [transcription] [multimodal-input] [toolkit] · Verification: verified (fetched primary source) · Cluster 06</small>

### `bittner2022basicpitch` — BasicPitch — A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation

*Rachel M. Bittner, Juan José Bosch, David Rubinstein, Gabriel Meseguer-Brocal, Sebastian Ewert; Spotify Audio Intelligence Lab; ICASSP 2022*

Links: https://github.com/spotify/basic-pitch ; demo https://basicpitch.io ; TS port https://github.com/spotify/basic-pitch-ts

Very small CNN (harmonic CQT input) predicting onsets, notes and multipitch, instrument-agnostic, outputting MIDI *with pitch bends*. Input: any audio (mp3/wav/flac…), resampled to 22.05 kHz; outputs MIDI, note CSV, raw NPZ. Python and TypeScript (runs in-browser). Apache-2.0. The user chooses thresholds (onset/frame) and minimum note length via CLI/web sliders, which is the main error-correction knob.

**Evidence.** Paper reports competitive note F1 with far fewer parameters than Onsets-and-Frames-class models; best on single-instrument recordings.

**For the studio.** The pragmatic default for hum/voice→MIDI in a browser-based studio (permissive licence, JS port, pitch-bend capture preserves expressive intent of a sung line).

<small>Tags: [transcription] [humming] [toolkit] [DAW-plugin] · Verification: verified (fetched primary source) · Cluster 06</small>

## S1.2. Compose: voice / humming

### `ghias1995qbh` — QBH-1995 — Query By Humming: Musical Information Retrieval in an Audio Database

*Asif Ghias, Jonathan Logan, David Chamberlin, Brian C. Smith; Cornell University; ACM Multimedia '95, 1995*

Links: https://www.cs.cornell.edu/zeno/papers/humming/humming.html ; https://dl.acm.org/doi/10.1145/217279.215273

The founding query-by-humming paper. User hums into a microphone; autocorrelation pitch tracking converts the hum into a 3-symbol contour string (U/D/S = up/down/same relative to previous note); approximate string matching (error-tolerant) against contour strings derived from a MIDI database (183 songs). Interaction: hum → ranked song list; errors handled by tolerance in the matcher, not by user correction.

**Evidence.** 10–12 pitch transitions sufficed to discriminate 90% of the 183 songs; search < 4 s per 100 songs on a Sparc 2; pitch tracking took 20–45 s.

**For the studio.** Establishes the design principle that hummed input should be reduced to a *robust, coarse representation* (contour) before matching/generation, since exact pitch from voice is unreliable. Useful as a fallback for "find the motif I hummed earlier" inside a project.

<small>Tags: [humming] [transcription] [history] [multimodal-input] · Verification: verified (fetched primary source) · Cluster 06</small>

### `donahue2023singsong` — SingSong — SingSong: Generating Musical Accompaniments from Singing

*Chris Donahue, Antoine Caillon, Adam Roberts, et al. (Ethan Manilow, Philippe Esling, Andrea Agostinelli, Mauro Verzetti, Ian Simon, Olivier Pietquin, Neil Zeghidour, Jesse Engel); Google (Magenta/DeepMind); arXiv Jan 2023.*

Links: https://arxiv.org/abs/2301.12662 ; https://chrisdonahue.com/publication/23-01-singsong/

Vocal audio → instrumental accompaniment audio. Source separation applied to a large music corpus yields (vocal, instrumental) pairs; AudioLM is adapted for conditional generation. User sings/hums; system returns a full-band backing track. No symbolic intermediate; the only control is the input vocal itself (re-sing to change).

**Evidence.** Listeners significantly preferred SingSong instrumentals over a strong retrieval baseline in pairwise tests (exact percentage not confirmed here).

**For the studio.** The strongest demonstration that a hummed/sung line alone carries enough information to imply harmony, groove and style. For the studio this argues for a *symbolic* SingSong: sung melody → chords + arrangement in notation that the composer can then edit.

<small>Tags: [humming] [audio-generation] [accompaniment] [multimodal-input] · Verification: verified (arXiv page; lab page) · Clusters 02, 04, 06</small>

### `frank2020humtosearch` — HumToSearch — The Machine Learning Behind Hum to Search (Google)

*Christian Frank (with Alex Tudor, Duc Dung Nguyen, Matej Kastelic, Mihajlo Velimirović, et al.); Google Research Zürich; Google AI Blog, 12 Nov 2020 (product launch Oct 2020)*

Links: https://research.google/blog/the-machine-learning-behind-hum-to-search/

Production humming search in the Google app: user taps mic → "search a song" → hums/sings/whistles 10–15 s. A neural network embeds the hum spectrogram so that it lands near embeddings of the *original studio recordings* (>500k songs) — no intermediate MIDI. Training data scarcity was solved by synthesising hummed versions from recordings via SPICE pitch extraction, later a neural hum-like generator; triplet loss plus confidence-based loss. Output: ranked candidate songs; no user correction beyond re-humming.

**Evidence.** Blog reports qualitative accuracy gains from the synthetic-hum augmentation and confidence loss; no public metrics.

**For the studio.** Shows that *embedding-based* matching of hums against audio is production-viable, useful for "which of my sketches/reference tracks is this?" retrieval inside a project; also a cautionary example of an opaque pipeline with no editable intermediate.

<small>Tags: [humming] [product] [multimodal-input] · Verification: verified (fetched primary source) · Cluster 06</small>

### `doremir2014scorecloud` — Sing2Notes — ScoreCloud (Doremir) and Sing2Notes (Klangio): sing → notation products

*Doremir Music Research AB (Stockholm; Sven Ahlbäck, Sven Emtell); ScoreCleaner 2011 → ScoreCloud 2014–. Klangio GmbH (Karlsruhe); Sing2Notes app 2021–.*

Links: https://scorecloud.com/ ; https://klang.io/sing2notes/

Consumer tools that transcribe singing/playing directly to sheet music. ScoreCloud (desktop Studio + mobile Express) transcribes audio or MIDI into notation with polyphonic analysis; MusicXML/MIDI export in paid tiers. Sing2Notes: record, upload or paste a YouTube link → sheet music in seconds, exported as PDF/MIDI (quantised and unquantised)/MusicXML; an **Edit Mode** lets users fix notes in-app; free tier = first 20 s.

**Evidence.** No published accuracy figures; Klangio claims >4M transcriptions.

**For the studio.** The commercial baseline for "hum → notation → fix by hand". Their UX (quantised vs unquantised export, in-app edit mode) is the minimum the studio must match.

<small>Tags: [humming] [transcription] [notation] [product] · Verification: verified (product pages fetched; ScoreCloud history via Wikipedia) · Cluster 06</small>

### `floresgarcia2025sketch2sound` — Sketch2Sound — Sketch2Sound: Controllable Audio Generation via Time-Varying Signals and Sonic Imitations

*Hugo Flores García, Oriol Nieto, Justin Salamon, Bryan Pardo, Prem Seetharaman; Northwestern + Adobe Research; ICASSP 2025 (arXiv Dec 2024).*

Links: https://arxiv.org/abs/2412.08550 ; demo https://hugofloresgarcia.art/sketch2sound/

Adds three **interpretable time-varying controls—loudness, spectral centroid (brightness), pitch**—to a text-to-audio DiT via one linear layer per control (40k fine-tune steps); controls are extracted from a **vocal imitation** or any "sonic sketch", with random median filtering at train time so users can choose how tightly to follow the gesture.

**Evidence.** Retains text adherence and fidelity while following vocal-imitation control curves.

**For the studio.** "Hum/sing/vocalise a gesture" → time-aligned control of generation, with a tunable looseness knob—very close to the multimodal *sketch* annotation idea.

<small>Tags: [audio-generation] [humming] [sketch] [controllability] [multimodal-input] · Verification: verified (abstract); authors partial · Cluster 04</small>

### `magenta2020tonetransfer` — ToneTransfer — Tone Transfer (DDSP in the browser)

*Magenta + Google AIUX teams; Google Research; released 1 Oct 2020*

Links: https://magenta.withgoogle.com/tone-transfer ; https://sites.research.google/tonetransfer

Web app: record or upload humming/singing/any instrument; SPICE extracts pitch, a DDSP model (TF.js) re-renders it as flute, saxophone, violin, trumpet, etc. The human controls the input performance (pitch contour, dynamics, timing) and picks the target instrument; UX research explicitly targeted non-Western instruments as inputs.

**Evidence.** Product; user research described on the blog; year-long Magenta/AIUX collaboration.

**For the studio.** Concrete precedent for **humming as input** to a musical rendering step; the whole pipeline (sing → pitch → timbre) is exactly the founder's "hum an idea, get an instrument line."

<small>Tags: [humming] [multimodal-input] [audio-generation] [style-transfer] [product] · Verification: verified (official page fetched) · Cluster 01</small>

### `cartwright2015vocalsketch` — VocalSketch — VocalSketch: Vocally Imitating Audio Concepts

*Mark Cartwright, Bryan Pardo; Northwestern University; CHI 2015*

Links: https://interactiveaudiolab.github.io/assets/papers/cartwright_pardo_chi2015.pdf ; data https://github.com/interactiveaudiolab/VocalSketchDataSet

Crowd-sourced dataset of 4,429 vocal imitations (from 10,750 recordings, 248 contributors) of everyday sounds, instruments, synthesizer patches; plus a recognition study. Establishes "vocal sketching" of *timbre* (not melody) as an input modality for sound search/design.

**Evidence.** Forced-choice identification accuracy 0.80 for everyday sounds, 0.45 instruments, 0.42 commercial synths, 0.54 single synth sounds (chance 0.1); free-response 0.23–0.27.

**For the studio.** Beyond melody, composers can *vocalise* a desired sound ("this pad should go 'shhwaaa'"); the numbers show that works for timbrally distinctive targets and needs disambiguation for instruments — argues for showing top-k candidate sounds to pick from.

<small>Tags: [humming] [dataset] [HCI-study] [multimodal-input] · Verification: verified (fetched primary source) · Cluster 06</small>

### `liu2023humtrans` — HumTrans — HumTrans: A Novel Open-Source Dataset for Humming Melody Transcription and Beyond

*Shansong Liu, Xu Li, Dian Li, Ying Shan; ARC Lab, Tencent PCG; arXiv Sept/Oct 2023 (also ICASSP 2024)*

Links: https://arxiv.org/abs/2309.09623 ; https://github.com/shansongliu/HumTrans

56.22 h of humming: 500 compositions split into 1,000 segments, each hummed twice by 10 music-trained students via a web interface with a reference melody, so ground truth is known. Baseline evaluation of four vocal-transcription models.

**Evidence.** Best baseline (JDC-STP) only ~6.8% note F1 (validation) / 5.7% (test) — humming is far harder than sung lyrics for existing models.

**For the studio.** Quantifies how bad "just transcribe the hum" is out of the box and provides the training/eval set for a studio-specific hum model; also supports the design decision to always show the transcription for confirmation.

<small>Tags: [humming] [dataset] [transcription] [evaluation] · Verification: verified (fetched primary source) · Cluster 06</small>

### `gupta2024dynhumtrans` — DynHumTrans — Dynamic HumTrans: Humming Transcription Using CNNs and Dynamic Programming

*Shubham Gupta, Isaac Neri Gomez-Sarmiento, Faez Amjed Mezdari, Mirco Ravanelli, Cem Subakan; Mila / Université Laval / Concordia; arXiv Oct 2024 (Springer LNCS chapter 2024/25)*

Links: https://arxiv.org/abs/2410.05455 ; https://github.com/shubham-gupta-30/humming_transcription

CNN frame classifier + dynamic-programming decoding for hum → notes; the authors also *correct* HumTrans's onset/offset ground truth and release fixed annotations.

**Evidence.** Octave-invariant note+onset F1 0.673 vs 0.564 for the next-best method; similar accuracy octave-aware.

**For the studio.** Current best open baseline for the hum-to-MIDI step; DP decoding with musical constraints (scale, tempo grid) is the natural place to inject the composer's annotations (key, meter) as priors.

<small>Tags: [humming] [transcription] · Verification: verified (fetched primary source) · Cluster 06</small>

### `vochlea2021dubler` — Dubler — Vochlea Dubler 2 (and Jam Origin MIDI Guitar) — real-time voice/instrument → MIDI controllers

*Vochlea Music (London), Dubler 2 released 2021; Jam Origin (Denmark), MIDI Guitar 2 (2016–) / MIDI Guitar 3 open beta (jam.live)*

Links: https://vochlea.com/products/dubler2 ; review https://www.soundonsound.com/reviews/vochlea-dubler-2 ; https://www.jamorigin.com/

Dubler 2 converts singing/humming/beatboxing to MIDI in real time: pitch → notes (with a visual "note wheel" and key/scale restriction), vowels (aaa/ooo/eee) → CC, up to 12 recorded examples per beatbox sound train drum triggers. Error handling: a "Stickiness" slider smooths note transitions; scale lock; users adapt technique. £189 (software) / £249 with mic. MIDI Guitar is the analogous polyphonic guitar→MIDI plugin (standalone/VST/AU/iOS).

**Evidence.** Sound On Sound (Nov 2021) reports low latency for triggers, slightly more for pitch; no published accuracy study.

**For the studio.** Shows the *interaction design* of hum-to-MIDI that works for musicians: constrain (scale lock), smooth (stickiness), visualise (note wheel), and let users train per-user sounds. Directly reusable patterns for the studio's live hum-in step.

<small>Tags: [humming] [product] [real-time] [DAW-plugin] · Verification: verified (product pages + review fetched) · Cluster 06</small>

## S1.3. Compose: sketch / pen

### `benetatos2022drawlisten` — DrawAndListen — Draw and Listen! A Sketch-Based System for Music Inpainting

*Christodoulos Benetatos, Zhiyao Duan; University of Rochester (AIR Lab). TISMIR 5(1):141–155, 2022. **Not CMU** — included as the music-specific sketch-editing analogue to ExpressEdit.*

Links: https://doi.org/10.5334/tismir.128 ; https://labsites.rochester.edu/air/projects/DrawAndListen.html

Fill missing measures of a monophonic melody from **hand-drawn curves**: a pitch-contour curve and a note-density (rhythm) curve, plus pitch/rhythm offset sliders; a multi-encoder/decoder VAE disentangles relative pitch, relative rhythm and surrounding context.

**Evidence.** Objective + subjective evaluation on the Irish folk dataset (24,065 tunes); beats rule-based and genetic baselines on musicality and fidelity to the sketch; users without notation knowledge found it intuitive.

**For the studio.** Demonstrates "scribble on the notation → infill" in the symbolic domain — the sketch modality of the founder's loop — but only for monophonic melody and without NL or audio annotations; combining it with ExpressEdit's grammar is open territory. (Related but unverified: "MIDI-Draw: Sketching to Control Melody Generation", 2023.)

<small>Tags: [sketch] [infilling] [symbolic-generation] [HCI-study] [annotation] · Verification: verified (journal page) · Cluster 02</small>

### `hearn2015staffpad` — StaffPad — StaffPad (pen-based handwriting-to-notation, product)

*David William Hearn; StaffPad Ltd; Windows/Surface 2015, iPad 2020; US$90*

Links: https://www.staffpad.net/ ; review https://www.scoringnotes.com/reviews/staffpad-for-ipad/

Handwrite notes, rests, dynamics, articulations and slurs with a stylus on a staff; recognition runs *one measure at a time* when the pen moves to the next bar, replacing ink with engraved notation. Misrecognitions are fixed by re-writing or via a correction palette. Adds DAW-like automation lanes (expression, pan, volume), premium sample libraries, and **ScoreSync**/StaffPad Reader for pushing parts and *shared annotations* to players' iPads in rehearsal.

**Evidence.** Review reports "generally strong" recognition with occasional misinterpretation; no published accuracy.

**For the studio.** The commercial proof that measure-granular, pen-first notation entry is usable by composers; its "ink → engraved, keep ink for annotations" duality and rehearsal-sync feature are directly relevant.

<small>Tags: [sketch] [notation] [product] [annotation] · Verification: verified (product and review fetched) · Cluster 06</small>

### `xenakis1977upic` — UPIC — UPIC (Xenakis, CEMAMu, 1977) and IanniX (open-source graphical sequencer)

*Iannis Xenakis with engineer Patrick Saint-Jean; CEMAMu, Paris; first prototype 1977, real-time version 1987. IanniX: IanniX Association (Thierry Coduys et al.), 2000s–present; Scordato, eContact! 19.3 (2017) "From UPIC to IanniX".*

Links: https://www.iannis-xenakis.org/en/dictionary-upic/ ; https://www.iannix.org/en/whatisiannix/ ; https://github.com/buzzinglight/IanniX ; https://econtact.ca/19_3/scordato_iannix.html

UPIC: composer draws arcs on a CAD-style tablet (x = time, y = pitch) and also *draws* waveforms and envelopes; a wavetable synthesiser plays the page; the same drawing can act as waveform or control signal at different time scales. First all-computer piece: *Mycènes Alpha* (1978). IanniX (GPL-3) generalises this: triggers, curves and cursors in a 2D/3D scene emit OSC/MIDI to any environment; scriptable in JavaScript.

**Evidence.** Historical; no user studies. Les Ateliers UPIC (1986) → CCMIX pedagogical use until 2007.

**For the studio.** The origin of "drawing is a score"; also a warning — UPIC drawings map to *sound* not to notation, so the compiler must decide what a scribble *means* (pitch contour? dynamics? density?). IanniX's separation of drawn geometry from the sound engine is a clean model for a sketch layer that emits control data.

<small>Tags: [sketch] [history] [music-as-code] [toolkit] · Verification: verified (fetched primary sources; Scordato article partial) · Cluster 06</small>

### `garcia2012paper` — PaperSubstrates — Interactive Paper Substrates to Support Musical Creation (and PaperComposer, InkSplorer)

*Jérémie Garcia, Theophanis Tsandilas, Carlos Agon, Wendy E. Mackay; Inria / Université Paris-Sud / IRCAM; CHI 2012 (DOI 10.1145/2207676.2208316); PaperComposer at IHM 2014 (DOI 10.1145/2670444.2670450); InkSplorer at NIME 2011*

Links: https://dl.acm.org/doi/10.1145/2207676.2208316 ; https://hal.science/hal-00664334

Anoto-pen "interactive paper" components that composers lay out themselves (staff, curve, keyboard, timeline substrates) and link to OpenMusic/Max; pen strokes on paper become data (e.g., drawn curves → parameters) while remaining sketchable paper. PaperComposer lets composers build their own paper interfaces. Grounded in field studies of contemporary composers' paper sketching practices.

**Evidence.** Participatory design with professional composers (IRCAM); qualitative.

**For the studio.** Shows composers want *personalised* sketch substrates rather than one fixed sketch UI, and that pen curves are naturally understood as *control functions* (dynamics, density, tempo) — a template for typed annotation "lanes".

<small>Tags: [sketch] [HCI-study] [creativity-support] [music-as-code] · Verification: partial (search-result metadata; full text not fetchable — ACM/HAL blocked) · Cluster 06</small>

### `chen2020sketchnet` — SketchNet — Music SketchNet: Controllable Music Generation via Factorized Representations of Pitch and Rhythm

*Ke Chen, Cheng-i Wang, Taylor Berg-Kirkpatrick, Shlomo Dubnov; UC San Diego / Smule; ISMIR 2020*

Links: https://arxiv.org/abs/2008.01291 ; code: https://github.com/RetroCirce/Music-SketchNet

"Sketch" = partial specification of a missing measure: the user supplies a pitch contour, a rhythm pattern, or both, and the model completes it. SketchVAE factorises pitch and rhythm; SketchInpainter predicts latent codes for missing bars from context; SketchConnector fuses user sketches with predictions. Monophonic folk melodies (Irish/Scottish, 4/4).

**Evidence.** ~16k training / 2k test melodies; listening test with 106 subjects (318 responses); improved pitch/rhythm accuracy and subjective musicality over baselines.

**For the studio.** Formalises sketch-as-constraint infilling — exactly the "annotate this bar with a rough contour/rhythm and compile the notes" operation, with pitch and rhythm as *separately annotatable* lanes.

<small>Tags: [sketch] [infilling] [controllability] [symbolic-generation] · Verification: verified (arXiv abstract fetched) · Clusters 03, 06</small>

### `farbood2004hyperscore` — Hyperscore — Hyperscore: a graphical sketchpad for novice composers

*Morwaread (Mary) Farbood, Egon Pasztor, Kevin Jennings; Tod Machover's Opera of the Future group, MIT Media Lab; IEEE Computer Graphics & Applications 24(1), 2004 (system from 2001–2002; ICMC 2007 follow-up "Composing with Hyperscore"); commercialized by Harmony Line Inc. 2004–2017; rebuilt by Peter Torpey (2021), web version 2022 (v5.0) under nonprofit New Harmony Line*

Links: https://doi.org/10.1109/MCG.2004.1255809 ; https://en.wikipedia.org/wiki/Hyperscore ; https://www.hyperscore.com/ (TLS misconfigured at fetch time)

Users first create short **motives** (melodic/rhythmic fragments) in "motive windows," each assigned a color; then in a **sketch window** they *draw* colored lines whose contour and vertical position control pitch/transposition of that motive over time, layering many lines into a texture. A separate **harmony line** is drawn to shape harmonic tension; the system auto-harmonizes so the texture stays consonant/dissonant as drawn. Output is General-MIDI playback and an exportable score. Used by children in Machover's *Toy Symphony* (2002–03) to compose orchestral pieces, in schools and hospitals, and in the City Symphonies.

**Evidence.** Toy Symphony workshops in Dublin, Glasgow, Berlin, Boston, New York (7–12 children each, five sessions); nearly all children completed a string-orchestra piece; observed visual-pattern vs aural strategies.

**For the studio.** *The* precedent for "scribble to compose": a freehand line becomes a compile instruction over human-authored motives, with a separate drawn control for harmony. Its motive/sketch/harmony-line decomposition is a strong candidate for the studio's sketch layer.

<small>Tags: [sketch] [symbolic-generation] [notation] [creativity-support] [education] [history] [controllability] · Verification: verified (fetched primary source) · Clusters 01, 06</small>

### `liang2024drawlody` — Drawlody — Drawlody: Sketch-Based Melody Creation with Enhanced Usability and Interpretability

*Qihao Liang, Ye Wang; National University of Singapore (SMC lab); IEEE Transactions on Multimedia, 2023/2024*

Links: https://smcnus.comp.nus.edu.sg/archive/pdf/2024/2024_Drawlody__IEEE_TMM_Finalised.pdf

User draws a simplified melodic contour; a CNN-Transformer encoder-decoder maps it to a melody via a Generalised Melody Contour (GMC) representation and "FlexMIDI" (basic pitch trend + pitch "flex" around tonal centres); outputs MIDI/audio with adjustable tempo/duration and a *visual explanation* showing sketch–melody alignment.

**Evidence.** 18 participants (6 trained); user-friendliness 4.38/5 vs 2.94 (chord-based) and 2.38 (DAW) interfaces; interpretability 4.50/5; beat rule-based and CNN baselines on musicality; still below expert compositions on richness/stability.

**For the studio.** Best-evidenced sketch→melody system; its alignment visualisation is a model for showing *how* the compiler interpreted an annotation so the composer can correct the right thing.

<small>Tags: [sketch] [symbolic-generation] [controllability] [HCI-study] · Verification: verified (fetched primary source) · Cluster 06</small>

### `namgyal2022mididraw` — MIDIDraw — MIDI-Draw: Sketching to Control Melody Generation

*Tashi Namgyal, Raul Santos-Rodriguez, Peter Flach; University of Bristol; ISMIR 2022 Late-Breaking/Demo (arXiv May 2023)*

Links: https://arxiv.org/abs/2305.11605

User draws a pitch contour on a canvas; a conditional VAE trained on synthetic melodies (contours parameterised by low-frequency cosine components) generates note sequences that lie on or scatter around the curve. Proof of concept; constant rhythm.

**Evidence.** Preliminary user testing: non-musicians drew over-oscillating curves (need guidance); users wanted rhythm variation.

**For the studio.** Small but instructive: drawn contours need *smoothing/guidance affordances*, and rhythm must be a separate control — informs the design of a contour-annotation tool.

<small>Tags: [sketch] [controllability] [symbolic-generation] · Verification: verified (fetched primary source) · Cluster 06</small>

### `coughlan2006interaction` — CoughlanJohnson — Interaction in Creative Tasks: Ideation, Representation and Evaluation in Composition

*Tim Coughlan, Peter Johnson; University of Bath; CHI 2006*

Links: https://oro.open.ac.uk/43523 (CHI 2006 proceedings version via ACM DL)

Observational study of composers (individual and collaborating) analysing how ideas are represented and evaluated; proposes cycles of ideation and evaluation as atomic units of creative interaction, catalogues representation types used in composition, and prototypes a "Sonic Sketchpad" for musical idea representation.

**Evidence.** Qualitative observations; number of composers not stated in abstract.

**For the studio.** Theoretical grounding for the compose→annotate→evaluate loop: representation (sketch/annotation) is the *central* activity, not a preliminary; tools should support incomplete, ambiguous representations.

<small>Tags: [HCI-study] [sketch] [creativity-support] [co-creation-framework] · Verification: verified (fetched institutional repository abstract) · Cluster 06</small>

### `cavez2025euterpen` — EuterPen — EuterPen: Unleashing Creative Expression in Music Score Writing

*Vincent Cavez, Catherine Letondal, Caroline Appert, Emmanuel Pietriga; Université Paris-Saclay / CNRS / Inria; CHI 2025 (DOI 10.1145/3706598.3713488)*

Links: https://dl.acm.org/doi/10.1145/3706598.3713488 ; PDF https://www.vincentcavez.com/euterPen.pdf

A notation-program prototype that *selectively relaxes syntactic and structural constraints*: with pen and touch, composers input and move symbols with more freedom, and can "make space on, between and around staves to insert additional content such as digital ink, pictures and audio samples." Designed through prototyping phases, a participatory design workshop and interviews.

**Evidence.** Feedback from participating professional composers described the approach as compelling and promising (qualitative).

**For the studio.** The closest existing realisation of the studio's "scribble on the score, paste an image or audio clip next to a passage" annotation model. Suggests annotations should live in a spatial layer *interleaved with* the score, not in a side panel.

<small>Tags: [sketch] [annotation] [notation] [multimodal-input] [HCI-study] · Verification: verified (abstract via Semantic Scholar API; author page) · Cluster 06</small>

### `cavez2024challenges` — CavezCHI24 — Challenges of Music Score Writing and the Potentials of Interactive Surfaces

*Vincent Cavez, Catherine Letondal, Emmanuel Pietriga, Caroline Appert; Université Paris-Saclay, CNRS, Inria (LISN/ILDA); CHI 2024 (DOI 10.1145/3613904.3642079)*

Links: https://dl.acm.org/doi/10.1145/3613904.3642079 ; https://inria.hal.science/hal-04497643

Interviews with nine professional composers; analyses frictions in notation programs ("elaborate structured document editors" that enforce notation rules) through the Cognitive Dimensions of Notations framework; argues pen+touch surfaces can *temporarily break structure* to reconcile the need for engraving rigor with creative flexibility.

**Evidence.** N=9 interviews; qualitative findings on premature commitment, viscosity, and reliance on paper alongside software.

**For the studio.** Empirical justification for the studio's premise that composers need a loosely-structured annotation/sketch layer *on top of* a strict symbolic model.

<small>Tags: [HCI-study] [notation] [sketch] [creativity-support] · Verification: verified (abstract via Semantic Scholar API; author page) · Cluster 06</small>

## S1.4. Compose: image / video / text inspiration

### `liu2024mumullama` — MuMuLLaMA — M²UGen / MuMu-LLaMA: Multi-modal Music Understanding and Generation via Large Language Models

*Atin Sakkeer Hussain, Shansong Liu, Chenshuo Sun, Ying Shan (M²UGen, arXiv Nov 2023); Shansong Liu, Atin Sakkeer Hussain, Qilong Wu, Chenshuo Sun, Ying Shan (MuMu-LLaMA, arXiv Dec 2024); ARC Lab, Tencent PCG*

Links: https://arxiv.org/abs/2311.11255 ; https://arxiv.org/abs/2412.06660 ; https://github.com/shansongliu/MuMu-LLaMA

LLaMA with MERT (music), ViT (image) and ViViT (video) encoders via understanding adapters; output adapters drive MusicGen/AudioLDM 2. Tasks: music QA, text→music, *prompt-based music editing* (MUEdit: speed, pitch, instrument changes), image→music and video→music. Datasets MUCaps/MUImage/MUVideo/MUEdit total 167.69 h.

**Evidence.** Subjective preference 58.2% (text→music), 81.3% (image→music), 80.7% (video→music) over baselines.

**For the studio.** Demonstrates a single conversational agent accepting *any* modality plus edit instructions — the architectural shape of the studio's annotation compiler — but at the audio level; the symbolic analogue remains to be built.

<small>Tags: [multimodal-input] [image] [video] [editing] [LLM-agent] [audio-generation] · Verification: verified (fetched MuMu-LLaMA PDF; author lists partly from arXiv listings) · Cluster 06</small>

### `rinaldi2024art2mus` — Art2Mus — Art2Mus: Bridging Visual Arts and Music through Cross-Modal Generation (and 2026 extension)

*Ivan Rinaldi, Nicola Fanelli, Giovanna Castellano, Gennaro Vessio; University of Bari Aldo Moro; ECCV 2024 AI4VA workshop (arXiv Oct 2024). Extended version with Matteo Mendula, Florence Levé, Matteo Testi (arXiv Feb 2026, "ArtSound" dataset).*

Links: https://arxiv.org/abs/2410.04906 ; https://arxiv.org/abs/2602.17599

Adds an ImageBind-based image encoder + projection to frozen AudioLDM 2 to generate audio from a digitised painting, trained on synthetic artwork–music pairs (10k ArtGraph artworks × FMA tracks matched by embedding similarity). 2026 version: 105,884 pairs with dual-modality captions; Visual Conditioning Extractor and Image Aligner remove the text bottleneck.

**Evidence.** 2024: lower KL than baselines but human raters *preferred* standard AudioLDM 2 output. 2026: 15 participants; ImageBind variants slightly better on quality, CLIP variants on semantic alignment.

**For the studio.** An honest negative result — end-to-end image→audio without a symbolic or textual intermediate did not beat text-only generation in listener preference, supporting the studio's "image → editable proposal" stance.

<small>Tags: [image] [audio-generation] [dataset] [evaluation] · Verification: verified (fetched primary sources) · Cluster 06</small>

### `kang2024video2music` — Video2Music — Video2Music: Suitable Music Generation from Videos using an Affective Multimodal Transformer Model

*Jaeyong Kang, Soujanya Poria, Dorien Herremans; Singapore University of Technology and Design; Expert Systems with Applications 249 (2024) (arXiv Nov 2023)*

Links: https://arxiv.org/abs/2311.00968 ; https://github.com/AMAAI-Lab/Video2Music

Video → *symbolic chord sequence* (then MIDI with rhythm/loudness variation). Video features: scene cuts, motion, emotion probabilities, semantics; an Affective Multimodal Transformer decodes chords with an affective-matching loss. User supplies video (file or YouTube), desired key and an optional seed chord progression. Dataset MuVi-Sync (748 videos).

**Evidence.** 21 raters, 7-point scale: 4.2 overall vs 3.5 for a Music Transformer baseline; significant gains on harmonic/rhythmic/loudness matching (p<0.00001). Limitation: chords only, can feel repetitive.

**For the studio.** The main *symbolic* video-to-music system — output is a chord chart the composer can edit, with key and seed controls; a good fit for scoring-to-picture inside a notation-first studio.

<small>Tags: [video] [symbolic-generation] [controllability] [dataset] · Verification: verified (fetched primary source) · Cluster 06</small>

### `su2024v2meow` — V2Meow — V2Meow: Meowing to the Visual Beat via Video-to-Music Generation

*Kun Su, Judith Yue Li, Qingqing Huang, Dima Kuzmin, Joonseok Lee, Chris Donahue, Fei Sha, Aren Jansen, Yu Wang, Mauro Verzetti, Timo Denk; Google Research / DeepMind et al.; AAAI 2024 (arXiv May 2023)*

Links: https://arxiv.org/abs/2305.06594 ; https://ojs.aaai.org/index.php/AAAI/article/view/28299

Video frames (1 fps; I3D flow, CLIP, ViT-VQGAN features) plus optional text prompt → 10-s music audio via a three-stage autoregressive pipeline (video → semantic tokens → coarse → fine acoustic tokens, SoundStream decode). Text prompt is the only user control besides the video.

**Evidence.** MV100K (110k music videos); ~200 raters, 3,500+ ratings; 83.8% visual-relevance preference on MV100K; FAD/KL/MuLan-cycle/beat metrics.

**For the studio.** State of the art for "insert a video as annotation" at the audio level; shows text can steer style while video sets pacing — but offers no symbolic output for a composer to edit.

<small>Tags: [video] [audio-generation] [text-conditioning] · Verification: verified (fetched primary source) · Cluster 06</small>

### `li2024muvi` — MuVi — MuVi: Video-to-Music Generation with Semantic Alignment and Rhythmic Synchronization (and VidMusician)

*Ruiqi Li, Siqi Zheng, Xize Cheng, Ziang Zhang, Shengpeng Ji, Zhou Zhao; Zhejiang University (arXiv Oct 2024, "work in progress"). VidMusician: Sifei Li, Binxin Yang, Chunji Yin, Chong Sun, Yuxin Zhang, Weiming Dong, Chen Li; CAS Institute of Automation / WeChat, Tencent (arXiv Dec 2024).*

Links: https://arxiv.org/abs/2410.12957 ; https://arxiv.org/abs/2412.06296

MuVi: visual adaptor compresses VideoMAE V2 features to audio-rate; contrastive pre-training with *temporal-shift* and random-replacement negatives teaches beat-level synchrony; flow-matching DiT generates audio non-autoregressively; style/genre controls. VidMusician: global visual features as semantic conditions (cross-attention) and local features as rhythmic cues (in-attention) on a text-to-music backbone; DVMSet dataset.

**Evidence.** MuVi beat-hit score 49.23% vs 25.14% for M²UGen; MOS-Q 3.81. VidMusician outperforms prior methods on DVMSet incl. AI-generated videos.

**For the studio.** Separates *semantic* and *rhythmic* video conditioning — the two annotation types a film composer actually marks (mood, hit points). Suggests a symbolic pipeline: detect hit points → annotate → compile.

<small>Tags: [video] [audio-generation] [controllability] · Verification: verified (fetched primary sources) · Cluster 06</small>

### `zhang2022vis2mus` — Vis2Mus — Vis2Mus: Exploring Multimodal Representation Mapping for Controllable Music Generation

*Runbang Zhang, Yixiao Zhang, Kai Shao, Ying Shan, Gus Xia; NYU Shanghai Music X Lab / QMUL C4DM / Tencent / MBZUAI; arXiv Nov 2022*

Links: https://arxiv.org/abs/2211.05543 ; https://github.com/ldzhangyx/vis2mus

Uses an image as an *interface* to symbolic accompaniment: an analysis-by-synthesis approach discovers that visual→music mapping is approximately *equivariant* — brightness, contrast and style transformations on the image correspond to musical transformations. User picks a melody sketch + accompaniment image, applies style transfer, then fine-tunes brightness/contrast to steer the generated symbolic accompaniment.

**Evidence.** User studies: participants matched transformed music to transformed images at 62.5% (brightness), 68.2% (contrast) vs 50% chance, 60.6% (style) vs 25% chance; all p<0.05.

**For the studio.** A rare *symbolic* image-conditioned system with an interpretable control story; demonstrates images as continuous knobs (not just semantic prompts) over arrangement texture.

<small>Tags: [image] [symbolic-generation] [controllability] [accompaniment] · Verification: verified (fetched primary source) · Cluster 06</small>

### `chowdhury2024melfusion` — MeLFusion — MeLFusion: Synthesizing Music from Image and Language Cues using Diffusion Models

*Sanjoy Chowdhury, Sayan Nag, K J Joseph, Balaji Vasan Srinivasan, Dinesh Manocha; U. Maryland / U. Toronto / Adobe Research; CVPR 2024*

Links: https://arxiv.org/abs/2406.04673 ; https://github.com/schowdhury671/melfusion

Text-to-music diffusion model augmented with a "visual synapse" that injects self-attention features from a pretrained text-to-image model into the music model's cross-attention via learnable blending parameters. Input: image + text; output: audio. New dataset MeLBench (11,250 musician-annotated ⟨image, text, music⟩ triplets) and metric IMSM.

**Evidence.** Up to 67.98% relative FAD improvement over text-only; 75-participant subjective study on 100 samples.

**For the studio.** Shows images add real information beyond captions for *mood/timbre*; but output is audio only — suitable for the studio's rendering/arrangement stage rather than composition.

<small>Tags: [image] [audio-generation] [text-conditioning] [dataset] · Verification: verified (fetched primary source) · Cluster 06</small>

### `kim2025amuse` — Amuse — Amuse: Human-AI Collaborative Songwriting with Multimodal Inspirations

*Yewon Kim (KAIST → now CMU PhD), Sung-Ju Lee (KAIST), Chris Donahue (CMU). ACM CHI 2025 (Yokohama), **Best Paper Award** (top ~1%; confirmed on the G-CLef page and Kim's site). arXiv Dec 2024.*

Links: https://arxiv.org/abs/2412.18940 ; https://doi.org/10.1145/3706598.3713818 ; project: https://yewon-kim.com/amuse/ ; code: https://github.com/elianakim/Amuse ; video: https://youtu.be/FbFD3B2OCo8

A songwriting assistant that turns image, text, or audio "inspirations" into **chord progressions** inside Hookpad (deployed as a Chrome extension alongside Hooktheory's Aria copilot). Pipeline: (1) multimodal LLM (GPT-4o-2024-05-13, T=1.0) extracts *music keywords* from the inspiration — the user can inspect, add or delete keywords (transparent intermediate layer); (2) the LLM is prompted to generate N *diverse* 4-bar progressions (varying root/quality/extensions, diatonic vs chromatic patterns, cadences; Self-BLEU 0.30 vs 0.61 for naive repeated querying); (3) **rejection sampling against a unimodal chord prior**: two LSTMs estimate P(x) (trained on the 50-hour Hooktheory melody/chord dataset from Sheet Sage) and Q(x) (trained on 25,000 GPT-4o-generated progressions); a candidate is accepted iff u < P(x)/(M·Q(x)) with M=7.64 (95th percentile). This sidesteps the absence of paired multimodal↔chord data. Audio inspirations are handled by a separate "Chord Transcriber" (chords extracted from the audio) vs the "Chord Generator" for image/text. Accepted chords paste into the Hookpad editor for playback/editing; users then continue with Aria for melody. Released code covers the chord-generation method (training P/Q, rejection sampling, interactive keyword→chords CLI), not the extension UI; no license file at repo root.

**Evidence.** Formative interviews N=8 hobbyist songwriters (inspiration from audio 7, narrative 3, visual 2). **User study N=10** (8 hobbyists, 2 professionals; active Hookpad/Aria users), within-subjects Baseline (Aria only) vs Assist (Amuse+Aria), 8-bar chorus in 25 min, Wilcoxon signed-rank: inspiration support 6.20 vs 4.60 (p<.01), task alignment 6.10 vs 4.30 (p=.016), output quality (self-rated) 6.40 vs 5.30 (p=.023); CSI facets controllability 5.80 vs 4.40, collaboration 5.80 vs 3.90, exploration 6.10 vs 4.40, expressiveness 6.00 vs 4.20 (all p<.05); *no* difference in completion time (17.4 vs 17.6 min) or in externally judged composition quality. Usage patterns: kick-start with inspiration (6), ad-hoc inspiration flow (3), lyrics-centred (1). **Listening study N=45** (900 pairwise judgments): Amuse ≈ LSTM prior on coherence, both ≫ raw GPT-4o (p=.009 / 2e-5); Amuse most preferred for keyword relevance (58%, p=.006 vs LSTM). JSD to Hooktheory bigram distribution: prior 0.30, Amuse 0.46, GPT-4o 0.57.

**For the studio.** It is the reference design for *multimodal annotation → symbolic material*: keywords as a human-legible, editable contract between the annotation and the generator; LLM breadth disciplined by a small domain prior; output landing in an editable notation surface. Also a warning: participants expected the *downstream* model (Aria) to know the inspiration context — the studio's annotations must propagate through the whole compile chain, not just one stage.

<small>Tags: [multimodal-input] [image] [text-conditioning] [symbolic-generation] [HCI-study] [co-creation-framework] [creativity-support] [notation] [controllability] [annotation] · Verification: verified (arXiv HTML full text, project page, GitHub README, lab page) · Clusters 02, 05, 06</small>

### `tian2025vidmuse` — VidMuse — VidMuse: A Simple Video-to-Music Generation Framework with Long-Short-Term Modeling

*Zeyue Tian, Zhaoyang Liu, Ruibin Yuan, Jiahao Pan, Qifeng Liu, Xu Tan, Qifeng Chen, Wei Xue, Yike Guo; HKUST / Microsoft Research Asia; CVPR 2025 (arXiv June 2024)*

Links: https://arxiv.org/abs/2406.04321 ; https://github.com/ZeyueT/VidMuse ; https://vidmuse.github.io/

CLIP visual encoder → Long-Short-Term Visual module (segment-level and video-level features fused by cross-attention) → autoregressive music-token decoder → EnCodec 32 kHz audio. V2M dataset: ~360k video–music pairs for pretraining, 20k fine-tune, 300 benchmark. Video-only conditioning; no user controls.

**Evidence.** FAD/FD/KL/Density/Coverage/ImageBind score; A/B study of 600 samples with 40 participants on quality, alignment, musicality.

**For the studio.** Scale reference for video→audio; its long/short-term split (global mood vs local cues) is the right decomposition for annotating a *cue sheet* (global style + hit points) in a symbolic system.

<small>Tags: [video] [audio-generation] [dataset] · Verification: verified (fetched primary source) · Cluster 06</small>

## S1.5. Compose: example audio & personal style

### `dinculescu2019midime` — MidiMe — Personalizing a MusicVAE model with user data

*Monica Dinculescu, Jesse Engel, Adam Roberts; Google Brain (Magenta); NeurIPS 2019 Workshop on Machine Learning for Creativity and Design*

Links: https://magenta.tensorflow.org/midi-me

Trains a tiny VAE (4-D latent) on top of MusicVAE's 256-D latent space using one user MIDI file, in-browser in seconds; the user then explores a personal 4-knob space that generates variations "in the style of" their input without memorising it.

**Evidence.** Demo/technique paper; no controlled study.

**For the studio.** A lightweight mechanism for *example-based personalisation* — the composer's own sketches define the space the compiler samples from.

<small>Tags: [symbolic-generation] [controllability] [style-transfer] [toolkit] · Verification: verified (fetched Magenta blog) · Cluster 05</small>

### `neutone2024morpho` — NeutoneMorpho — Neutone Morpho / Neutone FX

*Neutone Inc. (Tokyo/London, ex-Qosmo); Neutone FX (2022) hosts community RAVE-style models; Morpho (2024) real-time tone morphing.*

Links: https://neutone.ai ; https://neutone.jp/morpho

[A][I] VST3/AU plugin running neural audio models in real time: transforms incoming audio's timbre into a trained model's (instruments, voices, textures) with dry/wet, latency compensation; SDK for artists to train/publish models on their own recordings.

**Evidence.** STARTS Prize nomination; used in electronic/experimental practice.

**For the studio.** "Insert example audio" as a *timbre* annotation is realisable with models trained on the composer's own material — an ethical audio-level counterpart to the symbolic core.

<small>Tags: [product] [audio-generation] [style-transfer] [real-time] [DAW-plugin] · Verification: partial · Cluster 08</small>

### `rouard2024musicgenstyle` — MusicGenStyle — Audio Conditioning for Music Generation via Discrete Bottleneck Features (MusicGen-Style)

*Simon Rouard, Yossi Adi, Jade Copet, Axel Roebel, Alexandre Défossez; Meta / IRCAM; ISMIR 2024.*

Links: https://arxiv.org/abs/2407.12563 ; code/weights in AudioCraft (musicgen-style)

Conditions MusicGen on an **audio excerpt's style** via a discrete bottleneck (RVQ + heavy dropout) so the model copies *style* not *content*; also compares to textual inversion; **double classifier-free guidance** balances text vs audio conditioning at inference. Weights CC-BY-NC.

**Evidence.** Automatic + human studies on style adherence vs text adherence.

**For the studio.** "Insert example audio" as an annotation channel—the composer drops in a reference track and the renderer adopts its style while keeping the composer's material.

<small>Tags: [audio-generation] [style-transfer] [multimodal-input] [controllability] · Verification: verified (abstract; authors partial) · Cluster 04</small>

## S2.1. Annotate: encodings, standards & tools

### `cannam2010sonicvisualiser` — SonicVisualiser — Sonic Visualiser: An Open Source Application for Viewing, Analysing, and Annotating Music Audio Files

*Chris Cannam, Christian Landone, Mark Sandler; Centre for Digital Music, QMUL; ACM Multimedia 2010 (software since 2007)*

Links: https://www.sonicvisualiser.org/ ; paper https://www.sonicvisualiser.org/sv2010.pdf ; https://github.com/sonic-visualiser/sonic-visualiser

Desktop tool (GPL) for annotating audio: layers of time instants, time-value curves, notes, regions and labels over waveform/spectrogram; annotations entered by clicking, *tapping* keys during playback, or MIDI input; Vamp plugins add automatic beat/onset/chord/key/segmentation layers that the user then corrects. Export to CSV, MIDI, RDF (Music Ontology).

**Evidence.** Widely used in MIR/musicology; no formal study in the paper.

**For the studio.** The reference model for *audio-anchored* annotation layers and for "auto-annotate then hand-correct" — the pattern the studio needs for reference-audio annotations (beats, chords, form).

<small>Tags: [annotation] [toolkit] [transcription] [theory-analysis] · Verification: verified (fetched primary source) · Cluster 06</small>

### `egozy2018concertcue` — ConcertCue — ConcertCue: live program-note streaming for classical concerts

*Eran Egozy (with student Nathan Gutierrez '17 and collaborators); MIT Music Technology Lab; 2017–present; Knight Foundation grant $50k (July 2018)*

Links: https://musictech.mit.edu/concertcue/ ; https://www.concertcue.com/

Mobile web app that streams time-synchronized program notes (text, images, media) to audience phones during a live performance, cued to specific musical events. Deployed at MIT ensembles, Boston Symphony Orchestra (Tanglewood and "Casual Fridays," 2017–2020), Boston Baroque, New World Symphony, Radius Ensemble, Michigan Tech.

**Evidence.** Deployments and grant; a conference paper exists (I recall a NIME 2018 paper by Egozy and Eun Young Lee) but could not be verified this session.

**For the studio.** A model for *time-aligned annotation* of a score/performance for a human reader — the same data structure the studio needs for annotations that steer AI, but pointed at audiences.

<small>Tags: [annotation] [real-time] [product] [education] · Verification: verified (project page); paper unverified · Cluster 01</small>

### `giraud2018dezrann` — Dezrann — Dezrann: a web framework to share music analysis (2018) / Interacting with Annotated and Synchronized Music Corpora on the Dezrann Web Platform (2025)

*Mathieu Giraud, Richard Groult, Emmanuel Leguy; CRIStAL (CNRS/Univ. Lille) & MIS (UPJV); TENOR 2018. Ballester, Bacot, Bigo, Borsan, … Giraud et al. (27 authors); TISMIR 2025 (DOI 10.5334/tismir.212)*

Links: https://www.dezrann.net ; https://www.tenor-conference.org/proceedings/2018/14_Giraud_tenor18.pdf ; https://transactions.ismir.net/articles/10.5334/tismir.212

Browser platform for *analytical annotation* of scores and audio: labels (type, onset, optional duration, tag/comment) are placed by left-to-right drag (span) or top-to-bottom gesture (instant, e.g., cadence) on a staff or in zones above/below the score; positions are in **symbolic musical time** (measure + beat, snapping to beat grid/onsets) so the same labels align to score, waveform and video. Stored as `.dez` JSON. GPLv3+ code, ODbL data. 2025: 10 corpora, 1,500+ pieces, 35,000+ annotations (harmony, structure, texture, form), collaborative editing.

**Evidence.** Corpus scale above; used in musicology teaching and MIR ground truth.

**For the studio.** The best existing *format and UI* for typed, time-anchored, staff-scoped score annotations that machines can read — the studio's annotation layer could adopt `.dez`-style semantics directly and add "instruction" as a label type.

<small>Tags: [annotation] [theory-analysis] [corpus] [toolkit] [notation] · Verification: verified (fetched primary sources) · Cluster 06</small>

### `goebl2023meifriend` — meiFriend — mei-friend: browser-based MEI editor with GitHub integration

*Werner Goebl, David M. Weigl et al.; mdw – University of Music and Performing Arts Vienna; 2022– (ISMIR 2023 LBD / MEC papers)*

Links: https://mei-friend.mdw.ac.at/ ; https://github.com/mei-friend/mei-friend

"Last-mile" editor: code view of MEI side-by-side with a live Verovio rendering; imports MusicXML/Humdrum/PAE/ABC, exports MEI/SVG/MIDI; **GitHub integration** (open, fork, commit encodings — version control for scores), and **Web Annotations / RDF linked-data annotations** attached to score elements.

**Evidence.** Tool paper; adoption in MEI community.

**For the studio.** Concrete precedent for (a) text ⇄ notation dual editing (a projectional-editor pattern), (b) git-based history for symbolic music, and (c) standards-based annotations anchored to notation ids.

<small>Tags: [notation] [annotation] [toolkit] [editing] · Verification: partial (site fetched; authorship/paper details from recall) · Cluster 06</small>

### `fu2026tactus` — Tactus — Opportunities to Support Musicians' Score-based Practice with Context-Specific Annotations on Tablet

*Xintian Fu, Vincent Cavez; Université Paris-Saclay / CNRS / Inria and Stanford; CHI EA 2026 (DOI 10.1145/3772363.3798332)*

Links: https://dl.acm.org/doi/10.1145/3772363.3798332 ; PDF https://www.vincentcavez.com/pdf/Tactus.pdf

Video analysis of 17 musicians' practice sessions plus 10 interviews; identifies *performance-oriented* (persistent: dynamics, bowings, breaths) vs *practice-oriented* (temporary: rhythm visualisations, accidentals, progress) annotations; proposes "context-specific annotations" that are dynamic — system feedback (performance analysis), feedforward (anticipating difficulty) and user-created dynamic marks — prototyped as the web app Tactus.

**Evidence.** N=17 videos, 10 interviews, questionnaire evaluation of feature videos (Likert).

**For the studio.** Provides a taxonomy of annotation *lifetimes* (persistent vs ephemeral) and *authors* (human vs system) that the studio's annotation layer should encode explicitly.

<small>Tags: [annotation] [HCI-study] [notation] · Verification: verified (fetched PDF) · Cluster 06</small>

### `newzik2026readers` — ReaderApps — forScore, Newzik (and nkoda, Enote): rehearsal-annotation score readers

*forScore LLC (iPad, 2010–); Newzik SAS (Paris; iOS/web; ~450k users, 150+ institutions); nkoda (subscription library); Enote (AI-digitised interactive scores)*

Links: https://forscore.co/ ; https://newzik.com/en/

PDF/MusicXML score readers with Apple-Pencil annotation (layers, stamps, fingerings, markers), setlists, page turning via pedals/face gestures. Newzik adds **LiveScores** (OMR turns PDFs into interactive MusicXML: navigation, transposition) and *real-time shared annotation sync* across an ensemble (conductor's marks propagate to players), plus MusicXML/MIDI export.

**Evidence.** Product claims; Tactus (above) studied the underlying practices.

**For the studio.** Rehearsal marks are the most common real-world "annotation on a score"; Newzik's shared-annotation model shows annotations as first-class, syncable objects separate from the score — the same separation the studio needs between human intent and compiled notation.

<small>Tags: [annotation] [product] [notation] · Verification: verified (forScore, Newzik pages fetched; nkoda/Enote partial) · Cluster 06</small>

## S2.2. Annotate: machine-proposed annotations (analysis)

### `bock2016madmom` — Key/chord estimation and phrase segmentation — the standard baselines

*Chord/key from audio: madmom (Böck et al., 2016), Korzeniowski & Widmer (ISMIR 2016/2018 CNN chord & key), Essentia/Chordino (Mauch & Dixon 2010); symbolic key: Krumhansl–Schmuckler / Temperley (music21 `analyze('key')`); melodic phrase segmentation: Cambouropoulos LBDM (2001), Pearce et al. IDyOM (2010), Guan et al. "Melodic phrase segmentation by deep neural networks" (2018); lead-sheet harmonic function labelling: Chen & Su, Hooktheory data, and "functional" chord labels in Chordonomicon*

Links: https://github.com/CPJKU/madmom ; https://github.com/mtg/essentia

Mature, mostly pre-transformer components that still power practical systems (Chordify, Moises chord detection). Symbolic phrase segmentation lacks a large shared benchmark (Essen folk phrase marks are the usual one).

**Evidence.** MIREX chord estimation plateaued ~80–85% MajMin accuracy by 2019.

**For the studio.** Off-the-shelf pieces for turning hummed/recorded input into chords and phrases before symbolic editing.

<small>Tags: [theory-analysis] [transcription] [toolkit] · Verification: partial (recalled) · Cluster 07</small>

### `finkensiep2018skipgrams` — Galant schema detection — computational Gjerdingen schemata

*Christoph Finkensiep, Markus Neuwirth, Martin Rohrmeier (EPFL; ISMIR 2018 "Generalized Skipgrams for Pattern Discovery in Polyphonic Streams"); Andreas Katsiavalos, Tom Collins, Bret Battey (ISMIR 2019, "An initial computational model for musical schemata theory"); James Symons (Music Theory Spectrum 2017, "Temporal regularity as a key to uncovering statistically significant schemas in an eighteenth-century corpus")*

Links: (ISMIR archive PDFs; not re-fetched)

Pattern-discovery and matching approaches to identify Gjerdingen's voice-leading schemata (Prinner, Romanesca, Fonte, Monte…) in encoded scores; Finkensiep et al. use skipgrams over polyphonic note streams with a hand-annotated schema dataset; Katsiavalos et al. build a prototype-matching model.

**Evidence.** Small annotated sets; precision/recall modest — schema detection remains open.

**For the studio.** Schemata are the "idioms/design patterns" of a style — a natural annotation vocabulary for style-aware compile hints (cf. arranger styles).

<small>Tags: [theory-analysis] [style-transfer] · Verification: unverified (recall; could not fetch ISMIR archive) · Cluster 07</small>

### `karystinaios2023chordgnn` — ChordGNN — Roman Numeral Analysis with Graph Neural Networks (onset-wise from note-wise)

*Emmanouil Karystinaios, Gerhard Widmer; JKU Linz; ISMIR 2023*

Links: https://arxiv.org/abs/2307.03544 ; https://github.com/manoskary/chordgnn

Represents the score as a note graph (partitura), runs a GNN over notes, then a learned edge-contraction pools note-wise features to onset-wise predictions of Roman numeral components; variants with NADE and post-processing.

**Evidence.** Reported higher accuracy than AugmentedNet on the same reference datasets (exact deltas not re-fetched). Related JKU work: cadence detection with GNNs (ISMIR 2022), voice separation (2023).

**For the studio.** Shows note-level graph representations (not piano-roll) as the right substrate for analysis — the same structure a notation editor already holds.

<small>Tags: [theory-analysis] [representation] · Verification: verified · Cluster 07</small>

### `sailor2024rnbert` — RNBert — Fine-tuning a masked language model for Roman numeral analysis

*Malcolm Sailor; Yale; ISMIR 2024 (Zenodo DOI 10.5281/zenodo.14877455)*

Links: https://github.com/malcolmsailor/rnbert

Takes MusicBERT (Zeng et al. 2021, OctupleMIDI) pretrained on large unlabeled symbolic data and fine-tunes it (with layer freezing) for key prediction and key-conditioned Roman-numeral prediction on When-in-Rome-style data; compares against AugmentedNet/ChordGNN.

**Evidence.** Reports state-of-the-art on the Roman numeral task via transfer from unlabeled pretraining (numbers not re-fetched).

**For the studio.** Demonstrates the pretrain-then-analyse recipe: one symbolic foundation model can serve both generation and annotation heads.

<small>Tags: [theory-analysis] [representation] · Verification: verified (repo) · Cluster 07</small>

### `napoleslopez2021augmentednet` — AugmentedNet — Roman numeral analysis network with synthetic training examples

*Néstor Nápoles López, Mark Gotham, Ichiro Fujinaga; McGill / Cornell; ISMIR 2021; v1.9.1 (2022 dissertation)*

Links: https://github.com/napulen/AugmentedNet ; ISMIR 2021 paper

CRNN reading MusicXML (pitch-spelling-aware encoding) and predicting 11 tonal tasks jointly (key, degree, quality, inversion, root, harmonic rhythm, pitch-class sets…) then assembling Roman numerals; trained on aggregated corpora (BPS, When-in-Rome, Haydn Sun quartets, ABC, TAVERN, WTC) plus synthetic texturisation. Outputs annotated MusicXML + CSV; MIT.

**Evidence.** Best config: 82.9% key, 67.0% scale degree, 46.4% full Roman numeral on the held-out test sets. Adopted in Sibelius (harmonic analysis), Vimu.app, MusicLang.

**For the studio.** A deployable "auto-annotate harmony" backend whose confidence is low enough that the human-in-the-loop correction step is essential — perfectly matching the annotate→edit loop.

<small>Tags: [theory-analysis] [annotation] [toolkit] · Verification: verified · Cluster 07</small>

### `nieto2016msaf` — MSAF — Music Structure Analysis Framework

*Oriol Nieto, Juan Pablo Bello; NYU; ISMIR 2016 ("Systematic exploration of computational music structure research"); v0.1.80 June 2023*

Links: https://github.com/urinieto/msaf

MIT Python framework bundling boundary algorithms (Foote, Structural Features, C-NMF, OLDA, Spectral Clustering, VMO) and labelling algorithms with mir_eval evaluation on SALAMI/Beatles/Isophonics, from audio features.

**Evidence.** The reference comparison harness for classical structure methods.

**For the studio.** Baseline section segmentation for reference audio the composer drops in as an annotation.

<small>Tags: [structure] [toolkit] [evaluation] · Verification: verified · Cluster 07</small>

### `dai2024interconnections` — StructureInterconnections — The Interconnections of Music Structure, Harmony, Melody, Rhythm, and Predictivity

*Shuqi Dai, Huan Zhang, Roger B. Dannenberg; CMU. Music & Science vol. 7, 2024 (extends "Automatic Analysis and Influence of Hierarchical Structure on Melody, Rhythm and Harmony in Popular Music", CSMC-MuMe 2020). Dai's PhD (CMU CS, advisor Dannenberg, completed 2024) centres on this structure work plus singing (SingStyle111, ISMIR 2023; ExpressiveSinger, ACM MM 2024).*

Links: https://doi.org/10.1177/20592043241234758 ; https://www.shuqid.net/

Algorithms extracting two-level (section/phrase) repetition structure from 909 Chinese pop MIDI transcriptions, then quantifying how structural position conditions harmony, pitch distributions, rhythm and predictability.

**Evidence.** 93% phrase-boundary accuracy; repeated phrases cover 50–90% of most songs; V–I at section ends 94% vs 47% elsewhere; entropy lower at boundaries; 2–3 sections per song with 1–6 phrases each.

**For the studio.** Ready-made structure analyser and priors for a "structure view" of a composition, and for compile-time sanity checks (e.g., cadence placement).

<small>Tags: [theory-analysis] [structure] [corpus] [representation] · Verification: verified (journal page) · Cluster 02</small>

### `dai2022missing` — WhatIsMissing — What Is Missing in Deep Music Generation? A Study of Repetition and Structure in Popular Music

*Shuqi Dai, Huiran Yu / Huan Zhang, Roger B. Dannenberg; Carnegie Mellon University; ISMIR 2022 ("What is missing in deep music generation? A study of repetition and structure in popular music"), JNMR 2023 ("Personalised popular music generation using imitation and structure"), plus earlier "Automatic analysis and influence of hierarchical structure on melody, rhythm and harmony in popular music" (CSMC+MuMe 2020)*

Links: https://arxiv.org/abs/2209.00182 ; PDF: https://www.cs.cmu.edu/~rbd/papers/repetition-ismir2022.pdf

Analysis of two pop datasets (Chinese and American) establishing four principles: hierarchical structure levels; song-specific repetition with limited vocabulary; interaction between structure and rhythm/melody/harmony; non-random repetition trends measurable via cross-entropy. Music from recent deep generators is analysed with the same tools and "often reveals striking differences from a structural perspective."

**Evidence.** Quantitative repetition statistics on POP909 vs. generated music; listening tests for the imitation system (details not re-fetched).

**For the studio.** Argues for explicit structural annotation (sections, repetition relations) as a first-class input to generation — exactly what the annotate step should capture. (Cross-ref: Dannenberg belongs to accompaniment/HCI clusters too.)

<small>Tags: [structure] [theory-analysis] [symbolic-generation] [controllability] · Verification: verified (arXiv page) · Clusters 02, 07</small>

### `nihahn2024schenker` — Computational Schenkerian analysis — new dataset, notation software, graph representation

*Stephen Ni-Hahn, Weihan Xu, Jerry Yin, Rico Zhu, Simon Mak, Yue Jiang, Cynthia Rudin; Duke University; ISMIR 2024 (arXiv 2408.07184). Anchored by Phillip Kirlin & David Jensen (ISMIR 2011 / JNMR 2015 probabilistic MOP models, 41 analyses)*

Links: https://arxiv.org/abs/2408.07184

Largest machine-readable Schenkerian analysis dataset (>140 excerpts vs 41 previously), custom notation software for entering/visualising reductions, and a heterogeneous-graph representation framing analysis as hierarchical graph clustering (allowing multiple voices and complex harmonic relations, beyond Kirlin's maximal outerplanar graphs).

**Evidence.** Dataset and software released; baseline models reported.

**For the studio.** Hierarchical reduction is the theory-side counterpart of the founder's "compile" (surface ← deep structure); this is the only open dataset/tooling for it.

<small>Tags: [theory-analysis] [dataset] [structure] [notation] · Verification: verified · Cluster 07</small>

### `kim2023allinone` — All-In-One — metrical and functional structure analysis on demixed audio

*Taejun Kim, Juhan Nam; KAIST; WASPAA 2023 (arXiv 2307.16425); pip `allin1`*

Links: https://arxiv.org/abs/2307.16425 ; https://github.com/mir-aidj/all-in-one

Single model on source-separated spectrograms jointly predicting beats, downbeats, section boundaries and functional labels (intro/verse/chorus/bridge/outro) using dilated neighbourhood attention; ablations show tasks mutually improve.

**Evidence.** State of the art on Harmonix Set across all four tasks with fewer parameters than prior models.

**For the studio.** One call gives the structural skeleton of a reference track — the scaffold onto which a "compile" can map sections.

<small>Tags: [structure] [transcription] · Verification: verified · Cluster 07</small>

### `chen2021attend` — Chen & Su — Functional harmony recognition and "Attend to Chords" (Harmony Transformer)

*Tsung-Ping Chen, Li Su; Academia Sinica, Taipei; ISMIR 2018 ("Functional harmony recognition of symbolic music data with multi-task recurrent neural networks"), ISMIR 2019 (Harmony Transformer), TISMIR 2021 ("Attend to Chords…", DOI 10.5334/tismir.65)*

Links: https://doi.org/10.5334/tismir.65

Multi-task RNN then Transformer encoder-decoder that jointly segments chord regions and labels key/Roman numerals from symbolic (BPS-FH) or audio input; introduced the Beethoven Piano Sonata Functional Harmony (BPS-FH) dataset.

**Evidence.** TISMIR paper shows Transformer-based models outperform RNN baselines on chord symbol and Roman-numeral recognition on BPS-FH.

**For the studio.** Established the segmentation+labelling framing of functional harmony analysis that later models adopt.

<small>Tags: [theory-analysis] · Verification: verified (Crossref record) · Cluster 07</small>

### `huang2005palestrinapal` — Counterpoint / voice-leading rule checkers

*music21 `voiceLeading` module (VoiceLeadingQuartet: parallel fifths/octaves, hidden intervals, voice crossing — Cuthbert lab); Palestrina Pal (Jonathan Huang & Elaine Chew, 2005); species-counterpoint solvers/checkers in Strasheela (Anders & Miranda), and LLM-era checkers used as reward functions (e.g., rule-based critics in 2024–25 RL fine-tuning of Bach-style generators)*

Links: https://music21.org/music21docs/moduleReference/moduleVoiceLeading.html

Deterministic rule engines that flag voice-leading errors in SATB/species exercises; used pedagogically and as constraints/rewards for generation.

**Evidence.** No large comparative benchmark; rule sets vary by textbook.

**For the studio.** Cheap, explainable "linters" for the compile output — the software-engineering analogy the founder will appreciate (compiler warnings for parallel fifths).

<small>Tags: [theory-analysis] [education] [toolkit] · Verification: partial (music21 module recalled; others unverified) · Cluster 07</small>

## S2.3. Annotate: control vocabularies

### `tan2022melodyinfilling` — StructuralMelodyInfilling — Melody Infilling with User-Provided Structural Context

*Chih-Pin Tan, Alvin W. Y. Su, Yi-Hsuan Yang (NCKU / Academia Sinica); ISMIR 2022*

Links: https://arxiv.org/abs/2210.02829 ; code: https://github.com/tanchihpin0517/structure-aware_infilling

Transformer that fills a missing melody segment given past/future context *and* user-provided structural information (e.g., which earlier phrase the gap should echo), via an attention-selecting module, so the fill respects form rather than only local smoothness.

**Evidence.** Objective and subjective results show structure-conditioned fills beat structure-agnostic baselines on pop melodies.

**For the studio.** Infilling that takes *form annotations* ("this is the return of A") as input — precisely the annotate→compile pattern.

<small>Tags: [infilling] [structure] [annotation] [symbolic-generation] · Verification: verified (arXiv abstract fetched; authors from knowledge) · Cluster 03</small>

### `vonrutte2023figaro` — FIGARO — FIGARO: Generating Symbolic Music with Fine-Grained Artistic Control

*Dimitri von Rütte, Luca Biggio, Yannic Kilcher, Thomas Hofmann (ETH Zürich); ICLR 2023 (arXiv Jan 2022)*

Links: https://arxiv.org/abs/2201.10936 ; code: https://github.com/dvruette/figaro

"Description-to-sequence": a per-bar description made of *expert* features (instruments present, chords, time signature, note density, mean pitch, mean velocity, mean duration) plus *learned* VQ-VAE codes conditions a seq2seq Transformer that emits REMI+ (multi-track REMI) tokens. A composer can write or edit the bar-by-bar description (change chords, add an instrument, raise density) and regenerate; also enables style transfer by swapping learned codes.

**Evidence.** SOTA controllable generation on Lakh MIDI; generalises to out-of-distribution descriptions.

**For the studio.** Bar-level description = a formal annotation language; FIGARO is the closest to "annotate bars with chords/density/instrumentation, then compile".

<small>Tags: [controllability] [symbolic-generation] [style-transfer] [annotation] [representation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `young2021compositionalsteering` — CompositionalSteering — Compositional Steering of Music Transformers

*Halley Young, Vincent Dumoulin, Pablo Samuel Castro, Jesse Engel, Cheng-Zhi Anna Huang; Google Brain / UPenn; HAI-GEN Workshop at ACM IUI 2021*

Links: listed on https://czhuang.github.io/ ; workshop: https://hai-gen.github.io/2021/

Steers a pretrained Music Transformer at sampling time by *composing* several lightweight attribute controls (e.g., pitch-range, density, key) into one product-of-experts-style distribution, so users can combine constraints without retraining the base model.

**Evidence.** Workshop paper; quantitative attribute-adherence results (details not re-verified).

**For the studio.** A route to letting many simultaneous annotations ("keep this in the low register, denser here, stay in D minor") jointly constrain a compile step on a frozen model.

<small>Tags: [controllability] [symbolic-generation] [annotation] · Verification: partial (title/venue verified via homepage; method from recall) · Cluster 01</small>

## S2.4. Annotate: multimodal annotation as instruction

### `elkins2025dawzy` — DAWZY — DAWZY: A New Addition to AI-powered "Human in the Loop" Music Co-creation

*Aaron C. Elkins, Sawyer Blankenship, Sanchit Singh, Uyiosa Philip Amadasun, Adrian Kieback, Aman Chadha; San Diego State University; arXiv Dec 2025*

Links: https://arxiv.org/abs/2512.03289

Open-source voice-first assistant for REAPER. Natural-language requests (text, voice, or hum) are converted by an LLM into *reversible* DAW actions: three MCP tools (state query, parameter adjustment, beat generation), atomic scripts with undo. A minimal chat box replaces menu navigation; the DAW remains the workspace.

**Evidence.** N=21 user study; MOS (1–5): enjoyment 4.48, learning 4.38, collaboration 4.29, usability 4.14, control 3.81.

**For the studio.** A concrete "voice-controlled DAW" reference with the right architecture for the studio's edit step — LLM emits *reversible code* against the host application's API (a compile-to-actions pattern), and control was the lowest-rated dimension, flagging the need for direct-manipulation fallbacks.

<small>Tags: [LLM-agent] [DAW-plugin] [HCI-study] [multimodal-input] [music-as-code] · Verification: verified (fetched primary source) · Cluster 06</small>

### `tilekbay2024expressedit` — ExpressEdit — ExpressEdit: Video Editing with Natural Language and Sketching

*Bekzat Tilekbay, Saelyne Yang, Michal Lewkowicz (Yale), Alex Suryapranata, Juho Kim; KAIST KIXLAB (+ Yale). ACM IUI 2024 (also HAI-GEN 2024 workshop). **Not CMU.***

Links: https://arxiv.org/abs/2403.17693 ; https://doi.org/10.1145/3640543.3645164 ; https://expressedit.kixlab.org/ ; code: https://github.com/fesiib/video-editing-pipeline ; demo video: https://youtu.be/t16Se9rNLLQ

Editing informational videos by **describing an edit in natural language and sketching on a video frame** (rectangles/free-form marks marking regions) — the timeline is used for positional references and for adjusting results. Pipeline: GPT-4 **parses the command into four reference types — temporal ("whenever he discusses tips"), spatial ("top-left", or the sketch), edit operation, and parameters**; temporal references are resolved positionally (timecodes), against the transcript, or against dense visual captions (BLIP-2/InternVideo) via SentenceTransformer similarity (top-10 segments); spatial references are resolved by Segment-Anything instance crops matched to the text/sketch in CLIP space; operation/parameter references handle explicit, relative and abstract directives. Output is a set of **edit suggestions** (7 operations: text, image, shape, cut, zoom, crop, blur) the user can accept, reject, or manually adjust (span on timeline, position/size on canvas, parameters), with an **"Examine" panel** showing how each reference was interpreted.

**Evidence.** Formative study N=10 editors, 176 multimodal edit requests (all had NL; 78/97 visual ones were sketches on frames). Pipeline accuracy on 50 ground-truth commands: temporal recall 0.68, spatial mIoU 0.56, operation F1 0.82. User study N=10 novices, 40-min task: 5.2 multimodal commands, 9.3 requests incl. iterations, 16.6 final edits; **45.98% of suggestions accepted; 58.09% of final edits were modified suggestions**; time split ~31% ideating/describing, 33% examining, 35% manual editing; SUS 75.7; creativity support 5.7/7; Examine feature rated 6.1/7. Sketches appeared in 26% of commands and simplified spatial specification; vague commands failed; users wanted animation/transitions/audio ops and multi-frame sketching.

**For the studio.** The best worked template for **multimodal annotation-driven editing**: a *reference-type grammar* (when / where / what / how) that a music version can copy almost verbatim (temporal → bars/beats/sections or "the second time the chorus comes", spatial → staff/voice/register, operation → reharmonise/thin/transpose/add counter-line, parameters → "brighter", "like the reference clip"); resolvers per modality (score search, audio-similarity for example clips, sketch → contour/region); and — crucially — *inspectable, editable suggestions* rather than silent rewrites. No music-specific ExpressEdit exists yet; the closest music analogues are Draw and Listen! (sketch→melody inpainting, below) and Amuse (multimodal→chords, no sketch, no spatial targeting).

<small>Tags: [annotation] [sketch] [multimodal-input] [editing] [LLM-agent] [HCI-study] [video] [mixed-initiative] · Verification: verified (arXiv HTML full text; project page) · Clusters 02, 06</small>

### `thisgoober2026real` — REAL — REAL Pipeline (GitHub: This-Goober/REAL)

*GitHub user "This-Goober" (self-described two-person student team; the account's other repos are music-related — "ré.ai", a personal site of a young violinist, and "TUNE", a violin-intonation pitch-analysis "skill"). Public repo, MIT licence, 0 stars; batch-1 field sessions dated 2026-08. **No acronym expansion is given anywhere in the repo; no paper exists.***

Links: https://github.com/This-Goober/REAL ; demo video: https://www.youtube.com/watch?v=Oz6rBUQU4j8 ; live storyboard demo: https://this-goober.github.io/REAL/skills/batch-1/outputs/STORYBOARD-segment.html

An AI-assisted **video** (not music) editing pipeline implemented as four **Claude skills** (Claude apps / Claude Code) whose stance is "an AI agent acting as a production crew for a human director … the human makes every creative call; the agent does the bookkeeping and refuses to guess." Steps: `/real-brainstorm` (idea/script → NOTEBOOK.md + SHOTLIST.md), `/real-create-catalogue` (footage folder → approved renames + `asset-catalog.json`, with dHash near-duplicate detection that *asks the creator* in the uncertain band), `/real-storyboarding` (→ interactive review page + `reel.json`, the single authoritative edit; every timing badged `estimated` or `measured`), `/real-compile` (`reel.json` → validated `.fcpxml` for Final Cut Pro; "zero editorial decisions"). Core idea: **word anchors** — "the word is the identity, the timestamp is derived": placements are pinned to spoken words and timestamps are re-derived at compile time from a measured clock (ffmpeg `silencedetect` on the narration; forced alignment planned). Requires macOS + Final Cut Pro, Python 3.10+, ffmpeg; rendering is deliberately out of scope (output is an editable timeline). Status: batch 1 field-tested on real reels; batch 2 rebuilt, 21/21 synthetic regression checks; a "capability journal" with one entry (word-anchor snapping).

**Evidence.** Self-reported measurements only: estimated clock 7% long overall but 28% long on one beat; cue offsets of −1.7 s / −1.05 s under estimation; 22 placements silently dropped by a batch-1 translator; cloud connectors ~350k tokens/MB. Key stated finding: "A random error looks like noise. A coherent error reads as an editorial fact."

**For the studio.** Not a research contribution and not about music, but a vocabulary and architecture twin of the founder's loop (brainstorm → catalogue → storyboard → **compile**, human as director, agent as crew) built on the same agentic tooling the studio might use. Transferable design rules: one owner per decision; one authoritative machine-readable artefact (`reel.json` ↔ an annotated score file); anchors on semantic events (word ↔ beat/bar/note) with derived timing; loud refusal on anything not representable; badge estimated vs measured. If the founder listed it as *music* related, that is a misattribution — only the owner's sibling repos (TUNE) are musical.

<small>Tags: [LLM-agent] [video] [editing] [toolkit] [co-creation-framework] [product] · Verification: verified (README, journal, gap report fetched raw; GitHub profile) · Cluster 02</small>

## S2.5. Annotate: economics of human labelling

### `bukey2024justlabel` — JLTR — Just Label the Repeats for In-The-Wild Audio-to-Score Alignment

*Irmak Bukey, Michael Feffer, Chris Donahue; CMU. ISMIR 2024.*

Links: https://arxiv.org/abs/2411.07428 ; code: https://github.com/irmakbky/jltr-alignment

Offline alignment of real performance audio to *scanned sheet music*: improved score features (measure detection) and audio features (raw onset probabilities from a transcription model), plus a **clickable UI where the human labels repeat signs and jumps** instead of relying on automatic detection.

**Evidence.** Measure-level alignment accuracy 33% → 82% (150% relative) over prior methods.

**For the studio.** Concrete evidence that a tiny, well-chosen human annotation beats automation; also the plumbing for aligning reference recordings to the score the composer is editing.

<small>Tags: [annotation] [notation] [transcription] [structure] [HCI-study] · Verification: verified (arXiv page) · Cluster 02</small>

## S3.1. Compile: symbolic representations & tokenizers

### `walshaw2011abc` — ABC-abcjs — ABC notation (standard 2.1) and abcjs

*Chris Walshaw (ABC, 1991; standard v2.1 Dec 2011); abc2midi/abcm2ps (James Allwright; Jef Moine); abcjs: Paul Rosen (v6.6.3, Apr 2026)*

Links: https://abcnotation.com/wiki/abc:standard:v2.1 ; https://github.com/paulrosen/abcjs

ABC: plain-text tune format (header fields X:, T:, M:, L:, K:; body of note letters with duration/pitch modifiers); abc2midi compiles to MIDI, abcm2ps to PostScript/SVG. abcjs renders ABC to SVG in the browser, synthesises playback, and provides a *live editor* that re-renders on every keystroke (text ⇄ score).

**Evidence.** ABC is the dominant text IR in recent music LLMs (ChatMusician, NotaGen, GPT-4 experiments).

**For the studio.** A compact, LLM-friendly textual score language with an existing compile chain (text → MIDI/SVG) and live re-render — the most practical "source code" candidate for the studio's compile step, at the cost of weaker support for complex polyphony/layout than MusicXML/MEI.

<small>Tags: [representation] [music-as-code] [notation] [toolkit] · Verification: verified (fetched primary sources) · Cluster 06</small>

### `huron1995humdrum` — Humdrum — Humdrum and the **kern representation

*David Huron (1990s); Humdrum Toolkit; humlib / Verovio Humdrum Viewer (Craig Sapp)*

Links: https://www.humdrum.org/ ; https://www.humdrum.org/guide/ch01/ ; https://verovio.humdrum.org

Tab-separated "spines" (columns per voice/data type) × rows (successive time points) in plain text; **kern encodes pitch/duration/rests/barlines; 70+ Unix-style tools composable via pipes; users add custom spines (e.g., **harm for Roman numerals, **text, **dynam) — i.e., *annotations are just parallel columns*.

**Evidence.** Long-standing basis for corpora (KernScores, Bach chorales) and now the OMR target of Sheet Music Transformer.

**For the studio.** Humdrum's spine model is an elegant way to store aligned human annotations next to notes in one text file that both LLMs and tools can consume; the "annotation spine" is a ready-made design.

<small>Tags: [representation] [annotation] [toolkit] [theory-analysis] · Verification: verified (fetched primary source) · Cluster 06</small>

### `dong2023mmt` — MMT — Multitrack Music Transformer

*Hao-Wen Dong, Ke Chen, Shlomo Dubnov, Julian McAuley, Taylor Berg-Kirkpatrick (UC San Diego); ICASSP 2023*

Links: https://arxiv.org/abs/2207.06983 ; code: https://github.com/salu133445/mmt ; demo: https://salu133445.github.io/mmt/

Each note is one 6-tuple event (type, beat, position, pitch, duration, instrument) with multi-head output, giving 2.6–3.5× more music per token than MMM/REMI+ and fast inference; 64 instruments; trained on the Symbolic Orchestral Database (5,743 pieces). Modes: unconditioned, *instrument-informed* (user lists instruments) and n-beat continuation; no infilling. Includes attention analysis (consonant intervals, aligned beats).

**Evidence.** Competitive quality with large speed/memory gains; suitable for real-time creative tools.

**For the studio.** Efficient multi-track/orchestral representation; instrument-specification is a basic orchestration control.

<small>Tags: [symbolic-generation] [representation] [controllability] [real-time] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `zeng2021musicbert` — Octuple/MusicBERT + MidiBERT-Piano — MusicBERT: Symbolic Music Understanding with Large-Scale Pre-Training; BERT-like Pre-training for Symbolic Piano Music Classification Tasks

*Mingliang Zeng, Xu Tan, Rui Wang, et al. (Microsoft Research Asia); ACL 2021 Findings. MidiBERT-Piano: Yi-Hui Chou, I-Chun Chen, Chin-Jui Chang, Joann Ching, Yi-Hsuan Yang (Academia Sinica); arXiv 2021, Journal of Creative Music Systems 2024*

Links: https://arxiv.org/abs/2106.05630 ; https://github.com/microsoft/muzic ; https://arxiv.org/abs/2107.05223 ; https://github.com/wazenmai/MIDI-BERT

MusicBERT introduces *OctupleMIDI*, an 8-field token per note (bar, position, instrument, pitch, duration, velocity, time signature, tempo) and bar-level masking, pre-trained on >1M MIDI songs; downstream melody completion, accompaniment suggestion, genre and style classification. MidiBERT-Piano compares REMI vs Compound-Word inputs for BERT pre-training on piano MIDI, with note-level (melody extraction, velocity) and sequence-level (composer, emotion) tasks. Both are *understanding* models, not generators.

**Evidence.** MusicBERT beats non-pretrained baselines on all four tasks; MidiBERT beats RNN baselines on four classification tasks.

**For the studio.** Understanding models are needed for the "annotate" step (auto-labelling melody/track roles, style, emotion) and Octuple is the compact multi-track note representation used by many later systems.

<small>Tags: [representation] [theory-analysis] [dataset] · Verification: verified (arXiv abstracts fetched) · Cluster 03</small>

### `w3c2021musicxml40` — MusicXML-MNX — MusicXML 4.0 and MNX (W3C Music Notation Community Group)

*W3C Music Notation Community Group (co-chairs incl. Adrian Holovaty; MusicXML editor Karim Ratib from 2026); MusicXML 4.0 Final Community Group Specification 1 June 2021; MNX in active specification-working-group meetings through Aug 2026*

Links: https://www.w3.org/2021/06/musicxml40/ ; https://www.w3.org/community/music-notation/ ; MNX spec at https://mnx.formats.music

MusicXML: the interchange standard for notation (250+ applications), XML, W3C CG FSA licence. MNX: the successor designed as JSON (`.mnx.json` decided Mar 2026; top-level `mnx` key; IDs up to 256 ASCII chars for app interop) with explicit semantic vs. visual separation; as of the 25 Aug 2026 working-group minutes the group was still settling core encoding (e.g., per-part maximum staves/ossia handling, integer vs float numerics) — **MNX is not yet a finished, widely implemented standard in 2026**.

**Evidence.** Standards documents and meeting minutes.

**For the studio.** Interchange must be MusicXML 4.0 today; MNX's JSON design and id discipline are worth tracking (and its unfinished state means a studio-internal JSON model is justified), but annotations beyond `<direction>` text are out of scope for both — hence the need for a separate annotation layer.

<small>Tags: [representation] [notation] · Verification: verified (fetched W3C pages/minutes) · Cluster 06</small>

### `hsiao2021compoundword` — CPWord — Compound Word Transformer: Learning to Compose Full-Song Music over Dynamic Directed Hypergraphs

*Wen-Yi Hsiao, Jen-Yu Liu, Yin-Cheng Yeh, Yi-Hsuan Yang (Taiwan AI Labs / Academia Sinica); AAAI 2021*

Links: https://arxiv.org/abs/2101.02402 ; code: https://github.com/YatingMusic/compound-word-transformer

Groups co-occurring tokens into a "compound word" per time step, split into a *note* family (pitch, duration, velocity) and a *metric* family (position/bar, tempo, chord), each predicted by its own head with type-specific embedding sizes. Cuts sequence length several-fold so full pop-piano songs (~10k REMI tokens) fit in a linear Transformer.

**Evidence.** 5–10× faster training convergence than REMI with comparable quality; enables full-song generation.

**For the studio.** Shows that a structured, typed token (rather than a flat stream) is both faster and more musically legible — a good target format for a studio's internal representation and for MidiTok's CPWord implementation.

<small>Tags: [representation] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `huang2020popmusictransformer` — REMI / PopMusicTransformer — Pop Music Transformer: Beat-based Modeling and Generation of Expressive Pop Piano Compositions

*Yu-Siang Huang, Yi-Hsuan Yang (Taiwan AI Labs / Academia Sinica); ACM Multimedia 2020*

Links: https://arxiv.org/abs/2002.00212 ; code: https://github.com/YatingMusic/remi

Introduces REMI ("revamped MIDI-derived events"): Bar, Position (16/bar), Tempo, Chord (60 types), Note-On, Note Velocity (32), Note Duration tokens — imposing a metrical grid so the Transformer-XL "knows" where beats and bars are. Trained on transcribed pop piano; generates from scratch or continues a prompt. Chord and tempo tokens are explicit and can be seeded, but there is no infilling.

**Evidence.** Objective beat/downbeat salience metrics and a listening study show better rhythmic and harmonic coherence than MIDI-like tokens.

**For the studio.** REMI (and REMI+) is the de-facto default MIDI tokenization (MidiTok, FIGARO, Text2midi); bar/position/chord tokens are exactly the anchors a bar-level annotation system needs.

<small>Tags: [representation] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

## S3.2. Compile: infilling & constrained regeneration

### `papadopoulos2016flowcomposer` — FlowComposer — Assisted Lead Sheet Composition using FlowComposer (Flow Machines / "Daddy's Car")

*Alexandre Papadopoulos, Pierre Roy, François Pachet; Sony CSL Paris; CP 2016 (22nd Int. Conf. on Principles and Practice of Constraint Programming), Toulouse*

Links: https://www.francoispachet.fr/wp-content/uploads/2021/01/roy-16b.pdf ; "Daddy's Car" (Carré, Pachet, Ghedini 2016) https://www.youtube.com/watch?v=LSHZ_b05W7o

Web lead-sheet editor: the user picks a style corpus (from >12,000 lead sheets), enters partial melody and/or chords, and the system fills in the rest using Markov chains with regular (metrical) constraints; the user can select any region and regenerate only that fragment, with sliders for harmonic conformance, "inspiration" from the current piece vs corpus, note duration and chord-change rate.

**Evidence.** Deployed in professional projects (Benoît Carré's album incl. "Daddy's Car"; three songs for the musical *Beyond the Fence*, London 2016). Observed usage: composers rarely generate more than 8 bars at a time; they use it for fragments inside longer human compositions.

**For the studio.** The closest 2016 precedent for the founder's loop — symbolic lead sheet, partial human input, constrained regeneration of selected regions, style-by-corpus. Its usage data (short fragments, lock-and-regenerate) are design priors.

<small>Tags: [symbolic-generation] [infilling] [editing] [controllability] [notation] [style-transfer] [history] · Verification: verified (fetched CP 2016 PDF) · Cluster 05</small>

### `lv2023getmusic` — GETMusic — GETMusic: Generating Any Music Tracks with a Unified Representation and Diffusion Framework

*Ang Lv, Xu Tan, Peiling Lu, et al. (Renmin University / Microsoft Research Asia); arXiv 2023*

Links: https://arxiv.org/abs/2305.10841 ; code: https://github.com/microsoft/muzic/tree/main/getmusic

*GETScore* stacks tracks vertically and time horizontally, two rows (pitch, duration) per track; *GETDiff* is a discrete diffusion model trained to denoise masked target tracks given intact source tracks, so any of the 665 source→target combinations over six tracks (bass, drums, guitar, piano, strings, melody) — and zero-shot infilling of arbitrary masked cells — work from one model.

**Evidence.** Beats PopMAG and Museformer on chord accuracy and distribution metrics; 10 music-trained raters, κ>0.6.

**For the studio.** "Give me a bass line for these tracks / fill bars 9–12 of the guitar" as a single masked-denoising operation on a track×time grid — a natural fit for a multi-track score editor.

<small>Tags: [infilling] [accompaniment] [symbolic-generation] [representation] · Verification: verified (arXiv PDF fetched; author list from knowledge) · Cluster 03</small>

### `pati2019inpaintnet` — InpaintNet — Learning to Traverse Latent Spaces for Musical Score Inpainting

*Ashis Pati, Alexander Lerch, Gaëtan Hadjeres (Georgia Tech / Sony CSL); ISMIR 2019*

Links: https://arxiv.org/abs/1907.01164 ; code: https://github.com/ashispati/InpaintNet

VAE-RNN that, given the measures before and after a gap in a monophonic melody, generates a path through the VAE latent space to produce the missing measures — explicitly framed as a tool for interactive composition (fill a hole, keep both sides).

**Evidence.** Objective metrics and listening test vs. baselines; latent-space traversal was viable and coherent.

**For the studio.** Early monophonic melody infilling with past/future context; motivates latent-space editing as a complement to token infilling.

<small>Tags: [infilling] [editing] [symbolic-generation] · Verification: verified (arXiv abstract fetched; authors from knowledge) · Cluster 03</small>

### `huang2017coconet` — Coconet — Counterpoint by Convolution

*Cheng-Zhi Anna Huang, Tim Cooijmans, Adam Roberts, Aaron Courville, Douglas Eck; Google Brain / Université de Montréal; ISMIR 2017 (arXiv 1903.07227)*

Links: https://arxiv.org/abs/1903.07227 ; code in Magenta: https://github.com/magenta/magenta/tree/main/magenta/models/coconet

A convolutional model over a piano-roll of four voices (JSB chorales) trained as an orderless NADE to *complete partial scores*: any subset of notes can be masked and re-sampled. Generation uses blocked Gibbs sampling as "an analogue to rewriting." Input: a partial score with arbitrary masks; output: completed four-voice counterpoint. The human controls *which* cells are fixed vs. regenerated, in any order.

**Evidence.** Gibbs sampling beat ancestral sampling on both log-likelihood and human evaluation; abstract states this is because some conditional distributions are poorly modelled. The abstract's framing: "human composers write music in a nonlinear fashion, scribbling motifs here and there, often revisiting choices previously made."

**For the studio.** The canonical *infilling-as-editing* model: the composer authors some material, leaves holes, and the model "compiles" the rest; then the composer re-masks and re-runs. Directly underlies the Bach Doodle and Cococo.

<small>Tags: [symbolic-generation] [infilling] [editing] [notation] [controllability] · Verification: verified (arXiv abstract fetched; authors/venue from Huang's homepage) · Clusters 01, 03</small>

### `chang2021xlnet` — XLNetInfill — Variable-Length Music Score Infilling via XLNet and Musically Specialized Positional Encoding

*Chin-Jui Chang, Chun-Yi Lee, Yi-Hsuan Yang (NTHU / Academia Sinica); ISMIR 2021*

Links: https://arxiv.org/abs/2108.05064 ; code: https://github.com/reichang182/variable-length-piano-infilling

Adapts XLNet's permutation LM to fill a gap of *variable* length (up to 128 notes) in polyphonic piano scores given past and future context, with a relative-bar positional encoding and look-ahead onset prediction so the fill lands on the right beat.

**Evidence.** Objective metrics and human evaluation outperform prior infilling baselines; handles variable gap lengths that fixed-length models cannot.

**For the studio.** Shows how to infill when the composer deletes an arbitrary span and the number of notes is unknown — a common editing case.

<small>Tags: [infilling] [editing] [symbolic-generation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `zhouzheng2025midirwkv` — MIDI-RWKV — Adaptable Symbolic Music Infilling with MIDI-RWKV (a.k.a. Personalizable Long-Context Symbolic Music Infilling with MIDI-RWKV)

*Christian Zhou-Zheng, Philippe Pasquier (SFU Metacreation Lab); arXiv Jun 2025 (v2)*

Links: https://arxiv.org/abs/2506.13001 ; code/weights: https://github.com/christianazinn/MIDI-RWKV

Compact foundation model on the linear-time RWKV-7 architecture for multi-track, long-context, controllable infilling that can run on edge devices; introduces *state tuning* (fine-tuning only the initial recurrent state) for style personalisation from a handful of a composer's own files. Explicitly framed around iterative refinement of existing work rather than from-scratch generation.

**Evidence.** 31-page evaluation (17 tables) against prior infilling models; open code and weights (CC-BY 4.0).

**For the studio.** Addresses two studio requirements at once — local/offline inference and personalisation to the composer's own style with very little data.

<small>Tags: [infilling] [editing] [style-transfer] [controllability] [symbolic-generation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `ippolito2018infilling` — InfillingPiano — Infilling Piano Performances

*Daphne Ippolito, Anna Huang, Curtis Hawthorne, Douglas Eck; Google Brain; NeurIPS 2018 Workshop on Machine Learning for Creativity and Design*

Links: listed on https://czhuang.github.io/ ; workshop: https://neurips2018creativity.github.io/

Extends Music Transformer-style performance modelling to *fill in a missing middle section* of an expressive piano performance given the surrounding context, i.e. infilling in the performance-MIDI (event-token) domain rather than the piano-roll domain of Coconet. A companion workshop paper ("Transformer-NADE for Piano Performances", same venue) explores orderless training for the same goal.

**Evidence.** Workshop paper; qualitative examples.

**For the studio.** Shows that the "leave a hole, let the AI compile it" operation extends to expressive timing/velocity data, not just notes — relevant when the studio edits *performances* rather than scores.

<small>Tags: [symbolic-generation] [infilling] [editing] [expression-performance] · Verification: partial (title/venue from Huang's homepage; content from recall) · Cluster 01</small>

### `hadjeres2017deepbach` — DeepBach — DeepBach: a Steerable Model for Bach Chorales Generation

*Gaëtan Hadjeres, François Pachet, Frank Nielsen (Sony CSL Paris / LIP6 / École Polytechnique); ICML 2017*

Links: https://arxiv.org/abs/1612.01010 ; code: https://github.com/Ghadjeres/DeepBach

Four-voice chorale model (bidirectional LSTMs per voice) sampled by pseudo-Gibbs resampling of individual notes, so a user can *fix* any notes, rhythms or cadences/fermatas and regenerate the rest — implemented as a MuseScore plugin where the composer selects a region and asks for re-harmonisation. Inputs: a partial or complete chorale plus constraints; outputs: a complete chorale.

**Evidence.** Discrimination test with ~1,270 participants: DeepBach outputs were judged "Bach" nearly as often as real chorales; experts fooled at high rates.

**For the studio.** The original *steerable, notation-editor-integrated* symbolic model — the earliest concrete instance of "edit in the score, regenerate the rest".

<small>Tags: [symbolic-generation] [infilling] [editing] [notation] [controllability] [history] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `ens2020mmm` — MMM — MMM: Exploring Conditional Multi-Track Music Generation with the Transformer

*Jeff Ens, Philippe Pasquier (Metacreation Lab, Simon Fraser University); arXiv 2020*

Links: https://arxiv.org/abs/2008.06048 ; demo/code: https://github.com/jeffreyjohnens/MMM ; https://jeffreyjohnens.github.io/MMM/

GPT-2-style model over a *MultiTrack* representation in which each track's bars are serialised as their own time-ordered sequence and tracks are concatenated (so a whole track or single bar can be masked and regenerated — the *BarFill* variant). Users control which tracks/bars to (re)generate, instrument per track and note-density level; an interactive interface targets iterative composition.

**Evidence.** Qualitative/interactive demonstration; became the basis of MIDI-GPT.

**For the studio.** The origin of bar×track infilling with attribute controls, the operation a symbolic studio most needs; representation is in MidiTok.

<small>Tags: [infilling] [editing] [controllability] [symbolic-generation] [representation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `thickstun2024anticipatory` — AMT — Anticipatory Music Transformer

*John Thickstun, David Hall, Chris Donahue, Percy Liang; Stanford CRFM. arXiv June 2023; TMLR 2024.*

Links: https://arxiv.org/abs/2306.08620 ; code: https://github.com/jthickstun/anticipation ; blog: https://crfm.stanford.edu/2023/06/16/anticipatory-music-transformer.html ; co-composition blog: https://crfm.stanford.edu/2024/08/06/co-composition.html

"Anticipation": a controllable generative model of an event process conditioned *asynchronously* on a correlated control process, implemented by interleaving control tokens shortly before the events they constrain. For symbolic music the controls are a subset of the notes themselves, so the same model does prompted continuation, **span infilling**, and **accompaniment given a fixed part**. Trained on Lakh MIDI (released checkpoints in several sizes, ~128M–780M per repo — unverified here).

**Evidence.** Matches autoregressive models on prompted generation; human evaluators rated anticipatory accompaniments similar in musicality to human-composed music over 20-s clips.

**For the studio.** The generative primitive for "compile": the human pins arbitrary notes/parts (the controls), the model fills the remainder; controls can be sparse or dense and live anywhere in time, which is exactly what score-level annotations produce. Underlies Hookpad Aria and MIDInfinite.

<small>Tags: [symbolic-generation] [infilling] [controllability] [accompaniment] [representation] · Verification: verified (arXiv abstract) · Clusters 02, 03</small>

### `min2023polyffusion` — Polyffusion — Polyffusion: A Diffusion Model for Polyphonic Score Generation with Internal and External Controls

*Lejun Min, Junyan Jiang, Gus Xia, Jingwei Zhao (NYU Shanghai / MBZUAI / NUS); ISMIR 2023*

Links: https://arxiv.org/abs/2307.10304 ; code: https://github.com/aik2mlj/polyffusion

Image-diffusion over 8-bar piano-roll segments (POP909). *Internal control* = inpainting masks (keep melody, fill accompaniment; fill arbitrary regions; iterate for long form); *external control* = cross-attention on chord or texture embeddings from pre-trained encoders. One model covers melody→accompaniment, accompaniment→melody, arbitrary segment inpainting and chord/texture-conditioned arrangement.

**Evidence.** 36-participant listening study on creativity/naturalness/musicality; significantly beats Transformer and sampling baselines on most metrics; 0 invalid notes in 160 samples.

**For the studio.** Cleanly separates "what to keep" (mask) from "what to steer" (condition), which maps onto annotation types; piano-roll masks correspond to region selection in a score editor.

<small>Tags: [infilling] [controllability] [accompaniment] [symbolic-generation] [representation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `malandro2023composersassistant` — ComposersAssistant — Composer's Assistant: An Interactive Transformer for Multi-Track MIDI Infilling; Composer's Assistant 2: Interactive Multi-Track MIDI Infilling with Fine-Grained User Control

*Martin E. Malandro (Sam Houston State University); ISMIR 2023 and ISMIR 2024*

Links: https://arxiv.org/abs/2301.12525 ; https://arxiv.org/abs/2407.14700 ; code/plugin: https://github.com/m-malandro/composers-assistant-REAPER

T5-style encoder–decoder (d=384, 10+10 layers) that fills arbitrary deleted *track-measures* in a multi-track MIDI project, wired into REAPER via scripts: the composer creates empty MIDI items on named tracks to indicate what to generate. v1 controls: per-track mono/poly tokens and implicit chord/rhythm conditioning via temporary guide tracks. v2 adds two rhythmic-conditioning modes, horizontal and vertical note-onset density, several pitch controls (range etc.) and a "rhythmic interest" control. Trained only on permissively-licensed MIDI.

**Evidence.** v1 listening test N=25 (rankings); v2 shows large objective gains and a listening study finding AI-completed excerpts rated comparably to fully human ones.

**For the studio.** The most complete existing example of DAW-embedded, composer-driven multi-track infilling with fine-grained controls — essentially a prototype of the studio's "compile the missing parts" step.

<small>Tags: [infilling] [editing] [controllability] [DAW-plugin] [co-creation-framework] [symbolic-generation] · Verification: verified (arXiv PDFs fetched) · Cluster 03</small>

### `malandro2024composersassistant2` — ComposersAssistant2 — Composer's Assistant 2: Interactive Multi-Track MIDI Infilling with Fine-Grained User Control

*Martin E. Malandro, Sam Houston State University; CA1 ISMIR 2023 (arXiv 2301.12525), CA2 ISMIR 2024 (arXiv 2407.14700).*

Links: https://arxiv.org/abs/2407.14700 ; https://github.com/m-malandro/composers-assistant-REAPER (CC BY 4.0)

[S][I] T5-like transformer for **multi-track MIDI infilling at the track–measure level** inside REAPER: the user deletes/selects bars on any tracks and the model fills them, with controls for rhythmic conditioning (2 types), horizontal/vertical onset density, pitch range/steps, "rhythmic interest". Code, weights and REAPER scripts released (CC BY 4.0).

**Evidence.** Listening study found no significant quality difference between real music and pieces co-composed with the tool; objective metrics improved substantially over v1.

**For the studio.** The cleanest open-source instantiation of "edit → compile the hole" in a real DAW with fine-grained controls; directly reusable. Cross-ref infilling cluster.

<small>Tags: [infilling] [DAW-plugin] [controllability] [symbolic-generation] [toolkit] · Verification: verified (fetched arXiv abstract) · Clusters 05, 08</small>

### `pasquier2025midigpt` — MIDI-GPT — MIDI-GPT: A Controllable Generative Model for Computer-Assisted Multitrack Music Composition

*Philippe Pasquier, Jeff Ens, Nathan Fradet, Paul Triana, Davide Rizzotti (SFU Metacreation Lab), Jean-Baptiste Rolland, Maryam Safi (Steinberg); arXiv Jan 2025 (reported as AAAI 2025 — venue not confirmed from a primary source)*

Links: https://www.metacreation.net/projects/midi-gpt ; https://github.com/Metacreation-Lab/MIDI-GPT ; https://github.com/Metacreation-Lab/midigpt-REAPER

~20M-parameter Transformer (6 layers, 2048-token context) successor to MMM: bars are sequenced *within* tracks, then tracks concatenated, enabling infilling at bar and track level for all 128 GM instruments. Conditioning: instrument, 10 instrument-relative note-density levels, polyphony range, note-duration range (5 bins), and style (MusicMap ontology). Trained on GigaMIDI. Integrated in Steinberg Cubase, an Ableton Live plugin, Teenage Engineering OP-Z, Elias game-audio middleware and the Calliope web app.

**Evidence.** Paper evaluates originality, stylistic similarity and control effectiveness (density/duration controls effective, polyphony weaker).

**For the studio.** Alternative open infilling backbone with explicit attribute sliders; its RAIL licence and GigaMIDI provenance illustrate the licensing trade-offs the studio must weigh.

<small>Tags: [infilling] [editing] [controllability] [DAW-plugin] [product] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Clusters 03, 08</small>

### `guo2022musiac` — MusIAC — MusIAC: An extensible generative framework for Music Infilling Applications with multi-level Control

*Rui Guo, Ivor Simpson, Chris Kiefer, Thor Magnusson, Dorien Herremans (University of Sussex / SUTD); EvoMUSART 2022 (arXiv Feb 2022)*

Links: https://arxiv.org/abs/2202.05528 ; code: https://github.com/ruiguo-bio/musiac

Transformer infilling of multi-track MIDI with *track-level* control tokens (note density, polyphony rate, occupation rate) and *bar-level* tokens (tensile strain and cloud diameter — tonal-tension measures from the spiral array), plus key/tempo/time-signature/instrument. A Colab interface lets a musician upload MIDI, choose what to infill and set controls, then download MIDI/WAV. A 2025 IEEE Access follow-up, "An Exploration of Controllability in Symbolic Music Infilling" (Herremans group), extends this analysis.

**Evidence.** Control tokens improve perceived artistic coherence vs. density-only control.

**For the studio.** Introduces *tension* as an annotatable bar-level control — a high-level, composer-meaningful handle beyond density.

<small>Tags: [infilling] [controllability] [editing] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

## S3.3. Compile: attribute/text/rule-conditioned symbolic generation

### `roberts2018musicvae` — MusicVAE — A Hierarchical Latent Vector Model for Learning Long-Term Structure in Music

*Adam Roberts, Jesse Engel, Colin Raffel, Curtis Hawthorne, Douglas Eck; Google Brain (Magenta); ICML 2018 (arXiv 1803.05428)*

Links: https://arxiv.org/abs/1803.05428 ; https://github.com/magenta/magenta/tree/main/magenta/models/music_vae ; https://magenta.withgoogle.com/music-vae

A recurrent VAE with a hierarchical "conductor" decoder that emits embeddings per bar, then decodes each bar, avoiding posterior collapse and enabling 16-bar melodies, drum patterns and trios. The human controls generation via the latent space: sampling, *interpolation between two clips*, and attribute vectors. Backs Magenta Studio's Generate/Interpolate and the AI Song Contest teams' workflows.

**Evidence.** "Dramatically better sampling, interpolation, and reconstruction performance than a flat baseline"; listening tests on interpolations.

**For the studio.** Latent-space interpolation is a concrete *edit primitive* ("morph my A-section groove toward my B-section groove"); MusicVAE is the reference open implementation.

<small>Tags: [symbolic-generation] [representation] [editing] [controllability] [structure] · Verification: verified (arXiv abstract fetched) · Cluster 01</small>

### `tan2020fadernets` — FaderNets — Music FaderNets: Controllable Music Generation Based on High-Level Features via Low-Level Feature Modelling

*Hao Hao Tan, Dorien Herremans (SUTD); ISMIR 2020*

Links: https://arxiv.org/abs/2007.15474 ; code: https://github.com/gudgud96/music-fader-nets

Disentangled "faders" for low-level attributes (rhythm density, note density) in a VAE, with a Gaussian-mixture latent that captures the high-level attribute *arousal* semi-supervised from 1% labels; sliding a fader rewrites an existing piano phrase along that dimension.

**Evidence.** Learns arousal with minimal labels; enables arousal style transfer on VGMIDI.

**For the studio.** Shows how emotion-level annotations ("more intense here") can be grounded in low-level controllable features.

<small>Tags: [controllability] [style-transfer] [editing] [symbolic-generation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `bhandari2025text2midi` — Text2midi — Text2midi: Generating Symbolic Music from Captions

*Keshav Bhandari, Abhinaba Roy, Kyra Wang, Geeta Puri, Simon Colton, Dorien Herremans (QMUL / SUTD); AAAI 2025*

Links: https://arxiv.org/abs/2412.16526 ; code/demo: https://github.com/AMAAI-Lab/Text2midi

Frozen FLAN-T5 text encoder + 18-layer autoregressive decoder (272M params, 159M trainable) emitting REMI+ tokens (MidiTok); pre-trained on SymphonyNet with pseudo-captions, fine-tuned on MidiCaps (168K MIDI–caption pairs). Control via musical terms in the caption (tempo, key, chords, mood, genre); from-scratch only.

**Evidence.** Beats MuseCoco on tempo (65.8% vs 54.6%) and key accuracy (35.6% vs 14.6%) and CLAP score; 11 listeners rated it above MuseCoco but below ground truth; struggles with instrumentation specificity; 2,048-token context.

**For the studio.** Open, reproducible text→MIDI baseline; its weaknesses (instrumentation, length) illustrate why text alone is an insufficient control surface.

<small>Tags: [text-conditioning] [symbolic-generation] [dataset] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `petteno2025lcdiff` — LC-Diff — Conditional Diffusion as Latent Constraints for Controllable Symbolic Music Generation

*Matteo Pettenò, Alessandro Ilic Mezza, Alberto Bernardini (Politecnico di Milano); ISMIR 2025 (arXiv Nov 2025)*

Links: https://arxiv.org/abs/2511.07156 ; https://ismir2025program.ismir.net/poster_133.html

Keeps a frozen unconditional VAE and trains small conditional diffusion priors on its latent space as plug-and-play constraints, giving fader-like control over note density, pitch range, melodic contour and rhythmic complexity (Toussaint) for monophonic melodies (10M sequences from 176K MIDI files).

**Evidence.** Pearson correlation >0.8 between requested and realised attributes for all attributes, beating attribute-regularised VAEs and cVAEs; better Fréchet Music Distance.

**For the studio.** Another retrofit-control mechanism: new controls without touching the base model.

<small>Tags: [controllability] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `lu2023musecoco` — MuseCoco — MuseCoco: Generating Symbolic Music from Text

*Peiling Lu, Xin Xu, Chenfei Kang, et al. (Microsoft Research Asia); arXiv Jun 2023*

Links: https://arxiv.org/abs/2306.00110 ; code: https://github.com/microsoft/muzic/tree/main/musecoco

Two-stage text→symbolic: (1) text-to-attribute understanding (a BERT-style classifier over ~12 attributes such as instrument, rhythm/danceability, bar count, time signature, key, tempo, pitch range, emotion, genre, time) and (2) attribute-to-music generation (1.2B-parameter decoder). Because the interface is attributes, users can bypass text and set attributes directly; outputs are editable MIDI. From-scratch only.

**Evidence.** ~20% higher objective control accuracy than baselines; higher musicality/controllability ratings; large model beats GPT-4 (ABC) in their study.

**For the studio.** Demonstrates that text should be *compiled to an explicit attribute layer* the composer can inspect and override — an argument against opaque text-to-song.

<small>Tags: [text-conditioning] [controllability] [symbolic-generation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `huang2024scg` — SCG — Symbolic Music Generation with Non-Differentiable Rule Guided Diffusion

*Yujia Huang, Adishree Ghatare, Yuanzhe Liu, et al. (Caltech / RPI / NVIDIA / Dalhousie–Vector); ICML 2024*

Links: https://arxiv.org/abs/2402.14285 ; code: https://github.com/yjhuangcd/rule-guided-music

Stochastic Control Guidance steers a pre-trained latent diffusion model (piano-roll) toward *non-differentiable* rules — pitch-class histogram, horizontal/vertical note density, chord progression — by forward-evaluating the rule on candidate samples at each step, training-free. Supports *editing*: modify an existing piece within a chosen time window, either as a variant or to satisfy new rules.

**Evidence.** Improves both rule adherence and quality over baselines (including classifier guidance) on symbolic piano data.

**For the studio.** New annotation types can be added as plain functions without retraining; window-based editing of an existing piece fits the loop exactly.

<small>Tags: [controllability] [editing] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `lin2026diffsymbo` — Diff-Symbo — Diff-Symbo: Text-Controlled Long-Duration Symbolic Music Generation Using Autoregressive Latent Diffusion Model

*Zhiwei Lin, Jun Chen, Boshi Tang, et al. (Tsinghua / industry); arXiv Aug 2026*

Links: https://arxiv.org/abs/2608.05222

Autoregressive latent diffusion for text-conditioned multi-track symbolic music aimed at long durations and consistency; addresses paired-data scarcity with 19,345 LLM-generated text templates.

**Evidence.** Reports gains in controllability and quality over GPT-4, MuseCoco and MMT baselines.

**For the studio.** Indicative of the mid-2026 frontier for text→symbolic; still from-scratch generation, no editing.

<small>Tags: [text-conditioning] [symbolic-generation] · Verification: verified (arXiv abstract fetched; very recent, not peer-reviewed) · Cluster 03</small>

## S3.4. Compile: structure-aware & hierarchical pipelines

### `yu2022museformer` — Museformer — Museformer: Transformer with Fine- and Coarse-Grained Attention for Music Generation

*Botao Yu, Peiling Lu, Rui Wang, et al. (Nanjing University / Microsoft Research Asia / Peking University); NeurIPS 2022*

Links: https://arxiv.org/abs/2210.10349 ; code: https://github.com/microsoft/muzic/tree/main/museformer

Sparse attention where each bar attends finely to "structure-related" previous bars (1, 2, 4, 8, 12, 16, 24, 32 bars back — chosen from bar-similarity statistics) and coarsely to summaries of the others; models >3× longer sequences than full attention for full-song multi-track generation from scratch (Lakh MIDI). No infilling or user controls.

**Evidence.** Better perplexity at all lengths; repetition-similarity curves closer to human music; higher human ratings for short- and long-term structure.

**For the studio.** Encodes a musical prior (repetition at phrase-multiples) into architecture — informs how a studio's models should see form.

<small>Tags: [structure] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `huang2018musictransformer` — MusicTransformer — Music Transformer: Generating Music with Long-Term Structure

*Cheng-Zhi Anna Huang, Ashish Vaswani, Jakob Uszkoreit, Noam Shazeer, Ian Simon, Curtis Hawthorne, Andrew M. Dai, Matthew D. Hoffman, Monica Dinculescu, Douglas Eck; Google Brain; ICLR 2019 (arXiv 1809.04281, Sept 2018)*

Links: https://arxiv.org/abs/1809.04281 ; code: https://github.com/magenta/magenta (Magenta); project: https://magenta.tensorflow.org/music-transformer

Decoder-only Transformer over MIDI-like performance events (NOTE_ON/NOTE_OFF, TIME_SHIFT, VELOCITY) with a memory-efficient *relative* self-attention (linear rather than quadratic memory), enabling ~minute-long piano continuations with repeated motifs. Inputs: a primer (or a melody for the accompaniment variant); output: a continuation. Human control is limited to priming and melody-conditioning; no infilling.

**Evidence.** State-of-the-art NLL on Piano-e-Competition; listening studies preferred it over PerformanceRNN and vanilla Transformer. Huang's homepage claims it is the most-cited music-generation paper at ICLR.

**For the studio.** The workhorse symbolic model of the lineage; the melody→accompaniment seq2seq mode is a literal "compile a lead sheet into a piano part" primitive, and motif-continuation supports iterative development of human-authored ideas.

<small>Tags: [symbolic-generation] [structure] [accompaniment] [expression-performance] · Verification: verified (arXiv abstract fetched) · Clusters 01, 03</small>

### `chen2024sympac` — SymPAC — SymPAC: Scalable Symbolic Music Generation with Prompts and Constraints

*Haonan Chen, Jordan B. L. Smith, Bochen Li, et al. (ByteDance / QMUL / CUHK); ISMIR 2024*

Links: https://arxiv.org/abs/2409.03055

Trains a multi-track symbolic model solely on ~1M in-house *audio* tracks auto-transcribed with MIR models (beat, chords, sections, multi-track transcription). Control is via *prompt bars* — a leading block holding genre, section labels, tempo, chords and track list that the user can fully or partially specify — and via finite-state-machine *constrained decoding* that guarantees generated tokens obey the grammar and the user's constraints.

**Evidence.** 12 MIR researchers/producers rated it significantly above FIGARO and MMT on coherence, richness, arrangement, structure and overall.

**For the studio.** Hard constraints at decode time (rather than soft conditioning) are what a composer expects when they write "Cmaj7 here"; prompt bars are a compact section-level annotation.

<small>Tags: [controllability] [symbolic-generation] [structure] [transcription] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `dai2023personalised` — PersonalisedImitation — Personalised Popular Music Generation Using Imitation and Structure

*Shuqi Dai, Xichu Ma, Ye Wang, Roger B. Dannenberg; CMU + NUS. Journal of New Music Research 51(1), 2022 (published 2023). arXiv 2021.*

Links: https://doi.org/10.1080/09298215.2023.2166848

Statistical-ML system that *imitates* a chosen reference song's structure, melody, chord progression and bass style to generate a new personalised song — structure analysis first, then generation constrained to the analysed template; explicitly designed so a user can pick what to imitate.

**Evidence.** Subjective evaluation (details not fetched; publisher page blocked).

**For the studio.** "Insert example audio/score as annotation → imitate its structure" is one of the founder's core interactions; this is a symbolic-domain precedent.

<small>Tags: [symbolic-generation] [structure] [style-transfer] [controllability] · Verification: partial (bibliography + search snippets; publisher page 403) · Cluster 02</small>

### `dai2021controllable` — MusicFrameworks — Controllable Deep Melody Generation via Hierarchical Music Structure Representation

*Shuqi Dai, Zeyu Jin, Celso Gomes, Roger B. Dannenberg (CMU / Adobe); ISMIR 2021. Follow-up: Shuqi Dai, Huiran Yu, Roger B. Dannenberg (CMU); ISMIR 2022*

Links: https://arxiv.org/abs/2109.00663 ; https://arxiv.org/abs/2209.00182 ; https://shuqid.net/

"MusicFrameworks": a hierarchical representation with **section- and phrase-level structure**, a *basic melody* (skeleton), rhythm structure and chords; two Transformer networks generate rhythm and basic melody, then a third generates the final melody autoregressively conditioned on them. Users can **alter chords, basic melody, and rhythm structure** to customise or vary a piece — long-form generation with explicit, editable structure.

**Evidence.** Listeners preferred generated melodies over POP909 human melodies ~50% of the time; corpus analysis quantifies non-random repetition.

**For the studio.** A concrete, editable structural skeleton (section/phrase/basic melody/rhythm/chords) — exactly the intermediate "annotation layer" a composer edits before the AI compiles the surface.

<small>Tags: [symbolic-generation] [structure] [controllability] [representation] [editing] · Verification: verified (arXiv page) · Clusters 02, 03</small>

### `wang2024wholesong` — WholeSong — Whole-Song Hierarchical Generation of Symbolic Music Using Cascaded Diffusion Models

*Ziyu Wang, Lejun Min, Gus Xia (NYU Shanghai / MBZUAI Music X Lab); ICLR 2024*

Links: https://arxiv.org/abs/2405.09901 ; code: https://github.com/ZZWaang/whole-song-gen ; OpenReview: https://openreview.net/forum?id=sn7CYWyavh

Four cascaded piano-roll diffusion models generate a full pop song top-down: (1) form/phrase structure and key, (2) reduced lead sheet (harmonic skeleton), (3) lead sheet (melody + chords), (4) accompaniment — each conditioned on the levels above. Every level is an interpretable, editable symbolic object, and external pre-trained encoders can steer chord progression, rhythm patterns and accompaniment texture.

**Evidence.** Human study shows higher ratings for full-song structure than flat baselines; controllability demonstrated at each level.

**For the studio.** The most literal existing "compiler": human-editable intermediate representations at every stage of a form→lead-sheet→arrangement pipeline.

<small>Tags: [structure] [symbolic-generation] [controllability] [accompaniment] [co-creation-framework] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

## S3.5. Compile: harmonization, accompaniment & arrangement

### `huang2016chordripple` — Chordripple — Chordripple: Recommending Chords to Help Novice Composers Go Beyond the Ordinary

*Cheng-Zhi Anna Huang, David Duvenaud, Krzysztof Z. Gajos; Harvard University; ACM IUI, 2016*

Links: https://doi.org/10.1145/2856767.2856792 ; PDF https://www.eecs.harvard.edu/~kgajos/papers/2016/huang16chordripple.pdf

A chord-recommendation tool for novice composers. As the user writes a chord progression, Chordripple suggests replacement or next chords, ranked by a learned chord embedding (a word2vec-style "chord2vec" trained on a pop/rock corpus) so that suggestions are both plausible and "beyond the ordinary." The human keeps authorship: the system only proposes, and proposals are ranked by adventurousness.

**Evidence.** Study 1: 15 participants with composition experience, think-aloud + interviews. Study 2: 9 music students, three conditions (typical, adventurous, ripple); adventurous recommendations significantly increased chord novelty (p=0.0039); ripples did not increase adoption; users split between wanting familiar vs "breaking-out" suggestions.

**For the studio.** Earliest Huang work on *recommendation as steering* in a symbolic (chord) representation — a lightweight "suggest, don't dictate" pattern for the harmony layer of the studio.

<small>Tags: [symbolic-generation] [controllability] [creativity-support] [HCI-study] [representation] · Verification: partial (title/venue/year verified from Huang's homepage; system details from recall) · Clusters 01, 05</small>

### `zhao2021accomontage` — AccoMontage — AccoMontage: Accompaniment Arrangement via Phrase Selection and Style Transfer; AccoMontage2: A Complete Harmonization and Accompaniment Arrangement System

*Jingwei Zhao, Gus Xia (Music X Lab, NYU Shanghai); ISMIR 2021. AccoMontage2: Li Yi, Haochen Hu, Jingwei Zhao, Gus Xia; ISMIR 2022*

Links: https://arxiv.org/abs/2108.11213 ; https://github.com/zhaojw1998/AccoMontage ; https://arxiv.org/abs/2209.00353 ; https://github.com/billyblu2000/AccoMontage2

Lead sheet (melody + chords) → full-length piano accompaniment by (1) retrieving accompaniment *phrases* from a database with dynamic programming over phrase fitness and transition smoothness, then (2) re-harmonising them to the target chords via a chord–texture disentangled VAE (style transfer). AccoMontage2 adds a melody-harmonisation module (structured chord progressions via three loss terms) and a GUI where users pick chord style (Pop/R&B/Dark) and texture density/rhythmic complexity.

**Evidence.** 72 participants: significantly better coherence and structure than learning-only baselines (p<0.05), musicality marginal (p=0.053).

**For the studio.** "Retrieve human-made material and adapt it to my chords" is a compositionally transparent form of compile — and the phrase database could be the composer's own past work.

<small>Tags: [accompaniment] [style-transfer] [structure] [symbolic-generation] [controllability] · Verification: verified (arXiv PDFs/abstracts fetched) · Cluster 03</small>

### `zhao2023qa` — QandA — Q&A: Query-Based Representation Learning for Multi-Track Symbolic Music re-Arrangement

*Jingwei Zhao, Gus Xia, Ye Wang (NUS / NYU Shanghai / MBZUAI); IJCAI 2023 (AI, the Arts and Creativity track)*

Links: https://arxiv.org/abs/2306.01635 ; code: https://github.com/zhaojw1998/Query-and-reArrange

Self-supervised content/style disentanglement for multi-track music: content is learned from the mixture, style (function) from individual tracks, and a query-based decoder re-renders the piece for a new set of tracks. Covers re-instrumentation, piano-cover generation, orchestration (piano → band) and voice separation with the user choosing the target instrumentation.

**Evidence.** Better multi-track structure and quality than baselines in objective and subjective tests.

**For the studio.** "Arrange this piano sketch for this ensemble" as one operation with chosen tracks — a key compile step for an arranger-workstation heritage.

<small>Tags: [accompaniment] [style-transfer] [symbolic-generation] [controllability] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `zhao2024structured` — StructuredArrangement — Structured Multi-Track Accompaniment Arrangement via Style Prior Modelling

*Jingwei Zhao, Gus Xia, Ziyu Wang, Ye Wang (NUS / MBZUAI / NYU Shanghai); NeurIPS 2024 (arXiv Oct 2023)*

Links: https://arxiv.org/abs/2310.16334 ; code/demo: https://github.com/zhaojw1998/Structured-Arrangement-Code ; https://proceedings.neurips.cc/paper_files/paper/2024/hash/b95cb2d3f647dae571203bab285077e7-Abstract-Conference.html

Two-stage "compile" from lead sheet to full band: (1) piano arrangement via texture-style retrieval (AccoMontage lineage), (2) orchestration by infusing per-track *function* styles, modelled as vector-quantised style codes whose long-term flow is generated by a multi-stream Transformer prior — giving whole-song coherence, genre choice and hierarchical control over the arrangement.

**Evidence.** Higher coherence, structure and quality than baselines with lower compute; whole-song outputs.

**For the studio.** Closest existing system to the founder's arranger-workstation vision (lead sheet in, structured multi-track arrangement out) with editable intermediate piano stage.

<small>Tags: [accompaniment] [structure] [symbolic-generation] [controllability] [style-transfer] · Verification: verified (arXiv abstract fetched; venue via NeurIPS proceedings page) · Cluster 03</small>

### `jiang2025functionalignment` — FunctionAlignment — Versatile Symbolic Music-for-Music Modeling via Function Alignment

*Junyan Jiang, Daniel Chin, Liwei Lin, Xuanjie Liu, Gus Xia (NYU Shanghai / MBZUAI Music X Lab); ISMIR 2025*

Links: https://arxiv.org/abs/2506.15548

Two pretrained symbolic LMs (a RoFormer trained from scratch on 357K Los Angeles MIDI files, 16th-note grid) — one reading a *reference* sequence, one writing a *target* — joined by a lightweight adapter, so understanding (chord recognition, metrical analysis) and generation (chord-conditioned melody, melody-conditioned chords, drums↔song) are the same "music-for-music" operation, parameter-efficiently.

**Evidence.** Strong results across five tasks incl. few-shot chord recognition and metre transcription on RWC-Pop (93 songs); code and weights released.

**For the studio.** A general recipe for "given this part, produce/analyse that part" with small adapters — exactly the pluggable operator set a compile pipeline needs.

<small>Tags: [symbolic-generation] [accompaniment] [theory-analysis] [controllability] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `kaliakatsospapakostas2025harmonization` — BstarHarmonization — Incorporating Structure and Chord Constraints in Symbolic Transformer-based Melodic Harmonization

*Maximos Kaliakatsos-Papakostas, Konstantinos Soiledis, Konstantinos-Theodoros Tsamis, et al. (Hellenic Mediterranean University / Athena RC / Aristotle University of Thessaloniki); arXiv Dec 2025*

Links: https://arxiv.org/abs/2512.07627 ; https://zenodo.org/records/16948248

Melody harmonisation (Hooktheory, 17,476 lead sheets) with BART and GPT-2 models that accept structure tokens and *user-specified chord constraints* at given bar/beat positions; proposes B* (beam + A* + backtracking) decoding to guarantee the constrained chords appear where requested.

**Evidence.** Soft constraints satisfied only 50–63% of the time; B* reaches 90–98% at ~400–1,900 model calls; chord-symbol tokens beat pitch-class tokens under constraints.

**For the studio.** Directly addresses "I want this chord here" as a hard constraint in a lead-sheet workflow — an editing-style harmonisation primitive.

<small>Tags: [accompaniment] [controllability] [editing] [symbolic-generation] [notation] · Verification: verified (arXiv PDF/HTML fetched) · Cluster 03</small>

### `pgmusic2026biab` — Band-in-a-Box — chords + style → full arrangement (PG Music, 1990–2026)

*PG Music (Peter Gannon, Victoria BC); first Atari/PC release 1990; RealTracks (recorded musicians, 2007–); Band-in-a-Box 2026 (Windows/Mac)*

Links: https://www.pgmusic.com ; https://www.pgmusic.com/manuals/bbw2026full/chapter7.htm

Type chord symbols (C, Fm7, C13b9) into a bar grid, choose a style → complete arrangement (piano, bass, drums, guitar, strings/horns) rendered either as MIDI styles or as time-stretched, pitch-shifted **RealTracks** audio (>4,400 hours of studio recordings in 2026; 202 new sets this year). 2026 adds a redesigned GUI, Multi-View, and "AI-Notes" polyphonic audio→MIDI transcription. Also melodist/soloist generators, notation view, export to DAW (RealBand, DAW plugin).

**Evidence.** Continuous commercial development for 36 years; closed source.

**For the studio.** The longest-lived "compile" product: symbolic, human-authored input (chords) → arrangement; its style library/RealTracks show the value of curated, licensed performance data over generic synthesis — and its dated UX shows the room for an annotation-driven, notation-first alternative.

<small>Tags: [accompaniment] [product] [history] [symbolic-generation] · Verification: verified (2026 product page); history partial · Cluster 07</small>

### `wu2026stemphonic` — Stemphonic — Stemphonic: All-at-once Flexible Multi-stem Music Generation

*Shih-Lun Wu, Ge Zhu, Juan-Pablo Cáceres, Cheng-Zhi Anna Huang, Nicholas J. Bryan; Adobe Research (internship); arXiv 2602.09891, Feb 2026*

Links: https://arxiv.org/abs/2602.09891 ; demo: https://stemphonic-demo.vercel.app

Diffusion/flow model that generates a *variable set of synchronized stems in one pass* (vs. fixed-stem parallel or slow one-stem-at-a-time). Tricks: stem grouping in batches, shared initial noise within a group, conditioning on existing sub-mixes, and per-stem binary **activity patterns** (when each instrument plays). Conditioning: global + per-stem text, tempo, existing audio.

**Evidence.** FAD_stem/FAD_mix, CLAP, activity-F1 on MoisesDB and MUSDB; 25–50% faster than iterative baseline, better mix quality with a 2-pass scheme.

**For the studio.** Arrangement-as-compile: given the composer's existing stems and an "activity score," it fills in the remaining parts — aligned with the founder's arranger-workstation instincts.

<small>Tags: [audio-generation] [accompaniment] [controllability] [text-conditioning] [structure] · Verification: verified (arXiv HTML fetched) · Cluster 01</small>

## S3.6. Compile: music LLMs & music-as-code

### `wang2015chuck` — AudioLangs — Csound, SuperCollider, Max/Pure Data, ChucK, Faust: audio programming languages

*Csound: Barry Vercoe, MIT, 1985/86 (LGPL; Csound 7, web IDE). SuperCollider: James McCartney 1996, GPL 2002 (v3.14.1). Max: Miller Puckette, IRCAM 1988 (Cycling '74); Pure Data: Puckette 1996 (open source). ChucK: Ge Wang & Perry Cook, Princeton/Stanford, ICMC 2003; CMJ 2015 (v1.5.5.x; WebChucK). Faust: GRAME-CNCM (Orlarey, Fober, Letz), 2002–.*

Links: https://csound.com/ ; https://supercollider.github.io/ ; https://puredata.info/ ; https://chuck.stanford.edu/ ; https://faust.grame.fr/

Csound: orchestra (instrument definitions) + score (note events) text files rendered to audio — a pure compile model. SuperCollider: scsynth server + sclang client; on-the-fly code evaluation. Max/Pd: visual dataflow patching with real-time signal graphs. ChucK: "strongly-timed" concurrent language where time is a first-class variable and code is added/replaced while running. Faust: functional block-diagram DSL compiled to C++/C/LLVM/WASM/Rust and to plugins/apps/web.

**Evidence.** Canonical systems; each with long publication records.

**For the studio.** Two compile philosophies to borrow: Csound's *orchestra/score separation* (sound design vs. musical text — analogous to arrangement/rendering vs. notation) and ChucK/SC's *live re-evaluation* (edit code while music plays). Faust proves a DSL can compile to many targets — a model for compiling one musical IR to MusicXML, MIDI and audio.

<small>Tags: [music-as-code] [toolkit] [real-time] [history] · Verification: verified (all project sites fetched) · Cluster 06</small>

### `yu2023musicagent` — MusicAgent — MusicAgent: An AI Agent for Music Understanding and Generation with Large Language Models

*Dingyao Yu, Kaitao Song, Peiling Lu, Tianyu He, Xu Tan, Wei Ye, Shikun Zhang, Jiang Bian; Microsoft Research Asia, Peking University; EMNLP 2023 (system demonstrations)*

Links: https://arxiv.org/abs/2310.11954 ; https://github.com/microsoft/muzic

LLM (ChatGPT) decomposes a user request into sub-tasks and invokes music tools aggregated from Hugging Face, GitHub and web APIs (generation such as timbre synthesis and analysis such as classification), handling format conversions between tools.

**Evidence.** Demonstration; no user study.

**For the studio.** Shows the tool-orchestration pattern the "compiler" could use internally (route sub-tasks to specialised models) — but without a human-editable intermediate.

<small>Tags: [LLM-agent] [toolkit] · Verification: partial (arXiv abstract fetched; author list from recall) · Cluster 05</small>

### `nienhuys2003lilypond` — LilyPond — LilyPond: music engraving compiler

*Han-Wen Nienhuys, Jan Nieuwenhuizen (1996–); GNU project; "LilyPond, a system for automated music engraving," XIV Colloquium on Musical Informatics, 2003*

Links: https://lilypond.org/

Text source (`\relative c' { c4 d e f }`) is *compiled* into engraved PDF/SVG/MIDI; layout decisions are made programmatically following classical engraving rules; extensible in Scheme. GPL. Explicitly the "music as source code → compiler → typeset output" model; used by Sheet Sage and MuseScore export pipelines.

**Evidence.** Decades of use; engraving quality frequently cited.

**For the studio.** The literal precedent for "compile"; its pain points (edit–compile latency, error messages in terms of source not score) are exactly what a live, projectional studio should fix.

<small>Tags: [music-as-code] [notation] [toolkit] · Verification: verified (site fetched; 2003 paper partial) · Cluster 06</small>

### `assayag1999openmusic` — CAC — OpenMusic, bach, PWGL: computer-aided composition environments

*OpenMusic: Carlos Agon, Gérard Assayag, Jean Bresson, Karim Haddad; IRCAM Music Representations team, 1998– (GPLv3; OM 8.0 released 30 Mar 2026; Assayag et al., CMJ 1999). bach: Andrea Agostini & Daniele Ghisi, 2010– (GPLv3; CMJ 2015). PWGL: Mikael Laurson, Mika Kuuskankare, Vesa Norilo, Sibelius Academy (CMJ 2009).*

Links: https://github.com/openmusic-project/openmusic ; https://www.bachproject.net/

OpenMusic: visual Lisp programming — patches of boxes compute musical structures displayed in editable common-notation, piano-roll and sound editors; the *maquette* arranges patches on a timeline. bach: brings CAC into Max in real time with `bach.roll` (proportional notation) and `bach.score` (measured notation) objects editable by mouse *or* by patching, plus cage/dada/ears libraries. PWGL: Lisp-based visual environment with the Expressive Notation Package.

**Evidence.** Used by generations of IRCAM/Ircam-adjacent composers; extensive literature.

**For the studio.** These are the composers' own "compile" tools: programs generate notation that is then hand-edited — the same loop the studio proposes, with AI replacing hand-written Lisp. Their dual editing (edit the program or edit the output notation) is the central UX question for the studio: which edits round-trip?

<small>Tags: [music-as-code] [notation] [toolkit] [history] · Verification: verified (OpenMusic, bach sites fetched; PWGL partial) · Cluster 06</small>

### `deng2024composerx` — ComposerX — ComposerX: Multi-Agent Symbolic Music Composition with LLMs

*Qixin Deng, Qikai Yang, Ruibin Yuan, Yipeng Huang, Yi Wang, Xubo Liu, et al. (19 authors incl. Gus Xia, Emmanouil Benetos, Wenwu Wang, Wei Xue, Yike Guo); Rochester, CMU, HKUST, QMUL, Surrey; ISMIR 2024 (arXiv 2024)*

Links: https://arxiv.org/abs/2404.18081 ; https://github.com/lllindsey0615/ComposerX

Six GPT-4 agents — Group Leader, Melody, Harmony, Instrument, Reviewer, Arrangement — collaborate to write polyphonic pieces in ABC notation from a text brief, with a review/revision loop.

**Evidence.** 98.2% generation success; multi-agent preferred over single-agent (0.77 preference); 32.2% of outputs judged human-composed vs 55.4% for real human pieces; ~$0.80 per piece. Rater counts not reported.

**For the studio.** A pure-LLM, notation-native "compiler" with explicit role decomposition and a critic; a baseline the studio could extend with human annotations entering at any agent.

<small>Tags: [LLM-agent] [symbolic-generation] [notation] [music-as-code] [evaluation] · Verification: verified (fetched arXiv HTML) · Cluster 05</small>

### `dannenberg1997nyquist` — Nyquist-Audacity — Nyquist (composition/synthesis language) and Audacity (editor)

*Roger B. Dannenberg, "Machine Tongues XIX: Nyquist, a Language for Composition and Sound Synthesis", Computer Music Journal 21(3), 1997 (also "The Nyquist Composition Environment", ICMC 2008). Dominic Mazzoni & Roger B. Dannenberg, "A Fast Data Structure for Disk-Based Audio Editing", Computer Music Journal 26(2), 2002 — the Audacity architecture paper; Audacity was begun at CMU in 1999–2000 by Mazzoni and Dannenberg.*

Links: https://www.cs.cmu.edu/~music/nyquist ; https://www.audacityteam.org/ ; https://www.cs.cmu.edu/~rbd/bib.html

Nyquist: a Lisp/SAL-based language in which *scores are programs* (behaviours, transformations, temporal combinators like `sim`/`seq`) — music-as-code lineage. Audacity: the dominant open-source audio editor (Nyquist is its plug-in scripting language).

**Evidence.** Decades of use; Audacity is among the most downloaded open-source audio tools.

**For the studio.** Both are CMU precedents for the founder's two pillars — music as compilable program (Nyquist) and open-source editing infrastructure (Audacity); also shows that a scripting language embedded in an editor is a viable extension surface.

<small>Tags: [music-as-code] [toolkit] [history] [editing] [product] · Verification: verified (author bibliography) · Cluster 02</small>

### `yuan2024chatmusician` — ChatMusician — ChatMusician: Understanding and Generating Music Intrinsically with LLM

*Ruibin Yuan, Hanfeng Lin, Yi Wang, et al. (M-A-P / HKUST / QMUL and others); arXiv Feb 2024 (published in Findings of ACL 2024 — venue from knowledge, not re-fetched)*

Links: https://arxiv.org/abs/2402.16153 ; code/models: https://github.com/hf-lin/ChatMusician ; https://shanghaicannon.github.io/ChatMusician/

LLaMA2-7B continually pretrained/fine-tuned on MusicPile (4B tokens) to read and write **ABC notation** with a plain text tokenizer — "music as a second language." Generates full pieces conditioned on text, chords, melodies, motifs and musical forms; also answers theory questions (MusicTheoryBench).

**Evidence.** ChatMusician beats LLaMA-2 and GPT-3.5 zero-shot on MusicTheoryBench; GPT-4 reasoning accuracy reported near random on the reasoning split (recalled; not re-fetched).

**For the studio.** Proof that a general LLM can treat a textual score language as code — the enabling assumption for an annotation→ABC/kern compiler; also shows conditioning on *partial symbolic material* (motif, chords, form) works.

<small>Tags: [music-as-code] [symbolic-generation] [text-conditioning] [LLM-agent] [representation] · Verification: verified (arXiv abstract fetched) · Clusters 03, 06, 07</small>

### `wu2024melodyt5` — MelodyT5 — MelodyT5: A Unified Score-to-Score Transformer for Symbolic Music Processing

*Shangda Wu, Yashan Wang, Xiaobing Li, Feng Yu, Maosong Sun (Central Conservatory of Music / Tsinghua); ISMIR 2024*

Links: https://arxiv.org/abs/2407.02277 ; code: https://github.com/sanderwood/melodyt5 ; https://huggingface.co/sander-wood/melodyt5

Encoder–decoder over ABC that unifies seven melody-centric score-to-score tasks (e.g., melody generation, harmonisation, melodisation, segmentation, variation) in one model, pre-trained on MelodyHub (261K melodies, >1M task instances).

**Evidence.** Multi-task transfer improves low-data tasks vs single-task models.

**For the studio.** A single "score in → score out" model for lead-sheet operations (add chords to a melody, write a melody over chords, segment phrases) — the kind of operator a compile step chains.

<small>Tags: [symbolic-generation] [accompaniment] [notation] [structure] · Verification: verified (arXiv abstract fetched; authors from GitHub/knowledge) · Cluster 03</small>

### `wu2025midillm` — MIDI-LLM — MIDI-LLM: Adapting Large Language Models for Text-to-MIDI Music Generation

*Shih-Lun Wu, Dave Carlton, Ryan Miyakawa, Yoon Kim, Chris Donahue, Cheng-Zhi Anna Huang (MIT / CMU / industry); ISMIR 2026 (arXiv Nov 2025)*

Links: https://arxiv.org/abs/2511.03942 ; https://openreview.net/pdf?id=GVW9YixIAI

Extends Llama 3.2 (1B) vocabulary with ~55k MIDI tokens (Anticipatory Music Transformer arrival-time encoding: onset, duration, instrument-pitch); two-stage training (continued pretraining on music text + MIDI, then SFT on text–MIDI pairs). Keeps the standard LLM architecture so vLLM-style acceleration applies.

**Evidence.** Outperforms Text2midi on controllability and quality; in-the-wild study with 58 musicians and ~4,000 generations showed higher acceptance for lead-sheet generation.

**For the studio.** Strongest recent evidence that a general LLM can be turned into a symbolic co-writer for *lead sheets* while retaining language for dialogue — a plausible backbone for an annotation-understanding "compiler front end".

<small>Tags: [symbolic-generation] [text-conditioning] [music-as-code] [LLM-agent] · Verification: verified (arXiv abstract fetched) · Clusters 03, 06</small>

### `omar2019hazel` — LiveProg — Live programming (Tanimoto 2013), Hazel typed holes (POPL 2019), and projectional editing (JetBrains MPS)

*Steven L. Tanimoto, "A Perspective on the Evolution of Live Programming," LIVE 2013 (ICSE workshop). Cyrus Omar, Ian Voysey, Ravi Chugh, Matthew A. Hammer, "Live Functional Programming with Typed Holes," POPL 2019 (PACMPL 3). JetBrains MPS (projectional language workbench).*

Links: https://arxiv.org/abs/1805.00155 ; https://hazel.org ; https://www.jetbrains.com/mps/concepts/

Tanimoto's liveness levels (1–6) describe how immediately a program's edits are reflected in running output. Hazel gives a dynamic semantics for *incomplete* programs: evaluation proceeds *around* typed holes, so every editor state yields feedback. MPS edits the AST directly (no parser) and projects it in multiple notations (text, tables, diagrams) simultaneously.

**Evidence.** Formal semantics (Hazel); industrial use (MPS).

**For the studio.** Three pillars for a musical compile-edit loop: (1) liveness — re-render/re-play on every annotation; (2) *holes* — a score with `[to be composed]` regions should still compile and play, with the AI filling holes; (3) projectional editing — one musical model viewed as notation, piano roll, chord chart and text, all editable.

<small>Tags: [music-as-code] [editing] [representation] · Verification: verified for Hazel and MPS (fetched); Tanimoto partial · Cluster 06</small>

### `mclean2014tidal` — LiveCoding — TidalCycles, Strudel, Sonic Pi, Gibber, FoxDot: live coding environments

*TidalCycles: Alex McLean, 2009– (Haskell; "Making programming languages to dance to: live coding with Tidal," FARM 2014). Strudel: Felix Roos, Alex McLean et al., 2022– (JS port of Tidal; AGPL-3.0; codeberg.org/uzu/strudel; ICLC 2023 paper). Sonic Pi: Sam Aaron, 2012– (Ruby; v5.0; "From Sonic Pi to Overtone," FARM 2013 with Alan Blackwell). Gibber: Charlie Roberts (ICMC 2012). FoxDot: Ryan Kirkbride (Python; ICLC 2016).*

Links: https://tidalcycles.org/ ; https://strudel.cc ; https://codeberg.org/uzu/strudel ; https://sonic-pi.net/ ; https://gibber.cc/

Pattern languages where short code expressions describe cyclic musical patterns and are *re-evaluated live* while sound continues (Tidal/Strudel mini-notation `"bd sd [hh hh]"`; Sonic Pi `live_loop` with `sync`, Ableton Link). Strudel runs entirely in the browser with inline visualisations and a tutorial REPL; Gibber annotates the running code with live values. Sonic Pi was co-designed with teachers for UK computing curricula.

**Evidence.** Community scale (algorave); Sonic Pi education deployments; Strudel adoption via browser.

**For the studio.** Live coding is the most developed practice of *music as continuously recompiled code*; mini-notations show how terse a musical text IR can be, and Strudel/Gibber show in-editor visual feedback of what the code produced — a pattern for showing how annotations compiled.

<small>Tags: [music-as-code] [real-time] [education] [toolkit] · Verification: verified (sites fetched; McLean 2014 metadata via S2; Roos & McLean 2023 / Aaron & Blackwell 2013 / Kirkbride 2016 partial) · Cluster 06</small>

### `qu2024mupt` — MuPT — MuPT: A Generative Symbolic Music Pretrained Transformer

*Xingwei Qu, Yuelin Bai, Yinghao Ma, et al. (M-A-P / Waterloo / HKUST / Manchester); arXiv Apr 2024 (widely reported as accepted at ICLR 2025 — venue not confirmed from a primary source)*

Links: https://arxiv.org/abs/2404.06393 ; https://map-mupt.github.io/ ; models on Hugging Face (m-a-p/MuPT-*)

Family of 190M–4.23B-parameter decoders trained on 33.6B tokens of ABC with 8,192-token context. Introduces *SMT-ABC* (Synchronized Multi-Track ABC), interleaving bars of the same index across tracks with `<|>` delimiters so multi-part alignment survives; proposes a Symbolic Music Scaling law under data repetition. Generation is from-scratch/continuation.

**Evidence.** ABC outperformed MIDI tokens for LLMs in their study; scaling law fits with repeated epochs.

**For the studio.** SMT-ABC is the most practical text encoding of multi-track *scores* (bar-aligned) — a candidate interchange format between the studio's notation view and LLMs.

<small>Tags: [symbolic-generation] [representation] [notation] [LLM-agent] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

### `wang2025notagen` — NotaGen — NotaGen: Advancing Musicality in Symbolic Music Generation with Large Language Model Training Paradigms

*Yashan Wang, Shangda Wu, Jianhuai Hu, et al. (Central Conservatory of Music, Beijing, and others); arXiv Feb 2025 (v5 2025)*

Links: https://arxiv.org/abs/2502.18008 ; code/weights: https://github.com/ElectricAlexis/NotaGen ; demo: https://electricalexis.github.io/notagen-demo/

LLM-style pipeline for classical *scores* in ABC: pre-train on 1.6M pieces, fine-tune on ~9K high-quality classical works, then reinforce with *CLaMP-DPO* (preference optimisation using the CLaMP 2 music–text model as an automatic judge, no human labels). Conditioning is a "period–composer–instrumentation" prompt; generation from scratch.

**Evidence.** Subjective A/B tests favour NotaGen over baselines (and human-composed pieces in some comparisons); CLaMP-DPO improves controllability and quality.

**For the studio.** The current strongest open *score*-level generator and a template for RL-from-model-feedback that could be redirected at composer-specified rewards (annotations).

<small>Tags: [symbolic-generation] [notation] [controllability] [LLM-agent] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `kim2026decomposer` — Decomposer — Decomposer: Learning to Decompile Symbolic Music to Programs

*Yewon Kim, Apurva Gandhi, David Chung, Graham Neubig, Chris Donahue; CMU. Preprint, July 2026 (arXiv 2607.01849).*

Links: https://arxiv.org/abs/2607.01849 ; project: https://yewon-kim.com/decomposer ; code: https://github.com/elianakim/Decomposer ; demo: https://huggingface.co/spaces/haiyewon/decomposer-demo

Post-training framework that converts MIDI into **executable Strudel programs** (a live-coding music DSL) that re-render the input while exposing repeated patterns, voices, harmony and timing as *editable code*. Base model Qwen3-8B. Stage 1: SFT on **STRUDEL-SYNTH**, 21,174 (Strudel, MIDI) pairs distilled from a frontier LLM (Claude Opus 4.6) and rendered — ~30× the 688 public Strudel programs. Stage 2: RL with execution-based rewards computed from the input MIDI and program alone (so unpaired MIDI can be used): a *faithfulness* reward (render program → compare to input) and a *readability* reward (penalise note-by-note transcription). Users edit the program and re-render.

**Evidence.** Compile rate 0.99 vs 0.75–0.82 for frontier LLMs; onset F1 on Lakh 0.60 vs 0.27–0.28 (GPT-5.5, Claude Opus 4.6, Gemini 3.5 Flash); multi-instrument onset F1 0.58 vs 0.21–0.23; readability rubric 0.61 (LMD) / 0.74 (Strudel-Synth) vs 0.09 for a heuristic converter and 0.29–0.36 for frontier LLMs; generalises to GigaMIDI, Nottingham, NES-MDB. Ablations show an explicit faithfulness↔readability trade-off and that RL without SFT plateaus. No user study.

**For the studio.** This *is* the "composition as program, compiled by AI" idea, run in the decompile direction: it gives the studio a candidate intermediate representation (structured program) in which human edits are semantic (change a loop, a transposition, a voice) and the compile step is deterministic rendering. Pair with a forward model (program + annotations → new program) to close the loop.

<small>Tags: [music-as-code] [representation] [symbolic-generation] [editing] [structure] [LLM-agent] · Verification: verified (arXiv HTML full text; project page) · Cluster 02</small>

### `xu2026libretto` — Libretto — Libretto: Giving LLM Agents a Sense of Musical Structure

*Yichen Xu; UC Berkeley; arXiv June 2026 (CC BY 4.0)*

Links: https://arxiv.org/abs/2606.22708 ; https://github.com/Xyc-arch/Libretto ; https://libretto.site/

A text grammar for symbolic music with explicit onset slots, voice declarations and bar-level blocks (timing is readable without accumulating durations), plus a 29-axis "structural fingerprint" (rhythm, harmony, melody, texture, form, variation) calibrated to corpus percentiles. An LLM agent runs generate → measure → *musician-readable feedback* ("reduce harmonic instability") → revise loops; supports gap-filling, whole-piece composition, style morphing and pedagogy drills.

**Evidence.** 314-song Lakh reference corpus; gap-filling pass rate 12% (single shot) → 39% (loop); full-piece generation 94% with retrieval + refinement; copy-risk gates.

**For the studio.** The closest thing to an "annotation-driven compiler": human-legible structural notes steer revision of a text-encoded score in a loop — precisely the compile→annotate→edit cycle, though the feedback is currently generated by metrics rather than by a composer's margin notes.

<small>Tags: [music-as-code] [LLM-agent] [symbolic-generation] [structure] [evaluation] [infilling] · Verification: verified (fetched primary source) · Cluster 06</small>

### `zhang2021cosmic` — COSMIC — A Conversational Interface for Human-AI Music Co-Creation

*Yixiao Zhang, Gus Xia, Mark Levy, Simon Dixon; QMUL C4DM, NYU Shanghai, Apple; NIME 2021*

Links: https://doi.org/10.21428/92fbeb44.110a7a32

An early chatbot-style music co-creation system: natural-language requests are parsed into intents and routed to generation modules (melody, lyrics), and the user iterates by conversation.

**Evidence.** System paper with preliminary demonstration; no large study.

**For the studio.** Precursor of LLM-orchestrated conversational music tools (Loop Copilot, MusicAgent); useful as the origin point of the "conversational vs direct-manipulation" comparison.

<small>Tags: [LLM-agent] [symbolic-generation] [co-creation-framework] · Verification: partial (Crossref metadata verified; content from recall) · Cluster 05</small>

## S3.7. Compile: expressive performance rendering

### `jeong2019virtuosonet` — VirtuosoNet — VirtuosoNet: A Hierarchical RNN-based System for Modeling Expressive Piano Performance

*Dasaem Jeong, Taegyun Kwon, Yoojin Kim, Juhan Nam (KAIST / SNU); ISMIR 2019*

Links: https://archives.ismir.net/ismir2019/paper/000112.pdf ; code: https://github.com/jdasam/virtuosoNet

MusicXML score (with dynamics/articulation/tempo markings) → expressive performance MIDI (tempo, velocity, onset deviation, articulation, pedal) via a hierarchical attention score encoder, CVAE performance encoder (style latent) and measure→note two-level decoder. Trained on 226 pieces / 1,052 Yamaha e-Competition performances aligned to scores.

**Evidence.** Five piano students rated three pieces on seven criteria; significant gains over prior systems, near human quality for lyrical melodies.

**For the studio.** Establishes MusicXML→expressive MIDI as a learnable, style-controllable rendering stage and uses score annotations (markings) as inputs.

<small>Tags: [expression-performance] [notation] [controllability] · Verification: verified (ISMIR PDF fetched) · Cluster 03</small>

### `zhang2024dexter` — DExter / RenderBox — DExter: Learning and Controlling Performance Expression with Diffusion Models; RenderBox: Expressive Performance Rendering with Text Control

*Huan Zhang, Shreyan Chowdhury, Carlos Cancino-Chacón, Jinhua Liang, Simon Dixon, Gerhard Widmer (QMUL / JKU Linz); Applied Sciences 2024 (arXiv Jun 2024). RenderBox: Huan Zhang, Akira Maezawa, Simon Dixon (QMUL / Yamaha); arXiv Feb 2025*

Links: https://arxiv.org/abs/2406.14850 ; https://www.mdpi.com/2076-3417/14/15/6543 ; https://arxiv.org/abs/2502.07711

DExter: diffusion over performance-parameter sequences conditioned on the score and on perceptual *mid-level features*, enabling interpretation generation, steering and style transfer between performers. RenderBox: a diffusion Transformer that renders score+text ("play it tenderly, slightly rushed") directly to multi-instrument *audio* with curriculum learning from synthesis to expressive performance.

**Evidence.** DExter matches prior renderers on quantitative metrics and listening tests while capturing time-varying expressive correlations. RenderBox: strong FAD/CLAP, tempo/pitch accuracy and human ratings of naturalness and prompt adherence.

**For the studio.** Text- and feature-steered expression are the "annotate the performance" layer; RenderBox also points to audio-cluster work (score→audio without a MIDI intermediary).

<small>Tags: [expression-performance] [controllability] [text-conditioning] [audio-generation] · Verification: verified (arXiv abstracts fetched) · Cluster 03</small>

### `borovik2023scoreperformer` — ScorePerformer / PianoFlow — ScorePerformer: Expressive Piano Performance Rendering with Fine-Grained Control; SyMuPe: Affective and Controllable Symbolic Music Performance

*Ilya Borovik, Vladimir Viro (Peachnote); ISMIR 2023. SyMuPe/PianoFlow: Ilya Borovik, Dmitrii Gavrilev, Vladimir Viro; ACM Multimedia 2025*

Links: https://archives.ismir.net/ismir2023/paper/000069.pdf ; https://github.com/ilya16/ScorePerformer ; https://arxiv.org/abs/2511.03425

ScorePerformer: SPMuple tokens (8 score + 4 performance fields), an MMD-VAE Transformer with hierarchical style embeddings at global/bar/beat/onset level, and *direction-marking classifiers* that map words like crescendo, staccato, ritardando to latent deltas — so a user can steer rendering with score-like directions at any granularity (ASAP: 212 pieces, 937 performances). PianoFlow (SyMuPe): conditional flow matching on 2,968 h of aligned score–performance MIDI (PERiScoPe) with emotion and free-text (Flan-T5) controls; 355 notes/s inference.

**Evidence.** ScorePerformer: correlation/MAE on tempo, onset deviation, duration, velocity. PianoFlow: 67.1% pairwise win rate (708 ratings, 26 listeners), preferred over human recordings in 54% of comparisons.

**For the studio.** Expression control via *notated directions and text* at bar/beat/note granularity is exactly annotation-driven rendering; real-time-capable.

<small>Tags: [expression-performance] [controllability] [annotation] [text-conditioning] [real-time] · Verification: verified (ISMIR PDF and arXiv abstract fetched) · Cluster 03</small>

### `wu2022mididdsp` — MIDIDDSP — MIDI-DDSP: Detailed Control of Musical Performance via Hierarchical Modeling

*Yusong Wu, Ethan Manilow, Yi Deng, Rigel Swavely, Kyle Kastner, Tim Cooijmans, Aaron Courville, Cheng-Zhi Anna Huang, Jesse Engel; Mila/Université de Montréal, Northwestern, Google Brain; ICLR 2022 oral (arXiv 2112.09312); Outstanding Paper at NeurIPS 2021 CtrlGen workshop*

Links: https://arxiv.org/abs/2112.09312 ; code https://github.com/magenta/midi-ddsp ; DDSP https://arxiv.org/abs/2001.04643

Three-level hierarchy **notes → performance → synthesis**: from MIDI it predicts per-note expression (vibrato, dynamics, articulation, brightness…), then DDSP synthesis parameters, then audio (URMP monophonic instruments). Users can intervene at any level — write notes, tweak an expression curve, or edit synthesis parameters — or let learned priors fill in.

**Evidence.** Reconstructs high-fidelity audio, predicts performance attributes, allows independent manipulation of expression, and renders new note sequences realistically (listening tests in paper).

**For the studio.** The clearest published instance of a *compiler with intermediate representations*: score → expressive performance → sound, every stage human-editable. Maps one-to-one onto the founder's "compile" metaphor.

<small>Tags: [expression-performance] [audio-generation] [controllability] [editing] [representation] [notation] · Verification: verified (arXiv abstract fetched) · Clusters 01, 03, 04</small>

## S3.8. Compile: audio rendering & symbolic-conditioned audio

### `tsai2025musecontrollite` — MuseControlLite — MuseControlLite: Multifunctional Music Generation with Lightweight Conditioners

*Fang-Duo Tsai, Shih-Lun Wu, Weijaw Lee, et al. (Sheng-Ping Yang, Bo-Rui Chen, Hao-Chung Cheng, Yi-Hsuan Yang); National Taiwan University; ICML 2025.*

Links: https://arxiv.org/abs/2506.18729 ; code/weights https://github.com/fundwotsai2001/MuseControlLite

85M-parameter decoupled cross-attention adapters on **Stable Audio Open** with **rotary positional embeddings** for time-varying conditions—**melody, rhythm, dynamics—plus audio inpainting and outpainting**; 6.75× fewer trainable params than Stable Audio Open ControlNet.

**Evidence.** Melody control accuracy 56.6%→61.1% with RoPE; beats MusicGen-Large and SAO-ControlNet on control metrics at lower cost.

**For the studio.** Practical, open, cheap recipe for a controllable *and* region-editable renderer on a CC-trained base—arguably the best starting point for a studio prototype's audio stage.

<small>Tags: [audio-generation] [controllability] [infilling] [editing] [toolkit] · Verification: verified · Cluster 04</small>

### `zhu2024musichifi` — MusicHiFi — MusicHiFi: Fast High-Fidelity Stereo Vocoding

*Ge Zhu, Juan-Pablo Caceres, Zhiyao Duan, Nicholas J. Bryan; University of Rochester + Adobe Research; IEEE Signal Processing Letters 2024 (arXiv Mar 2024). (Authors partial.)*

Links: https://arxiv.org/abs/2403.10493 ; demo https://MusicHiFi.github.io/web/

Cascade of three GANs—mel → audio vocoder, **bandwidth extension** (downsampling-compatible), **mono → stereo upmix** (downmix-compatible)—to turn low-res mono model outputs into 44.1 kHz stereo quickly.

**Evidence.** Comparable or better quality and spatialisation vs baselines with faster inference.

**For the studio.** A rendering back-end concern: many controllable models output 16–32 kHz mono; this shows the finishing stage can be modular and fast.

<small>Tags: [audio-generation] [toolkit] · Verification: partial · Cluster 04</small>

### `melechovsky2024mustango` — Mustango — Mustango: Toward Controllable Text-to-Music Generation

*Jan Melechovsky, Zixun Guo, Deepanway Ghosal, Navonil Majumder, Dorien Herremans, Soujanya Poria; SUTD (Singapore); NAACL 2024.*

Links: https://arxiv.org/abs/2311.08355 ; code https://github.com/AMAAI-Lab/mustango ; dataset MusicBench

Latent diffusion (Tango lineage) with **MuNet**, a music-domain-knowledge-informed UNet guidance module that consumes chords, beats, key and tempo parsed from the prompt. Releases **MusicBench** (52k music–text pairs, augmented with pitch-shift/tempo/volume changes and MIR-extracted theory captions). Open weights.

**Evidence.** Better controllability (chord/beat/key/tempo accuracy) than MusicGen and AudioLDM2; FAD/KL competitive.

**For the studio.** Demonstrates chord/key/tempo-aware audio generation from structured text—an interface layer between a lead sheet and an audio renderer.

<small>Tags: [audio-generation] [controllability] [text-conditioning] [dataset] [theory-analysis] · Verification: verified · Cluster 04</small>

### `engel2020ddsp` — DDSP — DDSP: Differentiable Digital Signal Processing

*Jesse Engel, Lamtharn (Hanoi) Hantrakul, Chenjie Gu, Adam Roberts; Google Brain (Magenta); ICLR 2020 (arXiv 2001.04643)*

Links: https://arxiv.org/abs/2001.04643 ; https://github.com/magenta/ddsp ; https://magenta.withgoogle.com/ddsp

A library of differentiable synthesizer/effects modules (harmonic additive synth, filtered noise, reverb) so neural nets output *interpretable synthesis parameters* (f0, loudness, harmonic distribution) instead of raw waveforms. Enables independent control of pitch and loudness, extrapolation to unseen pitches, dereverberation, and timbre transfer between instruments with small models.

**Evidence.** High-fidelity monophonic resynthesis without autoregressive or adversarial models; ablations in the paper.

**For the studio.** The interpretable-parameter approach is how a rendering layer can stay *editable* after generation (nudge vibrato, change loudness curve) rather than being a fixed audio blob — consistent with the "compile, then edit again" loop.

<small>Tags: [audio-generation] [controllability] [style-transfer] [toolkit] [expression-performance] · Verification: verified (arXiv abstract fetched) · Cluster 01</small>

### `lin2023cocomulla` — CocoMulla — Content-based Controls for Music Large Language Modeling (Coco-Mulla)

*Liwei Lin, Gus Xia, Junyan Jiang, Yixiao Zhang; NYU Shanghai / MBZUAI / QMUL; arXiv Oct 2023 (rev. 2024); ISMIR 2024 version "Arrange, Inpaint, and Refine".*

Links: https://arxiv.org/abs/2310.17162 ; code https://github.com/Kikyo-16/coco-mulla-repo

Parameter-efficient (<4% params) fine-tuning of MusicGen to accept **chord progressions and drum tracks (MIDI/symbolic) plus pitch/melody content controls** alongside text, trained on <300 songs; supports arrangement and variation from symbolic input.

**Evidence.** Chord/rhythm adherence and quality vs MusicGen baselines; low-resource training.

**For the studio.** Cheap recipe for teaching an existing audio LM to read *the composer's chords and drum MIDI*—the bridge from lead sheet to audio with tiny data.

<small>Tags: [audio-generation] [controllability] [symbolic-generation] [accompaniment] · Verification: verified · Cluster 04</small>

### `lyria2025livemusic` — LiveMusicModels — Live Music Models (Magenta RealTime & Lyria RealTime)

*Lyria Team, Google DeepMind (Caillon, McWilliams, Tarakajian, Simon, Manco, Engel, … Donahue, Han, Roberts; 30+ authors). arXiv Aug 2025 (2508.04651); Magenta RealTime open weights June 2025; Magenta RealTime 2 (MRT2) released later with 230M and 2.4B parameter models.*

Links: https://arxiv.org/abs/2508.04651 ; code: https://github.com/magenta/magenta-realtime (Apache-2.0) ; weights: https://huggingface.co/google/magenta-realtime-2 ; https://magenta.withgoogle.com/mrt2

"Live music models" produce a continuous audio stream with synchronised user control. v1: 800M encoder–decoder transformer over **SpectroStream** (48 kHz stereo codec) tokens, steered by weighted blends of text/audio prompt embeddings from **MusicCoCa**; 10-s context, 2-s chunks; ran on free Colab TPU; trained on ~190k h instrumental stock music; open weights (permissive + bespoke terms). **v2**: ~15× lower latency (40-ms frames, ~200 ms control latency), runs in real time on Apple Silicon (C++/MLX engine), causal sliding-window attention, **MIDI note control (Auto-Strum and precise-onset modes), drums on/off, multi-signal classifier-free guidance**; trained on ~71k h mostly-instrumental stock music with **MT3-inferred MIDI labels**; fine-tuning "coming soon". Open counterpart of Lyria RealTime.

**Evidence.** Outperforms other open-weights music models on automatic quality metrics despite fewer parameters; RTF 1.8× on an H100.

**For the studio.** The only open, on-laptop, **MIDI-steerable real-time audio model**—the closest thing to an AI band member for a keyboardist; also the first open model whose training explicitly pairs audio with (transcribed) symbolic data. Limitation: short context (no long-form structure), instrumental only.

<small>Tags: [audio-generation] [real-time] [controllability] [symbolic-generation] [accompaniment] [toolkit] · Verification: verified (arXiv abstract + HTML fetched) · Clusters 01, 02, 04, 08</small>

### `magenta2022ddspvst` — DDSPVST — DDSP-VST (neural synth/effect plugin + web trainer)

*Magenta team (Jesse Engel et al.); Google; 2022*

Links: https://magenta.withgoogle.com/ddsp-vst ; https://github.com/magenta/ddsp-vst

macOS/Windows VST/AU plugins: a MIDI-playable neural synthesizer and an audio effect that re-timbres any input while preserving pitch and dynamics; a free Colab web trainer builds a personal model from "as little as a couple minutes of audio."

**Evidence.** Product release; no formal study.

**For the studio.** Shows the founder's "insert example audio" annotation can literally become a *trained timbre* in minutes and live inside the DAW.

<small>Tags: [DAW-plugin] [audio-generation] [style-transfer] [product] [multimodal-input] · Verification: verified (official page fetched; release year from recall) · Cluster 01</small>

### `tal2024jasco` — JASCO — Joint Audio and Symbolic Conditioning for Temporally Controlled Text-to-Music Generation

*Or Tal, Alon Ziv, Itai Gat, Felix Kreuk, Yossi Adi; Hebrew University / Meta FAIR; ISMIR 2024 (arXiv Jun 2024).*

Links: https://arxiv.org/abs/2406.10970 ; project https://pages.cs.huji.ac.il/adiyoss-lab/JASCO ; code/weights in AudioCraft

Flow-matching text-to-music model that accepts **symbolic local controls—chord progressions (time-aligned), melody (salience matrix)—and audio controls—separated drum track, full-mix embedding**, via information-bottleneck layers and temporal blurring. Generates ~10-s 32 kHz clips. Open code (MIT) and weights (CC-BY-NC 4.0).

**Evidence.** Objective metrics + human study: comparable quality to baselines with "significantly better and more versatile controls" (chord/melody adherence).

**For the studio.** The clearest open example of **lead-sheet-style conditioning (chords + melody) of an audio model**—the basic "compile a lead sheet to audio" primitive. Clip length and NC license are limits.

<small>Tags: [audio-generation] [controllability] [symbolic-generation] [accompaniment] [text-conditioning] · Verification: verified · Cluster 04</small>

### `wu2024musiccontrolnet` — MusicControlNet — Music ControlNet: Multiple Time-varying Controls for Music Generation

*Shih-Lun Wu (CMU LTI MS), Chris Donahue (CMU), Shinji Watanabe (CMU LTI), Nicholas J. Bryan (Adobe Research). arXiv Nov 2023; IEEE/ACM TASLP 2024. Basis of Adobe's "Project Music GenAI Control" (Feb 2024). Described in the CMU SCS magazine piece "Expanding Music Generation with Adobe" (Marylee Williams).*

Links: https://arxiv.org/abs/2311.07069 ; https://musiccontrolnet.github.io/web/ ; https://magazine.cs.cmu.edu/expanding-music-generation ; Adobe blog: https://blog.adobe.com/en/publish/2024/02/28/adobe-research-audio-creation-editing

Diffusion model over spectrograms with ControlNet-style adapters giving **time-varying controls** — melody, dynamics, and rhythm curves — alongside text; controls are extracted from training audio and may be *partially specified in time* (e.g., a melody for bars 1–4 only, free elsewhere). The user can supply controls by playing, composing, or literally drawing curves.

**Evidence.** 49% more faithful to input melodies than MusicGen's melody conditioning with 35× fewer parameters and 11× less training data; two extra control types beyond text+melody.

**For the studio.** The audio-rendering side of the loop: symbolic/drawn annotations (melody line, dynamics envelope, rhythm) steer audio generation, and *partial* specification is exactly the compile-a-region interaction. CMU–Adobe collaboration shows the industry path.

<small>Tags: [audio-generation] [controllability] [sketch] [text-conditioning] [editing] [multimodal-input] · Verification: verified (arXiv page, magazine article, lab page) · Clusters 02, 04</small>

### `hou2024melodycontrolnet` — MelodyTextControlNetDiT — Editing Music with Melody and Text: Using ControlNet for Diffusion Transformer

*Siyuan Hou, Shansong Liu, Ruibin Yuan, et al. (Wei Xue, Ying Shan, Mangsuo Zhao, Chao Zhang); Tsinghua + Tencent ARC + HKUST; ICASSP 2025 (arXiv Oct 2024). (Authors partial.)*

Links: https://arxiv.org/abs/2410.05151

ControlNet branch on Stable Audio's DiT for **melody-conditioned editing**, using a **top-k constant-Q transform** melody representation to reduce ambiguity, with curriculum learning to balance text vs melody; variable-length generation/editing.

**Evidence.** Better melody-controlled editing than MusicGen while retaining text-to-music quality (open instrumental data).

**For the studio.** Another route to "keep my melody, re-render everything else"—with a representation (CQT peaks) close to a transcribable pitch line.

<small>Tags: [audio-generation] [controllability] [editing] [style-transfer] · Verification: partial (abstract fetched; authors from recall) · Cluster 04</small>

### `novack2024ditto` — DITTO — DITTO: Diffusion Inference-Time T-Optimization for Music Generation / DITTO-2

*Zachary Novack, Julian McAuley, Taylor Berg-Kirkpatrick, Nicholas J. Bryan; UC San Diego + Adobe Research; DITTO: ICML 2024 (oral); DITTO-2: ISMIR 2024.*

Links: https://arxiv.org/abs/2401.12179 ; https://arxiv.org/abs/2405.20289 ; demos https://DITTO-Music.github.io/web/ , https://ditto-music.github.io/ditto2/

**Training-free control**: optimise the initial noise latents of a frozen text-to-music diffusion model through any differentiable feature-matching loss—yielding **inpainting, outpainting, looping, intensity (loudness curve), melody, and musical-structure (self-similarity) control** from one model. DITTO-2 distils the model (consistency-trajectory distillation) and optimises through a one-step surrogate, giving 10–20× speed-up (faster than real time) and new targets such as maximising CLAP text adherence.

**Evidence.** SOTA on nearly all control tasks vs training-based baselines (Music ControlNet) and guidance methods; user-study/objective metrics; DITTO-2 improves both control and quality while much faster.

**For the studio.** General mechanism to turn *any* composer annotation with a computable target (a hummed contour, a dynamics sketch, a form diagram) into a constraint on a frozen renderer—no retraining per annotation type.

<small>Tags: [audio-generation] [controllability] [editing] [infilling] [structure] [annotation] · Verification: verified · Cluster 04</small>

## S3.9. Compile: text-to-music & full-song audio generation

### `ziv2024magnet` — MAGNeT — Masked Audio Generation using a Single Non-Autoregressive Transformer

*Alon Ziv, Itai Gat, Gael Le Lan, et al. (Tal Remez, Felix Kreuk, Alexandre Défossez, Jade Copet, Gabriel Synnaeve, Yossi Adi); Meta FAIR; ICLR 2024.*

Links: https://arxiv.org/abs/2401.04577 ; code/weights in AudioCraft

Non-autoregressive masked generative modelling over EnCodec token streams with span masking, iterative decoding, and rescoring by an external model; hybrid AR-then-NAR variant. ~7× faster than MusicGen at comparable quality. Text only; weights CC-BY-NC.

**Evidence.** Human + objective evaluation vs MusicGen/AudioGen; latency/throughput trade-offs analysed.

**For the studio.** Masked/iterative decoding is inherently editable (re-mask a region and re-decode)—a natural fit for local re-compilation.

<small>Tags: [audio-generation] [infilling] [text-conditioning] · Verification: verified · Cluster 04</small>

### `agostinelli2023musiclm` — MusicLM — MusicLM: Generating Music From Text

*Andrea Agostinelli, Timo I. Denk, Zalán Borsos, et al. (13 authors incl. Jesse Engel, Neil Zeghidour, Christian Frank); Google Research; arXiv, Jan 2023.*

Links: https://arxiv.org/abs/2301.11325 ; project https://google-research.github.io/seanet/musiclm/examples/ ; dataset MusicCaps (Kaggle)

Hierarchical sequence-to-sequence generation: MuLan (joint music–text embedding) conditions a w2v-BERT semantic-token stage and a SoundStream acoustic-token stage (AudioLM lineage). Generates 24 kHz music from text, and—crucially for this project—can be conditioned on a **hummed or whistled melody** plus text (melody tokens from a dedicated embedding), transforming the user's melody into the described style. Released **MusicCaps** (5.5k expert-captioned 10-s clips), the de-facto text-to-music benchmark. Closed weights; productised as MusicFX / Dream Track.

**Evidence.** Outperformed Mubert and Riffusion in audio quality and text adherence (FAD, KLD, MuLan cycle consistency + human listening tests).

**For the studio.** The first mainstream demonstration that a *hummed melody* can steer a text-to-music model—precisely the "hum or sing" annotation channel in the studio vision. MusicCaps remains the standard evaluation set.

<small>Tags: [audio-generation] [text-conditioning] [humming] [multimodal-input] [dataset] [evaluation] · Verification: verified (abstract + HF paper page for authors) · Cluster 04</small>

### `mariani2024msdm` — MSDM — Multi-Source Diffusion Models for Simultaneous Music Generation and Separation

*Giorgio Mariani, Irene Tallini, Emilian Postolache, et al. (Michele Mancusi, Luca Cosmo, Emanuele Rodolà); Sapienza University of Rome (GLADIA); ICLR 2024 (oral).*

Links: https://arxiv.org/abs/2302.02257 ; code https://github.com/gladia-research-group/multi-source-diffusion-models

Learns the *joint* score of stems (Slakh2100: bass, drums, guitar, piano) so one diffusion model does **total generation, source separation (Dirac-likelihood inference), and source imputation—generate missing stems given the others** (e.g., piano to fit given drums). Open code/weights (research).

**Evidence.** First single model for both generation and separation; competitive separation SI-SDR on Slakh; qualitative imputation.

**For the studio.** "Partial-score → complete arrangement" as *conditional sampling in a joint stem model*; also gives separation for free (annotating existing recordings).

<small>Tags: [audio-generation] [accompaniment] [infilling] [transcription] · Verification: verified · Cluster 04</small>

### `liu2024audioldm2` — AudioLDM 2 — AudioLDM 2: Learning Holistic Audio Generation with Self-supervised Pretraining

*Haohe Liu, Yi Yuan, Xubo Liu, et al. (Xinhao Mei, Qiuqiang Kong, Qiao Tian, Yuping Wang, Wenwu Wang, Yuxuan Wang, Mark D. Plumbley); Surrey / ByteDance; IEEE/ACM TASLP 2024 (arXiv Aug 2023).*

Links: https://arxiv.org/abs/2308.05734 ; code https://github.com/haoheliu/AudioLDM2 ; https://audioldm.github.io/audioldm2

Introduces a "language of audio" (LOA): AudioMAE features as an intermediate representation; a GPT-2 translates any conditioning modality (text, phonemes, audio) into LOA, then latent diffusion renders. One framework for text-to-audio, text-to-music, text-to-speech. Open weights (music-specific checkpoint). Text only for music; no explicit symbolic control.

**Evidence.** SOTA/competitive on AudioCaps, MusicCaps, LJSpeech.

**For the studio.** Shows how a general intermediate representation lets one renderer serve many conditioning types—an architectural pattern relevant to a "compiler" that must accept notation, text, hums, and audio examples.

<small>Tags: [audio-generation] [text-conditioning] [representation] · Verification: verified (abstract); author list from memory (partial) · Cluster 04</small>

### `liu2023audioldm` — AudioLDM — AudioLDM: Text-to-Audio Generation with Latent Diffusion Models

*Haohe Liu, Zehua Chen, Yi Yuan, et al. (Xinhao Mei, Xubo Liu, Danilo Mandic, Wenwu Wang, Mark D. Plumbley); University of Surrey / Imperial; ICML 2023.*

Links: https://arxiv.org/abs/2301.12503 ; code https://github.com/haoheliu/AudioLDM ; https://audioldm.github.io

Latent diffusion in a VAE-compressed mel space, conditioned on CLAP embeddings (train on audio embeddings, infer from text). Enables **zero-shot text-guided manipulation—style transfer, inpainting, super-resolution**—without task-specific training. Trainable on a single GPU. Open code and weights.

**Evidence.** SOTA TTA on AudioCaps by FD/IS/KL and subjective ratings at the time.

**For the studio.** Template for "inpaint a region, keep the rest" in the audio domain; also the base model for ZETA/ZEUS editing and MusicMagus.

<small>Tags: [audio-generation] [text-conditioning] [editing] [infilling] · Verification: verified · Cluster 04</small>

### `heartmula2026` — HeartMuLa — HeartMuLa family (HeartMuLa, HeartCodec, HeartTranscriptor, HeartCLAP)

*HeartMuLa org (HKUST-affiliated team — institution partial); releases Dec 2025 – Feb 2026 (HeartMuLa-oss-3B "happy-new-year" Feb 13 2026); 7B internal.*

Links: https://github.com/HeartMuLa/heartlib

Open-source song foundation model family: **HeartMuLa** (music LM, 3B open; 7B internal), **HeartCodec** (12.5 Hz audio codec), **HeartTranscriptor** (Whisper-based lyrics transcription), **HeartCLAP** (audio–text alignment). Inputs: lyrics + comma-separated tags (reference-audio conditioning planned); outputs full songs (default ≤240 s) at RTF≈1.0; multi-GPU or lazy-loaded single GPU. **Apache-2.0** code and weights.

**Evidence.** Self-reported: 7B "comparable to Suno in musicality, fidelity and controllability"; no external benchmark.

**For the studio.** Representative of the 2026 wave of permissively licensed song models; its bundled transcription/CLAP tools are useful for annotation pipelines.

<small>Tags: [audio-generation] [text-conditioning] [toolkit] [transcription] · Verification: verified (README); institution partial · Cluster 04</small>

### `copet2023musicgen` — MusicGen — Simple and Controllable Music Generation

*Jade Copet, Felix Kreuk, Itai Gat, et al. (Tal Remez, David Kant, Gabriel Synnaeve, Yossi Adi, Alexandre Défossez); Meta AI (FAIR); NeurIPS 2023.*

Links: https://arxiv.org/abs/2306.05284 ; code https://github.com/facebookresearch/audiocraft (AudioCraft)

Single-stage autoregressive transformer LM over interleaved EnCodec token streams (codebook interleaving patterns replace cascades). Conditioning: text (T5) and **melody via chromagram** of a reference audio (e.g., a whistled/played melody). 300M/1.5B/3.3B, mono and stereo, 32 kHz, ~30 s. Open code (MIT) and weights (**CC-BY-NC 4.0**, non-commercial). Widely fine-tuned (Coco-Mulla, Instruct-MusicGen, MusicGen-Style, MusicGen-Stem all build on it).

**Evidence.** Human study (overall quality, text relevance, melody similarity) and objective metrics (FAD, KL, CLAP) vs MusicLM, Riffusion, Mousai, Noise2Music; ablations on interleaving patterns.

**For the studio.** The most-extended open text-to-music backbone; chromagram melody conditioning is a coarse but usable "sketch → audio" channel; non-commercial weights are a constraint for a shipped product.

<small>Tags: [audio-generation] [text-conditioning] [controllability] [humming] [toolkit] · Verification: verified · Cluster 04</small>

### `nistal2024diffariff` — DiffARiff — Diff-A-Riff: Musical Accompaniment Co-creation via Latent Diffusion Models

*Javier Nistal, Marco Pasini, Cyran Aouameur, Maarten Grachten, Stefan Lattner; Sony CSL Paris; ISMIR 2024. (Follow-ups: Diff-A-Riff v2 / "Diff-MST" lineage at Sony CSL, 2025.)*

Links: https://arxiv.org/abs/2406.08384 ; https://sonycslparis.github.io/diffariff-companion/ — no weights

Latent diffusion (consistency autoencoder, 48 kHz pseudo-stereo) that generates a **single instrumental accompaniment track fitting a given music context (mix)**, steerable by **audio reference (CLAP) and/or text**; low compute; designed for DAW workflows rather than whole-song generation.

**Evidence.** Objective metrics + listening tests vs baselines; ablations of conditioning.

**For the studio.** Explicitly *co-creation*-oriented: one part at a time, matched to context, with example-audio steering—matches the "insert example audio" and "compile one part" primitives.

<small>Tags: [audio-generation] [accompaniment] [co-creation-framework] [multimodal-input] · Verification: verified · Cluster 04</small>

### `parker2024stemgen` — StemGen — StemGen: A Music Generation Model That Listens

*Julian D. Parker, Janne Spijkervet, Katerina Kosta, et al. (Furkan Yesiler, Boris Kuznetsov, Ju-Chiang Wang, Matt Avent, Jitong Chen, Duc Le); ByteDance SAMI; ICASSP 2024.*

Links: https://arxiv.org/abs/2312.08723 ; examples https://julian-parker.github.io/stemgen/ — no weights

Non-autoregressive masked transformer (MAGNeT/SoundStorm-style) that takes an **existing multi-stem musical context** and generates a **new stem** (e.g., bass given drums+keys) with a category token; improvements: causal bias sampling, classifier-free guidance over context.

**Evidence.** FAD and MIR-descriptor alignment (key/tempo/chroma coherence with context) comparable to text-conditioned models; trained on open + proprietary data.

**For the studio.** Frames generation as *response to what's already there*—the essence of a co-arranger adding parts under a composer's material.

<small>Tags: [audio-generation] [accompaniment] [mixed-initiative] · Verification: verified (arXiv + ICASSP listing) · Cluster 04</small>

### `gong2025acestep` — ACEStep1 — ACE-Step: A Step Towards Music Generation Foundation Model (v1.0)

*Junmin Gong, Sean Zhao (Wenxiao Zhao), Sen Wang, Shengyuan Xu, Jing Guo; **ACE Studio + StepFun**; arXiv May/Jun 2025; released May 2025.*

Links: https://arxiv.org/abs/2506.00045 ; code https://github.com/ace-step/ACE-Step ; https://ace-step.github.io

Diffusion (flow) model over Sana's Deep Compression AutoEncoder (DCAE) latents with a lightweight *linear* transformer; semantic alignment via REPA to MERT and m-hubert. Generates up to 4 min of music with vocals in ~20 s on an A100 (≈15× faster than LM-based systems). Supports **variations, repainting (local re-generation of a time range), lyric editing (change words while keeping melody/accompaniment), lyric2vocal, singing2accompaniment, voice cloning, remixing** via LoRA controllers. Inputs: tags/caption + structured lyrics; audio reference; no MIDI. Apache-2.0.

**Evidence.** Claims better structural coherence than diffusion-only baselines; internal comparisons only.

**For the studio.** First fully open model with a *menu of editing operations* (repaint / lyric-edit / variation) rather than one-shot generation—effectively an open Suno with edit primitives; Apache-2.0.

<small>Tags: [audio-generation] [editing] [infilling] [text-conditioning] [toolkit] · Verification: verified · Cluster 04</small>

### `gong2026acestep15` — ACEStep15 — ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation

*Junmin Gong, Yulin Song, Wenxiao Zhao, Sen Wang, Shengyuan Xu, et al.; **co-led by ACE Studio and StepFun**; arXiv Jan 31 / Feb 6 2026; XL (4B) release Apr 2 2026; repo v0.1.8 May 18 2026.*

Links: https://arxiv.org/abs/2602.00744 ; code https://github.com/ace-step/ACE-Step-1.5 ; https://ace-step.github.io

**Hybrid LM-planner + Diffusion Transformer**: a language model (0.6B/1.7B/4B) converts a user query into a "song blueprint" (metadata, lyrics, captions via chain-of-thought), which conditions a DiT decoder over DCAE latents. New in 1.5 vs 1.0: LM planner; **intrinsic RL alignment** (no external reward model); **XL 4B DiT** series (base/sft/turbo); 8-step turbo; **cover generation, repainting (selective local editing), vocal-to-accompaniment, track separation, multi-track layering, lyric-structure control, BPM/key/time-signature metadata control, audio understanding (BPM/key extraction)**, 50+ languages, **LoRA from a few songs**. Speed: <2 s per full song on A100, <10 s on RTX 3090; runs from <4–6 GB VRAM (2B turbo, DiT only) to ≥24 GB (XL sft + 4B LM); CUDA/ROCm/Intel XPU/macOS MLX/CPU; Gradio UI, REST/Python API, **VST3 plugin**. **MIT license.** No MIDI/chord input; no training-data statement.

**Evidence.** Tech report claims "quality beyond most commercial music models" (internal listening tests); no third-party benchmark.

**For the studio.** The strongest open candidate for the studio's *audio renderer/arranger* today: permissive license, consumer hardware, DAW plugin, and native repaint/cover/vocal→BGM primitives. Its LM-planner is essentially a "compiler front-end" from intent to blueprint—the studio can replace that planner with the composer's notation + annotations. Missing symbolic conditioning is the gap to fill (LoRA/ControlNet-style adapters on the DiT).

<small>Tags: [audio-generation] [editing] [infilling] [accompaniment] [LLM-agent] [toolkit] [DAW-plugin] · Verification: verified (README + arXiv) · Cluster 04</small>

### `prajwal2024musicflow` — MusicFlow — MusicFlow: Cascaded Flow Matching for Text Guided Music Generation

*K R Prajwal, Bowen Shi, Matthew Le, et al. (Apoorv Vyas, Andros Tjandra, Mahi Luthra, Baishan Guo, Huiyu Wang, Triantafyllos Afouras, David Kant, Wei-Ning Hsu); Meta FAIR; ICML 2024 (arXiv Oct 2024).*

Links: https://arxiv.org/abs/2410.20478 — no public code/weights

Two flow-matching networks: text → HuBERT semantic units, then (text, semantic) → EnCodec acoustic features. Trained with masked prediction so the same model performs **continuation and infilling** zero-shot. 2–5× smaller than MusicGen with comparable quality; non-autoregressive.

**Evidence.** Competitive FAD/CLAP on MusicCaps with 50–80% fewer parameters; infilling evaluated by masking spans.

**For the studio.** Masked-prediction training is the principled route to "recompile this span given surrounding context"; also shows flow matching as a fast alternative to AR decoding.

<small>Tags: [audio-generation] [infilling] [text-conditioning] · Verification: verified · Cluster 04</small>

### `li2023jen1` — JEN-1 — JEN-1: Text-Guided Universal Music Generation with Omnidirectional Diffusion Models

*Peike Li, Boyu Chen, Yao Yao, et al. (Yikai Wang, Allen Wang, Alex Wang); Futureverse; arXiv, Aug 2023 (also IEEE CAI 2024).*

Links: https://arxiv.org/abs/2308.04729 ; demo https://www.jenmusic.ai (product) — no code

Latent diffusion in a masked-autoencoder latent with "omnidirectional" training that mixes bidirectional and autoregressive (causal) modes so one model does **text-to-music, inpainting, and continuation**. Text only; closed weights (commercial product "JEN").

**Evidence.** Claims better FAD/CLAP than MusicGen and Noise2Music on MusicCaps with ~22.6% of MusicGen's parameters.

**For the studio.** Early proof that generation + region-inpainting + continuation can be one model—the three primitives of an audio "recompile" step.

<small>Tags: [audio-generation] [infilling] [editing] [text-conditioning] · Verification: verified · Cluster 04</small>

### `dhariwal2020jukebox` — Jukebox — Jukebox: A Generative Model for Music

*Prafulla Dhariwal, Heewoo Jun, Christine Payne, et al. (Jong Wook Kim, Alec Radford, Ilya Sutskever); OpenAI; arXiv, 2020.*

Links: https://arxiv.org/abs/2005.00341 ; code https://github.com/openai/jukebox ; samples https://jukebox.openai.com

First raw-audio model to generate minutes-long songs *with singing*. Multi-scale VQ-VAE compresses 44.1 kHz audio into three levels of discrete codes; autoregressive Transformers (up to 5B) model the top level and upsample. Conditioning: artist, genre, and unaligned lyrics; also "primed" continuation from an audio excerpt. No symbolic conditioning; no editing beyond continuation; extremely slow (hours per minute of audio).

**Evidence.** Qualitative; human-perceived coherence "up to multiple minutes"; lyrics conditioning improved singing controllability. No formal listening study reported in the abstract.

**For the studio.** Historical anchor for text/metadata-to-song; also the encoder later reused as a feature extractor for music understanding (e.g., LLark). Shows the cost of end-to-end audio without symbolic structure.

<small>Tags: [audio-generation] [history] [text-conditioning] · Verification: verified · Cluster 04</small>

### `huang2023noise2music` — Noise2Music — Noise2Music: Text-conditioned Music Generation with Diffusion Models

*Qingqing Huang, Daniel S. Park, Tao Wang, et al. (15 authors incl. Quoc V. Le, Wei Han); Google; arXiv, Feb 2023.*

Links: https://arxiv.org/abs/2302.03917 ; examples https://google-research.github.io/noise2music

Cascaded diffusion: a generator produces an intermediate representation (low-fi waveform or spectrogram) from text, a cascader upsamples to 24 kHz 30-s clips. Training captions were pseudo-labelled at scale using an LLM (to generate candidate descriptions) and MuLan (to score them). Text only; no editing, no symbolic control; closed.

**Evidence.** Captures genre, tempo, instrumentation, mood, era; competitive FAD/MuLan metrics vs MusicLM (paper).

**For the studio.** Establishes the LLM-pseudo-labelling recipe for building text–music datasets—reusable when building annotation corpora for a symbolic-first studio.

<small>Tags: [audio-generation] [text-conditioning] [dataset] · Verification: verified · Cluster 04</small>

### `yuan2025yue` — YuE — YuE: Scaling Open Foundation Models for Long-Form Music Generation

*Ruibin Yuan, Hanfeng Lin, Shuyue Guo, Ge Zhang, Jiahao Pan, et al. (44 authors); Multimodal Art Projection (M-A-P) / HKUST / others; arXiv Mar 2025 (v2 Sep 2025); released Jan 2025.*

Links: https://arxiv.org/abs/2503.08638 ; code/weights https://github.com/multimodal-art-projection/YuE

LLaMA-2-based two-stage LM (7B stage-1 over semantic tokens + 1B stage-2 acoustic + upsampler) for **lyrics-to-song up to 5 min** with **track-decoupled next-token prediction** (vocal and accompaniment tokens interleaved), structural progressive conditioning (segment-by-segment), and **in-context learning with a 30-s audio prompt** (single or dual-track) for style/voice transfer; bidirectional generation. Multilingual (EN/ZH/YUE/JA/KO). **Apache-2.0** code and weights, commercial use encouraged. Heavy: 24 GB VRAM minimum, ~360 s per 30 s on a 4090.

**Evidence.** Human preference and objective metrics vs Suno/Udio-class systems (claims parity/superiority on some axes); strong MARBLE understanding transfer.

**For the studio.** Proof that open lyrics-to-song at commercial quality is possible; dual-track generation yields separable vocal/accompaniment stems; ICL-from-audio is a form of "insert example audio" annotation.

<small>Tags: [audio-generation] [text-conditioning] [accompaniment] [multimodal-input] · Verification: verified · Cluster 04</small>

### `forsgren2022riffusion` — Riffusion → ProducerAI → Google Flow Music — Riffusion (spectrogram Stable Diffusion) and its 2025–2026 commercial afterlife

*Seth Forsgren & Hayk Martiros (Dec 2022, hobby project); Riffusion Inc. ($4M 2023); public beta with in-house "FUZZ" model Jan 2025; rebranded **Producer.ai / ProducerAI** (Jul 2025); **acquired by Google Feb 24, 2026** (team joined Google Labs + DeepMind); relaunched on Lyria 3 and renamed **Google Flow Music** Apr 2026.*

Links: https://en.wikipedia.org/wiki/Riffusion ; https://www.musicbusinessworldwide.com/google-acquires-ai-music-platform-and-suno-challenger-producerai/ ; https://9to5google.com/2026/04/20/producerai-becomes-google-flow-music/ ; https://flowmusic.app

Original Riffusion fine-tuned Stable Diffusion on mel-spectrogram images and inverted them to audio; used latent interpolation to loop/morph. ProducerAI pivoted to a **conversational, multi-turn refinement UX** ("creative collaborator") rather than one-shot prompts. Flow Music (Gemini + Lyria 3/3.5) offers "replace & extend" of specific sections, iterative variation, lyrics/vocals, SynthID watermarking, integration with Nano Banana (art) and Veo (video); included in Google AI plans.

**Evidence.** No papers; product claims only.

**For the studio.** Case study of the market moving from single-shot prompt to conversational, section-level iteration—the studio's loop, but audio-only and without notation. Also a warning: independent open-ish players get absorbed by platforms.

<small>Tags: [audio-generation] [product] [editing] [history] [LLM-agent] · Verification: verified (Wikipedia + MBW + 9to5Google) · Cluster 04</small>

### `rouard2025musicgenstem` — MusicGenStem — MusicGen-Stem: Multi-stem Music Generation and Edition through Autoregressive Modeling

*Simon Rouard, Robin San Roman, Yossi Adi, Axel Roebel; IRCAM / Meta; ICASSP 2025.*

Links: https://arxiv.org/abs/2501.01757 ; demo https://simonrouard.github.io/musicgenstem/ ; weights promised (AudioCraft)

Trains **one EnCodec-style codec per stem (bass, drums, other)** and a MusicGen-style LM over the parallel token streams, so it can generate full mixes *or* **edit/regenerate one stem given the others** ("bass on top of existing drums"), enabling iterative, mixed-initiative composition. Text conditioning; ~30 s.

**Evidence.** Objective metrics + subjective tests on stem-conditional generation quality and coherence.

**For the studio.** Directly implements "compile one part while others are fixed"—a stem-wise loop; also shows per-stem codecs as a representation choice.

<small>Tags: [audio-generation] [accompaniment] [editing] [mixed-initiative] [representation] · Verification: verified · Cluster 04</small>

### `evans2024stableaudioopen` — StableAudioOpen — Stable Audio Open

*Stability AI; Stable Audio Open 1.0 paper 31 July 2024 (Evans, Parker, Carr, Zukowski, Taylor, Pons; ICASSP 2025); Stable Audio 2.5 launched 10 Sept 2025; WMG–Stability partnership 19 Nov 2025 (UMG–Stability Oct 2024).*

Links: https://arxiv.org/abs/2407.14358 ; https://huggingface.co/stabilityai/stable-audio-open-1.0 ; https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale

Open-weights text-to-audio DiT (≈1.2B) generating 44.1 kHz stereo up to 47 s, trained **only on Creative Commons audio from Freesound and the Free Music Archive** (≈486k recordings). Weights under the Stability AI Community License (free below revenue threshold). Text + timing conditioning; no symbolic input; commonly used as the base for controllable adapters (MuseControlLite, Melody+Text ControlNet-DiT, Sketch2Sound).

**Evidence.** Competitive FDopenl3/KL/CLAP vs closed models on AudioCaps and Song Describer; quality gap on music with vocals acknowledged.

**For the studio.** The cleanest-provenance open music/sound model; the natural base for fine-tuning region-editing and symbolic-conditioning adapters for an open-source studio.

<small>Tags: [product] [audio-generation] [text-conditioning] [ethics-legal] [dataset] · Verification: verified · Clusters 04, 08</small>

### `evans2024longform` — StableAudio2 — Long-form Music Generation with Latent Diffusion (Stable Audio 2.0)

*Zach Evans, Julian D. Parker, CJ Carr, Zack Zukowski, Josiah Taylor, Jordi Pons; Stability AI; ISMIR 2024 (arXiv Apr 2024). Predecessor: "Fast Timing-Conditioned Latent Audio Diffusion" (Stable Audio 1.0, ICML 2024, arXiv 2402.04825).*

Links: https://arxiv.org/abs/2404.10301 ; code https://github.com/Stability-AI/stable-audio-tools ; product https://stableaudio.com

Diffusion transformer over a highly compressed (21.5 Hz) continuous latent from a new autoencoder; **timing conditioning** (start time, total length) lets the user choose duration and position; generates full 4 m 45 s stereo 44.1 kHz tracks with intro/development/outro; **audio-to-audio style transfer** by initialising from a user's audio. Stable Audio 1.0 introduced timing conditioning and 95-s stereo. Weights of 1.0/2.0 not open (trained on licensed AudioSparx data); the open sibling is Stable Audio Open.

**Evidence.** Better FDopenl3, KL, CLAP than baselines; listening test confirmed structural coherence over long durations.

**For the studio.** Timing conditioning is a simple, explicit *structural* control (where in the piece am I?) that composers understand; audio-to-audio initialisation is a re-rendering primitive.

<small>Tags: [audio-generation] [text-conditioning] [structure] [style-transfer] [controllability] · Verification: verified · Cluster 04</small>

### `liu2025songgen` — SongGen — SongGen: A Single Stage Auto-regressive Transformer for Text-to-Song Generation

*Zihan Liu, Shuangrui Ding, Zhixiong Zhang, et al. (Xiaoyi Dong, Pan Zhang, Yuhang Zang, Yuhang Cao, Dahua Lin, Jiaqi Wang); Shanghai AI Lab / CUHK; ICML 2025.*

Links: https://arxiv.org/abs/2502.13128 ; code/weights https://github.com/LiuZH-19/SongGen

1.3B single-stage AR transformer over X-Codec tokens; inputs = lyrics + descriptive text + optional 3-s voice reference; **mixed mode** (vocals+accompaniment jointly, "Mixed Pro" with auxiliary vocal target) and **dual-track mode** (separate vocal and accompaniment streams, interleaved). 30-s English songs; **Apache-2.0**; fully open data pipeline (~2k h).

**Evidence.** Ablations of token patterns across modes; objective + MOS vs baselines.

**For the studio.** Small, fully open, and produces *separated* vocal/accompaniment—useful as a research baseline for stem-aware rendering.

<small>Tags: [audio-generation] [text-conditioning] [accompaniment] [toolkit] · Verification: verified · Cluster 04</small>

### `ning2025diffrhythm` — DiffRhythm — DiffRhythm: Blazingly Fast and Embarrassingly Simple End-to-End Full-Length Song Generation with Latent Diffusion

*Ziqian Ning, Huakang Chen, Yuepeng Jiang, et al. (Chunbo Hao, Guobin Ma, Shuai Wang, Jixun Yao, Lei Xie); ASLP Lab, Northwestern Polytechnical University; ACL 2025 (arXiv Mar 2025); DiffRhythm 2 arXiv 2510.22950 (Oct 2025).*

Links: https://arxiv.org/abs/2503.01183 ; code/weights https://github.com/ASLP-lab/DiffRhythm

Non-autoregressive latent diffusion (DiT) generating **full songs up to 4 m 45 s in ~10 s** from **timestamped lyrics (.lrc) + a style prompt (text or reference audio)**; instrumental mode; v1.2 adds extension/editing; DiffRhythm+ variant. **Apache-2.0** code and weights; ≥8 GB VRAM.

**Evidence.** Objective (FAD, intelligibility) and subjective results vs Suno/YuE-class baselines.

**For the studio.** Sentence-level lyric timestamps are a *structural, time-aligned* condition—closer to a score than free text; speed makes iterative re-rendering practical.

<small>Tags: [audio-generation] [text-conditioning] [structure] [editing] · Verification: verified · Cluster 04</small>

## S3.10. Compile: music-understanding models as critics

### `wu2023clap` — LAION-CLAP — Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation

*CLAP: Yusong Wu et al. (LAION-CLAP, ICASSP 2023) and Elizalde et al. (Microsoft CLAP, 2023). MusicCaps: Agostinelli et al. (MusicLM, 2023) — 5.5k 10-s AudioSet clips with expert captions. Song Describer Dataset: Ilaria Manco, Benno Weck et al. (NeurIPS 2023 ML4Audio workshop) — 1.1k crowd captions on 706 CC-licensed full tracks.*

Links: https://arxiv.org/abs/2211.06687 ; https://www.kaggle.com/datasets/googleai/musiccaps ; https://arxiv.org/abs/2311.10057

Contrastive text–audio encoders (HTSAT + RoBERTa) with feature fusion for variable-length audio; music-specific checkpoints exist. The de-facto text conditioner (AudioLDM, Stable Audio Open, Diff-A-Riff) and evaluation metric ("CLAP score").

**Evidence.** Used across MusicGen/AudioLDM/Stable Audio papers; 2025 studies show CLAP score correlates only moderately with human preference.

**For the studio.** Text is one of the studio's annotation modalities; CLAP-style alignment scores can be a *soft* check that a rendered passage matches a textual annotation, not a quality metric.

<small>Tags: [representation] [text-conditioning] [evaluation] [dataset] · Verification: verified · Clusters 04, 08</small>

### `tang2024salmonn` — SALMONN — SALMONN: Towards Generic Hearing Abilities for Large Language Models

*Changli Tang, Wenyi Yu, Guangzhi Sun, et al. (Xianzhao Chen, Tian Tan, Wei Li, Lu Lu, Zejun Ma, Chao Zhang); Tsinghua + ByteDance; ICLR 2024.*

Links: https://arxiv.org/abs/2310.13289 ; code https://github.com/bytedance/SALMONN

Whisper (speech) + BEATs (audio) encoders → Q-Former → Vicuna; handles speech, audio events **and music** (captioning, QA); "activation tuning" unlocks emergent tasks (audio storytelling). Open weights.

**Evidence.** Competitive on ASR/AST/emotion/music captioning; emergent zero-shot abilities.

**For the studio.** General "hearing" LLM able to describe hummed input, speech instructions and music in one model—relevant to a multimodal annotation front-end.

<small>Tags: [LLM-agent] [multimodal-input] [annotation] · Verification: verified · Cluster 04</small>

### `zhu2025muq` — MuQ — MuQ: Self-Supervised Music Representation Learning with Mel Residual Vector Quantization

*Haina Zhu, Yizhi Zhou, Hangting Chen, et al. (Jianwei Yu, Ziyang Ma, Rongzhi Gu, Yi Luo, Wei Tan, Xie Chen); Tencent AI Lab + SJTU; arXiv Jan 2025.*

Links: https://arxiv.org/abs/2501.01108 ; code/weights https://github.com/tencent-ailab/MuQ

SSL music encoder using a light **Mel-RVQ** tokenizer as target (more stable/efficient than random projection or MERT's teachers) and **MuQ-MuLan**, a contrastive music–text model (open MuLan analogue). Open weights.

**Evidence.** Beats MERT and MusicFM on downstream tasks with only 0.9k h pretraining; SOTA zero-shot tagging on MagnaTagATune.

**For the studio.** An open MuLan-style text–music embedding is needed for retrieval, text-adherence scoring, and DITTO/Text2FX-style optimisation targets.

<small>Tags: [representation] [text-conditioning] [evaluation] [toolkit] · Verification: verified (abstract); authors partial · Cluster 04</small>

### `gardner2024llark` — LLark — LLark: A Multimodal Instruction-Following Language Model for Music

*Josh Gardner, Simon Durand, Daniel Stoller, Rachel M. Bittner; Spotify Research; ICML 2024.*

Links: https://arxiv.org/abs/2310.07160 ; code https://github.com/spotify-research/llark (training code; no weights)

Jukebox-5B encoder + Llama-2 trained on instruction data auto-generated from open datasets' annotations (MusicCaps, YouTube8M-MusicTextClips, MusicNet, FMA, MTG-Jamendo, MagnaTagATune) for **music understanding (key, tempo, instruments), captioning and reasoning**.

**Evidence.** Matches/outperforms baselines on understanding; high human agreement on captioning/reasoning; trained entirely on open data/models.

**For the studio.** Demonstrates that theory-level facts (key, tempo) can be produced conversationally from audio—an ingredient for automatic annotation of recordings.

<small>Tags: [LLM-agent] [annotation] [theory-analysis] · Verification: verified · Cluster 04</small>

### `zhao2024openmu` — OpenMU — OpenMU: Your Swiss Army Knife for Music Understanding

*Mengjie Zhao, Zhi Zhong, Zhuoyuan Mao, et al. (Shiqi Yang, Wei-Hsiang Liao, Shusuke Takahashi, Hiromi Wakaki, Yuki Mitsufuji); Sony; arXiv Oct 2024.*

Links: https://arxiv.org/abs/2410.15573 ; code/data https://github.com/mzhaojp22/openmu

**OpenMU-Bench** (≈1M examples) covering music captioning, QA/reasoning, **lyrics understanding, ABC-notation understanding and tool use**; **OpenMU** model (LLaVA-style two-stage training) trained on it. Open.

**Evidence.** Outperforms MU-LLaMA on the bench; ablations across task types.

**For the studio.** The only understanding benchmark that mixes *audio* with *symbolic notation (ABC)* and tool use—closest to what a studio critic/annotator must do.

<small>Tags: [LLM-agent] [evaluation] [dataset] [notation] [music-as-code] · Verification: verified (GitHub README) · Cluster 04</small>

### `chu2024qwen2audio` — AudioLLMs — Qwen2-Audio (2024) / Qwen2.5-Omni (2025) / Gemini 2.5 audio (2025)

*Qwen2-Audio: Yunfei Chu, Jin Xu, Qian Yang, et al.; Alibaba Qwen; arXiv Jul 2024; 7B, Apache-2.0 weights. Qwen2.5-Omni: Qwen team; arXiv Mar 2025 (Thinker–Talker, 7B/3B, Apache-2.0). Gemini 2.5 Pro/Flash: Google DeepMind, 2025; native audio input (hours-long), closed API.*

Links: https://arxiv.org/abs/2407.10759 ; https://arxiv.org/abs/2503.20215 ; https://deepmind.google/models/gemini/

General audio-language models with two modes (voice chat, audio analysis); trained on speech, sounds and music; can describe music (genre, instruments, mood), roughly estimate tempo and answer music questions, but are not music-specialised. Gemini 2.5 is the strongest closed generalist for long-audio understanding and is what the Music AI Sandbox / Flow Music pair with Lyria.

**Evidence.** Qwen2-Audio beat Gemini-1.5-pro on AIR-Bench audio instruction tasks; on MuChoMusic-style music tests, open audio LLMs still show text over-reliance (see MuChoMusic).

**For the studio.** Off-the-shelf multimodal front-ends for parsing spoken/hummed/verbal annotations and producing first-draft critiques; not yet trustworthy for fine music-theory judgments.

<small>Tags: [LLM-agent] [multimodal-input] [annotation] · Verification: partial (Qwen2-Audio abstract verified; others recall) · Cluster 04</small>

### `castellon2021codified` — JukeMIR — Codified Audio Language Modeling Learns Useful Representations for Music Information Retrieval

*Rodrigo Castellon, Chris Donahue, Percy Liang; Stanford. ISMIR 2021 (Best Paper runner-up).*

Links: https://arxiv.org/abs/2107.05677 ; code: https://github.com/p-lambda/jukemir

Shows OpenAI Jukebox's intermediate representations transfer to MIR tasks (tagging, genre, key, emotion), beating spectrogram and prior pretrained features — the "Jukebox-era" result that seeded Sheet Sage and SynTheory.

**Evidence.** State-of-the-art or competitive on four MIR benchmarks with linear probes.

**For the studio.** Justifies using large generative-audio backbones as analysis features when the composer inserts example audio.

<small>Tags: [representation] [transcription] [evaluation] · Verification: partial (publication list; abstract not fetched) · Cluster 02</small>

### `liu2023mullama` — MULLaMA — Music Understanding LLaMA: Advancing Text-to-Music Generation with Question Answering and Captioning

*Shansong Liu, Atin Sakkeer Hussain, Chenshuo Sun, Ying Shan; Tencent ARC / NUS; ICASSP 2024 (arXiv Aug 2023).*

Links: https://arxiv.org/abs/2308.11276 ; code https://github.com/shansongliu/MU-LLaMA

MERT encoder + adapter + LLaMA for **music question answering and captioning**; introduces MusicQA (QA pairs generated from captioning datasets with MPT-7B). Open code/weights (research).

**Evidence.** SOTA on MusicQA and captioning (BLEU/METEOR/ROUGE/BERTScore) vs LTU/LLaMA-Adapter at the time.

**For the studio.** Baseline architecture for an "annotator that answers questions about a clip"; also its dataset recipe.

<small>Tags: [LLM-agent] [annotation] [evaluation] [dataset] · Verification: verified · Cluster 04</small>

### `li2024mert` — MERT — MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training

*Yizhi Li, Ruibin Yuan, Ge Zhang, et al. (20 authors incl. Yinghao Ma, Emmanouil Benetos, Jie Fu); M-A-P / Sheffield / QMUL / others; ICLR 2024.*

Links: https://arxiv.org/abs/2306.00107 ; weights https://huggingface.co/m-a-p/MERT-v1-330M ; code https://github.com/yizhilll/MERT

HuBERT-style masked prediction with two teachers—an RVQ-VAE (EnCodec) acoustic teacher and a **CQT musical (pitch/harmony) teacher**; 95M and 330M; general-purpose music representation. **CC-BY-SA 4.0** (v1) weights. Used as encoder in MU-LLaMA, MusiLingo, ACE-Step (REPA), YuE evaluation.

**Evidence.** SOTA/competitive across 14 MIR tasks (tagging, key, genre, emotion, beat, pitch, singer id…).

**For the studio.** The default open backbone for any audio-side annotation (key/chord/beat/emotion probes) and for embedding-based critique.

<small>Tags: [representation] [theory-analysis] [transcription] [toolkit] · Verification: verified · Cluster 04</small>

### `deng2024musilingo` — MusiLingo — MusiLingo: Bridging Music and Text with Pre-trained Language Models for Music Captioning and Query Response

*Zihao Deng, Yinghao Ma, Yudong Liu, et al. (Rongchen Guo, Ge Zhang, Wenhu Chen, Wenhao Huang, Emmanouil Benetos); QMUL / M-A-P; NAACL 2024 Findings (arXiv Sep 2023).*

Links: https://arxiv.org/abs/2309.08730 ; code https://github.com/zihaod/MusiLingo

MERT + single projection layer + Vicuna, instruction-tuned on MusicCaps-derived captions and MusicInstruct QA; open weights.

**Evidence.** Competitive captioning and QA vs MU-LLaMA / LTU.

**For the studio.** Lightweight open alternative for clip-level annotation.

<small>Tags: [LLM-agent] [annotation] · Verification: partial · Cluster 04</small>

## S4.1. Edit: editing paradigms

### `cypher1993wwid` — PBD — Watch What I Do: Programming by Demonstration

*Allen Cypher (ed.), with Daniel C. Halbert, David Kurlander, Henry Lieberman, David Maulsby, Brad A. Myers, Alan Turransky; MIT Press, 1993*

Links: https://acypher.com/wwid/

Collected systems in which "if a user knows how to perform a task on the computer, that should be sufficient to create a program to perform the task": the system generalises from demonstrated examples to a reusable procedure, with the user correcting over-/under-generalisation.

**Evidence.** Survey volume.

**For the studio.** Frames *example audio/MIDI as a demonstration*: "voice the chords like this passage" is PBD — the compiler should generalise a demonstrated arrangement pattern and let the composer correct the generalisation.

<small>Tags: [editing] [history] [co-creation-framework] · Verification: verified (book site fetched) · Cluster 06</small>

### `shneiderman1983direct` — DirectManipulation — Direct Manipulation: A Step Beyond Programming Languages

*Ben Shneiderman; University of Maryland; IEEE Computer 16(8), 1983*

Links: https://doi.org/10.1109/MC.1983.1654471

Defines direct manipulation: continuous representation of the object of interest; physical actions instead of complex syntax; rapid, incremental, reversible operations with immediately visible effect. Contrasted with command languages.

**Evidence.** Conceptual; foundational.

**For the studio.** The yardstick against which conversational (prompt) editing of music must be judged; the studio's notation view should remain the continuously visible object, with hum/sketch/text as *operators* on selections.

<small>Tags: [editing] [history] [HCI-study] · Verification: partial (well-known; not fetched) · Cluster 06</small>

### `masson2024directgpt` — DirectGPT — DirectGPT: A Direct Manipulation Interface to Interact with Large Language Models

*Damien Masson, Sylvain Malacria, Géry Casiez, Daniel Vogel; University of Waterloo / Inria Lille / Université de Lille; CHI 2024 (arXiv Oct 2023)*

Links: https://arxiv.org/abs/2310.03691 (CHI 2024 proceedings version via ACM DL)

A UI layer over ChatGPT that turns direct-manipulation actions into engineered prompts: continuous representation of generated objects; toolbar commands that reuse prompt syntax; outputs that can be dragged/selected to compose prompts; undo. Evaluated on editing text, code and vector images.

**Evidence.** Users were 50% faster, used 50% fewer prompts and 72% shorter prompts vs. baseline ChatGPT.

**For the studio.** Directly informs the "edit" step: select bars/voices on the score, then hum/type/draw — the selection becomes the scope of the compiled instruction, dramatically shortening prompts.

<small>Tags: [editing] [LLM-agent] [HCI-study] [controllability] · Verification: verified (fetched primary source) · Cluster 06</small>

### `igarashi1999teddy` — Teddy — Teddy: A Sketching Interface for 3D Freeform Design

*Takeo Igarashi, Satoshi Matsuoka, Hidehiko Tanaka; University of Tokyo; SIGGRAPH 1999*

Links: https://www-ui.is.s.u-tokyo.ac.jp/~takeo/teddy/teddy.htm

Freeform 2D strokes are inflated into 3D models; extrusion, cutting and smoothing are also strokes. Establishes the sketch-based-interface principle: infer a plausible complete object from an ambiguous gesture, immediately show it, and let the user refine with further gestures.

**Evidence.** Demonstrations; later user studies in the SBIM community.

**For the studio.** The interaction contract for sketch→music: coarse gesture, plausible inference, instant display, gestural refinement (rather than dialog boxes).

<small>Tags: [sketch] [editing] [history] · Verification: verified (project page fetched) · Cluster 06</small>

### `brooks2023instructpix2pix` — InstructPix2Pix — InstructPix2Pix: Learning to Follow Image Editing Instructions

*Tim Brooks, Aleksander Holynski, Alexei A. Efros; UC Berkeley; CVPR 2023 (arXiv Nov 2022)*

Links: https://arxiv.org/abs/2211.09800 ; https://www.timothybrooks.com/instruct-pix2pix

Conditional diffusion model that takes (image, edit instruction) → edited image in one forward pass. Training pairs were *synthesised* by GPT-3 (instruction + edited caption) and Stable Diffusion with prompt-to-prompt, avoiding human labelling.

**Evidence.** Qualitative generalisation to real images and arbitrary instructions; ablations.

**For the studio.** The template for *instruction-conditioned editing* of an existing artefact and for bootstrapping (score, annotation, edited-score) training triples synthetically — the missing dataset for annotation-driven symbolic editing.

<small>Tags: [editing] [text-conditioning] [controllability] · Verification: verified (fetched primary source) · Cluster 06</small>

## S4.2. Edit: symbolic editing, variation & proofreading

### `zhang2025groove` — NotThatGroove — Not that Groove: Zero-Shot Symbolic Music Editing (v2: Zero-Shot Symbolic Music Editing as a Reasoning Task for Large Language Models)

*Li Zhang (Drexel University); arXiv May 2025 (v2 May 2026)*

Links: https://arxiv.org/abs/2505.08203

Studies whether general LLMs can *edit* an existing drum groove from natural-language instructions (specific "add a cymbal on beat 1", descriptive "reduce hi-hat activity", stylistic "make it funkier") with no training, using a compact text "drumroll" notation (one line per instrument, one character per 16th). Evaluation via expert-authored unit tests rather than ground-truth edits.

**Evidence.** Unit tests agree with professional musicians (89% TPR / 94% TNR); best of 8 LLMs (gpt-4.1-mini) passes 68% of tests; reasoning models help.

**For the studio.** The clearest existing study of NL-instruction *editing* of symbolic music; shows it is feasible in a narrow domain and that test-based evaluation is the right tool for edit verification.

<small>Tags: [editing] [LLM-agent] [text-conditioning] [evaluation] [symbolic-generation] · Verification: verified (arXiv PDF/HTML fetched) · Cluster 03</small>

### `wu2023musemorphose` — MuseMorphose — MuseMorphose: Full-Song and Fine-Grained Piano Music Style Transfer with One Transformer VAE

*Shih-Lun Wu, Yi-Hsuan Yang (Academia Sinica / Taiwan AI Labs); IEEE/ACM TASLP 2023 (arXiv May 2021)*

Links: https://arxiv.org/abs/2105.04090 ; code: https://github.com/YatingMusic/MuseMorphose

Transformer VAE where each bar of an existing pop-piano piece is encoded to a latent and decoded conditioned on user-set *bar-level* attributes (rhythmic intensity, polyphony, 8 levels each), so the piece's content is preserved while its texture is rewritten bar by bar — attribute-conditioned *editing* of a whole song.

**Evidence.** Beats RNN (MusicVAE-style) baselines on fidelity, attribute-control accuracy and diversity across full songs.

**For the studio.** A model of "keep the piece, turn a knob per bar" — annotation-as-fader on an existing composition.

<small>Tags: [style-transfer] [editing] [controllability] [symbolic-generation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

## S4.3. Edit: audio editing & inpainting

### `adobe2024musicgenaicontrol` — AdobeMusicGenAIControl — Adobe Project Music GenAI Control

*Adobe Research (Nicholas J. Bryan) with UC San Diego (Zachary Novack, Julian McAuley, Taylor Berg-Kirkpatrick) and CMU (Shih-Lun Wu, Chris Donahue, Shinji Watanabe); announced Feb 28 2024 (Hot Pod Summit); research prototype.*

Links: https://blog.adobe.com/en/publish/2024/02/28/adobe-research-audio-creation-editing

Text-to-music followed by **fine-grained editing controls in the same workflow**: tempo, structure, repeating patterns, intensity, clip length, remix of a section, reference melody, seamless loops—"pixel-level control for music". Technically the productisation of Music ControlNet + DITTO (below). Never shipped publicly (as of 2026).

**Evidence.** See Music ControlNet / DITTO papers.

**For the studio.** A major vendor framing the problem exactly as "generate, then *edit with musical parameters*", validating the loop; also shows that the research (ControlNet + inference-time optimisation) is mature enough to prototype.

<small>Tags: [audio-generation] [editing] [controllability] [product] · Verification: verified · Cluster 04</small>

### `chu2025text2fx` — Text2FX — Text2FX: Harnessing CLAP Embeddings for Text-Guided Audio Effects

*Annie Chu, Patrick O'Reilly, Julia Barnett, Bryan Pardo; Northwestern University; ICASSP 2025.*

Links: https://arxiv.org/abs/2409.18847 ; code https://github.com/anniejchu/text2fx

Training-free: optimise **differentiable audio-effect parameters (EQ, reverb)** so the processed audio's CLAP embedding matches a text prompt ("warmer", "in-your-face"); parameters stay interpretable/editable; generalises to any differentiable effect and any shared text–audio space.

**Evidence.** Listener study comparing algorithmic results with human perception of the prompts.

**For the studio.** Text annotations that adjust *interpretable production parameters* rather than regenerate audio—an "annotate → tweak the mix" path that keeps human control.

<small>Tags: [editing] [text-conditioning] [controllability] [expression-performance] · Verification: verified · Cluster 04</small>

### `han2023instructme` — InstructME — InstructME: An Instruction Guided Music Edit Framework with Latent Diffusion Models

*Bing Han, Junyu Dai, Weituo Hao, et al. (Xinyan He, Dong Guo, Jitong Chen, Yuxuan Wang, Yanmin Qian); SJTU + ByteDance; IJCAI 2024 (arXiv Aug 2023). (Author list partial.)*

Links: https://arxiv.org/abs/2308.14360 ; demo https://musicedit.github.io/ — no code

Music-specific instruction editor: **add / remove / extract / replace instruments and remix**, multi-round editing; a **chord-progression matrix** is injected as a condition to preserve harmony across edits; chunk transformer for long-range consistency.

**Evidence.** Objective + subjective comparisons vs AUDIT-style baselines.

**For the studio.** Explicit harmonic conditioning inside an editor—edits stay true to the composer's chords.

<small>Tags: [audio-generation] [editing] [controllability] [symbolic-generation] · Verification: verified (abstract + demo page); authors partial · Cluster 04</small>

### `yang2025songeditor` — SongEditor — SongEditor: Adapting Zero-Shot Song Generation Language Model as a Multi-Task Editor

*Chenyu Yang, Shuai Wang, Hangting Chen, et al. (Jianwei Yu, Wei Tan, Rongzhi Gu, Yaoxun Xu, Yizhi Zhou, Haina Zhu, Haizhou Li); CUHK-Shenzhen + Tencent AI Lab; AAAI 2025 (arXiv Dec 2024).*

Links: https://arxiv.org/abs/2412.13786 ; demo https://cypress-yang.github.io/SongEditor_demo/

First **song-editing paradigm for LM-based song generation**: music tokenizer + AR LM + diffusion decoder; supports **segment-wise editing (regenerate a section with modified lyrics)** and **track-wise editing (vocals vs accompaniment)**, as well as full generation. Closed weights.

**Evidence.** Objective + subjective metrics on editing coherence and lyric accuracy.

**For the studio.** Lyric-level, section-level editing of songs with vocals—the vocal counterpart of "edit the notation and recompile".

<small>Tags: [audio-generation] [editing] [infilling] [accompaniment] · Verification: verified · Cluster 04</small>

### `lelan2024melodyflow` — MelodyFlow — High Fidelity Text-Guided Music Editing via Single-Stage Flow Matching

*Gael Le Lan, Bowen Shi, Zhaoheng Ni, et al. (12 authors incl. Wei-Ning Hsu, Vikas Chandra); Meta; arXiv Jul 2024 (rev. Oct 2024).*

Links: https://arxiv.org/abs/2407.03648 ; demo https://melodyflow.github.io ; weights (facebook/melodyflow) in AudioCraft

Diffusion-transformer trained with flow matching on stereo variable-length audio; adapts **ReNoise latent inversion** to flow matching with regularisation for **zero-shot text-guided editing** of an existing clip (change genre/instrumentation while preserving melody/structure). Fast (few steps). Weights CC-BY-NC.

**Evidence.** Outperformed ReNoise and DDIM inversion baselines on editing consistency/quality.

**For the studio.** Inversion-based editing keeps the composer's *content* fixed while changing rendering—analogous to re-orchestrating a passage.

<small>Tags: [audio-generation] [editing] [style-transfer] · Verification: verified · Cluster 04</small>

### `manor2024zeta` — ZETA-ZEUS — Zero-Shot Unsupervised and Text-Based Audio Editing Using DDPM Inversion

*Hila Manor, Tomer Michaeli; Technion; ICML 2024.*

Links: https://arxiv.org/abs/2402.10009 ; code https://github.com/HilaManor/AudioEditingCode ; https://hilamanor.github.io/AudioEditing/

Applies **edit-friendly DDPM inversion** to AudioLDM2: **ZETA** = text-based editing of *real* recordings (change instrument/genre while preserving structure); **ZEUS** = unsupervised discovery of semantic edit directions (PCA of posterior-mean directions), enabling edits like "add/remove an instrument's participation" or **melodic improvisations** without any text.

**Evidence.** Outperformed SDEdit/DDIM baselines on CLAP/LPAPS/FAD trade-offs; qualitative musical edits.

**For the studio.** Editing *the composer's own recordings* (not just model outputs) and discovering musically meaningful edit axes without labels—useful for exploration on a hummed take or a stem.

<small>Tags: [audio-generation] [editing] [style-transfer] · Verification: verified · Cluster 04</small>

### `wang2026latentft` — LatentFT — Latent Fourier Transform

*Mason L. Wang, Cheng-Zhi Anna Huang; MIT CSAIL (HAI-Res); arXiv 2604.17986, Apr 2026*

Links: https://arxiv.org/abs/2604.17986

Diffusion autoencoder whose latent sequence is transformed with a DFT into a "latent spectrum" separating musical information by *timescale*; training masks latent frequencies at random so the decoder learns to reconstruct from partial spectra. At inference, users apply custom masks to keep/blend patterns at chosen latent frequencies — an "equalizer for musical patterns" enabling variations, blends of two pieces, and isolation of characteristics.

**Evidence.** Qualitative and reconstruction experiments (details not extracted).

**For the studio.** A non-text, timescale-aware *edit* control ("keep the phrase-level shape, vary the surface") that could sit behind a scribble/annotation gesture.

<small>Tags: [editing] [representation] [controllability] [audio-generation] · Verification: verified (arXiv HTML fetched) · Cluster 01</small>

### `novack2025arc` — StableAudio25 — Stable Audio 2.5 (enterprise; inpainting; ARC post-training)

*Stability AI; announced **Sep 10–11, 2025**. Underlying acceleration method: "Fast Text-to-Audio Generation with Adversarial Post-Training" (Zachary Novack, Zach Evans, Zack Zukowski, et al.; arXiv May 2025), which also produced **Stable Audio Open Small** (open weights).*

Links: https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale ; ARC paper https://arxiv.org/abs/2505.08175

3-minute tracks in <2 s on GPU; multi-part structure (intro/development/outro); **inpainting** (upload audio, pick a region/start point, generate continuation/fill) and audio-to-audio; **ARC** = adversarial relativistic-contrastive post-training (first non-distillation acceleration for diffusion/flow), ~12 s of 44.1 kHz stereo in ~75 ms on H100 and ~7 s on a phone for the Open Small variant; "ping-pong" sampling. 2.5 trained on a "fully licensed dataset" (AudioSparx); available via API, fal, Replicate, ComfyUI, on-prem enterprise (WPP partnership). 2.5 weights closed; Open Small weights open.

**Evidence.** ARC paper: latency/quality/CLAP trade-offs vs distillation baselines.

**For the studio.** Sub-second generation makes *interactive* recompilation feasible; inpainting-as-API is the primitive for "regenerate bars 17–24".

<small>Tags: [audio-generation] [editing] [infilling] [product] [real-time] · Verification: verified (official announcement + arXiv) · Cluster 04</small>

### `zhang2024musicmagus` — MusicMagus — MusicMagus: Zero-Shot Text-to-Music Editing via Diffusion Models

*Yixiao Zhang, Yukara Ikemiya, Gus Xia, et al. (Naoki Murata, Marco Martínez-Ramírez, Wei-Hsiang Liao, Yuki Mitsufuji, Simon Dixon); QMUL + Sony AI + MBZUAI; IJCAI 2024.*

Links: https://arxiv.org/abs/2402.06178 ; code https://github.com/ldzhangyx/MusicMagus

Zero-shot editing of *generated* music by manipulating the text-embedding difference in latent space (word swap, e.g., "piano"→"guitar") with cross-attention constraints to keep unedited attributes; works with pretrained text-to-music diffusion (AudioLDM2). Edits genre, mood, instrument; limited on real (non-generated) audio.

**Evidence.** Outperformed zero-shot and some supervised baselines on style/timbre transfer (CLAP, structure preservation, human ratings).

**For the studio.** Cheap "re-orchestrate this passage" via text edits; limitation on real audio motivates inversion methods (ZETA, MelodyFlow).

<small>Tags: [audio-generation] [editing] [style-transfer] · Verification: verified · Cluster 04</small>

### `zhang2025instructmusicgen` — InstructMusicGen — Instruct-MusicGen: Unlocking Text-to-Music Editing for Music Language Models via Instruction Tuning

*Yixiao Zhang, Yukara Ikemiya, Woosung Choi, et al. (Naoki Murata, Marco A. Martínez-Ramírez, Liwei Lin, Gus Xia, Wei-Hsiang Liao, Yuki Mitsufuji, Simon Dixon); QMUL + Sony AI; ISMIR 2025 (arXiv May 2024).*

Links: https://arxiv.org/abs/2405.18386 ; code https://github.com/ldzhangyx/instruct-MusicGen

Adds an audio-fusion and a text-fusion module to frozen MusicGen (+8% params, 5k steps) so it follows **"add / remove / separate a stem"** instructions over an input clip; open code and weights (inherits NC license).

**Evidence.** Matches task-specific models on Slakh/MoisesDB-based editing metrics with tiny training cost.

**For the studio.** Cheap way to make an open audio LM stem-editable via language—useful for "add strings under the chorus" style annotations.

<small>Tags: [audio-generation] [editing] [accompaniment] [text-conditioning] · Verification: verified · Cluster 04</small>

### `wang2023audit` — AUDIT — AUDIT: Audio Editing by Following Instructions with Latent Diffusion Models

*Yuancheng Wang, Zeqian Ju, Xu Tan, et al. (Lei He, Zhizheng Wu, Jiang Bian, Sheng Zhao); CUHK-Shenzhen + Microsoft Research Asia; NeurIPS 2023 (arXiv Apr 2023).*

Links: https://arxiv.org/abs/2304.00830 ; demo https://audit-demo.github.io/

First **instruction-following audio editor**: trained on (instruction, input audio, output audio) triplets so users say "add a dog barking" / "replace the piano with guitar"; tasks: add, drop, replace, **inpainting**, super-resolution. Latent diffusion; general audio rather than music-specific.

**Evidence.** SOTA objective and subjective results on constructed editing benchmarks.

**For the studio.** Establishes the "natural-language edit instruction over an existing clip" pattern later specialised to music (InstructME, Instruct-MusicGen).

<small>Tags: [audio-generation] [editing] [infilling] [text-conditioning] · Verification: verified · Cluster 04</small>

## S4.4. Edit: AI→human feedback & explanation

### `bryankinns2021xai` — XAIArts — Exploring XAI for the Arts: Explaining Latent Space in Generative Music

*Nick Bryan-Kinns, Berker Banar, Corey Ford, Courtney N. Reed, Yixiao Zhang, Simon Colton, Jack Armitage; QMUL; XAI4Debugging workshop @ NeurIPS 2021 (arXiv 2023); follow-ups: Bryan-Kinns et al., "Exploring Variational Auto-Encoder Architectures, Configurations, and Datasets for Generative Music Explainable AI," Machine Intelligence Research 2024; Bryan-Kinns, "Reflections on Explainable AI for the Arts (XAIxArts)," Interactions 2024*

Links: https://arxiv.org/abs/2308.05496

Regularises the first four latent dimensions of MeasureVAE to correspond to rhythmic complexity, note range, note density and average interval jump, and builds a real-time interface + visualisations so users can see and manipulate what each dimension does.

**Evidence.** Technical demonstration; later user studies in the XAIxArts line (2023–2024 workshops at C&C) evaluate explanations with musicians.

**For the studio.** Shows how to make generative controls *legible* — semantic knobs plus visual explanations — a requirement for annotations to have predictable effects.

<small>Tags: [controllability] [evaluation] [symbolic-generation] [co-creation-framework] · Verification: verified (fetched arXiv PDF) · Cluster 05</small>

### `ramoneda2024refinpaint` — RefinPaint — Music Proofreading with RefinPaint: Where and How to Modify Compositions Given Context

*Pedro Ramoneda, Martín Rocamora, Taketo Akama; Universitat Pompeu Fabra, Sony CSL Tokyo; ISMIR 2024*

Links: https://arxiv.org/abs/2407.09099 ; https://github.com/ta603/RefinPaint ; https://refinpaint.github.io/

Two-model loop for symbolic music: a *feedback/critic* model identifies which notes are weakest given context ("where to modify"), and an inpainting model resamples them ("how"); iterated as "proofreading" for both machine- and human-composed drafts. Users pick bars and how much content to keep.

**Evidence.** Listening study with 15 annotators across 50/30/10% fragment sizes — RefinPaint preferred over baseline at all sizes; 4 amateur composers all reported improved drafts and time saved.

**For the studio.** Literally an AI *annotator*: it marks the score where it thinks changes are needed — the machine half of the annotate→edit loop and a model for AI→human communication on notation.

<small>Tags: [infilling] [editing] [annotation] [notation] [symbolic-generation] [evaluation] · Verification: verified (fetched arXiv HTML) · Cluster 05</small>

## S4.5. Edit: history, versioning & alternatives

### `foscarin2019diff` — ScoreDiff — A Diff Procedure for Music Score Files

*Francesco Foscarin, Florent Jacquemard, Raphaël Fournier-S'niehotta; CNAM / Inria Paris; 6th International Conference on Digital Libraries for Musicology (DLfM), 2019 (DOI 10.1145/3358664.3358671)*

Links: https://doi.org/10.1145/3358664.3358671

Compares two scores at the *graphical notation* level via an intermediate tree representation per bar/voice, combining sequence edit distance (bars) with tree edit distance (beaming/tuplet hierarchies); a Verovio-based visualiser shows the two scores side by side with differences highlighted. Motivated by collaborative editing and version control; validated on OMR datasets.

**Evidence.** Evaluation on OMR output vs ground truth; tool released.

**For the studio.** The only fetched research artefact for *musical diff* — necessary for showing what the compiler changed between versions and for reviewing AI edits like a code review.

<small>Tags: [notation] [editing] [toolkit] [evaluation] · Verification: verified (metadata/abstract via Semantic Scholar API) · Cluster 06</small>

### `terry2002sideviews` — Alternatives — Alternatives, history and branching in creative tools (Side Views; Juxtapose; Subjunctive Interfaces)

*Michael Terry & Elizabeth Mynatt, "Side Views: Persistent, On-Demand Previews for Open-Ended Tasks," UIST 2002; Björn Hartmann, Loren Yu, Abel Allison, Yeonsoo Yang, Scott Klemmer, "Design as Exploration: Creating Interface Alternatives through Parallel Authoring and Runtime Tuning" (Juxtapose), UIST 2008; Aran Lunzer & Kasper Hornbæk, "Subjunctive Interfaces: Extending Applications to Support Parallel Setup, Viewing and Control of Alternative Scenarios," ACM TOCHI 14(4), 2008*

Links: https://doi.org/10.1145/571985.571996 ; https://doi.org/10.1145/1449715.1449724 ; https://doi.org/10.1145/1314683.1314685

The HCI lineage for working with *multiple alternatives in parallel*: previews of possible outcomes before committing (Side Views), parallel code/design variants with linked editing and runtime tuning (Juxtapose), and side-by-side alternative scenarios (Subjunctive Interfaces). Terry & Mynatt's "Recognizing Creative Needs in User Interface Design" (C&C 2002) frames near-term experimentation, variation and evaluation as core creative needs.

**Evidence.** Lab studies in each paper showing users explore more alternatives and compare more readily; conceptual foundation for later "version tree" tools in creative software.

**For the studio.** Anchors the version-tree / branching requirement of the compile loop (each annotate→compile produces alternatives that must be compared, kept, or merged) in established HCI results; complements Cococo's "multiple alternatives" and Calliope's batch+rank.

<small>Tags: [creativity-support] [history] [co-creation-framework] · Verification: partial (canonical works; DOIs from recall, not fetched this session) · Cluster 05</small>

### `suh2024luminate` — Luminate — Luminate: Structured Generation and Exploration of Design Space with LLMs for Human-AI Co-Creation (and Parallel Paths)

*Sangho Suh, Meng Chen, Bryan Min, Toby Jia-Jun Li, Haijun Xia; UC San Diego / Notre Dame; CHI 2024 (DOI 10.1145/3613904.3642400). Precedent: Michael Terry, Elizabeth Mynatt, Kumiyo Nakakoji, Yasuhiro Yamamoto, "Variation in Element and Action: Supporting Simultaneous Development of Alternative Solutions" (Parallel Paths), CHI 2004.*

Links: https://arxiv.org/abs/2310.12953

Instead of one chat answer, the LLM first generates *dimensions* of the design space, then a structured grid/space of many responses that users browse, filter, evaluate and combine. Parallel Paths (2004) let image editors develop several alternatives side by side from a shared history.

**Evidence.** Luminate: N=14 professional writers found it feasible and useful for exploration.

**For the studio.** Model for *variation trees* over compiled outputs: several arrangements of the same annotated passage explored in parallel, with dimensions (density, register, style) as axes — a music analogue is not yet published.

<small>Tags: [creativity-support] [LLM-agent] [HCI-study] [co-creation-framework] · Verification: verified (Luminate fetched); Parallel Paths partial · Cluster 06</small>

### `grossman2010chronicle` — Chronicle — Chronicle: Capture, Exploration, and Playback of Document Workflow Histories

*Tovi Grossman, Justin Matejka, George Fitzmaurice; Autodesk Research; UIST 2010*

Links: https://www.research.autodesk.com/publications/chronicle-capture-exploration-and-playback-of-document-workflow-histories/

Records the full video and event history of a graphical document; users click any region of the final document to see the workflow, tools and settings that produced it, and play it back. Later shipped as Autodesk Screencast.

**Evidence.** User study found it useful and easy to use.

**For the studio.** Provenance UI for creative artefacts: clicking a passage in the compiled score should reveal *which annotations and which compile* produced it — essential for trust in AI-authored material.

<small>Tags: [editing] [HCI-study] [creativity-support] · Verification: verified (project page fetched; first author from recall) · Cluster 06</small>

### `flat2026history` — FlatHistory — Flat.io version history (and Splice Studio / Blend as DAW-project precedents)

*Tutteo Ltd (Flat.io), ongoing; Splice Studio (Splice, DAW project backup/versioning, 2013 – discontinued c. 2021); Blend.io (DAW project sharing/remixing, 2013 – defunct)*

Links: https://help.flat.io/en/music-notation-software/history/

Flat auto-syncs every edit; major versions are created every ≤50 modifications; free users can restore the 10 most recent major versions, paid users can scrub *every single change* with a video-like slider, see change locations on a score scrollbar, view per-contributor colour coding, restore, or export any state to MusicXML/MIDI. Splice Studio offered git-like commit history and collaboration for Ableton/Logic/FL project files; Blend offered project sharing and forking.

**Evidence.** Product documentation.

**For the studio.** Flat shows a linear, fine-grained, attributable history for notation is deliverable; the demise of Splice Studio/Blend signals that *file-level* DAW versioning had limited pull — semantic, musically-aware diffs and branches are the unexplored space.

<small>Tags: [product] [editing] [notation] · Verification: Flat verified (fetched); Splice Studio and Blend unverified (recall) · Cluster 06</small>

## S5.1. Play: score following & accompaniment

### `dannenberg2014hcmp` — HCMP — Human-Computer Music Performance (HCMP) programme

*Roger B. Dannenberg with Nicolas E. Gold, Dawen Liang, Guangyu Xia (and others); CMU. "Human-Computer Music Performance: From Synchronized Accompaniment to Musical Partner" (SMC 2013); "Methods and Prospects for Human-Computer Music Performance of Popular Music" and "Active Scores: Representation and Synchronization in HCMP of Popular Music" (Computer Music Journal 38(2), 2014); "HCMP: A Brief History and Future Prospects" (JASA 2014).*

Links: https://www.cs.cmu.edu/~rbd/bib.html ; https://www.cs.cmu.edu/~music/cmp/

Framework for computers as *performing partners* in popular music (bands, not soloist + accompaniment): beat/section-level synchronisation, "active scores" (machine-readable, structure-aware scores that can be re-sequenced live, with repeats/cues), and roles for human cueing. Later offshoots: Xia's improvised duet interaction (NIME 2017), Accomplice (current keyboard accompaniment project), Arco (ICMC 2025), O2 networking (CMJ 2022).

**Evidence.** System papers and performances; no large N studies.

**For the studio.** "Active scores" are an early structured-score representation designed for both humans and machines to edit and follow — a direct ancestor of an annotated, compilable score.

<small>Tags: [history] [accompaniment] [real-time] [structure] [notation] [representation] · Verification: verified (author bibliography) · Cluster 02</small>

## S5.2. Play: improvisation partners

### `blanchard2025jambot` — JamBot — The jam_bot, a Real-Time System for Collaborative Free Improvisation with Music Language Models

*Lancelot Blanchard, Perry Naseck, Stephen Brade, Kimaya Lecamwasam, Jordan Rudess, Cheng-Zhi Anna Huang, Joseph A. Paradiso; MIT Media Lab (Responsive Environments) + HAI-Res; ISMIR 2025 (Daejeon); DOI 10.5281/zenodo.17706584*

Links: https://zenodo.org/records/17706584 ; https://ismir2025program.ismir.net/poster_321.html ; project: https://arts.mit.edu/jordan-rudess-mit/

A stage system that improvises with Dream Theater keyboardist Jordan Rudess (CAST Visiting Artist). Built on Music Transformer, fine-tuned on Rudess's own recorded basslines, chords and melodies; the model is prompted into distinct *roles* (lead, accompaniment, call-and-response) via modified context/conditioning; a low-latency multi-threaded scheduler "listens, and prompts and schedules model generations seamlessly." A preview screen shows upcoming decisions; restart and kill-switch preserve performer agency; a kinetic petal sculpture (Naseck) externalizes the AI's state. Premiered 21 Sept 2024 (work-in-progress) and later in a sold-out concert.

**Evidence.** Performance-based evaluation and practitioner reflection (details not fetched).

**For the studio.** Demonstrates *personalized* symbolic models (fine-tuned on one artist's material) with explicit role assignment — a model for the studio letting a composer "compile" in their own voice — and again the pattern of previewing AI intent.

<small>Tags: [real-time] [accompaniment] [mixed-initiative] [expression-performance] [symbolic-generation] · Verification: verified (Zenodo + ISMIR program + Arts at MIT pages fetched) · Clusters 01, 05</small>

### `shepardson2022notochord` — Notochord — Notochord: A Flexible Probabilistic Model for Real-Time MIDI Performance

*Victor Shepardson, Thor Magnusson (Intelligent Instruments Lab, Iceland University of the Arts); AIMC 2022 (arXiv 2024)*

Links: https://arxiv.org/abs/2403.12000 ; https://github.com/Intelligent-Instruments-Lab/notochord (MIT)

Autoregressive model over MIDI *sub-events* (instrument, pitch, time, velocity) trained on Lakh MIDI with <10 ms latency; because each sub-event is sampled separately, a performer can fix or constrain any of them, enabling harmonisers, improvisers, steerable generation and likelihood-based interfaces (apps: Homunculus, Harmonizer, Improviser).

**Evidence.** Open-source system paper with live performances; no controlled user study.

**For the studio.** The clearest example of *sub-event-level* human intervention in a generative model — the real-time analogue of editing a note in the score and letting the model re-condition.

<small>Tags: [real-time] [symbolic-generation] [controllability] [accompaniment] [toolkit] · Verification: verified (fetched arXiv abstract + GitHub README) · Cluster 05</small>

## S5.3. Play: RL-tuned & live neural models

### `scarlatos2025realjam` — ReaLJam — ReaLJam: Real-Time Human-AI Music Jamming with Reinforcement Learning-Tuned Transformers

*Alexander Scarlatos, Yusong Wu, Ian Simon, Adam Roberts, Tim Cooijmans, Natasha Jaques, Cassie Tarakajian, Cheng-Zhi Anna Huang; UMass Amherst / Mila / Google DeepMind / UW; CHI 2025 Extended Abstracts (arXiv 2502.21267)*

Links: https://arxiv.org/abs/2502.21267 ; demo https://storage.googleapis.com/genjam/index.html

Web interface + client-server protocol wrapping ReaLchords for live jamming: user plays melody on a MIDI keyboard or computer keys; agent outputs chords. Key idea is **anticipation**: the agent continually predicts how the performance will unfold and shows upcoming chords in a "waterfall" descending toward the piano — committed chords opaque, revisable predictions semi-transparent. Round-trip latency typically <100 ms at 150 BPM. Three model variants (MLE, RL-S, RL-M) and many user-adjustable settings.

**Evidence.** N=6 experienced musicians, 60-min sessions (baseline + 8 modified settings + free choice). Enjoyment 4.3/5, adaptation 2.7/5; RL-trained models beat the pretrained one on all measures; users valued "surprise" that still matched expectation, wanted genre control and structure awareness; preferences for settings varied strongly by individual and did not always match objective ratings.

**For the studio.** Concrete UI for *showing an agent's plan before it commits* — the visual language the studio needs whenever the AI proposes material in real time; plus evidence that customization per musician is essential.

<small>Tags: [real-time] [accompaniment] [HCI-study] [mixed-initiative] [controllability] · Verification: verified (arXiv PDF fetched) · Clusters 01, 05</small>

### `donahue2019pianogenie` — PianoGenie — Piano Genie

*Chris Donahue, Ian Simon, Sander Dieleman; Google Brain (Magenta) / UCSD / DeepMind; ACM IUI 2019 (arXiv 1810.05246)*

Links: https://arxiv.org/abs/1810.05246 ; code: https://github.com/tensorflow/magenta/tree/master/magenta/models/piano_genie ; demo: https://chrisdonahue.com/piano-genie

An "intelligent controller": eight buttons are decoded in real time into plausible 88-key piano music by an RNN autoencoder with a discrete bottleneck; musically meaningful constraints on the encoder make button contour map to pitch contour. Input: button presses with timing; output: piano notes. The human controls rhythm, phrasing, and rough melodic contour; the model fills in exact pitches.

**Evidence.** Qualitative/user demo; no controlled N reported in abstract.

**For the studio.** A gesture-level "sketch → notes" mapping: the user supplies contour and rhythm (very close to humming/scribbling a line), the model compiles pitches. A template for low-fidelity human input steering high-fidelity output.

<small>Tags: [real-time] [expression-performance] [symbolic-generation] [creativity-support] [history] · Verification: verified (arXiv abstract fetched) · Clusters 01, 02, 05</small>

### `scurto2021coexplorer` — CoExplorer — Designing Deep Reinforcement Learning for Human Parameter Exploration

*Hugo Scurto, Bavo Van Kerrebroeck, Baptiste Caramiaux, Frédéric Bevilacqua; IRCAM/STMS, Sorbonne Université; ACM Transactions on Computer-Human Interaction 28(1), 2021 (arXiv 2019)*

Links: https://arxiv.org/abs/1907.00824 ; https://doi.org/10.1145/3414472

Co-Explorer: a deep-RL agent explores a synthesiser's high-dimensional parameter space and adapts to the sound designer's *like/dislike feedback*, alternating between autonomous exploration and user-directed moves — a critique/feedback-loop paradigm rather than direct manipulation.

**Evidence.** User-centred design with observational studies, agent-behaviour tests and a workshop evaluation with professional sound designers; positive reception; diverse exploration behaviours; design guidelines for "co-exploration."

**For the studio.** A concrete design for *feedback-as-steering* (thumbs up/down on compiled results shaping the next compile) with musicians in the loop.

<small>Tags: [HCI-study] [controllability] [mixed-initiative] [real-time] · Verification: partial (arXiv abstract fetched; N and TOCHI DOI from recall) · Cluster 05</small>

### `wu2026streaming` — StreamAccomp — Streaming Generation for Music Accompaniment

*Yusong Wu, Mason Wang, Heidi Lei, Stephen Brade, Lancelot Blanchard, Shih-Lun Wu, Aaron Courville, Cheng-Zhi Anna Huang; Mila / MIT; ISMIR 2026 (arXiv 2510.22105, Oct 2025)*

Links: https://arxiv.org/abs/2510.22105 ; https://github.com/lukewys/stream-music-gen ; https://lukewys.github.io/stream-music-gen

Real-time *audio-to-audio* accompaniment: a 16-layer decoder-only Transformer over DAC RVQ tokens (50 Hz, 4 codebooks) listens to an incoming stem and emits an accompanying stem, across 18 GM instrument families (Slakh2100). Formalizes two design knobs: **future visibility** t_f (latency offset, −4 to +4 s) and **output chunk size** k, trained across the grid with a delay pattern.

**Evidence.** COCOLA coherence, Beat-F1 and FAD on 1,024 Slakh clips plus blind pairwise listening; larger t_f improves coherence but demands faster inference; "naive maximum-likelihood streaming training is insufficient for coherent accompaniment where future context is not available."

**For the studio.** Quantifies the latency/coherence trade-off the studio will face in any live audio layer, and is open code.

<small>Tags: [audio-generation] [real-time] [accompaniment] [evaluation] · Verification: verified (arXiv HTML fetched) · Cluster 01</small>

### `wu2026gapt` — GAPT — Generative Adversarial Post-Training Mitigates Reward Hacking in Live Human-AI Music Interaction

*Yusong Wu, Stephen Brade, Aleksandra Teng Ma, Tia-Jane Fowler, Enning Yang, Berker Banar, Aaron Courville, Natasha Jaques, Cheng-Zhi Anna Huang; Mila / MIT / Georgia Tech / UW / McGill; ICLR 2026 (arXiv 2511.17879)*

Links: https://arxiv.org/abs/2511.17879 ; code: https://github.com/lukewys/realchords-pytorch ; audio: https://realchords-GAPT.github.io

Addresses "reward hacking" in RL post-training of ReaLchords-style melody→chord agents, where coherence rewards drive collapse to "repetitive, trivial, and low-coverage chord choices." Adds a co-evolving discriminator that separates policy trajectories from real data; the policy maximizes discriminator output alongside coherence rewards, with a two-phase (warm-up then confidence-gated) update schedule.

**Evidence.** Simulation with fixed melodies and learned melody agents (Pareto frontier of harmony ~85% note-in-chord vs Vendi-score diversity); in-person study with **12 expert musicians**, three anonymized systems × three tasks; GAPT rated highest on adaptation quality, adaptation speed and perceived control/agency, significantly beating ReaLchords on speed and agency (p<0.05).

**For the studio.** Shows *diversity* must be an explicit training target for a co-creative agent or it becomes boring; also the first open PyTorch stack for the whole ReaLchords family.

<small>Tags: [real-time] [accompaniment] [HCI-study] [evaluation] [symbolic-generation] · Verification: verified (arXiv HTML fetched) · Cluster 01</small>

### `wu2024realchords` — ReaLchords — Adaptive Accompaniment with ReaLchords

*Yusong Wu, Tim Cooijmans, Kyle Kastner, Adam Roberts, Ian Simon, Alexander Scarlatos, Chris Donahue, Cassie Tarakajian, Shayegan Omidshafiei, Aaron Courville, Pablo Samuel Castro, Natasha Jaques, Cheng-Zhi Anna Huang; Google DeepMind / Mila; ICML 2024, PMLR 235:53328–53345 (arXiv 2506.14723)*

Links: https://proceedings.mlr.press/v235/wu24c.html ; https://arxiv.org/abs/2506.14723 ; audio: https://storage.googleapis.com/realchords/index.html ; PyTorch reimplementation: https://github.com/lukewys/realchords-pytorch

An *online* (causal, no future access) chord-accompaniment model for a live melody. Frame-based at 16th-note resolution (≤256 frames), 5,041-chord vocabulary, 8-layer decoder (512-d). Pretrained by MLE on ~38k Hooktheory melody–chord pairs, then RL-finetuned with (a) self-supervised reward models (contrastive InfoNCE and discriminative, multi-scale) scoring harmonic *and temporal* coherence and (b) a KL term distilling from an offline encoder-decoder teacher that *can* see the future melody — "forcing anticipation."

**Evidence.** Note-in-chord ratio 54.3% (ReaLchords-M) vs 37.0% for online MLE; recovers from a tritone transposition at beat 17 within 2–3 beats (MLE never does); listening test with 10 musicians, 192 pairwise comparisons: significantly preferred over MLE and distillation-only baselines; self-supervised rewards correlated with human judgments.

**For the studio.** The state-of-the-art recipe for a responsive harmonic partner that follows the *human's* line rather than the reverse; symbolic (chord-symbol) output plugs straight into a lead-sheet workflow.

<small>Tags: [real-time] [accompaniment] [symbolic-generation] [mixed-initiative] [evaluation] · Verification: verified (PMLR page + arXiv HTML fetched) · Clusters 01, 02</small>

### `novack2026lmdm` — LMDM — Live Music Diffusion Models: Efficient Fine-Tuning and Post-Training of Interactive Diffusion Music Generators

*Zachary Novack*, Stephen Brade*, Haven Kim, Hugo Flores García, Nithya Shikarpur, Chinmay Talegaonkar, Suwan Kim, Valerie K. Chen, Julian McAuley, Taylor Berg-Kirkpatrick, Cheng-Zhi Anna Huang; UCSD / MIT / Adobe; arXiv 2605.22717, May 2026*

Links: https://arxiv.org/abs/2605.22717 ; audio: https://stephenbrade.github.io/lmdm-public/

Repurposes an open audio diffusion model (Stable Audio Open Small, 340M) into a streaming, block-wise generator with KV-caching (encoder-decoder or block-causal variants) and an "ARC-Forcing" adversarial post-training that curbs error accumulation without RL or reward models. Modes: text-conditioned streaming, **sketch-based synthesis** (time-aligned top-k CQT loudness controls extracted from a musician's live audio), and stem-conditioned jamming with adjustable future visibility (−2..+2 s). Deployed via ONNX + C++/JUCE as a "generative delay" effect on a consumer gaming laptop.

**Evidence.** ~30 ms latency after post-training (8 steps), TTFF 0.03 s; FD/KL/CLAP competitive with Stable Audio Open and MusicGen-Large at far lower latency; N=3 musicians (sax, guitar, cello) described it as a "musical partner rather than simple effect"; limits: EDM bias from MTG-Jamendo, quality below frontier models.

**For the studio.** Open recipe for a local, low-latency audio partner that accepts *sketch-like control signals*; the "generative delay" is a fresh instrument metaphor for the studio's audio layer.

<small>Tags: [audio-generation] [real-time] [sketch] [controllability] [DAW-plugin] [text-conditioning] · Verification: verified (arXiv HTML fetched) · Cluster 01</small>

## S5.4. Play: design spaces, practice & games

### `wang2025rise` — RISE — RISE: Adaptive Music Playback for Realtime Intensity Synchronization with Exercise

*Alexander Wang (Michigan/CMU), Chris Donahue (CMU), Dhruv Jain (Michigan). ISMIR 2025 (Daejeon).*

Links: https://gclef-cmu.org/static/pdfs/2025rise.pdf

Estimates intense song segments (structure analysis + drum-stem loudness), finds cutpoints via recurrence matrices, and a state machine loops/skips segments in real time to align music energy with workout intervals.

**Evidence.** 6 raters on 514 clips: transition naturalness 4.3/5 vs 4.5/5 unmodified (n.s.); N=12 users, 11/12 preferred adaptive.

**For the studio.** Structure-aware *rearrangement* of existing audio by cut-points — a form of non-destructive audio editing on musical structure.

<small>Tags: [structure] [editing] [real-time] [HCI-study] · Verification: verified (PDF) · Cluster 02</small>

### `wang2024musicaware` — MusicAwareVA — Towards Music-Aware Virtual Assistants

*Alexander Wang, David Lindlbauer, Chris Donahue; CMU HCII/CSD. ACM UIST 2024.*

Links: https://doi.org/10.1145/3654777.3676416 ; https://ayw0.github.io/publications/2024-MVA/

Spoken notifications are re-sung in harmony with the currently playing music (lyrics replaced by the alert), instead of muting playback.

**Evidence.** User study: musical assistant fit music better, less intrusive, more delightful than standard (N not captured).

**For the studio.** Peripheral; shows the HCII–G-CLef pairing and a "generate-to-fit-existing-music" constraint problem.

<small>Tags: [HCI-study] [audio-generation] [accompaniment] · Verification: verified (project page) · Cluster 02</small>

### `egozy2005harmonix` — Harmonix — Guitar Hero / Rock Band (Harmonix Music Systems) as music-making interfaces

*Eran Egozy and Alex Rigopulos (co-founders, MIT Media Lab alumni, Machover's group); Harmonix, founded 1995; Guitar Hero 2005, Rock Band 2007*

Links: https://mta.mit.edu/person/eran-egozy ; https://www.harmonixmusic.com/

Rhythm games that let non-musicians *perform* music via simplified controllers and a scrolling "note highway," with tight audio-visual feedback and scoring. Harmonix grew out of Media Lab work on making musical expression accessible (Egozy and Rigopulos both did master's research under Machover). >35 million units sold; Egozy in Time 100.

**Evidence.** Commercial history (MIT bio). Egozy's specific public statements about games as music-making interfaces were not retrievable this session (unverified).

**For the studio.** The note-highway/anticipation visual and the "make anyone feel like a musician" goal are direct ancestors of ReaLJam's waterfall and Piano Genie — useful for the studio's performance/jam UI.

<small>Tags: [game] [history] [creativity-support] [real-time] · Verification: partial (bio verified; quotes unverified) · Cluster 01</small>

### `egozy2016harmonix` — Egozy — Approaches to Musical Expression in Harmonix Video Games; live score following; AI-augmented instruments

*Eran Egozy; IMS NUS Lecture Notes 2016 (DOI 10.1142/9789813140103_0002); Matthew Caren & Eran Egozy, JAES 2025 ("Real-Time In-Browser Time Warping for Live Score Following"); Lancelot Blanchard, Perry Naseck, Egozy, Joseph Paradiso, 2024 ("Developing Symbiotic Virtuosity: AI-Augmented Musical Instruments…")*

Links: https://doi.org/10.1142/9789813140103_0002 ; https://doi.org/10.17743/jaes.2022.0244

Egozy's account of how Guitar Hero/Rock Band/Dance Central/Fuser designed for *musical expression* within game constraints (scoring, freestyle sections, note-highway abstraction); recent MIT work on browser-based real-time score following (online time warping) and on AI-augmented instruments in live performance (with the Media Lab).

**Evidence.** Descriptive/design papers; the JAES paper reports latency/accuracy of in-browser alignment (numbers not fetched).

**For the studio.** Direct lineage from game interfaces to expressive control; in-browser score following is a component for aligning the composer's live playing/singing to notation as an annotation.

<small>Tags: [game] [HCI-study] [real-time] [education] · Verification: verified (Crossref records) · Cluster 07</small>

### `harmonix2020fuser` — Harmonix Fuser / DropMix — mashup games as arrangement interfaces

*Harmonix (Boston; acquired by Epic Games 2021); DropMix (with Hasbro, 2017: physical NFC cards + app mixing stems in-key/in-tempo); Fuser (2020: real-time 4-slot stem mashups, key/tempo matching, live-DJ campaign; servers shut down Dec 2022)*

Links: https://en.wikipedia.org/wiki/Fuser_(video_game) ; https://en.wikipedia.org/wiki/DropMix

Consumer products that made *arrangement by stem selection* a game mechanic: pick vocals/bass/drums/lead from different licensed songs, engine time-stretches/pitch-shifts to a common key and tempo, with scoring for musical timing (drops on downbeats).

**Evidence.** Commercial; critically praised for accessibility of musical mixing.

**For the studio.** Demonstrates casual users can make coherent arrangements from constrained stems when the system handles key/tempo — a UX lesson for the "compile" step.

<small>Tags: [game] [product] [accompaniment] · Verification: partial (recalled) · Cluster 07</small>

### `miller2009schizophonic` — Kiri Miller — Guitar Hero/Rock Band as musical performance and learning

*Kiri Miller; Brown University; JSAM 2009 ("Schizophonic Performance: Guitar Hero, Rock Band, and Virtual Virtuosity"); book *Playing Along: Digital Games, YouTube, and Virtual Performance* (Oxford 2012, ch. "How Musical Is Guitar Hero?")*

Links: https://doi.org/10.1017/s1752196309990666 ; https://doi.org/10.1093/acprof:oso/9780199753451.003.0003

Ethnographic study (interviews, surveys of players) arguing these games are a form of musical performance and informal music learning (rhythm, structure, listening), while analysing their limits; later pedagogical literature (e.g., "Musical Representation in Guitar Hero and Rock Band," 2010) and Harmonix's *Rock Band* in-classroom pilots build on this.

**Evidence.** Qualitative; the canonical reference for game-based music learning.

**For the studio.** Grounds the claim that game-like interfaces can carry genuine musical agency — relevant if the studio uses playful, game-derived interaction for annotation (e.g., tapping rhythms, "note highway" input).

<small>Tags: [game] [education] [HCI-study] · Verification: verified (Crossref) · Cluster 07</small>

### `brade2026agentsinconcert` — AgentsInConcert — Agents in Concert: A Case-Study of Bringing AI to the Stage in Practice

*Stephen Brade, Teng Ma, Lancelot Blanchard, Kimaya Lecamwasam, Carlos Mariano Salcedo, Suwan Kim, Perry Naseck, Andrew Li, Matthew R. Michalek, Sebastian Franjou, Cheng-Zhi Anna Huang; MIT (HAI-Res + Media Lab); ACM IUI 2026, DOI 10.1145/3742413.3789104*

Links: https://doi.org/10.1145/3742413.3789104

Case study of deploying multiple AI music agents in a real concert (the jam_bot / Jordan Rudess + MIT Chamber Chorus program at the Media Lab), documenting the practical engineering, rehearsal and performer-agency lessons of bringing generative agents on stage.

**Evidence.** Reflective case study (details behind ACM paywall; not fetched).

**For the studio.** Field lessons on robustness, previews/kill-switches and rehearsal workflows for any "performance mode" of the studio.

<small>Tags: [real-time] [HCI-study] [mixed-initiative] · Verification: partial (title/authors/venue from dblp + ACM DOI; content inferred from related jam_bot coverage) · Cluster 01</small>

## E1. Evidence: controlled studies of co-creative systems

### `wang2026multiverse` — MultiVerse — MultiVerse: A Creator-Centered Approach to Steering Context-Adaptive Lyrics

*Alexander Wang, Chris Donahue, David Lindlbauer; CMU HCII/CSD. ACM UIST 2026 (arXiv Aug 2026).*

Links: https://arxiv.org/abs/2608.19350 ; https://doi.org/10.1145/3830398.3830530 ; https://ayw0.github.io/multiverse/

"C3" creator-centred adaptive-media authoring: songwriters explicitly author *controls* (intent, lyric structure such as rhyme/rhythm placement, locked phrases, audience context) that govern how an LLM adapts lyrics per listener; rule-based validators enforce the controls.

**Evidence.** N=10 songwriters, MultiVerse vs a prompting workflow; creators preferred explicit constraint authoring, acknowledging flexibility/iteration-speed trade-offs; interviews on authorship and new compositional strategies.

**For the studio.** Same philosophy as the studio — the *creator authors constraints*, the model fills — applied to lyrics; the validator-enforced-controls pattern is a good compile-time check design.

<small>Tags: [co-creation-framework] [controllability] [HCI-study] [text-conditioning] · Verification: verified (arXiv abstract; project page) · Cluster 02</small>

### `frid2020example` — MusicByExample — Music Creation by Example

*Emma Frid, Celso Gomes, Zeyu Jin; KTH, Adobe Research; CHI 2020*

Links: https://doi.org/10.1145/3313831.3376514

UI paradigm for video creators who need soundtrack music: the user supplies an *example song*; an AI engine generates similar music which the user can interactively regenerate and mix (stem-level control), rather than describing music in words.

**Evidence.** Multi-phase studies with 104 video creators in total; example-based input was found more natural than tag/text search and revealed design insights on human–AI collaboration (control, trust in regeneration).

**For the studio.** Validates "insert example audio as an annotation" as a primary steering modality for people who think in references rather than theory terms.

<small>Tags: [HCI-study] [multimodal-input] [audio-generation] [controllability] · Verification: verified (Semantic Scholar abstract + Crossref metadata; full text not fetched) · Cluster 05</small>

### `oros2026cmu` — CMU-Udio-2026 — "Generative AI and Musical Creativity" (CMU news, Jan 30 2026: "As AI-Generated Music Advances, Humans Still Lead in Creativity")

*Jose Oros (PhD student, Information Systems, Heinz College), Rahul Telang (Trustees Professor of IS, Heinz), Richard Randall (Assoc. Prof. of Music Theory, School of Music). Poster #18, Conference on Digital Experimentation (CODE\@MIT), Nov 14–15 2025. CMU news story by Stacey Federoff, Jan 30 2026 (Heinz repost Feb 2026; phys.org Feb 2026). **No paper, preprint or SSRN working paper is public as of Sept 2026**; Oros was to defend in May 2026. *Not* a Donahue/G-CLef study.*

Links: https://www.cmu.edu/news/stories/archives/2026/january/as-ai-generated-music-advances-humans-still-lead-in-creativity-cmu-research-finds ; https://www.heinz.cmu.edu/media/2026/February/as-ai-generated-music-advances-humans-still-lead-in-creativity-cmu-research-finds ; https://ide.mit.edu/events/2025-conference-on-digital-experimentation-mit-codemit/

Randomised experiment: **140 musically trained participants** each composed a **15-second melody on a small piano keyboard**; a randomly selected treatment group could use **Udio** (text-prompt music generator) to generate tunes "for inspiration", the control group composed unaided. All melodies were then rated by a **separate group of listeners on creativity, enjoyment and musicality**.

**Evidence.** Reported claims (verbatim from the article): AI-assisted melodies "were slower, used fewer notes and were judged by listeners as less creative." The article does not disambiguate "slower" (tempo vs. composition time), does not report effect sizes, rater N, or which of enjoyment/musicality differed significantly. Quotes: Oros — "We're trying to understand how these tools shape music and if they can support creative ideation when composing songs"; "A lot of studies on the effect of AI focus on productivity, but creativity and novelty are central outcomes." Randall — "Humans create music out of their own personal experiences and inspirations, and that resonates." Telang raised training-corpus/copyright concerns.

**For the studio.** Direct empirical support for the founder's rejection of text-to-full-song as *the* creative paradigm: Udio-as-inspiration in a composition task made output less creative by listener judgement. It is also a caution: the AI condition was a *prompt-to-audio* tool bolted beside a keyboard, not an integrated symbolic co-creator — the studio should be evaluated with the same design (randomised, blind raters) to show the difference. Treat numbers as preliminary until the paper appears.

<small>Tags: [HCI-study] [evaluation] [creativity-support] [ethics-legal] · Verification: verified (CMU + Heinz articles, CODE\@MIT programme fetched); underlying paper unverified/unpublished · Clusters 02, 08</small>

### `tchemeube2023mmmc` — MMM-C — Evaluating Human-AI Interaction via Usability, User Experience and Acceptance Measures for MMM-C: A Creative AI System for Music Composition

*Renaud Bougueng Tchemeube, Jeff Ens, Cale Plut, Philippe Pasquier, Maryam Safi, Yvan Grabit, Jean-Baptiste Rolland; Simon Fraser University, Steinberg; IJCAI 2023 (AI, the Arts and Creativity track)*

Links: https://doi.org/10.24963/ijcai.2023/640 ; https://arxiv.org/abs/2504.14071

MMM integrated into Cubase as a one-parameter plugin: select bars on tracks → set temperature → Generate (model conditions on vertical and horizontal context and instrument).

**Evidence.** 3-part mixed-methods study, 18 expert composers (8 hobbyist, 10 professional). SUS 73.8–75.7; TAM ease 3.1–3.3/5, usefulness 3.4–3.7/5; CSI enjoyment highest (3.85/5); ease of control 5.2/10 but *desire for more control 9.5/10*. Users engaged in repeated generation and heavy curation; retained authorship; no hobbyist/professional differences.

**For the studio.** Quantifies the cost of under-parameterised control and shows in-DAW integration is necessary but insufficient — the annotation layer is the missing control channel.

<small>Tags: [HCI-study] [DAW-plugin] [controllability] [evaluation] [symbolic-generation] · Verification: verified (fetched arXiv HTML) · Cluster 05</small>

### `louie2020cococo` — Cococo — Novice-AI Music Co-Creation via AI-Steering Tools for Deep Generative Models

*Ryan Louie, Andy Coenen, Cheng-Zhi Anna Huang, Michael Terry, Carrie J. Cai; Northwestern University / Google Research; ACM CHI 2020*

Links: https://doi.org/10.1145/3313831.3376739 ; PDF: https://youralien.github.io/files/cococo_chi2020_copy.pdf ; demo video: https://www.youtube.com/watch?v=jmlc-0pHcOw

A web notation/piano-roll editor on top of Coconet with four "AI-steering tools": **Voice Lanes** (restrict generation to chosen voices and time spans), **Example-Based Sliders** (similarity to a reference passage), **Semantic Sliders** (conventional↔surprising via temperature; happy↔sad via major/minor triad bias), and **Multiple Alternatives** (audition several fills). All implemented as "soft priors" on Coconet's sampling distribution, no retraining. Input: partial four-voice score + slider settings; output: infilled score the user keeps editing.

**Evidence.** Needfinding study found the baseline AI "overwhelm[s] users with the amount of musical content" and frustrates with non-determinism. Summative within-subjects study, N=21 novices, 15-min tasks: Cococo beat the conventional infilling interface on controllability (5.9 vs 3.5), comprehensibility (5.3 vs 3.2), sense of collaboration (5.9 vs 4.0), self-efficacy (5.9 vs 3.7), ownership (5.2 vs 3.8), creative expression (5.5 vs 3.8), all p<0.01. Users built pieces "bit-by-bit" voice-by-voice and used "generate, audition, edit" loops; one described the system as "an art assistant, who is extremely proficient, but has a clear understanding of who is in control." Authors: generative capabilities "may need to be partitioned into smaller, semantically meaningful tools to promote effective co-creation."

**For the studio.** The best-documented blueprint for the studio's edit/annotate/compile UI: annotations (lanes, sliders, examples) become constraints on a compile step; the study quantifies their effect on ownership.

<small>Tags: [HCI-study] [co-creation-framework] [controllability] [infilling] [editing] [notation] [creativity-support] [mixed-initiative] · Verification: verified (author PDF fetched) · Clusters 01, 05</small>

### `louie2022expressive` — ExpressiveCommunication — Expressive Communication: A Common Framework for Evaluating Developments in Generative Models and Steering Interfaces

*Ryan Louie, Jesse Engel, Cheng-Zhi Anna Huang; Northwestern University / Google Research; ACM IUI 2022 (arXiv 2111.14951)*

Links: https://arxiv.org/abs/2111.14951 ; https://doi.org/10.1145/3490099.3511159

An evaluation framework and 2×2 study: two models (PerformanceRNN vs Music Transformer) × two interfaces ("Radio" — curate random full phrases — vs "Steering" — chunk-by-chunk composition with semantic filtering). Composers write music to express a given image/word; listeners judge whether it communicates the intended feeling and how musical it is.

**Evidence.** 26 composers made 100+ pieces; 20 listeners gave 1,020 head-to-head comparisons. Steering interface: ownership 4.8 vs 2.42, control 5.0 vs 2.58 (p<1e-6); its pieces better evoked target feelings and sounded more musical. Music Transformer: preferred for feeling (p<0.001) and musicality (p<1e-5). Steering mattered most when the target emotion (e.g., fear) fought the model's bias. Conclusion: "more expressive models and more steerable interfaces are important and complementary."

**For the studio.** Gives the studio an evaluation protocol (composer self-report + blind listener judgments of communicative intent) and evidence to justify investing in editing/steering UI even as models improve.

<small>Tags: [evaluation] [HCI-study] [co-creation-framework] [controllability] [creativity-support] · Verification: verified (arXiv PDF fetched) · Clusters 01, 05</small>

### `krol2025ownership` — RhapsodyRefiner — Supporting Creative Ownership through Deep Learning-Based Music Variation

*Stephen James Krol, Maria Teresa Llano, Jon McCormack; Monash University, University of Sussex; arXiv 2025 (2509.25834)*

Links: https://arxiv.org/abs/2509.25834

"Rhapsody Refiner": a standalone tool that takes the musician's own MIDI and produces *variations* by selectively masking notes and re-predicting them with MusicBERT under user-set parameters; deliberately depends on strong human input and does not compose from scratch.

**Evidence.** Four-week ecological study with 8 practising musicians (songwriters, producers, educators, instrumentalists): tutorial, independent use, journals, logs, semi-structured interviews, thematic analysis. Findings: valued for "moments, not whole ideas"; dependence on the musician's input promoted ownership of process and artefact; participants rejected automatic completion; imperfection/randomness prompted creative problem-solving.

**For the studio.** Strongest recent evidence for the founder's stance — AI that transforms *authored* material preserves ownership; also a rare longitudinal (in-the-wild) study design to emulate.

<small>Tags: [HCI-study] [editing] [symbolic-generation] [creativity-support] [evaluation] · Verification: verified (fetched arXiv HTML) · Cluster 05</small>

### `zhang2023loopcopilot` — LoopCopilot — Loop Copilot: Conducting AI Ensembles for Music Generation and Iterative Editing

*Yixiao Zhang, Akira Maezawa, Gus Xia, Kazuhiko Yamamoto, Simon Dixon; QMUL, Yamaha, NYU Shanghai; arXiv 2023*

Links: https://arxiv.org/abs/2310.12404

Conversational system where an LLM "conductor" interprets requests, selects and chains backend audio models (MusicGen, AudioLDM, Demucs, etc.) for generation (text-to-music, drums, impression-to-music) and *editing* (add/remove track, regenerate, effects, pitch/speed), with a Global Attribute Table (tempo, key, genre, mood, instruments, audio files) as shared blackboard for continuity across turns.

**Evidence.** N=8 music/audio-technology users; SUS 75.3±15.3, TAM 4.09±1.09; valued for inspiration; complaints: limited musical-attribute control, prompt responsiveness, desire for DAW integration.

**For the studio.** Its Global Attribute Table is an early "compilation state" object; its failure modes (coarse control, no DAW) argue for symbolic, editable intermediate representations.

<small>Tags: [LLM-agent] [audio-generation] [editing] [HCI-study] · Verification: verified (fetched arXiv abstract) · Cluster 05</small>

## E2. Evidence: field studies & practitioner perspectives

### `sturm2019machinefolk` — MachineFolk — Machine learning research that matters for music creation: A case study (folk-rnn)

*Bob L. Sturm, Oded Ben-Tal, Úna Monaghan, Nick Collins, Dorien Herremans, Elaine Chew, Gaëtan Hadjeres, Emmanuel Deruty, François Pachet; KTH, Kingston, Cambridge, Durham, SUTD, QMUL, Sony CSL; Journal of New Music Research 48(1):36–55, 2019*

Links: https://doi.org/10.1080/09298215.2018.1515233 ; https://folkrnn.org ; album *Let's Have Another Gan Ainm* (2018)

Case study of folk-rnn (LSTM over ABC-notation Irish/Scottish tunes) used by traditional and contemporary musicians and composers over several years — concerts, an album, a musical — to ask what ML research "matters" for music creation.

**Evidence.** Practitioner accounts: generated tunes are *raw material* requiring editing, arrangement and performance; musicians valued the tool as a source of unexpected ideas but cared about the tradition's social meaning; the paper argues for evaluating ML by its usefulness to practice rather than by likelihood.

**For the studio.** Notation-native (ABC) generation actually used by working musicians; validates "AI output is material to edit," and the community-attitude concerns the studio must respect.

<small>Tags: [HCI-study] [symbolic-generation] [notation] [ethics-legal] [evaluation] · Verification: verified (Crossref metadata; content from companion Arts paper) · Cluster 05</small>

### `huang2020aisongcontest` — AISongContest — AI Song Contest: Human-AI Co-Creation in Songwriting

*Cheng-Zhi Anna Huang, Hendrik Vincent Koops, Ed Newton-Rex, Monica Dinculescu, Carrie J. Cai; Google Brain / RTL Netherlands / ByteDance; ISMIR 2020 (arXiv 2010.05388)*

Links: https://arxiv.org/abs/2010.05388 ; https://doi.org/10.5281/zenodo.4245530

Survey-based thematic analysis of how 13 teams (61 people, 2–15 per team, median 4) built songs with AI for the 2020 VPRO AI Song Contest. Not a system: a field study of real co-creation workflows across lyrics, melody, harmony, bass, drums, vocal/instrument synthesis and structure.

**Evidence.** Teams used a median of 4 model types (GPT-2, CharRNN, MusicVAE, Coconet, DrumRNN, WaveNet, GANs…); "rarely attempted end-to-end generation"; generated massively and curated post hoc (one team 450 melodies; another 10,000 lyric lines); steered by priming inputs, fine-tuning on curated data, latent interpolation; manually authored structure because small models lack "holistic context." One team described "jamming with another musician… priming the AI with chord progressions, hearing AI output, riffing on that output." Conclusion: need interfaces that are "more decomposable, steerable, interpretable, and adaptive."

**For the studio.** Independent evidence that expert practitioners *already* work in the founder's modular, iterative way and want the AI to fit into it; the four adjectives are a ready-made requirements list.

<small>Tags: [HCI-study] [co-creation-framework] [controllability] [structure] [evaluation] · Verification: verified (arXiv PDF fetched) · Clusters 01, 05</small>

### `ford2024reflection` — ReflectionAIMusic — Reflection Across AI-based Music Composition

*Corey Ford, Ashley Noel-Hirst, Sara Cardinale, Jackson Loth, Pedro Sarmento, Elizabeth Wilson, Lewis Wolstanholme, Kyle Worrall, Nick Bryan-Kinns; QMUL, York, UAL Creative Computing Institute; ACM Creativity & Cognition 2024*

Links: https://doi.org/10.1145/3635636.3656185

Eight composer-researchers each composed with a different AI tool (Markov chains to VAEs), pausing hourly to reflect on screenshots of their work; first-person accounts, interviews and questionnaires analysed for patterns of *reflection*.

**Evidence.** Composers reflected mostly on future directions while *curating* AI-generated content; curation is where creative decisions concentrate; supports designing for reflection (history, comparison) rather than only generation.

**For the studio.** Suggests the compile loop should surface *history and alternatives* to support reflection, and that annotation moments are reflective moments worth capturing.

<small>Tags: [HCI-study] [creativity-support] [evaluation] · Verification: verified (Semantic Scholar abstract) · Cluster 05</small>

### `deruty2022sonycsl` — SonyCSLPractice — On the Development and Practice of AI Technology for Contemporary Popular Music Production

*Emmanuel Deruty, Maarten Grachten, Stefan Lattner, Javier Nistal, Cyran Aouameur; Sony CSL Paris; TISMIR 5(1), 2022*

Links: https://doi.org/10.5334/tismir.100

Reflection on 6–18-month collaborations with six professional acts (Niro, Twenty9, Hyper Music, Uèle Lamore, Whim Therapy, Donn Healy) using Sony CSL prototypes (DrumNet, BassNet, LeadNet, DrumGAN, Notono, Planet Drums, ResonanceEQ, ProfileEQ); argues in-studio popular-music practice is audio-first and that audio tools fit it better than MIDI tools.

**Evidence.** Qualitative thematic analysis of interviews and workflow documentation. Patterns: "pull" (explicit queries) over "push" (unsolicited suggestions); *priming* on the artist's own audio; generate-and-curate; latent-space navigation; exploiting artefacts ("AI, the new analog?"); repurposing tools. Friction: leaving the DAW, lack of recognisable control, need for visualisation. Proposes validation by workflow integration, task simplification, stimulation, identifiable contribution and commercial viability.

**For the studio.** The most in-depth professional-producer study; its "pull, prime on my material, keep me in the DAW" findings are design constraints — and its audio-first claim is the counterpoint the symbolic-first studio must answer (e.g., by rendering stems).

<small>Tags: [HCI-study] [audio-generation] [DAW-plugin] [controllability] [evaluation] · Verification: verified (fetched TISMIR page) · Cluster 05</small>

### `ronchini2025ttmuserstudy` — TTMUserStudy — AI-Assisted Music Production: A User Study on Text-to-Music Models

*Francesca Ronchini, Luca Comanducci, Simone Marcucci, Fabio Antonacci; Politecnico di Milano; CMMR 2025 (17th Int. Symposium on Computer Music Multidisciplinary Research), London (arXiv 2509.23364)*

Links: https://arxiv.org/abs/2509.23364

Qualitative study: **N = 17 music producers (7 countries)** used a custom tool combining **MusicGen** with **HT-Demucs 6-stem separation**; semi-structured interviews + thematic analysis.

**Evidence.** N=17 producers from 7 countries (mixed experience); pre-survey, recorded session, Likert questionnaire, interviews, thematic analysis. TTM seen as *inspiration*, not production-ready: 94% would use it in ideation; barriers were intent–output misalignment, tempo/key/beat alignment, limited editability; ethical worries about copyright, compensation and homogenisation from Western-centric data.

**For the studio.** Rare empirical evidence from working producers that text prompting alone fails at the *structural alignment* level (tempo/key/beat)—precisely what symbolic-first conditioning solves. Cross-cluster with HCI/co-creation studies.

<small>Tags: [HCI-study] [text-conditioning] [audio-generation] [ethics-legal] · Verification: verified (HTML full text) · Clusters 04, 05</small>

### `micchi2021ikeepcounting` — IKeepCounting — I Keep Counting: An Experiment in Human/AI Co-creative Songwriting

*Gianluca Micchi, Louis Bigo, Mathieu Giraud, Richard Groult, Florence Levé; Algomus (Univ. Lille / CRIStAL, Univ. Picardie); TISMIR 4(1), 2021*

Links: https://doi.org/10.5334/tismir.93

First-person account of an AI Song Contest 2020 entry: structure from a Markov model (SALAMI), chords from an LSTM (Eurovision MIDI), lyrics from GPT-2 seeded with Eurovision bigrams, hook from a classical-theme database; humans filtered candidates (sometimes by dice roll), composed verse melodies, arranged and produced. Contrasts "AI as automation" with "AI as suggestion."

**Evidence.** >25 documented human interventions; surprising AI chords (F#maj7, Bbm) acted as productive constraints; the team argues deliberate selection/modification of AI material constitutes authorship and released the song CC-BY-SA.

**For the studio.** A concrete, honest log of a *compile-from-parts* workflow and of how constraints from AI suggestions can enhance creativity; supports logging interventions as provenance.

<small>Tags: [HCI-study] [co-creation-framework] [symbolic-generation] [structure] [ethics-legal] · Verification: verified (fetched TISMIR article page) · Cluster 05</small>

### `oros2026helpthathurts` — Generative AI in composition teaching — early empirical papers (2024–2026)

*Jose Eduardo Oros, Richard Randall, Rahul Telang (CMU), "Help That Hurts: The Creativity Cost of Generative AI Ideation in Music Composition" (SSRN 2026, DOI 10.2139/ssrn.6481538); Bin Liu & Yuanyuan Liao, "Integrating IBM Watson BEAT generative AI software into flute music learning" (Education and Information Technologies 2025, DOI 10.1007/s10639-025-13394-y); SunYoung Park & YoungSun Choo, "Exploring Interactions with AI-Based Music Composition Tools Across Different Levels of Musical Expertise" (Korean Music Education Society 2026); Prapussornchaikul & Gonsalves, WAIE 2024*

Links: https://doi.org/10.2139/ssrn.6481538 ; https://doi.org/10.1007/s10639-025-13394-y

First wave of studies on generative AI in music learning: an experiment suggesting AI ideation can *reduce* creative output quality/originality in composition tasks ("help that hurts"); classroom integrations of generative tools; expertise-dependent interaction patterns with AI composition tools.

**Evidence.** Study designs and N not fetched (Crossref metadata only); venue quality mixed — treat as indicative, not conclusive. No dedicated ISMIR/NIME "LLM feedback on student compositions" paper could be verified in this pass.

**For the studio.** Early evidence that *how* AI assistance is inserted matters for creative outcomes — supporting the founder's "human-centred, AI as compiler not ideator" stance; also a gap the studio could study (feedback on compositions rather than generation).

<small>Tags: [education] [HCI-study] [creativity-support] [evaluation] · Verification: partial (Crossref records only) · Cluster 07</small>

### `morris2024haisp` — HAISP — HAISP: A Dataset of Human-AI Songwriting Processes from the AI Song Contest (and its 2025 expansion)

*Lidia J. Morris, Rebecca Leger, Michele Newman, John Ashley Burgoyne, Ryan Groves, Natasha Mangal, Jin Ha Lee; University of Washington, Fraunhofer IIS, University of Amsterdam, AI Song Contest; ISMIR 2024; expansion: Morris, Newman, Tang, Singh, Vélez Vásquez, Leger, Lee, ISMIR 2025*

Links: https://doi.org/10.5281/zenodo.14877357 ; https://doi.org/10.5281/zenodo.17706323

Coded dataset of the *process* descriptions submitted by AI Song Contest teams (34 submissions from 2023; extended with 2024 entries) — which tools were used for which task, how decisions were made, what control creators retained — rather than the songs.

**Evidence.** 2025 paper compares 2023 vs 2024 cohorts: shifts in collaboration patterns, differences in creative agency between general-purpose systems (e.g., Suno/ChatGPT-style) and fine-tuned/custom tools, and design recommendations for songwriting platforms.

**For the studio.** The only longitudinal, coded corpus of real human–AI songwriting workflows; a source for a taxonomy of tasks and control points the compile loop should cover.

<small>Tags: [dataset] [HCI-study] [co-creation-framework] [structure] · Verification: verified (fetched Zenodo records) · Cluster 05</small>

### `newman2023perceptions` — Newman2023 — Human-AI Music Creation: Understanding the Perceptions and Experiences of Music Creators for Ethical and Productive Collaboration

*Michele Newman, Lidia J. Morris, Jin Ha Lee; University of Washington iSchool; ISMIR 2023*

Links: https://doi.org/10.5281/zenodo.10265227 ; https://archives.ismir.net/ismir2023/paper/000008.pdf

Case studies of how professional creators perceive and use AI for melody, harmony, lyrics and mixing.

**Evidence.** N=6 professionals (classical/jazz composer, film/game composer, interactive-media composer, electroacoustic composer, sound artist, DJ; 5+ years experience; 5 active AI users, 1 sceptic), 60–90 min semi-structured interviews, two-coder inductive–deductive coding (ATLAS.ti). Twelve categories in two themes (AI as collaborator; democratisation). Design implications: preserve creative control (AI for ideation/exploration, not intentional decisions); interoperability (MIDI/WAV/MusicXML export or in-software integration); separate "influences" (ideas) from "mechanisms" (housekeeping); prefer open-source, explainable models over black boxes; role of AI shifts with context.

**For the studio.** Explicitly asks for MusicXML/MIDI interoperability, open models and control preservation — a near-verbatim endorsement of the studio's symbolic-first, open-source stance.

<small>Tags: [HCI-study] [ethics-legal] [co-creation-framework] [notation] · Verification: verified (fetched ISMIR PDF) · Cluster 05</small>

### `suh2021socialglue` — SocialGlue — AI as Social Glue: Uncovering the Roles of Deep Generative AI during Social Music Composition

*Minhyang (Mia) Suh, Emily Youngblom, Michael Terry, Carrie J. Cai; Google Research / University of Washington; CHI 2021*

Links: https://doi.org/10.1145/3411764.3445219

Lab study of *pairs* of strangers co-composing with and without Cococo's generative model, to see how AI reshapes human–human creative collaboration.

**Evidence.** N=30 (15 pairs stratified: 5 novice, 5 hobbyist, 5 serious composer pairs), two 20-minute co-composition tasks, think-aloud + interviews. AI acted as common-ground seeder, psychological safety net, progress catalyst, friction mitigator and *role transformer* — pairs shifted from co-composing to co-*producing* (evaluating AI output), easing collaboration but reducing its depth.

**For the studio.** Warns that a generous compiler can turn composers into curators; the studio should keep authoring primitives (notation editing, sketching) primary and generation secondary.

<small>Tags: [HCI-study] [co-creation-framework] [creativity-support] · Verification: partial (ACM page blocked; N/method from a secondary summary and OUCI index) · Cluster 05</small>

### `fu2025novice` — NoviceProduction — Exploring the Collaborative Co-Creation Process with AI: A Case Study in Novice Music Production

*Yue Fu, Michele Newman, Lewis Going, Qiuzi Feng, Jin Ha Lee; University of Washington iSchool; ACM DIS 2025*

Links: https://arxiv.org/abs/2501.15276

10-week capstone course in which three teams of undergraduates with little production experience each produced three tracks using AI tools; artefact review plus interviews.

**Evidence.** N=9 interviewed (of 20), 55–70 min each, reflexive thematic analysis. AI accelerated ideation but compressed preparation; a new "collaging and refinement" stage emerged to integrate heterogeneous AI outputs; AI mediated group dynamics (blunter critique of AI output); participants prized human emotional expression and consciously retained control.

**For the studio.** "Collaging and refinement" is precisely the assembly step the founder calls *compile*; the study shows novices need tooling for it.

<small>Tags: [HCI-study] [education] [co-creation-framework] · Verification: verified (fetched arXiv HTML) · Cluster 05</small>

## E3. Evidence: deployed systems with usage data

### `huang2019bachdoodle` — BachDoodle — The Bach Doodle: Approachable Music Composition with Machine Learning at Scale

*Cheng-Zhi Anna Huang, Curtis Hawthorne, Adam Roberts, Monica Dinculescu, James Wexler, Leon Hong, Jacob Howcroft; Google Brain / Google Doodles; ISMIR 2019 (arXiv 1907.06637)*

Links: https://arxiv.org/abs/1907.06637 ; dataset: https://magenta.withgoogle.com/datasets/bach-doodle ; interactive: https://www.google.com/doodles/celebrating-johann-sebastian-bach

Google's first AI-powered Doodle (March 2019). Users enter a two-bar melody on a simplified sheet-music grid; Coconet (re-implemented in TensorFlow.js, quantized to ~400 KB, 40 s → 2 s) harmonizes it into four voices in Bach style, running in-browser or on Cloud TPU depending on a speed calibration. Users could rate results and opt in to a public dataset.

**Evidence.** >55 million harmonization queries in three days, 350 cumulative years of engagement. The released Bach Doodle Dataset contains 21.6 million harmonizations from 8.5 million sessions (melody, harmonization, rating, country, session duration, playback count), CC BY 4.0.

**For the studio.** Proof at planetary scale that *human-authored melody → AI-compiled harmonization* on a notation surface is approachable for total novices; the dataset is a unique record of how people rate AI harmonizations of their own material.

<small>Tags: [symbolic-generation] [notation] [infilling] [dataset] [education] [product] [HCI-study] · Verification: verified (arXiv abstract and dataset page fetched) · Clusters 01, 05, 07</small>

### `donahue2024hookpadaria` — HookpadAria — Hookpad Aria: A Copilot for Songwriters

*Chris Donahue, Shih-Lun Wu, Yewon Kim, Dave Carlton, Ryan Miyakawa, John Thickstun; CMU + Hooktheory + Cornell. ISMIR 2024 Late-Breaking Demo (arXiv 2502.08122, Feb 2025). Product beta March 2024, official launch August 2024.*

Links: https://www.hooktheory.com/hookpad ; https://www.hooktheory.com/hookpad/aria ; https://www.hooktheory.com/blog/generative-ai-songwriting/

Generative copilot integrated into Hookpad, a web lead-sheet editor (melody + harmony, symbolic). Capabilities designed for *non-sequential* workflows: (1) left-to-right continuation, (2) **infilling missing spans in the middle of existing material**, (3) harmony from melody and melody from harmony. Built on the Anticipatory Music Transformer approach (per Donahue's site) trained on Hooktheory's crowd-annotated corpus. Framed explicitly as a "scalable data flywheel for music co-creation".

**Evidence.** No published study by Hooktheory; Amuse's formative interviews (N=8 Aria users) report it is valued for contextual suggestions but lacks multimodal inspiration input.

**For the studio.** The closest shipping analogue of the founder's loop (symbolic, region-based, editable, harmony-aware) and proof that an academic infilling model can be productised on a small, consented, functional-harmony dataset. Cross-ref cluster on infilling (Anticipatory Music Transformer).

<small>Tags: [product] [symbolic-generation] [infilling] [notation] [co-creation-framework] [DAW-plugin] · Verification: verified (arXiv abstract; chrisdonahue.com news) · Clusters 02, 05, 07, 08</small>

### `casini2025sunoudio` — SunoUdioAnalysis — Data-Driven Analysis of Text-Conditioned AI-Generated Music: A Case Study with Suno and Udio

*Luca Casini, Laura Cros Vila, David Dalmazzo, Anna-Kaisa Kaila, Bob L. T. Sturm; KTH Stockholm (MUSAiC); arXiv Sept 2025.*

Links: https://arxiv.org/abs/2509.11824

Large-scale analysis of user prompts, metatags and generated lyrics from Suno and Udio (May–Oct 2024) using text embeddings/clustering; identifies lyrical themes, language use and "peculiar" steering strategies via metatags.

**Evidence.** Corpus analysis with interactive plots.

**For the studio.** Empirical picture of how people actually try to *control* text-to-song systems — the pain points a symbolic, annotation-based interface should solve.

<small>Tags: [evaluation] [text-conditioning] [HCI-study] · Verification: verified · Cluster 08</small>

## E4. Evaluation: metrics for generated music

### `huang2025audiomos` — AudioMOS — AudioMOS Challenge 2025 and ICASSP 2026 Automatic Song Aesthetics Evaluation (ASAE) Challenge

*AudioMOS: Wen-Chin Huang, Hui Wang, Cheng Liu, Yi-Chiao Wu, Andros Tjandra, Wei-Ning Hsu, Erica Cooper, Yong Qin, Tomoki Toda (Nagoya/Nankai/Meta/NII), arXiv Sept 2025 (ASRU 2025). ASAE: ICASSP 2026 grand challenge (arXiv 2601.07237, Jan 2026).*

Links: https://arxiv.org/abs/2509.01336 ; https://arxiv.org/abs/2601.07237

Shared tasks for *predicting* human quality ratings of generated audio: AudioMOS Track 1 = text-to-music overall quality + text alignment (MusicEval), Track 2 = Meta **Audiobox Aesthetics** four axes (production quality, complexity, enjoyment, usefulness) across TTS/TTA/TTM; ASAE = overall musicality plus five aesthetic dimensions of full AI songs. 24 teams (AudioMOS); baselines beaten.

**Evidence.** Community benchmarks; establishes MOS-prediction as a research line.

**For the studio.** Off-the-shelf aesthetic predictors (Audiobox Aesthetics, winning ASAE systems) can rank candidate renders before the composer hears them — a cheap pre-filter in a compile loop.

<small>Tags: [evaluation] [audio-generation] · Verification: verified · Cluster 08</small>

### `gui2024fad` — FADadapt — Adapting Fréchet Audio Distance for Generative Music Evaluation (fadtk)

*Azalea Gui, Hannes Gamper, Sebastian Braun, Dimitra Emmanouilidou; Microsoft Research; ICASSP 2024.*

Links: https://arxiv.org/abs/2311.01616 ; https://github.com/microsoft/fadtk

Shows FAD's sample-size bias, poor embedding choice (VGGish) and weak reference sets; proposes extrapolating to infinite sample size, using **CLAP-LAION-music** embeddings and music reference sets, and **per-song FAD** for outlier detection.

**Evidence.** Correlated with human listening data and MusicCaps quality annotations across several generative systems.

**For the studio.** If FAD is used at all, use fadtk's recipe.

<small>Tags: [evaluation] [audio-generation] [toolkit] · Verification: verified · Cluster 08</small>

### `liu2025musiceval` — MusicEval — MusicEval: A Generative Music Dataset with Expert Ratings for Automatic Text-to-Music Evaluation

*Cheng Liu, Hui Wang, Jinghua Zhao, Shiwan Zhao, Hui Bu, Xin Xu, Jiaming Zhou, Haoqin Sun, Yong Qin; Nankai University / AISHELL; ICASSP 2025 (arXiv Jan 2025).*

Links: https://arxiv.org/abs/2501.10811 ; https://www.aishelltech.com/AISHELL_7A

2,748 clips from 31 text-to-music systems over 384 prompts rated by 14 music professionals (13,740 ratings) on overall musical impression and text alignment; a CLAP-based MOS predictor baseline. Basis of AudioMOS Challenge 2025 Track 1.

**Evidence.** Dataset + baseline released.

**For the studio.** Expert-rated reference data for training/validating any automatic "does the render match the annotation" judge.

<small>Tags: [evaluation] [dataset] [text-conditioning] · Verification: verified · Cluster 08</small>

### `kader2025survey` — EvalSurvey — A Survey on Evaluation Metrics for Music Generation

*Faria Binte Kader & Santu Karmaker; University of Central Florida; arXiv Aug 2025.*

Links: https://arxiv.org/abs/2509.00051

Taxonomy of objective (symbolic and audio) and subjective metrics; identifies poor metric–perception correlation, cross-cultural bias and lack of standardisation; proposes directions for a comprehensive framework.

**Evidence.** Survey.

**For the studio.** One-stop map for the literature review's evaluation section.

<small>Tags: [evaluation] · Verification: verified · Cluster 08</small>

### `figueiredo2025echoes` — EchoesHumanity — Echoes of Humanity: Exploring the Perceived Humanness of AI Music

*Flavio Figueiredo, Giovanni Martinelli, Henrique Sousa, Pedro Rodrigues, Frederico Pedrosa, Lucas N. Ferreira; UFMG (Brazil); NeurIPS 2025 Creative AI track (arXiv 2509.25601).*

Links: https://arxiv.org/abs/2509.25601

Blind, Turing-like pairwise test with a randomised crossover design on *real-world* Suno outputs vs human songs, controlling pairwise similarity; free-text justifications analysed.

**Evidence.** Listeners' ability to spot the AI track **causally increases when pairs are similar**; cues cited are mostly vocal/technical.

**For the studio.** Methodological template for "can listeners tell compiled from hand-arranged" tests; pair-matching matters.

<small>Tags: [evaluation] [HCI-study] · Verification: verified · Cluster 08</small>

### `grotschla2025benchmarking` — HumanPrefBench — Benchmarking Music Generation Models and Metrics via Human Preference Studies

*Florian Grötschla, Ahmet Solak, Luca A. Lanzendörfer, Roger Wattenhofer; ETH Zürich; ICASSP 2025 (arXiv June 2025).*

Links: https://arxiv.org/abs/2506.19085 ; https://doi.org/10.1109/ICASSP49660.2025.10887745

6,000 songs from 12 SOTA generators; 15,000 pairwise comparisons by 2,500 raters; ranks models and computes correlation of FAD/KAD/CLAP and other metrics with human preference; data released.

**Evidence.** First human-preference ranking of current models; documents metric–human gaps.

**For the studio.** Methodological template (pairwise, large-N, open data) and a caution against metric-driven claims.

<small>Tags: [evaluation] [audio-generation] [dataset] · Verification: verified · Cluster 08</small>

### `zhang2025aesthetics` — AestheticsVsPref — From Aesthetics to Human Preferences: Comparative Perspectives of Evaluating Text-to-Music Systems

*Huan Zhang, Jinhua Liang, Huy Phan, Wenwu Wang, Emmanouil Benetos; QMUL/Surrey; arXiv 30 Apr 2025.*

Links: https://arxiv.org/abs/2504.21815

Compares perceptual aesthetic scores and distributional metrics (Mauve Audio Divergence, KAD) against human preferences over five leading TTM systems; finds automatic metrics inconsistent with human judgment; releases a multi-model benchmark set.

**Evidence.** Human study across five systems.

**For the studio.** Independent confirmation that human-centred evaluation must be primary.

<small>Tags: [evaluation] [audio-generation] · Verification: verified · Cluster 08</small>

### `manco2023songdescriber` — SongDescriber — The Song Describer Dataset: A Corpus of Audio Captions for Music-and-Language Evaluation

*Ilaria Manco, Benno Weck, SeungHeon Doh, et al. (Minz Won, Yixiao Zhang, Dmitry Bogdanov, Yusong Wu, Ke Chen, Philip Tovstogan, Emmanouil Benetos, Elio Quinton, György Fazekas, Juhan Nam); QMUL / UPF / KAIST / others; NeurIPS 2023 ML4Audio workshop.*

Links: https://arxiv.org/abs/2311.10057 ; data https://zenodo.org/records/10072001

**1.1k crowd-sourced captions for 706 CC-licensed tracks (MTG-Jamendo)**; used to evaluate captioning, text-to-music generation and retrieval (e.g., Stable Audio Open reports on it).

**Evidence.** Shows cross-dataset performance variation vs MusicCaps.

**For the studio.** A clean-license evaluation set for any text-conditioned rendering the studio ships.

<small>Tags: [dataset] [evaluation] · Verification: verified (abstract); authors partial · Cluster 04</small>

### `retkowski2024fmd` — FMD — Fréchet Music Distance (symbolic)

*Jan Retkowski, Jakub Stępniak, Mateusz Modrzejewski; Warsaw University of Technology; arXiv Dec 2024 (rev. Jan 2025), COLING 2025.*

Links: https://arxiv.org/abs/2412.07948 ; https://github.com/jryban/frechet-music-distance

Fréchet distance over embeddings of *symbolic* music (CLaMP 2 / MusicGen-encoder–style) between reference and generated MIDI/ABC sets; validated to separate model quality levels across datasets.

**Evidence.** Sensitivity experiments across models/datasets; released code.

**For the studio.** The first standard distributional metric for **symbolic** output — the studio's native domain.

<small>Tags: [evaluation] [symbolic-generation] [toolkit] · Verification: verified · Cluster 08</small>

### `kilgour2019fad` — FAD — Fréchet Audio Distance

*Kevin Kilgour, Mauricio Zuluaga, Dominik Roblek, Matthew Sharifi; Google; Interspeech 2019 (arXiv 1812.08466, Dec 2018).*

Links: https://arxiv.org/abs/1812.08466 ; https://github.com/google-research/google-research/tree/master/frechet_audio_distance

Fréchet distance between Gaussians fit to VGGish embeddings of reference vs evaluated audio sets; originally proposed for music *enhancement*, then adopted as the default metric for generative music/audio.

**Evidence.** Correlated with human ratings of enhancement artefacts in the original paper only.

**For the studio.** Ubiquitous but flawed baseline; know its assumptions before using it for rendered output.

<small>Tags: [evaluation] [audio-generation] · Verification: partial · Cluster 08</small>

### `yang2020evaluation` — YangLerch — On the evaluation of generative models in music

*Li-Chia Yang, Alexander Lerch; Georgia Tech Center for Music Technology; Neural Computing and Applications 32:4773–4784, 2020 (online 2018)*

Links: https://doi.org/10.1007/s00521-018-3849-7 ; https://github.com/RichardYang40148/mgeval

Proposes musically informed objective metrics (pitch/rhythm feature distributions; absolute measures and relative measures via KL divergence and overlap area against a reference set) so that generative-model papers can report reproducible, comparable results when full listening studies are infeasible.

**Evidence.** Demonstrated on symbolic generation systems; the mgeval toolkit is widely used.

**For the studio.** Complements HCI measures with artefact-level metrics for regression-testing the compiler (e.g., does an annotation move feature distributions as intended?).

<small>Tags: [evaluation] [symbolic-generation] [toolkit] · Verification: verified (fetched Springer page) · Clusters 05, 08</small>

### `huang2025aligning` — MAD — Aligning Text-to-Music Evaluation with Human Preferences

*Yichen Huang, Zachary Novack, Koichi Saito, Jiatong Shi, Shinji Watanabe, Yuki Mitsufuji, John Thickstun, Chris Donahue; CMU + UCSD + Sony + Cornell. ISMIR 2025 (arXiv Mar 2025).*

Links: https://arxiv.org/abs/2503.16669

Shows Fréchet Audio Distance is inconsistent and weakly correlated with human judgement; proposes **MAUVE Audio Divergence (MAD)** on self-supervised audio embeddings and releases the **MusicPrefs** human-preference dataset.

**Evidence.** MAD average rank correlation 0.84 vs FAD 0.49 on synthetic tests; 0.62 vs 0.14 correlation with MusicPrefs.

**For the studio.** A defensible automatic metric for rendered audio during iteration.

<small>Tags: [evaluation] [audio-generation] [dataset] · Verification: verified (arXiv abstract) · Cluster 02</small>

### `kim2025musicarena` — MusicArena — Music Arena: Live Evaluation for Text-to-Music

*Yonghyun Kim, Wayne Chi, Anastasios N. Angelopoulos, Wei-Lin Chiang, Koichi Saito, Shinji Watanabe, Yuki Mitsufuji, Chris Donahue; CMU + Sony AI + LMArena. arXiv July 2025; NeurIPS 2025 Creative AI track. Platform launched July 2025.*

Links: https://arxiv.org/abs/2507.20900 ; https://music-arena.org ; data: https://huggingface.co/music-arena

Open platform for live pairwise human-preference evaluation of text-to-music models: users type prompts, hear two outputs, vote; LLM-based routing handles heterogeneous model signatures; collects listening behaviour and free-text feedback; rolling open data releases with privacy guarantees; leaderboard.

**Evidence.** Platform + protocol paper; blog (Sept 2025) reports first findings.

**For the studio.** Evaluation infrastructure and an open preference dataset; the studio could run its symbolic/arrangement outputs through an Arena-style protocol.

<small>Tags: [evaluation] [audio-generation] [dataset] · Verification: verified (arXiv abstract; lab page) · Cluster 02</small>

### `chung2025kad` — KAD — KAD: No More FAD! Kernel Audio Distance

*Yoonjin Chung, Pilsun Eu, Junwon Lee, Keunwoo Choi, Juhan Nam, Ben Sangbae Chon; Gaudio Lab / KAIST; arXiv Feb 2025 (ICASSP-track).*

Links: https://arxiv.org/abs/2502.15602 ; https://github.com/YoonjinXD/kadtk

Replaces the Gaussian/Fréchet assumption with an MMD kernel distance: distribution-free, unbiased, converges with small sample sizes, GPU-scalable.

**Evidence.** Reports stronger alignment with human perceptual judgments than FAD.

**For the studio.** Preferred distributional metric for any audio renderer evaluation in 2026.

<small>Tags: [evaluation] [audio-generation] [toolkit] · Verification: verified · Cluster 08</small>

## E5. Evaluation: creativity & co-creativity frameworks

### `cherry2014csi` — CSI — Quantifying the Creativity Support of Digital Tools through the Creativity Support Index

*Erin Cherry & Celine Latulipe, UNC Charlotte; *ACM TOCHI* 21(4), 2014 (earlier CHI EA 2009 "The creativity support index", Carroll & Latulipe).*

Links: https://doi.org/10.1145/2617588

Psychometric questionnaire with six factors — **Exploration, Expressiveness, Immersion, Enjoyment, Results Worth Effort, Collaboration** — each rated on two agreement items, plus paired-factor comparisons that weight factors by importance for the task, yielding a 0–100 score.

**Evidence.** Developed and validated over several iterations with hundreds of participants; now the standard instrument in music co-creation studies (used by Amuse 2025, MMM-C 2023 and many others).

**For the studio.** The instrument the studio should adopt for comparing interaction designs (e.g., with/without annotations, with/without version tree).

<small>Tags: [evaluation] [creativity-support] [HCI-study] · Verification: partial (title/venue/DOI confirmed via search results; full text not fetched) · Clusters 05, 08</small>

### `ritchie2007criteria` — Ritchie — Some empirical criteria for attributing creativity to a computer program

*Graeme Ritchie, University of Aberdeen; *Minds and Machines* 17(1), 67–99, 2007 (earlier 2001 workshop version).*

Links: https://doi.org/10.1007/s11023-007-9066-2

Eighteen formal criteria over an "inspiring set" and output set using ratings of *typicality* and *quality*: novelty relative to the inspiring set, proportion of good/typical outputs, etc.

**Evidence.** Applied to several CC systems (e.g., by Pereira et al.).

**For the studio.** Gives a principled way to measure whether compiled output is *both* stylistically typical of the composer's material and of high quality without merely copying it.

<small>Tags: [evaluation] [co-creation-framework] · Verification: partial · Cluster 08</small>

### `boden2004creativemind` — Boden — Boden's P-/H-creativity and exploratory/combinational/transformational creativity

*Margaret A. Boden, University of Sussex; *The Creative Mind: Myths and Mechanisms* (1990; 2nd ed. Routledge 2004).*

Links: https://doi.org/10.4324/9780203508527

Psychological (P-) vs historical (H-) creativity; three kinds of creativity — combinational, exploratory (within a conceptual space), transformational (changing the space). Standard vocabulary in computational creativity.

**Evidence.** Theoretical.

**For the studio.** Lets the project state precisely what the AI is expected to do: mostly *exploratory* generation inside the composer-defined space, with the human providing transformational moves.

<small>Tags: [evaluation] [co-creation-framework] [creativity-support] · Verification: partial · Cluster 08</small>

### `jordanous2012standardised` — CCEval — Computational-creativity evaluation anchors (Boden; Colton & Wiggins; Jordanous)

*Margaret Boden, *The Creative Mind: Myths and Mechanisms*, 2nd ed., Routledge 2004; Simon Colton & Geraint Wiggins, "Computational Creativity: The Final Frontier?", ECAI 2012; Anna Jordanous, "A Standardised Procedure for Evaluating Creative Systems (SPECS)", Cognitive Computation 4(3):246–279, 2012*

Links: https://doi.org/10.1007/s12559-012-9156-1 (Jordanous)

Boden's P-/H-creativity and combinational/exploratory/transformational creativity; Colton & Wiggins' definition of computational creativity and the "creative tripod" (skill, appreciation, imagination); Jordanous' SPECS — 14 components of creativity and a three-step procedure (define creativity for the domain, choose standards, test).

**Evidence.** Applied to GenJam-like improvisers and others; meta-evaluation paper (ICCC 2014).

**For the studio.** Provides the definitions a literature review needs before discussing "co-creativity"; SPECS is a candidate for evaluating the compiler's contributions as *creative* rather than merely useful.

<small>Tags: [co-creation-framework] [evaluation] [theory-analysis] · Verification: partial (Jordanous verified via Crossref; Boden/Colton–Wiggins from recall) · Clusters 05, 08</small>

### `karimi2018evaluating` — Karimi2018 — Evaluating Creativity in Computational Co-Creative Systems

*Pegah Karimi, Kazjon Grace, Mary Lou Maher, Nicholas Davis; UNC Charlotte / U. Sydney; ICCC 2018 (arXiv 1807.09886).*

Links: https://arxiv.org/abs/1807.09886 ; https://computationalcreativity.net/iccc2018/sites/default/files/papers/ICCC_2018_paper_26.pdf

Framework of four questions for co-creative evaluation — **who** evaluates (human/AI/both), **what** is evaluated (product, process, interaction/collaboration), **when** (during/after/continuous), **how** (metrics, qualitative, user studies); surveys existing systems and finds most evaluate only user experience.

**Evidence.** Survey/analysis; finds existing systems overwhelmingly evaluate user experience rather than the creativity of the collaboration or the artefact.

**For the studio.** Structures the evaluation plan: the studio should evaluate the *interaction* (annotation→compile turn-taking) and the *process*, not just final pieces.

<small>Tags: [evaluation] [co-creation-framework] [mixed-initiative] · Verification: verified (fetched arXiv abstract) · Clusters 05, 08</small>

### `colton2008tripod` — ColtonTripod — Creativity versus the perception of creativity in computational systems (the "creative tripod")

*Simon Colton, Imperial College London; AAAI Spring Symposium on Creative Intelligent Systems, 2008.*

Links: https://www.aaai.org/Papers/Symposia/Spring/2008/SS-08-03/SS08-03-003.pdf

A system is perceived as creative if it exhibits **skill, appreciation and imagination** (the tripod); emphasises framing/perception and later (Colton & Wiggins 2012; Colton, Charnley & Pease's FACE/IDEA) the need for systems to explain themselves.

**Evidence.** Conceptual; applied to The Painting Fool.

**For the studio.** "Appreciation" = the AI's ability to evaluate its own output against the composer's annotations — the missing leg in most generators and a design goal for the compiler.

<small>Tags: [evaluation] [co-creation-framework] · Verification: partial · Cluster 08</small>

## E6. Evaluation: music-theory competence benchmarks

### `weck2024muchomusic` — MuChoMusic — MuChoMusic: Evaluating Music Understanding in Multimodal Audio-Language Models

*Benno Weck, Ilaria Manco, Emmanouil Benetos, Elio Quinton, George Fazekas, Dmitry Bogdanov; UPF / QMUL / UMG; ISMIR 2024 (arXiv 2408.01337)*

Links: https://arxiv.org/abs/2408.01337 ; https://github.com/mulab-mir/muchomusic

1,187 human-validated multiple-choice questions on 644 tracks (from MusicCaps and Song Describer) covering knowledge (theory, instrumentation) and reasoning (cultural/functional context); evaluates five open audio-language models.

**Evidence.** Five open audio LLMs (e.g., MU-LLaMA, MusiLingo, SALMONN, Qwen-Audio, M2UGen) evaluated; finding: **over-reliance on the language modality**—models often answer without using the audio.

**For the studio.** Cautionary evidence: current audio LLMs cannot yet be trusted as automatic critics; a symbolic-first studio can instead ground critique in notation/MIR features.

<small>Tags: [evaluation] [LLM-agent] [multimodal-input] · Verification: verified · Clusters 04, 07, 08</small>

### `kumar2026howfar` — HowFarLLMs — How Far Can Pretrained LLMs Go in Symbolic Music? Controlled Comparisons of Supervised and Preference-based Adaptation

*Deepak Kumar, Emmanouil Karystinaios, Gerhard Widmer, Markus Schedl (JKU Linz); NLP4MusA 2026 (arXiv Jan 2026)*

Links: https://arxiv.org/abs/2601.22764

Controlled comparison of off-the-shelf instruction-tuned LLMs vs. domain-adapted variants (SFT vs. preference optimisation/DPO) vs. a music-specialised baseline on ABC generation and understanding across several corpora, analysing the domain-adaptation vs. prior-preservation trade-off and how metrics disagree.

**Evidence.** Multiple corpora and metrics; shows adaptation choices materially change outcomes and that standard metrics behave idiosyncratically for music.

**For the studio.** Practical guidance for turning a general LLM into the studio's notation-literate assistant.

<small>Tags: [LLM-agent] [evaluation] [symbolic-generation] [notation] · Verification: verified (arXiv abstract fetched) · Cluster 03</small>

### `wei2024musictheory` — SynTheory — Do Music Generation Models Encode Music Theory?

*Megan Wei, Michael Freeman, Chris Donahue, Chen Sun; Brown + CMU. ISMIR 2024.*

Links: https://arxiv.org/abs/2410.00872 ; https://brown-palm.github.io/music-theory ; code: https://github.com/brown-palm/syntheory

SynTheory, a synthetic MIDI+audio dataset isolating tempo, time signature, notes, intervals, scales, chords and progressions; probes Jukebox and MusicGen representations layer-by-layer for these concepts.

**Evidence.** Theory concepts are linearly detectable; detectability varies by model size and layer.

**For the studio.** A method to check whether a chosen backbone "understands" the symbolic concepts the composer annotates with.

<small>Tags: [theory-analysis] [evaluation] [dataset] [representation] · Verification: verified (arXiv page) · Cluster 02</small>

### `li2024ziqieval` — SymbolicLLMBenchmarks — ZIQI-Eval; ABC-Eval; (WildScore)

*ZIQI-Eval: Jiajia Li, Lu Yang, Mingni Tang, et al. (Wuhan University / SJTU / Shenyang Conservatory), arXiv Jun 2024 (reported as ACL 2024 Findings — venue not confirmed from a primary source). ABC-Eval: Jiahao Zhao, Yunjia Li, Wei Li, Kazuyoshi Yoshii (Kyoto University / Fudan), arXiv Sep 2025. WildScore: Gagan Mundada, Yash Vishe, Amit Namburi, et al. (UC San Diego), arXiv Sep 2025.*

Links: https://arxiv.org/abs/2406.15885 ; https://github.com/zcli-charlie/ZIQI-Eval ; https://arxiv.org/abs/2509.23350 ; https://arxiv.org/abs/2509.04744

ZIQI-Eval: >14,000 questions across 10 categories / 56 sub-categories of music knowledge (theory, history, instruments, symbolic tasks) for text LLMs. ABC-Eval: 1,086 items over 10 sub-tasks on ABC scores from syntax to segment- and sequence-level understanding and instruction following. WildScore: in-the-wild multimodal reasoning over *score images* with real user questions (belongs primarily to the multimodal cluster). Also MusicTheoryBench (ChatMusician).

**Evidence.** ZIQI-Eval: all 16 LLMs "poor". ABC-Eval: 7 LLMs incl. GPT-5/Gemini/DeepSeek score >90% on syntax but near random on sequence-level tasks (e.g., emotion). WildScore: mixed strengths and clear gaps.

**For the studio.** Quantifies where an LLM orchestrator can and cannot be trusted with notation; motivates specialised models plus verification (unit tests, constraints).

<small>Tags: [evaluation] [LLM-agent] [notation] [theory-analysis] · Verification: verified (arXiv abstracts/PDFs fetched) · Cluster 03</small>

## B1. Substrate: notation engines & editors

### `soundslice2026` — Soundslice — web notation + audio/video sync platform and API

*Adrian Holovaty (Chicago), 2012–*

Links: https://www.soundslice.com ; https://www.soundslice.com/help/data-api/

Browser player/editor where notation (MusicXML, Guitar Pro, PowerTab, TuxGuitar upload; PDF/image scanning via web UI) is synchronised to recordings (YouTube/Vimeo/MP3/video) through *syncpoints*; loop/slow-down/transpose for practice. Data API (Teacher/Licensing plans only; HTTP Basic auth) covers slices, notation upload/download & MusicXML export, recordings, syncpoints, lists; embed API for players. In 2025 Holovaty added ASCII-tab import after ChatGPT repeatedly hallucinated that Soundslice supported it (widely reported).

**Evidence.** Commercial, closed; strong UX benchmark for notation↔audio alignment.

**For the studio.** The best worked example of aligning symbolic notation to reference audio — directly relevant to "insert example audio" annotations and rendering feedback loops.

<small>Tags: [product] [notation] [education] [multimodal-input] · Verification: verified (API docs fetched) · Cluster 07</small>

### `osmd2026` — OSMD — OpenSheetMusicDisplay

*Andrea Zanchi (PhonicScore, Vienna) and contributors; 2016–; v2.0.0 June 2026*

Links: https://github.com/opensheetmusicdisplay/opensheetmusicdisplay ; https://opensheetmusicdisplay.org

TypeScript MusicXML renderer for browser/Node built on VexFlow; BSD-3-Clause. Parses MusicXML into an internal graphical model and lays out systems automatically; a renderer, not an editor. Sponsor-only extras (OSMD Audio Player, React Native/iOS/Android examples). Documented gaps: some pedal marks, tremolo between notes, cross-staff slurs.

**Evidence.** De-facto choice for MusicXML display in web music-ed apps; version 2.0 (2026) is the first major since 1.x.

**For the studio.** Fast path to displaying MusicXML from any notation app; pair with cursor/playback for score-following. For annotation depth, Verovio/MEI is stronger.

<small>Tags: [notation] [toolkit] · Verification: verified · Cluster 07</small>

### `avid2026sibelius` — Sibelius2026 — Sibelius (Avid) 2025–2026 releases

*Avid; monthly/quarterly releases (2025.12, 2026.02).*

Links: https://www.avid.com/resource-center/sibelius-february-2026-release

[S] Feb 2026: dark/light themes, engraving rules, ManuScript scripting extensions, crash fixes; **no AI features**. A rumoured "Sibelius AI" could not be confirmed in any Avid release note through Feb 2026.

**For the studio.** Confirms takeaway 4.

<small>Tags: [product] [notation] · Verification: verified (absence) · Cluster 08</small>

### `alphatab2026` — alphaTab — cross-platform notation/tablature rendering with built-in synth

*Daniel Kuschny (CoderLine); v1.8.3 May 2026*

Links: https://github.com/CoderLine/alphaTab ; https://alphatab.net

MPL-2.0 TypeScript library (also .NET and Kotlin/Android builds) that renders Guitar Pro 3–7, alphaTex, and MusicXML to SVG/raster and plays them back via its own MIDI + SoundFont2 synthesizer (alphaSynth) through Web Audio, with cursor/score sync and tempo control.

**Evidence.** 1.7k stars; one of the few OSS engines shipping notation + synchronised synth playback in one package.

**For the studio.** Reference architecture for "score + playback + cursor" in the browser; guitar/tab focus is complementary to piano-centric tools.

<small>Tags: [notation] [toolkit] [real-time] · Verification: verified · Cluster 07</small>

### `flat2026` — Flat.io / Noteflight — cloud notation editors with APIs

*Flat (Tutteo, Paris, 2015–); Noteflight (Hal Leonard, 2008–)*

Links: https://flat.io/developers

Flat: collaborative browser notation editor with REST API, Embed JS API (render/play/edit scores in your page), and "Edit on Flat" import API; MusicXML/MIDI import-export; Flat for Education. Noteflight: browser editor with Noteflight Learn (education), audio-recording assessment; API less open (partial).

**Evidence.** Commercial; widely adopted in schools.

**For the studio.** Demonstrates embeddable editable notation as a service; the studio could either embed or, more consistently with its open ethos, build on Verovio/OSMD.

<small>Tags: [product] [notation] [education] · Verification: partial (Flat page fetched; Noteflight recalled) · Cluster 07</small>

### `lilypond2026` — LilyPond — LilyPond music engraving program

*Han-Wen Nienhuys, Jan Nieuwenhuizen (1996–) and community; v2.26.0 stable 21 Apr 2026; 2.27.x dev*

Links: https://lilypond.org ; https://gitlab.com/lilypond/lilypond

GPL text-based engraver (`.ly` language, Scheme-extensible) producing PDF/SVG/MIDI; batch, not interactive. 2.26 consolidates changes since Oct 2022 branch (Guile 3, Cairo backend work). Used as the render backend by music21, Frescobaldi, Denemo.

**Evidence.** Long regarded as the engraving-quality benchmark for OSS.

**For the studio.** A "music as code" ancestor: score-as-program compiled to notation — literally the founder's compile metaphor. Slow (seconds per page) so suited to final export, not live editing.

<small>Tags: [notation] [music-as-code] [toolkit] [history] · Verification: verified · Cluster 07</small>

### `pugin2014verovio` — MEI-Verovio — MEI (Music Encoding Initiative) and Verovio

*MEI community (Board, Technical Team; Music Encoding Conference), current MEI 5; hosted since 2026 by Akademie der Wissenschaften und Literatur Mainz and RISM Digital Center Bern. Verovio: Laurent Pugin, Rodolfo Zitellini (Swiss RISM), Perry Roland (U. Virginia); ISMIR 2014.*

Links: https://music-encoding.org/ ; https://www.verovio.org ; paper https://archives.ismir.net/ismir2014/paper/000221.pdf ; https://github.com/rism-digital/verovio

MEI is an XML encoding for the full history of Western notation with rich *editorial* markup (readings, corrections, supplied text, genetic/revision layers) and links to facsimiles and audio; Educational Community License 2.0. Verovio engraves MEI to SVG in which every graphical element is an addressable XML element with MEI ids, enabling in-browser interactive scores (also accepts MusicXML, Humdrum, ABC, PAE); open source (LGPL).

**Evidence.** De facto standard in digital musicology editions; Verovio powers mei-friend, Dezrann visualisation, Foscarin's diff viewer, etc.

**For the studio.** The best open-source route to an in-browser, engraving-quality, *annotatable* score: MEI supports editorial/analytical layers and every rendered glyph carries an ID, enabling scribble/sketch overlays and click-to-annotate tied to symbolic elements.

<small>Tags: [representation] [notation] [annotation] [toolkit] · Verification: verified (fetched primary sources) · Clusters 06, 07</small>

### `vexflow2024` — VexFlow — VexFlow music notation rendering library

*Mohit Muthanna Cheppudira (2010–) and contributors; v4.2.6 Aug 2024 stable; VexFlow 5 in development at github.com/vexflow/vexflow*

Links: https://github.com/0xfe/vexflow ; https://vexflow.com

MIT-licensed TypeScript library rendering notation and tablature to SVG/Canvas; low-level (you place staves/voices) with EasyScore text API (`score.notes('C#5/q, B4')`). Used by OSMD, Flat (historically), many ed-tech apps.

**Evidence.** 4.3k stars; long-lived; no automatic system/page layout — that is what OSMD adds.

**For the studio.** The building block for custom, non-standard views (e.g., sketch overlays, partial fragments, lead-sheet chord grids) where a full-score engraver is overkill.

<small>Tags: [notation] [toolkit] · Verification: verified · Cluster 07</small>

### `musegroup2025musescore46` — MuseScore46 — MuseScore Studio 4.6 / 4.7 + Muse Hub (Muse Group)

*Muse Group (Martin Keary product lead); 4.5 (Mar 2025), 4.6 (30 Sept 2025), 4.7 (2026); open-source (GPLv3).*

Links: https://musescore.org/en/4.6 ; https://github.com/musescore/MuseScore

[S] Free notation editor with Muse Sounds orchestral playback via Muse Hub; 4.6 added percussion panel, guitar techniques, fretboard auto-fill from chord symbols, MusicXML improvements; planned **Cantai** AI choir integration (delayed). No generative composition features. Also hosts musescore.com score-sharing (source of PDMX public-domain subset).

**For the studio.** The obvious open-source engraving/playback substrate (or fork target) for a notation-first studio; also the community whose scores feed licence-clean datasets.

<small>Tags: [product] [notation] [toolkit] · Verification: verified · Cluster 08</small>

### `musescore2026studio` — MuseScore Studio 4.x — open-source notation editor (Muse Group)

*Muse Group (Martin Keary, Tantacrul; Peter Jonas et al.); 4.5 Feb 2025, 4.6 30 Sep 2025, 4.7.x 2026; MuseScore Studio 5 development started Dec 2025*

Links: https://musescore.org/en/4.6 ; https://musescore.org/en/4.7.4 ; https://musescore.org/en/4.5-and-beyond ; https://github.com/musescore/MuseScore

GPL-3 notation editor (C++/Qt 6.9) with MuseSounds sample libraries (free, distributed via the proprietary Muse Hub app), VST3 hosting, MusicXML/MIDI import-export, and a QML plugin API (updated in 4.6 to expose all elements/properties added since 4.0; a replacement "extensions framework" was announced then deferred). 4.6: any SMuFL font, realtime MIDI note preview with duration/velocity, guitar techniques, TablEdit import. 4.7 (2026): engraving tools, audio-engine upgrades, and a File-menu shortcut to an online **MP3→MSCZ converter (beta)** — Muse Group's first shipped audio-to-score AI feature. Roadmap for 5.0: DAW-like automation, piano-roll, audio staves with time-stretch, MIDI mapping.

**Evidence.** Most-used free notation software; musescore.com hosts millions of user scores (see PDMX / scraping entries).

**For the studio.** The obvious open editor to interoperate with (MSCZ/MusicXML), and its 5.0 direction (notation+DAW hybrid) overlaps the studio's; the limited, read-mostly plugin API is a known pain point.

<small>Tags: [notation] [product] [toolkit] [DAW-plugin] · Verification: verified · Cluster 07</small>

### `abcjs2026` — abcjs — ABC notation renderer and player

*Paul Rosen; v6.6.3 Apr 2026*

Links: https://github.com/paulrosen/abcjs ; https://abcjs.net

JavaScript library rendering ABC text to SVG, with editor live-rendering, transposition, tablature, chord grids, and Web Audio playback via soundfonts. MIT license (partial: fetched page did not confirm license text).

**Evidence.** 2.3k stars; the standard for ABC-on-the-web; ABC is also the notation LLMs (ChatMusician, MuPT) generate most fluently.

**For the studio.** Cheapest text↔notation round trip — an LLM can emit ABC and the user sees/edits notation instantly; ideal for lead-sheet-level "compile" drafts.

<small>Tags: [notation] [toolkit] [music-as-code] · Verification: verified (license partial) · Cluster 07</small>

### `steinberg2025dorico6` — Dorico6 — Dorico 6 (Steinberg)

*Steinberg (Daniel Spreadbury et al.), released 30 Apr 2025; $99 update, Finale/Sibelius crossgrade.*

Links: https://blog.dorico.com/2025/04/dorico-6-released/

[S] Notation: new **Proofreading panel** (flags meter/marking/instrument-change problems), cutaway scores, chord-symbol customisation, engraving rulers/grid, condensing, Fill view. **No generative/ML features.** Existing "Generate notes from chord symbols"/"Generate chord symbols from selection" are rule-based.

**For the studio.** Now the professional engraving reference (post-Finale); a natural export target (MusicXML/Dorico) and evidence that the notation market has *no* AI composition assistant.

<small>Tags: [product] [notation] · Verification: verified · Cluster 08</small>

### `cheppudira2010vexflow` — WebRenderers — OpenSheetMusicDisplay, VexFlow, alphaTab (browser notation rendering)

*VexFlow: Mohit Muthanna Cheppudira (2010–; MIT; v4.2.6 Aug 2024, v5 in development). OSMD: Phonicscore GmbH, Vienna (BSD-3). alphaTab: Daniel Kuschny (MPL-2.0; Guitar Pro/MusicXML/alphaTex).*

Links: https://github.com/0xfe/vexflow ; https://github.com/opensheetmusicdisplay/opensheetmusicdisplay ; https://www.alphatab.net

VexFlow: low-level JS engraving to SVG/Canvas with the EasyScore API. OSMD: MusicXML → VexFlow renderer for browser/Node (SVG/PNG, cursor, transposition, tablature; explicitly "a renderer, not an editor"; playback in early access). alphaTab: renders tablature/notation from Guitar Pro, MusicXML and its own alphaTex text language with synth playback.

**Evidence.** Widely deployed OSS.

**For the studio.** The practical component options for a web-based score surface: Verovio (MEI-native, ids) vs OSMD/VexFlow (MusicXML-native) vs abcjs (ABC-native); choice couples to the IR decision.

<small>Tags: [toolkit] [notation] · Verification: verified (VexFlow, OSMD fetched; alphaTab partial) · Cluster 06</small>

## B2. Substrate: symbolic toolkits

### `cancinochacon2022partitura` — partitura — Python package for symbolic music processing (score–performance)

*Carlos Cancino-Chacón, Silvan Peter, Emmanouil Karystinaios, Francesco Foscarin, Maarten Grachten, Gerhard Widmer; JKU Linz; ISMIR 2019 LBD, MEC 2022; v1.9.0 May 2026*

Links: https://github.com/CPJKU/partitura ; https://partitura.readthedocs.io

Apache-2.0 library parsing MusicXML, MEI, Humdrum **kern, MIDI into a `Score` with structured note arrays; performance MIDI handling; score–performance alignment (Match files); performance-feature extraction; export to MIDI/MusicXML/WAV. Basis of JKU's expressive-performance (Basis Mixer), score-following (ACCompanion) and GNN analysis (ChordGNN, cadence detection) work.

**Evidence.** ERC "Whither Music?" funded; actively released through 2026.

**For the studio.** The toolkit for linking notation to human performances (e.g., the founder playing a passage on the Nord as an annotation of how a phrase should feel).

<small>Tags: [toolkit] [representation] [expression-performance] [notation] · Verification: verified · Cluster 07</small>

### `cuthbert2010music21` — music21 — music21: A Toolkit for Computer-Aided Musicology (Cuthbert)

*Euterpea/HSoM: Paul Hudak & Donya Quick, Yale; *The Haskell School of Music* (Cambridge UP, 2018); development concluded. Alda: Dave Yarwood, 2012– (EPL-2.0). music21: Michael Scott Asato Cuthbert, MIT, 2006– (BSD-3; v10.5.0 June 2026; Cuthbert & Ariza, ISMIR 2010).*

Links: https://github.com/cuthbertLab/music21 ; docs: https://www.music21.org/music21docs/ ; corpus list: https://www.music21.org/music21docs/about/referenceCorpus.html ; module: https://www.music21.org/music21docs/moduleReference/moduleCorpusChorales.html

Python toolkit "for computer-aided musical analysis and computational musicology." Parses MusicXML, MIDI, ABC, Humdrum **kern, MEI, Noteworthy, Capella etc. into a hierarchical `Stream` object model (Score → Part → Measure → Note/Chord/etc.) and writes MusicXML, MIDI, LilyPond (PNG/PDF), braille, and text; opens scores in MuseScore/Finale. Analysis: key finding (Krumhansl-Schmuckler et al.), `roman.romanNumeralFromChord`/`RomanNumeral`, chord identification, intervals, voice-leading, meter/beat-strength, feature extraction (jSymbolic/native), search/similarity, serial matrices, plotting. Bundled corpus (BSD code; scores public domain or by permission): all Bach chorales (371 Riemenschneider, addressable via `corpus.chorales.Iterator` by Riemenschneider/BWV/Kalmus/Budapest/Bärenreiter numbering or title), Bach cantatas/organ works, Palestrina (200+ mass movements), Monteverdi madrigals (books 3–5), Beethoven/Haydn/Mozart quartets, Essen folksong (ABC), O'Neill's 1,800+ Irish tunes, Aird's Airs, Josquin, Schubert, Schumann, Joplin, Webern, trecento music, theory exercises. License BSD-3-clause; Python ≥3.12; ~2.5k GitHub stars.

**Evidence.** Widely used in computational musicology; known limitations: pure-Python speed (parsing thousands of scores is slow — symusic benchmarks report 100×+ speedups on MIDI), MusicXML round-trip preserves pitch/rhythm/spanners well but not full layout; MEI export absent.

**For the studio.** The symbolic layer's parser/analyzer/exporter: read the composer's MusicXML, annotate with Roman numerals and keys, search corpora for exemplars, emit MusicXML/MIDI/LilyPond after the AI compiles. Its corpus is also training/evaluation data.

<small>Tags: [toolkit] [notation] [representation] [theory-analysis] [corpus] [music-as-code] · Verification: verified (GitHub README, docs pages fetched); ISMIR 2010 citation partial · Clusters 01, 06, 07</small>

### `roberts2018magentajs` — MagentaJS — Magenta.js: A JavaScript Library for Music Generation (and the Magenta ecosystem)

*Google Magenta (Adam Roberts, Curtis Hawthorne, Monica Dinculescu et al.); \@magenta/music 1.x (2018–2021), Apache-2.0; MIDI-DDSP (Yusong Wu et al., ICLR 2022)*

Links: https://github.com/magenta/magenta-js ; https://github.com/magenta/midi-ddsp ; https://magenta.github.io/magenta-js/music/demos/

TypeScript/TensorFlow.js packages running MusicVAE, MelodyRNN, DrumsRNN, PerformanceRNN, ImprovRNN (plus Onsets&Frames, Piano Genie, GANSynth, DDSP in later releases) in the browser; MIDI-DDSP renders MIDI to expressive monophonic instrument audio with note-level expression controls (Colab demo; no maintained browser build). Magenta.js has no recent releases — effectively frozen; Magenta's active work moved to Magenta RealTime (2025, audio).

**Evidence.** Demos powered many 2018–2021 co-creation prototypes (e.g., Bach Doodle used Coconet in TF.js).

**For the studio.** If the studio has a web front end, magenta-js and the NoteSequence schema are ready-made pieces for symbolic in-browser inference and interchange.

<small>Tags: [toolkit] [symbolic-generation] [expression-performance] [history] · Verification: verified (magenta-js README); MIDI-DDSP partial · Clusters 01, 07</small>

### `dong2020muspy` — MusPy — a toolkit for symbolic music generation

*Hao-Wen Dong, Ke Chen, Julian McAuley, Taylor Berg-Kirkpatrick; UC San Diego; ISMIR 2020; v0.5.0 Apr 2022*

Links: https://github.com/salu133445/muspy ; https://arxiv.org/abs/2008.01951

MIT Python library unifying dataset download/management (Lakh, MAESTRO, NES-MDB, JSB, Nottingham, Essen, Wikifonia…), I/O (MIDI, MusicXML, ABC, note-seq, pretty_midi, music21), representations (pitch, event, piano-roll, note) and objective metrics (pitch-class entropy, scale consistency, groove consistency) plus rendering via FluidSynth.

**Evidence.** ISMIR 2020 paper includes a cross-dataset generalisation study; maintenance slowed after 2022.

**For the studio.** Blueprint for a dataset/representation abstraction layer and for objective metrics in an evaluation harness.

<small>Tags: [toolkit] [dataset] [evaluation] [representation] · Verification: verified · Cluster 07</small>

### `fradet2021miditok` — MidiTok — MidiTok: A Python package for MIDI file tokenization

*Nathan Fradet, Jean-Pierre Briot, Fabien Chhel, Amal El Fallah Seghrouchni, Nicolas Gutowski (Sorbonne / Aubay); ISMIR 2021 Late-Breaking Demo; extended arXiv 2023 (2310.17202); v3.0.6 (July 2025)*

Links: https://github.com/Natooz/MidiTok ; docs: https://miditok.readthedocs.io ; https://archives.ismir.net/ismir2021/latebreaking/000005.pdf ; https://arxiv.org/abs/2310.17202

MIT-licensed library implementing REMI, REMI+, MIDI-Like, TSD, Structured, CPWord, Octuple, MuMIDI, MMM and PerTok tokenizers behind one API, with BPE/Unigram/WordPiece sub-word training (via HF tokenizers), data augmentation, PyTorch Dataset/Collator utilities and Hugging Face Hub integration.

**Evidence.** Standard tokeniser in symbolic-generation papers 2022–2026; companion paper "Byte Pair Encoding for Symbolic Music" (Fradet et al., EMNLP 2023).

**For the studio.** Any in-house symbolic model (infill, continuation, arrangement) will need a tokeniser; MidiTok is the interoperable default and its MMM/bar-infilling tokenisations map directly onto region-scoped editing.

<small>Tags: [toolkit] [representation] [symbolic-generation] · Verification: verified (GitHub README fetched) · Clusters 03, 07</small>

### `liao2024symusic` — symusic — a swift and unified toolkit for symbolic music processing

*Yikai Liao, Zhongqi Luo et al.; ISMIR 2024 Late-Breaking Demo; v0.5–0.6 2025–26*

Links: https://github.com/Yikai-Liao/symusic ; https://symusic.readthedocs.io

C++20 core with nanobind Python bindings; loads/saves MIDI and ABC; tick/quarter/second time units; vectorised transforms (shift pitch/time/velocity, filter), piano-roll extraction, NumPy/pickle serialisation, SoundFont synthesis via prestosynth. MIT.

**Evidence.** Benchmarks show parsing "hundreds of times faster" than mido/pretty_midi/miditoolkit; adopted as MidiTok's I/O backend.

**For the studio.** The performance backbone for corpus-scale preprocessing and low-latency in-app MIDI manipulation.

<small>Tags: [toolkit] [representation] · Verification: verified · Cluster 07</small>

### `wu2024muskitsespnet` — MuskitsESPnet — Muskits-ESPnet: A Comprehensive Toolkit for Singing Voice Synthesis in New Paradigm

*Yuning Wu, Jiatong Shi, et al., Shinji Watanabe, Qin Jin; CMU WAVLab + Renmin University. ACM Multimedia 2024 (open-source software track); successor to Muskits (Interspeech 2022).*

Links: https://arxiv.org/abs/2409.07226 ; https://doi.org/10.1145/3664647.3685000 ; code: https://github.com/espnet/espnet

ESPnet-based singing-voice-synthesis toolkit: score/lyrics → singing, with continuous (SSL) and discrete (codec) pretrained-audio paradigms, multiple score input formats, **automatic music-score correction**, and perception-based auto-evaluation. Watanabe's group otherwise touches music mainly through co-authorship (Music ControlNet, Music Arena, MAD) and the Sony collaboration. Note: **MuQ** (self-supervised music representation with Mel-RVQ, TASLP 2025) is Tencent AI Lab / SJTU, *not* CMU.

**Evidence.** Toolkit paper; recipes/benchmarks rather than user studies.

**For the studio.** The open-source path from a symbolic vocal line + lyrics to a rendered vocal — the "render this part" compile step for voice.

<small>Tags: [toolkit] [audio-generation] [notation] [transcription] · Verification: partial (arXiv abstract fetched; author list from recall/search snippet) · Cluster 02</small>

### `raffel2014prettymidi` — mido / pretty_midi / miditoolkit / note-seq — legacy Python MIDI stack

*mido (Ole Martin Bjørndalen, 2013–, MIT); pretty_midi (Colin Raffel & Daniel Ellis, ISMIR 2014 LBD, MIT); miditoolkit (Yu-Siang Huang, 2020, MIT; tick-based, used by REMI/Compound Word); note-seq (Google Magenta, Apache-2.0) with the `NoteSequence` protobuf (music.proto) used across Magenta models*

Links: https://github.com/mido/mido ; https://github.com/craffel/pretty-midi ; https://github.com/YatingMusic/miditoolkit ; https://github.com/magenta/note-seq/blob/main/note_seq/protobuf/music.proto

mido = message-level MIDI I/O and real-time ports (rtmidi); pretty_midi = note-level, seconds-based API with tempo-map handling and FluidSynth rendering; miditoolkit = tick-preserving alternative; NoteSequence = language-neutral protobuf schema (notes, tempos, time signatures, pitch bends, control changes) with quantisation utilities.

**Evidence.** Still the most common dependencies in MIR code; symusic now outperforms them but exposes compatible concepts.

**For the studio.** Interop requirement — most public checkpoints and datasets are read with these; NoteSequence is a proven serialisation design for an internal symbolic IR.

<small>Tags: [toolkit] [representation] · Verification: partial (recalled; note-seq proto URL confirmed by search snippet) · Cluster 07</small>

## B3. Substrate: runtime & integration

### `roberts2019magentastudio` — MagentaStudio — Magenta Studio: Augmenting Creativity with Deep Learning in Ableton Live

*Adam Roberts, Jesse Engel, Yotam Mann, Jon Gillick, Claire Kayacik, Signe Nørly, Monica Dinculescu, Carey Radebaugh, Curtis Hawthorne, Douglas Eck; Google Brain (Magenta); MUME workshop 2019; v2.0 as Ableton Live 10.1+ Max-for-Live device*

Links: https://magenta.tensorflow.org/studio ; https://research.google/pubs/magenta-studio-augmenting-creativity-with-deep-learning-in-ableton-live/ ; https://github.com/magenta

Five DAW-plugin tools wrapping Magenta models: Continue (RNN continues a melody/drum clip up to 32 bars), Generate (MusicVAE 4-bar phrases), Interpolate (MusicVAE, up to 16 clips between two), Groove (GrooVAE humanizes drum timing/velocity, trained on ~15 h of drummer recordings), Drumify (GrooVAE turns any rhythm into a drum groove). Inputs/outputs are MIDI clips in Live; controls are temperature, variation count and clip selection.

**Evidence.** No formal user study in the paper; adoption/feedback informal. Demonstrated that in-DAW clip-level AI tools are feasible for mainstream producers.

**For the studio.** The reference example of generative tools packaged as *small, composable DAW operations* on user clips rather than a text-to-song box; the exact "operate on my material" granularity the founder wants.

<small>Tags: [DAW-plugin] [product] [symbolic-generation] [editing] [toolkit] · Verification: verified (official page fetched); workshop-paper citation partial · Clusters 01, 05</small>

### `clavia2023nordstage4` — Nord Stage (MIDI implementation basics)

*Clavia (Stockholm); Nord Stage 4 (2023) is current — a "Nord Stage 6" does not exist as of Sept 2026 (not verified; the founder's instrument is likely a Stage 3 or 4)*

Links: https://www.nordkeyboards.com/products/nord-stage-4 (manual PDF lists MIDI implementation)

Stage 3/4 transmit on a global MIDI channel with per-section (Organ/Piano/Synth) channels optionally, Program Change/Bank Select for program selection, CC for panel controls, and USB-MIDI class-compliant output — i.e., trivially usable as a Web MIDI input device in Chromium.

**Evidence.** Not re-fetched.

**For the studio.** Confirms the "hum/play it in" annotation path is a plain MIDI input problem; program-change mapping can select studio sounds from the keyboard.

<small>Tags: [product] [real-time] · Verification: unverified (recall) · Cluster 07</small>

### `metacreation2023mmm4live` — MMM4Live — MMM4Live: Multi-Track Music Machine for Ableton Live

*Metacreation Lab (Philippe Pasquier, Jeff Ens, Renaud Bougueng Tchemeube et al.), Simon Fraser University; Max-for-Live device, beta 2023–2024*

Links: https://www.metacreation.net/projects/mmm4live ; https://cycling74.com/projects/mmm4live

Ableton Live device that generates or continues multi-track MIDI clips (4- or 16-bar templates) with the MMM Transformer, conditioning new tracks on existing ones, with "fine control of iterative resampling"; runs locally on macOS.

**Evidence.** Closed beta; documentation v0.1b2; no published study yet.

**For the studio.** Shows the Metacreation lineage moving from web to in-DAW; useful comparator for a symbolic compiler plugin.

<small>Tags: [DAW-plugin] [symbolic-generation] [product] · Verification: verified (fetched project page) · Cluster 05</small>

### `tchemeube2022calliope` — Calliope — Calliope: A Co-creative Interface for Multi-Track Music Generation (and Apollo)

*Renaud Bougueng Tchemeube, Jeff Ens, Philippe Pasquier; Metacreation Lab, Simon Fraser University; ACM Creativity & Cognition 2022 and ICCC 2022 (Apollo: ICCC 2019)*

Links: https://doi.org/10.1145/3527927.3535200 ; https://arxiv.org/abs/2504.14058 ; https://metacreation.net/calliope ; Apollo https://arxiv.org/abs/2504.14055

Web app over the Multi-Track Music Machine (MMM, Transformer trained on ~500k MIDI files): upload MIDI, view piano roll, select bars/tracks for *infilling* or generate full multi-track material, batch-generate up to 1,000 candidates and rank them; global controls (temperature, polyphony limit, % preservation, tracks/bars per step) and per-track controls (128 GM instruments, note density 0–10, polyphony range, duration range). Apollo (2019) is the earlier corpus-based style-imitation environment.

**Evidence.** System paper; the human-factors evaluation appeared as MMM-C (below).

**For the studio.** Demonstrates the *attribute-controlled bar/track infilling + batch alternatives + ranking* workflow on symbolic multi-track material — the natural implementation of "compile the parts I annotated."

<small>Tags: [symbolic-generation] [infilling] [controllability] [DAW-plugin] [toolkit] · Verification: verified (fetched ICCC 2022 PDF) · Cluster 05</small>

### `ahuja2025abletonmcp` — AbletonMCP — Ableton MCP (LLM → Ableton Live bridge) and the LLM-agent-in-DAW wave

*Siddharth Ahuja (ahujasid), open-source, Mar 2025; many forks (jpoindexter 200+ tools; LofiFren; itsuzef); parallel projects for Logic/REAPER/Bitwig/FL via MCP or OSC.*

Links: https://github.com/ahujasid/ableton-mcp

[S][I] MIT-licensed MCP server + Ableton Remote Script over a socket; Claude/other LLMs create tracks, MIDI clips and notes, load instruments/effects, set tempo/playback, and build arrangements in Arrangement View from natural-language instructions. ~3k GitHub stars. Limitations noted by author: complex arrangements must be chunked; default devices only.

**Evidence.** Community demos; no formal study.

**For the studio.** Proof of demand for *conversational control of a DAW* and a reusable pattern (tool-calling agent → structured music edits). Cross-ref LLM-agent cluster.

<small>Tags: [product] [LLM-agent] [DAW-plugin] [symbolic-generation] [toolkit] · Verification: verified · Cluster 08</small>

### `clap2022` — DAW integration protocols — VST3, CLAP, AU, ReaScript, Ableton Link, Max for Live

*VST3 (Steinberg, SDK dual GPLv3/proprietary); CLAP (u-he + Bitwig, announced June 2022, MIT, C ABI); Audio Units (Apple); ReaScript (Cockos REAPER: Lua/EEL2/Python scripting of the DAW); Ableton Link (Ableton, 2016, GPLv2+ with commercial option; tempo/beat/phase sync over LAN); Max for Live (Cycling '74/Ableton)*

Links: https://github.com/free-audio/clap ; https://github.com/Ableton/link ; https://www.reaper.fm/sdk/reascript/reascript.php ; https://steinbergmedia.github.io/vst3_dev_portal/

Plugin ABIs let a studio "compiler" appear inside a DAW as an instrument/MIDI-effect; CLAP is the permissively-licensed, extension-based alternative to VST3 with per-note modulation and thread-pool hosting, supported by Bitwig, REAPER, FL Studio, MultitrackStudio and via NIH-plug/iPlug2/JUCE 8. ReaScript enables scripted manipulation of REAPER projects (used by many MIR/AI bridges). Link syncs tempo across apps — an easy way to keep a browser studio in time with Ableton Live.

**Evidence.** CLAP README (fetched) confirms stable 1.x ABI and MIT; adoption details recalled.

**For the studio.** Composers live in DAWs; a CLAP/VST3 bridge plus Link keeps the studio a co-creator inside existing workflows rather than another island.

<small>Tags: [DAW-plugin] [toolkit] [real-time] · Verification: partial (CLAP verified; others recalled) · Cluster 07</small>

### `w3c2026webmidi` — Web MIDI + Web Audio + Tone.js — browser audio/MIDI substrate (status 2026)

*W3C Web MIDI API (Working Draft; Chris Wilson et al.); Web Audio API (W3C Recommendation 2021); Tone.js by Yotam Mann (2014–), MIT*

Links: https://caniuse.com/midi ; https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API ; https://github.com/Tonejs/Tone.js

Web MIDI support: Chrome 43+, Edge 79+, Opera 30+, Samsung Internet, Firefox 108+ (via site-permission add-on); **Safari desktop and iOS: unsupported, no roadmap** (Apple cites fingerprinting). Web Audio API is universal; AudioWorklet enables sample-accurate DSP/WASM synths. Tone.js provides DAW-like Transport, scheduling, synths, effects, Sampler (npm v15.x 2024; GitHub release tags lag).

**Evidence.** caniuse global support ~81%; the Safari gap is the single biggest platform risk for a web-first studio taking live keyboard input.

**For the studio.** Determines architecture: web UI for notation/annotation, but MIDI-controller input (Nord Stage) needs Chromium or a desktop wrapper; Tone.js is the natural playback/transport layer.

<small>Tags: [toolkit] [real-time] · Verification: verified (caniuse, Tone.js repo); Tone.js version partial · Cluster 07</small>

### `zhou2024midinfinite` — MIDInfinite — Local Deployment of Large-Scale Music AI Models on Commodity Hardware

*Xun Zhou, Charlie Ruan, Zihe Zhao, Tianqi Chen, Chris Donahue; CMU. ISMIR 2024 LBD.*

Links: https://arxiv.org/abs/2411.09625 ; demo: https://rickzx.github.io/inf-music

Ports the Anticipatory Music Transformer to the browser via MLC (WebGPU); infinite MIDI stream demo.

**Evidence.** 51 notes/s on an M3 MacBook Pro; faster than playback 72.9% of the time, 86.3% with 2-s buffering.

**For the studio.** Proof that a symbolic infilling model can run client-side — relevant to an open-source studio's deployment story.

<small>Tags: [toolkit] [symbolic-generation] [real-time] · Verification: verified (arXiv page) · Cluster 02</small>

### `spessasynth2026` — Browser synthesis: spessasynth, FluidSynth-WASM, alphaSynth, SoundFont/SFZ

*spessasus (spessasynth_lib v4.3, Apache-2.0); FluidSynth (LGPL-2.1, 2002–; Emscripten ports e.g. js-synthesizer); SFZ format (rgc:audio 2002, open spec; sfizz LGPL/BSD player)*

Links: https://github.com/spessasus/spessasynth_lib ; https://github.com/spessasus/spessasynth_core ; https://www.fluidsynth.org ; https://sfzformat.com

spessasynth: pure TypeScript SF2/SF3/DLS/SFOGG synthesizer running in an AudioWorklet or Worker, MIDI file read/write/playback, offline render to WAV, soundbank editing — no WASM needed. FluidSynth: the reference SoundFont synth (C), used server-side and via WASM in browsers. SFZ: text-based sample-instrument format widely used for free orchestral libraries.

**Evidence.** spessasynth is actively maintained (2025–26); FluidSynth remains the standard for offline MIDI→audio rendering in research pipelines (used by symusic via prestosynth, MusPy).

**For the studio.** Enables immediate audition of symbolic output in-browser and headless rendering for evaluation; SF2/SFZ give a free, redistributable sound palette (GM soundfonts, Salamander piano, VSCO).

<small>Tags: [toolkit] [real-time] [audio-generation] · Verification: verified (spessasynth); FluidSynth/SFZ partial · Cluster 07</small>

## B4. Substrate: datasets & corpora

### `lev2024lamidi` — Los Angeles MIDI Dataset — ~405k deduplicated MIDIs

*Aleksandr Lev (asigalov61, "Project Los Angeles"); v4.0 2024*

Links: https://github.com/asigalov61/Los-Angeles-MIDI-Dataset ; HF `projectlosangeles/Los-Angeles-MIDI-Dataset`

~405,000 "read-checked, 100% de-duped" MIDI files aggregated from public sources, with metadata and per-file chord data plus search utilities; repo Apache-2.0 (underlying files' provenance unstated).

**Evidence.** Community dataset behind the author's many "Tegridy" MIDI models; no peer-reviewed paper.

**For the studio.** Quick, large, permissively-labelled multitrack data — but provenance is weaker than PDMX/Lakh; treat as research-only.

<small>Tags: [dataset] [ethics-legal] · Verification: verified (repo) · Cluster 07</small>

### `raffel2016lakh` — Lakh MIDI Dataset (LMD) — 176,581 unique MIDI files

*Colin Raffel; Columbia University; PhD thesis "Learning-Based Methods for Comparing Sequences…" 2016*

Links: https://colinraffel.com/projects/lmd/

176,581 deduplicated MIDI files scraped from the web; LMD-matched (45,129 files aligned to Million Song Dataset entries) and LMD-aligned subsets. License CC-BY 4.0 for the collection; the MIDI files are user transcriptions of copyrighted songs (legal grey zone for downstream commercial use).

**Evidence.** The most-used multitrack symbolic training set 2016–2024 (MuseGAN, MMM, MidiCaps, etc.); quality is very uneven (many files are GM karaoke-style).

**For the studio.** Primary source of multi-instrument arrangements for training/eval "compile" models; quality filtering essential.

<small>Tags: [dataset] [corpus] [ethics-legal] · Verification: partial (recalled; widely documented) · Cluster 07</small>

### `hawthorne2019maestro` — MAESTRO — MIDI and Audio Edited for Synchronous TRacks and Organization

*Curtis Hawthorne, Andriy Stasyuk, Adam Roberts et al.; Google Magenta; ICLR 2019 ("Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset"); v3.0.0 2021*

Links: https://magenta.tensorflow.org/datasets/maestro ; https://arxiv.org/abs/1810.12247

~200 hours, 1,276 performances from the International Piano-e-Competition (Yamaha Disklavier), audio + fine-aligned MIDI (~3 ms), composer/title metadata, train/val/test splits. License CC-BY-NC-SA 4.0.

**Evidence.** Standard benchmark for piano transcription (Onsets & Frames) and expressive piano generation (Music Transformer, Perceiver-AR).

**For the studio.** Gold standard for expressive performance MIDI; the NC license blocks use in a commercial product but not in a research-grade open studio.

<small>Tags: [dataset] [expression-performance] [transcription] · Verification: partial (recalled) · Cluster 07</small>

### `zhang2022atepp` — ATEPP — Automatically Transcribed Expressive Piano Performance

*Huan Zhang, Jingjing Tang, Syed Rifat Mahmud Rafee, Simon Dixon, George Fazekas; QMUL; ISMIR 2022; v1.2*

Links: https://github.com/tangjjbetsy/ATEPP

11,674 performances (~1,000 h) by 49 virtuoso pianists covering 1,595 movements by 25 composers, transcribed from commercial recordings; ~43% have aligned MusicXML scores; Composition Entity Linker for metadata. CC-BY 4.0.

**Evidence.** Designed for performer-identification and expressive-rendering studies (multiple performances per piece).

**For the studio.** Multiple interpretations of the same score = training signal for "render this passage *like this*" expression controls.

<small>Tags: [dataset] [expression-performance] [transcription] · Verification: verified · Cluster 07</small>

### `wang2020pop909` — JSB Chorales, Nottingham, POP909, Wikifonia — classic small symbolic sets

*JSB Chorales: 382 four-part Bach chorales (Boulanger-Lewandowski, Bengio, Vincent ICML 2012 splits; music21 corpus has 371+); Nottingham: ~1,200 British/American folk tunes with chords in ABC (Eric Foxley; Boulanger-Lewandowski 2012 MIDI version); POP909: 909 Chinese pop songs, piano arrangements (melody/bridge/piano tracks) + chord/beat/key annotations, ~60 h (Ziyu Wang, Ke Chen, Junyan Jiang et al., NYU Shanghai, ISMIR 2020); Wikifonia: ~6,000 lead sheets in MusicXML (site closed 2013 after publisher pressure; still circulates in research, not legally redistributable)*

Links: https://github.com/music-x-lab/POP909-Dataset ; https://abc.sourceforge.net/NMD/ ; music21 corpus

The standard "toy-to-medium" corpora for harmonisation (JSB), melody+chord modelling (Nottingham, Wikifonia), and pop arrangement/accompaniment (POP909). POP909 license: research/non-commercial (partial).

**Evidence.** JSB remains the canonical benchmark for voice-leading/harmonisation models (DeepBach, Coconet).

**For the studio.** Fast evaluation beds for harmonisation and lead-sheet→arrangement tasks; POP909's melody/accompaniment split is a direct analogue of "compile a piano part from a lead sheet."

<small>Tags: [dataset] [corpus] [accompaniment] · Verification: partial (recalled) · Cluster 07</small>

### `melechovsky2024midicaps` — MidiCaps — 168k MIDI files with text captions

*Jan Melechovsky, Abhinaba Roy, Dorien Herremans; SUTD Singapore; ISMIR 2024*

Links: https://arxiv.org/abs/2406.02255 ; HF `amaai-lab/MidiCaps`

>168,000 Lakh-derived MIDI files each with an LLM-generated caption built from extracted features (tempo, chords, time signature, instruments, genre, mood); listening study validated caption quality. Licence CC-BY-SA 4.0 (partial). Follow-ups: Text2midi (2024), symbolic captioning work 2025.

**Evidence.** "First openly available large-scale MIDI dataset with text captions."

**For the studio.** Enables text annotations ↔ symbolic mapping (e.g., "make the bridge darker") for training or retrieval.

<small>Tags: [dataset] [text-conditioning] [annotation] · Verification: verified (abstract); licence partial · Cluster 07</small>

### `ens2021metamidi` — MetaMIDI Dataset (MMD) — 436,631 MIDI files with audio/metadata matches

*Jeff Ens, Philippe Pasquier; Simon Fraser University; ISMIR 2021*

Links: https://github.com/jeffreyjohnens/MetaMIDIDataset ; Zenodo (registration)

436,631 MIDIs; scraped artist/title for 221,504; 10.7M audio–MIDI matches linking 237,236 MIDIs to Spotify tracks (829,728 high-reliability); 168,032 with MusicBrainz IDs; genre for 143,868. Access requires registration, affiliation, and a no-redistribution agreement.

**Evidence.** Underlies MMM (Multi-Track Music Machine) training.

**For the studio.** Larger and better-labelled than Lakh, but its terms preclude bundling; useful for research-only pretraining.

<small>Tags: [dataset] [ethics-legal] · Verification: verified · Cluster 07</small>

### `hentschel2021mozart` — DCML corpora — Distant Listening Corpus and the DCML harmony standard

*Johannes Hentschel, Markus Neuwirth, Martin Rohrmeier et al.; EPFL Digital and Cognitive Musicology Lab; ABC (Annotated Beethoven Corpus) 2018 (Frontiers), Annotated Mozart Sonatas 2021 (TISMIR), Distant Listening Corpus 2025*

Links: https://github.com/DCMLab/dcml_corpora ; https://github.com/DCMLab/ABC ; https://github.com/DCMLab/mozart_piano_sonatas

Expert Roman-numeral annotations (DCML standard: chord, inversion, applied chords, phrase and cadence labels) entered directly in MuseScore .mscx files and extracted to TSV (notes, measures, harmonies) with the `ms3` parser; 12 public sub-corpora (Beethoven quartets and sonatas, Mozart sonatas, Chopin mazurkas, Corelli, Debussy, Dvořák, Grieg, Liszt, Medtner, Schumann, Tchaikovsky). Licence CC-BY-NC-SA 4.0 (partial).

**Evidence.** Multi-annotator review workflow; the basis of numerous corpus-study papers.

**For the studio.** Exemplar of annotations *living inside the score file* (harmony labels as staff text) — the same pattern the studio needs for human+AI annotations.

<small>Tags: [corpus] [theory-analysis] [annotation] · Verification: verified (repo); licence/paper partial · Cluster 07</small>

### `bradshaw2025ariamidi` — Aria-MIDI + Aria — Aria-MIDI: A Dataset of Piano MIDI Files for Symbolic Music Modeling; Scaling Self-Supervised Representation Learning for Symbolic Piano Performance

*Louis Bradshaw, Simon Colton (QMUL); ICLR 2025. Aria model: Louis Bradshaw, Honglu Fan, Alexander Spangher, Stella Biderman, Simon Colton (QMUL / EleutherAI / USC / Geneva); ISMIR 2025*

Links: https://arxiv.org/abs/2504.15071 ; https://github.com/loubbrad/aria-midi ; https://arxiv.org/abs/2506.23869 ; https://github.com/EleutherAI/aria

Aria-MIDI: 1.19M MIDI files (~801K after dedup, ~100,000 hours) transcribed from internet solo-piano recordings via an LLM-driven crawler, a piano/non-piano audio classifier and the Aria-AMT transcriber, with LLM-extracted metadata (composer 99.3% accuracy); CC-BY-NC-SA 4.0. Aria: a 650M-parameter decoder trained on it with an *absolute-onset* tokenization (onsets relative to 5-s segments instead of cumulative time-shifts), fine-tuned for continuation, contrastive embeddings (SimCLR) and classification. Human control: prompt continuation only (plus a Disklavier turn-taking duet demo, "Aria-Duet", arXiv 2511.01663).

**Evidence.** Trained listeners preferred Aria continuations over Anticipatory Music Transformer and MusicGen (p<0.001), on par with Suno v3.5; SOTA composer/genre classification from embeddings.

**For the studio.** The largest open piano dataset and the strongest open piano continuation model; the tokenization insight (absolute onsets) is relevant to any studio representation; licence is non-commercial.

<small>Tags: [dataset] [symbolic-generation] [representation] [transcription] [expression-performance] · Verification: verified (arXiv PDFs fetched) · Clusters 03, 07, 08</small>

### `gotham2019wheninrome` — WhenInRome — When in Rome: A Meta-corpus of Functional Harmony (RomanText)

*Mark Gotham, Gianluca Micchi, Néstor Nápoles López, Malcolm Sailor; TISMIR 2023 (DOI 10.5334/tismir.165); RomanText format from Tymoczko, Gotham, Cuthbert, Ariza (ISMIR 2019)*

Links: https://transactions.ismir.net/articles/10.5334/tismir.165 ; https://github.com/MarkGotham/When-in-Rome

~2,000 analyses of ~1,500 works encoded in RomanText (.rntxt; parsed by music21), aligned to scores (mxl or remote links): Bach chorales (371) & preludes, Beethoven quartets (16) & sonata first movements (32) & variations, Mozart sonatas (18) & variations, Chopin mazurkas (56), Haydn Op. 20, Schubert cycles, Monteverdi madrigals (48), textbook modulation examples. New content CC-BY-SA 4.0; converted analyses keep source licences.

**Evidence.** The largest open training/eval set for symbolic Roman-numeral analysis (used by AugmentedNet, RNBert).

**For the studio.** A proven text syntax in which humans annotate harmony *as instructions the machine can read* ("m5 V7 m6 I") — a natural template for the studio's harmonic-annotation lane and for LLM-readable analysis.

<small>Tags: [theory-analysis] [annotation] [corpus] [representation] · Verification: verified (fetched primary source) · Clusters 06, 07</small>

### `gotham2022openscore` — OpenScore Lieder & OpenScore String Quartets — CC0 critical-quality encodings

*Mark Gotham, Peter Jonas (OpenScore / MuseScore); MEC 2021 (proc. 2022) "The OpenScore Lieder Corpus"; String Quartets corpus (Gotham et al., 2023)*

Links: https://github.com/OpenScore/Lieder ; https://github.com/OpenScore/StringQuartets ; https://musescore.com/openscore-lieder-corpus

Lieder: 1,200+ 19th-century songs by 100+ composers, crowd-transcribed and professionally proofread, in MuseScore .mscx (batch-convertible to MusicXML/MIDI/PDF/MP3) with composers/scores/sets TSV metadata; CC0. String Quartets: ~100 movements from the classical/romantic repertoire (partial), same pipeline.

**Evidence.** Best Poster, MEC 2021; used by When-in-Rome analyses and DCML.

**For the studio.** Public-domain, notation-level, *proofread* scores — ideal both for training and as the demo repertoire for annotation tools.

<small>Tags: [corpus] [dataset] [notation] · Verification: verified (Lieder); Quartets partial · Cluster 07</small>

### `neuwirth2018abc` — DCML-ABC — The Annotated Beethoven Corpus (ABC) and the DCML harmony annotation standard

*Markus Neuwirth, Daniel Harasim, Fabian C. Moss, Martin Rohrmeier; DCML, EPFL; Frontiers in Digital Humanities 5, 2018 (DOI 10.3389/fdigh.2018.00016); corpus v2.x maintained 2018–2025*

Links: https://github.com/DCMLab/ABC ; https://dcmlab.github.io/standards ; https://zenodo.org/records/14996911

Expert harmonic analyses of all 16 Beethoven string quartets (80 movements, ~36,000 labels) entered *directly into MuseScore files as text (harmony/lyrics) attached to notes*, then extracted with the `ms3` parser into TSV tables (notes, measures, chords, labels). The DCML standard is a regular-expression-defined modified Roman-numeral syntax (key, root, inversion, extensions, suspensions, recursive applied chords like V7/V/V, phrase and cadence marks). CC BY-NC-SA 4.0.

**Evidence.** Corpus scale; inter-annotator review process; downstream ML use.

**For the studio.** Demonstrates the "annotate on the score in the editor, parse to a machine-readable table" workflow the studio wants — human marks typed on the notation become structured data via a grammar. The regex-defined label grammar is directly reusable for validating harmonic instructions.

<small>Tags: [theory-analysis] [annotation] [corpus] [representation] · Verification: verified (fetched repository) · Cluster 06</small>

### `manilow2019slakh` — Audio stems & captions — MusicNet, Slakh2100, MedleyDB, MUSDB18, MusicCaps, Song Describer

*MusicNet (John Thickstun, Zaid Harchaoui, Sham Kakade; ICLR 2017; 330 classical recordings, 34 h, >1M note labels; CC-BY 4.0); Slakh2100 (Ethan Manilow, Gordon Wichern, Prem Seetharaman, Jonathan Le Roux; MERL; WASPAA 2019; 2,100 Lakh MIDIs rendered with pro sample libraries, 145 h of stems; CC-BY 4.0); MedleyDB 1.0/2.0 (Rachel Bittner et al., NYU; ISMIR 2014; 122+74 multitracks; CC-BY-NC-SA); MUSDB18 / MUSDB18-HQ (Zafar Rafii et al., 2017; 150 songs ~10 h, 4 stems; mixed licences, some tracks restricted); MusicCaps (Andrea Agostinelli et al., Google, 2023; 5,521 ten-second AudioSet clips with expert captions; CC-BY-SA 4.0); Song Describer (Ilaria Manco, Benno Weck et al.; NeurIPS 2023 ML4Audio; ~1.1k captions for 706 CC-licensed tracks; CC-BY)*

Links: https://zenodo.org/record/5120004 (MusicNet) ; http://www.slakh.com ; https://medleydb.weebly.com ; https://sigsep.github.io/datasets/musdb.html ; https://www.kaggle.com/datasets/googleai/musiccaps ; https://github.com/mulab-mir/song-describer-dataset

The audio-side complements: MusicNet and Slakh give note-aligned audio (Slakh synthetic but multitrack with MIDI ground truth — the ideal "render a compile" testbed); MedleyDB/MUSDB18 are separation benchmarks; MusicCaps/Song Describer are the text-audio evaluation sets used by every text-to-music model.

**Evidence.** All are standard benchmarks in their tasks.

**For the studio.** Slakh2100 is uniquely useful: symbolic multitrack ↔ stems pairs for training arrangement-rendering and for evaluating symbolic "compiles" by audio similarity.

<small>Tags: [dataset] [transcription] [audio-generation] [evaluation] · Verification: partial (recalled) · Cluster 07</small>

### `long2024pdmx` — PDMX — Public Domain MusicXML dataset (>250k scores)

*Phillip Long, Zachary Novack, Taylor Berg-Kirkpatrick, Julian McAuley; UC San Diego; ICASSP 2025 (arXiv Sept 2024).*

Links: https://arxiv.org/abs/2409.10831 ; https://github.com/pnlong/PDMX ; Zenodo 13763756

>250,000 MusicXML scores collected from MuseScore.com restricted to works marked public domain, with user ratings, genre tags, and annotations enabling quality filtering; CC-BY 4.0; released with MusicRender (a MusPy extension handling MusicXML expressive markings). Experiments show rating-based subsets improve multitrack generation.

**Evidence.** Authors call it "the largest available copyright-free symbolic music dataset."

**For the studio.** The cleanest large notation-level (not MIDI-level) corpus — includes dynamics, articulations, lyrics — i.e., exactly the representation a notation-first studio manipulates.

<small>Tags: [dataset] [notation] [ethics-legal] [symbolic-generation] · Verification: verified · Clusters 07, 08</small>

### `kong2020giantmidi` — GiantMIDI-Piano — 10,855 transcribed classical piano pieces

*Qiuqiang Kong, Bochen Li, Jitong Chen, Yuxuan Wang; ByteDance; arXiv 2020, TISMIR 2022*

Links: https://github.com/bytedance/GiantMIDI-Piano ; https://arxiv.org/abs/2010.07061

10,855 MIDI files / ~1,237 hours from 2,786 composers, transcribed from YouTube solo-piano audio with Kong's high-resolution transcription model; curated subset 7,236 files (1,787 composers). CC-BY 4.0. Repo archived (read-only) April 2025.

**Evidence.** Transcription quality evaluated against MAESTRO; widely used as a large classical-piano pretraining corpus.

**For the studio.** Permissive-licence expressive piano data (the founder's instrument family) for pretraining.

<small>Tags: [dataset] [transcription] [expression-performance] · Verification: verified · Cluster 07</small>

### `kantarelis2024chordonomicon` — Chordonomicon — 666,000 songs' chord progressions

*Spyridon Kantarelis, Konstantinos Thomas, Vassilis Lyberatos, Edmund Dervakos, Giorgos Stamou; NTUA Athens; arXiv Oct 2024 (v3 Dec 2024)*

Links: https://arxiv.org/abs/2410.22046 ; HF `ailsntua/Chordonomicon`

>666k user-generated chord sequences scraped from guitar-tab sites, with section labels (verse/chorus…), genre, release year, Spotify IDs, and harmonic-function tags; provided as text and graph representations. Paper CC-BY 4.0; dataset license per repo (partial).

**Evidence.** Demonstrated genre classification and progression generation baselines.

**For the studio.** Chord-level structural priors for pop songwriting (David Foster-style harmonic vocabulary) at a scale no MIDI corpus offers.

<small>Tags: [dataset] [theory-analysis] [structure] · Verification: verified · Cluster 07</small>

### `xu2025metascore` — MetaScore — Generating Symbolic Music from Natural Language Prompts using an LLM-Enhanced Dataset

*Weihan Xu, Julian McAuley, Shlomo Dubnov, Taylor Berg-Kirkpatrick, Hao-Wen Dong (Duke / UC San Diego / U. Michigan); ISMIR 2025 (arXiv Oct 2024)*

Links: https://arxiv.org/abs/2410.02084 ; https://ismir2025program.ismir.net/poster_32.html

MetaScore: 963K MuseScore-sourced scores with metadata (genre via classifier, composer, complexity, instruments), plus LLM (BLOOM) generated captions. Two generators: MST-Tags (categorical control) and MST-Text (free-text), both built on REMI+/MMT-style representations — i.e., scores are converted to MIDI tokens rather than generated as MusicXML.

**Evidence.** 22-participant study: MST-Text comparable to Text2midi on overall quality and better than a BART baseline on coherence, arrangement and adherence.

**For the studio.** Largest *score*-origin (not performance) dataset; tag-conditioning offers a controllable alternative to captions; confirms the absence of native MusicXML generation.

<small>Tags: [dataset] [text-conditioning] [notation] [symbolic-generation] · Verification: verified (arXiv PDF fetched) · Cluster 03</small>

## B5. Substrate: education & pedagogy

### `egozy21m385` — Egozy21M385 — 21M.385 / 6.4550 Interactive Music Systems (Eran Egozy, MIT)

*Eran Egozy (Harmonix co-founder; MIT Music & Theater Arts / EECS); offered since ~2014; OCW Fall 2016. 21M.383 Computational Music Theory & Analysis (Cuthbert) is covered by another agent.*

Links: https://catalog.mit.edu/subjects/21m/ ; https://musictech.mit.edu/courses/ ; https://mta.mit.edu/person/eran-egozy

Catalog: "Explores audio synthesis, musical structure, human computer interaction (HCI), and visual presentation for the creation of interactive musical experiences." Students build real-time Python (Kivy) apps: synthesis, sequencing, MIDI/gesture input, note-highway and rhythm-game-style interfaces, culminating in team final projects and a public demo concert. Egozy also teaches 21M.387/6.3020 Fundamentals of Music Processing. Students call it "their favorite class at MIT so far… because it employs both sides of their personalities" (Egozy, Spectrum 2025).

**Evidence.** Course description verified; specifics of labs from recall of past syllabi.

**For the studio.** A proven curriculum for teaching composers to build musical software — and a pipeline of collaborators; its architecture (Python + real-time audio + notation-free interaction) contrasts with the studio's notation-first stance.

<small>Tags: [education] [real-time] [game] [creativity-support] · Verification: partial (catalog/course list verified; lab details from recall) · Clusters 01, 07</small>

### `freeman2019earsketch` — EarSketch — coding + music remixing for broadening participation (Georgia Tech)

*Jason Freeman, Brian Magerko, Doug Edwards, Roxanne Moore et al.; Georgia Tech; Organised Sound 2013; SIGCSE 2014–2017; CACM 2019 ("EarSketch: engaging broad populations in computing through music", DOI 10.1145/3333613)*

Links: https://earsketch.gatech.edu ; https://doi.org/10.1145/3333613

Browser DAW-like environment where students write Python or JavaScript to place licensed loop samples on tracks, apply effects and algorithmic structure (`fitMedia`, `makeBeat`), with curriculum aligned to AP CS Principles; used by >1M learners (claim, partial).

**Evidence.** Studies report increased intent to persist in computing, especially among under-represented students (CACM 2019 summarises).

**For the studio.** Evidence that code-as-composition scales to novices and that a sample/loop palette plus algorithmic structure is an approachable "compile" model.

<small>Tags: [education] [music-as-code] [HCI-study] · Verification: verified (Crossref) · Cluster 07</small>

### `horn2022tunepad` — TunePad — Python + music for CS learning (Northwestern TIDAL Lab)

*Michael Horn, Nichole Pinkard, Amartya Banerjee, Matthew Brucker, Jamie Gorson et al.; Northwestern University with Georgia Tech (EarSketch team); IDC 2017 demo; CHI 2022 ("TunePad Playbooks", DOI 10.1145/3491102.3502021); NSF DRL-1612619/1451762/1837661*

Links: https://tunepad.com ; https://doi.org/10.1145/3491102.3502021

Free browser platform where learners write Python (`playNote`, `rest`, loops, functions) in notebook-like cells to produce beats, basslines, chords and melodies with real-time playback; Playbooks are tutorial+code documents; classroom research with teens in Chicago.

**Evidence.** CHI 2022 reports design and deployment findings; multiple studies of engagement/computational-thinking gains (details not fetched).

**For the studio.** The clearest existing realisation of "music as code that compiles to sound," including cell/notebook UI ideas for a composition-as-program editor.

<small>Tags: [education] [music-as-code] [HCI-study] · Verification: verified (Crossref + site) · Cluster 07</small>

### `cuthbert2023ocw21m383` — OCW21M383 — MIT OCW 21M.383 Computational Music Theory and Analysis (Spring 2023) and "Video 12b: Chorales as a Corpus"

*Michael Scott Asato Cuthbert; MIT OpenCourseWare; Spring 2023; CC BY-NC-SA*

Links: https://ocw.mit.edu/courses/21m-383-computational-music-theory-and-analysis-spring-2023/ ; https://ocw.mit.edu/courses/21m-383-computational-music-theory-and-analysis-spring-2023/pages/about-the-course-and-music21/ ; https://learn.mit.edu/search?resource=18680&resource_title=video-12b-chorales-as-a-corpus

"Presents major approaches to computational music theory and musicology in the symbolic (score-based) domain… algorithms for music theory, encoding, corpus studies, musical search and similarity, feature extraction and machine learning, music generation, and computational music perception." Every problem set is Python + music21 in notebooks ("as you proceed through this class, you'll be unlocking features of music21"). Lecture arc: how computers "hear" music → pitch/duration/score representation → Streams as hierarchies → MusicXML (incl. interview with Michael Good) → **corpus studies and statistics on the Bach chorales** (Videos 12b "Chorales as a Corpus", 12c plotting, 12d ties; Classes 13–15 corpus statistics, encoding corpora, voice leading) → equivalence classes/OPTIC → music cognition guest sessions → scales, chords and Roman numerals (Video 22b: "Working and Composing with Scales, Chords, and Roman Numerals"; 22c algorithmic improvisation, George Lewis) → three classes of algorithmic composition → feature extraction/ML/AI → OMR and visualization. Video 12b demonstrates treating the 371 chorales as a queryable dataset (iterate, filter by number/title, analyze keys/harmony across the set) — the same corpus that trains Coconet.

**Evidence.** Full syllabus/video list fetched; the individual Video 12b page could not be fetched (redirect loop), so its exact contents are inferred from title and course context.

**For the studio.** A tested pedagogy for teaching composers to treat notation as data and to write analysis "programs" — the mindset behind "composition as a program to be compiled"; also a source of exercises for a studio tutorial.

<small>Tags: [education] [theory-analysis] [corpus] [notation] [music-as-code] [toolkit] · Verification: verified (course pages fetched); Video 12b content partial · Cluster 01</small>

### `aaron2016sonicpi` — Sonic Pi — live coding for schools

*Sam Aaron (with Alan Blackwell, Pamela Burnard); University of Cambridge / Raspberry Pi Foundation; JMTE 2016 ("The development of Sonic Pi and its use in educational partnerships", DOI 10.1386/jmte.9.1.75_1); IJPADM 2016; MIT-licensed software*

Links: https://sonic-pi.net ; https://doi.org/10.1386/jmte.9.1.75_1

Ruby-based live-coding environment (SuperCollider backend) with `live_loop`, samples, synths and effects, designed for the UK computing curriculum and for performance ("Sonic Pi: Live & Coding" project with schools).

**Evidence.** Classroom studies with teachers/students in Cambridge; later Korean and UK Code Club studies.

**For the studio.** Live loops embody an *iterative edit-while-playing* loop — an interaction model worth borrowing for annotate→compile cycles.

<small>Tags: [education] [music-as-code] [real-time] · Verification: verified (Crossref) · Cluster 07</small>

### `yousician2026` — Practice/learning apps — Yousician, Simply Piano, Flowkey, Melodics, Piano Marvel, SmartMusic, Chordify, Moises

*Yousician (Helsinki, 2010–; pitch-detection feedback for guitar/piano/bass/ukulele/voice); Simply Piano (JoyTunes/Simply, Tel Aviv); Flowkey (Berlin; Yamaha-partnered); Melodics (Auckland; pad/keys/drums timing training); Piano Marvel (US; MIDI-based assessment + SASR sight-reading test); SmartMusic (MakeMusic; assessment of scanned band/orchestra parts — sunset alongside Finale, status partial); Chordify (Utrecht, 2013–; automatic chord extraction from any audio/YouTube, from de Haas/Koops/Wiering's research); Moises (Moises Systems, 2019–; stem separation, chord and key detection, tempo control for practice)*

Links: https://yousician.com ; https://www.simplypiano.com ; https://www.flowkey.com ; https://melodics.com ; https://pianomarvel.com ; https://chordify.net ; https://moises.ai

Commercial "AI tutor" ecosystem based on real-time pitch/onset detection (mic) or MIDI, gamified progress, and, increasingly, source separation and chord recognition to turn any recording into practice material.

**Evidence.** Few peer-reviewed efficacy studies; industry-scale user bases.

**For the studio.** They define user expectations for real-time feedback on playing/singing — reusable for the "hum or play it in" annotation path — and show stem separation (Moises) as a practical way to ingest example audio.

<small>Tags: [education] [product] [transcription] [real-time] · Verification: partial (recalled) · Cluster 07</small>

## C1. Context: product landscape

### `ableton2024live12` — Live12 — Ableton Live 12 "Similar Sounds", MIDI Generators/Transformations

*Ableton, Berlin; Live 12 released 5 Mar 2024; 12.1/12.2/12.3 (2024–25).*

Links: https://www.ableton.com/en/live/what-is-new-in-12/

[S][I] No generative AI for music; **Sound Similarity Search** uses ML audio embeddings to find similar samples/presets in the library; new rule-based **MIDI Generators** (Rhythm, Seed, Shape, Stacks) and **Transformations** (Arpeggiate, Connect, Ornament, Quantize, Recombine, Strum…) are non-neural, fully editable devices. Max-for-Live hosts third-party ML devices (Magenta Studio, Neutone).

**For the studio.** Ableton's stance — deterministic, transparent generators + ML only for *retrieval* — is a deliberate design position that many producers trust; a good foil for the studio's "AI as compiler" and a reminder that transparency is a feature.

<small>Tags: [product] [symbolic-generation] [DAW-plugin] · Verification: partial · Cluster 08</small>

### `apple2024logicpro11` — LogicPro11 — Logic Pro 11 Session Players, Stem Splitter, ChromaGlow, Chord Track (Apple)

*Apple; announced 7 May 2024, released 13 May 2024 (Logic Pro for Mac 11 / iPad 2); 11.1 (Nov 2024) and 11.2 (2025) updates added instruments/features.*

Links: https://www.apple.com/newsroom/2024/05/logic-pro-takes-music-making-to-the-next-level-with-new-ai-features/

[S][I] **Session Players** = Drummer (2013) + new **Bass Player** (8 players; complexity/intensity; slides, mutes, dead notes, pickup hits) + **Keyboard Player** (4 styles, block chords → extended voicings) that *follow the Chord Track* and can be edited as MIDI regions ("trained in collaboration with" session musicians). **Stem Splitter** (4 stems, on-device Apple silicon); **ChromaGlow** saturation. $199.99 / free update.

**Evidence.** No public evaluation; widely reviewed as the first mainstream DAW with generative *symbolic* accompaniment beyond drums.

**For the studio.** The best current example of "chords + style → editable MIDI parts" inside a DAW — the arranger-keyboard idea reborn. Its parameters (complexity, intensity, style) are a reasonable minimum control vocabulary for the studio's "compile" step; its lack of notation view, multimodal input or arrangement-level reasoning is the gap.

<small>Tags: [product] [accompaniment] [symbolic-generation] [editing] [DAW-plugin] · Verification: verified · Cluster 08</small>

### `dreamtonics2025synthv2` — SynthV2 — Synthesizer V Studio 2 Pro (Dreamtonics) and the AI-singer category (ACE Studio, Vocaloid 6, Kits.ai)

*Dreamtonics (Kanru Hua), SV Studio 2 Pro announced Dec 2024, released 2025; ACE Studio (Timedomain, 2022→2025 v1.9+); Yamaha Vocaloid 6 (Oct 2022, VOCALO CHANGER); Kits.ai (2023→, licensed artist voices).*

Links: https://dreamtonics.com/synthesizerv/ ; https://acestudio.ai ; https://www.vocaloid.com ; https://www.kits.ai

[S→A][I] Note-level piano-roll + lyrics → sung vocals with per-note pitch/timbre/breath editing, style/vocal-mode parameters, AI retakes; ACE Studio adds audio-to-MIDI+lyrics import and expressive "AI Pitch"; Vocaloid 6 adds voice-to-voice conversion; Kits.ai sells licensed, revenue-shared artist voice models.

**For the studio.** These are *symbolic-first* vocal renderers — a compiled score's vocal line can be rendered without any text-to-song model, keeping authorship with the composer. Also models a consent-based voice-licensing business (Kits.ai).

<small>Tags: [product] [expression-performance] [symbolic-generation] [notation] [ethics-legal] · Verification: partial · Cluster 08</small>

### `elevenlabs2025music` — ElevenMusic — ElevenLabs Music (Eleven Music v1 Aug 2025; Music v2 2026)

*ElevenLabs; launched 5 Aug 2025 with licences from Merlin Network and Kobalt; later consumer "ElevenMusic" remix/streaming service (2026).*

Links: https://techcrunch.com/2025/08/05/elevenlabs-launches-an-ai-music-generator-which-it-claims-is-cleared-for-commercial-use/

Text-to-song with vocals, **lyric editing throughout the track, section regeneration (verse/chorus/bridge) without restarting**, instrumentals, **2–6 stem export**, multilingual, mid-track genre transitions, long-form; API supports generation, **audio-reference matching, inpainting** and long-form composition. Claims training on licensed data only and "cleared for commercial use". Closed; no symbolic input; not real-time.

**Evidence.** First major text-to-music launch built on licences rather than post-hoc settlement.

**For the studio.** Another commercial confirmation that section-level regeneration + stems + inpainting are baseline expectations; the licensed-data positioning is the new norm.

<small>Tags: [audio-generation] [product] [editing] [infilling] [ethics-legal] · Verification: verified (product page); licensing partners partial · Clusters 04, 08</small>

### `google2025lyria2` — Lyria2-Sandbox — Google DeepMind Lyria / Lyria 2 / Music AI Sandbox / MusicFX DJ

*Google DeepMind + Google Labs + YouTube. MusicFX (AI Test Kitchen, 2023–24); Music AI Sandbox expanded with Lyria 2 (Apr 2025); Lyria RealTime API (20 May 2025); Lyria 3 in Gemini app (Feb 2026); **Google acquired Producer.ai (formerly Riffusion) 25 Feb 2026** and relaunched it as **Google Flow Music** (Lyria 3 Pro); Believe/TuneCore partnership 6 May 2026; Lyria 3.5 current.*

Links: https://deepmind.google/models/lyria/ ; https://deepmind.google/blog/music-ai-sandbox-now-with-new-features-and-broader-access/ ; https://www.musicbusinessworldwide.com/believe-partners-with-google-to-offer-ai-music-creation-tool-flow-music-to-its-artists/

Lyria (RL-tuned for quality/prompt adherence) powers: **Music AI Sandbox** with *Create* (text + optional lyrics placed on a timeline, key, tempo), *Extend* (continue uploaded/generated audio), *Edit* (transform mood/genre of a whole clip or a **selected region**, fill gaps, blend transitions—i.e., inpainting), multitrack views and loop generation; **MusicFX DJ** (real-time mixing of weighted text prompts with instrument toggles, brightness/chaos/density, key/tempo, 48 kHz stereo streaming). Lyria 2: 48 kHz stereo, "professional-grade". All outputs SynthID-watermarked. Closed weights; no symbolic (MIDI) input; key/tempo are the only structured controls.

**Evidence.** Ranked among top systems in 2025 human-preference benchmarks (Grötschla et al.); no independent user studies of the Sandbox published.

**For the studio.** Most complete *audio-level* editing loop among big-tech offerings (extend/inpaint/real-time steer) and the only one with a public open-weights real-time model — a candidate rendering/"audio compile" back-end, subject to licence review.

<small>Tags: [audio-generation] [product] [editing] [infilling] [real-time] [controllability] · Verification: verified · Clusters 04, 08</small>

### `google2025lyriarealtime` — LyriaRT-Lyria3 — Lyria RealTime API, Lyria 3 / 3.5, Gemini integration (2025–2026)

*Google DeepMind / Google Labs. **Lyria RealTime** API in Gemini API / AI Studio Jun 12 2025 (announced I/O May 2025); **Lyria 3** Feb 2026 (with ProducerAI acquisition, Gemini app music); **Lyria 3.5** mid-2026 (3-minute songs, sharper vocals/lyrics; in Flow Music and Gemini).*

Links: https://magenta.withgoogle.com/lyria-realtime ; https://deepmind.google/models/lyria/lyria-realtime/ ; https://deepmind.google/models/lyria/

Lyria RealTime is a **block-autoregressive streaming model** (48 kHz stereo) steered moment-to-moment by weighted blends of text prompts plus BPM, key, note density, brightness, instrumentation—**≤2 s from control change to audible effect**; open-sourced demo apps PromptDJ, **PromptDJ-MIDI** (physical MIDI controllers map to parameters), PromptDJ-Pad. Lyria 3/3.5: full songs with multilingual vocals, lyrics, image-to-music via Gemini, up to 3 min, SynthID; trained on music Google/YouTube "have the right to use".

**Evidence.** No papers beyond "Live Music Models" (see Magenta RT); product claims.

**For the studio.** Real-time steering with MIDI *controllers* (parameters, not notes) is the closed-source ceiling for "jam with the AI"; the open counterpart (Magenta RT 2) now accepts MIDI *notes*.

<small>Tags: [audio-generation] [real-time] [product] [controllability] [multimodal-input] [image] · Verification: verified (official pages); Lyria 3.5 details partial · Cluster 04</small>

### `googledeepmind2025sandbox` — MusicAISandbox — Music AI Sandbox (Google DeepMind × YouTube Music AI Incubator)

*Google DeepMind and YouTube; announced Nov 2023, expanded 24 Apr 2025 (Lyria 2 / Lyria RealTime)*

Links: https://deepmind.google/discover/blog/music-ai-sandbox-now-with-new-features-and-broader-access/

Experimental toolkit with *Create* (describe sound/genre/mood, place lyrics on a timeline with tempo and key), *Extend* (continue uploaded or generated audio), and *Edit* (transform mood/genre/style by prompt or presets, fill gaps, create transitions); Lyria RealTime enables moment-to-moment interactive control. Co-designed with musicians in the YouTube Music AI Incubator (e.g., The Range, Isabella Kensington, Adrie, Sidecar Tommy).

**Evidence.** Blog/industry; no peer-reviewed user study published as of this writing.

**For the studio.** The most prominent industry attempt at *musician-co-designed* generative tooling whose verbs (create/extend/edit on a timeline) mirror the studio's loop, but audio-first and closed.

<small>Tags: [product] [audio-generation] [editing] [real-time] [co-creation-framework] · Verification: verified (fetched DeepMind blog) · Cluster 05</small>

### `hexachords2022orb` — OrbCaptain — Orb Producer Suite 3 (Hexachords) and Captain Chords Epic (Mixed In Key)

*Hexachords (Orb Composer 2018 → Orb Producer Suite 3.0 ~2021–22); Mixed In Key (Captain Plugins 2017 → Captain Chords Epic 2022–23).*

Links: https://www.hexachords.com ; https://mixedinkey.com/captain-plugins/

[S][I] Four MIDI-generating plugins (Chords, Melody, Bass, Arpeggio) that share a chord progression and generate/re-roll parts per block ("AI" = constraint/probabilistic engines); Captain Chords: chord progression builder with style presets, melody/bass companions, drag-out MIDI.

**For the studio.** Shows the practical "one shared chord track drives many part generators" architecture — a small-scale compile loop — and the UI convention of *re-roll a block*.

<small>Tags: [product] [symbolic-generation] [DAW-plugin] [accompaniment] · Verification: partial · Cluster 08</small>

### `mureka2025` — Mureka — Mureka (Kunlun Tech / Skywork AI)

*Kunlun Tech (Beijing); Mureka O1 / V6 announced Mar 2025 (O1 marketed as first "chain-of-thought" music model), later V7/V7.5 (2025) — versions partial.*

Links: https://www.mureka.ai

Text/lyrics-to-song with Easy/Custom/Soundtrack modes, remix, reference-song style, vocals + instrumentals; API. Closed; no symbolic input.

**Evidence.** None public; vendor claims of MOS parity with Suno.

**For the studio.** Shows the Chinese commercial ecosystem (alongside open YuE/ACE-Step/DiffRhythm from Chinese labs) converging on the same one-shot paradigm.

<small>Tags: [audio-generation] [product] · Verification: partial (homepage confirms product; versions from recall) · Cluster 04</small>

### `kunlun2025mureka` — Mureka — Mureka (Kunlun Tech / Skywork AI), Mureka O1 "music reasoning" model

*Kunlun Tech (Beijing); Mureka O1 launched 26 Mar 2025 (claimed first chain-of-thought "MusiCoT" music model), Mureka V7 later 2025; API and fine-tuning on user songs.*

Links: https://www.mureka.ai ; https://www.prnewswire.com/news-releases/kunlun-tech-launches-the-worlds-first-music-reasoning-large-model-mureka-o1-leading-the-global-ai-music-revolution-302411665.html

[A][I-partial] Lyrics-first text-to-song with vocals; "reasoning" over structure before generation; reference-audio style conditioning; song editing (section regeneration), stem export; developer API.

**Evidence.** Vendor benchmarks only.

**For the studio.** Example of *planning-then-generating* (structure first) in a commercial model — the audio analogue of the founder's compile step; also one of the few platforms offering *fine-tune on your own catalogue*.

<small>Tags: [product] [audio-generation] [structure] [text-conditioning] · Verification: partial · Cluster 08</small>

### `moises2025aistudio` — MoisesStudio — Moises AI Studio (Moises / Music.AI)

*Moises Systems (Geraldo Ramos), Salt Lake City/Brazil; AI Studio launched 20 Aug 2025.*

Links: https://moises.ai/newsroom/product-announcements/launch-ai-studio/

[A][I] Generates **context-aware instrumental stems** that adapt to the user's existing audio (harmony adherence + style from audio reference/text/presets) inside a simplified DAW; bundled stem separation, beat/chord detection, voice conversion, auto-mix/master. Explicitly does **not** generate full songs, lyrics or vocals; company stresses licensed/annotated training data for separation.

**For the studio.** A commercial "add a part to *my* track" system — the audio-domain counterpart of the studio's compile-one-part step — and a positioning (no full songs) that matches the founder's philosophy.

<small>Tags: [product] [audio-generation] [accompaniment] [editing] [transcription] · Verification: verified · Cluster 08</small>

### `scaler2025v3` — Scaler3 — Scaler 3 (Scaler Music / Plugin Boutique)

*Scaler Music (Davide Carbone) / Plugin Boutique; announced NAMM Jan 2025, released Mar 2025.*

Links: https://www.scalerplugin.com ; https://help.pluginboutique.com/hc/en-us/articles/35864679857684-What-s-new-in-Scaler-3

[S][I] Chord/scale detection from MIDI or audio, chord-set suggestions by genre/artist "style", an **Arrange page** (multi-track timeline for chords, bass, melody, phrases), built-in sounds, performances/phrases per chord; rule/curated-content based rather than neural. Exports MIDI to the host.

**For the studio.** Market-leading "harmony assistant" plugin; its arrange page shows demand for lead-sheet-to-arrangement inside DAWs, but with no notation and canned phrases.

<small>Tags: [product] [symbolic-generation] [theory-analysis] [DAW-plugin] · Verification: partial · Cluster 08</small>

### `splice2025landr` — SpliceLANDR — Splice and LANDR AI features (context only)

*Splice (sample marketplace; "Create"/stack-based AI assembly, 2023; later AI search/"Skills"); LANDR (AI mastering since 2014; AI distribution/plugins).*

Links: https://splice.com ; https://www.landr.com

Not generative music models per se: Splice uses retrieval/ML to assemble compatible sample stacks (key/tempo matched) and later added AI-assisted search and sample generation partnerships; LANDR is best known for automated mastering. Both are *tool-level* AI inside producer workflows rather than text-to-song.

**Evidence.** None.

**For the studio.** Examples of AI as *assistant inside the DAW* (matching, mastering) rather than composer replacement—closer in spirit to the studio's "enabler" framing.

<small>Tags: [product] [DAW-plugin] · Verification: unverified (recall; not fetched) · Cluster 04</small>

### `splice2024create` — SpliceCreate — Splice "Create" (Stacks)

*Splice; Create launched 2023, expanded 2024–25.*

Links: https://splice.com/sounds/create

[A][I] Not generative: assembles a *stack* of key/BPM-compatible human-made samples from Splice's licensed library from a seed sound, swappable per layer, exportable to the DAW. (Splice also offers AI-powered search and, 2025, "Splice Skills"/plugins.)

**For the studio.** Retrieval-and-assembly of *licensed human material* as an alternative to generation — a legally clean "compile" strategy for audio texture.

<small>Tags: [product] [audio-generation] [toolkit] · Verification: partial (page fetched but content JS-rendered) · Cluster 08</small>

### `suno2026` — Suno — Suno (v3 → v3.5 → v4 → v4.5 → v5 → v5.5) and Suno Studio

*Suno Inc. (Cambridge, MA; founded 2022 by ex-Kensho engineers). Model timeline (from official release notes): v3 alpha Feb 22 2024 (2-min clips), v3.5 May 24 2024 (4-min, 2-min extensions), v4 Nov 19 2024, v4.5 May 1 2025, **v5 Sep 23 2025**, v4.5-all free tier Oct 21 2025, **v5.5 Mar 26 2026** (+ "Custom Models": train a personal v5.5). **Suno Studio** generative DAW Sep 25 2025 (Premier tier); MIDI import/record/edit Aug 13 2026; "Voices" Aug 7 2026; natural-language lyrics editing Jul 9 2026.*

Links: https://suno.com ; https://suno.com/release-notes ; https://www.musicbusinessworldwide.com/suno-launches-its-own-daw-after-introducing-most-powerful-model-yet/ ; WMG deal https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/

Text/lyrics-to-full-song with vocals. Editing affordances added over time: **Audio Input** (upload/record to extend, Jun 2024), **Stems** (vocal/instrumental split Jul 2024; later 12-stem export), **Covers** (keep melody, change style, Sep 2024), **Replace Section** (regenerate a time range, Oct 2024), **Personas** (save vocal/style identity, Oct 2024), **Remaster** (re-render with newer model, Nov 2024), **Extend**, **Add Vocals / Add Instrumental**, **Hooks** (short-form video). Suno Studio: multitrack timeline, generate stems/parts to match existing tracks, BPM/pitch/volume control, synths/effects, and (2026) MIDI. No public model details; no symbolic conditioning of the generator; not real-time. Legal: RIAA/major-label suits (Jun 2024) alleging stream-ripping; **WMG settled Nov 25 2025**—licensed models in 2026, current models deprecated, free tier non-downloadable, paid download caps, artist opt-in for name/voice; UMG/Sony suits and GEMA/Koda claims continued as of late 2025.

**Evidence.** Pricing: Pro ~$8–10/mo, Premier ~$24–30/mo. Audited by litigation: UMG/Sony discovery says Suno trained on "millions" of their recordings (May 2026 filing).

**For the studio.** The archetype the founder rejects—but its feature history (stems → replace-section → covers/personas → DAW → MIDI) is the strongest market evidence that users demand iterative, part-level, notation-adjacent control. Studio should offer what Suno Studio cannot: notation as the source of truth, explainable "compile", open weights and provenance.

<small>Tags: [audio-generation] [product] [editing] [text-conditioning] [ethics-legal] [DAW-plugin] · Verification: verified (official release notes + MBW) · Clusters 04, 08</small>

### `udio2025` — Udio — Udio (v1 → v1.5 → v1.5 Allegro) and the 2025 UMG/WMG walled-garden pivot

*Uncharted Labs / Udio (NYC), founded Dec 2023 by ex-Google DeepMind researchers David Ding, Conor Durkan, Charlie Nash, Yaroslav Ganin, Andrew Sanchez; public beta Apr 10 2024; v1.5 Jul 23 2024; v1.5 Allegro Mar 18 2025; "Udio Playground" Oct 9 2025. **UMG settlement Oct 29 2025**; WMG deal Nov 2025.*

Links: https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/ ; https://www.prnewswire.com/news-releases/universal-music-group-and-udio-announce-udios-first-strategic-agreements-for-new-licensed-ai-music-creation-platform-302599129.html

Text/lyrics-to-song generating ~30-s segments that are **extended** forwards/backwards into full songs; **Remix** (re-generate with a new prompt from an existing clip), **audio Inpainting** (select a region and regenerate—premium), audio upload, stems. After the UMG deal: a **"walled garden"**—downloads disabled (48-h grace window), streaming/sharing only, fingerprinting and filtering, and a new subscription platform trained only on licensed music to launch in 2026. Closed model; no symbolic conditioning; not real-time.

**Evidence.** Reddit/user backlash over lost downloads (Billboard, Nov 2025); antitrust commentary on the walled-garden model.

**For the studio.** Udio pioneered mainstream *audio inpainting* in a consumer song tool, then became the first "licensed-only" platform—illustrating both the demand for region editing and the fragility of building on unlicensed corpora. A composer-centric open studio avoids both traps by rendering the composer's own material.

<small>Tags: [audio-generation] [product] [editing] [infilling] [ethics-legal] · Verification: verified (Wikipedia + MBW); v2/2026 platform details partial · Clusters 04, 08</small>

### `suno2025wavtool` — WavTool — WavTool (browser DAW with GPT-4 "Conductor") → acquired by Suno

*WavTool (2023, San Francisco); acquired by Suno 30 June 2025.*

Links: https://suno.com/blog/suno-acquires-wavtool

[S]+[A][I] Browser DAW with VST support, sample-accurate editing, stem separation, AI-generated MIDI, and a chat assistant ("Conductor", GPT-4) that edits the project from natural language. Became the basis of Suno Studio.

**For the studio.** Early "LLM inside the DAW" product; its acquisition shows the text-to-song leaders buying *editability*.

<small>Tags: [product] [LLM-agent] [DAW-plugin] · Verification: verified · Cluster 08</small>

## C2. Context: law & policy

### `sturm2019openquestions` — AIMusicOpenQuestions — Artificial Intelligence and Music: Open Questions of Copyright Law and Engineering Praxis

*Bob L. T. Sturm, Maria Iglesias, Oded Ben-Tal, Marius Miron, Emilia Gómez; KTH, EC Joint Research Centre, Kingston, UPF; *Arts* 8(3):115, 2019*

Links: https://doi.org/10.3390/arts8030115

Uses folk-rnn to examine (1) EU copyright questions (authorship of AI output, training on protected works, accidental reproduction) and (2) engineers' responsibilities (document limitations; evaluate for fairness/accountability/transparency, not just accuracy).

**Evidence.** Legal analysis plus practitioner testimony: musicians treated output as raw material; concerns centred on disrupting traditions rather than job loss; some gained regular performance work from AI-assisted repertoire.

**For the studio.** Frames provenance logging and consented training data as engineering duties; supports human-authored-input designs as the clearest path to copyrightable output.

<small>Tags: [ethics-legal] [HCI-study] [symbolic-generation] · Verification: verified (fetched MDPI page) · Cluster 05</small>

### `eu2024aiact` — EUAIAct — EU AI Act GPAI obligations (from 2 Aug 2025), GPAI Code of Practice (10 July 2025) and training-content summary template (24 July 2025)

*European Parliament & Council, Regulation (EU) 2024/1689 (in force 1 Aug 2024); European Commission / AI Office guidelines and template, July 2025; obligations for general-purpose AI providers apply from 2 Aug 2025 (enforcement powers from Aug 2026; legacy models by Aug 2027).*

Links: https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai ; https://www.mayerbrown.com/en/insights/publications/2025/08/eu-ai-act-news-rules-on-general-purpose-ai-start-applying-guidelines-and-template-for-summary-of-training-data-finalized

GPAI providers must keep technical documentation, adopt a **copyright policy** (respect machine-readable opt-outs under Art. 4(3) DSM), and publish a **"sufficiently detailed summary" of training content** using the Commission's template; the voluntary Code of Practice has a copyright chapter (lawful access, honour robots.txt/opt-outs, mitigate infringing outputs). Open-source models get some exemptions but **not** from the copyright policy and training summary duties.

**Evidence.** Regulation + guidance; first enforcement from Aug 2026.

**For the studio.** If the studio releases model weights in the EU, it must publish a training-content summary and honour opt-outs — trivial if it trains only on PD/CC/consented data.

<small>Tags: [ethics-legal] · Verification: partial · Cluster 08</small>

### `umg2024vsuno` — LabelsVSuno — UMG Recordings et al. v. Suno (D. Mass. 1:24-cv-11611) and UMG et al. v. Uncharted Labs/Udio (S.D.N.Y. 1:24-cv-04777)

*Filed 24 June 2024 by UMG, Sony Music and Warner (coordinated by RIAA). Sept 2025: plaintiffs sought to add **stream-ripping / DMCA §1201(a)** claims (YouTube circumvention); judge allowed the amendment (2025–26). **26 May 2026:** UMG & Sony moved to file a second amended complaint asserting **61,026** recordings after discovery showed training on "millions" of their recordings; dispositive-motion deadline Jan 2027 (scheduling order Mar 2026). Warner exited both cases via settlements (Nov 2025); Udio case resolved with UMG (Oct 2025) and WMG; **Sony and UMG v. Suno remains active** and is the bellwether for fair use in music-AI training.*

Links: https://www.musicbusinessworldwide.com/umg-and-sony-seek-to-add-61000-copyrighted-works-to-suno-lawsuit-after-discovery-reveals-suno-trained-on-millions-of-their-recordings/ ; https://www.musicbusinessworldwide.com/files/2026/05/UMG_Sony_Suno.pdf

Direct infringement (unlicensed copying for training), plus §1201 anti-circumvention; Suno/Udio plead fair use and (initially) refused to disclose training data. Statutory damages up to $150k/work sought.

**Evidence.** Complaints include side-by-side prompt outputs replicating recordings (e.g., producer-tag reproductions).

**For the studio.** Defines the legal risk of audio models trained on commercial recordings; underscores why the studio should not depend on such models and should keep provenance of everything it trains on.

<small>Tags: [ethics-legal] [audio-generation] · Verification: verified · Cluster 08</small>

### `concord2023anthropic` — ConcordAnthropic — Concord Music Group et al. v. Anthropic (lyrics)

*Filed Oct 2023 (M.D. Tenn., transferred to N.D. Cal.); Jan 2025 stipulation on output guardrails; ongoing 2026 (partial). Related: *Bartz v. Anthropic* (books) June 2025 fair-use ruling and $1.5bn settlement Sept 2025 — training on lawfully acquired books held fair use, pirated copies not.*

Links: https://www.courtlistener.com/?q=Concord+Music+Group+v.+Anthropic

Music publishers allege Claude reproduced lyrics; case tests output-side infringement and guardrails for LLMs, complementing the German GEMA rulings.

**Evidence.** Pending.

**For the studio.** Lyrics handling in any LLM component should include guardrails against reproducing protected lyrics.

<small>Tags: [ethics-legal] [LLM-agent] · Verification: partial/unverified (2026 status) · Cluster 08</small>

### `lgmunich2025gemaopenai` — GEMAvOpenAI — GEMA v. OpenAI (LG München I, 42 O 14139/24, 11 Nov 2025)

*Munich Regional Court I, 42nd Civil Chamber; GEMA (German collecting society) v. OpenAI over nine German song lyrics; judgment 11 Nov 2025 (appeal pending).*

Links: https://www.loc.gov/item/global-legal-monitor/2026-01-13/germany-court-prohibits-memorization-and-reproduction-of-copyrighted-song-lyrics-in-ai-models/

Held that **memorisation of lyrics in model weights is a reproduction** (§16 UrhG) not covered by the text-and-data-mining exception (§44b UrhG, Art. 4 DSM Directive), and that outputting them is a further infringement attributable to OpenAI, not the prompting user; damages and injunction; OpenAI must license.

**Evidence.** First European merits ruling on GenAI training/memorisation.

**For the studio.** Any model the studio trains/ships must avoid verbatim memorisation of protected works (lyrics *and* scores); public-domain/CC symbolic corpora avoid the issue.

<small>Tags: [ethics-legal] · Verification: verified (LOC summary + law-firm notes) · Cluster 08</small>

### `lgmunich2026gemasuno` — GEMAvSuno — GEMA v. Suno (LG München I, 42 O 763/25, **31 July 2026**)

*Same chamber (presiding judge Elke Schwager); GEMA sued Jan 2025 over outputs resembling "Daddy Cool", "Rasputin", "Forever Young", "Big in Japan", "Atemlos", "Mambo No. 5"; oral hearing Jan 2026; judgment 31 July 2026; Suno says it will explore appeal. (**Note:** the ruling is July 2026, not January 2026 as sometimes reported; January was the hearing.)*

Links: https://www.juve-patent.com/cases/munich-regional-court-stops-suno-using-gema-protected-music/ ; https://variety.com/2026/digital/news/suno-loses-ai-lawsuit-gema-1236825010/

Court found the works were "effectively stored" in Suno's models (memorisation → reproduction), that stream-ripping from YouTube circumvented technical protection, that §44b TDM does not apply where works are retained in reproducible form, and that Suno (not basic-prompt users) is liable for infringing outputs generated in Germany. Remedies: cease-and-desist, disclosure of revenues, damages TBD; not yet enforceable.

**Evidence.** First European judgment against a music generator on the merits.

**For the studio.** Extends the OpenAI logic from lyrics to *music*; makes memorisation audits (MiRA) and clean data non-negotiable for any EU-distributed model.

<small>Tags: [ethics-legal] [audio-generation] · Verification: verified · Cluster 08</small>

### `thaler2025perlmutter` — Thaler — Thaler v. Perlmutter (D.C. Cir. 2025; cert. denied 2 Mar 2026)

*Stephen Thaler (Creativity Machine, "A Recent Entrance to Paradise"); D.D.C. 2023 (Howell J.); D.C. Circuit affirmed 18 Mar 2025 (Millett J.); cert. petition No. 25-449 filed 9 Oct 2025; **certiorari denied 2 Mar 2026**.*

Links: https://www.scotusblog.com/cases/thaler-v-perlmutter/

The Copyright Act requires a **human author**; a work autonomously generated by an AI with no human authorship is unregistrable. Question presented: whether AI outputs "without a direct, traditional authorial contribution by a natural person can be copyrighted." Left undecided: how much human contribution suffices.

**Evidence.** Final for now in the U.S.

**For the studio.** Cements the value of keeping the human as author of record; the studio's provenance logs (who wrote/edited what) may become evidence of authorship.

<small>Tags: [ethics-legal] · Verification: verified · Cluster 08</small>

### `tennessee2024elvis` — ELVISAct — Tennessee ELVIS Act (Ensuring Likeness Voice and Image Security), signed 21 Mar 2024, effective 1 July 2024

*Tennessee General Assembly / Gov. Bill Lee; first U.S. state law updating right of publicity to cover **voice** (incl. simulations) against unauthorised AI clones; followed by similar bills in other states and federal NO FAKES Act proposals (2024–25).*

Links: https://www.tn.gov/governor/news/2024/3/21/photos--gov--lee-signs-elvis-act-into-law.html

Civil liability for unauthorised use of an individual's voice/likeness and for distributing tools whose primary purpose is producing such replicas.

**Evidence.** Legislation.

**For the studio.** Any voice-rendering feature must use consented/licensed voice models (Kits.ai-style) or synthetic voices.

<small>Tags: [ethics-legal] [expression-performance] · Verification: partial · Cluster 08</small>

### `usco2025part2` — USCOReports — U.S. Copyright Office, *Copyright and Artificial Intelligence* Parts 1–3; Perlmutter dismissal

*USCO (Register Shira Perlmutter). Part 1 *Digital Replicas* (31 July 2024); **Part 2 *Copyrightability* (29 Jan 2025)**; **Part 3 *Generative AI Training* pre-publication (9 May 2025)**; Perlmutter removed by the White House 10 May 2025 (litigation over the removal followed); final Part 3 not confirmed published as of Sept 2026.*

Links: https://www.copyright.gov/ai/ ; https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf

Part 2: prompts alone do not confer authorship; **human-authored expressive inputs, creative selection/arrangement, and modifications of AI output are protectable** to the extent of the human contribution; case-by-case. Part 3: training on copyrighted works is prima facie reproduction; fair use depends on transformativeness and market effects — likely fair for research/non-substitutive uses, **unlikely where outputs compete with the training works** or data was obtained illegally; endorses voluntary licensing markets.

**Evidence.** Policy reports (not binding law) but heavily cited by courts and litigants.

**For the studio.** Part 2 is the strongest argument for the studio's design: notation written, edited and arranged by the composer, with AI as a tool, yields a *copyrightable* work; text-to-song outputs generally do not.

<small>Tags: [ethics-legal] · Verification: partial (dates from multiple secondary sources) · Cluster 08</small>

### `umg2025udio` — UMGUdio — UMG–Udio settlement and licensed platform (29 Oct 2025)

*Universal Music Group & Udio; announced 29 Oct 2025; first partner agreements (publishers etc.) Nov 2025.*

Links: https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/

Compensatory settlement (undisclosed) + recorded-music and publishing licences; a **2026 subscription platform** in a "walled garden" (no downloads, fingerprinting/filtering), artist/songwriter opt-in and revenue; Udio's current product continues with tightened controls (downloads disabled).

**Evidence.** First settlement in the RIAA cases; strong user backlash; antitrust commentary.

**For the studio.** Sets the template — licensing in exchange for containment — that the rest of the industry (WMG–Suno) followed.

<small>Tags: [ethics-legal] [product] · Verification: verified · Cluster 08</small>

### `wmg2025suno` — WMGDeals — Warner Music Group settlements: Udio (19 Nov 2025), Stability AI partnership (19 Nov 2025), Suno (25 Nov 2025)

*WMG (Robert Kyncl) with Udio, Stability AI and Suno, Nov 2025.*

Links: https://www.musicbusinessworldwide.com/warner-music-group-settles-with-suno-strikes-first-of-its-kind-deal-with-ai-song-generator/ ; https://musically.com/2025/11/19/wmg-becomes-second-major-label-to-sign-a-deal-with-stability-ai/

WMG–Suno: Suno to launch **licensed models in 2026 and deprecate current ones**; artist **opt-in** for name/image/voice/compositions; **free tier cannot download** (play/share only), paid tiers get monthly caps with paid top-ups; Suno buys Songkick. WMG–Udio: licensed platform (mirrors UMG deal). WMG–Stability: co-develop "responsible" pro tools trained on licensed data.

**Evidence.** Suno implemented the caps on 3 Sept 2026 (see Suno entry).

**For the studio.** Confirms the direction: licensed audio generation = constrained ownership. The studio's differentiator is user-owned symbolic output.

<small>Tags: [ethics-legal] [product] · Verification: verified · Cluster 08</small>

## C3. Context: ethics, provenance & disclosure

### `deezer2026aistats` — DeezerStats — Deezer AI-content statistics 2025–2026

*Deezer newsroom: Jan 2025 ~10% of daily deliveries fully AI (~10k/day); Apr 2025 18% (20k/day); Sept 2025 28% (30k/day); **12 Nov 2025 34% (50k/day)**; **Apr 2026 44% (75k/day)**; **21 July 2026: >50% at peak in June 2026 (~90k/day)**; 13.4M AI tracks tagged in 2025.*

Links: https://newsroom-deezer.com/2026/07/ai-music-exceeds-50-percent-daily-uploads-deezer/ ; https://newsroom-deezer.com/2026/04/ai-generated-tracks-represent-44-of-new-uploaded-music/

Deezer's proprietary detector (claimed 99.8% accuracy, <1 false positive per 10k) tags fully-AI albums, **labels them to listeners (since June 2026)**, excludes them from algorithmic/editorial recommendation, and removes fraudulent/idle AI tracks. AI tracks draw only 1–3% of streams; **~85% of their streams are fraudulent**.

**Evidence.** Platform telemetry (self-reported).

**For the studio.** Quantifies the flood the studio positions against, and shows that *disclosure + demotion* is now normal — human-authored provenance is an asset.

<small>Tags: [ethics-legal] [product] · Verification: verified · Cluster 08</small>

### `newtonrex2024fairlytrained` — FairlyTrained — Fairly Trained certification and Ed Newton-Rex's resignation from Stability AI

*Ed Newton-Rex resigned as VP Audio at Stability AI 15 Nov 2023 over the company's fair-use stance on training; launched non-profit **Fairly Trained** 17 Jan 2024 (Licensed Model certification; standards tightened 2025).*

Links: https://www.fairlytrained.org ; https://ed.newtonrex.com/blog/launching-fairly-trained

Certifies generative models trained only on licensed, public-domain, or consented data (e.g., Beatoven, Soundful, Tuney, Kits.ai, LANDR, Endel, Lemonaide among early certified companies; Stable Audio Open's data would qualify).

**Evidence.** Certification list; industry recognition.

**For the studio.** A concrete external standard the studio could meet for any released model.

<small>Tags: [ethics-legal] · Verification: partial · Cluster 08</small>

### `herndon2021hollyplus` — ArtistPositions — Artist-led positions: Holly Herndon's Holly+ and Spawning; Dadabots

*Holly Herndon & Mat Dryhurst (Holly+, 2021; Spawning / "Have I Been Trained?", 2022–); CJ Carr & Zack Zukowski (Dadabots; "Generating Albums with SampleRNN to Imitate Metal, Rock, and Punk Bands," MUME 2018, arXiv 1811.06633)*

Links: https://holly.plus ; https://spawning.ai ; https://dadabots.com ; https://arxiv.org/abs/1811.06633

Practising artists' models of consent and co-creation: Holly+ offers a voice model of Herndon under a DAO-governed licence so others can *co-create with her identity*; Spawning builds consent/opt-out infrastructure for training data; Dadabots run raw-audio models as a "band," publishing 24/7 generated streams and arguing for AI as a new genre/instrument rather than a replacement.

**Evidence.** Artist practice and public writing; no formal studies.

**For the studio.** Articulates what leading artists want from AI — consent, identity control, and AI as instrument — useful positioning for an open, composer-centred studio.

<small>Tags: [ethics-legal] [product] [audio-generation] [history] · Verification: partial (well-known projects; pages not fetched in this session) · Cluster 05</small>

### `usdoj2024smith` — SmithFraud — United States v. Michael Smith (S.D.N.Y.): AI-generated streaming fraud

*Indicted 4 Sept 2024 (wire fraud, money laundering; ~$10M alleged, 2017–2024); **pleaded guilty 19 Mar 2026** to conspiracy to commit wire fraud ($8.09M); sentencing set 29 July 2026 (outcome not verified).*

Links: https://www.aimusicpreneur.com/ai-music-news/michael-smith-ai-streaming-fraud-guilty-plea-2026/

Hundreds of thousands of AI-generated tracks (many sourced at up to 10k songs/month; hundreds credited to Boomy's CEO as co-writer) streamed by ~1,040 bot accounts (~661k fake streams/day) across Spotify, Apple, Amazon, YouTube; detected by the Mechanical Licensing Collective in 2023, not by the DSPs.

**Evidence.** First U.S. criminal case of AI-music streaming fraud.

**For the studio.** Illustrates the misuse mode of one-shot mass generation; a composer-centric studio has no comparable attack surface.

<small>Tags: [ethics-legal] · Verification: verified · Cluster 08</small>

### `newtonrex2024statement` — StatementAITraining — "Statement on AI training" (22 Oct 2024)

*Organised by Ed Newton-Rex; launched with ~10,500 signatories (Björn Ulvaeus, Thom Yorke, Radiohead, The Cure, Kate Bush, Julianne Moore, Kazuo Ishiguro…), later >50,000.*

Links: https://ed.newtonrex.com/statement-on-ai-training

One sentence: "The unlicensed use of creative works for training generative AI is a major, unjust threat to the livelihoods of the people behind those works, and must not be permitted."

**Evidence.** Signatory count; used in UK Data (Use and Access) Bill lobbying (2025) alongside the silent album *Is This What We Want?* (Feb 2025).

**For the studio.** Signals where much of the creative community stands; a consent-based studio can credibly align with it.

<small>Tags: [ethics-legal] · Verification: partial · Cluster 08</small>

### `epple2024watermarking` — TrainingWatermark — Watermarking Training Data of Music Generation Models

*Pascal Epple, Igor Shilov, Bozhidar Stevanoski, Yves-Alexandre de Montjoye; Imperial College London; arXiv Dec 2024 (rev. 2025).*

Links: https://arxiv.org/abs/2412.08549

Tests whether audio watermarks in training data survive into a music generator's outputs (MusicGen fine-tuning), as a membership/provenance mechanism for rights-holders.

**Evidence.** Watermarks partially detectable in outputs depending on strength/proportion.

**For the studio.** Provenance tooling relevant to dataset governance for an open model.

<small>Tags: [ethics-legal] [evaluation] [audio-generation] · Verification: partial · Cluster 08</small>

### `batlleroca2024mira` — MiRA — Towards Assessing Data Replication in Music Generation with Music Similarity Metrics on Raw Audio (MiRA)

*Roser Batlle-Roca, Wei-Hsiang Liao, Xavier Serra, Yuki Mitsufuji, Emilia Gómez; UPF Barcelona / Sony AI; ISMIR 2024 (arXiv 2407.14364).*

Links: https://arxiv.org/abs/2407.14364 ; https://github.com/roserbatlleroca/mira

Model-independent tool using several audio similarity metrics (CLAP, DEfNet/Discogs-EffNet, CoverID, etc.) to detect *exact* replication of training data in generated audio; validated with controlled synthetic replication across genres.

**Evidence.** Detects exact replication at proportions above ~10%; released for transparency audits.

**For the studio.** Any renderer the studio ships should be audited for memorisation; MiRA is the open baseline.

<small>Tags: [evaluation] [ethics-legal] [audio-generation] [toolkit] · Verification: verified · Cluster 08</small>

### `spawning2022haveibeentrained` — Spawning — Spawning / "Have I Been Trained?" (Holly Herndon & Mat Dryhurst)

*Spawning AI (Herndon, Dryhurst, Jordan Meyer), founded 2022; *Have I Been Trained?* search over LAION-5B (Sept 2022); *Do Not Train* registry / ai.txt (2023); Source.Plus PD/CC dataset platform (2024); Herndon & Dryhurst's *Holly+* vocal deepfake (2021) and *The Call* (2024, Serpentine) as consent-based training artworks.*

Links: https://spawning.ai ; https://haveibeentrained.com

Opt-out infrastructure (registries honoured by Stability, Hugging Face) and an artistic practice of *consensual* dataset creation.

**Evidence.** >1.5 billion opt-outs reported by 2024 (unverified figure).

**For the studio.** Model for consent-first data governance and for artists training on their *own* voices/material — matching the studio's ethos.

<small>Tags: [ethics-legal] · Verification: partial · Cluster 08</small>

### `spotify2025aipolicy` — SpotifyPolicy — Spotify AI policies (25 Sept 2025)

*Spotify (Sam Duboff, Charlie Hellman), 25 Sept 2025.*

Links: https://www.musicbusinessworldwide.com/spotify-has-deleted-75m-spammy-tracks-as-it-unveils-new-ai-music-policies/

(1) **Impersonation policy** — unauthorised AI voice clones removable; (2) **spam filter** against mass uploads, duplicates, SEO tricks, <30-s bait tracks (75M "spammy" tracks removed in the prior 12 months); (3) support for the **DDEX AI-disclosure metadata standard** so labels/distributors credit AI's role in vocals, instrumentation or production. Endorsed by UMG and WMG.

**Evidence.** Policy statement.

**For the studio.** DDEX AI credits are a concrete metadata target for the studio's export ("human-composed; AI-assisted arrangement/rendering").

<small>Tags: [ethics-legal] [product] · Verification: verified · Cluster 08</small>

### `xmader2021musescore` — MuseScore.com scraping — the "musescore-dataset" and its ethics

*Xmader (GitHub), 2020–Sept 2021 (unmaintained); contrasted with PDMX (2024)*

Links: https://github.com/Xmader/musescore-dataset

Unofficial dump of MuseScore.com score metadata, user data and MSCZ files via the site's public API, distributed over IPFS explicitly so that "no one can take it down"; no licence, "at your own risk" warnings. Most scores on musescore.com are user arrangements of copyrighted works; Muse Group's ToS forbids bulk download. Several 2022–2024 symbolic-model papers trained on such dumps without disclosure of terms.

**Evidence.** Repo status confirmed; PDMX authors explicitly cite copyright concerns as motivation and filter to public-domain scores.

**For the studio.** A research-grade open studio should adopt PDMX-style provenance discipline (public domain / CC-only, per-file licence metadata) — both ethically and to keep the door open to commercial adoption.

<small>Tags: [ethics-legal] [dataset] · Verification: verified · Cluster 07</small>

## C4. Context: economics & attitudes

### `apraamcos2024ai` — APRAAMCOS — APRA AMCOS *AI and Music* report (19 Aug 2024)

*APRA AMCOS (Australia/NZ) with Goldmedia; survey of 4,200+ members, May–June 2024.*

Links: https://www.apraamcos.com.au/about-us/news-and-events/ai-in-music-report

38% already use AI; **54% agree AI can assist the creative process**; 82% fear for their livelihood; 65% risks > opportunities; 83% worry about discoverability; 97% want policy action and training-data disclosure; 95% demand permission before use; 23% of revenue at risk by 2028 (AUD 519M cumulative); 89% of Aboriginal & Torres Strait Islander creators fear cultural appropriation. (Ivors Academy/UK Musicians' Union surveys 2024–25 report similar ~⅔ concern levels — partial.)

**Evidence.** Largest member survey of its kind.

**For the studio.** Quantifies the demand for *assistive* AI with consent — the studio's target segment.

<small>Tags: [ethics-legal] [HCI-study] · Verification: verified · Cluster 08</small>

### `cisac2024pmp` — CISACStudy — CISAC/PMP Strategy global economic study (4 Dec 2024)

*CISAC with PMP Strategy; Dec 2024.*

Links: https://www.cisac.org/services/reports-and-research/cisacpmp-strategy-ai-study

Gen-AI music+audiovisual outputs market to reach ~€64bn by 2028 (music ~€16bn/yr); music creators risk losing **24% of revenues by 2028** (cumulative ~€10bn) via substitution and unlicensed training; calls for licensing and transparency.

**Evidence.** Economic modelling.

**For the studio.** Same as above; global scope.

<small>Tags: [ethics-legal] · Verification: partial · Cluster 08</small>

### `deezer2025ipsos` — DeezerIpsos — Deezer/Ipsos survey: 97% cannot tell AI from human music

*Deezer & Ipsos Digital; 9,000 adults in 8 countries, fielded 6–10 Oct 2025, published 12 Nov 2025.*

Links: https://newsroom-deezer.com/2025/11/deezer-ipsos-survey-ai-music/

Blind listening + attitudes: 97% failed to distinguish fully-AI tracks; 71% surprised; 52% uncomfortable; 80% want labelling; 70% see a threat to musicians' livelihoods; 65% oppose training on copyrighted material.

**Evidence.** Large-N cross-national survey (industry-commissioned).

**For the studio.** Public appetite for disclosure/labelling and for human authorship — supports provenance metadata as a studio feature.

<small>Tags: [evaluation] [ethics-legal] [HCI-study] · Verification: verified · Cluster 08</small>

### `goldmedia2024gemasacem` — GEMASACEM — GEMA/SACEM × Goldmedia study *AI and Music* (30 Jan 2024)

*Goldmedia GmbH for GEMA and SACEM; published Jan 2024; survey of ~15,000 members.*

Links: https://www.gema.de/en/news/ai-study ; https://www.goldmedia.com/fileadmin/goldmedia/Studie/2023/GEMA-SACEM_AI-and-Music/AI_and_Music_GEMA_SACEM_Goldmedia.pdf

Forecasts the generative-AI music market at ~$3bn by 2028 and **27% of creators' revenues at risk by 2028**; 35% of members already use AI; 71% see risks > opportunities; 95% want disclosure of training data; GEMA later proposed a two-pillar licensing model for AI (Sept 2024).

**Evidence.** Member survey + market model.

**For the studio.** Establishes the economic framing collecting societies use; the studio's positioning (assist human members) is compatible with GEMA's stance.

<small>Tags: [ethics-legal] · Verification: partial · Cluster 08</small>

## X. X

### `nokey-08-ProductTable — Other` — ProductTable — Other tools (summary table)


<small>Verification: n/a · Cluster 08</small>

### `nokey-08-EthicalFooting — Why` — EthicalFooting — Why a symbolic-first, human-authored studio has a different ethical footing (synthesis note)

*Synthesis of the above (this document).*

Links: —

(1) **Authorship/copyrightability:** outputs are notation the composer wrote, selected, arranged and edited → protectable under USCO Part 2 / Thaler line; text-to-song outputs largely are not. (2) **Training data:** symbolic corpora with clean provenance exist (PDMX, JSB, Nottingham, TheoryTab-style consented analyses, the composer's own works), whereas SOTA audio models are trained on commercial recordings now judged infringing in Germany. (3) **Memorisation:** symbolic models trained on PD data cannot reproduce protected recordings; style learned from *the user's own* sketches (OMax/Continuator lineage) sidesteps the pastiche problem. (4) **Voice/likeness:** render vocals via consented singing synthesis (SynthV/ACE/Kits) or none — ELVIS Act compliant. (5) **Disclosure:** emit DDEX AI credits / provenance logs by default. (6) **Market substitution:** the studio increases human output rather than substituting for it, aligning with GEMA/CISAC/APRA member preferences (54% want assistive AI). Residual risks: style imitation of living composers, use of transcribed-from-audio corpora (Aria-MIDI), and any bundled audio renderer's training data.

**Evidence.** See cited entries.

**For the studio.** This is the ethics section of the manifesto/literature review.

<small>Tags: [ethics-legal] [notation] [symbolic-generation] · Verification: synthesis · Cluster 08</small>
