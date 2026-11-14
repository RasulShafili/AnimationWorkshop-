#!/usr/bin/env python3
"""Chapter 7 sound: the care home (soft room tone, snow-muffled quiet, a distant clock-free hum), Lina's breath, the
gold swell into the palace and running footsteps on marble, door opening into the remembered kitchen where Ayla HUMS
the waltz (our own melody, sung as a soft synth hum), Lina humming the same waltz in the care home, the rhythm
taps, a warm string-like swell when Ayla comes back, laughter (soft), the cold fade, pills down the drain, and the
waltz on piano + music box for the seasons montage. Timeline = same formulas as src/Chapter7.tsx."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *
D = meta("c7"); T = {}
T["ayla3"] = 30; T["n1"] = T["ayla3"] + D["ayla3"] + 16; T["n2"] = T["n1"] + D["n1"] + 6; T["run"] = T["n2"] + D["n2"] + 8; T["n3"] = T["run"] + 30
T["mem"] = T["n3"] + D["n3"] + 4; T["n4"] = T["mem"] + 64; T["hum"] = T["n4"] + D["n4"] + 24; T["ayla4"] = T["hum"] + 210; T["n6"] = T["ayla4"] + D["ayla4"] + 16
T["n7"] = T["n6"] + D["n6"] + 10; T["n8"] = T["n7"] + D["n7"] + 18; T["n9"] = T["n8"] + D["n8"] + 6; T["end"] = T["n9"] + D["n9"] + 160
print("end", T["end"])
m = Mix(T["end"], seed=71); N = m.N
def sec(a, b, fade=6): return m.env([(0, 0), (max(0, a - fade), 0), (a, 1), (b, 1), (b + fade, 0), (T["end"], 0)])
WALTZ = [72, 76, 79, 77, 76, 74, 72, 74, 76, 72, 69, 71, 72, 76, 79, 81, 79, 77, 76, 74, 72]
def hum(t0, beats, g, base=0, beat=.42, voice=1.0):
    """a soft hummed voice (vibrato + nasal formant) singing the waltz from t0"""
    for k in range(beats):
        p = WALTZ[k % len(WALTZ)] + base; dur = beat * (2 if k % 3 == 2 else 1) * .98; n = int(dur * SR); s = np.arange(n) / SR
        f0 = hz(p) * (1 + .006 * np.sin(2 * np.pi * 5.2 * s)); ph = 2 * np.pi * np.cumsum(f0) / SR
        y = (np.sin(ph) + .45 * np.sin(2 * ph) + .2 * np.sin(3 * ph)) * np.minimum(1, s / .06) * np.minimum(1, (dur - s) / .08)
        m.voice_arr = None
        yv = bp(y, 180, 1400) * voice; a = int((t0 + k * beat) * SR); b = min(N, a + len(yv)); m.vo[a:b] += yv[:b - a] * g
care = np.maximum(sec(0, T["run"]), sec(T["hum"], T["n8"]))
m.bed(lp(m.noise(N), 250), care, .035)
m.bed(lp(m.noise(N), 250), sec(T["n9"] + 70, T["end"]), .02)
n = int(1.2 * SR); s = np.arange(n) / SR; m.place(ft(T["n1"]) + .4, bp(m.noise(n), 300, 1500) * np.sin(np.pi * s / 1.2) * .5, .05, -.2, .3)      # a shaky breath
# gold swell → palace, running steps on marble with reverb, door opens into the memory
n = int(1.6 * SR); s = np.arange(n) / SR; m.place(ft(T["run"]) - 1.2, sum(np.sin(2 * np.pi * hz(p) * (1 + .4 * s / 1.6) * s) for p in (76, 83, 88, 95)) * np.exp(-((s - 1.3) ** 2) / .2) * .25, .35, 0, .7)
m.thump(ft(T["run"]), .6, 38)
m._mus(0, lp(sum(np.sin(2 * np.pi * hz(p) * m.t * (1 + .003 * np.sin(2 * np.pi * 5 * m.t + p))) for p in (57, 64, 69, 72)) / 4, 2500) * sec(T["run"], T["mem"]), .05)
stopAt = T["n3"] + D["n3"] - 40
for k in range(int((stopAt - T["n3"]) / 8)): m.step(ft(T["n3"] + k * 8), .2, -.1)
for k in range(4):
    n = int(.7 * SR); s = np.arange(n) / SR; m.place(ft(stopAt + 8) + k * .1, np.sin(2 * np.pi * (160 + 30 * k + 40 * np.sin(2 * np.pi * 6 * s)) * s) * np.sin(np.pi * s / .7) * .3, .06, .3, .8)
# the memory: kitchen, Ayla hums the waltz (quiet, a little far), record crackle
m.bed(hp(m.noise(N), 3000) * (np.abs(m.noise(N)) > 2.6), sec(T["mem"], T["hum"]), .02)
hum(ft(T["mem"] + 6), 14, .10, base=-5, voice=.9)
# Lina hums the same waltz in the care home (a little higher, closer)
hum(ft(T["hum"] + 6), 15, .16, base=0)
for k in range(10): m.thump(ft(T["hum"] + 80 + k * 13), .05, 120)                     # fingers tapping the armrest
# Ayla comes back: warm swell (string-like pad), soft laughter, then cold fade
m._mus(0, lp(sum(np.sin(2 * np.pi * hz(p) * m.t * (1 + .004 * np.sin(2 * np.pi * 5.5 * m.t + p))) for p in (60, 64, 67, 72, 76)) / 5, 3000) * sec(T["hum"] + 150, T["n7"] + 20, 40), .07)
for k in range(6):
    n = int(.25 * SR); s = np.arange(n) / SR; m.place(ft(T["n6"]) + .3 + k * .45, bp(m.noise(n), 400, 2500) * np.exp(-s * 10) * (1 + np.sin(2 * np.pi * 9 * s)), .03, (-1) ** k * .3, .4)
# pills: rattle, pour, water swirl into the drain
for k in range(8):
    n = int(.05 * SR); s = np.arange(n) / SR; m.place(ft(T["n8"] + 12) + k * .07, bp(m.noise(n), 2500, 8000) * np.exp(-s * 70), .08, .2, .3)
n = int(2.2 * SR); u = np.linspace(0, 1, n); m.place(ft(T["n8"] + 4), bp(m.noise(n), 300, 2500) * np.sin(np.pi * u) * (1 + .5 * np.sin(2 * np.pi * 3 * u)), .08, 0, .3)
# score: sad piano in the care home; the waltz on piano + music box for the seasons montage (resolution)
m.score([[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]], bar=3.0, gain=.03, piano=True, start=0, end=ft(T["run"]))
m.score([[57, 60, 64], [52, 55, 59]], bar=3.0, gain=.025, piano=True, start=ft(T["n7"]), end=ft(T["n9"]))
k = 0; t = ft(T["n9"]) + .2
while t < ft(T["end"]) - 1:
    p = WALTZ[k % len(WALTZ)]; n = int(1.6 * SR); s = np.arange(n) / SR
    m._mus(t, (np.sin(2 * np.pi * hz(p) * s) + .25 * np.sin(2 * np.pi * hz(p) * 3.01 * s)) * np.exp(-s * 3), .05, .2)
    if k % 3 == 0: m._mus(t, (np.sin(2 * np.pi * hz(p - 24) * s) + .3 * np.sin(2 * np.pi * hz(p - 12) * s)) * np.exp(-s * 1.5), .05, -.2)
    k += 1; t += .44
for k in ("ayla3", "n1", "n2", "n3", "n4", "ayla4", "n6", "n7", "n8", "n9"): m.vo_line(f"c7_{k}", T[k])
m.render(f"{ROOT}/public/c7.wav")
