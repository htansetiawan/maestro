"""Prepare a short previously generated ACE voice as SoulX timbre conditioning."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np,librosa
import cmudict
ROOT=Path(__file__).resolve().parents[1]
source=ROOT.parent/'011_yard_piano_fresh_ace_vocal/audio/vocals.mp3'
start,end=7.38,16.4
sr=24000
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-ss',str(start),'-t',str(end-start),'-ac','1','-ar',str(sr),'-f','f32le','-'])
y=np.frombuffer(raw,dtype='<f4').copy()
np.save(ROOT/'work/prompt.npy',y)
f0,voiced,prob=librosa.pyin(y,sr=sr,hop_length=240,frame_length=2048,fmin=65,fmax=700)
t=np.arange(len(f0))*.01
asr=json.loads((ROOT/'record/prompt-asr.json').read_text())
dict_en=cmudict.dict()
rows=[]
for c in asr['chunks']:
 a,b=c['timestamp'];w=c['text'].strip().lower().strip('.,')
 if a>=start and b<=end and b>a:
  vals=f0[(t>=a-start+.06)&(t<=b-start-.06)&np.isfinite(f0)]
  assert len(vals),w
  pitch=int(round(librosa.hz_to_midi(np.median(vals))))
  rows.append(dict(word=w,onset=round(a-start,3),duration=round(b-a,3),midi=pitch,phonemes=dict_en[w][0],voiced_median_hz=float(np.median(vals))))
meta=[dict(index='synthetic_ace_timbre',language='English',time=[0,round((end-start)*1000)],duration=' '.join(str(r['duration']) for r in rows),text=' '.join(r['word'] for r in rows),phoneme=' '.join('en_'+'-'.join(r['phonemes']) for r in rows),note_pitch=' '.join(str(r['midi']) for r in rows),note_type=' '.join('2' for r in rows))]
(ROOT/'inputs/prompt-metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
with source.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
(ROOT/'record/prompt-provenance.json').write_text(json.dumps(dict(source=str(source.relative_to(ROOT.parent.parent)),source_sha256=digest,start_seconds=start,end_seconds=end,voice_origin='Synthetic ACE-Step voice from experiment 011; not an external singer recording',alignment='Whisper-base.en word timestamps; estimated, not manually verified phoneme alignment',pitch='Median librosa pYIN F0 per word; approximate prompt annotation only',words=rows),indent=2)+'\n')
print(rows,flush=True)
