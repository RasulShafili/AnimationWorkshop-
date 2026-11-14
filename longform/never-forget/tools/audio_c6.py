#!/usr/bin/env python3
"""Chapter 6 sound: a silent night room (faint wind, a far car), the memory replays as cold, distorted flashes
(laughter murmur, a door closing, the doctor's muffled voice), getting faster ("on repeat") with tape-rewind whirs,
a match strike + paper burning + fizz in the sink, a calm sweep for "forgetting is healthy", the clinic tone, the
pill bottle sliding and rattling, then a long held silence with a single low piano note."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c6"); T = {}
T["n1"] = 16; T["n2"] = T["n1"] + D["n1"] + 6; T["n3"] = T["n2"] + D["n2"] + 4; T["n4"] = T["n3"] + D["n3"] + 22; T["n5"] = T["n4"] + D["n4"] + 10
T["hale2"] = T["n5"] + D["n5"] + 14; T["pill"] = T["hale2"] + D["hale2"] - 26; T["n6"] = T["hale2"] + D["hale2"] + 30; T["end"] = T["n6"] + D["n6"] + 80
print("end", T["end"])
m = Mix(T["end"], seed=61); N = m.N
def sec(a, b, fade=6): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
night = sec(0, T["n3"])
m.bed(lp(m.noise(N), 220) * (1 + .5 * np.sin(2 * np.pi * .1 * m.t)), night, .05)
n = int(3 * SR); u = np.linspace(0, 1, n); m.place(1.0, bp(m.noise(n), 200, 1200) * np.sin(np.pi * u) ** 2, .03, .7, .6)
# replays: cold whoosh in, laughter murmur / door / muffled voice, rewind whirs that speed up
m.whoosh(ft(T["n3"]) - .3, d=.6, g=.18, lo=300, hi=6000)
rep = sec(T["n3"], T["n4"] - 4)
m.bed(bp(m.noise(N), 500, 2500) * (1 + .8 * lp(np.abs(m.noise(N)), 6)), sec(T["n3"], T["n3"] + round(D["n3"] * .3)), .06)      # kids laughing (murmur)
m.thump(ft(T["n3"] + round(D["n3"] * .3) + 50), .5, 55)                                                                          # the door closes
m.bed(lp(bp(m.noise(N), 200, 900), 600) * (1 + np.sin(2 * np.pi * 4 * m.t)), sec(T["n3"] + round(D["n3"] * .58), T["n4"] - 4), .05)   # muffled voice
for k in range(10):
    t0 = ft(T["n3"] + round(D["n3"] * .78)) + k * max(.1, .35 - k * .03); n = int(.25 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * np.cumsum(900 - 600 * s / .25) / SR) * np.exp(-s * 8) * .3 + bp(m.noise(n), 1500, 6000) * np.exp(-s * 10) * .3, .1, 0, .4)
m._mus(0, np.sin(2 * np.pi * 55 * m.t) * rep, .04)
# sink: match strike, paper catches, crackle, fizz of water at the end
n = int(.3 * SR); s = np.arange(n) / SR; m.place(ft(T["n4"] + 8), bp(m.noise(n), 2000, 9000) * np.exp(-s * 12), .3, .1, .3)
fire = sec(T["n4"] + 12, T["n4"] + 60, 10)
m.bed(bp(m.noise(N), 300, 4000) * (np.abs(m.noise(N)) > 2.2) * 3 + lp(m.noise(N), 400), fire, .05)
n = int(2.5 * SR); u = np.linspace(0, 1, n); m.place(ft(T["n4"] + 40), hp(m.noise(n), 3000) * np.sin(np.pi * u) * .5, .06, 0, .7)
n = int(1.8 * SR); s = np.arange(n) / SR; m.place(ft(T["n4"] + 46), sum(np.sin(2 * np.pi * hz(p) * (1 + .3 * s / 1.8) * s) for p in (76, 83, 88)) * np.sin(np.pi * s / 1.8) * .15, .2, 0, .8)   # words rise (gold shimmer)
m.whoosh(ft(T["n5"]) + .3, d=2.4, g=.08, lo=200, hi=2500)
# clinic + pill slide + rattle
m.bed(lp(m.noise(N), 500) + .3 * np.sin(2 * np.pi * 100 * m.t), sec(T["hale2"], T["end"]), .025)
n = int(.7 * SR); u = np.linspace(0, 1, n); m.place(ft(T["pill"]), bp(m.noise(n), 300, 2500) * np.sin(np.pi * u) * (1 - u), .12, .2, .2)
for k in range(5):
    n = int(.05 * SR); s = np.arange(n) / SR; m.place(ft(T["pill"]) + .2 + k * .06, bp(m.noise(n), 2500, 8000) * np.exp(-s * 70), .08, .2, .2)
# score: sparse, cold piano; one low note held under the final beat
m.score([[45, 48, 52], [41, 45, 48], [40, 43, 47], [45, 48, 52]], bar=3.2, gain=.03, piano=True, start=0, end=ft(T["n3"]))
m.score([[45, 48, 52], [43, 47, 50]], bar=3.2, gain=.025, piano=True, start=ft(T["n5"]), end=ft(T["n6"]))
n = int(ft(T["end"] - T["n6"]) * SR); s = np.arange(n) / SR; m._mus(ft(T["n6"]), np.sin(2 * np.pi * hz(33) * s) * np.minimum(1, s / 2) * np.minimum(1, (s[-1] - s) / 2), .06)
for k in ("n1", "n2", "n3", "n4", "n5", "hale2", "n6"): m.vo_line(f"c6_{k}", T[k])
m.render(f"{ROOT}/public/c6.wav")
