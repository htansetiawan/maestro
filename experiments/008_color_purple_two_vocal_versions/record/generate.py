"""Version A: one score-conditioned YuE2 piano-and-vocal generation."""
import argparse
from importlib.metadata import version
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path('/tmp/maestro-yue2')
sys.path.insert(0, str(RUNTIME/'skills/yue2-music/scripts'))
from abc_tools import parse_abc


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument('--output-name',default='new-piano-vocal')
    cli.add_argument('--max-tokens',type=int,default=9000)
    args=cli.parse_args()
    if not args.output_name.replace('-','').isalnum():
        raise ValueError('Use a simple output directory name')
    import torch
    import numpy as np
    import soundfile as sf
    from yue2 import YuE2Pipeline
    from yue2.storage import verify_result
    request = json.loads((ROOT/'inputs/request.json').read_text())
    score = parse_abc(request['abc'])
    assert score.voices['Vocal'].notes and score.voices['Ins'].notes
    assert request['abc'] == (ROOT/'inputs/vocal.abc').read_text()
    torch.set_num_threads(4)
    if torch.cuda.mem_get_info()[0] < 24*2**30:
        raise RuntimeError('Need 24 GiB free before this full vocal run')
    paths = json.loads((RUNTIME/'model-paths.json').read_text())
    revision = subprocess.check_output(['git','-C',str(RUNTIME),'rev-parse','HEAD'],text=True).strip()
    assert revision == '3d21f8f5d31be867f4c3b2e6beafb0f2e52f8c10'
    out = ROOT/'outputs'/args.output_name
    out.mkdir(parents=True, exist_ok=False)
    protocol = dict(request=request, source_revision=revision,
        model_revision=Path(paths['m-a-p/YuE2-3B']).name,
        vae_revision=Path(paths['m-a-p/YuE2-Vae']).name,
        runtime={p:version(p) for p in ['yue2-infer','torch','transformers','numpy']},
        pipeline=dict(device='cuda',memory_budget_gib=24,offload_ar=True,
                      vae_core_frames=1024,backend='torch',quantization='none'),
        semantic_sampling=dict(max_tokens=args.max_tokens),
        source_score_sha256=hashlib.sha256((ROOT.parent/'007_color_purple_sheet_yue2/prepared/score.abc').read_bytes()).hexdigest(),
        purpose='A new joint piano+vocal performance; prior piano waveform is not an input.')
    write(out/'attempt.json',protocol)
    start = time.perf_counter()
    try:
        torch.cuda.reset_peak_memory_stats()
        with YuE2Pipeline.from_pretrained(paths['m-a-p/YuE2-3B'],vae=paths['m-a-p/YuE2-Vae'],
                local_files_only=True,**protocol['pipeline']) as pipe:
            song = pipe(**request,semantic_sampling=protocol['semantic_sampling'])
            song.save_artifacts(out)
        verify_result(out)
        assert (out/'score.abc').read_text()==request['abc']
        audio, sr = sf.read(out/'audio.flac',dtype='float32',always_2d=True)
        assert sr==48000 and audio.shape[1]==2 and np.isfinite(audio).all()
        rms=float(np.sqrt(np.mean(audio.astype(np.float64)**2)))
        assert rms>1e-5
        write(out/'measurement.json',dict(elapsed_seconds=time.perf_counter()-start,
            audio_seconds=len(audio)/sr,peak=float(np.abs(audio).max()),rms=rms,
            clipped_fraction=float(np.mean(np.abs(audio)>=.99999)),truncated=song.truncated,
            manifest_verified=True,score_preserved_in_saved_input=True,
            peak_cuda_gib=torch.cuda.max_memory_allocated()/2**30,
            audio_score_adherence_measured=False))
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(out/'audio.flac'),
                        '-c:a','libmp3lame','-b:a','256k',str(out/'audio.mp3')],check=True)
        print(json.dumps(dict(output=str(out),seconds=len(audio)/sr,truncated=song.truncated)),flush=True)
    except Exception as error:
        write(out/'failure.json',dict(error=str(error),traceback=traceback.format_exc()))
        raise


if __name__ == '__main__':
    main()
