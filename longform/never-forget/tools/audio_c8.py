#!/usr/bin/env python3
"""Chapter 8 sound: the palace at night (low airy drone, the memory motif slowed and minor), footsteps, the dark door
(silence pocket), the handle rattles, THREE KNOCKS from the other side, a long low swell to black, the PART 2 hit,
then the warm music-box theme for the outro and end card. Timeline = same formulas as src/Chapter8.tsx."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c8"); T = {}
T["n1"] = 20; T["n2"] = T["n1"] + D["n1"] + 8; T["hall"] = T["n2"] + round(D["n2"] * .5); T["lina1"] = T["n2"] + D["n2"] + 8; T["push"] = T["lina1"] + D["lina1"] + 10
T["n3"] = T["push"] + 84; T["card"] = T["n3"] + D["n3"] + 24; T["n4"] = T["card"] + 96; T["n5"] = T["n4"] + D["n4"] + 10; T["end"] = T["n5"] + D["n5"] + 360
print("end", T["end"])
m = Mix(T["end"], seed=81); N = m.N
def sec(a, b, fade=8): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
night = sec(0, T["card"] - 10)
m._mus(0, lp(sum(np.sin(2 * np.pi * hz(p) * m.t * (1 + .003 * np.sin(2 * np.pi * 4 * m.t + p))) for p in (45, 52, 57, 60)) / 4, 1500) * night, .05)
m.bed(lp(m.noise(N), 300), night, .03)
motif = [76, 79, 83, 81, 79, 76, 74, 76]
for k in range(int(ft(T["n2"]) / .8)):                                   # the memory motif, slow and in minor
    n = int(2 * SR); s = np.arange(n) / SR; p = motif[k % 8] - (1 if motif[k % 8] in (76, 81) else 0)
    m._mus(.3 + k * .8, (np.sin(2 * np.pi * hz(p) * s) + .2 * np.sin(2 * np.pi * hz(p) * 3.01 * s)) * np.exp(-s * 2.5), .035, .3 * (-1) ** k)
for k in range(int(T["n2"] / 22)): m.step(ft(k * 22) + .3, .1, .1)
# the dark door: everything drops out except a low hum; handle rattle, then three knocks from the other side
m.bed(np.sin(2 * np.pi * 41 * m.t), sec(T["hall"], T["card"]), .05)
for k in range(5):
    n = int(.06 * SR); s = np.arange(n) / SR; m.place(ft(T["push"] + 12) + k * .08, (bp(m.noise(n), 800, 4000) + np.sin(2 * np.pi * 300 * s)) * np.exp(-s * 60), .15, .2, .4)
for kk in (34, 46, 58):
    m.thump(ft(T["push"] + kk), .55, 70); n = int(.2 * SR); s = np.arange(n) / SR
    m.place(ft(T["push"] + kk), bp(m.noise(n), 150, 1200) * np.exp(-s * 25), .35, .25, .8)
n = int(ft(T["card"] - T["n3"]) * SR); s = np.arange(n) / SR
m.place(ft(T["n3"]), sum(np.sin(2 * np.pi * hz(p) * s) for p in (33, 40, 45)) * np.minimum(1, s / 2) * np.minimum(1, (s[-1] - s) / .5), .12, 0, .5)
m.thump(ft(T["card"]), 1.0, 32); m.hit(ft(T["card"]), .35)
# outro: warm music box theme + soft pad, end card
k = 0; t = ft(T["card"] + 40)
while t < ft(T["end"]) - 1.5:
    p = motif[k % 8] + (0 if k % 16 < 8 else 2); n = int(1.6 * SR); s = np.arange(n) / SR
    m._mus(t, (np.sin(2 * np.pi * hz(p) * s) + .25 * np.sin(2 * np.pi * hz(p) * 3.01 * s)) * np.exp(-s * 3), .05, .25 * (-1) ** k)
    k += 1; t += .5
m.score([[57, 64, 69, 72], [53, 60, 65, 69], [55, 62, 67, 71], [57, 64, 69, 72]], bar=2.0, gain=.035, piano=False, start=ft(T["card"] + 40), end=ft(T["end"]))
for k in ("n1", "n2", "lina1", "n3", "n4", "n5"): m.vo_line(f"c8_{k}", T[k])
m.render(f"{ROOT}/public/c8.wav")
