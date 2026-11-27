#!/usr/bin/env python3
"""mafia: voice + a place bed (street / room / night / engine), SFX cued from script words, quiet ORIGINAL plucked score, −14 LUFS → out/audio.wav"""
import sys, os, json, numpy as np
D = "/home/rasul/Desktop/Animations/longform25/mafia"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"
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
# ---------------------------------------------------------------- place beds: (start, street, room, night, engine)
ENV = [(0, .6, 0, 0, 1), (c0("c02"), 0, .7, 0, 0), (A("c02_n3", -.1), 0, 0, .8, .6), (W("c02_n3", "river", 0, .3), 0, 0, 0, 0), (A("c02_n4", -.1), 0, .8, 0, 0), (c0("c03"), 0, .8, 0, 0), (c0("c04"), .3, .4, 0, 0),
       (A("c04_n3", -.1), 0, .5, 0, 0), (A("c04_n4", -.1), 0, .8, 0, 0), (A("c04_old1", -.3), .3, .4, 0, 0), (c0("c05"), 0, .8, 0, 0), (W("c05_n1", "Real", 0, -.1), 1, 0, 0, 0), (A("c05_n2", -.1), 0, .8, 0, 0),
       (c0("c06"), .5, 0, 0, 0), (c0("c07"), 0, .8, 0, 0), (A("c07_n3", -.1), .7, 0, 0, .5), (A("c07_n4", -.1), .2, 0, 0, .8), (c0("c08"), .6, 0, 0, 1), (A("c08_n2", -.1), .3, 0, .4, .3), (A("c08_baby1", -.2), .6, 0, 0, 1),
       (W("c08_n4", "other", 0, .5), .6, 0, 0, 0), (A("c08_n5", -.1), .3, .3, 0, 0), (c0("c09"), 0, .8, 0, 0), (A("c09_n4", -.1), 0, .2, .9, 0), (c0("c10"), 0, .8, 0, 0), (A("c10_n4", -.1), 0, .2, .7, 0), (A("c10_n5", -.1), 0, .8, 0, 0),
       (c0("c11"), 0, .8, 0, 0), (W("c11_n1", "witness", 0, -.1), .6, 0, .4, 0), (A("c11_n2", -.1), 0, .5, 0, 0), (A("c11_n3", -.1), .5, 0, 0, 0), (c0("c12"), 0, .7, 0, 0), (A("c12_don1", -.1), 0, .3, .8, 0), (A("c12_n3", -.1), 0, .6, .3, 0)]
def curve(k):
    tt = [0.0]; v = [ENV[0][k]]
    for a, b in zip(ENV, ENV[1:]): tt += [b[0] - .15, b[0] + .15]; v += [a[k], b[k]]
    return np.interp(t, tt, v)
street = lambda: bp(nz(), 120, 1100) * .6 + bp(nz(), 2500, 7000) * .12
m.bed(street(), curve(1), .030, .25, street()); room = lambda: lp(nz(), 380); m.bed(room(), curve(2), .022, .25, room()); night = lambda: lp(nz(), 300); m.bed(night(), curve(3), .020, .25, night())
ce = curve(4); n_ = N; s_ = np.arange(n_) / SR; eng = (np.sign(np.sin(2 * np.pi * (55 + 18 * np.sin(2 * np.pi * .23 * s_)) * s_)) * .35 + bp(nz(), 40, 400)) * ce; m.place(0, lp(eng, 900), .05, 0, .2)
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
squeal(.4, .05, 1.2); horn(1.6, .05); siren(A("c01_n2"), B("c01_n2", 2.0), .02); m.whoosh(B("c01_n2", .2), 1.6, .10, 200, 3000); m.thump(B("c01_n2", .3), .35)
click(A("c02_n1", .2), .1); m.whoosh(W("c02_n2", "Real", 0, -.1), .6, .05, 400, 3000)
squeal(W("c02_n3", "slid", 0, -.1), .05, 1.4); crunch(W("c02_n3", "bridge", 0, .2), .3); splash(W("c02_n3", "river", 0, .1), .25, 1.6); rumble(W("c02_n3", "river", 0, .2), A("c02_n4"), .06, 30, 200)
m.chime(W("c02_n4", "woke"), 84, .03); m.chime(W("c02_n4", "Warm"), 88, .025); heart(W("c02_n5", "reborn", 0, -.2), .35)
for k, wd in enumerate(("one", "two", "three", "four")): pop(W(f"c03_n{(1, 2, 3, 5)[k]}", "Problem", 0, .05), .09)
cry(A("c03_baby1", -.1), B("c03_baby1"), .015); boing(W("c03_n2", "bowling"), .06)
for k in range(3): pop(W("c03_n5", "asleep", 0, .3 + .25 * k), .04, False)
crowd(c0("c04"), A("c04_n3"), .03); [clink(W("c04_n1", "envelope", 0, .2 * k), .03) for k in range(3)]; m.whoosh(A("c04_n3", -.1), 1.0, .06, 200, 2500)
for wd in ("boss", "underboss", "consigliere", "captains", "soldiers"): m.thump(W("c04_n3", wd, 0, -.05), .15)
m.thump(W("c04_n4", "Omert"), .25); crowd(A("c04_old1", -.3), c1("c04"), .02)
for k in range(8): m.place(A("c05_n1", .3 + .45 * k), np.sin(2 * np.pi * 2200 * np.arange(int(.05 * SR)) / SR) * .5, .02)
for k in range(8): m.step(W("c05_n1", "walks", 0, .2 + .45 * k), .06)
pop(W("c05_n4", "teddy"), .1); n_ = int(1.0 * SR); s_ = np.arange(n_) / SR; m.place(A("c05_n5", .1), bp(m.noise(n_), 2000, 6000) * (np.sin(2 * np.pi * 18 * s_) > 0) * .5, .04)
for k in range(4): m.chime(W("c06_n4", "BEAR"[k], 0, 0), 76 + 3 * k, .04); click(W("c06_n4", "BEAR"[k]), .1)
for k in range(6): m.chime(A("c06_n1", .5 + .9 * k), 93 + (k % 3), .006)
m.chime(W("c06_dana1", "Why"), 70, .02); n_ = int(1.2 * SR); s_ = np.arange(n_) / SR; m.place(W("c06_n5", "writes"), bp(m.noise(n_), 3000, 7000) * (.5 + .5 * np.sin(2 * np.pi * 9 * s_)), .02)
m.chime(A("c07_n1", .2), 96, .03); m.chime(A("c07_n1", .5), 96, .03); m.thump(W("c07_n3", "third"), .2)
cry(A("c07_n4", .2), B("c07_mom1"), .03); squeal(W("c07_n5", "spins", 0, -.1), .06, 1.2); squeal(W("c07_n5", "spin", 1, -.1), .05, 1.0)
squeal(A("c08_n6", .2), .04, .8); horn(W("c08_n6", "red", 0, .1), .05); crunch(W("c08_n6", "fruit", 0, .25), .3); [pop(W("c08_n6", "oranges", 0, .1 * k), .04, False) for k in range(6)]; horn(W("c08_n6", "bus", 0, .1), .12, .9)
squeal(W("c08_baby1", "Left", 0, .3), .07, 1.4); pop(W("c08_n3", "pacifier", 0, .1), .15)
n_ = int(1.2 * SR); s_ = np.arange(n_) / SR; m.place(W("c08_n4", "two"), bp(m.noise(n_), 2500, 8000) * (.6 + .4 * np.sin(2 * np.pi * 30 * s_)), .06)
cans_(W("c08_n4", "trash", 0, -.1)); crunch(W("c08_n4", "other", 0, .5), .4); siren(W("c08_n4", "sirens"), B("c08_sal1", .5), .04)
crowd(A("c08_n5"), c1("c08"), .03, True); [clink(A("c08_n5", .5 + .15 * k), .03) for k in range(3)]
m.thump(W("c09_n2", "RICO"), .2); gavel_(A("c09_n3", 1.2)); m.thump(W("c09_n3", "hundred"), .3)
door_bang(W("c10_n1", "explodes")); [m.step(W("c10_n1", "explodes", 0, .3 + .18 * k), .15) for k in range(10)]
for wd in ("office", "walls", "cars", "freezer"): m.thump(W("c10_n2", wd, 0, -.05), .12)
for k in range(6): m.thump(W("c10_n2", "walls", 0, .2 + .3 * k), .08, 160)
heart(W("c10_n5", "throw", 0, -.4), .3); m.whoosh(W("c10_n5", "throw", 0, .1), .9, .08, 300, 3000); m.thump(A("c10_n6", .1), .12)
gavel_(A("c11_n1", 1.0)); rumble(W("c11_n1", "witness"), A("c11_n2"), .04, 30, 110)
for k in range(14): pop(A("c11_n2", .5 + .3 * k), .02)
crowd(W("c11_n3", "Uncle"), W("c11_n3", "Nobody", 0, 1.5), .03, True); clink(W("c11_n4", "winks"), .05)
for k in range(3): m.chime(A("c12_n1", .1 + .2 * k), 84 + 4 * k, .03)
click(W("c12_n1", "letter"), .1); n_ = int(.8 * SR); s_ = np.arange(n_) / SR; m.place(W("c12_n1", "Inside", 0, -.3), bp(m.noise(n_), 1500, 6000) * np.exp(-s_ * 3), .05)
heart(B("c12_don1", .2), .4); heart(B("c12_don1", .9), .3); creak(W("c12_n3", "subscribe"), .05); m.thump(B("c12_n3", .6), .25)
# ---------------------------------------------------------------- score
def pluck(f, d=.5): n = int(d * SR); s = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * k * s) * np.exp(-s * (6 + 3 * k)) for k, a in ((1, 1), (2, .35), (3, .15))) * np.minimum(1, s / .004)
def pad(ch, a, b, gg): n = int((b - a) * SR); s = np.arange(n) / SR; m._mus(a, lp(sum(np.sin(2 * np.pi * hz(q) * s) for q in ch), 1100) * np.minimum(1, s) * np.minimum(1, b - a - s), gg)
MOODS = {"play": ([64, 67, 71, 72, 71, 67, 69, 71, 64, 67, 72, 74, 72, 71, 69, 67], [[52, 59, 64], [48, 55, 60], [45, 52, 57], [47, 54, 59]], .30),
         "tense": ([57, 60, 64, 60, 59, 62, 65, 62, 57, 60, 64, 69, 68, 64, 62, 59], [[45, 52, 57], [46, 53, 58], [45, 52, 57], [44, 51, 56]], .32),
         "calm": ([67, 71, 74, 71, 66, 69, 72, 69, 64, 67, 71, 76, 74, 71, 67, 66], [[43, 50, 55], [42, 49, 54], [40, 47, 52], [47, 54, 59]], .46),
         "warm": ([72, 76, 79, 77, 76, 72, 74, 76, 77, 74, 72, 69, 71, 72, 74, 76], [[48, 55, 60], [53, 60, 65], [50, 57, 62], [43, 50, 55]], .42)}
for a_id, b_id, mood in [("c01", "c01", "tense"), ("c02", "c02", "calm"), ("c03", "c03", "play"), ("c04", "c04", "warm"), ("c05", "c06", "play"), ("c07", "c08", "tense"), ("c09", "c09", "calm"), ("c10", "c10", "tense"), ("c11", "c11", "warm"), ("c12", "c12", "calm")]:
    a = c0(a_id) + .2; b = c1(b_id) - .2; mel, chs, step = MOODS[mood]; k = 0; q = a
    while q < b - .3:
        if k % 2 == 0 or mood == "play": m._mus(q, pluck(hz(mel[k % 16])), .026, .2 * (-1) ** k)
        if k % 4 == 0: m._mus(q, pluck(hz(chs[(k // 8) % 4][0]), .7), .026)
        q += step; k += 1
    q = a; i = 0
    while q < b - .5: pad(chs[i % 4], q, min(b, q + step * 8), .020); q += step * 8; i += 1
m.render(f"{D}/out/audio.wav"); print("TOTAL", round(TOTAL, 1))
