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
          open(f"{D}/out/global.json", "w"), indent=1)
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
wavfile.write(f"{D}/out/vo_only.wav", SR, (vo_only / (np.abs(vo_only).max() + 1e-9) * 30000).astype(np.int16))
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
    for ev in x["J"].get("events", []):
        if ev[0] == "zero":
            za, zb = x["off"] + max(0.0, ev[1]), x["off"] + min(ev[2], x["dur"])
            if zb - za > 0.3: zero_g(za, zb)
            if ev[2] < x["dur"] - 0.2: m.thump(x["off"] + ev[2] + 0.35, 0.35)
# special beats
G_ = {l["id"]: (l["t0"], l["t1"]) for l in json.load(open(f"{D}/out/global.json"))["lines"]}
m.thump(G_["c09_n1"][0] + 0.6, 0.3)                                        # splash into the paddling pool
for k in range(3): m.whoosh(G_["c09_n1"][0] + 0.62 + k * 0.05, 0.5, 0.05, 1500, 8000)
for k in range(6): m.place(G_["c17_n1"][0] + 1.2 + k * 0.05, bp(m.noise(int(0.8 * SR)), 300, 3000) * np.exp(-np.arange(int(0.8 * SR)) / SR * 2), 0.05)   # gym gasp
for k in range(4): m.place(G_["c12_n1"][0] + 1.0 + k * 0.6, np.sin(2 * np.pi * 330 * np.arange(int(0.35 * SR)) / SR) * 0.6 + np.sin(2 * np.pi * 415 * np.arange(int(0.35 * SR)) / SR) * 0.4, 0.04)   # horns
m.thump(G_["c17_n1"][0] + 2.8, 0.3); m.thump(G_["c32_n1"][0] + 1.85, 0.35)                                       # sandbox crunch
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
m.render(f"{D}/out/audio_all.wav")
print("TOTAL", round(TOTAL, 1))
