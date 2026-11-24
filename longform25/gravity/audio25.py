#!/usr/bin/env python3
"""Whole-video audio for gravity: VO lines at their global times, zero-g moments (lift whoosh + weightless shimmer + thump on return),
an ambience bed per location, a quiet ORIGINAL plucked score that changes mood with the story, −14 LUFS.
Also writes out/vo_only.wav (for word timings) and out/global.json (chapter offsets + global line times).
  python3 tools/audio_all.py"""
import sys, json, os, numpy as np
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools")
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform3d/gravity")
from audio_lib import Mix, SR, hz, lp, bp, hp
from scipy.io import wavfile
from order import ORDER
D = "/home/rasul/Desktop/Animations/longform3d/gravity"
FPS = 24
chap = []; off = 0.0
for c in ORDER:
    J = json.load(open(f"{D}/out/{c}_timeline.json")); NF = int(J["end"] * FPS) + 1; dur = NF / FPS
    chap.append({"id": c, "off": off, "dur": dur, "J": J}); off += dur
TOTAL = off
json.dump({"total": TOTAL, "chapters": [{"id": x["id"], "off": x["off"], "dur": x["dur"]} for x in chap],
           "lines": [{"id": l["id"], "t0": x["off"] + l["t0"], "t1": x["off"] + l["t1"], "who": l["who"]} for x in chap for l in x["J"]["lines"]]},
          open("/home/rasul/Desktop/Animations/longform25/gravity/out/global_copy.json", "w"), indent=1)
m = Mix(int(TOTAL * 30) + 60, seed=7); N = m.N; t = m.t
vo_only = np.zeros(N)
def load16(p):
    sr, y = wavfile.read(p); y = y.astype(float) / 32768
    return np.interp(np.arange(int(len(y) * SR / sr)) * sr / SR, np.arange(len(y)), y)
for x in chap:
    for l in x["J"]["lines"]:
        for k, f in enumerate(l["files"]):
            a = x["off"] + l["t0"]; m.voice(f"{D}/vo16/{f}", a * 30, 1.0)
            y = load16(f"{D}/vo16/{f}"); i = int(a * SR); j = min(N, i + len(y)); vo_only[i:j] += y[:j - i]
wavfile.write("/home/rasul/Desktop/Animations/longform25/gravity/out/vo_only.wav", SR, (vo_only / (np.abs(vo_only).max() + 1e-9) * 30000).astype(np.int16))
# ---------------------------------------------------------------- sfx atoms
def seg_env(a, b, fade=0.5): return np.clip(np.minimum((t - a) / fade, (b - t) / fade), 0, 1)
def pop(t0, g=0.3, out=True):
    n = int(0.25 * SR); s = np.arange(n) / SR
    f0 = 900 if out else 500; sweep = np.sin(2 * np.pi * np.cumsum(f0 + (1200 if out else -300) * s / 0.25) / SR) * np.exp(-s * 18)
    m.place(t0, sweep * 0.8 + bp(m.noise(n), 1500, 7000) * np.exp(-s * 30) * 0.5, g, 0, .4); m.whoosh(t0 - (0.12 if out else 0.0), 0.3, g * 0.35, 600, 6000)
def crackle(a, b, g=0.08):
    n = int((b - a) * SR)
    if n <= 0: return
    s = np.arange(n) / SR; buzz = np.sign(np.sin(2 * np.pi * 110 * s)) * (np.random.default_rng(int(a * 10)).random(n) < 0.02) + bp(m.noise(n), 3000, 8000) * 0.3
    m.place(a, buzz * np.minimum(1, s / 0.1) * np.minimum(1, (b - a - s) / 0.1), g, 0, .3)
def bed_noise(lo, hi, a, b, g, wob=0.0, rate=0.15):
    x = bp(m.noise(N), lo, hi); x2 = bp(m.noise(N), lo, hi)
    e = seg_env(a, b, 0.4) * (1 + wob * np.sin(2 * np.pi * rate * t)); m.bed(x, e, g, .4, x2)
def chirps(a, b, g=0.02):
    tt = a + 0.3; k = 0
    while tt < b - 0.3: m.chime(tt, 96 + (k % 5), g); tt += 0.6 + (k % 3) * 0.37; k += 1
AMB = {   # set → ambience
    "kitchen_dressed": lambda a, b: bed_noise(150, 900, a, b, 0.005),
    "living_room": lambda a, b: bed_noise(150, 900, a, b, 0.004),
    "space": lambda a, b: bed_noise(40, 140, a, b, 0.02),
    "street_dressed": lambda a, b: (bed_noise(60, 500, a, b, 0.025), chirps(a, b, 0.01)),
    "backyard": lambda a, b: (bed_noise(200, 1500, a, b, 0.006), chirps(a, b)),
    "bathroom": lambda a, b: bed_noise(300, 2500, a, b, 0.006),
    "classroom_dressed": lambda a, b: bed_noise(200, 1200, a, b, 0.006),
    "gym": lambda a, b: bed_noise(200, 2000, a, b, 0.012, 0.2, 0.3),
    "bedroom_tp": lambda a, b: bed_noise(150, 900, a, b, 0.004),
    "beach": lambda a, b: bed_noise(150, 2000, a, b, 0.045, 0.8, 0.1),
}
def zero_g(a, b, g=0.05):
    """the stomach-lift: rising whoosh, a high glassy shimmer while weightless, a soft thump when gravity returns"""
    m.whoosh(a - 0.1, 0.6, g * 1.6, 300, 4000)
    n = int(max(0.2, b - a) * SR); x = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * x + 0.8 * np.sin(2 * np.pi * 0.7 * x)) for f in (880, 1320, 1760)) * np.minimum(1, x / 0.4) * np.minimum(1, (n / SR - x) / 0.3)
    m.place(a, y * 0.25, g, 0, .5)
for x in chap:
    a, b = x["off"], x["off"] + x["dur"]; f = AMB.get(x["J"].get("set"))
    if f: f(a, b)
# ---- cues of the 2.5D cut (global seconds), taken from the scene code
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25"); sys.path.insert(0, "/home/rasul/Desktop/Animations/longform25/gravity")
import show25 as S, scenes_b as SB, scenes_f as SF
wt, lt = S.wt, S.lt; O_ = {c: S.CH[c]["off"] for c in S.CH}; g = lambda c, t: O_[c] + t
Z = [(4.95, 17.08), (g("c06", lt("c06_n2") + .3), g("c06", 12.6)), (g("c08", SB.TZ8), g("c08", SB.T8B)), (g("c11", lt("c11_n2") - .3), g("c11", 13.2)), (g("c12", wt("c12_n1", "slides") - .25), g("c12", wt("c12_n1", "slides") + 2.4)),
     (g("c14", wt("c14_n1", "stomach") - .1), g("c14", 7.0)), (g("c15", 10.2), g("c17", wt("c17_n1", "comes") + .1)), (g("c18", wt("c18_n1", "that") - .15), g("c19", wt("c19_n1", "gravity") + .45)), (g("c21", wt("c21_n1", "gravity") - .1), g("c22", 9.0)), (g("c25", wt("c25_n1", "When") - .1), g("c25", wt("c25_n1", "Only") + .9)), (g("c27", 1.0), g("c27", 11.5)), (g("c27", wt("c27_n2", "push") - .05), g("c27", wt("c27_n2", "before") + 1.1)), (SF.GZ, SF.GB)]
for za, zb in Z: zero_g(za, min(zb, za + 9), .045)
def splash(t0, g_=.3):
    n = int(1.2 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 300, 6000) * np.exp(-s * 4.5) * (1 - np.exp(-s * 90)), g_, 0, .3); m.thump(t0, g_)
    for k in range(7): pop(t0 + .25 + k * .09, .05, k % 2 == 0)
def boing(t0, g_=.16):
    n = int(.7 * SR); s = np.arange(n) / SR; m.place(t0, np.sin(2 * np.pi * np.cumsum(150 + 90 * np.sin(2 * np.pi * 9 * s) * np.exp(-s * 4)) / SR) * np.exp(-s * 4), g_, 0, .2)
def skid(t0, d=1.4, g_=.06):
    n = int(d * SR); s = np.arange(n) / SR; m.place(t0, (np.sin(2 * np.pi * np.cumsum(900 - 180 * s / d + 25 * np.sin(2 * np.pi * 23 * s)) / SR) * .5 + bp(m.noise(n), 700, 2600)) * np.minimum(1, s / .08) * np.minimum(1, (d - s) / .4), g_, 0, .3)
def click(t0, g_=.14):
    n = int(.05 * SR); s = np.arange(n) / SR; m.place(t0, bp(m.noise(n), 1500, 6000) * np.exp(-s * 120), g_); m.place(t0 + .045, bp(m.noise(n), 900, 4000) * np.exp(-s * 90), g_ * .8)
def clatter(t0, n_=7, g_=.12):
    rr = np.random.default_rng(int(t0 * 10))
    for k in range(n_): q = t0 + rr.random() * .5; n = int(.12 * SR); s = np.arange(n) / SR; f0 = 500 + 1500 * rr.random(); m.place(q, np.sin(2 * np.pi * f0 * s) * np.exp(-s * 45) + bp(m.noise(n), 1000, 5000) * np.exp(-s * 80) * .6, g_ * (.5 + .5 * rr.random()), rr.random() - .5)
def meow(t0, g_=.06):
    n = int(.6 * SR); s = np.arange(n) / SR; f0 = 520 + 260 * np.sin(np.pi * s / .6); y = sum(np.sin(2 * np.pi * np.cumsum(f0 * k) / SR) / k for k in (1, 2, 3, 4)); m.place(t0, y * np.sin(np.pi * s / .6) ** .7, g_, .2, .2)
def gasp(t0, g_=.05):
    for k in range(6): n = int(.7 * SR); s = np.arange(n) / SR; m.place(t0 + k * .05, bp(m.noise(n), 300, 3000) * np.exp(-s * 2.2), g_)
# kitchen
clatter(3.8, 8, .06); clatter(17.35, 14, .16); m.thump(17.42, .35); splash(17.45, .18); meow(13.6); meow(17.2); click(2.04, .10)
m.whoosh(g("c03", 1.0), .6, .12, 300, 4000)
for k in range(5): click(g("c04", wt("c04_n1", "gravity") - .1 + k * .52), .10)
pop(g("c04", wt("c04_n2", "floats") - .1), .25)
m.whoosh(g("c05", wt("c05_n1", "Earth") - .1), 1.6, .07, 200, 2500); m.whoosh(g("c05", wt("c05_n1", "but") - .05), 1.2, .06, 300, 3000)
# backyard: ONE fall, one splash
tf = np.sqrt(2 * 4.55 / 9.8); m.whoosh(g("c09", .1), tf, .16, 300, 3500); splash(g("c09", .12 + tf), .34)
for k in range(3): pop(g("c07", wt("c07_n1", "full") - .1 + .3 + k * .42), .16)
pop(g("c09", lt("c09_maya1") - .1), .2); m.chime(g("c09", wt("c09_n2", "Maya", 1) + .1), 84, .06)
# sick
m.whoosh(g("c10", wt("c10_n1", "Deep") - .1), .9, .10, 200, 3000); clatter(g("c10", wt("c10_n1", "tiny")), 10, .05)
# traffic
skid(g("c11", lt("c11_n2") - .2), 2.4, .05); skid(g("c12", wt("c12_n1", "slides") - .1), 1.9, .07)
for k in range(4): m.place(g("c12", wt("c12_n1", "slides") + k * .5), np.sin(2 * np.pi * 330 * np.arange(int(.32 * SR)) / SR) * .6 + np.sin(2 * np.pi * 415 * np.arange(int(.32 * SR)) / SR) * .4, .035)
pop(g("c12", wt("c12_n1", "But") + .8), .2)
# school
for k in range(7): click(g("c13", wt("c13_coach1", "Yes") - .1 + .06 * k), .10)
for k in range(2): click(g("c13", wt("c13_n1", "Backpacks") + .1 + .2 * k), .13)
m.whoosh(g("c14", wt("c14_n1", "lighting") - .4), .5, .10, 800, 6000); m.whoosh(g("c14", wt("c14_n1", "stomach")), .5, .08, 300, 1800)
# gym
for k in range(9): m.thump(g("c15", .3 + k * .51), .07)
gasp(g("c15", 10.9)); m.whoosh(g("c17", wt("c17_n1", "comes") + .1), 1.7, .22, 250, 3000); tl = wt("c17_n1", "comes") + .1 + np.sqrt(2 * (13.85 - .75) / 9.8); m.thump(g("c17", tl), .45); boing(g("c17", tl)); boing(g("c17", tl + 1.15), .12); boing(g("c17", tl + 2.14), .08)
for k in range(11): m.thump(g("c16", wt("c16_coach1", "Every") + .4 + .12 * k), .10)
# night
m.whoosh(g("c19", wt("c19_n1", "gravity") + .45), .62, .14, 300, 3000); m.thump(g("c19", wt("c19_n1", "gravity") + .45 + .6), .35); boing(g("c19", wt("c19_n1", "gravity") + 1.05), .08)
for k in range(4): click(g("c20", wt("c20_n1", "You", 1) + .8 + .45 * k), .13)
m.thump(g("c20", wt("c20_n2", "get") + .6), .3)
# water
splash(g("c21", 2.2), .10); splash(g("c22", wt("c22_n1", "out") + .9 + 1.15), .28)
for k in range(8): pop(g("c21", wt("c21_n2", "pulls") + .15 * k), .06)
# space
m.place(g("c23", wt("c23_n1", "five") - .1), np.sin(2 * np.pi * np.cumsum(np.linspace(900, 120, int(.35 * SR))) / SR) * np.exp(-np.arange(int(.35 * SR)) / SR * 9), .16); m.whoosh(g("c23", lt("c23_n2") + 9.0), 2.2, .10, 200, 2500); m.whoosh(g("c23", wt("c23_n2", "And")), 1.6, .07, 200, 2000)
for k in range(8): pop(g("c25", wt("c25_n1", "pop") + .05 * ((k * 3) % 8)), .13)
pop(g("c25", wt("c25_n1", "Only") + .85), .25)
# new normal + game
click(g("c26", wt("c26_n1", "Every", 1)), .12); clatter(g("c26", wt("c26_n1", "Every", 1) + .6), 8, .05); m.whoosh(g("c27", wt("c27_n2", "push") - .05), .7, .12, 300, 4000); m.thump(g("c27", wt("c27_n2", "before") + 1.5), .3); boing(g("c27", wt("c27_n2", "She") + .1), .14)
for k in range(10): click(g("c26", .1 + k * .12), .05)
# rescue
for k in range(3): m.whoosh(g("c28", 1.8 + 1.3 * k), .8, .05, 300, 1800)
gasp(SF.GZ + .1, .04); m.whoosh(SF.LET, 1.2, .09, 300, 2600); m.whoosh(SF.PUSH - .05, 1.0, .20, 250, 4500); m.thump(SF.PUSH, .3)
click(g("c31", wt("c31_n1", "Then")), .10); m.thump(SF.CATCH, .25)
tf = np.sqrt(2 * (SF.HEND[2] - .34) / 9.8); m.whoosh(SF.GB, tf, .18, 300, 3500); n = int(1.0 * SR); s = np.arange(n) / SR; m.place(SF.GB + tf, bp(m.noise(n), 500, 5000) * np.exp(-s * 6), .30, 0, .2); m.thump(SF.GB + tf, .4); clatter(SF.GB + tf + .1, 10, .04)
m.thump(g("c33", wt("c33_n2", "six") - .1), .35); pop(g("c33", wt("c33_n3", "illegal") - .2), .2); m.thump(g("c34", wt("c34_n1", "grab") - .1), .28)
# ---------------------------------------------------------------- original score: plucks + pad, mood per section
def pluck(f, d=0.5):
    n = int(d * SR); s = np.arange(n) / SR; y = sum(a * np.sin(2 * np.pi * f * k * s) * np.exp(-s * (6 + 3 * k)) for k, a in ((1, 1), (2, .4), (3, .2)))
    return y * np.minimum(1, s / 0.004)
def pad(ch, a, b, g):
    n = int((b - a) * SR); s = np.arange(n) / SR; y = sum(np.sin(2 * np.pi * hz(q) * s) for q in ch)
    m._mus(a, lp(y, 1100) * np.minimum(1, s / 1.0) * np.minimum(1, (b - a - s) / 1.0), g)
MOODS = {"play": ([60, 64, 67, 72, 71, 67, 64, 62, 60, 64, 69, 67, 65, 64, 62, 59], [[48, 55, 60], [45, 52, 57], [41, 48, 53], [43, 50, 55]], 0.28),
         "tense": ([57, 60, 64, 60, 59, 62, 65, 62, 57, 60, 64, 69, 68, 64, 62, 59], [[45, 52, 57], [46, 53, 58], [45, 52, 57], [44, 52, 56]], 0.3),
         "calm": ([64, 67, 71, 67, 62, 66, 69, 66, 60, 64, 67, 72, 71, 67, 64, 62], [[52, 59, 64], [50, 57, 62], [48, 55, 60], [47, 54, 59]], 0.45),
         "warm": ([67, 71, 74, 72, 71, 67, 69, 71, 72, 69, 67, 64, 66, 67, 69, 71], [[43, 50, 55], [48, 55, 60], [45, 52, 57], [50, 57, 62]], 0.42)}
SECT = [("c01", "c03", "play"), ("c04", "c06", "calm"), ("c07", "c09", "play"), ("c10", "c12", "tense"), ("c13", "c14", "play"), ("c15", "c17", "tense"),
        ("c18", "c20", "calm"), ("c21", "c22", "warm"), ("c23", "c25", "calm"), ("c26", "c27", "warm"), ("c28", "c32", "tense"), ("c33", "c34", "play")]
CO = {x["id"]: x for x in chap}
for a_id, b_id, mood in SECT:
    a = CO[a_id]["off"] + 0.2; b = CO[b_id]["off"] + CO[b_id]["dur"] - 0.2; mel, chs, step = MOODS[mood]
    k = 0; tt = a
    while tt < b - 0.3:
        if k % 2 == 0 or mood == "play": m._mus(tt, pluck(hz(mel[k % 16])), 0.03, 0.2 * (-1) ** k)
        if k % 4 == 0: m._mus(tt, pluck(hz(chs[(k // 8) % 4][0]), 0.7), 0.03)
        tt += step; k += 1
    tt = a; i = 0
    while tt < b - 0.5: pad(chs[i % 4], tt, min(b, tt + step * 8), 0.022); tt += step * 8; i += 1
m.render("/home/rasul/Desktop/Animations/longform25/gravity/out/audio25.wav")
print("TOTAL", round(TOTAL, 1))
