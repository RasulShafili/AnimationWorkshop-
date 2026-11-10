#!/usr/bin/env python3
"""SFX-only soundtrack (no music, no melodies) for you-glow-in-the-dark.
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
B, HITS = T["beats"], T["hits"]
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

# ---- continuous beds (never silent) ----
dur = lambda a, b: (ft(a), ft(b))
bed(*dur(0, B[1] + 4), room_tone, .25); bed(*dur(0, B[1] + 4), chirp_cricket, .05, -.6); bed(*dur(10, B[1] + 4), chirp_cricket, .035, .6)
bed(*dur(0, B[1] + 4), heartbeat, .35); bed(*dur(0, B[1] + 4), shimmer, .07)
bed(*dur(B[1] - 4, B[2] + 4), lambda d: lp(rng.uniform(-1, 1, int(d * SR)), 120) * 2, .3); bed(*dur(B[1] - 4, B[2] + 4), heartbeat if False else (lambda d: heartbeat(d, 82)), .3)
bed(*dur(B[2] - 4, B[3] + 4), lambda d: hum(d, 120) * .3 + room_tone(d), .2)
bed(*dur(B[3] - 4, B[5] + 4), watery, .4); bed(*dur(B[3] - 4, B[4] + 4), bubbles, .1, -.3); bed(*dur(B[4] - 4, B[5] + 4), lambda d: bubbles(d, 14, 200, 600), .1, .3)
bed(*dur(B[5] - 4, B[6] + 4), lambda d: room_tone(d) + .4 * hum(d, 100), .22); bed(*dur(B[5] - 4, B[6] + 4), lambda d: heartbeat(d, 70), .25)
bed(*dur(B[6] - 4, B[7] + 4), room_tone, .2); bed(*dur(B[6] - 4, B[7] + 4), birds, .04, -.5)
bed(*dur(B[7] - 4, 960), room_tone, .25); bed(*dur(B[7] - 4, 960), chirp_cricket, .05, -.6); bed(*dur(B[7] + 10, 960), chirp_cricket, .035, .6)
bed(*dur(B[7] - 4, 960), shimmer, .06); bed(*dur(B[8], 960), heartbeat, .3)

# ---- events ----
# typewriter blips (lengths from timing.json)
for b in range(1, 9):
    n = sum(len(t) for line in T["texts"][b] for t, _ in line)
    for c in range(0, n, 2): add(ft(B[b] + 3 + c / 1.6), click(1500 + (c % 4) * 120, .02), .1)

# 1: photons twinkle off the body, arms lift with a soft swoosh
for i in range(16): add(ft(3 + i * 6.5) + rng.uniform(0, .05), sparkle_s(.25), .1, rng.uniform(-.6, .6))
add(ft(30), whoosh(.5, True), .12)
# 2: blink, rubbery strain, sweat drip, gauge needle zap at 1000X
add(ft(B[1] + 6), blink_s(), .4); add(ft(B[1] + 20), stretch(1.4), .35)
add(ft(B[1] + 32), zap(1600, 300, .25), .14); add(ft(B[1] + 34), thud(.2), .35)
for k in range(2): add(ft(B[1] + 56 + k * 40), bloop(900, False, .08), .2, .5)
# 3: camera power-up, REC beeps, geiger ticks following the reveal
add(ft(B[2] + 2), zap(200, 1200, .35), .1)
for f in range(B[2], B[3], 30): add(ft(f), click(2400, .04), .12, -.6)
ease = lambda t: (lambda u: 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2)(min(1, max(0, t)))
for f in range(B[2] + 4, B[3] - 2):
    for j in range(int(ease((f - B[2] - 4) / 88) * 6 + .3 + rng.random())): add(ft(f) + rng.random() / FPS, tick(), .3 + .15 * rng.random(), rng.uniform(-.4, .4))
add(ft(B[2] + 72), click(1000, .08), .25)   # shutter
add(ft(B[2] + 74), click(700, .06), .22)
# 4: cell pops in, nucleus blink, mitochondria spark crackles
add(ft(B[3] + 2), bloop(240, True, .18), .5); add(ft(B[3] + 9), bloop(380, True, .12), .35)
for f in range(B[3] + 20, B[4], 9): add(ft(f), sparkle_s(.12), .07, rng.uniform(-.7, .7))
for f in [B[3] + 70]: add(ft(f), blink_s(), .3)
# 5: radicals charge, slam, photon zips upward
for i, h in enumerate(HITS):
    add(ft(h - 16), zap(150, 600, .5), .08, (-1) ** i * .4)
    add(ft(h), thud(), .7); add(ft(h), bp(rng.uniform(-1, 1, int(.12 * SR)), 300, 4000) * np.exp(-tt(.12) * 30), .5)
    add(ft(h + 1), zap(900 + i * 200, 4000, .4), .1); add(ft(h + 2), sparkle_s(.5), .15)
# 6: scanner sweep across the face, wink
add(ft(B[5] + 8), scan(1.4), .2); add(ft(B[5] + 47), sparkle_s(.3), .12); add(ft(B[5] + 50), ding(2600, .35), .1)
# 7: tick-tock that speeds up as the hands race, then the meter maxes out
last = None
for f in range(B[6], B[7] - 4):
    q = int((10 + 6 * ease((f - B[6] - 6) / 86)) * 6)
    if q != last: add(ft(f), tock(q % 2 == 0), .32); last = q
add(ft(B[6] + 92), sparkle_s(.6), .18); add(ft(B[6] + 92), ding(2200, .5), .1)
# 8: each firefly arrives with a tiny glitter
for i in range(14): add(ft(B[7] + 3 * i + 14), sparkle_s(.18), .1, rng.uniform(-.7, .7))
# 9: wave swish + wink twinkle + final glitter
add(ft(B[8] + 22), whoosh(.3, True), .14); add(ft(B[8] + 34), sparkle_s(.3), .14); add(ft(B[8] + 80), sparkle_s(.8), .18)
# scene changes
for c in B[1:8]: add(ft(c) - .22, whoosh(.44, True), .14)

mix = np.stack([hp(L, 30), hp(R, 30)], 1)[: int(SR * DUR)]
nf = int(.25 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = np.tanh(mix * g * 1.05) / 1.05 * .93
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
# report the quietest 0.5 s window so we know nothing goes empty
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s window", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
