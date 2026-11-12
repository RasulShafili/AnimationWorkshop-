#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
C = dict(field=190, decide=580, shout=840, dig=1120, hosp=1290, end=1550)
V = dict(n0=10, n1=196, n2=346, n3=512, n4=586, n5=776, h0=846, n6=966, m0=1200, n7=1258, n8=1296, n9=1484)
m = Mix(C["end"], seed=7)
# dawn: birds + soft wind; the crack; the avalanche roar
dawn = m.env([(0, 1), (60, 1), (70, 0), (C["end"], 0)])
for k in range(8):
    t0 = m.rng.uniform(0, 2); n = int(.1 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * np.cumsum(3200 + 900 * np.sin(np.pi * s / s[-1])) / SR) * np.sin(np.pi * s / s[-1]) ** 2, .03, m.rng.uniform(-.8, .8), .5)
m.bed(bp(m.noise(m.N), 200, 1500), m.env([(0, .6), (C["end"], .6)]), .06, .5)
n = int(1.5 * SR); s = np.arange(n) / SR; m.place(ft(55), hp(m.noise(n), 800) * np.exp(-s * 6) + np.sin(2 * np.pi * 50 * s) * np.exp(-s * 2), .7, 0, .7)
roar = m.env([(0, 0), (70, 0), (100, 1), (170, 1), (200, 0), (C["end"], 0)])
m.bed(lp(m.noise(m.N), 300) * 1.5 + bp(m.noise(m.N), 300, 2000) * .4, roar, .5, .4)
# helicopter: thwop-thwop rotor + turbine whine, dominating until it lands and spins down
heli = m.env([(0, 0), (C["field"], 1), (C["shout"] + 40, 1), (C["shout"] + 120, .5), (C["shout"] + 150, 0), (C["end"], 0)])
rate = 6.5 * m.env([(0, 1), (C["shout"] + 60, 1), (C["shout"] + 150, .2), (C["end"], .2)])
ph = np.cumsum(rate) / SR; thwop = (np.maximum(0, np.sin(2 * np.pi * ph)) ** 6) * lp(m.noise(m.N), 400) * 3
whine = np.sin(2 * np.pi * np.cumsum(1800 * (0.5 + 0.5 * rate / 6.5)) / SR) * .08
m.bed(thwop + whine + lp(m.noise(m.N), 150) * .6, heli * m.env([(0, 1), (C["decide"], .55), (C["shout"], .75), (C["end"], .75)]), .45, .3)
# tension pulse during the search (low, no beeps)
tt = ft(V["n3"])
while tt < ft(C["shout"]): m.thump(tt, .25, 36); tt += .7
# the silence opens: rescuers' hearts (quiet, many) + one slow heart under the snow (louder)
op = ft(C["shout"] + 120)
for i in range(6):
    tt = op + i * .13
    while tt < ft(C["dig"]): m.thump(tt, .08, 48 + i * 3); tt += 60 / (95 + i * 6)
tt = op + .5
while tt < ft(C["dig"] + 60): m.thump(tt, .5, 34); tt += 1.6
m.bed(bp(m.noise(m.N), 200, 1200), m.env([(0, 0), (C["shout"] + 120, 0), (C["shout"] + 140, .7), (C["dig"], .7), (C["dig"] + 10, 0), (C["end"], 0)]), .05, .6)
# digging + joy
for k in range(20):
    n = int(.22 * SR); s = np.arange(n) / SR; m.place(ft(C["dig"]) + k * .2, bp(m.noise(n), 500, 4000) * np.exp(-s * 14), .14, m.rng.uniform(-.4, .4), .4)
n = int(2.5 * SR); u = np.linspace(0, 1, n); m.place(ft(V["m0"] + 50), bp(m.noise(n), 300, 3000) * np.sin(np.pi * u) ** .7, .18, 0, .6)
# hospital: muffled room (low-passed tone), his ears ringing faintly
hosp = m.env([(0, 0), (C["hosp"], 0), (C["hosp"] + 5, 1), (C["end"], 1)])
m.bed(lp(m.noise(m.N), 250), hosp, .08)
n = int(4 * SR); s = np.arange(n) / SR; m.place(ft(C["hosp"]), np.sin(2 * np.pi * 3800 * s) * np.exp(-s * .6), .03, 0, .2)
m.hit(ft(C["shout"]), .3)
for c in (C["field"], C["decide"], C["dig"], C["hosp"]): m.whoosh(ft(c) - .3, g=.1)
# score: tense minor under the search, a hopeful major swell for the rescue + hospital
m.score([[57, 60, 64], [53, 57, 60], [52, 55, 59], [52, 56, 59]], bar=3.0, gain=.05, start=ft(C["field"]), end=ft(C["shout"]))
m.score([[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]], bar=3.0, gain=.07, start=ft(C["dig"] + 40))
for k in range(10): m.voice(f"{ROOT}/vo/c7_{k}.wav", V[f"n{k}"])
m.voice(f"{ROOT}/vo/h7_0.wav", V["h0"]); m.voice(f"{ROOT}/vo/m7_0.wav", V["m0"])
m.render(f"{ROOT}/public/ch7.wav")
