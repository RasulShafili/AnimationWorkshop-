#!/usr/bin/env python3
"""SFX-only soundtrack (no music, no melodies) for eyes-see-upside-down.
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
B, ON, OFF = T["beats"], T["gogglesOn"], T["gogglesOff"]
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

dur = lambda a, b: (ft(a), ft(b))
ease = lambda t: (lambda u: 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2)(min(1, max(0, t)))
def deep_hum(d): return lp(rng.uniform(-1, 1, int(d * SR)), 160) * 1.5 + .25 * hum(d, 55)
def spin(d):
    """rotation swoosh: noise whose band slides, no pitch"""
    n = int(d * SR); w = rng.uniform(-1, 1, n); u = np.linspace(0, 1, n)
    return (lp(w, 900) * (1 - u) + bp(w, 1200, 5000) * u) * np.sin(np.pi * u) ** 1.2
def wobble(d):
    s_ = tt(d); return bp(rng.uniform(-1, 1, len(s_)), 300, 1400) * (0.5 + 0.5 * np.sin(2 * np.pi * 3.2 * s_)) ** 2
def flip_page(): s_ = tt(.07); return hp(rng.uniform(-1, 1, len(s_)), 2500) * np.exp(-s_ * 45)
def clack(): s_ = tt(.06); return (bp(rng.uniform(-1, 1, len(s_)), 1500, 6000) + np.sin(2 * np.pi * 900 * s_) * .5) * np.exp(-s_ * 90)
def tweet(d):
    y = np.zeros(int(d * SR))
    for t in np.arange(0, d - .1, .16):
        s_ = tt(.06); i = int(t * SR); y[i:i + len(s_)] += np.sin(2 * np.pi * np.cumsum(3600 + 900 * np.sin(np.pi * s_ / .06)) / SR) * np.sin(np.pi * s_ / .06)
    return y

# ---- beds: never silent ----
ROOM = [(0, B[1]), (B[4], B[8])]
for a_, b_ in ROOM:
    bed(*dur(max(0, a_ - 4), b_ + 4), room_tone, .25); bed(*dur(max(0, a_ - 4), b_ + 4), birds, .035, -.5)
bed(*dur(B[1] - 4, B[2] + 4), deep_hum, .3)
bed(*dur(B[2] - 4, B[3] + 4), lambda d: deep_hum(d) + .4 * shimmer(d), .28)
bed(*dur(B[3] - 4, B[4] + 4), lambda d: deep_hum(d) + .3 * hum(d, 110), .26)
bed(*dur(B[8] - 4, 960), lambda d: deep_hum(d) + .5 * shimmer(d), .28)

# ---- events ----
for b in range(1, 9):
    n = sum(len(t) for line in T["texts"][b] for t, _ in line)
    for c in range(0, n, 2): add(ft(B[b] + 3 + c / 1.6), click(1500 + (c % 4) * 120, .02), .1)
# 1: the room swings upside down
add(0, spin(.9), .4); add(ft(10), thud(.25), .4); add(ft(24), wobble(1.6), .1)
# 2: rays zap across, image pops onto the retina
add(ft(B[1] + 8), zap(300, 2400, 1.0) * .5, .1); add(ft(B[1] + 36), zap(2400, 600, .9) * .5, .1)
add(ft(B[1] + 64), bloop(500, True, .12), .35); add(ft(B[1] + 66), sparkle_s(.4), .14)
# 3: soft shimmer as the upside-down image lights the retina
add(ft(B[2] + 4), sparkle_s(.8), .14); add(ft(B[2] + 40), bloop(300, False, .2), .2)
# 4: brain thinks, frame spins upright, sparkle
for f in range(B[3] + 4, B[3] + 22, 6): add(ft(f), click(900, .03), .12)
add(ft(B[3] + 22), spin(1.15), .35); add(ft(B[3] + 56), ding(2200, .5), .12); add(ft(B[3] + 56), sparkle_s(.6), .16)
# 5: goggles drop onto the face
add(ft(B[4] + 2), whoosh(.6, False), .18); add(ft(ON), clack(), .5); add(ft(ON + 1), bloop(260, True, .12), .3)
# 6: dizzy wobble, stumbling steps, sweat drips
add(ft(B[5]), spin(.6), .25); add(ft(B[5] + 6), wobble(3.2), .16)
for k in range(5): add(ft(B[5] + 12 + k * 18), thud(.18), .35, (-1) ** k * .4)
for k in range(3): add(ft(B[5] + 20 + k * 20), bloop(1000, False, .07), .16, .5)
# 7: seven page flips while the world slowly turns back upright
add(ft(B[6] + 8), spin(2.8) * .7, .3)
last = 1
for f in range(B[6], B[7]):
    d = min(8, 1 + int(ease((f - B[6] - 8) / 84) * 7.99))
    if d != last: add(ft(f), flip_page(), .32); last = d
add(ft(B[6] + 92), sparkle_s(.5), .16)
# 8: goggles yanked off, world flips again, dizzy birdies
add(ft(OFF), bloop(400, True, .1), .35); add(ft(OFF + 2), whoosh(.4, True), .2)
add(ft(OFF + 14), spin(.6), .45); add(ft(OFF + 28), thud(.3), .45); add(ft(OFF + 30), tweet(2.0), .07, .3)
# 9: brain winks, sparkles
add(ft(B[8] + 30), sparkle_s(.3), .14); add(ft(B[8] + 32), ding(2400, .3), .1); add(ft(B[8] + 80), sparkle_s(.8), .16)
for c in (B[1], B[2], B[3], B[4], B[8]): add(ft(c) - .22, whoosh(.44, True), .14)

mix = np.stack([hp(L, 30), hp(R, 30)], 1)[: int(SR * DUR)]
nf = int(.25 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = np.tanh(mix * g * 1.05) / 1.05 * .93
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
# report the quietest 0.5 s window so we know nothing goes empty
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s window", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
