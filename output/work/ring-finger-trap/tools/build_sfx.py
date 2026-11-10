#!/usr/bin/env python3
"""SFX-only soundtrack for ring-finger-trap (desk room tone + wall clock; x-ray scanner hum). Was adapted from nose-hum-test (no music, no melody). Timings come from src/timing.json.
Beds: stage room tone + soft crowd murmur; inside-the-head rumble + air hiss. The hum itself is one steady
buzzy pitch (a sound effect of a person humming), muffled and cut off when the nose is pinched."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timing.json"))
SR, FPS = 44100, T["fps"]
DUR = T["totalFrames"] / FPS
N = int(SR * DUR) + SR
B, SLAM, FOLD, LIFTS, UNFOLD, FREE = T["beats"], T["slam"], T["fold"], T["lifts"], T["unfold"], T["freeLift"]
rng = np.random.default_rng(23)
ft = lambda f: f / FPS
bp = lambda x, lo, hi: sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
tt = lambda d: np.arange(int(d * SR)) / SR
L, R = np.zeros(N), np.zeros(N)

def add(t, y, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(y))
    if i >= N or j <= max(i, 0): return
    y = y[:j - i] * g; L[i:j] += y * (1 - max(0, pan)); R[i:j] += y * (1 + min(0, pan))
def fade(y, a=.01, r=.05):
    n = len(y); e = np.ones(n); ai, ri = max(1, int(a * SR)), max(1, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return y * e
def bed(f0, f1, fn, g, pan=0.0): add(ft(f0), fade(fn(ft(f1) - ft(f0)), .15, .15), g, pan)
noise = lambda d: rng.uniform(-1, 1, int(d * SR))

# ---- atoms ----
def room(d): return lp(noise(d), 380) * 1.2
def crowd(d):
    """distant audience murmur: many band-passed noise voices with slow random swells, no pitch"""
    y = np.zeros(int(d * SR)); t = tt(d)
    for k in range(6):
        env = 0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(.2, .6) * t + rng.uniform(0, 6))
        y += bp(noise(d), rng.uniform(300, 500), rng.uniform(900, 1500)) * env
    return y / 3
def spot_hum(d): t = tt(d); return (np.sin(2 * np.pi * 100 * t) + .3 * np.sin(2 * np.pi * 200 * t)) * .5 + bp(noise(d), 3000, 6000) * .15
def body(d): t = tt(d); return lp(noise(d), 140) * 1.6 * (0.8 + 0.2 * np.sin(2 * np.pi * 1.1 * t))
def hiss(d, lo=1500, hi=5000): return bp(noise(d), lo, hi)
def hum_voice(d, f0=132.0):
    """one steady nasal hum: buzzy source + nasal formants, a touch of vibrato; it is a single held pitch, not a tune"""
    t = tt(d); ph = 2 * np.pi * np.cumsum(f0 * (1 + .006 * np.sin(2 * np.pi * 5.2 * t))) / SR
    src = sum(np.sin(k * ph) / k ** 1.1 for k in range(1, 18))
    return (bp(src, 200, 400) * 1.2 + bp(src, 900, 1300) * .5 + bp(src, 2200, 2800) * .15) * .6
def click(f0=1800, d=.012): s = tt(d); return np.sin(2 * np.pi * f0 * s) * np.exp(-s * 400)
def tick(): s = tt(.02); return (bp(noise(.02), 2500, 8000) + np.sin(2 * np.pi * 2600 * s) * .4) * np.exp(-s * 260)
def thud(d=.34): s = tt(d); return np.sin(2 * np.pi * np.cumsum(40 + 130 * np.exp(-s * 30)) / SR) * np.exp(-s * 11)
def whoosh(d=.4, up=True):
    n = int(d * SR); w = noise(d)[:n]; m = np.linspace(0, 1, n) if up else np.linspace(1, 0, n)
    return (lp(w, 700) * (1 - m) + hp(w, 2600) * m * .6) * np.sin(np.linspace(0, np.pi, n)) ** 2
def bloop(f0, up=True, d=.12): s = tt(d); return np.sin(2 * np.pi * np.cumsum(f0 * (1 + (1.4 if up else -.5) * s / d)) / SR) * np.sin(np.pi * s / d) ** 1.5
def squish():
    s = tt(.12); y = bp(noise(.12), 400, 1600) * np.exp(-s * 25); b = bloop(220, False, .1); y[:len(b)] += b * .5; return y
def buzzer(d=.45): s = tt(d); return np.sign(np.sin(2 * np.pi * 110 * s)) * .35 * np.exp(-s * 3) + bp(noise(d), 200, 900) * .3 * np.exp(-s * 5)
def pop(): s = tt(.06); return (np.sin(2 * np.pi * np.cumsum(900 * np.exp(-s * 30) + 200) / SR) + bp(noise(.06), 1000, 6000) * .6) * np.exp(-s * 70)
def shutter():
    """the stage-shutter transition: a fast rattle of slats plus a soft swish"""
    y = np.zeros(int(.4 * SR))
    for k in range(8): s = tt(.015); i = int(k * .03 * SR); y[i:i + len(s)] += bp(noise(.015), 1500, 6000)[:len(s)] * np.exp(-s * 300) * (1 - k / 10)
    return y + whoosh(.4, True) * .5
def sparkle(d=.4): s = tt(d); return hp(noise(d), 6000) * np.exp(-s * 9) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * s)))
def creak(d): s = tt(d); return bp(noise(d), 300, 900) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * s))) * .6


def wood_tap(): s = tt(.09); return (bp(noise(.09), 500, 2500) * .8 + np.sin(2 * np.pi * 320 * s) * .6) * np.exp(-s * 55)
def knuckle(): s = tt(.05); return bp(noise(.05), 1500, 7000) * np.exp(-s * 120) * 1.4
def clank(): s = tt(.3); return (np.sin(2 * np.pi * 1700 * s) * .5 + np.sin(2 * np.pi * 2900 * s) * .3 + bp(noise(.3), 2000, 8000) * .4) * np.exp(-s * 14)
def strain_s(d): s = tt(d); return bp(noise(d), 200, 700) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 11 * s))) * np.sin(np.pi * s / d)
def scanner(d): t = tt(d); return (np.sin(2 * np.pi * 60 * t) * .6 + np.sin(2 * np.pi * 180 * t) * .2) + bp(noise(d), 4000, 9000) * .1
def clock(d):
    y = np.zeros(int(d * SR))
    for k, t in enumerate(np.arange(0, d - .05, .5)): s = tt(.03); i = int(t * SR); y[i:i + len(s)] += bp(noise(.03), 2000 if k % 2 else 1200, 6000)[:len(s)] * np.exp(-s * 160)
    return y
def iris(): n = int(.45 * SR); u = np.linspace(0, 1, n); w = noise(.45)[:n]; return (lp(w, 600) * (1 - u) + bp(w, 1500, 5000) * u) * np.sin(np.pi * u) ** 2 + np.sin(2 * np.pi * np.cumsum(200 + 500 * u) / SR) * .15 * np.sin(np.pi * u)
def thump(): s = tt(.18); return np.sin(2 * np.pi * np.cumsum(60 + 60 * np.exp(-s * 30)) / SR) * np.exp(-s * 16)

# ---- beds (never silent) ----
for a, b in ((0, B[2]), (B[3], B[5])):
    bed(max(0, a - 7), b + 7, room, .3); bed(max(0, a - 7), b + 7, clock, .1, .4); bed(max(0, a - 7), b + 7, spot_hum, .02)
bed(B[2] - 7, B[3] + 7, scanner, .12); bed(B[2] - 7, B[3] + 7, body, .25)
d3 = ft(B[3]) - ft(B[2]); add(ft(B[2]), fade(hiss(d3, 3000, 8000) * (0.5 + 0.5 * np.sin(2 * np.pi * .5 * tt(d3))), .2, .2), .05)

# ---- events ----
add(0, whoosh(ft(SLAM) + .05, False), .35); add(ft(SLAM), thud(.35), .7); add(ft(SLAM), wood_tap(), .6)
add(ft(FOLD + 2), knuckle(), .5); add(ft(FOLD + 12), wood_tap(), .3)
add(ft(52), clank(), .35); add(ft(54), strain_s(1.2), .25); add(ft(70), buzzer(.3), .18)
for b in range(1, 5):
    n = sum(len(t) for line in T["texts"][b] for t, _ in line)
    for c in range(0, n, 2): add(ft(B[b] + 3 + c / 1.6), click(1500 + (c % 4) * 120, .02), .08)
for k, at in enumerate(LIFTS[:3]):
    add(ft(at), whoosh(.18, True), .12); add(ft(at + 4), bloop(600 + k * 150, True, .1), .3); add(ft(at + 27), wood_tap(), .45)
add(ft(LIFTS[3]), strain_s(.9), .3); add(ft(LIFTS[3] + 4), buzzer(.4), .25); add(ft(LIFTS[3] + 4), thud(.2), .3)
for k in range(4): add(ft(B[2] + 30 + k * 19.6), thump(), .35); add(ft(B[2] + 30 + k * 19.6), strain_s(.4), .15)
add(ft(B[2] + 12), sparkle(.5), .1); add(ft(B[2] + 40), bloop(300, False, .15), .25)
add(ft(UNFOLD), knuckle(), .45); add(ft(UNFOLD + 10), wood_tap(), .3)
add(ft(FREE), pop(), .45); add(ft(FREE + 2), sparkle(.7), .18); add(ft(FREE + 4), bloop(700, True, .12), .3)
add(ft(B[4] + 14), clank(), .3)
for k in range(4): add(ft(B[4] + 20 + k * 12), strain_s(.25), .12)
add(ft(B[5] - 26), whoosh(.8, True), .25)
for c in B[1:5]: add(ft(c - 7), iris(), .3)

mix = np.stack([hp(L, 30), hp(R, 30)], 1)[: int(SR * DUR)]
mix = np.tanh(mix * 1.05) / 1.05 * .93
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("peak", round(float(np.abs(mix).max()), 3), "quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s")
