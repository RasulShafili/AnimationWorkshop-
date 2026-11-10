#!/usr/bin/env python3
"""coffee-nap: calm original music-box tune in D (approved style, see cat-no-sweet v2): an ORIGINAL 8-bit tune that follows the picture,
plus SFX. No voices. 120 BPM, 9 bars of 4/4 = 18 s. Every scene event lands on a musical stinger.
Timings from src/timing.json."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timing.json"))
SR, FPS = 44100, T["fps"]
DUR = T["totalFrames"] / FPS
N = int(SR * DUR)
BEAT = 60 / T["bpm"]                       # 0.5 s
B = T["beats"]
rng = np.random.default_rng(11)
ft = lambda f: f / FPS
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
bp = lambda x, a, b: sosfilt(butter(2, [a, b], "bandpass", fs=SR, output="sos"), x)
mus, sfx = np.zeros((N, 2)), np.zeros((N, 2))

def put(buf, t, y, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(y))
    if i >= N or j <= max(0, i): return
    y = y[: j - i] * g
    buf[i:j, 0] += y * (1 - max(0, pan)); buf[i:j, 1] += y * (1 + min(0, pan))
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def adsr(n, a=.005, d=.08, s=.6, r=.06):
    e = np.ones(n) * s; ai, di, ri = int(a * SR), int(d * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, max(1, ai))[:len(e[:ai])]; e[ai:ai + di] = np.linspace(1, s, max(1, di))[:len(e[ai:ai + di])]
    if ri: e[-ri:] *= np.linspace(1, 0, ri)
    return e
def pulse(m, dur, duty=.25, vib=0.0, bend=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = hz(m) * (1 + vib * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t * 4)) * 2 ** (bend * t / dur / 12)
    ph = np.cumsum(f) / SR % 1
    return lp(np.where(ph < duty, 1.0, -1.0), 7000) * adsr(n)
def tri(m, dur):
    n = int(dur * SR); ph = np.cumsum(np.full(n, hz(m))) / SR % 1
    return (2 * np.abs(2 * ph - 1) - 1) * adsr(n, .003, .05, .85, .04)
def bell(m, dur=.6):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * hz(m) * t) + .35 * np.sin(2 * np.pi * hz(m) * 2.76 * t) * np.exp(-t * 9)) * np.exp(-t * 5)
def kick():
    n = int(.18 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(55 + 110 * np.exp(-t * 40)) / SR) * np.exp(-t * 18)
def hat(open_=False):
    n = int((.09 if open_ else .03) * SR); t = np.arange(n) / SR
    return hp(rng.uniform(-1, 1, n), 7000) * np.exp(-t * (30 if open_ else 120))
def snare():
    n = int(.14 * SR); t = np.arange(n) / SR
    return bp(rng.uniform(-1, 1, n), 1500, 7000) * np.exp(-t * 28) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .4

# ---------------- the tune (D major, new melody for this video) ----------------
CH = [(50, [62, 66, 69]), (47, [59, 62, 66]), (43, [55, 59, 62]), (45, [57, 61, 64]), (50, [62, 66, 69]),
      (42, [54, 57, 61]), (43, [55, 59, 62]), (45, [57, 61, 64]), (50, [62, 66, 69])]
E8 = BEAT / 2
def soft(m, dur):
    n = int((dur + .35) * SR); t = np.arange(n) / SR; ph = np.cumsum(np.full(n, hz(m))) / SR % 1
    y = (2 * np.abs(2 * ph - 1) - 1) * .7 + np.sin(2 * np.pi * hz(m) * 2 * t) * .18 * np.exp(-t * 6)
    return lp(y, 3500) * np.minimum(1, t / .02) * np.exp(-t * 2.2)
LEAD = [(0, 0, 78, 3), (0, 3, 76, 1), (0, 4, 74, 4), (1, 0, 71, 2), (1, 2, 74, 2), (1, 4, 78, 4), (2, 0, 79, 3), (2, 3, 78, 1), (2, 4, 74, 4),
        (3, 0, 76, 6), (4, 0, 81, 2), (4, 2, 78, 2), (4, 4, 74, 4), (5, 0, 73, 2), (5, 2, 76, 2), (5, 4, 81, 4), (6, 0, 79, 4), (6, 4, 83, 4),
        (7, 0, 81, 3), (7, 3, 79, 1), (7, 4, 76, 4), (8, 0, 78, 4), (8, 4, 74, 4)]
for bar, e, m, l in LEAD: put(mus, bar * 4 * BEAT + e * E8, soft(m, l * E8), .13, .1)
for bar, (root, chord) in enumerate(CH):
    t0 = bar * 4 * BEAT
    for k in (0, 2): put(mus, t0 + k * BEAT, tri(root - 12, BEAT * 1.7) * np.exp(-np.arange(int(BEAT * 1.7 * SR)) / SR * 1.5), .14)
    for k, idx in enumerate([0, 1, 2, 1]): put(mus, t0 + k * BEAT, bell(chord[idx] + 12, .9), .028, -.3 if k % 2 else .3)

# ---------------- stingers on the picture ----------------
for i, m in enumerate([74, 71, 67, 62]): put(mus, ft(T["cupDown"]) + .2 + i * .3, soft(m, .3), .08)       # drifting off
for i, m in enumerate([86, 90, 93]): put(mus, ft(T["kick"]) + i * .08, bell(m, .7), .09)                 # caffeine reaches the brain
for i in range(4): put(mus, ft(B[2] + 66 + i * 7 + 14), bell(81 + [0, 4, 7, 12][i], .5), .07)          # caffeine docks
for i, m in enumerate([74, 78, 81, 86]): put(mus, ft(T["wake"]) + i * .07, bell(m, .7), .09)             # wake-up fanfare

# ---------------- SFX ----------------
def burst(d, lo, hi, dec):
    n = int(d * SR); t = np.arange(n) / SR
    return bp(rng.uniform(-1, 1, n), lo, hi) * np.exp(-t * dec)
n = int(DUR * SR); t = np.arange(n) / SR
room = np.interp(t, [0, ft(B[1]) - .1, ft(B[1]), ft(B[3]), ft(B[3]) + .1, DUR], [1, 1, 0, 0, 1, 1])
sunny = np.interp(t, [0, ft(T["wake"]) + .2, ft(T["wake"]) + 1.2, DUR - .9, DUR], [0, 0, 1, 1, 0])
rain = lp(rng.uniform(-1, 1, n), 5000) * .5 + bp(rng.uniform(-1, 1, n), 2000, 8000) * .4
drops = np.zeros(n)
for k in range(260):
    i = int(rng.uniform(0, DUR - .05) * SR); m = int(.01 * SR); drops[i:i + m] += rng.uniform(-1, 1, m) * np.exp(-np.arange(m) / m * 4) * rng.uniform(.2, 1)
put(sfx, 0, (rain + bp(drops, 1500, 7000) * .8) * room * (1 - sunny * .85), .13)                   # rain on the window
put(sfx, 0, lp(rng.uniform(-1, 1, n), 220) * room, .14)                                                # room tone
put(sfx, 0, (lp(rng.uniform(-1, 1, n), 180) + np.sin(2 * np.pi * 55 * t) * .3) * (1 - room), .2)       # inside-the-body hum
for k in range(30):                                                                                     # birds once the sun is out
    t0 = rng.uniform(ft(T["wake"]) + 1, DUR - 1.2)
    m = int(rng.uniform(.05, .1) * SR); s = np.arange(m) / SR
    fr = rng.uniform(2800, 4200) + rng.uniform(-800, 800) * s / s[-1] + 250 * np.sin(2 * np.pi * rng.uniform(25, 45) * s)
    put(sfx, t0, np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * s / s[-1]) ** 2, rng.uniform(.03, .05), rng.uniform(-.8, .8))
def slurp(at, g=.16):
    m = int(.45 * SR); u = np.linspace(0, 1, m)
    put(sfx, at, bp(rng.uniform(-1, 1, m), 700, 3500) * np.sin(np.pi * u) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * u)), g, .2)
slurp(.05); slurp(DUR - .5, .12)
m = int(.25 * SR); s = np.arange(m) / SR
put(sfx, ft(T["cupDown"]), (np.sin(2 * np.pi * 1850 * s) + .6 * np.sin(2 * np.pi * 2730 * s)) * np.exp(-s * 22) + burst(.25, 800, 4000, 60)[:m] * .4, .14, .4)   # mug clink
def snore(at, g):
    m = int(1.1 * SR); u = np.linspace(0, 1, m)
    put(sfx, at, (lp(rng.uniform(-1, 1, m), 600) * (1 + np.sin(2 * np.pi * 38 * u * 1.1)) * .5) * np.sin(np.pi * u) ** 2, g)
for t0 in np.arange(ft(T["asleep"]), ft(T["ring"]) - .5, 1.6):
    if ft(B[1]) - .6 < t0 < ft(B[3]): g = .07
    else: g = .14
    snore(t0, g)
for f0 in range(B[1] + 6, T["kick"], 6):                                                               # stopwatch ticks
    put(sfx, ft(f0), burst(.02, 2500, 8000, 200), .2, .1 if (f0 // 6) % 2 else -.1)
for i in range(9):                                                                                      # caffeine bubbles leave the stomach
    put(sfx, ft(B[1] + 4 + i * 9), np.sin(2 * np.pi * np.cumsum(np.linspace(300, 700, int(.08 * SR))) / SR) * np.hanning(int(.08 * SR)), .07, -.2)
m = int(.8 * SR); u = np.linspace(0, 1, m)
put(sfx, ft(T["kick"]), hp(rng.uniform(-1, 1, m), 4000) * np.exp(-u * 5) * .5 + np.sin(2 * np.pi * np.cumsum(200 + 800 * u) / SR) * np.exp(-u * 4) * .4, .2)  # brain zap
for i in range(4):                                                                                      # adenosine floats away
    m = int(.18 * SR); s = np.arange(m) / SR
    put(sfx, ft(B[2] + 12 + i * 10), np.sin(2 * np.pi * np.cumsum(500 + 900 * s / s[-1]) / SR) * np.exp(-s * 10), .1, -.5 + i * .33)
for i in range(4):                                                                                      # caffeine clicks into the receptor
    put(sfx, ft(B[2] + 66 + i * 7 + 14), burst(.04, 1500, 6000, 90) + 0, .3, -.5 + i * .33)
m = int(1.2 * SR); u = np.linspace(0, 1, m)
put(sfx, ft(B[2] + 92), hp(rng.uniform(-1, 1, m), 5000) * np.sin(np.pi * u) * (0.5 + 0.5 * np.sin(2 * np.pi * 12 * u)), .06)   # glow shimmer
m = int(ft(T["wake"] + 8 - T["ring"]) * SR); s = np.arange(m) / SR                                      # alarm bell
bellr = (np.sign(np.sin(2 * np.pi * 22 * s)) * .5 + .5) * (np.sin(2 * np.pi * 1500 * s) + .5 * np.sin(2 * np.pi * 2350 * s))
put(sfx, ft(T["ring"]), bellr * np.minimum(1, (m - np.arange(m)) / (.15 * SR)), .1, .5)
m = int(.4 * SR); u = np.linspace(0, 1, m)
put(sfx, ft(T["wake"]), np.sin(2 * np.pi * np.cumsum(180 + 500 * u) / SR) * np.sin(np.pi * u) * .6 + bp(rng.uniform(-1, 1, m), 800, 5000) * np.sin(np.pi * u) ** 2 * .5, .25)   # spring up
m = int(1.2 * SR); u = np.linspace(0, 1, m)
put(sfx, ft(T["wake"] + 4), np.sin(2 * np.pi * np.cumsum(300 + 900 * u) / SR) * (np.sin(2 * np.pi * 10 * u) > 0) * np.sin(np.pi * u) * .3, .1, .6)   # battery charging
for f0 in range(T["wake"] + 6, B[5] - 30, 13): put(sfx, ft(f0), bell(96 + (f0 % 3) * 2, .3), .025, rng.uniform(-.7, .7))   # sparkles
for c in B[1:5]:                                                                                        # iris swooshes
    m = int(.45 * SR); u = np.linspace(0, 1, m); w = rng.uniform(-1, 1, m)
    put(sfx, ft(c) - .23, (lp(w, 700) * (1 - u) + bp(w, 1200, 5000) * u) * np.sin(np.pi * u) ** 2, .16)

# ---------------- mix ----------------
ir = rng.uniform(-1, 1, int(.9 * SR)) * np.exp(-np.arange(int(.9 * SR)) / SR * 5); ir /= np.sqrt((ir ** 2).sum())
musw = np.stack([fftconvolve(mus[:, k], ir)[:N] for k in range(2)], 1)
mix = (mus + musw * .3) * 0.55 + sfx
mix = np.stack([hp(mix[:, 0], 30), hp(mix[:, 1], 30)], 1)
mix /= np.abs(mix).max() + 1e-9
mix = np.tanh(mix * 1.1) / np.tanh(1.1) * .9
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "loudest", round(max(rms), 1))
