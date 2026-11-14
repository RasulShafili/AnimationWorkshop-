#!/usr/bin/env python3
"""Chapter 3 sound: school morning (room tone, distant chatter murmur, birds outside), page flips + gold shimmer,
pencil scratching, a red-pen stamp, cafeteria clatter, card shuffle/spread, the gold glance sweep, hallway reverb,
the memory replay (dreamy, muffled), footsteps walking away, and a lonely end (rain on the cafeteria windows).
Light playful score that turns melancholic for the last beat. Timeline = same formulas as src/Chapter3.tsx."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c3"); T = {}
T["n1"] = 12; T["book"] = T["n1"] + round(D["n1"] * 0.42); T["exam"] = T["n1"] + D["n1"] + 10; T["stand"] = T["exam"] + 54
T["sam1"] = T["stand"] + 34; T["lina1"] = T["sam1"] + D["sam1"] + 6; T["cafe"] = T["lina1"] + D["lina1"] + 14
T["n2"] = T["cafe"] + 10; T["cards"] = T["n2"] + D["n2"] - 20; T["n3"] = T["n2"] + D["n2"] + 8; T["n4"] = T["n3"] + D["n3"] + 8; T["glance"] = T["n4"] + 4
T["sam2"] = T["n4"] + D["n4"] + 10; T["hall"] = T["sam2"] + D["sam2"] + 14; T["sam3"] = T["hall"] + 10; T["rew"] = T["sam3"] + D["sam3"] + 6; T["lina2"] = T["rew"] + 14
T["back"] = T["lina2"] + D["lina2"] + 8; T["n5"] = T["back"] + 18; T["n6"] = T["n5"] + D["n5"] + 8; T["alone"] = T["n6"] + round(D["n6"] * 0.45); T["end"] = T["n6"] + D["n6"] + 40
print("end", T["end"])
m = Mix(T["end"], seed=31); N = m.N
def sec(a, b, fade=5): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
murmur = bp(m.noise(N), 250, 1800) * (1 + .5 * lp(np.abs(m.noise(N)), 4))
m.bed(murmur, sec(0, T["cafe"]) * .5 + sec(T["cafe"], T["hall"]) * .9 + sec(T["n6"], T["end"]) * .4, .03)
m.bed(lp(m.noise(N), 300), sec(0, T["end"]), .03)
for k in range(8):                                                     # birds outside the classroom window
    t0 = m.rng.uniform(0, ft(T["cafe"])); n = int(.25 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * (3400 + 800 * np.sin(2 * np.pi * 16 * s)) * s) * np.exp(-s * 14), .012, .7, .5)
# page flips (every 3 frames) + gold shimmer as the words lift off
for k in range(int((T["exam"] - T["book"]) / 3)):
    n = int(.06 * SR); s = np.arange(n) / SR; m.place(ft(T["book"] + k * 3), bp(m.noise(n), 1500, 7000) * np.exp(-s * 50), .1, .2, .3)
n = int(1.6 * SR); u = np.linspace(0, 1, n); m.place(ft(T["book"]), hp(m.noise(n), 5000) * np.sin(np.pi * u) * (1 + .5 * np.sin(2 * np.pi * 30 * u)), .04, 0, .8)
# pencil scratching fast, then the red "100" stamp
for k in range(40):
    n = int(.07 * SR); s = np.arange(n) / SR; m.place(ft(T["exam"]) + k * .035, bp(m.noise(n), 2500, 8000) * np.sin(np.pi * s / .07), .06, -.1, .2)
m.thump(ft(T["exam"] + 46), .45, 70); m.hit(ft(T["exam"] + 46), .15)
m.whoosh(ft(T["stand"]) - .2, g=.06)
n = int(.5 * SR); s = np.arange(n) / SR; m.place(ft(T["stand"] + 2), bp(m.noise(n), 150, 900) * np.exp(-s * 8), .2, 0, .3)          # chair scrape as she stands
# cafeteria: trays, cutlery clinks (soft), card shuffle then spread
for k in range(10):
    t0 = ft(T["cafe"]) + m.rng.uniform(0, ft(T["hall"] - T["cafe"])); n = int(.12 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * (2400 + 600 * m.rng.random()) * s) * np.exp(-s * 40) * .4 + bp(m.noise(n), 2000, 6000) * np.exp(-s * 50), .03, m.rng.uniform(-.6, .6), .5)
for k in range(14):
    n = int(.04 * SR); s = np.arange(n) / SR; m.place(ft(T["cafe"] + 20) + k * .05, bp(m.noise(n), 1200, 6000) * np.exp(-s * 70), .12, .1, .3)
n = int(.7 * SR); u = np.linspace(0, 1, n); m.place(ft(T["cards"]), bp(m.noise(n), 1500, 7000) * np.sin(np.pi * u), .1, 0, .3)
# the glance: a rising gold sweep across the deck
n = int(ft(T["sam2"] - T["glance"]) * SR); s = np.arange(n) / SR
m.place(ft(T["glance"] + 14), sum(np.sin(2 * np.pi * hz(p) * (1 + .5 * s / s[-1]) * s) for p in (76, 83, 88)) * np.sin(np.pi * s / s[-1]) * .12, .25, 0, .7)
m.chime(ft(T["n4"]) + .1, m=88, g=.05)
# hallway: lockers slam in the distance, reverb; memory replay muffled cafeteria
for k in range(3): m.hit(ft(T["hall"]) + .4 + k * 1.1, .05)
m.whoosh(ft(T["rew"]) - .4, d=.8, g=.15, lo=200, hi=3000); m.chime(ft(T["rew"]), m=88, g=.05)
m.bed(lp(murmur, 700), sec(T["rew"], T["back"]), .05)
m.whoosh(ft(T["back"]) - .3, d=.4, g=.12, lo=800, hi=8000)
# Sam walks away
away0 = T["n5"] + 20
for k in range(int((T["n6"] - away0) / 24) + 1): m.step(ft(away0 + k * 24), .14, .3)
# lonely end: rain on the cafeteria windows, sparse piano
m.bed(bp(m.noise(N), 1500, 7000), sec(T["n6"], T["end"], 10), .035)
# score: playful pizzicato-ish loop for the school part, melancholic minor for the end
m.score([[60, 64, 67], [57, 60, 64], [62, 65, 69], [55, 59, 62]], bar=1.6, gain=.03, piano=True, start=0, end=ft(T["rew"]))
m.score([[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]], bar=3.0, gain=.035, piano=True, start=ft(T["n5"]), end=ft(T["end"]))
for k in ("n1", "sam1", "lina1", "n2", "n3", "n4", "sam2", "sam3", "lina2", "n5", "n6"): m.vo_line(f"c3_{k}", T[k])
m.render(f"{ROOT}/public/c3.wav")
