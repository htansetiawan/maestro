"""Build an inspectable note timeline and MP3-only listening comparison."""
from pathlib import Path
import json,html,hashlib
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'inputs/score.json').read_text())
g=json.loads((ROOT/'record/generation.json').read_text())
p=json.loads((ROOT/'record/pitch-check.json').read_text())
a=json.loads((ROOT/'record/lyric-check.json').read_text())
r=json.loads((ROOT/'record/request.json').read_text())
e=html.escape
base='https://raw.githubusercontent.com/htansetiawan/maestro/main/experiments/012_yard_note_control/'
def note(n):return ['C','C♯','D','E♭','E','F','F♯','G','A♭','A','B♭','B'][n%12]+str(n//12-1)
rows='\n'.join(f"| {x['word']} | {note(x['midi'])} | {x['start']:.2f} | {x['end']-x['start']:.2f} |"for x in s['events'])
(ROOT/'README.md').write_text(f'''# 012 — A 25-second note-controlled vocal over the original piano

This experiment separates writing the vocal melody from rendering its voice.
A short line was composed against audio-derived timing anchors from the original
Color Purple piano recording. SoulX-Singer renders explicit notes, English
phonemes and durations. The original piano excerpt is mixed back unchanged.
No sheet music or previous YuE2 score was imported.

## Listen

- [Piano + synthesized singing, 25 seconds]({base}audio/mix.mp3)
- [Singing alone]({base}audio/vocal.mp3)
- [Piano + deterministic note guide]({base}audio/note-guide.mp3) — synthesized tones, not singing
- [Original piano excerpt]({base}audio/piano.mp3)
- [Interactive piano-roll page](index.html) · [Editable score JSON](inputs/score.json) · [MIDI with lyrics](inputs/vocal.mid)

Only MP3 audio is retained and published for this trial. Temporary lossless arrays
are removed after evaluation and successful MP3 validation. Original user sources
and older experiment files are untouched.

## Design

The excerpt covers **1.70–26.70 seconds** of the original 3:30 recording. Eight
phrase anchors were chosen from its onset/CQT evidence. The vocal has 27 notes,
F3–D4, four short lyric lines and explicit phrase-end breathing spaces. Chord
labels are tentative harmonic interpretations of the audio: an F-centered pedal
with major/minor upper-voice changes. They are not a verified chord transcription.
The intermediate note onsets are composed subdivisions between anchors, not a
claim of measured beat-by-beat alignment.

```
{s['lyrics']}
```

English pronunciations come from CMUdict 1.1.1 (one-syllable `our` selected).
The compiled native SoulX metadata supplies word phonemes, MIDI pitches, note
classes and durations on a 20 ms grid. All words here are assigned one syllable
and one note. The syllable map is an actual model input in this experiment.
MIDI uses 120 BPM solely as a seconds-to-ticks carrier; the source's performed
phrase timing is represented by the event timestamps, not a fixed 120 BPM pulse.

## Singer and inference

[SoulX-Singer](https://github.com/Soul-AILab/SoulX-Singer) is used in **score** mode,
with automatic transposition disabled, pitch shift 0, 32 steps, CFG 3 and seed
20261007. A 9.02-second excerpt of experiment 011's synthetic ACE voice provides
timbre conditioning. Its approximate word times come from Whisper-base.en and
word pitches from pYIN; no real singer reference was imported. The reference
annotation is imperfect and may affect output quality.

The model receives this synthetic voice reference and the explicit vocal score.
It does not receive the piano waveform; the designed score carries the intended
musical relationship to the accompaniment. There is no vocal time warping after
synthesis. The native output is exactly 600,000 samples at 24 kHz, or 25 seconds.
It is resampled to 48 kHz to mix with the original stereo piano excerpt.

Model revision `{r['model_revision']}`, code revision `{r['code_revision']}`;
weight SHA256 `{r['model_sha256']}`. Model and vocoder share the official 2.8 GB
checkpoint, retained in the model cache, never Git. The isolated runtime keeps
upstream Transformers 4.41.2 with existing Torch 2.10/CUDA 12.8 for Blackwell;
this differs from the upstream Torch 2.2/Python 3.10 setup and is recorded.
Inference including loading: {g['elapsed_seconds']:.1f} seconds; peak CUDA allocation
{g['peak_cuda_gib']:.2f} GiB. No candidate/seed search was performed.

## Measured results and limits

- pYIN estimated all **{p['notes_median_within_50_cents']}/{p['notes_total']}** notes' median absolute pitch errors within 50 cents.
- Median absolute error over {p['voiced_inner_frames']} voiced inner-note frames: **{p['median_absolute_cents']:.1f} cents**;
  {100*p['voiced_frames_within_50_cents']:.1f}% of these frames are within 50 cents.
- The estimator excludes 120 ms at note edges and can make voicing/octave errors.
  This is pitch evidence, not measured phoneme synchronization or a musical-fit score.
- One-pass ASR: {a['result']['text'].strip()!r}.
  It recovers the four lines with errors; it is not verified lyric ground truth.
- Mix = `piano + {g['vocal_gain']:.9f} × vocal`; overall gain {g['mix_gain']:.1f}.
  Piano timing and level are preserved. Pre-MP3 subtraction recovers the piano
  within {g['piano_recovery_max_error_before_mp3']:.3g}; MP3 adds lossy encoding.
- Mix peak {g['mix_peak']:.4f}. Vocal-only preview gain {g['vocal_export_gain']:.4f} prevents export clipping.
- Musical fit, phrasing and voice quality require listening. No auditory quality
  acceptance or successful piano alignment is claimed from these measurements.

## Inspect or reproduce

[Target metadata](inputs/target-metadata.json), [prompt provenance](record/prompt-provenance.json),
[pitch measurements](record/pitch-check.json), [ASR diagnostic](record/lyric-check.json),
[run request](record/request.json), [generation record](record/generation.json).

The scripts in `record/` prepare audio evidence, reference voice and score, run
inference, evaluate pitch/lyrics and build the page. Use the installed
`/tmp/maestro-soulx-env/bin/python` for score preparation and synthesis; the
existing YuE2 Python environment for Whisper diagnostics. The 25-second piano
and synthetic voice source files from prior experiments must remain available.
`prepare_prompt.py` recreates the temporary reference array;
`generate.py` refuses an existing mix; use a new experiment directory for reruns.
Regenerate before evaluating pitch, because the temporary generated array is
removed after the completed experiment's validation. The score JSON/MIDI and
native target metadata are the editable, persistent representation.

| Syllable | Note | Start in excerpt (s) | Duration (s) |
|---|---|---:|---:|
{rows}
''')
svg=[]
for n in range(52,64):
 y=25+(63-n)*25
 svg.append(f'<line x1="55" y1="{y+12}" x2="1055" y2="{y+12}" stroke="#ecebe8"/><text x="6" y="{y+17}" font-size="12" fill="#777">{note(n)}</text>')
for sec in range(0,26,5):
 x=55+sec*40;svg.append(f'<line x1="{x}" y1="20" x2="{x}" y2="325" stroke="#ddd"/><text x="{x}" y="350" font-size="12">{sec}s</text>')
for i,x in enumerate(s['events']):
 left=55+x['start']*40;y=25+(63-x['midi'])*25;width=(x['end']-x['start'])*40
 label=f"{x['word']}: {note(x['midi'])}, {x['start']:.2f}–{x['end']:.2f}s"
 svg.append(f'<g class="note" data-start="{x["start"]}" data-end="{x["end"]}" tabindex="0" role="button" aria-label="{e(label)}"><title>{e(label)}</title><rect x="{left:.2f}" y="{y}" width="{width:.2f}" height="22" rx="4"/><text x="{left+3:.2f}" y="{y+15}" font-size="10">{e(x["word"])}</text></g>')
svg.append('<line id="cursor" x1="55" x2="55" y1="20" y2="325" stroke="#d04a38" stroke-width="2"/>')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Yard — note-controlled vocal</title><style>
body{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}main{max-width:1100px;margin:auto;padding:40px 22px}h1{font-size:clamp(30px,5vw,44px);line-height:1.2}small,.muted{color:#777}a{color:inherit}audio{width:100%}.players{display:grid;grid-template-columns:1fr 1fr;gap:22px}.player{background:#f7f7f5;padding:16px;border-radius:8px}.player h2{font-size:18px;margin:0 0 8px}.roll{overflow:auto;border:1px solid #e6e5e2;border-radius:8px}.roll svg{width:100%;min-width:760px;display:block}.note{cursor:pointer;outline:none}.note rect{fill:#c8d9cc}.note.active rect,.note:focus rect,.note:hover rect{fill:#86b698}.note text{pointer-events:none;fill:#26382b}section{margin-top:32px;border-top:1px solid #e6e5e2;padding-top:16px}pre{white-space:pre-wrap;font:inherit}.stats{display:flex;gap:16px;flex-wrap:wrap}.stats span{background:#f3f3f1;padding:8px 12px;border-radius:5px}@media(max-width:650px){.players{grid-template-columns:1fr}}
</style></head><body><main><small>MAESTRO · EXPERIMENT 012</small><h1>Write the notes.<br>Then render the singer.</h1>
<p>A 25-second vocal line over the original piano. Every syllable has an explicit pitch and duration.</p>
<div class="players">'''
for key,title in [('mix','Piano + singing'),('vocal','Singing alone'),('note-guide','Piano + note guide'),('piano','Original piano excerpt')]:
 page+=f'<div class="player"><h2>{title}</h2><audio id="{key}" controls preload="metadata" src="audio/{key}.mp3"></audio><a href="audio/{key}.mp3" download>Download MP3</a></div>'
page+='</div><section><h2>The vocal line</h2><p class="muted">Click a note to seek the selected player. Times are relative to the excerpt, which starts at 1.70 seconds in the original recording. The note-guide player uses synthesized tones, not singing.</p><div class="roll"><svg viewBox="0 0 1100 370" aria-label="27-note vocal piano roll">'+''.join(svg)+'</svg></div>'
page+=f'<p><a href="inputs/vocal.mid">MIDI + lyrics</a> · <a href="inputs/score.json">Editable note table</a> · <a href="inputs/target-metadata.json">Actual model conditioning</a></p><pre>{e(s["lyrics"])}</pre></section>'
page+=f'<section><h2>What the measurements show</h2><div class="stats"><span>{p["notes_median_within_50_cents"]}/27 notes within 50 cents at the median</span><span>{p["median_absolute_cents"]:.1f} cents median frame error</span></div><p>Estimated from the generated voice with pYIN, excluding note edges. This checks pitch following; it does not establish good phrasing, lyric timing or a pleasing fit with the piano.</p><details><summary>Speech-recognition diagnostic</summary><p>{e(a["result"]["text"])}</p><p class="muted">One automatic transcription, with errors; not verified lyrics.</p></details></section>'
page+='<section><h2>How it was made</h2><p>Audio onset analysis → composed notes and syllable times → SoulX-Singer score-mode synthesis → original piano + generated voice. A short synthetic ACE vocal supplied the timbre reference. No sheet music imported and no piano time stretching.</p><p><a href="README.md">Full experiment record</a> · <a href="record/pitch-check.json">Pitch measurements</a> · <a href="https://github.com/Soul-AILab/SoulX-Singer">Official SoulX-Singer implementation</a></p></section>'
page+='''</main><script>
const players=[...document.querySelectorAll('audio')];let active=players[0];
players.forEach(p=>p.addEventListener('play',()=>{active=p;players.forEach(q=>{if(q!==p)q.pause()})}));
function seek(note){active.currentTime=Number(note.dataset.start);active.play().catch(()=>{});}
document.querySelectorAll('.note').forEach(n=>{n.addEventListener('click',()=>seek(n));n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();seek(n)}})});
function tick(){const t=active.currentTime;const x=55+40*t;const c=document.getElementById('cursor');c.setAttribute('x1',x);c.setAttribute('x2',x);document.querySelectorAll('.note').forEach(n=>n.classList.toggle('active',t>=Number(n.dataset.start)&&t<Number(n.dataset.end)));requestAnimationFrame(tick)}tick();
</script></body></html>'''
(ROOT/'index.html').write_text(page)
manifest={}
for path in (ROOT/'audio').glob('*.mp3'):
 with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
 manifest[path.name]=dict(bytes=path.stat().st_size,sha256=sha)
(ROOT/'record/delivery.json').write_text(json.dumps(dict(format='MP3 only',files=manifest),indent=2)+'\n')
print('Built note timeline and delivery records.')
