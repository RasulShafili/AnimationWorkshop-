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

H = T["hits"]; OUT, BEAM = T["outside"], T["beamOut"]
arena = env([(0, 1), (H[4] + 4, 1), (H[4] + 8, 0), (END, 0)])
city = env([(0, 0), (OUT - 1, 0), (OUT + 2, 1), (B[4] - 2, 1), (B[4], 0), (BEAM - 1, 0), (BEAM + 2, 1), (B[5] - 2, 1), (B[5], 0), (END, 0)])
space = env([(0, 0), (H[5] + 2, 0), (H[5] + 4, 1), (END, 1)])
ruin = env([(0, 0), (B[5] - 1, 0), (B[5] + 2, 1), (END, 1)]) * (1 - space)
# ---- arena crowd, cheering harder after each punch, "OOOH" on the big ones
cheer = 0.6 + 0.4 * smooth(np.abs(noise(N)), 0.8) / 0.5
bed(bp(noise(N), 250, 2500) * cheer, bp(noise(N), 260, 2600) * cheer[::-1], arena, 0.14, 0.6)
for i in range(4):
    n = int((1.2 + i * .6) * SR); u = np.linspace(0, 1, n)
    place(ft(H[i]) + .05, bp(noise(n), 200, 3000) * np.sin(np.pi * u) ** .5 * (1 - u) * 1.4, .12 + i * .1, 0, .7)
for k in range(10):
    f0 = rng.uniform(0, H[4]); n = int(.4 * SR); s = np.arange(n) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(2200 + 900 * np.sin(np.pi * s / s[-1])) / SR) * np.sin(np.pi * s / s[-1]), .02, rng.uniform(-.8, .8), .6)
n = int(1.5 * SR); u = np.linspace(0, 1, n); place(ft(H[4]) + .3, bp(noise(n), 600, 3500) * np.sin(np.pi * u) * (1 - u), .25, 0, .8)   # crowd screams
# ---- night city outside (wind, traffic hum)
bed(bp(noise(N), 250, 1300), bp(noise(N), 260, 1400), city, .12, .4); bed(lp(noise(N), 160), lp(noise(N), 160), city, .3, .2)
# ---- the ten punches, each heavier
for i, hf in enumerate(H):
    whoosh(ft(hf) - .25, .3, .08 + i * .03, 400, 6000)
    thud(ft(hf), .45 + i * .06, .1)
    if i == 1: place(ft(hf) + .55, lp(noise(int(.5 * SR)), 700) * np.exp(-np.arange(int(.5 * SR)) / SR * 10), .4, 0, .4)   # body hits the canvas
    if i == 2: place(ft(hf) + 1.2, lp(noise(int(.6 * SR)), 900) * np.exp(-np.arange(int(.6 * SR)) / SR * 9), .45, .4, .5)  # lands outside the ring
    if i == 3:   # through the roof: crash and metal, then a long fading whistle outside
        boom(ft(hf) + .02, .35, 1.5, 60); n = int(.8 * SR); s = np.arange(n) / SR
        place(ft(hf) + .9, bp(noise(n), 1500, 7000) * np.exp(-s * 5) + np.sin(2 * np.pi * np.cumsum(900 + 400 * np.sin(2 * np.pi * 7 * s)) / SR) * np.exp(-s * 4) * .2, .3, .3, .6)
        n = int(1.6 * SR); s = np.arange(n) / SR
        place(ft(OUT), np.sin(2 * np.pi * np.cumsum(1400 - 700 * s / s[-1]) / SR) * (1 - s / s[-1]) * .3, .2, .5, .6)
    if i == 4:   # the beam: a charged zap, then the arena explodes
        n = int(.9 * SR); s = np.arange(n) / SR
        place(ft(hf), (np.sin(2 * np.pi * np.cumsum(180 + 60 * np.sin(2 * np.pi * 30 * s)) / SR) * .6 + bp(noise(n), 2000, 9000) * .5) * np.minimum(1, s * 50) * np.exp(-s * 2), .5, 0, .5)
        boom(ft(BEAM + 6), 1.0, 4.5)
    if i >= 5: boom(ft(hf) + .1, .7 + (i - 5) * .12, 4.0 + i * .4, 40 - (i - 5) * 3)
    if i >= 5:   # glove charging up before each space punch
        d = .7; n = int(d * SR); s = np.arange(n) / SR; u = s / d
        place(ft(hf) - d, np.sin(2 * np.pi * np.cumsum(80 + 220 * u ** 2) / SR) * u ** 2, .25, 0, .4)
# beam into space (punch 6)
n = int(2.2 * SR); s = np.arange(n) / SR
place(ft(H[5]) + .1, bp(noise(n), 300, 4000) * np.exp(-s * 1.2) * .8 + np.sin(2 * np.pi * 70 * s) * np.exp(-s * 1.5), .4, 0, .6)
# oceans boiling
boilE = env([(0, 0), (H[7], 0), (H[7] + 30, 1), (H[9], 1), (H[9] + 6, 0), (END, 0)])
bed(bp(noise(N), 2500, 9000), bp(noise(N), 2500, 9000), boilE, .08, .4)
for k in range(220):
    f0 = rng.uniform(H[7], H[9]); n = int(.04 * SR); s = np.arange(n) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(rng.uniform(150, 400) * (1 + 3 * s / s[-1])) / SR) * np.exp(-s * 60), .05 * boilE[int(ft(f0) * SR)], rng.uniform(-.8, .8), .4)
# cracking crust (punch 9) and the final break (punch 10)
n = int(2.5 * SR); s = np.arange(n) / SR
place(ft(H[8]), (bp(noise(n), 200, 3000) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * s))) + lp(noise(n), 120) * 2) * np.exp(-s * .8), .4, 0, .6)
boom(ft(H[9] + 6), 1.3, 8.0, 26)
# ---- space drone + ruined ring wind and embers
dr = sum(np.sin(2 * np.pi * fq * t + rng.uniform(0, 6)) * a for fq, a in ((41, .5), (55.3, .35), (82.1, .2)))
bed(dr + lp(noise(N), 120) * .4, dr + lp(noise(N), 120) * .4, space, .2, .4)
gust = 0.5 + 0.5 * smooth(np.abs(noise(N)), 0.6) / 0.6
bed(bp(noise(N), 150, 1200) * gust, bp(noise(N), 160, 1300) * gust[::-1], ruin, .3, .5)
# ---- the doubling ticks
K = T["clock"]
def clock(f):
    for i in range(len(K) - 1):
        if f < K[i + 1][0]: return K[i][1] + (K[i + 1][1] - K[i][1]) * (f - K[i][0]) / (K[i + 1][0] - K[i][0])
    return K[-1][1]
last, lastT = -1, -9
for f in range(0, END):
    nn = int(clock(f) // 2)
    if nn != last and ft(f) - lastT > .07:
        m = int(.03 * SR); s = np.arange(m) / SR
        place(ft(f), np.sin(2 * np.pi * (1500 + min(nn, 99) * 12) * s) * np.exp(-s * 160), .05, .3, .2); lastT = ft(f)
    last = nn
for c in B[1:10]: whoosh(ft(c) - .25, .4, .08, 500, 5000)
whoosh(ft(END) - 1.2, 1.2, .3, 400, 6000, rise=True)
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
