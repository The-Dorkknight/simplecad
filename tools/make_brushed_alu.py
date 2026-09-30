#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright Matthew Armstrong (https://github.com/The-Dorkknight)
# Licensed under the PolyForm Noncommercial License 1.0.0. No warranty.
"""Seamless brushed-aluminium grain tile (from the brushed-aluminium-panel skill),
plus SimpleCAD's Qt variants."""
import argparse, numpy as np
from PIL import Image
ap = argparse.ArgumentParser()
ap.add_argument("--amp", type=float, default=18)
ap.add_argument("--streak", type=float, default=17)
ap.add_argument("--seed", type=int, default=31)
ap.add_argument("--w", type=int, default=1024); ap.add_argument("--h", type=int, default=512)
a = ap.parse_args()
rng = np.random.default_rng(a.seed); W, H = a.w, a.h
ky = np.fft.fftfreq(H)[:, None] * 2 * np.pi; kx = np.fft.fftfreq(W)[None, :] * 2 * np.pi
def aniso(sx, sy, src=None):
    n = rng.standard_normal((H, W)) if src is None else src
    r = np.real(np.fft.ifft2(np.fft.fft2(n) * np.exp(-0.5 * ((kx * sx) ** 2 + (ky * sy) ** 2))))
    return (r - r.mean()) / r.std()
patch = np.abs(aniso(160, 40))
streaks = aniso(a.streak, 0.5) * (0.75 + 0.5 * patch)
fine = aniso(6, 0.45)
sparks = (rng.random((H, W)) > 0.993) * rng.uniform(1, 2.5, (H, W))
glints = np.maximum(aniso(9, 0.4, sparks.astype(float)), 0)
g = 0.8 * streaks + 0.5 * fine + 0.5 * glints
g = (g - g.mean()) / g.std()
grain = np.clip(128 + g * a.amp, 0, 255).astype(np.uint8)
# 1) raw grey grain, drawn by QPainter in Overlay mode at half size (retina-sharp)
Image.fromarray(grain, "L").save("brushed_alu_grain.png", optimize=True)
# 2) pre-blended tile for Qt stylesheets (no blend modes there): grain overlaid on #9ea3a7
base = np.array([0x9e, 0xa3, 0xa7], float) / 255.0
gn = grain.astype(float)[..., None] / 255.0
over = np.where(base < 0.5, 2 * base * gn, 1 - 2 * (1 - base) * (1 - gn))
tile = Image.fromarray((over * 255).round().astype(np.uint8), "RGB")
tile.resize((W // 2, H // 2), Image.LANCZOS).save("brushed_alu_tile.png", optimize=True)
print("done")
