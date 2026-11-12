#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
C = dict(toast=100, cls=190, tell=400, mia=450, cut=560, end=720); V = dict(n0=6, n1=104, n2=196, t0=306, n3=404, m0=456, n4=566)
m = Mix(C["end"], seed=3)
outside = m.env([(0, 1), (C["toast"] - 2, 1), (C["toast"], 0), (C["end"], 0)])
m.bed(lp(m.noise(m.N), 300), outside, .1)
# bus engine coming round the corner (low rumble + diesel buzz, getting louder), brakes hiss
eng = (np.sin(2 * np.pi * 48 * m.t) * .5 + np.sign(np.sin(2 * np.pi * 96 * m.t)) * .2) * m.env([(0, .2), (60, .6), (95, 1), (C["toast"], 0)])
m.bed(lp(eng, 600), outside, .25, .3)
n = int(.8 * SR); s = np.arange(n) / SR; m.place(ft(90), hp(m.noise(n), 3000) * np.exp(-s * 4), .15, -.4, .4)
# kitchen: toaster tick, then POP
kitchen = m.env([(0, 0), (C["toast"], 0), (C["toast"] + 1, 1), (C["cls"] - 1, 1), (C["cls"], 0), (C["end"], 0)])
for k in range(30): n = int(.01 * SR); m.place(ft(C["toast"]) + k * .08, hp(m.noise(n), 2000) * np.exp(-np.arange(n) / SR * 400), .04 * (k < 26), .2, .1)
n = int(.25 * SR); s = np.arange(n) / SR; m.place(ft(C["toast"] + 66), bp(m.noise(n), 800, 5000) * np.exp(-s * 30) + np.sin(2 * np.pi * 300 * s) * np.exp(-s * 40) * .5, .4, .2, .3)
m.chime(ft(C["toast"] + 70), 88, .06)
# classroom room tone, pencil scratches, the whispered teachers (muffled), the class reacting
cls = m.env([(0, 0), (C["cls"], 0), (C["cls"] + 2, 1), (C["mia"] - 2, 1), (C["mia"], 0), (C["end"], 0)])
m.bed(bp(m.noise(m.N), 200, 2000), cls, .05, .3)
for k in range(40): n = int(.06 * SR); s = np.arange(n) / SR; m.place(m.rng.uniform(ft(C["cls"]), ft(C["tell"])), bp(m.noise(n), 3000, 8000) * np.sin(np.pi * s / s[-1]), .02, m.rng.uniform(-.6, .6), .3)
n = int(1.2 * SR); u = np.linspace(0, 1, n); m.place(ft(C["tell"] + 18), bp(m.noise(n), 300, 3000) * np.sin(np.pi * u) * .8, .25, 0, .5)   # 'whaaat' murmur
# hallway: chatter + locker slams
hall = m.env([(0, 0), (C["mia"], 0), (C["mia"] + 2, 1), (C["cut"] - 2, 1), (C["cut"], 0), (C["end"], 0)])
m.bed(bp(m.noise(m.N), 300, 2500) * (0.6 + 0.4 * np.sin(2 * np.pi * .7 * m.t)), hall, .07, .5)
for t0 in (ft(C["mia"] + 12), ft(C["mia"] + 70)): n = int(.4 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 200, 3000) * np.exp(-s * 18) + np.sin(2 * np.pi * 140 * s) * np.exp(-s * 20) * .5, .15, .6, .6)
# phone buzzing two floors down
for k in range(5):
    n = int(.35 * SR); s = np.arange(n) / SR; m.place(ft(C["cut"] + 62) + k * .7, np.sign(np.sin(2 * np.pi * 150 * s)) * np.sin(np.pi * s / s[-1]) * .5, .12, .3, .4)
for c in (C["toast"], C["cls"], C["mia"], C["cut"]): m.whoosh(ft(c) - .3)
m.score([[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]], bar=3.0, gain=.05)
for k, key in enumerate(["n0", "n1", "n2", "n3", "n4"]): m.voice(f"{ROOT}/vo/c3_{k}.wav", V[key])
m.voice(f"{ROOT}/vo/t3_0.wav", V["t0"], .7); m.voice(f"{ROOT}/vo/m3_0.wav", V["m0"])
m.render(f"{ROOT}/public/ch3.wav")
