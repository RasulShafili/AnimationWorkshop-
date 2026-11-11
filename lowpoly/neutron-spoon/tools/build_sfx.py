#!/usr/bin/env python3
"""Realistic SFX bed + Kokoro narration for neutron-spoon. No music. Timings: src/timeline.json.
Night city -> spoon hum -> blast; REWIND = the blast audio reversed and sped up; space drone -> star collapse;
seesaw creaks; earth rumble as the dot sinks; second blast; orbit rumble; whoosh back to frame 0."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, FPS = 44100, T["fps"]
END = T["total"]; DUR = END / FPS; N = int(SR * DUR)
B = T["beats"]; BOOM, BOOM2, COL = T["boom"], T["boom2"], T["collapse"]
rng = np.random.default_rng(11)
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
def boom(t0, g, length=5.0):
    n = int(length * SR); s = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-s * 6)) / SR) * np.exp(-s * 1.1)
    crack = (noise(n) * np.exp(-s * 14) + hp(noise(n), 2500) * np.exp(-s * 30)) * .8
    roll = lp(noise(n), 220) * (0.5 + 0.5 * smooth(np.abs(noise(n)), 3) / 0.6) * np.exp(-s * 0.7) * np.minimum(1, s * 6)
    place(t0, sub * 1.0 + crack + roll * 1.4, g, 0, 0.6)
def whoosh(t0, d, g, lo=300, hi=5000, rise=False):
    n = int(d * SR); u = np.linspace(0, 1, n); w = noise(n)
    shape = u ** 2 if rise else np.sin(np.pi * u) ** 2
    place(t0, bp(w, lo, hi) * shape, g, 0, 0.6)

city = env([(0, 1), (BOOM, 1), (BOOM + 2, .3), (B[1], .3), (B[2] - 2, .3), (B[2], 0), (B[5], 0), (B[5] + 4, 1), (BOOM2, 1), (BOOM2 + 2, .3), (BOOM2 + 90, .2), (BOOM2 + 92, 0), (END - 30, 0), (END, 1)])
space = env([(0, 0), (B[2] - 2, 0), (B[2] + 6, 1), (B[5] - 4, 1), (B[5], 0), (BOOM2 + 88, 0), (BOOM2 + 96, 1), (END - 20, 1), (END, 0)])
# ---- night city: wind, distant traffic hum, crickets, a far siren
bed(bp(noise(N), 250, 1300), bp(noise(N), 260, 1400), city, 0.12, 0.4)
bed(lp(noise(N), 160), lp(noise(N), 160), city, 0.3, 0.2)
for k in range(60):
    f0 = rng.uniform(0, END); g = city[min(N - 1, int(ft(f0) * SR))]
    if g < .5: continue
    for j in range(3):
        n = int(.02 * SR); s = np.arange(n) / SR
        place(ft(f0) + j * .05, np.sin(2 * np.pi * 4600 * s) * np.sin(np.pi * s / s[-1]), .025 * g, rng.uniform(-.7, .7), .4)
# ---- space: deep evolving drone + faint shimmer
dr = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * a for f, a in ((41, .5), (55.3, .35), (82.1, .2), (110.4, .1)))
dr *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.13 * t)
bed(dr + lp(noise(N), 120) * .4, dr + lp(noise(N), 120) * .4, space, 0.22, 0.4)
bed(bp(noise(N), 3000, 8000) * .3, bp(noise(N), 3000, 8000) * .3, space, 0.05, 0.8)

# ---- spoon hum rising to the first blast (cold open)
for (a, bb) in ((T["spoonIn"], BOOM), (B[5] + 8, BOOM2)):
    d = ft(bb) - ft(a); n = int(d * SR); s = np.arange(n) / SR; u = s / d
    hum = np.sin(2 * np.pi * np.cumsum(90 + 260 * u ** 2) / SR) + .4 * np.sin(2 * np.pi * np.cumsum(180 + 520 * u ** 2) / SR)
    place(ft(a), (hum + bp(noise(n), 2000, 7000) * u * .5) * u ** 1.3, 0.35, 0, 0.5)
boom(ft(BOOM), 1.0)
boom(ft(BOOM2), 1.1, 7.0)
for k in range(30):  # debris and glass after each blast
    for bb in (BOOM, BOOM2):
        n = int(rng.uniform(.01, .04) * SR); s = np.arange(n) / SR
        place(ft(bb) + rng.uniform(.4, 2.5), hp(noise(n), 2500) * np.exp(-s * 150), rng.uniform(.04, .12), rng.uniform(-.8, .8), .5)

# ---- star collapse: inward suck, crack, then pulsar ticks
whoosh(ft(COL) - 1.2, 1.5, 0.5, 100, 3000, rise=True)
boom(ft(COL + 8), 0.7, 4.0)
for k in range(int((B[3] - COL - 20) / FPS * 5)):
    n = int(.012 * SR); s = np.arange(n) / SR
    place(ft(COL + 20) + k / 5, bp(noise(n), 1500, 6000) * np.exp(-s * 300) + np.sin(2 * np.pi * 900 * s) * np.exp(-s * 200) * .5, .08, (-1) ** k * .3, .5)
# ---- seesaw: people popping onto the pan, wood creaks, a clunk when it levels
for k in range(26):
    f0 = B[3] + 4 + k * 2.8; n = int(.05 * SR); s = np.arange(n) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(500 + 500 * s / s[-1]) / SR) * np.exp(-s * 50), .05, .5, .3)
for k in range(3):
    f0 = B[3] + 30 + k * 16; n = int(.7 * SR); s = np.arange(n) / SR
    cr = np.sin(2 * np.pi * np.cumsum(170 + 60 * np.sin(2 * np.pi * 2 * s)) / SR) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 30 * s))) * np.sin(np.pi * s / s[-1])
    place(ft(f0), bp(cr, 200, 2500), .14, 0, .5)
n = int(.4 * SR); s = np.arange(n) / SR
place(ft(B[3] + 80), lp(noise(n), 600) * np.exp(-s * 18) + np.sin(2 * np.pi * 90 * s) * np.exp(-s * 12), .5, 0, .5)
# ---- earth: rumble that deepens as the dot sinks, then a questioning wobble
d = ft(90 - 20); n = int(d * SR); s = np.arange(n) / SR; u = s / d
place(ft(B[4] + 20), (lp(noise(n), 200) * (1 - u) + lp(noise(n), 70) * u * 1.6) * u * 1.5 + np.sin(2 * np.pi * np.cumsum(140 - 90 * u) / SR) * .3 * u, .5, 0, .6)
# ---- shot changes and the loop
for c in (B[2], B[3], B[4], B[5], B[6]): whoosh(ft(c) - .3, .5, .12, 500, 5000)
whoosh(ft(END) - 1.2, 1.2, .35, 400, 6000, rise=True)

# ---- REWIND: the cold-open audio, reversed and 3.2x faster (pitched up like a tape)
def rev_segment(x):
    a, b = int(ft(B[1]) * SR), int(ft(B[2]) * SR)
    src = x[: int(ft(96) * SR)][::-1]; idx = np.linspace(0, len(src) - 1, b - a)
    x[a:b] = np.interp(idx, np.arange(len(src)), src) * np.sin(np.pi * np.linspace(0, 1, b - a)) ** .3 * .8
for arr in (dry_L, dry_R, wet_L, wet_R): rev_segment(arr)
n = int(ft(30) * SR); s = np.arange(n) / SR
place(ft(B[1]), bp(noise(n), 3000, 9000) * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * s)), .08, 0, .1)   # tape hiss

# ---- reverb
ir_n = int(2.8 * SR); s = np.arange(ir_n) / SR
irL = lp(noise(ir_n), 5000) * np.exp(-s * 2.4); irR = lp(noise(ir_n), 5000) * np.exp(-s * 2.4)
irL[: int(.012 * SR)] = 0; irR[: int(.017 * SR)] = 0
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
L = dry_L + fftconvolve(wet_L, irL)[:N] * 0.9; R = dry_R + fftconvolve(wet_R, irR)[:N] * 0.9
mix = np.stack([hp(L, 25), hp(R, 25)], 1); mix /= np.abs(mix).max() + 1e-9
# ---- narration with ducking
vo = np.zeros(N)
for i, f in enumerate(T["vo"]):
    sr, y = wavfile.read(f"{ROOT}/vo/l{i}.wav"); y = y.astype(np.float64) / 32768
    if y.ndim > 1: y = y.mean(1)
    a = int(ft(f) * SR); b = min(N, a + len(y)); vo[a:b] += y[: b - a]
vo = hp(vo, 80) / (np.abs(vo).max() + 1e-9)
vo_room = fftconvolve(vo, irL[: int(.6 * SR)])[:N] * 0.08
duck = 1 - 0.55 * np.clip(smooth(np.abs(vo), 6) * 6, 0, 1)
mix = mix * duck[:, None] * 0.55 + np.stack([vo + vo_room, vo + vo_room], 1) * 0.9
mix /= np.abs(mix).max() + 1e-9
mix = np.tanh(mix * 1.15) / np.tanh(1.15) * 0.9
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s; loudest", round(max(rms), 1))
