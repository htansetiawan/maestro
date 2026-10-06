"""Rerender the truncated candidate's exact saved plan with a larger token cap."""
import json
from pathlib import Path
import subprocess
import time
import torch
from yue2 import YuE2Pipeline, SymbolicPlan, SongResult
from yue2.storage import identity, verify_result
from run import ROOT, SOURCE

torch.set_num_threads(4)
source = ROOT/'outputs/planned-20261005'
out = ROOT/'outputs/planned-20261005-extended'
verify_result(source)
plan = SymbolicPlan.load(source)
out.mkdir(parents=True, exist_ok=False)
paths = json.loads((SOURCE/'model-paths.json').read_text())
protocol = json.loads((ROOT/'record/protocol.json').read_text())
override = {'max_tokens':3500}
(out/'attempt.json').write_text(json.dumps(dict(
    reason='Original 1800-token limit truncated an 80.42-second plan.',
    source=source.name, change=override,
    selection='Same saved score and seed. Original retained; no best-of-N selection.'),indent=2)+'\n')
with YuE2Pipeline.from_pretrained(paths['m-a-p/YuE2-3B'],
        vae=paths['m-a-p/YuE2-Vae'],local_files_only=True,**protocol['pipeline']) as pipe:
    start = time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    semantic = pipe.generate_semantic(plan,sampling=override)
    nar_start = time.perf_counter()
    latents = pipe.synthesize(semantic)
    nar_seconds = time.perf_counter()-nar_start
    vae_start = time.perf_counter()
    audio = pipe.decode(latents)
    config = pipe.effective_config(plan.request,semantic_sampling=override)
    timing = dict(abc=plan.timing,semantic=semantic.timing,nar_seconds=nar_seconds,
                  vae_seconds=time.perf_counter()-vae_start,e2e_seconds=time.perf_counter()-start)
    result = SongResult(audio,48000,semantic,latents,config,pipe.weights,timing,
                        identity(dict(request=plan.request.to_dict(),config=config,weights=pipe.weights)))
    result.save_artifacts(out)
    (out/'measurement.json').write_text(json.dumps(dict(
        elapsed_seconds=time.perf_counter()-start,
        peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,
        peak_reserved_gib=torch.cuda.max_memory_reserved()/2**30),indent=2)+'\n')
    subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(out/'audio.flac'),
                    '-c:a','libmp3lame','-b:a','256k',str(out/'audio.mp3')],check=True)
    print('COMPLETE',len(audio)/48000,result.truncated,flush=True)
