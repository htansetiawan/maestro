"""Audio-only pitch/onset evidence for selecting a short piano phrase."""
from pathlib import Path
import json, subprocess
import numpy as np
import librosa
from scipy.signal import find_peaks
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
work=ROOT/'work';work.mkdir(exist_ok=True)
sr=22050;hop=256
raw=subprocess.check_output(['ffmpeg','-v','error','-i','/tmp/theme_from_the_color_purple.mp3','-t','55','-ac','1','-ar',str(sr),'-f','f32le','-'])
y=np.frombuffer(raw,dtype='<f4').copy()
cqt=np.abs(librosa.cqt(y,sr=sr,hop_length=hop,fmin=librosa.midi_to_hz(36),n_bins=72,bins_per_octave=12,tuning=0))
t=np.arange(cqt.shape[1])*hop/sr
onset=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
peaks,_=find_peaks(onset,distance=int(.15*sr/hop),prominence=.5)
rows=[]
for frame in peaks:
 a=cqt[:,frame:min(frame+10,cqt.shape[1])].mean(axis=1)
 local,_=find_peaks(a)
 top=sorted(local,key=lambda k:a[k],reverse=True)[:9]
 rows.append(dict(time=round(frame*hop/sr,3),strength=round(float(onset[frame]),3),pitches=[dict(note=librosa.midi_to_note(36+k),midi=int(36+k),strength=round(float(a[k]),3)) for k in top]))
(ROOT/'record/piano-onsets.json').write_text(json.dumps(rows,indent=2)+'\n')
np.savez(work/'piano-analysis.npz',cqt=cqt,t=t,onset=onset,y=y,sr=sr,hop=hop)
fig,axes=plt.subplots(2,1,figsize=(18,8),gridspec_kw={'height_ratios':[5,1]},sharex=True)
axes[0].imshow(librosa.amplitude_to_db(cqt,ref=np.max),origin='lower',aspect='auto',extent=[0,t[-1],35.5,107.5],vmin=-45,vmax=0,cmap='magma')
axes[0].set_yticks(range(36,97,3));axes[0].set_yticklabels([librosa.midi_to_note(n) for n in range(36,97,3)])
axes[0].set_ylim(40,88);axes[0].grid(alpha=.2);axes[0].set_ylabel('CQT pitch bin (harmonics included)')
axes[1].plot(np.arange(len(onset))*hop/sr,onset);axes[1].set_xlabel('Original piano recording time (seconds)')
axes[1].set_xticks(np.arange(0,56,1));axes[1].grid(alpha=.25)
fig.tight_layout();fig.savefig(work/'piano-analysis.png',dpi=140)
print('Analysis saved',len(rows),'onsets',flush=True)
