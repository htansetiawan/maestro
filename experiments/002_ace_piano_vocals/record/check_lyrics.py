"""ASR spot-check; transcription is evidence of words, not a musical quality rating."""
import json
import os
from pathlib import Path
import subprocess

os.environ['HF_HOME'] = '/tmp/maestro-hf-cache'
os.environ['HF_HUB_DISABLE_XET'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

import soundfile as sf
import torch
from transformers import pipeline

root = Path('/tmp/maestro-yard-vocals')
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(root/'vocals.wav'),
                '-ar', '16000', '-ac', '1', str(root/'vocals-asr.wav')], check=True)
samples, sr = sf.read(root/'vocals-asr.wav', dtype='float32')
asr = pipeline('automatic-speech-recognition', model='openai/whisper-base.en',
               device=0, torch_dtype=torch.float16)
result = asr({'raw': samples, 'sampling_rate': sr}, chunk_length_s=30,
             stride_length_s=5, return_timestamps=True)
(root/'transcription.json').write_text(json.dumps(result, indent=2))
print(result['text'], flush=True)
