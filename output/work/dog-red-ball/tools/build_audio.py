#!/usr/bin/env python3
"""dog-red-ball: calm original music-box tune in G (approved style, see cat-no-sweet v2): an ORIGINAL 8-bit tune that follows the picture,
plus SFX. No voices. 120 BPM, 9 bars of 4/4 = 18 s. Every scene event lands on a musical stinger.
Timings from src/timing.json."""
import json, os
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = json.load(open(f"{ROOT}/src/timing.json"))
SR, FPS = 44100, T["fps"]
DUR = T["totalFrames"] / FPS
N = int(SR * DUR)
BEAT = 60 / T["bpm"]                       # 0.5 s
B = T["beats"]
rng = np.random.default_rng(8)
ft = lambda f: f / FPS
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
bp = lambda x, a, b: sosfilt(butter(2, [a, b], "bandpass", fs=SR, output="sos"), x)
mus, sfx = np.zeros((N, 2)), np.zeros((N, 2))

def put(buf, t, y, g=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(y))
    if i >= N or j <= max(0, i): return
    y = y[: j - i] * g
    buf[i:j, 0] += y * (1 - max(0, pan)); buf[i:j, 1] += y * (1 + min(0, pan))
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def adsr(n, a=.005, d=.08, s=.6, r=.06):
    e = np.ones(n) * s; ai, di, ri = int(a * SR), int(d * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, max(1, ai))[:len(e[:ai])]; e[ai:ai + di] = np.linspace(1, s, max(1, di))[:len(e[ai:ai + di])]
    if ri: e[-ri:] *= np.linspace(1, 0, ri)
    return e
def pulse(m, dur, duty=.25, vib=0.0, bend=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = hz(m) * (1 + vib * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t * 4)) * 2 ** (bend * t / dur / 12)
    ph = np.cumsum(f) / SR % 1
    return lp(np.where(ph < duty, 1.0, -1.0), 7000) * adsr(n)
def tri(m, dur):
    n = int(dur * SR); ph = np.cumsum(np.full(n, hz(m))) / SR % 1
    return (2 * np.abs(2 * ph - 1) - 1) * adsr(n, .003, .05, .85, .04)
def bell(m, dur=.6):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * hz(m) * t) + .35 * np.sin(2 * np.pi * hz(m) * 2.76 * t) * np.exp(-t * 9)) * np.exp(-t * 5)
def kick():
    n = int(.18 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(55 + 110 * np.exp(-t * 40)) / SR) * np.exp(-t * 18)
def hat(open_=False):
    n = int((.09 if open_ else .03) * SR); t = np.arange(n) / SR
    return hp(rng.uniform(-1, 1, n), 7000) * np.exp(-t * (30 if open_ else 120))
def snare():
    n = int(.14 * SR); t = np.arange(n) / SR
    return bp(rng.uniform(-1, 1, n), 1500, 7000) * np.exp(-t * 28) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .4

# ---------------- the tune (G major, new melody for this video) ----------------
CH = [(55, [67, 71, 74]), (52, [64, 67, 71]), (48, [60, 64, 67]), (50, [62, 66, 69]), (55, [67, 71, 74]),
      (47, [59, 62, 66]), (48, [60, 64, 67]), (50, [62, 66, 69]), (55, [67, 71, 74])]
E8 = BEAT / 2
def soft(m, dur):
    n = int((dur + .35) * SR); t = np.arange(n) / SR; ph = np.cumsum(np.full(n, hz(m))) / SR % 1
    y = (2 * np.abs(2 * ph - 1) - 1) * .7 + np.sin(2 * np.pi * hz(m) * 2 * t) * .18 * np.exp(-t * 6)
    return lp(y, 3500) * np.minimum(1, t / .02) * np.exp(-t * 2.2)
LEAD = [(0, 0, 74, 2), (0, 2, 71, 2), (0, 4, 67, 4), (1, 0, 71, 6), (2, 0, 72, 3), (2, 3, 76, 1), (2, 4, 79, 4), (3, 0, 78, 6),
        (4, 0, 79, 2), (4, 2, 83, 2), (4, 4, 81, 4), (5, 0, 78, 6), (6, 0, 76, 4), (6, 4, 72, 4), (7, 0, 74, 3), (7, 3, 76, 1), (7, 4, 78, 4),
        (8, 0, 79, 4), (8, 4, 74, 4)]
for bar, e, m, l in LEAD: put(mus, bar * 4 * BEAT + e * E8, soft(m, l * E8), .13, .1)
for bar, (root, chord) in enumerate(CH):
    t0 = bar * 4 * BEAT
    for k in (0, 2): put(mus, t0 + k * BEAT, tri(root - 12, BEAT * 1.7) * np.exp(-np.arange(int(BEAT * 1.7 * SR)) / SR * 1.5), .14)
    for k, idx in enumerate([0, 2, 1, 2]): put(mus, t0 + k * BEAT, bell(chord[idx] + 12, .9), .028, -.3 if k % 2 else .3)

# ---------------- stingers on the picture ----------------
S0, S1 = T["sweep"]
n = int(ft(S1 - S0) * SR); u = np.linspace(0, 1, n)                      # colours draining: a soft falling shimmer
put(sfx, ft(S0), hp(rng.uniform(-1, 1, n), 3000) * np.sin(np.pi * u) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * u)), .1)
for i, m in enumerate([79, 76, 72]): put(mus, ft(S0) + i * .4, bell(m, .7), .07)
for i, m in enumerate([67, 73]): put(mus, ft(S1) + .1 + i * .22, soft(m, .3), .1)   # puzzled "hm?"
for i in range(2): put(mus, ft(B[2]) + .15 + i * 1.0, bell(86 - i * 5, .8), .08)     # cone discs pop in
for i, m in enumerate([79, 83, 86]): put(mus, ft(T["catch"]) + i * .09, bell(m, .6), .08)  # caught it!

# ---------------- SFX ----------------
def burst(d, lo, hi, dec):
    n = int(d * SR); t = np.arange(n) / SR
    return bp(rng.uniform(-1, 1, n), lo, hi) * np.exp(-t * dec)
n = int(DUR * SR); t = np.arange(n) / SR
parkbed = np.interp(t, [0, ft(B[2]) - .1, ft(B[2]), ft(B[3]), ft(B[3]) + .1, DUR], [1, 1, 0, 0, 1, 1])
put(sfx, 0, (bp(rng.uniform(-1, 1, n), 300, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * .15 * t)) * .5 + lp(rng.uniform(-1, 1, n), 200) * .5) * parkbed, .16)   # breeze
put(sfx, 0, lp(rng.uniform(-1, 1, n), 250) * (1 - parkbed), .18)                                                             # quiet "inside the eye" tone
for k in range(34):                                                       # birds
    t0 = rng.uniform(0, DUR - .3)
    if parkbed[int(t0 * SR)] < .5: continue
    m = int(rng.uniform(.05, .1) * SR); s = np.arange(m) / SR
    fr = rng.uniform(2800, 4200) + rng.uniform(-800, 800) * s / s[-1] + 250 * np.sin(2 * np.pi * rng.uniform(25, 45) * s)
    put(sfx, t0, np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * s / s[-1]) ** 2, rng.uniform(.03, .06), rng.uniform(-.8, .8))
for f0 in list(range(72, 90, 5)) + list(range(B[1] + 6, B[2] - 6, 7)):    # sniffing
    put(sfx, ft(f0), burst(.09, 1500, 6000, 25) * np.sin(np.linspace(0, np.pi, int(.09 * SR))), .16, -.2)
for f0 in range(B[0] + 4, T["sweep"][0], 12):                             # happy panting before the colours go
    put(sfx, ft(f0), burst(.12, 600, 3000, 14), .06, -.2)
def woof():
    m = int(.16 * SR); s = np.arange(m) / SR
    return (np.sin(2 * np.pi * np.cumsum(420 - 260 * s / s[-1]) / SR) * .6 + bp(rng.uniform(-1, 1, m), 400, 2200) * .6) * np.sin(np.pi * s / s[-1]) ** .7
put(sfx, ft(T["throw"]) - .3, woof(), .2, .1)                             # excited woof before the throw
m = int(.35 * SR); u = np.linspace(0, 1, m); put(sfx, ft(T["throw"]), bp(rng.uniform(-1, 1, m), 600, 5000) * np.sin(np.pi * u) ** 2, .2, -.4)   # throw whoosh
for k in range(int((T["catch"] - T["throw"] - 6) / 4)):                   # paws on grass
    put(sfx, ft(T["throw"] + 6 + k * 4), burst(.05, 200, 1500, 50), .12, -.3 + k * .06)
m = int(.2 * SR); s = np.arange(m) / SR
put(sfx, ft(T["land"]), np.sin(2 * np.pi * np.cumsum(180 + 120 * np.exp(-s * 30)) / SR) * np.exp(-s * 18) + burst(.2, 300, 2000, 30)[:m] * .5, .3, .4)   # ball lands
put(sfx, ft(T["catch"]), burst(.08, 500, 3000, 40), .3, .3)               # chomp
put(sfx, ft(T["catch"]) + .5, woof(), .12, .2)
for f0 in range(B[4] + 6, B[5] - 26, 10): put(sfx, ft(f0), burst(.12, 600, 3000, 14), .06, -.2)   # proud panting
for c in B[1:5]:                                                          # slide transitions
    m = int(.4 * SR); u = np.linspace(0, 1, m); w = rng.uniform(-1, 1, m)
    put(sfx, ft(c) - .2, (lp(w, 800) * (1 - u) + bp(w, 1500, 6000) * u) * np.sin(np.pi * u) ** 2, .14)

# ---------------- mix ----------------
ir = rng.uniform(-1, 1, int(.9 * SR)) * np.exp(-np.arange(int(.9 * SR)) / SR * 5); ir /= np.sqrt((ir ** 2).sum())
musw = np.stack([fftconvolve(mus[:, k], ir)[:N] for k in range(2)], 1)
mix = (mus + musw * .3) * 0.55 + sfx
mix = np.stack([hp(mix[:, 0], 30), hp(mix[:, 1], 30)], 1)
mix /= np.abs(mix).max() + 1e-9
mix = np.tanh(mix * 1.1) / np.tanh(1.1) * .9
os.makedirs(f"{ROOT}/public", exist_ok=True)
wavfile.write(f"{ROOT}/public/mix_raw.wav", SR, (mix * 32767).astype(np.int16))
w = int(.5 * SR); rms = [20 * np.log10(np.sqrt((mix[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(mix) - w, w // 2)]
print("quietest 0.5s", round(min(rms), 1), "loudest", round(max(rms), 1))
