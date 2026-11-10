#!/usr/bin/env python3
"""Realistic, flowing SFX bed for sun-black-hole. No music, no melody, no chiptune beeps.
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
B, COL = T["beats"], T["collapse"]
LIGHT_OFF = round(T["shellStart"] + (T["shellEnd"] - T["shellStart"]) * 6 / 6.6)
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

# ---------------- continuous layers (each crossfades through the whole video) ----------------
# 1. deep space drone: brown noise below 110 Hz, slowly breathing, decorrelated L/R
dL, dR = lp(brown(N), 110), lp(brown(N), 110)
breath = 0.75 + 0.25 * np.sin(2 * np.pi * 0.11 * t) * np.sin(2 * np.pi * 0.047 * t + 1)
stereo_bed(dL * breath, dR * breath, env([(0, 0.7), (540, 0.9)]), 1.0, 0.2)

# 2. sun: roaring plasma = band-passed noise with turbulent amplitude + crackle grains, grows until the collapse
roar_e = env([(0, 0.8), (COL - 14, 1.0), (COL - 2, 1.3), (COL, 0), (540, 0)])
turb = 0.6 + 0.4 * smooth(np.abs(noise(N)), 6) / 0.8
rL, rR = bp(noise(N), 90, 700) * turb, bp(noise(N), 90, 700) * turb[::-1]
stereo_bed(rL, rR, roar_e, 0.55, 0.35)
for k in range(int(ft(COL) * 60)):
    tt0 = rng.uniform(0, ft(COL) - .05); d = rng.uniform(.01, .04); n = int(d * SR)
    place(tt0, hp(noise(n), 1800) * np.exp(-np.arange(n) / SR * 90), rng.uniform(.04, .12), rng.uniform(-.7, .7), .6)

# 3. black hole: a sub hum (two close sines beating) + low rumble; in space only, swells at the dive
END = T["total"]; DARK = T["dark"]; I0, I1 = T["freeze"]
hole_e = env([(0, 0), (COL, 0), (COL + 20, 0.8), (B[3] - 4, 0.7), (B[3], 0), (B[6], 0), (B[6] + 10, 0.5), (END - 60, 0.8), (END, 1.2)])
sub = np.sin(2 * np.pi * 38 * t) + 0.7 * np.sin(2 * np.pi * 38.6 * t) + 0.25 * np.sin(2 * np.pi * 76.3 * t)
stereo_bed(sub * 0.5 + lp(noise(N), 220) * 0.6, sub * 0.5 + lp(noise(N), 220) * 0.6, hole_e, 0.35, 0.25)
# the space drone steps back while we are on the ground
dry_L[:] *= env([(0, 1), (B[3] - 4, 1), (B[3], 0.35), (B[6], 0.35), (B[6] + 6, 1), (END, 1)]); dry_R[:] *= env([(0, 1), (B[3] - 4, 1), (B[3], 0.35), (B[6], 0.35), (B[6] + 6, 1), (END, 1)])
wet_L[:] *= env([(0, 1), (B[3] - 4, 1), (B[3], 0.35), (B[6], 0.35), (B[6] + 6, 1), (END, 1)]); wet_R[:] *= env([(0, 1), (B[3] - 4, 1), (B[3], 0.35), (B[6], 0.35), (B[6] + 6, 1), (END, 1)])

# 4. town at noon: light breeze, distant traffic, birdsong (stops dead at the blackout)
day_e = env([(0, 0), (B[3], 0), (B[3] + 4, 1), (DARK, 1), (DARK + 1, 0), (END, 0)])
stereo_bed(bp(noise(N), 300, 1500) * 0.5 + lp(noise(N), 160) * 0.8, bp(noise(N), 300, 1500) * 0.5 + lp(noise(N), 160) * 0.8, day_e, 0.25, 0.3)
for k in range(14):  # birds: short natural chirps with random pitch glides
    f0 = B[3] + 4 + k * (DARK - B[3] - 6) / 14 + rng.uniform(-2, 2); n = int(rng.uniform(.06, .12) * SR); s = np.arange(n) / SR
    fr = rng.uniform(2800, 4200) + rng.uniform(-900, 900) * s / s[-1] + 300 * np.sin(2 * np.pi * rng.uniform(25, 45) * s)
    place(ft(f0), np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * s / s[-1]) ** 2, rng.uniform(.04, .08), rng.uniform(-.8, .8), 0.5)
# blackout: a deep pressure "whoomp", then electrical hum and the lamps clunking on one by one
n = int(1.6 * SR); s = np.arange(n) / SR
place(ft(DARK), np.sin(2 * np.pi * np.cumsum(45 + 40 * np.exp(-s * 8)) / SR) * np.exp(-s * 2.2) + lp(noise(n), 400) * np.exp(-s * 6) * .5, 0.7, 0, 0.6)
night_e = env([(0, 0), (DARK, 0), (DARK + 10, 1), (B[6] - 4, 1), (B[6], 0), (END, 0)])
mains = np.sin(2 * np.pi * 100 * t) * .4 + np.sin(2 * np.pi * 200 * t) * .15 + bp(noise(N), 2000, 6000) * .08
stereo_bed(mains, mains, night_e * env([(0, 1), (B[5], 1), (B[5] + 20, 0.3), (END, 0.3)]), 0.05, 0.3)
for i in range(4):
    n = int(.12 * SR); s = np.arange(n) / SR
    place(ft(DARK + 4 + i * 4), (bp(noise(n), 400, 3000) * np.exp(-s * 50) + np.sin(2 * np.pi * 120 * s) * np.exp(-s * 30) * .5), 0.3, -0.6 + i * 0.4, 0.5)
for i in range(6):  # windows light up: soft switch clicks
    n = int(.03 * SR); s = np.arange(n) / SR
    place(ft(DARK + 6 + i * 5), bp(noise(n), 1500, 6000) * np.exp(-s * 200), 0.12, -0.7 + i * 0.28, 0.4)
for k, f0 in enumerate((DARK + 30, DARK + 70)):  # a distant dog
    for j in range(2):
        n = int(.18 * SR); s = np.arange(n) / SR
        bark = bp(noise(n), 400, 1800) * np.exp(-s * 14) + np.sin(2 * np.pi * np.cumsum(500 - 400 * s) / SR) * np.exp(-s * 18) * .4
        place(ft(f0) + j * .28, bark, 0.06, 0.7 - k * 1.4, 0.9)

# 5. cold wind + snow hiss from the week of dying plants through the freezing sea
wind_e = env([(0, 0), (B[4] - 6, 0), (B[4] + 30, 0.7), (B[5], 0.9), (B[6] - 4, 1.0), (B[6], 0), (END, 0)])
gust = 0.5 + 0.5 * smooth(np.abs(noise(N)), 0.8) / 0.6
wL = bp(noise(N), 500, 2600) * gust; wR = bp(noise(N), 600, 3000) * gust[::-1]
thin = env([(0, 1), (B[4], 1), (T["year"], 0.5), (END, 0.5)])
stereo_bed(wL * thin + lp(wL, 400) * (1 - thin), wR * thin + lp(wR, 400) * (1 - thin), wind_e, 0.24, 0.45)
stereo_bed(hp(noise(N), 6000), hp(noise(N), 6000), env([(0, 0), (T["snow"], 0), (T["snow"] + 60, 1), (B[6] - 4, 1), (B[6], 0), (END, 0)]), 0.03, 0.2)
# running footsteps on frozen grass, then doors slamming shut
for i in range(5):
    r0 = T["run"][0] + i * 6
    for k in range(9):
        n = int(.06 * SR); s = np.arange(n) / SR
        place(ft(r0 + k * 7), (bp(noise(n), 300, 2500) * np.exp(-s * 70)), 0.08, -0.6 + i * 0.3, 0.3)
    n = int(.4 * SR); s = np.arange(n) / SR
    place(ft(r0 + (T["run"][1] - T["run"][0])), np.sin(2 * np.pi * np.cumsum(90 + 60 * np.exp(-s * 30)) / SR) * np.exp(-s * 12) + bp(noise(n), 300, 3000) * np.exp(-s * 30) * .6, 0.3, -0.6 + i * 0.3, 0.6)
for k in range(5):  # branches creaking as the trees die
    n = int(.6 * SR); s = np.arange(n) / SR
    place(ft(T["wilt"][0] + 10 + k * 22), bp(noise(n), 300, 1200) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * rng.uniform(10, 18) * s))) * np.sin(np.pi * s / s[-1]), 0.07, rng.uniform(-.8, .8), 0.6)

# 6. the sea: waves lapping that slow and stop as the ice spreads
sea_e = env([(0, 0), (B[5] - 10, 0), (B[5] + 6, 1), (I1, 0.15), (B[6] - 4, 0.1), (B[6], 0), (END, 0)])
lap = 0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(np.interp(t, [ft(B[5]), ft(I1)], [0.35, 0.08])) / SR)
stereo_bed(bp(noise(N), 200, 2500) * lap ** 2, bp(noise(N), 200, 2500) * np.roll(lap, 4000) ** 2, sea_e, 0.3, 0.4)
for k in range(55):
    p = (k / 55) ** 0.7; f0 = I0 + p * (I1 + 10 - I0) + rng.uniform(-4, 4)
    n = int(rng.uniform(.04, .12) * SR); s = np.arange(n) / SR
    place(ft(f0), hp(noise(n), 1500) * np.exp(-s * 60) + bp(noise(n), 200, 900) * np.exp(-s * 25) * .6, rng.uniform(.08, .2) * (0.5 + p), rng.uniform(-.8, .8), 0.8)
for k in range(4):
    f0 = I0 + 14 + k * 26; n = int(1.1 * SR); s = np.arange(n) / SR
    g = np.sin(2 * np.pi * np.cumsum(70 + 25 * np.sin(2 * np.pi * 1.3 * s) - 20 * s) / SR) * np.sin(np.pi * s / s[-1]) ** 2
    place(ft(f0), lp(g + bp(noise(n), 60, 300) * .5, 400), 0.22, (-1) ** k * .4, 0.7)
for k in range(3):  # the boat's hull creaking as the ice grips it
    n = int(.8 * SR); s = np.arange(n) / SR
    place(ft(I0 + 30 + k * 30), bp(noise(n), 150, 700) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * s))) * np.sin(np.pi * s / s[-1]), 0.1, -0.4, 0.6)

# cuts between space and ground: a short breath of air
for c in (B[3], B[6]):
    n = int(.5 * SR); u = np.linspace(0, 1, n)
    place(ft(c) - .25, bp(noise(n), 400, 4000) * np.sin(np.pi * u) ** 2, 0.25, 0, 0.5)

# final dive: rising rumble + air rush into the hole, cut by the flash that loops to frame 0
d = ft(END) - ft(END - 70); n = int(d * SR); u = np.linspace(0, 1, n)
w = noise(n); place(ft(END - 70), (lp(w, 300) * (1 - u) + lp(w, 2200) * u) * u ** 2.5 + bp(noise(n), 1000, 6000) * u ** 4 * .5, 0.6, 0, 0.6)
n = int(.4 * SR); u = np.linspace(0, 1, n)
place(ft(END) - .4, bp(noise(n), 90, 700) * u ** 2, 0.4, 0, 0.3)

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
VO_AT = [f for f, _ in T["vo"]]
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
print("LIGHT_OFF", LIGHT_OFF, "quietest 0.5s", round(min(rms), 1), "dB at", round(int(np.argmin(rms)) * .25, 2), "s; loudest", round(max(rms), 1))
