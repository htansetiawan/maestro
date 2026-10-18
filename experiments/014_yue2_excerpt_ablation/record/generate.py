"""Render every prepared condition with one YuE2 model load. GPU required.

MP3-only policy (experiments/AGENTS.md): lossless and latent arrays are deleted
after the MP3 is validated. Small records (request, score, config, timings) stay.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
from importlib.metadata import version

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path.home() / 'maestro-runtime'
os.environ.setdefault('HF_HOME', str(RUNTIME / 'hf'))
MODEL_REVISION = 'c044757a011169583f363168348ae380946efff8'
VAE_REVISION = '152733a19ad43aa67e367f9b5503ef8075bb5126'
SOURCE_REVISION = '3d21f8f5d31be867f4c3b2e6beafb0f2e52f8c10'
MAX_TOKENS = 3500          # ~44 s nominal; 006 rendered 50 s within 1800 at ~25 tokens/s


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def main():
    only = sys.argv[1:]
    import torch
    from yue2 import YuE2Pipeline
    from yue2.storage import verify_result
    import soundfile as sf
    import numpy as np
    revision = subprocess.check_output(['git', '-C', str(RUNTIME / 'YuE'), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == SOURCE_REVISION, revision
    free, _ = torch.cuda.mem_get_info()
    if free < 17 * 2**30:
        raise RuntimeError(f'Only {free/2**30:.1f} GiB free; 17 GiB required. No other job is stopped.')
    torch.set_num_threads(4)
    manifest = json.loads((ROOT / 'prepared/manifest.json').read_text())
    pipeline_args = dict(device='cuda', memory_budget_gib=17, offload_ar=True,
                         vae_core_frames=512, backend='torch', quantization='none')
    protocol = dict(source_revision=revision, model_revision=MODEL_REVISION, vae_revision=VAE_REVISION,
                    runtime={p: version(p) for p in ('yue2-infer', 'torch', 'transformers', 'numpy', 'huggingface-hub')},
                    pipeline=pipeline_args, semantic_sampling=dict(max_tokens=MAX_TOKENS),
                    audio_policy='MP3 256k retained; FLAC and latent/token arrays deleted after validation')
    write(ROOT / 'record/protocol.json', protocol)
    log = (ROOT / 'record/generation.log').open('a')
    with YuE2Pipeline.from_pretrained('m-a-p/YuE2-3B', vae='m-a-p/YuE2-Vae', revision=MODEL_REVISION,
                                     vae_revision=VAE_REVISION, local_files_only=True, **pipeline_args) as pipe:
        for rid in manifest['requests']:
            if only and rid not in only:
                continue
            out = ROOT / 'outputs' / rid
            if out.exists():
                print('retaining existing attempt', rid, flush=True)
                continue
            request = json.loads((ROOT / 'prepared' / rid / 'request.json').read_text())
            out.mkdir(parents=True)
            write(out / 'attempt.json', dict(request={k: v for k, v in request.items() if k != 'abc'},
                                             abc_sha256=__import__('hashlib').sha256(request.get('abc', '').encode()).hexdigest(),
                                             status='submitted'))
            start = time.perf_counter()
            try:
                torch.cuda.reset_peak_memory_stats()
                result = pipe(**request, semantic_sampling=protocol['semantic_sampling'])
                result.save_artifacts(out)
                verify_result(out)
                if 'abc' in request:
                    assert (out / 'score.abc').read_text() == request['abc']
                info = sf.info(out / 'audio.flac')
                audio, sr = sf.read(out / 'audio.flac', dtype='float32', always_2d=True)
                assert np.isfinite(audio).all() and sr == 48000 and audio.shape[1] == 2
                rms = float(np.sqrt(np.mean(np.square(audio, dtype=np.float64))))
                assert rms > 1e-5, 'silent output'
                subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(out / 'audio.flac'),
                                '-c:a', 'libmp3lame', '-b:a', '256k', str(out / 'audio.mp3')], check=True)
                probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                                 '-of', 'csv=p=0', str(out / 'audio.mp3')], text=True)
                mp3_seconds = float(probe.strip())
                assert abs(mp3_seconds - info.frames / sr) < 0.5, (mp3_seconds, info.frames / sr)
                measurement = dict(seconds=time.perf_counter() - start,
                                   peak_allocated_gib=torch.cuda.max_memory_allocated() / 2**30,
                                   audio_seconds=info.frames / sr, audio_peak=float(np.abs(audio).max()), audio_rms=rms,
                                   truncated=result.truncated, mp3_seconds=mp3_seconds, lossless_deleted=True,
                                   adherence_measured=False)
                write(out / 'measurement.json', measurement)
                for name in ('audio.flac', 'latent.npy'):
                    (out / name).unlink(missing_ok=True)
                for extra in out.glob('*.npy'):
                    extra.unlink()
                write(out / 'attempt.json', dict(json.loads((out / 'attempt.json').read_text()), status='completed'))
                print(json.dumps(dict(id=rid, **measurement)), file=log, flush=True)
                print('done', rid, round(measurement['audio_seconds'], 1), 's', 'truncated', result.truncated, flush=True)
            except Exception as error:
                write(out / 'failure.json', dict(error=str(error), traceback=traceback.format_exc()))
                print('FAILED', rid, error, file=log, flush=True)
                print('FAILED', rid, error, flush=True)


if __name__ == '__main__':
    main()
