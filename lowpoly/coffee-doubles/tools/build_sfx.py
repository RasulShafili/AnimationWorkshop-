#!/usr/bin/env python3
"""Realistic, flowing SFX bed for coffee-doubles (adapted from no-sleep). No music, no melody, no chiptune beeps.
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
B = T["beats"]; END = T["total"]; CUPS = T["cupsAt"]; REL = T["release"]; CRASH = T["crash"]
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

# ---------------- café beds (no voices: cups, machine, street) ----------------
cafe = env([(0, 1), (B[5] - 4, 1), (B[5], 0), (CRASH, 0), (CRASH + 6, .6), (END, .4)])
stereo_bed(lp(noise(N), 220) * 1.2 + bp(noise(N), 300, 1200) * .3, lp(noise(N), 220) * 1.2 + bp(noise(N), 300, 1200) * .3, cafe, 0.22, 0.4)
for k in range(26):                                                    # distant cups and spoons on saucers
    t0 = rng.uniform(0, DUR - .3)
    if cafe[int(t0 * SR)] < .5: continue
    m = int(.25 * SR); s = np.arange(m) / SR; fr = rng.uniform(2200, 4200)
    place(t0, (np.sin(2 * np.pi * fr * s) + .5 * np.sin(2 * np.pi * fr * 2.7 * s)) * np.exp(-s * 18), rng.uniform(.012, .03), rng.uniform(-.9, .9), .9)
for t0 in (1.8, 9.5, 16.0):                                            # espresso machine hiss in the background
    m = int(2.2 * SR); u = np.linspace(0, 1, m)
    place(t0, bp(noise(m), 2500, 8000) * np.sin(np.pi * u) ** .5 * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * u)), .04, -.7, .7)
# ---------------- each new cup: a ceramic clunk on the table + a pour ----------------
for k, a in enumerate(CUPS):
    m = int(.35 * SR); s = np.arange(m) / SR
    clunk = (np.sin(2 * np.pi * 180 * s) * .6 + np.sin(2 * np.pi * 1450 * s) * .3 + bp(noise(m), 500, 4000) * .4) * np.exp(-s * 22)
    place(ft(a + 10), clunk, .45 if k < 8 else .3, .35 + (k % 3) * .1, .4)
    if k in (0, 1, 2, 4, 8):
        m = int(.6 * SR); u = np.linspace(0, 1, m)
        place(ft(a) - .3, bp(noise(m), 300, 2200) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * u)) * np.sin(np.pi * u), .12, .3, .5)
# ---------------- typing that speeds up, then stalls ----------------
spd = [0, 3.0, 6.0, 9.0, 13.0]
for bi in range(1, 5):
    tt0 = ft(B[bi]); r = spd[bi]
    while tt0 < ft(B[bi + 1]) - .1:
        m = int(.02 * SR); s = np.arange(m) / SR
        place(tt0, bp(noise(m), 1500, 6000) * np.exp(-s * 220), .05 + .01 * bi, rng.uniform(-.2, .2), .3)
        tt0 += rng.uniform(.6, 1.4) / r
# ---------------- heartbeat speeding with the cups; tinnitus in the danger zone ----------------
def lubdub():
    m = int(.42 * SR); s = np.arange(m) / SR; y = np.zeros(m)
    for off, aa in ((0, 1), (.16, .65)):
        i = int(off * SR); ss = s[: m - i]; y[i:] += np.sin(2 * np.pi * np.cumsum(48 + 30 * np.exp(-ss * 40)) / SR) * np.exp(-ss * 22) * aa
    return lp(y, 300)
bpm_of = lambda f: min(185, 72 + np.log2(max(1, sum(1 for a in CUPS if f >= a))) * 27)
tt0 = ft(B[1])
while tt0 < ft(B[5]) - .2:
    f0 = tt0 * FPS; place(tt0, lubdub(), .25 + .1 * (f0 > B[3]) + .15 * (f0 > B[4]), 0, .3); tt0 += 60 / bpm_of(f0)
ring = np.sin(2 * np.pi * 7400 * t) * .25 + np.sin(2 * np.pi * 7410 * t) * .25
stereo_bed(ring, ring, env([(0, 0), (B[4], 0), (B[4] + 30, 1), (B[5] - 4, 1), (B[5], 0), (END, 0)]), 0.025, 0.2)
for k in range(int((B[5] - B[4]) / 9)):                                # monitor-like alarm beeps
    if k % 2: continue
    m = int(.09 * SR); s = np.arange(m) / SR
    place(ft(B[4] + 10 + k * 9), np.sin(2 * np.pi * 1300 * s) * np.minimum(1, s * 300) * np.exp(-s * 6), .06, .5, .4)
# anxiety: a low unsettled drone from 8 cups
stereo_bed(lp(noise(N), 90) * 1.5 + np.sin(2 * np.pi * 51 * t) * .3, lp(noise(N), 90) * 1.5, env([(0, 0), (B[3], 0), (B[3] + 30, .7), (B[4], 1), (B[5] - 4, 1), (B[5], 0), (END, 0)]), 0.25, 0.3)
# ---------------- the synapse: beans clicking into receptors, the pile humming, then the flood ----------------
syn = env([(0, 0), (B[5] - 2, 0), (B[5] + 6, 1), (CRASH - 4, 1), (CRASH, 0), (END, 0)])
stereo_bed(lp(noise(N), 400) * (0.6 + 0.4 * np.sin(2 * np.pi * .4 * t)), lp(noise(N), 400), syn, 0.25, 0.4)
for k in range(30):
    f0 = B[5] + 10 + k * ((REL - B[5] - 10) / 30)
    m = int(.12 * SR); s = np.arange(m) / SR
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(500 + 200 * s / s[-1]) / SR) * np.sin(np.pi * s / s[-1]) * .5, .05 + .002 * k, rng.uniform(-.7, .7), .6)   # adenosine piling up
for k in range(7):                                                     # beans popping out
    m = int(.08 * SR); s = np.arange(m) / SR
    place(ft(REL) + k * .05, np.sin(2 * np.pi * np.cumsum(300 + 900 * s / s[-1]) / SR) * np.exp(-s * 30), .18, -.6 + k * .2, .5)
m = int(1.6 * SR); u = np.linspace(0, 1, m); w = noise(m)
place(ft(REL + 8), (lp(w, 300) * (1 - u) + bp(w, 600, 4000) * u) * np.sin(np.pi * u) ** .6, .5, 0, .7)        # the flood
# ---------------- the crash: head hits the table, mugs topple, the world goes muffled ----------------
m = int(.7 * SR); s = np.arange(m) / SR
place(ft(CRASH + 18), np.sin(2 * np.pi * np.cumsum(55 + 70 * np.exp(-s * 14)) / SR) * np.exp(-s * 6) + bp(noise(m), 200, 2500) * np.exp(-s * 12) * .6, .8, 0, .4)
for k in range(9):
    m = int(.3 * SR); s = np.arange(m) / SR; fr = rng.uniform(900, 1700)
    place(ft(CRASH + 24) + k * rng.uniform(.04, .12), (np.sin(2 * np.pi * fr * s) * .5 + bp(noise(m), 800, 5000) * .5) * np.exp(-s * 14), .2, rng.uniform(-.2, .8), .5)
for k in range(3):
    m = int(1.4 * SR); u = np.linspace(0, 1, m)
    place(ft(CRASH + 45) + k * 1.6, bp(noise(m), 250, 1100) * np.sin(np.pi * u) ** 2, .08, -.2, .5)
for c in list(B[1:7]) + [CRASH]:
    m = int(.45 * SR); u = np.linspace(0, 1, m); w = noise(m)
    place(ft(c) - .25, (lp(w, 500) * (1 - u) + bp(w, 1200, 6000) * u) * np.sin(np.pi * u) ** 2, .14, 0, .5)

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
