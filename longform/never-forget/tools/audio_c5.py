#!/usr/bin/env python3
"""Chapter 5 sound: Grandma's warm apartment (kettle hiss, birds, the record player's crackle + an ORIGINAL old-time
waltz on a music box), rolling pin thumps, shuffled cards, then the forgetting: the music detunes and thins out, the
fridge hum + door, the room going quiet as the light fades, a clinic room tone, and the two minds (a soft tone that
loses notes as Ayla's doors go dark). Timeline = same formulas as src/Chapter5.tsx."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c5"); T = {}
T["n1"] = 14; T["n2"] = T["n1"] + D["n1"] + 8; T["ayla1"] = T["n2"] + D["n2"] + 8; T["n3"] = T["ayla1"] + D["ayla1"] + 16; T["n4"] = T["n3"] + D["n3"] + 6
T["ayla2"] = T["n4"] + D["n4"] + 10; T["hale1"] = T["ayla2"] + D["ayla2"] + 16; T["n5"] = T["hale1"] + D["hale1"] + 16; T["end"] = T["n5"] + D["n5"] + 60
print("end", T["end"])
m = Mix(T["end"], seed=51); N = m.N
def sec(a, b, fade=6): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
home = sec(0, T["hale1"])
m.bed(lp(m.noise(N), 300), home, .03)
m.bed(hp(m.noise(N), 3000) * (np.abs(m.noise(N)) > 2.6), sec(0, T["n3"]), .02)                  # record crackle
for k in range(6):                                                                              # birds at the window
    t0 = m.rng.uniform(0, ft(T["n3"])); n = int(.25 * SR); s = np.arange(n) / SR
    m.place(t0, np.sin(2 * np.pi * (3000 + 700 * np.sin(2 * np.pi * 15 * s)) * s) * np.exp(-s * 14), .012, -.6, .5)
for k in range(int(ft(T["n2"] - T["n1"]) / .55)): m.thump(ft(T["n1"]) + k * .55, .06, 90)      # rolling pin
for k in range(10):
    n = int(.04 * SR); s = np.arange(n) / SR; m.place(ft(T["n2"] + round(D["n2"] * .62)) + k * .05, bp(m.noise(n), 1200, 6000) * np.exp(-s * 70), .1, .2, .3)
# the waltz (our own melody, 3/4) on a music box: warm until the forgetting starts, then it detunes and drops notes
waltz = [72, 76, 79, 77, 76, 74, 72, 74, 76, 72, 69, 71, 72, 76, 79, 81, 79, 77, 76, 74, 72]
beat = .42; k = 0; t = .3
while t < ft(T["hale1"]):
    fading = t > ft(T["n3"]); drop = fading and m.rng.random() < min(.7, (t - ft(T["n3"])) / 8)
    if not drop:
        p = waltz[k % len(waltz)]; det = 1 + (m.rng.uniform(-.02, .02) if fading else 0)
        n = int(1.4 * SR); s = np.arange(n) / SR
        m._mus(t, (np.sin(2 * np.pi * hz(p) * det * s) + .25 * np.sin(2 * np.pi * hz(p) * 3.01 * s)) * np.exp(-s * 3.2), .05 if not fading else .035, .2)
        if k % 3 == 0: m._mus(t, np.sin(2 * np.pi * hz(p - 24) * s) * np.exp(-s * 2), .035, -.2)
    k += 1; t += beat * (1.15 if fading else 1)
# fridge door + hum, calendar stamp, time-lapse whoosh of the lost afternoon
n4a = T["n4"] + round(D["n4"] * .3); n4b = T["n4"] + round(D["n4"] * .62)
n = int(.4 * SR); s = np.arange(n) / SR; m.place(ft(T["n4"]) + .1, bp(m.noise(n), 200, 1500) * np.exp(-s * 10), .15, 0, .3)
m.bed(np.sin(2 * np.pi * 60 * m.t) + .3 * np.sin(2 * np.pi * 120 * m.t), sec(T["n4"], n4a), .015)
m.thump(ft(n4a + 18), .3, 60)
n = int(ft(T["ayla2"] - n4b) * SR); u = np.linspace(0, 1, n); m.place(ft(n4b), bp(m.noise(n), 300, 3000) * u * (1 - u) * 2, .05, 0, .6)
# clinic: cool room tone + the light box hum
m.bed(lp(m.noise(N), 500) + .3 * np.sin(2 * np.pi * 100 * m.t), sec(T["hale1"], T["n5"]), .03)
# two minds: a sustained chord that loses notes as Ayla's doors go dark
for i, p in enumerate((57, 64, 69, 72, 76, 79)):
    a, b = ft(T["n5"]), ft(T["end"]); dur = (b - a) * (1 - i * .13); n = int(dur * SR); s = np.arange(n) / SR
    m._mus(a, np.sin(2 * np.pi * hz(p) * s) * np.minimum(1, s / 1.5) * np.minimum(1, (dur - s) / 1.0), .025, .3 * (-1) ** i)
for k in ("n1", "n2", "ayla1", "n3", "n4", "ayla2", "hale1", "n5"): m.vo_line(f"c5_{k}", T[k])
m.render(f"{ROOT}/public/c5.wav")
