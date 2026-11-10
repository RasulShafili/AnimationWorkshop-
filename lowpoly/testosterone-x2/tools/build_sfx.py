#!/usr/bin/env python3
"""Realistic, flowing SFX bed for testosterone-x2 (adapted from oxygen-doubled). No music, no melody, no chiptune beeps.
One continuous space drone that morphs between scenes (sun roar -> black-hole sub hum -> cold wind),
plus cinematic one-shots (implosion + boom, light-shell sweep, ice cracks, final dive). Everything is sent
through a long synthetic stereo reverb so the sound flows instead of clicking. Timings: src/timeline.json."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timeline.json"))
SR, FPS = 44100, T["fps"]
DUR = T["total"] / FPS
N = int(SR * DUR)
B = T["beats"]; END = T["total"]; EV = T["every"]; HEART = T["heart"]; M0, M1 = T["molecules"]
rng = np.random.default_rng(5)
ft = lambda f: f / FPS
t = np.arange(N) / SR
sos = lambda kind, f: butter(2, f, kind, fs=SR, output="sos")
lp = lambda x, f: sosfilt(sos("low", f), x)
hp = lambda x, f: sosfilt(sos("high", f), x)
bp = lambda x, a, b: sosfilt(sos("bandpass", [a, b]), x)
noise = lambda n: rng.standard_normal(n)
def brown(n): x = np.cumsum(noise(n)); x -= lp(x, 8); return x / (np.abs(x).max() + 1e-9)
def env(points):
    """piecewise-linear envelope over the whole timeline from [(frame, value), ...]"""
    fs, vs = zip(*points); return np.interp(t, np.array(fs) / FPS, vs)
def smooth(x, hz=3): return lp(lp(x, hz), hz)

dry_L, dry_R = np.zeros(N), np.zeros(N)       # dry
wet_L, wet_R = np.zeros(N), np.zeros(N)       # sent to reverb
def place(t0, y, g=1.0, pan=0.0, send=0.5):
    i = int(t0 * SR); j = min(N, i + len(y))
    if i >= N or j <= max(0, i): return
    y = y[:j - i] * g; a, b = (1 - max(0, pan)), (1 + min(0, pan))
    dry_L[i:j] += y * a; dry_R[i:j] += y * b; wet_L[i:j] += y * a * send; wet_R[i:j] += y * b * send
def stereo_bed(yL, yR, e, g, send=0.3):
    dry_L[:] += yL * e * g; dry_R[:] += yR * e * g; wet_L[:] += yL * e * g * send; wet_R[:] += yR * e * g * send

# ---------------- beds per scene ----------------
gym = env([(0, 1), (B[3] - 4, 1), (B[3], 0), (M1, 0), (M1 + 6, 1), (END, 1)])
stereo_bed(lp(noise(N), 180) * 1.2, lp(noise(N), 180) * 1.2, gym, 0.25, 0.3)                                   # room tone
stereo_bed(bp(noise(N), 300, 1200) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.07 * t)), bp(noise(N), 300, 1200), gym, 0.05, 0.5)  # city through the windows
hvac = np.sin(2 * np.pi * 60 * t) * .3 + bp(noise(N), 1500, 4000) * .15
stereo_bed(hvac, hvac, gym, 0.04, 0.2)
for k in range(10):  # someone racking weights far away
    f0 = rng.uniform(0, END)
    if not (f0 < B[3] - 20 or f0 > M1 + 20): continue
    n = int(.35 * SR); s = np.arange(n) / SR
    place(ft(f0), (np.sin(2 * np.pi * 820 * s) * .4 + np.sin(2 * np.pi * 1330 * s) * .25 + bp(noise(n), 800, 4000) * .4) * np.exp(-s * 16), .05, rng.uniform(-.9, .9), .9)
vessel = env([(0, 0), (B[3] - 4, 0), (B[3] + 4, 1), (HEART - 2, 1), (HEART + 2, 0), (END, 0)])
thick = env([(0, 1), (B[3], 1), (HEART, .35), (END, .35)])
stereo_bed(lp(noise(N), 500) * (0.6 + 0.4 * thick), lp(noise(N), 500), vessel, 0.45, 0.4)                  # blood rushing, slowing
heart_e = env([(0, 0), (HEART - 2, 0), (HEART + 2, 1), (B[4] - 2, 1), (B[4] + 2, 0), (END, 0)])
stereo_bed(lp(noise(N), 120), lp(noise(N), 120), heart_e, 0.4, 0.3)
mol = env([(0, 0), (M0 - 2, 0), (M0 + 4, 1), (M1 - 2, 1), (M1 + 2, 0), (END, 0)])
stereo_bed(bp(noise(N), 200, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.3 * t)), bp(noise(N), 220, 950), mol, 0.18, 0.6)

def lubdub(g=1.0):
    n = int(.42 * SR); s = np.arange(n) / SR; y = np.zeros(n)
    for off, a in ((0, 1), (.16, .65)):
        i = int(off * SR); m = n - i; ss = s[:m]
        y[i:] += np.sin(2 * np.pi * np.cumsum(48 + 30 * np.exp(-ss * 40)) / SR) * np.exp(-ss * 22) * a
    return lp(y, 300) * g
# heartbeat under the vessel (getting heavier) and racing in the heart shot
tt0 = ft(B[3])
while tt0 < ft(HEART): place(tt0, lubdub(), .55, 0, .3); tt0 += 60 / 78
tt0 = ft(HEART)
while tt0 < ft(B[4]):
    bpm = 72 + (168 - 72) * (tt0 - ft(HEART)) / (ft(B[4]) - ft(HEART)); place(tt0, lubdub(), .85, 0, .3); tt0 += 60 / bpm
# squishy cells bumping in the thick blood
for k in range(40):
    f0 = rng.uniform(B[3], HEART); n = int(rng.uniform(.04, .09) * SR); s = np.arange(n) / SR
    place(ft(f0), lp(noise(n), 700) * np.sin(np.pi * s / s[-1]) ** 2, .08 * (f0 - B[3]) / (HEART - B[3]) + .02, rng.uniform(-.7, .7), .5)

# ---------------- the doubling pulse every 2 s: a deep thump that grows ----------------
for k in range(1, END // EV + 1):
    n = int(.6 * SR); s = np.arange(n) / SR
    thump = np.sin(2 * np.pi * np.cumsum(42 + 60 * np.exp(-s * 18)) / SR) * np.exp(-s * 6) + bp(noise(n), 60, 400) * np.exp(-s * 14) * .4
    place(ft(k * EV), thump, min(.9, .25 + k * .05), 0, .3)
    n = int(.25 * SR); u = np.linspace(0, 1, n)
    place(ft(k * EV) - .25, bp(noise(n), 1000, 6000) * u ** 3, .08 + k * .01, 0, .4)   # tiny inhale before each hit

# ---------------- body events ----------------
for k in range(5):  # dumbbell curls: grip creak + air
    n = int(.5 * SR); u = np.linspace(0, 1, n)
    place(ft(8 + k * 39.3), bp(noise(n), 300, 1800) * np.sin(np.pi * u) ** 2, .07, .3, .4)
n = int(.6 * SR); s = np.arange(n) / SR   # the dropped dumbbell: heavy clang on rubber, a bounce, a roll
clang = (np.sin(2 * np.pi * 180 * s) * .5 + np.sin(2 * np.pi * 455 * s) * .3 + bp(noise(n), 100, 1500)) * np.exp(-s * 12)
place(ft(T["drop"] + 9), clang, .7, .4, .5); place(ft(T["drop"] + 15), clang * .4, .5, .45, .5)
n = int(1.2 * SR); s = np.arange(n) / SR
place(ft(T["drop"] + 16), bp(noise(n), 150, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * s)) * np.exp(-s * 2.5), .15, .5, .4)
for k in range(8):  # muscles swelling: rubbery stretch creaks
    f0 = T["muscle"][0] + k * 12; n = int(.45 * SR); s = np.arange(n) / SR
    fr = rng.uniform(90, 160) * (1 + .5 * s / s[-1])
    cr = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rng.uniform(30, 60) * s))) * np.sin(np.pi * s / s[-1])
    place(ft(f0), bp(cr, 100, 2500), .14, rng.uniform(-.5, .5), .4)
n = int(.5 * SR); u = np.linspace(0, 1, n); place(ft(125), bp(noise(n), 400, 4000) * np.sin(np.pi * u) ** 2, .2, 0, .4)  # flex swoosh
# shirt rip: a fast ragged tear, then the halves flapping away
n = int(.55 * SR); s = np.arange(n) / SR
grain = np.repeat(rng.uniform(0, 1, n // 90 + 1), 90)[:n] ** 3
place(ft(T["rip"]) - .1, bp(noise(n), 800, 7000) * grain * np.minimum(1, s * 30) * np.exp(-s * 3), .75, 0, .4)
for k in range(2):
    n = int(.7 * SR); u = np.linspace(0, 1, n)
    place(ft(T["rip"] + 4), bp(noise(n), 200, 2500) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * u)) * (1 - u) ** 2, .15, (-1) ** k * .7, .5)
for k in range(12):  # beard bristling in
    f0 = T["beard"][0] + k * 7; n = int(.3 * SR); u = np.linspace(0, 1, n)
    place(ft(f0), hp(noise(n), 4000) * np.sin(np.pi * u) ** 2, .05, rng.uniform(-.4, .4), .3)
for k in range(12):  # acne: tiny wet pops
    f0 = T["acne"][0] + k * 6 + rng.uniform(0, 3); n = int(.04 * SR); s = np.arange(n) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(900 - 600 * s / s[-1]) / SR) * np.exp(-s * 80), .16, rng.uniform(-.5, .5), .3)
for k in range(14):  # hair falling: soft rustles
    f0 = T["hair"][0] + k * 5; n = int(.25 * SR); u = np.linspace(0, 1, n)
    place(ft(f0), bp(noise(n), 3000, 9000) * np.sin(np.pi * u) ** 3, .04, rng.uniform(-.5, .5), .4)
# aromatase chomps and conversions
for k in range(16):
    f0 = M0 + 12 + k * 8; n = int(.12 * SR); s = np.arange(n) / SR
    place(ft(f0), lp(noise(n), 900) * np.exp(-s * 25) + np.sin(2 * np.pi * np.cumsum(260 - 140 * s / s[-1]) / SR) * np.exp(-s * 30) * .6, .18, 0, .4)
    n = int(.3 * SR); s = np.arange(n) / SR
    place(ft(f0 + 4), hp(noise(n), 6000) * np.exp(-s * 12), .05, .3, .6)
# chest change: a soft slow inflating stretch
n = int(2.6 * SR); u = np.linspace(0, 1, n)
place(ft(T["chest"][0]), bp(noise(n), 150, 900) * np.sin(np.pi * u) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * u)), .18, 0, .4)
# the end: pounding heart and a racing monitor beep
tt0 = ft(B[5])
while tt0 < ft(END) - .3:
    place(tt0, lubdub(), .55, 0, .3)
    n = int(.08 * SR); s = np.arange(n) / SR
    place(tt0 + .02, np.sin(2 * np.pi * 1000 * s) * np.minimum(1, s * 200) * np.exp(-s * 8), .05, .6, .5)
    tt0 += 60 / 150
# cuts into and out of the body
for c in (B[3], HEART, M0, M1):
    n = int(.6 * SR); u = np.linspace(0, 1, n); w = noise(n)
    place(ft(c) - .3, (lp(w, 500) * (1 - u) + bp(w, 1200, 6000) * u) * np.sin(np.pi * u) ** 2, .3, 0, .5)
n = int(1.0 * SR); u = np.linspace(0, 1, n)
place(ft(END) - 1.0, bp(noise(n), 400, 5000) * u ** 2, .2, 0, .5)

# ---------------- reverb (synthetic stereo hall, 2.8 s) ----------------
ir_n = int(2.8 * SR); s = np.arange(ir_n) / SR
irL = lp(noise(ir_n), 5000) * np.exp(-s * 2.4); irR = lp(noise(ir_n), 5000) * np.exp(-s * 2.4)
irL[: int(.012 * SR)] = 0; irR[: int(.017 * SR)] = 0
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
L = dry_L + fftconvolve(wet_L, irL)[:N] * 0.9
R = dry_R + fftconvolve(wet_R, irR)[:N] * 0.9
mix = np.stack([hp(L, 25), hp(R, 25)], 1)
mix /= np.abs(mix).max() + 1e-9

# ---------------- narration (Kokoro am_fenrir, vo/l*.wav) with ducking ----------------
VO_AT = T["vo"]
vo = np.zeros(N)
for i, f in enumerate(VO_AT):
    sr, y = wavfile.read(f"{ROOT}/vo/l{i}.wav"); y = y.astype(np.float64) / 32768
    a = int(ft(f) * SR); b = min(N, a + len(y)); vo[a:b] += y[: b - a]
vo = hp(vo, 80) / (np.abs(vo).max() + 1e-9)
# a little room so the voice sits in the same space as the effects
vo_room = fftconvolve(vo, irL[: int(.6 * SR)])[:N] * 0.08
duck = 1 - 0.55 * np.clip(smooth(np.abs(vo), 6) * 6, 0, 1)
mix = mix * duck[:, None] * 0.55 + np.stack([vo + vo_room, vo + vo_room], 1) * 0.9
mix /= np.abs(mix).max() + 1e-9
mix = np.tanh(mix * 1.15) / np.tanh(1.15) * 0.9
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s; loudest", round(max(rms), 1))
