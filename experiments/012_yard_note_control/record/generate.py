"""Render the explicit short score with SoulX-Singer, then publish only MP3 audio."""
from pathlib import Path
from importlib.metadata import version
import hashlib,json,os,subprocess,time,sys,traceback
import numpy as np
import torch
from scipy.signal import resample_poly
from cli.inference import build_model
from soulxsinger.utils.file_utils import load_config
from soulxsinger.utils.data_processor import DataProcessor
ROOT=Path(__file__).resolve().parents[1]
RUNTIME=Path('/tmp/maestro-soulx-singer')
MODEL=Path('/tmp/maestro-hf-cache/models--Soul-AILab--SoulX-Singer/snapshots/40493ad90286056c7a9095035164434a79daa8c9/model.pt')

def digest(path):
 with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def write(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')

def mp3(path,audio,sr):
 data=np.asarray(audio,dtype='<f4')
 channels=1 if data.ndim==1 else data.shape[1]
 subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(sr),'-ac',str(channels),'-i','pipe:0','-c:a','libmp3lame','-b:a','192k',str(path)],input=data.tobytes(),check=True)

def main():
 if (ROOT/'audio/mix.mp3').exists():raise RuntimeError('Refusing to overwrite existing take')
 if torch.cuda.mem_get_info()[0] < 20*2**30:raise RuntimeError('Need 20 GiB free before synthesis')
 score=json.loads((ROOT/'inputs/score.json').read_text())
 assert digest('/tmp/theme_from_the_color_purple.mp3')==score['source_sha256']
 torch.set_num_threads(4);torch.manual_seed(20261007);np.random.seed(20261007)
 config=load_config(str(RUNTIME/'soulxsinger/config/soulxsinger.yaml'))
 request=dict(model='Soul-AILab/SoulX-Singer',model_revision=MODEL.parent.name,
  code_revision=subprocess.check_output(['git','-C',str(RUNTIME),'rev-parse','HEAD'],text=True).strip(),
  model_sha256=digest(MODEL),control='score',auto_shift=False,pitch_shift=0,seed=20261007,
  n_steps=int(config.infer.n_steps),cfg=float(config.infer.cfg),fp16=True,
  runtime={p:version(p)for p in ['torch','torchaudio','transformers','numpy','librosa','cmudict']},
  runtime_note='Isolated Transformers 4.41.2; existing Torch 2.10 CUDA 12.8 and NumPy 2.2.6 reused for Blackwell. Not the upstream Torch 2.2/Python 3.10 environment.',
  target_metadata_sha256=digest(ROOT/'inputs/target-metadata.json'),prompt_metadata_sha256=digest(ROOT/'inputs/prompt-metadata.json'),
  voice_reference='Synthetic ACE-Step excerpt from experiment 011; see prompt-provenance.json',
  conditioning='Explicit note pitch/duration and English phonemes. Piano waveform is used only for original excerpt/mixing; the melody was composed against its analyzed timing.')
 write(ROOT/'record/request.json',request)
 started=time.perf_counter();torch.cuda.reset_peak_memory_stats()
 model=build_model(str(MODEL),config,'cuda',use_fp16=True)
 dp=DataProcessor(hop_size=config.audio.hop_size,sample_rate=config.audio.sample_rate,phoneset_path=str(RUNTIME/'soulxsinger/utils/phoneme/phone_set.json'),device='cuda')
 pm=json.loads((ROOT/'inputs/prompt-metadata.json').read_text())[0]
 tm=json.loads((ROOT/'inputs/target-metadata.json').read_text())[0]
 prompt=dp.process(pm,None)
 prompt['waveform']=torch.from_numpy(np.load(ROOT/'work/prompt.npy')).unsqueeze(0).to('cuda')[:,:prompt['mel2note'].shape[1]*480]
 target=dp.process(tm,None)
 with torch.inference_mode():
  result=model.infer(dict(prompt=prompt,target=target),auto_shift=False,pitch_shift=0,n_steps=config.infer.n_steps,cfg=config.infer.cfg,control='score',use_fp16=True)
 voice=result.squeeze().float().cpu().numpy()
 assert voice.ndim==1 and np.isfinite(voice).all() and np.sqrt(np.mean(voice**2))>1e-5
 native_samples=len(voice);sr=24000;target_samples=round(score['excerpt_seconds']*sr)
 assert abs(native_samples-target_samples)<=480
 voice=np.pad(voice,(0,max(0,target_samples-native_samples)))[:target_samples]
 np.save(ROOT/'work/generated-voice.npy',voice)
 raw=subprocess.check_output(['ffmpeg','-v','error','-i','/tmp/theme_from_the_color_purple.mp3','-ss',str(score['excerpt_start']),'-t',str(score['excerpt_seconds']),'-ar','48000','-ac','2','-f','f32le','-'])
 piano=np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
 vocal=resample_poly(voice,2,1).astype(np.float32)
 assert len(vocal)==len(piano)
 gain=float(np.sqrt(np.mean(piano**2))/np.sqrt(np.mean(vocal**2))*.8)
 mixed=piano+gain*vocal[:,None]
 mix_gain=min(1.,.95/max(float(np.abs(mixed).max()),1e-8));mixed*=mix_gain
 vocal_export_gain=min(1.,.95/max(float(np.abs(voice).max()),1e-8))
 recovered=mixed/mix_gain-gain*vocal[:,None]
 error=float(np.max(np.abs(recovered-piano)));assert error<2e-6
 mp3(ROOT/'audio/mix.mp3',mixed,48000)
 mp3(ROOT/'audio/vocal.mp3',voice*vocal_export_gain,sr)
 mp3(ROOT/'audio/piano.mp3',piano,48000)
 record=dict(status='complete',duration_seconds=len(piano)/48000,native_voice_samples=native_samples,target_samples=target_samples,
  elapsed_seconds=time.perf_counter()-started,peak_cuda_gib=torch.cuda.max_memory_allocated()/2**30,
  vocal_gain=gain,mix_gain=mix_gain,vocal_export_gain=vocal_export_gain,mix_peak=float(np.abs(mixed).max()),
  piano_recovery_max_error_before_mp3=error,piano_time_stretched=False,
  note_accuracy_measured=False,lyric_accuracy_measured=False,audition_performed=False,
  files={p.name:dict(bytes=p.stat().st_size,sha256=digest(p))for p in (ROOT/'audio').glob('*.mp3')})
 write(ROOT/'record/generation.json',record)
 print(json.dumps(record),flush=True)

if __name__=='__main__':
 try:main()
 except Exception as e:
  write(ROOT/'record/failure.json',dict(error=str(e),traceback=traceback.format_exc()))
  raise
