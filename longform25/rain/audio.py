#!/usr/bin/env python3
"""rain: voice + a rain bed that changes with the place (outside / inside / none on day 365), SFX cued from the script words, quiet ORIGINAL plucked score, −14 LUFS → out/audio.wav"""
import sys, os, json, numpy as np
D = "/home/rasul/Desktop/Animations/longform25/rain"; os.environ["SHOW_DATA"] = D + "/out"; os.environ["SHOW_VO"] = D + "/vo16"
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25")
from audio_lib import Mix, SR, hz, lp, bp, hp
import show25 as S
G = json.load(open(f"{D}/out/global.json")); TOTAL = G["total"]; wt, lt = S.wt, S.lt; CO = {x["id"]: x for x in G["chapters"]}
m = Mix(int(TOTAL * 30) + 60, seed=11); N = m.N; t = m.t
for l in G["lines"]: m.voice(f"{D}/vo16/{l['id']}.wav", l["t0"] * 30, 1.0)
g = lambda c, x: CO[c]["off"] + x
W = lambda line, word, n=0, d=0.0: g(line[:3], wt(line, word, n)) + d
A = lambda line, d=0.0: g(line[:3], lt(line)) + d
B = lambda line, d=0.0: g(line[:3], lt(line, 1)) + d
def c0(c): return CO[c]["off"]
def c1(c): return CO[c]["off"] + CO[c]["dur"]
# ---------------------------------------------------------------- rain bed: (start, outside level, inside level)
ENV = [(0, 1, .0), (A("c01_coach1", -.75), .12, .9), (c0("c02"), .1, .15), (c0("c03"), .05, .8), (W("c03_n1", "football", 0, -.1), .7, 0), (W("c03_n1", "everybody", 0, -.1), .05, .7), (W("c03_n2", "falling", 0, -.15), .3, 0), (c0("c04"), .95, 0), (W("c04_n1", "weather", 0, -.15), .08, .4), (A("c04_n2"), .95, 0), (W("c04_n2", "About"), .5, 0), (A("c04_n3"), .9, 0), (W("c04_n3", "But"), .5, 0),
       (c0("c05"), .45, 0), (A("c05_n3"), 1, 0), (c0("c06"), 1, 0), (c0("c07"), .9, 0), (W("c07_n1", "If"), .3, 0), (c0("c08"), .05, .7), (A("c08_n2", -.2), 1.15, .3), (W("c08_n2", "After"), .15, 1), (W("c08_n2", "Somehow"), .0, .25), (c0("c09"), .25, .7), (c0("c10"), 1, 0), (W("c10_n1", "Power"), .45, 0), (A("c10_n2"), .95, 0), (W("c10_n2", "drains", 0, -.2), .35, 0), (A("c10_n3"), .95, 0),
       (c0("c11"), .9, 0), (W("c11_n1", "Wet"), .45, 0), (A("c11_n2", -.1), .1, .8), (A("c11_maya1", -.5), .9, 0), (c0("c12"), .85, 0), (W("c12_n2", "Anything"), .4, 0), (W("c12_n2", "It", 0), .85, 0), (c0("c13"), .8, 0), (A("c13_coach1", -.15), .1, .7), (c0("c14"), .15, .3), (A("c14_n2"), .1, .1), (W("c14_n2", "And"), .05, .5), (c0("c15"), .8, 0), (A("c15_n2"), .3, 0), (W("c15_n2", "No"), .85, 0), (W("c15_n3", "So"), .05, .6),
       (c0("c16"), .6, 0), (A("c16_n3"), .4, 0), (W("c16_n3", "So"), .85, 0), (c0("c17"), .9, 0), (W("c17_n2", "Water"), .45, 0), (A("c17_n3"), .6, 0), (c0("c18"), .85, 0), (W("c18_n1", "You", 0), .1, .75), (A("c18_maya1"), .05, .4), (c0("c19"), .8, 0), (c0("c21"), .1, .8), (A("c21_n2"), 1, 0), (W("c21_n2", "In"), .1, .8), (c0("c22"), 1, 0), (c0("c23"), .6, 0), (A("c23_n2"), .3, 0), (c0("c24"), .7, 0), (c1("c24") - .35, .5, 0), (c1("c24"), 0, 0), (TOTAL, 0, 0)]
def curve(k):
    tt = [0.0]; v = [ENV[0][k]]
    for a, b in zip(ENV, ENV[1:]): tt += [b[0] - .12, b[0] + .12]; v += [a[k], b[k]]
    return np.interp(t, tt, v)
nz = lambda: m.noise(N)
hiss = lambda: bp(nz(), 900, 7500) * .55 + bp(nz(), 250, 900) * .55
m.bed(hiss(), curve(1), .050, .25, hiss()); ins = lambda: bp(nz(), 120, 700); m.bed(ins(), curve(2), .052, .25, ins())
rr = np.random.default_rng(5); eo = curve(1); ei = curve(2)
for k in range(int(TOTAL * 7)):                                 # single drops near the listener
    q = rr.random() * TOTAL; e = eo[min(N - 1, int(q * SR))] + .6 * ei[min(N - 1, int(q * SR))]
    if rr.random() > e: continue
    n = int(.07 * SR); s = np.arange(n) / SR; f0 = 900 + 2200 * rr.random(); m.place(q, np.sin(2 * np.pi * f0 * s * (1 + 2 * s)) * np.exp(-s * 85), .010 + .012 * rr.random(), rr.random() * 1.6 - .8, .3)
# ---------------------------------------------------------------- atoms
def pop(t0, g_=.2, up=True):
    n = int(.25 * SR); s = np.arange(n) / SR; f0 = 900 if up else 500; m.place(t0, np.sin(2 * np.pi * np.cumsum(f0 + (1200 if up else -300) * s / .25) / SR) * np.exp(-s * 18) * .8, g_, 0, .4)
def splash(t0, g_=.3, d=1.2):
    n = int(d * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 300, 6000) * np.exp(-s * 4.5) * (1 - np.exp(-s * 90)), g_, 0, .3)
    for k in range(6): pop(t0 + .22 + k * .09, .04, k % 2 == 0)
def swish(t0, g_=.07, d=.7): n = int(d * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 400, 2600) * np.sin(np.pi * s / d) ** 1.5, g_, 0, .3); pop(t0 + d * .6, g_ * .35)
def rows(a, b, rate=.75, g_=.07):
    q = a
    while q < b - .3: swish(q, g_); q += 1 / rate
def boing(t0, g_=.14): n = int(.7 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(150 + 90 * np.sin(2 * np.pi * 9 * s) * np.exp(-s * 4)) / SR) * np.exp(-s * 4), g_, 0, .2)
def click(t0, g_=.13): n = int(.05 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 1500, 6000) * np.exp(-s * 120), g_)
def wood(t0, g_=.2, f=210): n = int(.22 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * f * s) * np.exp(-s * 30) + bp(m.noise(n), 500, 3500) * np.exp(-s * 60) * .6, g_, 0, .3)
def meow(t0, g_=.05): n = int(.6 * SR); s = np.arange(n) / SR; f0 = 520 + 260 * np.sin(np.pi * s / .6); m.place(t0, sum(np.sin(2 * np.pi * np.cumsum(f0 * k) / SR) / k for k in (1, 2, 3, 4)) * np.sin(np.pi * s / .6) ** .7, g_, .2, .2)
def gasp(t0, g_=.04):
    for k in range(6): n = int(.7 * SR); s = np.arange(n) / SR; m.place(t0 + k * .05, bp(m.noise(n), 300, 3000) * np.exp(-s * 2.2), g_)
def rumble(a, b, g_=.2, lo=25, hi_=140, up=.6):
    n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, bp(m.noise(n), lo, hi_) * np.minimum(1, s / up) * np.minimum(1, (b - a - s) / .5), g_, 0, .2)
def roar(a, b, g_=.1): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, (bp(m.noise(n), 80, 600) + .5 * bp(m.noise(n), 600, 3000)) * np.minimum(1, s / (b - a) * 1.4) * np.minimum(1, (b - a - s) / .25), g_, 0, .3)
def gurgle(a, b, g_=.08):
    q = a; k = 0
    while q < b: pop(q, g_ * (.5 + .5 * rr.random()), k % 2 == 0); q += .09 + .10 * rr.random(); k += 1
def plink(t0, p, g_=.06): n = int(.5 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * hz(p) * s) * np.exp(-s * 9) + .4 * np.sin(2 * np.pi * hz(p) * 2.76 * s) * np.exp(-s * 16), g_, rr.random() - .5, .4)
def saw(a, b, g_=.07):
    q = a
    while q < b: n = int(.22 * SR); s = np.arange(n) / SR; m.place(q, bp(m.noise(n), 700, 3200) * np.sin(np.pi * s / .22), g_); q += .24
def crunch(t0, g_=.25): n = int(.5 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 200, 2500) * np.exp(-s * 9) * (1 + np.sin(2 * np.pi * 40 * s)), g_, 0, .3); m.thump(t0, g_)
def snap(t0, g_=.35): n = int(.3 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 900, 7000) * np.exp(-s * 45) + np.sin(2 * np.pi * np.cumsum(700 * np.exp(-s * 12)) / SR) * np.exp(-s * 14) * .6, g_, 0, .4)
def chirps(a, b, g_=.014):
    q = a + .3; k = 0
    while q < b - .3: m.chime(q, 96 + (k * 2) % 7, g_); q += .5 + (k % 3) * .41; k += 1
def radiohiss(a, b, g_=.03): n = int((b - a) * SR); s = np.arange(n) / SR; m.place(a, bp(m.noise(n), 900, 2600) * (.6 + .4 * np.sin(2 * np.pi * 3 * s)) * np.minimum(1, s / .1) * np.minimum(1, (b - a - s) / .1), g_)
# ---------------------------------------------------------------- cues
rows(.1, A("c01_coach1", -.9), .75, .08); meow(1.3, .035); m.thump(A("c01_coach1", -.7), .2); splash(A("c01_coach1", -.7), .12); m.whoosh(c0("c02"), 1.8, .12, 200, 3000); m.thump(A("c02_n1", .1), .3)
pop(c0("c03") + .1, .12); boing(W("c03_n1", "cancelled", 0, -.1), .12); pop(W("c03_n2", "falling", 0, -.1), .15); m.thump(W("c03_n2", "don't", 0, .1), .2); boing(W("c03_n2", "round", 0, -.2), .14); pop(W("c03_n2", "hamburger", 0, 0), .18)
for k in range(7): pop(W("c04_n1", "weather", 0, .0) + .12 * k, .09)
gurgle(W("c04_n2", "About"), W("c04_n2", "About") + 1.6, .05); m.whoosh(W("c04_n3", "one"), 2.4, .09, 150, 2500); m.thump(W("c04_n3", "thirty"), .25)
gurgle(A("c05_n1", .3), B("c05_n1"), .035); pop(W("c05_n1", "sponge"), .15); boing(W("c05_n1", "sponge", 0, .1), .08); m.thump(W("c05_n2", "fills"), .3); m.whoosh(W("c05_n2", "every"), 1.4, .10, 250, 2500); swish(A("c05_n3"), .16, 1.4)
splash(A("c06_n1", 1.2), .24); swish(W("c06_n1", "Thirty"), .14, 1.2); m.whoosh(W("c06_n1", "Sixty"), 1.6, .12, 120, 1500); m.thump(W("c06_n1", "Sixty"), .25); swish(A("c06_n2", .3), .14, 1.5); m.chime(W("c06_n2", "loves"), 84, .06); m.chime(W("c06_n2", "loves", 0, .18), 88, .06)
for k in range(8): m.step(A("c06_coach1", -.1 + .24 * k), .2); 
for k in range(5): swish(A("c06_coach1", .1 + .4 * k), .08, .4)
gurgle(W("c07_n1", "squeezed"), W("c07_n1", "squeezed") + 2, .05); m.whoosh(W("c07_n1", "only", 0, -.9), 1.2, .08, 200, 2500); pop(W("c07_n1", "only"), .2); m.whoosh(W("c07_n2", "evaporates"), .7, .07, 300, 4000); m.whoosh(W("c07_n2", "blows"), .8, .08, 300, 3000); swish(W("c07_n2", "runs"), .12, 1.0); rumble(A("c07_n3"), B("c07_n3"), .10, 50, 200); m.thump(W("c07_n3", "maximum"), .3); m.whoosh(A("c07_n4", .4), 1.2, .07, 200, 1500)
for k, wd in enumerate(("shoes", "curtains", "bread")): gurgle(W("c08_n1", wd, 0, -.2), W("c08_n1", wd, 0, .5), .05); boing(W("c08_n1", wd, 0, .25), .07)
pop(W("c08_mom1", "green", 0, 0), .06); m.thump(c0("c09") + 1.05, .45); wood(c0("c09") + 1.05, .3, 130); splash(c0("c09") + 1.1, .28, 2.0); gasp(c0("c09") + 1.3); swish(A("c09_n2"), .10, 1.0); wood(W("c09_n2", "sofa"), .1, 150); boing(W("c09_n2", "fridge"), .10); meow(W("c09_n2", "boat"), .035)
for k in range(8): wood(A("c09_n3", .1 + .28 * k), .10, 160 + 10 * (k % 2))
swish(W("c09_n3", "cat", 0, -.1), .12); meow(W("c09_n3", "carries", 1, .2), .05)
for k in range(7): click(c0("c10") + 1.2 + .22 * k, .16)
rumble(c0("c10") + 1.2, c0("c10") + 2.9, .12, 30, 90); m.whoosh(W("c10_n1", "Now"), 1.4, .12, 120, 1800)
for k in range(3): snap(W("c10_n1", "inside", 0, .2 + .3 * k), .10)
gurgle(W("c10_n2", "drains"), B("c10_n2"), .07)
for k in range(22): plink(A("c10_n3", .4 + .31 * k), (72, 76, 79, 84, 81, 74)[(k * 5) % 6], .045)
pop(A("c11_n1", .2), .08); m.thump(W("c11_n1", "heavy"), .28); m.thump(W("c11_n1", "slippery"), .28); rumble(W("c11_n1", "just"), B("c11_n1", .3), .22); rumble(A("c11_n2", .7), B("c11_n2", .4), .34, 25, 160); crunch(A("c11_n2", 1.0), .14)
for k in range(3): n = int(.5 * SR); s = np.arange(n) / SR; m.place(W("c11_n2", "swing") + .7 * k, np.sin(2 * np.pi * np.cumsum(820 + 160 * np.sin(np.pi * s / .5)) / SR) * np.sin(np.pi * s / .5), .018)
rows(A("c11_maya1", -.5), B("c11_maya1", .6), .8, .05)
for k, wd in enumerate(("You", "mom", "Maya", "Maya's", "Leo")): pop(W("c12_n1", wd, 0, 0), .08)
meow(W("c12_n1", "hates", 0, -.1), .07); m.thump(W("c12_n1", "hates"), .15)
for k in range(9): wood(A("c12_n2", .1 + .57 * k), .16, 240)
gurgle(W("c12_n2", "Anything"), W("c12_n2", "Anything") + 1.6, .04); q0 = W("c12_n2", "It", 0, -.1); L3 = (c1("c12") - q0) / 3
gurgle(q0 + .3, q0 + L3, .06); splash(q0 + L3 + .7, .26); m.chime(q0 + 2 * L3 + .1, 84, .07); m.chime(q0 + 2 * L3 + .25, 88, .07); m.chime(q0 + 2 * L3 + .4, 91, .07)
rows(c0("c13") + .2, W("c13_n1", "There's"), .7, .05)
for k in range(8): click(W("c13_n1", "barber", 0, -.1 + .2 * k), .10)
rows(W("c13_n1", "school", 0, -.3), A("c13_coach1", -.2), .7, .05)
pop(W("c14_n1", "Roots"), .12); gurgle(W("c14_n1", "drowns"), B("c14_n1", .2), .05)
for wd in ("Rice", "Mushrooms", "Watercress"): pop(W("c14_n2", wd, 0, -.05), .18)
swish(W("c14_n2", "fish", 0, -.4), .12); splash(A("c14_n3", .3), .14)
m.whoosh(A("c15_n2", .9), .6, .06, 300, 3000); pop(A("c15_n2", 1.2), .12); m.thump(W("c15_n2", "No"), .12)
for k in range(5): m.whoosh(W("c15_n3", "paints", 0, -.1 + .5 * k), .4, .05, 1200, 6000)
m.chime(W("c15_n3", "big", 0, 0), 79, .06); m.chime(W("c15_n3", "big", 0, .2), 83, .06); m.chime(W("c15_n3", "big", 0, .4), 86, .07)
m.whoosh(W("c16_n1", "three", 0, -.1), 1.3, .06, 300, 3000); m.thump(W("c16_n1", "row", 0, -.2), .2); m.whoosh(A("c16_n2"), 1.6, .09, 120, 1500); rumble(W("c16_n2", "rainy"), B("c16_n2"), .07, 30, 100); m.thump(W("c16_n3", "dinosaurs"), .4)
for k in range(8): m.thump(W("c16_n3", "dinosaurs", 0, .3 + .28 * k), .14)
radiohiss(c0("c17") + .2, W("c17_n1", "Dam", 0, -.2), .035); m.thump(W("c17_n1", "Dam", 0, -.05), .5); roar(W("c17_n1", "Dam"), B("c17_n2"), .035); rumble(W("c17_n2", "Water"), B("c17_n2"), .14, 25, 90); m.thump(A("c17_n3", .05), .18); rumble(W("c17_n3", "Nobody"), c1("c17"), .26, 25, 120)
for k in range(5): crunch(W("c17_n3", "Nobody", 0, .5 + .45 * k), .10)
rows(c0("c18") + .1, W("c18_n1", "You", 0, -.1), .75, .07); splash(W("c18_n1", "climb", 0, .2), .10); m.whoosh(W("c18_n1", "open"), .5, .06, 800, 5000); tr = B("c18_n2", -1.0); m.thump(tr, .6); rumble(tr, c1("c18"), .42, 22, 120, .08); gasp(tr + .3)
crunch(c0("c19") + .25, .45); roar(c0("c19") + .2, W("c19_n1", "and"), .13); rumble(c0("c19") + .2, W("c19_n1", "and"), .30); m.thump(W("c19_n1", "ten"), .4); rumble(W("c19_n1", "and"), c1("c19"), .08, 25, 100); swish(W("c19_n3", "wave"), .14, 1.6); gurgle(W("c19_n3", "holding"), B("c19_n3", .2), .06); m.thump(A("c19_maya1", -.1), .2)
snap(c0("c20") + .55, .30)
for k in range(3): snap(W("c20_n1", "coach", 0, -.25 + .55 + .42 * k), .28)
for k in range(9): snap(W("c20_n1", "Roof", 0, .2 + .34 * k), .13); 
rumble(W("c20_n1", "Roof"), c1("c20"), .12, 25, 110); gasp(A("c20_maya1", -.3)); m.thump(A("c20_maya1", -.2), .3)
for k in range(7): wood(c0("c21") + .4 + .75 * k, .10, 180)
rows(A("c21_n2"), W("c21_n2", "In"), 1.7, .13); rows(W("c21_n2", "In"), A("c21_leo1", -.2), 1.5, .08); splash(W("c21_n2", "In", 0, .1), .18); crunch(W("c21_n3", "one", 0, .1), .22); m.chime(W("c21_n3", "hugs"), 84, .06); rows(W("c21_n3", "and", 0), c1("c21"), 1.5, .09); rumble(c0("c21"), c1("c21"), .14, 25, 110)
roar(c0("c22"), B("c22_n3", .2), .17); rumble(c0("c22"), B("c22_n3", .2), .26); sn = W("c22_n2", "snaps", 0, -.05); saw(A("c22_n2"), sn - .2, .09); snap(sn, .55); m.whoosh(sn + .1, 1.2, .2, 200, 4000); m.whoosh(A("c22_n3"), 2.6, .24, 120, 3500); splash(A("c22_n3", .2), .30, 2.0); gasp(A("c22_n3", .2), .06); m.whoosh(W("c22_n3", "wave"), 3.0, .20, 100, 2000); m.chime(B("c22_n3", .9), 79, .06); m.chime(B("c22_n3", 1.2), 83, .06); m.chime(B("c22_n3", 1.5), 86, .07)
rumble(c0("c23"), A("c23_n2"), .05, 30, 100); m.thump(A("c23_n2", .75), .3); wood(A("c23_n2", .75), .2, 130); m.chime(W("c23_n2", "hill"), 84, .05)
for k in range(8): m.step(W("c23_n2", "Even", 0, .1 + .24 * k), .15)
m.thump(A("c23_coach1", .0), .2); m.chime(B("c23_coach1", .1), 88, .06)
rows(c0("c24") + .2, W("c24_n1", "They"), .8, .05); splash(W("c24_n1", "Babies", 0, .2), .08); splash(W("c24_n1", "cat", 0, .85), .16); meow(W("c24_n1", "cat", 0, 1.4), .05)
for k in range(3): m.chime(W("c24_n2", "People", 0, .4 + .7 * k), 79 + 4 * k, .05)
qd = [B("c25_n3") - 1.0 - 4.2 + 1.6 * k for k in range(0)]
tl = W("c25_n3", "line", 0, -.2); [m.chime(tl + .55 * k, (72, 76, 79, 83, 84)[k], .035) for k in range(5)]; m.chime(W("c25_n3", "face"), 88, .07); plink(W("c25_n3", "roof", 0, .5), 79, .05); plink(W("c25_n3", "roof", 0, 1.5), 76, .035)
chirps(tl + 1, c1("c28") - 4, .012); ws = W("c26_n1", "screams"); gasp(ws, .05); m.thump(ws, .2); boing(W("c26_n1", "stuck"), .10)
for k in range(14): m.step(A("c26_leo1", -.1 + .17 * k), .12)
pop(W("c26_n2", "shadow"), .15); m.chime(W("c26_n2", "year"), 84, .06)
swish(A("c27_n1", .2), .14, 1.6); 
for k in range(4): swish(W("c27_n1", "leaves", 0, .1 + .55 * k), .05, .4)
for k in range(11): pop(W("c27_n1", "But", 0, .3 + .10 * k), .06)
m.chime(W("c27_n1", "green"), 84, .06); m.whoosh(A("c27_n2", .4), 1.6, .06, 400, 3000)
for k in range(4): click(c0("c28") + .6 + .75 * k, .05)
hear = B("c28_n2", .15); plink(hear, 84, .16); pop(hear, .12); splash(hear, .05, .5); m.thump(hear + .75, .15)
for k in range(3): plink(A("c28_n4", .9 + 1.1 * k), 84, .10)
m.thump(A("c28_coach1", -.25), .35); boing(A("c28_coach1", -.2), .10); m.thump(B("c28_coach1", .4), .25)
for k in range(5): plink(B("c28_coach1", .8 + .4 * k), (72, 76, 79, 84, 81)[k], .06)
# ---------------------------------------------------------------- score
def pluck(f, d=.5): n = int(d * SR); s = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * k * s) * np.exp(-s * (6 + 3 * k)) for k, a in ((1, 1), (2, .35), (3, .15))) * np.minimum(1, s / .004)
def pad(ch, a, b, gg): n = int((b - a) * SR); s = np.arange(n) / SR; m._mus(a, lp(sum(np.sin(2 * np.pi * hz(q) * s) for q in ch), 1100) * np.minimum(1, s) * np.minimum(1, b - a - s), gg)
MOODS = {"play": ([62, 66, 69, 74, 73, 69, 66, 64, 62, 67, 71, 69, 66, 64, 61, 64], [[50, 57, 62], [47, 54, 59], [43, 50, 55], [45, 52, 57]], .30),
         "tense": ([59, 62, 66, 62, 61, 64, 67, 64, 59, 62, 66, 71, 70, 66, 64, 61], [[47, 54, 59], [48, 55, 60], [47, 54, 59], [46, 53, 58]], .30),
         "calm": ([66, 69, 73, 69, 64, 68, 71, 68, 62, 66, 69, 74, 73, 69, 66, 64], [[42, 49, 54], [40, 47, 52], [38, 45, 50], [45, 52, 57]], .46),
         "warm": ([69, 73, 76, 74, 73, 69, 71, 73, 74, 71, 69, 66, 68, 69, 71, 73], [[45, 52, 57], [50, 57, 62], [47, 54, 59], [40, 47, 52]], .42)}
for a_id, b_id, mood in [("c01", "c04", "play"), ("c05", "c07", "calm"), ("c08", "c09", "play"), ("c10", "c11", "tense"), ("c12", "c14", "play"), ("c15", "c16", "calm"), ("c17", "c22", "tense"), ("c23", "c24", "warm"), ("c26", "c27", "warm"), ("c28", "c28", "play")]:
    a = c0(a_id) + .2; b = (c1(b_id) if b_id != "c28" else A("c28_n2", -.3)) - .2; mel, chs, step = MOODS[mood]; k = 0; q = a
    while q < b - .3:
        if k % 2 == 0 or mood == "play": m._mus(q, pluck(hz(mel[k % 16])), .028, .2 * (-1) ** k)
        if k % 4 == 0: m._mus(q, pluck(hz(chs[(k // 8) % 4][0]), .7), .028)
        q += step; k += 1
    q = a; i = 0
    while q < b - .5: pad(chs[i % 4], q, min(b, q + step * 8), .021); q += step * 8; i += 1
m.render(f"{D}/out/audio.wav"); print("TOTAL", round(TOTAL, 1))
