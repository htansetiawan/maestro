"""Estimate note following with pYIN; this is not a perceptual quality score."""
from pathlib import Path
import json,subprocess
import numpy as np,librosa
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'inputs/score.json').read_text());sr=24000
voice=np.load(ROOT/'work/generated-voice.npy')
f0,voiced,prob=librosa.pyin(voice,sr=sr,hop_length=240,frame_length=2048,fmin=65,fmax=700)
t=np.arange(len(f0))*.01
notes=[];all_cents=[]
for e in s['events']:
 lo=e['start']+.12;hi=e['end']-.12
 sel=(t>=lo)&(t<hi);good=sel&np.isfinite(f0)
 cents=1200*np.log2(f0[good]/librosa.midi_to_hz(e['midi']))
 all_cents.extend(cents.tolist())
 notes.append(dict(word=e['word'],start=e['start'],end=e['end'],midi=e['midi'],expected_hz=float(librosa.midi_to_hz(e['midi'])),voiced_frames=int(good.sum()),total_inner_frames=int(sel.sum()),median_error_cents=float(np.median(cents)) if len(cents) else None,median_absolute_error_cents=float(np.median(np.abs(cents))) if len(cents) else None))
c=np.array(all_cents);med=[n['median_absolute_error_cents']for n in notes if n['median_absolute_error_cents'] is not None]
result=dict(method='librosa pYIN, 24 kHz, 10 ms hop, 2048 frame, 65–700 Hz; exclude 120 ms at note edges',scope='Estimated pitch agreement on voiced inner-note frames. Does not measure syllable timing, lyric accuracy or musical fit. pYIN can make octave/voicing errors.',notes_evaluated=len(med),notes_total=len(notes),notes_median_within_50_cents=sum(v<=50 for v in med),median_absolute_cents=float(np.median(np.abs(c))),voiced_inner_frames=len(c),voiced_frames_within_50_cents=float(np.mean(np.abs(c)<=50)),notes=notes)
(ROOT/'record/pitch-check.json').write_text(json.dumps(result,indent=2)+'\n')
# Deterministic note guide uses only explicitly designed notes, not the model output.
sr2=48000;n=round(s['excerpt_seconds']*sr2);guide=np.zeros(n,np.float32)
for e in s['events']:
 a=round(e['start']*sr2);b=round(e['end']*sr2);tt=np.arange(b-a)/sr2;freq=librosa.midi_to_hz(e['midi'])
 tone=np.sin(2*np.pi*freq*tt)+.25*np.sin(4*np.pi*freq*tt)+.10*np.sin(6*np.pi*freq*tt)
 env=np.minimum(1,tt/.035)*np.minimum(1,(len(tt)/sr2-tt)/.07)
 guide[a:b]+=(tone*env*.07).astype(np.float32)
raw=subprocess.check_output(['ffmpeg','-v','error','-i','/tmp/theme_from_the_color_purple.mp3','-ss',str(s['excerpt_start']),'-t',str(s['excerpt_seconds']),'-ar','48000','-ac','2','-f','f32le','-'])
piano=np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy();mixed=piano+guide[:,None]
peak=np.abs(mixed).max();mixed*=min(1,.95/max(peak,1e-8))
subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar','48000','-ac','2','-i','pipe:0','-c:a','libmp3lame','-b:a','192k',str(ROOT/'audio/note-guide.mp3')],input=mixed.astype('<f4').tobytes(),check=True)
print({k:v for k,v in result.items()if k!='notes'},flush=True)
