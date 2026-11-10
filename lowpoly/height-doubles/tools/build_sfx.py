#!/usr/bin/env python3
"""SFX-only soundtrack (no music) for height-doubles: a tick + growth surge every second, a sound for each milestone,
and a continuous bed (yard -> wind -> space) so it is never silent. Timings come from src/timeline.json."""
import json, os, sys
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, DUR = 44100, float(T["seconds"])
N = int(SR * DUR) + SR
rng = np.random.default_rng(5)
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
def bed(t0, t1, y_fn, g, pan=0.0): add(t0, fade(y_fn(t1 - t0), .05 if t0 == 0 else .4, .4), g, pan)

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

# ---- beds ----
def wind(d, lo=200, hi=1200):
    s_ = tt(d); return bp(rng.uniform(-1, 1, len(s_)), lo, hi) * (0.55 + 0.45 * np.sin(2 * np.pi * .23 * s_) * np.sin(2 * np.pi * .07 * s_ + 1))
def space_drone(d):
    s_ = tt(d); return lp(rng.uniform(-1, 1, len(s_)), 90) * 2.2 + .25 * np.sin(2 * np.pi * 41 * s_) * (0.6 + 0.4 * np.sin(2 * np.pi * .1 * s_))
bed(0, 9.6, room_tone, .25); bed(0, 9.6, birds, .05, -.4); bed(0, 6, lambda d: chirp_cricket(d) * 0, 0)
bed(8.5, 16.5, wind, .35); bed(11, 16.5, lambda d: wind(d, 120, 600), .3)
bed(15.5, DUR, space_drone, .35); bed(15.5, DUR, shimmer, .05)

# ---- every second: a tick, then a growth surge that gets heavier as you get bigger ----
for n in range(1, int(DUR)):
    k = n / DUR
    add(n, click(1400 - 600 * k, .03), .5)
    s_ = tt(.42); w = rng.uniform(-1, 1, len(s_)); u = s_ / s_[-1]
    surge = (lp(w, 300 + 2500 * (1 - k)) * np.sin(np.pi * u) ** .7)
    add(n + .01, surge, .45 + .35 * k)
    add(n + .02, thud(.3 + .3 * k) , .25 + .5 * k)
    # creaky stretch: wobbling band noise (no pitch)
    add(n + .03, bp(rng.uniform(-1, 1, int(.35 * SR)), 180, 700) * np.sin(np.pi * tt(.35) / .35) * (0.6 + 0.4 * np.sin(2 * np.pi * 14 * tt(.35))), .18)

# ---- milestones ----
add(0.0, whoosh(.75, False), .55); add(0.62, thud(.45), .45); add(0.66, sparkle_s(.3), .12)   # 0 camera flies back from the face, lands
add(1.1, click(600, .05), .3); add(1.15, bloop(900, False, .1), .2)  # 1 hoop
add(2.1, bp(rng.uniform(-1, 1, int(.4 * SR)), 300, 3000) * np.exp(-tt(.4) * 9), .35)   # 2 house creaks/crunch
add(3.1, bp(rng.uniform(-1, 1, int(.6 * SR)), 1500, 6000) * np.exp(-tt(.6) * 6), .2)   # 3 leaves rustle
for k in range(4): add(5.1 + k * .2, whoosh(.3, False), .12)                           # 5 shadow sweeps
add(7.05, thud(.8), .9); add(7.1, lp(rng.uniform(-1, 1, int(1.0 * SR)), 120) * np.exp(-tt(1.0) * 3), .9)  # 7 weight
for k in range(6): add(8.05 + k * .07, bp(rng.uniform(-1, 1, int(.12 * SR)), 800, 5000) * np.exp(-tt(.12) * 30), .5, (k % 2 - .5))       # 8 cracks
add(8.05, lp(rng.uniform(-1, 1, int(1.6 * SR)), 90) * np.exp(-tt(1.6) * 1.5) * 2, .8)  # 8 rumble
add(9.1, sparkle_s(.4), .14)                                          # 9 past the tower
add(10.05, whoosh(.9, True), .35)                                     # 10 clouds
add(12.1, bp(rng.uniform(-1, 1, int(1.0 * SR)), 250, 900) * np.sin(np.pi * tt(1.0)) * .8, .35)  # 12 thin air gasp
add(13.1, lp(rng.uniform(-1, 1, int(1.2 * SR)), 200) * np.exp(-tt(1.2) * 2), .6)        # 13 mountain rumble
s_ = tt(1.8); jet = bp(rng.uniform(-1, 1, len(s_)), 300, 4000) * np.exp(-((s_ - .9) / .45) ** 2); add(13.6, jet, .7, -.3)  # 14 jet flyby
add(15.1, whoosh(1.0, True) * .8, .3)                                 # 15 sky turns black
add(16.05, lp(rng.uniform(-1, 1, int(1.4 * SR)), 70) * np.exp(-tt(1.4) * 1.2) * 2.5, .7)  # 16 into space boom
for k in range(6): add(17.1 + k * .16, zap(3000, 600, .25) * .6, .1, rng.uniform(-.6, .6))  # 17 meteors
for k in range(3): add(18.1 + k * .22, ding(1500, .12) + .5 * ding(1180, .12), .12, -.4)   # 18 ISS radio
for k in range(4): add(19.1 + k * .25, ding(2600, .08), .08, rng.uniform(-.6, .6))          # 19 satellites
add(20.05, lp(rng.uniform(-1, 1, int(1.5 * SR)), 60) * np.sin(np.pi * tt(1.5) / 1.5) * 2.5, .5)  # 20 earth curves
add(23.05, thud(1.2), .9); add(23.1, lp(rng.uniform(-1, 1, int(2.0 * SR)), 55) * np.exp(-tt(2.0) * 1.2) * 3, .7)  # 23 bigger than earth
for k in range(2): add(24.1 + k * .3, ding(2200, .1), .08, .4)
for k in range(3): add(25.1 + k * .25, ding(1900, .1), .08, -.4)
add(26.1, sparkle_s(.5), .12)
add(28.05, sparkle_s(1.0), .22); add(28.1, ding(880, .9) + .4 * ding(1320, .9), .1)     # 28 the moon
add(30.1, whoosh(.8, True), .3); add(31.1, sparkle_s(.8), .2)

mix = np.stack([hp(L, 28), hp(R, 28)], 1)[: int(SR * DUR)]
nf = int(.3 * SR); mix[-nf:] *= np.linspace(1, 0, nf)[:, None]
g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
mix = np.tanh(mix * g * 1.05) / 1.05 * .93
wavfile.write(f"{ROOT}/public/mix.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s window", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
