#!/usr/bin/env python3
"""adults: voice + a place bed (street / room / night / fire), SFX cued from script words, quiet ORIGINAL plucked score, −14 LUFS → out/audio.wav"""
import sys, os, json, numpy as np
D = "/home/rasul/Desktop/Animations/longform25/adults"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"
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
# ---------------------------------------------------------------- place beds: (start, street, room, night, fire)
ENV = [(0, 1, 0, 0, 0), (A("c01_n2", -.1), .3, .6, 0, 0), (A("c01_n3", -.1), 1, 0, 0, 0), (c0("c02"), 0, 0, 0, 0), (c0("c03"), 0, .8, 0, 0), (A("c03_n3", -.1), 1, 0, 0, 0), (c0("c04"), 0, .8, 0, 0), (A("c04_n3", -.1), 0, 0, 0, 0),
       (c0("c05"), 1, 0, 0, 0), (c0("c06"), .3, 0, .6, 0), (A("c06_n2", -.1), 0, .3, .8, 0), (c0("c07"), 0, .7, .2, 0), (A("c07_n2", -.1), .8, 0, 0, 0), (A("c07_n3", -.1), 0, 0, 0, 0), (A("c07_n6", -.1), 1, 0, 0, 0), (W("c07_n7", "control", 0, -.2), 0, .9, 0, 0),
       (A("c07_n5", -.1), 0, 0, 1, 0), (c0("c08"), 0, .8, 0, 0), (A("c08_n2", -.1), 1, 0, 0, 0), (A("c08_n3", -.1), 0, 0, 0, 0), (A("c08_maya1", -.1), 0, .8, 0, 0), (c0("c09"), 0, .8, 0, 0), (A("c09_n3", -.1), .6, .4, 0, 0), (W("c09_n3", "only", 0, -.1), 1, 0, 0, 0),
       (c0("c10"), 1, 0, 0, 0), (c0("c11"), 0, .8, 0, 0), (A("c11_n3", -.1), 1, 0, 0, 0), (c0("c12"), .6, .4, 0, 0), (W("c12_n1", "deer", 1, -.2), 1, 0, 0, 0), (c0("c13"), 0, .8, 0, 0), (A("c13_n3", -.1), 1, 0, 0, 0), (A("c13_n4", -.1), 0, .8, 0, 0),
       (c0("c14"), 1, 0, 0, 0), (W("c14_n3", "Deer", 0, -.1), 1, 0, 0, 0), (c0("c15"), 0, .3, .8, 0), (W("c15_n1", "curtain", 0, -.1), 0, .3, .4, .6), (A("c15_n2", -.1), 0, 0, .6, .5), (A("c15_maya1", -.1), 0, 0, .3, 1), (A("c15_n4", -.1), .5, 0, .2, .15),
       (c0("c16"), 1, 0, 0, 0), (W("c16_n2", "But", 0, -.1), 0, .8, 0, 0), (c0("c17"), 0, .2, .9, 0), (c0("c19"), .4, 0, .5, 0), (A("c19_mom1", -.1), 0, .2, .9, 0), (c0("c20"), 0, .2, .9, 0), (A("c20_n2", -.1), 0, 0, 0, 0), (A("c20_n3", -.1), 0, .1, .9, 0)]
def curve(k):
    tt = [0.0]; v = [ENV[0][k]]
    for a, b in zip(ENV, ENV[1:]): tt += [b[0] - .15, b[0] + .15]; v += [a[k], b[k]]
    return np.interp(t, tt, v)
street = lambda: bp(nz(), 150, 1200) * .6 + bp(nz(), 2500, 7000) * .15
m.bed(street(), curve(1), .030, .25, street()); room = lambda: lp(nz(), 380); m.bed(room(), curve(2), .022, .25, room()); night = lambda: lp(nz(), 300); m.bed(night(), curve(3), .020, .25, night())
fire = lambda: bp(nz(), 60, 900); m.bed(fire(), curve(4), .07, .25, fire())
es, en, ef = curve(1), curve(3), curve(4)
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
rumble(0, A("c01_n2", -.1), .10, 30, 110); rumble(A("c01_n2", -.1), A("c01_n3", -.1), .06, 30, 110)
for k in range(5): horn(W("c01_n2", "Leo", 0, .5) + .45 * k, .07)
for k in range(2): horn(A("c01_leo1", .05 + .45 * k), .08)
for k in range(5): swish(W("c01_leo1", "Move", 0, .05 * k), .06, .4)
squeal(W("c01_maya1", "Brake", 1, -.1), .05, 1.4); crunch(A("c01_n3", .0), .35); leaves(A("c01_n3", .05), .14, 1.6); pop(W("c01_n3", "best", 0, -.1), .10)
m.whoosh(c0("c02") + .1, 1.6, .10, 200, 3000); m.thump(A("c02_n1", .2), .3)
pop(c0("c03") + .2, .06); m.chime(W("c03_n2", "coffee"), 84, .03); click(W("c03_n2", "phone", 0, .05), .08); clink(W("c03_n2", "keys", 0, .05), .04); m.thump(W("c03_n2", "gone"), .18)
rumble(A("c03_n3"), B("c03_n3", .5), .04, 40, 160)
for k in range(24): pop(A("c04_n1", .4 + .12 * k), .05 + .03 * (k % 3 == 0), k % 2 == 0)
radiohiss(A("c04_n2", .1), B("c04_n2", .3), .012)
for k in range(5): n_ = int(.25 * SR); s_ = np.arange(n_) / SR; m.place(W("c04_n2", "chair", 0, .1 + .5 * k), np.sin(2 * np.pi * np.cumsum(900 + 400 * s_) / SR) * np.sin(np.pi * s_ / .25), .012)
m.whoosh(A("c04_n3", .2), 1.6, .08, 150, 2500); m.thump(W("c04_n3", "vanished"), .2)
for k in range(10): pop(W("c04_n3", "eighteen", 0, .2 + .12 * k), .04, False)
m.whoosh(A("c04_n4"), 1.4, .07, 300, 4000); m.thump(W("c04_n4", "third"), .22)
crowd(c0("c05"), c1("c05"), .03, True); pop(W("c05_n2", "Ice", 0, -.05), .12); pop(W("c05_n2", "lunch", 0, -.05), .12); mower(W("c05_n2", "Somebody", 0, -.1), B("c05_n2", .3), .04)
gurgle(A("c05_n5"), A("c05_n5", 3.0), .03)
for k in range(5): m.step(A("c05_n3", .4 + .3 * k), .12)
crowd(W("c05_marcus1", "president", 0, .3), B("c05_marcus1", 1.2), .05, True)
for k in range(5): m.chime(A("c06_n1", .5 + .9 * k), 76 - 2 * k, .02)
radiohiss(c0("c07") + .1, A("c07_n2"), .004); rumble(A("c07_n2"), B("c07_n3"), .06, 30, 90); swish(A("c07_n3", .3), .05)
for k in range(10): click(A("c07_n6", .3 + .55 * k), .03)
crowd(W("c07_n7", "control", 0, -.2), B("c07_maya1"), .01)
for k in range(8): n_ = int(.4 * SR); s_ = np.arange(n_) / SR; m.place(W("c07_n7", "flashing", 0, .5 * k - 1.5), np.sin(2 * np.pi * 620 * s_) * np.sin(np.pi * s_ / .4) * .5, .018)
for k in range(4): n_ = int(.6 * SR); s_ = np.arange(n_) / SR; m.place(W("c07_n4", "switch", 0, .35 * k), np.sin(2 * np.pi * np.cumsum(300 * np.exp(-s_ * 3)) / SR) * np.exp(-s_ * 4), .06)
for k in range(3): m.thump(W("c07_n5", "blink", 0, .15 * k), .08); click(W("c07_n5", "blink", 0, .15 * k), .1)
m.thump(W("c07_n5", "dark"), .35); m.thump(W("c07_n5", "next"), .18); m.thump(W("c07_n5", "next", 1), .12)
for k in range(6): gurgle(A("c08_n1", .9 + .9 * k), A("c08_n1", 1.2 + .9 * k), .05)
rumble(W("c08_n2", "Electric"), W("c08_n2", "holds"), .04, 60, 200); gurgle(W("c08_n2", "holds"), B("c08_n2", .4), .02)
for wd, k in (("No", 0), ("pumps", 0), ("pumps", 1)): m.thump(W("c08_n3", wd, k), .15)
boing(A("c08_maya1", .2), .05)
buzz(W("c09_n2", "smells"), B("c09_n2", .8), .015); pop(W("c09_n2", "yogurt"), .12)
for k in range(3): pop(W("c09_n4", "last", 0, .3 * k), .05, False)
click(B("c09_leo1", .1), .25); m.chime(B("c09_leo1", .2), 88, .03)
crowd(W("c09_n3", "only"), c1("c09"), .03)
for k in range(5): clink(A("c10_n1", .5 + .1 * k), .02)
for k in range(5): m.step(A("c10_n2", .1 + .35 * k), .12)
pop(W("c10_maya1", "fourteen"), .08); pop(W("c10_maya1", "chips"), .08)
clink(W("c10_n3", "unlocks", 0, .3), .06); clink(W("c10_n3", "unlocks", 0, .6), .05); m.thump(W("c10_n3", "unlocks", 0, .8), .15); crowd(W("c10_n3", "unlocks", 0, .9), c1("c10"), .03, True)
for k in range(6): pop(W("c11_n1", "milk", 0, -.1 + .2 * k), .02)
pop(W("c11_n4", "Feeding"), .06); pop(W("c11_n4", "Feeding", 1), .06); pop(W("c11_n4", "Feeding", 2), .06)
rumble(A("c11_n3"), c1("c11"), .06, 30, 110)
rumble(c0("c12"), A("c12_n2", .3), .05, 30, 110)
for k in range(3): horn(A("c12_n1", .2 + .45 * k), .08)
squeal(A("c12_n2", -.4), .04, 1.0); crunch(A("c12_n2", .05), .3); leaves(A("c12_n2", .1), .12, 1.4); m.chime(W("c12_n2", "survives"), 84, .04); m.chime(W("c12_n2", "survives", 0, .15), 88, .04)
m.whoosh(A("c13_n2"), .6, .05, 400, 3000)
for wd in ("Water", "Food", "Baby", "Fire"): pop(W("c13_n2", wd, 0, -.05), .12)
for k in range(10): bark(A("c13_n3", .3 + .8 * k), .04)
bark(W("c13_leo1", "Captain"), .06); bark(W("c13_leo1", "Captain", 1), .06); crowd(W("c13_marcus1", "If"), B("c13_marcus1", 1.0), .04, True)
for k in range(5): pop(W("c14_n5", "counts", 0, .3 * k), .03)
pop(W("c14_n6", "vegetable"), .12)
for k in range(3): m.chime(W("c15_n1", "curtain", 0, .2 + .15 * k), 70 - 2 * k, .03)
rumble(W("c15_n1", "curtain"), B("c15_n4"), .10, 30, 140, 1.0)
for k in range(20): splash(A("c15_n3", .2 + .55 * k), .05)
crowd(A("c15_n3"), B("c15_n3", .5), .04)
crowd(A("c16_marcus1", -.2), A("c16_n1", .1), .02); crowd(A("c16_n1", .2), B("c16_n1", 1.0), .06, True); crowd(W("c16_n2", "boos", 0, -.1), W("c16_n2", "boos", 0, 1.2), .07)
for k in range(5): n_ = int(.4 * SR); s_ = np.arange(n_) / SR; m.place(W("c16_n2", "But", 0, .4 + .35 * k), bp(m.noise(n_), 2000, 7000) * (.5 + .5 * np.sin(2 * np.pi * 14 * s_)) * np.sin(np.pi * s_ / .4), .02)
for k in range(3): m.step(A("c17_n1", .3 + .5 * k), .06)
creak(W("c17_n2", "closet", 0, -.1), .03); click(W("c17_n2", "turn", 0, .1), .12); radiohiss(W("c17_n2", "Static"), B("c17_n4", .3), .025)
radiohiss(A("c18_mom1", -.5), B("c18_n2", .5), .012); n_ = int(.15 * SR); s_ = np.arange(n_) / SR; m.place(A("c18_mom1", -.25), np.sin(2 * np.pi * 1200 * s_) * np.exp(-s_ * 20), .04)
heart(W("c18_n1", "heart", 0, .3)); heart(W("c18_n1", "heart", 0, 1.0), .3)
m.whoosh(A("c19_n1"), 1.2, .05, 300, 3000); m.thump(W("c19_n1", "Two"), .15); radiohiss(A("c19_mom1", -.2), B("c19_mom1", .2), .012)
for k in range(4): n_ = int(.25 * SR); s_ = np.arange(n_) / SR; m.place(A("c19_n2", .2 + .3 * k), bp(m.noise(n_), 400, 2500) * np.exp(-s_ * 8), .02)
m.chime(A("c20_n2", .1), 84, .04); m.chime(A("c20_n2", .3), 88, .04); creak(W("c20_n3", "basement", 0, .2), .06); m.thump(B("c20_n3", .6), .25)
# ---------------------------------------------------------------- score
def pluck(f, d=.5): n = int(d * SR); s = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * k * s) * np.exp(-s * (6 + 3 * k)) for k, a in ((1, 1), (2, .35), (3, .15))) * np.minimum(1, s / .004)
def pad(ch, a, b, gg): n = int((b - a) * SR); s = np.arange(n) / SR; m._mus(a, lp(sum(np.sin(2 * np.pi * hz(q) * s) for q in ch), 1100) * np.minimum(1, s) * np.minimum(1, b - a - s), gg)
MOODS = {"play": ([64, 67, 71, 72, 71, 67, 69, 71, 64, 67, 72, 74, 72, 71, 69, 67], [[52, 59, 64], [48, 55, 60], [45, 52, 57], [47, 54, 59]], .30),
         "tense": ([57, 60, 64, 60, 59, 62, 65, 62, 57, 60, 64, 69, 68, 64, 62, 59], [[45, 52, 57], [46, 53, 58], [45, 52, 57], [44, 51, 56]], .32),
         "calm": ([67, 71, 74, 71, 66, 69, 72, 69, 64, 67, 71, 76, 74, 71, 67, 66], [[43, 50, 55], [42, 49, 54], [40, 47, 52], [47, 54, 59]], .46),
         "warm": ([72, 76, 79, 77, 76, 72, 74, 76, 77, 74, 72, 69, 71, 72, 74, 76], [[48, 55, 60], [53, 60, 65], [50, 57, 62], [43, 50, 55]], .42)}
for a_id, b_id, mood in [("c01", "c01", "play"), ("c03", "c04", "calm"), ("c05", "c05", "play"), ("c06", "c06", "calm"), ("c07", "c08", "tense"), ("c09", "c10", "play"), ("c11", "c13", "play"), ("c14", "c14", "warm"), ("c15", "c15", "tense"), ("c16", "c16", "warm"), ("c17", "c17", "calm"), ("c19", "c20", "warm")]:
    a = c0(a_id) + .2; b = c1(b_id) - .2; mel, chs, step = MOODS[mood]; k = 0; q = a
    while q < b - .3:
        if k % 2 == 0 or mood == "play": m._mus(q, pluck(hz(mel[k % 16])), .026, .2 * (-1) ** k)
        if k % 4 == 0: m._mus(q, pluck(hz(chs[(k // 8) % 4][0]), .7), .026)
        q += step; k += 1
    q = a; i = 0
    while q < b - .5: pad(chs[i % 4], q, min(b, q + step * 8), .020); q += step * 8; i += 1
m.render(f"{D}/out/audio.wav"); print("TOTAL", round(TOTAL, 1))
