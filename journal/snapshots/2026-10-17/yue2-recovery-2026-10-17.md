# October 17 experiment recovery record

The morning Claude session was located locally. Its first request at 07:10 PDT asked for Stable Audio trials, image-score-to-ABC fidelity checks, and a closer investigation of humming and score control. This record describes recovered preparation, not completed experiments.

## Files recovered

| Experiment | Prepared work | Result status at recovery |
|---|---|---|
| `013_score_reading_fidelity` | Scripts to run Audiveris, homr and oemer on the five score pages, compare MusicXML readings with the earlier manual melody, and render a listening comparison. | No OMR outputs or comparison results found. |
| `014_yue2_excerpt_ablation` | Pickup through bar 16: 51 melody notes, 17 chord events, nominal duration 44.32 seconds. Five prepared requests across four conditions. | ABC requests and MIDI files exist; no generated audio or evaluation outputs found. |
| `015_stable_audio_open` | Text-to-audio and audio-to-audio scripts, using a 47-second piano excerpt and several noise levels. | No generated results found; setup logs report missing `stable_audio_tools`. The session also reported gated model access. |

The YuE2 conditions are melody only, melody plus chords, melody plus chords with a constructed bass line, and model-composed music. The melody-plus-chords condition has two seeds; the other conditions have one. The bass is derived from chord symbols, not transcribed from the printed left hand. Putting it into the `Vocal` part is an experimental use of the interface, not verified piano-bass control. Melody-only also changes `cot` mode, so it is not a pure chord-removal comparison.

## Where the session stopped

Runtime setup moved to `~/maestro-runtime/`. The analysis log ends with missing `audioread`; the Stable Audio log reports installation/import failure. A GPU job specification exists, but no queue status file or experiment output was found during recovery. The session records its environment-build wait task as stopped at **08:30 PDT on October 17**. The final assistant message's promise that jobs would proceed is not evidence that they ran.

A separate, unfinished **October 19** journal draft also exists. It is preserved. The October 17 entry records this week's current reading and plans.

## What the score interface tells us

The installed YuE2 workflow describes `Vocal` and `Ins` as monophonic lines, with harmony expressed through chord symbols. Its bounded ABC helper rejects polyphonic note stacks. That is a limitation of this documented input path; it does not establish that every possible YuE2 pipeline has the same limits. [Upstream format reference](https://github.com/multimodal-art-projection/YuE/blob/3d21f8f5d31be867f4c3b2e6beafb0f2e52f8c10/skills/yue2-music/references/abc-editing.md).

Experiment 007 supplied a lead-line/chord reduction, omitting the written accompaniment, lower chord tones and pedal. Those details therefore could not be tested for exact reproduction. It remains unproven why the rendered melody or overall performance sounded wrong.

The manual transcription is a provisional comparison reference, not independently established ground truth. A score-reading test must check it against the image before interpreting disagreement as an OMR error. Likewise, matching saved ABC to input ABC does not measure audible note adherence.

## Planned continuation

1. Verify a short passage from PDF/image through MusicXML and the model's ABC representation, recording omissions and timing changes.
2. Try a separate short sound/humming-to-score path, retaining the raw transcription and human corrections in ABC/MusicXML.
3. Test melody imitation, then an isolated vocal with explicit notes, lyrics and timing. Confirm whether the chosen workflow generates an isolated voice or a mixture before claiming vocal-only output.
4. Add chords, bass and accompaniment only after the simpler cases can be evaluated.

No new model run, dependency installation or queue restart was performed during this recovery.
