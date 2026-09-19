from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parents[2]
ID_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Runtime(StrictModel):
    ace_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    variant: Literal["base", "sft", "turbo", "xl_base", "xl_sft", "xl_turbo"] = "base"
    device: Literal["cuda", "cpu", "mps"] = "cuda"
    precision: Literal["bf16", "fp32"] = "bf16"


class Data(StrictModel):
    manifest: str = "data/recordings.jsonl"
    min_seconds: float = Field(default=10, gt=0)
    max_seconds: float = Field(default=180, gt=0, le=600)
    validation_fraction: float = Field(default=0.2, gt=0, lt=1)
    # External material (e.g. YouTube) enters the manifest with rights="unverified".
    # It can be staged as listening/analysis reference by default; putting it into the
    # training split requires this explicit opt-in, which is recorded in the frozen config.
    allow_unverified_rights: bool = False


class LoRA(StrictModel):
    rank: int = Field(default=16, gt=0)
    alpha: int = Field(default=32, gt=0)
    dropout: float = Field(default=0, ge=0, lt=1)


class Train(StrictModel):
    steps: int = Field(default=200, gt=0)
    learning_rate: float = Field(default=1e-4, gt=0)
    gradient_accumulation: int = Field(default=4, gt=0)
    save_every: int = Field(default=50, gt=0)
    validation_samples: int = Field(default=4, gt=0)
    cfg_dropout: float = Field(default=0.15, ge=0, le=1)


class Preference(StrictModel):
    steps: int = Field(default=100, gt=0)
    learning_rate: float = Field(default=1e-5, gt=0)
    gradient_accumulation: int = Field(default=2, gt=0)
    save_every: int = Field(default=25, gt=0)
    beta: float = Field(default=10, gt=0)
    sft_anchor: float = Field(default=0.1, ge=0)


class Generation(StrictModel):
    feedback_prompts: str = "prompts/feedback.jsonl"
    eval_prompts: str = "prompts/eval.jsonl"
    seeds: list[int] = Field(default=[101, 202], min_length=2)
    inference_steps: int = Field(default=50, gt=0)
    guidance_scale: float = Field(default=7, ge=1, le=15)


class Judge(StrictModel):
    model: str = "laion/clap-htsat-unfused"
    min_margin: float = Field(default=0.01, ge=0)
    window_seconds: float = Field(default=10, gt=0, le=10)


class Config(StrictModel):
    seed: int = Field(default=42, ge=0)
    runtime: Runtime
    data: Data = Data()
    lora: LoRA = LoRA()
    sft: Train = Train()
    preference: Preference = Preference()
    generation: Generation = Generation()
    judge: Judge = Judge()


def load_config(path: Path) -> Config:
    cfg = Config.model_validate(tomllib.loads(path.read_text()))
    if cfg.data.min_seconds > cfg.data.max_seconds:
        raise ValueError("min_seconds must not exceed max_seconds")
    if len(set(cfg.generation.seeds)) != len(cfg.generation.seeds):
        raise ValueError("Generation seeds must be distinct")
    if any(seed < 0 for seed in cfg.generation.seeds):
        raise ValueError("Generation seeds must be nonnegative")
    if "turbo" in cfg.runtime.variant and cfg.generation.inference_steps > 20:
        raise ValueError("Use at most 20 inference steps for a turbo checkpoint")
    return cfg
