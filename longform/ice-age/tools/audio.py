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
    # ---- ice age SFX (all synthesized)
    def trumpet(self, t0, g=.4, far=False):      # mammoth: rising brassy formant blare with growl
        d = 1.8; n = int(d * SR); s = np.arange(n) / SR; f = 210 + 260 * np.minimum(1, s / .35) - 60 * np.maximum(0, s - 1.1)
        src = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (1 + .3 * np.sin(2 * np.pi * 31 * s)) + self.noise(n) * .25
        y = bp(src, 600, 1400) + bp(src, 1800, 2600) * .5 + lp(src, 400) * .4; e = np.minimum(1, s / .08) * np.minimum(1, (d - s) / .5)
        y = y * e; y = lp(y, 1500) * .6 if far else y; self.place(t0, y, g * (.5 if far else 1), .2, .6 if far else .35)
    def roar(self, t0, g=.4, far=False):
        d = 2.0; n = int(d * SR); s = np.arange(n) / SR; f = 70 + 40 * np.sin(np.pi * s / d)
        src = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .6 + self.noise(n) * .8
        y = lp(src, 900) + bp(src, 200, 600) * .6; e = np.minimum(1, s / .2) * np.minimum(1, (d - s) / .8)
        self.place(t0, (lp(y, 600) if far else y) * e, g * (.5 if far else 1), -.2, .5)
    def snowsteps(self, a, b, every=.45, g=.1):
        t = a
        while t < b - .1:
            n = int(.14 * SR); self.place(t, bp(self.noise(n), 900, 4000) * env_ad(n, .01, .05), g, self.rng.uniform(-.2, .2), .2); t += every * (.9 + .2 * self.rng.random())
    def mop(self, a, b):
        t = a
        while t < b - .5: n = int(.9 * SR); s = np.arange(n) / SR; self.place(t, bp(self.noise(n), 400, 2500) * np.sin(np.pi * s / .9) ** 2, .05, .3, .3); t += 1.3
    def glowhum(self, a, b):
        n = int((b - a) * SR); s = np.arange(n) / SR; y = sum(np.sin(2 * np.pi * f * s + np.sin(2 * np.pi * .5 * s)) for f in (220, 330, 441))
        self.place(a, y * np.minimum(1, s / 2) * np.minimum(1, (b - a - s) / .5) * (.6 + .4 * np.sin(2 * np.pi * 1.3 * s)), .025, 0, .6)
    def flash(self, t0):
        self.hit(t0, .5); n = int(2.5 * SR); s = np.arange(n) / SR; self.place(t0, hp(self.noise(n), 2000) * np.exp(-s * 1.6), .12, 0, .7)
    def dig(self, a, b):
        t = a
        while t < b - .2: n = int(.25 * SR); self.place(t, lp(self.noise(n), 1500) * env_ad(n, .02, .08), .14, self.rng.uniform(-.3, .3), .2); t += .45 + .2 * self.rng.random()
    def rub(self, a, b):
        n = int((b - a) * SR); s = np.arange(n) / SR; y = bp(self.noise(n), 600, 2500) * (.5 + .5 * np.sin(2 * np.pi * 3.2 * s)) ** 2
        self.place(a, y * np.minimum(1, s / .3) * np.minimum(1, (b - a - s) / .3), .07, .1, .2)
    def stones(self, t0):
        for k in range(4): self.place(t0 + k * .18, tone(1800 + 600 * self.rng.random(), .08, ((1, 1), (2.7, .5)), 40), .12, .2, .3)
    def flint(self, t0, g=.4):
        n = int(.12 * SR); self.place(t0, hp(self.noise(n), 3000) * env_ad(n, .001, .02) + tone(2600, .12, ((1, 1), (2.3, .6)), 50), g * .5, .1, .3)
        for k in range(5): self.place(t0 + .02 + k * .015, hp(self.noise(int(.02 * SR)), 6000), g * .15, self.rng.uniform(-.4, .4), .4)
    def whoomp(self, t0):
        n = int(1.2 * SR); s = np.arange(n) / SR; self.place(t0, lp(self.noise(n), 700) * np.minimum(1, s / .1) * np.exp(-s * 2.5), .3, 0, .4)
    def spearup(self, t0):
        for k in range(4): self.place(t0 + k * .12, bp(self.noise(int(.15 * SR)), 500, 3000) * env_ad(int(.15 * SR), .01, .05), .12, -.4 + .25 * k, .3)
    def marker(self, t0, d=1.5, g=.06):
        n = int(d * SR); s = np.arange(n) / SR; self.place(t0, bp(self.noise(n), 2000, 6000) * (.4 + .6 * (np.sin(2 * np.pi * 4 * s) > 0)), g, .2, .2)
    def cough(self, t0):
        for k in range(2): n = int(.22 * SR); self.place(t0 + k * .3, bp(self.noise(n), 300, 1800) * env_ad(n, .01, .07), .1, -.2, .3)
    def boil(self, a, b):
        t = a
        while t < b: self.place(t, tone(400 + 500 * self.rng.random(), .06, ((1, 1),), 60), .04, self.rng.uniform(-.3, .3), .3); t += .05 + .12 * self.rng.random()
    def carve(self, a, b):
        t = a
        while t < b - .3: n = int(.3 * SR); self.place(t, bp(self.noise(n), 2500, 7000) * np.sin(np.pi * np.arange(n) / n), .04, .2, .2); t += .55 + .3 * self.rng.random()
    def slip(self, t0):
        n = int(.5 * SR); self.place(t0, bp(self.noise(n), 1500, 5000) * np.linspace(1, 0, n), .15, .2, .3); self.thump(t0 + .45, .45, 70)
    def cheer(self, t0):
        for k in range(5): self.place(t0 + k * .15, bp(self.noise(int(.8 * SR)), 300, 2000) * env_ad(int(.8 * SR), .05, .3), .1, self.rng.uniform(-.6, .6), .5)
    def crack(self, t0): self.place(t0, hp(self.noise(int(.08 * SR)), 1500) * env_ad(int(.08 * SR), .001, .02), .35, 0, .3)
    def sled(self, a, b):
        n = int((b - a) * SR); s = np.arange(n) / SR; self.place(a, bp(self.noise(n), 800, 3500) * (.6 + .4 * np.sin(2 * np.pi * .9 * s)) * np.minimum(1, s / .5) * np.minimum(1, (b - a - s) / .5), .04, 0, .3)
    def paint(self, a, b):
        t = a
        while t < b - .4: n = int(.5 * SR); self.place(t, bp(self.noise(n), 500, 2500) * np.sin(np.pi * np.arange(n) / n) ** 2, .05, .1, .3); t += .8 + .4 * self.rng.random()
    def powerdown(self, t0):
        n = int(1.0 * SR); s = np.arange(n) / SR; self.place(t0, np.sin(2 * np.pi * np.cumsum(900 * np.exp(-s * 3)) / SR) * np.exp(-s * 2.5), .06, 0, .4)
    def lightson(self, t0):
        for k in range(3): self.place(t0 + k * .25, tone(110, .4, ((1, 1), (2, .5)), 8) + hp(self.noise(int(.4 * SR)), 3000) * .2, .08, -.4 + .4 * k, .3)
    def beep(self, t0): self.place(t0, tone(1760, .15, ((1, 1),), 10), .05, 0, .2)
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
        if kind == "blizzard": self.bed(lp(self.noise(N), 900) * (.55 + .45 * np.sin(2 * np.pi * .17 * self.t) ** 2) + bp(self.noise(N), 2500, 5000) * .15, e, .1 * g, x2=lp(self.noise(N), 900) * (.55 + .45 * np.cos(2 * np.pi * .13 * self.t) ** 2))
        if kind == "museum": self.bed(np.sin(2 * np.pi * 60 * self.t) * .2 + lp(self.noise(N), 250) * .5, e, .04 * g)
        if kind == "cave":
            self.bed(lp(self.noise(N), 200), e, .03 * g); t = a
            while t < b - .3: self.place(t, tone(1400 + 900 * self.rng.random(), .25, ((1, 1),), 18), .035 * g, self.rng.uniform(-.6, .6), .8); t += 1.2 + 2 * self.rng.random()
        if kind == "torch": self.bed(lp(self.noise(N), 350) * (.7 + .3 * np.sin(2 * np.pi * 2.3 * self.t)), e, .03 * g)
        if kind == "river": self.bed(bp(self.noise(N), 300, 2500) * (.8 + .2 * np.sin(2 * np.pi * .3 * self.t)), e, .035 * g, x2=bp(self.noise(N), 300, 2500))
        if kind == "camp":
            self.bed(lp(self.noise(N), 500), e, .03 * g); t = a + 1
            while t < b - 1: self.place(t, bp(self.noise(int(.5 * SR)), 300, 1500) * env_ad(int(.5 * SR), .05, .15), .02 * g, self.rng.uniform(-.7, .7), .6); t += 1.5 + 2.5 * self.rng.random()
        if kind == "generator": self.bed(lp(self.noise(N), 150) + np.sin(2 * np.pi * 50 * self.t) * .3, e, .03 * g)
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

# ---------------- per-chapter cues (ice age) ----------------
def cues(ch, m, T, END):
    L = lambda k, off=0: (T[k]["line"] + off) / FPS
    A = lambda k, fr=0.: (T[k]["s"] + (T[k]["e"] - T[k]["s"]) * fr) / FPS
    E = lambda k: T[k]["e"] / FPS; end = END / FPS
    V = lambda k, band=None, g=1.: m.vo_line(f"{ch}_{k}", T[k]["line"], g, band)
    lines = [(b.get("key") or b["id"]) for b in PLAN[ch] if b.get("id")]
    if ch == "c1":
        m.amb("blizzard", 0, A("title")); music(m, "tense", A("n1"), A("title"), .8)
        m.snowsteps(A("n1", .3), A("n2"), .5); m.amb("museum", A("n2"), E("n2"), .8); m.whoosh(A("n2") - .1); m.whoosh(E("n2") - .2)
        m.trumpet(A("n3", .35), .5); m.thump(A("n3", .55), .5, 38); m.thump(A("n3", .7), .45, 36)
        m.riser(A("n4"), E("n4") - A("n4"), .14); m.hit(A("title"), .5); m.trumpet(A("title") + .3, .25, far=True)
    if ch == "c2":
        m.amb("museum", 0, A("n4", .6)); music(m, "warm", 0, A("n2"), .8); music(m, "mystery", A("n2"), A("n4"))
        m.mop(A("n1"), A("eli1")); m.glowhum(A("n3"), A("n4", .7)); m.riser(A("n4"), E("n4") - A("n4"), .2)
        m.flash(A("flash")); m.amb("blizzard", A("flash", .5), end)
    if ch == "c3":
        m.amb("blizzard", 0, A("n2", .6)); music(m, "tense", 0, A("n2", .6), .7)
        m.snowsteps(A("n1"), A("fact1"), .55); m.heart(A("fact1"), E("fact1"), 84, .25); m.click(A("eli1", .1), .2)
        m.dig(A("n2", .2), A("n2", .6)); m.amb("cave", A("n2", .6), end, .7); music(m, "sad", A("n2", .6), end, .8)
    if ch == "c4":
        m.amb("wind", 0, end, .7); music(m, "hope", 0, end, .8)
        m.trumpet(A("n2", .3), .22, far=True); m.trumpet(A("fact2", .4), .2, far=True); m.roar(A("n3", .55), .3, far=True)
        m.whoosh(A("fact1")); m.whoosh(A("fact3"))
    if ch == "c5":
        m.amb("river", 0, A("n4")); music(m, "warm", 0, A("n3"), .7); music(m, "mystery", A("n3"), A("spark"), .8)
        m.rub(A("eli1", .5), E("n2")); m.stones(A("n3", .4)); 
        for k in range(6): m.flint(A("fact1", .35) + k * .55, .3 + .05 * k)
        m.flint(A("spark", .1), .5); m.flint(A("spark", .45), .5); m.whoomp(A("spark", .6)); m.amb("fire", A("spark", .6), end, .9)
        music(m, "hope", A("eli2"), A("n4"), .8); music(m, "tense", A("n4"), end, .7); m.snowsteps(A("n4", .3), end, .7, .08)
    if ch == "c6":
        m.amb("river", 0, end, .6); m.amb("fire", 0, end, .5); music(m, "tense", 0, A("fact1"), .8)
        m.spearup(A("n1", .5)); m.thump(L("tor1"), .4, 50); music(m, "mystery", A("fact1"), A("pip1"), .7); music(m, "warm", A("pip1"), end, .8)
    if ch == "c7":
        m.amb("camp", 0, end); m.amb("fire", 0, end, .6); music(m, "warm", 0, A("n2"), .8); music(m, "hope", A("n3"), end, .7)
        m.marker(A("n3b", .3), 2.0, .05)
    if ch == "c8":
        m.amb("camp", 0, end, .6); m.amb("fire", 0, end, .5); music(m, "sad", 0, A("n2"), .8); music(m, "mystery", A("n2"), A("n3"), .8)
        m.cough(A("n1", .4)); m.cough(A("n1", .75)); m.boil(A("n3", .3), E("n3")); music(m, "hope", A("tor1"), end, .7)
    if ch == "c9":
        m.amb("wind", 0, end, .6); m.amb("fire", A("n2"), E("nia1"), .6); music(m, "warm", 0, A("n3"), .7)
        m.carve(A("n2", .3), E("n2")); m.whoosh(A("fact1", .4), .5, .2); m.whoosh(A("nia1", .2), .5, .2)
        music(m, "tense", A("n3"), A("n4")); m.snowsteps(A("n3"), E("n3"), .4, .12); music(m, "action", A("n4"), E("throw"))
        m.trumpet(A("n4", .35), .55); for_t = [m.thump(A("n4") + k * .45, .45, 36) for k in range(int((E("n4") - A("n4")) / .45))]
        m.slip(A("n4", .55)); m.whoosh(A("throw") + .25, .5, .3); m.thump(A("throw") + .75, .3, 60); m.trumpet(E("throw") - .2, .45)
        music(m, "hope", A("n5"), A("n6"), .9); m.cheer(A("n5", .3)); music(m, "warm", A("n6"), end, .8); m.carve(A("n6", .2), E("n6"))
    if ch == "c10":
        m.amb("blizzard", 0, A("n2")); m.amb("camp", A("n2"), E("n2"), .5); m.amb("blizzard", E("n2"), A("fact1"), .9)
        music(m, "tense", 0, A("fact1"), .8); m.snowsteps(A("n3"), A("n3", .7), .3, .12); m.crack(A("eli2", .6))
        music(m, "sad", A("fact1"), A("n4"), .8); m.amb("wind", A("tor1"), end, .6); music(m, "hope", A("n4"), end, .8)
        m.sled(A("n4"), E("n4")); m.carve(A("n5", .2), E("n5"))
    if ch == "c11":
        m.amb("cave", 0, end); m.amb("torch", 0, end, .7); music(m, "mystery", 0, A("n2"), .8)
        m.snowsteps(0, A("n1", .8), .5, .05); m.click(A("n2", .2), .2); music(m, "sad", A("n2"), A("nia1"), .8)
        m.paint(A("n3", .1), E("n3")); m.powerdown(A("n4", .3)); music(m, "warm", A("nia1"), end, .9)
    if ch == "c12":
        m.amb("cave", 0, A("n5")); m.amb("generator", 0, A("n5"), .6); music(m, "mystery", 0, A("n3"), .8)
        m.click(L("voss1", 30), .3); m.lightson(A("n2") + .1); m.heart(A("voss2"), E("voss2"), 72, .3)
        m.beep(A("n2b", .4)); m.beep(A("n3", .1)); m.hit(A("n3", .2), .35); m.riser(A("n4"), E("n4") - A("n4"), .15); m.hit(A("reveal"), .55)
        m.amb("camp", A("n5"), end, .4); m.amb("fire", A("n5"), end, .6); music(m, "warm", A("n5"), end, .9)
    for k in lines: V(k)

def build(ch):
    T, END = timeline(ch); m = Z(END, seed=int(ch[1:]) * 7)
    cues(ch, m, T, END); m.render(f"{ROOT}/public/{ch}.wav"); print(ch, "frames", END, f"{END / FPS:.1f}s")

if __name__ == "__main__":
    for ch in (sys.argv[1:] or [f"c{i}" for i in range(1, 13)]): build(ch)
