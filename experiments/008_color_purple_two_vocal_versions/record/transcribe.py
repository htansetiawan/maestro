"""CPU lyric diagnostic; recognized text is not a singing or alignment score."""
import argparse
import json
import os
from pathlib import Path
import subprocess

os.environ.update(HF_HOME='/tmp/maestro-hf-cache',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
import numpy as np
import torch
from transformers import pipeline

ROOT=Path(__file__).resolve().parents[1]
cli=argparse.ArgumentParser();cli.add_argument('input',type=Path);cli.add_argument('--name',required=True)
args=cli.parse_args()
torch.set_num_threads(4)
recognizer=pipeline('automatic-speech-recognition',model='openai/whisper-base.en',device='cpu',torch_dtype=torch.float32)
data=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(args.input),'-ar','16000','-ac','1','-f','f32le','-'])
result=recognizer({'raw':np.frombuffer(data,dtype='<f4').copy(),'sampling_rate':16000},
                 chunk_length_s=30,stride_length_s=5,return_timestamps=True)
record=dict(model='openai/whisper-base.en',source=str(args.input.resolve().relative_to(ROOT)),
            scope='One ASR diagnostic pass; not ground truth, phoneme alignment, or a musical quality rating',result=result)
(ROOT/'record'/('transcript-'+args.name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(result['text'],flush=True)
