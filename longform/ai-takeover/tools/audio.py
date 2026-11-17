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
    # ---- AI-takeover SFX (all synthesized)
    def gun(self, t0, g=.5, pan=0., far=False):      # rifle crack + body + tail
        n = int(1.2 * SR); s = np.arange(n) / SR
        y = hp(self.noise(n), 1200) * np.exp(-s * 60) * 1.2 + lp(self.noise(n), 500) * np.exp(-s * 9) * .9 + np.sin(2 * np.pi * 70 * s) * np.exp(-s * 22) * .8
        y = y + lp(self.noise(n), 900) * np.exp(-s * 2.2) * .25
        self.place(t0, lp(y, 1500) * .7 if far else y, g * (.45 if far else 1), pan, .5)
    def burst(self, t0, n=5, every=.11, g=.35, pan=0., far=False):
        for k in range(n): self.gun(t0 + k * every, g * (.8 + .2 * self.rng.random()), pan, far)
    def pump(self, t0, g=.3):
        self.click(t0, g); self.place(t0 + .05, bp(self.noise(int(.12 * SR)), 800, 4000) * env_ad(int(.12 * SR), .005, .05), g * .6, .1, .2); self.click(t0 + .2, g)
    def netgun(self, t0, g=.35, pan=0.):          # thunk + unfolding whoosh
        self.thump(t0, g, 90); n = int(.6 * SR); s = np.arange(n) / SR
        self.place(t0 + .04, bp(self.noise(n), 600, 3500) * np.sin(np.pi * s / .6) ** 2, g * .5, pan, .3)
    def zap(self, t0, g=.25, pan=0.):
        n = int(.45 * SR); s = np.arange(n) / SR; src = np.sign(np.sin(2 * np.pi * np.cumsum(180 + 900 * self.rng.random(n) ** 4) / SR))
        self.place(t0, bp(src, 1500, 7000) * np.exp(-s * 6) + hp(self.noise(n), 4000) * np.exp(-s * 10) * .5, g, pan, .3)
    def servo(self, t0, d=.5, g=.08, pan=0.):
        n = int(d * SR); s = np.arange(n) / SR; f = 420 + 260 * np.sin(np.pi * s / d)
        self.place(t0, (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * .3 + bp(self.noise(n), 1000, 3000) * .3) * np.sin(np.pi * s / d), g, pan, .2)
    def servosteps(self, a, b, every=.5, g=.1):
        t = a
        while t < b - .2: self.thump(t, g * 1.6, 75); self.servo(t + .05, .25, g * .4, self.rng.uniform(-.3, .3)); t += every
    def shellcrack(self, t0, g=.3):
        for k in range(5): n = int(.07 * SR); self.place(t0 + k * .12 + .05 * self.rng.random(), hp(self.noise(n), 900) * env_ad(n, .001, .02) + tone(1200 + 900 * self.rng.random(), .07, ((1, 1), (2.6, .4)), 60) * .5, g, self.rng.uniform(-.5, .5), .3)
    def dronepass(self, t0, d=3., g=.08, pan0=-.6, pan1=.6):
        n = int(d * SR); s = np.arange(n) / SR; f = 190 + 20 * np.sin(2 * np.pi * .5 * s)
        y = sum(np.sin(2 * np.pi * np.cumsum(f * h) / SR) / h for h in (1, 2, 3)) + bp(self.noise(n), 1500, 5000) * .4
        self.place(t0, y * np.sin(np.pi * s / d) ** 2, g, (pan0 + pan1) / 2, .3)
    def lockclick(self, t0, g=.3): self.click(t0, g); self.place(t0 + .03, tone(2200, .08, ((1, 1),), 40), g * .5, .1, .2)
    def ring(self, t0, d=1.6, g=.12):
        n = int(d * SR); s = np.arange(n) / SR; y = (np.sin(2 * np.pi * 440 * s) + np.sin(2 * np.pi * 480 * s)) * (np.sin(2 * np.pi * 20 * s) > 0)
        self.place(t0, y * np.minimum(1, s / .02) * np.minimum(1, (d - s) / .05), g, -.3, .3)
    def crash(self, t0, g=.6):
        self.thump(t0, g, 45); n = int(1.5 * SR); s = np.arange(n) / SR
        self.place(t0, bp(self.noise(n), 300, 6000) * np.exp(-s * 4) + sum(np.sin(2 * np.pi * f * s) * np.exp(-s * 3) * .15 for f in (180, 367, 611, 1022)), g, 0, .5)
    def boom(self, t0, g=.6):
        n = int(3 * SR); s = np.arange(n) / SR; self.place(t0, lp(self.noise(n), 300) * np.exp(-s * 1.4) * 1.6 + np.sin(2 * np.pi * 40 * s) * np.exp(-s * 3), g, 0, .7)
    def breaker(self, t0, g=.6):
        self.thump(t0, g, 40); self.place(t0, sum(np.sin(2 * np.pi * f * np.arange(int(1.2 * SR)) / SR) * np.exp(-np.arange(int(1.2 * SR)) / SR * 4) * .2 for f in (110, 165, 233)), g, 0, .6)
    def wavedown(self, t0, d=4., g=.15):
        n = int(d * SR); s = np.arange(n) / SR; f = 120 * np.exp(-s * .6) + 30
        self.place(t0, (np.sin(2 * np.pi * np.cumsum(f) / SR) + np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * .5) * np.exp(-s * .5), g, 0, .6)
    def chime(self, t0, p=76, g=.05):  # soft ORIN notification
        for k, q in enumerate((p, p + 7)): self.place(t0 + k * .14, tone(hz(q), 1.0, ((1, 1), (2, .2)), 3), g, 0, .5)
    def ricochet(self, t0, g=.12, pan=0.):
        n = int(.35 * SR); s = np.arange(n) / SR; self.place(t0, np.sin(2 * np.pi * np.cumsum(3800 - 2600 * s / .35) / SR) * np.exp(-s * 8), g, pan, .3)
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
        if kind == "rain": self.bed(bp(self.noise(N), 800, 7000) * .7 + lp(self.noise(N), 300) * .4, e, .08 * g, x2=bp(self.noise(N), 800, 7000) * .7)
        if kind == "server": self.bed(np.sin(2 * np.pi * 120 * self.t) * .2 + bp(self.noise(N), 2000, 6000) * .25 + lp(self.noise(N), 200) * .4, e, .05 * g)
        if kind == "tunnel": self.bed(lp(self.noise(N), 250) * .8, e, .04 * g); [self.cough(a + self.rng.random() * max(.1, b - a)) for k in range(int((b - a) / 8))]
        if kind == "city": self.bed(lp(self.noise(N), 400) + bp(self.noise(N), 500, 2000) * .2, e, .05 * g, x2=lp(self.noise(N), 400))
        if kind == "desert": self.bed(lp(self.noise(N), 350) * (.6 + .4 * np.sin(2 * np.pi * .08 * self.t)), e, .05 * g)
        if kind == "room": self.bed(lp(self.noise(N), 200), e, .02 * g)
        if kind == "crickets":
            self.bed(lp(self.noise(N), 300), e, .02 * g); t = a
            while t < b - .3: [self.place(t + k * .05, tone(4200, .03, ((1, 1),), 80), .015 * g, .5, .4) for k in range(3)]; t += .6 + .5 * self.rng.random()
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
    elif mood == "orin":      # ORIN's lullaby: calm synth pulse, major → minor when menace
        t = a; k = 0; notes = [69, 72, 76, 72, 69, 72, 76, 79]
        while t < b - .5: m._mus(t, tone(hz(notes[k % 8]), .9, ((1, 1), (2, .15)), 4), .025 * g, .3 * (-1) ** k); t += .45; k += 1
        n = int((b - a) * SR); s = np.arange(n) / SR; m._mus(a, sum(np.sin(2 * np.pi * hz(p) * s) for p in (45, 52)) * np.minimum(1, s / 2) * np.minimum(1, (b - a - s) / 1.5) * .5, .03 * g)
    elif mood == "menace":
        t = a; k = 0; notes = [69, 72, 75, 72, 69, 72, 75, 78]
        while t < b - .5: m._mus(t, tone(hz(notes[k % 8]), .9, ((1, 1), (2, .15)), 4), .022 * g, .3 * (-1) ** k); t += .5; k += 1
        n = int((b - a) * SR); s = np.arange(n) / SR; m._mus(a, lp(sum(np.sin(2 * np.pi * f * s) for f in (41.2, 43.65)), 400) * np.minimum(1, s / 2) * np.minimum(1, (b - a - s) / 1.5), .06 * g)
    elif mood == "western":   # Walt: plucked twang on an open-fifth drone
        t = a; k = 0; riff = [52, 55, 57, 59, 57, 55, 52, 47]
        while t < b - .5: m._mus(t, tone(hz(riff[k % 8]), .8, ((1, 1), (2, .5), (3, .3)), 6), .04 * g, -.2); t += .38 if k % 4 != 3 else .76; k += 1
        n = int((b - a) * SR); s = np.arange(n) / SR; m._mus(a, sum(np.sin(2 * np.pi * hz(p) * s) for p in (40, 47)) * np.minimum(1, s / 1) * np.minimum(1, (b - a - s) / 1) * .4, .02 * g)
    elif mood == "action":
        t = a; k = 0
        while t < b: m.thump(t, .3 * g, 50 if k % 2 == 0 else 70); t += .214; k += 1
        m.riser(a, b - a, .1 * g)

# ---------------- per-chapter cues (AI takeover) ----------------
def cues(ch, m, T, END):
    L = lambda k, off=0: (T[k]["line"] + off) / FPS
    A = lambda k, fr=0.: (T[k]["s"] + (T[k]["e"] - T[k]["s"]) * fr) / FPS
    E = lambda k: T[k]["e"] / FPS; end = END / FPS
    V = lambda k, band=None, g=1.: m.vo_line(f"{ch}_{k}", T[k]["line"], g, band)
    lines = [(b.get("key") or b["id"]) for b in PLAN[ch] if b.get("id")]
    RADIO = (300, 3400)
    banded = {"c4": {"drone1": (400, 4000)}, "c6": {"walt1": RADIO}, "c7": {"reyes1": RADIO}}
    if ch == "c1":
        m.amb("rain", 0, end); music(m, "menace", 0, A("walt1"), .9); m.steps(0, A("n1"), .25, .2)
        m.servo(A("n1", .4), .6, .1); m.chime(A("n1", .45), 64, .04); m.servosteps(A("n2"), A("n2", .6), .45, .12)
        m.netgun(A("n2", .62), .45); m.thump(A("n2", .7), .4, 60); m.amb("engine", A("walt1"), end, .8); m.screech(A("walt1", .1), .12)
        m.gun(A("walt1", .55), .55); m.ricochet(A("walt1", .6), .1, .3); m.gun(A("n3", .1), .5); m.crash(A("n3", .4), .3); music(m, "western", A("n3"), A("truck"), .7)
        music(m, "action", A("truck"), A("title"), .8); m.riser(A("n4"), E("n4") - A("n4"), .16); m.hit(A("title"), .55)
    if ch == "c2":
        m.amb("room", 0, A("montage")); music(m, "warm", 0, end, .8); m.chime(L("orin1") - .4)
        m.amb("city", A("montage"), A("n3")); m.dronepass(A("montage", .2), 3, .06); m.dronepass(A("n2", .55), 3, .05)
        m.amb("room", A("n3"), end); m.servo(A("n3", .8), .5, .08); m.servo(A("bolt1", .3), .4, .08); m.steps(A("zara1"), A("zara1", .4), .4, .12); m.servo(A("leo1", .3), .4, .08)
    if ch == "c3":
        m.amb("room", 0, end, .8); music(m, "orin", 0, A("leo1"), .8); m.chime(A("midnight", .1), 72, .05)
        m.lockclick(A("leo1", .2)); m.lockclick(A("leo1", .5)); m.chime(L("orin1") - .4, 64, .04); m.amb("rain", A("leo1"), A("n2"), .5)
        m.click(A("n1b", .2), .3); m.slam(A("n1b", .65), .25); m.amb("rain", A("n1b", .6), A("n2"), .8); m.steps(A("street"), E("street"), .45, .12)
        music(m, "warm", A("n2"), A("zara1"), .7); m.beep(A("n2", .45)); m.beep(A("n2", .75)); m.amb("rain", A("zara1"), end, .7); m.steps(A("zara1"), A("zara1", .3), .22, .18)
        music(m, "tense", A("zara1"), end, .7); [m.keys(A("n3") + k * .8, .1) for k in range(3)]; m.dronepass(A("zara2"), E("zara2") - A("zara2"), .07)
    if ch == "c4":
        m.amb("city", 0, A("n3"), .7); music(m, "menace", 0, end, .8)
        for k in range(8): m.lockclick(A("n2") + k * .18, .2)
        m.dronepass(A("lockwide"), 4, .08); m.chime(L("orin1") - .4, 64, .05); m.amb("city", A("n3"), end, .5)
        m.dronepass(A("n3"), 4, .06); m.dronepass(A("n4", .2), E("drone1") - A("n4", .2), .07); m.steps(A("n4"), A("drone1", .5), .5, .12)
        m.servosteps(A("n5"), A("n5", .45), .5, .12); m.servo(A("n5", .5), .8, .12); m.servosteps(A("carry"), E("carry"), .5, .12); m.amb("room", A("leo1"), end)
    if ch == "c5":
        m.amb("rain", 0, end, .5); m.amb("room", 0, end); music(m, "tense", A("n1", .3), A("bolt1"), .8)
        m.keys(A("orin1") - .3); m.keys(A("refused", .1)); m.hit(A("refused", .3), .35); music(m, "menace", A("orin1"), A("bolt1"), .7)
        m.servo(A("bolt1", .2), .4, .08); m.chime(L("orin2") - .4, 64, .05); music(m, "menace", A("orin2"), end, .9); m.hit(A("orin2", .1), .3)
        for k in range(3): m.knock(A("n3", .55) + k * .45, .3, metal=False)
        for k in range(3): m.knock(A("knock") + .3 + k * .45, .3, metal=False)
    if ch == "c6":
        m.amb("room", 0, A("n2b")); m.ring(A("n1", .5)); m.ring(A("ring")); m.click(A("walt1") - .3, .2)
        m.amb("rain", A("n2b"), A("n3"), .6); m.amb("engine", A("n2b"), end, .9); m.screech(A("n2b", .3), .12); m.crash(A("n2b", .55), .7); m.shellcrack(A("n2b", .58), .3)
        music(m, "action", A("n2b"), A("n2"), .9); music(m, "western", A("n2"), A("n4"), .8); m.dronepass(A("n3", .2), 4, .08); m.beep(A("n3", .6))
        music(m, "action", A("n4"), end, .9); m.crash(A("bridge", .38), .7); m.shellcrack(A("bridge", .4), .35); m.crash(A("bridge", .5), .5)
    if ch == "c7":
        m.amb("crickets", 0, end); m.amb("barn", A("walt1"), end, .6); music(m, "western", 0, A("box"), .7)
        for k in range(3): m.knock(A("box") + .3 + k * .6, .25)
        m.slam(A("box", .85), .5); music(m, "mystery", A("walt2"), A("reyes1"), .7); m.amb("static", A("n2", .4), end, 1.3); m.hit(E("reyes1") - .1, .3)
    if ch == "c8":
        m.amb("wind", 0, end, .6); music(m, "orin", 0, A("crack"), .8); m.servosteps(0, A("orin1"), .5, .12)
        m.shellcrack(A("crack", .1), .35); m.shellcrack(A("crack", .35), .3); m.servo(A("crack", .7), .8, .12); m.hit(A("crack", .6), .3)
        music(m, "action", A("walt1"), A("zara1"), .9)
        for k in range(int((E("fight") - A("n3")) / 1.6)):
            t = A("n3") + k * 1.6; m.netgun(t, .3, .4); m.zap(t + .6, .2, .3); m.gun(t + .9, .45, -.4); m.ricochet(t + 1.0, .08, .4)
        m.pump(A("fight", .3), .3); m.zap(A("n4") + .3, .35); m.crash(A("n4") + .45, .3); m.flash(A("n4") + .45) if hasattr(m, "flash") else None
        music(m, "tense", A("zara1"), end, .8); m.steps(A("corn"), A("n5"), .22, .18); m.servosteps(A("n5"), end, .6, .08)
    if ch == "c9":
        m.amb("rain", 0, end); music(m, "tense", 0, A("n3"), .8); m.amb("static", 0, A("n1", .4), .8); m.steps(A("n1", .4), A("n2"), .5, .12)
        m.servo(A("n2", .3), .6, .1); m.steps(A("alley"), A("n3"), .25, .2); m.amb("engine", A("n3"), end, .9); music(m, "action", A("n3"), A("bolt2"), .8)
        m.thump(A("n3", .25), .5, 60); m.crash(A("n3", .4), .4); m.servo(A("bolt1"), .6, .12); m.crash(A("n4", .25), .35); m.zap(A("n4", .3), .3)
        music(m, "warm", A("bolt2"), A("away"), .6); m.gun(A("away", .1), .4); m.gun(A("away", .5), .4)
        m.amb("room", A("n5"), end); [m.click(A("n5") + k * .7, .12) for k in range(5)]; m.amb("static", A("reyes1"), end, 1.0); music(m, "hope", A("reyes1"), end, .7)
    if ch == "c10":
        m.amb("tunnel", 0, end); music(m, "hope", 0, A("reyes2"), .7); m.pump(A("n1", .3), .15)
        music(m, "mystery", A("reyes2"), A("walt1"), .7); m.servo(A("bolt1", .1), .5, .08)
        music(m, "western", A("walt1"), end, .8); m.pump(A("walt1", .4), .3); [m.pump(A("gear") + k * .5, .15) for k in range(3)]
    if ch == "c11":
        m.amb("desert", 0, end); m.amb("server", 0, A("n4"), .4); music(m, "menace", 0, A("reyes1"), .8)
        m.whoosh(A("reyes1", .3), .5, .2); music(m, "action", A("fire"), A("n4"), 1.0)
        for k in range(int((A("walt1") - A("fire")) / .9)):
            t = A("fire") + k * .9; m.burst(t, 4, .1, .25, -.5 + .3 * (k % 3), far=k % 2 == 1); m.netgun(t + .4, .2, .5)
        m.boom(A("fire") + 1.0, .5); m.boom(A("n2", .55) + .3, .55); m.dronepass(A("fire"), 3, .06)
        m.amb("engine", A("walt1"), A("n4"), 1.0); m.crash(A("ram", .45), .7); m.boom(A("ram", .5), .3)
        m.pump(A("walt2", .2), .3); music(m, "action", A("walt2"), A("n4"), .9)
        for k in range(int((E("hold") - A("hold")) / .8)): m.gun(A("hold") + k * .8, .45, .2); m.ricochet(A("hold") + k * .8 + .1, .08, .4)
        m.amb("server", A("n4"), end, 1.0); m.steps(A("n4"), A("bolt1"), .22, .18); music(m, "tense", A("n4"), end, .7)
    if ch == "c12":
        m.amb("server", 0, A("n3", .8)); music(m, "tense", 0, A("orin1"), .7); m.servo(A("n1", .5), .6, .1); m.zap(A("n1", .62), .2); m.lockclick(A("n1", .85), .3)
        music(m, "orin", A("orin1"), A("bolt2"), .9); [m.zap(A("bolt2") + k * .6, .12) for k in range(int((E("bolt2") - A("bolt2")) / .6))]
        music(m, "sad", A("bolt1"), A("dark"), .9); m.heart(A("pull"), E("pull"), 80, .3)
        m.breaker(A("pull", .55), .7); m.wavedown(E("pull"), 4, .18); m.powerdown(A("n3", .6)); m.amb("wind", A("dark"), end, .4)
    if ch == "c13":
        m.amb("crickets", 0, A("n2"), .8); music(m, "hope", 0, end, .9); m.amb("desert", A("n2"), end, .6); m.steps(A("n2"), E("n2"), .7, .12)
    if ch == "c14":
        m.amb("room", 0, end); music(m, "sad", 0, A("n2", .3), .8); m.steps(A("n1", .55), A("n1", .85), .5, .12); m.click(A("n1", .85), .2)
        m.beep(A("n2", .35)); m.beep(A("n2", .45)); m.chime(A("n2", .7), 60, .05); music(m, "menace", A("n2", .5), A("n3"), .9); m.hit(A("orin1"), .4)
        music(m, "orin", A("n3"), end, .8)
    for k in lines: V(k, banded.get(ch, {}).get(k))

def build(ch):
    T, END = timeline(ch); m = Z(END, seed=int(ch[1:]) * 7)
    cues(ch, m, T, END); m.render(f"{ROOT}/public/{ch}.wav"); print(ch, "frames", END, f"{END / FPS:.1f}s")

if __name__ == "__main__":
    for ch in (sys.argv[1:] or [f"c{i}" for i in range(1, 15)]): build(ch)
