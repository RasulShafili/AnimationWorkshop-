#!/usr/bin/env python3
"""Cold open sound: police room (fluorescent hum, rain on the window), coffee slam, the gold memory swell, the street
three years ago heard through a dreamy filter, the car pass and the time-freeze, keyboard + MATCH FOUND stab, rain
and footsteps outside, title boom. Original score: low minor pad + a music-box motif for memories (our own notes).
Timeline must match src/ColdOpen.tsx (same formulas)."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c1")
T = {}
T["okafor1"] = 48; T["photo"] = T["okafor1"] + 76
T["okafor2"] = T["okafor1"] + D["okafor1"] + 10
T["n1"] = T["okafor2"] + D["okafor2"] + 12
T["n2"] = T["n1"] + D["n1"] + 6
T["flash"] = T["n2"] + D["n2"] + 4
T["rew"] = T["flash"] + 12
T["lina1"] = T["rew"] + 26; T["plate"] = T["lina1"] + 34
T["lina2"] = T["lina1"] + D["lina1"] + 10; T["fresh"] = T["lina2"] + round(D["lina2"] * 0.55)
T["lina3"] = T["lina2"] + D["lina2"] + 10
T["tip"] = T["lina3"] + D["lina3"] + 14
T["knock"] = T["tip"]; T["spillCU"] = T["tip"] + 26; T["screen"] = T["tip"] + 66
T["n3"] = T["screen"] + 66; T["two"] = T["screen"] + 84
T["loftus"] = T["n3"] + D["n3"] + 10
T["ext"] = T["loftus"] + 135
T["n4"] = T["ext"] + 10
T["title"] = T["n4"] + D["n4"] + 20
T["n5"] = T["title"] + 10
T["end"] = T["n5"] + D["n5"] + 45
print("end", T["end"])
m = Mix(T["end"], seed=11)
N = m.N
def sec(a, b): return m.env([(0, 0), (max(0, a - 3), 0), (a, 1), (b, 1), (b + 3, 0), (T["end"], 0)])
room = np.maximum(sec(0, T["rew"]), sec(T["tip"], T["loftus"]))
# police room: fluorescent hum + rain on glass
hum = (np.sin(2 * np.pi * 120 * m.t) + .4 * np.sin(2 * np.pi * 240 * m.t)) * (1 + .3 * np.sin(2 * np.pi * .3 * m.t))
m.bed(hum, room, .018)
rain = bp(m.noise(N), 1500, 7000) * (1 + .5 * lp(np.abs(m.noise(N)), 3))
m.bed(rain, room * .6 + sec(T["ext"], T["title"]) * 1.4, .05, x2=bp(m.noise(N), 1500, 7000))
m.bed(lp(m.noise(N), 300), room + sec(T["ext"], T["title"]), .05)
# 1) coffee slam on a metal table
m.thump(ft(8), .9, 55); m.hit(ft(8), .55)
n = int(.6 * SR); s = np.arange(n) / SR; m.place(ft(8), (np.sin(2 * np.pi * 820 * s) + .6 * np.sin(2 * np.pi * 1310 * s)) * np.exp(-s * 9) * .3, .35, .1, .4)
n = int(.35 * SR); s = np.arange(n) / SR; m.place(ft(9), bp(m.noise(n), 600, 4000) * np.exp(-s * 12), .3, 0, .3)     # splash
m.whoosh(ft(42) - .2, g=.08)
# 2) photo slides across the table
n = int(.9 * SR); u = np.linspace(0, 1, n); m.place(ft(T["photo"]), bp(m.noise(n), 2000, 8000) * np.sin(np.pi * u) ** 2, .12, .2, .2)
m.whoosh(ft(T["okafor2"]) - .25, g=.07)
# 3) the gold memory swell: rising shimmer into a soft boom, then the street fades in (low-passed, dreamy)
n = int(1.4 * SR); s = np.arange(n) / SR; sw = sum(np.sin(2 * np.pi * hz(m0) * (1 + .5 * s / 1.4) * s) * np.exp(-((s - 1.2) ** 2) / .2) for m0 in (76, 83, 88, 95))
m.place(ft(T["flash"]) - 1.15, sw * .25, .4, 0, .6)
m.thump(ft(T["flash"]), .7, 38); m.whoosh(ft(T["flash"]) - .1, d=.9, g=.2, lo=200, hi=3000)
mem = sec(T["rew"], T["tip"])
m.bed(lp(bp(m.noise(N), 300, 3000), 1200), mem, .05)                  # distant street
for k in range(10):                                                     # birds, dreamy and far
    t0 = ft(T["rew"]) + m.rng.uniform(0, ft(T["tip"] - T["rew"])); n = int(.25 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * (3200 + 900 * np.sin(2 * np.pi * 14 * s)) * s) * np.exp(-s * 14), .02, m.rng.uniform(-.7, .7), .7)
# the car passes (engine + tyres, doppler) then FREEZES: time-stop tape-slow + low boom
t_stop = ft(T["lina1"] + 30); n = int((t_stop - ft(T["rew"])) * SR); s = np.arange(n) / SR; prog = s / s[-1]
eng = np.sin(2 * np.pi * (70 - 30 * prog ** 2) * s + 3 * np.sin(2 * np.pi * 9 * s)) * .5 + bp(m.noise(n), 200, 1500) * .6
y = eng * np.minimum(1, prog * 3) * (1 - prog ** 3); K = 12; L = len(y) // K
for k in range(K):                                                       # pan sweeps left → right in chunks
    seg = y[k * L:(k + 1) * L + 400].copy(); w = np.minimum(1, np.minimum(np.arange(len(seg)), len(seg) - np.arange(len(seg))) / 400)
    m.place(ft(T["rew"]) + k * L / SR, seg * w, .25, .6 - 1.0 * (k + .5) / K, .3)
n = int(.8 * SR); s = np.arange(n) / SR; m.place(t_stop - .4, np.sin(2 * np.pi * (300 * np.exp(-s * 3)) * s) * np.exp(-s * 3) * .4, .3, 0, .5)
m.thump(t_stop, .5, 40)
for k in ("plate", "lina2", "fresh"): m.chime(ft(T[k] + (10 if k == "lina2" else 0)), m=88 if k != "fresh" else 91, g=.05)
# 4) snap back; Okafor's hand knocks the cup (+7), it falls on its side (+16), coffee glugs out and spreads (close-up)
m.whoosh(ft(T["knock"]) - .3, d=.4, g=.18, lo=800, hi=8000); m.hit(ft(T["knock"]), .2)
n = int(.12 * SR); s = np.arange(n) / SR; m.place(ft(T["knock"] + 7), (bp(m.noise(n), 900, 5000) * .7 + np.sin(2 * np.pi * 520 * s) * .5) * np.exp(-s * 45), .35, .15, .2)   # knuckle on paper cup
n = int(.3 * SR); s = np.arange(n) / SR; m.place(ft(T["knock"] + 16), (bp(m.noise(n), 300, 3000) + np.sin(2 * np.pi * 180 * s) * .6) * np.exp(-s * 16), .45, .2, .3)  # cup hits the table
n = int(.18 * SR); s = np.arange(n) / SR; m.place(ft(T["knock"] + 19), bp(m.noise(n), 600, 4000) * np.exp(-s * 25), .2, .25, .3)                                   # lid pops off
for k in range(9):                                                                                                                                                # glugs while pouring
    n = int(.11 * SR); s = np.arange(n) / SR; f0 = 260 + 40 * np.sin(k)
    m.place(ft(T["spillCU"]) + k * .12, np.sin(2 * np.pi * (f0 + 300 * s) * s) * np.exp(-s * 30) * .6 + bp(m.noise(n), 400, 2500) * np.exp(-s * 40) * .4, .14, .2, .3)
n = int(1.3 * SR); u = np.linspace(0, 1, n); m.place(ft(T["spillCU"] + 4), bp(m.noise(n), 500, 3000) * np.sin(np.pi * u) * (1 + .4 * np.sin(2 * np.pi * 11 * u)), .1, .2, .3)  # spreading
for k in range(4): m.place(ft(T["spillCU"] + 24) + k * .23, np.sin(2 * np.pi * 900 * np.arange(int(.05 * SR)) / SR) * np.exp(-np.arange(int(.05 * SR)) / SR * 80), .07, .3, .4)  # drips
# 5) keyboard typing + search whirr + MATCH FOUND stab (a hit + low brass-like chord, no beeps)
for k in range(7):
    n = int(.04 * SR); s = np.arange(n) / SR; m.place(ft(T["screen"] + 6 + k * 3) + m.rng.uniform(0, .02), bp(m.noise(n), 1500, 6000) * np.exp(-s * 120), .25, .1, .2)
n = int(.8 * SR); s = np.arange(n) / SR; m.place(ft(T["screen"] + 34), bp(m.noise(n), 800, 3000) * .3, .06, 0, .2)
m.hit(ft(T["screen"] + 60), .5); m.thump(ft(T["screen"] + 60), .6, 45)
n = int(1.6 * SR); s = np.arange(n) / SR; stab = sum(np.sin(2 * np.pi * hz(p) * s) + .3 * np.sin(4 * np.pi * hz(p) * s) for p in (45, 52, 57, 60)) * np.exp(-s * 2.2)
m.place(ft(T["screen"] + 60), lp(stab, 1800) * .25, .4, 0, .5)
# 6) Loftus: whoosh in; outside: footsteps on the wet street, a distant siren swell
m.whoosh(ft(T["loftus"]) - .3, g=.12); m.whoosh(ft(T["ext"]) - .3, g=.12)
for k in range(9): m.step(ft(T["ext"] + 6 + k * 16), .22, .1)
n = int(4 * SR); s = np.arange(n) / SR; m.place(ft(T["ext"] + 20), np.sin(2 * np.pi * (650 + 180 * np.sin(2 * np.pi * .7 * s)) * s) * np.sin(np.pi * s / 4) * .2, .05, .7, .8)
# 7) title: boom + shimmer
m.thump(ft(T["title"]), 1.0, 34); m.hit(ft(T["title"]), .3); m.whoosh(ft(T["title"]) - .5, d=.8, g=.2)
n = int(3 * SR); s = np.arange(n) / SR; m.place(ft(T["title"]), sum(np.sin(2 * np.pi * hz(p) * s) for p in (69, 76, 81, 88)) * np.exp(-s * 1.2) * .2, .25, 0, .8)
# score: tense minor pad for the room, music-box motif in the memory, warm swell for the title
m.score([[45, 48, 52], [41, 45, 48], [43, 47, 50], [40, 44, 47]], bar=3.2, gain=.035, piano=False, start=ft(40), end=ft(T["rew"]))
motif = [76, 79, 83, 81, 79, 76, 74, 76]
for k in range(int((ft(T["tip"]) - ft(T["rew"])) / .55)):
    t0 = ft(T["rew"]) + .3 + k * .55; n = int(1.6 * SR); s = np.arange(n) / SR; p = motif[k % len(motif)]
    m._mus(t0, (np.sin(2 * np.pi * hz(p) * s) + .25 * np.sin(2 * np.pi * hz(p) * 3.01 * s)) * np.exp(-s * 3.5), .05, .3 * (-1) ** k)
m.score([[45, 48, 52], [41, 45, 48], [43, 47, 50], [40, 43, 47]], bar=3.0, gain=.035, piano=True, start=ft(T["tip"]), end=ft(T["title"]))
m.score([[45, 52, 57, 60], [41, 48, 53, 57]], bar=2.0, gain=.06, piano=True, start=ft(T["title"]), end=ft(T["end"]))
# voices (Okafor slightly roomy, everyone dry)
for k in ("okafor1", "okafor2", "n1", "n2", "lina1", "lina2", "lina3", "n3", "n4", "n5"): m.vo_line(f"c1_{k}", T[k])
m.render(f"{ROOT}/public/c1.wav")
