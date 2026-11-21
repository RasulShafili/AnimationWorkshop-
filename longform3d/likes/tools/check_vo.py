#!/usr/bin/env python3
"""Whisper small.en on every voice file; print lines whose words differ from the job text (word ratio < 0.85)."""
import re, json, subprocess, difflib, numpy as np
from faster_whisper import WhisperModel
norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("-", " ").replace("|", " ")).split()
m = WhisperModel("small.en", device="cpu", compute_type="int8"); bad = 0
for j in json.load(open("vo/jobs_all.json")):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", j["out"], "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    heard = " ".join(s.text for s in m.transcribe(a, language="en")[0]); r = difflib.SequenceMatcher(None, norm(j["text"]), norm(heard)).ratio()
    if r < 0.85: bad += 1; print(f"{r:.2f} {j['out']}\n   want: {j['text'][:110]}\n   got:  {heard.strip()[:110]}", flush=True)
print("CHECKED", bad, "suspicious")
