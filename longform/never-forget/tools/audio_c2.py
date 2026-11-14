#!/usr/bin/env python3
"""Chapter 2 sound: cool data-viz bed (soft droplets, dust shimmer, sweeps), the warm overflow swell, the Memory
Palace (airy choir-like pad + the music-box memory motif from the cold open, soft door creaks), calendar page flips,
marble footsteps, muffled fog. No beeps/ticks. Timeline = same formulas as src/Chapter2.tsx."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c2"); T = {}
T["n1"] = 10; T["n2"] = T["n1"] + D["n1"] + 6; T["curve"] = T["n2"] + D["n2"] + 4; T["n3"] = T["curve"] + 70
T["n4"] = T["n3"] + D["n3"] + 8; T["n5"] = T["n4"] + D["n4"] + 12; T["flood"] = T["n5"] + D["n5"] + 10; T["pal"] = T["flood"] + 24
T["n6"] = T["pal"] + 10; T["n7"] = T["n6"] + D["n6"] + 10; T["cal"] = T["n7"] + D["n7"] + 20; T["n8"] = T["cal"] + 6; T["n9"] = T["n8"] + D["n8"] + 8
T["hall"] = T["n9"] + D["n9"] + 10; T["n10"] = T["hall"] + 8; T["fog"] = T["n10"] + D["n10"] + 14; T["lina1"] = T["fog"] + 75; T["end"] = T["lina1"] + D["lina1"] + 30
print("end", T["end"])
m = Mix(T["end"], seed=21); N = m.N
def sec(a, b, fade=6): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
# cool bed for the data-viz part, airy palace bed after
m.bed(lp(m.noise(N), 400), sec(0, T["pal"]), .03)
for k in range(int(ft(T["curve"]) / .09)):                       # soft droplets falling into the bucket (water, low)
    n = int(.06 * SR); s = np.arange(n) / SR; f0 = 500 + 300 * m.rng.random()
    m.place(.3 + k * .09 + m.rng.uniform(0, .04), np.sin(2 * np.pi * f0 * (1 + 2 * s) * s) * np.exp(-s * 70), .025, m.rng.uniform(-.3, .3), .5)
m.whoosh(ft(T["curve"]) - .3, g=.1)
n = int(1.4 * SR); u = np.linspace(0, 1, n); m.place(ft(T["curve"] + 4), bp(m.noise(n), 600, 3000) * u * (1 - u) * 3, .05, 0, .4)   # the line being drawn
n3a = T["n3"] + round(D["n3"] * .36); n3b = T["n3"] + round(D["n3"] * .72)
for t0 in (T["n3"] + 8, n3a + 6):                                  # dust shimmer as things dissolve
    n = int(1.0 * SR); u = np.linspace(0, 1, n); m.place(ft(t0), hp(m.noise(n), 4000) * np.sin(np.pi * u) * (1 + .6 * np.sin(2 * np.pi * 23 * u)), .06, .3, .7)
m.thump(ft(n3b), .5, 40)
m.whoosh(ft(T["n4"]) + .2, d=1.6, g=.1, lo=200, hi=2500)
# warm swell into the overflow, bright chord at the flood
m.score([[48, 55, 60, 64]], bar=ft(T["pal"] - T["n5"]), gain=.035, piano=False, start=ft(T["n5"]), end=ft(T["pal"]))
n = int(1.6 * SR); s = np.arange(n) / SR; m.place(ft(T["flood"]) - .6, sum(np.sin(2 * np.pi * hz(p) * (1 + .3 * s / 1.6) * s) for p in (72, 79, 84, 91)) * np.exp(-((s - 1.2) ** 2) / .3) * .25, .3, 0, .7)
m.thump(ft(T["pal"]), .5, 36); m.hit(ft(T["pal"]), .2)
# palace: choir-ish pad (detuned sines with vibrato) + the memory motif on a music box
pal = np.maximum(sec(T["pal"], T["cal"]), np.maximum(sec(T["hall"], T["fog"]), sec(T["lina1"], T["end"])))
choir = sum(np.sin(2 * np.pi * hz(p) * m.t * (1 + .003 * np.sin(2 * np.pi * 5 * m.t + p))) for p in (57, 64, 69, 72, 76)) / 5
m._mus(0, lp(choir, 2500) * pal, .05)
motif = [76, 79, 83, 81, 79, 76, 74, 76, 72, 74, 76, 79]
for a, b in ((T["pal"], T["cal"]), (T["hall"], T["fog"])):
    for k in range(int((ft(b) - ft(a)) / .5)):
        t0 = ft(a) + .2 + k * .5; n = int(1.6 * SR); s = np.arange(n) / SR; p = motif[k % len(motif)]
        m._mus(t0, (np.sin(2 * np.pi * hz(p) * s) + .25 * np.sin(2 * np.pi * hz(p) * 3.01 * s)) * np.exp(-s * 3.5), .045, .3 * (-1) ** k)
for k in range(5):                                                   # doors creak open softly during "every door still opens"
    n = int(.7 * SR); s = np.arange(n) / SR; f0 = 180 + 60 * k
    m.place(ft(T["n7"]) + k * .35, np.sin(2 * np.pi * (f0 + 40 * np.sin(2 * np.pi * 7 * s)) * s) * np.sin(np.pi * s / .7) * .3 + bp(m.noise(n), 800, 3000) * np.sin(np.pi * s / .7) * .2, .06, (-1) ** k * .5, .8)
# calendar page flips at each stop (0, 26, 52, 78 frames) + a soft landing chime
for st in range(0, T["hall"] - T["cal"], 30):
    for j in range(7):
        n = int(.05 * SR); s = np.arange(n) / SR; m.place(ft(T["cal"] + st) + j * .045, bp(m.noise(n), 1500, 7000) * np.exp(-s * 60), .12, -.2, .3)
    m.chime(ft(T["cal"] + st + 11), m=[84, 86, 88, 91][(st // 30) % 4], g=.04)
# hall: footsteps on marble (step every half stride), with reverb
spd = 1000 / (T["fog"] - T["hall"]); every = 145 / spd
k = 0
while T["hall"] + k * every < T["fog"]: m.step(ft(T["hall"] + k * every), .14, .1); k += 1
for k in range(4): m.step(ft(T["fog"] + 4 + k * 13), .13, -.2)   # Lina walks in to the fogged doors
# fog corridor: muffled low hum + airy shimmer
fog = sec(T["fog"], T["lina1"] + 10)
m.bed(lp(m.noise(N), 250), fog, .06); m._mus(0, np.sin(2 * np.pi * 55 * m.t) * fog, .03)
m.whoosh(ft(T["fog"]) - .3, g=.1); m.whoosh(ft(T["hall"]) - .3, g=.08); m.whoosh(ft(T["cal"]) - .3, g=.08)
for k in ("n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9", "n10", "lina1"): m.vo_line(f"c2_{k}", T[k])
m.render(f"{ROOT}/public/c2.wav")
