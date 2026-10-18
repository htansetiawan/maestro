"""Listening page for the MusicGen-melody and EnCodec round-trip trials."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    p = ROOT / 'outputs' / name
    return {r['label']: r for r in json.loads(p.read_text())} if p.exists() else {}


m_cp, m_she, m_enc = load('measure-cp-30s.json'), load('measure-she-30s.json'), load('measure-encodec.json')
chroma = json.loads((ROOT / 'outputs/chroma.json').read_text()) if (ROOT / 'outputs/chroma.json').exists() else {}


def pct(x):
    return f'{x*100:.0f}%'


def gen(cond):
    p = ROOT / 'outputs' / cond / 'generation.json'
    return json.loads(p.read_text()) if p.exists() else {}


def stats(r, cond=None):
    if not r:
        return ''
    tempo = f'{r["tempo_ratio"]:.2f}×' if r.get('tempo_ratio') else 'n/a'
    ch = f'<span>chroma similarity to its reference <b>{chroma[cond]:.2f}</b></span>' if cond in chroma else ''
    return (f'<div class="stats">{ch}<span><b>{pct(r["melody_recall"])}</b> of written notes in order</span><span>top-line precision {pct(r["skyline_precision"])}</span><span>{pct(r["exact_recall"])} in the written octave</span>'
            f'<span>longest exact run {r["longest_exact_run"]}</span><span>tempo {tempo}</span></div>')


def card(cond, title, note, r):
    g = gen(cond)
    secs = f'{g["audio_seconds"]:.0f} s' if 'audio_seconds' in g else (f'{g["seconds_audio"]:.0f} s' if 'seconds_audio' in g else '')
    return (f'<div class="player"><h2>{title}</h2><p class="muted">{note} · {secs}</p>'
            f'<audio controls preload="metadata" src="outputs/{cond}/audio.mp3"></audio><a href="outputs/{cond}/audio.mp3" download>Download MP3</a>{stats(r, cond)}</div>')


mg = ''.join([
    card('cp-guide', 'MusicGen-melody · Color Purple, from the written melody', 'Melody condition: the synthesized guide of the 17-bar lead line, first 30 s', m_cp.get('cp-guide')),
    card('cp-recording', 'MusicGen-melody · Color Purple, from the recording', 'Melody condition: the pianist\'s recording, first 30 s', m_cp.get('cp-recording')),
    card('cp-text-only', 'MusicGen-melody · text only', 'Same prompt, no melody condition; graded against the Color Purple line as a floor', m_cp.get('cp-text-only')),
    card('she-guide', 'MusicGen-melody · She, from the transcribed vocal line', 'Melody condition: the synthesized guide of the transcribed line, first 30 s', m_she.get('she-guide')),
])
rows = ''
for cond, label in [('encodec24-1.5kbps', 'EnCodec 24 kHz, 1.5 kbps (2 codebooks)'), ('encodec24-3kbps', 'EnCodec 24 kHz, 3 kbps (4)'), ('encodec24-6kbps', 'EnCodec 24 kHz, 6 kbps (8)'),
                    ('encodec24-12kbps', 'EnCodec 24 kHz, 12 kbps (16)'), ('encodec24-24kbps', 'EnCodec 24 kHz, 24 kbps (32)'), ('encodec32-musicgen', 'MusicGen\'s EnCodec 32 kHz, 4 codebooks (≈2.2 kbps)')]:
    r = m_enc.get(cond)
    if not r:
        continue
    rows += (f'<tr><td>{label}</td><td>{chroma.get(cond, float("nan")):.2f}</td><td>{pct(r["melody_recall"])}</td><td>{pct(r["skyline_precision"])}</td><td>{pct(r["exact_recall"])}</td><td>{r["longest_exact_run"]}</td>'
             f'<td><audio controls preload="none" src="outputs/{cond}/audio.mp3"></audio></td></tr>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MusicGen and EnCodec</title><style>
body{{font:17px/1.65 system-ui;color:#37352f;background:#fff;margin:0}}main{{max-width:1100px;margin:auto;padding:40px 22px}}h1{{font-size:clamp(30px,5vw,44px);line-height:1.2}}small,.muted{{color:#777}}a{{color:inherit}}audio{{width:100%}}.players{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}.player{{background:#f7f7f5;padding:16px;border-radius:8px}}.player h2{{font-size:18px;margin:0 0 8px}}section{{margin-top:32px;border-top:1px solid #e6e5e2;padding-top:16px}}.stats{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}.stats span{{background:#eceee9;padding:6px 10px;border-radius:5px;font-size:14px}}table{{border-collapse:collapse;width:100%;font-size:15px}}td,th{{text-align:left;padding:8px;border-bottom:1px solid #eee;vertical-align:middle}}td audio{{min-width:220px}}@media(max-width:650px){{.players{{grid-template-columns:1fr}}}}
</style><link rel="stylesheet" href="../../assets/listening.css"><script defer src="../../assets/listening.js"></script></head><body><main>
<nav class="listening-nav" aria-label="Listening experiments"><a class="journal-link" href="../../journal/">← Journal</a><div><a href="../014_yue2_excerpt_ablation/">014 · What YuE2 keeps of a score</a><a href="../015_stable_audio_open/">015 · Stable Audio Open</a><a href="../018_musicgen_encodec/" aria-current="page">018 · MusicGen and EnCodec</a></div></nav>
<small>MAESTRO · EXPERIMENT 018</small><h1>A melody-conditioned generator,<br>and the codec underneath it.</h1>
<p>MusicGen-melody (Meta, 2023) is a 1.5-billion-parameter language model over EnCodec audio tokens. It takes a text prompt and, optionally, a reference recording reduced to a chromagram, and generates up to 30 seconds. It has no symbolic input: a melody is given to it as sound. Here it receives the same melodies as experiments 014 and 016, as synthesized guides and as the original recording, with the prompt "solo acoustic grand piano, expressive ballad, no vocals". Each clip is transcribed and its top line aligned to the written melody, the 014 method, and its chroma is compared with the audio it was conditioned on, the 015 method. The text-only clip is graded the same way as a floor: 60% recall and 0.37 chroma is what unrelated piano in the same style scores. MusicGen's piano is dense (top-line precision 15%), so recall is read against that floor, not against 100%. Below the clips, EnCodec alone: the Color Purple recording encoded and decoded at six settings, to show what the token layer keeps before any generation happens.</p>
<div class="players">{mg}</div>
<section><h2>EnCodec round trips: the recording through the codec and back</h2>
<table><tr><th>Codec setting</th><th>Chroma similarity to the recording</th><th>Top-line notes kept (any octave)</th><th>Top-line precision</th><th>In the written octave</th><th>Longest exact run</th><th>Listen</th></tr>{rows}</table>
<p class="muted">Reference: the recording itself scores 96% recall, 84% in octave, run 13, top-line precision 38% with this method (experiment 014). Precision falls at low bitrates because the transcriber hears codec artefacts as extra notes; the chroma column shows the harmony itself is kept at every setting.</p></section>
<p><a href="README.md">Full experiment record</a> · <a href="record/generation-log.json">Generation log</a></p>
</main></body></html>'''
(ROOT / 'index.html').write_text(page)
print('wrote', ROOT / 'index.html')
