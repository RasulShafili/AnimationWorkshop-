#!/usr/bin/env python3
"""SFX + Kokoro narration for punch-doubles. No music. Timings: src/timeline.json.
Cold open (planet cracks, breaks) -> REWIND (cold-open audio reversed) -> arena crowd, punch thuds, KO crash ->
TNT blast -> Hiroshima -> asteroid -> oceans hiss -> ruined ring wind, bell, charge riser, last punch -> planet breaks.
A soft tick on every doubling of the punch counter (rate-capped)."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, FPS = 44100, T["fps"]; END = T["total"]; DUR = END / FPS; N = int(SR * DUR); B = T["beats"]
rng = np.random.default_rng(21)
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
def boom(t0, g, length=5.0, low=38):
    n = int(length * SR); s = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(low + 70 * np.exp(-s * 6)) / SR) * np.exp(-s * 1.1)
    crack = (noise(n) * np.exp(-s * 14) + hp(noise(n), 2500) * np.exp(-s * 30)) * .8
    roll = lp(noise(n), 220) * (0.5 + 0.5 * smooth(np.abs(noise(n)), 3) / 0.6) * np.exp(-s * 0.7) * np.minimum(1, s * 6)
    place(t0, sub + crack + roll * 1.4, g, 0, 0.6)
def whoosh(t0, d, g, lo=300, hi=5000, rise=False):
    n = int(d * SR); u = np.linspace(0, 1, n); shape = u ** 2 if rise else np.sin(np.pi * u) ** 2
    place(t0, bp(noise(n), lo, hi) * shape, g, 0, 0.6)
def thud(t0, g, pan=0):
    n = int(.35 * SR); s = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-s * 30)) / SR) * np.exp(-s * 14) + lp(noise(n), 1800) * np.exp(-s * 40) * .7 + hp(noise(n), 3000) * np.exp(-s * 90) * .3
    place(t0, y, g, pan, 0.3)
def bell(t0, g):
    n = int(2.5 * SR); s = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * s) * a * np.exp(-s * d) for f, a, d in ((1180, 1, 1.4), (2950, .5, 2.5), (4330, .3, 3.5), (6100, .15, 5)))
    place(t0, y * np.minimum(1, s * 400), g, 0, 0.5)

arena = env([(0, 0), (B[2] - 2, 0), (B[2] + 6, 1), (T["tnt"], 1), (T["tnt"] + 2, 0), (END, 0)])
space = env([(0, 1), (B[1], 1), (B[2] - 2, 1), (B[2], 0), (B[6] - 2, 0), (B[6] + 2, 1), (B[8] - 2, 1), (B[8], 0), (T["last"] + 17, 0), (T["last"] + 19, 1), (END, 1)])
ruin = env([(0, 0), (B[8] - 2, 0), (B[8] + 4, 1), (T["last"] + 17, 1), (T["last"] + 19, 0), (END, 0)])
# ---- arena crowd: murmur, swelling cheers, whistles; a big "OOOH" on the KO
cheer = 0.6 + 0.4 * smooth(np.abs(noise(N)), 0.8) / 0.5
bed(bp(noise(N), 250, 2500) * cheer, bp(noise(N), 260, 2600) * cheer[::-1], arena, 0.14, 0.6)
for j in T["jabs"]: place(ft(j), bp(noise(int(1.2 * SR)), 300, 2200) * np.sin(np.pi * np.linspace(0, 1, int(1.2 * SR))), .12, 0, .7)
n = int(2.8 * SR); u = np.linspace(0, 1, n)
place(ft(T["ko"]), bp(noise(n), 200, 3000) * np.sin(np.pi * u) ** .5 * (1 - u) * 1.5, .4, 0, .7)
for k in range(10):
    f0 = rng.uniform(B[2], T["tnt"]); n = int(.4 * SR); s = np.arange(n) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(2200 + 900 * np.sin(np.pi * s / s[-1])) / SR) * np.sin(np.pi * s / s[-1]), .02, rng.uniform(-.8, .8), .6)
# ---- punches
for j in T["jabs"]: whoosh(ft(j) - .15, .2, .08, 800, 5000); thud(ft(j), .5, .1)
whoosh(ft(T["ko"]) - .2, .25, .15, 500, 6000); thud(ft(T["ko"]), .9); boom(ft(T["ko"]) + .02, .25, 1.2, 60)
n = int(.6 * SR); s = np.arange(n) / SR   # opponent lands outside the ring
place(ft(T["ko"] + 26), lp(noise(n), 900) * np.exp(-s * 10) + np.sin(2 * np.pi * 55 * s) * np.exp(-s * 9), .5, .4, .5)
whoosh(ft(T["tnt"]) - .3, .35, .2, 400, 7000); boom(ft(T["tnt"]), .8, 3.5, 50)
n = int(1.5 * SR); u = np.linspace(0, 1, n); place(ft(T["tnt"]) + .1, bp(noise(n), 600, 3500) * (1 - u) ** 2, .2, 0, .8)   # screams swallowed
boom(ft(T["hiro"]), 1.0, 5.0)
boom(ft(T["astro"]), 1.1, 5.5, 32)
# ---- oceans boiling: hiss + bubbling
boilE = env([(0, 0), (B[7], 0), (B[7] + 30, 1), (B[8] - 4, 1), (B[8], 0), (END, 0)])
bed(bp(noise(N), 2500, 9000), bp(noise(N), 2500, 9000), boilE, .1, .4)
for k in range(220):
    f0 = rng.uniform(B[7], B[8] - 5); n = int(.04 * SR); s = np.arange(n) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(rng.uniform(150, 400) * (1 + 3 * s / s[-1])) / SR) * np.exp(-s * 60), .05 * boilE[int(ft(f0) * SR)], rng.uniform(-.8, .8), .4)
# ---- space drone + ruined world wind/fire
dr = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * a for f, a in ((41, .5), (55.3, .35), (82.1, .2)))
bed(dr + lp(noise(N), 120) * .4, dr + lp(noise(N), 120) * .4, space, .2, .4)
gust = 0.5 + 0.5 * smooth(np.abs(noise(N)), 0.6) / 0.6
bed(bp(noise(N), 150, 1200) * gust, bp(noise(N), 160, 1300) * gust[::-1], ruin, .3, .5)
for k in range(120):
    f0 = rng.uniform(B[8], T["last"] + 17); n = int(rng.uniform(.005, .02) * SR); s = np.arange(n) / SR
    place(ft(f0), hp(noise(n), 1500) * np.exp(-s * 200), rng.uniform(.03, .1), rng.uniform(-.8, .8), .5)
bell(ft(T["bell"]), .35); bell(ft(T["bell"]) + .45, .35)
d = ft(T["last"]) - ft(T["bell"] + 20); n = int(d * SR); s = np.arange(n) / SR; u = s / d   # charge riser
place(ft(T["bell"] + 20), (np.sin(2 * np.pi * np.cumsum(60 + 140 * u ** 2) / SR) * .6 + bp(noise(n), 400, 4000) * u) * u ** 1.6, .5, 0, .5)
whoosh(ft(T["last"]) - .3, .35, .3, 300, 7000); thud(ft(T["last"]), 1.0)
# ---- the planet breaking (cold open + the real one)
for crackAt, br in ((T["crack"], T["shatter"]), (T["last"] + 19, T["shatter2"])):
    n = int(ft(br - crackAt + 4) * SR); s = np.arange(n) / SR
    place(ft(crackAt), (bp(noise(n), 200, 3000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * s))) + lp(noise(n), 120) * 2) * np.minimum(1, s * 3), .45, 0, .6)
    boom(ft(br), 1.2, 7.0, 28)
# ---- the doubling ticks
last = -1; lastT = -9
K = T["clock"]
def clock(f):
    for i in range(len(K) - 1):
        if f < K[i + 1][0]: return K[i][1] + (K[i + 1][1] - K[i][1]) * (f - K[i][0]) / (K[i + 1][0] - K[i][0])
    return K[-1][1]
for f in range(B[2], END):
    nn = int(clock(f) // 2)
    if nn != last and ft(f) - lastT > .07:
        m = int(.03 * SR); s = np.arange(m) / SR
        place(ft(f), np.sin(2 * np.pi * (1500 + min(nn, 99) * 12) * s) * np.exp(-s * 160), .05, .3, .2); lastT = ft(f)
    last = nn
for c in (B[3], B[4], B[5], B[6], B[7], B[8]): whoosh(ft(c) - .3, .5, .1, 500, 5000)
whoosh(ft(END) - 1.2, 1.2, .3, 400, 6000, rise=True)
# ---- REWIND: cold-open audio reversed and sped up
def rev_segment(x):
    a, b = int(ft(B[1]) * SR), int(ft(B[2]) * SR)
    src = x[: int(ft(96) * SR)][::-1]; idx = np.linspace(0, len(src) - 1, b - a)
    x[a:b] = np.interp(idx, np.arange(len(src)), src) * .8
for arr in (dry_L, dry_R, wet_L, wet_R): rev_segment(arr)
# ---- reverb, narration, ducking
ir_n = int(2.6 * SR); s = np.arange(ir_n) / SR
irL = lp(noise(ir_n), 5000) * np.exp(-s * 2.5); irR = lp(noise(ir_n), 5000) * np.exp(-s * 2.5)
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
vo_room = fftconvolve(vo, irL[: int(.6 * SR)])[:N] * .08
duck = 1 - .55 * np.clip(smooth(np.abs(vo), 6) * 6, 0, 1)
mix = mix * duck[:, None] * .55 + np.stack([vo + vo_room, vo + vo_room], 1) * .9
mix /= np.abs(mix).max() + 1e-9; mix = np.tanh(mix * 1.15) / np.tanh(1.15) * .9
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s; loudest", round(max(rms), 1))
