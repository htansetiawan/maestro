# Studio experiment 01: Shape a musical moment

[Open the Music Kitchen studio](../studio/).

The first prototype explores a concrete interaction: select a phrase, express a change through a contour or tapped rhythm, and hear the result while the rest of the arrangement stays fixed. It uses an original eight-bar procedural sketch, editable musical events, and browser synthesis. It is a working interaction experiment, not a trained music-generation model or a finished production tool.

The visual direction is a quiet studio: warm neutral surfaces, generous space, restrained color for each instrument, and a contextual panel for one selected phrase. The product inspiration is the simplicity of modern audio workspaces such as [ElevenLabs Studio](https://elevenlabs.io/studio). The interaction analogy comes from [Meta SAM 3D](https://ai.meta.com/blog/sam-3d/): an explicit selection grounds what the system acts on. The prototype uses neither service and does not reconstruct music from a mixed recording.

The proposed musical equivalent of selecting an object is selecting a meaningful musical region: a bass response, a drum pattern, a melodic phrase, or eventually a relationship between parts. This version supports explicit two-bar regions on separate tracks. Recognizing such objects in arbitrary audio is a separate, unsolved requirement for the larger product.

**What works in this version.** Play or pause the arrangement, select any of sixteen phrases, mute or pin tracks, change tempo, and rename the project. The piano begins pinned. Draw an eight-point contour or use accessible Rise, Fall, and Level buttons; adjust density; tap a rhythm; and apply the transformation to the selected phrase. Before/Now compares versions, and Undo restores the preceding project state.

Project data is saved on the device through browser storage where available. It can also be downloaded as JSON. Audio export renders the current arrangement to a mono WAV file. Uploaded images remain a visual reference for the current visit; they are not sent to a model or saved with the project. The text control recognizes a small documented set of directions—sparse, dense, rising, and falling—and maps them to the same controls.

**The recipe is an executable first sketch of a language.** It describes a transformation at a selected musical scope:

```text
phrase bass [5:6] {
  density 0.25
  contour [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]
  rhythm [0, 3, 8, 12, 16, 23, 28]
}
```

The actual interpreter accepts the four displayed tracks, two-bar ranges 1:2 through 7:8, density from 0.15 to 1, eight contour values from 0 to 1, and rhythm steps from 0 to 31 or `auto`. Rhythm steps divide a two-bar phrase into 32 sixteenth-note positions in 4/4. Pinned tracks reject changes. Unsupported syntax produces an error; it is not passed to a general-purpose code evaluator.

Each instrument interprets those controls according to its role. Bass contour selects pitches from the local chord; drum contour controls hi-hat emphasis. A string contour can shift register. This is deliberately a small mapping, not a universal theory of musical gesture. The mapping’s musical usefulness needs evaluation.

**Notation remains one useful view.** A future representation could also describe relationships: the bass answers a vocal gap, strings follow an energy curve, a motif returns with different orchestration, or a reference contributes only its rhythmic feel. Such relationships are hypotheses for a richer language, not implemented features of this prototype. Traditional notation can coexist with them; replacing it is not a prerequisite for exploring new interaction.

The central idea is that several surfaces can edit the same musical decision: a drawn shape, a demonstration, a textual recipe, a conventional score, and the resulting sound. The prototype connects the first three implemented controls—drawing, tapping, and a small recipe—to explicit events and playback. Humming and learned interpretation remain future work.

**Limits and next tests.** The sound is procedural browser synthesis, with no sampled instrument library, imported piano performance, model-generated accompaniment, automatic source separation, or live microphone transcription. The arrangement uses fixed demo harmony, and the first controls do not claim independent transfer of mood, style, or musical identity. Before/Now is a version comparison, not a blind listening experiment.

The next useful session asks a musician to select an unsatisfactory phrase, demonstrate a change, and decide whether the result matches their intention. Record where the interaction helps and where the mapping breaks down. That evidence should determine whether the next investment is better sound, a different representation, humming input, or more capable arrangement generation.
