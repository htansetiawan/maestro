"""Auto-label: draft captions and metadata from the audio itself, for a human to confirm.

Three analyses feed a deterministic caption template:

* tempo and key (librosa beat tracking, Krumhansl-Schmuckler key profiles);
* structure (beat-synchronous features, agglomerative segmentation, loudness per section);
* instrument presence over time (CLAP zero-shot scores on a fixed vocabulary).

The template writes the same words for the same evidence every time, which is what the
downstream model needs: a consistent vocabulary it can be prompted with later. Every draft
is written as ``TODO: <draft>`` so the training gate still refuses it until a person has
listened and saved. Nothing here is a judgment of quality.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import soundfile as sf

from .config import Config
from .io import read_jsonl, write_json, write_jsonl

ANALYSIS_DIR = Path("data/analysis")
SR = 22050
PITCH_NAMES = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

# Controlled vocabulary: manifest word -> CLAP text prompt. Keep these words in captions.
VOCABULARY = {
    "piano": "grand piano playing melody and chords",
    "strings": "orchestral strings, violins and cellos",
    "drums": "a drum kit with snare and hi-hat",
    "bass": "electric bass guitar",
    "electric guitar": "electric guitar",
    "acoustic guitar": "acoustic guitar strumming or picking",
    "synthesizer": "synthesizer pads",
    "brass": "trumpets and a brass section",
    "saxophone": "saxophone solo",
    "choir": "a choir of many voices singing",
    "male vocals": "a man singing lead vocals",
    "female vocals": "a woman singing lead vocals",
}
VOCAL_TAGS = {"male vocals", "female vocals", "choir"}
# Zero-shot CLAP probabilities are soft and spread across the vocabulary. A tag is listed
# when it is in the top three of a window with at least this probability, in at least
# this share of the windows. Below that it is treated as noise, not an instrument.
TAG_MIN_PROB = 0.15
TAG_TOP_K = 3
TAG_MIN_SHARE = 0.25
TAG_MIN_WINDOWS = 2


# --------------------------------------------------------------------------- signal analysis


def load_mono(path: Path, sr: int = SR) -> tuple[np.ndarray, int]:
    import librosa

    y, _ = librosa.load(path, sr=sr, mono=True)
    return y.astype(np.float32), sr


def estimate_tempo(y: np.ndarray, sr: int) -> dict:
    import librosa

    onset = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = float(np.atleast_1d(librosa.feature.tempo(onset_envelope=onset, sr=sr,
                                                      start_bpm=90, std_bpm=1.0))[0])
    note = ""
    if tempo > 140:  # ballads often come back doubled; report the felt pulse
        tempo, note = tempo / 2, "halved from a double-time estimate"
    density = float(len(librosa.onset.onset_detect(onset_envelope=onset, sr=sr)) / (len(y) / sr))
    return {"bpm": int(round(tempo)), "note": note, "onsets_per_second": round(density, 2)}


def estimate_key(y: np.ndarray, sr: int) -> dict:
    import librosa

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    profile = chroma.mean(axis=1)
    if profile.sum() <= 0:
        return {"keyscale": "", "confidence": 0.0}
    scores = []
    for shift in range(12):
        rolled = np.roll(profile, -shift)
        scores.append((float(np.corrcoef(rolled, MAJOR)[0, 1]), shift, "major"))
        scores.append((float(np.corrcoef(rolled, MINOR)[0, 1]), shift, "minor"))
    scores.sort(reverse=True)
    best, second = scores[0], scores[1]
    return {"keyscale": f"{PITCH_NAMES[best[1]]} {best[2]}",
            "confidence": round(best[0] - second[0], 3),
            "runner_up": f"{PITCH_NAMES[second[1]]} {second[2]}"}


def estimate_sections(y: np.ndarray, sr: int, duration: float,
                      min_section_seconds: float = 12.0) -> list[dict]:
    """Coarse sections with a loudness label each. Boundaries are approximate.

    Timbre (MFCC), harmony (chroma) and loudness are z-scored so each counts equally,
    smoothed over about two seconds, then over-segmented and merged back until no
    section is shorter than ``min_section_seconds``. Short attack and decay frames at the
    edges therefore never become sections of their own.
    """
    import librosa

    hop = 512
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=hop)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    loud = 20 * np.log10(rms + 1e-6)
    feats = np.vstack([mfcc, chroma, loud[None, :], loud[None, :]])
    feats = (feats - feats.mean(axis=1, keepdims=True)) / (feats.std(axis=1, keepdims=True) + 1e-9)
    win = max(1, int(2 * sr / hop))
    kernel = np.ones(win) / win
    feats = np.vstack([np.convolve(row, kernel, mode="same") for row in feats])
    n = feats.shape[1]
    min_frames = max(1, int(min_section_seconds * sr / hop))
    k = int(np.clip(round(duration / 12), 2, 24))
    bounds = list(librosa.segment.agglomerative(feats, k)) + [n]
    # Merge short sections into the neighbour whose mean feature is closer.
    changed = True
    while changed and len(bounds) > 2:
        changed = False
        for i in range(len(bounds) - 1):
            if bounds[i + 1] - bounds[i] < min_frames:
                left_ok, right_ok = i > 0, i + 2 < len(bounds)
                if left_ok and right_ok:
                    seg = feats[:, bounds[i]:bounds[i + 1]].mean(axis=1)
                    left = feats[:, bounds[i - 1]:bounds[i]].mean(axis=1)
                    right = feats[:, bounds[i + 1]:bounds[i + 2]].mean(axis=1)
                    drop = i if np.linalg.norm(seg - left) <= np.linalg.norm(seg - right) else i + 1
                elif left_ok:
                    drop = i
                else:
                    drop = i + 1
                del bounds[drop]
                changed = True
                break
    ref = np.percentile(rms[rms > 0], 95) if np.any(rms > 0) else 1.0
    sections = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        level = float(20 * np.log10((rms[a:b].mean() + 1e-9) / (ref + 1e-9)))
        label = "full" if level > -6 else "moderate" if level > -14 else "quiet"
        t0, t1 = librosa.frames_to_time([a, b], sr=sr, hop_length=hop)
        sections.append({"start": round(float(t0), 1), "end": round(float(t1), 1),
                         "level_db": round(level, 1), "dynamics": label})
    return sections


def clap_tags(path: Path, window_seconds: float = 10.0, device: str | None = None) -> dict:
    """Zero-shot instrument presence per window with a frozen CLAP model."""
    import torch
    from transformers import AutoProcessor, ClapModel

    name = "laion/clap-htsat-unfused"
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    processor = AutoProcessor.from_pretrained(name)
    model = ClapModel.from_pretrained(name).to(device).eval()
    words = list(VOCABULARY)
    with torch.no_grad():
        text = processor(text=[VOCABULARY[w] for w in words], return_tensors="pt", padding=True)
        text_emb = model.get_text_features(**{k: v.to(device) for k, v in text.items()})
        text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
    info = sf.info(path)
    windows = []
    with sf.SoundFile(path) as handle:
        frames = int(window_seconds * info.samplerate)
        start = 0
        while start < info.frames:
            handle.seek(start)
            block = handle.read(frames, dtype="float32", always_2d=True).mean(axis=1)
            if len(block) < info.samplerate * 3:
                break
            import librosa

            mono = librosa.resample(block, orig_sr=info.samplerate, target_sr=48000)
            inputs = processor(audios=mono, sampling_rate=48000, return_tensors="pt")
            with torch.no_grad():
                emb = model.get_audio_features(**{k: v.to(device) for k, v in inputs.items()})
                emb = emb / emb.norm(dim=-1, keepdim=True)
                probs = (100 * emb @ text_emb.T).softmax(dim=-1)[0].cpu().numpy()
            windows.append({"start": round(start / info.samplerate, 1),
                            "probs": {w: round(float(p), 3) for w, p in zip(words, probs)}})
            start += frames
    return {"window_seconds": window_seconds, "windows": windows, "model": name}


def summarise_tags(tags: dict) -> dict:
    """Which vocabulary words are present overall, and when each first appears."""
    windows = tags.get("windows", [])
    present, first_seen, mass = {}, {}, {}
    for w in windows:
        ranked = sorted(w["probs"].items(), key=lambda kv: -kv[1])[:TAG_TOP_K]
        for word, p in ranked:
            if p >= TAG_MIN_PROB:
                present[word] = present.get(word, 0) + 1
                mass[word] = mass.get(word, 0.0) + p
                first_seen.setdefault(word, w["start"])
    need = max(TAG_MIN_WINDOWS, int(np.ceil(TAG_MIN_SHARE * len(windows))))
    kept = {w: n for w, n in present.items() if n >= need}
    # Vocals are allowed with a lower share: a verse or two of singing is still singing.
    for w, n in present.items():
        if w in VOCAL_TAGS and n >= TAG_MIN_WINDOWS and w not in kept and \
                n >= 0.15 * len(windows):
            kept[w] = n
    ordered = sorted(kept, key=lambda w: (-mass.get(w, 0.0), first_seen[w]))
    return {"instruments": [w for w in ordered if w not in VOCAL_TAGS],
            "vocals": [w for w in ordered if w in VOCAL_TAGS],
            "first_seen": {w: first_seen[w] for w in ordered},
            "window_counts": kept, "windows_total": len(windows)}


# --------------------------------------------------------------------------- caption template


def _mmss(s: float) -> str:
    return f"{int(s // 60)}:{int(s % 60):02d}"


def tempo_word(bpm: int) -> str:
    if bpm < 66:
        return "very slow"
    if bpm < 84:
        return "slow"
    if bpm < 104:
        return "moderate"
    if bpm < 128:
        return "medium-up"
    return "fast"


def draft_caption(analysis: dict) -> str:
    """Describe analysis evidence without inferring musical roles or genre.

    Tag frequency cannot identify the lead instrument, and the first matching
    window is not necessarily an entrance. These remain human refinements.
    """
    tags = analysis["tags"]
    instruments = tags["instruments"]
    vocals = tags["vocals"]
    sections = analysis["sections"]
    parts = []
    if vocals:
        voice = " and ".join(vocals)
        parts.append(f"Music with {voice}.")
    else:
        # An empty detector result also occurs with --no-clap. Absence of
        # detected vocals alone is not evidence that a recording is instrumental.
        parts.append("Music recording.")
    if instruments:
        parts.append(f"Instrumentation includes {', '.join(instruments)}.")
    if sections:
        opening = sections[0]["dynamics"]
        loudest = max(sections, key=lambda s: s["level_db"])
        closing = sections[-1]["dynamics"]
        arc = f"{opening.capitalize()} opening"
        if loudest is not sections[0] and loudest is not sections[-1]:
            arc += f"; loudest section starts around {_mmss(loudest['start'])}"
        arc += f"; {closing} ending."
        parts.append(arc)
    bpm = analysis["tempo"]["bpm"]
    key = analysis["key"]["keyscale"]
    parts.append(f"{tempo_word(bpm).capitalize()} tempo, {bpm} BPM" + (f", {key}." if key else "."))
    return " ".join(parts)


# --------------------------------------------------------------------------- driver


def analyse_clip(path: Path, use_clap: bool = True, device: str | None = None) -> dict:
    y, sr = load_mono(path)
    duration = len(y) / sr
    analysis = {"duration": round(duration, 1), "tempo": estimate_tempo(y, sr),
                "key": estimate_key(y, sr), "sections": estimate_sections(y, sr, duration)}
    raw = clap_tags(path, device=device) if use_clap else {"windows": []}
    analysis["tags"] = summarise_tags(raw)
    analysis["tags_raw"] = raw
    analysis["caption"] = draft_caption(analysis)
    analysis["suggested_role"] = "reference" if analysis["tags"]["vocals"] else "train"
    return analysis


def autolabel(root: Path, cfg: Config, ids: list[str] | None = None, force: bool = False,
              use_clap: bool = True, device: str | None = None, log=print) -> dict:
    """Analyse manifest rows and write draft captions + metadata. Skips human captions."""
    manifest = root / cfg.data.manifest
    rows = read_jsonl(manifest)
    out_dir = root / ANALYSIS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    done, skipped = [], []
    for row in rows:
        if ids and row["id"] not in ids:
            continue
        if "TODO" not in row["caption"] and not force:
            skipped.append(row["id"])
            continue
        path = root / row["audio_path"]
        log(f"analysing {row['id']} ({path.name})")
        analysis = analyse_clip(path, use_clap=use_clap, device=device)
        write_json(out_dir / f"{row['id']}.json", analysis)
        row["caption"] = "TODO: " + analysis["caption"]
        row["bpm"] = analysis["tempo"]["bpm"]
        if analysis["key"]["keyscale"]:
            row["keyscale"] = analysis["key"]["keyscale"]
        row["timesignature"] = row.get("timesignature") or "4"
        words = analysis["tags"]["instruments"] + analysis["tags"]["vocals"]
        if words:
            row["instruments"] = words
        done.append(row["id"])
        log(f"  -> {analysis['caption']}")
        write_jsonl(manifest, rows)
    return {"labelled": done, "skipped_human": skipped}


def load_analysis(root: Path, clip_id: str) -> dict | None:
    path = root / ANALYSIS_DIR / f"{clip_id}.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text())
    data.pop("tags_raw", None)  # large; the UI only needs the summary
    return data
