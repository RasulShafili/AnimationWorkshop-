#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
C = dict(street=350, talk=500, cabin=600, end=830); V = dict(n0=6, n1=44, n2=178, n3=356, m0=506, h0=545, n4=612)
m = Mix(C["end"], seed=6)
night = m.env([(0, 1), (C["street"] - 2, 1), (C["street"], 0), (C["end"], 0)])
m.bed(hp(m.noise(m.N), 3000), night, .1, .2, hp(m.noise(m.N), 3000))                 # the hiss
body = m.env([(0, 0), (V["n2"], 0), (V["n2"] + 15, 1), (C["street"] - 2, 1), (C["street"], 0), (C["end"], 0)])
m.bed(lp(m.noise(m.N), 180) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.2 * m.t)), body, .3)  # blood rushing
tt = ft(30)
while tt < ft(C["street"]): m.thump(tt, .55 if tt > ft(V["n2"]) else .3, 40); tt += .95
for k in range(5):                                                                     # joint creaks
    n = int(.25 * SR); s = np.arange(n) / SR; m.place(ft(V["n2"]) + .8 + k * 1.1, bp(np.sign(np.sin(2 * np.pi * 30 * s)) * m.noise(n) * .3, 300, 2000) * np.sin(np.pi * s / s[-1]), .15, m.rng.uniform(-.5, .5), .3)
# street: traffic bed, then the motorbike roar (painfully loud, then ring)
street = m.env([(0, 0), (C["street"], 0), (C["street"] + 2, 1), (C["cabin"] - 2, 1), (C["cabin"], 0), (C["end"], 0)])
m.bed(lp(m.noise(m.N), 400), street, .12)
d = 2.2; n = int(d * SR); s = np.arange(n) / SR; u = s / d
fq = 90 + 40 * np.sin(np.pi * u); bike = (np.sign(np.sin(2 * np.pi * np.cumsum(fq) / SR)) * .6 + bp(m.noise(n), 200, 3000)) * np.sin(np.pi * u) ** 2
m.place(ft(C["street"] + 20), lp(bike, 3000), .7, 0, .2)
n = int(2.5 * SR); s = np.arange(n) / SR; m.place(ft(C["street"] + 45), np.sin(2 * np.pi * 4200 * s) * np.exp(-s * 1.2), .05, 0, .2)   # tinnitus ring
# mountains: wind, crunching snow steps, car engine arriving
mtn = m.env([(0, 0), (C["cabin"], 0), (C["cabin"] + 4, 1), (C["end"], 1)])
m.bed(bp(m.noise(m.N), 200, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * .2 * m.t)), mtn, .1, .5)
car = m.env([(0, 0), (C["cabin"], .8), (C["cabin"] + 110, .5), (C["cabin"] + 120, 0), (C["end"], 0)])
m.bed(lp(np.sin(2 * np.pi * 45 * m.t) + m.noise(m.N) * .3, 500), car, .15)
for k in range(14):
    n = int(.12 * SR); s = np.arange(n) / SR; m.place(ft(C["cabin"] + 125) + k * .4, bp(m.noise(n), 400, 3000) * np.exp(-s * 25), .12, (-1) ** k * .2, .3)
for c in (C["street"], C["talk"], C["cabin"]): m.whoosh(ft(c) - .3, g=.1)
m.score([[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]], bar=4.0, gain=.04, end=ft(C["street"]))
m.score([[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]], bar=3.5, gain=.055, start=ft(C["cabin"]))
for k, key in enumerate(["n0", "n1", "n2", "n3", "n4"]): m.voice(f"{ROOT}/vo/c6_{k}.wav", V[key])
m.voice(f"{ROOT}/vo/m6_0.wav", V["m0"]); m.voice(f"{ROOT}/vo/h6_0.wav", V["h0"])
m.render(f"{ROOT}/public/ch6.wav")
