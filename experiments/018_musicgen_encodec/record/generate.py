"""MusicGen-melody and EnCodec on the same melodies as 014 and 016.

MusicGen-melody (Meta, 2023; 1.5B parameters) is a text-to-music language model
over EnCodec tokens that also accepts a reference recording, reduced to a
chromagram, as a melody condition. It generates at most 30 s. Conditions here
share the prompt "solo acoustic grand piano, expressive ballad, no vocals";
the melody reference changes:

  cp-guide       Color Purple written melody, synthesized guide (014), first 30 s
  cp-recording   Color Purple source recording (005), first 30 s
  cp-text-only   no melody reference (control)
  she-guide      She transcribed vocal line, synthesized guide (016), first 30 s

EnCodec round trips (encode then decode, nothing generated) measure what the
codec layer alone keeps of the Color Purple recording's melody: encodec_24khz
at 1.5, 3, 6, 12 and 24 kbps, and MusicGen's own 32 kHz codec (4 codebooks,
about 2.2 kbps), the representation MusicGen generates in.

MP3 only is kept (experiments/AGENTS.md). Everything runs with HF_HOME set to
~/maestro-runtime/hf.
"""
import json
from pathlib import Path
import subprocess
import time

import librosa
import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, EncodecModel, MusicgenMelodyForConditionalGeneration

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT.parent
PROMPT = 'solo acoustic grand piano, expressive ballad, no vocals'
SEED = 20261018
REFS = {
    'cp-guide': EXP / '014_yue2_excerpt_ablation/inputs/melody-guide.mp3',
    'cp-recording': EXP / '005_color_purple_orchestra/data/source.wav',
    'cp-text-only': None,
    'she-guide': EXP / '016_she_sheet_to_voice/inputs/melody-guide.mp3',
}


def to_mp3(wav, sr, out):
    tmp = out.with_suffix('.wav')
    sf.write(tmp, wav, sr)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(tmp), '-c:a', 'libmp3lame', '-b:a', '256k', str(out)], check=True)
    tmp.unlink()


def musicgen(dev):
    proc = AutoProcessor.from_pretrained('facebook/musicgen-melody')
    model = MusicgenMelodyForConditionalGeneration.from_pretrained('facebook/musicgen-melody', torch_dtype=torch.float32).to(dev).eval()
    sr_out = model.config.audio_encoder.sampling_rate
    log = []
    for cond, ref in REFS.items():
        out = ROOT / 'outputs' / cond
        out.mkdir(parents=True, exist_ok=True)
        if ref is None:
            inputs = proc(text=[PROMPT], padding=True, return_tensors='pt')
        else:
            y, _ = librosa.load(str(ref), sr=proc.feature_extractor.sampling_rate, mono=True, duration=30.0)
            inputs = proc(audio=y, sampling_rate=proc.feature_extractor.sampling_rate, text=[PROMPT], padding=True, return_tensors='pt')
        torch.manual_seed(SEED)
        t0 = time.time()
        with torch.no_grad():
            audio = model.generate(**{k: v.to(dev) for k, v in inputs.items()}, do_sample=True, guidance_scale=3.0, max_new_tokens=1500)
        wav = audio[0, 0].float().cpu().numpy()
        to_mp3(wav, sr_out, out / 'audio.mp3')
        rec = dict(condition=cond, reference=str(ref.relative_to(EXP)) if ref else None, prompt=PROMPT, seed=SEED, guidance_scale=3.0,
                   max_new_tokens=1500, audio_seconds=len(wav) / sr_out, seconds=time.time() - t0,
                   peak_allocated_gib=torch.cuda.max_memory_allocated() / 2**30 if dev == 'cuda' else None,
                   model='facebook/musicgen-melody', transformers=__import__('transformers').__version__)
        (out / 'generation.json').write_text(json.dumps(rec, indent=2) + '\n')
        print(json.dumps(rec), flush=True)
        log.append(rec)
    codec = model.audio_encoder  # the 32 kHz EnCodec MusicGen generates in
    del model
    return codec, log


def roundtrips(dev, musicgen_codec):
    src = REFS['cp-recording']
    y, sr = librosa.load(str(src), sr=None, mono=True, duration=46.0)
    recs = []
    enc = EncodecModel.from_pretrained('facebook/encodec_24khz').to(dev).eval()
    y24 = librosa.resample(y, orig_sr=sr, target_sr=24000)
    for bw in (1.5, 3.0, 6.0, 12.0, 24.0):
        x = torch.tensor(y24)[None, None].to(dev)
        with torch.no_grad():
            e = enc.encode(x, bandwidth=bw)
            d = enc.decode(e.audio_codes, e.audio_scales)[0]
        out = ROOT / 'outputs' / f'encodec24-{bw:g}kbps'
        out.mkdir(parents=True, exist_ok=True)
        to_mp3(d[0, 0].cpu().numpy(), 24000, out / 'audio.mp3')
        recs.append(dict(condition=out.name, model='facebook/encodec_24khz', bandwidth_kbps=bw, codebooks=int(e.audio_codes.shape[-2]), seconds_audio=len(y24) / 24000))
    y32 = librosa.resample(y, orig_sr=sr, target_sr=32000)
    x = torch.tensor(y32)[None, None].to(dev)
    with torch.no_grad():
        e = musicgen_codec.encode(x)
        d = musicgen_codec.decode(e.audio_codes, e.audio_scales)[0]
    out = ROOT / 'outputs' / 'encodec32-musicgen'
    out.mkdir(parents=True, exist_ok=True)
    to_mp3(d[0, 0].cpu().numpy(), 32000, out / 'audio.mp3')
    recs.append(dict(condition=out.name, model='musicgen-melody audio_encoder (EnCodec 32 kHz)', codebooks=int(e.audio_codes.shape[-2]),
                     frame_rate_hz=50, seconds_audio=len(y32) / 32000))
    for r in recs:
        (ROOT / 'outputs' / r['condition'] / 'generation.json').write_text(json.dumps(r, indent=2) + '\n')
        print(json.dumps(r), flush=True)
    return recs


def main():
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    codec, log = musicgen(dev)
    log += roundtrips(dev, codec)
    (ROOT / 'record/generation-log.json').write_text(json.dumps(log, indent=2) + '\n')
    print('GEN18_DONE', flush=True)


if __name__ == '__main__':
    main()
