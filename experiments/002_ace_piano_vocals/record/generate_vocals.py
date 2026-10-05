"""Generate one source-conditioned vocal stem and mix with the supplied piano."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

os.environ['ACESTEP_CHECKPOINTS_DIR'] = '/tmp/maestro-ace-step/checkpoints'
os.environ['HF_HOME'] = '/tmp/maestro-hf-cache'
os.environ['ACESTEP_GENERATION_TIMEOUT'] = '1200'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import numpy as np
import soundfile as sf
import torch
from acestep.handler import AceStepHandler
from acestep.inference import GenerationConfig, GenerationParams, generate_music

root = Path('/tmp/maestro-yard-vocals')
source = root / 'piano.wav'
lyrics = (root / 'lyrics.txt').read_text()
caption = ('Warm intimate male lead singing an English piano ballad about the Yard, '
           'red brick buildings, evening light and belonging. Natural expressive tenor, '
           'clear words, gentle legato phrasing, subtle vibrato and audible breath. '
           'One solo singer responding to the provided piano accompaniment, restrained '
           'verse and a gently rising chorus. Vocal stem only, no additional instruments.')
params = GenerationParams(
    task_type='lego', instruction='Generate the VOCALS track based on the audio context:',
    src_audio=str(source), caption=caption, lyrics=lyrics,
    instrumental=False, vocal_language='en',
    inference_steps=50, guidance_scale=7.0, seed=20261004,
    repainting_start=0.0, repainting_end=-1.0,
    thinking=False, use_cot_metas=False, use_cot_caption=False,
    use_cot_language=False, use_cot_lyrics=False, audio_codes='',
    enable_normalization=False,
)
config = GenerationConfig(batch_size=1, use_random_seed=False,
                          seeds=[20261004], audio_format='wav32')
manifest = {
    'ace_revision': subprocess.check_output(['git', '-C', '/tmp/maestro-ace-step',
                                           'rev-parse', 'HEAD'], text=True).strip(),
    'model': 'acestep-v15-xl-base',
    'source_file': '/tmp/st_elmo_fire.m4a',
    'source_sha256': hashlib.sha256(Path('/tmp/st_elmo_fire.m4a').read_bytes()).hexdigest(),
    'model_revisions': json.loads((root / 'model_revisions.json').read_text()),
    'parameters': params.to_dict(), 'config': config.to_dict(),
    'gpu': torch.cuda.get_device_name(0),
}
(root / 'generation.json').write_text(json.dumps(manifest, indent=2))
print('Initializing XL Base on', manifest['gpu'], flush=True)
dit = AceStepHandler()
status, success = dit.initialize_service(
    project_root='/tmp/maestro-ace-step', config_path='acestep-v15-xl-base',
    device='cuda', use_flash_attention=False, compile_model=False,
    offload_to_cpu=False, quantization=None, prefer_source='huggingface')
print(status, flush=True)
if not success:
    raise RuntimeError(status)
started = time.monotonic()
result = generate_music(dit, None, params, config, save_dir=str(root / 'raw'))
if not result.success or len(result.audios) != 1:
    raise RuntimeError(f'ACE generation failed: {result.error}')
shutil.copyfile(result.audios[0]['path'], root / 'vocals.wav')
piano, sr = sf.read(source, always_2d=True, dtype='float32')
vocal, vocal_sr = sf.read(root / 'vocals.wav', always_2d=True, dtype='float32')
if sr != vocal_sr:
    raise RuntimeError(f'Sample rate mismatch: {sr} vs {vocal_sr}')
if not np.isfinite(vocal).all() or np.sqrt(np.mean(vocal ** 2)) < 1e-5:
    raise RuntimeError('Vocal output is silent or nonfinite')
vocal = np.pad(vocal, ((0, max(0, len(piano)-len(vocal))), (0, 0)))[:len(piano)]
vocal = np.repeat(vocal, 2, axis=1) if vocal.shape[1] == 1 else vocal
piano_rms = float(np.sqrt(np.mean(piano ** 2)))
vocal_rms = float(np.sqrt(np.mean(vocal ** 2)))
vocal_gain = piano_rms / vocal_rms * 10 ** (2 / 20)
mix = piano + vocal * vocal_gain
mix_gain = min(1.0, .95 / max(float(np.max(np.abs(mix))), 1e-8))
sf.write(root / 'yard-piano-and-voice.wav', mix * mix_gain, sr, subtype='PCM_24')
manifest.update(generation_seconds=time.monotonic()-started,
                duration_seconds=len(piano)/sr, raw_vocal_seconds=sf.info(root/'vocals.wav').duration,
                vocal_gain=vocal_gain, mix_gain=mix_gain,
                piano_rms=piano_rms, vocal_rms=vocal_rms)
(root / 'generation.json').write_text(json.dumps(manifest, indent=2))
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(root/'yard-piano-and-voice.wav'),
                '-c:a', 'libmp3lame', '-b:a', '256k', str(root/'yard-piano-and-voice.mp3')], check=True)
print('Saved', root/'yard-piano-and-voice.mp3', flush=True)
