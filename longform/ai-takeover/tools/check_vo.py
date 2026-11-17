#!/usr/bin/env python3
"""Whisper small.en on every generated line; print the ones whose words differ from SCRIPT.md (word-level ratio)."""
import re, sys, glob, subprocess, difflib, numpy as np
from faster_whisper import WhisperModel
S = {f"{c}_{i}": t for c, i, w, t in re.findall(r"- \[(c\d+)\.(\w+)\] (\w+)[^:]*: (.*)", open("SCRIPT.md").read())}
norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("-", " ")).split()
m = WhisperModel("small.en", device="cpu", compute_type="int8")
pre = sys.argv[1:] or ["c"]
for f in sorted(glob.glob("vo/c*_*.wav")):
    n = f[3:-4]
    if n.endswith(".orig") or n not in S or not any(n.startswith(p + "_") or p == "c" for p in pre): continue
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    got = " ".join(s.text for s in m.transcribe(a, language="en")[0])
    r = difflib.SequenceMatcher(None, norm(S[n]), norm(got)).ratio()
    print(f"{'OK ' if r > .85 else 'BAD'} {r:.2f} {n:12s} | {got.strip()}" if r <= .85 or "-v" in sys.argv else f"OK  {r:.2f} {n}", flush=True)
