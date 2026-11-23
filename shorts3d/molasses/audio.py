#!/usr/bin/env python3
"""Audio for "The Tank Everyone Laughed At": VO, an original plucked motif (light while they mock, darker as the tank
groans, cut dead at the burst, one sad chord after), synthesized SFX on every beat, layered Chatterbox laughs, −14 LUFS.
  python3 audio.py  →  out/audio.wav"""
import sys, json, os, numpy as np
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools")
from audio_lib import Mix, SR, hz, lp, bp, hp
from scipy.io import wavfile
D = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f"{D}/timeline.json")); W = json.load(open(f"{D}/words.json")); SH = json.load(open(f"{D}/out/shots.json"))
LN = {l["id"]: l for l in TL["lines"]}; END = TL["end"]
def wt(word, n=0): return [w[0] for w in W if w[2].lower().strip(".,!?") == word.lower()][n]
s = lambda k: SH[k]["t0"]
m = Mix(int(END * 30) + 30, seed=6); N = m.N; t = m.t
def load(path):
    sr, y = wavfile.read(path); y = y.astype(float)
    if y.ndim > 1: y = y.mean(1)
    y /= (np.abs(y).max() + 1e-9); return np.interp(np.arange(int(len(y) * SR / sr)) * sr / SR, np.arange(len(y)), y)
def env_seg(a, b, fade=0.4): return np.clip(np.minimum((t - a) / fade, (b - t) / fade), 0, 1)
m.voice(f"{D}/vo/vo_full.wav", 0, 1.0)
# ---------------------------------------------------------------- music (original motif, G minor-ish, 104 bpm)
def pluck(f, d=0.5):
    n = int(d * SR); x = np.arange(n) / SR; y = np.zeros(n)
    for k, a in ((1, 1), (2, .45), (3, .22), (4, .1)): y += a * np.sin(2 * np.pi * f * k * x) * np.exp(-x * (7 + 3 * k))
    return y * np.minimum(1, x / 0.004)
def pad(chord, a, b, g):
    n = int((b - a) * SR); x = np.arange(n) / SR; y = np.zeros(n)
    for mm in chord: y += np.sin(2 * np.pi * hz(mm) * x + np.sin(2 * np.pi * 5 * x) * 0.15) + 0.3 * np.sin(4 * np.pi * hz(mm) * x)
    m._mus(a, lp(y, 1200) * np.minimum(1, x / 0.8) * np.minimum(1, (b - a - x) / 0.8), g)
beat = 60 / 104
MOT = [67, 70, 74, 70, 69, 72, 75, 72, 67, 70, 74, 79, 77, 74, 72, 69]
CH = [[55, 62, 67], [51, 58, 63], [53, 60, 65], [50, 57, 62]]
def section(a, b, g=0.045, dark=False, octave=0):
    k = 0; tt = a
    while tt < b - 0.1:
        if k % 2 == 0 or not dark: m._mus(tt, pluck(hz(MOT[k % 16] + octave - (12 if dark else 0)), 0.45), g, 0.25 * (-1) ** k)
        if k % 2 == 0: m._mus(tt, pluck(hz(CH[(k // 8) % 4][0] - 12), 0.6), g * 0.9)
        tt += beat / 2; k += 1
    i = 0; tt = a
    while tt < b - 0.2: pad([c - (12 if dark else 0) for c in CH[i % 4]], tt, min(b, tt + beat * 4), g * (0.5 if not dark else 0.8)); tt += beat * 4; i += 1
f_split = wt("split") - 0.05
section(s("S02"), LN["n08"]["t0"] - 0.2, 0.045)                       # the street mocks him
section(LN["n08"]["t0"], LN["n11"]["t0"] - 0.3, 0.05, dark=True)        # the warm day, the groaning
pad([43, 50, 55, 58], LN["n12"]["t0"] + 1.2, LN["n13"]["t0"] + 0.2, 0.05)   # after: one sad chord
section(LN["n13"]["t0"], END - 0.3, 0.04, dark=True, octave=5)          # the explanation
# ---------------------------------------------------------------- sfx atoms
def groan(t0, d=1.8, g=0.5, f=55):
    n = int(d * SR); x = np.arange(n) / SR
    ph = np.cumsum(f * (1 + 0.18 * np.sin(2 * np.pi * 0.9 * x) + 0.08 * np.sin(2 * np.pi * 3.1 * x))) / SR
    y = (2 * (ph % 1) - 1) * 0.6 + np.sin(2 * np.pi * ph * 2.03) * 0.4
    y = bp(y, 70, 700) * np.sin(np.pi * np.minimum(1, x / d)) ** 0.7 + bp(m.noise(n), 200, 900) * 0.15 * np.sin(np.pi * x / d)
    m.place(t0, y, g, 0, .6)
def drip(t0, g=0.12):
    n = int(0.12 * SR); x = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(500 + 900 * np.exp(-x * 40)) / SR) * np.exp(-x * 35); m.place(t0, y, g, 0.2, .3)
def swish(t0, d=0.35, g=0.12): m.whoosh(t0, d, g, 900, 6000)
def pump(a, b, g=0.08):
    tt = a
    while tt < b: m.thump(tt, g); tt += 0.55
def bang(t0, g=0.5):
    n = int(0.3 * SR); x = np.arange(n) / SR
    y = bp(m.noise(n), 600, 7000) * np.exp(-x * 30) * 1.2 + np.sin(2 * np.pi * 180 * x) * np.exp(-x * 25); m.place(t0, y, g, np.random.uniform(-.4, .4), .5)
def boom(t0, g=1.0, d=3.5):
    n = int(d * SR); x = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(32 + 45 * np.exp(-x * 4)) / SR) * np.exp(-x * 1.3) * 1.4 + lp(m.noise(n), 900) * np.exp(-x * 1.6) * 2
    m.place(t0, y, g, 0, .7)
def roar(a, b, g=0.5):
    n = int((b - a) * SR); x = np.arange(n) / SR
    y = lp(m.noise(n), 500) * 2.5 + bp(m.noise(n), 600, 2500) * 0.6
    y *= np.minimum(1, x / 0.3) * np.minimum(1, (b - a - x) / 1.2); m.place(a, y, g, 0, .7)
def crash(t0, g=0.5):
    n = int(1.2 * SR); x = np.arange(n) / SR
    y = bp(m.noise(n), 300, 5000) * np.exp(-x * 4) * 1.4 + lp(m.noise(n), 200) * np.exp(-x * 3) * 2; m.place(t0, y, g, -0.3, .6)
def screech(t0, d=1.4, g=0.25):
    n = int(d * SR); x = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(900 - 400 * x / d + 40 * np.sin(2 * np.pi * 7 * x)) / SR) * np.sin(np.pi * x / d); y = y + bp(m.noise(n), 2000, 6000) * 0.2 * np.sin(np.pi * x / d)
    m.place(t0, y, g, 0.3, .5)
def laughs(a, b, g=0.33, k=(0, 1, 2, 3, 4, 5)):
    for j, i in enumerate(k):
        p = f"{D}/vo/laugh{i}.wav"
        if not os.path.exists(p): continue
        y = load(p); tt = a + 0.12 * j; y = y[:int(max(0.3, b - tt) * SR)]; y *= np.minimum(1, (len(y) - np.arange(len(y))) / (0.25 * SR))
        m.place(tt, y, g * (0.9 if j % 2 else 0.7), 0.5 * ((-1) ** j) * (0.3 + 0.1 * j), .4)
def wind(a, b, g):
    x = lp(m.noise(N), 400) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t)); m.bed(x, env_seg(a, b, 1.0), g, .5)
def city(a, b, g):
    x = bp(m.noise(N), 200, 1500); m.bed(x, env_seg(a, b, 0.6), g, .4)
def steps(a, b, every=0.26, g=0.22):
    tt = a
    while tt < b: m.step(tt, g); tt += every
# ---------------------------------------------------------------- beats
wind(0, s("S02"), 0.05); groan(0.25, 2.2, 0.55, 48)                                      # night: the tank groans
city(s("S02"), LN["n08"]["t0"], 0.012); wind(s("S02"), LN["n11"]["t0"], 0.025)
laughs(LN["n02"]["t0"] + 0.1, LN["n03"]["t0"] + 0.3, 0.33)
m.whoosh(s("S04"), 1.4, 0.08, 200, 2500)
pump(s("S05"), s("S06"), 0.1)
for k in range(5): drip(s("S06") + 0.2 + k * 0.42, 0.13)
for k in range(5): swish(s("S07") + 0.3 + k * 0.52, 0.3, 0.1)
for k in range(7): drip(s("S08") + 0.15 + k * 0.5, 0.11)
m.chime(s("S09") + 0.3, 70, 0.03)
laughs(LN["n07"]["t0"] - 0.05, LN["b01"]["t0"] + 0.4, 0.42)
pump(s("S13"), s("S14"), 0.12)
for k in range(4): drip(s("S14") + 0.3 + k * 0.62, 0.09)
groan(s("S15") + 0.05, 1.6, 0.75, 44); groan(s("S15") + 0.9, 1.2, 0.4, 61)
steps(s("S16") + 0.05, s("S17") - 0.05)
laughs(LN["n10"]["t0"] + 0.4, LN["n11"]["t0"] - 0.35, 0.28, k=(0, 1, 3))
# the disaster
r0 = wt("rivets") + 0.05
for k in range(8): bang(r0 + k * 0.13 + (k % 3) * 0.04, 0.45)
groan(s("S19"), 1.0, 0.5, 40)
boom(f_split, 1.0); roar(f_split + 0.1, LN["n12"]["t1"] + 0.3, 0.55)
crash(SH["S22"]["t0"] + 4 / 24, 0.6); screech(SH["S22"]["t0"] + 10 / 24, 1.4, 0.22)
wind(s("S23"), s("S24"), 0.06)
m.whoosh(s("S24") + 0.1, 1.8, 0.06, 150, 1500); m.thump(wt("tested") + 0.05, 0.3)                 # the sign
groan(s("S25") + 0.1, 1.6, 0.35, 50)
wind(s("S26"), s("S27"), 0.08)
for k in range(10): m.chime(s("S26") + 0.3 + k * 0.45, 100 + (k % 3), 0.008)                          # frost glints
for k in range(3): swish(s("S27") + 0.35 + k * 0.45, 0.32, 0.1)
groan(END - 1.6, 1.6, 0.4, 48)                                                                       # loops into the night groan
m.render(f"{D}/out/audio.wav")
