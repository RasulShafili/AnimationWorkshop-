#!/usr/bin/env python3
"""SFX + full narration for andromeda. No music, no beeps. Ground (sky) shots: night breeze + crickets.
Space shots: deep evolving drone, airy shimmer; a slow sub swell into each galaxy pass; a big low 'whoom' at the
first collision; glittering for the starburst; a soft data-shimmer for the 100,000 simulations."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, FPS = 44100, T["fps"]; END = T["total"]; DUR = END / FPS; N = int(SR * DUR); B = T["beats"]
rng = np.random.default_rng(51)
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

ground = env([(0, 1), (B[3] - 3, 1), (B[3] + 3, 0), (T["skyIn"] - 3, 0), (T["skyIn"] + 3, 1), (B[5] - 3, 1), (B[5] + 3, 0), (B[7] - 3, 0), (B[7] + 3, 1), (END, 1)])
space = 1 - ground
# ---- night on the ridge: breeze + crickets
gust = 0.6 + 0.4 * smooth(np.abs(noise(N)), 0.4) / 0.5
bed(bp(noise(N), 200, 1200) * gust, bp(noise(N), 210, 1300) * gust[::-1], ground, .12, .4)
for k in range(140):
    t0 = rng.uniform(0, DUR - .3)
    if ground[int(t0 * SR)] < .5: continue
    fq = rng.uniform(4300, 5200); pan = rng.uniform(-.8, .8)
    for j in range(int(rng.integers(2, 5))):
        n = int(.022 * SR); s = np.arange(n) / SR
        place(t0 + j * .055, np.sin(2 * np.pi * fq * s) * np.sin(np.pi * s / s[-1]), .02, pan, .4)
# ---- space drone: slow chords of sines + filtered noise, evolving
dr = sum(np.sin(2 * np.pi * fq * t + 0.3 * np.sin(2 * np.pi * .05 * t + k)) * a for k, (fq, a) in enumerate(((36.7, .5), (55, .4), (73.4, .25), (110, .12), (164.8, .06))))
dr *= 0.7 + 0.3 * np.sin(2 * np.pi * .07 * t)
shimmer = bp(noise(N), 4000, 10000) * (0.5 + 0.5 * np.sin(2 * np.pi * .13 * t))
bed(dr + shimmer * .3, dr + shimmer[::-1] * .3, space * env([(0, .4), (B[2], .7), (B[3], 1), (END, 1)]) + ground * .25, .25, .6)
# ---- time-lapse whoosh as Andromeda grows (beat 2)
d = ft(B[3] - B[2]); n = int(d * SR); u = np.linspace(0, 1, n)
place(ft(B[2]), (bp(noise(n), 150, 2500) * u ** 1.5 + np.sin(2 * np.pi * np.cumsum(40 + 50 * u) / SR) * u * .5), .35, 0, .6)
# ---- galaxy passes: slow sub swells; the first collision gets a long low 'whoom'
def swell(t0, d, g):
    n = int(d * SR); s = np.arange(n) / SR; u = s / d
    place(t0, (np.sin(2 * np.pi * np.cumsum(30 + 25 * np.sin(np.pi * u)) / SR) + lp(noise(n), 160) * .8) * np.sin(np.pi * u) ** 1.5, g, 0, .7)
f_first = int(B[3] + (9.24 - 6.6) / (11.6 - 6.6) * (B[4] - B[3]))
swell(ft(f_first) - 2.0, 4.5, .9)
n = int(6 * SR); s = np.arange(n) / SR
place(ft(f_first), np.sin(2 * np.pi * np.cumsum(26 + 40 * np.exp(-s * 2)) / SR) * np.exp(-s * .6) * 1.2 + lp(noise(n), 220) * np.exp(-s * .5) * np.minimum(1, s * 4), .7, 0, .8)
swell(ft(B[5]) + .5, 3.5, .6)
# ---- starburst glitter: thousands of tiny bright pings (not beeps: noisy and soft)
for k in range(260):
    t0 = rng.uniform(ft(B[4]), ft(B[5]) + 1.5); n = int(rng.uniform(.03, .09) * SR); s = np.arange(n) / SR
    place(t0, bp(noise(n), 5000, 12000) * np.exp(-s * 60), rng.uniform(.03, .08), rng.uniform(-.9, .9), .8)
# ---- the 100,000 simulations: a rushing data shimmer
d = ft(B[7] - B[6]); n = int(d * SR); u = np.linspace(0, 1, n)
place(ft(B[6]) + 1.3, bp(noise(n), 2500, 9000) * np.sin(np.pi * u) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * np.arange(n) / SR)), .18, 0, .7)
for c in (B[1], B[2], B[3], T["skyIn"], B[5], B[6], B[7]):
    n = int(.6 * SR); u = np.linspace(0, 1, n); place(ft(c) - .3, bp(noise(n), 400, 5000) * np.sin(np.pi * u) ** 2, .1, 0, .6)
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
