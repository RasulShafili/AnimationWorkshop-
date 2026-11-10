#!/usr/bin/env python3
"""Realistic, flowing SFX bed for oxygen-doubled (adapted from sun-black-hole). No music, no melody, no chiptune beeps.
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
B = T["beats"]; END = T["total"]; STRIKE = T["strike"]; R0, R1 = T["rust"]; F0, F1 = T["fly"]
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

# ---------------- continuous layers ----------------
# outdoor air: soft gusty wind, decorrelated L/R, everywhere
gust = 0.55 + 0.45 * smooth(np.abs(noise(N)), 0.6) / 0.6
stereo_bed(bp(noise(N), 250, 1400) * gust, bp(noise(N), 260, 1500) * gust[::-1], env([(0, .6), (B[2], .6), (B[3], .9), (B[5], .6), (END, 1.0)]), 0.18, 0.4)
stereo_bed(lp(noise(N), 140), lp(noise(N), 140), env([(0, 1), (END, 1)]), 0.25, 0.2)            # distant town rumble
day = env([(0, 1), (R0, 1), (R0 + 20, 0.2), (R0 + 50, 1), (R0 + 95, 0.2), (R0 + 125, 1), (R1, 1), (END, 1)])
for k in range(70):  # birds in daylight, quiet during the fire
    f0 = rng.uniform(0, END); 
    if B[2] + 30 < f0 < B[3] + 30: continue
    n = int(rng.uniform(.05, .11) * SR); s = np.arange(n) / SR
    fr = rng.uniform(2800, 4300) + rng.uniform(-900, 900) * s / s[-1] + 300 * np.sin(2 * np.pi * rng.uniform(25, 45) * s)
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * s / s[-1]) ** 2 * day[min(N - 1, int(ft(f0) * SR))], rng.uniform(.025, .06), rng.uniform(-.8, .8), 0.5)
for k in range(40):  # crickets at night in the time-lapse
    f0 = R0 + rng.uniform(0, R1 - R0); g = 1 - day[int(ft(f0) * SR)]
    if g < .3: continue
    for j in range(3):
        n = int(.02 * SR); s = np.arange(n) / SR
        place(ft(f0) + j * .05, np.sin(2 * np.pi * 4500 * s) * np.sin(np.pi * s / s[-1]), .025 * g, rng.uniform(-.7, .7), .4)

# campfire: crackle grains + soft roar, louder in the park shots, much bigger after the oxygen jump
camp_e = env([(0, .5), (T["flare"] - 1, .5), (T["flare"] + 4, 1.6), (T["flare"] + 40, 1.0), (B[1], 1.0), (B[2], .6), (B[2] + 20, .1), (B[4] - 10, .1), (B[4] + 10, .6), (B[5], .6), (B[5] + 40, .2), (END - 30, .2), (END, .5)])
stereo_bed(bp(noise(N), 120, 900) * (0.7 + 0.3 * smooth(np.abs(noise(N)), 4) / 0.8), bp(noise(N), 120, 900), camp_e, 0.16, 0.3)
for k in range(int(DUR * 14)):
    t0 = rng.uniform(0, DUR - .05); g = camp_e[int(t0 * SR)]
    n = int(rng.uniform(.006, .03) * SR); s = np.arange(n) / SR
    place(t0, hp(noise(n), 1500) * np.exp(-s * rng.uniform(120, 300)), rng.uniform(.04, .14) * g, rng.uniform(-.4, .4), .4)

# ---------------- events ----------------
# the oxygen jump: a long airy inhale rising to a whoomp as the fire flares
d = ft(T["gauge"][1]) - ft(T["gauge"][0]); n = int(d * SR); u = np.linspace(0, 1, n); w = noise(n)
place(ft(T["gauge"][0]), (lp(w, 400) * (1 - u) + bp(w, 1200, 7000) * u) * u ** 1.5, 0.45, 0, 0.6)
n = int(1.4 * SR); s = np.arange(n) / SR
place(ft(T["flare"]), np.sin(2 * np.pi * np.cumsum(55 + 50 * np.exp(-s * 10)) / SR) * np.exp(-s * 3) * .8 + bp(noise(n), 150, 2500) * np.exp(-s * 2.5), 0.7, 0, 0.5)
# runner's footsteps on the sand track
for k in range(int((B[2] - B[1] + 40) / 9.5)):
    n = int(.07 * SR); s = np.arange(n) / SR
    place(ft(B[1] - 20 + k * 9.5), bp(noise(n), 250, 2200) * np.exp(-s * 55), 0.14, 0.25 if k % 2 else -0.25, 0.3)
# lightning: a ripping crack, then thunder rolling for seconds
n = int(.35 * SR); s = np.arange(n) / SR
place(ft(STRIKE), (noise(n) * np.exp(-s * 18) + hp(noise(n), 2000) * np.exp(-s * 40)), 0.9, 0.2, 0.4)
n = int(4.5 * SR); s = np.arange(n) / SR; roll = 0.5 + 0.5 * smooth(np.abs(noise(n)), 3) / 0.6
place(ft(STRIKE) + .15, lp(noise(n), 260) * roll * np.exp(-s * 0.9) * np.minimum(1, s * 8), 1.0, 0, 0.7)
# the forest fire: a roar that grows as it spreads, dense crackles, trees cracking and falling
fire_e = env([(0, 0), (STRIKE + 4, 0), (STRIKE + 30, .5), (STRIKE + 110, 1.0), (T["spread"][1], 1.0), (B[3] - 6, .8), (B[3] + 10, .15), (B[3] + 80, 0), (END, 0)])
stereo_bed(bp(noise(N), 60, 700) * (0.6 + 0.4 * smooth(np.abs(noise(N)), 5) / 0.8), bp(noise(N), 60, 700), fire_e, 0.55, 0.4)
for k in range(260):
    f0 = rng.uniform(STRIKE + 4, B[3] + 40); g = fire_e[int(ft(f0) * SR)]
    n = int(rng.uniform(.005, .025) * SR); s = np.arange(n) / SR
    place(ft(f0), hp(noise(n), 1200) * np.exp(-s * rng.uniform(100, 260)), rng.uniform(.06, .2) * g, rng.uniform(-.8, .8), .5)
for k in range(4):
    f0 = STRIKE + 60 + k * 38; n = int(1.0 * SR); s = np.arange(n) / SR
    crack = bp(noise(n), 300, 3000) * np.exp(-s * 30) + np.sin(2 * np.pi * np.cumsum(70 + 40 * np.exp(-s * 10)) / SR) * np.exp(-s * 6) * .6 * (s > .35)
    place(ft(f0), crack, 0.3, rng.uniform(-.6, .6), 0.6)
# rust time-lapse: day/night whooshes, metal groans and creaks, rattling flakes
for k in range(4):
    n = int(.9 * SR); u = np.linspace(0, 1, n)
    place(ft(R0 + k * (R1 - R0) / 4), bp(noise(n), 300, 5000) * np.sin(np.pi * u) ** 2, 0.2, (-1) ** k * .5, 0.6)
for k in range(6):
    f0 = R0 + 10 + k * 22; n = int(rng.uniform(.6, 1.1) * SR); s = np.arange(n) / SR
    fr = rng.uniform(140, 260) * (1 + .3 * np.sin(2 * np.pi * rng.uniform(1, 3) * s))
    groan = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rng.uniform(12, 25) * s))) * np.sin(np.pi * s / s[-1])
    place(ft(f0), bp(groan, 150, 2500), 0.12, rng.uniform(-.7, .7), 0.6)
for k in range(40):
    n = int(.015 * SR); s = np.arange(n) / SR
    place(ft(rng.uniform(R0, R1)), bp(noise(n), 2500, 9000) * np.exp(-s * 200), .05, rng.uniform(-.8, .8), .5)
# dragonfly: a low wing buzz that swings left/right as it circles
d = ft(F1 + 10) - ft(F0 - 10); n = int(d * SR); s = np.arange(n) / SR
buzz = bp(noise(n), 120, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 26 * s)) ** 2 + np.sin(2 * np.pi * 52 * s) * .25
e = np.minimum(1, s * 2) * np.minimum(1, (d - s) * 2) * (0.75 + 0.25 * np.sin(2 * np.pi * (0.035 * FPS / (2 * np.pi)) * s))
pan = np.sin(2 * np.pi * (0.035 * FPS / (2 * np.pi)) * s)
i0 = int(ft(F0 - 10) * SR); j0 = min(N, i0 + n)
for arr, sgn, wet in ((dry_L, -1, wet_L), (dry_R, 1, wet_R)):
    seg = buzz[: j0 - i0] * e[: j0 - i0] * (1 + sgn * pan[: j0 - i0] * .6) * .35
    arr[i0:j0] += seg; wet[i0:j0] += seg * .3
# ending: wind swell as the camera pulls out, then a whoosh back into frame 0
n = int(2.2 * SR); u = np.linspace(0, 1, n)
place(ft(B[5]), bp(noise(n), 200, 3000) * np.sin(np.pi * u) ** 2, 0.3, 0, 0.6)
n = int(1.2 * SR); u = np.linspace(0, 1, n); w = noise(n)
place(ft(END) - 1.2, (lp(w, 400) * (1 - u) + bp(w, 1500, 6000) * u) * u ** 2, 0.4, 0, 0.5)
# shot changes: soft air swishes
for c in B[1:6]:
    n = int(.5 * SR); u = np.linspace(0, 1, n)
    place(ft(c) - .3, bp(noise(n), 500, 5000) * np.sin(np.pi * u) ** 2, 0.12, 0, 0.5)

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
