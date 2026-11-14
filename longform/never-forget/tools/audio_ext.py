#!/usr/bin/env python3
"""Sound for the extension chapters c9 (lab), c10 (Sam's party), c11 (cinema), c12 (Grandma's stories).
  python3 tools/audio_ext.py c9   (timelines = same formulas as src/Chapter9..12.tsx)"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
ch = sys.argv[1]; D = meta(ch); T = {}
def sec(m, a, b, fade=6): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
MOTIF = [76, 79, 83, 81, 79, 76, 74, 76]
WALTZ = [72, 76, 79, 77, 76, 74, 72, 74, 76, 72, 69, 71, 72, 76, 79, 81, 79, 77, 76, 74, 72]
def box(m, a, b, notes, beat, g=.045):
    k = 0; t = a
    while t < b - .5:
        p = notes[k % len(notes)]; n = int(1.6 * SR); s = np.arange(n) / SR
        m._mus(t, (np.sin(2 * np.pi * hz(p) * s) + .25 * np.sin(2 * np.pi * hz(p) * 3.01 * s)) * np.exp(-s * 3), g, .25 * (-1) ** k); k += 1; t += beat
if ch == "c9":
    T["n1"] = 14; T["doc1"] = T["n1"] + D["n1"] + 6; T["lina1"] = T["doc1"] + D["doc1"] + 6; T["n2"] = T["lina1"] + D["lina1"] + 6; T["doc2"] = T["n2"] + D["n2"] + 6
    T["n3"] = T["doc2"] + D["doc2"] + 8; T["doc3"] = T["n3"] + D["n3"] + 4; T["n4"] = T["doc3"] + D["doc3"] + 8; T["n5"] = T["n4"] + D["n4"] + 8; T["end"] = T["n5"] + D["n5"] + 60
    m = Mix(T["end"], seed=91); N = m.N
    m.bed(lp(m.noise(N), 400) + .3 * np.sin(2 * np.pi * 100 * m.t), sec(m, 0, T["n3"]), .03)
    for k in range(20):                                   # the score ticking up: soft marimba-like plucks (not beeps)
        n = int(.3 * SR); s = np.arange(n) / SR; p = 72 + (k % 5) * 2
        m.place(ft(T["n2"]) + k * ft(D["n2"]) * .045, (np.sin(2 * np.pi * hz(p) * s) + .4 * np.sin(4 * np.pi * hz(p) * s)) * np.exp(-s * 14), .03, .3, .4)
    m.chime(ft(T["doc2"]) - .3, m=88, g=.06)
    m.whoosh(ft(T["n3"]) - .3, g=.1); m._mus(0, lp(sum(np.sin(2 * np.pi * hz(p) * m.t) for p in (45, 52, 57)), 900) * sec(m, T["n3"], T["n4"]), .04)
    for k in range(3):
        n = int(.5 * SR); u = np.linspace(0, 1, n); m.place(ft(T["n5"] + k * 26), bp(m.noise(n), 1000, 7000) * np.sin(np.pi * u), .12, -.3 + .3 * k, .3)   # paper whoosh
        m.thump(ft(T["n5"] + k * 26 + 14), .3, 60)
    m.score([[60, 64, 67], [62, 65, 69], [57, 60, 64], [59, 62, 67]], bar=2.0, gain=.03, piano=True, start=0, end=ft(T["end"]))
    lines = ("n1", "doc1", "lina1", "n2", "doc2", "n3", "doc3", "n4", "n5")
elif ch == "c10":
    T["n1"] = 14; T["n2"] = T["n1"] + D["n1"] + 6; T["sam1"] = T["n2"] + D["n2"] + 8; T["n3"] = T["sam1"] + D["sam1"] + 8; T["n4"] = T["n3"] + D["n3"] + 6
    T["surprise"] = T["n4"] + D["n4"] + 8; T["sam2"] = T["surprise"] + 44; T["lina1"] = T["sam2"] + D["sam2"] + 6; T["n5"] = T["lina1"] + D["lina1"] + 8; T["end"] = T["n5"] + D["n5"] + 50
    m = Mix(T["end"], seed=101); N = m.N
    m.bed(lp(m.noise(N), 220), sec(m, 0, T["sam1"]), .04)
    m.whoosh(ft(T["sam1"]) - .5, d=.8, g=.14, lo=200, hi=3000); m.chime(ft(T["sam1"] - 6), m=88, g=.05)
    m.bed(lp(bp(m.noise(N), 300, 2000), 900), sec(m, T["sam1"], T["n3"]), .04)
    box(m, ft(T["n3"]), ft(T["surprise"]), MOTIF, .42)
    for k in range(3): m.place(ft(T["n4"]) + .3 + k * .5, np.sin(2 * np.pi * hz(84 + 3 * k) * np.arange(int(.5 * SR)) / SR) * np.exp(-np.arange(int(.5 * SR)) / SR * 6) * .3, .05, 0, .5)
    m.bed(bp(m.noise(N), 300, 2500) * (1 + .6 * lp(np.abs(m.noise(N)), 5)), sec(m, T["surprise"] + 26, T["end"]), .06)        # friends cheering
    n = int(.15 * SR); s = np.arange(n) / SR
    for k in range(3): m.place(ft(T["surprise"] + 26) + k * .05, bp(m.noise(n), 1000, 8000) * np.exp(-s * 30), .4, (-1) ** k * .5, .4)   # party poppers
    m.score([[60, 64, 67, 72], [65, 69, 72], [67, 71, 74], [60, 64, 67]], bar=1.4, gain=.04, piano=True, start=ft(T["surprise"] + 26), end=ft(T["end"]))
    lines = ("n1", "n2", "sam1", "n3", "n4", "sam2", "lina1", "n5")
elif ch == "c11":
    T["n1"] = 14; T["n2"] = T["n1"] + D["n1"] + 8; T["n3"] = T["n2"] + D["n2"] + 10; T["end"] = T["n3"] + D["n3"] + 50
    m = Mix(T["end"], seed=111); N = m.N
    m.bed(lp(m.noise(N), 300), sec(m, 0, T["end"]), .04)
    m.bed(bp(m.noise(N), 1500, 5000) * (1 + .5 * np.sin(2 * np.pi * 24 * m.t)), sec(m, 0, T["end"]), .012)                    # projector whirr
    box(m, .3, ft(T["n3"]), MOTIF, .55, .04)
    m.score([[45, 48, 52], [41, 45, 48]], bar=2.4, gain=.03, piano=True, start=ft(T["n3"]), end=ft(T["end"]))
    lines = ("n1", "n2", "n3")
elif ch == "c13":
    T["n1"] = 12; T["okafor1"] = T["n1"] + D["n1"] + 6; T["lina1"] = T["okafor1"] + D["okafor1"] + 6; T["flash"] = T["lina1"] + round(D["lina1"] * .3)
    T["n2"] = T["lina1"] + D["lina1"] + 8; T["okafor2"] = T["n2"] + D["n2"] + 6; T["n3"] = T["okafor2"] + D["okafor2"] + 8; T["n4"] = T["n3"] + D["n3"] + 30; T["end"] = T["n4"] + D["n4"] + 40
    m = Mix(T["end"], seed=131); N = m.N
    for k in range(3):                                    # phone vibrating
        n = int(.45 * SR); s = np.arange(n) / SR; m.place(.2 + k * .8, lp((np.sign(np.sin(2 * np.pi * 150 * s)) * .5 + bp(m.noise(n), 100, 400)) * (s < .4), 900) * .5, .15, .1, .2)
    m.bed(lp(m.noise(N), 300) + .3 * np.sin(2 * np.pi * 120 * m.t), sec(m, T["okafor1"], T["lina1"]), .03)
    m.whoosh(ft(T["flash"]) - .3, d=.6, g=.12, lo=300, hi=4000); m.chime(ft(T["flash"]), m=88, g=.05)
    m.bed(lp(bp(m.noise(N), 200, 1500), 800), sec(m, T["flash"], T["flash"] + 50), .05)
    for k in range(3): m.thump(ft(T["n2"] + k * round(D["n2"] / 3) + 2), .35, 60); m.chime(ft(T["n2"] + k * round(D["n2"] / 3) + 3), m=84 + 2 * k, g=.04)
    for k in range(22):
        n = int(.04 * SR); s = np.arange(n) / SR; m.place(ft(T["n3"]) + k * .05, bp(m.noise(n), 1500, 6000) * np.exp(-s * 120), .12, .1, .2)
    m.chime(ft(T["n3"] + 54), m=91, g=.05)
    m.bed(bp(m.noise(N), 1500, 7000), sec(m, T["n4"], T["end"]), .04)
    for k in range(6): m.step(ft(T["n4"] + 6 + k * 18), .2, .1)
    m.score([[60, 64, 67], [62, 65, 69], [64, 67, 71], [65, 69, 72]], bar=1.6, gain=.035, piano=True, start=0, end=ft(T["end"]))
    lines = ("n1", "okafor1", "lina1", "n2", "okafor2", "n3", "n4")
else:
    T["n1"] = 14; T["n2"] = T["n1"] + D["n1"] + 8; T["ayla1"] = T["n2"] + D["n2"] + 12; T["n3"] = T["ayla1"] + D["ayla1"] + 10; T["end"] = T["n3"] + D["n3"] + 70
    m = Mix(T["end"], seed=121); N = m.N
    m.bed(lp(m.noise(N), 250), sec(m, 0, T["end"]), .03)
    for k in range(3): m.chime(ft(T["n2"] + round(D["n2"] * (0, .36, .66)[k])), m=(84, 86, 88)[k], g=.04)
    for k in range(5):
        n = int(.25 * SR); s = np.arange(n) / SR; m.place(ft(T["ayla1"]) + .4 + k * .4, bp(m.noise(n), 400, 2500) * np.exp(-s * 10) * (1 + np.sin(2 * np.pi * 9 * s)), .03, (-1) ** k * .3, .4)
    box(m, .3, ft(T["end"]), WALTZ, .44, .045)
    lines = ("n1", "n2", "ayla1", "n3")
print("end", T["end"])
for k in lines: m.vo_line(f"{ch}_{k}", T[k])
m.render(f"{ROOT}/public/{ch}.wav")
