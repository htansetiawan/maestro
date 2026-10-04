# Music Kitchen: Executable Musical Intent for Human–AI Co-Creation

The governing direction is now the [Music Kitchen product brief](MUSIC-KITCHEN-PRODUCT.md): a personal arranging studio for pianist-songwriters, with research driven by obstacles to the intended experience. This document supplies supporting literature and optional research questions; its study-first sequence is not the product roadmap.

Music Kitchen proposes a composition environment in which people express musical ideas through humming, playing, sketching, notation, and language; an AI companion helps translate those ideas into an editable musical specification; and a music engine realizes that specification for listening and revision. The composer controls what is committed, what remains ambiguous, and where the system may contribute. The central research question is whether making musical intent **persistent, executable, and contestable** improves composers’ ability to realize and develop their own ideas.

The broad ambition has substantial precedent. Musical programming, interactive machine learning, constrained generation, multimodal songwriting, and AI assistants inside music software are established research directions. The promising contribution is therefore a particular representation and interaction contract, tested against strong alternatives. A defensible hypothesis is that a composer-owned specification, coupled to bounded generation and verifiable feedback, can improve control, understanding, and expressive exploration. This is a proposal, not a claim of demonstrated effectiveness or first invention.

This focused literature synthesis covers sources available through September 10, 2026. It emphasizes primary research and original system documentation, distinguishes published research from preprints, and concentrates on composition and revision. It is not an exhaustive systematic review. The proposed initial population is composers and songwriters who can recognize and revise musical ideas, including people who do not read staff notation or program. Live ensemble performance and unrestricted full-song production are extensions beyond the first experiment.

The relevant research term is **human–AI music co-creation**, or **AI-assisted composition** when the human’s creative authority is central. “Procreation” is unlikely to communicate the intended research area. The conductor metaphor is useful for delegation, but it should not assume that a complete piece already exists in the composer’s head. The environment must support both realizing an existing idea and discovering an idea through making and listening.

**The argument from prior work begins with a distinction between musical capability and creative interaction.** Music Transformer demonstrated long-range symbolic generation using efficient relative attention, including motif continuation and melody-conditioned accompaniment. Those capabilities provide musical material and context sensitivity; they do not by themselves establish an interface for precise revision or explain the composer’s experience. Its relevant publication history is the 2018 preprint and ICLR 2019 paper. [1](https://arxiv.org/abs/1809.04281)

Coconet, described in *Counterpoint by Convolution*, models completion of partially specified music and iterative revision. DeepBach similarly makes user constraints part of generation. These are particularly relevant ancestors because a composer often knows scattered parts of a piece before knowing the intervening material. Music Kitchen should inherit this capacity to work around existing decisions. [2](https://arxiv.org/abs/1903.07227) [3](https://proceedings.mlr.press/v70/hadjeres17a.html)

The HCI evidence is unusually close to the proposal. Cococo’s steering tools let novices restrict generation to voices and regions, adjust example-based and semantic controls, and compare alternatives. Its study with 21 novices reported improvements in control, comprehension, and ownership. The AI Song Contest study examined 13 teams comprising 61 participants and identified needs for more decomposable, steerable, interpretable, and adaptive tools. Neither establishes that a DSL is necessary, but both motivate studying the relationship between the scale of machine intervention and human agency. [4](https://ceur-ws.org/Vol-2848/HAI-GEN-Paper-1.pdf) [5](https://program.ismir2020.net/static/final_papers/167.pdf)

*Expressive Communication* provides an especially useful evaluation model: assess composers’ experience alongside listeners’ judgments of whether the resulting music expresses the intended imagery. Its study with 26 composers found complementary benefits from better steering interfaces and more expressive models. It does not justify a universal claim that interface quality matters more than model quality. For Music Kitchen, model quality should be held constant when testing interface mechanisms. [6](https://arxiv.org/abs/2111.14951)

| Research line and selected sources | What already exists | Implication for Music Kitchen |
|---|---|---|
| Graphical composition: Hyperscore, 2004 | Sketches and graphical structures mediate composition for people with limited musical training. [7](https://opera.media.mit.edu/papers/IEEE2004.pdf) | Musical intent can be expressed without either prose or typed code. |
| Musical programming: OpenMusic | Visual programs combine musical objects and transformations; the maquette organizes them in time. [8](https://openmusic-project.github.io/openmusic/overview.html) | An executable musical representation is established prior art. |
| Interactive machine learning: Fiebrink and Caramiaux, 2016 preprint | Treats learning algorithms as creative interfaces shaped by musicians’ goals and interaction. [9](https://arxiv.org/abs/1611.00379) | The feedback loop must accommodate personal meanings and changing goals. |
| Symbolic infilling: Anticipatory Music Transformer, 2023/2024 | Generates around fixed control events, supporting accompaniment and infilling. [10](https://arxiv.org/abs/2306.08620) | A plausible generation substrate for preserving authored material. |
| Performance control: MIDI-DDSP, ICLR 2022 | Exposes a hierarchy of notes, performance attributes, and synthesis parameters. [11](https://arxiv.org/abs/2112.09312) | Editable notes alone do not capture expressive performance. |
| Controlled audio: MusicGen, 2023; JASCO, 2024 | MusicGen supports text and melodic conditioning; JASCO combines temporal symbolic and audio conditions, including chords, melody, and drums. [12](https://arxiv.org/abs/2306.05284) [13](https://arxiv.org/abs/2406.10970) | Avoid claiming that audio generation has no control. Study the strength and reliability of particular controls. |
| Language and symbolic music: ChatMusician, Findings of ACL 2024 | Uses text-compatible ABC notation for music understanding and generation. [14](https://aclanthology.org/2024.findings-acl.373/) | Language models producing musical notation are not a new contribution by themselves. |
| Orchestrated tools: Loop Copilot, 2023/2024 | An LLM coordinates specialized music models and maintains shared musical attributes across iterative requests. [15](https://arxiv.org/abs/2310.12404) | “AI as the glue between music tools” has direct precedent. |
| Deployed symbolic assistance: Hookpad Aria, ISMIR 2024 demo / 2025 preprint | Supports continuation, infilling, and melody–harmony generation in a lead-sheet editor; reports 318,000 suggestions and 74,000 acceptances across 3,000 users. [16](https://arxiv.org/abs/2502.08122) | Use an integrated symbolic assistant as a baseline; acceptance does not establish lasting creative value. |
| Multimodal inspiration: Amuse, CHI 2025 | Converts image, text, and audio inspirations into chord suggestions; editable music keywords mediate interpretation. [17](https://arxiv.org/abs/2412.18940) | Editable intermediate interpretation and multimodal musical inspiration also have precedent. |
| DAW assistance: DAWZY, December 2025 preprint | Converts text and speech into reversible REAPER actions and humming into MIDI with Basic Pitch. [18](https://arxiv.org/abs/2512.03289) | A hum-to-code-to-DAW workflow is insufficient as a novelty claim. |
| Structured musical intent: Inspiration-to-Structure, AAAI 2026 | Generates structured musical sections from melodic ideas and language through specialized modeling. [19](https://ojs.aaai.org/index.php/AAAI/article/view/37163) | “Inspiration to musical structure” needs a more specific representation or HCI contribution. |
| Agent-readable representation: Libretto, June 2026 preprint | Uses explicit onsets, voices, bars, and computed structural feedback to support iterative symbolic revision. [20](https://arxiv.org/abs/2606.22708) | A readable music grammar plus an agent revision loop is already close prior art. |
| Text-conditioned lead sheets: MIDI-LLM, August 2026 revision | Adapts an LLM for MIDI and lead-sheet generation/infilling; reports a study with 58 Hookpad Aria users and 4,002 outputs. The source identifies acceptance to ISMIR 2026. [21](https://arxiv.org/abs/2511.03942v2) | Compare against current text-controlled symbolic assistance, not only early text-to-audio systems. |

Several recent sources further narrow the originality claim. *Who Decides How Knowing Becomes Doing?* explicitly studies visible and editable reasoning surfaces in music co-creation. Its September 2025 preprint is relevant to contestability, although the inspected version contains unresolved publication-template fields; its reported findings should be treated as provisional rather than established venue-verified evidence. Music Kitchen cannot claim to introduce contestability into musical AI. [22](https://arxiv.org/html/2509.10331v1)

Chang and Jing’s August 26, 2026 article describes a composer translating auditory judgments into executable sampling constraints and filtering rules through natural-language programming. The work includes a listening experiment, but its generator construction centers on one composer and a small personal corpus. It is direct precedent for the proposed listening-to-rules loop, while leaving room for a comparative study of reusable interaction mechanisms across composers. [23](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1903971/full)

Hawley’s August 2026 preprint investigates hierarchical representations for symbolic music understanding, variation, and inpainting in support of co-creative agents. It strengthens the case for representations at multiple musical scales. Decodability of features from embeddings, however, should not be equated with evidence that a composer understands or can reliably control the system. [24](https://arxiv.org/abs/2608.04378)

**The proposed contribution is an executable agreement about musical intent.** A composition state should include the musical material, the composer’s current commitments, the system’s unresolved interpretations, and the changes currently delegated to AI. This agreement is external to the model, inspectable by the composer, and enforced wherever the engine has a reliable checker. It persists across turns instead of depending on the model remembering a conversation correctly.

Five properties make that agreement testable. First, musical references identify an exact object or region. Second, a constraint distinguishes something that must hold from a preference that can be negotiated. Third, a delegation scope defines the parts and properties the AI may change. Fourth, proposed changes have an observable before/after difference. Fifth, the composer can revise the interpretation or undo the transformation. These are proposed design requirements, not established sufficient conditions for human agency.

“Keep my melody” illustrates why this is a research problem. It could mean preserving exact pitches and rhythms, preserving only melodic contour, preserving phrase identity while allowing ornamentation, or preserving an expressive recording. A system that silently chooses one interpretation can obey its own representation while violating the composer’s intention. Music Kitchen should expose the interpretation when it matters, using playback and concrete alternatives rather than demanding a long formal specification before work begins.

The DSL is therefore best conceived as an underlying representation with multiple editing surfaces. A composer might hum the phrase, circle a note, drag a chord label, and say “make this ending less final.” These actions refer to the same musical objects. Typed code is available for users who benefit from it; graphical editing and auditory demonstration remain complete ways to participate. The research hypothesis is about access to meaningful commitments, not about making every composer become a programmer.

A DSL is neither necessary nor sufficient for human control: direct manipulation can provide precise control, while an inscrutable program can create a new barrier. Its value must be established by the tasks it makes easier. The “compiler” metaphor also needs limits: an underspecified musical request permits many realizations. Deterministic parsing and checking can surround probabilistic proposal generation without pretending that aesthetic interpretation has a single correct compilation.

```text
Humming / playing / sketching / notation / language
                         ↓
       Candidate interpretation, with ambiguity exposed
                         ↕
 Composer-owned musical state and executable constraints
                         ↓
     AI proposes a change within the delegated scope
                         ↓
     Engine checks the change and renders a preview
                         ↓
      Listen + inspect differences + compare versions
                         ↓
        Accept / revise / reject / change the goal
                         ↺
```

This is a proposed architecture. No working Music Kitchen implementation or experimental result is claimed here.

**The representation needs more than a sequence of notes.** Its smallest useful unit is a musical object with a stable identity: a note event, chord, motif, phrase, part, performance gesture, or audio region. Objects need musical-time anchors and links to their source, including the original recording when applicable. Stable identities let a constraint continue to refer to a motif after that motif moves to another bar.

The composition layer stores events and relationships: pitches, onsets, durations, voices, phrase boundaries, chord labels, and repeated or transformed motifs. The performance layer stores timing deviations, articulation, dynamics, and other supported expressive controls. The sound layer identifies instruments, audio material, and processing. MIDI-DDSP’s hierarchy is a useful precedent for separating these levels, although a first prototype need not implement its synthesis architecture. [11](https://arxiv.org/abs/2112.09312)

An additional intent layer stores protected material, preferences, delegation scope, and unresolved hypotheses. “Preserve these note events exactly” is different from “retain the feeling of this performance.” Only the first has an immediately precise checker. Mood words should remain user-interpreted preferences unless grounded in an explicit, editable operational definition. “Tender” must not silently become a universal rule for minor harmony, slow tempo, or low density.

The internal representation need not replace existing interchange formats. It can retain MIDI or notation events and attach intent metadata in a separate document. Import and export should explicitly identify unsupported information. Round-trip preservation is a property to test within a supported feature set, not a blanket promise that every score, performance, and production detail survives arbitrary conversions.

A proposed DSL interaction could look like this. The syntax is illustrative pseudocode; `confirmed_take` refers to a transcription that the composer has already reviewed.

```text
project "Evening sketch" {
  meter = 4/4
  tempo = 84

  motif theme = confirmed_take("hum-01")
  place theme in melody at bars 1..4

  edit accompaniment at bars 1..4 {
    may_change = [chords, voicing, rhythm]
    must preserve(melody.pitch, melody.onset, melody.duration)
    must preserve(all_material_outside_selection)
    prefer fewer_onsets_than(previous_accompaniment)
    prefer mood("tender", reference = "composer-example-02")
    propose alternatives = 3
  }
}
```

The first two requirements are executable invariants over the supported symbolic state. Fewer onsets is measurable, but whether it is musically appropriate remains a judgment. The mood preference is an invitation to explore, not a guarantee. A visible operation record should distinguish these three cases. If no candidate satisfies the hard constraints, the system returns that result and lets the composer decide what to relax.

**A concrete session makes the HCI claim clearer.** A composer hums a four-bar melody. The system presents the recording beside a candidate transcription and flags an ambiguous repeated note. The composer corrects its duration by dragging or singing that moment again. That corrected representation becomes the protected melody; the raw performance remains available so quantization does not erase the original idea.

The composer requests three accompaniments and selects one. Later, they point to the last two bars and ask for a less conclusive ending while preserving the melody. The companion offers explicit interpretations, such as changing the cadence or reducing the final accompaniment’s density. Preview controls let the composer hear those alternatives before committing to either. This interaction exposes the translation from an aesthetic phrase into a musical operation.

After an edit, the feedback might read: “Melody pitches and timing preserved; two accompaniment chords changed; accompaniment onsets reduced from 12 to 8.” Those statements come from checks on the actual changes. “This may feel less settled” is a separate suggestion, supported by a listening comparison rather than presented as an objective fact. Undo restores the preceding project state, including the associated constraints and interpretation.

Basic Pitch demonstrates an accessible audio-to-MIDI route, and DAWZY already uses it for humming. Transcription is nevertheless an estimate of performed events, not direct access to imagined intent. The crucial new experiment would investigate whether reviewing and correcting the transcription helps users express their idea without breaking creative flow. [25](https://engineering.atspotify.com/2022/6/meet-basic-pitch) [18](https://arxiv.org/abs/2512.03289)

**Interpretability should be defined by what the composer can understand and do.** There are at least four distinct targets: understanding the stored musical representation; understanding the operation applied; understanding how a control affects the result; and understanding the internal mechanism of a learned model. A visible DSL primarily addresses the first two. It does not make a neural generator mechanistically interpretable.

Work on explainable generative music has mapped latent dimensions to musical attributes and provided interactive feedback for inspecting their effects. A context-sensitive XAI position paper likewise argues that explanations should fit the audience and setting. These provide foundations for assessing explanations through musical tasks, rather than assuming that a technical visualization is useful because it exposes model information. [26](https://arxiv.org/abs/2308.05496) [27](https://arxiv.org/abs/2309.04491)

Music Kitchen should prioritize three forms of evidence: a semantic diff identifying changed musical objects, a check identifying satisfied or violated commitments, and a controlled listening comparison. For example, hold notes and instruments fixed while varying articulation, then let the composer predict and audition the difference. If the renderer cannot isolate that property, expose the resulting side effects instead of describing the control as independent.

Generated explanations require particular discipline. An LLM can describe the recorded operation, but its prose is not evidence of why its neural network selected a chord. The operation record can establish that a chord changed and that a melody lock held. It cannot establish that the model understood grief or intended a particular emotional effect. Explanation correctness and composer comprehension must be measured separately.

Libretto is a close technical comparison: its representation deliberately abstracts away velocity, microtiming, original timbre, and unpitched percussion while exposing quantized symbolic structure and computed descriptors. A plausible extension is to investigate human-editable commitments across composition and performance, with evaluation centered on composers’ interventions. The mere addition of a grammar or structural feedback would not establish originality. [20](https://arxiv.org/html/2606.22708v1)

**The listening loop is initially interactive search.** A composer listens, notices a mismatch or possibility, and changes the material or the intention. This resembles sequential optimization, but formal reinforcement learning is not required. A frozen generator, explicit constraints, and human selection can support the loop. Early work should test whether the interaction is useful before introducing online model adaptation.

If personalization becomes necessary, a first extension is candidate ranking from explicit comparisons. The composer might prefer accompaniment A to B for this passage while remaining indifferent about their relative value elsewhere. Feedback should therefore include context, the selected region, the current goal, and an option for neither candidate. Accepting a candidate after exhaustion is not a clean positive reward, and rejection may reflect an incorrect interpretation rather than poor music.

A later RL formulation could define state as the project, commitments, and recent feedback; actions as bounded proposals or clarification requests; and reward as feedback on a proposal’s usefulness. Hard constraints should be enforced outside the reward function whenever possible, so an agent cannot trade a forbidden edit for a higher aesthetic score. This is a proposed formulation, not a trained method or a claim that sparse feedback will suffice.

No universal scalar for beauty is required. A composer may want ambiguity, friction, a particular bodily feeling, or an intentionally awkward phrase. Their preferences can change after hearing an unexpected result. The system should allow branching and revising the goal, including explicitly inviting surprise within a selected region. Human control includes deciding when to relinquish detailed control.

**A first prototype should isolate the contribution.** Limit it to four- or eight-bar passages with a melody and a simple accompaniment. Support humming or MIDI import, correction of the input, locking selected note properties, accompaniment generation, one scoped revision operation, version comparison, and export. Add a performance control only if its effects can be rendered and checked consistently. General orchestration, automatic mixing, and full-song generation would obscure the first study’s causal question.

The companion proposes typed operations against the current musical state. A validator checks object references, time boundaries, allowed properties, and invariants before a proposal becomes an accepted edit. The generator fills only the delegated material. A renderer produces a prompt preview from the accepted symbolic and performance state. The interpreter, generator, checker, and renderer should remain separately inspectable so a failure can be assigned to the right stage.

Repeatability requires more than storing a random seed. Preserve accepted generated material, the operation log, relevant model and renderer versions, and references to sound assets. A quick deterministic preview can support composition experiments; a later high-fidelity rendering path can be evaluated separately. Identical notation does not imply identical audio when instruments, performance interpretation, or processing change.

**The study should distinguish actual control from the feeling of control.** Four questions organize the proposed evaluation:

1. Does an editable specification reduce unintended changes and repair effort relative to conversational control over the same engine?
2. Do semantic diffs and constraint checks improve composers’ predictions and error detection beyond a readable musical representation alone?
3. Can people who do not code express and revise commitments through humming and direct manipulation without excessive specification effort?
4. How does the system affect ownership, exploration, and the development of musical intent over repeated use?

Begin with formative sessions involving roughly 6–10 composers or songwriters across relevant skill levels. This is a planning range, not a statistically powered sample. Ask participants to demonstrate actual revisions, including ambiguous requests and corrections that existing tools make difficult. Develop the supported vocabulary from those sessions rather than assuming traditional harmony terminology fits every participant.

The main controlled experiment can compare three conditions using the same generator, renderer, and task materials. Condition A provides conversational instructions and auditioning in an editor. Condition B adds persistent, directly editable musical commitments and scoped generation. Condition C adds verified diffs, compliance feedback, and controlled comparisons. This separates the representation’s contribution from the feedback mechanism’s contribution. All conditions should retain ordinary manual editing and undo, with matched candidate budgets and measured latency.

Use counterbalanced conditions and equivalent but different musical tasks to reduce learning effects. Determine the main sample size from pilot variance and a preregistered minimum effect of interest. Include participant and task effects in analysis, report confidence intervals, and distinguish planned outcomes from exploratory findings. An additional comparison with an established symbolic editor or copilot tests ecological usefulness, but a different engine introduces confounds and should be interpreted accordingly.

| Outcome | Proposed operational measure | Limitation to address |
|---|---|---|
| Commitment preservation | Violations of composer-confirmed protected pitches, timing, regions, and permitted edit properties | A wrong interpretation can pass every checker; evaluate interpretation agreement separately. |
| Revision efficiency | Time and number of corrective actions to an accepted target revision | Faster work is not always better creative work; separate repair from chosen exploration. |
| Locality | Amount of change outside the permitted region or property set | Score preservation does not imply acoustic independence when effects or resonance cross boundaries. |
| Comprehension | Predict which material will change, identify the cause of a mismatch, and choose an appropriate correction | Task accuracy is stronger evidence than self-reported understanding alone. |
| Calibrated reliance | Acceptance of valid suggestions versus detection or rejection of flawed ones in designated diagnostic tasks | More trust is not necessarily an improvement. |
| Expressive success | Composer intent ratings and blinded listener comparisons against an articulated brief | Listener consensus does not define artistic worth or every composer’s goal. |
| Creative experience | Ownership, agency, workload, and accounts of useful surprise or frustration | Self-report should be interpreted with behavior and interviews. |
| Sustained usefulness | Repeated use, retained edits, abandoned branches, and transfer to personal projects | Early novelty and demand effects can inflate a single-session result. |

Keep a bounded revision task and an open composition task separate. The first might require changing an accompaniment while preserving a supplied melody; it supports an objective constraint measure. The second starts with the participant’s own hum or fragment and allows the intention to evolve; it supports inquiry into exploration and ownership. The Expressive Communication approach offers a precedent for connecting composer intent with listener response without treating audio quality as the sole outcome. [6](https://arxiv.org/abs/2111.14951)

Follow the controlled experiment with a small longitudinal deployment in participants’ own projects. Examine whether the representation becomes a useful part of thinking, whether users hide it after learning the tool, and whether explanations interrupt listening. Failure is informative: the DSL might impose too much overhead, meaningful edits might resist formalization, or better control might narrow exploration. These would revise the design claim rather than simply count as usability defects.

**A position paper is a viable first contribution if it delivers an argument reviewers can examine.** The paper should provide the literature comparison above, define the executable agreement, offer detailed interaction scenarios, and specify falsifiable claims. It should explicitly compare against OpenMusic, Cococo, Amuse, DAWZY, Libretto, and recent work on editable reasoning and perceptual rules. A broad statement that humans should stay creative would mostly restate existing motivations.

A possible abstract is:

> Human–AI music co-creation requires interfaces through which composers can express incomplete ideas, preserve commitments, and understand the consequences of delegated changes. We propose Music Kitchen, a research framework for representing musical intent as an editable, executable agreement between composer and system. Humming, performance, sketches, notation, and language contribute to a shared representation containing musical material, constraints, preferences, and explicit delegation scopes. An AI companion proposes bounded transformations; an engine checks supported invariants and renders alternatives; and composers revise both the music and its specification through listening. Drawing on musical programming, interactive machine learning, constrained generation, and creativity-support research, we distinguish representation transparency, operation accountability, and model interpretability. We articulate design requirements and an evaluation agenda measuring commitment preservation, correction effort, comprehension, expressive success, and creative agency. The framework treats formalization as a revisable aid to musical thinking and identifies when ambiguity and surprise should remain available to the composer.

The most defensible next contribution is a small system plus evidence for one mechanism: whether executable musical commitments help people preserve and revise their ideas, and whether checked feedback improves their understanding. A position paper can establish the conceptual framework now. Demonstrating that it improves creative work requires the comparative and longitudinal evidence described above.

**Sources and evidence notes.** Dates below identify publication or the inspected preprint version. Linked numbered references above point directly to the corresponding originals. Preprint findings are author-reported and not independent replications. Concept descriptions based on abstracts are used only for scope and capability; the closest overlaps and study interpretations were also checked against full text where accessible.

1. Huang, Cheng-Zhi Anna, et al. *Music Transformer*. 2018 preprint; ICLR 2019. [Original paper](https://arxiv.org/abs/1809.04281).
2. Huang, Cheng-Zhi Anna, Tim Cooijmans, Adam Roberts, Aaron Courville, and Douglas Eck. *Counterpoint by Convolution*. Original ISMIR 2017 work; linked arXiv record, 2019. [Original paper](https://arxiv.org/abs/1903.07227).
3. Hadjeres, Gaëtan, François Pachet, and Frank Nielsen. *DeepBach: a Steerable Model for Bach Chorales Generation*. ICML 2017, PMLR 70, 1362–1371. [Proceedings](https://proceedings.mlr.press/v70/hadjeres17a.html).
4. Louie, Ryan, Andy Coenen, Cheng Zhi Huang, Michael Terry, and Carrie J. Cai. *Cococo: AI-Steering Tools for Music Novices Co-Creating with Generative Models*. IUI 2020 workshop summary of the full CHI 2020 paper, *Novice-AI Music Co-Creation via AI-Steering Tools for Deep Generative Models*. [Accessible workshop paper](https://ceur-ws.org/Vol-2848/HAI-GEN-Paper-1.pdf); [CHI DOI](https://doi.org/10.1145/3313831.3376739).
5. Huang, Cheng-Zhi Anna, et al. *AI Song Contest: Human-AI Co-Creation in Songwriting*. ISMIR 2020. [Proceedings paper](https://program.ismir2020.net/static/final_papers/167.pdf).
6. Louie, Ryan, Jesse Engel, and Cheng-Zhi Anna Huang. *Expressive Communication: A Common Framework for Evaluating Developments in Generative Models and Steering Interfaces*. 2021 preprint; IUI 2022 publication. [Full text](https://arxiv.org/html/2111.14951v1); [publication DOI](https://doi.org/10.1145/3490099.3511159).
7. Farbood, Morwaread M., Egon Pasztor, and Kevin Jennings. *Hyperscore: A Graphical Sketchpad for Novice Composers*. IEEE Computer Graphics and Applications, 24(1), 2004. [Author-hosted paper](https://opera.media.mit.edu/papers/IEEE2004.pdf).
8. OpenMusic project. *Overview*. Undated project documentation, accessed September 10, 2026. [Official documentation](https://openmusic-project.github.io/openmusic/overview.html).
9. Fiebrink, Rebecca, and Baptiste Caramiaux. *The Machine Learning Algorithm as Creative Musical Tool*. 2016 preprint for the Oxford Handbook of Algorithmic Music. [Original manuscript](https://arxiv.org/abs/1611.00379).
10. Thickstun, John, David Hall, Chris Donahue, and Percy Liang. *Anticipatory Music Transformer*. 2023 preprint; July 2024 TMLR accepted version. [Original paper](https://arxiv.org/abs/2306.08620).
11. Wu, Yusong, et al. *MIDI-DDSP: Detailed Control of Musical Performance via Hierarchical Modeling*. ICLR 2022. [Original paper](https://arxiv.org/abs/2112.09312).
12. Copet, Jade, et al. *Simple and Controllable Music Generation*. NeurIPS 2023. [Original paper](https://arxiv.org/abs/2306.05284).
13. Tal, Or, Alon Ziv, Itai Gat, Felix Kreuk, and Yossi Adi. *Joint Audio and Symbolic Conditioning for Temporally Controlled Text-to-Music Generation*. JASCO, 2024. [Original paper](https://arxiv.org/abs/2406.10970).
14. Yuan et al. *ChatMusician: Understanding and Generating Music Intrinsically with LLM*. Findings of ACL 2024. [Proceedings](https://aclanthology.org/2024.findings-acl.373/).
15. Zhang, Yixiao, Akira Maezawa, Gus Xia, Kazuhiko Yamamoto, and Simon Dixon. *Loop Copilot: Conducting AI Ensembles for Music Generation and Iterative Editing*. October 2023 preprint, revised August 2024. [Original paper](https://arxiv.org/abs/2310.12404).
16. Donahue, Chris, Shih-Lun Wu, Yewon Kim, Dave Carlton, Ryan Miyakawa, and John Thickstun. *Hookpad Aria: A Copilot for Songwriters*. ISMIR 2024 late-breaking demo; February 2025 preprint. [Original report](https://arxiv.org/abs/2502.08122).
17. Kim, Yewon, Sung-Ju Lee, and Chris Donahue. *Amuse: Human-AI Collaborative Songwriting with Multimodal Inspirations*. CHI 2025. [Full text](https://arxiv.org/html/2412.18940v2).
18. Elkins, Aaron C., et al. *DAWZY: A New Addition to AI powered “Human in the Loop” Music Co-creation*. December 2, 2025 preprint. [Full text](https://arxiv.org/html/2512.03289v1). Capability and evaluation details were checked; the reported 21-person rating study does not establish superiority of an entire workflow under matched experimental conditions.
19. Hu, Zhejing, et al. *Is Symbolic Music a Specific Language? Exploring Inspiration-to-Structure Machine Composition via LLMs*. AAAI 2026, 40(3), 1837–1845. [Proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/37163). Abstract-level capability comparison; its reported creativity scores are not treated as general measures of artistic value.
20. Xu, Yichen. *Libretto: Giving LLM Agents a Sense of Musical Structure*. June 21, 2026 preprint. [Full text](https://arxiv.org/html/2606.22708v1). Representation and evaluation design are close prior art; structural metric performance is not evidence of improved composer agency.
21. Wu, Shih-Lun, Dave Carlton, Ryan Miyakawa, Yoon Kim, Chris Donahue, and Cheng-Zhi Anna Huang. *MIDI-LLM: Improving Text-to-MIDI Music Generation via Adapting Large Language Models*. August 4, 2026 revision; source reports ISMIR 2026 acceptance. [Version inspected](https://arxiv.org/abs/2511.03942v2).
22. Hu, Zhejing, et al. *Who Decides How Knowing Becomes Doing? Redistributing Authority in Human–AI Music Co-Creation*. September 12, 2025 preprint. [Full text](https://arxiv.org/html/2509.10331v1). Relevant conceptual overlap; publication-template placeholders remain in this version, and no venue status is inferred from them.
23. Chang and Jing. *From Perceptual Rule Transformation to Listener Attribution Judgments: A Blind-Listening Experiment on AI-Generated, Human–AI Collaborative, and Human-Composed Music*. Frontiers in Psychology 17, August 26, 2026. [Full article](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1903971/full).
24. Hawley, Scott H. *Helping Music Co-Creation Agents “Listen” Well: Hierarchical Self-Supervised World Models for Understanding and Generation*. August 5, 2026 preprint. [Original paper](https://arxiv.org/abs/2608.04378). Source describes a submission to a future track, not an accepted publication.
25. Spotify Engineering. *Meet Basic Pitch: Spotify’s Open Source Audio-to-MIDI Converter*. June 2022, introducing the ICASSP 2022 transcription research. [First-party technical account](https://engineering.atspotify.com/2022/6/meet-basic-pitch).
26. Bryan-Kinns, Nick, et al. *Exploring XAI for the Arts: Explaining Latent Space in Generative Music*. August 10, 2023 preprint. [Original paper](https://arxiv.org/abs/2308.05496).
27. Privato, Nicola, and Jack Armitage. *A Context-Sensitive Approach to XAI in Music Performance*. September 5, 2023 position-paper preprint. [Original paper](https://arxiv.org/abs/2309.04491).
