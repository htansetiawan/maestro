# Music Anatomy

An interactive research atlas for ACE-Step 1.5, created October 5, 2026.

Public guide: https://htansetiawan.github.io/maestro/anatomy/

From this directory, run:

```bash
python3 -m http.server 8765
```

Visit `http://localhost:8765`. The GitHub Pages entry point is `index.html`; its assets are in `dist/`. The site has no application dependencies or model backend.

## Included

- Task-aware, six-stage ACE-Step pipeline explorer, with mechanism, tensors/math, code boundaries, and research opportunities.
- Representation-rate calculator and explicitly synthetic visualizations.
- Browser numerical flow-matching illustration with seeded noise, Euler/Heun integration, guidance, and an interval mask.
- Small monophonic score compiler with validation, typed event/performance IRs, transposition, oscillator playback, and real MIDI / MusicXML export.
- Model training overview, a trace of the committed piano/vocal experiment, and a research path toward symbolic conditioning.
- Linked primary sources, pinned code revisions, configuration provenance, and an explicit distinction between implementation, illustration, and proposed research.

The symbolic example is hand-authored; it is not a piano transcription. The website does not run ACE-Step, analyze uploads, or claim to disclose Suno's private architecture.

The audio uses the existing experiment's published mix and a newly encoded MP3 listening copy of its vocal WAV. No pitch correction or retiming was applied.

GitHub Pages serves the repository root from `main`. The guide is linked from the Maestro homepage.

The optional private Sites copy uses `.openai/hosting.json` and `dist/` as its static directory.
