#!/usr/bin/env python3
"""Melody trial (user approved one video with music, 2026-11-10): an ORIGINAL 8-bit tune that follows the picture,
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

# ---------------- the tune ----------------
# chords per bar (2 s each): F  Dm  Bb  C  F  Am  Bb  C  F(→C, loops)
CH = [(53, [65, 69, 72]), (50, [62, 65, 69]), (46, [58, 62, 65]), (48, [60, 64, 67]), (53, [65, 69, 72]),
      (45, [57, 60, 64]), (46, [58, 62, 65]), (48, [60, 64, 67]), (53, [65, 69, 72])]
E8 = BEAT / 2
def soft(m, dur):
    """gentle music-box voice: triangle + a touch of octave sine, soft attack, long tail"""
    n = int((dur + .35) * SR); t = np.arange(n) / SR; ph = np.cumsum(np.full(n, hz(m))) / SR % 1
    y = (2 * np.abs(2 * ph - 1) - 1) * .7 + np.sin(2 * np.pi * hz(m) * 2 * t) * .18 * np.exp(-t * 6)
    return lp(y, 3500) * np.minimum(1, t / .02) * np.exp(-t * 2.2)
# calm lead: long notes, lots of space (bar, eighth, midi, eighths)
LEAD = [
    (0, 0, 72, 3), (0, 3, 74, 1), (0, 4, 72, 4),
    (1, 0, 69, 6),
    (2, 0, 70, 4), (2, 4, 69, 4),
    (3, 0, 67, 6),
    (4, 0, 72, 2), (4, 2, 77, 4), (4, 6, 76, 2),
    (5, 0, 72, 6),
    (6, 0, 74, 4), (6, 4, 70, 4),
    (7, 0, 72, 3), (7, 3, 74, 1), (7, 4, 76, 4),
    (8, 0, 77, 4), (8, 4, 72, 4),
]
for bar, e, m, l in LEAD:
    put(mus, bar * 4 * BEAT + e * E8, soft(m, l * E8), .13, .1)
for bar, (root, chord) in enumerate(CH):
    t0 = bar * 4 * BEAT
    for k in (0, 2):                                                                       # quiet bass on 1 and 3
        put(mus, t0 + k * BEAT, tri(root - 12, BEAT * 1.7) * np.exp(-np.arange(int(BEAT * 1.7 * SR)) / SR * 1.5), .14)
    for k, idx in enumerate([0, 1, 2, 1]):                                                 # music-box chord tones on the beat
        put(mus, t0 + k * BEAT, bell(chord[idx] + 12, .9), .028, -.3 if k % 2 else .3)

# ---------------- stingers on the picture ----------------
# the disgusted "bleh": two comic falling notes
for i, (m, d) in enumerate([(69, .22), (66, .45)]):
    put(mus, ft(T["bleh"]) + i * .26, soft(m, d) * 1.0, .12)
# sugar bouncing off: a springy boing
for at in T["bounce"]:
    n = int(.45 * SR); t = np.arange(n) / SR
    boing = np.sin(2 * np.pi * np.cumsum(300 + 500 * (1 - np.exp(-t * 9)) + 60 * np.sin(2 * np.pi * 14 * t)) / SR) * np.exp(-t * 6)
    put(sfx, ft(at), boing, .3, -.2)
# umami docking: bright two-bell chime
for i, at in enumerate(T["dock"]):
    put(mus, ft(at), bell(84 + i * 4, .7), .09); put(mus, ft(at) + .06, bell(91, .5), .04)
# fish reveal: a quick rising fanfare
for i, m in enumerate([72, 76, 79, 84]):
    put(mus, ft(T["fishCut"]) + i * .09, bell(m + 12, .6), .07)

# ---------------- SFX ----------------
def noise_burst(d, lo, hi, dec):
    n = int(d * SR); t = np.arange(n) / SR
    return bp(rng.uniform(-1, 1, n), lo, hi) * np.exp(-t * dec)
for k in range(3):                                   # sniff sniff sniff
    put(sfx, ft(T["sniff"]) + k * .16, noise_burst(.1, 1500, 6000, 25) * np.sin(np.linspace(0, np.pi, int(.1 * SR))), .22, .2)
put(sfx, ft(T["bleh"]) + .05, noise_burst(.18, 300, 2000, 12), .12)            # blep
n = int(DUR * SR); t = np.arange(n) / SR
room = lp(rng.uniform(-1, 1, n), 300) * 0.6 + np.sin(2 * np.pi * 50 * t) * .05   # fridge hum
kitchen = np.interp(t, [0, ft(B[1]) - .1, ft(B[1]), ft(T["fishCut"]), ft(T["fishCut"]) + .1, DUR], [1, 1, 0, 0, 1, 1])
put(sfx, 0, room * kitchen, .18)
wet = lp(rng.uniform(-1, 1, n), 600) * (0.6 + 0.4 * np.sin(2 * np.pi * .7 * t))      # inside the mouth
put(sfx, 0, wet * (1 - kitchen), .2)
for k in range(24):                                  # crickets outside the window
    t0 = rng.uniform(0, DUR - .3)
    if kitchen[int(t0 * SR)] < .5: continue
    for j in range(3):
        m = int(.02 * SR); s = np.arange(m) / SR
        put(sfx, t0 + j * .05, np.sin(2 * np.pi * 4700 * s) * np.sin(np.pi * s / s[-1]), .02, .7)
for f in range(B[3], B[4], 1):                       # licks: soft wet plops on each lick peak
    if int((f - B[3]) * 0.35 / np.pi) != int((f - 1 - B[3]) * 0.35 / np.pi) and (f - B[3]) % 18 < 9:
        n2 = int(.07 * SR); s = np.arange(n2) / SR
        put(sfx, ft(f), np.sin(2 * np.pi * np.cumsum(500 + 700 * s / s[-1]) / SR) * np.exp(-s * 40), .12, .2)
for c in (B[1], B[2], T["fishCut"], B[3], B[4]):     # wipes
    n2 = int(.4 * SR); u = np.linspace(0, 1, n2)
    put(sfx, ft(c) - .2, bp(rng.uniform(-1, 1, n2), 800, 6000) * np.sin(np.pi * u) ** 2, .14)
n2 = int(.5 * SR); s = np.arange(n2) / SR
put(sfx, ft(B[4]) + 0.8, np.sin(2 * np.pi * np.cumsum(1200 + 600 * np.sin(np.pi * s / s[-1])) / SR) * np.exp(-s * 6), .06, .4)   # wink twinkle

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
