"""Extract a small, reproducible Foster style-training corpus."""
import hashlib
import json
from pathlib import Path

import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "001_ace_audio_personalization"
EXCLUDED = {"loc-01-theme-from-the-color-purple-001",  # evaluation composition
            "loc-01-03-this-must-be-love-001", "loc-glory-of-love-001"}  # alternate encodes


def main():
    clips = ROOT / "data/clips"
    clips.mkdir(parents=True, exist_ok=True)
    manifest = ROOT / "data/dataset.json"
    if manifest.exists():
        raise FileExistsError(manifest)
    samples = []
    for line in (SOURCE / "data/recordings.jsonl").read_text().splitlines():
        row = json.loads(line)
        if not row["id"].startswith("loc-") or row["id"] in EXCLUDED:
            continue
        source = SOURCE / row["audio_path"]
        with source.open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").hexdigest()
        info = sf.info(source)
        for offset in (30, 120):
            target = clips / f"{row['id']}-{offset}s.wav"
            if target.exists():
                raise FileExistsError(target)
            audio, sr = sf.read(source, start=offset * info.samplerate,
                                frames=30 * info.samplerate, dtype="float32", always_2d=True)
            assert len(audio) == 30 * sr
            sf.write(target, audio, sr, subtype="PCM_24")
            samples.append(dict(filename=target.name, audio_path=str(target),
                                caption="Music from a David Foster recording.",
                                lyrics="", is_instrumental=False, duration=30,
                                bpm=None, keyscale="", timesignature="",
                                source_id=row["id"], source_path=str(source),
                                source_sha256=digest, offset_seconds=offset,
                                lyrics_status="unknown; empty conditioning",
                                instrumentation_status="not annotated; mixed vocal/instrumental corpus",
                                rights=row["rights"]))
    manifest.write_text(json.dumps({"samples": samples}, indent=2) + "\n")
    print(f"{len(samples)} clips, {len(samples) * 30 / 60:g} minutes; {manifest}")


if __name__ == "__main__":
    main()
