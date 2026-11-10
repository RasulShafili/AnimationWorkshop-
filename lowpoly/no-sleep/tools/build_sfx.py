#!/usr/bin/env python3
"""Realistic, flowing SFX bed for no-sleep (adapted from testosterone-x2). No music, no melody, no chiptune beeps.
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
B = T["beats"]; END = T["total"]; MICRO = T["micro"]; FALL = T["fall"]
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

# ---------------- beds ----------------
room_e = env([(0, 1), (B[4] - 4, 1), (B[4], 0), (B[5], 0), (B[5] + 6, 1), (END, 1)])
stereo_bed(lp(noise(N), 170) * 1.2, lp(noise(N), 170) * 1.2, room_e, 0.22, 0.3)                       # night room tone
pc = np.sin(2 * np.pi * 120 * t) * .25 + bp(noise(N), 2000, 5000) * .12                                # computer fan
stereo_bed(pc, pc, room_e * env([(0, 1), (B[1], 1), (B[1] + 20, .4), (FALL + 40, .4), (FALL + 80, .1), (END, .1)]), 0.06, 0.2, )
for k in range(40):                                                                                    # crickets outside
    t0 = rng.uniform(0, DUR - .3)
    if room_e[int(t0 * SR)] < .5: continue
    for j in range(3):
        m = int(.02 * SR); s = np.arange(m) / SR
        place(t0 + j * .05, np.sin(2 * np.pi * 4600 * s) * np.sin(np.pi * s / s[-1]), .02, rng.uniform(-.8, .8), .5)
# the clock: ticks racing during the hook, then a slow heavy tick for the rest of the room scenes
tk = 0.0
while tk < ft(B[1]):
    m = int(.02 * SR); s = np.arange(m) / SR
    place(tk, bp(noise(m), 2500, 7000) * np.exp(-s * 220), .12, .4, .4); tk += max(.05, .28 - tk * .09)
for k, f0 in enumerate(range(B[1], END, 30)):
    if B[4] <= f0 < B[5]: continue
    m = int(.03 * SR); s = np.arange(m) / SR
    place(ft(f0), bp(noise(m), 1500 if k % 2 else 2200, 6000) * np.exp(-s * 160), .07, .5, .5)
# time passing in the hook: day/night whooshes
for k in range(3):
    m = int(.55 * SR); u = np.linspace(0, 1, m)
    place(ft(8 + k * 20), bp(noise(m), 400, 5000) * np.sin(np.pi * u) ** 2, .14, (-1) ** k * .5, .5)
# counter jumps: a deep thump on every beat
for c in B[1:6]:
    m = int(.6 * SR); s = np.arange(m) / SR
    place(ft(c), np.sin(2 * np.pi * np.cumsum(42 + 60 * np.exp(-s * 18)) / SR) * np.exp(-s * 6) + bp(noise(m), 60, 400) * np.exp(-s * 14) * .4, .6, 0, .3)
    m = int(.5 * SR); u = np.linspace(0, 1, m); w = noise(m)
    place(ft(c) - .3, (lp(w, 500) * (1 - u) + bp(w, 1200, 6000) * u) * np.sin(np.pi * u) ** 2, .2, 0, .5)

# ---------------- 24 h: woozy, stumbling ----------------
wz = env([(0, 0), (B[1], 0), (B[1] + 15, 1), (B[2] - 6, 1), (B[2], 0), (END, 0)])
woozy = np.sin(2 * np.pi * np.cumsum(70 + 14 * np.sin(2 * np.pi * .6 * t)) / SR) * .5 + lp(noise(N), 300) * .6
stereo_bed(woozy * (1 + .5 * np.sin(2 * np.pi * .35 * t)), woozy * (1 - .5 * np.sin(2 * np.pi * .35 * t)), wz, 0.14, 0.5)
for k in range(11):                                                                                    # uneven footsteps
    m = int(.09 * SR); s = np.arange(m) / SR
    place(ft(B[1] + 8 + k * 12 + rng.uniform(-3, 3)), bp(noise(m), 150, 1400) * np.exp(-s * 40) + np.sin(2 * np.pi * 80 * s) * np.exp(-s * 30) * .5, .22, -.5 + k * .1, .4)

# ---------------- 48 h: microsleeps (the room drops away to a heartbeat, then snaps back) ----------------
def lubdub():
    m = int(.42 * SR); s = np.arange(m) / SR; y = np.zeros(m)
    for off, a in ((0, 1), (.16, .65)):
        i = int(off * SR); ss = s[: m - i]; y[i:] += np.sin(2 * np.pi * np.cumsum(48 + 30 * np.exp(-ss * 40)) / SR) * np.exp(-ss * 22) * a
    return lp(y, 300)
duck = np.ones(N)
for a, b in MICRO:
    i0, i1 = int(ft(a) * SR), int(ft(b) * SR)
    duck[i0:i1] = 0.12
    m = int(.5 * SR); u = np.linspace(0, 1, m)
    place(ft(a) - .45, lp(noise(m), 900 - 700 * u[0]) * u ** 2 * .0 + np.sin(2 * np.pi * np.cumsum(300 - 220 * u) / SR) * np.sin(np.pi * u) * .4, .25, 0, .6)   # sinking tone
    tt0 = ft(a) + .1
    while tt0 < ft(b) - .2: place(tt0, lubdub(), .0, 0, 0); tt0 += .8
    m = int(.35 * SR); u = np.linspace(0, 1, m)
    place(ft(b) - .05, bp(noise(m), 800, 7000) * (1 - u) ** 2, .45, 0, .5)                               # jolt awake
duck = smooth(duck, 20)
dry_L *= duck; dry_R *= duck; wet_L *= duck; wet_R *= duck
for a, b in MICRO:                                                                                    # heartbeat stays through the blackout
    tt0 = ft(a) + .1
    while tt0 < ft(b) - .2: place(tt0, lubdub(), .7, 0, .3); tt0 += .8
    stereo_seg = lp(noise(int((ft(b) - ft(a)) * SR)), 120)
    place(ft(a), stereo_seg * np.sin(np.linspace(0, np.pi, len(stereo_seg))), .5, 0, .2)

# ---------------- 72 h: hallucinations (dissonant airy tones, reversed swells, skittering) ----------------
h_e = env([(0, 0), (B[3], 0), (B[3] + 40, 1), (B[4] - 6, 1), (B[4], 0), (END, 0)])
eerie = sum(np.sin(2 * np.pi * fq * t + ph) for fq, ph in ((233, 0), (247, 1), (311, 2), (466.5, 3))) * .2 * (0.6 + 0.4 * np.sin(2 * np.pi * .23 * t))
air = bp(noise(N), 1500, 5000) * (0.5 + 0.5 * np.sin(2 * np.pi * .9 * t)) ** 3 * .5
stereo_bed(eerie + air, eerie * .8 + air[::-1], h_e, 0.13, 0.8)
for k in range(5):
    m = int(.8 * SR); u = np.linspace(0, 1, m)
    place(ft(B[3] + 10 + k * 18), bp(noise(m), 600, 4000) * u ** 3, .2, (-1) ** k * .7, .8)             # reversed swells
for k in range(30):
    m = int(.02 * SR); s = np.arange(m) / SR
    place(ft(rng.uniform(B[3] + 20, B[4])), bp(noise(m), 3000, 9000) * np.exp(-s * 200), .07, rng.uniform(-.9, .9), .7)

# ---------------- the brain: electrical activity, patches powering down ----------------
b_e = env([(0, 0), (B[4] - 2, 0), (B[4] + 6, 1), (B[5] - 4, 1), (B[5], 0), (END, 0)])
hum = np.sin(2 * np.pi * 55 * t) * .5 + np.sin(2 * np.pi * 110.4 * t) * .25 + lp(noise(N), 200) * .5
quiet = env([(0, 1), (B[4], 1), (B[5], .45), (END, .45)])                                               # less activity as more of it sleeps
stereo_bed(hum, hum, b_e, 0.3, 0.3)
for k in range(150):
    f0 = rng.uniform(B[4], B[5]); 
    if rng.uniform() > quiet[int(ft(f0) * SR)]: continue
    m = int(rng.uniform(.01, .03) * SR); s = np.arange(m) / SR
    place(ft(f0), hp(noise(m), 3000) * np.exp(-s * 150), rng.uniform(.04, .1), rng.uniform(-.8, .8), .5)   # neural crackle
L5 = B[5] - B[4] - 20
for st in (0.12, 0.3, 0.48, 0.62, 0.78):                                                              # each patch shutting down
    m = int(.9 * SR); s = np.arange(m) / SR
    down = np.sin(2 * np.pi * np.cumsum(420 * np.exp(-s * 2.6) + 50) / SR) * np.exp(-s * 2.2) * .5 + lp(noise(m), 500) * np.exp(-s * 4) * .5
    place(ft(B[4] + st * L5), down, .3, rng.uniform(-.5, .5), .6)

# ---------------- the crash ----------------
m = int(.5 * SR); u = np.linspace(0, 1, m); place(ft(FALL + 6), bp(noise(m), 300, 3000) * np.sin(np.pi * u) ** 2, .25, -.3, .4)          # falling air
m = int(.7 * SR); s = np.arange(m) / SR
place(ft(FALL + 30), np.sin(2 * np.pi * np.cumsum(50 + 60 * np.exp(-s * 14)) / SR) * np.exp(-s * 5) + lp(noise(m), 700) * np.exp(-s * 7), .8, -.3, .4)   # body onto mattress
for k in range(3):                                                                                     # bed springs settling
    m = int(.12 * SR); s = np.arange(m) / SR
    place(ft(FALL + 38 + k * 7), np.sin(2 * np.pi * (700 - k * 90) * s) * np.exp(-s * 30) * .5 + bp(noise(m), 500, 3000) * np.exp(-s * 40) * .4, .12, -.4, .5)
for k in range(3):                                                                                     # slow sleepy breathing (air only)
    m = int(1.4 * SR); u = np.linspace(0, 1, m)
    place(ft(FALL + 60) + k * 1.5, bp(noise(m), 300, 1400) * np.sin(np.pi * u) ** 2 * (0.6 + 0.4 * (u < .45)), .1, -.3, .5)

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
