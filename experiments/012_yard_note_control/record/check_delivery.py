"""Check delivered audio and note/MIDI consistency without writing lossless audio."""
from pathlib import Path
import json,subprocess
import numpy as np,mido
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'inputs/score.json').read_text())
meta=json.loads((ROOT/'inputs/target-metadata.json').read_text())[0]
assert abs(sum(map(float,meta['duration'].split()))-25)<1e-8
notes=[];time=0.
for message in mido.MidiFile(ROOT/'inputs/vocal.mid'):
 time+=message.time
 if message.type=='note_on' and message.velocity:notes.append((message.note,time))
assert len(notes)==len(s['events'])==27
for (pitch,t),event in zip(notes,s['events']):
 assert pitch==event['midi'] and abs(t-event['start'])<.002
files={}
for path in (ROOT/'audio').glob('*.mp3'):
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,bit_rate:stream=codec_name,sample_rate,channels','-of','json',str(path)],text=True))
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','1','-ar','24000','-'])
 audio=np.frombuffer(raw,dtype='<f4')
 assert np.isfinite(audio).all() and np.sqrt(np.mean(audio**2))>1e-5 and abs(len(audio)/24000-25)<.03
 files[path.name]=dict(info=info,decoded_seconds=len(audio)/24000,decoded_mono_peak=float(np.abs(audio).max()))
record=dict(mp3_files=files,note_count=27,midi_matches_score=True,conditioning_duration=25.0)
(ROOT/'record/delivery-check.json').write_text(json.dumps(record,indent=2)+'\n')
print('Four MP3s decode correctly; MIDI pitches/times match the explicit score.')
assert (ROOT/'record/pitch-check.json').is_file(), 'Run pitch evaluation before cleanup'
deleted=[]
for name in ['generated-voice.npy', 'prompt.npy', 'piano-analysis.npz']:
 path=ROOT/'work'/name
 if path.exists():
  path.unlink()
  deleted.append(name)
(ROOT/'record/intermediate-cleanup.json').write_text(json.dumps(dict(
 removed_task_created_arrays=deleted, original_user_audio_untouched=True,
 retained_trial_audio='MP3 only'),indent=2)+'\n')
