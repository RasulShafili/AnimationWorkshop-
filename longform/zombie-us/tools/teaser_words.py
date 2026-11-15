#!/usr/bin/env python3
"""Word timings for a teaser clip from the real timeline (no Whisper): words of each SCRIPT.md line are spread over
the line's duration by character length. python3 tools/teaser_words.py c1 [start_frame] > src/teaser_words.json"""
import json, re, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from audio import timeline
ch = sys.argv[1]; off = int(sys.argv[2]) if len(sys.argv) > 2 else 0
S = {i: t for c, i, w, t in re.findall(r"- \[(c\d+)\.(\w+)\] (\w+)[^:]*: (.*)", open("SCRIPT.md").read()) if c == ch}
T, _ = timeline(ch); out = []
for k, b in T.items():
    if k not in S: continue
    words = S[k].replace("…", "...").split(); L = sum(len(w) + 1 for w in words); t = b["line"] - off
    for w in words:
        d = b["dur"] * (len(w) + 1) / L; out.append({"w": w, "s": round(t, 1), "e": round(t + d, 1)}); t += d
print(json.dumps(out))
