"""Validate on CPU by default. Pass --generate later to run the frozen score."""
import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path('/tmp/maestro-yue2')
REVISION = '3d21f8f5d31be867f4c3b2e6beafb0f2e52f8c10'


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--generate', action='store_true')
    args = cli.parse_args()
    sys.path.insert(0, str(RUNTIME/'skills/yue2-music/instrumental/scripts'))
    from instrumental import load_prepared
    from yue2.protocol import SongRequest, token_prefixes, CONTEXT
    from yue2.tokenization_yue2 import YuE2TextTokenizer
    request = load_prepared(ROOT/'prepared')
    paths = json.loads((RUNTIME/'model-paths.json').read_text())
    tokenizer = YuE2TextTokenizer(Path(paths['m-a-p/YuE2-3B'])/'qwen.tiktoken')
    ids = tokenizer.encode(request['abc'])
    assert tokenizer.decode(ids) == request['abc']
    prefix = token_prefixes(SongRequest(**request), tokenizer, ids)
    assert len(prefix) + 9000 <= CONTEXT
    revision = subprocess.check_output(['git', '-C', str(RUNTIME), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == REVISION, 'Runtime changed; review before generating'
    checks = dict(prepared_hashes_verified=True, native_tokenizer_roundtrip=True,
                  score_sha256=hashlib.sha256(request['abc'].encode()).hexdigest(),
                  abc_tokens=len(ids), prefix_tokens=len(prefix), semantic_token_limit=9000,
                  context_limit=CONTEXT, context_fits=True, model_loaded=False)
    write(ROOT/'record/preflight.json', checks)
    print(json.dumps(checks, indent=2), flush=True)
    if not args.generate:
        print('Preparation only: no GPU inference requested.', flush=True)
        return
    import torch
    from yue2 import YuE2Pipeline
    from yue2.storage import verify_result
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA unavailable; the score remains prepared.')
    free, _ = torch.cuda.mem_get_info()
    if free < 17*2**30:
        raise RuntimeError(f'Only {free/2**30:.1f} GiB free. This run requires 17 GiB free; no other jobs will be stopped.')
    torch.set_num_threads(4)
    out = ROOT/'outputs'/request['id']
    out.mkdir(parents=True, exist_ok=False)
    protocol = dict(request=request, source_revision=revision,
                    model_revision=Path(paths['m-a-p/YuE2-3B']).name,
                    vae_revision=Path(paths['m-a-p/YuE2-Vae']).name,
                    runtime={p:version(p) for p in ['yue2-infer','torch','transformers','numpy','huggingface-hub']},
                    pipeline=dict(device='cuda', memory_budget_gib=17, offload_ar=True,
                                  vae_core_frames=512, backend='torch', quantization='none'),
                    semantic_sampling=dict(max_tokens=9000),
                    recipe_difference='Use installed 0.1.6 runtime and pinned checkpoints from experiment 006; '
                                      'bundled instrumental release.json pins an older 0.1.5 recipe.',
                    status='submitted', preflight=checks)
    write(out/'attempt.json', protocol)
    start = time.perf_counter()
    try:
        torch.cuda.reset_peak_memory_stats()
        with YuE2Pipeline.from_pretrained(paths['m-a-p/YuE2-3B'], vae=paths['m-a-p/YuE2-Vae'],
                                         local_files_only=True, **protocol['pipeline']) as pipe:
            result = pipe(**request, semantic_sampling=protocol['semantic_sampling'])
            result.save_artifacts(out)
        verify_result(out)
        assert (out/'score.abc').read_text() == request['abc']
        import numpy as np
        import soundfile as sf
        info = sf.info(out/'audio.flac')
        assert info.samplerate == 48000 and info.channels == 2 and info.frames > 0
        peak, energy, samples, clipped = 0.0, 0.0, 0, 0
        for block in sf.blocks(out/'audio.flac', blocksize=48000, dtype='float32', always_2d=True):
            assert np.isfinite(block).all(), 'Nonfinite audio'
            peak = max(peak, float(np.abs(block).max()))
            energy += float(np.square(block, dtype=np.float64).sum())
            samples += block.size
            clipped += int((np.abs(block) >= .99999).sum())
        rms = (energy/samples)**.5
        assert rms > 1e-5, 'Generated audio is effectively silent'
        write(out/'measurement.json', dict(seconds=time.perf_counter()-start,
              peak_allocated_gib=torch.cuda.max_memory_allocated()/2**30,
              peak_reserved_gib=torch.cuda.max_memory_reserved()/2**30,
              audio_seconds=info.frames/info.samplerate, audio_peak=peak, audio_rms=rms,
              fraction_at_full_scale=clipped/samples, artifact_manifest_verified=True,
              truncated=result.truncated, score_preserved_in_artifacts=True,
              audio_note_adherence_measured=False))
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(out/'audio.flac'),
                        '-c:a','libmp3lame','-b:a','256k',str(out/'audio.mp3')],check=True)
        print('Saved', out, 'truncated:', result.truncated)
    except Exception as error:
        write(out/'failure.json',dict(error=str(error),traceback=traceback.format_exc()))
        raise


if __name__ == '__main__':
    main()
