#!/usr/bin/env python3
"""Chapter audio: voices (thoughts = same voice + 'inside the head' echo), one original mood cue, shimmer on every
thought ring, pop on every sign, truck whoosh; loudnorm −14 LUFS via audio_lib.Mix.render.
  python3 tools/audio_ch.py c1 [c2 …]   (reads out/<c>_timeline.json written by build.py)"""
import sys, json, numpy as np
sys.path.insert(0, "/home/rasul/Desktop/Animations/longform/ai-takeover/tools")
from audio_lib import Mix, SR, hz, lp, bp, hp
from scipy.io import wavfile
D = "/home/rasul/Desktop/Animations/longform3d/thoughts"
MOOD = {"c1": "playful", "c2": "playful", "c3": "playful", "c4": "playful", "c4b": "busy", "c5": "shy", "c5b": "sad", "c6": "comic",
        "c7": "tense", "c7b": "warm", "c8": "hollow", "c8b": "warm", "c9": "dream", "c9b": "hope", "c10": "action", "c11": "sad",
        "c11b": "warm", "c12": "tender", "c13": "musicbox"}
def tone(f, d, dec=3.0, partials=((1, 1), (3.01, .22))):
    n = int(d * SR); s = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * p * s) for p, a in partials) * np.exp(-s * dec)
def music(m, mood, a, b):
    """original cues only (simple chords + our own little melodies)"""
    chords = {"playful": [[60, 64, 67], [65, 69, 72], [62, 65, 69], [67, 71, 74]], "shy": [[64, 67, 71], [60, 64, 67], [57, 60, 64], [62, 66, 69]],
              "sad": [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], "comic": [[60, 64, 67], [62, 65, 69], [64, 67, 71], [65, 69, 72]],
              "tense": [[57, 60, 64], [58, 62, 65], [57, 60, 64], [56, 59, 64]], "warm": [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]],
              "hollow": [[50, 57, 62], [48, 55, 60], [46, 53, 58], [48, 55, 60]], "dream": [[62, 66, 69, 73], [59, 62, 66, 69], [55, 59, 62, 66], [57, 61, 64, 67]],
              "hope": [[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]], "action": [[52, 55, 59], [53, 57, 60], [50, 53, 57], [52, 56, 59]],
              "tender": [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]], "musicbox": [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]],
              "busy": [[60, 64, 67], [62, 65, 69]]}[mood]
    m.score([[n for n in c] for c in chords], bar=2.4 if mood in ("playful", "comic", "action", "busy") else 3.2, gain=.022, piano=mood in ("sad", "tender", "hollow", "shy"), start=a, end=b)
    mel = {"playful": ([72, 76, 79, 76, 77, 74, 72, 71], .3), "comic": ([72, 71, 72, 76, 74, 72, 71, 67], .26), "musicbox": ([76, 79, 81, 79, 76, 74, 72, 74], .45),
           "hope": ([74, 76, 78, 81, 78, 76], .55), "dream": ([81, 78, 76, 73, 76, 78], .6), "warm": ([72, 74, 76, 79, 76, 74], .5)}.get(mood)
    if mel:
        t = a + .4; k = 0
        while t < b - .8: m._mus(t, tone(hz(mel[0][k % len(mel[0])]), 1.0), .03, .2 * (-1) ** k); t += mel[1]; k += 1
    if mood == "action":
        t = a; k = 0
        while t < b: m.thump(t, .22, 50 if k % 2 == 0 else 70); t += .3; k += 1
def thought_fx(y):
    """inside-the-head: soft low-pass + two short echoes"""
    out = np.copy(y); d1, d2 = int(.09 * SR), int(.19 * SR)
    out[d1:] += y[:-d1] * .32; out[d2:] += y[:-d2] * .14; return lp(out, 6000) * .95
for cid in sys.argv[1:]:
    J = json.load(open(f"{D}/out/{cid}_timeline.json")); END = J["end"]; m = Mix(int(END * 30) + 2, seed=hash(cid) % 99)
    for ln in J["lines"]:
        t = ln["t0"]
        for f in ln["files"]:
            sr, y = wavfile.read(f"{D}/vo16/{f}"); y = y.astype(float) / 32768
            y = np.interp(np.arange(int(len(y) * SR / sr)) * sr / SR, np.arange(len(y)), y)
            if ln["thought"]: y = thought_fx(y)
            i = int(t * SR); j = min(m.N, i + len(y)); m.vo[i:j] += y[:j - i]; t += len(y) / SR + .15
    for ev in J["events"]:
        if ev[0] == "shimmer":
            for k, p in enumerate((88, 92, 95, 100)): m.place(ev[1] - .05 + k * .04, tone(hz(p), .9, 5, ((1, 1),)), .05, .3 * (-1) ** k, .8)
        elif ev[0] == "pop":
            n = int(.09 * SR); s = np.arange(n) / SR; m.place(ev[1], np.sin(2 * np.pi * np.cumsum(900 + 1400 * np.exp(-s * 60)) / SR) * np.exp(-s * 45), .3, 0, .3)
        elif ev[0] == "truck":
            m.whoosh(ev[1] + 1.2, 2.4, .35, 80, 1500); m.thump(ev[1] + 2.2, .2, 40)
    music(m, MOOD.get(cid, "warm"), 0, END)
    m.render(f"{D}/out/{cid}.wav")
