#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
C = dict(site=95, silence=260, xray=360, rescue=580, chief=690, head=780, end=900); V = dict(n0=6, n1=100, k0=266, n2=366, n3=482, k1=696, n4=786)
m = Mix(C["end"], seed=5)
# TV news: rumble on the TV speaker + a news sting
tv = m.env([(0, 1), (C["site"] - 2, 1), (C["site"], 0), (C["end"], 0)])
m.bed(bp(lp(m.noise(m.N), 200), 80, 400) * 2, tv, .25)
for k, mm in enumerate([76, 79, 83]): m.chime(.2 + k * .15, mm, .07)
# rescue site: generators, excavator, shouts (filtered noise), dust; all stop in the silence
site = m.env([(0, 0), (C["site"], 0), (C["site"] + 2, 1), (C["silence"] + 18, 1), (C["silence"] + 28, 0), (C["rescue"], 0), (C["rescue"] + 10, .7), (C["head"] - 2, .7), (C["head"], 0), (C["end"], 0)])
gen = np.sin(2 * np.pi * 60 * m.t) * .4 + np.sign(np.sin(2 * np.pi * 120 * m.t)) * .15 + lp(m.noise(m.N), 300) * .6
m.bed(lp(gen, 900), site, .2, .3)
for k in range(14):
    t0 = m.rng.uniform(ft(C["site"]), ft(C["silence"])); n = int(.3 * SR); s = np.arange(n) / SR
    m.place(t0, bp(m.noise(n), 300, 4000) * np.exp(-s * 10), .1, m.rng.uniform(-.8, .8), .5)    # debris knocks
# the silence: only wind + the heartbeats coming through (from the sound view)
quiet = m.env([(0, 0), (C["silence"] + 25, 0), (C["silence"] + 35, 1), (C["rescue"] - 2, 1), (C["rescue"], 0), (C["end"], 0)])
m.bed(bp(m.noise(m.N), 200, 1200), quiet, .06, .6)
for i in range(3):
    tt = ft(C["xray"]) + i * .2
    while tt < ft(C["rescue"]): m.thump(tt, .32, 42 + i * 4); tt += .8 + i * .07
# rescue: digging scrapes, then a cheer swell
for k in range(16):
    n = int(.25 * SR); s = np.arange(n) / SR; m.place(ft(C["rescue"]) + k * .22, bp(m.noise(n), 500, 4000) * np.exp(-s * 12), .12, m.rng.uniform(-.4, .4), .4)
n = int(3 * SR); u = np.linspace(0, 1, n); m.place(ft(C["rescue"] + 80), bp(m.noise(n), 300, 3000) * np.sin(np.pi * u) ** .7 * (0.7 + 0.3 * np.sin(2 * np.pi * 6 * u)), .3, 0, .6)
# headline: paper whoosh + camera flashes
m.whoosh(ft(C["head"]) - .1, .8, .25, 400, 7000)
for k in range(6): n = int(.08 * SR); s = np.arange(n) / SR; m.place(ft(C["head"] + 20) + k * .35, hp(m.noise(n), 3000) * np.exp(-s * 60), .12, m.rng.uniform(-.7, .7), .4)
for c in (C["site"], C["xray"], C["rescue"]): m.whoosh(ft(c) - .3, g=.1)
m.score([[57, 60, 64], [55, 59, 62], [53, 57, 60], [52, 56, 59]], bar=3.5, gain=.05, end=ft(C["silence"]))
m.score([[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]], bar=3.0, gain=.06, start=ft(C["rescue"] + 60))
for k, key in enumerate(["n0", "n1", "n2", "n3", "n4"]): m.voice(f"{ROOT}/vo/c5_{k}.wav", V[key])
m.voice(f"{ROOT}/vo/k5_0.wav", V["k0"]); m.voice(f"{ROOT}/vo/k5_1.wav", V["k1"])
m.render(f"{ROOT}/public/ch5.wav")
