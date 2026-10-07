"""After version A, isolate its singer with official HTDemucs weights."""
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import random
import time

os.environ.setdefault('TORCH_HOME','/tmp/maestro-demucs-cache')
import numpy as np
import soundfile as sf
import torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
from demucs.audio import convert_audio

ROOT = Path(__file__).resolve().parents[1]


def main():
    torch.set_num_threads(4)
    torch.manual_seed(20261006)
    random.seed(20261006)
    np.random.seed(20261006)
    selection=json.loads((ROOT/'record/selection.json').read_text())
    source = ROOT/'outputs'/selection['version_a']/'audio.flac'
    out = ROOT/'outputs/separated'
    out.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter()
    mixture,sr=sf.read(source,dtype='float32',always_2d=True)
    model=get_model('htdemucs')
    wav=convert_audio(torch.from_numpy(mixture.T.copy()),sr,model.samplerate,model.audio_channels)
    ref=wav.mean(0)
    mean,std=ref.mean(),ref.std()
    assert std>1e-5
    normalized=(wav-mean)/std
    with torch.inference_mode():
        sources=apply_model(model,normalized[None],device='cuda',shifts=1,split=True,
                            overlap=.25,progress=True,num_workers=0)[0]
    sources=sources.cpu()*std+mean
    vocal=sources[model.sources.index('vocals')]
    vocal=convert_audio(vocal,model.samplerate,sr,2).T.numpy()
    if len(vocal)<len(mixture):
        vocal=np.pad(vocal,((0,len(mixture)-len(vocal)),(0,0)))
    vocal=vocal[:len(mixture)]
    accompaniment=mixture-vocal
    assert np.isfinite(vocal).all() and np.isfinite(accompaniment).all()
    sf.write(out/'vocals.flac',vocal,sr,subtype='PCM_24')
    sf.write(out/'accompaniment.flac',accompaniment,sr,subtype='PCM_24')
    weights=Path(os.environ['TORCH_HOME'])/'hub/checkpoints/955717e8-8726e21a.th'
    report=dict(operation='source separation of version A; not new singing generation',
        model='htdemucs',demucs_version=version('demucs'),seed=20261006,shifts=1,overlap=.25,
        weights_sha256=hashlib.sha256(weights.read_bytes()).hexdigest(),
        official_weights_url='https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/955717e8-8726e21a.th',
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        seconds=len(vocal)/sr,sample_rate=sr,elapsed_seconds=time.perf_counter()-start,
        vocal_rms=float(np.sqrt(np.mean(vocal.astype(np.float64)**2))),
        mixture_reconstruction_max_error=float(np.max(np.abs(vocal+accompaniment-mixture))),
        caveat='The vocal estimate may retain piano leakage and separation artifacts.')
    (out/'separation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    main()
