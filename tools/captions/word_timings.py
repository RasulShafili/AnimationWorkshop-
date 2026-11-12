#!/usr/bin/env python3
"""Word timings for burned-in captions, from a narration wav and its known text (no ASR needed).

  python3 word_timings.py vo/l0.wav "What if your speed doubled every two seconds?" [--at FRAME] [--fps 30] >> words.json

Finds where speech starts/ends and the pauses inside it (RMS envelope), splits the text at punctuation to match the
pauses when the counts agree, and spreads the words inside each stretch by their syllable weight.
Output: JSON list [{"w": "speed", "s": start_frame, "e": end_frame}, ...] (frames are absolute when --at is given).
If whisper is installed (tools/whisper-venv), word_timings_whisper.py is more exact; this is the fallback.
"""
import json, re, sys
import numpy as np
from scipy.io import wavfile

args = sys.argv[1:]
def opt(n, d, c=float):
    if n in args: i = args.index(n); v = c(args[i + 1]); del args[i:i + 2]; return v
    return d
at, fps = opt("--at", 0), opt("--fps", 30)
wav, text = args[0], args[1]
sr, y = wavfile.read(wav); y = y.astype(np.float64); y = y.mean(1) if y.ndim > 1 else y; y /= (np.abs(y).max() + 1e-9)
hop = int(sr * 0.01); rms = np.array([np.sqrt((y[i:i + hop] ** 2).mean()) for i in range(0, len(y) - hop, hop)])
on = rms > max(0.02, rms.max() * 0.06)
# speech stretches separated by pauses >= 140 ms
segs, i = [], 0
while i < len(on):
    if on[i]:
        j = i
        while j < len(on) and (on[j] or (j + 14 < len(on) and on[j:j + 14].any())): j += 1
        segs.append([i * 0.01, j * 0.01]); i = j
    else: i += 1
words = text.split()
syl = lambda w: max(1, len(re.findall(r"[aeiouy]+", w.lower())) + (1 if re.search(r"\d", w) else 0))
# phrases = words up to punctuation; use them if they match the pauses, else one stretch for everything
phrases, cur = [], []
for w in words:
    cur.append(w)
    if re.search(r"[,.!?;:…]$", w): phrases.append(cur); cur = []
if cur: phrases.append(cur)
if len(phrases) != len(segs): phrases, segs = [words], [[segs[0][0], segs[-1][1]]] if segs else [[0, len(y) / sr]]
out = []
for ph, (s0, s1) in zip(phrases, segs):
    wts = [syl(w) + 0.3 for w in ph]; tot = sum(wts); t = s0
    for w, k in zip(ph, wts):
        d = (s1 - s0) * k / tot
        out.append({"w": w, "s": round(at + t * fps, 1), "e": round(at + (t + d) * fps, 1)}); t += d
print(json.dumps(out))
