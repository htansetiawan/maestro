# Music Kitchen: From a Piano Idea to Your Own Song

**Product promise:** Play the part you know. Shape the rest by listening, demonstrating, and choosing.

Music Kitchen is a personal arranging studio for people who have musical ideas and taste but cannot perform, arrange, and produce every instrument. A pianist-songwriter can bring piano and lyrics, hear a band develop around them, and direct the arrangement through playing, humming, tapping, examples, simple controls, and occasional language. The product succeeds when the person completes music they recognize as their own and wants to keep making more.

This product direction governs the earlier [research proposal](MUSIC-KITCHEN.md). Research is supporting work undertaken when a concrete product behavior cannot be delivered reliably with existing methods. A DSL, notation system, new model, or interpretability study earns its place by improving the musical experience. None is a required customer-facing centerpiece.

**The initial customer is the pianist-songwriter who wants an arranger and a band.** The motivating example is an aspiring retirement composer who wants to concentrate on piano and lyrics while developing an original musical voice informed by favorite recordings and artists, including Dave Grusin, David Foster, David Benoit, Lee Ritenour, and Kahitna. The product should welcome both experienced musicians and people whose ear is ahead of their technical vocabulary. It need not assume that either group can already name the chords or explain a desired orchestration.

The customer’s job is: “Help me develop this piano-and-vocal idea into an arrangement I love, and let me change what bothers me without learning every instrument or rebuilding the whole song.” The primary output is a revisable song project, with a listenable demo and separate parts. Notation is an optional view or export. Commercial hit potential is an aspiration; it cannot be promised or sensibly used as the first product validation metric.

**A target session starts with music.** The composer records a verse and chorus on piano, adds lyrics, and optionally sings a rough melody. They identify which recordings should be preserved and which are sketches the system may interpret. Music Kitchen retains the source takes and proposes a section map, pulse, and harmonic reading. The composer can correct an interpretation by replaying, choosing between audible alternatives, or editing a label. It should ask about uncertainty only when the answer materially affects the next musical step.

The composer selects a reference passage and indicates what they like about it: its bass movement, drum pocket, string entrance, harmonic color, or broad sense of space. The system uses those references to propose a restrained arrangement around the supplied material. Bass, drums, and other generated instruments occupy separate tracks. The piano and lyric draft remain identifiable, and a sung melody constrains where the accompaniment leaves room.

The composer listens. The bass is attractive but too active under the verse. They select the verse’s bass track, tap a simpler rhythm, and keep its current sound. The drums need a different feel: they tap or beatbox the intended pattern over the phrase. The strings should enter later: they drag the entrance marker to the next line of lyrics. Each interaction previews a scoped revision, with easy comparison to the previous version.

Later, they sing a new response phrase and assign it to guitar, leaving the vocal melody intact. They compare two chorus arrangements, keep one, and return the next day to finish the bridge. The saved project contains the accepted parts, source recordings, references, and decisions needed to continue. The product value spans the whole loop: starting, hearing, directing, revising, and returning.

**Multimodality means being able to correct the system musically.** Supporting several upload types is only the beginning. The important behavior is attaching a demonstration to a particular part, moment, and intended change.

| What the composer wants | Natural interaction | Proposed system behavior |
|---|---|---|
| “The bass should move like this.” | Select bass and hum or play a phrase. | Offer a bass interpretation with appropriate register and timing; preview before replacement. |
| “This is the groove.” | Tap or beatbox over the passage. | Propose a drum pattern from the demonstration; expose ambiguities in instrument assignment through alternatives. |
| “I like this bass rhythm, but keep our notes.” | Mark a reference passage and select rhythm as the influence. | Adapt rhythmic organization while preserving the selected pitch commitments. |
| “The strings should bloom here.” | Point to a lyric line and draw an energy curve. | Propose entry, dynamics, register, and density changes, with audible alternatives for ambiguous interpretations. |
| “That section is too busy.” | Select the accompaniment and move a density control. | Reduce activity in that region without silently rewriting protected piano or vocal material. |
| “Keep this moment.” | Pin a phrase or performance. | Preserve the selected musical material during subsequent revisions. |
| “A has the right feel, B has the better ending.” | Mark preferred regions in an A/B comparison. | Propose a combined version and make any transition repair audible and reversible. |
| “I cannot explain it yet.” | Choose between two contrasting short previews. | Narrow the immediate choice without requiring a verbal theory of the desired mood. |

These are intended capabilities, not claims that current models can reliably perform each operation. Demonstration itself can be ambiguous: a hummed phrase might specify pitch, rhythm, contour, or an expressive gesture. Selection and a lightweight “use rhythm / use notes / use both” choice can resolve more than an open-ended conversation.

**Musical influences should become a personal reference collection.** The named artists are starting points for the composer’s taste, not fixed presets or interchangeable definitions of a genre. Ask the person to identify actual passages and what attracts them. A reference might contribute harmonic movement, another rhythmic feel, and a third the way instruments enter around a melody. The system should make those contributions separable and revisable wherever supported.

For example, a collection might contain a piano passage the composer enjoys, a bass groove, a string entrance, and one of the composer’s own previous songs. The product proposes interpretations and lets the composer correct them through sound. Over time, it can retain explicit preferences such as “leave the verse sparse” or “offer lyrical bass responses between vocal phrases.” One accepted suggestion should not silently become a permanent style rule.

“DNA” is a useful metaphor for influence but not a technical control by itself. A product hypothesis is that users benefit from transferring selected musical qualities into their own material. Whether a system can separate those qualities reliably is a question for prototypes and listening tests. A percentage blend of artist names would imply a precision the product has not established.

**The visible workspace should stay simple.** A first interface can have a recording area, a timeline with separate instrument lanes, a lyrics view, a small reference tray, and a contextual editing panel. Selecting a passage reveals actions such as play a replacement, demonstrate rhythm, compare takes, preserve this, or simplify. The composer should be able to make a successful correction without opening a chat window.

Use progressive disclosure for technical information. At the surface: the original and proposed sound, the selected region, and a brief statement of the change. On request: notes, chord alternatives, timing, articulation, and why a particular constraint could not be honored. A composer who wants to learn can inspect the musical explanation. Someone who wants to continue playing can simply audition and act.

Interpretability serves practical questions: “What did you hear me do?”, “What are you changing?”, “What will stay?”, and “How do I fix this?” A readable operation record is useful evidence about the edit. It is not proof that the model understood an emotion. Audio comparison must remain central.

**Existing products set a serious baseline.** This snapshot was checked against first-party documentation on September 10, 2026; the capabilities below are documented vendor claims, not hands-on test results.

| Existing product | Relevant documented capability | What to test before building an alternative |
|---|---|---|
| Logic Pro | Session Players follow chords and can follow another track’s rhythm. Logic Pro 12 adds Chord ID for audio or MIDI regions. [Session Players](https://support.apple.com/en-gb/guide/logicpro/lgcpbf624405/mac), [rhythmic following](https://support.apple.com/en-sg/guide/logicpro/lgcpca8dca3d/mac), [Logic Pro 12](https://support.apple.com/en-il/guide/logicpro/lgcp4a62a494/mac) | How much work does a piano songwriter need to get, understand, and revise a suitable accompaniment? |
| Moises | Advertises generation of separate instruments around audio or MIDI, reference-audio conditioning, and selected-region generation. [Stem Generation](https://moises.ai/features/stem-generation/) | Can users make a precise second or third correction by demonstration while retaining accepted material? |
| Suno Studio 2.0 | Supports MIDI recording/editing and MIDI clips as generation prompts, alongside chat, stems, and automation. [August 2026 announcement](https://suno.com/blog/studio-2) | How reliably can a user preserve authored details and direct individual musical relationships across revisions? |

The proposed opportunity is a coherent interaction loop for directing accompaniment by demonstration and reference. This is a differentiation hypothesis, not a claim that competitors lack every part of that loop. If existing products already satisfy the target session, Music Kitchen should integrate with them or narrow its focus to a demonstrated difficulty.

**The underlying system should combine musical tools with AI interpretation.** A useful internal project state includes source audio, performed events, musical sections, tentative harmonic analyses, reference passages, generated parts, and protected decisions. It needs to retain distinctions between exact source material and inferred descriptions. Audio preserves performance detail that a coarse symbolic representation can discard; symbolic events provide precise handles for supported edits. Neither representation alone should be presumed sufficient.

The AI companion translates a situated request into a bounded proposal: where to work, which musical property to alter, which engine to use, and what to preserve. Existing signal-processing tools estimate timing, pitch, or stems; arrangement methods propose parts; samplers and synthesis render performances; validators check supported constraints. Some timbral or expressive tasks may warrant generative audio. The appropriate engine depends on the intended edit.

The DSL, if needed, is an internal agreement between these components. It can represent “change the drum rhythm in this phrase, retain the sound, preserve these accents.” It should emerge from real editing tasks rather than begin as an ambitious universal language for all music. A legible serialization may help debugging and advanced use, but customer value does not depend on exposing code.

Modern AI can help connect disciplines and reduce the expertise required to use their tools. Its knowledge must still be grounded in the actual project and actual audio. Describing syncopation correctly does not demonstrate that the generated rhythm is appropriate; generating valid code does not demonstrate that it edited the intended track. The execution layer must verify what it can and provide audible evidence for what remains musical judgment.

**The first build should deliver one complete musical loop.** Target a 30–60 second piano passage with optional sung melody and lyrics. Preserve the source piano. Generate separate bass and drum parts, then support one demonstration-based bass correction and one rhythmic correction to drums. Save and reopen the project, compare previous versions, and export a mix plus individual parts. Strings, guitar responses, and larger song structure are subsequent additions after this loop works.

The first technical spike can use a clean MIDI piano input to isolate arranging and interaction problems. The first customer-facing prototype should also accept recorded piano, or explicitly expose that limitation; otherwise it fails an important part of the intended accessibility. Rough vocals serve as melody and phrasing guides. Generating a polished singer is a separate capability and need not block testing the core product.

Start with asynchronous generation after recording a phrase. Provide immediate playback of existing material and quick previews for direct edits. Measure time until a usable suggestion and time to audible correction; choose acceptable latency targets from sessions with musicians. Continuous real-time accompaniment can follow if musicians need it, since it adds synchronization and latency requirements to an already substantial task.

A sensible sequence is to prototype the interaction using existing musical tools, compare it with current products on the same excerpts, and then automate the most valuable operations. Early sessions may use a human arranger behind part of the workflow, disclosed to participants, to test whether demonstrations communicate intent before treating model performance as the only problem. Such a session validates an interaction concept, not end-to-end automation.

**Research follows an observed product failure.**

| Failure encountered while building | Engineering work to try first | Research question if the failure persists |
|---|---|---|
| The system mistakes a rhythmic hum for literal melody. | Selection context, explicit mode choices, candidate transcription, replay correction. | How can demonstrations be interpreted with minimal interruption? |
| A reference transfers the wrong characteristic. | Let users select source region and intended property; compare candidate transfers. | Can rhythm, harmony, timbre, and phrasing influences be separated reliably? |
| Bass and drums each sound good but clash together. | Shared chord/time state, joint audition, coordinated regeneration. | What representation captures cross-part musical dependence well enough for local editing? |
| Changing one part disrupts an accepted passage. | Scoped operations, preserved assets, event comparisons, version restoration. | How can conditional generation preserve musical commitments across coupled representations? |
| Correct notes sound like an unconvincing performance. | Better sound libraries, articulation mappings, timing and dynamics controls. | Which performance models provide realistic results with usable control? |
| The system responds to every criticism by making the song generic. | Explicit alternatives, contextual preferences, easy reset and branching. | How can personalization learn taste without narrowing exploration prematurely? |
| Users cannot tell how to correct a suggestion. | Better selection, audible contrasts, relevant controls, brief change descriptions. | Which feedback helps people build an effective understanding of the tool? |

**Product validation centers on finished musical progress.** The first milestone is a composer bringing an original piano fragment, obtaining useful accompaniment, making two targeted musical corrections without specialist terminology, and saving a result they want to develop further. This is an acceptance scenario, not a forecast about how long development will take.

Measure how many sessions reach that milestone, how many corrections succeed, whether protected material changes, and whether composers return to continue their own projects. Count time spent repairing mistakes separately from time spent willingly exploring. Record rejected suggestions and the reasons, because an arrangement can be technically correct and artistically unwanted.

Initial customer interviews and trials should test willingness to pay for the completed workflow, not enthusiasm for an AI demo. Track the cost of completed useful sessions, including rejected generations, before committing to pricing. Potential defensibility lies in excellent interaction, dependable musical execution, and a consented body of real correction examples; it does not follow automatically from having a chat interface or a new DSL.

The immediate deliverable is a believable session in which a pianist can direct a small band through musical examples and hear the intended correction. A research project becomes justified when a recurring obstacle to that session survives good engineering and existing methods.
