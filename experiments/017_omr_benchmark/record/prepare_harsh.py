"""Third page condition: a phone photograph of a printed page.

Takes the clean 300 dpi renderings and produces pages/harsh: half resolution
(about 150 dpi), 1.5 degree skew, uneven lighting across the page, lens blur,
sensor noise and JPEG compression at quality 40. Unlike the 'degraded' condition
(skew 0.5 degrees, blur, hard threshold), this is meant to resemble what a user
actually uploads from a phone.
"""
import io
from pathlib import Path
import random

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
random.seed(20261018)
rng = np.random.default_rng(20261018)


def harsh(img):
    w, h = img.size
    small = img.resize((w // 2, h // 2), Image.LANCZOS)
    rotated = small.rotate(random.choice([-1.5, 1.5]), resample=Image.BICUBIC, fillcolor=235, expand=False)
    a = np.asarray(rotated).astype(np.float32)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    light = 0.62 + 0.38 * (xx / a.shape[1]) * (1 - 0.3 * yy / a.shape[0])   # darker on the left, lighter to the right
    a = a * light
    a = np.clip(a + rng.normal(0, 10, a.shape), 0, 255).astype(np.uint8)
    blurred = Image.fromarray(a).filter(ImageFilter.GaussianBlur(radius=1.0))
    buf = io.BytesIO()
    blurred.convert('RGB').save(buf, 'JPEG', quality=40)
    return Image.open(io.BytesIO(buf.getvalue())).convert('L')


def main():
    out = ROOT / 'pages/harsh'
    out.mkdir(parents=True, exist_ok=True)
    for p in sorted((ROOT / 'pages/clean').glob('*.png')):
        harsh(Image.open(p).convert('L')).save(out / p.name)
        print('wrote', out / p.name)


if __name__ == '__main__':
    main()
