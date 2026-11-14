#!/usr/bin/env python3
"""Chapter 4 sound: Vegas strip (traffic, distant crowd, neon buzz), casino floor (slot-machine jingles as soft bell
chords — no beeps, crowd murmur, chips clacking), card deal swishes, the counting data-viz shimmer, chips pushed,
guards' heavy steps, a "record stop" style beat before "Fair.", the hard cut to the quiet bedroom, phone vibrating.
Score: a sly jazzy loop (walking bass + brushes made from noise) for Vegas; soft piano at home."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c4"); T = {}
T["n1"] = 24; T["casino"] = T["n1"] + D["n1"] + 8; T["n2"] = T["casino"] + 10; T["count"] = T["n2"] + 40; T["chips"] = T["n2"] + D["n2"] + 30
T["sam1"] = T["chips"] + 45; T["guards"] = T["sam1"] + D["sam1"] + 10; T["man"] = T["guards"] + 44; T["manager1"] = T["man"]; T["n3"] = T["man"] + D["manager1"] + 14
T["now"] = T["n3"] + D["n3"] + 34; T["n4"] = T["now"] + 16; T["phone"] = T["n4"] + D["n4"] + 6; T["end"] = T["phone"] + 70
print("end", T["end"])
m = Mix(T["end"], seed=41); N = m.N
def sec(a, b, fade=5): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
street = np.maximum(sec(0, T["casino"]), sec(T["n3"], T["now"]))
m.bed(lp(m.noise(N), 500), street, .07)                                              # traffic rumble
m.bed(np.sin(2 * np.pi * 120 * m.t) * (1 + .3 * np.sin(2 * np.pi * 7 * m.t)), street, .006)   # neon buzz
for k in range(4):                                                                   # cars passing
    t0 = m.rng.uniform(0, ft(T["casino"])); n = int(1.6 * SR); u = np.linspace(0, 1, n)
    m.place(t0, bp(m.noise(n), 200, 2000) * np.sin(np.pi * u) ** 2, .08, -.8 + 1.6 * m.rng.random(), .3)
floor = sec(T["casino"], T["n3"])
m.bed(bp(m.noise(N), 300, 2000) * (1 + .4 * lp(np.abs(m.noise(N)), 3)), floor, .05)  # casino crowd
for k in range(int(ft(T["n3"] - T["casino"]) / .9)):                                  # slot machines: soft bell arpeggios
    t0 = ft(T["casino"]) + k * .9 + m.rng.uniform(0, .4)
    for j, p in enumerate([84, 88, 91][: 1 + int(m.rng.random() * 3)]):
        n = int(.5 * SR); s = np.arange(n) / SR; m.place(t0 + j * .07, np.sin(2 * np.pi * hz(p) * s) * np.exp(-s * 9), .012, m.rng.uniform(-.8, .8), .6)
# card deals + chips
for k in range(6):
    n = int(.12 * SR); u = np.linspace(0, 1, n); m.place(ft(T["casino"] + 14) + k * .35, bp(m.noise(n), 2000, 8000) * np.sin(np.pi * u), .1, .2, .3)
n = int(ft(T["chips"] - T["count"]) * SR); s = np.arange(n) / SR
m.place(ft(T["count"]), hp(m.noise(n), 4000) * .3 * (1 + .5 * np.sin(2 * np.pi * 12 * s)) * np.minimum(1, s * 2) * np.minimum(1, (s[-1] - s) * 2), .05, 0, .6)
for k in range(18):
    n = int(.05 * SR); s = np.arange(n) / SR; m.place(ft(T["chips"]) + k * .08, (np.sin(2 * np.pi * 2600 * s) * .4 + bp(m.noise(n), 2000, 6000)) * np.exp(-s * 80), .12, .1, .3)
# guards: heavy steps
for k in range(5): m.step(ft(T["guards"]) + k * .4, .3, .5); m.thump(ft(T["guards"]) + k * .4, .12, 50)
# before "Fair.": the jazz loop stops dead (tape-stop), then the street
n = int(.5 * SR); s = np.arange(n) / SR; m.place(ft(T["n3"]) - .55, np.sin(2 * np.pi * np.cumsum(220 * np.exp(-s * 5)) / SR) * np.exp(-s * 3), .12, 0, .2)
# hard cut to the bedroom: silence, clock-free room tone, then the phone vibrating
room = sec(T["now"], T["end"])
m.bed(lp(m.noise(N), 200), room, .03)
for k in range(3):
    n = int(.45 * SR); s = np.arange(n) / SR; buzz = (np.sign(np.sin(2 * np.pi * 150 * s)) * .5 + bp(m.noise(n), 100, 400)) * (s < .4)
    m.place(ft(T["phone"] - 30) + k * .8, lp(buzz, 900) * .5, .18, .1, .2)
# score: jazzy walking bass + noise brushes for Vegas, soft piano at home
bass = [40, 43, 45, 47, 48, 47, 45, 43]; beat = .38
for k in range(int(ft(T["n3"] - 4) / beat)):
    t0 = k * beat; n = int(beat * SR); s = np.arange(n) / SR; p = bass[k % 8] - 12
    m._mus(t0, (np.sin(2 * np.pi * hz(p) * s) + .3 * np.sin(4 * np.pi * hz(p) * s)) * np.exp(-s * 6), .07, -.1)
    nb = int(.12 * SR); sb = np.arange(nb) / SR; m._mus(t0 + (beat / 2 if k % 2 else 0), bp(m.noise(nb), 3000, 9000) * np.exp(-sb * 30), .025, .3)
m.score([[57, 60, 64], [53, 57, 60]], bar=2.4, gain=.03, piano=True, start=ft(T["now"] + 10), end=ft(T["end"]))
for k in ("n1", "n2", "sam1", "manager1", "n3", "n4"): m.vo_line(f"c4_{k}", T[k])
m.render(f"{ROOT}/public/c4.wav")
