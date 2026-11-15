#!/usr/bin/env python3
"""One audio builder for every chapter: reads src/plan.json + the voice lengths (src/vo_cN.ts), rebuilds the same
timeline as src/Player.tsx, places the voice lines (radio/phone band-passed), an original mood score, ambience beds
and synthesized SFX from the cue table below, then renders public/cN.wav (two-pass loudnorm −14 LUFS).
  python3 tools/audio.py c1 [c2 ...]      (no args = all chapters)"""
import sys, json, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio_lib import *

PLAN = json.load(open(f"{ROOT}/src/plan.json"))
def timeline(ch):
    D = meta(ch); T = {}; t = 0
    for b in PLAN[ch]:
        k = b.get("key") or b["id"]; dur = D.get(b["id"], 60) if b.get("id") else b.get("hold", 30)
        line = t + b.get("pre", 0); e = line + dur + b.get("post", 0); T[k] = dict(s=t, line=line, dur=dur, e=e); t = e
    return T, t

# ---------------- synthesized SFX atoms (all original) ----------------
def env_ad(n, a=.005, d=.2):
    s = np.arange(n) / SR; return np.minimum(1, s / max(a, 1e-4)) * np.exp(-s / max(d, 1e-4))
def tone(f, d, partials=((1, 1),), dec=3.):
    n = int(d * SR); s = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * p * s) for p, a in partials) * np.exp(-s * dec)
class Z(Mix):
    def groan(self, t0, f0=95, d=1.6, g=.12, pan=0.):
        n = int(d * SR); s = np.arange(n) / SR; f = f0 * (1 - .25 * s / d) * (1 + .03 * np.sin(2 * np.pi * 5.5 * s))
        src = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .5 + self.noise(n) * .35
        y = bp(src, 500, 900) * 1.2 + bp(src, 1000, 1300) * .6 + lp(src, 300) * .5
        e = np.minimum(1, s / .35) * np.minimum(1, (d - s) / .4); self.place(t0, y * e, g, pan, .45)
    def crowd(self, a, b, n=12, g=.06, f0=90):
        for i in range(n): self.groan(a + self.rng.random() * max(.1, b - a - 1.5), f0 * (.8 + .5 * self.rng.random()), 1.2 + self.rng.random() * 1.6, g * (.6 + .6 * self.rng.random()), self.rng.uniform(-.7, .7))
    def slap(self, t0, g=.4, pan=0.):
        n = int(.5 * SR); s = np.arange(n) / SR
        y = bp(self.noise(n), 700, 6000) * np.exp(-s * 35) + np.sin(2 * np.pi * 90 * s) * np.exp(-s * 25) * .8 + sum(np.sin(2 * np.pi * f * s) * np.exp(-s * 9) * .12 for f in (2130, 3410, 5220))
        self.place(t0, y, g, pan, .4)
    def knock(self, t0, g=.6, metal=True):
        n = int(.45 * SR); s = np.arange(n) / SR
        y = np.sin(2 * np.pi * np.cumsum(95 + 60 * np.exp(-s * 40)) / SR) * np.exp(-s * 22) + bp(self.noise(n), 200, 1600) * np.exp(-s * 45) * .7
        if metal: y += sum(np.sin(2 * np.pi * f * s) * np.exp(-s * 7) * .1 for f in (183, 412, 655))
        self.place(t0, y, g, -.1, .5)
    def clang(self, t0, g=.35, pan=.3):
        for k, gg in ((0, 1), (.22, .45), (.37, .2)):
            y = tone(523, .9, ((1, .6), (2.47, .5), (4.22, .4), (6.5, .25)), 6) + bp(self.noise(int(.9 * SR)), 2000, 8000) * np.exp(-np.arange(int(.9 * SR)) / SR * 40) * .4
            self.place(t0 + k, y, g * gg, pan, .6)
    def squeal(self, t0, d=1.0, g=.22):
        n = int(d * SR); s = np.arange(n) / SR; f = 2300 + 900 * s / d
        y = (np.sin(2 * np.pi * np.cumsum(f) / SR) + .4 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * (.7 + .3 * np.sin(2 * np.pi * 13 * s)) + hp(self.noise(n), 2000) * .5
        self.place(t0, y * np.minimum(1, s / .03) * np.minimum(1, (d - s) / .1), g, .1, .3)
    def buzz(self, t0, n_=3, g=.18):
        for k in range(n_):
            n = int(.35 * SR); s = np.arange(n) / SR; self.place(t0 + k * .55, lp(np.sign(np.sin(2 * np.pi * 165 * s)), 900) * np.minimum(1, s / .01) * np.minimum(1, (.35 - s) / .02), g, .2, .1)
    def ring(self, t0, n_=2, g=.12):
        for k in range(n_):
            n = int(1.0 * SR); s = np.arange(n) / SR; y = (np.sin(2 * np.pi * 440 * s) + np.sin(2 * np.pi * 480 * s)) * (np.sin(2 * np.pi * 20 * s) > 0) * np.minimum(1, (1 - s) / .05)
            self.place(t0 + k * 1.5, bp(y, 300, 3400), g, .2, .1)
    def alert(self, t0, d=2.4, g=.14):
        n = int(d * SR); s = np.arange(n) / SR; y = (np.sin(2 * np.pi * 853 * s) + np.sin(2 * np.pi * 960 * s)) * ((s * 2.5) % 1 < .75)
        self.place(t0, y * np.minimum(1, (d - s) / .05), g, 0, .2)
    def honk(self, t0, g=.12, f=400, d=.45, pan=0.):
        n = int(d * SR); s = np.arange(n) / SR; y = lp(np.sign(np.sin(2 * np.pi * f * s)) + np.sign(np.sin(2 * np.pi * f * 1.26 * s)), 2500)
        self.place(t0, y * np.minimum(1, s / .01) * np.minimum(1, (d - s) / .03), g, pan, .4)
    def slam(self, t0, g=.5):
        self.thump(t0, g, 55); n = int(.8 * SR); s = np.arange(n) / SR; self.place(t0, sum(np.sin(2 * np.pi * f * s) * np.exp(-s * 6) * .15 for f in (220, 347, 590)) + bp(self.noise(n), 300, 3000) * np.exp(-s * 30), g, 0, .5)
    def click(self, t0, g=.2):
        n = int(.05 * SR); s = np.arange(n) / SR; self.place(t0, bp(self.noise(n), 2000, 8000) * np.exp(-s * 120), g, .2, .2)
    def bolt(self, t0, g=.35):
        self.click(t0, g); self.click(t0 + .12, g * .8); n = int(.25 * SR); s = np.arange(n) / SR; self.place(t0 + .1, tone(800, .25, ((1, .5), (2.3, .3)), 20), g * .6, 0, .3)
    def keys(self, t0, g=.15):
        for k in range(7): self.place(t0 + k * .045 + self.rng.random() * .02, tone(3000 + self.rng.random() * 3000, .2, ((1, 1), (1.6, .5)), 25), g, .2, .4)
    def screech(self, t0, g=.12):
        for k in range(6):
            n = int(.07 * SR); s = np.arange(n) / SR; f = 6500 - 2500 * s / .07; self.place(t0 + k * .09, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * s / .07), g, .3, .4)
    def marker(self, t0, d=1.5, g=.06):
        k = 0.
        while k < d: n = int(.12 * SR); s = np.arange(n) / SR; self.place(t0 + k, bp(self.noise(n), 2500, 6000) * np.sin(np.pi * s / .12), g, -.2, .2); k += .14 + self.rng.random() * .1
    def heart(self, a, b, bpm=70, g=.4):
        t = a
        while t < b: self.thump(t, g, 42); t += 60 / bpm
    def steps(self, a, b, every=.32, g=.18):
        t = a
        while t < b: self.step(t, g, self.rng.uniform(-.2, .2)); t += every
    def jet(self, t0, d=5., g=.25):
        n = int(d * SR); s = np.arange(n) / SR; self.place(t0, lp(self.noise(n), 1200 ) * np.minimum(1, s / 1.5) * np.minimum(1, (d - s) / 1.5) + bp(self.noise(n), 3000, 7000) * .15 * np.minimum(1, s / 2), g, 0, .4)
    def riser(self, t0, d=3., g=.12):
        n = int(d * SR); s = np.arange(n) / SR; self.place(t0, sum(np.sin(2 * np.pi * np.cumsum(f * (1 + s / d)) / SR) for f in (55, 82.5, 110)) * (s / d) ** 2, g, 0, .6)
    # ---- ambience beds (between seconds a and b, faded)
    def amb(self, kind, a, b, g=1.):
        e = self.env([(0, 0), (max(0, a * FPS - 12), 0), (a * FPS, 1), (b * FPS, 1), (b * FPS + 12, 0), (self.N / SR * FPS + 1, 0)]); N = self.N
        if kind == "store": self.bed(np.sin(2 * np.pi * 60 * self.t) * .3 + np.sin(2 * np.pi * 120 * self.t) * .12 + lp(self.noise(N), 400) * .4, e, .05 * g)
        if kind == "night": self.bed(lp(self.noise(N), 500), e, .05 * g, x2=lp(self.noise(N), 500))
        if kind == "wind": self.bed(lp(self.noise(N), 600) * (.6 + .4 * np.sin(2 * np.pi * .13 * self.t)), e, .07 * g, x2=lp(self.noise(N), 600) * (.6 + .4 * np.cos(2 * np.pi * .11 * self.t)))
        if kind == "airport": self.bed(bp(self.noise(N), 300, 2500) * (.6 + .4 * np.sin(2 * np.pi * .4 * self.t) * np.sin(2 * np.pi * .23 * self.t)), e, .08 * g, x2=bp(self.noise(N), 300, 2500))
        if kind == "kitchen":
            self.bed(lp(self.noise(N), 300), e, .02 * g)
            t = a
            while t < b - .3:
                for k in range(3): self.place(t + k * .09, tone(3800 + self.rng.random() * 1500, .07, ((1, 1),), 30), .05 * g, .6, .5)
                t += 1.2 + self.rng.random() * 2.5
        if kind == "highway": self.bed(lp(self.noise(N), 250), e, .1 * g, x2=lp(self.noise(N), 250))
        if kind == "engine": self.bed(lp(self.noise(N), 120) * 1.5 + np.sin(2 * np.pi * 48 * self.t + np.sin(2 * np.pi * 3 * self.t)) * .3, e, .09 * g)
        if kind == "static": self.bed(hp(self.noise(N), 1500) * (.7 + .3 * (self.rng.random(N) > .997)), e, .035 * g)
        if kind == "fire":
            self.bed(lp(self.noise(N), 300), e, .03 * g)
            for k in range(int((b - a) * 8)): self.click(a + self.rng.random() * (b - a), .05 * g)
        if kind == "er": self.bed(bp(self.noise(N), 400, 2500) * .6, e, .05 * g); [self.chime(a + k * 1.1, 88, .03 * g) for k in range(int((b - a) / 1.1))]
        if kind == "barn": self.bed(lp(self.noise(N), 500) * (.6 + .4 * np.sin(2 * np.pi * .09 * self.t)), e, .06 * g)

# ---------------- original music ----------------
def music(m, mood, a, b, g=1.):
    if b - a < .5: return
    if mood == "tense":
        n = int((b - a) * SR); s = np.arange(n) / SR; fade = np.minimum(1, s / 1.5) * np.minimum(1, (b - a - s) / 1.0)
        dr = sum(np.sin(2 * np.pi * f * s * (1 + .002 * np.sin(2 * np.pi * .2 * s + f))) for f in (55, 82.4, 58.3)) / 3
        m._mus(a, lp(dr, 600) * fade, .06 * g); hi = sum(np.sin(2 * np.pi * f * s) for f in (659, 698)) * (.5 + .5 * np.sin(2 * np.pi * .07 * s)) * fade
        m._mus(a, hi, .006 * g, .3)
    elif mood == "warm":      # music box: original 8-bar tune in C major over a soft pad
        m.score([[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]], bar=2.4, gain=.03 * g, piano=False, start=a, end=b)
        tune = [76, 79, 81, 79, 76, 74, 72, 74, 76, 76, 74, 72, 74, 79, 77, 76]; t = a + .3; k = 0
        while t < b - 1: p = tune[k % 16]; m._mus(t, tone(hz(p), 1.4, ((1, 1), (3.01, .22)), 3.2), .045 * g, .2 * (-1) ** k); t += .6; k += 1
    elif mood == "mystery": m.score([[57, 60, 64, 69], [53, 57, 60, 65], [50, 53, 57, 62], [52, 56, 59, 64]], bar=3.2, gain=.035 * g, piano=True, start=a, end=b)
    elif mood == "sad": m.score([[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [55, 59, 62, 67]], bar=3.6, gain=.04 * g, piano=True, start=a, end=b, octave=0)
    elif mood == "hope":
        m.score([[62, 66, 69, 74], [59, 62, 66, 71], [55, 59, 62, 67], [57, 61, 64, 69]], bar=2.8, gain=.035 * g, piano=False, start=a, end=b)
        tune = [74, 76, 78, 81, 78, 76, 74, 73, 71, 73, 74, 76]; t = a + .5; k = 0
        while t < b - 1: m._mus(t, tone(hz(tune[k % 12]), 1.6, ((1, 1), (3.01, .2)), 2.8), .04 * g, .2 * (-1) ** k); t += .7; k += 1
    elif mood == "action":
        t = a; k = 0
        while t < b: m.thump(t, .3 * g, 50 if k % 2 == 0 else 70); t += .214; k += 1
        m.riser(a, b - a, .1 * g)

# ---------------- per-chapter cues ----------------
def cues(ch, m, T, END):
    L = lambda k, off=0: (T[k]["line"] + off) / FPS                              # seconds at a line start (+ frames)
    A = lambda k, fr=0.: (T[k]["s"] + (T[k]["e"] - T[k]["s"]) * fr) / FPS       # seconds at a fraction of a beat
    E = lambda k: T[k]["e"] / FPS; end = END / FPS
    V = lambda k, band=None, g=1.: m.vo_line(f"{ch}_{k}", T[k]["line"], g, band)
    R = (350, 3400)                                                                # phone / radio band
    if ch == "c1":
        m.amb("store", 0, A("title")); m.crowd(0, A("title"), 26, .07); music(m, "tense", 0, A("title"))
        m.place(0.2, lp(m.noise(int(1.2 * SR)), 900) * np.exp(-np.arange(int(1.2 * SR)) / SR * 2), .15)   # cart roll
        m.thump(A("open", .85), .4, 60)
        for i in range(14): m.slap(A("slap") + i * .11 + m.rng.random() * .05, .35, m.rng.uniform(-.6, .6))
        m.slap(A("n2", .5), .3, .4); m.click(A("hush", .45), .3); m.heart(A("hush"), A("n4"), 64, .35)
        m.riser(A("n4"), E("n4") - A("n4") + .3, .14); m.hit(A("title"), .45); m.whoosh(A("n3") - .2); m.whoosh(A("n3", .5) - .2)
        for k in ("n1", "n2", "mira1", "kai1", "n3", "n4"): V(k)
    if ch == "c2":
        m.amb("kitchen", 0, end); music(m, "warm", 0, A("n2", .45)); music(m, "mystery", A("n2", .45), end, .8)
        m.keys(L("mom1", 20)); m.place(A("n2", .5), bp(m.noise(int(2 * SR)), 300, 3000) * .3 * np.sin(np.pi * np.arange(int(2 * SR)) / SR / 2), .05)
        for k in ("n1", "mom1", "mira1", "mom2", "kai1", "n2"): V(k)
    if ch == "c3":
        m.amb("wind", 0, A("n2")); m.amb("barn", A("n2"), A("fact1")); music(m, "mystery", 0, end)
        m.screech(A("n2", .38)); m.thump(A("n2", .42), .3, 80); m.screech(A("n3", .4), .08)
        m.place(A("fact1"), bp(m.noise(int((E("n4") - A("fact1")) * SR)), 60, 300) * .5, .05)        # micro hum
        m.heart(A("n4"), E("n4"), 120, .3); m.jet(A("n5"), E("n5") - A("n5") + .5, .3)
        for k in ("n1", "n2", "n3", "fact1", "n4", "n5"): V(k)
    if ch == "c4":
        m.amb("airport", 0, A("n4")); music(m, "mystery", 0, A("n3")); music(m, "tense", A("n3"), end)
        m.chime(A("n1", .55), 79, .05); m.chime(A("n1", .55) + .4, 84, .05); m.heart(A("n2"), E("n2"), 90, .25)
        m.hit(A("n3") + 1.0, .3); m.groan(A("n3") + .9, 120, 1.0, .15); m.riser(A("n4"), E("n4") - A("n4"), .1)
        for k in ("n1", "fact1", "n2", "n3", "n4"): V(k)
    if ch == "c5":
        music(m, "mystery", 0, A("n3")); m.amb("store", A("n3"), end, .6); m.buzz(L("n3", 50), 4)
        m.ring(A("ring") + .1, 1); m.amb("er", A("mom1"), E("mom1")); m.amb("er", A("mom2"), E("mom2"))
        m.click(A("dead") + .2, .3); music(m, "sad", A("dead"), end); m.heart(A("mom1"), E("mom2"), 80, .25)
        for k in ("n1", "fact1", "n2", "n3", "kai1", "kai2", "n4"): V(k)
        V("mom1", R); V("mom2", R)
    if ch == "c6":
        m.amb("wind", 0, A("n2")); m.amb("highway", A("n2"), A("n4")); m.amb("wind", A("n4"), end); music(m, "tense", 0, end, .8)
        m.steps(A("n1"), A("n1", .45), .2, .2); m.alert(A("n1", .58) + .1)
        for i in range(10): m.honk(A("n2") + i * .9 + m.rng.random() * .5, .1, 380 + m.rng.random() * 100, .3 + m.rng.random() * .4, m.rng.uniform(-.7, .7))
        for k in ("n1", "mira1", "kai1", "n2", "fact1", "n3", "n4"): V(k)
    if ch == "c7":
        m.amb("store", 0, end, .7); music(m, "mystery", A("n1"), A("n3")); music(m, "tense", A("n3"), end)
        m.keys(A("dock") + .1); m.bolt(A("dock", .3)); m.place(A("dock", .35), lp(m.noise(int(.8 * SR)), 600) * np.exp(-np.arange(int(.8 * SR)) / SR * 3), .12)
        m.marker(A("n1", .5) + .4, 2.4); [m.slap(A("n3") + 1 + i * .3, .3, m.rng.uniform(-.5, .5)) for i in range(5)]; m.crowd(A("n3"), end, 8, .06)
        for k in ("ruiz1", "kai1", "ruiz2", "n1", "fact1", "n2", "n3"): V(k)
    if ch == "c8":
        m.amb("wind", 0, A("n4")); m.amb("store", A("n4"), end); music(m, "mystery", 0, A("ruiz1")); m.crowd(0, A("n4"), 8, .04)
        t_can = A("n2") + (10 + 2 + 24) / FPS; m.whoosh(A("n2") + 12 / FPS, .4, .1); m.clang(t_can, .35, .3); m.crowd(t_can + .3, t_can + 3, 10, .07)
        m.marker(A("n4") + .3, E("n4") - A("n4") - .5)
        for i, k in enumerate((0, 10, 20)): m.knock(A("knock") + k / FPS, .55)
        m.knock(L("ruiz2", -20), .4)
        for k in ("n1", "n2", "n3", "n4", "fact1", "ruiz1", "kai1", "ruiz2"): V(k)
    if ch == "c9":
        m.amb("store", 0, end, .6); music(m, "tense", 0, A("dana2")); music(m, "sad", A("dana2"), end, .7)
        for k in (0, 10, 20): m.knock(A("knock") + k / FPS, .6)
        m.heart(A("n1"), E("check"), 76, .3); m.bolt(A("check") + .1); m.click(A("check", .5), .2)
        for k in ("dana1", "ruiz1", "kai1", "n1", "n2", "dana2"): V(k)
    if ch == "c10":
        m.amb("store", 0, end, .5); m.amb("fire", 0, end, .5); music(m, "mystery", 0, A("mira1")); music(m, "sad", A("mira1"), end)
        m.marker(A("dana1") + .3, E("dana1") - A("dana1") - .5); m.place(A("fact1"), lp(m.noise(int(6 * SR)), 2000) * .2, .03)
        for k in ("dana1", "n1", "fact1", "fact2", "mira1", "dana2", "n2"): V(k)
    if ch == "c11":
        m.amb("night", 0, end); music(m, "mystery", 0, A("holt1")); m.amb("static", A("static"), E("holt1"))
        m.click(A("n1", .55) + .5, .2); m.click(A("static") + .3, .3); music(m, "hope", A("holt1", .5), A("kai1"), .8); music(m, "tense", A("n2"), end, .8)
        m.crowd(A("n2"), end, 5, .05)
        for k in ("n1", "fact1", "fact2", "fact3", "kai1", "ruiz1", "n2"): V(k)
        V("holt1", R, .9)
    if ch == "c12":
        m.amb("night", 0, A("n3")); music(m, "tense", 0, A("squeal")); m.crowd(0, A("squeal"), 6, .04)
        m.steps(A("n1"), E("n2"), .5, .08); m.squeal(A("squeal") + .05, .9, .25); m.crowd(A("squeal") + .4, A("n3"), 30, .09, 110)
        music(m, "action", A("kai1"), A("run", .95)); m.steps(A("ruiz1"), A("run", .8), .16, .22)
        m.slam(A("run", .62)); m.groan(A("run", .45), 130, 1.0, .2); m.place(A("run", .95), np.zeros(10), 0)
        m.amb("engine", A("n3"), end); music(m, "sad", A("ruiz2"), end); m.slam(A("n4", .15), .3)
        for k in ("n1", "n2", "kai1", "ruiz1", "n3", "ruiz2", "dana1", "ruiz3", "n4", "mira1", "kai2"): V(k)
    if ch == "c13":
        m.amb("engine", 0, end); m.amb("wind", 0, end, .6); music(m, "hope", 0, end, .9)
        for k in ("n1", "fact1", "n2", "n3"): V(k)
    if ch == "c14":
        m.amb("wind", 0, end); m.amb("fire", A("n2"), end, .6); music(m, "hope", 0, A("mira1")); music(m, "mystery", A("n4"), end)
        m.place(0.3, lp(m.noise(int(3 * SR)), 300) * np.linspace(1, 0, int(3 * SR)), .2); m.click(L("holt1", -6), .25); m.hit(A("mira1"), .25)
        for k in ("n1", "holt1", "n2", "n3", "mira1", "n4"): V(k)
    if ch == "c15":
        m.amb("fire", 0, A("n2"), .5); m.steps(0, A("n1"), .18, .2); music(m, "tense", A("n1"), A("part2"))
        m.heart(A("page"), E("n3"), 60, .4); m.marker(L("n3") + .1, 1.3, .05); m.screech(A("n3", .62), .1)
        m.hit(A("part2"), .55); m.thump(A("part2"), .8, 34); music(m, "warm", A("n4"), end, .9)
        for k in ("n1", "n2", "n3", "n4"): V(k)

def build(ch):
    T, END = timeline(ch); m = Z(END, seed=int(ch[1:]) * 7)
    cues(ch, m, T, END); m.render(f"{ROOT}/public/{ch}.wav"); print(ch, "frames", END, f"{END / FPS:.1f}s")

if __name__ == "__main__":
    for ch in (sys.argv[1:] or [f"c{i}" for i in range(1, 16)]): build(ch)
