#!/usr/bin/env python3
"""SFX + full narration for rogue-blackhole. No music, no beeps.
Space: cold drone; an ominous sub that swells as the hole closes in; a deep gravitational 'whoom' + scatter hiss at the
closest pass; a hit on the twist. Microlensing: rising shimmer. Lake shore at night: water lapping + crickets.
Frozen Earth: icy wind + ice cracks."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, FPS = 44100, T["fps"]; END = T["total"]; DUR = END / FPS; N = int(SR * DUR); B = T["beats"]
rng = np.random.default_rng(61)
ft = lambda f: f / FPS
t = np.arange(N) / SR
sos = lambda kind, f: butter(2, f, kind, fs=SR, output="sos")
lp = lambda x, f: sosfilt(sos("low", f), x)
hp = lambda x, f: sosfilt(sos("high", f), x)
bp = lambda x, a, b: sosfilt(sos("bandpass", [a, b]), x)
noise = lambda n: rng.standard_normal(n)
def env(points): fs, vs = zip(*points); return np.interp(t, np.array(fs) / FPS, vs)
def smooth(x, hz=3): return lp(lp(x, hz), hz)
dry_L, dry_R, wet_L, wet_R = (np.zeros(N) for _ in range(4))
def place(t0, y, g=1.0, pan=0.0, send=0.5):
    i = int(t0 * SR); j = min(N, i + len(y))
    if i >= N or j <= max(0, i): return
    y = y[:j - i] * g; a, b = (1 - max(0, pan)), (1 + min(0, pan))
    dry_L[i:j] += y * a; dry_R[i:j] += y * b; wet_L[i:j] += y * a * send; wet_R[i:j] += y * b * send
def bed(yL, yR, e, g, send=0.3):
    dry_L[:] += yL * e * g; dry_R[:] += yR * e * g; wet_L[:] += yL * e * g * send; wet_R[:] += yR * e * g * send
def whoosh(t0, d, g, lo=300, hi=5000):
    n = int(d * SR); u = np.linspace(0, 1, n); place(t0, bp(noise(n), lo, hi) * np.sin(np.pi * u) ** 2, g, 0, .5)

lake = env([(0, 0), (B[2] - 3, 0), (B[2] + 3, 1), (B[3] - 3, 1), (B[3] + 3, 0), (END, 0)])
frozen = env([(0, 0), (T["frozenIn"] - 3, 0), (T["frozenIn"] + 3, 1), (B[7] - 3, 1), (B[7] + 3, 0), (END, 0)])
space = np.clip(1 - lake - frozen, 0, 1)
# ---- cold space drone + ominous sub that grows with the approach
dr = sum(np.sin(2 * np.pi * fq * t + 0.4 * np.sin(2 * np.pi * .04 * t + k)) * a for k, (fq, a) in enumerate(((32.7, .5), (49, .35), (65.4, .2), (98, .1), (146.8, .05))))
threat = env([(0, .5), (B[3], .5), (B[4] - 10, 1.0), (B[4] + 40, 1.3), (B[5], 1.0), (END, .8)])
shimmer = bp(noise(N), 4500, 11000) * (0.5 + 0.5 * np.sin(2 * np.pi * .11 * t))
bed(dr * threat + shimmer * .25, dr * threat + shimmer[::-1] * .25, space + frozen * .4, .26, .6)
# ---- microlensing: a rising glassy shimmer while the ring forms
d = ft(B[2] - B[1]); n = int(d * SR); s = np.arange(n) / SR; u = s / d
place(ft(B[1]), (np.sin(2 * np.pi * 880 * s + 3 * np.sin(2 * np.pi * .4 * s)) * .15 + bp(noise(n), 3000, 9000) * .5) * np.sin(np.pi * u) ** 2, .2, 0, .9)
# ---- lake shore: water lapping + crickets
lap = lp(noise(N), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * .35 * t) ** 8)
bed(lap, lp(noise(N), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * .35 * t + 1.3) ** 8), lake, .25, .3)
for k in range(60):
    t0 = rng.uniform(ft(B[2]), ft(B[3]) - .3); fq = rng.uniform(4300, 5200); pan = rng.uniform(-.8, .8)
    for j in range(int(rng.integers(2, 5))):
        n = int(.022 * SR); s = np.arange(n) / SR; place(t0 + j * .055, np.sin(2 * np.pi * fq * s) * np.sin(np.pi * s / s[-1]), .02, pan, .4)
# ---- approach: Neptune pass whoosh, then the closest pass: a deep whoom + asteroid scatter hiss
whoosh(ft(B[3]) + 1.5, 2.5, .15, 200, 3000)
f_close = B[4] + int((22.9 - 21.2) / (24.6 - 21.2) * (B[5] - B[4]))
n = int(7 * SR); s = np.arange(n) / SR
place(ft(f_close) - .6, np.sin(2 * np.pi * np.cumsum(24 + 30 * np.exp(-((s - .6) / .5) ** 2)) / SR) * np.minimum(1, s * 2) * np.exp(-s * .45) * 1.3 + lp(noise(n), 200) * np.exp(-s * .5) * np.minimum(1, s * 3), .8, 0, .8)
for k in range(220):
    t0 = rng.uniform(ft(B[4]) + .5, ft(B[5]) + 1); n = int(rng.uniform(.15, .5) * SR); uu = np.linspace(0, 1, n)
    place(t0, bp(noise(n), 2000, 9000) * np.sin(np.pi * uu) ** 2, rng.uniform(.02, .05), rng.uniform(-.9, .9), .7)
# ---- the twist: a hollow hit
n = int(3 * SR); s = np.arange(n) / SR
place(ft(B[5]) + .1, (np.sin(2 * np.pi * 55 * s) + .5 * np.sin(2 * np.pi * 82.4 * s)) * np.exp(-s * 1.2) + hp(noise(n), 1500) * np.exp(-s * 25) * .5, .45, 0, .8)
# ---- frozen Earth: icy wind and ice cracking
gust = 0.5 + 0.5 * smooth(np.abs(noise(N)), 0.5) / 0.5
bed(bp(noise(N), 500, 3500) * gust, bp(noise(N), 520, 3600) * gust[::-1], frozen, .2, .5)
for k in range(9):
    t0 = rng.uniform(ft(T["frozenIn"]) + .5, ft(B[7]) - .5); n = int(.6 * SR); s = np.arange(n) / SR
    place(t0, hp(noise(n), 1200) * np.exp(-s * 18) + np.sin(2 * np.pi * np.cumsum(900 * np.exp(-s * 6) + 120) / SR) * np.exp(-s * 8) * .3, .2, rng.uniform(-.7, .7), .7)
for c in (B[1], B[2], B[3], B[4], B[6], T["frozenIn"], B[7]): whoosh(ft(c) - .3, .6, .09, 400, 5000)
# ---- reverb, dry narration, ducking
ir_n = int(3.5 * SR); s = np.arange(ir_n) / SR
irL = lp(noise(ir_n), 5000) * np.exp(-s * 1.8); irR = lp(noise(ir_n), 5000) * np.exp(-s * 1.8)
irL[: int(.012 * SR)] = 0; irR[: int(.017 * SR)] = 0; irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
L = dry_L + fftconvolve(wet_L, irL)[:N] * .9; R = dry_R + fftconvolve(wet_R, irR)[:N] * .9
mix = np.stack([hp(L, 25), hp(R, 25)], 1); mix /= np.abs(mix).max() + 1e-9
vo = np.zeros(N)
for i, f in enumerate(T["vo"]):
    sr, y = wavfile.read(f"{ROOT}/vo/l{i}.wav"); y = y.astype(np.float64) / (32768 if y.dtype == np.int16 else 1)
    if y.ndim > 1: y = y.mean(1)
    if sr != SR: y = np.interp(np.arange(int(len(y) * SR / sr)) * sr / SR, np.arange(len(y)), y)
    a = int(ft(f) * SR); b = min(N, a + len(y)); vo[a:b] += y[: b - a]
vo = hp(vo, 80) / (np.abs(vo).max() + 1e-9)
duck = 1 - .55 * np.clip(smooth(np.abs(vo), 6) * 6, 0, 1)
mix = mix * duck[:, None] * .5 + np.stack([vo, vo], 1) * .9
mix /= np.abs(mix).max() + 1e-9; mix = np.tanh(mix * 1.15) / np.tanh(1.15) * .9
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s; loudest", round(max(rms), 1))
