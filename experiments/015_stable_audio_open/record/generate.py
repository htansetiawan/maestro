"""Stable Audio Open 1.0: text-to-audio and audio-to-audio over the Color Purple piano.

Conditions are predeclared; no candidate selection. MP3-only policy applies.
If the gated weights are not accessible with the configured Hugging Face token,
the run records status=gated and exits 3 without generating.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
RUNTIME = Path.home() / 'maestro-runtime'
os.environ.setdefault('HF_HOME', str(RUNTIME / 'hf'))
SOURCE = REPO / 'experiments/005_color_purple_orchestra/data/source.wav'   # local, gitignored copy of the recording
MODEL = 'stabilityai/stable-audio-open-1.0'
PIANO = ('Solo acoustic grand piano, lyrical pastoral ballad, gentle flowing arpeggio accompaniment, '
         'expressive legato melody, F major, 88 BPM, intimate studio recording')
ORCHESTRA = ('Solo piano accompanied by a warm string orchestra and soft woodwinds, cinematic film score '
             'arrangement, lyrical pastoral theme, F major, 88 BPM')
SECONDS = 47
CONDITIONS = [
    dict(id='t2a-piano-20261017', prompt=PIANO, seed=20261017),
    dict(id='t2a-piano-20261018', prompt=PIANO, seed=20261018),
    dict(id='a2a-piano-sigma0.5', prompt=PIANO, seed=20261017, init_noise_level=0.5),
    dict(id='a2a-piano-sigma2', prompt=PIANO, seed=20261017, init_noise_level=2.0),
    dict(id='a2a-piano-sigma8', prompt=PIANO, seed=20261017, init_noise_level=8.0),
    dict(id='a2a-orchestra-sigma2', prompt=ORCHESTRA, seed=20261017, init_noise_level=2.0),
    dict(id='a2a-orchestra-sigma8', prompt=ORCHESTRA, seed=20261017, init_noise_level=8.0),
]


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def gate_open():
    import urllib.request
    req = urllib.request.Request(f'https://huggingface.co/{MODEL}/resolve/main/model_config.json',
                                 headers={'Authorization': f'Bearer {os.environ.get("HF_TOKEN", "")}'}, method='HEAD')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200
    except Exception as error:   # 401/403 are HTTPError
        return getattr(error, 'code', None) == 200


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--only', nargs='*')
    cli.add_argument('--steps', type=int, default=100)
    cli.add_argument('--cfg', type=float, default=7.0)
    args = cli.parse_args()
    record = ROOT / 'record'
    if not gate_open():
        write(record / 'status.json', dict(status='gated', model=MODEL,
              action='Accept the model license at https://huggingface.co/' + MODEL +
                     ' with the account that owns HF_TOKEN, and give a fine-grained token gated-repo read access.'))
        print('Stable Audio Open weights are not accessible; see record/status.json', flush=True)
        return 3
    import torch, torchaudio, numpy as np, soundfile as sf
    from einops import rearrange
    from stable_audio_tools import get_pretrained_model
    from stable_audio_tools.inference.generation import generate_diffusion_cond
    from importlib.metadata import version
    device = 'cuda'
    free, _ = torch.cuda.mem_get_info()
    if free < 8 * 2**30:
        raise RuntimeError(f'Only {free/2**30:.1f} GiB free; 8 GiB required. No other job is stopped.')
    t0 = time.perf_counter()
    model, config = get_pretrained_model(MODEL)
    model = model.to(device)
    sr, sample_size = config['sample_rate'], config['sample_size']
    load_seconds = time.perf_counter() - t0
    source, source_sr = sf.read(SOURCE, dtype='float32', always_2d=True)
    source = torch.from_numpy(source.T)
    source = torchaudio.functional.resample(source, source_sr, sr)[:, :sample_size]
    init = (sr, source)
    protocol = dict(model=MODEL, sample_rate=sr, sample_size=sample_size, model_seconds=sample_size / sr,
                    steps=args.steps, cfg_scale=args.cfg, sampler='dpmpp-3m-sde', sigma_min=0.3, sigma_max=500,
                    source=str(SOURCE.relative_to(REPO)), source_excerpt_seconds=min(SECONDS, sample_size / sr),
                    runtime={p: version(p) for p in ('stable-audio-tools', 'torch', 'torchaudio')},
                    load_seconds=load_seconds, conditions=CONDITIONS,
                    note='init_noise_level is the k-diffusion sigma at which sampling starts from the encoded source; '
                         'lower keeps more of the source. Levels are a first sweep, not tuned values.')
    write(record / 'protocol.json', protocol)
    write(record / 'status.json', dict(status='running'))
    log = (record / 'generation.log').open('a')
    for cond in CONDITIONS:
        if args.only and cond['id'] not in args.only:
            continue
        out = ROOT / 'outputs' / cond['id']
        if out.exists():
            print('retaining', cond['id'], flush=True)
            continue
        out.mkdir(parents=True)
        write(out / 'request.json', cond)
        start = time.perf_counter()
        try:
            torch.cuda.reset_peak_memory_stats()
            conditioning = [dict(prompt=cond['prompt'], seconds_start=0, seconds_total=SECONDS)]
            kwargs = {}
            if 'init_noise_level' in cond:
                kwargs = dict(init_audio=init, init_noise_level=cond['init_noise_level'])
            output = generate_diffusion_cond(model, steps=args.steps, cfg_scale=args.cfg, conditioning=conditioning,
                                             sample_size=sample_size, sigma_min=0.3, sigma_max=500,
                                             sampler_type='dpmpp-3m-sde', device=device, seed=cond['seed'], **kwargs)
            output = rearrange(output, 'b d n -> d (b n)').to(torch.float32)
            peak = float(output.abs().max())
            output = (output / max(peak, 1e-6)).clamp(-1, 1).cpu().numpy().T
            wav = out / 'audio.wav'
            sf.write(wav, output, sr)
            subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(wav), '-c:a', 'libmp3lame',
                            '-b:a', '256k', str(out / 'audio.mp3')], check=True)
            seconds = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                                     '-of', 'csv=p=0', str(out / 'audio.mp3')], text=True))
            assert abs(seconds - output.shape[0] / sr) < 0.5
            wav.unlink()
            m = dict(seconds=time.perf_counter() - start, peak_allocated_gib=torch.cuda.max_memory_allocated() / 2**30,
                     audio_seconds=output.shape[0] / sr, raw_peak=peak, normalized=True, lossless_deleted=True)
            write(out / 'measurement.json', m)
            print(json.dumps(dict(id=cond['id'], **m)), file=log, flush=True)
            print('done', cond['id'], flush=True)
        except Exception as error:
            write(out / 'failure.json', dict(error=str(error), traceback=traceback.format_exc()))
            print('FAILED', cond['id'], error, file=log, flush=True)
    write(record / 'status.json', dict(status='completed'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
