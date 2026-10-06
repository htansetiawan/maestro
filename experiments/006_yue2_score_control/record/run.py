"""Four predeclared candidates; retain failures and avoid best-of-N selection."""
import argparse
from importlib.metadata import version
import json
import os
from pathlib import Path
import subprocess
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/tmp/maestro-yue2')
MODEL_REVISION = 'c044757a011169583f363168348ae380946efff8'
VAE_REVISION = '152733a19ad43aa67e367f9b5503ef8075bb5126'
STYLE = ('English, intimate cinematic piano ballad, warm expressive male baritone, '
         'acoustic grand piano accompaniment only, tender nostalgic college memories, '
         'clear lyrics, gentle legato, C major, 90 BPM, short verse and chorus, '
         'minimal intro and outro, no drums, no choir')


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def requests():
    lyrics = (ROOT / 'inputs/lyrics.txt').read_text()
    abc = (ROOT / 'inputs/motif.abc').read_text()
    return [dict(id=f'{mode}-{seed}', style=STYLE, lyrics=lyrics, cot='melody',
                 seed=seed, **({'abc': abc} if mode == 'fixed' else {}))
            for seed in (20261005, 20261006) for mode in ('fixed', 'planned')]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', choices=[r['id'] for r in requests()])
    args = parser.parse_args()
    import torch
    from yue2 import YuE2Pipeline

    torch.set_num_threads(4)
    os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
    paths = json.loads((SOURCE / 'model-paths.json').read_text())
    protocol = dict(source_revision=subprocess.check_output(
        ['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip(),
        model_revision=MODEL_REVISION, vae_revision=VAE_REVISION,
        runtime={p: version(p) for p in ('yue2-infer', 'torch', 'transformers',
                                        'numpy', 'huggingface-hub', 'accelerate')},
        pipeline=dict(device='cuda', memory_budget_gib=17, offload_ar=True,
                      vae_core_frames=512, backend='torch', quantization='none'),
        semantic_sampling=dict(max_tokens=1800),
        rationale='Short listening pilot. Same style, lyrics, seeds and melody-only mode; '
                  'only external versus model-composed score differs. No candidate selection.',
        requests=requests())
    record = ROOT / 'record'
    protocol_file = record / 'protocol.json'
    if protocol_file.exists() and json.loads(protocol_file.read_text()) != protocol:
        raise RuntimeError('Protocol changed; start a separate experiment')
    write(protocol_file, protocol)
    with YuE2Pipeline.from_pretrained(paths['m-a-p/YuE2-3B'],
            vae=paths['m-a-p/YuE2-Vae'], local_files_only=True,
            **protocol['pipeline']) as pipe:
        for request in protocol['requests']:
            if args.only and request['id'] != args.only:
                continue
            out = ROOT / 'outputs' / request['id']
            if out.exists():
                print('Retaining existing attempt:', out, flush=True)
                continue
            out.mkdir(parents=True)
            write(out / 'attempt.json', dict(request=request, event='submitted'))
            print('START', request['id'], flush=True)
            start = time.perf_counter()
            torch.cuda.reset_peak_memory_stats()
            try:
                result = pipe(**request, semantic_sampling=protocol['semantic_sampling'])
                result.save_artifacts(out)
                write(out / 'measurement.json', dict(
                    elapsed_seconds=time.perf_counter()-start,
                    peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,
                    peak_reserved_gib=torch.cuda.max_memory_reserved()/2**30))
                subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i',
                    str(out / 'audio.flac'), '-c:a', 'libmp3lame', '-b:a', '256k',
                    str(out / 'audio.mp3')], check=True)
                print('COMPLETE', request['id'], result.truncated, flush=True)
            except Exception as exc:
                write(out / 'failure.json', dict(error=str(exc), traceback=traceback.format_exc(),
                                               elapsed_seconds=time.perf_counter()-start))
                raise


if __name__ == '__main__':
    main()
