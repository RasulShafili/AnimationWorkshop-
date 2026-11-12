#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
C = dict(close=160, montage=340, dad=450, end=580); V = dict(n0=8, u0=166, n1=230, n2=272, n3=346, d0=456, n4=548)
m = Mix(C["end"], seed=4)
m.bed(lp(m.noise(m.N), 150), m.env([(0, 1), (C["end"], 1)]), .1)          # kitchen at night, fridge hum
m.bed(np.sin(2 * np.pi * 50 * m.t) * .2, m.env([(0, 1), (C["end"], 1)]), .03)
for k in range(12):                                                        # shuffles + chip clacks
    t0 = m.rng.uniform(0, ft(C["close"])); n = int(.05 * SR); s = np.arange(n) / SR
    m.place(t0, bp(m.noise(n), 2000, 7000) * np.exp(-s * 70), .08, m.rng.uniform(-.6, .6), .3)
# the uncle's heartbeat: we hear it speed up after he lies
per0, per1 = 60 / 78, 60 / 132; tt = ft(C["close"]) - 1
while tt < ft(C["montage"]):
    p = per0 + (per1 - per0) * min(1, max(0, (tt - ft(V["u0"])) / 1.0)); m.thump(tt, .45); tt += p
# card flips at the reveal
for k in range(5):
    n = int(.06 * SR); s = np.arange(n) / SR; m.place(ft(315) + k * .1, bp(m.noise(n), 1500, 6000) * np.exp(-s * 60), .2, -.2 + k * .1, .3)
m.hit(ft(318), .3)
# montage: chips sliding + a soft tick per win (wood click, not a beep)
for k in range(11):
    n = int(.08 * SR); s = np.arange(n) / SR; m.place(ft(C["montage"] + k * 8), bp(m.noise(n), 600, 3000) * np.exp(-s * 50) + np.sin(2 * np.pi * 900 * s) * np.exp(-s * 70) * .3, .18, .3, .3)
n = int(1.5 * SR); u = np.linspace(0, 1, n); m.place(ft(C["montage"] + 10), bp(m.noise(n), 1500, 6000) * np.sin(np.pi * u) * .5, .12, .4, .4)
for c in (C["close"], C["montage"], C["dad"]): m.whoosh(ft(c) - .3, g=.1)
m.score([[50, 53, 57], [55, 58, 62], [48, 52, 55], [52, 55, 59]], bar=2.5, gain=.05)   # playful minor jazz-ish loop
for k, key in enumerate(["n0", "n1", "n2", "n3", "n4"]): m.voice(f"{ROOT}/vo/c4_{k}.wav", V[key])
m.voice(f"{ROOT}/vo/u4_0.wav", V["u0"]); m.voice(f"{ROOT}/vo/d4_0.wav", V["d0"])
m.render(f"{ROOT}/public/ch4.wav")
