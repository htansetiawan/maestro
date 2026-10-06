"""Independent lyric diagnostic on mixtures; Whisper errors require listening."""
import json
import os
from pathlib import Path
import subprocess
import numpy as np

os.environ['HF_HOME'] = '/tmp/maestro-hf-cache'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
import torch
from transformers import pipeline

ROOT = Path(__file__).resolve().parents[1]
torch.set_num_threads(4)
recognizer = pipeline('automatic-speech-recognition',model='openai/whisper-base.en',
                      device='cpu',torch_dtype=torch.float32)
saved = ROOT/'record/transcripts.json'
rows = json.loads(saved.read_text())['transcripts'] if saved.exists() else {}
for path in sorted((ROOT/'outputs').glob('*/audio.flac')):
    if path.parent.name in rows:
        continue
    data = subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),
                                  '-ar','16000','-ac','1','-f','f32le','-'])
    result = recognizer({'raw':np.frombuffer(data,dtype='<f4').copy(),'sampling_rate':16000},
                        chunk_length_s=30,stride_length_s=5,return_timestamps=True)
    rows[path.parent.name] = result
    print(path.parent.name, result['text'],flush=True)
(ROOT/'record/transcripts.json').write_text(json.dumps(dict(
    model='openai/whisper-base.en',scope='ASR of complete mixture; not ground truth or a melody metric',
    transcripts=rows),indent=2)+'\n')
