"""Check artifacts and symbolic inputs; no claim of measured audio-note fidelity."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import soundfile as sf
from yue2.storage import verify_result

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, '/tmp/maestro-yue2/skills/yue2-music/scripts')
from abc_tools import parse_abc


def score_info(text):
    score = parse_abc(text)
    return dict(bpm=score.bpm, nominal_seconds=float(score.voices['Vocal'].time)*60/score.bpm,
                notes=[dict(onset_quarters=float(t), midi=p, duration_quarters=float(d))
                       for t, p, d in score.voices['Vocal'].notes])


def main():
    expected = [55,60,64,57,60,65,62,64,55,60,64,57,60,65,69,67]*2
    target = score_info((ROOT / 'inputs/motif.abc').read_text())
    assert [n['midi'] for n in target['notes']] == expected
    assert [n['onset_quarters'] for n in target['notes']] == list(range(32))
    assert all(n['duration_quarters'] == 1 for n in target['notes'])
    assert target['bpm'] == 90
    guide = ROOT / 'inputs/motif-guide.wav'
    if not guide.exists():
        sr = 48000
        audio = np.zeros(round((target['nominal_seconds']+.3)*sr), dtype=np.float32)
        t = np.arange(round(.6*sr))/sr
        env = np.minimum(t/.012, 1)*np.minimum((t[-1]-t)/.04, 1)*np.exp(-2*t)
        for event in target['notes']:
            hz = 440*2**((event['midi']-69)/12)
            note = .3*env*(np.sin(2*np.pi*hz*t)+.2*np.sin(4*np.pi*hz*t))
            start = round(event['onset_quarters']*60/90*sr)
            audio[start:start+len(note)] += note.astype(np.float32)
        sf.write(guide, audio, sr, subtype='PCM_24')
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(guide),
                        '-c:a','libmp3lame','-b:a','192k',str(guide.with_suffix('.mp3'))],check=True)
        spec = importlib.util.spec_from_file_location('melody_hint', ROOT.parent /
            '005_color_purple_orchestra/record/melody_hint.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.write_midi(ROOT/'inputs/motif.mid', module.compile_notes(module.PHRASES*2),90)
    rows = []
    for path in sorted((ROOT/'outputs').iterdir()):
        if not (path/'result.json').exists():
            rows.append(dict(id=path.name, status='incomplete', failure=(path/'failure.json').exists()))
            continue
        result = verify_result(path)
        audio, sr = sf.read(path/'audio.flac',dtype='float32',always_2d=True)
        assert sr == 48000 and audio.shape[1] == 2 and np.isfinite(audio).all()
        rms = float(np.sqrt(np.mean(audio**2)))
        assert rms > 1e-5
        row = dict(id=path.name,status='complete',seconds=len(audio)/sr,
                   peak=float(np.abs(audio).max()),rms=rms,channels=2,sample_rate=sr,
                   fraction_at_full_scale=float(np.mean(np.abs(audio)>=.99999)),
                   truncated=result['truncated'],manifest_verified=True,
                   measurement=json.loads((path/'measurement.json').read_text()))
        try:
            row['symbolic_score'] = score_info((path/'score.abc').read_text())
        except ValueError as exc:
            row['score_inspection_error'] = str(exc)
        if path.name.startswith('fixed-'):
            assert (path/'score.abc').read_bytes() == (ROOT/'inputs/motif.abc').read_bytes()
            row['provided_score_preserved_in_artifacts'] = True
        rows.append(row)
    report = dict(target=target,candidates=rows,audio_pitch_alignment_measured=False,
                  listening_status='Pending user evaluation; file integrity is not musical quality.',
                  duration_caution='Total audio duration includes intros/outros; it does not isolate vocal timing.')
    (ROOT/'record/checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in row.items() if k!='symbolic_score'} for row in rows],indent=2))


if __name__ == '__main__':
    main()
