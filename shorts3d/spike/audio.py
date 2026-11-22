#!/usr/bin/env python3
"""Audio for the spike Short: VO (vo/vo_full.wav), original storytelling music (pizzicato-like plucks + low strings
pad, darker in the storm, stops dead on the boom), synthesized SFX on the story beats, crowd laughs (Chatterbox
takes layered). −14 LUFS via audio_lib.Mix.render.   python3 audio.py  →  out/audio.wav"""
import sys, json, os, numpy as np
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools")
from audio_lib import Mix, SR, hz, lp, bp, hp
from scipy.io import wavfile
D = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(f"{D}/timeline.json")); W = json.load(open(f"{D}/words.json")); SH = json.load(open(f"{D}/out/shots.json"))
LN = {l["id"]: l for l in TL["lines"]}; END = TL["end"]
def wt(word, n=0): return [w[0] for w in W if w[2] == word][n]
m = Mix(int(END * 30) + 30, seed=4); N = m.N; t = m.t
def load(path, sr_to=SR):
    sr, y = wavfile.read(path); y = y.astype(float)
    if y.ndim > 1: y = y.mean(1)
    y /= (np.abs(y).max() + 1e-9); return np.interp(np.arange(int(len(y) * sr_to / sr)) * sr / sr_to, np.arange(len(y)), y)
def env_seg(a, b, fade=0.4):
    return np.clip(np.minimum((t - a) / fade, (b - t) / fade), 0, 1)
# ---------------------------------------------------------------- voice
m.voice(f"{D}/vo/vo_full.wav", 0, 1.0)
# ---------------------------------------------------------------- music (original): plucked motif in D minor, 112 bpm
def pluck(f, d=0.5, g=1.0):
    n = int(d * SR); s = np.arange(n) / SR; y = np.zeros(n)
    for k, a in ((1, 1), (2, .45), (3, .22), (4, .1)): y += a * np.sin(2 * np.pi * f * k * s) * np.exp(-s * (7 + 3 * k))
    return y * np.minimum(1, s / 0.004) * g
def pad(chord, a, b, g):
    n = int((b - a) * SR); s = np.arange(n) / SR; y = np.zeros(n)
    for mm in chord: y += np.sin(2 * np.pi * hz(mm) * s + np.sin(2 * np.pi * 5 * s) * 0.15) + 0.3 * np.sin(4 * np.pi * hz(mm) * s)
    y = lp(y, 1200) * np.minimum(1, s / 0.8) * np.minimum(1, (b - a - s) / 0.8); m._mus(a, y, g)
beat = 60 / 112
MOT = [62, 65, 69, 65, 64, 67, 70, 67, 62, 65, 69, 72, 70, 69, 67, 64]          # our own little motif
CH = [[50, 57, 62], [46, 53, 58], [48, 55, 60], [45, 52, 57]]
def section(a, b, g=0.05, motif=True, dark=False, octave=0):
    k = 0; tt = a
    while tt < b - 0.1:
        if motif and (k % 2 == 0 or not dark): m._mus(tt, pluck(hz(MOT[k % 16] + octave - (12 if dark else 0)), 0.45), g, 0.25 * (-1) ** k)
        if k % 2 == 0: m._mus(tt, pluck(hz(CH[(k // 8) % 4][0] - 12), 0.6), g * 0.9)
        tt += beat / 2; k += 1
    i = 0; tt = a
    while tt < b - 0.2:
        pad([c - (12 if dark else 0) for c in CH[i % 4]], tt, min(b, tt + beat * 4), g * (0.5 if not dark else 0.8)); tt += beat * 4; i += 1
section(0.2, LN["n06"]["t0"], 0.045)                                   # playful mocking town
section(LN["n06"]["t0"], LN["n08"]["t0"] - 0.2, 0.04, dark=False, octave=-5)   # weeks later, greyer
section(LN["n08"]["t0"], LN["n11"]["t0"] - 0.3, 0.05, dark=True)        # storm night
pad([50, 57, 62, 65], LN["n11"]["t0"] - 0.1, LN["n12"]["t0"] + 0.3, 0.05)  # morning: one sad chord
section(LN["n12"]["t0"], wt("found") + 0.15, 0.045, dark=True, octave=0)   # explanation, tension
section(wt("found") + 1.4, wt("church", 2) - 0.1, 0.04)                     # the spike's road: lighter
section(wt("church", 2) - 0.1, wt("church", 2) + 1.6, 0.05, dark=True)
# ---------------------------------------------------------------- sfx atoms
def clink(t0, g=0.25, f=2400):
    n = int(0.35 * SR); s = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * r * s) * np.exp(-s * d) for r, a, d in ((1, 1, 18), (2.76, .5, 25), (5.4, .25, 35))) + bp(m.noise(n), 2000, 8000) * np.exp(-s * 80) * .4
    m.place(t0, y, g, -0.2, .3)
def thunder(t0, g=0.8, crack=True, d=3.5):
    n = int(d * SR); s = np.arange(n) / SR
    rum = lp(m.noise(n), 160) * (np.exp(-s * 1.1) * (1 + 0.6 * np.sin(2 * np.pi * 1.7 * s))) * 3
    y = rum
    if crack: y = y + bp(m.noise(n), 900, 9000) * np.exp(-s * 9) * 0.9 + lp(m.noise(n), 600) * np.exp(-s * 4) * 1.5
    m.place(t0, y, g, 0, .6)
def zap(a, b, g=0.25):
    n = int((b - a) * SR); s = np.arange(n) / SR
    y = (np.sign(np.sin(2 * np.pi * (120 + 40 * np.sin(s * 37)) * s)) * 0.3 + bp(m.noise(n), 2000, 7000)) * np.minimum(1, s / 0.02) * np.minimum(1, (b - a - s) / 0.05)
    m.place(a, y, g, 0, .3)
def boom(t0, g=1.0, d=4.0):
    n = int(d * SR); s = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(30 + 50 * np.exp(-s * 4)) / SR) * np.exp(-s * 1.3) * 1.4 + lp(m.noise(n), 900) * np.exp(-s * 1.8) * 2 + bp(m.noise(n), 1500, 8000) * np.exp(-s * 6)
    m.place(t0, y, g, 0, .7)
def bell(t0, f=196, g=0.25, d=3.0, muff=False):
    n = int(d * SR); s = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * r * s) * np.exp(-s * dd) for r, a, dd in ((0.5, .6, 1.2), (1, 1, 1.5), (1.19, .5, 2.2), (1.5, .35, 2.8), (2.0, .4, 3.5), (2.74, .2, 5), (3.76, .1, 7)))
    y = y * np.minimum(1, s / 0.003)
    if muff: y = lp(y, 900)
    m.place(t0, y, g, 0.15, .7)
def laughs(a, b, g=0.35, k=(0, 1, 2, 3, 4, 5)):
    for j, i in enumerate(k):
        p = f"{D}/vo/laugh{i}.wav"
        if not os.path.exists(p): continue
        y = load(p); tt = a + 0.12 * j
        y = y[:int(max(0.3, b - tt) * SR)]; y *= np.minimum(1, (len(y) - np.arange(len(y))) / (0.25 * SR))
        m.place(tt, y, g * (0.9 if j % 2 else 0.7), 0.5 * ((-1) ** j) * (0.3 + 0.1 * j), .4)
def rain(a, b, g):
    x = hp(bp(m.noise(N), 1500, 9000), 1200); x2 = hp(bp(m.noise(N), 1500, 9000), 1200)
    m.bed(x, env_seg(a, b, 0.6), g, .3, x2)
def wind(a, b, g):
    x = lp(m.noise(N), 400) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t)); m.bed(x, env_seg(a, b, 1.0), g, .5)
def steps_splash(a, b, every=0.27, g=0.25):
    tt = a
    while tt < b: m.step(tt, g); n = int(0.12 * SR); m.place(tt, bp(m.noise(n), 1200, 6000) * np.exp(-np.arange(n) / SR * 30), g * 0.6); tt += every
# ---------------------------------------------------------------- beats
s = lambda k: SH[k]["t0"]
# day town ambience: birds-ish chirps + murmur
wind(0, LN["n06"]["t0"], 0.03)
for i in range(18):
    tt = 0.5 + i * 1.2 + (i % 3) * 0.3
    if tt < LN["n06"]["t0"]: m.chime(tt, 96 + (i % 4), 0.015)
tt = 0.45
while tt < s("S02"): clink(tt, 0.22); tt += 2 * np.pi / 13            # hammer on the spike
laughs(LN["n02"]["t0"] + 0.1, LN["n03"]["t0"] + 0.4, 0.33)
m.whoosh(s("S04"), 1.2, 0.08, 200, 2500)
for k in range(3): bell(s("S05") + 0.1 + k * 1.3, 196, 0.22)
# ringing room: thunder + muffled bells
thunder(wt("thunder") + 0.05, 0.55)
tt = s("S06") + 0.2; k = 0
while tt < s("S07"): bell(tt, 196 if k % 2 == 0 else 233, 0.16, 2.5, muff=True); tt += 0.75; k += 1
# kids' rocks
for j in range(2):
    for k in range(2):
        t0 = s("S08") + 0.35 + j * 0.35 + k * 0.9
        if t0 < s("S09") - 0.2: m.whoosh(t0, 0.4, 0.06, 800, 5000); clink(t0 + 14 / 24, 0.25, 3100)
# storm day
wind(LN["n06"]["t0"], LN["n08"]["t0"], 0.06); rain(LN["n06"]["t0"], LN["n08"]["t0"], 0.012)
thunder(wt("hit", 0) + 0.08, 0.95); zap(wt("hit", 0) + 0.15, wt("hit", 0) + 0.85, 0.22); m.thump(wt("hit", 0) + 0.8, 0.35)
thunder(LN["n06"]["t0"] + 0.3, 0.3, crack=False)
laughs(LN["n07"]["t0"], LN["t01"]["t0"] + 0.5, 0.42)
# storm night
rain(LN["n08"]["t0"] - 0.25, LN["n11"]["t0"] - 0.35, 0.035); wind(LN["n08"]["t0"] - 0.25, LN["n11"]["t0"] - 0.35, 0.09)
thunder(33.5, 0.45, crack=False); thunder(34.6, 0.5, crack=False)
tt = wt("bells", 1) - 0.1; k = 0
while tt < s("S17") + 0.6: bell(tt, 196 if k % 2 == 0 else 233, 0.26 if tt < s("S16") + 0.8 else 0.12, 2.5); tt += 0.5; k += 1
thunder(wt("sky") + 0.06, 1.0, d=4.5)
steps_splash(s("S17") + 0.1, s("S18") - 0.1)
tt = s("S18");
while tt < LN["n11"]["t0"] - 0.3: bell(tt, 196 if int(tt * 2) % 2 == 0 else 233, 0.07, 2.0, muff=True); tt += 0.5
laughs(LN["n10"]["t0"] - 0.05, LN["n11"]["t0"] - 0.3, 0.3, k=(0, 1, 3))
# morning after: wind + crackle, nothing else
wind(LN["n11"]["t0"] - 0.3, LN["n12"]["t0"] + 0.5, 0.05)
for i in range(30):
    tt = LN["n11"]["t0"] + i * 0.09 + (i % 5) * 0.03
    n = int(0.02 * SR); m.place(tt, bp(m.noise(n), 2000, 7000) * np.exp(-np.arange(n) / SR * 200), 0.05)
# explanation
m.whoosh(s("S21") + 0.1, 2.5, 0.06, 150, 1500)
thunder(wt("hit", 1) + 0.05, 0.9); zap(wt("hit", 1) + 0.12, wt("found") + 0.1, 0.18); boom(wt("found") + 0.15, 1.0)
thunder(wt("lightning", 3) + 0.08, 0.8); zap(wt("lightning", 3) + 0.15, wt("ground.") + 0.1, 0.16); m.thump(wt("ground.") + 0.1, 0.25)
zap(s("S24") + 0.1, s("S24") + 0.8, 0.2); boom(s("S24") + 0.8, 1.2, 3.0)
m.render(f"{D}/out/audio.wav")
