# Default caption refresh — September 19, 2026

At Henry's request, refreshed all 28 default captions directly in the local workbench
dataset using the existing per-song librosa and CLAP analysis. These are automatic
annotations, not a new listening review or a new model analysis run.

The caption template now describes detected instrumentation without assuming that the
most frequently detected instrument is the lead. It no longer invents piano when the
instrument list is empty, assumes a pop-ballad genre from vocal detection, treats first
detection as an exact entrance, or describes every loudest section as a gradual build.
An absence of vocal detections is not described as proof that a song is instrumental.

All 28 captions remain editable drafts; the workbench prefills them without the TODO
prefix. Human-written captions are skipped. The original manifest and a per-song
before/after record are backed up under the ignored `data/backups/` directory. Audio,
musical metadata and train/reference assignments were not changed.

The actual manifest at this refresh still has all 28 rows assigned to `train`, despite
the journal's stated 14 instrumental / 14 reference plan. The saved analyses suggest
`reference` for 14 songs with detected vocals. This refresh does not implement that
split or certify that any row is ready for training.

Validation: six caption/analysis tests pass, including missing-instrument cases and
preservation of human captions. The private dataset and audio remain outside Git;
the template correction, tests and this record are versioned.

The running workbench's local authenticated API was checked: it serves all 28 updated
captions and matches the manifest exactly. The public API check returned HTTP 403, so
that external route was not independently verified. No service restart was performed;
the running app reads captions from disk on each request.
