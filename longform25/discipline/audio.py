#!/usr/bin/env python3
"""discipline: voice + a place bed (street / room / night / engine), SFX cued from script words, quiet ORIGINAL plucked score, −14 LUFS → out/audio.wav"""
import sys, os, json, numpy as np
D = "/home/rasul/Desktop/Animations/longform25/discipline"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from audio_lib import Mix, SR, hz, lp, bp, hp
import show25 as S
G = json.load(open(f"{D}/out/global.json")); TOTAL = G["total"]; wt, lt = S.wt, S.lt; CO = {x["id"]: x for x in G["chapters"]}
m = Mix(int(TOTAL * 30) + 60, seed=13); N = m.N; t = m.t
for l in G["lines"]: m.voice(f"{D}/vo16/{l['id']}.wav", l["t0"] * 30, 1.0)
g = lambda c, x: CO[c]["off"] + x
W = lambda line, word, n=0, d=0.0: g(line[:3], wt(line, word, n)) + d
A = lambda line, d=0.0: g(line[:3], lt(line)) + d
B = lambda line, d=0.0: g(line[:3], lt(line, 1)) + d
def c0(c): return CO[c]["off"]
def c1(c): return CO[c]["off"] + CO[c]["dur"]
rr = np.random.default_rng(5); nz = lambda: m.noise(N)
# ---------------------------------------------------------------- place beds: (start, street/park, room, night, crowd)
ENV = [(0, 0, 0, 0, .7), (A("c01_n2", -.1), 0, .8, 0, 0), (A("c01_n3", -.1), 0, 0, 0, .7), (c0("c02"), 0, .8, 0, 0), (A("c02_n4", -.1), 0, 0, .8, 0), (A("c02_n6", -.1), 0, .8, 0, 0),
       (c0("c03"), 0, .3, .5, 0), (A("c03_n5", -.1), 0, .8, 0, 0), (A("c03_n3", -.1), 0, .5, 0, .5), (A("c03_n4", -.1), 0, .5, 0, 0), (c0("c04"), 0, .4, 0, .4), (A("c04_n3", -.1), .8, 0, 0, 0), (A("c04_n4", -.1), 0, .5, 0, 0),
       (c0("c05"), 1, 0, 0, 0), (A("c05_n6", -.1), 0, .8, 0, 0), (W("c05_n3", "bus", 0, -.2), .8, 0, 0, 0), (W("c05_n3", "Chess", 0, -.1), 0, .4, 0, .6), (W("c05_n3", "Coding", 0, -.1), 0, 0, .8, 0), (A("c05_mom1", -.1), 0, .8, 0, 0), (A("c05_n4", -.1), .8, 0, 0, 0), (A("c05_n5", -.1), 0, .6, 0, 0),
       (c0("c06"), 0, .3, 0, .8), (A("c06_n3", -.1), 0, .4, 0, .4), (c0("c07"), 0, .3, 0, .7), (c0("c08"), 0, 0, 0, .8), (W("c08_n4", "scan", 0, -.2), 0, .8, 0, 0), (A("c08_n5", -.1), 0, 0, 0, .7),
       (c0("c09"), 1, 0, 0, 0), (A("c09_n2", -.1), 0, 0, .8, 0), (A("c09_n3", -.1), 0, .7, 0, .3), (A("c09_n5", -.1), .7, 0, 0, 0), (c0("c10"), 0, 0, .8, 0), (A("c10_n3", -.1), 1, 0, 0, 0), (W("c10_n3", "limp", 0, -.1), 0, .4, 0, .3),
       (A("c10_n4", -.1), 0, .6, .4, 0), (A("c10_n6", -.1), 0, 0, .8, 0), (c0("c11"), .9, 0, 0, 0), (W("c11_n7", "burst", 0, -.1), 0, .3, 0, .6), (c0("c12"), .8, 0, 0, 0), (A("c12_n3", -.1), 0, .7, 0, 0), (A("c12_jay1", -.1), 0, .4, 0, .5),
       (c0("c13"), .6, 0, 0, 1), (A("c13_n2", -.1), 0, .6, 0, 0), (A("c13_n3", -.1), 0, 0, .9, 0)]
def curve(k):
    tt = [0.0]; v = [ENV[0][k]]
    for a, b in zip(ENV, ENV[1:]): tt += [b[0] - .15, b[0] + .15]; v += [a[k], b[k]]
    return np.interp(t, tt, v)
street = lambda: bp(nz(), 120, 1100) * .6 + bp(nz(), 2500, 7000) * .12
m.bed(street(), curve(1), .030, .25, street()); room = lambda: lp(nz(), 380); m.bed(room(), curve(2), .022, .25, room()); night = lambda: lp(nz(), 300); m.bed(night(), curve(3), .020, .25, night())
crowdbed = lambda: bp(nz(), 250, 1800) * (.8 + .2 * np.sin(2 * np.pi * .7 * t)); m.bed(crowdbed(), curve(4), .018, .3, crowdbed())
es, en, ef = curve(1), curve(3), curve(4) * 0

for k in range(int(TOTAL * 1.2)):                              # birds on the street, crickets at night, crackles in the fire
    q = rr.random() * TOTAL; i = min(N - 1, int(q * SR))
    if rr.random() < es[i] * .5: m.chime(q, 93 + rr.integers(0, 8), .008 + .006 * rr.random())
    if rr.random() < en[i] * .8: n = int(.12 * SR); s = np.arange(n) / SR; m.place(q, np.sin(2 * np.pi * 4300 * s) * (np.sin(2 * np.pi * 40 * s) > 0) * np.exp(-s * 12), .006, rr.random() - .5, .2)
for k in range(int(TOTAL * 9)):
    q = rr.random() * TOTAL; i = min(N - 1, int(q * SR))
    if rr.random() < ef[i]: n = int(.03 * SR); s = np.arange(n) / SR; m.place(q, bp(m.noise(n), 800, 6000) * np.exp(-s * 160), .05 * rr.random(), rr.random() - .5, .2)
# ---------------------------------------------------------------- atoms
def pop(t0, g_=.2, up=True):
    n = int(.25 * SR); s = np.arange(n) / SR; f0 = 900 if up else 500; m.place(t0, np.sin(2 * np.pi * np.cumsum(f0 + (1200 if up else -300) * s / .25) / SR) * np.exp(-s * 18) * .8, g_, 0, .4)
def swish(t0, g_=.07, d=.7): n = int(d * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 400, 2600) * np.sin(np.pi * s / d) ** 1.5, g_, 0, .3)
def boing(t0, g_=.14): n = int(.7 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(150 + 90 * np.sin(2 * np.pi * 9 * s) * np.exp(-s * 4)) / SR) * np.exp(-s * 4), g_, 0, .2)
def click(t0, g_=.13): n = int(.05 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 1500, 6000) * np.exp(-s * 120), g_)
def rumble(a, b, g_=.2, lo=25, hi_=140, up=.6):
    n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, bp(m.noise(n), lo, hi_) * np.minimum(1, s / up) * np.minimum(1, (b - a - s) / .5), g_, 0, .2)
def crunch(t0, g_=.25): n = int(.5 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 200, 2500) * np.exp(-s * 9) * (1 + np.sin(2 * np.pi * 40 * s)), g_, 0, .3); m.thump(t0, g_)
def leaves(t0, g_=.12, d=1.2): n = int(d * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 1500, 7000) * np.exp(-s * 3) * (.6 + .4 * np.sin(2 * np.pi * 23 * s)), g_, 0, .3)
def horn(t0, g_=.10, d=.32): n = int(d * SR); s = np.arange(n) / SR; m.place(t0, (np.sign(np.sin(2 * np.pi * 330 * s)) * .5 + np.sign(np.sin(2 * np.pi * 415 * s)) * .5) * np.minimum(1, s / .01) * np.minimum(1, (d - s) / .02), g_, 0, .2)
def squeal(t0, g_=.05, d=1.0): n = int(d * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(2400 + 300 * np.sin(2 * np.pi * 13 * s)) / SR) * np.sin(np.pi * s / d), g_, 0, .3)
def gurgle(a, b, g_=.08):
    q = a; k = 0
    while q < b: pop(q, g_ * (.5 + .5 * rr.random()), k % 2 == 0); q += .09 + .10 * rr.random(); k += 1
def radiohiss(a, b, g_=.03): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, bp(m.noise(n), 900, 2600) * (.6 + .4 * np.sin(2 * np.pi * 3 * s)) * np.minimum(1, s / .1) * np.minimum(1, (b - a - s) / .1), g_)
def bark(t0, g_=.06): n = int(.18 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 300, 1800) * np.exp(-s * 18) + np.sin(2 * np.pi * np.cumsum(420 - 300 * s) / SR) * np.exp(-s * 14) * .5, g_, rr.random() - .5, .3)
def crowd(a, b, g_=.05, cheer=False): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, bp(m.noise(n), 250, 2200 if not cheer else 4000) * (.7 + .3 * np.sin(2 * np.pi * 1.3 * s)) * np.minimum(1, s / .3) * np.minimum(1, (b - a - s) / .4), g_, 0, .4)
def splash(t0, g_=.12, d=.8): n = int(d * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 300, 6000) * np.exp(-s * 5) * (1 - np.exp(-s * 90)), g_, rr.random() - .5, .3)
def heart(t0, g_=.4): m.thump(t0, g_, 50); m.thump(t0 + .22, g_ * .7, 50)
def creak(t0, g_=.05, d=1.2): n = int(d * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(180 + 120 * np.sin(2 * np.pi * .8 * s) + 30 * (np.sin(2 * np.pi * 37 * s) > .6)) / SR) * np.sin(np.pi * s / d) * .8, g_, 0, .4)
def mower(a, b, g_=.05): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, np.sign(np.sin(2 * np.pi * 70 * s)) * .4 * np.minimum(1, s / .2) * np.minimum(1, (b - a - s) / .3), g_, .3, .2)
def buzz(a, b, g_=.02): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, np.sin(2 * np.pi * (210 + 30 * np.sin(2 * np.pi * 3 * s)) * s) * np.minimum(1, s / .2) * np.minimum(1, (b - a - s) / .2), g_, .2, .2)
def clink(t0, g_=.06): [m.chime(t0 + .06 * k, 100 + 3 * k, g_) for k in range(3)]
# ---------------------------------------------------------------- cues
def siren(a, b, g_=.03): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, np.sin(2 * np.pi * np.cumsum(700 + 250 * np.sign(np.sin(2 * np.pi * 1.4 * s))) / SR) * np.minimum(1, s / .4) * np.minimum(1, (b - a - s) / .4), g_, .3, .5)
def gavel_(t0, g_=.3): m.thump(t0, g_, 140); click(t0, .2)
def door_bang(t0): crunch(t0, .45); m.thump(t0, .5, 45); [m.place(t0 + .05 + .07 * k, bp(m.noise(int(.08 * SR)), 1200, 5000) * np.exp(-np.arange(int(.08 * SR)) / SR * 50), .05, rr.random() - .5) for k in range(8)]
def cans_(t0): [m.place(t0 + .08 * k, np.sin(2 * np.pi * (900 + 500 * k) * np.arange(int(.3 * SR)) / SR) * np.exp(-np.arange(int(.3 * SR)) / SR * 12) * .4 + bp(m.noise(int(.3 * SR)), 2000, 8000) * np.exp(-np.arange(int(.3 * SR)) / SR * 20), .12, rr.random() - .5) for k in range(5)]
def cry(a, b, g_=.05):
    q = a
    while q < b: n = int(.7 * SR); s = np.arange(n) / SR; m.place(q, np.sin(2 * np.pi * np.cumsum(520 + 120 * np.sin(np.pi * s / .7) + 30 * np.sin(2 * np.pi * 7 * s)) / SR) * np.sin(np.pi * s / .7) * .6, g_, 0, .2); q += .9
def tick(a, b, g_=.05, step=1.0):
    q = a
    while q < b: click(q, g_); q += step
def ding(t0, g_=.05, note=88): m.chime(t0, note, g_); m.chime(t0 + .12, note + 7, g_ * .8)
def notif(t0, g_=.05): m.chime(t0, 91, g_); m.chime(t0 + .09, 96, g_)
def clank(t0, g_=.12): [m.place(t0 + .01 * k, np.sin(2 * np.pi * f * np.arange(int(.4 * SR)) / SR) * np.exp(-np.arange(int(.4 * SR)) / SR * 9), g_ * .5, 0, .2) for k, f in enumerate((620, 1340, 2210))]; m.thump(t0, g_ * 1.5, 90)
def typing(a, b, g_=.05):
    q = a
    while q < b: click(q, g_ * (.6 + .4 * rr.random())); q += .07 + .06 * rr.random()
def strum(t0, g_=.05, root=55): [m._mus(t0 + .02 * k, pluck(hz(root + iv), 1.2), g_, .1) for k, iv in enumerate((0, 7, 12, 16, 19))]
def kaching(t0, g_=.06): click(t0, .1); m.chime(t0 + .05, 100, g_); m.chime(t0 + .12, 105, g_)
def ring(a, b, g_=.04):
    q = a
    while q < b: [m.chime(q + .07 * k, 98 + (k % 2) * 4, g_) for k in range(5)]; q += 1.0
def run_steps(a, b, g_=.08, step=.28):
    q = a
    while q < b: m.step(q, g_); q += step
def rain(a, b, g_=.04): n = int((b - a) * SR); s_ = np.arange(n) / SR; m.place(a, bp(m.noise(n), 1500, 8000) * np.minimum(1, s_ / .3) * np.minimum(1, (b - a - s_) / .3), g_, 0, .4)
def whisper(a, b, g_=.03): n = int((b - a) * SR); s_ = np.arange(n) / SR; m.place(a, bp(m.noise(n), 2500, 7000) * (.5 + .5 * np.sin(2 * np.pi * 4 * s_)) * np.minimum(1, s_ / .2) * np.minimum(1, (b - a - s_) / .2), g_, rr.random() - .5, .3)
def pluck(f, d=.5): n = int(d * SR); s = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * k * s) * np.exp(-s * (6 + 3 * k)) for k, a in ((1, 1), (2, .35), (3, .15))) * np.minimum(1, s / .004)
# c01 the TV room
tick(0, A("c01_n1", 1.2), .05); ding(W("c01_n1", "hours", 0, -.3), .07, 84); crowd(c0("c01"), B("c01_host1", .3), .03)
for wd in ("pizza", "console", "puppies"): pop(W("c01_n1", wd, 0, -.05), .05)
for k in range(5): bark(W("c01_n1", "puppies", 0, .2 + .35 * k), .05)
m.whoosh(W("c01_n1", "book", 0, -.2), .5, .04, 600, 4000); crowd(A("c01_host1", -.1), B("c01_host1", .4), .05, True); m.whoosh(A("c01_n2", -.3), .8, .06, 200, 2500)
for k in range(3): pop(W("c01_n2", "Forty", 0, .15 * k), .05)
m.thump(W("c01_n2", "Zero"), .2); m.whoosh(A("c01_n3", -.2), .8, .05, 200, 2500); m.thump(B("c01_n3", .1), .3); m.chime(B("c01_n3", .1), 76, .04)
# c02 who you were + the app
click(W("c02_n1", "Screen"), .08); ding(W("c02_n1", "nine"), .04, 70)
strum(W("c02_n2", "guitar", 0, .1), .02); click(W("c02_n2", "gym"), .06); m.thump(W("c02_n2", "science"), .08)
for wd in ("Five", "Tomorrow", "Next"): pop(W("c02_n3", wd, 0, -.05), .05, False)
m.thump(W("c02_n3", "loudest"), .2); m.whoosh(A("c02_mom1", -.3), .4, .05, 500, 3000)
notif(W("c02_n4", "app"), .06); click(W("c02_n5", "accept", 0, .1), .15); ding(W("c02_n5", "accept", 0, .15), .05, 96); m.whoosh(W("c02_n6", "gone", 0, -.2), 1.0, .06, 300, 5000)
# c03 day one
tick(c0("c03"), W("c03_n1", "turn"), .03); click(W("c03_n1", "turn", 0, .2), .15)
for k in range(8): m.thump(A("c03_n5", .2 + .45 * k), .05, 80)
for k in range(10): m.whoosh(W("c03_n5", "room", 0, .2 * k), .25, .03, 500, 4000)
rain(A("c03_n2", -.1), W("c03_n2", "Broccoli", 0, -.1), .05); clink(W("c03_n2", "Broccoli", 0, .4), .03); m.thump(W("c03_n2", "drawer", 0, .1), .1, 120)
crowd(A("c03_n3"), B("c03_jay1"), .02); ding(W("c03_n3", "finish", 0, .4), .04, 88)
for k in range(3): pop(A("c03_n4", 2.0 + .8 * k), .04)
# c04 the gym
clank(W("c04_n1", "can't"), .1); crowd(A("c04_ty1", -.1), B("c04_ty1", 1.0), .05, True); m.whoosh(W("c04_n2", "quit"), .6, .04, 300, 3000)
rain(W("c04_n3", "Rain", 0, -.2), W("c04_n3", "snow", 0, -.1), .06); run_steps(A("c04_n3"), B("c04_n3"), .05, .45); ding(W("c04_n4", "zero", 0, .1), .06, 84)
# c05 montage
run_steps(c0("c05"), A("c05_n6"), .05, .3); heart(W("c05_n1", "die", 0, -.1), .2); pop(W("c05_n1", "twenty"), .05); pop(W("c05_n1", "thirty"), .05)
for k in range(10): m.thump(A("c05_n6", .1 + .3 * k), .05, 80)
for k in range(3): m.place(W("c05_n6", "neighbors", 0, .3 + .5 * k), bp(m.noise(int(.25 * SR)), 300, 900) * np.exp(-np.arange(int(.25 * SR)) / SR * 10), .03, .5)
for k in range(6): m._mus(A("c05_n2", .1 + .45 * k), pluck(hz((52, 55, 59, 64, 59, 55)[k]), .9), .04, .1)
m.place(W("c05_n3", "bus", 0, -.2), bp(m.noise(int(1.5 * SR)), 40, 300), .05); click(W("c05_n3", "Chess", 0, .3), .1); typing(W("c05_n3", "Coding", 0, .1), W("c05_n3", "eight", 0, -.2), .04)
for k in range(5): m.chime(A("c05_mom1", .2 + .25 * k), 96 + k, .015)
for k in range(5): m.chime(A("c05_n4", .3 + .5 * k), 93 + k, .015)
m.whoosh(A("c05_n5"), .5, .04, 400, 3000); for_ = [kaching(W("c05_n5", "grades", 0, .4 + .25 * k), .03) for k in range(5)]
# c06 talent show + 100 kg
crowd(c0("c06"), A("c06_n5"), .03); click(W("c06_n5", "open"), .1); heart(W("c06_n5", "cut"), .25); m.whoosh(W("c06_n5", "Somebody"), .8, .03, 200, 1500)
for k in range(8): m._mus(W("c06_n6", "play", 0, .1 + .3 * k), pluck(hz((64, 64, 67, 64, 72, 71, 69, 67)[k]), .6), .05, .0)
crowd(W("c06_n2", "minutes", 0, .3), A("c06_n3"), .07, True); notif(W("c06_n2", "films"), .04); [ding(W("c06_n2", "morning", 0, .3 * k), .02, 90 + 2 * k) for k in range(4)]
clank(A("c06_n3", .5), .1); clank(A("c06_n3", 1.0), .1); crowd(A("c06_ty1", -.1), B("c06_ty1"), .02)
for k in range(5): clank(A("c06_n4", .9 + .9 * k), .08); m.thump(A("c06_n4", .5 + .9 * k), .08, 70)
# c07 aura + envy
for k in range(6): m.chime(A("c07_n1", .2 + .4 * k), 98 + k % 3, .015)
m.whoosh(W("c07_n1", "Aura", 0, -.2), 1.4, .04, 1000, 7000); m.chime(W("c07_n2", "sir", 0, .2), 70, .03)
for k in range(4): m.chime(W("c07_n3", "Five", 0, .15 * k), 96, .02)
whisper(A("c07_n4"), B("c07_n4"), .04); whisper(A("c07_n5"), B("c07_n5"), .03); [notif(A("c07_n5", .4 + .5 * k), .03) for k in range(4)]; m.thump(W("c07_n6", "TV"), .2)
# c08 the TV room
crowd(c0("c08"), W("c08_n4", "scan", 0, -.2), .025); [bark(W("c08_ty1", "Puppies", 0, .3 * k), .04) for k in range(3)]
for k in range(8): m.chime(W("c08_n2", "console", 0, .15 * k), (84, 88, 91, 96)[k % 4], .02)
pop(W("c08_n2", "page"), .03); ding(A("c08_host1", -.2), .06, 84); crowd(A("c08_host1"), B("c08_host1"), .05, True)
for k in range(6): click(W("c08_n3", "book", 0, .4 * k), .05)
buzz(W("c08_n4", "scan"), B("c08_n4"), .03); for_ = [click(A("c08_n5", .3 + .12 * k), .04) for k in range(14)]; ding(W("c08_n5", "blindfolded", 0, 1.2), .05, 88)
# c09 the app + the offer
run_steps(c0("c09"), A("c09_n2"), .04, .3); typing(A("c09_n2"), B("c09_n2"), .04)
for k in range(9): ding(A("c09_n3", .3 + .3 * k), .02 + .004 * k, 84 + 2 * k)
kaching(A("c09_n4", .1), .06); ring(A("c09_n5"), W("c09_n5", "hundred", 0, -.3), .03); m.thump(W("c09_n5", "hundred"), .25); m.thump(W("c09_n5", "Friday"), .15)
# c10 the cost
rumble(A("c10_n2"), B("c10_n2"), .04, 30, 120); run_steps(A("c10_n3"), W("c10_n3", "limp"), .05, .3); crunch(W("c10_n3", "knee"), .15); heart(W("c10_n3", "anyway"), .2)
notif(A("c10_n4", .2), .04); m.place(W("c10_n4", "Movie"), bp(m.noise(int(2 * SR)), 200, 3000), .01)
ring(W("c10_n5", "rings"), W("c10_n5", "rings", 0, 2.0), .05); [m.step(W("c10_n5", "walk", 0, .3 * k), .06) for k in range(5)]; buzz(A("c10_n6"), B("c10_n6", 1.0), .02)
# c11 the choice
tick(A("c11_n1"), B("c11_n1"), .04); notif(A("c11_n2"), .06); heart(W("c11_n3", "forgot"), .3); heart(W("c11_n3", "solo"), .3)
tick(A("c11_n4"), B("c11_n4"), .05, .5); m.thump(W("c11_n5", "stop", 0, .05), .3); m.whoosh(W("c11_n5", "stop", 0, .1), 1.2, .05, 200, 2000)
run_steps(A("c11_n6"), B("c11_n6", 2.0), .09, .24); heart(W("c11_n6", "knee"), .3); door_bang(W("c11_n7", "burst")); crowd(W("c11_n7", "burst", 0, .3), B("c11_mia1", 1.0), .02)
for k in range(12): m._mus(W("c11_n7", "sings", 0, .1 + .32 * k), pluck(hz((72, 74, 76, 77, 79, 77, 76, 74, 72, 76, 79, 84)[k]), .8), .05, 0)
crowd(B("c11_n7", .2), B("c11_mia1", 1.4), .06, True)
# c12 after
notif(A("c12_n1", .1), .04); m.thump(W("c12_n2", "tool"), .12); m.thump(W("c12_n2", "boss"), .12)
for k in range(3): pop(W("c12_n3", ("Monday", "Wednesday", "Sunday")[k]), .05)
crowd(A("c12_jay1", -.2), c1("c12"), .03); pop(W("c12_n4", "early"), .05)
# c13 one year later + the cliffhanger
crowd(c0("c13"), A("c13_n2"), .07, True); kaching(W("c13_n2", "fifty"), .05); strum(W("c13_n2", "guitar", 0, .2), .04)
notif(W("c13_n3", "lights"), .06); rumble(W("c13_n3", "update"), B("c13_n4", 1.5), .05, 30, 100); heart(A("c13_n4"), .35); heart(A("c13_n4", .8), .35); m.thump(A("c13_n5", -.1), .2)
# ---------------------------------------------------------------- score
def pad(ch, a, b, gg): n = int((b - a) * SR); s = np.arange(n) / SR; m._mus(a, lp(sum(np.sin(2 * np.pi * hz(q) * s) for q in ch), 1100) * np.minimum(1, s) * np.minimum(1, b - a - s), gg)
MOODS = {"play": ([64, 67, 71, 72, 71, 67, 69, 71, 64, 67, 72, 74, 72, 71, 69, 67], [[52, 59, 64], [48, 55, 60], [45, 52, 57], [47, 54, 59]], .30),
         "tense": ([57, 60, 64, 60, 59, 62, 65, 62, 57, 60, 64, 69, 68, 64, 62, 59], [[45, 52, 57], [46, 53, 58], [45, 52, 57], [44, 51, 56]], .32),
         "calm": ([67, 71, 74, 71, 66, 69, 72, 69, 64, 67, 71, 76, 74, 71, 67, 66], [[43, 50, 55], [42, 49, 54], [40, 47, 52], [47, 54, 59]], .46),
         "warm": ([72, 76, 79, 77, 76, 72, 74, 76, 77, 74, 72, 69, 71, 72, 74, 76], [[48, 55, 60], [53, 60, 65], [50, 57, 62], [43, 50, 55]], .42)}
for a_id, b_id, mood in [("c01", "c01", "tense"), ("c02", "c02", "calm"), ("c03", "c03", "play"), ("c04", "c04", "tense"), ("c05", "c05", "play"), ("c06", "c06", "warm"), ("c07", "c07", "tense"), ("c08", "c09", "play"), ("c10", "c10", "calm"), ("c11", "c11", "tense"), ("c12", "c12", "warm"), ("c13", "c13", "warm")]:
    a = c0(a_id) + .2; b = c1(b_id) - .2; mel, chs, step = MOODS[mood]; k = 0; q = a
    while q < b - .3:
        if k % 2 == 0 or mood == "play": m._mus(q, pluck(hz(mel[k % 16])), .026, .2 * (-1) ** k)
        if k % 4 == 0: m._mus(q, pluck(hz(chs[(k // 8) % 4][0]), .7), .026)
        q += step; k += 1
    q = a; i = 0
    while q < b - .5: pad(chs[i % 4], q, min(b, q + step * 8), .020); q += step * 8; i += 1
m.render(f"{D}/out/audio.wav"); print("TOTAL", round(TOTAL, 1))
