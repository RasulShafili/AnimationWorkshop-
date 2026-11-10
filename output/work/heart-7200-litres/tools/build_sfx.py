#!/usr/bin/env python3
"""SFX-only soundtrack (no music, no melodies) for heart-7200-litres.
A continuous ambience bed per scene so the video never goes quiet, plus a sound for every on-screen event.
All timings come from src/timing.json, the same numbers the picture uses."""
import json, os, sys
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timing.json"))
SR, FPS, DUR = 44100, T["fps"], 32.0
N = int(SR * DUR) + SR
B, BP = T["beats"], T["beatPeriod"]
rng = np.random.default_rng(11)
ft = lambda f: f / FPS
bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
tt = lambda d: np.arange(int(d * SR)) / SR

L, R = np.zeros(N), np.zeros(N)
def add(t, y, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(y))
    if i >= N or j <= max(i, 0): return
    y = y[:j - i] * g
    L[i:j] += y * (1 - max(0, pan)); R[i:j] += y * (1 + min(0, pan))

def fade(y, a=.01, r=.05):
    n = len(y); e = np.ones(n); ai, ri = max(1, int(a * SR)), max(1, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return y * e
def bed(t0, t1, y_fn, g, pan=0.0):           # a looped ambience between two frames, soft edges
    y = fade(y_fn(t1 - t0), .25, .25); add(t0, y, g, pan)

# ---- sound atoms ----
def chirp_cricket(d):
    """crickets: bursts of 4.6 kHz pulses, random gaps, two insects panned apart"""
    y = np.zeros(int(d * SR)); t = 0.0
    while t < d - .3:
        n = rng.integers(3, 6)
        for k in range(n):
            s = tt(.022); y[int((t + k * .045) * SR):int((t + k * .045) * SR) + len(s)] += np.sin(2 * np.pi * 4600 * s) * np.sin(np.pi * s / .022)
        t += n * .045 + rng.uniform(.25, .6)
    return y
def room_tone(d): return lp(rng.uniform(-1, 1, int(d * SR)), 400)
def heartbeat(d, bpm=64):
    y = np.zeros(int(d * SR)); p = 60 / bpm
    for b in np.arange(0, d - .3, p):
        for off, g in ((0, 1), (.17, .7)):
            s = tt(.13); i = int((b + off) * SR)
            y[i:i + len(s)] += np.sin(2 * np.pi * np.cumsum(45 + 30 * np.exp(-s * 40)) / SR) * np.exp(-s * 22) * g
    return y
def shimmer(d):
    """airy sparkle bed: band-passed noise with slow movement, no pitch"""
    n = rng.uniform(-1, 1, int(d * SR)); t = tt(d)
    return bp(n, 5000, 11000) * (0.5 + 0.5 * np.sin(2 * np.pi * .7 * t)) ** 2
def bubbles(d, rate=9, lo=250, hi=700):
    y = np.zeros(int(d * SR))
    for t in np.sort(rng.uniform(0, d - .15, int(d * rate))):
        f0 = rng.uniform(lo, hi); s = tt(rng.uniform(.04, .09)); i = int(t * SR)
        y[i:i + len(s)] += np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.2 * s / s[-1])) / SR) * np.sin(np.pi * s / s[-1]) * rng.uniform(.4, 1)
    return y
def watery(d): return lp(rng.uniform(-1, 1, int(d * SR)), 260) * (0.7 + 0.3 * np.sin(2 * np.pi * .4 * tt(d)))
def hum(d, f=60): t = tt(d); return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * 2 * f * t)) * (0.8 + 0.2 * np.sin(2 * np.pi * 3 * t))
def birds(d):
    y = np.zeros(int(d * SR))
    for t in np.arange(.2, d - .4, .7) + rng.uniform(0, .3, len(np.arange(.2, d - .4, .7))):
        for k in range(rng.integers(2, 4)):
            s = tt(.07); i = int((t + k * .09) * SR); f0 = rng.uniform(3000, 4200)
            y[i:i + len(s)] += np.sin(2 * np.pi * np.cumsum(f0 + 1500 * np.sin(np.pi * s / .07)) / SR) * np.sin(np.pi * s / .07)
    return y

def click(f0=1800, d=.012): s = tt(d); return np.sin(2 * np.pi * f0 * s) * np.exp(-s * 400)
def tick(): return bp(rng.uniform(-1, 1, int(.006 * SR)), 2500, 9000) * np.hanning(int(.006 * SR))
def sparkle_s(d=.35):
    """non-melodic glitter: high noise burst with a fast shimmer"""
    s = tt(d); return hp(rng.uniform(-1, 1, len(s)), 6000) * np.exp(-s * 9) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * s)))
def ding(f0, d=.6):
    s = tt(d); return (np.sin(2 * np.pi * f0 * s) + .4 * np.sin(2 * np.pi * f0 * 2.76 * s) * np.exp(-s * 8)) * np.exp(-s * 6)
def bloop(f0, up=True, d=.11):
    s = tt(d); return np.sin(2 * np.pi * np.cumsum(f0 * (1 + (1.4 if up else -.5) * s / d)) / SR) * np.sin(np.pi * s / d) ** 1.5
def whoosh(d=.44, up=True):
    n = int(d * SR); w = rng.uniform(-1, 1, n); m = np.linspace(0, 1, n) if up else np.linspace(1, 0, n)
    return (lp(w, 700) * (1 - m) + hp(w, 2600) * m * .6) * np.sin(np.linspace(0, np.pi, n)) ** 2
def thud(d=.34): s = tt(d); return np.sin(2 * np.pi * np.cumsum(38 + 120 * np.exp(-s * 30)) / SR) * np.exp(-s * 11)
def zap(f0, f1, d=.3):
    s = tt(d); fr = f0 * (f1 / f0) ** (s / d)
    return np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * np.exp(-s * 7) * .5
def stretch(d=1.3):
    """rubbery strain: wobbling filtered noise, pitchless"""
    s = tt(d); n = rng.uniform(-1, 1, len(s)); f = 300 + 200 * np.sin(2 * np.pi * 7 * s)
    return bp(n, 250, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * s)) * np.sin(np.pi * s / d)
def scan(d=1.4): s = tt(d); return (bp(rng.uniform(-1, 1, len(s)), 1500, 4000) * .7 + np.sin(2 * np.pi * 120 * s) * .3) * np.sin(np.pi * s / d) ** .6
def blink_s(): s = tt(.06); return lp(rng.uniform(-1, 1, len(s)), 1500) * np.exp(-s * 60)
def tock(hi=True): s = tt(.03); return (bp(rng.uniform(-1, 1, len(s)), 1800 if hi else 900, 5000 if hi else 2500) * .8 + np.sin(2 * np.pi * (1400 if hi else 900) * s) * .4) * np.exp(-s * 140)

# ---- the heartbeat is the spine of the soundtrack: locked to the picture's beat period ----
def lubdub(g=1.0):
    y = np.zeros(int(.5 * SR))
    for off, gg, f0 in ((0, 1, 52), (6 / FPS, .65, 62)):
        s_ = tt(.16); i = int(off * SR)
        y[i:i + len(s_)] += (np.sin(2 * np.pi * np.cumsum(f0 + 40 * np.exp(-s_ * 40)) / SR) * np.exp(-s_ * 20)
                             + lp(rng.uniform(-1, 1, len(s_)), 300) * np.exp(-s_ * 50) * .4) * gg
    return y * g
HB_GAIN = {0: .9, 1: .55, 2: .8, 3: .45, 4: .5, 5: .7, 6: .3, 7: .7, 8: 1.0}
for k in range(0, 960 // BP + 1):
    f = k * BP
    if f >= 958: break
    sc = next(i for i in range(9) if f < B[i + 1])
    add(ft(f), lubdub(HB_GAIN[sc]), .55)

# continuous beds so nothing is ever silent
dur = lambda a, b: (ft(a), ft(b))
bed(*dur(0, B[4] + 4), lambda d: lp(rng.uniform(-1, 1, int(d * SR)), 180) * 1.6, .22)          # inner body whoosh
bed(*dur(0, B[4] + 4), lambda d: bp(rng.uniform(-1, 1, int(d * SR)), 300, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.2 * tt(d))), .05)
bed(*dur(B[4] - 4, B[5] + 4), room_tone, .25); bed(*dur(B[4] - 4, B[5] + 4), chirp_cricket, .05, -.6); bed(*dur(B[4] + 10, B[5] + 4), chirp_cricket, .035, .6)
bed(*dur(B[5] - 4, B[6] + 4), lambda d: lp(rng.uniform(-1, 1, int(d * SR)), 180) * 1.6, .22)
bed(*dur(B[6] - 4, B[7] + 4), lambda d: bp(rng.uniform(-1, 1, int(d * SR)), 400, 2500) * (0.7 + 0.3 * np.sin(2 * np.pi * .5 * tt(d))), .07)   # pool water
bed(*dur(B[7] - 4, 960), room_tone, .25); bed(*dur(B[7] - 4, 960), birds, .03, -.5)

# ---- events ----
for b in range(1, 9):
    n = sum(len(t) for line in T["texts"][b] for t, _ in line)
    for c in range(0, n, 2): add(ft(B[b] + 3 + c / 1.6), click(1500 + (c % 4) * 120, .02), .1)
ease = lambda t: (lambda u: 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2)(min(1, max(0, t)))
def counter_ticks(f0, f1, fn, g=.1):
    last = None
    for f in range(f0, f1):
        v = fn(f)
        if v != last and last is not None: add(ft(f), click(2200, .01), g)
        last = v
def gurgle(d):
    s_ = tt(d); return bp(rng.uniform(-1, 1, len(s_)), 200, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * (6 + 3 * np.sin(2 * np.pi * .7 * s_)) * s_)) ** 2

# 1: litres counter (every ~100 L a tick)
counter_ticks(2, B[1], lambda f: int(7200 * (0.18 + 0.82 * ease(f / 100)) // 120), .09)
# 2: blood pours along the pipe into the jug, stopwatch ticks, "full" ding
bed(ft(B[1] + 4), ft(B[2]), gurgle, .3, .3)
for f in range(B[1], B[2], 2): add(ft(f), tick(), .12, -.5)
add(ft(B[1] + 98), ding(1800, .5), .14)
# 3: ECG beeps on every beat + beat counter ticks
for k in range(B[2] // BP + 1, B[3] // BP + 1): add(ft(k * BP), ding(1000, .09), .12)
counter_ticks(B[2], B[3], lambda f: int(100000 * ease((f - B[2]) / 95) // 2500), .09)
# 4: each barrel lands with a hollow thunk
for i in range(36):
    t = B[3] + (i / 36) * 80 * 0.6 + 6
    s_ = tt(.12); add(ft(t), (np.sin(2 * np.pi * (140 + (i % 6) * 12) * s_) * np.exp(-s_ * 30) + bp(rng.uniform(-1, 1, len(s_)), 500, 2000) * np.exp(-s_ * 60) * .5), .3, ((i % 6) - 2.5) / 4)
# 5: bedside monitor beeps + soft snores
for k in range(B[4] // BP + 1, B[5] // BP + 1): add(ft(k * BP), ding(1000, .08), .08, .5)
for k in range(3):
    s_ = tt(.8); add(ft(B[4] + 18 + k * 32), bp(rng.uniform(-1, 1, len(s_)), 90, 500) * np.sin(np.pi * s_ / .8) ** 2, .3, -.3)
# 6: calendar pages flutter + racing counter
for f in range(B[5], B[6], 5): s_ = tt(.05); add(ft(f), hp(rng.uniform(-1, 1, len(s_)), 2500) * np.exp(-s_ * 50), .15, rng.uniform(-.5, .5))
counter_ticks(B[5], B[6], lambda f: int(80 * ease((f - B[5]) / 96)), .1)
# 7: every pool fills with a little splash
for i in range(80):
    t = B[6] + ease(i / 80) * 0 + i * 85 / 80 * 1.0
    s_ = tt(.07); add(ft(B[6] + (i / 80) * 85), bp(rng.uniform(-1, 1, len(s_)), 1500, 6000) * np.exp(-s_ * 45), .12, ((i % 8) - 3.5) / 5)
# 8: fist and heart pop in, wink
add(ft(B[7] + 2), bloop(240, True, .14), .45); add(ft(B[7] + 16), bloop(330, True, .14), .45)
add(ft(B[7] + 36), sparkle_s(.3), .12); add(ft(B[7] + 52), ding(2400, .3), .1)
# 9: hand meets chest (soft pat), heartbeat swells
s_ = tt(.08); add(ft(B[8] + 18), lp(rng.uniform(-1, 1, len(s_)), 800) * np.exp(-s_ * 40), .5)
add(ft(B[8] + 90), sparkle_s(.6), .14)
for c in B[1:9]: add(ft(c) - .22, whoosh(.44, True), .14)

mix = np.stack([hp(L, 30), hp(R, 30)], 1)[: int(SR * DUR)]
nf = int(.25 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = np.tanh(mix * g * 1.05) / 1.05 * .93
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
# report the quietest 0.5 s window so we know nothing goes empty
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s window", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
