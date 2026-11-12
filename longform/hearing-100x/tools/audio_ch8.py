#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
C = dict(ocean=210, reveal=610, outro=790, end=1090); V = dict(s0=50, s1=216, s2=512, n0=616, n1=800, n2=940)
m = Mix(C["end"], seed=8)
mtn = m.env([(0, 1), (C["ocean"] - 2, 1), (C["ocean"], 0), (C["reveal"], 0), (C["reveal"] + 2, 1), (C["end"], 1)])
m.bed(bp(m.noise(m.N), 200, 1500), mtn, .07, .5)
for k in range(3):                                         # phone vibrating/ringing (a soft marimba-like ring, not a beep)
    for j, mm in enumerate([76, 79]): m.chime(ft(12) + k * .45 + j * .12, mm, .06)
# ocean: deep rumble, bubbles, the 1997 'bloop' (rising low sweep), then a giant slow heartbeat
oc = m.env([(0, 0), (C["ocean"], 0), (C["ocean"] + 4, 1), (C["reveal"] - 4, 1), (C["reveal"], 0), (C["end"], 0)])
m.bed(lp(m.noise(m.N), 120) * 1.4, oc, .3, .6)
for k in range(30):
    t0 = m.rng.uniform(ft(C["ocean"]), ft(C["reveal"])); n = int(.06 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * np.cumsum(400 + 900 * s / s[-1]) / SR) * np.exp(-s * 40), .04, m.rng.uniform(-.6, .6), .6)
d = 3.0; n = int(d * SR); s = np.arange(n) / SR; u = s / d
m.place(ft(V["s1"] + 120), np.sin(2 * np.pi * np.cumsum(30 + 60 * u ** 1.5) / SR) * np.sin(np.pi * u) ** 1.5, .5, 0, .8)
tt = ft(V["s2"] + 40)
while tt < ft(C["outro"]): m.thump(tt, .6, 28); tt += 2.0
m.hit(ft(720), .45)
for c in (C["ocean"], C["reveal"], C["outro"]): m.whoosh(ft(c) - .3, g=.1)
m.score([[57, 60, 64], [53, 57, 60], [52, 55, 59], [52, 56, 59]], bar=3.5, gain=.045, end=ft(C["outro"]))
m.score([[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]], bar=3.0, gain=.07, start=ft(C["outro"]))
for k in range(3): m.voice(f"{ROOT}/vo/s8_{k}.wav", V[f"s{k}"])
for k in range(3): m.voice(f"{ROOT}/vo/c8_{k}.wav", V[f"n{k}"])
m.render(f"{ROOT}/public/ch8.wav")
