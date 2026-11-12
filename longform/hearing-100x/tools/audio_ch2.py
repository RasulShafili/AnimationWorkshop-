#!/usr/bin/env python3
import numpy as np, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
C = dict(field=170, house=280, ear=380, hiss=770, end=900); VO = [10, 176, 286, 386, 525, 776]
m = Mix(C["end"], seed=2)
# morning room: birds, distant city; meter fill riser
morning = m.env([(0, 1), (C["field"] - 2, 1), (C["field"], 0), (C["end"], 0)])
m.bed(lp(m.noise(m.N), 200), morning, .08)
for k in range(10):
    t0 = m.rng.uniform(0, ft(C["field"]) - .3); n = int(.1 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * np.cumsum(3000 + 1200 * np.sin(np.pi * s / s[-1])) / SR) * np.sin(np.pi * s / s[-1]) ** 2, .03, m.rng.uniform(-.8, .8), .5)
n = int(2.3 * SR); u = np.linspace(0, 1, n); m.place(1.0, bp(m.noise(n), 600, 6000) * u ** 2 * .6, .12, 0, .4)
# field: crowd murmur far, wind, whisper travelling L->R (filtered noise 'psst')
field = m.env([(0, 0), (C["field"], 0), (C["field"] + 2, 1), (C["house"] - 2, 1), (C["house"], 0), (C["end"], 0)])
m.bed(bp(m.noise(m.N), 200, 1200), field, .1, .4)
for k, d in enumerate([0, .25, .5]):
    n = int(.22 * SR); s = np.arange(n) / SR; m.place(ft(C["field"] + 20) + d, bp(m.noise(n), 2500, 8000) * np.sin(np.pi * s / s[-1]) ** 2, .15, -.6 + k * .6, .3)
# house: mosquito buzz, LOUD (that's the joke), with flutter
house = m.env([(0, 0), (C["house"], 0), (C["house"] + 3, 1), (C["ear"] - 3, 1), (C["ear"], 0), (C["end"], 0)])
buzz = np.sign(np.sin(2 * np.pi * np.cumsum(560 + 40 * np.sin(2 * np.pi * 3 * m.t)) / SR)) * .4 + np.sin(2 * np.pi * np.cumsum(560 + 40 * np.sin(2 * np.pi * 3 * m.t)) / SR) * .6
m.bed(lp(buzz, 4000), house, .12, .2)
# ear: molecule pitter-patter (tiny clicks), growing; then hiss forever (the bed for the night)
ear = m.env([(0, 0), (C["ear"], 0), (C["ear"] + 20, .5), (C["hiss"] - 2, 1), (C["end"], 0)])
for k in range(900):
    t0 = m.rng.uniform(ft(C["ear"]), ft(C["hiss"])); n = int(.004 * SR); g = ear[int(t0 * SR)]
    m.place(t0, hp(m.noise(n), 3000) * np.exp(-np.arange(n) / SR * 900), .06 * g, m.rng.uniform(-.5, .5), .2)
hiss = m.env([(0, 0), (C["ear"] + 150, 0), (C["hiss"], .6), (C["hiss"] + 20, 1), (C["end"], 1)])
m.bed(hp(m.noise(m.N), 3000), hiss, .1, .2, hp(m.noise(m.N), 3000))
for c in (C["field"], C["house"], C["ear"], C["hiss"]): m.whoosh(ft(c) - .3)
m.score([[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]], gain=.045, end=ft(C["hiss"]))
for i, f0 in enumerate(VO): m.voice(f"{ROOT}/vo/c2_{i}.wav", f0)
m.render(f"{ROOT}/public/ch2.wav")
