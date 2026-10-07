"""One ASR diagnostic of the short generated vocal; not ground truth."""
import os,json,subprocess
from pathlib import Path
os.environ.update(HF_HOME='/tmp/maestro-hf-cache',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
import numpy as np,torch
from transformers import pipeline
torch.set_num_threads(4)
root=Path(__file__).resolve().parents[1]
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(root/'audio/vocal.mp3'),'-ar','16000','-ac','1','-f','f32le','-'])
asr=pipeline('automatic-speech-recognition',model='openai/whisper-base.en',device='cpu',torch_dtype=torch.float32)
result=asr({'raw':np.frombuffer(raw,dtype='<f4').copy(),'sampling_rate':16000},return_timestamps=True)
record=dict(model='openai/whisper-base.en',scope='One-pass ASR diagnostic; not verified words or alignment',result=result)
(root/'record/lyric-check.json').write_text(json.dumps(record,indent=2)+'\n')
print(result['text'],flush=True)
