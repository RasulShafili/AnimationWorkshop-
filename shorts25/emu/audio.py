#!/usr/bin/env python3
"""emu Short: voice + outback bed + SFX on every beat + a cheeky original march motif, −14 LUFS"""
import sys, os, json, numpy as np
D = "/home/rasul/Desktop/Animations/shorts25/emu"; os.environ.update(SHOW_DATA=D + "/out", SHOW_VO=D + "/vo16")
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from audio_lib import Mix, SR, hz, lp, bp, hp
import show25 as S
G = json.load(open(f"{D}/out/global.json")); TOTAL = G["total"]; wt, lt = S.wt, S.lt; m = Mix(int(TOTAL * 30) + 30, seed=3); N = m.N; t = m.t
for l in G["lines"]: m.voice(f"{D}/vo16/{l['id']}.wav", l["t0"] * 30, 1.0)
A = lambda i, d=0.: lt(i) + d
B = lambda i, d=0.: lt(i, 1) + d
W = lambda i, x, n=0, d=0.: wt(i, x, n) + d
m.bed(bp(m.noise(N), 200, 1400), np.ones(N) * (1 + 0 * t), .008, .3, bp(m.noise(N), 200, 1400))
rr = np.random.default_rng(2)
def pop(t0, g=.2): n = int(.25 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(900 + 1200 * s / .25) / SR) * np.exp(-s * 18) * .8, g, 0, .4)
def boing(t0, g=.14): n = int(.7 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(150 + 90 * np.sin(2 * np.pi * 9 * s) * np.exp(-s * 4)) / SR) * np.exp(-s * 4), g, 0, .2)
def click(t0, g=.2): n = int(.06 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 1500, 6000) * np.exp(-s * 110), g)
def drumm(t0, g=.10): n = int(.5 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(95 + 40 * np.exp(-s * 20)) / SR) * np.exp(-s * 9) * (1 + .5 * np.sin(2 * np.pi * 17 * s)), g, 0, .3)   # the emu's drumming boom
def honk(t0, g=.06): n = int(.35 * SR); s = np.arange(n) / SR; m.place(t0, sum(np.sin(2 * np.pi * np.cumsum((230 + 60 * np.sin(np.pi * s / .35)) * k) / SR) / k for k in range(1, 6)) * np.sin(np.pi * s / .35), g, 0, .2)
def feet(a, b, rate=9, g=.10):
    q = a
    while q < b: m.step(q, g * (.6 + .4 * rr.random()), rr.random() - .5); q += 1 / rate
def engine(a, b, g=.05): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, (np.sign(np.sin(2 * np.pi * np.cumsum(46 + 6 * np.sin(2 * np.pi * 1.6 * s)) / SR)) * .5 + bp(m.noise(n), 60, 400)) * np.minimum(1, s / .2) * np.minimum(1, (b - a - s) / .2), g, 0, .2)
def ha(t0, g=.05, f=220):
    for k in range(4): n = int(.16 * SR); s = np.arange(n) / SR; m.place(t0 + .17 * k, (sum(np.sin(2 * np.pi * np.cumsum((f - 15 * k + 30 * np.exp(-s * 20)) * j) / SR) / j for j in (1, 2, 3, 4)) + bp(m.noise(n), 600, 2500) * .4) * np.sin(np.pi * s / .16), g, .3 * (-1) ** k, .3)
for k in range(9): m.step(.1 + .42 * k, .26)
for wd in ("two", "ten", "cameraman"): m.thump(W("c01_n1", wd, 0, -.05), .28)
m.thump(W("c01_n1", "enemy", 0, -.1), .5); honk(W("c01_n1", "birds", 0, .25), .05); drumm(A("c01_n2", .1)); feet(A("c01_n2"), A("c01_n2", 1.6), 7, .06)
for k in range(6): click(W("c01_n2", "eating", 0, .22 * k), .09)
for k, f in enumerate((210, 160, 240)): ha(A("c01_n4", .15 + .12 * k), .045, f); ha(A("c01_n4", .95 + .12 * k), .04, f)
for k in range(5): m.whoosh(B("c01_s1", -.4 + .2 * k), .14, .07, 500, 3000)
m.step(A("c01_n5", .5), .08); m.step(A("c01_n5", .9), .08); boing(W("c01_n5", "split", 0, -.2)); feet(W("c01_n5", "split", 0, -.15), B("c01_n5", .1), 16, .14); m.whoosh(W("c01_n5", "split", 0, -.2), 1.4, .12, 250, 3000)
drumm(W("c01_n6", "thousand", 0, -.1), .12); drumm(W("c01_n6", "thousand", 0, .5), .12); feet(W("c01_n6", "thousand", 0, -.2), W("c01_n6", "perfect", 0, -.3), 12, .07); m.chime(W("c01_n6", "perfect"), 84, .05); click(W("c01_n6", "jammed", 0, -.05), .45); click(W("c01_n6", "jammed", 0, .28), .25); honk(W("c01_n6", "jammed", 0, .55), .07)
engine(A("c01_n7"), B("c01_n7", .05), .05); feet(W("c01_n7", "chased"), B("c01_n7"), 13, .10); m.whoosh(W("c01_n7", "couldn't", 0, .4), .9, .12, 300, 3500); honk(W("c01_n7", "catch", 0, .25), .06)
for k in range(6): boing(W("c01_n7", "bounced", 0, .42 * k), .07); m.thump(W("c01_n7", "bounced", 0, .42 * k), .2)
drumm(W("c01_n8", "lookout"), .10); [click(W("c01_n8", "ate", 0, -.5 + .2 * k), .07) for k in range(5)]
[honk(W("c01_n8", "warned", 0, .1 + .28 * k), .09) for k in range(3)]; feet(W("c01_n8", "warned", 0, .6), B("c01_n8", .1), 16, .13)
for k in range(16): click(A("c01_n9", .05 + .1 * k), .07)
drumm(W("c01_n9", "farms"), .10); m.thump(W("c01_n10", "casualties", 0, -.1), .3); m.thump(W("c01_n10", "dignity", 0, -.2), .45); boing(W("c01_n10", "dignity", 0, .1), .10); m.whoosh(W("c01_n10", "dignity", 0, .5), .5, .08, 300, 2000)
engine(A("c01_n11"), W("c01_n11", "farmers"), .04); pop(W("c01_n11", "something", 0, .2), .15)
for k in range(9): m.thump(A("c01_n12", -.1 + .07 * k), .12); click(A("c01_n12", -.1 + .07 * k), .10)
boing(A("c01_n12", .75), .10); m.thump(W("c01_n13", "war", 0, -.08), .45); drumm(W("c01_n13", "emus"), .10); honk(B("c01_n13", .25), .07); [click(W("c01_n13", "lunch", 0, .2 + .25 * k), .07) for k in range(5)]
def pluck(f, d=.35): n = int(d * SR); s = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * k * s) * np.exp(-s * (9 + 4 * k)) for k, a in ((1, 1), (2, .4), (3, .2))) * np.minimum(1, s / .004)
MEL = [55, 62, 59, 62, 55, 62, 60, 59, 57, 64, 60, 64, 57, 62, 60, 57]; q = .05; k = 0; stop = [(W("c01_n6", "jammed", 0, -.3), W("c01_n6", "jammed", 0, .9)), (A("c01_n12", -.3), A("c01_n12", .9))]
while q < TOTAL - .3:
    if not any(a < q < b for a, b in stop): m._mus(q, pluck(hz(MEL[k % 16])), .030, .25 * (-1) ** k); (m._mus(q, pluck(hz(MEL[k % 16] - 12), .5), .022) if k % 2 == 0 else None)
    q += .26; k += 1
m.render(f"{D}/out/audio.wav"); print("TOTAL", TOTAL)
