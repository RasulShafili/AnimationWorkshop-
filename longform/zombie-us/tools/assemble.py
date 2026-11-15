#!/usr/bin/env python3
"""Assemble the final cut: render chapter cards, mux every chapter with its wav, concat in order, write the YouTube
chapter list and exact subtitles (from SCRIPT.md text + the same timeline as src/Player.tsx).
  python3 tools/assemble.py            (expects out/cN_noaudio.mp4 and public/cN.wav for c1..c15)"""
import json, os, re, subprocess, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio import timeline, Z, SR, FPS, ROOT
os.chdir(ROOT)
CH = [f"c{i}" for i in range(1, 16)]
TITLES = {"c1": "Day 3, 2:14 AM", "c2": "A normal Tuesday", "c3": "How it started", "c4": "Patient zero", "c5": "The math of the end",
  "c6": "Day 2: The exodus", "c7": "The fortress", "c8": "Day 5: The rules", "c9": "Day 7: The knock", "c10": "Why they attack",
  "c11": "Day 14: The radio", "c12": "Day 21: The cost", "c13": "The road north", "c14": "Day 30: The safe zone", "c15": "Tent 48"}
CARD = 54
run = lambda *a: subprocess.run(list(a), check=True, stdin=subprocess.DEVNULL)

# card audio: a low hit + soft whoosh (original)
m = Z(CARD, seed=5); m.whoosh(0.0, .7, .12); m.thump(0.05, .5, 40); m.render("public/card.wav")
segs = []
for i, ch in enumerate(CH):
    if i > 0:
        out = f"out/card_{i}.mp4"
        if not os.path.exists(out):
            run("npx", "remotion", "render", "src/index.ts", "ChapterCard", "out/card_tmp.mp4", "--muted", f"--props={json.dumps({'num': i, 'title': TITLES[ch]})}", "--log=error")
            run("ffmpeg", "-v", "error", "-y", "-i", "out/card_tmp.mp4", "-i", "public/card.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", out)
        segs.append(("card", ch, out, CARD))
    T, end = timeline(ch)
    out = f"out/{ch}.mp4"
    run("ffmpeg", "-v", "error", "-y", "-i", f"out/{ch}_noaudio.mp4", "-i", f"public/{ch}.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", out)
    segs.append(("ch", ch, out, end))
open("out/concat.txt", "w").write("".join(f"file '{os.path.basename(s[2])}'\n" for s in segs))
run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/concat.txt", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "out/zombie-us_full.mp4")

# chapters + subtitles
S = {f"{c}_{i}": (w, t) for c, i, w, t in re.findall(r"- \[(c\d+)\.(\w+)\] (\w+)[^:]*: (.*)", open("SCRIPT.md").read())}
fmt = lambda f: f"{int(f // 30 // 3600):02d}:{int(f // 30 % 3600 // 60):02d}:{int(f // 30 % 60):02d},{int(round((f % 30) / 30 * 1000)) % 1000:03d}"
mmss = lambda f: f"{int(f // 30 // 60)}:{int(f // 30 % 60):02d}"
t0 = 0; chapters = []; cues = []
for kind, ch, _, n in segs:
    if kind == "ch":
        chapters.append(f"{mmss(t0 - (CARD if ch != 'c1' else 0))} {TITLES[ch]}")
        T, _ = timeline(ch)
        for k, b in T.items():
            if f"{ch}_{k}" in S: cues.append((t0 + b["line"], t0 + b["line"] + b["dur"], S[f"{ch}_{k}"][1].replace("…", "...")))
    t0 += n
open("out/chapters.txt", "w").write("\n".join(chapters) + "\n")
srt = []
for j, (a, b, txt) in enumerate(cues, 1):
    words = txt.split(); lines = [txt] if len(txt) <= 42 else [" ".join(words[:len(words) // 2]), " ".join(words[len(words) // 2:])]
    if len(txt) > 84:   # long lines: split into two cues by time
        h = len(words) // 2; mid = a + (b - a) * h / len(words)
        srt.append((a, mid, " ".join(words[:h]))); srt.append((mid, b, " ".join(words[h:])))
    else: srt.append((a, b, "\n".join(lines)))
open("out/subtitles_en.srt", "w").write("".join(f"{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(srt, 1)))
print("total", mmss(t0), f"({t0 / 30:.1f}s)"); print(open("out/chapters.txt").read())
