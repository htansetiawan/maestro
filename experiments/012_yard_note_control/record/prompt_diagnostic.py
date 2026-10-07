"""Get word times for a short existing synthetic voice reference (ASR estimate)."""
import os,json,subprocess
from pathlib import Path
os.environ.update(HF_HOME='/tmp/maestro-hf-cache',HF_HUB_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
import torch,numpy as np
from transformers import pipeline
torch.set_num_threads(4)
root=Path(__file__).resolve().parents[1]
source=root.parent/'011_yard_piano_fresh_ace_vocal/audio/vocals.mp3'
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-t','30','-ac','1','-ar','16000','-f','f32le','-'])
asr=pipeline('automatic-speech-recognition',model='openai/whisper-base.en',device='cpu',torch_dtype=torch.float32)
result=asr({'raw':np.frombuffer(raw,dtype='<f4').copy(),'sampling_rate':16000},return_timestamps='word')
(root/'record/prompt-asr.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
